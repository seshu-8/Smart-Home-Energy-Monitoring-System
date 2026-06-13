/*
 * Smart Home Energy Monitoring System
 * =====================================
 * Hardware  : ESP32 (38-pin DevKit)
 * Sensors   : ACS712-30A (current), ZMPT101B (voltage)
 * Display   : 0.96" OLED SSD1306 (I2C)
 * Alert     : Buzzer + Red LED
 * Cloud     : ThingSpeak via Wi-Fi
 * IDE       : Arduino IDE 2.x
 *
 * Libraries required (install via Library Manager):
 *   - Adafruit SSD1306        (OLED display)
 *   - Adafruit GFX Library    (graphics)
 *   - ThingSpeak              (cloud upload)
 *   - WiFi                    (built-in for ESP32)
 *
 * Wiring Summary:
 *   ACS712 OUT  → GPIO34 (ADC1_CH6 — analog input)
 *   ZMPT101B OUT→ GPIO35 (ADC1_CH7 — analog input)
 *   OLED SDA    → GPIO21
 *   OLED SCL    → GPIO22
 *   BUZZER +    → GPIO26
 *   RED LED     → GPIO27 (via 330Ω resistor)
 *   GREEN LED   → GPIO25 (via 330Ω resistor)
 *   RELAY IN    → GPIO32
 */

#include <WiFi.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include "ThingSpeak.h"

// ─────────────────────────────────────────────────────────────────
// CONFIGURATION — edit these values before uploading
// ─────────────────────────────────────────────────────────────────
const char* WIFI_SSID       = "Your_WiFi_SSID";
const char* WIFI_PASSWORD   = "Your_WiFi_Password";
unsigned long CHANNEL_ID    = 0;           // ThingSpeak Channel ID
const char*   WRITE_API_KEY = "YOUR_API_KEY"; // ThingSpeak Write API Key

// ─────────────────────────────────────────────────────────────────
// PIN DEFINITIONS
// ─────────────────────────────────────────────────────────────────
#define PIN_CURRENT   34    // ACS712 analog output
#define PIN_VOLTAGE   35    // ZMPT101B analog output
#define PIN_BUZZER    26
#define PIN_LED_RED   27
#define PIN_LED_GREEN 25
#define PIN_RELAY     32

// ─────────────────────────────────────────────────────────────────
// SENSOR CALIBRATION CONSTANTS
// ─────────────────────────────────────────────────────────────────
// ACS712-30A: sensitivity = 66 mV/A, midpoint at VCC/2 = 1650mV
// ESP32 ADC: 12-bit → 0–4095, reference voltage 3.3V
#define ACS712_SENSITIVITY  0.066   // V/A for 30A variant
#define ACS712_MIDPOINT     1.65    // V (VCC/2 with 3.3V supply)
#define ADC_REF_VOLTAGE     3.3     // V
#define ADC_RESOLUTION      4096    // 12-bit
#define SAMPLES_PER_READ    500     // Number of samples to average (noise reduction)

// ZMPT101B calibration factor — adjust based on your module's trim pot
// Measure actual voltage with multimeter and adjust until values match
#define VOLTAGE_CALIBRATION 0.5265  // Empirically determined

// Power factor for typical household loads
#define POWER_FACTOR 0.9

// Cost per kWh in INR (Hyderabad TSSPDCL domestic rate)
#define COST_PER_KWH 7.0

// Alert threshold: 3000W = 3kW
#define POWER_THRESHOLD_W 3000.0

// ─────────────────────────────────────────────────────────────────
// OLED DISPLAY CONFIG
// ─────────────────────────────────────────────────────────────────
#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64
#define OLED_RESET   -1  // No reset pin (connected to ESP32 EN)
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

// ─────────────────────────────────────────────────────────────────
// GLOBAL STATE
// ─────────────────────────────────────────────────────────────────
WiFiClient wifiClient;

float voltage_V       = 0.0;
float current_A       = 0.0;
float power_W         = 0.0;
float energy_Wh       = 0.0;
float cost_INR        = 0.0;
bool  highPowerAlert  = false;

unsigned long lastThingSpeakUpdate = 0;
unsigned long lastCalcTime         = 0;
const long    THINGSPEAK_INTERVAL  = 15000;  // 15 sec (free tier limit)
const long    CALC_INTERVAL        = 1000;   // 1 sec between readings


// ═════════════════════════════════════════════════════════════════
// SETUP
// ═════════════════════════════════════════════════════════════════
void setup() {
  Serial.begin(115200);
  delay(500);
  Serial.println("\n=== Smart Home Energy Monitor ===");

  // Pin modes
  pinMode(PIN_BUZZER,    OUTPUT);
  pinMode(PIN_LED_RED,   OUTPUT);
  pinMode(PIN_LED_GREEN, OUTPUT);
  pinMode(PIN_RELAY,     OUTPUT);

  // Safe initial states
  digitalWrite(PIN_RELAY,     HIGH);  // Relay NC = power ON by default
  digitalWrite(PIN_LED_GREEN, HIGH);  // Green ON = system running
  digitalWrite(PIN_LED_RED,   LOW);
  digitalWrite(PIN_BUZZER,    LOW);

  // OLED init
  if (!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) {
    Serial.println("OLED not found — check wiring");
  } else {
    showSplashScreen();
  }

  // Wi-Fi connect
  connectWiFi();

  // ThingSpeak init
  ThingSpeak.begin(wifiClient);

  Serial.println("Setup complete. Starting monitoring loop...\n");
}


// ═════════════════════════════════════════════════════════════════
// MAIN LOOP
// ═════════════════════════════════════════════════════════════════
void loop() {
  unsigned long now = millis();

  // ── Read & calculate every CALC_INTERVAL ──────────────────────
  if (now - lastCalcTime >= CALC_INTERVAL) {
    lastCalcTime = now;

    voltage_V = readVoltage();
    current_A = readCurrent();
    power_W   = voltage_V * current_A * POWER_FACTOR;

    // Accumulate energy (P × Δt in hours)
    float dt_hours = (float)CALC_INTERVAL / 3600000.0;
    energy_Wh += power_W * dt_hours;
    cost_INR   = (energy_Wh / 1000.0) * COST_PER_KWH;

    // Alert check
    checkAlert(power_W);

    // Serial monitor output
    Serial.printf("V=%.2fV  I=%.3fA  P=%.2fW  E=%.4fWh  ₹%.4f  %s\n",
                  voltage_V, current_A, power_W, energy_Wh, cost_INR,
                  highPowerAlert ? "⚠️ HIGH" : "✅ OK");

    // OLED refresh
    updateDisplay();
  }

  // ── ThingSpeak push every 15 sec ──────────────────────────────
  if (now - lastThingSpeakUpdate >= THINGSPEAK_INTERVAL) {
    lastThingSpeakUpdate = now;
    if (WiFi.status() == WL_CONNECTED) {
      pushToThingSpeak();
    } else {
      Serial.println("[WiFi] Disconnected — attempting reconnect...");
      connectWiFi();
    }
  }
}


// ═════════════════════════════════════════════════════════════════
// SENSOR READING FUNCTIONS
// ═════════════════════════════════════════════════════════════════

/**
 * Read RMS current from ACS712.
 * Takes SAMPLES_PER_READ readings, computes RMS for AC accuracy.
 */
float readCurrent() {
  float sumSquares = 0.0;
  for (int i = 0; i < SAMPLES_PER_READ; i++) {
    int raw = analogRead(PIN_CURRENT);
    float voltage_at_pin = (raw / (float)ADC_RESOLUTION) * ADC_REF_VOLTAGE;
    float centered       = voltage_at_pin - ACS712_MIDPOINT;
    float instantCurrent = centered / ACS712_SENSITIVITY;
    sumSquares += instantCurrent * instantCurrent;
  }
  float rms = sqrt(sumSquares / SAMPLES_PER_READ);
  return (rms < 0.05) ? 0.0 : rms;  // Dead-band: ignore noise < 50mA
}

/**
 * Read RMS voltage from ZMPT101B.
 * Similar RMS sampling approach.
 */
float readVoltage() {
  float sumSquares = 0.0;
  for (int i = 0; i < SAMPLES_PER_READ; i++) {
    int raw = analogRead(PIN_VOLTAGE);
    float centered = (raw - ADC_RESOLUTION / 2.0);
    sumSquares += centered * centered;
  }
  float rms = sqrt(sumSquares / SAMPLES_PER_READ);
  return rms * VOLTAGE_CALIBRATION;
}


// ═════════════════════════════════════════════════════════════════
// ALERT & SAFETY FUNCTIONS
// ═════════════════════════════════════════════════════════════════
void checkAlert(float power) {
  if (power > POWER_THRESHOLD_W) {
    highPowerAlert = true;
    digitalWrite(PIN_LED_RED,   HIGH);
    digitalWrite(PIN_LED_GREEN, LOW);
    // Buzzer beep pattern: 3 short beeps
    for (int b = 0; b < 3; b++) {
      digitalWrite(PIN_BUZZER, HIGH); delay(100);
      digitalWrite(PIN_BUZZER, LOW);  delay(100);
    }
    // OPTIONAL: Trip relay if extreme overload (>6kW)
    if (power > POWER_THRESHOLD_W * 2.0) {
      Serial.println("🚨 OVERLOAD! Tripping relay...");
      digitalWrite(PIN_RELAY, LOW);   // Cut power
      delay(2000);
      digitalWrite(PIN_RELAY, HIGH);  // Restore after 2s
    }
  } else {
    highPowerAlert = false;
    digitalWrite(PIN_LED_RED,   LOW);
    digitalWrite(PIN_LED_GREEN, HIGH);
    digitalWrite(PIN_BUZZER,    LOW);
  }
}


// ═════════════════════════════════════════════════════════════════
// OLED DISPLAY FUNCTIONS
// ═════════════════════════════════════════════════════════════════
void showSplashScreen() {
  display.clearDisplay();
  display.setTextSize(1);
  display.setTextColor(SSD1306_WHITE);
  display.setCursor(10, 10);
  display.println("Smart Energy");
  display.setCursor(10, 22);
  display.println("Monitor v1.0");
  display.setCursor(10, 38);
  display.println("Initializing...");
  display.display();
  delay(2000);
}

void updateDisplay() {
  display.clearDisplay();
  display.setTextSize(1);
  display.setTextColor(SSD1306_WHITE);

  // Header
  display.setCursor(0, 0);
  display.println(highPowerAlert ? "! HIGH POWER !" : "Energy Monitor");

  // Values
  display.setCursor(0, 12);
  display.printf("V: %.1f V", voltage_V);
  display.setCursor(64, 12);
  display.printf("I: %.2f A", current_A);

  display.setCursor(0, 24);
  display.printf("P: %.1f W", power_W);
  display.setCursor(64, 24);
  display.printf("PF:%.2f", POWER_FACTOR);

  display.setCursor(0, 36);
  display.printf("E: %.4f Wh", energy_Wh);

  display.setCursor(0, 48);
  display.printf("Cost: Rs.%.4f", cost_INR);

  display.display();
}


// ═════════════════════════════════════════════════════════════════
// WI-FI & THINGSPEAK
// ═════════════════════════════════════════════════════════════════
void connectWiFi() {
  Serial.printf("Connecting to %s ", WIFI_SSID);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  int tries = 0;
  while (WiFi.status() != WL_CONNECTED && tries < 20) {
    delay(500); Serial.print(".");
    tries++;
  }
  if (WiFi.status() == WL_CONNECTED) {
    Serial.printf("\n✅ Connected. IP: %s\n", WiFi.localIP().toString().c_str());
  } else {
    Serial.println("\n⚠️  WiFi failed — running offline");
  }
}

void pushToThingSpeak() {
  ThingSpeak.setField(1, voltage_V);
  ThingSpeak.setField(2, current_A);
  ThingSpeak.setField(3, power_W);
  ThingSpeak.setField(4, energy_Wh);
  ThingSpeak.setField(5, cost_INR);
  ThingSpeak.setField(6, (int)highPowerAlert);

  int status = ThingSpeak.writeFields(CHANNEL_ID, WRITE_API_KEY);
  if (status == 200) {
    Serial.println("[ThingSpeak] ✅ Data uploaded");
  } else {
    Serial.printf("[ThingSpeak] ❌ Error: %d\n", status);
  }
}
