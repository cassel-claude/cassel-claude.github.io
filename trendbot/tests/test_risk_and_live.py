import pytest

from trendbot import live, risk


def test_limits_cap_each_asset_and_the_total():
    lim = risk.Limits(max_weight_per_asset=0.4, max_total_invested=0.99, per_asset_caps={"SOXX": 0.34})
    out = risk.apply_limits({"SOXX": 0.5, "VOO": 0.5, "GLD": 0.5}, lim)
    assert sum(out.values()) == pytest.approx(0.99)
    assert out["SOXX"] < 0.34 and max(out.values()) <= 0.4


def test_limits_reject_shorts_and_unlisted_symbols():
    with pytest.raises(ValueError):
        risk.apply_limits({"VOO": -0.1}, risk.Limits())
    with pytest.raises(ValueError):
        risk.apply_limits({"TSLA": 0.1}, risk.Limits(allowed_symbols=frozenset({"VOO"})))


def test_plan_closes_dropped_funds_skips_tiny_trades_and_sells_first():
    orders = live.plan_orders({"VOO": 0.5, "GLD": 0.49}, equity=1000,
                              positions={"VOO": 200.0, "TLT": 300.0, "GLD": 495.0})
    assert [(o.symbol, o.side) for o in orders] == [("TLT", "close"), ("VOO", "buy")]
    assert orders[1].notional == pytest.approx(300.0)


class FakeBroker:
    def __init__(self):
        self.calls = []

    def buy(self, symbol, notional):
        self.calls.append(("buy", symbol, notional))
        return f"b-{symbol}"

    def sell(self, symbol, notional):
        self.calls.append(("sell", symbol, notional))
        return f"s-{symbol}"

    def close(self, symbol):
        self.calls.append(("close", symbol))
        return f"c-{symbol}"

    def wait(self, refs, timeout):
        self.calls.append(("wait", tuple(refs)))


def test_execute_waits_for_sales_before_buying():
    broker = FakeBroker()
    live.execute([live.Order("VOO", "buy", 300.0), live.Order("TLT", "close", 300.0)], broker, dry_run=False)
    assert broker.calls == [("close", "TLT"), ("wait", ("c-TLT",)), ("buy", "VOO", 300.0)]


def test_dry_run_sends_nothing():
    broker = FakeBroker()
    log = live.execute([live.Order("VOO", "buy", 300.0)], broker, dry_run=True)
    assert broker.calls == [] and log[0].startswith("DRY RUN")
