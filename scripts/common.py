"""Shared paths and helpers for the FreightSurcharge pipeline.

Every script imports from here so no path is written twice. Run scripts from
anywhere; paths resolve from this file.
"""
import os, re, sys, time, json, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / 'data' / 'raw'
TENK = RAW / 'sec_10k'
BEA = RAW / 'bea'
FRED = RAW / 'fred'
EIA = RAW / 'eia'
EXTRACT = ROOT / 'data' / 'extract'
PROCESSED = ROOT / 'data' / 'processed'
SRC = ROOT / 'src'
DIST = ROOT / 'dist'

UA = {'User-Agent': 'Data4ThePeople research eric@asaltollc.com'}

EXTRACT_COLS = ('company,ticker,mode,scope,fiscal_year,fuel_surcharge_revenue_musd,'
                'base_revenue_musd,fuel_surcharge_pct,rev_incl,rev_excl,method,'
                'source_file,quote').split(',')


def keys():
    """Load the central D4TP keys. Never print a key."""
    sys.path.insert(0, os.path.expanduser('~/.claude/d4tp-process'))
    from d4tp_env import load_env, get_key
    load_env()
    return get_key


def get(url, tries=4, timeout=60):
    for i in range(tries):
        try:
            return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=timeout).read()
        except Exception:
            if i == tries - 1:
                raise
            time.sleep(2 * (i + 1))


def tenk(name):
    """Text of one downloaded 10-K. Accepts 'X.txt' or 'tenk/X.txt'."""
    return (TENK / Path(name).name).read_text(errors='ignore')


def quote(fn, pat, maxlen=200):
    """Find a regex in a 10-K and return the matched text, which becomes the quote."""
    t = tenk(fn)
    m = re.search(pat, t)
    assert m, f'pattern not found in {fn}: {pat}'
    s = m.group(0)
    assert len(s) <= maxlen, f'quote too long in {fn}: {len(s)}'
    return s


def renderings(musd):
    """Ways a dollar amount in millions can be written in a filing, at the
    precision it was recorded. $560.017 million matches "560,017" (a table in
    thousands) but not "560". Used to confirm a number really appears in its
    quote or filing.
    """
    d = len(repr(float(musd)).split('.')[1].rstrip('0'))
    out = {f'{round(musd * 1000):,}',          # 245,580 (tables in thousands)
           f'{musd:,.{d}f}', f'{musd:,.{d + 1}f}'}  # 1,619 / 51.4 / 754.0
    if musd >= 1000 and round(musd) % 100 == 0:
        b = musd / 1000
        out |= {f'{b:.1f} billion', f'{b:.2f} billion'}  # 2.6 billion
        if b == int(b):
            out.add(f'{int(b)} billion')                  # 1 billion
    return out


def appears(musd, text, near=None, window=250):
    """True if a rendering of this amount appears in text as a whole number token.

    With `near` (a regex), the label must also appear in the `window` characters
    before the number, so a revenue base only counts on a revenue line.
    """
    for r in renderings(musd):
        for m in re.finditer(r'(?<![\d.,])' + re.escape(r) + r'(?![\d])', text):
            if near is None or re.search(near, text[max(0, m.start() - window):m.start()], re.I):
                return True
    return False


def write_json(path, obj):
    Path(path).write_text(json.dumps(obj, separators=(',', ':')))
