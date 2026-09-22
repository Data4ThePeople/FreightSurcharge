"""2022 and 2017 Economic Census revenue for truck transportation (NAICS 484) by industry.

Output: data/raw/census/ecn_484_<year>.json  (rows as returned by the Census API; revenue in $1,000)
"""
import json
from common import RAW, get, keys

OUT = RAW / 'census'
OUT.mkdir(parents=True, exist_ok=True)
k = keys()('CENSUS_API_KEY')
for year in (2022, 2017):
    v = f'NAICS{year}'
    rows = json.loads(get(f'https://api.census.gov/data/{year}/ecnbasic?get={v}_LABEL,RCPTOT,ESTAB&for=us:*&{v}=484*&key={k}'))
    (OUT / f'ecn_484_{year}.json').write_text(json.dumps(rows, indent=0))
    print(year, len(rows) - 1, 'rows')
