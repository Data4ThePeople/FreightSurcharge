import re,csv
import sys; from pathlib import Path; sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common import TENK, EXTRACT, EXTRACT_COLS
rows=[]
def q(fn,pat):
    t=(TENK/fn).read_text(errors='ignore')
    m=re.search(pat,t)
    assert m, (fn,pat)
    s=m.group(0); assert len(s)<=200,(fn,len(s)); assert s in t
    return s
def add(co,tk,scope,fy,fn,pat,method,fsc='',base='',pct='',inc='',exc=''):
    quote=q(fn,pat)
    if method in('stated_dollars','derived_subtraction') and pct=='': pct=round(fsc/base*100,2)
    rows.append(dict(company=co,ticker=tk,mode='LTL',scope=scope,fiscal_year=fy,fuel_surcharge_revenue_musd=fsc,base_revenue_musd=base,fuel_surcharge_pct=pct,rev_incl=inc,rev_excl=exc,method=method,source_file=fn,quote=quote))
# ODFL
O=('Old Dominion Freight Line','ODFL','Total company revenue')
add(*O,2002,'ODFL_2003-12-31.txt',r'the fuel surcharge increased to 4\.4% of revenue from 3\.1% in 2002','stated_pct',pct=3.1)
odfl={2003:(r'the fuel surcharge increased to 4\.4% of revenue from 3\.1% in 2002',4.4),
2004:(r'the fuel surcharge increased to 6\.3% of revenue from 4\.4% in 2003',6.3),
2005:(r'the fuel surcharge increased to 10\.3% of revenue from 6\.3% in 2004',10.3),
2006:(r'the fuel surcharge increased to 11\.9% of revenue from 10\.3% in 2005',11.9),
2007:(r'Fuel surcharge revenue increased to 12\.4% of revenue from 11\.9% in 2006',12.4),
2008:(r'Fuel surcharge revenue increased to 17\.2% of revenue from 12\.4% in 2007',17.2),
2009:(r'Fuel surcharge revenue decreased to 9\.6% of revenue from 17\.2% of revenue in 2008',9.6),
2010:(r'Fuel surcharge revenue increased to 12\.3% of revenue from 9\.6% in 2009',12.3),
2011:(r'Fuel surcharge revenue increased to 16\.4% of revenue from 12\.3% in 2010',16.4),
2012:(r'Fuel surcharge revenue increased to 16\.7% of revenue in 2012 from 16\.4% in 2011',16.7),
2013:(r'Fuel surcharge revenue decreased to 16\.1% of revenue in 2013 from 16\.5% in 2012',16.1),
2014:(r'Fuel surcharge revenue decreased to 15\.5% of revenue in 2014 from 16\.1% in 2013',15.5),
2015:(r'Fuel surcharge revenue decreased to 10\.4% of revenue in 2015 from 15\.5% in 2014',10.4),
2016:(r'Fuel surcharge revenue decreased to 9\.5% of revenue in 2016 from 10\.4% in 2015',9.5),
2017:(r'fuel surcharges increased to 11\.1% in 2017 from 9\.5% in 2016',11.1),
2018:(r'fuel surcharges increased to 13\.3% in 2018 from 11\.1% in 2017',13.3),
2019:(r'fuel surcharges decreased to 12\.7% in 2019 as compared to 13\.3% in 2018',12.7),
2020:(r'fuel surcharges decreased to 10\.5% in 2020 as compared to 12\.7% in 2019',10.5)}
for y,(p,v) in odfl.items(): add(*O,y,f'ODFL_{y}-12-31.txt',p,'stated_pct',pct=v)
# SAIA
S=('Saia (SCS Transportation pre-2006)','SAIA')
seg='Saia LTL subsidiary segment (excl. Jevic); FSC = operating revenue minus operating revenue excluding fuel surcharge'
add(*S,seg,2002,'SAIA_2003-12-31.txt',r'revenue of \$489\.8 million in 2002.{0,120}?excluding fuel surcharge was \$480\.3 million in 2002','derived_subtraction',fsc=round(489.8-480.3,1),base=489.8)
add(*S,seg,2003,'SAIA_2003-12-31.txt',r'revenue of \$520\.7 million in 2003.{0,120}?excluding fuel surcharge was \$502\.3 million in 2003','derived_subtraction',fsc=round(520.7-502.3,1),base=520.7)
add(*S,seg,2004,'SAIA_2004-12-31.txt',r'revenue of \$645\.4 million in 2004.{0,120}?excluding fuel surcharge was \$607\.8 million in 2004','derived_subtraction',fsc=round(645.4-607.8,1),base=645.4)
add(*S,seg,2005,'SAIA_2005-12-31.txt',r'revenue of \$754\.0 million in 2005.{0,120}?excluding fuel surcharge was \$679\.9 million in 2005','derived_subtraction',fsc=round(754.0-679.9,1),base=754.0)
sc='Saia Inc. consolidated operating revenue (continuing ops)'
add(*S,sc,2006,'SAIA_2006-12-31.txt',r'Fuel surcharge revenue, which was 11\.9 percent of total revenue in 2006','stated_pct',pct=11.9)
add(*S,sc,2010,'SAIA_2012-12-31.txt',r'Fuel surcharge revenue increased to 16\.7% of operating revenue for the year ended December 31, 2011 compared to 12\.4% for the year ended December 31, 2010','stated_pct',pct=12.4)
add(*S,sc,2011,'SAIA_2012-12-31.txt',r'Fuel surcharge revenue increased to 16\.7% of operating revenue for the year ended December 31, 2011','stated_pct',pct=16.7)
saia={2012:(r'Fuel surcharge revenue increased to 17\.3% of operating revenue for the year ended December 31, 2012',17.3),
2013:(r'Fuel surcharge revenue decreased to 16\.8% of operating revenue for the year ended December 31, 2013',16.8),
2014:(r'Fuel surcharge revenue decreased to 16\.6% of operating revenue for the year ended December 31, 2014',16.6),
2015:(r'Fuel surcharge revenue decreased to 11\.7 % of operating revenue for the year ended December 31, 2015',11.7),
2016:(r'Fuel surcharge revenue decreased to 9\.7 % of operating revenue for the year ended December 31, 2016',9.7),
2017:(r'Fuel surcharge reve ?nue increased to 11\.5 percent of operating revenue for the year ended December 31, 2017',11.5),
2018:(r'Fuel surcharge revenue increased to 13\.6 percent of operating revenue for the year ended December 31, 2018',13.6),
2019:(r'Fuel surcharge revenue decrease ?d to 13\.0 percent of operating revenue for the year ended December 31, 2019',13.0),
2020:(r'Fuel surcharge revenue decrease ?d to 11\.1 percent of operating revenue for the year ended December 31, 2020',11.1),
2021:(r'Fuel surcharge revenue increase ?d to 14\.0 percent of operating revenue for the year ended December 31, 2021',14.0),
2022:(r'Fuel surcharge revenue increased to 19\.9 percent of operating revenue in 2022',19.9),
2023:(r'Fuel surcharge revenue decreased to 16\.9 percent of operating revenue in 2023',16.9),
2024:(r'Fuel surcharge revenue decreased to 15\.0 percent of operating revenue in 2024',15.0),
2025:(r'Fuel surcharge revenue remained flat at 15\.0 percent of operating revenue in 2025',15.0)}
for y,(p,v) in saia.items(): add(*S,sc,y,f'SAIA_{y}-12-31.txt',p,'stated_pct',pct=v)
# XPO
X=('XPO','XPO','North American LTL segment')
xpo=[(2019,'XPO_2021-12-31.txt',r'fuel surcharge revenue of \$433 million and \$532 million, respectively, for the years ended December 31, 2020 and 2019',532,3791),
(2020,'XPO_2021-12-31.txt',r'fuel surcharge revenue of \$632 million and \$433 million, respectively, for the years ended December 31, 2021 and 2020',433,3539),
(2021,'XPO_2021-12-31.txt',r'fuel surcharge revenue of \$632 million and \$433 million, respectively, for the years ended December 31, 2021 and 2020',632,4118),
(2022,'XPO_2022-12-31.txt',r'fuel surcharge revenue of \$1\.0 billion and \$632 million, respectively, for the years ended December 31, 2022 and 2021',1000,4645),
(2023,'XPO_2023-12-31.txt',r'fuel surcharge revenue of \$857 million and \$1\.0 billion, respectively, for the years ended December 31, 2023 and 2022',857,4671),
(2024,'XPO_2024-12-31.txt',r'fuel surcharge revenue of \$785 million and \$857 million, respectively, for the years ended December 31, 2024 and 2023',785,4899),
(2025,'XPO_2025-12-31.txt',r'fuel surcharge revenue of \$731 million and \$785 million, respectively, for the years ended December 31, 2025 and 2024',731,4832)]
for y,fn,p,f,b in xpo:
    t=(TENK/fn).read_text(errors='ignore'); assert f'{b:,}' in t,(fn,b)
    add(*X,y,fn,p,'stated_dollars',fsc=f,base=b)
cols=EXTRACT_COLS
with open(EXTRACT/'extract_LTL.csv','w',newline='') as fh:
    w=csv.DictWriter(fh,fieldnames=cols); w.writeheader(); w.writerows(rows)
from collections import Counter; print(Counter(r['ticker'] for r in rows))
for r in rows: print(r['ticker'],r['fiscal_year'],r['fuel_surcharge_pct'],r['fuel_surcharge_revenue_musd'],r['base_revenue_musd'])
