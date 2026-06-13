"""
report_generator.py
====================
Reads the CSV log and generates:
  1. A PDF energy report (with matplotlib charts embedded)
  2. A console summary

Dependencies: matplotlib, fpdf2
  pip install matplotlib fpdf2
"""

import csv
import os
from datetime import datetime


# ──────────────────────────────────────────────────────────────────
class ReportGenerator:
    def __init__(self, csv_path: str = "data/energy_log.csv"):
        self.csv_path = csv_path
        self.rows     = self._load_csv()

    # ──────────────────────────────────────────────────────────
    def _load_csv(self) -> list[dict]:
        rows = []
        try:
            with open(self.csv_path, "r") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    rows.append(row)
        except FileNotFoundError:
            print(f"  [ReportGenerator] CSV not found: {self.csv_path}")
        return rows

    # ──────────────────────────────────────────────────────────
    def _compute_summary(self) -> dict:
        if not self.rows:
            return {}
        voltages  = [float(r["voltage_V"]) for r in self.rows]
        currents  = [float(r["current_A"]) for r in self.rows]
        powers    = [float(r["power_W"])   for r in self.rows]
        energies  = [float(r["energy_Wh"]) for r in self.rows]
        alerts    = [r["alert_status"]     for r in self.rows]

        total_energy_wh = max(energies) if energies else 0.0
        total_cost      = float(self.rows[-1]["cost_INR"]) if self.rows else 0.0

        return {
            "samples"         : len(self.rows),
            "avg_voltage"     : round(sum(voltages) / len(voltages), 2),
            "avg_current"     : round(sum(currents) / len(currents), 3),
            "avg_power"       : round(sum(powers)   / len(powers),   2),
            "max_power"       : round(max(powers), 2),
            "total_energy_wh" : round(total_energy_wh, 4),
            "total_cost_inr"  : round(total_cost, 4),
            "high_alerts"     : alerts.count("HIGH"),
            "overload_alerts" : alerts.count("OVERLOAD"),
        }

    # ──────────────────────────────────────────────────────────
    def print_summary(self):
        s = self._compute_summary()
        if not s:
            print("No data to summarize.")
            return
        print("\n" + "=" * 50)
        print("  ENERGY MONITORING REPORT SUMMARY")
        print("=" * 50)
        print(f"  Samples collected  : {s['samples']}")
        print(f"  Avg Voltage        : {s['avg_voltage']} V")
        print(f"  Avg Current        : {s['avg_current']} A")
        print(f"  Avg Power          : {s['avg_power']} W")
        print(f"  Peak Power         : {s['max_power']} W")
        print(f"  Total Energy Used  : {s['total_energy_wh']} Wh")
        print(f"  Total Cost         : ₹{s['total_cost_inr']}")
        print(f"  HIGH Alerts        : {s['high_alerts']}")
        print(f"  OVERLOAD Alerts    : {s['overload_alerts']}")
        print("=" * 50)

    # ──────────────────────────────────────────────────────────
    def generate_pdf(self, output_path: str = "reports/energy_report.pdf"):
        """
        Generate a PDF report using matplotlib (charts) + fpdf2 (layout).
        Falls back to matplotlib-only PNG if fpdf2 not installed.
        """
        os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else ".", exist_ok=True)

        try:
            import matplotlib
            matplotlib.use("Agg")
            import matplotlib.pyplot as plt
            import matplotlib.gridspec as gridspec
            self._generate_matplotlib_report(output_path, plt, gridspec)
            print(f"  ✅ PDF Report saved: {output_path}")
        except ImportError:
            print("  ⚠️  matplotlib not found. Run: pip install matplotlib")
            self.print_summary()

    # ──────────────────────────────────────────────────────────
    def _generate_matplotlib_report(self, output_path, plt, gridspec):
        """Render a multi-chart PDF page using matplotlib."""
        if not self.rows:
            print("  No data rows to plot.")
            return

        samples  = [int(r["sample_no"])   for r in self.rows]
        voltages = [float(r["voltage_V"]) for r in self.rows]
        currents = [float(r["current_A"]) for r in self.rows]
        powers   = [float(r["power_W"])   for r in self.rows]
        energies = [float(r["energy_Wh"]) for r in self.rows]
        alerts   = [r["alert_status"]     for r in self.rows]

        # Color per alert status
        colors = ["#e74c3c" if a in ("HIGH", "OVERLOAD") else "#2ecc71" for a in alerts]

        s = self._compute_summary()

        fig = plt.figure(figsize=(14, 18), facecolor="#0f1923")
        fig.suptitle(
            "Smart Home Energy Monitoring Report",
            fontsize=18, fontweight="bold", color="white", y=0.98
        )

        gs = gridspec.GridSpec(4, 2, figure=fig, hspace=0.55, wspace=0.35)

        # ── Subplot helpers ────────────────────────────────────
        def styled_ax(pos, title, ylabel, color="#00bcd4"):
            ax = fig.add_subplot(pos)
            ax.set_facecolor("#1a2332")
            ax.set_title(title, color=color, fontsize=11, pad=8)
            ax.set_xlabel("Sample #", color="#aaa", fontsize=9)
            ax.set_ylabel(ylabel, color="#aaa", fontsize=9)
            ax.tick_params(colors="#aaa")
            for spine in ax.spines.values():
                spine.set_edgecolor("#2a3a4a")
            ax.grid(color="#2a3a4a", linestyle="--", linewidth=0.5)
            return ax

        # 1. Voltage
        ax1 = styled_ax(gs[0, 0], "Voltage Over Time", "Voltage (V)")
        ax1.plot(samples, voltages, color="#00bcd4", linewidth=1.8, marker="o", markersize=3)
        ax1.axhline(230, color="#ff9800", linestyle="--", linewidth=1, label="Nominal 230V")
        ax1.legend(fontsize=8, labelcolor="white", facecolor="#1a2332")

        # 2. Current
        ax2 = styled_ax(gs[0, 1], "Current Over Time", "Current (A)", "#ff9800")
        ax2.plot(samples, currents, color="#ff9800", linewidth=1.8, marker="s", markersize=3)

        # 3. Power (bar with alert coloring)
        ax3 = styled_ax(gs[1, 0], "Power Consumption", "Power (W)", "#e74c3c")
        ax3.bar(samples, powers, color=colors, alpha=0.85, width=0.7)
        ax3.axhline(3000, color="#e74c3c", linestyle="--", linewidth=1.2, label="Threshold 3kW")
        ax3.legend(fontsize=8, labelcolor="white", facecolor="#1a2332")

        # 4. Cumulative Energy
        ax4 = styled_ax(gs[1, 1], "Cumulative Energy Consumed", "Energy (Wh)", "#2ecc71")
        ax4.fill_between(samples, energies, color="#2ecc71", alpha=0.3)
        ax4.plot(samples, energies, color="#2ecc71", linewidth=1.8)

        # 5. Alert distribution (pie)
        ax5 = fig.add_subplot(gs[2, 0])
        ax5.set_facecolor("#1a2332")
        alert_counts = {
            "Normal"  : alerts.count("NORMAL"),
            "High"    : alerts.count("HIGH"),
            "Overload": alerts.count("OVERLOAD"),
        }
        pie_data   = [v for v in alert_counts.values() if v > 0]
        pie_labels = [k for k, v in alert_counts.items() if v > 0]
        pie_colors = ["#2ecc71", "#ff9800", "#e74c3c"][:len(pie_data)]
        ax5.pie(pie_data, labels=pie_labels, colors=pie_colors, autopct="%1.0f%%",
                textprops={"color": "white", "fontsize": 9})
        ax5.set_title("Alert Distribution", color="#00bcd4", fontsize=11, pad=8)

        # 6. Summary stats text box
        ax6 = fig.add_subplot(gs[2, 1])
        ax6.set_facecolor("#1a2332")
        ax6.axis("off")
        summary_text = (
            f"SESSION SUMMARY\n"
            f"{'─'*28}\n"
            f"Samples      : {s.get('samples', 0)}\n"
            f"Avg Voltage  : {s.get('avg_voltage', 0)} V\n"
            f"Avg Current  : {s.get('avg_current', 0)} A\n"
            f"Avg Power    : {s.get('avg_power', 0)} W\n"
            f"Peak Power   : {s.get('max_power', 0)} W\n"
            f"Total Energy : {s.get('total_energy_wh', 0)} Wh\n"
            f"Total Cost   : ₹{s.get('total_cost_inr', 0)}\n"
            f"HIGH Alerts  : {s.get('high_alerts', 0)}\n"
            f"OVL Alerts   : {s.get('overload_alerts', 0)}\n"
        )
        ax6.text(
            0.05, 0.95, summary_text,
            transform=ax6.transAxes,
            fontsize=10, verticalalignment="top",
            fontfamily="monospace", color="#e0e0e0",
            bbox=dict(boxstyle="round,pad=0.5", facecolor="#0d1820", edgecolor="#00bcd4")
        )

        # 7. Timestamp footer
        fig.text(
            0.5, 0.01,
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  |  "
            f"Smart Home Energy Monitoring System",
            ha="center", color="#666", fontsize=8
        )

        # Save
        plt.savefig(output_path, bbox_inches="tight", dpi=150, facecolor="#0f1923")
        plt.close()


# ──────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    reporter = ReportGenerator("data/energy_log.csv")
    reporter.print_summary()
    reporter.generate_pdf("reports/energy_report.pdf")
