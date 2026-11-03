# Trend bot

A monthly, rules-based trend-following bot for a small account.

**How it decides:** on the first trading day of each month it looks at last month's closing prices.
- It holds up to 3 of these ETFs: VOO, SOXX, IWM, VXUS, VWO, TLT, IEF, GLD, DBC.
- A fund qualifies only if it is above its 10-month average. Qualifying funds are ranked by their average
  return over the last 3, 6 and 12 months.
- Any empty slot is parked in a Treasury-bill fund (SGOV).

**What it never does:** short, use leverage, trade options, or trade between scheduled runs. No AI picks
trades; every decision follows the rules in `config.yaml`.

## Status

| Piece | State |
|---|---|
| Signals, backtest engine, rotation, risk limits, order planner | Built; 23 unit tests passing |
| Prediction-data study (credit, yield curve, inflation) | Run on offline 1928–2018 data: `reports/indicator_study.md` |
| Data clients (Ken French, FRED/ALFRED, Alpaca, Kalshi) | Written; parsers tested on sample data; **not yet run against the live services** |
| Monthly GitHub Actions workflow | Written; dry-run by default; the workflow cannot run in live mode |
| Rotation backtest on real ETF prices | Script ready (`scripts/backtest_rotation.py`); needs Alpaca data access |

## Safety rules (in code)

- **Default mode:** dry-run, which prints the orders it would send and sends nothing.
- **Modes:** `paper` uses Alpaca's fake-money account. `live` is refused unless `--i-understand-live` is
  passed, and the scheduled workflow can't use it at all.
- **Limits:**
  - at most 40% in any one fund, and at most 34% in SOXX;
  - at most 99% invested;
  - no symbols outside the configured list;
  - no negative weights, so no shorting.
- **Order of trades:** sells are sent first and must fill before any buys go out. Trades under 2% of the
  account are skipped.
- **Stale data:** the bot refuses to trade if last month's prices are missing.

## Setup checklist

1. Create a **private** GitHub repository (for example `trendbot`) and push this folder to it.
2. In the Claude cloud environment settings:
   - **Allowed domains:** `data.alpaca.markets`, `paper-api.alpaca.markets`, `mba.tuck.dartmouth.edu`,
     `api.stlouisfed.org`, `fred.stlouisfed.org`, `alfred.stlouisfed.org`, `api.elections.kalshi.com`
   - **Secrets:** `APCA_API_KEY_ID`, `APCA_API_SECRET_KEY` (Alpaca **paper** keys) and `FRED_API_KEY`
     (free from fred.stlouisfed.org)
3. Start a new session so the settings take effect.
4. In the GitHub repository settings, add the same Alpaca paper keys as Actions secrets. After a clean
   dry run, set the repository variable `BOT_MODE` to `paper`.
5. Paper-trade through at least 2–3 month-ends and check the orders and fills before deciding on real money.

## Commands

```
pip install -r requirements.txt
python -m pytest -q                              # unit tests (offline)
python scripts/indicator_study.py                # prediction-data study (offline)
python scripts/backtest_rotation.py              # needs Alpaca data access
python scripts/rebalance.py --mode dry-run --force
```
