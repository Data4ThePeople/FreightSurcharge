"""Build dist/index.html from the template and the processed data.

Injects:  DIESEL    weekly EIA diesel, [["YYYY-MM-DD", price], ...]
          REPORTED  data/processed/reported.json
          IO        truck and rail shares by layer, from data/processed/io_shares.json
          MODEL     surcharge settings and published tariffs, data/processed/surcharge_model.json
Also writes data/processed/diesel.json (the same series the page embeds).

Usage: python3 scripts/build_calculator.py [--until YYYY-MM-DD]
"""
import csv, json, sys
from common import EIA, PROCESSED, SRC, DIST

until = sys.argv[sys.argv.index('--until') + 1] if '--until' in sys.argv else None
weeks = [(r['week'], float(r['price'])) for r in csv.DictReader(open(EIA / 'diesel_weekly.csv'))]
if until:
    weeks = [w for w in weeks if w[0] <= until]
assert weeks == sorted(weeks) and len({w for w, _ in weeks}) == len(weeks), 'weeks out of order or duplicated'
diesel = json.dumps([[w, p] for w, p in weeks], separators=(',', ':'))
(PROCESSED / 'diesel.json').write_text(diesel)

io_ = json.loads((PROCESSED / 'io_shares.json').read_text())['layers']
io_all = json.loads((PROCESSED / 'io_shares.json').read_text())
IO = json.dumps({**{k: {'truck': v['truck'], 'rail': v['rail']} for k, v in io_.items()},
                 'mix': {'ltl': io_all['truck_mix']['ltl'], 'tl': io_all['truck_mix']['truckload_formula']}}, separators=(',', ':'))
reported = (PROCESSED / 'reported.json').read_text()
cover = json.dumps(json.loads((PROCESSED / 'coverage.json').read_text())['diesel']['standard_errors'], separators=(',', ':'))
model = json.dumps(json.loads((PROCESSED / 'surcharge_model.json').read_text()), separators=(',', ':'))

t = (SRC / 'calculator.template.html').read_text()
for marker, value in [('/*DIESEL*/[]', diesel), ('/*REPORTED*/{}', reported), ('/*IO*/{}', IO), ('/*MODEL*/{}', model), ('/*COVER*/{}', cover)]:
    assert t.count(marker) == 1, marker
    t = t.replace(marker, value)
DIST.mkdir(exist_ok=True)
# parse-check the page script with the macOS JavaScript engine, if present, before writing
import subprocess, tempfile, os
JSC = '/System/Library/Frameworks/JavaScriptCore.framework/Versions/Current/Helpers/jsc'
if os.path.exists(JSC):
    i = t.index('<script>') + 8; js = t[i:t.index('</script>', i)]
    with tempfile.TemporaryDirectory() as d:
        open(f'{d}/page.js', 'w').write(js)
        open(f'{d}/chk.js', 'w').write('try{ new Function(read("%s/page.js")); print("ok") }catch(e){ print("PARSE ERROR: "+e) }' % d)
        out = subprocess.run([JSC, f'{d}/chk.js'], capture_output=True, text=True).stdout.strip()
    assert out == 'ok', out
(DIST / 'index.html').write_text(t)

# run the page in headless Chrome, if present, and stop on any JavaScript error
CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
if os.path.exists(CHROME):
    with tempfile.TemporaryDirectory() as d:
        probe = t.replace('<script>', '<script>window.onerror=(m,u,l,c)=>{document.body.setAttribute("data-err",m+" @"+l+":"+c)};', 1)
        open(f'{d}/probe.html', 'w').write(probe)
        dom = subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--virtual-time-budget=3000', '--dump-dom',
                              f'file://{d}/probe.html'], capture_output=True, text=True, timeout=120).stdout
    import re as _re
    err = _re.search(r'data-err="([^"]*)"', dom)
    assert dom and not err, f'page JavaScript error: {err.group(1) if err else "no output from Chrome"}'
    print('page runs in Chrome without errors')
print('dist/index.html:', len(weeks), 'weeks through', weeks[-1][0], f'(${weeks[-1][1]})')
