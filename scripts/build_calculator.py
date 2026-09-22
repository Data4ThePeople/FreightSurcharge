"""Build dist/index.html from the template and the processed data.

Injects:  DIESEL    weekly EIA diesel, [["YYYY-MM-DD", price], ...]
          REPORTED  data/processed/reported.json
          IO        truck and rail shares by layer, from data/processed/io_shares.json
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
IO = json.dumps({k: {'truck': v['truck'], 'rail': v['rail']} for k, v in io_.items()}, separators=(',', ':'))
reported = (PROCESSED / 'reported.json').read_text()

t = (SRC / 'calculator.template.html').read_text()
for marker, value in [('/*DIESEL*/[]', diesel), ('/*REPORTED*/{}', reported), ('/*IO*/{}', IO)]:
    assert t.count(marker) == 1, marker
    t = t.replace(marker, value)
DIST.mkdir(exist_ok=True)
(DIST / 'index.html').write_text(t)
print('dist/index.html:', len(weeks), 'weeks through', weeks[-1][0], f'(${weeks[-1][1]})')
