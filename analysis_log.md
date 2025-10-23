# Analysis Log

## 2025-10-23 — Kick-off & Data Familiarisation
- Activated the `Manim` conda environment for all Python execution to re-use preinstalled analytics packages.
- Inspected `flights_RUH.parquet`: 153,308 records with 23 columns spanning arrivals and departures (2025-03-14 → 2025-10-10 UTC).
- Noted heavy missingness in aircraft identifiers (`aircraft.reg`, `callSign`, `aircraft.modeS`) and modest gaps in destination metadata.
- Detected ~4% duplicate schedule/route combinations, supporting the owner's hint that row count > true trip count.
- Drafted the `analysis_plan.md` blueprint and accompanying workflow diagram to steer subsequent work.

## Next Focus
- Engineer robust identifiers to isolate unique flight movements before any aggregation.
- Build reusable scripts for quality checks, temporal profiling, airline/terminal analyses, and visual outputs.

## 2025-10-23 — Data Pipeline Construction
- Implemented `analysis/data_pipeline.py` to parse the parquet source, standardise date-time fields, and enrich categorical helpers (weekday, hour, codeshare flag, counterparty airport labels, terminal fill).
- Collapsed codeshare duplicates into 143,291 unique movement legs with movement-level identifiers and tokens describing associated airlines.
- Persisted enriched raw records and unique movement tables to `outputs/data`, alongside a quick summary of arrivals vs departures and codeshare prevalence for downstream analysis.

## 2025-10-23 — Visual Asset Generation
- Authored `analysis/generate_visuals.py` to derive trend, hourly, airline, terminal, and domestic/international views from the deduplicated movements.
- Exported five PNG figures into `outputs/figures` to anchor the upcoming dashboard and instructional materials.

## 2025-10-23 — Metric Summary Build
- Added `analysis/summary_metrics.py` to materialise reusable aggregates (movement counts, destination mix, airline leaders, hourly distribution, terminal splits).
- Persisted the metrics dictionary to `outputs/data/summary_metrics.json` for consumption by the dashboard and README authoring steps.

## 2025-10-23 — Dashboard Assembly
- Automated `outputs/dashboard.html` creation via `analysis/build_dashboard.py`, weaving headline KPIs with the generated figures.
- Documented the deduplication assumption (codeshare collapse) and the treatment of arrival destination fields as origin airports for inbound flights.

## 2025-10-23 — Deduplication Refinement
- Tightened movement identifiers to include terminal codes, ensuring one row per unique leg and reconciling counts between movement tables and visual summaries.
- Updated `movement_summary.csv` to expose source record totals and redundant row deltas for transparent reporting of the 9,263 duplicated inputs collapsed during processing.

## 2025-10-23 — Documentation & Comparison
- Authored `README.md` to walk students through the dataset context, tooling, reproducible scripts, core insights, and contrast with the external PySpark notebook.
- Reviewed `Shahad.md` and recorded the key methodological gaps (status filtering, arrival-origin interpretation, airline undercounts) for the concluding comparison section.
