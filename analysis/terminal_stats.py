from __future__ import annotations

import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
metrics_path = BASE_DIR / "outputs" / "data" / "summary_metrics.json"

metrics = json.loads(metrics_path.read_text(encoding="utf-8"))
terminals = metrics["terminal_usage"]

overall = 0
for counts in terminals.values():
    counts["total"] = counts.get("arrival", 0) + counts.get("departure", 0)
    overall += counts["total"]

print("Overall movements (from terminals):", overall)
for term, counts in sorted(terminals.items(), key=lambda kv: kv[1]["total"], reverse=True):
    share = counts["total"] / overall * 100 if overall else 0
    print(term, counts["total"], f"{share:.2f}%")
