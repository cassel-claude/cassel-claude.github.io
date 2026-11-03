# Blend study

Do strategies offset each other? Blends of stock, leveraged-trend and bond strategies.

Building blocks (monthly, US 1928-2018):
  Stocks      : hold the US stock market (1x)
  Trend 2x    : 2x stocks while the market is above its 10-month average, else T-bills
  Bonds       : hold high-grade corporate bonds (returns estimated from Moody's AAA yields, 20-year par bond)
  Bond trend  : bonds while above their 10-month average, else T-bills
Blends are rebalanced back to their target mix every month.
Daily check (S&P 500, 2000-2018): the same idea with realistic daily-reset 2x funds, rebalanced monthly.

## How the building blocks move together (monthly, 1928-2018)

Correlation of monthly returns (1 = move in lockstep, 0 = unrelated, negative = offset):

|  | Stocks | Trend 2x | Bonds | Bond trend |
|---|---|---|---|---|
| Stocks | 1.0 | 0.67 | 0.15 | 0.11 |
| Trend 2x | 0.67 | 1.0 | 0.1 | 0.1 |
| Bonds | 0.15 | 0.1 | 1.0 | 0.8 |
| Bond trend | 0.11 | 0.1 | 0.8 | 1.0 |

Average monthly return of each block in the stock market's worst 5% of months:

|  | Stocks | Trend 2x | Bonds | Bond trend |
|---|---|---|---|---|
| In the worst 5% of stock months | -11.8% | -8.5% | +0.0% | +0.3% |

## Blends, 1928-2018

|  | Annual return | Volatility | Worst drop | $1,000 became | Worst 12 months |
|---|---|---|---|---|---|
| Stocks only | 9.7% | 18.5% | -83.7% | $4,386,514 | -65.8% |
| Trend 2x only | 13.0% | 25.0% | -73.6% | $67,665,140 | -52.9% |
| Classic 60/40 stocks/bonds | 8.6% | 11.7% | -63.6% | $1,825,813 | -47.7% |
| 50% stocks + 50% trend 2x | 11.8% | 20.0% | -73.8% | $26,036,229 | -39.2% |
| 40% stocks + 40% trend 2x + 20% bonds | 11.0% | 16.2% | -63.1% | $13,258,509 | -33.6% |
| 1/3 stocks + 1/3 trend 2x + 1/3 bond trend | 10.5% | 13.6% | -53.2% | $8,649,354 | -27.8% |

## Blends, 1928-1949

|  | Annual return | Volatility | Worst drop | $1,000 became | Worst 12 months |
|---|---|---|---|---|---|
| Stocks only | 4.9% | 27.4% | -83.7% | $2,877 | -65.8% |
| Trend 2x only | 6.7% | 32.0% | -73.6% | $4,162 | -52.9% |
| Classic 60/40 stocks/bonds | 5.8% | 16.7% | -63.6% | $3,423 | -47.7% |
| 50% stocks + 50% trend 2x | 6.8% | 26.4% | -73.8% | $4,288 | -39.2% |
| 40% stocks + 40% trend 2x + 20% bonds | 7.0% | 21.3% | -63.1% | $4,463 | -33.6% |
| 1/3 stocks + 1/3 trend 2x + 1/3 bond trend | 7.0% | 17.8% | -53.2% | $4,388 | -27.8% |

## Blends, 1950-1979 (rising interest rates)

|  | Annual return | Volatility | Worst drop | $1,000 became | Worst 12 months |
|---|---|---|---|---|---|
| Stocks only | 10.8% | 13.8% | -46.4% | $21,449 | -41.1% |
| Trend 2x only | 14.8% | 21.1% | -34.6% | $63,382 | -34.3% |
| Classic 60/40 stocks/bonds | 7.6% | 8.8% | -32.8% | $8,975 | -29.0% |
| 50% stocks + 50% trend 2x | 13.1% | 16.4% | -38.3% | $39,689 | -31.2% |
| 40% stocks + 40% trend 2x + 20% bonds | 11.1% | 13.3% | -32.7% | $23,413 | -26.7% |
| 1/3 stocks + 1/3 trend 2x + 1/3 bond trend | 10.3% | 11.2% | -26.3% | $19,164 | -20.7% |

## Blends, 1980-1999 (falling interest rates)

|  | Annual return | Volatility | Worst drop | $1,000 became | Worst 12 months |
|---|---|---|---|---|---|
| Stocks only | 17.4% | 15.3% | -29.9% | $24,651 | -16.5% |
| Trend 2x only | 17.3% | 26.9% | -51.3% | $24,292 | -51.3% |
| Classic 60/40 stocks/bonds | 15.3% | 10.7% | -18.6% | $17,312 | -7.2% |
| 50% stocks + 50% trend 2x | 17.8% | 20.5% | -38.9% | $26,278 | -35.0% |
| 40% stocks + 40% trend 2x + 20% bonds | 16.9% | 16.9% | -31.6% | $22,682 | -27.2% |
| 1/3 stocks + 1/3 trend 2x + 1/3 bond trend | 16.4% | 14.3% | -26.1% | $20,954 | -21.9% |

## Blends, 2000-2018

|  | Annual return | Volatility | Worst drop | $1,000 became | Worst 12 months |
|---|---|---|---|---|---|
| Stocks only | 5.8% | 14.9% | -50.4% | $2,883 | -42.6% |
| Trend 2x only | 13.3% | 18.7% | -32.7% | $10,559 | -23.9% |
| Classic 60/40 stocks/bonds | 6.7% | 9.4% | -30.5% | $3,433 | -25.4% |
| 50% stocks + 50% trend 2x | 9.8% | 15.2% | -37.9% | $5,822 | -24.5% |
| 40% stocks + 40% trend 2x + 20% bonds | 9.5% | 12.1% | -26.5% | $5,594 | -19.3% |
| 1/3 stocks + 1/3 trend 2x + 1/3 bond trend | 8.8% | 10.1% | -23.7% | $4,908 | -17.9% |

## S&P 500 daily (realistic 2x fund), 2000-2018

|  | Annual return | Volatility | Worst drop | $1,000 became | Worst 12 months |
|---|---|---|---|---|---|
| Stocks only (S&P 500) | 4.8% | 19.1% | -55.6% | $2,438 | -47.8% |
| Trend 2x only | 12.8% | 23.3% | -33.2% | $9,851 | -29.8% |
| 50% stocks + 50% trend 2x | 9.0% | 18.9% | -36.3% | $5,157 | -26.6% |

## S&P 500 daily (realistic 2x fund), 2000-2002 crash

|  | Annual return | Volatility | Worst drop | $1,000 became | Worst 12 months |
|---|---|---|---|---|---|
| Stocks only (S&P 500) | -14.2% | 23.3% | -46.9% | $633 | -33.1% |
| Trend 2x only | -4.9% | 22.4% | -22.5% | $861 | -12.6% |
| 50% stocks + 50% trend 2x | -9.2% | 19.6% | -33.5% | $749 | -21.1% |

## S&P 500 daily (realistic 2x fund), 2008 crisis

|  | Annual return | Volatility | Worst drop | $1,000 became | Worst 12 months |
|---|---|---|---|---|---|
| Stocks only (S&P 500) | -33.9% | 38.3% | -55.6% | $538 | -47.8% |
| Trend 2x only | -4.2% | 14.0% | -19.8% | $937 | -10.9% |
| 50% stocks + 50% trend 2x | -19.8% | 20.8% | -36.3% | $718 | -26.6% |

## S&P 500 daily (realistic 2x fund), Apr 2009-2018

|  | Annual return | Volatility | Worst drop | $1,000 became | Worst 12 months |
|---|---|---|---|---|---|
| Stocks only (S&P 500) | 14.6% | 15.5% | -19.4% | $3,774 | -10.8% |
| Trend 2x only | 17.9% | 25.3% | -33.2% | $4,983 | -29.8% |
| 50% stocks + 50% trend 2x | 16.5% | 19.4% | -25.5% | $4,424 | -17.2% |
