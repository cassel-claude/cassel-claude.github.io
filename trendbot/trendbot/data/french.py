"""Ken French Data Library: free monthly US market, T-bill and industry returns since 1926 (no key needed)."""
from __future__ import annotations

import io
import zipfile

import pandas as pd
import requests

BASE = "https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/"


def parse_csv(text: str, section: int = 0) -> pd.DataFrame:
    """Parse one monthly table from a Ken French CSV file.

    Tables start with a header line beginning with ','; monthly rows start with a 6-digit YYYYMM.
    Annual tables (4-digit years) are skipped. Values are percent; -99.99 / -999 mean missing.
    Returns decimals indexed by month-end.
    """
    lines = text.splitlines()
    tables, i = [], 0
    while i < len(lines):
        if lines[i].strip().startswith(","):
            header = [h.strip() for h in lines[i].strip().split(",")[1:]]
            rows, j = [], i + 1
            while j < len(lines):
                parts = [p.strip() for p in lines[j].split(",")]
                if len(parts[0]) == 6 and parts[0].isdigit():
                    rows.append(parts)
                    j += 1
                else:
                    break
            if rows:
                tables.append((header, rows))
            i = j
        else:
            i += 1
    if not tables:
        raise ValueError("no monthly table found")
    header, rows = tables[section]
    idx = pd.to_datetime([r[0] for r in rows], format="%Y%m").to_period("M").to_timestamp(how="end").normalize()
    data = pd.DataFrame([[float(x) for x in r[1:len(header) + 1]] for r in rows], index=idx, columns=header)
    return data.mask(data <= -99.99) / 100.0


def _download(name: str, session=None) -> str:
    s = session or requests.Session()
    resp = s.get(BASE + name, timeout=60)
    resp.raise_for_status()
    with zipfile.ZipFile(io.BytesIO(resp.content)) as z:
        return z.read(z.namelist()[0]).decode("latin-1")


def market_and_cash(session=None) -> pd.DataFrame:
    df = parse_csv(_download("F-F_Research_Data_Factors_CSV.zip", session))
    return pd.DataFrame({"market": df["Mkt-RF"] + df["RF"], "cash": df["RF"]})


def industries(n: int = 10, session=None) -> pd.DataFrame:
    """Value-weighted monthly returns of n industry portfolios (n in 5, 10, 12, 17, 30, 38, 48, 49)."""
    return parse_csv(_download(f"{n}_Industry_Portfolios_CSV.zip", session), section=0)
