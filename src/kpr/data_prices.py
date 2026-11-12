"""Fetch and cache daily prices via yfinance."""
from __future__ import annotations

import logging
import time
from pathlib import Path
from typing import Optional

import pandas as pd
import yfinance as yf

RAW_DIR = Path("data/raw")
RAW_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

SECTOR_ETF = {
    "Technology": "XLK",
    "Healthcare": "XLV",
    "Consumer Discretionary": "XLY",
    "Materials": "XLB",
    "Financials": "XLF",
    "Energy": "XLE",
    "Industrials": "XLI",
    "Consumer Staples": "XLP",
    "Utilities": "XLU",
    "Real Estate": "XLRE",
    "Communication Services": "XLC",
    "Automobile": "CARZ",  # or industry proxy; fallback to XLY
    "Cement": "XLB",
}

BENCHMARK = {"US": "^GSPC", "IN": "^NSEI"}


def fetch_with_retry(ticker: str, start: str = "2009-01-01", end: Optional[str] = None, max_retries: int = 4) -> Optional[pd.DataFrame]:
    """Fetch adjusted close with exponential backoff."""
    for attempt in range(max_retries):
        try:
            df = yf.download(ticker, start=start, end=end, progress=False, auto_adjust=True, threads=False)
            if df is None or df.empty:
                logger.warning("Empty data for %s", ticker)
                return None
            if isinstance(df.columns, pd.MultiIndex):
                df = df["Close"] if "Close" in df.columns.get_level_values(0) else df.iloc[:, 0]
            else:
                df = df["Close"] if "Close" in df.columns else df.iloc[:, 0]
            df = df.to_frame(name="adj_close")
            df.index = pd.to_datetime(df.index).tz_localize(None)
            return df
        except Exception as e:
            wait = 2 ** attempt
            logger.warning("Attempt %d failed for %s: %s. Retrying in %ds", attempt + 1, ticker, e, wait)
            time.sleep(wait)
    logger.error("Failed to fetch %s after retries", ticker)
    return None


def cache_ticker(ticker: str, force: bool = False) -> bool:
    path = RAW_DIR / f"{ticker.replace('^', '')}.parquet"
    if path.exists() and not force:
        logger.info("Cache hit: %s", ticker)
        return True
    df = fetch_with_retry(ticker)
    if df is None or df.empty:
        return False
    df.to_parquet(path)
    logger.info("Cached %s (%d rows)", ticker, len(df))
    return True


def get_sector_mapping() -> pd.DataFrame:
    """Static-ish mapping. In production, enrich from yfinance.info and persist."""
    # Placeholder; real pipeline would call yf.Ticker(t).info for each and save
    mapping = pd.DataFrame({
        "ticker": ["NVDA", "AAPL", "MSFT", "JNJ", "PFE", "TSLA", "F", "GM", "VMC", "MLM"],
        "sector": ["Technology", "Technology", "Technology", "Healthcare", "Healthcare",
                   "Automobile", "Automobile", "Automobile", "Cement", "Cement"],
        "industry": ["Semiconductors", "Consumer Electronics", "Software", "Pharma",
                     "Pharma", "Auto Manufacturers", "Auto Manufacturers", "Auto Manufacturers",
                     "Building Materials", "Building Materials"],
        "country": ["US"] * 10,
    })
    mapping.to_csv("data/sector_mapping.csv", index=False)
    return mapping


def main() -> None:
    logger.info("Phase 1: Price cache")
    get_sector_mapping()
    tickers = ["^GSPC", "XLK", "XLV", "XLY", "XLB", "NVDA", "AAPL"]  # expand from events later
    failures = []
    for t in tickers:
        if not cache_ticker(t):
            failures.append(t)
    quality = Path("data/quality_report.md")
    quality.parent.mkdir(exist_ok=True)
    with quality.open("w") as f:
        f.write("# Data Quality Report\n\n")
        f.write(f"Failed tickers: {failures or 'none'}\n")
        f.write("Survivorship note: delisted tickers are logged and not silently dropped.\n")
    logger.info("Done. Failures: %s", failures)


if __name__ == "__main__":
    main()
