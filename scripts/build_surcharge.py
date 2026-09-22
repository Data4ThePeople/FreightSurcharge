"""Merge the four 10-K extracts into one table and check every row against its filing.

Inputs:  data/extract/extract_*.csv, data/raw/sec_10k/*.txt
Outputs: data/processed/fuel_surcharge_by_mode.csv   one row per carrier-year
         data/processed/reported.json                mode averages the calculator plots as rings
         data/processed/surcharge_checks.csv         every check, every row, pass or fail

Checks, per row (DATASETS.md issue 5):
  quote_in_filing   the quote appears word for word in the filing
  fsc_in_quote      the surcharge number in the row appears in the quote
                    (for derived rows: each component appears; for company-stated
                    percents: the percent appears)
  base_in_filing    the revenue base appears in the filing, on a revenue line
  pct_math          fuel_surcharge_pct == round(100 * fsc / base, 2)
Any failure stops the build.
"""
import csv, json, re
import pandas as pd
from common import EXTRACT, PROCESSED, tenk, appears

MODE_NAMES = {'Intermodal/Truck mix': 'Intermodal/truck mix'}
MODE_KEYS = {'Truckload': 'tl', 'LTL': 'ltl', 'Rail': 'rail'}   # J.B. Hunt is kept out of the averages
# Components for derived rows: every number used must be in the quote.
COMPONENTS = {('SAIA', 2002): (489.8, 480.3), ('SAIA', 2003): (520.7, 502.3),
              ('SAIA', 2004): (645.4, 607.8), ('SAIA', 2005): (754.0, 679.9),
              ('MRTN', 2007): (83.786, 3.314)}

REVENUE = r'revenue'   # a base must appear within 250 characters after this word

E = pd.concat([pd.read_csv(f) for f in sorted(EXTRACT.glob('extract_*.csv'))], ignore_index=True)
E['source_file'] = E.source_file.str.split('/').str[-1]
dropped = E[E.method == 'yoy_change_only']
E = E[E.method != 'yoy_change_only'].copy()
assert not E.duplicated(['ticker', 'fiscal_year']).any(), 'duplicate carrier-year'

E['mode'] = E['mode'].replace(MODE_NAMES)
calc = (100 * E.fuel_surcharge_revenue_musd / E.base_revenue_musd).round(2)
E['fuel_surcharge_pct'] = E.fuel_surcharge_pct.fillna(calc)

checks = []
for r in E.itertuples():
    t = tenk(r.source_file)
    c = dict(ticker=r.ticker, fiscal_year=r.fiscal_year, method=r.method)
    c['quote_in_filing'] = r.quote in t
    if r.method == 'stated_pct':
        c['fsc_in_quote'] = bool(re.search(r'(?<![\d.])' + re.escape(f'{r.fuel_surcharge_pct:.1f}') + r' ?(%|percent)', r.quote))
        c['base_in_filing'] = True          # the company states the percent; no base used
        c['pct_math'] = True
    else:
        comps = COMPONENTS.get((r.ticker, r.fiscal_year))
        if comps:
            c['fsc_in_quote'] = all(appears(x, r.quote) for x in comps)
            if r.method == 'derived_subtraction':
                c['fsc_in_quote'] &= abs((comps[0] - comps[1]) - r.fuel_surcharge_revenue_musd) < 1e-6
            else:
                c['fsc_in_quote'] &= abs(sum(comps) - r.fuel_surcharge_revenue_musd) < 1e-6
        else:
            c['fsc_in_quote'] = appears(r.fuel_surcharge_revenue_musd, r.quote)
        c['base_in_filing'] = appears(r.base_revenue_musd, t, near=REVENUE)
        c['pct_math'] = abs(round(100 * r.fuel_surcharge_revenue_musd / r.base_revenue_musd, 2) - r.fuel_surcharge_pct) < 1e-9
    checks.append(c)
C = pd.DataFrame(checks)
PROCESSED.mkdir(parents=True, exist_ok=True)
C.to_csv(PROCESSED / 'surcharge_checks.csv', index=False)
tests = ['quote_in_filing', 'fsc_in_quote', 'base_in_filing', 'pct_math']
fails = C[~C[tests].all(axis=1)]
print(f'{len(C)} rows checked; {len(fails)} with a failure')
if len(fails):
    print(fails.to_string(index=False))
    raise SystemExit('check failures: see data/processed/surcharge_checks.csv')

E['source_filing'] = E.source_file.map(lambda f: '{} 10-K, period ending {}'.format(*f[:-4].split('_', 1)))
out = E.rename(columns={'fuel_surcharge_pct': 'fuel_surcharge_pct_of_revenue'})[
    ['mode', 'company', 'ticker', 'fiscal_year', 'fuel_surcharge_revenue_musd', 'base_revenue_musd',
     'fuel_surcharge_pct_of_revenue', 'scope', 'method', 'source_filing', 'quote']]
out = out.sort_values(['mode', 'ticker', 'fiscal_year'])
out.to_csv(PROCESSED / 'fuel_surcharge_by_mode.csv', index=False)

rep = {}
for mode, key in MODE_KEYS.items():
    m = out[out['mode'] == mode]
    # average unrounded shares; company-stated percents have no dollars behind them
    exact = (100 * m.fuel_surcharge_revenue_musd / m.base_revenue_musd).fillna(m.fuel_surcharge_pct_of_revenue)
    g = exact.groupby(m.fiscal_year)
    rep[key] = {str(y): {'avg': round(float(v.mean()), 2), 'n': int(v.size)} for y, v in g}
(PROCESSED / 'reported.json').write_text(json.dumps(rep, separators=(',', ':')))
print(f'wrote {len(out)} rows; dropped {len(dropped)} change-only rows:',
      ', '.join(f'{a} {b}' for a, b in zip(dropped.ticker, dropped.fiscal_year)))
