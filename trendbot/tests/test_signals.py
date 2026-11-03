import numpy as np
import pandas as pd

from trendbot import signals


def test_above_average_uses_only_past_data():
    s = pd.Series(np.arange(1, 31, dtype=float))
    changed = s.copy()
    changed.iloc[20:] = 0.0
    pd.testing.assert_series_equal(signals.above_average(s, 5).iloc[:20], signals.above_average(changed, 5).iloc[:20])


def test_above_average_is_undefined_until_enough_history():
    out = signals.above_average(pd.Series([1.0, 2, 3, 4, 5]), 3)
    assert out.iloc[:2].isna().all() and out.iloc[2] == 1.0


def test_inflation_rule_applies_publication_lag():
    rng = np.random.default_rng(0)
    idx = pd.period_range("2000-01", periods=60, freq="M").to_timestamp(how="end")
    cpi = pd.Series(100 * np.cumprod(1 + rng.normal(0.002, 0.002, 60)), index=idx)
    pd.testing.assert_series_equal(
        signals.inflation_rising(cpi, 12, release_lag=1), signals.inflation_rising(cpi.shift(1), 12, release_lag=0)
    )


def test_credit_stress_flags_a_widening_spread():
    aaa = pd.Series(4.0, index=range(30))
    baa = pd.Series([5.0] * 20 + [7.0] * 10, index=range(30))
    out = signals.credit_stress(baa, aaa, 12)
    assert out.iloc[19] == 0.0 and out.iloc[20] == 1.0


def test_curve_inverted():
    out = signals.curve_inverted(pd.Series([3.0, 2.0]), pd.Series([2.5, 2.5]))
    assert out.tolist() == [0.0, 1.0]
