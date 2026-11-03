"""Backtest the cross-market rotation on real ETF prices (needs Alpaca data access, or a CSV of closes).

Compares, from the first month every fund has enough history:
  - VOO buy & hold
  - VOO trend filter (VOO or T-bills, 10-month average)
  - Rotation over the config's universe (top 3 trending funds, rest in T-bills)

Usage:
  python scripts/backtest_rotation.py                 # downloads daily closes from Alpaca (cached in data_cache/)
  python scripts/backtest_rotation.py --csv FILE      # date-indexed CSV of daily closes, one column per symbol
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pandas as pd
import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from trendbot import backtest, metrics, strategies  # noqa: E402

COST = 0.001


def load_closes(symbols, csv: str | None) -> pd.DataFrame:
    if csv:
        return pd.read_csv(csv, index_col=0, parse_dates=True)[symbols]
    cache = ROOT / "data_cache" / "alpaca_daily_closes.csv"
    if cache.exists():
        return pd.read_csv(cache, index_col=0, parse_dates=True)[symbols]
    from trendbot.data import alpaca

    closes = alpaca.daily_closes(symbols, start="2016-01-01",
                                 end=(pd.Timestamp.today().normalize() - pd.Timedelta(days=1)).date().isoformat())
    cache.parent.mkdir(exist_ok=True)
    closes.to_csv(cache)
    return closes


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv")
    args = ap.parse_args()
    cfg = yaml.safe_load((ROOT / "config.yaml").read_text())
    s = cfg["strategy"]
    cash_sym = s["cash_proxy"]
    closes = load_closes(list(s["universe"]) + [cash_sym], args.csv)
    monthly = closes.resample("ME").last()
    rets = monthly.pct_change()
    cash = rets[cash_sym].fillna(0.0)  # T-bill ETF; before it existed this treats cash as earning 0%
    universe = monthly[s["universe"]]

    weights = {
        "VOO buy & hold": pd.Series(1.0, index=monthly.index).where(universe["VOO"].notna(), 0.0),
        "VOO trend filter": strategies.trend_filter(universe["VOO"], s["trend_window_months"]),
        "Rotation (top 3 trending, rest T-bills)": strategies.rotation(
            universe, top_n=s["top_n"], lookbacks=tuple(s["lookbacks_months"]),
            trend_window=s["trend_window_months"]),
    }
    start = universe.dropna().index[max(s["lookbacks_months"]) + 1]
    res = {}
    for name, w in weights.items():
        asset_rets = rets["VOO"] if name.startswith("VOO") else rets[s["universe"]]
        net, held = backtest.run(w, asset_rets, cash, COST)
        res[name] = metrics.summarize(net.loc[start:], 12, held.loc[start:])
    table = metrics.format_table(pd.DataFrame(res).T)
    text = f"# Rotation backtest, {start:%Y-%m} to {monthly.index[-1]:%Y-%m}\n\n{metrics.to_markdown(table)}\n"
    (ROOT / "reports").mkdir(exist_ok=True)
    (ROOT / "reports" / "rotation_backtest.md").write_text(text)
    print(text)


if __name__ == "__main__":
    main()
