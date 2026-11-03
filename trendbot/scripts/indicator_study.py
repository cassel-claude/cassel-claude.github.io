"""Do "prediction data" indicators improve the trend rule? Offline study, US stock market 1928-2018.

Indicators (1 = conditions look BAD). Every rule was fixed before looking at any results:
  trend     : market below its 10-month average (the baseline rule)
  credit    : BAA-AAA corporate bond spread above its 12-month average (credit stress building)
  curve     : long-term AAA corporate yield below the T-bill yield (yield-curve inversion proxy)
  inflation : core CPI inflation above its 12-month average, using last month's release (1959+)

Part 1: when an indicator says BAD, is the next month actually worse than when it says GOOD?
Part 2: does acting on it (stocks or T-bills, checked monthly, 0.10% per trade) beat the trend rule?
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from trendbot import backtest, metrics, signals  # noqa: E402
from trendbot.data import bundled  # noqa: E402

COST = 0.001


def load():
    mc = bundled.market_and_cash()
    y = bundled.corporate_yields().reindex(mc.index)
    cpi = bundled.core_cpi().reindex(mc.index)
    level = signals.level_from_returns(mc["market"])
    tbill_yield = ((1 + mc["cash"]) ** 12 - 1) * 100
    bad = pd.DataFrame({
        "trend": 1 - signals.above_average(level, 10),
        "credit": signals.credit_stress(y["BAA"], y["AAA"], 12),
        "curve": signals.curve_inverted(y["AAA"], tbill_yield),
        "inflation": signals.inflation_rising(cpi, 12, release_lag=1),
    })
    return mc, bad


def predictive_table(mc, bad, start, end):
    excess_next = (mc["market"] - mc["cash"]).shift(-1)
    rows = {}
    for name in bad.columns:
        d = pd.DataFrame({"bad": bad[name], "next": excess_next}).loc[start:end].dropna()
        b, g = d.loc[d["bad"] == 1, "next"], d.loc[d["bad"] == 0, "next"]
        if len(b) < 10 or len(g) < 10:
            continue
        t = (g.mean() - b.mean()) / np.sqrt(g.var() / len(g) + b.var() / len(b))
        rows[name] = {
            "Months": len(d),
            "Flagged BAD": f"{len(b) / len(d):.0%}",
            "Next month after BAD": f"{b.mean():+.2%}",
            "Next month after GOOD": f"{g.mean():+.2%}",
            "Rose after BAD": f"{(b > 0).mean():.0%}",
            "Swing after BAD": f"±{b.std():.1%}",
            "Swing after GOOD": f"±{g.std():.1%}",
            "Gap t-stat": f"{t:.1f}",
        }
    return pd.DataFrame(rows).T


def strategies(bad):
    own = lambda s: 1 - s.fillna(0.0)  # noqa: E731
    t, c, i = bad["trend"].fillna(0.0), bad["credit"].fillna(0.0), bad["inflation"].fillna(0.0)
    return {
        "Buy & hold": pd.Series(1.0, index=bad.index),
        "Trend only (baseline)": own(bad["trend"]),
        "Credit only": own(bad["credit"]),
        "Curve only": own(bad["curve"]),
        "Trend + credit (out if EITHER bad)": own(np.maximum(t, c)),
        "Trend confirmed by credit (out only if BOTH bad)": own(np.minimum(t, c)),
        "Inflation only": own(bad["inflation"]),
        "Trend confirmed by inflation": own(np.minimum(t, i)),
    }


def performance_table(mc, weights, names, start, end):
    res = {}
    for name in names:
        net, held = backtest.run(weights[name], mc["market"], mc["cash"], COST)
        res[name] = metrics.summarize(net.loc[start:end], 12, held.loc[start:end])
    return metrics.format_table(pd.DataFrame(res).T)


def main() -> None:
    mc, bad = load()
    w = strategies(bad)
    core = ["Buy & hold", "Trend only (baseline)", "Credit only", "Curve only",
            "Trend + credit (out if EITHER bad)", "Trend confirmed by credit (out only if BOTH bad)"]
    infl = ["Buy & hold", "Trend only (baseline)", "Inflation only", "Trend confirmed by inflation",
            "Trend confirmed by credit (out only if BOTH bad)"]
    out = ["# Prediction-data study (offline, US stock market)", "", __doc__.strip(), ""]
    for label, a, b in [("1928-2018", "1928-01", "2018-10"), ("1928-1972", "1928-01", "1972-12"),
                        ("1973-2018", "1973-01", "2018-10")]:
        out += [f"## Part 1, {label}: next month's stock return over T-bills, after BAD vs GOOD", "",
                metrics.to_markdown(predictive_table(mc, bad, a, b)), ""]
    for label, a, b, names in [("1928-2018", "1928-01", "2018-11", core), ("1928-1972", "1928-01", "1972-12", core),
                               ("1973-2018", "1973-01", "2018-11", core), ("1959-2018", "1959-01", "2018-11", infl)]:
        out += [f"## Part 2, {label}: stocks or T-bills, monthly", "",
                metrics.to_markdown(performance_table(mc, w, names, a, b)), ""]
    text = "\n".join(out)
    (ROOT / "reports").mkdir(exist_ok=True)
    (ROOT / "reports" / "indicator_study.md").write_text(text)
    print(text)


if __name__ == "__main__":
    main()
