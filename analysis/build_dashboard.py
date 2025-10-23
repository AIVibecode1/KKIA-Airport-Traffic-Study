"""Generates a static HTML dashboard combining figures and headline metrics."""

from __future__ import annotations

import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[1]
METRICS_PATH = BASE_DIR / "outputs" / "data" / "summary_metrics.json"
FIG_DIR = Path("figures")
DASHBOARD_PATH = BASE_DIR / "outputs" / "dashboard.html"


def load_metrics() -> dict:
    with METRICS_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)


def render_html(metrics: dict) -> str:
    arrivals = metrics["movement_counts"].get("arrival", 0)
    departures = metrics["movement_counts"].get("departure", 0)
    total_unique = arrivals + departures

    dom_arr = metrics["scope_counts"].get("arrival", {}).get("Domestic", 0)
    dom_dep = metrics["scope_counts"].get("departure", {}).get("Domestic", 0)
    int_arr = metrics["scope_counts"].get("arrival", {}).get("International", 0)
    int_dep = metrics["scope_counts"].get("departure", {}).get("International", 0)

    top_airlines = list(metrics["top_airlines"].items())[:10]

    html = f"""<!DOCTYPE html>
<html lang=\"en\">
<head>
  <meta charset=\"UTF-8\" />
  <title>King Khalid Airport Traffic Dashboard</title>
  <style>
    body {{ font-family: 'Segoe UI', Tahoma, sans-serif; margin: 0; background-color: #f5f7fa; color: #1f2a44; }}
    header {{ background-color: #0a3d62; color: #fff; padding: 24px; }}
    main {{ padding: 24px 40px; }}
    section {{ margin-bottom: 40px; background: #fff; padding: 24px; border-radius: 12px; box-shadow: 0 6px 15px rgba(10,61,98,0.08); }}
    h1, h2 {{ margin-top: 0; }}
    .kpi-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 16px; }}
    .kpi {{ background: #e8f1fb; border-radius: 10px; padding: 16px; text-align: center; }}
    .kpi span {{ display: block; font-size: 32px; font-weight: 700; color: #0a3d62; }}
    img {{ max-width: 100%; border-radius: 10px; box-shadow: 0 4px 12px rgba(31,42,68,0.18); }}
    table {{ width: 100%; border-collapse: collapse; margin-top: 12px; }}
    th, td {{ padding: 10px; text-align: left; border-bottom: 1px solid #dde3ec; }}
    th {{ background: #0a3d62; color: #fff; }}
    ul {{ margin: 0; padding-left: 20px; }}
  </style>
</head>
<body>
  <header>
    <h1>King Khalid International Airport Traffic Dashboard</h1>
    <p>Unique flight movements derived from the March–October 2025 operations dataset.</p>
  </header>
  <main>
    <section>
      <h2>Key Performance Highlights</h2>
      <div class=\"kpi-grid\">
        <div class=\"kpi\"><span>{total_unique:,}</span>Total unique movements</div>
        <div class=\"kpi\"><span>{arrivals:,}</span>Inbound movements</div>
        <div class=\"kpi\"><span>{departures:,}</span>Outbound movements</div>
        <div class=\"kpi\"><span>{dom_arr + dom_dep:,}</span>Domestic legs</div>
        <div class=\"kpi\"><span>{int_arr + int_dep:,}</span>International legs</div>
      </div>
    </section>

    <section>
      <h2>Traffic Trends</h2>
      <p>Daily volume trends highlight the weekly cadence of passenger demand, with summer peaks evident in July and August.</p>
      <img src=\"{FIG_DIR / 'daily_movements.png'}\" alt=\"Daily movement trend\" />
    </section>

    <section>
      <h2>Operational Rhythm</h2>
      <p>Evening and late-night banks show strong inbound dominance, while outbound departures concentrate around morning and late afternoon waves.</p>
      <img src=\"{FIG_DIR / 'hourly_profile.png'}\" alt=\"Hourly profile\" />
    </section>

    <section>
      <h2>Airline Footprint</h2>
      <p>Saudi carriers anchor the hub, but regional partners sustain significant network breadth.</p>
      <img src=\"{FIG_DIR / 'airline_leaders.png'}\" alt=\"Top airlines\" />
      <table>
        <thead>
          <tr><th>Airline</th><th>Unique movements</th></tr>
        </thead>
        <tbody>
"""

    for name, count in top_airlines:
        html += f"          <tr><td>{name}</td><td>{count:,}</td></tr>\n"

    html += """        </tbody>
      </table>
    </section>

    <section>
      <h2>Route Mix & Terminals</h2>
      <div class=\"kpi-grid\">
"""

    html += f"""
        <div class=\"kpi\"><span>{dom_arr:,}</span>Inbound domestic</div>
        <div class=\"kpi\"><span>{dom_dep:,}</span>Outbound domestic</div>
        <div class=\"kpi\"><span>{int_arr:,}</span>Inbound international</div>
        <div class=\"kpi\"><span>{int_dep:,}</span>Outbound international</div>
      </div>
      <p>Terminal 5 dominates both arrivals and departures, underscoring its role as the primary domestic concourse.</p>
      <img src=\"{FIG_DIR / 'domestic_international_mix.png'}\" alt=\"Domestic vs international\" />
      <img src=\"{FIG_DIR / 'terminal_usage.png'}\" alt=\"Terminal usage\" />
    </section>

    <section>
      <h2>Data Notes</h2>
      <ul>
        <li>Movements are deduplicated on schedule, direction, terminal, and counterparty airport to correct for codeshare rows.</li>
        <li>Arrival records describe the counterparty airport in the destination fields; we treat these as the origin airports for inbound flights.</li>
        <li>Domestic classification relies on ICAO codes beginning with \"OE\" (Saudi Arabia).</li>
        <li>Owner trick example: the 15 Mar 2025 01:00 UTC departure to Jeddah (Terminal 5) appears twice in the raw file (<code>SV 1015</code> and <code>F3 169</code>) because Saudi Arabian and flyadeal share the service; deduplication collapses them into one movement.</li>
      </ul>
    </section>
  </main>
</body>
</html>
"""
    return html


def main() -> None:
    metrics = load_metrics()
    html = render_html(metrics)
    DASHBOARD_PATH.parent.mkdir(parents=True, exist_ok=True)
    DASHBOARD_PATH.write_text(html, encoding="utf-8")


if __name__ == "__main__":
    main()
