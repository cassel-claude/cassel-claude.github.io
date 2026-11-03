"""Turn target weights into orders. Dry-run by default."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


class Broker(Protocol):
    def equity(self) -> float: ...
    def positions(self) -> dict[str, float]: ...        # symbol -> current market value in dollars
    def buy(self, symbol: str, notional: float) -> str: ...
    def sell(self, symbol: str, notional: float) -> str: ...
    def close(self, symbol: str) -> str: ...
    def wait(self, refs: list[str], timeout: float) -> None: ...


@dataclass(frozen=True)
class Order:
    symbol: str
    side: str          # "buy", "sell" or "close"
    notional: float


def plan_orders(target_weights: dict[str, float], equity: float, positions: dict[str, float],
                min_trade: float = 5.0, band: float = 0.02) -> list[Order]:
    """Orders to move from `positions` to `target_weights` x `equity`.

    Positions with a zero target are closed completely. Other differences smaller than `min_trade` dollars
    or `band` (fraction of equity) are skipped to avoid churning. Sells and closes come before buys.
    """
    orders = []
    for sym in sorted(set(target_weights) | set(positions)):
        target = target_weights.get(sym, 0.0) * equity
        current = positions.get(sym, 0.0)
        if target <= 0.0:
            if current > 0:
                orders.append(Order(sym, "close", round(current, 2)))
            continue
        diff = target - current
        if abs(diff) >= max(min_trade, band * equity):
            orders.append(Order(sym, "buy" if diff > 0 else "sell", round(abs(diff), 2)))
    return sorted(orders, key=lambda o: o.side == "buy")


def _line(o: Order) -> str:
    return f"{o.side.upper():5s} {o.symbol:6s} ${o.notional:,.2f}"


def execute(orders: list[Order], broker: Broker | None, dry_run: bool = True, wait_timeout: float = 120) -> list[str]:
    """Send sells/closes, wait for them to fill so the cash is there, then send buys.
    In dry-run (or with no broker) nothing is sent."""
    sells = [o for o in orders if o.side != "buy"]
    buys = [o for o in orders if o.side == "buy"]
    if dry_run or broker is None:
        return [f"DRY RUN  {_line(o)}" for o in sells + buys]
    log, refs = [], []
    for o in sells:
        ref = broker.close(o.symbol) if o.side == "close" else broker.sell(o.symbol, o.notional)
        refs.append(ref)
        log.append(f"SENT     {_line(o)}  (order {ref})")
    if refs and buys:
        broker.wait(refs, wait_timeout)
    for o in buys:
        ref = broker.buy(o.symbol, o.notional)
        log.append(f"SENT     {_line(o)}  (order {ref})")
    return log
