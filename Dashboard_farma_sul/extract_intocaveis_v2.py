"""
Extrai dados completos para DN_INTOC_GRUPOS:
- 30 grupos (21 DIRETO + 7 OL + GAM + GAUCHA FARMA)
- fytd25, fytd26, janabr25, janabr26, meses (Jul/25-Abr/26)
"""
import pandas as pd, json, numpy as np

EXP_PATH = r'_Recursos\Giovano SCJ\Expandindo Distribuição Farma - Abril (FY26)\Expandindo Distribuição Farma - Abril (FY26).xlsx'
GAM_HIST  = r'_Recursos\Giovano SCJ\gam\vendas gam ano\RELATÓRIO GIOVANO 2024x2025.xlsx'
GAM_2026  = r'_Recursos\Giovano SCJ\gam\vendas gam ano\CERAS JOHNSON jan-fev-mar-abri-2026.xlsx'
GAUCHA_P  = r'_Recursos\Giovano SCJ\GAUCHA\positivação gaucha.xlsx'

EAN_LOCAO = 7894650005712
EAN_SPRAY = 7894650009567
EAN_KIDS  = 7894650940006

DIRETO_CLIENTS = [
    'ARAUJO','DROGAL','DROGARIA CATARINENSE','DROGARIA GLOBO',
    'DROGARIA ROSARIO','DROGARIA TAMOIO','DROGARIA VENANCIO','DROGASIL',
    'DROGASMIL','DSP','EXTRAFARMA','FARMA CONDE','INDIANA','NISSEI',
    'PACHECO','PAGUE MENOS','PANVEL','PRECO POPULAR','RAIA','REDEPHARMA',
    'SAO JOAO FARMACIAS'
]
OL_CLIENTS = ['OL MG','OL NE','OL PR/SC','OL RJ','OL RS','OL SPC','OL SPI']
MESES = ['202507','202508','202509','202510','202511','202512',
         '202601','202602','202603','202604']

def safe_dn(pdvs, total):
    return round(pdvs / total * 100, 1) if total > 0 else 0.0

def to_int(v):
    try:
        return int(v) if pd.notna(v) else 0
    except:
        return 0

def mk_fytd(total, locao, spray, kids):
    a = max(locao, spray, kids); t = min(locao, spray, kids)
    return {
        'soma': {'total':total,'algum':a,'dnAlgum':safe_dn(a,total),
                 'dois':a,'dnDois':safe_dn(a,total),'todos':t,'dnTodos':safe_dn(t,total)},
        'kids200':  {'total':total,'pdvs':kids, 'dn':safe_dn(kids, total)},
        'spray170': {'total':total,'pdvs':spray,'dn':safe_dn(spray,total)},
        'locao200': {'total':total,'pdvs':locao,'dn':safe_dn(locao,total)},
    }

def mk_mes(total, locao, spray, kids):
    a = max(locao, spray, kids)
    return {
        'total': total, 'soma_dn': safe_dn(a, total),
        'kids200':  {'total':total,'pdvs':kids, 'dn':safe_dn(kids, total)},
        'spray170': {'total':total,'pdvs':spray,'dn':safe_dn(spray,total)},
        'locao200': {'total':total,'pdvs':locao,'dn':safe_dn(locao,total)},
    }

# ── BASE tab: FYTD26 + janabr26 spray170 (correct EAN) ──────────────────────
print("Reading BASE tab...")
xl = pd.ExcelFile(EXP_PATH)
df_base = pd.read_excel(EXP_PATH, sheet_name='Base', header=4)
col_locao = 'Ean 007894650005712 PDVS'
col_spray = 'Ean 007894650009567 PDVS'
col_kids  = 'Ean 007894650940006 PDVS'
for c in [col_locao, col_spray, col_kids]:
    df_base[c] = pd.to_numeric(df_base[c], errors='coerce').fillna(0)
df_base['Bandeira_up'] = df_base['Bandeira'].astype(str).str.upper().str.strip()
df_base['CNPJ_str'] = df_base['CNPJ'].astype(str).str.replace(r'\.0$','',regex=True)

df_ol_map = pd.read_excel(EXP_PATH, sheet_name='Base OL', header=None)
hr = next(i for i,r in df_ol_map.iterrows() if any('cnpj' in str(v).lower() for v in r))
df_ol_map = pd.read_excel(EXP_PATH, sheet_name='Base OL', header=hr)
ol_col   = [c for c in df_ol_map.columns if 'OL' in str(c).upper() or c=='OL'][-1]
cnpj_col = [c for c in df_ol_map.columns if 'CNPJ' in str(c).upper()][0]
df_ol_map['CNPJ_str'] = df_ol_map[cnpj_col].astype(str).str.replace(r'\.0$','',regex=True)
df_merged = df_base.merge(df_ol_map[['CNPJ_str',ol_col]], on='CNPJ_str', how='left')

base_fytd26 = {}   # group -> (total, locao, spray, kids)
for cl in DIRETO_CLIENTS:
    sub = df_base[df_base['Bandeira_up'] == cl.upper()]
    t = len(sub)
    base_fytd26[cl] = (t,
        int((sub[col_locao]>0).sum()), int((sub[col_spray]>0).sum()),
        int((sub[col_kids]>0).sum()))

for ol in OL_CLIENTS:
    sub = df_merged[df_merged[ol_col].astype(str).str.upper().str.strip()==ol.upper()]
    if len(sub)==0:
        sub = df_merged[df_merged[ol_col].astype(str).str.upper().str.contains(
            ol.replace('OL ','').upper(), na=False)]
    t = len(sub)
    base_fytd26[ol] = (t,
        int((sub[col_locao]>0).sum()), int((sub[col_spray]>0).sum()),
        int((sub[col_kids]>0).sum()))

# ── DIRETO/OL sheets: FY25 annual + monthly FY25 Apr + monthly FY26 ──────────
print("Reading DIRETO/OL sheets...")
df_d  = xl.parse('DIRETO', header=None)
df_ol_sh = xl.parse('OL', header=None)

# Col offsets: Jul=8..A=11, Aug=12..A=15 ... Jan=32..A=35, Feb=36, Mar=40, Apr=44..A=47
MONTHLY_COLS = {
    '202507':(8,11),'202508':(12,15),'202509':(16,19),'202510':(20,23),
    '202511':(24,27),'202512':(28,31),'202601':(32,35),'202602':(36,39),
    '202603':(40,43),'202604':(44,47)
}
# FY25 monthly (same col layout, rows 6-26 DIRETO, rows 5-11 OL)
# FY25 Apr = col 44 (D), 47 (A)
# FY26 monthly rows 109-129 DIRETO, 53-59 OL

def parse_row(sheet, row_idx, col_d, col_a, univ_col=2):
    row = sheet.iloc[row_idx]
    univ = to_int(row.iloc[univ_col])
    d = to_int(row.iloc[col_d])
    a = to_int(row.iloc[col_a])
    return univ, d, a

groups = {}

for i, cl in enumerate(DIRETO_CLIENTS):
    # FY25 annual (col 3=D, 6=A)
    univ25, d25_ann, a25_ann = parse_row(df_d, 6+i, 3, 6)
    fytd25 = mk_fytd(univ25, d25_ann, a25_ann, d25_ann)

    # FY26 from BASE (correct spray)
    t26, l26, s26, k26 = base_fytd26[cl]
    fytd26 = mk_fytd(t26, l26, s26, k26)

    # janabr25 = FY25 April cumulative (col 44=D, 47=A)
    _, d25_apr, a25_apr = parse_row(df_d, 6+i, 44, 47)
    janabr25 = mk_fytd(univ25, d25_apr, a25_apr, d25_apr)

    # janabr26 = FY26 April (col 44=D), spray from BASE
    _, d26_apr, _ = parse_row(df_d, 109+i, 44, 47)
    univ26 = t26 if t26>0 else univ25
    janabr26 = mk_fytd(univ26, d26_apr, s26, d26_apr)  # s26 = BASE spray FYTD26

    # Monthly (FY26 rows 109-129)
    meses = {}
    for mes, (cd, ca) in MONTHLY_COLS.items():
        u, d, a = parse_row(df_d, 109+i, cd, ca)
        total = t26 if t26>0 else u
        meses[mes] = mk_mes(total, d, a, d)

    groups[cl] = {'fytd25':fytd25,'fytd26':fytd26,'janabr25':janabr25,'janabr26':janabr26,'meses':meses}

for i, ol in enumerate(OL_CLIENTS):
    univ25, d25_ann, a25_ann = parse_row(df_ol_sh, 5+i, 3, 6)
    fytd25 = mk_fytd(univ25, d25_ann, a25_ann, d25_ann)

    t26, l26, s26, k26 = base_fytd26[ol]
    fytd26 = mk_fytd(t26, l26, s26, k26)

    _, d25_apr, a25_apr = parse_row(df_ol_sh, 5+i, 44, 47)
    janabr25 = mk_fytd(univ25, d25_apr, a25_apr, d25_apr)

    _, d26_apr, _ = parse_row(df_ol_sh, 53+i, 44, 47)
    univ26 = t26 if t26>0 else univ25
    janabr26 = mk_fytd(univ26, d26_apr, s26, d26_apr)

    meses = {}
    for mes, (cd, ca) in MONTHLY_COLS.items():
        u, d, a = parse_row(df_ol_sh, 53+i, cd, ca)
        total = t26 if t26>0 else u
        meses[mes] = mk_mes(total, d, a, d)

    groups[ol] = {'fytd25':fytd25,'fytd26':fytd26,'janabr25':janabr25,'janabr26':janabr26,'meses':meses}

# ── GAM ───────────────────────────────────────────────────────────────────────
print("Processing GAM...")
df_hist = pd.read_excel(GAM_HIST)
df_2026 = pd.read_excel(GAM_2026)

def clean_ean(v):
    try: return int(round(float(v)))
    except: return None

def gam_stats(dfs, ean_col='CD EAN MERCADORIA', cnpj_col='CNPJ CLIENTE'):
    df = pd.concat(dfs, ignore_index=True)
    df['EAN_int'] = df[ean_col].apply(clean_ean)
    df['CNPJ_s'] = df[cnpj_col].astype(str).str.replace(r'\.0$','',regex=True)
    total = len(df['CNPJ_s'].unique())
    def pdvs(ean):
        m = (df['EAN_int']==ean) & (df.get('QUANTIDADES TOTAIS', pd.Series(1,index=df.index))>0)
        return len(df.loc[m,'CNPJ_s'].unique())
    return total, pdvs(EAN_LOCAO), pdvs(EAN_SPRAY), pdvs(EAN_KIDS)

MES_PERIOD = {
    (2025,'jul'):'202507',(2025,'ago'):'202508',(2025,'set'):'202509',
    (2025,'out'):'202510',(2025,'nov'):'202511',(2025,'dez'):'202512',
    (2026,'jan'):'202601',(2026,'fev'):'202602',(2026,'mar'):'202603',
    (2026,'abr'):'202604'
}

gam_fytd25 = gam_stats([
    df_hist[(df_hist['ANO']==2024)&(df_hist['MES'].isin(['jul','ago','set','out','nov','dez']))],
    df_hist[(df_hist['ANO']==2025)&(df_hist['MES'].isin(['jan','fev','mar','abr','mai','jun']))]
])
gam_fytd26 = gam_stats([
    df_hist[(df_hist['ANO']==2025)&(df_hist['MES'].isin(['jul','ago','set','out','nov','dez']))],
    df_2026[(df_2026['ANO']==2026)&(df_2026['MES'].isin(['jan','fev','mar','abr']))]
])
gam_janabr25 = gam_stats([df_hist[(df_hist['ANO']==2025)&(df_hist['MES'].isin(['jan','fev','mar','abr']))]])
gam_janabr26 = gam_stats([df_2026[(df_2026['ANO']==2026)&(df_2026['MES'].isin(['jan','fev','mar','abr']))]])

gam_monthly = {}
for (yr,mes),period in MES_PERIOD.items():
    src = df_2026 if yr==2026 else df_hist
    gam_monthly[period] = gam_stats([src[(src['ANO']==yr)&(src['MES']==mes)]])

groups['GAM'] = {
    'fytd25': mk_fytd(*gam_fytd25), 'fytd26': mk_fytd(*gam_fytd26),
    'janabr25': mk_fytd(*gam_janabr25), 'janabr26': mk_fytd(*gam_janabr26),
    'meses': {m: mk_mes(*v) for m,v in gam_monthly.items()}
}
print(f"  GAM janabr25: {safe_dn(gam_janabr25[2],gam_janabr25[0])}% spray | janabr26: {safe_dn(gam_janabr26[2],gam_janabr26[0])}%")

# ── GAUCHA FARMA ──────────────────────────────────────────────────────────────
print("Processing Gaúcha Farma...")
df_g = pd.read_excel(GAUCHA_P, header=None)
R_TOT=2; R_SPR=3; R_KID=14; R_LOC=15

def gcol(idx): return 9 + idx*3
def gval(r,i):
    try:
        v = df_g.iloc[r, gcol(i)]
        return int(v) if pd.notna(v) else 0
    except: return 0

def gaucha_agg(idx_list):
    total = max([gval(R_TOT,i) for i in idx_list],default=0)
    locao = max([gval(R_LOC,i) for i in idx_list],default=0)
    spray = max([gval(R_SPR,i) for i in idx_list],default=0)
    kids  = max([gval(R_KID,i) for i in idx_list],default=0)
    return total, locao, spray, kids

G_IDX = {
    '202507':14,'202508':15,'202509':16,'202510':17,'202511':18,'202512':19,
    '202601':20,'202602':21,'202603':22,'202604':23
}

gaucha_fytd25 = gaucha_agg(range(2,14))
gaucha_fytd26 = gaucha_agg(range(14,24))
gaucha_janabr25 = gaucha_agg(range(8,12))   # 2025/JAN-ABR
gaucha_janabr26 = gaucha_agg(range(20,24))  # 2026/JAN-ABR

groups['GAUCHA FARMA'] = {
    'fytd25': mk_fytd(*gaucha_fytd25), 'fytd26': mk_fytd(*gaucha_fytd26),
    'janabr25': mk_fytd(*gaucha_janabr25), 'janabr26': mk_fytd(*gaucha_janabr26),
    'meses': {m: mk_mes(gval(R_TOT,i), gval(R_LOC,i), gval(R_SPR,i), gval(R_KID,i))
              for m,i in G_IDX.items()}
}
print(f"  Gaúcha janabr25: {safe_dn(gaucha_janabr25[2],gaucha_janabr25[0])}% spray | janabr26: {safe_dn(gaucha_janabr26[2],gaucha_janabr26[0])}%")

# ── Serialize ─────────────────────────────────────────────────────────────────
print("\nSerializing...")
def serialize(obj, ind=0):
    p0 = '  '*ind; p1 = '  '*(ind+1)
    if isinstance(obj, dict):
        items = [f'{p1}{json.dumps(k)}: {serialize(v, ind+1).lstrip()}' for k,v in obj.items()]
        return '{\n' + ',\n'.join(items) + '\n' + p0 + '}'
    elif isinstance(obj, float):
        return f'{obj}'
    elif isinstance(obj, int):
        return str(obj)
    else:
        return json.dumps(obj)

lines = ['const DN_INTOC_GRUPOS = {']
lines.append(',\n'.join(f'  {json.dumps(g)}: {serialize(d, 1)}' for g,d in groups.items()))
lines.append('};')
js_block = '\n'.join(lines)

with open('_temp_intoc_grupos_v2.js', 'w', encoding='utf-8') as f:
    f.write(js_block)

print(f"Written: {len(js_block):,} chars, {len(groups)} groups")
print("Keys sample (ARAUJO):", list(groups['ARAUJO'].keys()))
