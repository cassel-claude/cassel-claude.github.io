# Prediction-data study (offline, US stock market)

Do "prediction data" indicators improve the trend rule? Offline study, US stock market 1928-2018.

Indicators (1 = conditions look BAD). Every rule was fixed before looking at any results:
  trend     : market below its 10-month average (the baseline rule)
  credit    : BAA-AAA corporate bond spread above its 12-month average (credit stress building)
  curve     : long-term AAA corporate yield below the T-bill yield (yield-curve inversion proxy)
  inflation : core CPI inflation above its 12-month average, using last month's release (1959+)

Part 1: when an indicator says BAD, is the next month actually worse than when it says GOOD?
Part 2: does acting on it (stocks or T-bills, checked monthly, 0.10% per trade) beat the trend rule?

## Part 1, 1928-2018: next month's stock return over T-bills, after BAD vs GOOD

|  | Months | Flagged BAD | Next month after BAD | Next month after GOOD | Rose after BAD | Swing after BAD | Swing after GOOD | Gap t-stat |
|---|---|---|---|---|---|---|---|---|
| trend | 1090 | 28% | +0.29% | +0.77% | 53% | ±7.5% | ±4.2% | 1.1 |
| credit | 1090 | 45% | +0.57% | +0.70% | 59% | ±6.4% | ±4.4% | 0.4 |
| curve | 1090 | 4% | -0.18% | +0.68% | 45% | ±5.7% | ±5.3% | 1.0 |
| inflation | 718 | 47% | +0.22% | +0.81% | 57% | ±4.7% | ±4.0% | 1.8 |

## Part 1, 1928-1972: next month's stock return over T-bills, after BAD vs GOOD

|  | Months | Flagged BAD | Next month after BAD | Next month after GOOD | Rose after BAD | Swing after BAD | Swing after GOOD | Gap t-stat |
|---|---|---|---|---|---|---|---|---|
| trend | 540 | 30% | +0.41% | +0.86% | 54% | ±8.7% | ±4.5% | 0.6 |
| credit | 540 | 43% | +0.63% | +0.80% | 60% | ±7.6% | ±4.7% | 0.3 |
| curve | 540 | 2% | +0.17% | +0.74% | 58% | ±7.1% | ±6.1% | 0.3 |
| inflation | 168 | 55% | +0.28% | +0.65% | 58% | ±3.9% | ±3.6% | 0.6 |

## Part 1, 1973-2018: next month's stock return over T-bills, after BAD vs GOOD

|  | Months | Flagged BAD | Next month after BAD | Next month after GOOD | Rose after BAD | Swing after BAD | Swing after GOOD | Gap t-stat |
|---|---|---|---|---|---|---|---|---|
| trend | 550 | 25% | +0.14% | +0.69% | 51% | ±5.9% | ±3.9% | 1.0 |
| credit | 550 | 47% | +0.51% | +0.60% | 59% | ±5.1% | ±4.0% | 0.2 |
| curve | 550 | 7% | -0.29% | +0.62% | 41% | ±5.3% | ±4.4% | 1.0 |
| inflation | 550 | 45% | +0.20% | +0.85% | 56% | ±4.9% | ±4.1% | 1.7 |

## Part 2, 1928-2018: stocks or T-bills, monthly

|  | Annual return | Volatility | Worst drop | $1,000 became | Avg invested | Traded/yr |
|---|---|---|---|---|---|---|
| Buy & hold | 9.7% | 18.5% | -83.7% | $4,386,514 | 100.0% | 0.0x |
| Trend only (baseline) | 9.5% | 12.5% | -43.1% | $3,729,561 | 72.5% | 1.4x |
| Credit only | 7.4% | 11.2% | -40.1% | $643,541 | 55.3% | 1.6x |
| Curve only | 9.8% | 18.0% | -80.4% | $4,943,325 | 95.5% | 0.5x |
| Trend + credit (out if EITHER bad) | 7.1% | 10.0% | -42.6% | $493,013 | 46.9% | 1.7x |
| Trend confirmed by credit (out only if BOTH bad) | 9.8% | 13.5% | -48.9% | $4,957,649 | 80.8% | 1.1x |

## Part 2, 1928-1972: stocks or T-bills, monthly

|  | Annual return | Volatility | Worst drop | $1,000 became | Avg invested | Traded/yr |
|---|---|---|---|---|---|---|
| Buy & hold | 8.9% | 21.1% | -83.7% | $46,529 | 100.0% | 0.0x |
| Trend only (baseline) | 8.6% | 13.2% | -43.1% | $40,455 | 70.0% | 1.5x |
| Credit only | 6.8% | 12.3% | -40.1% | $19,512 | 57.2% | 1.4x |
| Curve only | 8.9% | 20.8% | -80.4% | $46,044 | 97.8% | 0.4x |
| Trend + credit (out if EITHER bad) | 6.2% | 10.8% | -42.6% | $15,285 | 49.1% | 1.5x |
| Trend confirmed by credit (out only if BOTH bad) | 9.2% | 14.5% | -48.9% | $52,072 | 78.1% | 1.2x |

## Part 2, 1973-2018: stocks or T-bills, monthly

|  | Annual return | Volatility | Worst drop | $1,000 became | Avg invested | Traded/yr |
|---|---|---|---|---|---|---|
| Buy & hold | 10.4% | 15.6% | -50.4% | $94,274 | 100.0% | 0.0x |
| Trend only (baseline) | 10.4% | 11.8% | -24.5% | $92,190 | 75.0% | 1.4x |
| Credit only | 7.9% | 10.1% | -29.9% | $32,983 | 53.4% | 1.7x |
| Curve only | 10.7% | 14.8% | -50.4% | $107,361 | 93.3% | 0.6x |
| Trend + credit (out if EITHER bad) | 7.9% | 9.1% | -24.5% | $32,255 | 44.8% | 1.8x |
| Trend confirmed by credit (out only if BOTH bad) | 10.4% | 12.6% | -30.2% | $95,208 | 83.5% | 1.1x |

## Part 2, 1959-2018: stocks or T-bills, monthly

|  | Annual return | Volatility | Worst drop | $1,000 became | Avg invested | Traded/yr |
|---|---|---|---|---|---|---|
| Buy & hold | 10.1% | 15.0% | -50.4% | $319,007 | 100.0% | 0.0x |
| Trend only (baseline) | 9.9% | 11.2% | -24.5% | $290,531 | 74.7% | 1.4x |
| Inflation only | 9.3% | 10.1% | -27.6% | $202,118 | 52.7% | 1.5x |
| Trend confirmed by inflation | 10.5% | 12.7% | -31.3% | $388,060 | 83.9% | 1.0x |
| Trend confirmed by credit (out only if BOTH bad) | 9.9% | 12.0% | -32.2% | $293,495 | 82.3% | 1.2x |
