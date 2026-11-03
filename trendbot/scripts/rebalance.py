"""Monthly rebalance.

Modes:
  dry-run (default)  compute targets and print the orders it WOULD send; sends nothing
  paper              send orders to the Alpaca paper account (fake money)
  live               real money; refused unless --i-understand-live is also passed

Meant to be called every weekday by the scheduled GitHub Actions workflow; it acts only on the first trading
day of each month (unless --force), using closes through the end of the previous month.
"""
from __future__ import annotations

import argparse
import datetime as dt
import os
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from trendbot import live, portfolio  # noqa: E402
from trendbot.data import alpaca  # noqa: E402

MODES = ("dry-run", "paper", "live")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--mode", default="dry-run", choices=MODES)
    ap.add_argument("--force", action="store_true", help="run even if today is not the month's first trading day")
    ap.add_argument("--config", default=str(ROOT / "config.yaml"))
    ap.add_argument("--i-understand-live", action="store_true")
    args = ap.parse_args()
    if args.mode == "live" and not args.i_understand_live:
        print("Refusing to trade real money without --i-understand-live.")
        return 2

    cfg = yaml.safe_load(Path(args.config).read_text())
    broker = alpaca.AlpacaBroker(paper=(args.mode != "live"))
    today = dt.date.today()
    days = broker.trading_days(today.replace(day=1).isoformat(), today.isoformat())
    if not args.force and (not days or days[0] != today.isoformat()):
        print(f"{today}: not the first trading day of the month. Nothing to do.")
        return 0

    s = cfg["strategy"]
    symbols = list(s["universe"]) + ([s["cash_proxy"]] if s.get("cash_proxy") else [])
    closes = alpaca.daily_closes(symbols, start=(today - dt.timedelta(days=3 * 366)).isoformat(),
                                 end=(today - dt.timedelta(days=1)).isoformat(),
                                 feed=cfg["execution"].get("data_feed", "sip"))
    targets = portfolio.target_weights(cfg, closes, today)
    equity, positions = broker.equity(), broker.positions()
    ex = cfg["execution"]
    orders = live.plan_orders(targets, equity, positions, min_trade=ex["min_trade_dollars"],
                              band=ex["rebalance_band"])
    log = live.execute(orders, broker, dry_run=(args.mode == "dry-run"))

    lines = [f"## Rebalance {today} ({args.mode})", "", f"Account value: ${equity:,.2f}", "", "| Fund | Target |",
             "|---|---|"]
    lines += [f"| {sym} | {w:.1%} |" for sym, w in sorted(targets.items(), key=lambda kv: -kv[1])]
    lines += ["", "Orders:" if log else "No orders needed.", ""] + [f"    {line}" for line in log]
    summary = "\n".join(lines)
    print(summary)
    if os.environ.get("GITHUB_STEP_SUMMARY"):
        with open(os.environ["GITHUB_STEP_SUMMARY"], "a") as f:
            f.write(summary + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
