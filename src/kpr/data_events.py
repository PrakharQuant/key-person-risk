"""Build events.csv from EDGAR 8-K Item 5.02 + news verification."""
from __future__ import annotations

import logging
from pathlib import Path

import pandas as pd

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

EVENTS_PATH = Path("data/events.csv")

SAMPLE_EVENTS = [
    {
        "event_id": "NVDA_2026_11_12_CEO",
        "ticker": "NVDA",
        "company": "NVIDIA Corporation",
        "sector": "Technology",
        "industry": "Semiconductors",
        "country": "US",
        "role": "CEO",
        "announcement_datetime": "2026-11-12T09:00:00-05:00",
        "source_url": "https://www.reuters.com/business/retail-consumer/nvidia-ceo-jensen-huang-step-down-big-blow-ai-boom-2026-11-12/",
        "departure_type": "forced/scandal",
        "is_founder": True,
        "successor_named": True,
        "interim_only": True,
        "confounded": False,
        "notes": "Huang resigned amid personal scandal; Kress interim. DEVELOPING — not in statistical sample.",
        "manual_review_flag": True,
    },
    # Additional historical placeholders (real pipeline would scrape EDGAR)
    {
        "event_id": "AAPL_2011_08_24_CEO",
        "ticker": "AAPL",
        "company": "Apple Inc.",
        "sector": "Technology",
        "industry": "Consumer Electronics",
        "country": "US",
        "role": "CEO",
        "announcement_datetime": "2011-08-24T16:30:00-04:00",
        "source_url": "https://www.sec.gov/Archives/edgar/data/320193/000119312511232849/d8k.htm",
        "departure_type": "death/health",
        "is_founder": False,
        "successor_named": True,
        "interim_only": False,
        "confounded": False,
        "notes": "Steve Jobs resignation (health). Classic key-person case.",
        "manual_review_flag": False,
    },
]


def fetch_edgar_item502(start_year: int = 2010, end_year: int = 2026) -> pd.DataFrame:
    """Stub for SEC EDGAR 8-K Item 5.02 scraping / API.
    In full implementation: use sec-api.io or direct EDGAR full-text search + parse.
    """
    logger.info("EDGAR stub: returning sample events. Real fetch requires SEC user-agent and pagination.")
    return pd.DataFrame(SAMPLE_EVENTS)


def main() -> None:
    df = fetch_edgar_item502()
    # Align day-0 logic would go here (next trading day if after close)
    df.to_csv(EVENTS_PATH, index=False)
    logger.info("Wrote %d events to %s", len(df), EVENTS_PATH)
    # Quality note
    with open("data/quality_report.md", "a") as f:
        f.write("\n## Events\nSample dataset used for skeleton. Full EDGAR scrape targets 400+ events.\n")


if __name__ == "__main__":
    main()
