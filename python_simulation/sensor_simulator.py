"""
sensor_simulator.py
====================
Simulates ACS712 current sensor + ZMPT101B voltage sensor output.

Modes:
  normal   → typical home usage (fans, lights, fridge)
  high     → AC + washing machine running
  overload → all appliances ON simultaneously
  mixed    → cycles through all modes realistically
"""

import random
import math
import time


class SensorSimulator:
    """
    Mimics real ESP32 ADC readings from:
      - ACS712-30A current sensor
      - ZMPT101B voltage sensor module
    """

    # Typical appliance current draws at 230V India grid
    APPLIANCE_PROFILES = {
        "normal": [
            # (label, current_A)
            ("Lights + Fan",   0.52),   # ~120W
            ("Fridge",         0.87),   # ~200W
            ("TV + Set-top",   0.43),   # ~100W
            ("Laptop charger", 0.26),   # ~60W
        ],
        "high": [
            ("1.5-ton AC",     7.61),   # ~1750W
            ("Washing Machine",3.91),   # ~900W
            ("Fridge",         0.87),   # ~200W
            ("Lights",         0.22),   # ~50W
        ],
        "overload": [
            ("1.5-ton AC",     7.61),
            ("Geyser",        10.87),   # ~2500W
            ("Microwave",      5.22),   # ~1200W
            ("Washing Machine",3.91),
            ("Fridge",         0.87),
        ],
    }

    def __init__(self, mode: str = "mixed"):
        self.mode = mode
        self._mixed_cycle  = 0
        self._mixed_phases = ["normal", "normal", "high", "overload", "high", "normal"]

    # ──────────────────────────────────────────────────────────
    def read(self) -> tuple[float, float]:
        """
        Returns (voltage_V, current_A) with realistic noise.
        Voltage sags slightly under high load (line regulation).
        """
        active_mode = self._resolve_mode()
        profile     = self.APPLIANCE_PROFILES[active_mode]

        # Sum all appliance currents
        base_current = sum(c for _, c in profile)

        # Add sensor noise (±2% — realistic for ACS712)
        noise_factor  = random.uniform(0.98, 1.02)
        current       = round(base_current * noise_factor, 3)

        # Voltage sag under load (Indian grid: 220–240V nominal)
        voltage_base  = 230.0
        sag           = base_current * 0.05          # 0.05 Ω line impedance approx
        voltage_noise = random.uniform(-1.5, 1.5)
        voltage       = round(max(200.0, voltage_base - sag + voltage_noise), 2)

        return voltage, current

    # ──────────────────────────────────────────────────────────
    def _resolve_mode(self) -> str:
        if self.mode != "mixed":
            return self.mode
        # Cycle through phases to simulate realistic day pattern
        phase = self._mixed_phases[self._mixed_cycle % len(self._mixed_phases)]
        self._mixed_cycle += 1
        return phase


# ──────────────────────────────────────────────────────────────────
# Quick standalone test
# ──────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    sim = SensorSimulator(mode="mixed")
    print("Voltage (V) | Current (A)")
    print("-" * 30)
    for _ in range(10):
        v, i = sim.read()
        print(f"{v:.2f} V     | {i:.3f} A")
        time.sleep(0.3)
