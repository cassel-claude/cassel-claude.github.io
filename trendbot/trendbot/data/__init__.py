"""Data sources.

bundled : offline US data through 2018 (ships with the `arch` package) - works with no network access
french  : Ken French Data Library - US market, T-bill and industry returns since 1926 (free, no key)
fred    : St. Louis Fed FRED/ALFRED economic series (free key: FRED_API_KEY)
alpaca  : ETF daily prices and order placement (APCA_API_KEY_ID / APCA_API_SECRET_KEY)
kalshi  : prediction-market odds (public endpoints, no key)

The network clients (french, fred, alpaca, kalshi) are written against the providers' documented REST APIs
but have not yet been run against them from this environment; their parsers are unit-tested on sample payloads.
"""
