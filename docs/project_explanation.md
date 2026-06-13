# Smart Home Energy Monitoring System — Full Project Documentation

## 1. What Is It?

### Simple Explanation
Imagine your electricity meter only tells you your total bill at the end of the month. You have no idea which appliance is consuming the most or when. The Smart Home Energy Monitoring System is like a "live dashboard" for your electricity — it shows you **right now** how many watts you're using, what it's costing per hour, and screams at you when something is drawing dangerously high power.

### Technical Explanation
It is an **IoT (Internet of Things) embedded system** that:
- Uses an **ACS712 Hall Effect current sensor** to measure AC current flowing through the main electrical line
- Uses a **ZMPT101B transformer-based voltage sensor** to measure line voltage
- Feeds these analog readings into an **ESP32 microcontroller's 12-bit ADC**
- Applies **RMS calculation** to get true AC values from 500-sample windows
- Computes **real power (P = V × I × PF)** and accumulates **energy (E = P × t)**
- Estimates **electricity cost** using local tariff rate
- Fires **hardware alerts** (buzzer, LED, relay) when thresholds are breached
- Uploads data to **ThingSpeak cloud** via Wi-Fi HTTP API
- Logs all readings to **CSV** and generates **PDF reports** with matplotlib charts

---

## 2. The Monitoring Workflow

```
┌──────────────────┐
│  ACS712 Sensor   │  ← AC current through IP+ / IP- terminals
│  ZMPT101B Sensor │  ← Line voltage through AC transformer
└────────┬─────────┘
         │ Analog voltage signal (0–3.3V)
         ▼
┌──────────────────┐
│  ESP32 ADC       │  ← 12-bit, samples 500×/reading
│  (GPIO34, GPIO35)│
└────────┬─────────┘
         │ Digital values (0–4095)
         ▼
┌──────────────────────────────────────┐
│         ENERGY CALCULATION           │
│  V_rms = √(mean of V² samples)       │
│  I_rms = √(mean of I² samples)       │
│  P = V_rms × I_rms × 0.9 (PF)       │
│  E += P × (dt / 3600) Wh             │
│  Cost = (E/1000) × tariff_rate       │
└────────┬─────────────────────────────┘
         │
    ┌────┴──────┐
    ▼           ▼
┌────────┐  ┌──────────────────────────────┐
│ ALERT  │  │        OUTPUT                │
│ ENGINE │  │  • OLED: live V, I, P, Cost  │
│        │  │  • Serial: debugging         │
│ NORMAL │  │  • CSV: timestamped log      │
│ HIGH   │  │  • ThingSpeak: cloud push    │
│OVERLOAD│  │  • PDF: session report       │
└───┬────┘  └──────────────────────────────┘
    │
    ▼
┌──────────────────┐
│  HARDWARE ALERTS │
│  Buzzer: beep ×3 │
│  Red LED: ON     │
│  Relay: TRIP     │
└──────────────────┘
```

---

## 3. Industry Relevance

### Smart Homes
Companies like **Schneider Electric**, **Legrand**, and **Honeywell** sell home energy monitors starting at ₹15,000. The same principle — CT sensor + microcontroller + cloud — is their core architecture.

### Commercial Buildings
**LEED-certified** and **GRIHA-rated** buildings require energy sub-metering per floor/zone as a compliance requirement. Building Management Systems (BMS) use identical sensor setups at every distribution board.

### Factories
Industrial IoT (IIoT) platforms like **Siemens MindSphere** and **GE Predix** monitor individual machine power consumption to identify inefficient equipment, predict failures (motors drawing extra current = early bearing failure), and optimize shift scheduling to minimize peak demand charges.

### Energy Management Companies
**BSES**, **TSSPDCL**, and private energy aggregators use smart meters (advanced version of this project) to implement Time-of-Use pricing, detect energy theft via line loss analysis, and enable demand response programs.

### Solar Energy Companies
**Waaree**, **Adani Solar**, and **Tata Power Solar** integrate energy monitors with solar generation data to calculate:
- **Self-consumption rate** (solar used directly)
- **Grid export** (excess solar sold back)
- **Net metering** bill calculation

---

## 4. Tech Stack Selection Guide

### Option A — Arduino UNO + Simulated Data (Beginner)
- **Use when:** Complete beginner, just learning C/C++
- **Pros:** Simplest setup, lots of tutorials
- **Cons:** No Wi-Fi, no cloud, limited processing, no real sensor feasibility at scale

### Option B — ESP32 + ACS712 + ThingSpeak ✅ RECOMMENDED
- **Use when:** IoT course project, portfolio, placement
- **Pros:** Wi-Fi built-in, cloud integration, real sensor data, affordable
- **Cons:** Slightly steeper learning curve than UNO

### Option C — ESP32 + Smart Meter + MQTT + Node-RED (Advanced)
- **Use when:** Building a production system or research project
- **Pros:** Industry-standard protocols, scalable to hundreds of nodes
- **Cons:** Complex setup, requires MQTT broker, Node-RED server

**Recommendation for students:** Option B. It hits the sweet spot of being achievable without hardware (Python simulation covers the gap) while demonstrating all industry-relevant concepts.

---

## 5. GitHub Upload Strategy

### Repository Name
`Smart-Home-Energy-Monitoring-System`

### Description
`IoT-based real-time home energy monitor using ESP32, ACS712 current sensor, and ThingSpeak cloud. Includes Python simulation, interactive dashboard, CSV logging, and automated PDF reports.`

### Tags (Topics)
```
iot  esp32  energy-monitoring  python  arduino  thingspeak  smart-home
sensor  embedded-systems  dashboard  matplotlib  csv-logging  iot-project
```

### Commit Strategy
```
git init
git add .
git commit -m "Initial commit: project structure and documentation"

# After adding simulation code:
git commit -m "feat: add Python sensor simulator and energy calculator"

# After testing:
git commit -m "feat: add alert engine, CSV logger, and report generator"

# After dashboard:
git commit -m "feat: add interactive HTML dashboard with Chart.js"

# After Arduino code:
git commit -m "feat: add ESP32 Arduino firmware with ThingSpeak integration"

# After README:
git commit -m "docs: add complete README, circuit diagram, and interview prep"

# Final:
git commit -m "chore: add sample outputs and screenshots"
```

### What to Include as Screenshots
1. Project folder structure (screenshot of VS Code explorer)
2. Simulation running in terminal (console output)
3. CSV log file opened in Excel/LibreOffice
4. PDF report (all 4 charts visible)
5. HTML dashboard (all modes: normal, high, overload)
6. ThingSpeak channel dashboard (if hardware available)
7. Arduino Serial Monitor output (if hardware available)
8. Wokwi simulation screenshot (if using virtual hardware)

---

## 6. Screenshots / Proof Checklist

- [ ] `/images/01_folder_structure.png` — Project folder in VS Code or Explorer
- [ ] `/images/02_terminal_output.png` — Simulation running in terminal
- [ ] `/images/03_csv_log.png` — energy_log.csv open in spreadsheet
- [ ] `/images/04_pdf_report.png` — energy_report.pdf showing all charts
- [ ] `/images/05_dashboard_normal.png` — HTML dashboard in Normal mode
- [ ] `/images/06_dashboard_high.png` — Dashboard showing HIGH alert (red bars)
- [ ] `/images/07_dashboard_overload.png` — Dashboard during Overload
- [ ] `/images/08_thingspeak.png` — ThingSpeak channel (if available)
- [ ] `/images/09_circuit_diagram.png` — Wokwi or Fritzing circuit diagram
- [ ] `/images/10_github_repo.png` — GitHub repository page
