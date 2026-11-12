"""Unit tests with synthetic data of known answers."""
import numpy as np
import pandas as pd
import pytest

from kpr.event_study import (
    abnormal_returns,
    bootstrap_ci,
    cumulative_abnormal_return,
    cross_sectional_ttest,
    market_model_beta,
)


def test_market_model_beta_known():
    rng = np.random.default_rng(0)
    m = rng.normal(0.001, 0.01, 200)
    s = 0.0005 + 1.2 * m + rng.normal(0, 0.005, 200)
    stock = pd.Series(s)
    market = pd.Series(m)
    alpha, beta = market_model_beta(stock, market, min_obs=120)
    assert abs(beta - 1.2) < 0.15  # estimation noise
    assert abs(alpha - 0.0005) < 0.001


def test_car_math():
    ar = pd.Series([0.01, -0.02, 0.03, -0.01, 0.00])
    # event at index 2
    car = cumulative_abnormal_return(ar, -1, 1, event_idx=2)
    assert abs(car - ( -0.02 + 0.03 + -0.01)) < 1e-9


def test_cross_sectional():
    cars = np.array([-0.05, -0.03, -0.01, 0.02])
    res = cross_sectional_ttest(cars)
    assert res["n"] == 4
    assert res["mean"] == pytest.approx(-0.0175)


def test_bootstrap_ci_covers_mean():
    cars = np.array([-0.04, -0.02, 0.01, -0.03])
    lo, hi = bootstrap_ci(cars, n_boot=500)
    mean = cars.mean()
    assert lo < mean < hi
