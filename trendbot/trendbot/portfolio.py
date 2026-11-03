"""Build this month's target portfolio from the config and daily closes."""
from __future__ import annotations

import datetime as dt

import pandas as pd

from . import risk, strategies


def completed_month_ends(closes: pd.DataFrame, today: dt.date) -> pd.DataFrame:
    """Month-end closes for months that have fully ended before `today`."""
    monthly = closes.resample("ME").last()
    return monthly[monthly.index < pd.Timestamp(today.replace(day=1))]


def target_weights(cfg: dict, closes: pd.DataFrame, today: dt.date) -> dict[str, float]:
    s, lim = cfg["strategy"], cfg["limits"]
    monthly = completed_month_ends(closes[s["universe"]], today)
    expected = pd.Timestamp(today.replace(day=1)) - pd.Timedelta(days=1)
    if monthly.empty or monthly.index[-1].to_period("M") != expected.to_period("M"):
        raise RuntimeError(f"missing month-end data for {expected:%Y-%m}")
    w = strategies.rotation(monthly, top_n=s["top_n"], lookbacks=tuple(s["lookbacks_months"]),
                            trend_window=s["trend_window_months"]).iloc[-1]
    limits = risk.Limits(
        max_weight_per_asset=lim["max_weight_per_asset"],
        max_total_invested=lim["max_total_invested"],
        allowed_symbols=frozenset(s["universe"]),
        per_asset_caps=lim.get("per_asset_caps") or {},
    )
    target = risk.apply_limits({k: float(v) for k, v in w.items() if v > 0}, limits)
    residual = round(lim["max_total_invested"] - sum(target.values()), 6)
    if s.get("cash_proxy") and residual > 0:
        target[s["cash_proxy"]] = residual
    return target
