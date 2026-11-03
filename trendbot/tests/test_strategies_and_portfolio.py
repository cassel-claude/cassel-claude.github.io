import datetime as dt

import numpy as np
import pandas as pd
import pytest

from trendbot import portfolio, strategies

MONTHS = pd.period_range("2010-01", periods=24, freq="M").to_timestamp(how="end").normalize()
T = np.arange(24)

CFG = {
    "strategy": {
        "universe": ["VOO", "SOXX", "GLD", "TLT"],
        "cash_proxy": "SGOV",
        "top_n": 3,
        "lookbacks_months": [3, 6, 12],
        "trend_window_months": 10,
    },
    "limits": {"max_weight_per_asset": 0.40, "max_total_invested": 0.99, "per_asset_caps": {"SOXX": 0.34}},
}


def test_rotation_holds_the_strongest_trending_assets_equally():
    levels = pd.DataFrame({"fast": 100 * 1.03 ** T, "slow": 100 * 1.01 ** T, "down": 100 * 0.98 ** T,
                           "noise": 100 + np.sin(T)}, index=MONTHS)
    w = strategies.rotation(levels, top_n=2).iloc[-1]
    assert w["fast"] == 0.5 and w["slow"] == 0.5 and w["down"] == 0.0 and w["noise"] == 0.0


def test_rotation_goes_to_cash_when_nothing_is_trending_up():
    levels = pd.DataFrame({"a": 100 * 0.98 ** T, "b": 100 * 0.99 ** T}, index=MONTHS)
    assert strategies.rotation(levels, top_n=3).iloc[-1].sum() == 0.0


def _daily(growth_per_month: dict[str, float]) -> pd.DataFrame:
    idx = pd.bdate_range("2023-01-02", "2026-10-30")
    t = np.arange(len(idx)) / 21
    return pd.DataFrame({sym: 100 * (1 + g) ** t for sym, g in growth_per_month.items()}, index=idx)


def test_targets_are_capped_and_fully_allocated():
    closes = _daily({"VOO": 0.01, "SOXX": 0.03, "GLD": 0.02, "TLT": -0.01, "SGOV": 0.003})
    tw = portfolio.target_weights(CFG, closes, dt.date(2026, 11, 2))
    assert set(tw) == {"VOO", "SOXX", "GLD"}
    assert sum(tw.values()) == pytest.approx(0.99)
    assert tw["SOXX"] <= 0.34


def test_unused_slots_are_parked_in_the_cash_proxy():
    closes = _daily({"VOO": 0.01, "SOXX": -0.03, "GLD": -0.02, "TLT": -0.01, "SGOV": 0.003})
    tw = portfolio.target_weights(CFG, closes, dt.date(2026, 11, 2))
    assert tw["VOO"] == pytest.approx(1 / 3)
    assert tw["SGOV"] == pytest.approx(0.99 - 1 / 3, abs=1e-6)


def test_refuses_to_trade_on_stale_data():
    closes = _daily({"VOO": 0.01, "SOXX": 0.03, "GLD": 0.02, "TLT": -0.01, "SGOV": 0.003}).loc[:"2026-08-31"]
    with pytest.raises(RuntimeError):
        portfolio.target_weights(CFG, closes, dt.date(2026, 11, 2))
