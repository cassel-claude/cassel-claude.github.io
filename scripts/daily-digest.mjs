// Builds the daily market digest email (digest.html) from digest-config.json.
// Runs in GitHub Actions (see .github/workflows/daily-digest.yml); the send
// step is skipped when secrets are missing, so forks don't break.
//
// Env:
//   TWELVEDATA_API_KEY  required to fetch data (send=false without it)
//   TD_BASE             API base override, used by tests
//   TD_DELAY_MS         gap between API calls (default 8500 — free tier is 8 req/min)

import { readFileSync, writeFileSync, appendFileSync } from "node:fs";

const API_KEY = process.env.TWELVEDATA_API_KEY || "";
const BASE = process.env.TD_BASE || "https://api.twelvedata.com";
const DELAY = process.env.TD_DELAY_MS !== undefined ? Number(process.env.TD_DELAY_MS) : 8500;

function setOutput(k, v) {
  if (process.env.GITHUB_OUTPUT) appendFileSync(process.env.GITHUB_OUTPUT, `${k}=${v}\n`);
  else console.log(`[output] ${k}=${v}`);
}

if (!API_KEY) {
  console.log("TWELVEDATA_API_KEY secret not set — skipping digest (nothing sent).");
  setOutput("send", "false");
  process.exit(0);
}

const config = JSON.parse(readFileSync(new URL("../digest-config.json", import.meta.url), "utf8"));
const SYMBOLS = (config.symbols || []).slice(0, 12);
const MOVE_PCT = Number(config.big_move_pct) || 3;
if (!SYMBOLS.length) {
  console.log("digest-config.json has no symbols — skipping.");
  setOutput("send", "false");
  process.exit(0);
}

const sleep = ms => new Promise(r => setTimeout(r, ms));
async function td(path, params) {
  const u = new URL(BASE + "/" + path);
  for (const [k, v] of Object.entries(params)) u.searchParams.set(k, v);
  u.searchParams.set("apikey", API_KEY);
  const res = await fetch(u);
  const j = await res.json();
  if (j && j.status === "error") throw new Error(j.message || `API error ${j.code}`);
  return j;
}

/* ----- same indicator rules as tools/stock-tracker.html ----- */
function sma(vals, n) {
  if (vals.length < n) return null;
  let s = 0;
  for (let i = vals.length - n; i < vals.length; i++) s += vals[i];
  return s / n;
}
function rsi14(closes) {
  const n = 14;
  if (closes.length < n + 1) return null;
  let gain = 0, loss = 0;
  for (let i = 1; i <= n; i++) { const d = closes[i] - closes[i - 1]; if (d > 0) gain += d; else loss -= d; }
  let ag = gain / n, al = loss / n;
  for (let i = n + 1; i < closes.length; i++) {
    const d = closes[i] - closes[i - 1];
    ag = (ag * (n - 1) + Math.max(d, 0)) / n;
    al = (al * (n - 1) + Math.max(-d, 0)) / n;
  }
  if (al === 0) return 100;
  return 100 - 100 / (1 + ag / al);
}
const fmt = (n, d = 2) => (n === null || n === undefined || isNaN(n)) ? "—" : Number(n).toLocaleString("en-US", { minimumFractionDigits: d, maximumFractionDigits: d });

const rows = [];
for (let i = 0; i < SYMBOLS.length; i++) {
  const sym = SYMBOLS[i];
  const row = { sym, error: null, signals: [] };
  try {
    const q = await td("quote", { symbol: sym });
    row.price = parseFloat(q.close);
    row.chg = parseFloat(q.percent_change);
    row.name = q.name || "";
    if (DELAY) await sleep(DELAY);
    const ts = await td("time_series", { symbol: sym, interval: "1day", outputsize: 270 });
    const closes = ts.values.slice().reverse().map(v => parseFloat(v.close));
    closes[closes.length - 1] = row.price; // today's live/last price
    row.rsi = rsi14(closes);
    const s20 = sma(closes, 20), s50 = sma(closes, 50);
    const y = closes.slice(0, -1);
    const s20y = sma(y, 20), s50y = sma(y, 50);
    const yr = closes.slice(-252);
    const hi52 = Math.max(...yr), lo52 = Math.min(...yr);

    if (!isNaN(row.chg) && Math.abs(row.chg) >= MOVE_PCT)
      row.signals.push({ k: row.chg > 0 ? "up" : "down", t: `${row.chg > 0 ? "▲ up" : "▼ down"} ${fmt(Math.abs(row.chg), 1)}% today` });
    if (row.rsi !== null && row.rsi < 30) row.signals.push({ k: "up", t: `RSI ${fmt(row.rsi, 0)} — oversold` });
    if (row.rsi !== null && row.rsi > 70) row.signals.push({ k: "down", t: `RSI ${fmt(row.rsi, 0)} — overbought` });
    if (s20 && s50 && s20y <= s50y && s20 > s50) row.signals.push({ k: "up", t: "golden cross (20d over 50d)" });
    if (s20 && s50 && s20y >= s50y && s20 < s50) row.signals.push({ k: "down", t: "death cross (20d under 50d)" });
    if (row.price <= lo52 * 1.02) row.signals.push({ k: "up", t: `within 2% of 52-week low ($${fmt(lo52)})` });
    if (row.price >= hi52 * 0.98) row.signals.push({ k: "down", t: `within 2% of 52-week high ($${fmt(hi52)})` });
  } catch (e) {
    row.error = e.message;
    console.log(`  ${sym}: ${e.message}`);
  }
  rows.push(row);
  console.log(`fetched ${sym}${row.error ? " (error)" : ""}`);
  if (DELAY && i < SYMBOLS.length - 1) await sleep(DELAY);
}

const ok = rows.filter(r => !r.error);
if (!ok.length) {
  console.log("Every symbol failed — not sending a digest.");
  setOutput("send", "false");
  process.exit(1);
}

/* ----- build the email ----- */
const dateStr = new Date().toLocaleDateString("en-US", { timeZone: "America/New_York", weekday: "long", month: "long", day: "numeric", year: "numeric" });
const GREEN = "#0d6e5f", RED = "#b91c1c", MUTED = "#6b7280";
const chgHtml = c => isNaN(c) ? "—" : `<span style="color:${c >= 0 ? GREEN : RED}">${c >= 0 ? "▲ +" : "▼ "}${fmt(c)}%</span>`;
const sigHtml = s => `<span style="color:${s.k === "up" ? GREEN : RED}">${s.t}</span>`;

const tableRows = rows.map(r => r.error
  ? `<tr><td style="padding:8px;border-bottom:1px solid #e5e4df"><b>${r.sym}</b></td><td colspan="4" style="padding:8px;border-bottom:1px solid #e5e4df;color:${MUTED}">no data: ${r.error}</td></tr>`
  : `<tr>
      <td style="padding:8px;border-bottom:1px solid #e5e4df"><b>${r.sym}</b><br><span style="font-size:12px;color:${MUTED}">${r.name}</span></td>
      <td style="padding:8px;border-bottom:1px solid #e5e4df;text-align:right;font-family:monospace">$${fmt(r.price)}</td>
      <td style="padding:8px;border-bottom:1px solid #e5e4df;text-align:right;font-family:monospace">${chgHtml(r.chg)}</td>
      <td style="padding:8px;border-bottom:1px solid #e5e4df;text-align:right;font-family:monospace">${r.rsi !== null ? fmt(r.rsi, 0) : "—"}</td>
      <td style="padding:8px;border-bottom:1px solid #e5e4df">${r.signals.length ? r.signals.map(sigHtml).join("<br>") : `<span style="color:${MUTED}">—</span>`}</td>
    </tr>`).join("\n");

const flagged = ok.filter(r => r.signals.length);
const highlights = flagged.length
  ? `<ul style="padding-left:20px">${flagged.map(r => `<li style="margin:4px 0"><b>${r.sym}</b>: ${r.signals.map(s => s.t).join("; ")}</li>`).join("")}</ul>`
  : `<p style="color:${MUTED}">Nothing tripped a signal today.</p>`;

const html = `
<div style="font-family:Georgia,'Times New Roman',serif;color:#1a1d23;max-width:640px;margin:0 auto">
  <h2 style="margin-bottom:2px">Market digest — ${dateStr}</h2>
  <p style="color:${MUTED};font-size:14px;margin-top:0">From your <a href="https://cassel-claude.github.io/tools/stock-tracker.html" style="color:${GREEN}">stock tracker</a> · edit symbols in <code>digest-config.json</code></p>
  <h3 style="margin-bottom:6px">Today's signals</h3>
  ${highlights}
  <table style="border-collapse:collapse;width:100%;font-size:14px">
    <tr>
      <th style="text-align:left;padding:8px;border-bottom:2px solid #1a1d23;font-size:11px;letter-spacing:1px">SYMBOL</th>
      <th style="text-align:right;padding:8px;border-bottom:2px solid #1a1d23;font-size:11px;letter-spacing:1px">CLOSE</th>
      <th style="text-align:right;padding:8px;border-bottom:2px solid #1a1d23;font-size:11px;letter-spacing:1px">DAY</th>
      <th style="text-align:right;padding:8px;border-bottom:2px solid #1a1d23;font-size:11px;letter-spacing:1px">RSI 14</th>
      <th style="text-align:left;padding:8px;border-bottom:2px solid #1a1d23;font-size:11px;letter-spacing:1px">SIGNALS</th>
    </tr>
    ${tableRows}
  </table>
  <p style="font-size:12px;color:${MUTED};margin-top:16px">Signals are mechanical technical-analysis rules (RSI thresholds, moving-average crossovers, 52-week proximity) — watch prompts, not predictions or financial advice. Data via Twelve Data; free-tier quotes may be delayed.</p>
</div>`;
writeFileSync("digest.html", html);

const mover = ok.slice().sort((a, b) => Math.abs(b.chg || 0) - Math.abs(a.chg || 0))[0];
const subject = `📈 Market digest ${new Date().toLocaleDateString("en-US", { timeZone: "America/New_York", month: "short", day: "numeric" })}` +
  (mover && !isNaN(mover.chg) ? ` — ${mover.sym} ${mover.chg >= 0 ? "+" : ""}${fmt(mover.chg, 1)}%` : "") +
  (flagged.length ? ` · ${flagged.length} signal${flagged.length > 1 ? "s" : ""}` : "");
setOutput("subject", subject);
setOutput("send", "true");
console.log(`digest.html written · subject: ${subject}`);
