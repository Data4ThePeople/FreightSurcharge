import re,sys,glob
pat=sys.argv[2]; w=int(sys.argv[3]) if len(sys.argv)>3 else 250
for f in sorted(glob.glob('tenk/'+sys.argv[1]+'*')):
    t=open(f,errors='ignore').read()
    print('==',f)
    seen=0
    for m in re.finditer(pat,t,re.I):
        s=t[max(0,m.start()-w):m.end()+w]
        if re.search(r'\$ ?\d|\d%|\d+ percent|\(\d',s):
            print('  >',s.replace('\n',' '));seen+=1
        if seen>=int(sys.argv[4] if len(sys.argv)>4 else 4):break
