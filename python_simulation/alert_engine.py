"""
alert_engine.py
================
Monitors real-time power consumption and fires alerts when
thresholds are breached — mimicking a relay-controlled buzzer
on the ESP32 hardware.

Alert Levels:
  NORMAL  → Power below threshold
  HIGH    → Power exceeds threshold (buzzer + LED on hardware)
  OVERLOAD → Power > 2× threshold (relay trips in hardware)
"""


class AlertEngine:
    """
    Threshold-based alert system.

    On real hardware this would:
      HIGH     → digitalWrite(BUZZER_PIN, HIGH) for 1 second
      OVERLOAD → digitalWrite(RELAY_PIN, LOW)  to cut power
    """

    def __init__(self, threshold_watts: float = 3000.0):
        """
        Args:
            threshold_watts: Power level (W) that triggers HIGH alert.
                             Default 3000W = typical Indian home circuit limit.
        """
        self.threshold      = threshold_watts
        self.overload_limit = threshold_watts * 2.0   # 6000W default

        self._alert_count  = 0
        self._overload_count = 0

    # ──────────────────────────────────────────────────────────
    def check(self, power_w: float) -> str:
        """
        Evaluate power level and return alert status string.

        Returns:
            "NORMAL"   | "HIGH" | "OVERLOAD"
        """
        if power_w >= self.overload_limit:
            self._overload_count += 1
            self._trigger_overload(power_w)
            return "OVERLOAD"

        elif power_w >= self.threshold:
            self._alert_count += 1
            self._trigger_alert(power_w)
            return "HIGH"

        return "NORMAL"

    # ──────────────────────────────────────────────────────────
    def _trigger_alert(self, power_w: float):
        """Simulate buzzer beep + red LED on."""
        print(f"  ⚠️  HIGH POWER ALERT  →  {power_w:.1f}W  "
              f"(threshold: {self.threshold}W)")

    def _trigger_overload(self, power_w: float):
        """Simulate relay trip — would cut power in real hardware."""
        print(f"  🚨 OVERLOAD! RELAY TRIPPED  →  {power_w:.1f}W  "
              f"(limit: {self.overload_limit}W)")

    # ──────────────────────────────────────────────────────────
    def summary(self) -> dict:
        """Return alert statistics for the current session."""
        return {
            "total_high_alerts"    : self._alert_count,
            "total_overload_alerts": self._overload_count,
        }


# ──────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    engine = AlertEngine(threshold_watts=3000)
    test_values = [500, 1200, 3001, 5500, 6001, 1800]
    for p in test_values:
        status = engine.check(p)
        print(f"  Power={p}W  →  Status={status}")
    print("\nSession summary:", engine.summary())
