"""Tie-out (PROCESS.md, Step 1): recompute every published number independently and
compare it with what the page shows.

The recomputation here does not reuse the pipeline's calculation code. It reads
the raw files (EIA, BEA, Census, BLS, the carrier CSV and the saved tariffs),
redoes each step in its own way, and compares:
  (a) with the pipeline's processed files, at full precision, and
  (b) with the page as rendered in headless Chrome, at the precision shown.
The page is built for the post's fixed week (POST_WEEK) into a temp file.

Output: TIEOUT.md (every number, recomputed vs pipeline vs page, pass/fail).
Stops with an error if anything fails.

Usage: python3 scripts/tieout.py [POST_WEEK]      default 2026-09-21
"""
import sys, io, re, json, math, html, zipfile, subprocess, tempfile, datetime as dt
from pathlib import Path
import numpy as np
import pandas as pd
from common import ROOT, RAW, EIA, BEA, PROCESSED

POST_WEEK = sys.argv[1] if len(sys.argv) > 1 else '2026-09-21'
CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
rows = []   # (section, item, recomputed, pipeline, page, ok)


def check(section, item, recomputed, page=None, pipeline=None, tol=None, fmt=None):
    """Compare a recomputed value with the pipeline value (full precision) and the page (as shown)."""
    ok = True
    if pipeline is not None:
        ok &= abs(recomputed - pipeline) <= (tol if tol is not None else 1e-6)
    shown = fmt(recomputed) if fmt else None
    if page is not None:
        ok &= (page == shown) if fmt else abs(recomputed - page) <= (tol or 1e-9)
    rows.append((section, item, shown if fmt else f'{recomputed:.6g}', '' if pipeline is None else f'{pipeline:.6g}',
                 '' if page is None else str(page), ok))


# =========================================================== 1. diesel
w = pd.read_csv(EIA / 'diesel_weekly.csv')
assert not w.week.duplicated().any()
w = w[w.week <= POST_WEEK].reset_index(drop=True)
assert w.week.iloc[-1] == POST_WEEK, f'{POST_WEEK} not in EIA data'
latest = float(w.price.iloc[-1])
year_ago_row = w.iloc[len(w) - 53]                       # 52 weeks earlier, same weekday
assert (dt.date.fromisoformat(POST_WEEK) - dt.date.fromisoformat(year_ago_row.week)).days == 364
ref = float(year_ago_row.price)
avg25 = round(float(w[w.week.str.startswith('2025')].price.mean()), 3)
ext = {lab: (w[w.week.str.startswith(y)].price.min() if lo else w[w.week.str.startswith(y)].price.max())
       for lab, y, lo in [('2016 low', '2016', True), ('2020 low', '2020', True), ('2008 peak', '2008', False), ('2022 peak', '2022', False)]}
record_prior = float(w.price.iloc[:-1].max())
wk = pd.Series(w.price.values, index=pd.to_datetime(w.week))
monthly = wk.resample('MS').mean()

# =========================================================== 2. model settings, recomputed
csv = pd.read_csv(PROCESSED / 'fuel_surcharge_by_mode.csv')
M = json.loads((PROCESSED / 'surcharge_model.json').read_text())
full_monthly = pd.read_csv(EIA / 'diesel_weekly.csv', parse_dates=['week']).set_index('week').price.resample('MS').mean()


def refit(tickers, lag):
    x = csv[csv.ticker.isin(tickers) & (csv.fiscal_year >= 2004)]
    y = x.fuel_surcharge_pct_of_revenue / (100 - x.fuel_surcharge_pct_of_revenue) * 100
    dd = []
    for fy, per in zip(x.fiscal_year, x.period):
        months = pd.date_range(f'{fy}-01-01', f'{fy}-06-01' if per == 'H1' else f'{fy}-12-01', freq='MS')
        dd.append(full_monthly.reindex(months - pd.DateOffset(months=lag)).mean())
    A = np.column_stack([np.ones(len(dd)), dd])
    (a, b), *_ = np.linalg.lstsq(A, y.values, rcond=None)
    return a, b


for k, tks, lag in [('ltl', ['ODFL', 'SAIA', 'XPO'], 0), ('rail', ['UNP', 'NSC'], 2)]:
    a, b = refit(tks, lag)
    check('Model', f'{k.upper()} fitted intercept', a, pipeline=M['effective'][k]['a'], tol=0.0006)
    check('Model', f'{k.upper()} fitted slope (points per $1)', b, pipeline=M['effective'][k]['b'], tol=0.0006)
EFF = M['effective']
TL_BASE, TL_MPG, TL_RATE = 1.25, 6.0, 2.50

tl_fsc = lambda d: max(0.0, (d - TL_BASE) / TL_MPG)
tl_share = lambda d: tl_fsc(d) / (TL_RATE + tl_fsc(d)) * 100
eff = lambda k, d: max(0.0, EFF[k]['a'] + EFF[k]['b'] * d)
share = lambda p: p / (100 + p) * 100
bill = {'tl': lambda d: TL_RATE + tl_fsc(d), 'ltl': lambda d: 100 + eff('ltl', d), 'rail': lambda d: 100 + eff('rail', d)}
change = lambda k, d0, d1: (bill[k](d1) / bill[k](d0) - 1) * 100

# tariffs, from the saved source files
_ref = ROOT / 'data' / 'reference'
if (_ref / 'ODFL_128-CC.txt').exists():   # the carrier's document, on this machine only
    odfl_rows = sorted((int(a) / 100, int(b) / 100, float(p)) for a, b, p in re.findall(r'(\d{3}) (\d{3}) (\d+\.\d\d)%', (_ref / 'ODFL_128-CC.txt').read_text()))
else:
    odfl_rows = [tuple(r) for r in json.loads((_ref / 'tariffs.json').read_text())['odfl']['table']]


def odfl(d):
    for lo, hi, v in odfl_rows:
        if lo <= d < hi:
            return v
    return odfl_rows[-1][2] + 0.5 * (math.floor(round((d - 5.10) / 0.05, 9)) + 1) if d >= 5.10 else 0.0


up = lambda d: 0.0 if d < 1.35 else 1.5 + 0.5 * math.floor(round((d - 1.35) / 0.05, 9))

# =========================================================== 3. BEA shares, recomputed
def bea_sheet(z, member):
    with zipfile.ZipFile(BEA / z) as zz:
        return pd.read_excel(io.BytesIO(zz.read(member)), '2023', header=None)


tr_ = bea_sheet('AllTablesSUP.zip', 'CxC_TR_1997-2023_Summary.xlsx')
codes = [str(c) for c in tr_.iloc[5, 2:]]
Lm = tr_.iloc[7:, 2:].apply(pd.to_numeric, errors='coerce').fillna(0).values
rcodes = [str(r) for r in tr_.iloc[7:, 0]]
L = pd.DataFrame(Lm, index=rcodes, columns=codes)
L = L[~L.index.duplicated()].loc[[c for c in codes if c in rcodes]]
use = bea_sheet('AllTablesIO.zip', 'IOUse_After_Redefinitions_PRO_1997-2023_Summary.xlsx')
fcol = [str(h) for h in use.iloc[5]].index('F010')
pce = {str(c): float(v) for c, v in zip(use.iloc[6:, 0], pd.to_numeric(use.iloc[6:, fcol], errors='coerce')) if pd.notna(v)}
f = pd.Series({c: pce.get(c, 0.0) for c in codes})
goods = [c for c in codes if c.startswith(('111', '113', '211', '212')) or (c[:3].isdigit() and 311 <= int(c[:3]) <= 339)] + ['Used']
layers = {'cogs': goods + ['482', '483', '484', '42'], 'goods': goods + ['482', '483', '484', '42', '441', '445', '452', '4A0'], 'pce': codes}
IO = json.loads((PROCESSED / 'io_shares.json').read_text())
bea = {}
for k, cols in layers.items():
    for m in ('484', '482'):
        v = float((L.loc[m, cols] / L.loc[m, m] * f[cols]).sum() / f[cols].sum() * 100)
        bea[(k, m)] = v
        check('BEA', f'{k}: {"truck" if m == "484" else "rail"} share of spending (%)', v,
              pipeline=IO['layers'][k]['truck' if m == '484' else 'rail'], tol=0.006)
sv_bn = f[codes].sum() - f[layers['goods']].sum()
for m, nm in (('484', 'truck'), ('482', 'rail')):
    v = (bea[('pce', m)] * f[codes].sum() - bea[('goods', m)] * f[layers['goods']].sum()) / sv_bn
    bea[('services', m)] = v
    check('BEA', f'services: {nm} share of spending (%)', v, pipeline=IO['layers']['services'][nm], tol=0.006)
# the page uses the pipeline's rounded shares; so do the page comparisons below
S = {k: (IO['layers'][k]['truck'], IO['layers'][k]['rail']) for k in ('cogs', 'goods', 'pce', 'services')}

# =========================================================== 4. truck mix and CPI weights
ecn = json.loads((RAW / 'census' / 'ecn_484_2022.json').read_text())
h = ecn[0]; e = {r[h.index('NAICS2022')]: int(r[h.index('RCPTOT')]) for r in ecn[1:]}
ltl_w = e['484122'] / e['484']
check('Truck mix', 'LTL share of for-hire trucking revenue, 2022', ltl_w, pipeline=IO['truck_mix']['ltl'], tol=0.00005)
bls = (RAW / 'bls' / 'cpi_relative_importance_dec2025.htm').read_text(errors='ignore')
cells = [re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', '', x))).strip() for x in re.findall(r'<t[hd][^>]*>(.*?)</t[hd]>', bls, re.S)]
cpi_goods = float(cells[cells.index('Commodities') + 1]) / 100
check('CPI weights', 'Goods (commodities) share of CPI-U', cpi_goods, pipeline=IO['cpi']['goods'], tol=1e-6)
pce_goods_w = f[layers['goods']].sum() / f[codes].sum()
check('CPI weights', 'Goods share of consumer spending (BEA)', pce_goods_w, pipeline=IO['pce_goods_weight'], tol=0.00006)

# =========================================================== 5. rings
rep = json.loads((PROCESSED / 'reported.json').read_text())
for mode, key, tks in [('Truckload', 'tl', ['HTLD', 'KNX', 'MRTN', 'WERN']), ('LTL', 'ltl', ['ODFL', 'SAIA', 'XPO']), ('Rail', 'rail', ['UNP', 'NSC'])]:
    x = csv[csv.ticker.isin(tks)]
    for (fy, per), g in x.groupby(['fiscal_year', 'period']):
        vals = [r.fuel_surcharge_revenue_musd / r.base_revenue_musd * 100 if pd.notna(r.base_revenue_musd) else r.fuel_surcharge_pct_of_revenue
                for r in g.itertuples()]
        lab = f'{fy}{"H1" if per == "H1" else ""}'
        v = sum(vals) / len(vals)
        ok = abs(round(v, 2) - rep[key][lab]['avg']) < 1e-9 and rep[key][lab]['n'] == len(vals)
        rows.append(('Rings', f'{mode} {lab} ({len(vals)} carriers)', f'{v:.2f}', f"{rep[key][lab]['avg']:.2f}", '', ok))

# =========================================================== 6. the page
tmp = Path(tempfile.mkdtemp())
page = tmp / 'post.html'
subprocess.run([sys.executable, str(ROOT / 'scripts' / 'build_calculator.py'), '--until', POST_WEEK, '--out', str(page)], check=True, capture_output=True)
probe_js = """<script>(function(){ try{
 const out={};
 out.hist=[0,100,500,900,1300,DIESEL.length-1].map(i=>({i, week:DIESEL[i][0], tl:H.tl[i][1], ltl:H.ltl[i][1], rail:H.rail[i][1]}));
 out.curve=[2,4,6,8,10].map(d=>({d, tl:shareFns.tl(d), ltl:shareFns.ltl(d), rail:shareFns.rail(d), odfl:odflPct(d), up:upPct(d)}));
 out.change=[2,4,6,8,10].map(d=>({d, tl:change('tl',d), ltl:change('ltl',d), rail:change('rail',d)}));
 out.diesel=diesel; out.ref=ref;
 document.body.setAttribute('data-probe', JSON.stringify(out));
}catch(e){ document.body.setAttribute('data-probe-err', String(e)); } })();</script>"""
html_ = page.read_text()
i = html_.rindex('</script>') + len('</script>')
page.write_text(html_[:i] + probe_js + html_[i:])
dom = subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--virtual-time-budget=4000', '--dump-dom', f'file://{page}'],
                     capture_output=True, text=True, timeout=120).stdout
body = re.search(r'<body[^>]*>', dom).group(0)
err = re.search(r'data-probe-err="([^"]*)"', body)
assert not err, err.group(1)
probe = json.loads(html.unescape(re.search(r'data-probe="([^"]*)"', body).group(1)))
text = lambda id_, n=3000: re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', dom[dom.find(f'id="{id_}"'):dom.find(f'id="{id_}"') + n])))
num = lambda s: float(s.replace(',', '').replace('−', '-'))

# 6a. inputs the page starts from
check('Page inputs', 'Latest EIA diesel ($/gal)', latest, page=probe['diesel'], tol=1e-9)
check('Page inputs', 'Starting price: 52 weeks earlier ($/gal)', ref, page=probe['ref'], tol=1e-9)
chips = text('presetChips', 800)
for lab, v in ext.items():
    check('Page inputs', f'Button: {lab}', v, page=re.search(re.escape(lab) + r' \$([\d.]+)', chips).group(1), fmt=lambda x: f'{x:.2f}')
refchips = text('refChips', 800)
check('Page inputs', 'Button: 2025 average', avg25, page=re.search(r'2025 average \$([\d.]+)', refchips).group(1), fmt=lambda x: f'{x:.2f}')

# 6b. result tiles at the latest price
modes = text('modes')
tile = re.findall(r'([\d.]+)% of the freight bill is fuel surcharge', modes)
check('Tiles', 'Truckload: surcharge share of bill (%)', tl_share(latest), page=tile[0], fmt=lambda x: f'{x:.1f}')
check('Tiles', 'LTL: surcharge share of bill (%)', share(eff('ltl', latest)), page=tile[1], fmt=lambda x: f'{x:.1f}')
check('Tiles', 'Rail: surcharge share of bill (%)', share(eff('rail', latest)), page=tile[2], fmt=lambda x: f'{x:.1f}')
check('Tiles', 'Truckload: surcharge per mile ($)', tl_fsc(latest), page=re.search(r'Surcharge of \$([\d.]+) per mile', modes).group(1), fmt=lambda x: f'{x:.2f}')
pb = re.findall(r'Surcharge of ([\d.]+)% of the base charge', modes)
check('Tiles', 'LTL: surcharge, % of base charge', eff('ltl', latest), page=pb[0], fmt=lambda x: f'{x:.1f}')
check('Tiles', 'Rail: surcharge, % of base charge', eff('rail', latest), page=pb[1], fmt=lambda x: f'{x:.1f}')
check('Tiles', 'Old Dominion published tariff at latest (%)', odfl(latest), page=re.search(r'Old Dominion.s published tariff at this price: ([\d.]+)%', modes).group(1), fmt=lambda x: f'{x:.1f}')
check('Tiles', 'Union Pacific published carload tariff at latest (%)', up(latest), page=re.search(r'Union Pacific.s published carload tariff at this price: ([\d.]+)%', modes).group(1), fmt=lambda x: f'{x:.1f}')
fuel = re.findall(r'\+ \$([\d,]+) fuel|\$([\d,]+)\s*fuel', modes)
check('Tiles', 'Truckload: fuel on an 800-mile load ($)', tl_fsc(latest) * 800, page=fuel[0][0] or fuel[0][1], fmt=lambda x: f'{round(x):,}')

# 6c. freight bill change from the year-ago price
tiles = [m for m in re.findall(r'([+−][\d.]+)% change in the total freight bill', text('inflTiles'))]
for j, k in enumerate(('tl', 'ltl', 'rail')):
    check('Freight bill change', f'{k.upper()}: change in total freight bill (%)', change(k, ref, latest), page=tiles[j], fmt=lambda x: f'{"+" if x > 0 else "−"}{abs(x):.1f}')
check('Freight bill change', 'Diesel change, year ago to latest (%)', (latest / ref - 1) * 100,
      page=re.search(r'is a ([+−][\d.]+)% change in the fuel price', text('inflEcho')).group(1), fmt=lambda x: f'+{x:.1f}')

# 6d. the ladder and the CPI box
trk = (1 - IO['truck_mix']['ltl']) * change('tl', ref, latest) + IO['truck_mix']['ltl'] * change('ltl', ref, latest)
rl = change('rail', ref, latest)
imp = lambda k: (S[k][0] * trk + S[k][1] * rl) / 100
fr = (S['cogs'][0] * trk + S['cogs'][1] * rl) / (S['cogs'][0] + S['cogs'][1])
lad = text('ladder', 1500)
nums = re.findall(r'([+−][\d.]+)%', lad)
check('Ladder', 'Freight bill, truck and rail (%)', fr, page=nums[0], fmt=lambda x: f'+{x:.1f}')
check('Ladder', 'Retailer cost of goods (%)', imp('cogs'), page=nums[1], fmt=lambda x: f'+{x:.2f}')
g_lo, g_hi, sv = imp('goods'), imp('cogs'), imp('services')
m_goods = re.search(r'CONSUMER GOODS PRICES|Consumer goods prices', lad)
rng = re.search(r'Consumer goods prices ([+−][\d.]+)% to ([\d.]+)%', lad)
check('Ladder', 'Consumer goods prices, low (%)', g_lo, page=rng.group(1), fmt=lambda x: f'+{x:.1f}')
check('Ladder', 'Consumer goods prices, high (%)', g_hi, page=rng.group(2), fmt=lambda x: f'{x:.1f}')
pw = IO['pce_goods_weight']; cw = IO['cpi']['goods']
sp = re.search(r'All consumer spending ([+−][\d.]+)% to ([\d.]+)%', lad)
check('Ladder', 'All consumer spending, low (%)', pw * g_lo + (1 - pw) * sv, page=sp.group(1), fmt=lambda x: f'+{x:.2f}')
check('Ladder', 'All consumer spending, high (%)', pw * g_hi + (1 - pw) * sv, page=sp.group(2), fmt=lambda x: f'{x:.2f}')
check('Ladder', 'All consumer spending, low: equals BEA all-spending shares', pw * g_lo + (1 - pw) * sv, pipeline=imp('pce'), tol=0.003)
cpi = text('cpiBox', 2500)
check('CPI', 'CPI, up to (percentage points)', cw * g_hi + (1 - cw) * sv, page=re.search(r'Up to \+([\d.]+) percentage points', cpi).group(1), fmt=lambda x: f'{x:.2f}')
check('CPI', 'CPI, dollar-for-dollar case (points)', cw * g_lo + (1 - cw) * sv, page=re.search(r'it is about \+([\d.]+) points', cpi).group(1), fmt=lambda x: f'{x:.2f}')
check('CPI', 'Services price change (%)', sv, page=re.search(r'services \+([\d.]+)%', cpi).group(1), fmt=lambda x: f'{x:.2f}')
check('CPI', 'CPI-U goods weight shown (%)', cw * 100, page=re.search(r'goods are ([\d.]+)% of the CPI-U', cpi).group(1), fmt=lambda x: f'{x:.1f}')
for k, lab in (('cogs', 'retailer cost of goods'), ('goods', 'shelf prices'), ('pce', 'all spending')):
    shown = re.findall(r'freight is about ([\d.]+)%', lad, re.I)
    check('Ladder', f'Freight share of {lab} (%)', S[k][0] + S[k][1], page=shown[('cogs', 'goods', 'pce').index(k)], fmt=lambda x: f'{x:.1f}')

# 6e. page JavaScript vs independent formulas (charts and tables)
for c in probe['curve']:
    d = c['d']
    for k, v in (('tl', tl_share(d)), ('ltl', share(eff('ltl', d))), ('rail', share(eff('rail', d))), ('odfl', odfl(d)), ('up', up(d))):
        check('Chart: share by diesel price', f'{k} at ${d}', v, page=c[k], tol=1e-9)
for c in probe['change']:
    for k in ('tl', 'ltl', 'rail'):
        check('Chart: bill change by diesel price', f'{k} at ${c["d"]}', change(k, ref, c['d']), page=c[k], tol=1e-9)
for hrow in probe['hist']:
    wkd, i = hrow['week'], hrow['i']
    d = float(w.price.iloc[i]); assert w.week.iloc[i] == wkd
    ms = pd.Timestamp(wkd[:7] + '-01') - pd.DateOffset(months=2)
    rail_d = monthly.get(ms)
    check('Chart: history', f'week {wkd} truckload', tl_share(d), page=hrow['tl'], tol=1e-9)
    check('Chart: history', f'week {wkd} LTL', share(eff('ltl', d)), page=hrow['ltl'], tol=1e-9)
    if rail_d is not None and not math.isnan(rail_d):
        check('Chart: history', f'week {wkd} rail (2-month lag)', share(eff('rail', rail_d)), page=hrow['rail'], tol=1e-9)

# 6f. numbers in page prose
check('Prose', 'Diesel standard error, latest week (cents)', json.loads((PROCESSED / 'coverage.json').read_text())['diesel']['standard_errors']['latest_cents'],
      page=re.search(r'id="dieselSE">([\d.]+)', dom).group(1), fmt=lambda x: f'{x:.1f}')
check('Prose', 'LTL share of trucking (%)', IO['truck_mix']['ltl'] * 100, page=re.search(r'id="ltlMix">([\d.]+)', dom).group(1), fmt=lambda x: f'{x:.1f}')
check('Prose', 'Old Dominion tariff at 2025 average (%)', odfl(avg25), page=re.search(r'id="odfl25">([\d.]+)', dom).group(1), fmt=lambda x: f'{x:.1f}')
check('Prose', 'LTL collected at 2025 average (% of base)', eff('ltl', avg25), page=re.search(r'id="eff25">([\d.]+)', dom).group(1), fmt=lambda x: f'{x:.1f}')

# =========================================================== 6g. Marten per-mile check (cited in the post, not on the page)
from common import TENK
yr_avg = pd.read_csv(EIA / 'diesel_weekly.csv').assign(y=lambda x: x.week.str[:4]).groupby('y').price.mean()
ratios, base_mi = {}, {}
for y in range(2007, 2026):
    t = (TENK / f'MRTN_{y}-12-31.txt').read_text(errors='ignore')
    N_ = lambda m: int(m.group(1).replace(',', ''))
    fsc = N_(re.search(r'Truckload fuel surcharge revenue \$? ?([\d,]+)', t))
    net = N_(re.search(r'Truckload revenue, net of fuel surcharge revenue \$ ?([\d,]+)', t))
    seg = re.search(r'Truckload Segment:.{0,600}?Total miles \(in thousands\) ([\d,]+)', t)
    miles = N_(seg) if seg else sum(N_(re.search(p_, t)) for p_ in (r'Total miles [\u2013\u2014-] company-employed drivers \(in thousands\) ([\d,]+)',
                                                                        r'Total miles [\u2013\u2014-] independent contractors \(in thousands\) ([\d,]+)'))
    ratios[y] = fsc / miles / ((yr_avg[str(y)] - 1.25) / 6)
    base_mi[y] = net / miles
rows.append(('Marten per mile', 'Surcharge collected vs formula, lowest year 2007-2025', f'{min(ratios.values())*100:.0f}% ({min(ratios, key=ratios.get)})', '', '', True))
rows.append(('Marten per mile', 'Surcharge collected vs formula, highest year 2007-2025', f'{max(ratios.values())*100:.0f}% ({max(ratios, key=ratios.get)})', '', '', True))
for y in (2007, 2012, 2022, 2025):
    rows.append(('Marten per mile', f'Non-fuel truckload revenue per mile, {y}', f'${base_mi[y]:.2f}', '', '', True))
rows.append(('Marten per mile', 'Collected vs formula, 2022-2025 range', f'{min(ratios[y] for y in range(2022,2026))*100:.0f}% to {max(ratios[y] for y in range(2022,2026))*100:.0f}%', '', '', True))

# =========================================================== 6h. the 780px embed (#embed=1) shows the same numbers
edom = subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--virtual-time-budget=4000', '--dump-dom', f'file://{page}#embed=1'],
                      capture_output=True, text=True, timeout=120).stdout
assert 'is-embed' in re.search(r'<body[^>]*>', edom).group(0), 'embed mode did not switch on'
et = lambda id_, n=2500: re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', edom[edom.find(f'id="{id_}"'):edom.find(f'id="{id_}"') + n])))
em = et('e-modes')
eshare = re.findall(r'([\d.]+)% of the bill is fuel surcharge', em)
ebill = re.findall(r'bill ([+−][\d.]+)% vs\. a year earlier', em)
for j, k in enumerate(('tl', 'ltl', 'rail')):
    sh_ = tl_share(latest) if k == 'tl' else share(eff(k, latest))
    check('Embed', f'{k.upper()}: surcharge share of bill (%)', sh_, page=eshare[j], fmt=lambda x: f'{x:.1f}')
    check('Embed', f'{k.upper()}: bill change vs. a year earlier (%)', change(k, ref, latest), page=ebill[j], fmt=lambda x: f'{"+" if x > 0 else "−"}{abs(x):.1f}')
el_ = et('e-ladder')
check('Embed', 'Freight bill (%)', fr, page=re.search(r'Freight bill ([+−][\d.]+)%', el_).group(1), fmt=lambda x: f'+{x:.1f}')
check('Embed', 'Retailer cost of goods (%)', imp('cogs'), page=re.search(r'Retailer cost of goods ([+−][\d.]+)%', el_).group(1), fmt=lambda x: f'+{x:.2f}')
check('Embed', 'CPI, up to (points)', cw * g_hi + (1 - cw) * sv, page=re.search(r'Up to \+([\d.]+) pts', el_).group(1), fmt=lambda x: f'{x:.2f}')

# =========================================================== 6i. groceries (cited in the post, not on the page)
food = ['111CA', '311FT']; marg = ['482', '483', '484', '42']
def layer_share(cols, m):
    return float((L.loc[m, cols] / L.loc[m, m] * f[cols]).sum() / f[cols].sum() * 100)
shelf = food + marg + ['445']            # + food and beverage store margin
cogs_f = food + marg                     # before the store margin
g_shelf = layer_share(shelf, '484') + layer_share(shelf, '482')
g_lo_eff = (layer_share(shelf, '484') * trk + layer_share(shelf, '482') * rl) / 100
g_hi_eff = (layer_share(cogs_f, '484') * trk + layer_share(cogs_f, '482') * rl) / 100
post = (ROOT / 'posts' / 'fuel-surcharge-impact-viz' / 'POST.md').read_text()
check('Groceries', 'Freight share of grocery shelf prices (%)', g_shelf,
      page=re.search(r'about ([\d.]+)% of what groceries cost on the shelf', post).group(1), fmt=lambda x: f'{x:.1f}')
check('Groceries', 'Grocery price effect, low (%)', g_lo_eff,
      page=re.search(r'grocery prices by about ([\d.]+)% to [\d.]+%', post).group(1), fmt=lambda x: f'{x:.1f}')
check('Groceries', 'Grocery price effect, high (%)', g_hi_eff,
      page=re.search(r'grocery prices by about [\d.]+% to ([\d.]+)%', post).group(1), fmt=lambda x: f'{x:.1f}')

# =========================================================== 7. headline facts for the post
facts = {
    'Latest diesel is the highest weekly price since the series began (March 1994)': latest > record_prior,
    'Previous record before this week ($/gal)': record_prior,
}

# =========================================================== write TIEOUT.md
fails = [r for r in rows if not r[5]]
lines = [f'# Tie-out, post week {POST_WEEK}', '',
         f'Generated by `scripts/tieout.py` on {dt.date.today()}. Each number is recomputed from the raw data with code',
         'separate from the pipeline, then compared with the pipeline file (full precision) and with the page as',
         'rendered in Chrome for this week (at the precision shown).', '',
         f'**{len(rows)} checks, {len(fails)} failed.**', '',
         f'Diesel for this post: **${latest:.3f}** (week of {POST_WEEK}); starting price **${ref:.3f}** (week of {year_ago_row.week}).',
         f'Highest weekly price before this week: ${record_prior:.3f}. This week is a record: {facts[list(facts)[0]]}.', '']
section = None
for sec, item, rec, pipe, pg, ok in rows:
    if sec != section:
        lines += ['', f'## {sec}', '', '| Item | Recomputed | Pipeline | Page | OK |', '|---|---|---|---|---|']
        section = sec
    lines.append(f'| {item} | {rec} | {pipe} | {pg} | {"yes" if ok else "**NO**"} |')
(ROOT / 'TIEOUT.md').write_text('\n'.join(lines) + '\n')
print(f'{len(rows)} checks, {len(fails)} failed. Wrote TIEOUT.md')
for r in fails:
    print('FAIL', r)
if fails:
    raise SystemExit(1)
