# Design study

Design study: the strongest combination of the strategies that survived testing.

Designs (chosen before running; monthly data, US 1928-2018, bonds estimated from Moody's AAA yields):
  A  Trend 2x -> T-bills          : 2x stocks while the market is above its 10-month average, else T-bills
  B  Trend 2x -> bonds            : same, but when stocks trend down, hold bonds if bonds are trending up, else T-bills
  C  Three-way (bills)            : 1/3 stocks + 1/3 design A + 1/3 bond trend
  D  Three-way (bonds)            : 1/3 stocks + 1/3 design B + 1/3 bond trend
Robustness: designs B and D re-run with trend windows of 8/10/12 months and leverage of 1.5x/2x/2.5x.

## 1928-2018

|  | Annual return | Volatility | Worst drop | $1,000 became | Worst 12 months | Longest time below a peak |
|---|---|---|---|---|---|---|
| Stocks only (benchmark) | 9.7% | 18.5% | -83.7% | $4,386,514 | -65.8% | 15y 3m |
| 60/40 stocks/bonds (benchmark) | 8.6% | 11.7% | -63.6% | $1,825,813 | -47.7% | 6y 4m |
| A: Trend 2x -> T-bills | 13.0% | 25.0% | -73.6% | $67,665,140 | -52.9% | 9y 3m |
| B: Trend 2x -> bonds | 13.8% | 25.1% | -71.0% | $126,137,951 | -54.2% | 7y 2m |
| C: Three-way (bills) | 10.5% | 13.6% | -53.2% | $8,649,354 | -27.8% | 6y 4m |
| D: Three-way (bonds) | 10.7% | 13.7% | -51.6% | $10,600,406 | -28.3% | 6y 3m |

## 1928-1949

|  | Annual return | Volatility | Worst drop | $1,000 became | Worst 12 months | Longest time below a peak |
|---|---|---|---|---|---|---|
| Stocks only (benchmark) | 4.9% | 27.4% | -83.7% | $2,877 | -65.8% | 15y 3m |
| 60/40 stocks/bonds (benchmark) | 5.8% | 16.7% | -63.6% | $3,423 | -47.7% | 6y 4m |
| A: Trend 2x -> T-bills | 6.7% | 32.0% | -73.6% | $4,162 | -52.9% | 9y 3m |
| B: Trend 2x -> bonds | 7.7% | 32.0% | -71.0% | $5,145 | -54.2% | 7y 2m |
| C: Three-way (bills) | 7.0% | 17.8% | -53.2% | $4,388 | -27.8% | 6y 4m |
| D: Three-way (bonds) | 7.3% | 17.8% | -51.6% | $4,705 | -28.3% | 6y 3m |

## 1950-1979 (rising rates, inflation)

|  | Annual return | Volatility | Worst drop | $1,000 became | Worst 12 months | Longest time below a peak |
|---|---|---|---|---|---|---|
| Stocks only (benchmark) | 10.8% | 13.8% | -46.4% | $21,449 | -41.1% | 3y 11m |
| 60/40 stocks/bonds (benchmark) | 7.6% | 8.8% | -32.8% | $8,975 | -29.0% | 3y 1m |
| A: Trend 2x -> T-bills | 14.8% | 21.1% | -34.6% | $63,382 | -34.3% | 3y 0m |
| B: Trend 2x -> bonds | 14.9% | 21.2% | -38.1% | $64,229 | -37.2% | 3y 0m |
| C: Three-way (bills) | 10.3% | 11.2% | -26.3% | $19,164 | -20.7% | 2y 5m |
| D: Three-way (bonds) | 10.4% | 11.2% | -28.2% | $19,240 | -21.6% | 2y 5m |

## 1980-1999 (falling rates)

|  | Annual return | Volatility | Worst drop | $1,000 became | Worst 12 months | Longest time below a peak |
|---|---|---|---|---|---|---|
| Stocks only (benchmark) | 17.4% | 15.3% | -29.9% | $24,651 | -16.5% | 1y 10m |
| 60/40 stocks/bonds (benchmark) | 15.3% | 10.7% | -18.6% | $17,312 | -7.2% | 1y 4m |
| A: Trend 2x -> T-bills | 17.3% | 26.9% | -51.3% | $24,292 | -51.3% | 6y 1m |
| B: Trend 2x -> bonds | 17.6% | 27.1% | -52.1% | $25,641 | -50.4% | 5y 11m |
| C: Three-way (bills) | 16.4% | 14.3% | -26.1% | $20,954 | -21.9% | 1y 10m |
| D: Three-way (bonds) | 16.5% | 14.5% | -26.1% | $21,296 | -21.4% | 1y 9m |

## 2000-2018

|  | Annual return | Volatility | Worst drop | $1,000 became | Worst 12 months | Longest time below a peak |
|---|---|---|---|---|---|---|
| Stocks only (benchmark) | 5.8% | 14.9% | -50.4% | $2,883 | -42.6% | 6y 1m |
| 60/40 stocks/bonds (benchmark) | 6.7% | 9.4% | -30.5% | $3,433 | -25.4% | 3y 1m |
| A: Trend 2x -> T-bills | 13.3% | 18.7% | -32.7% | $10,559 | -23.9% | 3y 8m |
| B: Trend 2x -> bonds | 15.3% | 18.8% | -31.2% | $14,888 | -18.8% | 3y 2m |
| C: Three-way (bills) | 8.8% | 10.1% | -23.7% | $4,908 | -17.9% | 3y 6m |
| D: Three-way (bonds) | 9.4% | 10.3% | -25.9% | $5,499 | -20.3% | 3y 1m |

## Robustness, 1928-2018 (design | trend window | leverage)

|  | Annual return | Worst drop |
|---|---|---|
| B | 8-month | 1.5x | 10.6% | -70.3% |
| D | 8-month | 1.5x | 9.4% | -52.5% |
| B | 8-month | 2.0x | 12.0% | -82.5% |
| D | 8-month | 2.0x | 10.1% | -59.1% |
| B | 8-month | 2.5x | 12.9% | -90.4% |
| D | 8-month | 2.5x | 10.8% | -64.9% |
| B | 10-month | 1.5x | 11.9% | -57.6% |
| D | 10-month | 1.5x | 9.8% | -45.9% |
| B | 10-month | 2.0x | 13.8% | -71.0% |
| D | 10-month | 2.0x | 10.7% | -51.6% |
| B | 10-month | 2.5x | 15.1% | -82.5% |
| D | 10-month | 2.5x | 11.6% | -56.9% |
| B | 12-month | 1.5x | 12.3% | -63.0% |
| D | 12-month | 1.5x | 10.0% | -50.1% |
| B | 12-month | 2.0x | 14.4% | -75.7% |
| D | 12-month | 2.0x | 10.9% | -55.7% |
| B | 12-month | 2.5x | 16.0% | -84.8% |
| D | 12-month | 2.5x | 11.8% | -60.8% |
