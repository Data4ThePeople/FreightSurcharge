"""Six months ended June 30, 2026, from each carrier's second-quarter 10-Q.

Same scope as each carrier's recent annual rows, so the half-year point can sit
next to the annual rings. Union Pacific's June 10-Q gives only the second
quarter, so its half year is Q1 + Q2 from the two 10-Qs (Q2 is rounded to
$0.1 billion). A row with two filings lists both, separated by ';', and its
quote has one part per filing, separated by ' | '.
"""
import csv, re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common import EXTRACT, tenk

COLS = ['company', 'ticker', 'mode', 'scope', 'fiscal_year', 'period', 'fuel_surcharge_revenue_musd',
        'base_revenue_musd', 'fuel_surcharge_pct', 'method', 'source_file', 'quote', 'base_components']
rows = []
N = lambda s: int(s.replace(',', '')) / 1000


def q(src, pat, maxlen=260):
    m = re.search(pat, tenk(src))
    assert m, (src, pat)
    assert len(m.group(0)) <= maxlen, (src, len(m.group(0)))
    return m


def add(co, tk, mode, scope, fs, base, src, quote, method='stated_dollars', pct=None, base_components=''):
    rows.append(dict(base_components=base_components, company=co, ticker=tk, mode=mode, scope=scope + '; six months ended June 30, 2026',
                     fiscal_year=2026, period='H1', fuel_surcharge_revenue_musd='' if fs is None else round(fs, 3),
                     base_revenue_musd='' if base is None else round(base, 3),
                     fuel_surcharge_pct=pct if pct is not None else round(100 * fs / base, 2),
                     method=method, source_file=src, quote=quote))


def rev(src, pat):
    return N(q(src, pat).group(1))


# ---- Truckload ----
f = 'HTLD_2026-06-30.txt'
m = q(f, r'Operating revenue \$ [\d,]+ \$ [\d,]+ \$ ([\d,]+) \$ [\d,]+ Less: Fuel surcharge revenue [\d,]+ [\d,]+ ([\d,]+) [\d,]+')
add('Heartland Express', 'HTLD', 'Truckload', 'Consolidated operating revenue', N(m.group(2)), N(m.group(1)), f,
    q(f, r'Less: Fuel surcharge revenue [\d,]+ [\d,]+ [\d,]+ [\d,]+').group(0))

f = 'KNX_2026-06-30.txt'   # Truckload segment table: Q2 2026, Q2 2025, H1 2026, H1 2025
m = q(f, r'Non-GAAP Presentation Total revenue \$ [\d,]+ \$ [\d,]+ \$ ([\d,]+) \$ [\d,]+ Fuel surcharge \([\d,]+ ?\) \([\d,]+ ?\) \(([\d,]+) ?\)')
add('Knight-Swift Transportation', 'KNX', 'Truckload', 'Truckload segment (incl. U.S. Xpress from 7/1/2023)',
    N(m.group(2)), N(m.group(1)), f, m.group(0))

f = 'MRTN_2026-06-30.txt'
m = q(f, r'Truckload fuel surcharge revenue [\d,]+ [\d,]+ ([\d,]+) [\d,]+ .{0,160}?Dedicated fuel surcharge revenue [\d,]+ [\d,]+ ([\d,]+)')
tot = N(q(f, r'Total operating revenue \$ [\d,]+ \$ [\d,]+ \$ ([\d,]+)').group(1))
brk = N(q(f, r'Brokerage revenue [\d,]+ [\d,]+ ([\d,]+) [\d,]+').group(1))
add('Marten Transport', 'MRTN', 'Truckload', 'operating revenue excluding brokerage; truckload + dedicated fuel surcharge (intermodal exited)',
    N(m.group(1)) + N(m.group(2)), tot - brk, f, m.group(0), method='derived_sum_of_segments',
    base_components=f'{tot:.3f}|{brk:.3f}')
COMPONENTS_MRTN = (N(m.group(1)), N(m.group(2)))

f = 'WERN_2026-06-30.txt'
m = q(f, r'Trucking fuel surcharge revenues [\d,]+ [\d,]+ ([\d,]+) [\d,]+ Non-trucking and other operating revenues [\d,]+ [\d,]+ [\d,]+ [\d,]+ Operating revenues [\d,]+ 100\.0 [\d,]+ 100\.0 ([\d,]+) 100\.0')
add('Werner Enterprises', 'WERN', 'Truckload', 'TTS segment operating revenues (One-Way Truckload + Dedicated)',
    N(m.group(1)), N(m.group(2)), f, q(f, r'Trucking fuel surcharge revenues [\d,]+ [\d,]+ [\d,]+ [\d,]+').group(0))

# ---- LTL ----
f = 'SAIA_2026-06-30.txt'
m = q(f, r'Fuel surcharge revenue as a percentage of operating revenue increased to (\d+\.\d) percent for the six months ended June 30, 2026')
add('Saia (SCS Transportation pre-2006)', 'SAIA', 'LTL', 'Saia Inc. consolidated operating revenue (continuing ops)',
    None, None, f, m.group(0), method='stated_pct', pct=float(m.group(1)))

f = 'XPO_2026-06-30.txt'
m = q(f, r'\$(\d+) million and \$\d+ million, respectively, for the first six months of 2026 and 2025')
b = q(f, r'North American LTL European Transportation Corporate \(1\) Total Revenue \$ ([\d,]+) \$ [\d,]+ \$ — \$ ([\d,]+) Salaries')
# the first-six-months segment table is the third such table in the filing (Q2 2026, Q2 2025, H1 2026, H1 2025)
tabs = list(re.finditer(r'North American LTL European Transportation Corporate \(1\) Total Revenue \$ ([\d,]+)', tenk(f)))
assert len(tabs) == 4, len(tabs)
add('XPO', 'XPO', 'LTL', 'North American LTL segment', float(m.group(1)), float(tabs[2].group(1).replace(',', '')), f, m.group(0))

# ---- Rail ----
f1, f2 = 'UNP_2026-03-31.txt', 'UNP_2026-06-30.txt'
m1 = q(f1, r'Freight revenues from fuel surcharge programs increased to \$(\d+) million in the first quarter of 2026')
m2 = q(f2, r'Freight revenues from fuel surcharge programs increased to \$(\d+\.\d) billion in the second quarter of 2026')
ytd = [x for x in re.finditer(r'Freight revenues \$ ([\d,]+) \$ ([\d,]+)', tenk(f2)) if x.group(1) != '6,518']
assert ytd, 'UNP year-to-date freight revenues'
q1, q2 = float(m1.group(1)), float(m2.group(1)) * 1000
add('Union Pacific', 'UNP', 'Rail', 'UNP freight revenues, excl. other revenues', q1 + q2,
    float(ytd[0].group(1).replace(',', '')), f'{f1};{f2}', f'{m1.group(0)} | {m2.group(0)}', method='derived_sum_of_quarters')

f = 'NSC_2026-06-30.txt'
m = q(f, r'Revenues associated with these surcharges totaled \$\d+ million and \$\d+ million in the second quarters of 2026 and 2025, respectively, and \$(\d+) million and \$\d+ million for the first six months of 2026 and 2025')
b = q(f, r'Railway operating revenues \$ [\d,]+ \$ [\d,]+ \$ ([\d,]+) \$ [\d,]+')
add('Norfolk Southern', 'NSC', 'Rail', 'NSC railway operating revenues (total)', float(m.group(1)),
    float(b.group(1).replace(',', '')), f, m.group(0))

# ---- Intermodal/truck mix ----
f = 'JBHT_2026-06-30.txt'
m = q(f, r'Fuel surcharge revenues [\d,]+ [\d,]+ ([\d,]+) [\d,]+ Total operating revenues [\d,]+ [\d,]+ ([\d,]+) [\d,]+')
add('J.B. Hunt Transport Services', 'JBHT', 'Intermodal/Truck mix', 'consolidated', N(m.group(1)), N(m.group(2)), f,
    q(f, r'Fuel surcharge revenues [\d,]+ [\d,]+ [\d,]+ [\d,]+').group(0))

with open(EXTRACT / 'extract_2026H1.csv', 'w', newline='') as fh:
    w = csv.DictWriter(fh, COLS); w.writeheader(); w.writerows(rows)
for r in rows:
    print(r['ticker'], r['mode'], r['fuel_surcharge_revenue_musd'], r['base_revenue_musd'], r['fuel_surcharge_pct'])
print('MRTN components', COMPONENTS_MRTN)
