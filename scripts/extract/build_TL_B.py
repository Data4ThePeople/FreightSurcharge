import csv,re
rows=[]
def txt(f): return open('tenk/'+f).read()
def q(f,pat):
    t=txt(f); m=re.search(pat,t)
    assert m,(f,pat)
    s=m.group(0); assert len(s)<=200 and s in t; return s
def add(co,tk,mode,fy,fs,base,src,quote,method='stated_dollars',pct=''):
    rows.append(dict(company=co,ticker=tk,mode=mode,scope='consolidated',fiscal_year=fy,
      fuel_surcharge_revenue_musd=round(fs,3) if fs!='' else '',base_revenue_musd=round(base,3),
      fuel_surcharge_pct=round(100*fs/base,2) if fs!='' else pct,rev_incl=1,rev_excl=0,
      method=method,source_file='tenk/'+src,quote=quote))
# JBHT: income statement, thousands
for fy in range(2005,2026):
    f=f'JBHT_{fy}-12-31.txt'; t=txt(f)
    m=re.search(r'Fuel surcharge revenue ?s ([\d,]+) [\d,]+ [\d,]+ Total operating revenue ?s ([\d,]+)',t)
    fs=int(m.group(1).replace(',',''))/1000; base=int(m.group(2).replace(',',''))/1000
    add('J.B. Hunt Transport Services','JBHT','Intermodal/Truck mix',fy,fs,base,f,m.group(0))
    if fy==2005:
        g=re.search(r'Fuel surcharge revenues ([\d,]+) ([\d,]+) ([\d,]+) Total operating revenues ([\d,]+) ([\d,]+) ([\d,]+)',t)
        for i,y in ((2,2004),(3,2003)):
            add('J.B. Hunt Transport Services','JBHT','Intermodal/Truck mix',y,int(g.group(i).replace(',',''))/1000,int(g.group(i+3).replace(',',''))/1000,f,g.group(0))
M=('Marten Transport','MRTN','Truckload')
def mr(fy,fs,base,f,pat): add(*M,fy,fs,base,f,q(f,pat))
f='MRTN_2001-12-31.txt'
mr(1999,0.352,219.200,f,r'\$11\.6 million in 2000 and \$352,000 in 1999')
mr(2000,11.6,260.797,f,r'fuel surcharge revenue of \$10\.1 million in 2001, \$11\.6 million in 2000')
mr(2001,10.1,282.764,f,r'fuel surcharge revenue of \$10\.1 million in 2001')
mr(2002,5.5,293.096,'MRTN_2002-12-31.txt',r'fuel surcharge revenue of \$5\.5 million in 2002')
mr(2003,14.1,334.667,'MRTN_2003-12-31.txt',r'Fuel surcharge revenue was \$14\.1 million in the year ended December 31, 2003')
mr(2004,26.9,380.048,'MRTN_2004-12-31.txt',r'net of fuel surcharge revenue of \$26\.9 million in 2004')
mr(2005,57.127,460.202,'MRTN_2005-12-31.txt',r'Fuel surcharge revenue 57,127 26,920')
mr(2006,77.265,518.890,'MRTN_2006-12-31.txt',r'Fuel surcharge revenue 77,265 57,198')
mr(2007,83.786+3.314,560.017,'MRTN_2007-12-31.txt',r'Truckload fuel surcharge revenue 83,786 75,323')
mr(2008,132.6,607.099,'MRTN_2009-12-31.txt',r'fuel surcharge revenue decreasing to \$55\.7 million in 2009 from \$132\.6 million in 2008')
stated={2009:(55.7,505.874),2010:(75.9,516.920),2011:(113.0,603.679),2012:(121.1,638.456),2013:(127.7,659.214),
 2014:(125.2,672.929),2015:(72.3,664.994),2016:(53.2,671.144),2017:(67.1,698.120),2018:(106.2,787.594),2019:(103.4,843.271),
 2020:(83.8,874.374),2021:(117.7,973.644),2022:(210.4,1263.878),2023:(159.4,1131.455),2024:(123.7,963.708),2025:(104.7,883.652)}
for fy,(fs,b) in stated.items():
    f=f'MRTN_{fy}-12-31.txt'
    mr(fy,fs,b,f,r'[Ff]uel surcharge revenue[^.]{0,40}\$%s million[^.]{0,60}'%re.escape(f'{fs:.1f}'))
# verify MRTN base revenue appears in own file
for r in rows:
    t=open(r['source_file']).read()
    if r['ticker']=='MRTN': assert f"{r['base_revenue_musd']*1000:,.0f}" in t,(r['fiscal_year'])
    assert r['quote'] in t and len(r['quote'])<=200
cols='company,ticker,mode,scope,fiscal_year,fuel_surcharge_revenue_musd,base_revenue_musd,fuel_surcharge_pct,rev_incl,rev_excl,method,source_file,quote'.split(',')
rows.sort(key=lambda r:(r['ticker'],r['fiscal_year']))
with open('extract_TL_B.csv','w',newline='') as fh:
    w=csv.DictWriter(fh,cols); w.writeheader(); w.writerows(rows)
for r in rows: print(r['ticker'],r['fiscal_year'],r['fuel_surcharge_revenue_musd'],r['base_revenue_musd'],r['fuel_surcharge_pct'],r['quote'][:70])
