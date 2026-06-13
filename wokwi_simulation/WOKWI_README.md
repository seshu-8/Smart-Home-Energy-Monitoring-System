# Wokwi Simulation — Smart Home Energy Monitor
## ThingSpeak Channel 3406670

---

## ⚡ Quick Start (3 steps)

### Step 1 — Open Wokwi
Go to: https://wokwi.com/projects/new/esp32

### Step 2 — Load Files
Click the **"+"** tab in the editor and paste each file:
- `sketch.ino` → main code tab
- `diagram.json` → circuit tab (click the diagram.json tab)
- `libraries.txt` → auto-installs Adafruit SSD1306

### Step 3 — Press ▶ Start Simulation

---

## 🔌 Circuit Explanation

| Component | GPIO | Simulates |
|---|---|---|
| Potentiometer 1 (orange) | GPIO 34 | ACS712 current sensor output |
| Potentiometer 2 (purple) | GPIO 35 | ZMPT101B voltage sensor output |
| OLED SSD1306 SDA | GPIO 21 | I2C Data |
| OLED SSD1306 SCL | GPIO 22 | I2C Clock |
| Red LED + 330Ω | GPIO 27 | HIGH/OVERLOAD alert |
| Green LED + 330Ω | GPIO 25 | Normal status |
| Buzzer | GPIO 26 | Audible alert |
| Push Button | GPIO 33 | Reset energy counter |

---

## 🎛️ How to Simulate Different Loads

Rotate the potentiometers in the Wokwi simulation:

| Scenario | POT1 (Current) | POT2 (Voltage) | Expected |
|---|---|---|---|
| Standby / Idle | Far left (0%) | Mid (50%) | ~0W, No alert |
| Normal home (fans + fridge) | ~12% | ~50% | ~430W, Green LED |
| AC + washing machine | ~55% | ~50% | ~1450W, approaching threshold |
| HIGH alert trigger | ~60% | ~50% | >1500W, Red LED + Buzzer |
| OVERLOAD trigger | ~80%+ | ~50% | >3000W, Both LEDs flash |

### What each potentiometer maps to:
- **POT1 (GPIO34):** 0% = 0A, 100% = 25A
- **POT2 (GPIO35):** 0% = 200V, 100% = 240V (keep near 50% for 220V)

---

## 📡 ThingSpeak Integration

Your API key is already in the sketch: `89QGJJWRNRINYJDI`

The simulation pushes to your **Channel 3406670** every 15 seconds.

Field mapping:
```
Field 1 → Voltage (V)        ← from POT2
Field 2 → Current (A)        ← from POT1
Field 3 → Active Power (W)   ← V × I × 0.9
Field 4 → Energy (kWh)       ← cumulative
Field 5 → Cost (₹)           ← kWh × ₹7
Field 6 → Alert Status       ← 0/1/2
```

After the simulation runs for ~15 seconds, refresh your ThingSpeak channel — you'll see new data points appear on all 6 field charts.

---

## 📺 OLED Display Layout

```
┌────────────────────────┐
│   Energy Monitor   #3  │  ← push count
│────────────────────────│
│ V:229.8V   I:10.25A    │
│ P:2113.4W  PF:0.9      │
│ E:0.00587kWh           │
│ Cost:Rs.0.0411         │
└────────────────────────┘
```

During HIGH alert:
```
┌────────────────────────┐
│  ! HIGH POWER !   #5   │
│────────────────────────│
│ V:228.5V   I:15.82A    │
│ P:3266.7W  PF:0.9      │
│ ...                    │
└────────────────────────┘
```

---

## 🖥️ Serial Monitor Output

Open Serial Monitor at **115200 baud** to see:
```
============================================================
  Smart Home Energy Monitoring System — Wokwi Edition
  ThingSpeak Channel: 3406670
============================================================
[WiFi] Connecting to Wokwi-GUEST ........ ✓
[WiFi] IP: 10.10.0.2

Timestamp  | V(V)   | I(A)   | P(W)   | E(kWh)  | Cost(₹) | Alert
-----------|--------|--------|--------|---------|---------|-------
00:00:01   | 229.80 | 10.253 | 2113.5 | 0.00059 | 0.0041  | NORMAL
00:00:02   | 229.93 | 10.261 | 2115.5 | 0.00118 | 0.0083  | NORMAL
...
[TS] Pushing → ✓ Entry ID: 16  (V=229.8 I=10.25 P=2113W)
```

---

## 🔄 Reset Energy Counter

Press the **blue push button** (GPIO33) in the simulation to reset:
- `energy_kWh` → 0
- `cost_INR` → 0
- Push counter → 0

Useful for starting a fresh measurement session.

---

## 📸 Screenshots to Take for GitHub

1. **Simulation running** — OLED showing readings, green LED on
2. **HIGH alert** — Red LED on, buzzer active, OLED showing "HIGH POWER"
3. **OVERLOAD** — Both LEDs flashing pattern
4. **Serial monitor** — Table of readings with ThingSpeak push confirmations
5. **ThingSpeak charts** — After data appears on your channel (already uploaded!)

---

## 🔗 Share Your Wokwi Project

After setting up, click **Save** in Wokwi to get a shareable link:
`https://wokwi.com/projects/XXXXXXXXXXXXXXXXX`

Add this link to your GitHub README and LinkedIn post as proof of simulation.
