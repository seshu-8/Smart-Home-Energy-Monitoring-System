"""
energy_calculator.py
=====================
Handles all electrical calculations:
  - Apparent Power (VA)
  - Real Power (W) using power factor
  - Energy consumption (Wh, kWh)
  - Estimated electricity cost (INR)
"""


class EnergyCalculator:
    """
    Formulae used:
      Power (W)  = Voltage × Current × Power_Factor
      Energy (Wh) = Power (W) × Time (h)
      Energy (kWh) = Energy (Wh) / 1000
      Cost (INR) = Energy (kWh) × Rate (INR/kWh)

    Power Factor:
      Pure resistive loads (heater, bulb) → PF ≈ 1.0
      Inductive loads (AC, motor, fridge)  → PF ≈ 0.85
      We use 0.9 as a realistic household average.
    """

    POWER_FACTOR = 0.9  # Household average

    def __init__(self, cost_per_kwh: float = 7.0):
        """
        Args:
            cost_per_kwh: Electricity tariff in INR per kWh.
                          Hyderabad TSSPDCL domestic rate ~₹7/unit (2024).
        """
        self.cost_per_kwh = cost_per_kwh

    # ──────────────────────────────────────────────────────────
    def power(self, voltage: float, current: float) -> float:
        """
        Calculate real power in Watts.
        P = V × I × PF
        """
        return round(voltage * current * self.POWER_FACTOR, 4)

    def apparent_power(self, voltage: float, current: float) -> float:
        """
        Apparent power in VA (Volt-Amperes).
        S = V × I
        """
        return round(voltage * current, 4)

    def energy_wh(self, power_w: float, duration_seconds: float) -> float:
        """
        Energy consumed during this sample interval.
        E (Wh) = P (W) × t (hours)
                = P × (duration_seconds / 3600)
        """
        hours = duration_seconds / 3600.0
        return round(power_w * hours, 6)

    def to_kwh(self, energy_wh: float) -> float:
        """Convert Wh → kWh."""
        return round(energy_wh / 1000.0, 6)

    def cost(self, energy_wh: float) -> float:
        """
        Electricity cost in INR.
        Cost = kWh × tariff_rate
        """
        kwh = self.to_kwh(energy_wh)
        return round(kwh * self.cost_per_kwh, 4)

    def daily_projection(self, avg_power_w: float) -> dict:
        """
        Project daily / monthly usage from average power.

        Returns dict with:
          daily_kwh, monthly_kwh, daily_cost, monthly_cost
        """
        daily_kwh   = round((avg_power_w * 24) / 1000, 4)
        monthly_kwh = round(daily_kwh * 30, 4)
        return {
            "daily_kwh"    : daily_kwh,
            "monthly_kwh"  : monthly_kwh,
            "daily_cost"   : round(daily_kwh   * self.cost_per_kwh, 2),
            "monthly_cost" : round(monthly_kwh * self.cost_per_kwh, 2),
        }


# ──────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    calc = EnergyCalculator(cost_per_kwh=7.0)
    v, i = 230.0, 8.0
    p    = calc.power(v, i)
    e    = calc.energy_wh(p, 3600)          # 1 hour
    print(f"Power           : {p} W")
    print(f"Energy (1 hr)   : {e} Wh")
    print(f"Cost (1 hr)     : ₹{calc.cost(e)}")
    proj = calc.daily_projection(p)
    print(f"Daily projection: {proj}")
