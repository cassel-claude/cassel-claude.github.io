import numpy as np
import pandas as pd
import pytest

from trendbot import backtest


def test_weight_is_held_the_period_after_it_is_decided():
    idx = pd.RangeIndex(4)
    r = pd.Series([0.10, 0.10, -0.10, 0.10], index=idx)
    w = pd.Series([1.0, 0.0, 0.0, 0.0], index=idx)  # decided at end of period 0 -> held during period 1 only
    net, held = backtest.run(w, r, pd.Series(0.0, index=idx), cost_per_trade=0.0)
    assert held.iloc[:, 0].tolist() == [0.0, 1.0, 0.0, 0.0]
    assert net.tolist() == pytest.approx([0.0, 0.10, 0.0, 0.0])


def test_unspent_weight_earns_cash():
    idx = pd.RangeIndex(3)
    w = pd.Series([0.25, 0.25, 0.25], index=idx)
    net, _ = backtest.run(w, pd.Series(0.0, index=idx), pd.Series(0.01, index=idx), cost_per_trade=0.0)
    assert net.iloc[1] == pytest.approx(0.0075)


def test_costs_are_charged_on_buys_and_sells():
    idx = pd.RangeIndex(3)
    zero = pd.Series(0.0, index=idx)
    net, _ = backtest.run(pd.Series([1.0, 0.0, 0.0], index=idx), zero, zero, cost_per_trade=0.01)
    assert net.tolist() == pytest.approx([0.0, -0.01, -0.01])


def test_rejects_shorting_and_leverage():
    idx = pd.RangeIndex(2)
    zero = pd.Series(0.0, index=idx)
    with pytest.raises(ValueError):
        backtest.run(pd.Series([-0.5, 0.0], index=idx), zero, zero)
    w = pd.DataFrame({"a": [0.7, 0.0], "b": [0.7, 0.0]}, index=idx)
    with pytest.raises(ValueError):
        backtest.run(w, pd.DataFrame({"a": zero, "b": zero}), zero)


def test_rejects_holding_an_asset_with_missing_data():
    idx = pd.RangeIndex(3)
    rets = pd.DataFrame({"a": [0.01, np.nan, 0.01]}, index=idx)
    with pytest.raises(ValueError):
        backtest.run(pd.DataFrame({"a": [1.0, 1.0, 1.0]}, index=idx), rets, pd.Series(0.0, index=idx))
