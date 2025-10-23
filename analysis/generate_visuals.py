"""Produces static visualisations for the King Khalid Airport traffic study."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


BASE_DIR = Path(__file__).resolve().parents[1]
UNIQUE_PATH = BASE_DIR / "outputs" / "data" / "unique_movements.parquet"
FIG_DIR = BASE_DIR / "outputs" / "figures"


def load_unique_movements(path: Path) -> pd.DataFrame:
    df = pd.read_parquet(path)
    df["local_date"] = pd.to_datetime(df["local_date"])
    return df


def plot_daily_trend(df: pd.DataFrame) -> None:
    daily = (
        df.groupby(["local_date", "flight_type"], as_index=False)
        .agg(movements=("movement_id", "nunique"))
        .sort_values("local_date")
    )
    plt.figure(figsize=(12, 6))
    sns.lineplot(
        data=daily,
        x="local_date",
        y="movements",
        hue="flight_type",
        marker="o",
    )
    plt.title("Daily movements by direction (unique legs)")
    plt.xlabel("Local date (Asia/Riyadh)")
    plt.ylabel("Movements")
    plt.tight_layout()
    plt.savefig(FIG_DIR / "daily_movements.png", dpi=200)
    plt.close()


def plot_hour_distribution(df: pd.DataFrame) -> None:
    hourly = (
        df.groupby(["local_hour", "flight_type"], as_index=False)
        .agg(movements=("movement_id", "nunique"))
        .sort_values("local_hour")
    )
    plt.figure(figsize=(10, 6))
    sns.barplot(
        data=hourly,
        x="local_hour",
        y="movements",
        hue="flight_type",
    )
    plt.title("Hourly schedule distribution")
    plt.xlabel("Hour (local time)")
    plt.ylabel("Movements")
    plt.tight_layout()
    plt.savefig(FIG_DIR / "hourly_profile.png", dpi=200)
    plt.close()


def plot_airline_leaders(df: pd.DataFrame) -> None:
    exploded = df.explode("airline.name")
    exploded = exploded[exploded["airline.name"].notna()]
    top = (
        exploded.groupby("airline.name")
        .agg(movements=("movement_id", "nunique"))
        .sort_values("movements", ascending=False)
        .head(15)
        .reset_index()
    )
    plt.figure(figsize=(12, 6))
    sns.barplot(data=top, y="airline.name", x="movements", color="#1f77b4")
    plt.title("Top airlines by unique movements")
    plt.xlabel("Movements")
    plt.ylabel("Airline")
    plt.tight_layout()
    plt.savefig(FIG_DIR / "airline_leaders.png", dpi=200)
    plt.close()


def classify_domestic(counterparty_icao: str) -> str:
    if isinstance(counterparty_icao, str) and counterparty_icao.startswith("OE"):
        return "Domestic"
    return "International"


def plot_destination_mix(df: pd.DataFrame) -> None:
    df = df.copy()
    df["destination_scope"] = df["counterparty_airport_icao"].apply(classify_domestic)
    mix = (
        df.groupby(["destination_scope", "flight_type"], as_index=False)
        .agg(movements=("movement_id", "nunique"))
    )
    plt.figure(figsize=(8, 6))
    sns.barplot(
        data=mix,
        x="destination_scope",
        y="movements",
        hue="flight_type",
    )
    plt.title("Domestic vs international mix")
    plt.xlabel("")
    plt.ylabel("Movements")
    plt.tight_layout()
    plt.savefig(FIG_DIR / "domestic_international_mix.png", dpi=200)
    plt.close()


def plot_terminal_usage(df: pd.DataFrame) -> None:
    terminal = (
        df.groupby(["terminal", "flight_type"], as_index=False)
        .agg(movements=("movement_id", "nunique"))
        .sort_values("movements", ascending=False)
    )
    plt.figure(figsize=(10, 6))
    sns.barplot(
        data=terminal,
        y="terminal",
        x="movements",
        hue="flight_type",
    )
    plt.title("Terminal utilisation")
    plt.xlabel("Movements")
    plt.ylabel("Terminal")
    plt.tight_layout()
    plt.savefig(FIG_DIR / "terminal_usage.png", dpi=200)
    plt.close()


def main() -> None:
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    unique_df = load_unique_movements(UNIQUE_PATH)
    sns.set_theme(style="whitegrid")

    plot_daily_trend(unique_df)
    plot_hour_distribution(unique_df)
    plot_airline_leaders(unique_df)
    plot_destination_mix(unique_df)
    plot_terminal_usage(unique_df)


if __name__ == "__main__":
    main()
