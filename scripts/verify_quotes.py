import csv,glob,re,sys
rows=[];bad=[]
for f in sorted(glob.glob('extract_*.csv')):
    for r in csv.DictReader(open(f)):
        rows.append(r)
        t=open('tenk/'+r['source_file'].split('/')[-1]).read()
        norm=lambda s:re.sub(r'\s+',' ',s).strip()
        ok=norm(r['quote']) in t
        # number in quote check
        nums=[r['fuel_surcharge_revenue_musd'],r['fuel_surcharge_pct'],r['rev_excl']]
        if not ok: bad.append((r['ticker'],r['fiscal_year'],'QUOTE NOT FOUND',r['quote'][:90]))
print(len(rows),'rows;',len(bad),'failed')
for b in bad: print(b)
