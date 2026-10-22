"""
v4 — Corrige "Por Mês" para clientes DIRETO com gaps no DIRETO sheet:
- Usa 'positivação ano 2024x2025x2026.xlsx' para contagens mensais por rede
- DIRETO sheet cobria só alguns meses (ex: SAO JOAO mostrava 0 em Jul-Nov/25)
- Spray170 mensal estimado proporcionalmente (spray_fytd26 × D_mes / D_fytd26)
- RAIA, DROGASIL, e clientes pequenos sem match: mantém DIRETO sheet
"""
import pandas as pd, json

EXP_PATH   = r'_Recursos\Giovano SCJ\Expandindo Distribuição Farma - Abril (FY26)\Expandindo Distribuição Farma - Abril (FY26).xlsx'
GAM_HIST   = r'_Recursos\Giovano SCJ\gam\vendas gam ano\RELATÓRIO GIOVANO 2024x2025.xlsx'
GAM_2026   = r'_Recursos\Giovano SCJ\gam\vendas gam ano\CERAS JOHNSON jan-fev-mar-abri-2026.xlsx'
GAUCHA_P   = r'_Recursos\Giovano SCJ\GAUCHA\positivação gaucha.xlsx'
POSITIV_P  = r'_Recursos\Giovano SCJ\positivação ano 2024x2025x2026.xlsx'

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
    lo = cap(locao, total); sp = cap(spray, total); ki = cap(kids, total)
    return {
        'soma':    mk_soma(total, lo, sp, ki),
        'kids200': {'total':total,'pdvs':ki,'dn':safe_dn(ki,total)},
        'spray170':{'total':total,'pdvs':sp,'dn':safe_dn(sp,total)},
        'locao200':{'total':total,'pdvs':lo,'dn':safe_dn(lo,total)},
    }

def mk_mes(total, locao, spray, kids):
    return mk_period(total, locao, spray, kids)

def scale_spray(base_spray, base_locao, current_locao):
    if base_locao <= 0: return 0
    return round(base_spray * current_locao / base_locao)

def cell(df, row, col):
    try:
        v = df.iloc[row, col]; return int(v) if pd.notna(v) else 0
    except: return 0

# ── BASE tab: FYTD26 ──────────────────────────────────────────────────────────
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

base = {}
for cl in DIRETO_CLIENTS:
    sub = dfb[dfb['BU']==cl.upper()]
    t = len(sub)
    base[cl] = (t, int((sub[COL_L]>0).sum()), int((sub[COL_S]>0).sum()), int((sub[COL_K]>0).sum()))

for ol in OL_CLIENTS:
    sub = dfm[dfm[olc].astype(str).str.upper().str.strip()==ol.upper()]
    if not len(sub): sub = dfm[dfm[olc].astype(str).str.upper().str.contains(ol.replace('OL ','').upper(),na=False)]
    t = len(sub)
    base[ol] = (t, int((sub[COL_L]>0).sum()), int((sub[COL_S]>0).sum()), int((sub[COL_K]>0).sum()))

# ── POSITIVAÇÃO ANUAL: monthly locao counts per DIRETO client ─────────────────
print("Reading positivação file for monthly data...")
dfp = pd.read_excel(POSITIV_P, sheet_name='QUERY', header=0)
mcols_p = [c for c in dfp.columns if 'PDVS' in str(c)]
# Map period string → column name
pcol = {m: next((c for c in mcols_p if m in c), None) for m in MESES}

def positiv_monthly(sub_df):
    """Count positivated PDVs per month for a filtered sub-DataFrame."""
    result = {}
    for m in MESES:
        col = pcol.get(m)
        result[m] = int(sub_df[col].notna().sum()) if col and len(sub_df) > 0 else 0
    return result

# Build monthly locao counts per client
# Clients with clean 1-to-1 Grupo Economico match
ECO_MAP = {
    'ARAUJO':             ('eco', 'GRUPO DROGARIA ARAUJO'),
    'DROGAL':             ('eco', 'GRUPO DROGAL'),
    'DROGARIA VENANCIO':  ('eco', 'GRUPO VENANCIO'),
    'FARMA CONDE':        ('eco', 'FARMA CONDE REDE'),
    'INDIANA':            ('eco', 'GRUPO INDIANA'),
    'NISSEI':             ('eco', 'GRUPO NISSEI SA'),
    'PAGUE MENOS':        ('eco', 'GRUPO PAGUE MENOS'),
    'PANVEL':             ('eco', 'GRUPO PANVEL'),
    'REDEPHARMA':         ('eco', 'GRUPO REDEPHARMA'),
    'SAO JOAO FARMACIAS': ('eco', 'GRUPO SAO JOAO'),
    'DROGARIA ROSARIO':   ('eco', 'FARMACIA ROSARIO'),
    # Split within GRUPO DPSP by razao social
    'DSP':     ('razao_in_eco', ('GRUPO DPSP', 'DROGARIA SAO PAULO')),
    'PACHECO': ('razao_in_eco', ('GRUPO DPSP', 'PACHECO')),
}

positiv_monthly_data = {}  # cl -> {month -> count}

for cl, (mode, key) in ECO_MAP.items():
    if mode == 'eco':
        sub = dfp[dfp['Grupo Economico'] == key]
    elif mode == 'razao_in_eco':
        eco_name, razao_kw = key
        sub = dfp[(dfp['Grupo Economico'] == eco_name) &
                  (dfp['Razao Social'].str.upper().str.contains(razao_kw, na=False))]
    positiv_monthly_data[cl] = positiv_monthly(sub)
    t = len(sub)
    sample = positiv_monthly_data[cl]
    print(f"  {cl}: n={t}, Jul={sample['202507']}, Dec={sample['202512']}, Apr={sample['202604']}")

# ── DIRETO/OL sheets ─────────────────────────────────────────────────────────
print("Reading DIRETO/OL sheets...")
dfd  = xl.parse('DIRETO', header=None)
dfol = xl.parse('OL',     header=None)

groups = {}

for i, cl in enumerate(DIRETO_CLIENTS):
    t26, l26, s26, k26 = base[cl]

    # FY25 annual (col 3=D, 6=A)
    d25_ann = cell(dfd, 6+i, 3);  a25_ann = cell(dfd, 6+i, 6)
    fytd25 = mk_period(t26, d25_ann, a25_ann, d25_ann)

    # FY26 from BASE
    fytd26 = mk_period(t26, l26, s26, k26)

    # janabr25 = FY25 Apr cumul (col 44)
    d25_apr = cell(dfd, 6+i, 44)
    s25_apr = scale_spray(s26, l26, d25_apr)
    janabr25 = mk_period(t26, d25_apr, s25_apr, d25_apr)

    # janabr26 = FY26 Apr cumul (col 44)
    d26_apr = cell(dfd, 109+i, 44)
    janabr26 = mk_period(t26, d26_apr, s26, d26_apr)

    # Monthly: use positivação if available, else DIRETO sheet
    meses = {}
    for mes, (cd, ca) in MONTHLY_COLS.items():
        if cl in positiv_monthly_data:
            d_m = positiv_monthly_data[cl][mes]
        else:
            d_m = cell(dfd, 109+i, cd)  # fallback: DIRETO sheet
        s_m = scale_spray(s26, l26, d_m)
        meses[mes] = mk_mes(t26, d_m, s_m, d_m)

    groups[cl] = {'fytd25':fytd25,'fytd26':fytd26,'janabr25':janabr25,'janabr26':janabr26,'meses':meses}

    if cl in ('NISSEI','ARAUJO','SAO JOAO FARMACIAS','FARMA CONDE','PANVEL','PAGUE MENOS'):
        src = 'POSITIV' if cl in positiv_monthly_data else 'DIRETO'
        aug = meses['202508']['locao200']['pdvs']
        dec = meses['202512']['locao200']['pdvs']
        apr = meses['202604']['locao200']['pdvs']
        print(f"  [{src}] {cl}: t={t26}, Aug={aug} ({safe_dn(aug,t26)}%), Dec={dec} ({safe_dn(dec,t26)}%), Apr={apr} ({safe_dn(apr,t26)}%)")

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
def gam_s(dfs, ec='CD EAN MERCADORIA', cc='CNPJ CLIENTE', count_rows=False):
    """count_rows=True: conta linhas por EAN (correto para CERAS JOHNSON mensal → SUM mensal)
    count_rows=False: conta CNPJs únicos por EAN (correto para RELATÓRIO GIOVANO já agregado)"""
    df=pd.concat(dfs,ignore_index=True); df['E']=df[ec].apply(ce)
    df['C']=df[cc].astype(str).str.replace(r'\.0$','',regex=True)
    t=len(df['C'].unique())
    def p(e):
        mask=(df['E']==e)
        if 'QUANTIDADES TOTAIS' in df.columns: mask=mask&(df['QUANTIDADES TOTAIS']>0)
        return int(mask.sum()) if count_rows else len(df.loc[mask,'C'].unique())
    return t,p(EAN_LOCAO),p(EAN_SPRAY),p(EAN_KIDS)

# FYTD25/26 e janabr25: usa CNPJs únicos (RELATÓRIO GIOVANO = arquivo anual já agregado)
gf25=gam_s([dfh[(dfh['ANO']==2024)&(dfh['MES'].isin(['jul','ago','set','out','nov','dez']))],
            dfh[(dfh['ANO']==2025)&(dfh['MES'].isin(['jan','fev','mar','abr','mai','jun']))]])
gf26=gam_s([dfh[(dfh['ANO']==2025)&(dfh['MES'].isin(['jul','ago','set','out','nov','dez']))],
            df6[(df6['ANO']==2026)&(df6['MES'].isin(['jan','fev','mar','abr']))]])
gja25=gam_s([dfh[(dfh['ANO']==2025)&(dfh['MES'].isin(['jan','fev','mar','abr']))]])
# janabr26: usa contagem de linhas (CERAS JOHNSON mensal — SUM compradores mensais)
gja26=gam_s([df6[(df6['ANO']==2026)&(df6['MES'].isin(['jan','fev','mar','abr']))]], count_rows=True)
print(f"  GAM janabr26: t={gja26[0]}, locao={gja26[1]} ({safe_dn(gja26[1],gja26[0])}%), spray={gja26[2]} ({safe_dn(gja26[2],gja26[0])}%), kids={gja26[3]} ({safe_dn(gja26[3],gja26[0])}%)")
MP={(2025,'jul'):'202507',(2025,'ago'):'202508',(2025,'set'):'202509',(2025,'out'):'202510',
    (2025,'nov'):'202511',(2025,'dez'):'202512',(2026,'jan'):'202601',(2026,'fev'):'202602',
    (2026,'mar'):'202603',(2026,'abr'):'202604'}
gm={}
for (y,m),p in MP.items():
    # mensal: linhas = CNPJs únicos por mês (sem diferença prática), usa count_rows=True pra consistência
    src=df6 if y==2026 else dfh
    gm[p]=gam_s([src[(src['ANO']==y)&(src['MES']==m)]], count_rows=True)
groups['GAM']={'fytd25':mk_period(*gf25),'fytd26':mk_period(*gf26),
               'janabr25':mk_period(*gja25),'janabr26':mk_period(*gja26),
               'meses':{p:mk_mes(*v) for p,v in gm.items()}}

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

# ── Override mensal com dados REAIS de vendas+estoque do segundo cérebro ───────
# Critério aprovado pelo Giovano: loja conta se VENDEU o SKU OU tem ESTOQUE>0
# Estrutura por mês: (universo, locao200_pdvs, spray170_pdvs, kids200_pdvs)
# Nota: jan/fev SJ = só vendas (não há arquivo de estoque HB desses meses)
REAL_MESES = {
    'SAO JOAO FARMACIAS': {
        '202601': (1268, 1020, 1051, 1073),  # só vendas (s/ estoque jan)
        '202602': (1268,  821,  892,  962),  # só vendas (s/ estoque fev)
        '202603': (1268,  724,  958,  791),  # vendeu OU estoque (mar)
        '202604': (1268,  503,  602,  415),  # vendeu OU estoque (abr fechado)
    },
    'NISSEI': {
        '202604': (471, 461, 380, 323),  # vendas abr + estoque loja
    },
    'PANVEL': {
        '202604': (650, 644, 643, 641),  # vendas abr + estoque abr
    },
    'DROGARIA CATARINENSE': {  # Clamed bandeira DC; abr=vendeu OU estoque, demais=sell-out
        '202509': (76, 33, 36, 46), '202510': (76, 44, 40, 58),
        '202511': (76, 55, 51, 60), '202512': (76, 68, 66, 72),
        '202601': (76, 70, 70, 75), '202602': (76, 68, 68, 73),
        '202603': (76, 63, 66, 70), '202604': (76, 76, 73, 76),
    },
    'PRECO POPULAR': {  # Clamed bandeira PP; abr=vendeu OU estoque, demais=sell-out
        '202509': (578, 220, 311, 301), '202510': (578, 455, 264, 348),
        '202511': (578, 343, 416, 454), '202512': (578, 483, 543, 543),
        '202601': (578, 491, 460, 537), '202602': (578, 475, 518, 529),
        '202603': (578, 445, 466, 502), '202604': (578, 571, 550, 568),
    },
}
for cl, meses_real in REAL_MESES.items():
    if cl not in groups: continue
    for mes, (t, lo, sp, ki) in meses_real.items():
        groups[cl]['meses'][mes] = mk_mes(t, lo, sp, ki)
        print(f"  [REAL] {cl} {mes}: univ={t}, spray={safe_dn(sp,t)}%, locao={safe_dn(lo,t)}%, kids={safe_dn(ki,t)}%")

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

with open('_temp_v4.js','w',encoding='utf-8') as f: f.write(block)
print(f"\nDone: {len(block):,} chars, {len(groups)} groups")

# Validation
import re
vals = re.findall(r'"dn":\s*([\d.]+)', block)
over100 = [v for v in vals if float(v) > 100]
print(f"DN values: {len(vals)} total, {len(over100)} over 100%")
print("Keys:", list(next(iter(groups.values())).keys()))
