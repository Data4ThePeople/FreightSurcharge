"""Download every 10-K for the carriers in the study from SEC EDGAR as plain text.

Output: data/raw/sec_10k/<TICKER>_<period end>.txt (not in git). Skips files
already on disk, so re-running only adds new filings.
"""
import json, re, html, time
from common import TENK, get

CIK = {'ODFL': 878927, 'SAIA': 1177702, 'ARCB': 894405, 'XPO': 1166003, 'UNP': 100885,
       'CSX': 277948, 'NSC': 702165, 'KNX': 1492691, 'WERN': 793074, 'JBHT': 728535,
       'HTLD': 799233, 'MRTN': 799167, 'KNXold': 1041885}

def main():
  TENK.mkdir(parents=True, exist_ok=True)
  for t, c in CIK.items():
      s = json.loads(get(f'https://data.sec.gov/submissions/CIK{c:010d}.json'))
      blocks = [s['filings']['recent']] + [json.loads(get('https://data.sec.gov/submissions/' + f['name']))
                                           for f in s['filings'].get('files', [])]
      for b in blocks:
          for form, acc, doc, rd in zip(b['form'], b['accessionNumber'], b['primaryDocument'], b['reportDate']):
              if form != '10-K' or not doc:
                  continue
              out = TENK / f'{t}_{rd}.txt'
              if out.exists():
                  continue
              raw = get(f'https://www.sec.gov/Archives/edgar/data/{c}/{acc.replace("-", "")}/{doc}').decode('utf8', 'ignore')
              txt = re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', raw)))
              out.write_text(txt)
              time.sleep(0.15)
      print(t, len(list(TENK.glob(t + '_*'))), flush=True)


if __name__ == "__main__":
    main()
