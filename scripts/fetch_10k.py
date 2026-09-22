import json,urllib.request,time,re,os,html,sys
UA={'User-Agent':'Data4ThePeople research eric@asaltollc.com'}
def get(u):
    for i in range(4):
        try:
            return urllib.request.urlopen(urllib.request.Request(u,headers=UA),timeout=60).read()
        except Exception as e: time.sleep(2)
    return b''
C={'ODFL':878927,'SAIA':1177702,'ARCB':894405,'XPO':1166003,'UNP':100885,'CSX':277948,'NSC':702165,'KNX':1492691,'WERN':793074,'JBHT':728535,'HTLD':799233,'MRTN':799167,'KNXold':1041885}
for t,c in C.items():
    s=json.loads(get(f'https://data.sec.gov/submissions/CIK{c:010d}.json'))
    blocks=[s['filings']['recent']]+[json.loads(get('https://data.sec.gov/submissions/'+f['name'])) for f in s['filings'].get('files',[])]
    for b in blocks:
        for form,acc,doc,rd in zip(b['form'],b['accessionNumber'],b['primaryDocument'],b['reportDate']):
            if form!='10-K' or not doc: continue
            out=f'tenk/{t}_{rd}.txt'
            if os.path.exists(out): continue
            raw=get(f'https://www.sec.gov/Archives/edgar/data/{c}/{acc.replace("-","")}/{doc}').decode('utf8','ignore')
            txt=re.sub(r'<[^>]+>',' ',raw); txt=html.unescape(txt); txt=re.sub(r'\s+',' ',txt)
            open(out,'w').write(txt); time.sleep(0.15)
    print(t,len([f for f in os.listdir('tenk') if f.startswith(t+'_')]),flush=True)
