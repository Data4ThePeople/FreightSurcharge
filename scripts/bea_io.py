import pandas as pd, numpy as np
def tr(year):
    d=pd.read_excel('CxC_TR_1997-2023_Summary.xlsx',str(year),header=None)
    codes=[str(c) for c in d.iloc[5,2:].tolist()]; rows=[str(r) for r in d.iloc[7:,0].tolist()]
    L=d.iloc[7:,2:].copy(); L.index=rows; L.columns=codes
    L=L[~L.index.duplicated()]
    L=L.loc[[c for c in codes if c in L.index], codes].apply(pd.to_numeric,errors='coerce').fillna(0)
    return L
def use(year):
    u=pd.read_excel('IOUse_After_Redefinitions_PRO_1997-2023_Summary.xlsx',str(year),header=None)
    hdr=[str(h) for h in u.iloc[5].tolist()]
    i=hdr.index('F010')
    f=u.iloc[6:,[0,1,i]].copy(); f.columns=['code','name','pce']; f['code']=f.code.astype(str)
    f['pce']=pd.to_numeric(f.pce,errors='coerce')
    return f
if __name__=='__main__':
    f=use(2023); print(f[f.code.str.match(r'^(T|V|Used|Other|482|484|42|44|4A)')].to_string())
    L=tr(2023); print(L.shape, L.index[:5].tolist(), L.columns[-5:].tolist())
