import re,sys,glob
tk=sys.argv[1]; extra=sys.argv[2] if len(sys.argv)>2 else None
pats=[r'fuel surcharge[^.]{0,150}\d+\.\d+ ?%', r'\d+\.\d+ ?%[^.]{0,120}fuel surcharge', r'(excluding|excludes|exclusive of|before) (the )?fuel surcharges?', r'fuel surcharge revenue[^.]{0,150}\$ ?[\d.,]+', r'\$ ?[\d.,]+ (million|billion)[^.]{0,100}fuel surcharge']
if extra: pats=[extra]
for f in sorted(glob.glob(f'tenk/{tk}*.txt')):
    t=open(f,errors='ignore').read()
    print('==',f)
    seen=set()
    for p in pats:
        for m in re.finditer(p,t,re.I):
            s=max(0,m.start()-150); 
            if any(abs(s-x)<200 for x in seen): continue
            seen.add(s)
            print('  >',t[s:m.end()+150].replace('\n',' '))
