"""DN Abril/26 (vendeu OU tem estoque) — São João, Nissei, Clamed, Panvel"""
import pandas as pd
import os, csv

G = os.path.join('_Recursos', 'Giovano SCJ')
EAN_LOCAO = 7894650005712  # dashboard locao200
EAN_SPRAY = 7894650009567  # dashboard spray170
EAN_KIDS  = 7894650940006  # dashboard kids200
EANS = [(EAN_SPRAY,'spray170'),(EAN_LOCAO,'locao200'),(EAN_KIDS,'kids200')]

def norm(v):
    try: return int(round(float(str(v).strip())))
    except: return None

def show(label, univ, sold, stock):
    print(f'--- {label} (universo={univ}) ---')
    for ean, name in EANS:
        s = sold.get(ean,set()); e = stock.get(ean,set()); u = s|e
        print(f'  {name:9} ({ean}): vendeu={len(s):4} estoque={len(e):4} OU={len(u):4} -> DN={len(u)/univ*100:.1f}%')
    print()

# ════════ SÃO JOÃO ════════
sj = os.path.join(G,'são joao')
dv = pd.read_excel(os.path.join(sj,'vendas ceras abril fechado.xlsx'), sheet_name='Sheet1', header=0)
dv = dv[dv['Cod Barras']!='Total'].copy(); dv['EAN']=dv['Cod Barras'].apply(norm)
dv['Qt Giro']=pd.to_numeric(dv['Qt Giro'],errors='coerce').fillna(0)
de = pd.read_excel(os.path.join(sj,'estoque ceras abril fechado.xlsx'), sheet_name='Base ', header=0)
de = de[de['Cod Ean']!='Total'].copy(); de['EAN']=de['Cod Ean'].apply(norm)
de['Estoque Qtde']=pd.to_numeric(de['Estoque Qtde'],errors='coerce').fillna(0)
univ_sj = set(dv[dv['Qt Giro']>0]['Desc_Filial'].dropna()) | set(de[de['Estoque Qtde']>0]['Desc_Filial'].dropna())
sold={}; stock={}
for ean,_ in EANS:
    sold[ean]=set(dv[(dv['EAN']==ean)&(dv['Qt Giro']>0)]['Desc_Filial'].dropna())
    stock[ean]=set(de[(de['EAN']==ean)&(de['Estoque Qtde']>0)]['Desc_Filial'].dropna())
show('SÃO JOÃO', len(univ_sj), sold, stock)

# ════════ NISSEI ════════
ni = pd.read_excel(os.path.join(G,'nissei','ESTOQUE E VENDA NISSE ABRIL.xlsx'), sheet_name='ProdutosLoja', header=1)
ecol=[c for c in ni.columns if c.strip().upper()=='EAN'][0]
fcol=[c for c in ni.columns if 'Filial' in str(c)][0]
vcol=[c for c in ni.columns if 'Vendas Abril' in str(c)][0]
scol=[c for c in ni.columns if 'Estoque loja' in str(c)][0]
ni['EAN']=ni[ecol].apply(norm)
ni[vcol]=pd.to_numeric(ni[vcol],errors='coerce').fillna(0)
ni[scol]=pd.to_numeric(ni[scol],errors='coerce').fillna(0)
univ_ni=set(ni[fcol].dropna())
sold={}; stock={}
for ean,_ in EANS:
    sold[ean]=set(ni[(ni['EAN']==ean)&(ni[vcol]>0)][fcol].dropna())
    stock[ean]=set(ni[(ni['EAN']==ean)&(ni[scol]>0)][fcol].dropna())
show('NISSEI', len(univ_ni), sold, stock)

# ════════ CLAMED ════════
cl=os.path.join(G,'clamed','053405194207_202604 ultima22')
dvc=pd.read_csv(os.path.join(cl,'Vendas_053405194207_202604.csv'),sep=';',encoding='latin-1')
dec=pd.read_csv(os.path.join(cl,'Estoque_053405194207_202604.csv'),sep=';',encoding='latin-1')
dvc['EAN']=dvc['de_codigo_barras'].apply(norm); dvc['qt_vendida']=pd.to_numeric(dvc['qt_vendida'],errors='coerce').fillna(0)
dec['EAN']=dec['de_codigo_barras'].apply(norm); dec['qt_saldo_final']=pd.to_numeric(dec['qt_saldo_final'],errors='coerce').fillna(0)
univ_cl=set(dvc[dvc['qt_vendida']>0]['cd_filial'].dropna()) | set(dec[dec['qt_saldo_final']>0]['cd_filial'].dropna())
sold={}; stock={}
for ean,_ in EANS:
    sold[ean]=set(dvc[(dvc['EAN']==ean)&(dvc['qt_vendida']>0)]['cd_filial'].dropna())
    stock[ean]=set(dec[(dec['EAN']==ean)&(dec['qt_saldo_final']>0)]['cd_filial'].dropna())
show('CLAMED', len(univ_cl), sold, stock)

# ════════ PANVEL (estoque abril por loja; vendas por loja só até mar) ════════
pe=pd.read_excel(os.path.join(G,'panvel','RelatorioEstoqueCDLoja_28-04.xlsx'), header=0)
ecol=[c for c in pe.columns if str(c).strip()=='EAN'][0]
fcol=[c for c in pe.columns if 'Filial - Codigo' in str(c)][0]
scol=[c for c in pe.columns if 'Qtd Est Loja' in str(c)][0]
pe['EAN']=pe[ecol].apply(norm); pe[scol]=pd.to_numeric(pe[scol],errors='coerce').fillna(0)
# vendas ABRIL por loja
pv=pd.read_excel(os.path.join(G,'panvel','RelatorioVendaPorLoja-202604-parte-1_20260529091111.xlsx'), header=0)
becol=[c for c in pv.columns if 'Barras' in str(c)][0]
bfcol=[c for c in pv.columns if 'Filial Loja' in str(c)][0]
bqcol=[c for c in pv.columns if 'Quantidade Vendida' in str(c)][0]
pv['EAN']=pv[becol].apply(norm); pv[bqcol]=pd.to_numeric(pv[bqcol],errors='coerce').fillna(0)
univ_pv=set(pe[pe[scol]>0][fcol].dropna()) | set(pv[pv[bqcol]>0][bfcol].dropna())
sold={}; stock={}
for ean,_ in EANS:
    stock[ean]=set(pe[(pe['EAN']==ean)&(pe[scol]>0)][fcol].dropna())
    sold[ean]=set(pv[(pv['EAN']==ean)&(pv[bqcol]>0)][bfcol].dropna())  # vendas ABR por loja
print('PANVEL: estoque=ABR por loja | vendas=ABR por loja')
show('PANVEL', len(univ_pv), sold, stock)
