"""Freight's share of consumer prices, from the BEA 2023 input-output tables.

For each layer (retailer cost of goods, consumer goods prices, all consumer
spending) this computes how many cents of for-hire truck (484) and rail (482)
output sit behind each dollar of consumer spending, counting every step of
production (the Leontief total requirements).

Method: a price change dp_k in commodity k raises the price of commodity j by
dp_k * L[k,j] / L[k,k], where L is the commodity-by-commodity total
requirements table (the standard cost-push price model for a shock to one
sector). Weighting by personal consumption spending f_j gives freight's share
of a layer:  sum_j (L[k,j] / L[k,k]) * f_j  /  sum_j f_j.

Inputs:  data/raw/bea/AllTablesSUP.zip  (CxC_TR_1997-2023_Summary.xlsx)
         data/raw/bea/AllTablesIO.zip   (IOUse_After_Redefinitions_PRO_1997-2023_Summary.xlsx)
Output:  data/processed/io_shares.json  percent shares the calculator reads
"""
import io, json, zipfile
import numpy as np
import pandas as pd
from common import BEA, PROCESSED

YEAR = 2023
TRUCK, RAIL = '484', '482'


def sheet(zipname, member, year):
    with zipfile.ZipFile(BEA / zipname) as z:
        return pd.read_excel(io.BytesIO(z.read(member)), str(year), header=None)


def total_requirements(year):
    d = sheet('AllTablesSUP.zip', 'CxC_TR_1997-2023_Summary.xlsx', year)
    assert 'Total Requirements' in str(d.iloc[0, 0]) and str(d.iloc[3, 0]) == str(year)
    codes = [str(c) for c in d.iloc[5, 2:].tolist()]
    rows = [str(r) for r in d.iloc[7:, 0].tolist()]
    L = d.iloc[7:, 2:].copy(); L.index = rows; L.columns = codes
    L = L[~L.index.duplicated()]
    L = L.loc[[c for c in codes if c in L.index], codes].apply(pd.to_numeric, errors='coerce').fillna(0)
    assert L.shape[0] == L.shape[1], L.shape
    assert (np.diag(L) >= 1).all(), 'total requirements diagonal should be at least 1'
    return L


def pce(year):
    u = sheet('AllTablesIO.zip', 'IOUse_After_Redefinitions_PRO_1997-2023_Summary.xlsx', year)
    assert "Producers' Prices" in str(u.iloc[0, 0]) and str(u.iloc[3, 0]) == str(year)
    hdr = [str(h) for h in u.iloc[5].tolist()]
    i = hdr.index('F010')  # personal consumption expenditures
    f = u.iloc[6:, [0, 1, i]].copy(); f.columns = ['code', 'name', 'pce']
    f['code'] = f.code.astype(str)
    f['pce'] = pd.to_numeric(f.pce, errors='coerce')
    f = f.dropna(subset=['pce']).drop_duplicates('code').set_index('code')
    return f


L = total_requirements(YEAR)
F = pce(YEAR)
f = F.pce.reindex(L.columns).fillna(0)
missing = sorted(set(F.index) - set(L.columns) - {'nan'})
C = L.div(np.diag(L), axis=0)   # C[k, j] = L[k, j] / L[k, k]

goods = [c for c in L.columns if c.startswith(('111', '113', '211', '212'))
         or (c[:3].isdigit() and 311 <= int(c[:3]) <= 339)] + ['Used']
freight_margins = ['482', '483', '484']
wholesale = ['42']
retail = ['441', '445', '452', '4A0']
LAYERS = {
    'cogs':  ('Delivered goods cost to the retailer', goods + freight_margins + wholesale),
    'goods': ('Consumer goods prices after retail markup', goods + freight_margins + wholesale + retail),
    'pce':   ('All consumer spending, goods and services', list(L.columns)),
}

out = {'year': YEAR, 'vintage': 'BEA input-output accounts, September 2024 release', 'layers': {}}
for key, (name, cols) in LAYERS.items():
    assert all(c in L.columns for c in cols), [c for c in cols if c not in L.columns]
    tot = float(f[cols].sum())
    share = lambda k: float((C.loc[k, cols] * f[cols]).sum()) / tot * 100
    out['layers'][key] = dict(name=name, spending_bn=round(tot / 1e3, 1),
                              truck=round(share(TRUCK), 2), rail=round(share(RAIL), 2))
    print(f"{key:6s} {name:45s} ${tot/1e6:5.2f} trillion  truck {share(TRUCK):5.2f}%  rail {share(RAIL):5.2f}%")
print('PCE rows not in the requirements table:', missing)
# ---- truck mix: LTL share of for-hire trucking revenue, 2022 Economic Census ----
from common import RAW
def ecn(year):
    rows = json.loads((RAW / 'census' / f'ecn_484_{year}.json').read_text())
    h = rows[0]; code = h.index(f'NAICS{year}'); rev = h.index('RCPTOT')
    return {r[code]: int(r[rev]) for r in rows[1:]}
mix = {}
for year in (2022, 2017):
    e = ecn(year)
    parts = e['48411'] + e['484121'] + e['484122'] + e['4842']
    assert abs(parts - e['484']) <= 2, (year, parts, e['484'])   # industries add to the total
    mix[year] = dict(total_bn=round(e['484'] / 1e6, 1), ltl_bn=round(e['484122'] / 1e6, 1),
                     ltl_share=round(e['484122'] / e['484'], 4))
out['truck_mix'] = dict(source='Economic Census 2022, NAICS 484 revenue (RCPTOT)',
                        ltl=mix[2022]['ltl_share'], truckload_formula=round(1 - mix[2022]['ltl_share'], 4),
                        note='LTL (484122) uses the LTL formula; all other for-hire trucking uses the truckload formula',
                        by_year=mix)
print('truck mix:', {y: f"LTL {m['ltl_share']*100:.1f}% of ${m['total_bn']}B" for y, m in mix.items()})
PROCESSED.mkdir(parents=True, exist_ok=True)
(PROCESSED / 'io_shares.json').write_text(json.dumps(out, indent=1))
