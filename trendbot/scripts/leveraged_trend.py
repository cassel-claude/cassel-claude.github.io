"""Aiming above the index: leveraged index funds, held only while the trend is up.

Daily data (S&P 500 and Nasdaq, 2000-2018), modeled like real daily-reset leveraged ETFs (SSO/UPRO, QLD/TQQQ):
  L x fund daily return = L x index return - (L-1) x (T-bill + 0.5%/yr financing) - 0.9%/yr fees
Trend rule: checked at each month-end close (index vs its 200-day average), trade the next day,
            otherwise hold T-bills. 0.10% cost per switch.
Monthly data (US market 1928-2018): rough check with monthly-rebalanced leverage (ignores daily-reset effects).
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


def run(r_inv: pd.Series, r_cash: pd.Series, invested: pd.Series) -> pd.Series:
    sw = invested.astype(float).diff().abs().fillna(0.0)
    return pd.Series(np.where(invested, r_inv, r_cash), index=r_inv.index) - COST * sw


def daily(name: str, div: float, periods) -> str:
    px = bundled.daily_close(name)
    mc = bundled.market_and_cash()
    per = px.index.to_period("M")
    rf_m = pd.Series(mc["cash"].values, index=mc.index.to_period("M"))
    days = pd.Series(1, index=px.index).groupby(per).transform("count")
    rf = pd.Series([(1 + rf_m.get(p, rf_m.iloc[-1])) ** (1 / d) - 1 for p, d in zip(per, days)], index=px.index)
    idx_r = px.pct_change().fillna(0.0) + (1 + div) ** (1 / 252) - 1
    lev = {L: L * idx_r - (L - 1) * (rf + SPREAD / 252) - (FEE / 252 if L > 1 else 0.0) for L in (1, 2, 3)}
    is_me = pd.Series(per != pd.Series(per).shift(-1).to_numpy(), index=px.index)
    up = (px > px.rolling(200).mean()).where(is_me).ffill().shift(2).fillna(False).astype(bool)
    always = pd.Series(True, index=px.index)
    strategies = {f"Hold {L}x": run(lev[L], rf, always) for L in (1, 2, 3)}
    strategies.update({f"Trend {L}x (else T-bills)": run(lev[L], rf, up) for L in (1, 2, 3)})
    out = []
    for label, a, b in periods:
        rows = {}
        for k, r in strategies.items():
            s = metrics.summarize(r.loc[a:b], 252)
            s["worst_day"] = r.loc[a:b].min()
            rows[k] = s
        t = metrics.format_table(pd.DataFrame(rows).T.drop(columns=["volatility"]))
        t["Worst day"] = [f"{x:.1%}" for x in pd.DataFrame(rows).T["worst_day"]]
        t = t.drop(columns=["worst_day"])
        out += [f"## {name.upper()} {label}", "", metrics.to_markdown(t), ""]
    return "\n".join(out)


def monthly() -> str:
    mc = bundled.market_and_cash()
    mkt, rf = mc["market"], mc["cash"]
    up = (signals.above_average(signals.level_from_returns(mkt), 10) == 1.0).shift(1).fillna(False).astype(bool)
    lev = {L: L * mkt - (L - 1) * (rf + SPREAD / 12) - (FEE / 12 if L > 1 else 0.0) for L in (1, 2)}
    always = pd.Series(True, index=mkt.index)
    out = []
    for label, a, b in [("1928-2018", "1928-01", "2018-11"), ("1928-1949", "1928-01", "1949-12"),
                        ("1950-1999", "1950-01", "1999-12"), ("2000-2018", "2000-01", "2018-11")]:
        rows = {f"Hold {L}x": metrics.summarize(run(lev[L], rf, always).loc[a:b], 12) for L in (1, 2)}
        rows.update({f"Trend {L}x (else T-bills)": metrics.summarize(run(lev[L], rf, up).loc[a:b], 12) for L in (1, 2)})
        t = metrics.format_table(pd.DataFrame(rows).T.drop(columns=["volatility"]))
        out += [f"## US market (monthly, rough) {label}", "", metrics.to_markdown(t), ""]
    return "\n".join(out)


def main() -> None:
    text = "\n".join([
        "# Leveraged trend study", "", __doc__.strip(), "",
        daily("sp500", 0.019, [("2000-2018", "2000-01-03", "2018-12-31"), ("2000-2002 crash", "2000-01-03", "2002-12-31"),
                               ("2008 crisis", "2007-10-01", "2009-03-31"), ("Apr 2009-2018", "2009-04-01", "2018-12-31")]),
        daily("nasdaq", 0.008, [("2000-2018", "2000-01-03", "2018-12-31"), ("2003-2018", "2003-01-02", "2018-12-31")]),
        monthly(),
    ])
    (ROOT / "reports").mkdir(exist_ok=True)
    (ROOT / "reports" / "leveraged_trend.md").write_text(text)
    print(text)


if __name__ == "__main__":
    main()
