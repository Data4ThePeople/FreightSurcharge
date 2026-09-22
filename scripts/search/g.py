import re,sys,glob
pat=sys.argv[1]; files=sys.argv[2:]
for f in files:
    t=open(f).read()
    print("==",f)
    n=0
    for m in re.finditer(pat,t):
        print("  ..",t[max(0,m.start()-200):m.end()+250].replace("\n"," "))
        n+=1
        if n>=int(__import__('os').environ.get('N','4')): break
