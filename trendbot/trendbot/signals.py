"""Trend and indicator signals.

Every function uses only data up to and including each row's date, so a signal at date t can be acted on
after the close of t. Rule functions return floats: 1.0 / 0.0, or NaN where there is not yet enough history.
"""
from __future__ import annotations

import numpy as np


def level_from_returns(returns):
    return (1 + returns).cumprod()


def above_average(level, window: int):
    """1.0 where the level is above its trailing `window`-period simple average."""
    avg = level.rolling(window).mean()
    return (level > avg).astype(float).where(avg.notna())


def trailing_return(returns, window: int):
    return (1 + returns).rolling(window).apply(np.prod, raw=True) - 1


def multi_horizon_momentum(level, windows=(3, 6, 12)):
    """Average trailing return over several look-back windows (in periods)."""
    return sum(level.pct_change(w) for w in windows) / len(windows)


# ---- "Prediction data" rules: 1.0 means the indicator says conditions look BAD ----

def credit_stress(baa_yield, aaa_yield, window: int = 12):
    """Corporate credit spread (BAA minus AAA) above its trailing average: credit stress building."""
    spread = baa_yield - aaa_yield
    avg = spread.rolling(window).mean()
    return (spread > avg).astype(float).where(avg.notna())


def curve_inverted(long_yield, short_yield):
    """Long-term yield below the short-term yield (yield-curve inversion)."""
    valid = long_yield.notna() & short_yield.notna()
    return (long_yield < short_yield).astype(float).where(valid)


def inflation_rising(price_index, window: int = 12, release_lag: int = 1):
    """Year-over-year inflation above its trailing average. `release_lag` periods of delay model the fact
    that a month's CPI is published in the middle of the following month."""
    yoy = price_index.pct_change(12).shift(release_lag)
    avg = yoy.rolling(window).mean()
    return (yoy > avg).astype(float).where(avg.notna())
