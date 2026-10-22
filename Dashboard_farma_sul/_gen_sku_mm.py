"""Gera SKU_SHR_MM: share mensal por SKU (Jan/Fev/Mar/Abr 2026) por mercado,
alinhado à ordem de SKUs de SKU_MKT_MONTHLY. Fonte: Base Giovano (25-05).xlsx."""
import pandas as pd, os, re, json

HTML='Dashboard_Farma_Sul_20260512_2220.html'
SRC=os.path.join('_Recursos','Giovano SCJ','Base Giovano (25-05).xlsx')

# 1) ler SKU_MKT_MONTHLY do HTML
html=open(HTML,encoding='utf-8').read()
m=re.search(r'var SKU_MKT_MONTHLY = (\{.*?\});', html, re.DOTALL)
SKU_MKT=json.loads(m.group(1))

# 2) ler arquivo Nielsen
df=pd.read_excel(SRC,sheet_name='1-Tabela-1',header=8)
df.columns=[str(c).strip() for c in df.columns]
df=df[df['Data'].apply(lambda x: hasattr(x,'year'))].copy()
df['ym']=pd.to_datetime(df['Data']).dt.strftime('%Y%m')
df['mkt']=df['Markets'].astype(str).str.strip()
df['prod']=df['Products'].astype(str).str.strip()
df['shr']=pd.to_numeric(df['$ Shr - Product'],errors='coerce')

MONTHS=['202601','202602','202603','202604']
# índice rápido: (mkt,prod,ym) -> shr
piv=df[df['ym'].isin(MONTHS)].pivot_table(index=['mkt','prod'],columns='ym',values='shr',aggfunc='first')

def get(mkt,prod,ym):
    try:
        v=piv.loc[(mkt,prod),ym]
        return round(float(v),2) if pd.notna(v) else 0.0
    except: return 0.0

out={}
missing=set()
for mkt,d in SKU_MKT.items():
    skus=d['skus']
    rec={'jan':[],'fev':[],'mar':[],'abr':[]}
    for sku in skus:
        s=sku.strip()
        rec['jan'].append(get(mkt,s,'202601'))
        rec['fev'].append(get(mkt,s,'202602'))
        rec['mar'].append(get(mkt,s,'202603'))
        rec['abr'].append(get(mkt,s,'202604'))
        if (mkt,s) not in piv.index: missing.add((mkt,s))
    out[mkt]=rec

# 3) serializar compacto
def arr(a): return '['+','.join(str(x) for x in a)+']'
lines=[]
for mkt,rec in out.items():
    lines.append('  %s:{"jan":%s,"fev":%s,"mar":%s,"abr":%s}'%(json.dumps(mkt),arr(rec['jan']),arr(rec['fev']),arr(rec['mar']),arr(rec['abr'])))
block='var SKU_SHR_MM = {\n'+',\n'.join(lines)+'\n};'
open('_temp_sku_mm.js','w',encoding='utf-8').write(block)
print('Gerado: %d mercados, %d chars'%(len(out),len(block)))
print('SKUs sem match na fonte:', len(missing))
for x in list(missing)[:10]: print('   ', x)
# validação T.BR Farma
t=out['T.BR Farma']
print('\nT.BR Farma SKUs:', SKU_MKT['T.BR Farma']['skus'])
print('  jan:',t['jan'])
print('  abr:',t['abr'])
