"""
data_logger.py
===============
Logs every sensor reading + calculated values to a CSV file.
Mirrors what an SD card module would store on real ESP32 hardware.

CSV Columns:
  timestamp | sample_no | voltage_V | current_A | power_W |
  energy_Wh | cost_INR | alert_status
"""

import csv
import os
from datetime import datetime


class DataLogger:
    """
    Append-mode CSV logger.
    Creates file + header on first run; appends on subsequent runs.
    """

    HEADERS = [
        "timestamp",
        "sample_no",
        "voltage_V",
        "current_A",
        "power_W",
        "energy_Wh",
        "cost_INR",
        "alert_status",
    ]

    def __init__(self, csv_path: str = "data/energy_log.csv"):
        self.csv_path = csv_path
        self._ensure_file()

    # ──────────────────────────────────────────────────────────
    def _ensure_file(self):
        """Create CSV with header if it doesn't already exist."""
        os.makedirs(os.path.dirname(self.csv_path) if os.path.dirname(self.csv_path) else ".", exist_ok=True)
        if not os.path.exists(self.csv_path):
            with open(self.csv_path, "w", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=self.HEADERS)
                writer.writeheader()

    # ──────────────────────────────────────────────────────────
    def log(
        self,
        sample_no   : int,
        voltage     : float,
        current     : float,
        power_w     : float,
        energy_wh   : float,
        cost_inr    : float,
        alert_status: str,
    ):
        """Append one reading row to the CSV file."""
        row = {
            "timestamp"   : datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "sample_no"   : sample_no,
            "voltage_V"   : round(voltage,  2),
            "current_A"   : round(current,  3),
            "power_W"     : round(power_w,  2),
            "energy_Wh"   : round(energy_wh, 4),
            "cost_INR"    : round(cost_inr, 4),
            "alert_status": alert_status,
        }
        with open(self.csv_path, "a", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=self.HEADERS)
            writer.writerow(row)

    # ──────────────────────────────────────────────────────────
    def read_all(self) -> list[dict]:
        """Read all rows from CSV — used by report generator."""
        rows = []
        try:
            with open(self.csv_path, "r") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    rows.append(row)
        except FileNotFoundError:
            pass
        return rows

    # ──────────────────────────────────────────────────────────
    def clear(self):
        """Reset CSV — re-create with header only."""
        with open(self.csv_path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=self.HEADERS)
            writer.writeheader()
        print(f"  Log cleared: {self.csv_path}")


# ──────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    logger = DataLogger("data/test_log.csv")
    logger.log(1, 230.5, 2.15, 447.2, 0.2484, 0.00174, "NORMAL")
    logger.log(2, 229.8, 8.50, 1760.7, 1.2260, 0.00858, "HIGH")
    rows = logger.read_all()
    print(f"Logged {len(rows)} rows.")
    for r in rows:
        print(r)
