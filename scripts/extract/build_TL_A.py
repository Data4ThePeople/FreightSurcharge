"""Truckload group A: Knight-Swift, Werner, Heartland.

Rebuilt 2026-09-22; the desktop session made extract_TL_A.csv without a script.
Numbers are read from the filings by regex wherever a table exists. Narrative
years (Werner 2000-2003, Heartland 2002-2015) state the dollar amount, which is
checked against the quote.
"""
import csv, re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common import TENK, EXTRACT, EXTRACT_COLS, tenk, quote

rows = []
N = lambda s: int(s.replace(',', '')) / 1000  # thousands -> millions


def add(co, tk, scope, fy, fs, base, src, q, rev_excl=''):
    t = tenk(src)
    assert q in t and len(q) <= 200, (tk, fy)
    rows.append(dict(company=co, ticker=tk, mode='Truckload', scope=scope, fiscal_year=fy,
                     fuel_surcharge_revenue_musd=round(fs, 3), base_revenue_musd=round(base, 3),
                     fuel_surcharge_pct=round(100 * fs / base, 2), rev_incl=round(base, 3),
                     rev_excl=rev_excl, method='stated_dollars', source_file=src, quote=q))


def first(pat, t, what):
    m = re.search(pat, t)
    assert m, what
    return m


# ---- Knight-Swift: non-GAAP reconciliation lines, dollars in thousands ----
K = 'Knight-Swift Transportation'
kscope = {2017: 'Consolidated; all fuel surcharge (trucking+intermodal); Swift from 9/8/2017 merger',
          2018: 'Consolidated; all fuel surcharge (trucking+intermodal)',
          2019: 'Consolidated; trucking fuel surcharge (excl. intermodal)',
          2020: 'Consolidated; trucking fuel surcharge (excl. intermodal)',
          2021: 'Consolidated; truckload+LTL fuel surcharge (LTL from ACT/MME 2021)',
          2022: 'Consolidated; truckload+LTL fuel surcharge (LTL from ACT/MME 2021)',
          2023: 'Consolidated; truckload+LTL fuel surcharge (incl. U.S. Xpress from 7/1/2023)',
          2024: 'Consolidated; truckload+LTL fuel surcharge (incl. U.S. Xpress from 7/1/2023)',
          2025: 'Consolidated; truckload+LTL fuel surcharge (incl. U.S. Xpress from 7/1/2023)'}
for fy in range(2017, 2026):
    src = f'KNX_{fy}-12-31.txt'; t = tenk(src)
    base = N(first(r'Total revenue \$ ([\d,]+)', t, (src, 'revenue')).group(1))
    if fy <= 2018:
        m = first(r'Fuel surcharge \(([\d,]+) \)', t, (src, 'fsc'))
        q = m.group(0)
    elif fy <= 2020:
        m = first(r'Trucking fuel surcharge ([\d,]+) [\d,]+ [\d,]+', t, (src, 'fsc'))
        q = m.group(0)
    else:
        m = first(r'Truckload and LTL fuel surcharge ([\d,]+) [\d,]+ [\d,]+', t, (src, 'fsc'))
        q = m.group(0)
    fs = N(m.group(1))
    add(K, 'KNX', kscope[fy], fy, fs, base, src, q, rev_excl=round(base - fs, 3))

# ---- Werner ----
W = 'Werner Enterprises'
# 2000-2003: narrative dollars; base = consolidated operating revenues (see DATASETS.md issue 7)
wn = {2000: ('WERN_2001-12-31.txt', r'decreased from \$51\.4 million in 2000 to \$46\.2 million in 2001', 51.4, 1),
      2001: ('WERN_2001-12-31.txt', r'decreased from \$51\.4 million in 2000 to \$46\.2 million in 2001', 46.2, 0),
      2002: ('WERN_2002-12-31.txt', r'decreased from \$46\.2 million in 2001 to \$29\.1 million in 2002', 29.1, 0),
      2003: ('WERN_2003-12-31.txt', r'increased from \$29\.1 million in 2002 to \$61\.6 million in 2003', 61.6, 0)}
for fy, (src, pat, fs, col) in wn.items():
    t = tenk(src)
    m = first(r'Operating revenues \$ ?([\d,]+) \$ ?([\d,]+)', t, (src, 'revenue'))
    base = N(m.group(1 + col))
    add(W, 'WERN', 'Consolidated operating revenues (FSC is trucking fuel surcharge)', fy, fs, base, src, quote(src, pat))
# 2004-2012: TTS segment table "Revenues $X ... Less: trucking fuel surcharge revenues Y"
for fy in range(2004, 2013):
    src = f'WERN_{fy}-12-31.txt'; t = tenk(src)
    m = first(r'Less: trucking fuel surcharge revenues ([\d,]+) [\d,]+ [\d,]+', t, (src, 'fsc'))
    fs = N(m.group(1))
    # the TTS revenue line that the fuel line is subtracted from: last "Revenues $ X" before it
    head = t[:m.start()]
    rv = list(re.finditer(r'Revenues \$ ?([\d,]+)', head))
    assert rv, (src, 'TTS revenue')
    base = N(rv[-1].group(1))
    # the segment table also prints "Revenues, net of fuel surcharge"; confirm the subtraction ties out
    after = t[m.end():m.end() + 400]
    net = re.search(r'Revenues, net of fuel surcharges? \$? ?([\d,]+)', after)
    assert net and abs(N(net.group(1)) - (base - fs)) < 0.0015, (src, 'net check')
    add(W, 'WERN', 'Truckload Transportation Services segment revenues', fy, fs, base, src, m.group(0),
        rev_excl=round(base - fs, 3))
# 2013-2025: TTS table "Trucking fuel surcharge revenues X ... Operating revenues Y 100.0"
for fy in range(2013, 2026):
    src = f'WERN_{fy}-12-31.txt'; t = tenk(src)
    m = first(r'Trucking fuel surcharge revenues ([\d,]+) [\d,]+', t, (src, 'fsc'))
    fs = N(m.group(1))
    b = first(r'Operating revenues ([\d,]+) 100\.0', t[m.end():m.end() + 400], (src, 'TTS revenue'))
    base = N(b.group(1))
    scope = ('Truckload Transportation Services segment operating revenues' if fy <= 2018
             else 'TTS segment operating revenues (One-Way Truckload + Dedicated)')
    add(W, 'WERN', scope, fy, fs, base, src, m.group(0))

# ---- Heartland ----
H = 'Heartland Express'
hn = {2002: ('HTLD_2003-12-31.txt', r'Fuel surcharge revenue increased \$9\.4 million to \$15\.3 million from \$5\.9 million', 5.9),
      2003: ('HTLD_2003-12-31.txt', r'Fuel surcharge revenue increased \$9\.4 million to \$15\.3 million', 15.3),
      2004: ('HTLD_2004-12-31.txt', r'Fuel surcharge revenue increased \$13\.2 million to \$28\.5 million', 28.5),
      2005: ('HTLD_2005-12-31.txt', r'Fuel surcharge revenue increased \$31\.2 million to \$59\.7 million', 59.7),
      2006: ('HTLD_2006-12-31.txt', r'to \$81\.4 million in 2006', 81.4),
      2007: ('HTLD_2007-12-31.txt', r'to \$86\.6 million for the year ended December 31, 2007', 86.6),
      2008: ('HTLD_2008-12-31.txt', r'fuel surcharge revenue from \$86\.6 million in 2007 to \$130\.8 million in 2008', 130.8),
      2009: ('HTLD_2010-02-18.txt', r'fuel surcharge revenue from \$130\.8 million in 2008 to \$53\.3 million in 2009', 53.3),
      2010: ('HTLD_2010-12-31.txt', r'fuel surcharge revenue from \$53\.3 million in 2009 to \$75\.3 million in 2010', 75.3),
      2011: ('HTLD_2011-12-31.txt', r'fuel surcharge revenue from \$75\.3 million in 2010 to \$107\.8 million in 2011', 107.8),
      2012: ('HTLD_2012-12-31.txt', r'fuel surcharge revenue from \$107\.8 million in 2011 to \$112\.4 million in 2012', 112.4),
      2013: ('HTLD_2013-12-31.txt', r'fuel surcharge revenue from \$112\.4 million in 2012 to \$118\.4 million in 2013', 118.4),
      2014: ('HTLD_2014-12-31.txt', r'fuel surcharge revenue from \$118\.4 million in 2013 to \$170\.4 million in 2014', 170.4),
      2015: ('HTLD_2015-12-31.txt', r'fuel surcharge revenues were \$91\.8 million , \$170\.4 million', 91.8)}
hcol = {2002: 1}  # 2002 is read from the 2003 10-K's selected data, second column
for fy, (src, pat, fs) in hn.items():
    t = tenk(src)
    m = first(r'Operating revenue[ .]*\$ ?([\d,]+) \$ ?([\d,]+)', t, (src, 'revenue'))
    base = N(m.group(1 + hcol.get(fy, 0)))
    add(H, 'HTLD', 'Consolidated operating revenue', fy, fs, base, src, quote(src, pat))
for fy in range(2016, 2026):
    src = f'HTLD_{fy}-12-31.txt'; t = tenk(src)
    m = first(r'Less: Fuel surcharge revenue (?:\(non-GAAP\) )?([\d,]+) [\d,]+', t, (src, 'fsc'))
    fs = N(m.group(1))
    # the reconciliation this line belongs to opens with "Operating revenue $ X"
    rv = list(re.finditer(r'Operating revenue \$ ?([\d,]+)', t[:m.start()]))
    assert rv, (src, 'revenue')
    base = N(rv[-1].group(1))
    add(H, 'HTLD', 'Consolidated operating revenue', fy, fs, base, src, m.group(0), rev_excl=round(base - fs, 3))

rows.sort(key=lambda r: (r['ticker'] != 'KNX', r['ticker'] != 'WERN', r['fiscal_year']))
with open(EXTRACT / 'extract_TL_A.csv', 'w', newline='') as fh:
    w = csv.DictWriter(fh, EXTRACT_COLS); w.writeheader(); w.writerows(rows)
print(len(rows), 'rows')
