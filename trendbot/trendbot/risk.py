"""Hard limits applied to every target before it can become an order."""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Limits:
    max_weight_per_asset: float = 0.40
    max_total_invested: float = 0.99          # keep at least 1% uninvested for rounding and fees
    allowed_symbols: frozenset = field(default_factory=frozenset)
    per_asset_caps: dict = field(default_factory=dict)


def apply_limits(target: dict[str, float], limits: Limits) -> dict[str, float]:
    """Reject anything off the allowed list or negative (no shorting); cap each asset; scale the total down
    to `max_total_invested` if needed (no leverage)."""
    out = {}
    for sym, w in target.items():
        if limits.allowed_symbols and sym not in limits.allowed_symbols:
            raise ValueError(f"{sym} is not on the allowed list")
        if w < 0:
            raise ValueError(f"negative weight for {sym}: shorting is disabled")
        cap = min(limits.max_weight_per_asset, limits.per_asset_caps.get(sym, 1.0))
        out[sym] = min(float(w), cap)
    total = sum(out.values())
    if total > limits.max_total_invested:
        scale = limits.max_total_invested / total
        out = {s: w * scale for s, w in out.items()}
    return out
