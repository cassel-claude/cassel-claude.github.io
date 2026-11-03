"""Design study: the strongest combination of the strategies that survived testing.

Designs (chosen before running; monthly data, US 1928-2018, bonds estimated from Moody's AAA yields):
  A  Trend 2x -> T-bills          : 2x stocks while the market is above its 10-month average, else T-bills
  B  Trend 2x -> bonds            : same, but when stocks trend down, hold bonds if bonds are trending up, else T-bills
  C  Three-way (bills)            : 1/3 stocks + 1/3 design A + 1/3 bond trend
  D  Three-way (bonds)            : 1/3 stocks + 1/3 design B + 1/3 bond trend
Robustness: designs B and D re-run with trend windows of 8/10/12 months and leverage of 1.5x/2x/2.5x.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from trendbot import metrics, signals  # noqa: E402
from trendbot.data import bundled  # noqa: E402

sys.path.insert(0, str(ROOT / "scripts"))
from blend_study import COST, FEE, SPREAD, blend, bond_returns  # noqa: E402


def longest_underwater(r: pd.Series) -> int:
    w = (1 + r).cumprod()
    under = w < w.cummax()
    longest = run = 0
    for u in under:
        run = run + 1 if u else 0
        longest = max(longest, run)
    return longest


def pick(on: pd.Series, a: pd.Series, b: pd.Series) -> pd.Series:
    return pd.Series(np.where(on, a, b), index=a.index)


def designs(window: int = 10, lev: float = 2.0) -> dict:
    mc = bundled.market_and_cash()
    mkt, rf = mc["market"], mc["cash"]
    bonds = bond_returns(bundled.corporate_yields()["AAA"]).reindex(mkt.index).fillna(0.0)
    s_up = (signals.above_average(signals.level_from_returns(mkt), window) == 1.0).shift(1, fill_value=False)
    b_up = (signals.above_average(signals.level_from_returns(bonds), window) == 1.0).shift(1, fill_value=False)
    levered = lev * mkt - (lev - 1) * (rf + SPREAD / 12) - FEE / 12
    bond_trend = pick(b_up, bonds, rf) - COST * b_up.astype(float).diff().abs().fillna(0.0)
    sw = s_up.astype(float).diff().abs().fillna(0.0)
    a = pick(s_up, levered, rf) - COST * sw
    b = pick(s_up, levered, bond_trend) - COST * sw
    sleeves = pd.DataFrame({"stocks": mkt, "A": a, "B": b, "bond_trend": bond_trend}).loc["1927-07":]
    every = pd.Series(True, index=sleeves.index)
    third = 1 / 3
    return {
        "Stocks only (benchmark)": sleeves["stocks"],
        "60/40 stocks/bonds (benchmark)": blend(pd.DataFrame({"s": mkt, "b": bonds}).loc["1927-07":],
                                                 {"s": 0.6, "b": 0.4}, every),
        "A: Trend 2x -> T-bills": sleeves["A"],
        "B: Trend 2x -> bonds": sleeves["B"],
        "C: Three-way (bills)": blend(sleeves, {"stocks": third, "A": third, "bond_trend": third}, every),
        "D: Three-way (bonds)": blend(sleeves, {"stocks": third, "B": third, "bond_trend": third}, every),
    }


def table(series: dict, a: str, b: str) -> str:
    rows = {}
    for k, r in series.items():
        r = r.loc[a:b]
        s = metrics.summarize(r, 12)
        s["worst_12m"] = ((1 + r).rolling(12).apply(np.prod, raw=True) - 1).min()
        s["underwater"] = longest_underwater(r)
        rows[k] = s
    df = pd.DataFrame(rows).T
    t = metrics.format_table(df.drop(columns=["worst_12m", "underwater"]))
    t["Worst 12 months"] = [f"{x:.1%}" for x in df["worst_12m"]]
    t["Longest time below a peak"] = [f"{int(m) // 12}y {int(m) % 12}m" for m in df["underwater"]]
    return metrics.to_markdown(t)


def main() -> None:
    base = designs()
    out = ["# Design study", "", __doc__.strip(), ""]
    for label, a, b in [("1928-2018", "1928-01", "2018-11"), ("1928-1949", "1928-01", "1949-12"),
                        ("1950-1979 (rising rates, inflation)", "1950-01", "1979-12"),
                        ("1980-1999 (falling rates)", "1980-01", "1999-12"), ("2000-2018", "2000-01", "2018-11")]:
        out += [f"## {label}", "", table(base, a, b), ""]
    rows = {}
    for window in (8, 10, 12):
        for lev in (1.5, 2.0, 2.5):
            d = designs(window, lev)
            for name in ("B: Trend 2x -> bonds", "D: Three-way (bonds)"):
                r = d[name].loc["1928-01":"2018-11"]
                s = metrics.summarize(r, 12)
                rows[(name[:1], f"{window}-month", f"{lev}x")] = {
                    "Annual return": f"{s['annual_return']:.1%}", "Worst drop": f"{s['worst_drop']:.1%}"}
    rob = pd.DataFrame(rows).T
    rob.index = [f"{d} | {w} | {l}" for d, w, l in rob.index]
    out += ["## Robustness, 1928-2018 (design | trend window | leverage)", "", metrics.to_markdown(rob), ""]
    text = "\n".join(out)
    (ROOT / "reports" / "design_study.md").write_text(text)
    print(text)


if __name__ == "__main__":
    main()
