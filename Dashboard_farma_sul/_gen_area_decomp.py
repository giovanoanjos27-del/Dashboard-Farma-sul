# -*- coding: utf-8 -*-
"""Gera AREA_DECOMP: por agrupamento × marca, decomposição por área.
Cada área pode somar vários mercados. Suporta 'Outros' (remanescente de um agregado).
contrib_i = B26_i/ΣT26 − B25_i/ΣT25  (soma = var total do agrupamento)."""
import pandas as pd, os, json, shutil, tempfile

src=os.path.join('_Recursos','Giovano SCJ','Base Giovano (25-05).xlsx')
tmp=os.path.join(tempfile.gettempdir(),'_bg_gen.xlsx'); shutil.copy(src,tmp)
df=pd.read_excel(tmp,sheet_name='1-Tabela-1',header=8); os.remove(tmp)
df.columns=[str(c).strip() for c in df.columns]
df['mkt']=df['Markets'].astype(str).str.strip()
df['brand']=df['BRAND'].astype(str).str.strip()
df['dt']=df['Data'].astype(str)
df['val']=pd.to_numeric(df['$'],errors='coerce').fillna(0)
g=df.groupby(['mkt','brand','dt'])['val'].sum()
gt=df.groupby(['mkt','dt'])['val'].sum()
def bv(mk,brand,dt):
    try: return float(g.loc[(mk,brand,dt)])
    except: return 0.0
def tv(mk,dt):
    try: return float(gt.loc[(mk,dt)])
    except: return 0.0

A7=['CO','Gde RJ','Gde SP','Int SP','MG+ES+Int RJ','NE','Sul']
# Cada agrupamento: lista de áreas; cada área = (label, [mercados]).
# 'rem' opcional: (label, mercado_agregado) → área "Outros" = agregado − soma das outras.
GROUPS={
 'Farma Moderno':{'areas':[(x,['Farma Moderno '+x]) for x in A7]},
 'Farma Indep':{'areas':[(x,['Farma Indep '+x]) for x in A7]},
 'Farma Total':{'areas':[(x,['Farma '+x]) for x in A7]},
 'T.BR Farma (Canais)':{'areas':[('Farma Moderno',['T.BR Farma Moderno']),('Farma Indep',['T.BR Farma Indep'])]},
 'INFC Brasil (Regiões)':{'areas':[
    ('Sul',['INFC Sul']),
    ('Sudeste',['INFC SP','INFC Gde RJ','INFC MG+ES+Int RJ']),
    ('Nordeste',['INFC NE']),
    ('Centro-Oeste',['INFC CO']),
    ('Norte',['INFC Man+Bel+Ana'])]},
 'INFC Sul':{'areas':[
    ('Porto Alegre',['INFC Porto Alegre']),('Int RS',['INFC Int RS']),
    ('SC',['INFC SC']),('Curitiba',['INFC Curitiba']),('Int PR',['INFC Int PR'])]},
 'INFC Sudeste':{'areas':[
    ('Gde SP',['INFC Gde SP']),('Int SP',['INFC Int SP']),
    ('Gde RJ',['INFC Gde RJ']),('MG+ES+Int RJ',['INFC MG+ES+Int RJ'])]},
 'INFC Nordeste':{'areas':[
    ('BA',['INFC BA']),('CE',['INFC CE']),('PE',['INFC PE']),('MA+PI',['INFC MA+PI'])],
    'rem':('Outros NE','INFC NE')},
 'INFC Centro-Oeste':{'areas':[
    ('GO',['INFC GO']),('DF',['INFC DF'])],
    'rem':('Outros CO','INFC CO')},
 'INFC MG+ES+Int RJ':{'areas':[
    ('Belo Horizonte',['INFC Belo Horizonte']),('Int MG',['INFC Int MG'])],
    'rem':('ES+Int RJ','INFC MG+ES+Int RJ')},
}
BRANDS=['EXPOSIS','OFF!','XO INSETO','SUPER REPELEX']

out={}
for grp,cfg in GROUPS.items():
    pairs=list(cfg['areas']); labels=[l for l,_ in pairs]
    # total do agrupamento por dt
    def grpT(dt):
        s=sum(tv(m,dt) for _,mks in pairs for m in mks)
        if 'rem' in cfg: s += tv(cfg['rem'][1],dt) - sum(tv(m,dt) for _,mks in pairs for m in mks)
        return s
    if 'rem' in cfg:
        labels=labels+[cfg['rem'][0]]
    T26=tv(cfg['rem'][1],'FYTD26') if 'rem' in cfg else sum(tv(m,'FYTD26') for _,mks in pairs for m in mks)
    T25=tv(cfg['rem'][1],'FYTD25') if 'rem' in cfg else sum(tv(m,'FYTD25') for _,mks in pairs for m in mks)
    out[grp]={'areas':labels}
    for brand in BRANDS:
        val26=[];var=[];contrib=[]
        for lab,mks in pairs:
            b26=sum(bv(m,brand,'FYTD26') for m in mks); b25=sum(bv(m,brand,'FYTD25') for m in mks)
            t26a=sum(tv(m,'FYTD26') for m in mks); t25a=sum(tv(m,'FYTD25') for m in mks)
            val26.append(round(b26/1e6,2))
            var.append(round((b26/t26a-b25/t25a)*100,2) if t26a and t25a else 0)
            contrib.append(round((b26/T26-b25/T25)*100,3) if T26 and T25 else 0)
        if 'rem' in cfg:
            agg=cfg['rem'][1]
            b26=bv(agg,brand,'FYTD26')-sum(bv(m,brand,'FYTD26') for _,mks in pairs for m in mks)
            b25=bv(agg,brand,'FYTD25')-sum(bv(m,brand,'FYTD25') for _,mks in pairs for m in mks)
            t26a=tv(agg,'FYTD26')-sum(tv(m,'FYTD26') for _,mks in pairs for m in mks)
            t25a=tv(agg,'FYTD25')-sum(tv(m,'FYTD25') for _,mks in pairs for m in mks)
            val26.append(round(b26/1e6,2))
            var.append(round((b26/t26a-b25/t25a)*100,2) if t26a and t25a else 0)
            contrib.append(round((b26/T26-b25/T25)*100,3) if T26 and T25 else 0)
        out[grp][brand]={'val26':val26,'var':var,'contrib':contrib}

def arr(a): return '['+','.join(str(x) for x in a)+']'
lines=[]
for grp,d in out.items():
    parts=['"areas":'+json.dumps(d['areas'],ensure_ascii=False)]
    for b in BRANDS:
        bd=d[b]; parts.append(json.dumps(b)+':{"val26":'+arr(bd['val26'])+',"var":'+arr(bd['var'])+',"contrib":'+arr(bd['contrib'])+'}')
    lines.append('  '+json.dumps(grp,ensure_ascii=False)+':{'+','.join(parts)+'}')
block='var AREA_DECOMP = {\n'+',\n'.join(lines)+'\n};'
open('_temp_area_decomp.js','w',encoding='utf-8').write(block)
print('Gerado:',len(block),'chars,',len(out),'agrupamentos')
for grp in out: print('  ',grp,'->',out[grp]['areas'])
# validar EXPOSIS Brasil Regiões
e=out['INFC Brasil (Regiões)']['EXPOSIS']
print('\nEXPOSIS INFC Brasil contrib:',dict(zip(out['INFC Brasil (Regiões)']['areas'],e['contrib'])))
