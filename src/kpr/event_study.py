"""Market-model event study: AR, CAR, significance."""
from __future__ import annotations

import logging
from typing import Dict, Tuple

import numpy as np
import pandas as pd
from scipy import stats

logger = logging.getLogger(__name__)


def market_model_beta(
    stock_ret: pd.Series, market_ret: pd.Series, min_obs: int = 120
) -> Tuple[float, float]:
    """OLS beta and alpha over estimation window. Returns (alpha, beta)."""
    df = pd.concat([stock_ret, market_ret], axis=1, keys=["s", "m"]).dropna()
    if len(df) < min_obs:
        raise ValueError(f"Insufficient observations: {len(df)} < {min_obs}")
    y = df["s"].values
    X = np.column_stack([np.ones(len(df)), df["m"].values])
    coef, _, _, _ = np.linalg.lstsq(X, y, rcond=None)
    return float(coef[0]), float(coef[1])


def abnormal_returns(
    stock_ret: pd.Series, market_ret: pd.Series, alpha: float, beta: float
) -> pd.Series:
    """AR = stock - (alpha + beta * market)."""
    return stock_ret - (alpha + beta * market_ret)


def cumulative_abnormal_return(ar: pd.Series, start: int, end: int, event_idx: int) -> float:
    """CAR over relative days [start, end] inclusive."""
    window = ar.iloc[event_idx + start : event_idx + end + 1]
    return float(window.sum())


def cross_sectional_ttest(cars: np.ndarray) -> Dict[str, float]:
    """Mean, t-stat, p-value."""
    n = len(cars)
    mean = float(np.mean(cars))
    se = float(np.std(cars, ddof=1) / np.sqrt(n)) if n > 1 else np.nan
    tstat = mean / se if se and se > 0 else np.nan
    pval = 2 * (1 - stats.t.cdf(abs(tstat), n - 1)) if not np.isnan(tstat) else np.nan
    return {"n": n, "mean": mean, "tstat": tstat, "pval": pval}


def bootstrap_ci(cars: np.ndarray, n_boot: int = 1000, alpha: float = 0.05) -> Tuple[float, float]:
    """Percentile bootstrap CI for the mean."""
    rng = np.random.default_rng(42)
    means = [np.mean(rng.choice(cars, size=len(cars), replace=True)) for _ in range(n_boot)]
    return float(np.percentile(means, 100 * alpha / 2)), float(np.percentile(means, 100 * (1 - alpha / 2)))


def winsorize(series: pd.Series, lower: float = 0.01, upper: float = 0.99) -> pd.Series:
    lo, hi = series.quantile([lower, upper])
    return series.clip(lo, hi)


def main() -> None:
    logger.info("Phase 3: event study skeleton (full run after prices + events)")
    # In full pipeline: load prices, align event day 0, compute per-event CAR, save processed


if __name__ == "__main__":
    main()
