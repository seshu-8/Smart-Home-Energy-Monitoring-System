/*
 * ============================================================
 *  Smart Home Energy Monitoring System — WOKWI SIMULATION
 * ============================================================
 *  Platform  : Wokwi (https://wokwi.com)
 *  Board     : ESP32 DevKit V1 (38-pin)
 *  ThingSpeak: Channel ID 3406670
 *
 *  FIELD MAPPING (matches your ThingSpeak channel exactly):
 *    Field 1 → Voltage (V)
 *    Field 2 → Current (A)
 *    Field 3 → Active Power (W)
 *    Field 4 → Energy Consumed (kWh)
 *    Field 5 → Accumulated Cost (INR)
 *    Field 6 → Overload Alert Status (0=Normal, 1=High, 2=Overload)
 *
 *  WOKWI COMPONENTS (defined in diagram.json):
 *    - ESP32 DevKit V1
 *    - Potentiometer 1 → GPIO34 (simulates ACS712 current sensor)
 *    - Potentiometer 2 → GPIO35 (simulates ZMPT101B voltage sensor)
 *    - SSD1306 OLED 128x64 (I2C: SDA=GPIO21, SCL=GPIO22)
 *    - Red LED  → GPIO27 (alert indicator)
 *    - Green LED → GPIO25 (normal indicator)
 *    - Buzzer   → GPIO26
 *    - Push Button → GPIO33 (manual reset energy counter)
 *
 *  HOW TO USE IN WOKWI:
 *    1. Go to https://wokwi.com/projects/new/esp32
 *    2. Replace sketch.ino with this file
 *    3. Replace diagram.json with the provided diagram.json
 *    4. Press ▶ Start Simulation
 *    5. Rotate the potentiometers to simulate different loads
 *       - POT1 (GPIO34) = current sensor → turn right = more current
 *       - POT2 (GPIO35) = voltage sensor → keep ~mid for 230V
 *
 *  NOTE ON THINGSPEAK IN WOKWI:
 *    Wokwi supports simulated Wi-Fi. ThingSpeak pushes WILL work
 *    if you enter your real API key below. The serial monitor shows
 *    each push attempt and the ThingSpeak entry ID response.
 * ============================================================
 */

#include <WiFi.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

// ── ThingSpeak (no external library needed — raw HTTP) ───────
// Using raw HTTP GET avoids the ThingSpeak library version issues in Wokwi
WiFiClient client;

// ============================================================
//  ⚙️  CONFIGURATION — Edit these before running
// ============================================================
const char* WIFI_SSID      = "Wokwi-GUEST";   // Wokwi's built-in Wi-Fi (no password)
const char* WIFI_PASSWORD  = "";               // Leave empty for Wokwi
const char* TS_API_KEY     = "89QGJJWRNRINYJDI"; // Your Write API Key
const long  TS_CHANNEL_ID  = 3406670;

// Electricity tariff
const float COST_PER_KWH   = 7.0;   // ₹ per kWh (Hyderabad TSSPDCL)
const float POWER_FACTOR   = 0.9;
const float THRESHOLD_W    = 1500.0; // Alert threshold (W) — lowered for Wokwi pot range
const float OVERLOAD_W     = 3000.0; // Relay trip threshold

// ============================================================
//  PIN DEFINITIONS
// ============================================================
#define PIN_CURRENT    34   // Potentiometer 1 → simulates ACS712
#define PIN_VOLTAGE    35   // Potentiometer 2 → simulates ZMPT101B
#define PIN_BUZZER     26
#define PIN_LED_RED    27
#define PIN_LED_GREEN  25
#define PIN_BTN_RESET  33   // Push button: hold to reset energy counter

// ============================================================
//  OLED CONFIG
// ============================================================
#define SCREEN_W  128
#define SCREEN_H   64
#define OLED_ADDR 0x3C
Adafruit_SSD1306 oled(SCREEN_W, SCREEN_H, &Wire, -1);

// ============================================================
//  SIMULATION SCALING
// ============================================================
// Wokwi potentiometer: analogRead → 0..4095
// We map this to realistic household ranges:
//   Voltage: 200V – 240V   (POT2)
//   Current: 0A  – 25A    (POT1)
#define V_MIN  200.0
#define V_MAX  240.0
#define I_MIN    0.0
#define I_MAX   25.0

// ============================================================
//  GLOBAL STATE
// ============================================================
float voltage_V      = 0;
float current_A      = 0;
float power_W        = 0;
float energy_kWh     = 0;   // cumulative
float cost_INR       = 0;
int   alertStatus    = 0;   // 0=Normal 1=High 2=Overload

unsigned long lastCalcMs   = 0;
unsigned long lastPushMs   = 0;
unsigned long lastOledMs   = 0;
unsigned long sessionStartMs = 0;

const unsigned long CALC_INTERVAL_MS  =  1000;  // read sensors every 1s
const unsigned long PUSH_INTERVAL_MS  = 15000;  // push ThingSpeak every 15s
const unsigned long OLED_INTERVAL_MS  =  1000;  // refresh OLED every 1s

int   pushCount    = 0;
bool  wifiOK       = false;

// ============================================================
//  SETUP
// ============================================================
void setup() {
  Serial.begin(115200);
  delay(300);
  printBanner();

  // GPIO
  pinMode(PIN_BUZZER,    OUTPUT);
  pinMode(PIN_LED_RED,   OUTPUT);
  pinMode(PIN_LED_GREEN, OUTPUT);
  pinMode(PIN_BTN_RESET, INPUT_PULLUP);
  analogReadResolution(12);  // ESP32: 12-bit ADC (0-4095)

  // Safe initial state
  digitalWrite(PIN_LED_GREEN, HIGH);
  digitalWrite(PIN_LED_RED,   LOW);
  digitalWrite(PIN_BUZZER,    LOW);

  // OLED
  Wire.begin(21, 22);
  if (oled.begin(SSD1306_SWITCHCAPVCC, OLED_ADDR)) {
    showSplash();
  } else {
    Serial.println("[OLED] Not found — check wiring");
  }

  // Wi-Fi
  connectWiFi();

  sessionStartMs = millis();
  Serial.println("\n[SYS] Monitoring started. Rotate potentiometers to simulate load.\n");
  Serial.println("Timestamp        | V(V)   | I(A)   | P(W)   | E(kWh)  | Cost(₹) | Alert");
  Serial.println("-----------------|--------|--------|--------|---------|---------|-------");
}

// ============================================================
//  LOOP
// ============================================================
void loop() {
  unsigned long now = millis();

  // ── Reset button ──────────────────────────────────────────
  if (digitalRead(PIN_BTN_RESET) == LOW) {
    energy_kWh = 0;
    cost_INR   = 0;
    pushCount  = 0;
    sessionStartMs = now;
    Serial.println("[BTN] Energy counter RESET");
    delay(500); // debounce
  }

  // ── Sensor read & calculation ─────────────────────────────
  if (now - lastCalcMs >= CALC_INTERVAL_MS) {
    lastCalcMs = now;

    // Read potentiometers (0–4095)
    int rawI = analogRead(PIN_CURRENT);
    int rawV = analogRead(PIN_VOLTAGE);

    // Map to physical ranges
    current_A = mapFloat(rawI, 0, 4095, I_MIN, I_MAX);
    voltage_V = mapFloat(rawV, 0, 4095, V_MIN, V_MAX);

    // Add small simulated noise (±0.5%)
    current_A += (random(-5, 5) / 1000.0);
    voltage_V += (random(-5, 5) / 100.0);
    current_A = max(0.0f, current_A);

    // Power & energy
    power_W     = voltage_V * current_A * POWER_FACTOR;
    float dtH   = CALC_INTERVAL_MS / 3600000.0;  // Δt in hours
    energy_kWh += (power_W * dtH) / 1000.0;      // Wh → kWh
    cost_INR    = energy_kWh * COST_PER_KWH;

    // Alert
    if (power_W >= OVERLOAD_W)       alertStatus = 2;
    else if (power_W >= THRESHOLD_W) alertStatus = 1;
    else                             alertStatus = 0;

    handleAlert(alertStatus);
    printSerial(now);
  }

  // ── OLED refresh ──────────────────────────────────────────
  if (now - lastOledMs >= OLED_INTERVAL_MS) {
    lastOledMs = now;
    updateOLED();
  }

  // ── ThingSpeak push ───────────────────────────────────────
  if (wifiOK && (now - lastPushMs >= PUSH_INTERVAL_MS)) {
    lastPushMs = now;
    pushThingSpeak();
  }
}

// ============================================================
//  SENSOR HELPERS
// ============================================================
float mapFloat(int x, int in_min, int in_max, float out_min, float out_max) {
  return (float)(x - in_min) * (out_max - out_min) / (float)(in_max - in_min) + out_min;
}

// ============================================================
//  ALERT HANDLER
// ============================================================
void handleAlert(int status) {
  if (status == 0) {
    // Normal — green LED on, red off
    digitalWrite(PIN_LED_GREEN, HIGH);
    digitalWrite(PIN_LED_RED,   LOW);
    digitalWrite(PIN_BUZZER,    LOW);

  } else if (status == 1) {
    // HIGH — red LED blink, 2 buzzer beeps
    digitalWrite(PIN_LED_GREEN, LOW);
    digitalWrite(PIN_LED_RED,   HIGH);
    for (int i = 0; i < 2; i++) {
      digitalWrite(PIN_BUZZER, HIGH); delay(80);
      digitalWrite(PIN_BUZZER, LOW);  delay(80);
    }

  } else if (status == 2) {
    // OVERLOAD — RED only flashes, green stays OFF, 4 beeps
    digitalWrite(PIN_LED_GREEN, LOW);
    for (int i = 0; i < 4; i++) {
      digitalWrite(PIN_LED_RED, HIGH);
      digitalWrite(PIN_BUZZER,  HIGH); delay(150);
      digitalWrite(PIN_LED_RED, LOW);
      digitalWrite(PIN_BUZZER,  LOW);  delay(80);
    }
  }
}

// ============================================================
//  OLED DISPLAY
// ============================================================
void showSplash() {
  oled.clearDisplay();
  oled.setTextColor(WHITE);
  oled.setTextSize(1);
  oled.setCursor(8, 4);  oled.println("Smart Energy");
  oled.setCursor(8, 16); oled.println("Monitor v2.0");
  oled.setCursor(4, 30); oled.println("ThingSpeak IoT");
  oled.setCursor(4, 44); oled.println("Ch: 3406670");
  oled.drawRect(0, 0, 128, 64, WHITE);
  oled.display();
  delay(2500);
}

void updateOLED() {
  oled.clearDisplay();
  oled.setTextSize(1);
  oled.setTextColor(WHITE);

  // ── Header ──────────────────────────────────────────────
  const char* header = (alertStatus == 2) ? "!! OVERLOAD !!"
                     : (alertStatus == 1) ? "! HIGH POWER !"
                     : "Energy Monitor";
  oled.setCursor(alertStatus > 0 ? 4 : 12, 0);
  oled.println(header);
  oled.drawLine(0, 10, 128, 10, WHITE);

  // ── Row 1: V and I ──────────────────────────────────────
  oled.setCursor(0, 14);
  oled.print("V:"); oled.print(voltage_V, 1); oled.print("V");
  oled.setCursor(68, 14);
  oled.print("I:"); oled.print(current_A, 2); oled.print("A");

  // ── Row 2: Power ────────────────────────────────────────
  oled.setCursor(0, 26);
  oled.print("P:"); oled.print(power_W, 1); oled.print("W");
  oled.setCursor(68, 26);
  oled.print("PF:"); oled.print(POWER_FACTOR);

  // ── Row 3: Energy ───────────────────────────────────────
  oled.setCursor(0, 38);
  oled.print("E:"); oled.print(energy_kWh, 5); oled.print("kWh");

  // ── Row 4: Cost ─────────────────────────────────────────
  oled.setCursor(0, 50);
  oled.print("Cost:Rs."); oled.print(cost_INR, 4);

  // ── Push count ──────────────────────────────────────────
  oled.setCursor(100, 0);
  oled.print("#"); oled.print(pushCount);

  oled.display();
}

// ============================================================
//  SERIAL MONITOR OUTPUT
// ============================================================
void printSerial(unsigned long now) {
  unsigned long elapsed = (now - sessionStartMs) / 1000;
  char ts[12];
  sprintf(ts, "%02lu:%02lu:%02lu", elapsed/3600, (elapsed%3600)/60, elapsed%60);

  const char* alertStr = (alertStatus == 2) ? "OVERLOAD"
                       : (alertStatus == 1) ? "HIGH    "
                       : "NORMAL  ";

  Serial.printf("%s | %6.2f | %6.3f | %6.1f | %7.5f | %7.4f | %s\n",
    ts, voltage_V, current_A, power_W, energy_kWh, cost_INR, alertStr);
}

void printBanner() {
  Serial.println("============================================================");
  Serial.println("  Smart Home Energy Monitoring System — Wokwi Edition");
  Serial.println("  ThingSpeak Channel: 3406670");
  Serial.println("  Field 1=V  Field 2=I  Field 3=P  Field 4=kWh  Field 5=Cost  Field 6=Alert");
  Serial.println("============================================================");
}

// ============================================================
//  WI-FI
// ============================================================
void connectWiFi() {
  Serial.print("[WiFi] Connecting to ");
  Serial.print(WIFI_SSID);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  int tries = 0;
  while (WiFi.status() != WL_CONNECTED && tries < 25) {
    delay(400);
    Serial.print(".");
    tries++;
  }
  if (WiFi.status() == WL_CONNECTED) {
    wifiOK = true;
    Serial.println(" ✓");
    Serial.print("[WiFi] IP: ");
    Serial.println(WiFi.localIP());
  } else {
    wifiOK = false;
    Serial.println("\n[WiFi] FAILED — running offline (ThingSpeak disabled)");
  }
}

// ============================================================
//  THINGSPEAK PUSH — Raw HTTP GET (no library needed)
//  Matches your channel fields exactly
// ============================================================
void pushThingSpeak() {
  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("[TS] WiFi lost — skipping push");
    return;
  }

  // Build URL
  // Field mapping:
  //   field1 = Voltage (V)
  //   field2 = Current (A)
  //   field3 = Active Power (W)
  //   field4 = Energy Consumed (kWh)
  //   field5 = Accumulated Cost (INR)
  //   field6 = Overload Alert Status
  String url = "/update?api_key=";
  url += TS_API_KEY;
  url += "&field1=" + String(voltage_V,   2);
  url += "&field2=" + String(current_A,   3);
  url += "&field3=" + String(power_W,     1);
  url += "&field4=" + String(energy_kWh,  5);
  url += "&field5=" + String(cost_INR,    4);
  url += "&field6=" + String(alertStatus);

  Serial.print("[TS] Pushing → ");

  if (client.connect("api.thingspeak.com", 80)) {
    client.print("GET " + url + " HTTP/1.1\r\n");
    client.print("Host: api.thingspeak.com\r\n");
    client.print("Connection: close\r\n\r\n");

    // Wait for response (max 3s)
    unsigned long t = millis();
    while (!client.available() && millis() - t < 3000) delay(10);

    String resp = "";
    while (client.available()) {
      resp += (char)client.read();
    }
    client.stop();

    // ThingSpeak returns entry ID (integer) or 0 on failure
    int idx = resp.lastIndexOf("\r\n\r\n");
    String entryId = (idx >= 0) ? resp.substring(idx + 4) : "?";
    entryId.trim();

    if (entryId != "0" && entryId.length() > 0) {
      pushCount++;
      Serial.println("✓ Entry ID: " + entryId +
        "  (V=" + String(voltage_V,1) +
        " I=" + String(current_A,2) +
        " P=" + String(power_W,0) + "W)");
    } else {
      Serial.println("✗ Failed (rate limit or bad key)");
    }

  } else {
    Serial.println("✗ Can't reach api.thingspeak.com");
  }
}
