"""Backtest engine: rebalance to target weights each period; long-only; unspent weight earns the cash rate."""
from __future__ import annotations

import pandas as pd


def run(target_weights, asset_returns, cash_returns, cost_per_trade: float = 0.001):
    """Simulate holding `target_weights`.

    target_weights[t] is decided with information up to the END of period t and is held during period t+1.
    Rows with no decision yet (NaN) are treated as all-cash.
    cost_per_trade is charged on every dollar bought or sold of a risky asset (cash moves are free).
    Returns (net_returns, held_weights).
    """
    if isinstance(target_weights, pd.Series):
        target_weights = target_weights.to_frame("asset")
    if isinstance(asset_returns, pd.Series):
        asset_returns = asset_returns.to_frame(target_weights.columns[0])
    w = target_weights.reindex(index=asset_returns.index, columns=asset_returns.columns).astype(float).fillna(0.0)
    if (w < -1e-12).any().any():
        raise ValueError("negative weights: shorting is not supported")
    if (w.sum(axis=1) > 1 + 1e-9).any():
        raise ValueError("weights sum above 1: leverage is not supported")
    held = w.shift(1).fillna(0.0)
    if ((held > 0) & asset_returns.isna()).any().any():
        raise ValueError("weight assigned to an asset with no return data for that period")
    cash_w = 1.0 - held.sum(axis=1)
    gross = (held * asset_returns.fillna(0.0)).sum(axis=1) + cash_w * cash_returns.reindex(held.index).fillna(0.0)
    traded = held.diff().abs().sum(axis=1)
    traded.iloc[0] = held.iloc[0].abs().sum()
    return gross - cost_per_trade * traded, held
