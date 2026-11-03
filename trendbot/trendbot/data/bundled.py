"""Offline datasets that ship with the `arch` package (US data through late 2018).

Used for research until live data access is enabled. Sources: Fama-French (via Ken French's library),
Moody's corporate bond yields and core CPI (via FRED), Yahoo daily index prices.
"""
from __future__ import annotations

import pandas as pd


def _to_month_end(index) -> pd.DatetimeIndex:
    return pd.DatetimeIndex(index).to_period("M").to_timestamp(how="end").normalize()


def market_and_cash() -> pd.DataFrame:
    """Monthly US stock market total return and 1-month T-bill return (decimals), Jul 1926 - Nov 2018."""
    from arch.data import frenchdata

    ff = frenchdata.load()
    yyyymm = pd.Series(ff.index.asi8).astype(str)          # the bundled index encodes YYYYMM
    idx = _to_month_end(pd.to_datetime(yyyymm, format="%Y%m"))
    return pd.DataFrame(
        {"market": (ff["Mkt-RF"].values + ff["RF"].values) / 100, "cash": ff["RF"].values / 100}, index=idx
    )


def corporate_yields() -> pd.DataFrame:
    """Moody's AAA and BAA corporate bond yields (percent per year, monthly averages), 1919 - 2018."""
    from arch.data import default

    d = default.load()
    d.index = _to_month_end(d.index)
    return d[["AAA", "BAA"]].astype(float)


def core_cpi() -> pd.Series:
    """US core CPI index (CPILFESL), monthly, 1957 - 2018."""
    from arch.data import core_cpi as cpi

    d = cpi.load()
    s = d["CPILFESL"].astype(float)
    s.index = _to_month_end(s.index)
    return s


def daily_close(name: str) -> pd.Series:
    """Daily index closes, 1999 - 2018. name: 'sp500' or 'nasdaq' (price index, no dividends)."""
    from arch.data import nasdaq, sp500

    return {"sp500": sp500, "nasdaq": nasdaq}[name].load()["Adj Close"].astype(float)
