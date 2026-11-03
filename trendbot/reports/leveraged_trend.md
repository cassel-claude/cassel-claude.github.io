# Leveraged trend study

Aiming above the index: leveraged index funds, held only while the trend is up.

Daily data (S&P 500 and Nasdaq, 2000-2018), modeled like real daily-reset leveraged ETFs (SSO/UPRO, QLD/TQQQ):
  L x fund daily return = L x index return - (L-1) x (T-bill + 0.5%/yr financing) - 0.9%/yr fees
Trend rule: checked at each month-end close (index vs its 200-day average), trade the next day,
            otherwise hold T-bills. 0.10% cost per switch.
Monthly data (US market 1928-2018): rough check with monthly-rebalanced leverage (ignores daily-reset effects).

## SP500 2000-2018

|  | Annual return | Worst drop | $1,000 became | Worst day |
|---|---|---|---|---|
| Hold 1x | 4.8% | -55.6% | $2,438 | -9.0% |
| Hold 2x | 2.8% | -87.9% | $1,676 | -18.1% |
| Hold 3x | -2.1% | -98.1% | $672 | -27.1% |
| Trend 1x (else T-bills) | 8.3% | -17.5% | $4,524 | -6.7% |
| Trend 2x (else T-bills) | 12.8% | -33.2% | $9,851 | -13.3% |
| Trend 3x (else T-bills) | 16.7% | -47.2% | $18,595 | -20.0% |

## SP500 2000-2002 crash

|  | Annual return | Worst drop | $1,000 became | Worst day |
|---|---|---|---|---|
| Hold 1x | -14.2% | -46.9% | $633 | -5.8% |
| Hold 2x | -33.7% | -78.2% | $293 | -11.7% |
| Hold 3x | -51.1% | -92.0% | $118 | -17.5% |
| Trend 1x (else T-bills) | 0.1% | -11.1% | $1,004 | -5.8% |
| Trend 2x (else T-bills) | -4.9% | -22.5% | $861 | -11.7% |
| Trend 3x (else T-bills) | -10.6% | -36.8% | $716 | -17.5% |

## SP500 2008 crisis

|  | Annual return | Worst drop | $1,000 became | Worst day |
|---|---|---|---|---|
| Hold 1x | -33.9% | -55.6% | $538 | -9.0% |
| Hold 2x | -63.5% | -84.7% | $221 | -18.1% |
| Hold 3x | -82.5% | -95.7% | $73 | -27.1% |
| Trend 1x (else T-bills) | -1.0% | -9.9% | $985 | -2.9% |
| Trend 2x (else T-bills) | -4.2% | -19.8% | $937 | -5.9% |
| Trend 3x (else T-bills) | -7.7% | -29.0% | $887 | -8.8% |

## SP500 Apr 2009-2018

|  | Annual return | Worst drop | $1,000 became | Worst day |
|---|---|---|---|---|
| Hold 1x | 14.6% | -19.4% | $3,774 | -6.7% |
| Hold 2x | 26.0% | -36.5% | $9,520 | -13.3% |
| Hold 3x | 36.5% | -51.9% | $20,655 | -20.0% |
| Trend 1x (else T-bills) | 10.2% | -17.5% | $2,583 | -6.7% |
| Trend 2x (else T-bills) | 17.9% | -33.2% | $4,983 | -13.3% |
| Trend 3x (else T-bills) | 25.0% | -47.2% | $8,818 | -20.0% |

## NASDAQ 2000-2018

|  | Annual return | Worst drop | $1,000 became | Worst day |
|---|---|---|---|---|
| Hold 1x | 3.4% | -77.5% | $1,897 | -9.7% |
| Hold 2x | -2.6% | -97.9% | $612 | -19.4% |
| Hold 3x | -13.1% | -99.9% | $69 | -29.1% |
| Trend 1x (else T-bills) | 5.5% | -44.4% | $2,764 | -9.7% |
| Trend 2x (else T-bills) | 6.0% | -74.7% | $2,997 | -19.4% |
| Trend 3x (else T-bills) | 4.3% | -89.8% | $2,232 | -29.1% |

## NASDAQ 2003-2018

|  | Annual return | Worst drop | $1,000 became | Worst day |
|---|---|---|---|---|
| Hold 1x | 11.4% | -55.1% | $5,643 | -9.1% |
| Hold 2x | 16.1% | -84.4% | $10,835 | -18.3% |
| Hold 3x | 17.0% | -95.6% | $12,253 | -27.4% |
| Trend 1x (else T-bills) | 8.8% | -27.3% | $3,876 | -6.9% |
| Trend 2x (else T-bills) | 13.6% | -48.5% | $7,646 | -13.8% |
| Trend 3x (else T-bills) | 16.8% | -64.2% | $12,012 | -20.7% |

## US market (monthly, rough) 1928-2018

|  | Annual return | Worst drop | $1,000 became |
|---|---|---|---|
| Hold 1x | 9.7% | -83.7% | $4,386,514 |
| Hold 2x | 10.7% | -98.7% | $10,150,670 |
| Trend 1x (else T-bills) | 9.5% | -43.1% | $3,729,561 |
| Trend 2x (else T-bills) | 13.0% | -73.6% | $67,665,140 |

## US market (monthly, rough) 1928-1949

|  | Annual return | Worst drop | $1,000 became |
|---|---|---|---|
| Hold 1x | 4.9% | -83.7% | $2,877 |
| Hold 2x | -0.5% | -98.7% | $900 |
| Trend 1x (else T-bills) | 5.6% | -43.1% | $3,284 |
| Trend 2x (else T-bills) | 6.7% | -73.6% | $4,162 |

## US market (monthly, rough) 1950-1999

|  | Annual return | Worst drop | $1,000 became |
|---|---|---|---|
| Hold 1x | 13.4% | -46.4% | $528,752 |
| Hold 2x | 17.9% | -78.5% | $3,727,287 |
| Trend 1x (else T-bills) | 11.7% | -24.5% | $253,922 |
| Trend 2x (else T-bills) | 15.8% | -51.3% | $1,539,669 |

## US market (monthly, rough) 2000-2018

|  | Annual return | Worst drop | $1,000 became |
|---|---|---|---|
| Hold 1x | 5.8% | -50.4% | $2,883 |
| Hold 2x | 6.0% | -81.8% | $3,027 |
| Trend 1x (else T-bills) | 8.2% | -17.4% | $4,472 |
| Trend 2x (else T-bills) | 13.3% | -32.7% | $10,559 |
