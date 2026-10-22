"""
v3 — Correções:
1. Universe = BASE tab (evita DN>100%, corrige FARMA CONDE univ=13)
2. spray170 mensal/janabr estimado por proporção (spray_fytd26 * D_mes / D_fytd26)
3. PDVs sempre <= total (cap)
4. soma adicionado ao mk_mes (KPI cards no Por Mês)
"""
import pandas as pd, json

EXP_PATH = r'_Recursos\Giovano SCJ\Expandindo Distribuição Farma - Abril (FY26)\Expandindo Distribuição Farma - Abril (FY26).xlsx'
GAM_HIST  = r'_Recursos\Giovano SCJ\gam\vendas gam ano\RELATÓRIO GIOVANO 2024x2025.xlsx'
GAM_2026  = r'_Recursos\Giovano SCJ\gam\vendas gam ano\CERAS JOHNSON jan-fev-mar-abri-2026.xlsx'
GAUCHA_P  = r'_Recursos\Giovano SCJ\GAUCHA\positivação gaucha.xlsx'

EAN_LOCAO = 7894650005712; EAN_SPRAY = 7894650009567; EAN_KIDS = 7894650940006

DIRETO_CLIENTS = [
    'ARAUJO','DROGAL','DROGARIA CATARINENSE','DROGARIA GLOBO','DROGARIA ROSARIO',
    'DROGARIA TAMOIO','DROGARIA VENANCIO','DROGASIL','DROGASMIL','DSP',
    'EXTRAFARMA','FARMA CONDE','INDIANA','NISSEI','PACHECO','PAGUE MENOS',
    'PANVEL','PRECO POPULAR','RAIA','REDEPHARMA','SAO JOAO FARMACIAS'
]
OL_CLIENTS = ['OL MG','OL NE','OL PR/SC','OL RJ','OL RS','OL SPC','OL SPI']
MESES = ['202507','202508','202509','202510','202511','202512',
         '202601','202602','202603','202604']
MONTHLY_COLS = {
    '202507':(8,11),'202508':(12,15),'202509':(16,19),'202510':(20,23),
    '202511':(24,27),'202512':(28,31),'202601':(32,35),'202602':(36,39),
    '202603':(40,43),'202604':(44,47)
}

def safe_dn(pdvs, total):
    return round(pdvs / total * 100, 1) if total > 0 else 0.0

def cap(val, total):
    return min(int(val), int(total)) if total > 0 else int(val)

def to_int(v):
    try: return int(v) if pd.notna(v) else 0
    except: return 0

def mk_soma(total, locao, spray, kids):
    a = max(locao, spray, kids); t = min(locao, spray, kids)
    return {'total':total,'algum':a,'dnAlgum':safe_dn(a,total),
            'dois':a,'dnDois':safe_dn(a,total),'todos':t,'dnTodos':safe_dn(t,total)}

def mk_period(total, locao, spray, kids):
    """Used for fytd25/fytd26/janabr25/janabr26 AND meses (soma always included)"""
    lo = cap(locao, total); sp = cap(spray, total); ki = cap(kids, total)
    return {
        'soma':    mk_soma(total, lo, sp, ki),
        'kids200': {'total':total,'pdvs':ki,'dn':safe_dn(ki,total)},
        'spray170':{'total':total,'pdvs':sp,'dn':safe_dn(sp,total)},
        'locao200':{'total':total,'pdvs':lo,'dn':safe_dn(lo,total)},
    }

def mk_mes(total, locao, spray, kids):
    """Monthly: same structure as mk_period"""
    return mk_period(total, locao, spray, kids)

def scale_spray(base_spray, base_locao, current_locao):
    """Estimate spray proportionally from base FYTD26 spray × (current_D / fytd26_D)"""
    if base_locao <= 0: return 0
    return round(base_spray * current_locao / base_locao)

# ── BASE tab: FYTD26 (correct EANs) ─────────────────────────────────────────
print("Reading BASE tab...")
xl  = pd.ExcelFile(EXP_PATH)
dfb = pd.read_excel(EXP_PATH, sheet_name='Base', header=4)
COL_L = 'Ean 007894650005712 PDVS'; COL_S = 'Ean 007894650009567 PDVS'; COL_K = 'Ean 007894650940006 PDVS'
for c in [COL_L, COL_S, COL_K]: dfb[c] = pd.to_numeric(dfb[c], errors='coerce').fillna(0)
dfb['BU'] = dfb['Bandeira'].astype(str).str.upper().str.strip()
dfb['CS'] = dfb['CNPJ'].astype(str).str.replace(r'\.0$','',regex=True)

dfom = pd.read_excel(EXP_PATH, sheet_name='Base OL', header=None)
hr  = next(i for i,r in dfom.iterrows() if any('cnpj' in str(v).lower() for v in r))
dfom = pd.read_excel(EXP_PATH, sheet_name='Base OL', header=hr)
olc  = [c for c in dfom.columns if 'OL' in str(c).upper() or c=='OL'][-1]
cjc  = [c for c in dfom.columns if 'CNPJ' in str(c).upper()][0]
dfom['CS'] = dfom[cjc].astype(str).str.replace(r'\.0$','',regex=True)
dfm = dfb.merge(dfom[['CS',olc]], on='CS', how='left')

base = {}   # group -> (total, locao, spray, kids)
for cl in DIRETO_CLIENTS:
    sub = dfb[dfb['BU']==cl.upper()]
    t = len(sub)
    base[cl] = (t, int((sub[COL_L]>0).sum()), int((sub[COL_S]>0).sum()), int((sub[COL_K]>0).sum()))

for ol in OL_CLIENTS:
    sub = dfm[dfm[olc].astype(str).str.upper().str.strip()==ol.upper()]
    if not len(sub): sub = dfm[dfm[olc].astype(str).str.upper().str.contains(ol.replace('OL ','').upper(),na=False)]
    t = len(sub)
    base[ol] = (t, int((sub[COL_L]>0).sum()), int((sub[COL_S]>0).sum()), int((sub[COL_K]>0).sum()))

# ── DIRETO/OL sheets ─────────────────────────────────────────────────────────
print("Reading DIRETO/OL sheets...")
dfd  = xl.parse('DIRETO', header=None)
dfol = xl.parse('OL',     header=None)

def cell(df, row, col):
    try:
        v = df.iloc[row, col]; return int(v) if pd.notna(v) else 0
    except: return 0

groups = {}

for i, cl in enumerate(DIRETO_CLIENTS):
    t26, l26, s26, k26 = base[cl]   # canonical BASE universe + correct EAN counts

    # FY25 annual (col 3=D, 6=A) — use BASE univ for consistency
    d25_ann = cell(dfd, 6+i, 3);  a25_ann = cell(dfd, 6+i, 6)
    fytd25 = mk_period(t26, d25_ann, a25_ann, d25_ann)

    # FY26 from BASE (100% correct)
    fytd26 = mk_period(t26, l26, s26, k26)

    # janabr25 = FY25 Apr cumul (col 44 D) — spray estimated proportionally
    d25_apr = cell(dfd, 6+i, 44)
    s25_apr = scale_spray(s26, l26, d25_apr)
    janabr25 = mk_period(t26, d25_apr, s25_apr, d25_apr)

    # janabr26 = FY26 Apr cumul (col 44 D) — spray from BASE
    d26_apr = cell(dfd, 109+i, 44)
    janabr26 = mk_period(t26, d26_apr, s26, d26_apr)

    # Monthly (FY26 rows 109+i)
    meses = {}
    for mes, (cd, ca) in MONTHLY_COLS.items():
        d_m = cell(dfd, 109+i, cd)
        s_m = scale_spray(s26, l26, d_m)
        meses[mes] = mk_mes(t26, d_m, s_m, d_m)

    groups[cl] = {'fytd25':fytd25,'fytd26':fytd26,'janabr25':janabr25,'janabr26':janabr26,'meses':meses}
    # Debug a few
    if cl in ('NISSEI','ARAUJO','SAO JOAO FARMACIAS','FARMA CONDE'):
        print(f"  {cl}: t={t26}, fytd26 spray={s26} ({safe_dn(s26,t26)}%), janabr25 spray={cap(s25_apr,t26)} ({safe_dn(cap(s25_apr,t26),t26)}%)")

for i, ol in enumerate(OL_CLIENTS):
    t26, l26, s26, k26 = base[ol]
    d25_ann = cell(dfol, 5+i, 3); a25_ann = cell(dfol, 5+i, 6)
    fytd25 = mk_period(t26, d25_ann, a25_ann, d25_ann)
    fytd26 = mk_period(t26, l26, s26, k26)
    d25_apr = cell(dfol, 5+i, 44); s25_apr = scale_spray(s26, l26, d25_apr)
    janabr25 = mk_period(t26, d25_apr, s25_apr, d25_apr)
    d26_apr = cell(dfol, 53+i, 44); janabr26 = mk_period(t26, d26_apr, s26, d26_apr)
    meses = {}
    for mes, (cd, ca) in MONTHLY_COLS.items():
        d_m = cell(dfol, 53+i, cd); s_m = scale_spray(s26, l26, d_m)
        meses[mes] = mk_mes(t26, d_m, s_m, d_m)
    groups[ol] = {'fytd25':fytd25,'fytd26':fytd26,'janabr25':janabr25,'janabr26':janabr26,'meses':meses}

# ── GAM ──────────────────────────────────────────────────────────────────────
print("GAM...")
dfh = pd.read_excel(GAM_HIST); df6 = pd.read_excel(GAM_2026)
def ce(v):
    try: return int(round(float(v)))
    except: return None
def gam_s(dfs, ec='CD EAN MERCADORIA', cc='CNPJ CLIENTE'):
    df=pd.concat(dfs,ignore_index=True); df['E']=df[ec].apply(ce)
    df['C']=df[cc].astype(str).str.replace(r'\.0$','',regex=True)
    t=len(df['C'].unique())
    def p(e): m=(df['E']==e)&(df.get('QUANTIDADES TOTAIS',pd.Series(1,index=df.index))>0); return len(df.loc[m,'C'].unique())
    return t,p(EAN_LOCAO),p(EAN_SPRAY),p(EAN_KIDS)

gf25=gam_s([dfh[(dfh['ANO']==2024)&(dfh['MES'].isin(['jul','ago','set','out','nov','dez']))],
            dfh[(dfh['ANO']==2025)&(dfh['MES'].isin(['jan','fev','mar','abr','mai','jun']))]])
gf26=gam_s([dfh[(dfh['ANO']==2025)&(dfh['MES'].isin(['jul','ago','set','out','nov','dez']))],
            df6[(df6['ANO']==2026)&(df6['MES'].isin(['jan','fev','mar','abr']))]])
gja25=gam_s([dfh[(dfh['ANO']==2025)&(dfh['MES'].isin(['jan','fev','mar','abr']))]])
gja26=gam_s([df6[(df6['ANO']==2026)&(df6['MES'].isin(['jan','fev','mar','abr']))]])
MP={(2025,'jul'):'202507',(2025,'ago'):'202508',(2025,'set'):'202509',(2025,'out'):'202510',
    (2025,'nov'):'202511',(2025,'dez'):'202512',(2026,'jan'):'202601',(2026,'fev'):'202602',
    (2026,'mar'):'202603',(2026,'abr'):'202604'}
gm={}
for (y,m),p in MP.items():
    src=df6 if y==2026 else dfh; gm[p]=gam_s([src[(src['ANO']==y)&(src['MES']==m)]])
groups['GAM']={'fytd25':mk_period(*gf25),'fytd26':mk_period(*gf26),
               'janabr25':mk_period(*gja25),'janabr26':mk_period(*gja26),
               'meses':{p:mk_mes(*v) for p,v in gm.items()}}
print(f"  GAM janabr25 spray={safe_dn(gja25[2],gja25[0])}% | janabr26 spray={safe_dn(gja26[2],gja26[0])}%")

# ── GAUCHA FARMA ─────────────────────────────────────────────────────────────
print("Gaúcha...")
dfg=pd.read_excel(GAUCHA_P,header=None)
RT=2;RS=3;RK=14;RL=15
def gc(i): return 9+i*3
def gv(r,i):
    try: v=dfg.iloc[r,gc(i)]; return int(v) if pd.notna(v) else 0
    except: return 0
def gagg(idxs):
    t=max([gv(RT,i) for i in idxs],default=0)
    return t,max([gv(RL,i) for i in idxs],default=0),max([gv(RS,i) for i in idxs],default=0),max([gv(RK,i) for i in idxs],default=0)
GI={'202507':14,'202508':15,'202509':16,'202510':17,'202511':18,'202512':19,
    '202601':20,'202602':21,'202603':22,'202604':23}
guf25=gagg(range(2,14)); guf26=gagg(range(14,24))
guja25=gagg(range(8,12)); guja26=gagg(range(20,24))
groups['GAUCHA FARMA']={
    'fytd25':mk_period(*guf25),'fytd26':mk_period(*guf26),
    'janabr25':mk_period(*guja25),'janabr26':mk_period(*guja26),
    'meses':{p:mk_mes(gv(RT,i),gv(RL,i),gv(RS,i),gv(RK,i)) for p,i in GI.items()}}
print(f"  Gaúcha janabr25 spray={safe_dn(guja25[2],guja25[0])}% | janabr26 spray={safe_dn(guja26[2],guja26[0])}%")

# ── Serialize ─────────────────────────────────────────────────────────────────
def ser(o, n=0):
    p=('  '*n); p1=('  '*(n+1))
    if isinstance(o,dict):
        items=[f'{p1}{json.dumps(k)}: {ser(v,n+1).lstrip()}' for k,v in o.items()]
        return '{\n'+',\n'.join(items)+'\n'+p+'}'
    elif isinstance(o,float): return str(o)
    elif isinstance(o,int): return str(o)
    else: return json.dumps(o)

block = 'const DN_INTOC_GRUPOS = {\n'
block += ',\n'.join(f'  {json.dumps(g)}: {ser(d,1)}' for g,d in groups.items())
block += '\n};'

with open('_temp_v3.js','w',encoding='utf-8') as f: f.write(block)
print(f"\nDone: {len(block):,} chars, {len(groups)} groups")
print("Keys:", list(next(iter(groups.values())).keys()))
