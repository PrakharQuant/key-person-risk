# METHODOLOGY.md — Key Person Risk Index

## Event Study
1. Estimation window: trading days [-250, -30] relative to event day 0.
2. Require ≥ 120 valid observations.
3. Market model: R_i,t = α_i + β_i R_m,t + ε_i,t
4. AR_i,t = R_i,t − (α̂_i + β̂_i R_m,t)
5. CAR over windows W: CAR = Σ_{t∈W} AR_t
   Windows: [-1,+1], [0,+5], [0,+20]
6. Winsorize CARs at 1st/99th percentiles before aggregation.
7. Significance: cross-sectional t-test on mean CAR; bootstrap 95% CI (1 000 resamples); Wilcoxon signed-rank.

Day 0 alignment: if announcement after market close or on non-trading day, day 0 = next trading day.

## KPRI Formula (0–100)
For each sector with N ≥ 25:

severity_s = −mean(CAR[-1,+1]_s)   (higher = worse)

severity_shrunk = (N / (N + 20)) * severity_s + (20 / (N + 20)) * grand_mean

tail_s = −10th-percentile(CAR)

hit_rate_s = proportion(CAR < −2%)

persistence_s = proxy for incomplete recovery (higher = worse)

Each component is min-max normalized across sectors to [0, 100] (higher = more risk).

KPRI_s = 0.40·severity_shrunk_norm + 0.25·tail_norm + 0.20·hit_rate_norm + 0.15·persistence_norm

Weights are configurable in `src/kpr/index.py`. Bootstrap CIs on KPRI via resampling of underlying events.

Sectors with N < 25 are labeled "insufficient data" and not ranked.

## Hypothesis Test
Difference in mean CAR[-1,+1] between (Technology + Healthcare) and (Automobile + Cement), with bootstrap CI.
Regression: CAR ~ C(sector) + role + departure_type + founder + log(mktcap) + market_vol.

## Disclaimer
Correlation is not causation. Survivorship, thin samples, and confounding events are documented in LIMITATIONS.md. Research only — not investment advice.
