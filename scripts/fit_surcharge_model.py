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
         data/reference/tariffs.json (and, when present locally, the carriers' own documents)
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

# ---- published tariffs ----
# The carriers' own documents stay on this machine only (data/reference/, not in git).
# Their rules are recorded in data/reference/tariffs.json, which is in git. When the
# source documents are present, the rules are re-read from them and must match.
TARIFFS = REF / 'tariffs.json'


def odfl_pct(p, T):
    for lo, hi, v in T['table']:
        if lo <= p < hi:
            return v
    a = T['above']
    return T['table'][-1][2] + a['inc'] * (math.floor((p - a['start']) / a['step'] + 1e-9) + 1) if p >= a['start'] else 0.0


def up_pct(p, U):
    return 0.0 if p < U['threshold'] else U['start'] + U['inc'] * math.floor((p - U['threshold']) / U['step'] + 1e-9)


if (REF / 'ODFL_128-CC.txt').exists() and (REF / 'UP_carload_rate_based.html').exists():
    t = (REF / 'ODFL_128-CC.txt').read_text()
    assert 'Effective: April 9, 2025' in t
    rows = sorted((int(a) / 100, int(b) / 100, float(p)) for a, b, p in re.findall(r'(\d{3}) (\d{3}) (\d+\.\d\d)%', t))
    assert len(rows) == 80 and rows[0][0] == 1.00 and rows[-1][1] == 5.10, (len(rows), rows[0], rows[-1])
    assert all(rows[i][1] == rows[i + 1][0] for i in range(len(rows) - 1)), 'gap in ODFL table'
    assert 'For each 5 cents increase in the Fuel Index above 510 cents, increase the Fuel Surcharge by 0.5%' in t
    u = re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', (REF / 'UP_carload_rate_based.html').read_text(errors='ignore'))))
    assert 'equals or exceeds $1.35 per gallon, a surcharge beginning at 1.5% will apply' in u
    assert 'For every five-cent increase above $1.35 per gallon, the surcharge applied will increase by 0.5%' in u
    months = [(m, float(pc), float(b)) for m, pc, b in re.findall(r'(\w{3,4} 2026) (\d+\.\d)% \w{3,4} 2026 \$(\d\.\d{3})', u)]
    from_source = dict(
        odfl=dict(name='Old Dominion tariff ODFL 128-CC (effective April 9, 2025)',
                  source='https://www.odfl.com/us/en/resources/fuel-surcharge.html', table=[list(r) for r in rows],
                  above=dict(start=5.10, step=0.05, inc=0.5),
                  check=dict(diesel=6.285, published_pct=53.32, week='2026-09-14')),
        up=dict(name='Union Pacific carload rate-based standard HDF surcharge', source='https://www.up.com/shipping/surcharge/revenue',
                threshold=1.35, start=1.5, step=0.05, inc=0.5, lag_months=2,
                check=[dict(month=m, published_pct=pc, hdf_avg=b) for m, pc, b in months]))
    if TARIFFS.exists():
        saved = json.loads(TARIFFS.read_text())
        assert saved == json.loads(json.dumps(from_source)), 'tariffs.json no longer matches the source documents'
    TARIFFS.write_text(json.dumps(from_source, indent=1))
T = json.loads(TARIFFS.read_text())
# every recorded published value must reproduce from the recorded rules
c = T['odfl']['check']
assert abs(odfl_pct(c['diesel'], T['odfl']) - c['published_pct']) < 1e-9
for c in T['up']['check']:
    assert abs(up_pct(c['hdf_avg'], T['up']) - c['published_pct']) < 1e-9, c
odfl = {k: T['odfl'][k] for k in ('name', 'table', 'above')}
up = {k: T['up'][k] for k in ('name', 'threshold', 'start', 'step', 'inc', 'lag_months')}

out = dict(truckload=dict(base_price=1.25, mpg=6.0, base_rate_per_mile=2.50),
           effective=eff, sensitivity_fit_from_2002=sens, tariffs=dict(odfl=odfl, up=up))
(PROCESSED / 'surcharge_model.json').write_text(json.dumps(out, indent=1))
for k, v in eff.items():
    print(f"{k:4s} effective: on-base % = {v['a']} + {v['b']} x diesel  (r {v['r']}, n {v['n']}, {v['years']}, sd {v['resid_sd']}); "
          f"from 2002: {sens[k]['a']} + {sens[k]['b']} x diesel")
print('ODFL at $6.285:', odfl_pct(6.285, T['odfl']), '| UP months reproduced:', len(T['up']['check']))
