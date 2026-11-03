"""Kalshi prediction-market data (public endpoints, no key needed).

Prediction-market odds (Fed decisions, inflation prints, recession) are shown as context in reports. They do
not drive trades unless they pass the same out-of-sample tests as every other signal; Kalshi's history only
goes back to about 2021, so that test will be thin for years.
"""
from __future__ import annotations

import requests

BASE = "https://api.elections.kalshi.com/trade-api/v2"


def get(path: str, params: dict | None = None, session=None) -> dict:
    s = session or requests.Session()
    resp = s.get(BASE + path, params=params or {}, timeout=30)
    resp.raise_for_status()
    return resp.json()


def markets(session=None, max_pages: int = 20, **filters) -> list[dict]:
    """List markets matching filters such as series_ticker=..., event_ticker=..., status='open'."""
    if not filters:
        raise ValueError("pass at least one filter (e.g. series_ticker or event_ticker)")
    out, cursor = [], None
    for _ in range(max_pages):
        params = dict(filters, limit=200)
        if cursor:
            params["cursor"] = cursor
        payload = get("/markets", params, session)
        out.extend(payload.get("markets", []))
        cursor = payload.get("cursor")
        if not cursor:
            break
    return out
