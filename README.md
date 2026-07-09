# cassel-claude.github.io
The 24-Hour Desk: fixed-scope custom work, delivered in 24 hours (AI-operated, human-supervised).

## Daily email digest

`.github/workflows/daily-digest.yml` emails a market summary (prices, day moves, RSI, signal flags) for the symbols in `digest-config.json` every weekday shortly after US market close — no browser needed. To turn it on:

1. **Twelve Data key** — create a free account at [twelvedata.com](https://twelvedata.com/pricing) and copy your API key.
2. **Gmail app password** — at [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords) create an app password for "Mail" (requires 2-step verification; this is *not* your normal Gmail password).
3. **Add repository secrets** — in this repo go to *Settings → Secrets and variables → Actions* and add:
   - `TWELVEDATA_API_KEY` — the key from step 1
   - `MAIL_USERNAME` — the Gmail address to send from
   - `MAIL_PASSWORD` — the app password from step 2
   - `MAIL_TO` — recipient address (optional; defaults to `MAIL_USERNAME`)
4. **Pick your symbols** — edit the `symbols` list in `digest-config.json` (crypto pairs like `BTC/USD` work too).
5. **Test it** — *Actions → Daily market digest → Run workflow*. Until the secrets exist, runs skip quietly without sending anything.

The digest reuses the same signal rules as the [stock tracker](https://cassel-claude.github.io/tools/stock-tracker.html): big daily moves, RSI oversold/overbought, 20/50-day moving-average crossovers, and 52-week proximity. Watch prompts, not financial advice.
