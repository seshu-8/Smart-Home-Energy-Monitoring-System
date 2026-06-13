"""
Smart Home Energy Monitoring System
=====================================
Author      : Your Name
Date        : 2025
Description : Main entry point - runs full simulation pipeline
              (sensor reading → calculation → alerts → logging → report)
"""

import os
import sys

# Add project root to path
sys.path.insert(0, os.path.dirname(__file__))

from python_simulation.sensor_simulator import SensorSimulator
from python_simulation.energy_calculator import EnergyCalculator
from python_simulation.alert_engine import AlertEngine
from python_simulation.data_logger import DataLogger
from python_simulation.report_generator import ReportGenerator
from python_simulation.dashboard_updater import DashboardUpdater
import time

# ─────────────────────────────────────────────
# CONFIGURATION
# ─────────────────────────────────────────────
CONFIG = {
    "voltage_nominal"     : 230.0,   # Volts (India standard)
    "cost_per_kwh"        : 7.0,     # INR per kWh (Hyderabad average)
    "high_power_threshold": 3000.0,  # Watts - alert if exceeded
    "sample_interval_sec" : 2,       # How often to sample
    "total_samples"       : 30,      # Total readings in one run
    "mode"                : "mixed", # Options: normal | high | overload | mixed
    "log_csv"             : "data/energy_log.csv",
    "log_pdf"             : "reports/energy_report.pdf",
    "thingspeak_enabled"  : False,   # Set True + add API key for real cloud push
    "thingspeak_api_key"  : "YOUR_API_KEY_HERE",
}

def main():
    print("=" * 60)
    print("  Smart Home Energy Monitoring System")
    print("  Mode:", CONFIG["mode"].upper())
    print("=" * 60)

    # Initialize modules
    sensor    = SensorSimulator(mode=CONFIG["mode"])
    calc      = EnergyCalculator(cost_per_kwh=CONFIG["cost_per_kwh"])
    alert     = AlertEngine(threshold_watts=CONFIG["high_power_threshold"])
    logger    = DataLogger(csv_path=CONFIG["log_csv"])
    dashboard = DashboardUpdater(
        enabled=CONFIG["thingspeak_enabled"],
        api_key=CONFIG["thingspeak_api_key"]
    )

    print(f"\nRunning {CONFIG['total_samples']} samples every "
          f"{CONFIG['sample_interval_sec']}s ...\n")

    energy_total_wh = 0.0

    for i in range(1, CONFIG["total_samples"] + 1):
        # 1. Read sensor values
        voltage, current = sensor.read()

        # 2. Calculate power & energy
        power_w   = calc.power(voltage, current)
        energy_wh = calc.energy_wh(power_w, CONFIG["sample_interval_sec"])
        energy_total_wh += energy_wh
        cost_inr  = calc.cost(energy_total_wh)

        # 3. Check alerts
        alert_status = alert.check(power_w)

        # 4. Log to CSV
        logger.log(
            sample_no     = i,
            voltage       = voltage,
            current       = current,
            power_w       = power_w,
            energy_wh     = energy_total_wh,
            cost_inr      = cost_inr,
            alert_status  = alert_status,
        )

        # 5. Push to cloud dashboard (ThingSpeak)
        dashboard.update(voltage, current, power_w, energy_total_wh, cost_inr)

        # 6. Print to console
        flag = "⚠️  ALERT" if alert_status == "HIGH" else "✅ Normal"
        print(f"[{i:02d}] V={voltage:.1f}V  I={current:.3f}A  "
              f"P={power_w:.1f}W  E={energy_total_wh:.4f}Wh  "
              f"₹{cost_inr:.4f}  {flag}")

        time.sleep(CONFIG["sample_interval_sec"])

    # 7. Generate PDF report
    print("\n📄 Generating report ...")
    reporter = ReportGenerator(csv_path=CONFIG["log_csv"])
    reporter.generate_pdf(output_path=CONFIG["log_pdf"])

    print("\n" + "=" * 60)
    print(f"  ✅ Simulation Complete!")
    print(f"  Total Energy : {energy_total_wh:.4f} Wh")
    print(f"  Total Cost   : ₹{calc.cost(energy_total_wh):.4f}")
    print(f"  CSV Log      : {CONFIG['log_csv']}")
    print(f"  PDF Report   : {CONFIG['log_pdf']}")
    print("=" * 60)

if __name__ == "__main__":
    main()
