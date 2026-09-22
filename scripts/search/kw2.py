import re,sys,glob
pat=sys.argv[2]; w=int(sys.argv[3]); n=int(sys.argv[4])
for f in sorted(glob.glob('data/raw/sec_10k/'+sys.argv[1]+'*')):
    t=open(f,errors='ignore').read()
    print('==',f)
    seen=set()
    for m in re.finditer(pat,t,re.I):
        s=t[max(0,m.start()-w):m.end()+w]
        k=t[m.start():m.end()+80]
        if k in seen: continue
        seen.add(k); print('  >',s)
        if len(seen)>=n:break
