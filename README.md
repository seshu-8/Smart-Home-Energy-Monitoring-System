# ⚡ Smart Home Energy Monitoring System

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![ESP32](https://img.shields.io/badge/ESP32-Arduino-E7352C?style=for-the-badge&logo=arduino&logoColor=white)
![IoT](https://img.shields.io/badge/IoT-Energy%20Monitoring-00C9B1?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

**A complete IoT system to monitor, analyze, and alert on home electricity consumption in real time.**  
Supports both physical ESP32 hardware and a full Python virtual simulation.

[Live Dashboard Demo](#dashboard) · [Setup Guide](#setup) · [Arduino Code](arduino_code/) · [Python Simulation](python_simulation/)

</div>

---

## 📋 Table of Contents

- [Overview](#overview)
- [Problem Statement](#problem-statement)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Hardware Components](#hardware-components)
- [Project Architecture](#project-architecture)
- [Folder Structure](#folder-structure)
- [Setup & Installation](#setup--installation)
- [Running the Simulation](#running-the-simulation)
- [Hardware Setup](#hardware-setup)
- [Cloud Dashboard (ThingSpeak)](#cloud-dashboard-thingspeak)
- [Sample Output](#sample-output)
- [Interview Q&A](#interview-preparation)
- [Future Improvements](#future-improvements)

---

## Overview

The **Smart Home Energy Monitoring System** is an end-to-end IoT solution that:

1. **Reads** voltage and current from sensors (ACS712 + ZMPT101B) connected to an ESP32
2. **Calculates** real-time power (W), cumulative energy (Wh/kWh), and estimated electricity cost (₹)
3. **Alerts** homeowners via buzzer + LED when consumption exceeds a configured threshold
4. **Trips a relay** to protect circuits during overload conditions
5. **Displays** live readings on an OLED screen and a cloud dashboard (ThingSpeak)
6. **Logs** all data to CSV and generates automated PDF reports

**No hardware? No problem.** A complete Python simulation faithfully replicates all sensor data, calculations, alerts, and reporting.

---

## Problem Statement

- India wastes an estimated **17–20% of electricity** due to unmonitored consumption
- Average household has **no real-time visibility** into which appliances consume most power
- Electricity bills arrive 30 days after usage — too late to correct behaviour
- Industrial circuits risk costly equipment damage from overload conditions

**This system solves all four problems:**
- Real-time power visibility → instant feedback
- Per-session cost estimation → bill awareness before month-end
- Threshold alerts → behaviour change prompt
- Relay protection → hardware safety

---

## Features

| Feature | Status |
|---|---|
| Real-time voltage & current reading | ✅ |
| Power (W) calculation with power factor | ✅ |
| Cumulative energy (Wh/kWh) tracking | ✅ |
| Electricity cost estimation (₹/kWh) | ✅ |
| Threshold-based HIGH / OVERLOAD alerts | ✅ |
| Relay auto-trip on overload | ✅ (hardware) |
| OLED display | ✅ (hardware) |
| CSV data logging | ✅ |
| PDF report generation with charts | ✅ |
| ThingSpeak cloud dashboard | ✅ |
| Interactive HTML dashboard (local) | ✅ |
| Python virtual simulation | ✅ |
| Modular, beginner-friendly code | ✅ |

---

## Tech Stack

| Layer | Technology |
|---|---|
| Microcontroller | ESP32 DevKit (38-pin) |
| Current Sensor | ACS712-30A |
| Voltage Sensor | ZMPT101B |
| Display | 0.96" OLED SSD1306 (I2C) |
| Alert Hardware | Active Buzzer + Red/Green LEDs |
| Load Control | 5V Relay Module |
| Cloud Platform | ThingSpeak (free tier) |
| Simulation Language | Python 3.10+ |
| Visualization | Matplotlib, Chart.js (HTML dashboard) |
| Logging | CSV (built-in), PDF (matplotlib) |

---

## Hardware Components

| Component | Qty | Purpose | Approx Cost (INR) |
|---|---|---|---|
| ESP32 DevKit v1 | 1 | Main microcontroller + Wi-Fi | ₹350 |
| ACS712-30A Module | 1 | AC/DC current sensing | ₹120 |
| ZMPT101B Module | 1 | AC voltage sensing | ₹150 |
| 0.96" OLED (SSD1306) | 1 | Real-time display | ₹140 |
| 5V Relay Module | 1 | Load control / overload protection | ₹60 |
| Active Buzzer | 1 | Audible alert | ₹25 |
| Red + Green LED | 2 | Status indicators | ₹10 |
| 330Ω Resistors | 2 | LED current limiting | ₹5 |
| Jumper Wires | 20 | Connections | ₹50 |
| Breadboard | 1 | Prototyping | ₹70 |
| **Total** | | | **~₹980** |

---

## Project Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    INPUT LAYER                               │
│  ACS712 (Current)    ZMPT101B (Voltage)    Appliance Status │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│                  PROCESSING (ESP32 / Python)                 │
│  • Power = V × I × Power Factor (0.9)                       │
│  • Energy (Wh) = Power × Time                               │
│  • Cost (₹) = Energy (kWh) × Tariff Rate                    │
│  • Alert Check: Power vs Threshold (3000W)                  │
└───────────────────────┬─────────────────────────────────────┘
                        │
          ┌─────────────┴──────────────┐
          ▼                            ▼
┌─────────────────┐          ┌─────────────────────┐
│  LOCAL OUTPUT   │          │   CLOUD OUTPUT       │
│  • OLED Display │          │   • ThingSpeak       │
│  • Buzzer Alert │          │   • HTML Dashboard   │
│  • Relay Trip   │          │   • PDF Report       │
│  • CSV Log      │          │   • Email Alert*     │
└─────────────────┘          └─────────────────────┘
```

---

## Folder Structure

```
Smart-Home-Energy-Monitoring-System/
│
├── arduino_code/
│   └── energy_monitor.ino      # Complete ESP32 firmware
│
├── python_simulation/
│   ├── __init__.py
│   ├── sensor_simulator.py     # Simulates ACS712 + ZMPT101B readings
│   ├── energy_calculator.py    # Power, energy, cost calculations
│   ├── alert_engine.py         # Threshold monitoring + alerts
│   ├── data_logger.py          # CSV logging
│   ├── report_generator.py     # PDF chart report
│   └── dashboard_updater.py    # ThingSpeak cloud push
│
├── dashboard/
│   └── index.html              # Interactive browser dashboard (Chart.js)
│
├── data/
│   └── energy_log.csv          # Generated CSV log (auto-created on run)
│
├── reports/
│   └── energy_report.pdf       # Generated PDF report
│
├── circuit_diagram/
│   └── wiring_guide.txt        # Detailed wiring instructions + ASCII diagram
│
├── docs/
│   ├── project_explanation.md  # Full project documentation
│   └── interview_prep.md       # 10 Q&A for placement interviews
│
├── images/                     # Screenshots for README (add your own)
├── outputs/                    # Additional output files
│
├── main.py                     # Entry point — run this
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

---

## Setup & Installation

### Prerequisites
- Python 3.10 or higher
- pip package manager
- (Optional) Arduino IDE 2.x for hardware

### Step 1: Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/Smart-Home-Energy-Monitoring-System.git
cd Smart-Home-Energy-Monitoring-System
```

### Step 2: Install Python Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Create Required Folders
```bash
mkdir -p data reports outputs images
```

---

## Running the Simulation

```bash
python main.py
```

**Expected console output:**
```
============================================================
  Smart Home Energy Monitoring System
  Mode: MIXED
============================================================

Running 30 samples every 2s ...

[01] V=230.9V  I=2.068A  P=429.7W  E=0.2387Wh  ₹0.0017  ✅ Normal
[02] V=230.1V  I=2.065A  P=427.6W  E=0.4763Wh  ₹0.0033  ✅ Normal
[03] V=229.9V  I=12.851A  P=2658.5W  E=1.9533Wh  ₹0.0137  ✅ Normal
  ⚠️  HIGH POWER ALERT  →  5780.3W  (threshold: 3000W)
[04] V=228.4V  I=28.122A  P=5780.3W  E=5.1645Wh  ₹0.0362  ⚠️  ALERT
...

📄 Generating report ...
  ✅ PDF Report saved: reports/energy_report.pdf
```

### Change Simulation Mode

Edit `main.py` → `CONFIG["mode"]`:

| Mode | Simulates |
|---|---|
| `"normal"` | Fans, lights, fridge, laptop (~430W) |
| `"high"` | 1.5-ton AC + washing machine (~2850W) |
| `"overload"` | All appliances ON simultaneously (~6500W) |
| `"mixed"` | Realistic daily cycle (default) |

### Open HTML Dashboard

Open `dashboard/index.html` in any browser — no server needed.

---

## Hardware Setup

1. Wire components per `circuit_diagram/wiring_guide.txt`
2. Open `arduino_code/energy_monitor.ino` in Arduino IDE
3. Edit the config section:
   ```cpp
   const char* WIFI_SSID       = "Your_WiFi_Name";
   const char* WIFI_PASSWORD   = "Your_Password";
   unsigned long CHANNEL_ID    = 1234567;         // ThingSpeak
   const char*   WRITE_API_KEY = "ABCDEF123456";
   ```
4. Install libraries via Library Manager:
   - `Adafruit SSD1306`
   - `Adafruit GFX Library`
   - `ThingSpeak`
5. Select Board: **ESP32 Dev Module**, Port: your COM port
6. Upload → Open Serial Monitor at 115200 baud

---

## Cloud Dashboard (ThingSpeak)

1. Create free account at [thingspeak.com](https://thingspeak.com)
2. **New Channel** → add 6 fields:
   - Field 1: Voltage (V)
   - Field 2: Current (A)
   - Field 3: Power (W)
   - Field 4: Energy (Wh)
   - Field 5: Cost (INR)
   - Field 6: Alert Status
3. Copy your **Write API Key**
4. Paste into `main.py` → `CONFIG["thingspeak_api_key"]`
5. Set `CONFIG["thingspeak_enabled"] = True`

---

## Sample Output

### CSV Log (`data/energy_log.csv`)

```
timestamp,sample_no,voltage_V,current_A,power_W,energy_Wh,cost_INR,alert_status
2025-06-10 14:23:01,1,230.9,2.068,429.73,0.2387,0.0017,NORMAL
2025-06-10 14:23:03,2,230.1,2.065,427.58,0.4763,0.0033,NORMAL
2025-06-10 14:23:05,3,229.9,12.851,2658.5,1.9533,0.0137,NORMAL
2025-06-10 14:23:07,4,228.4,28.122,5780.3,5.1645,0.0362,HIGH
```

### Session Summary
```
Samples collected  : 30
Avg Voltage        : 229.69 V
Avg Current        : 10.019 A
Avg Power          : 2068.09 W
Peak Power         : 6014.24 W
Total Energy Used  : 34.47 Wh
Total Cost         : ₹0.2413
HIGH Alerts        : 4
OVERLOAD Alerts    : 1
```

---

## Interview Preparation

See [`docs/interview_prep.md`](docs/interview_prep.md) for 10 detailed Q&A covering:
- Project explanation
- Sensor working principles
- Energy calculations
- IoT protocols
- Cloud integration
- Power factor concepts
- Safety mechanisms

---

## Future Improvements

- [ ] Mobile app (React Native) with push notifications
- [ ] Appliance identification using current waveform signatures (ML)
- [ ] Per-outlet monitoring with individual relays
- [ ] Time-of-use tariff optimization (charge EV at off-peak hours)
- [ ] Solar generation monitoring + net metering calculation
- [ ] MQTT broker integration for multi-device home network
- [ ] Telegram bot alerts
- [ ] Historical trend analysis with anomaly detection

---

## License

MIT License — free to use for learning and portfolio purposes.

---

<div align="center">
Built with ❤️ as an IoT course project &nbsp;|&nbsp; Hyderabad, India
</div>
