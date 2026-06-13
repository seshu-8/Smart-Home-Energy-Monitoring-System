"""
dashboard_updater.py
=====================
Pushes sensor readings to ThingSpeak IoT cloud platform.
Also supports console-mode (enabled=False) for offline simulation.

ThingSpeak Fields Mapping:
  Field 1 → Voltage (V)
  Field 2 → Current (A)
  Field 3 → Power (W)
  Field 4 → Energy (Wh)
  Field 5 → Cost (INR)
  Field 6 → Alert Code (0=Normal, 1=High, 2=Overload)

Setup Instructions:
  1. Create free account at https://thingspeak.com
  2. Create new Channel with 6 fields (named as above)
  3. Copy your Write API Key
  4. Set thingspeak_api_key in main.py CONFIG
  5. Set thingspeak_enabled = True
"""

import time

try:
    import urllib.request
    import urllib.parse
    URLLIB_AVAILABLE = True
except ImportError:
    URLLIB_AVAILABLE = False


THINGSPEAK_URL = "https://api.thingspeak.com/update"

ALERT_CODE = {
    "NORMAL"  : 0,
    "HIGH"    : 1,
    "OVERLOAD": 2,
}


class DashboardUpdater:
    """
    Sends data to ThingSpeak cloud.
    Falls back gracefully if network unavailable or disabled.

    ThingSpeak free tier limit: 1 update per 15 seconds.
    Our 2-second sample interval exceeds this — in production
    you'd batch readings or use a paid tier / self-hosted instance.
    For demo purposes, every update attempt is logged.
    """

    def __init__(self, enabled: bool = False, api_key: str = ""):
        self.enabled = enabled and bool(api_key) and api_key != "YOUR_API_KEY_HERE"
        self.api_key = api_key
        self._last_push = 0
        self._push_interval = 15  # seconds (ThingSpeak free tier rate limit)

        if enabled and not self.enabled:
            print("  [Dashboard] ThingSpeak disabled: no valid API key set.")
        elif self.enabled:
            print(f"  [Dashboard] ThingSpeak ENABLED → {THINGSPEAK_URL}")

    # ──────────────────────────────────────────────────────────
    def update(
        self,
        voltage  : float,
        current  : float,
        power_w  : float,
        energy_wh: float,
        cost_inr : float,
        alert    : str = "NORMAL",
    ):
        """Push one data point to ThingSpeak (rate-limited)."""
        if not self.enabled:
            return  # silent no-op in offline/demo mode

        now = time.time()
        if now - self._last_push < self._push_interval:
            return  # rate limit: ThingSpeak allows 1 req / 15 sec on free

        params = {
            "api_key" : self.api_key,
            "field1"  : voltage,
            "field2"  : current,
            "field3"  : power_w,
            "field4"  : energy_wh,
            "field5"  : cost_inr,
            "field6"  : ALERT_CODE.get(alert, 0),
        }

        try:
            url     = THINGSPEAK_URL + "?" + urllib.parse.urlencode(params)
            req     = urllib.request.Request(url)
            with urllib.request.urlopen(req, timeout=5) as resp:
                entry_id = resp.read().decode("utf-8").strip()
            print(f"  [ThingSpeak] ✅ Entry ID: {entry_id}")
            self._last_push = now
        except Exception as e:
            print(f"  [ThingSpeak] ⚠️  Push failed: {e}")


# ──────────────────────────────────────────────────────────────────
# BLYNK ALTERNATIVE (commented out — uncomment to use)
# ──────────────────────────────────────────────────────────────────
# To use Blynk instead of ThingSpeak:
# 1. Create project at https://blynk.io
# 2. Add Virtual Pins V1-V6 for your 6 data fields
# 3. Install: pip install blynklib
# 4. Uncomment and adapt the class below
#
# class BlynkDashboard:
#     def __init__(self, auth_token):
#         import blynklib
#         self.blynk = blynklib.Blynk(auth_token)
#
#     def update(self, v, i, p, e, c, alert):
#         self.blynk.virtual_write(1, v)  # V1 = Voltage
#         self.blynk.virtual_write(2, i)  # V2 = Current
#         self.blynk.virtual_write(3, p)  # V3 = Power
#         self.blynk.virtual_write(4, e)  # V4 = Energy
#         self.blynk.virtual_write(5, c)  # V5 = Cost
#         self.blynk.virtual_write(6, alert)


# ──────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    # Test offline mode
    d = DashboardUpdater(enabled=False)
    d.update(230.5, 2.15, 444.7, 0.123, 0.00086, "NORMAL")
    print("Offline update: OK (no network call made)")
