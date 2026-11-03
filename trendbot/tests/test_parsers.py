import numpy as np
import pandas as pd
import pytest

from trendbot.data import alpaca, french, fred

FRENCH_SAMPLE = """This file was created by CMPT_ME_BEME_RETS using the 202409 CRSP database.
The 1-month TBill return is from Ibbotson and Associates Inc.

,Mkt-RF,SMB,HML,RF
192607,    2.96,   -2.56,   -2.43,    0.22
192608,    2.64,   -1.17,    3.82,    0.25

 Annual Factors: January-December
,Mkt-RF,SMB,HML,RF
  1927,   29.47,   -2.46,   -3.75,    3.12
"""


def test_french_parser_reads_only_the_monthly_table():
    df = french.parse_csv(FRENCH_SAMPLE)
    assert list(df.columns) == ["Mkt-RF", "SMB", "HML", "RF"]
    assert len(df) == 2
    assert df.index[0] == pd.Timestamp("1926-07-31")
    assert df.loc["1926-07-31", "RF"] == pytest.approx(0.0022)


def test_fred_parser_handles_missing_values():
    s = fred.parse_observations({"observations": [{"date": "2020-01-01", "value": "1.5"},
                                                  {"date": "2020-02-01", "value": "."}]})
    assert s.iloc[0] == 1.5 and np.isnan(s.iloc[1])


def test_alpaca_bar_parser():
    payload = {"bars": {"VOO": [{"t": "2024-01-02T05:00:00Z", "o": 1, "h": 1, "l": 1, "c": 400.5, "v": 10}]},
               "next_page_token": None}
    assert alpaca.parse_bars(payload)["VOO"][0] == (pd.Timestamp("2024-01-02"), 400.5)
