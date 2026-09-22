"""Surcharge settings for the calculator, each with a documented source.

Truckload: (EIA diesel - $1.25) / 6 mpg per mile. Checked against Marten's
  truckload surcharge per mile, 2007-2025 (DATASETS.md).
LTL and rail, "what shippers pay on average": surcharge as a percent of the
  non-surcharge charge, fitted as a straight line on diesel from the carriers'
  own 10-K and 10-Q figures, 2004 on. Rail uses the monthly average diesel
  price two months earlier, as Union Pacific bills it.
Published tariffs, for comparison: Old Dominion ODFL 128-CC (effective April 9,
  2025) and Union Pacific's carload rate-based standard HDF surcharge. Each is
  checked against the carrier's own published value for a known week.

Inputs:  data/processed/fuel_surcharge_by_mode.csv, data/raw/eia/diesel_weekly.csv,
         data/reference/ODFL_128-CC.txt, data/reference/UP_carload_rate_based.html
Output:  data/processed/surcharge_model.json
"""
import json, math, re, html
import numpy as np
import pandas as pd
from common import ROOT, EIA, PROCESSED

REF = ROOT / 'data' / 'reference'
FIT_FROM = 2004   # 2002-2003 rows are from years when surcharge programs were still being adopted

w = pd.read_csv(EIA / 'diesel_weekly.csv', parse_dates=['week']).set_index('week').price
monthly = w.resample('MS').mean()
d = pd.read_csv(PROCESSED / 'fuel_surcharge_by_mode.csv')


def period_diesel(year, period, lag):
    s = monthly.shift(lag)[str(year)]
    return float((s[:6] if period == 'H1' else s).mean())


def fit(tickers, lag, start):
    x = d[d.ticker.isin(tickers) & (d.fiscal_year >= start)].copy()
    x['on_base'] = x.fuel_surcharge_pct_of_revenue / (100 - x.fuel_surcharge_pct_of_revenue) * 100
    x['diesel'] = [period_diesel(y, p, lag) for y, p in zip(x.fiscal_year, x.period)]
    b, a = np.polyfit(x.diesel, x.on_base, 1)
    resid = x.on_base - (a + b * x.diesel)
    return dict(a=round(float(a), 3), b=round(float(b), 3), zero_at=round(float(-a / b), 3), n=int(len(x)),
                r=round(float(np.corrcoef(x.diesel, x.on_base)[0, 1]), 3),
                resid_sd=round(float(resid.std(ddof=2)), 2), carriers=sorted(tickers),
                years=f'{int(x.fiscal_year.min())}-{int(x.fiscal_year.max())}', lag_months=lag)


eff = {'ltl': fit(['ODFL', 'SAIA', 'XPO'], 0, FIT_FROM), 'rail': fit(['UNP', 'NSC'], 2, FIT_FROM)}
sens = {'ltl': fit(['ODFL', 'SAIA', 'XPO'], 0, 2002), 'rail': fit(['UNP', 'NSC'], 2, 2002)}

# ---- Old Dominion ODFL 128-CC ----
t = (REF / 'ODFL_128-CC.txt').read_text()
assert 'Effective: April 9, 2025' in t
rows = [(int(a) / 100, int(b) / 100, float(p)) for a, b, p in re.findall(r'(\d{3}) (\d{3}) (\d+\.\d\d)%', t)]
rows.sort()
assert len(rows) == 80 and rows[0][0] == 1.00 and rows[-1][1] == 5.10, (len(rows), rows[0], rows[-1])
assert all(rows[i][1] == rows[i + 1][0] for i in range(len(rows) - 1)), 'gap in ODFL table'
assert 'For each 5 cents increase in the Fuel Index above 510 cents, increase the Fuel Surcharge by 0.5%' in t
odfl = dict(name='Old Dominion tariff ODFL 128-CC (effective April 9, 2025)', table=rows,
            above=dict(start=5.10, step=0.05, inc=0.5))


def odfl_pct(p):
    for lo, hi, v in rows:
        if lo <= p < hi:
            return v
    if p >= 5.10:
        return rows[-1][2] + 0.5 * (math.floor((p - 5.10) / 0.05 + 1e-9) + 1)
    return 0.0


assert abs(odfl_pct(6.285) - 53.32) < 1e-9, odfl_pct(6.285)   # ODFL site: 53.32% for EIA $6.285 (week of 9/14/2026)

# ---- Union Pacific carload rate-based ----
u = re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', (REF / 'UP_carload_rate_based.html').read_text(errors='ignore'))))
assert 'equals or exceeds $1.35 per gallon, a surcharge beginning at 1.5% will apply' in u
assert 'For every five-cent increase above $1.35 per gallon, the surcharge applied will increase by 0.5%' in u
up = dict(name='Union Pacific carload rate-based standard HDF surcharge', threshold=1.35, start=1.5, step=0.05, inc=0.5, lag_months=2)
up_pct = lambda p: 0.0 if p < 1.35 else 1.5 + 0.5 * math.floor((p - 1.35) / 0.05 + 1e-9)
for month, pct, basis in re.findall(r'(\w{3,4} 2026) (\d+\.\d)% \w{3,4} 2026 \$(\d\.\d{3})', u):
    assert abs(up_pct(float(basis)) - float(pct)) < 1e-9, (month, pct, basis)   # every month on UP's page reproduces

out = dict(truckload=dict(base_price=1.25, mpg=6.0, base_rate_per_mile=2.50),
           effective=eff, sensitivity_fit_from_2002=sens, tariffs=dict(odfl=odfl, up=up))
(PROCESSED / 'surcharge_model.json').write_text(json.dumps(out, indent=1))
for k, v in eff.items():
    print(f"{k:4s} effective: on-base % = {v['a']} + {v['b']} x diesel  (r {v['r']}, n {v['n']}, {v['years']}, sd {v['resid_sd']}); "
          f"from 2002: {sens[k]['a']} + {sens[k]['b']} x diesel")
print('ODFL at $6.285:', odfl_pct(6.285), '| UP months reproduced:', len(re.findall(r'\w{3,4} 2026 \d+\.\d% \w{3,4} 2026 \$\d\.\d{3}', u)))
