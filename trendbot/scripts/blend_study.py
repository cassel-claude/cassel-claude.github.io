"""Do strategies offset each other? Blends of stock, leveraged-trend and bond strategies.

Building blocks (monthly, US 1928-2018):
  Stocks      : hold the US stock market (1x)
  Trend 2x    : 2x stocks while the market is above its 10-month average, else T-bills
  Bonds       : hold high-grade corporate bonds (returns estimated from Moody's AAA yields, 20-year par bond)
  Bond trend  : bonds while above their 10-month average, else T-bills
Blends are rebalanced back to their target mix every month.
Daily check (S&P 500, 2000-2018): the same idea with realistic daily-reset 2x funds, rebalanced monthly.
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

COST, SPREAD, FEE = 0.001, 0.005, 0.009


def bond_returns(yield_pct: pd.Series, maturity_years: int = 20) -> pd.Series:
    """Monthly total return of a par bond bought at last month's yield and repriced at this month's yield."""
    y, c = yield_pct / 100, yield_pct.shift(1) / 100
    n, yh = 2 * maturity_years - 1 / 6, y / 2
    price = (c / 2) * (1 - (1 + yh) ** (-n)) / yh + (1 + yh) ** (-n)
    return price - 1 + c / 12


def switch(r_in: pd.Series, r_out: pd.Series, on: pd.Series) -> pd.Series:
    sw = on.astype(float).diff().abs().fillna(0.0)
    return pd.Series(np.where(on, r_in, r_out), index=r_in.index) - COST * sw


def blend(sleeves: pd.DataFrame, weights: dict, rebalance: pd.Series) -> pd.Series:
    w = np.array([weights.get(c, 0.0) for c in sleeves.columns])
    vals, out, R, reb = w.copy(), [], sleeves.fillna(0.0).to_numpy(), rebalance.to_numpy()
    for i in range(len(R)):
        start = vals.sum()
        vals = vals * (1 + R[i])
        out.append(vals.sum() / start - 1)
        if reb[i]:
            vals = w * vals.sum()
    return pd.Series(out, index=sleeves.index)


def table(series: dict, ppy: int, a: str, b: str) -> str:
    rows = {}
    for k, r in series.items():
        s = metrics.summarize(r.loc[a:b], ppy)
        roll = (1 + r.loc[a:b]).rolling(ppy).apply(np.prod, raw=True) - 1
        s["worst_12m"] = roll.min()
        rows[k] = s
    df = pd.DataFrame(rows).T
    t = metrics.format_table(df.drop(columns=["worst_12m"]))
    t["Worst 12 months"] = [f"{x:.1%}" for x in df["worst_12m"]]
    return metrics.to_markdown(t)


def monthly_study() -> str:
    mc = bundled.market_and_cash()
    mkt, rf = mc["market"], mc["cash"]
    bonds = bond_returns(bundled.corporate_yields()["AAA"]).reindex(mkt.index)
    stocks_up = (signals.above_average(signals.level_from_returns(mkt), 10) == 1.0).shift(1, fill_value=False)
    bonds_up = (signals.above_average(signals.level_from_returns(bonds.fillna(0.0)), 10) == 1.0).shift(1, fill_value=False)
    lev2 = 2 * mkt - (rf + SPREAD / 12) - FEE / 12
    sleeves = pd.DataFrame({
        "Stocks": mkt,
        "Trend 2x": switch(lev2, rf, stocks_up),
        "Bonds": bonds,
        "Bond trend": switch(bonds, rf, bonds_up),
    }).loc["1927-07":]
    every = pd.Series(True, index=sleeves.index)
    mixes = {
        "Stocks only": {"Stocks": 1.0},
        "Trend 2x only": {"Trend 2x": 1.0},
        "Classic 60/40 stocks/bonds": {"Stocks": 0.6, "Bonds": 0.4},
        "50% stocks + 50% trend 2x": {"Stocks": 0.5, "Trend 2x": 0.5},
        "40% stocks + 40% trend 2x + 20% bonds": {"Stocks": 0.4, "Trend 2x": 0.4, "Bonds": 0.2},
        "1/3 stocks + 1/3 trend 2x + 1/3 bond trend": {"Stocks": 1 / 3, "Trend 2x": 1 / 3, "Bond trend": 1 / 3},
    }
    series = {k: blend(sleeves, w, every) for k, w in mixes.items()}
    out = ["## How the building blocks move together (monthly, 1928-2018)", "",
           "Correlation of monthly returns (1 = move in lockstep, 0 = unrelated, negative = offset):", "",
           metrics.to_markdown(sleeves.loc["1928-01":"2018-11"].corr().round(2)), "",
           "Average monthly return of each block in the stock market's worst 5% of months:", ""]
    worst = sleeves.loc["1928-01":"2018-11"]
    cut = worst["Stocks"].quantile(0.05)
    avg_bad = worst[worst["Stocks"] <= cut].mean().map(lambda x: f"{x:+.1%}")
    out += [metrics.to_markdown(avg_bad.to_frame("In the worst 5% of stock months").T), ""]
    for label, a, b in [("1928-2018", "1928-01", "2018-11"), ("1928-1949", "1928-01", "1949-12"),
                        ("1950-1979 (rising interest rates)", "1950-01", "1979-12"),
                        ("1980-1999 (falling interest rates)", "1980-01", "1999-12"),
                        ("2000-2018", "2000-01", "2018-11")]:
        out += [f"## Blends, {label}", "", table(series, 12, a, b), ""]
    return "\n".join(out)


def daily_study() -> str:
    px = bundled.daily_close("sp500")
    mc = bundled.market_and_cash()
    per = px.index.to_period("M")
    rf_m = pd.Series(mc["cash"].values, index=mc.index.to_period("M"))
    days = pd.Series(1, index=px.index).groupby(per).transform("count")
    rf = pd.Series([(1 + rf_m.get(p, rf_m.iloc[-1])) ** (1 / d) - 1 for p, d in zip(per, days)], index=px.index)
    r1 = px.pct_change().fillna(0.0) + 1.019 ** (1 / 252) - 1
    r2 = 2 * r1 - (rf + SPREAD / 252) - FEE / 252
    is_me = pd.Series(per != pd.Series(per).shift(-1).to_numpy(), index=px.index)
    up = (px > px.rolling(200).mean()).where(is_me).ffill().shift(2).fillna(False).astype(bool)
    sleeves = pd.DataFrame({"Stocks": r1, "Trend 2x": switch(r2, rf, up)})
    series = {
        "Stocks only (S&P 500)": blend(sleeves, {"Stocks": 1.0}, is_me),
        "Trend 2x only": blend(sleeves, {"Trend 2x": 1.0}, is_me),
        "50% stocks + 50% trend 2x": blend(sleeves, {"Stocks": 0.5, "Trend 2x": 0.5}, is_me),
    }
    out = []
    for label, a, b in [("2000-2018", "2000-01-03", "2018-12-31"), ("2000-2002 crash", "2000-01-03", "2002-12-31"),
                        ("2008 crisis", "2007-10-01", "2009-03-31"), ("Apr 2009-2018", "2009-04-01", "2018-12-31")]:
        out += [f"## S&P 500 daily (realistic 2x fund), {label}", "", table(series, 252, a, b), ""]
    return "\n".join(out)


def main() -> None:
    text = "\n".join(["# Blend study", "", __doc__.strip(), "", monthly_study(), daily_study()])
    (ROOT / "reports").mkdir(exist_ok=True)
    (ROOT / "reports" / "blend_study.md").write_text(text)
    print(text)


if __name__ == "__main__":
    main()
