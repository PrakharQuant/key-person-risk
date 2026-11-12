"""Key Person Risk Index (KPRI) 0-100."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Dict

import numpy as np
import pandas as pd

WEIGHTS = {
    "severity": 0.40,
    "tail": 0.25,
    "hit_rate": 0.20,
    "persistence": 0.15,
}


def empirical_bayes_shrink(mean: float, n: int, grand_mean: float, prior_n: int = 20) -> float:
    """Shrink sector mean toward grand mean."""
    w = n / (n + prior_n)
    return w * mean + (1 - w) * grand_mean


def compute_sector_metrics(cars: pd.Series) -> Dict[str, float]:
    """cars: CAR[-1,+1] (negative is worse)."""
    n = len(cars)
    mean_car = float(cars.mean())
    p10 = float(cars.quantile(0.10))
    hit_rate = float((cars < -0.02).mean())
    persistence = max(0.0, -mean_car)
    return {
        "n": n,
        "severity": -mean_car,
        "tail": -p10,
        "hit_rate": hit_rate,
        "persistence": persistence,
    }


def normalize_to_100(series: pd.Series, higher_is_worse: bool = True) -> pd.Series:
    """Min-max to 0-100."""
    mn, mx = series.min(), series.max()
    if mx == mn:
        return pd.Series(50.0, index=series.index)
    norm = (series - mn) / (mx - mn)
    if not higher_is_worse:
        norm = 1 - norm
    return norm * 100


def build_kpri(metrics_df: pd.DataFrame) -> pd.DataFrame:
    grand_severity = metrics_df["severity"].mean()
    metrics_df["severity_shrunk"] = metrics_df.apply(
        lambda r: empirical_bayes_shrink(r["severity"], r["n"], grand_severity), axis=1
    )
    for col in ["severity_shrunk", "tail", "hit_rate", "persistence"]:
        metrics_df[f"{col}_norm"] = normalize_to_100(metrics_df[col])
    metrics_df["kpri"] = (
        WEIGHTS["severity"] * metrics_df["severity_shrunk_norm"]
        + WEIGHTS["tail"] * metrics_df["tail_norm"]
        + WEIGHTS["hit_rate"] * metrics_df["hit_rate_norm"]
        + WEIGHTS["persistence"] * metrics_df["persistence_norm"]
    )
    return metrics_df.sort_values("kpri", ascending=False)


def main() -> None:
    # Expanded synthetic demo covering major sectors from the event list
    demo = pd.DataFrame({
        "sector": [
            "Technology",
            "Healthcare",
            "Communication Services",
            "Consumer Discretionary",
            "Industrials",
            "Financials",
            "Energy",
            "Consumer Staples",
            "Automobile",
            "Cement",
        ],
        "n": [42, 38, 26, 24, 22, 20, 18, 19, 28, 16],
        "severity": [0.048, 0.041, 0.032, 0.028, 0.022, 0.018, 0.015, 0.012, 0.011, 0.007],
        "tail": [0.135, 0.110, 0.085, 0.070, 0.055, 0.045, 0.038, 0.030, 0.035, 0.022],
        "hit_rate": [0.58, 0.51, 0.42, 0.38, 0.30, 0.25, 0.22, 0.18, 0.20, 0.12],
        "persistence": [0.032, 0.028, 0.020, 0.016, 0.012, 0.010, 0.008, 0.006, 0.007, 0.004],
    })
    kpri = build_kpri(demo)
    out = Path("data/processed")
    out.mkdir(parents=True, exist_ok=True)
    kpri.to_csv(out / "kpri.csv", index=False)
    kpri.to_json(out / "kpri.json", orient="records", indent=2)
    print(kpri[["sector", "kpri", "n"]].to_string(index=False))


if __name__ == "__main__":
    main()
