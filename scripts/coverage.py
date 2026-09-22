"""Source coverage check (PROCESS.md, Step 1): how complete each source is over time.

Outputs data/processed/coverage.json and prints a summary.

1. Carrier filings: for each mode and year, how many carriers are in the ring,
   how their revenue compares with the whole industry, and how each ring value
   was obtained (a table figure in thousands, a rounded narrative figure, a
   company-stated percent, or a derived figure).
2. EIA diesel: sample eras, published standard errors, and the June 2022
   sample change measured in EIA's own side-by-side comparison.
"""
import json, re
import pandas as pd
from common import RAW, EIA, PROCESSED, TENK

d = pd.read_csv(PROCESSED / 'fuel_surcharge_by_mode.csv')
MODES = {'Truckload': ['HTLD', 'KNX', 'MRTN', 'WERN'], 'LTL': ['ODFL', 'SAIA', 'XPO'], 'Rail': ['UNP', 'NSC']}


def kind(r):
    if r.method == 'stated_pct':
        return 'company-stated percent'
    if r.method.startswith('derived'):
        return 'derived (sum or difference of reported figures)'
    v = r.fuel_surcharge_revenue_musd
    return 'table figure (to $1,000)' if round(v * 1000) != round(v, 1) * 1000 else 'rounded narrative figure'


d['kind'] = [kind(r) for r in d.itertuples()]
out = {'rings': {}, 'industry': {}, 'diesel': {}}

# ---- 1a. ring composition by year ----
for mode, tks in MODES.items():
    m = d[d.ticker.isin(tks)]
    yrs = {}
    for (y, p), g in m.groupby(['fiscal_year', 'period']):
        yrs[f'{y}{"H1" if p == "H1" else ""}'] = dict(n=len(g), carriers=sorted(g.ticker), kinds=g.kind.value_counts().to_dict())
    out['rings'][mode] = yrs

# ---- 1b. sample revenue vs industry revenue ----
def ecn(year):
    rows = json.loads((RAW / 'census' / f'ecn_484_{year}.json').read_text())
    h = rows[0]; code = h.index(f'NAICS{year}'); rev = h.index('RCPTOT')
    return {r[code]: int(r[rev]) / 1000 for r in rows[1:]}   # $ millions

def rev_10k(tk, year, pats):
    for f in sorted(TENK.glob(f'{tk}_{year}-12-*.txt')):
        t = f.read_text(errors='ignore')
        for p in pats:
            m = re.search(p, t)
            if m:
                return float(m.group(1).replace(',', ''))
    return None

for year in (2012, 2017, 2022):
    e = ecn(year)
    for mode, naics in (('Truckload', '484121'), ('LTL', '484122')):
        g = d[d.ticker.isin(MODES[mode]) & (d.fiscal_year == year) & (d.period == 'FY')]
        # carriers that state only a percent: take total revenue from the same 10-K (coverage only)
        revs = {}
        for r in g.itertuples():
            if pd.notna(r.base_revenue_musd):
                revs[r.ticker] = float(r.base_revenue_musd)
            else:
                v = rev_10k(r.ticker, year, [r'Revenue from operations \$ ?([\d,]+)', r'Operating [Rr]evenue \$ ?([\d,]+)'])
                assert v, (r.ticker, year)
                revs[r.ticker] = v / 1000
        tot = sum(revs.values())
        out['industry'][f'{mode} {year}'] = dict(
            sample_revenue_musd=round(tot), industry_musd=round(e[naics]), share=round(tot / e[naics], 3),
            carriers={k: round(v) for k, v in revs.items()},
            note=f'Economic Census {year}, NAICS {naics}; carrier revenue is segment revenue and can include work outside {naics}')

for year in (2012, 2017, 2022, 2025):
    g = d[d.ticker.isin(MODES['Rail']) & (d.fiscal_year == year) & (d.period == 'FY')]
    ours = float(g.base_revenue_musd.sum())
    csx = rev_10k('CSX', year, [r'Total [Rr]evenue \$ ?([\d,]+)', r'Revenue \$ ?([\d,]+)'])
    bnsf = rev_10k('BNSF', year, [r'Total revenues \$ ?([\d,]+)', r'Revenues \$ ?([\d,]+)'])
    if csx and bnsf:
        out['industry'][f'Rail {year}'] = dict(sample_revenue_musd=round(ours), big_four_musd=round(ours + csx + bnsf),
                                               share=round(ours / (ours + csx + bnsf), 3), csx=csx, bnsf=bnsf,
                                               note='Share of the four largest U.S. railroads (UP, NS, CSX, BNSF) by revenue')

# ---- 2. EIA diesel ----
se = pd.read_excel(EIA / 'dieselfuel_recent_prices_and_SEs.xlsx')
se.columns = ['date', 'area', 'price', 'se', 'cv_flag']
us = se[se.area == 'United States']
comp = {}
for sheet in ('Comparison May 30, 2022', 'Comparison June 6, 2022'):
    c = pd.read_excel(EIA / 'dieselfuel_sample_comparisons.xlsx', sheet, header=None)
    row = c[c[0].astype(str).str.strip() == 'U.S.'].iloc[0]
    comp[sheet[11:]] = dict(old=float(row[2]), old_se=float(row[3]), new=float(row[4]), new_se=float(row[5]),
                            diff=float(row[6]), diff_se=float(row[7]))
out['diesel'] = dict(
    eras=[dict(period='1994 to about 2011', outlets=350, weighting='sample design v1 (EIA archive ver01)'),
          dict(period='about 2011 to June 6, 2022', outlets=403, weighting='state averages unweighted, then weighted; target CV at most 1%'),
          dict(period='June 13, 2022 on', outlets=590, weighting='each outlet weighted by its annual sales volume')],
    standard_errors=dict(weeks=int(len(us)), first=str(us.date.min().date()), last=str(us.date.max().date()),
                         median_cents=round(float(us.se.median()) * 100, 2), max_cents=round(float(us.se.max()) * 100, 2),
                         latest_cents=round(float(us.sort_values('date').se.iloc[-1]) * 100, 2),
                         weeks_flagged_cv_over_5pct=int(us.cv_flag.notna().sum())),
    sample_change_2022=comp)
(PROCESSED / 'coverage.json').write_text(json.dumps(out, indent=1, default=str))

# ---- summary ----
print('Industry coverage (carrier revenue / industry revenue):')
for k, v in out['industry'].items():
    print(f"  {k}: {v['share']*100:.1f}%  (${v['sample_revenue_musd']:,}M of ${v.get('industry_musd', v.get('big_four_musd')):,}M)")
print('Ring inputs by kind, all years:')
for mode, tks in MODES.items():
    print(' ', mode, d[d.ticker.isin(tks)].kind.value_counts().to_dict())
print('Diesel SE:', out['diesel']['standard_errors'])
print('2022 sample change:', {k: f"{v['diff']*100:+.1f}c (se {v['diff_se']*100:.1f}c)" for k, v in comp.items()})
