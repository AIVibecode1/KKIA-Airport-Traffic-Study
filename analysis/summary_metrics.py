"""Computes tabular metrics used in the report and dashboard."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[1]
UNIQUE_PATH = BASE_DIR / "outputs" / "data" / "unique_movements.parquet"
METRICS_PATH = BASE_DIR / "outputs" / "data" / "summary_metrics.json"


def classify_domestic(icao: str) -> str:
    if isinstance(icao, str) and icao.startswith("OE"):
        return "Domestic"
    return "International"


def main() -> None:
    df = pd.read_parquet(UNIQUE_PATH)

    movement_counts = (
        df.groupby("flight_type")["movement_id"].nunique().to_dict()
    )

    df["destination_scope"] = df["counterparty_airport_icao"].apply(classify_domestic)
    scope_counts = (
        df.groupby(["flight_type", "destination_scope"])["movement_id"]
        .nunique()
        .unstack(fill_value=0)
        .to_dict(orient="index")
    )

    exploded = df.explode("airline.name")
    exploded = exploded[exploded["airline.name"].notna()]
    top_airlines = (
        exploded.groupby("airline.name")["movement_id"].nunique()
        .sort_values(ascending=False)
        .head(15)
        .to_dict()
    )

    top_airport_series = (
        df[df["counterparty_airport_name"].notna()]
        .groupby(["flight_type", "counterparty_airport_name"])["movement_id"]
        .nunique()
        .sort_values(ascending=False)
        .groupby(level=0)
        .head(15)
    )
    top_airports: dict[str, list[dict[str, int]]] = {}
    for (flight_type, airport), value in top_airport_series.items():
        top_airports.setdefault(flight_type, []).append({
            "airport": airport,
            "movements": int(value),
        })

    hourly_profile = (
        df.groupby(["local_hour", "flight_type"])["movement_id"].nunique()
        .unstack(fill_value=0)
        .sort_index()
        .to_dict(orient="index")
    )

    terminals_table = (
        df.groupby(["terminal", "flight_type"])["movement_id"].nunique()
        .unstack(fill_value=0)
    )
    terminals_table["total"] = terminals_table.sum(axis=1)
    terminals = (
        terminals_table.sort_values("total", ascending=False)
        .drop(columns="total")
        .to_dict(orient="index")
    )

    metrics = {
        "movement_counts": movement_counts,
        "scope_counts": scope_counts,
        "top_airlines": top_airlines,
        "top_airports": top_airports,
        "hourly_profile": hourly_profile,
        "terminal_usage": terminals,
    }

    METRICS_PATH.parent.mkdir(parents=True, exist_ok=True)
    with METRICS_PATH.open("w", encoding="utf-8") as f:
        json.dump(metrics, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
