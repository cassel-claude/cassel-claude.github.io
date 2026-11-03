"""FRED / ALFRED economic data from the St. Louis Fed. Needs a free API key in FRED_API_KEY.

Useful series: T10Y3M (yield curve), BAMLH0A0HYM2 (high-yield credit spread), BAA / AAA (corporate yields),
ICSA (jobless claims), SAHMREALTIME (Sahm recession rule), VIXCLS (VIX), NFCI (financial conditions),
CPILFESL (core CPI), TB3MS (3-month T-bill).
"""
from __future__ import annotations

import os

import pandas as pd
import requests

API = "https://api.stlouisfed.org/fred/series/observations"


def parse_observations(payload: dict) -> pd.Series:
    obs = payload.get("observations", [])
    idx = pd.DatetimeIndex([pd.Timestamp(o["date"]) for o in obs])
    vals = [float(o["value"]) if o["value"] not in (".", "") else float("nan") for o in obs]
    return pd.Series(vals, index=idx, dtype=float)


def series(series_id: str, start: str = "1900-01-01", first_release_only: bool = False, session=None) -> pd.Series:
    """Observations for one series.

    first_release_only=True asks ALFRED for each value as first published, before later revisions. Use it for
    revised data (CPI, jobs, GDP) in backtests so the test only sees what was known at the time.
    """
    params = {
        "series_id": series_id,
        "api_key": os.environ["FRED_API_KEY"],
        "file_type": "json",
        "observation_start": start,
    }
    if first_release_only:
        params.update({"realtime_start": "1776-07-04", "realtime_end": "9999-12-31", "output_type": 4})
    s = session or requests.Session()
    resp = s.get(API, params=params, timeout=60)
    resp.raise_for_status()
    return parse_observations(resp.json()).rename(series_id)
