"""Alpaca REST access: ETF daily prices and order placement.

Reads APCA_API_KEY_ID and APCA_API_SECRET_KEY. Paper trading uses paper-api.alpaca.markets; live trading
uses api.alpaca.markets and must be explicitly requested by the caller.
"""
from __future__ import annotations

import os
import time

import pandas as pd
import requests

DATA_URL = "https://data.alpaca.markets/v2/stocks/bars"
PAPER_URL = "https://paper-api.alpaca.markets"
LIVE_URL = "https://api.alpaca.markets"
FINAL_STATES = {"filled", "canceled", "expired", "rejected"}


def _headers() -> dict:
    return {
        "APCA-API-KEY-ID": os.environ["APCA_API_KEY_ID"],
        "APCA-API-SECRET-KEY": os.environ["APCA_API_SECRET_KEY"],
    }


def parse_bars(payload: dict) -> dict[str, list[tuple[pd.Timestamp, float]]]:
    out = {}
    for sym, bars in (payload.get("bars") or {}).items():
        out[sym] = [(pd.Timestamp(b["t"]).tz_convert(None).normalize(), float(b["c"])) for b in bars]
    return out


def daily_closes(symbols, start: str, end: str | None = None, feed: str = "sip", adjustment: str = "all",
                 session=None) -> pd.DataFrame:
    """Split- and dividend-adjusted daily closes (columns = symbols). Pass an `end` before today: free data
    plans cannot query the most recent 15 minutes of consolidated (SIP) data."""
    s = session or requests.Session()
    params = {"symbols": ",".join(symbols), "timeframe": "1Day", "start": start, "adjustment": adjustment,
              "feed": feed, "limit": 10000}
    if end:
        params["end"] = end
    rows: dict[str, list] = {}
    while True:
        resp = s.get(DATA_URL, params=params, headers=_headers(), timeout=30)
        resp.raise_for_status()
        payload = resp.json()
        for sym, bars in parse_bars(payload).items():
            rows.setdefault(sym, []).extend(bars)
        token = payload.get("next_page_token")
        if not token:
            break
        params["page_token"] = token
    return pd.DataFrame({sym: pd.Series(dict(bars)) for sym, bars in rows.items() if bars}).sort_index()


class AlpacaBroker:
    """Minimal broker for the rebalancer: account value, positions, dollar-amount market orders."""

    def __init__(self, paper: bool = True, session=None):
        self.base = PAPER_URL if paper else LIVE_URL
        self.s = session or requests.Session()

    def _req(self, method: str, path: str, **kw):
        resp = self.s.request(method, self.base + path, headers=_headers(), timeout=30, **kw)
        resp.raise_for_status()
        return resp.json() if resp.content else {}

    def equity(self) -> float:
        return float(self._req("GET", "/v2/account")["equity"])

    def positions(self) -> dict[str, float]:
        return {p["symbol"]: float(p["market_value"]) for p in self._req("GET", "/v2/positions")}

    def trading_days(self, start: str, end: str) -> list[str]:
        return [d["date"] for d in self._req("GET", "/v2/calendar", params={"start": start, "end": end})]

    def _order(self, symbol: str, side: str, notional: float) -> str:
        body = {"symbol": symbol, "side": side, "type": "market", "time_in_force": "day",
                "notional": f"{notional:.2f}"}
        return self._req("POST", "/v2/orders", json=body)["id"]

    def buy(self, symbol: str, notional: float) -> str:
        return self._order(symbol, "buy", notional)

    def sell(self, symbol: str, notional: float) -> str:
        return self._order(symbol, "sell", notional)

    def close(self, symbol: str) -> str:
        return self._req("DELETE", f"/v2/positions/{symbol}").get("id", "closed")

    def wait(self, refs: list[str], timeout: float = 120) -> None:
        deadline, pending = time.time() + timeout, set(refs)
        while pending and time.time() < deadline:
            for ref in list(pending):
                if self._req("GET", f"/v2/orders/{ref}")["status"] in FINAL_STATES:
                    pending.discard(ref)
            if pending:
                time.sleep(2)
        if pending:
            raise TimeoutError(f"orders still open after {timeout}s: {sorted(pending)}")
