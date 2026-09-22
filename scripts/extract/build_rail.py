import csv,re
import sys; from pathlib import Path; sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common import TENK, EXTRACT, EXTRACT_COLS
U='Union Pacific';C='CSX';N='Norfolk Southern'
UQ={2006:"Includes fuel surcharge revenue of $1,619 million, $963 million, $292 million, $93 million, and $7 million for 2006, 2005, 2004, 2003, and 2002, respectively",
 2005:"In 2005, our fuel surcharge programs generated $1 billion in commodity revenue",
 2007:"Includes fuel surcharge revenue of $1,478 million, $1,619 million",
 2008:"Includes fuel surcharge revenue of $2,323 million, $1,478 million",
 2009:"Includes fuel surcharge revenue of $605 million, $2,323 million",
 2010:"Includes fuel surcharge revenue of $1,237 million, $605 million",
 2011:"Includes fuel surcharge revenue of $2,243 million, $1,237 million",
 2012:"Our fuel surcharge programs (excluding index-based contract escalators that contain some provision for fuel) generated freight revenues of $2.6 billion",
 2013:"Our fuel surcharge programs generated freight revenues of $2.6 billion, $2.6 billion, and $2.2 billion in 2013, 2012, and 2011",
 2014:"Our fuel surcharge programs generated freight revenues of $2.8 billion, $2.6 billion, and $2.6 billion in 2014, 2013, and 2012",
 2015:"Our fuel surcharge programs generated freight revenues of $ 1.3 billion, $2.8 billion, and $2.6 billion in 2015, 2014, and 2013",
 2016:"Our fuel surcharge programs generated freight revenues of $560 million",
 2017:"ncludes fuel surcharge revenue of $966 million, $560 million",
 2018:"Our fuel surcharge programs generated freight revenues of $1.7 billion, $966 million, and $560 million in 2018, 2017, and 2016",
 2019:"Our fuel surcharge programs generated freight revenues of $1.6 billion and $1.7 billion in 2019 and 2018",
 2020:"Includes fuel surcharge revenue of $967 million, $1.6 billion",
 2021:"Our fuel surcharge programs generated freight revenues of $1.7 billion and $1.0 billion in 2021 and 2020",
 2022:"Our fuel surcharge programs generated freight revenues of $3.7 billion and $1.7 billion in 2022 and 2021",
 2023:"Our fuel surcharge programs generated freight revenues of $3.0 billion and $3.7 billion in 2023 and 2022",
 2024:"Our fuel surcharge programs generated freight revenues of $2.6 billion and $3.0 billion in 2024 and 2023",
 2025:"Our fuel surcharge programs generated freight revenues of $2.3 billion and $2.6 billion in 2025 and 2024"}
ubase={2002:10663,2003:11041,2004:11692,2005:12957,2006:14862,2007:15516,2008:17118,2009:13373,2010:16069,2011:18508,2012:19686,2013:20684,2014:22560,2015:20397,2016:18601,2017:19837,2018:21384,2019:20243,2020:18251,2021:20244,2022:23159,2023:22571,2024:22811,2025:23220}
ufsr={2002:7,2003:93,2004:292,2005:1000,2006:1619,2007:1478,2008:2323,2009:605,2010:1237,2011:2243,2012:2600,2013:2600,2014:2800,2015:1300,2016:560,2017:966,2018:1700,2019:1600,2020:967,2021:1700,2022:3700,2023:3000,2024:2600,2025:2300}
rows=[]
for y in range(2002,2026):
    src=2006 if y<2005 else y
    scope='UNP freight revenues ("commodity revenue" through 2007 10-K), excl. other revenues'
    rows.append([U,'UNP','Rail',scope,y,ufsr[y],ubase[y],'',ubase[y],'','stated_dollars',f'UNP_{src}-12-31.txt',UQ[src]])
NQ={2008:"Fuel surcharge revenue amounted to $1.6 billion in 2008 (up $830 million) compared to $792 million in 2007 and $1 billion in 2006",
 2009:"Fuel surcharge revenue amounted to $370 million in 2009",
 2010:"Fuel surcharge revenue amounted to $724 million in 2010",
 2011:"Fuel surcharge revenue amounted to $1.3 billion in 2011",
 2012:"and totaled $1.3 billion in both years",
 2013:"Fuel surcharge revenue totaled $ 1,254 million in 2013",
 2014:"revenues in 2014 included $1,329 million of such surcharges",
 2016:"Revenues associated with fuel surcharges totaled $236 million, $477 million, and $1,329 million in 2016, 2015, and 2014",
 2017:"Revenues associated with fuel surcharges totaled $359 million, $236 million, and $477 million in 2017, 2016, and 2015",
 2018:"Revenues associated with fuel surcharges totaled $657 million, $359 million, and $236 million in 2018, 2017, and 2016",
 2019:"Fuel surcharge revenue (14) (30) (35)",
 2022:"Fuel surcharge revenues totaled $1.6 billion, $622 million, and $349 million in 2022, 2021, and 2020",
 2023:"Fuel surcharge revenues totaled $1.2 billion, $1.6 billion, and $622 million in 2023, 2022, and 2021",
 2024:"Fuel surcharge revenues totaled $962 million, $1.2 billion, and $1.6 billion in 2024, 2023, and 2022",
 2025:"Fuel surcharge revenues totaled $828 million, $962 million, and $1.2 billion in 2025, 2024, and 2023"}
nbase={2006:9407,2007:9432,2008:10661,2009:7969,2010:9516,2011:11172,2012:11040,2013:11245,2014:11624,2015:10511,2016:9888,2017:10551,2018:11458,2019:11296,2020:9789,2021:11142,2022:12745,2023:12156,2024:12123,2025:12180}
nfsr={2006:1000,2007:792,2008:1600,2009:370,2010:724,2011:1300,2012:1300,2013:1254,2014:1329,2015:477,2016:236,2017:359,2018:657,2019:-79,2020:349,2021:622,2022:1600,2023:1200,2024:962,2025:828}
nsrc={2006:2008,2007:2008,2015:2016,2020:2022,2021:2022}
for y in range(2006,2026):
    s=nsrc.get(y,y); m='yoy_change_only' if y==2019 else 'stated_dollars'
    scope='NSC railway operating revenues (total)'
    if y==2019: scope+='; YoY change = sum of stated segment changes Merchandise (14), Intermodal (30), Coal (35) vs 2018; no 2019 level disclosed'
    rows.append([N,'NSC','Rail',scope,y,nfsr[y],nbase[y],'',nbase[y],'',m,f'NSC_{s}-12-31.txt',NQ[s]])
rows.append([C,'CSX','Rail','CSX 2002 vs 2001 change; base not recorded (rail/other revenue split ambiguous)',2002,-25,'','','','','yoy_change_only','CSX_2003-12-26.txt',"since $25 million of fuel surcharge revenue was discontinued"])
rows.append([C,'CSX','Rail','CSX total revenue; 2015 vs 2014 decline in fuel surcharge',2015,-646,11811,'',11811,'','yoy_change_only','CSX_2015-12-25.txt',"mostly due to the decline in fuel surcharge of $646 million"])
bad=0
for r in rows:
    t=(TENK/r[11]).read_text(errors='ignore')
    if r[12] not in t: print('QUOTE MISSING',r[1],r[4]);bad+=1
    if len(r[12])>200: print('LONG',r[1],r[4])
    if r[6]!='' and f'{r[6]:,}' not in t: print('BASE MISSING',r[1],r[4],r[6]);bad+=1
with open(EXTRACT/'extract_RAIL.csv','w',newline='') as f:
    w=csv.writer(f);w.writerow(EXTRACT_COLS)
    w.writerows(rows)
print(len(rows),'rows; bad',bad)
