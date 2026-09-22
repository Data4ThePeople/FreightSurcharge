"""Download weekly EIA diesel prices (from EIA directly) and three BLS freight PPIs (via FRED).

Outputs:
  data/raw/eia/diesel_weekly.csv   week,price  (U.S. No 2 diesel retail, $/gal)
  data/raw/eia/pulled.txt          UTC time of the pull
  data/raw/fred/<series>.csv       FRED CSVs, as downloaded
"""
import json, csv, datetime as dt
from common import EIA, FRED, get, keys

SERIES = 'EMD_EPD2D_PTE_NUS_DPG'
key = keys()('EIA_API_KEY')
url = ('https://api.eia.gov/v2/petroleum/pri/gnd/data/?api_key=' + key +
       '&frequency=weekly&data[0]=value&facets[series][]=' + SERIES +
       '&sort[0][column]=period&sort[0][direction]=asc&length=5000')
rows = json.loads(get(url))['response']['data']
weeks = [(r['period'], float(r['value'])) for r in rows]
assert len({w for w, _ in weeks}) == len(weeks), 'duplicate weeks from EIA'
assert all(r['series'] == SERIES for r in rows)
EIA.mkdir(parents=True, exist_ok=True)
with open(EIA / 'diesel_weekly.csv', 'w', newline='') as f:
    w = csv.writer(f); w.writerow(['week', 'price']); w.writerows(weeks)
(EIA / 'pulled.txt').write_text(dt.datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC') + '\n')
print('EIA diesel', len(weeks), 'weeks,', weeks[0][0], 'to', weeks[-1][0], weeks[-1][1])

FRED.mkdir(parents=True, exist_ok=True)
for s in ['GASDESW', 'PCU484121484121', 'PCU484122484122', 'PCU482111482111']:
    (FRED / f'{s}.csv').write_bytes(get(f'https://fred.stlouisfed.org/graph/fredgraph.csv?id={s}'))
    print('FRED', s)
