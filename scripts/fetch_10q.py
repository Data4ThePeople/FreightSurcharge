"""Download 10-Q filings for 2026 as plain text (the six-month points on the rings chart).

Output: data/raw/sec_10q/<TICKER>_<period end>.txt (not in git).
"""
import json, re, html, time
from common import RAW, get
from fetch_10k import CIK

OUT = RAW / 'sec_10q'
OUT.mkdir(parents=True, exist_ok=True)
for t, c in CIK.items():
    if t in ('KNXold', 'ODFL'):   # no longer in the rings
        continue
    s = json.loads(get(f'https://data.sec.gov/submissions/CIK{c:010d}.json'))['filings']['recent']
    for form, acc, doc, rd in zip(s['form'], s['accessionNumber'], s['primaryDocument'], s['reportDate']):
        if form != '10-Q' or rd < '2026-01-01' or not doc:
            continue
        out = OUT / f'{t}_{rd}.txt'
        if not out.exists():
            raw = get(f'https://www.sec.gov/Archives/edgar/data/{c}/{acc.replace("-", "")}/{doc}').decode('utf8', 'ignore')
            out.write_text(re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', raw))))
            time.sleep(0.15)
        print(t, rd, out.stat().st_size)
