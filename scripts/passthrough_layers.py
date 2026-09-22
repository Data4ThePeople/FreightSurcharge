import pandas as pd, numpy as np, math
from io import StringIO
from io import *  # noqa
import importlib.util,sys
spec=importlib.util.spec_from_file_location('iox','io.py'); iox=importlib.util.module_from_spec(spec); spec.loader.exec_module(iox)

# fuel-only freight bill change, calculator formulas, 2025 avg diesel -> latest
P=dict(tlBase=1.25,tlMpg=6,tlRate=2.5,ltlBase=1.15,ltlStep=.05,ltlInc=.35,railBase=1.9,railStep=.04,railInc=.25)
def stepp(d,b,s,i): return 0 if d<=b else math.ceil((d-b)/s-1e-9)*i
bill={'tl':lambda d:P['tlRate']+max(0,(d-P['tlBase'])/P['tlMpg']),
      'ltl':lambda d:100+stepp(d,P['ltlBase'],P['ltlStep'],P['ltlInc']),
      'rail':lambda d:100+stepp(d,P['railBase'],P['railStep'],P['railInc'])}
dz=pd.read_csv('../GASDESW.csv',index_col=0,parse_dates=True).iloc[:,0]
d0=dz['2025'].mean(); d1=dz.iloc[-1]
x={k:bill[k](d1)/bill[k](d0)-1 for k in bill}
print(f"diesel 2025 avg {d0:.3f} -> latest {d1:.3f} ({(d1/d0-1)*100:.1f}%)", {k:round(v*100,2) for k,v in x.items()})

GOODS_PREFIX=('111','113','211','212','3')
FREIGHT=['481','482','483','484','486','487OS']
RETAIL=['441','445','452','4A0']
year=2023
L=iox.tr(year); f=iox.use(year).dropna(subset=['pce']).drop_duplicates('code').set_index('code').pce
f=f.reindex(L.columns).fillna(0)
goods=[c for c in L.columns if c.startswith(GOODS_PREFIX) and not c.startswith('3') or c[:1]=='3' and len(c)>=3 and c[:3].isdigit() and 311<=int(c[:3])<=339]
goods=[c for c in L.columns if c.startswith(('111','113','211','212')) or (c[:3].isdigit() and 311<=int(c[:3])<=339)]
goods+=['Used'] if 'Used' in L.columns else []
C=L.div(np.diag(L),axis=0)   # c_kj = L_kj / L_kk
def content(k,cols): return float((C.loc[k,cols]*f[cols]).sum())
freight_margin=['482','483','484']  # rail/water/truck margins on PCE (air/pipeline mostly not goods delivery for consumers)
wh=['42']; rt=[c for c in RETAIL if c in L.columns]
layers={
 'Goods at the factory gate (producer value)':goods,
 'Delivered goods cost to the retailer (COGS)':goods+freight_margin+wh,
 'Consumer goods prices (after retail markup)':goods+freight_margin+wh+rt,
 'All consumer spending (goods and services)':list(L.columns),
}
rows=[]
for name,cols in layers.items():
    tot=float(f[cols].sum())
    tk=content('484',cols)/tot; rl=content('482',cols)/tot
    truck_x=(x['tl']+x['ltl'])/2
    imp=tk*truck_x+rl*x['rail']
    rows.append(dict(layer=name,value_bn=round(tot/1e3),truck_share_pct=round(tk*100,2),rail_share_pct=round(rl*100,2),price_impact_pct=round(imp*100,2)))
r=pd.DataFrame(rows); print(r.to_string(index=False))
print('retail cols',rt,'| goods n',len(goods))
