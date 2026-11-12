# LIMITATIONS.md

- **Survivorship bias**: Delisted or acquired firms may be missing from yfinance. Failures are logged in data/quality_report.md and not silently dropped.
- **Look-ahead**: Estimation window is strictly pre-event.
- **Overlapping events / market shocks**: Events on crash days are flagged; sensitivity analysis recommended.
- **Thin samples**: Sectors with < 25 events are marked "insufficient data".
- **yfinance quirks**: Adjusted prices, missing history, ticker changes. Cached and reported.
- **Departure reason ambiguity**: LLM labels (if used) carry a manual_review_flag; primary sources are 8-K / exchange announcements.
- **Correlation ≠ causation**: Key-person effect cannot be isolated from concurrent news, sector sentiment, or selection.
- **Nvidia Nov 2026 case**: Developing event; excluded from statistical sample.

This is research, not investment advice.
