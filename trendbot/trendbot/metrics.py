"""Performance statistics and simple table formatting."""
from __future__ import annotations

import numpy as np
import pandas as pd


def summarize(returns: pd.Series, periods_per_year: int, weights=None) -> dict:
    r = returns.dropna()
    if r.empty:
        raise ValueError("no returns to summarize")
    wealth = (1 + r).cumprod()
    years = len(r) / periods_per_year
    out = {
        "annual_return": wealth.iloc[-1] ** (1 / years) - 1,
        "volatility": r.std() * np.sqrt(periods_per_year),
        "worst_drop": (wealth / wealth.cummax() - 1).min(),
        "growth_of_1000": 1000 * wealth.iloc[-1],
    }
    if weights is not None:
        w = weights.to_frame() if isinstance(weights, pd.Series) else weights
        w = w.reindex(r.index).fillna(0.0)
        out["invested"] = w.sum(axis=1).mean()
        out["traded_per_year"] = w.diff().abs().sum(axis=1).sum() / years
    return out


LABELS = {
    "annual_return": "Annual return",
    "volatility": "Volatility",
    "worst_drop": "Worst drop",
    "growth_of_1000": "$1,000 became",
    "invested": "Avg invested",
    "traded_per_year": "Traded/yr",
}


def format_table(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    for c in out.columns:
        if c in ("annual_return", "volatility", "worst_drop", "invested"):
            out[c] = out[c].map(lambda x: f"{x:.1%}")
        elif c == "growth_of_1000":
            out[c] = out[c].map(lambda x: f"${x:,.0f}")
        elif c == "traded_per_year":
            out[c] = out[c].map(lambda x: f"{x:.1f}x")
    return out.rename(columns=LABELS)


def to_markdown(df: pd.DataFrame) -> str:
    cols = [""] + [str(c) for c in df.columns]
    lines = ["| " + " | ".join(cols) + " |", "|" + "---|" * len(cols)]
    for idx, row in df.iterrows():
        lines.append("| " + " | ".join([str(idx)] + [str(v) for v in row]) + " |")
    return "\n".join(lines)
