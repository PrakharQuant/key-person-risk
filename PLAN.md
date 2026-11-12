# PLAN.md — Key Person Risk Index (KPRI)

## Research Question
Do sectors like Technology and Pharma/Healthcare suffer larger abnormal stock declines on CEO/CFO resignations than sectors like Automobiles or Cement/Materials? Quantify this and publish a ranked sectoral Key Person Risk Index (KPRI).

**Motivating live case (flagged "developing, not in the statistical sample")**: Nvidia, November 2026 — CEO Jensen Huang resigned amid scandal; CFO Colette Kress named interim CEO; stock fell ~13% at open on 12 Nov 2026 (market cap loss >$500B).

## Architecture
- **Static-first**: Precomputed JSON/CSV in `docs/` and `data/processed/`. GitHub Pages site (vanilla JS + Plotly.js). Weekly GitHub Action refreshes data and commits outputs.
- **Pipeline**: `make all` runs prices → events → event study → index → export to site.
- **Optional**: FastAPI on Render (`render.yaml`) serving the same precomputed files.
- **Reproducibility**: All raw data cached to parquet; static sector mapping; manual review flags on labels; every site statistic traces to a file in the repo.

## Data Sources
### Prices (yfinance)
- Daily adjusted close for event stocks, market benchmarks (`^GSPC` US, `^NSEI`/`^BSESN` India), sector ETFs (XLK, XLV, XLY, XLB, XLF, XLE, XLI, XLP, XLU, XLRE, XLC, plus industry groupings for Auto/Cement).
- Cache to `data/raw/*.parquet`. Retry with exponential backoff. Log failures to `data/quality_report.md`.
- Sector/industry from yfinance `info` + static mapping file for reproducibility. Industry-level buckets so Automobile and Cement are analyzable separately from broad GICS.

### Events (CEO/CFO departures)
Target: 400+ events, 2010–2026, ≥25 per sector bucket (else "insufficient data").
Columns: `event_id, ticker, company, sector, industry, country, role (CEO/CFO), announcement_datetime (tz-aware), source_url, departure_type, is_founder, successor_named, interim_only, confounded, notes, manual_review_flag`.

Priority sources:
1. SEC EDGAR 8-K Item 5.02 (structured, free, timestamped) for US.
2. NSE/BSE corporate announcements (SEBI Reg. 30) for India.
3. News (GDELT / Google News RSS / NewsAPI if key present) for timing verification and reason.

Announcement timing: if after close or non-trading day → day 0 = next trading day.

LLM-assisted classification (Anthropic API, optional via env) for `departure_type` from text, but all labels written to reviewable CSV with `manual_review_flag`. Never trust silently.

## Methodology (Event Study)
- Estimation window: [-250, -30] trading days; require ≥120 valid days.
- Market model: regress stock returns on market/sector benchmark.
- AR = actual − predicted. CAR windows: [-1,+1], [0,+5], [0,+20].
- Robustness: simple market-adjusted returns.
- Winsorize 1%/99%. Cross-sectional t-test, bootstrap CIs, Wilcoxon/sign test.
- Exclude or flag confounded events (earnings, M&A, index changes in window).
- Splits: sector, role, departure type (forced/scandal vs planned), founder, market-cap bucket.
- Formal hypothesis test: mean CAR difference Tech+Pharma vs Auto+Cement (with CI) + regression CAR ~ sector + role + type + founder + log(mktcap) + vol.

## Key Person Risk Index (KPRI)
0–100 score per sector, empirical-Bayes shrunk:
- Severity: mean negative CAR[-1,+1]
- Tail: 10th-percentile CAR
- Hit rate: % events with CAR < -2%
- Persistence: recovery in CAR[0,+20]
- Optional: post-event vol spike

Configurable weights. Normalize (min-max or z-score → 0–100). Bootstrap confidence bands. Sensitivity page for alternative weights.
Exact formulas in `METHODOLOGY.md`.

## Site Pages (docs/)
- Home: ranking bar chart with CI, headline findings, plain-English hypothesis verdict.
- Sector explorer: event list, average CAR path -10 to +20 with band, histogram.
- Event explorer: searchable table with CARs, types, source links.
- Case study: Nvidia/Huang (price path vs XLK, comparison to similar historical events).
- Methodology + Limitations.

Vanilla JS + Plotly.js, responsive, dark/light mode.

## Risks & Mitigations
- Survivorship bias (delisted/acquired): log missing tickers, note in quality report, do not drop silently.
- Look-ahead bias: estimation window strictly before event; no future data.
- Overlapping events / clustered shocks: flag and optionally exclude market-crash days; report sensitivity.
- Thin samples: "insufficient data" if N < 25; shrink toward grand mean.
- yfinance quirks (adjustments, delistings, missing): cache + quality report.
- Ambiguous departure reasons: LLM + mandatory manual review flag.
- Correlation ≠ causation: explicit disclaimer; research only, not investment advice.
- Data quality: all labels reviewable; sources linked.

## Phases & Commits
1. Phase 0: this PLAN.md (this commit).
2. Phase 1: price fetching + caching + sector mapping + quality report.
3. Phase 2: event dataset construction (EDGAR + news + India) + classification stub.
4. Phase 3: event study engine + tests with synthetic data.
5. Phase 4: KPRI calculation + export JSON.
6. Phase 5: GitHub Pages site + workflows.
7. Phase 6: optional FastAPI + polish + README with findings.

## Acceptance
- `make all` from scratch reproduces site.
- Tests pass in CI.
- Every statistic on site traces to CSV/JSON.
- README states main finding, N per sector, confidence level, and disclaimer.

**This is research, not investment advice.**
