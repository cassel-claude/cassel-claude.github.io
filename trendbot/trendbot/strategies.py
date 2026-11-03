"""Strategies: turn price history into period-end target weights (decided after the close)."""
from __future__ import annotations

import pandas as pd

from . import signals


def trend_filter(level: pd.Series, window: int = 10) -> pd.Series:
    """Own the asset (weight 1) while it is above its `window`-period average, otherwise cash (0)."""
    return signals.above_average(level, window).fillna(0.0)


def rotation(levels: pd.DataFrame, top_n: int = 3, lookbacks=(3, 6, 12), trend_window: int = 10) -> pd.DataFrame:
    """Cross-market rotation.

    Each period: rank assets by average trailing return over `lookbacks`; hold the top `top_n` among those
    that are above their `trend_window` average, at 1/top_n each. Empty slots stay in cash, so when most
    markets are falling, most of the money is parked in T-bills.
    """
    momentum = signals.multi_horizon_momentum(levels, lookbacks)
    trending = signals.above_average(levels, trend_window) == 1.0
    rank = momentum.where(trending).rank(axis=1, ascending=False, method="first")
    return (rank <= top_n).astype(float) / top_n
