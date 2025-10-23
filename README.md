# King Khalid International Airport Traffic Study

## Project Overview
This repository analyses 153,308 movement records captured for King Khalid International Airport (RUH) between 14 March and 10 October 2025. Each row represents a reported flight movement (arrival or departure) enriched with airline, schedule, and terminal attributes. The raw feed contains sizeable duplication caused by codeshare listings and repeated schedule snapshots, so the first priority was to reconcile those records into a trustworthy count of real movements.

## Environment & Tooling
- **Runtime:** Conda environment `Manim`
- **Core libraries:** `pandas`, `pyarrow`, `seaborn`, `matplotlib`, `plotly`
- **Artefact structure:**
  - `analysis/` — reproducible scripts (`data_pipeline.py`, `generate_visuals.py`, `summary_metrics.py`, `build_dashboard.py`)
  - `outputs/data/` — enriched parquet files, summaries, and metrics JSON
  - `outputs/figures/` — PNG charts shared across deliverables
  - `outputs/dashboard.html` — compiled HTML briefing
  - `analysis_log.md` — dated rationale for every processing decision

## Workflow Summary
1. **Data Profiling & Plan:** Reviewed schema in `Notes.md`, mapped owner hint (“row count ≠ trips”), and sketched the pipeline in `analysis_plan.md`.
2. **Feature Engineering:** `analysis/data_pipeline.py` converts the parquet file to `movements_enriched.parquet`, standardising timestamps, mapping terminals, flagging weekend activity, and clarifying that the “destination” fields in arrival rows actually describe the *origin* airport for inbound legs.
3. **Deduplication:** Unique legs are identified by direction, UTC schedule, counterparty ICAO, and terminal. This collapses 9,263 redundant rows, yielding **144,045 distinct movements** (72,140 arrivals, 71,905 departures). The movement summary also exposes the residual duplication per direction for transparency.
4. **Metrics & Visuals:** `summary_metrics.py` materialises reusable aggregates (top airlines, domestic mix, hourly cadence, terminal utilisation, leading airports). `generate_visuals.py` transforms those insights into five PNG figures stored under `outputs/figures`.
5. **Dashboard Assembly:** `build_dashboard.py` stitches the KPIs and charts into `outputs/dashboard.html`, providing a teaching-friendly narrative.

## Key Insights
- **Movement volume:** 144,045 real legs; 9,263 of the raw rows were duplicates triggered by codeshares or repeated snapshots (3.8% redundancy).
- **Direction split:** Arrivals (72,140) and departures (71,905) are balanced, reinforcing RUH’s role as a through hub.
- **Domestic vs. international:** 52.6% of movements connect to Saudi airports (ICAO prefix “OE”), while 47.4% serve international destinations. Jeddah, Dubai, Cairo, Abha, and Dammam dominate both inbound and outbound flows.
- **Airline footprint:** Saudi Arabian (58k), flynas (32.6k), and flyadeal (23.5k) lead traffic, with regional partners such as flydubai, Gulf Air, Qatar Airways, EgyptAir, and Etihad sustaining international corridors.
- **Terminal operations:** Terminal 5 handles 52% of movements, underscoring its domestic focus; Terminals 1, 3, and 4 each capture ~15%.
- **Hourly cadence:** Night banks (22:00–02:00) are arrival-heavy, whereas outbound peaks cluster at 07:00–11:00 and 16:00–19:00.

## Owner Hint (“Trick”) Explained
The data owner warned that a 150k-row file does not guarantee 150k distinct trips. Many records are duplicate representations of the same physical leg because different airlines share the same flight or the feed captured multiple schedule snapshots. We detect these cases by grouping on direction, scheduled UTC time, terminal, and the counterparty airport.

**Example:** On 15 March 2025 at 01:00 UTC a departure from Riyadh Terminal 5 heads to Jeddah. The raw file lists both `SV 1015` (Saudi Arabian) and `F3 169` (flyadeal) for that slot. They are the same aircraft operating a codeshare. Without consolidation the dataset double counts that movement; our pipeline collapses them into a single unique leg while keeping track of the airlines involved.

## Visual Catalogue
| Figure | Path | Description |
| --- | --- | --- |
| Daily movements | `outputs/figures/daily_movements.png` | Arrival vs. departure trend across the observation window |
| Hourly profile | `outputs/figures/hourly_profile.png` | Distribution of legs by local hour and direction |
| Airline leaders | `outputs/figures/airline_leaders.png` | Top 15 airlines after codeshare consolidation |
| Domestic vs. international | `outputs/figures/domestic_international_mix.png` | Directional mix between Saudi and foreign airports |
| Terminal usage | `outputs/figures/terminal_usage.png` | Movements handled per terminal |

## Reproducibility Guide
```bash
# 1. Build enriched tables and movement summary
conda run -n Manim python "analysis/data_pipeline.py"

# 2. Refresh charts
conda run -n Manim python "analysis/generate_visuals.py"

# 3. Update metric dictionary (optional if step 1 already ran)
conda run -n Manim python "analysis/summary_metrics.py"

# 4. Regenerate dashboard
conda run -n Manim python "analysis/build_dashboard.py"
```

## Comparison with Shahad.md Analysis
| Aspect | Our Findings | Shahad.md Claims | Commentary |
| --- | --- | --- | --- |
| Dedup strategy | Collapsed rows by schedule, direction, counterparty airport, and terminal, preserving 144,045 real legs | Filtered to status \[Departed, Canceled\] and picked the latest record per flight number and date, leaving 11,557 legs | Their filter discards 92% of movements because most records carry `status="Unknown"`; the dataset’s “Unknown” label stems from feed quality, not flight absence |
| Directional context | Treated arrival `destination_*` fields as origin airports for inbound traffic (per-owner hint) | Interpreted `origin_airport_name` as the actual origin for all rows | For arrivals this swaps roles: in raw data `origin_*` always equals RUH; ignoring this misplaces inbound source airports |
| Airline volume | Saudi Arabian ≈ 58k, flynas ≈ 33k, flyadeal ≈ 23k movements after dedup | Saudi Arabian 4,238, flynas 2,421, flyadeal 1,534 counts | The understatement cascades from the status filter that removes “Unknown” entries |
| Destination focus | Jeddah, Dubai, Cairo, Abha, Dammam lead both inbound/outbound after dedup | Medina, Doha, London, Dubai identified as top destinations | Differences follow from the restricted subset used; Medina appears lower in our arrivals once Unknown statuses are restored |
| Terminal coverage | Terminal 5 accounts for 52% of movements, 1/3 split across T1–T4 | Terminal utilisation not evaluated | Our pipeline quantifies the owner’s hint about duplicated rows per terminal |

## Lessons for Students
1. **Validate metadata quirks:** Arrival rows mirror RUH as `origin_*`; always confirm column semantics before aggregating.
2. **Beware of “Unknown” placeholders:** Missing statuses are common in aviation feeds; discarding them can erase genuine movements.
3. **Engineer deterministic keys:** Combining direction, schedule time, counterparty ICAO, and terminal provides a reliable movement signature more robust than flight numbers alone.
4. **Separate reproducible scripts from narrative assets:** The pipeline scripts, metrics JSON, figures, and HTML dashboard let you regenerate outputs from scratch without manual edits.

For a chronological account of the analysis decisions, consult `analysis_log.md`. The interactive recap is available in `outputs/dashboard.html`.
