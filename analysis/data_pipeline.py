"""Builds the cleaned dataset and unique movement table for King Khalid Airport analysis."""

from __future__ import annotations

from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[1]
RAW_PATH = BASE_DIR / "flights_RUH.parquet"
OUTPUT_DATA_DIR = BASE_DIR / "outputs" / "data"


def load_data(path: Path) -> pd.DataFrame:
    """Read the parquet file and normalise list-valued columns."""
    df = pd.read_parquet(path)
    if "movement.quality" in df.columns:
        df["movement.quality"] = df["movement.quality"].apply(
            lambda x: x[0] if isinstance(x, (list, tuple)) and x else x
        )
    return df


def prepare_features(df: pd.DataFrame) -> pd.DataFrame:
    """Create typed datetime fields and helper columns for analysis."""
    df = df.copy()
    df["scheduled_utc"] = pd.to_datetime(df["movement.scheduledTime.utc"], utc=True)
    df["scheduled_local"] = pd.to_datetime(df["movement.scheduledTime.local"], utc=True)
    df["local_date"] = df["scheduled_local"].dt.tz_convert("Asia/Riyadh").dt.date
    df["local_hour"] = (
        df["scheduled_local"].dt.tz_convert("Asia/Riyadh").dt.hour.astype("int8")
    )
    df["weekday"] = df["scheduled_local"].dt.tz_convert("Asia/Riyadh").dt.day_name()
    df["is_weekend"] = df["weekday"].isin(["Friday", "Saturday"])
    df["codeshare_flag"] = df["codeshareStatus"].eq("IsOperator")
    df["counterparty_airport_icao"] = df["destination_airport_icao"]
    df["counterparty_airport_name"] = df["destination_airport_name"]
    df["counterparty_airport_iata"] = df["destination_airport_iata"]
    df["terminal"] = df["movement.terminal"].fillna("Unknown")
    return df


def build_unique_movements(df: pd.DataFrame) -> pd.DataFrame:
    """Collapse codeshare duplicates into a single movement record."""
    key_cols = [
        "flight_type",
        "scheduled_utc",
        "counterparty_airport_icao",
        "counterparty_airport_iata",
        "terminal",
    ]
    df = df.copy()
    df["record_count"] = 1
    agg_funcs = {
        "flight_number": "first",
        "airline.name": lambda x: sorted({v for v in x if pd.notna(v)}),
        "airline.iata": lambda x: sorted(set(filter(pd.notna, x))),
        "airline.icao": lambda x: sorted(set(filter(pd.notna, x))),
        "codeshare_flag": "max",
        "isCargo": "max",
        "record_count": "sum",
        "local_date": "first",
        "local_hour": "first",
        "weekday": "first",
        "is_weekend": "max",
        "counterparty_airport_name": "first",
        "counterparty_airport_iata": "first",
    }
    grouped = df.groupby(key_cols, as_index=False).agg(agg_funcs)
    grouped.rename(columns={
        "record_count": "records_collapsed",
        "codeshare_flag": "has_codeshare_operator",
        "isCargo": "is_cargo",
    }, inplace=True)
    grouped["airline_count"] = grouped["airline.name"].apply(len)
    grouped["movement_id"] = (
        grouped["flight_type"].str[0].str.upper()
        + "_"
        + grouped["scheduled_utc"].dt.strftime("%Y%m%d%H%M")
        + "_"
        + grouped["counterparty_airport_icao"].fillna("UNK")
        + "_"
        + grouped["terminal"].astype(str).str.replace(" ", "").str.upper()
    )
    return grouped


def main() -> None:
    OUTPUT_DATA_DIR.mkdir(parents=True, exist_ok=True)
    df_raw = load_data(RAW_PATH)
    df_features = prepare_features(df_raw)
    df_unique = build_unique_movements(df_features)

    df_features.to_parquet(OUTPUT_DATA_DIR / "movements_enriched.parquet", index=False)
    df_unique.to_parquet(OUTPUT_DATA_DIR / "unique_movements.parquet", index=False)

    summary_unique = df_unique.groupby("flight_type").agg(
        movements=("movement_id", "nunique"),
        codeshare_routes=("has_codeshare_operator", "sum"),
        cargo_routes=("is_cargo", "sum"),
    )
    raw_counts = df_features.groupby("flight_type").size().rename("source_records")
    summary = summary_unique.join(raw_counts, on="flight_type")
    summary["redundant_rows"] = summary["source_records"] - summary["movements"]
    summary.to_csv(OUTPUT_DATA_DIR / "movement_summary.csv")


if __name__ == "__main__":
    main()
