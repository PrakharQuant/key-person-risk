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

## Is Key-Person Risk Priced?

**Theoretical arguments that it should be priced**

- **Idiosyncratic human-capital risk**: In incomplete markets, investors cannot fully hedge the loss of a founder or key executive whose human capital is firm-specific (e.g., vision, relationships, technical expertise). This creates a non-diversifiable component of cash-flow risk that should command a premium (Mayers 1972; Jarrow & Rosenfeld 1984).
- **Agency and governance channel**: Sudden departures can signal governance weakness or trigger value-destroying succession contests. Investors rationally discount firms with high key-person exposure ex ante.
- **Empirical evidence of abnormal returns**: Classic event studies (e.g., Warner et al. 1988; Hayes & Schaefer 1999; Bennedsen et al. 2020 on Danish family firms) document statistically significant negative CARs around CEO deaths or forced resignations, especially for founder-led and R&D-intensive firms. Persistent underperformance after the event is consistent with a priced risk factor rather than pure information surprise.
- **Cross-sectional pricing**: Firms with higher key-person concentration (founder-CEO, dual class, low succession readiness) exhibit higher expected returns or lower valuation multiples after controlling for standard risk factors (some evidence in family-firm and insider-ownership literature).

**Theoretical arguments that it may not be fully priced (or is only partially priced)**

- **Diversification**: For well-diversified investors, firm-specific key-person risk should be largely idiosyncratic and therefore not priced in equilibrium (CAPM / APT logic). Only if the risk is systematic (e.g., correlated across tech founders during a regulatory or talent shock) would it enter the pricing kernel.
- **Anticipation and succession planning**: Markets may already incorporate the probability of departure into the stock price via insurance-like discounts or the presence of a named successor. The residual CAR then reflects only the surprise component, not the level of key-person risk itself.
- **Confounding information**: Announcements often coincide with earnings, strategy shifts, or board actions. Isolating a pure “key-person risk premium” is econometrically difficult; observed CARs may simply be information effects.
- **Limited long-horizon evidence**: While short-window CARs are robust, evidence that high-KPRI sectors or stocks earn higher average returns over multi-year horizons (after standard risk adjustments) remains mixed and sample-dependent.

**Implication for this index**

The KPRI measures the *realized reaction* to departures (severity, tail, hit rate, persistence). A high KPRI sector is one in which the market has historically treated key-person events as material. Whether that historical reaction reflects a priced risk premium, an information effect, or both is an open question that the regression and long-horizon tests in this repository are designed to help illuminate. The index itself is descriptive; it does not claim to be a tradable factor.

## Disclaimer
Correlation is not causation. Survivorship, thin samples, and confounding events are documented in LIMITATIONS.md. Research only — not investment advice.
