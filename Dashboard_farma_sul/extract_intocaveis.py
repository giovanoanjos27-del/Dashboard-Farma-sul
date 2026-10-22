"""
Extrai dados para DN_INTOC_GRUPOS corrigido + GAM + Gaúcha Farma
"""
import pandas as pd
import json
import re
import numpy as np

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
    if total == 0:
        return 0.0
    return round(pdvs / total * 100, 1)

# =========================================================
# PART 1: BASE tab - FYTD26 only (all 3 correct EANs)
# =========================================================
print("Reading BASE tab...")
df_base = pd.read_excel(EXP_PATH, sheet_name='Base', header=4)
col_locao = 'Ean 007894650005712 PDVS'
col_spray = 'Ean 007894650009567 PDVS'
col_kids  = 'Ean 007894650940006 PDVS'

for c in [col_locao, col_spray, col_kids]:
    df_base[c] = pd.to_numeric(df_base[c], errors='coerce').fillna(0)

df_base['Bandeira_up'] = df_base['Bandeira'].astype(str).str.upper().str.strip()

print("Reading Base OL tab...")
df_ol_raw = pd.read_excel(EXP_PATH, sheet_name='Base OL', header=None)
# Find header row (has 'CNPJ' and 'OL' labels)
header_row = None
for i, row in df_ol_raw.iterrows():
    if any('cnpj' in str(v).lower() for v in row.values):
        header_row = i
        break

df_ol = pd.read_excel(EXP_PATH, sheet_name='Base OL', header=header_row)
print("Base OL cols:", list(df_ol.columns[:10]))
# Find OL column
ol_col = [c for c in df_ol.columns if 'OL' in str(c).upper() or c == 'OL'][-1]
cnpj_col = [c for c in df_ol.columns if 'CNPJ' in str(c).upper()][0]
print(f"OL col='{ol_col}', CNPJ col='{cnpj_col}'")

df_ol['CNPJ_str'] = df_ol[cnpj_col].astype(str).str.replace(r'\.0$','',regex=True).str.strip()
df_base['CNPJ_str'] = df_base['CNPJ'].astype(str).str.replace(r'\.0$','',regex=True).str.strip()

# Join BASE with OL mapping
df_merged = df_base.merge(df_ol[['CNPJ_str', ol_col]], on='CNPJ_str', how='left')

def extract_group_fytd26(sub):
    total = len(sub)
    if total == 0:
        return {'total':0,'locao':0,'spray':0,'kids':0}
    locao_pdvs = int((sub[col_locao] > 0).sum())
    spray_pdvs = int((sub[col_spray] > 0).sum())
    kids_pdvs  = int((sub[col_kids]  > 0).sum())
    return {'total': total, 'locao': locao_pdvs, 'spray': spray_pdvs, 'kids': kids_pdvs}

fytd26_base = {}
for cl in DIRETO_CLIENTS:
    sub = df_base[df_base['Bandeira_up'] == cl.upper()]
    fytd26_base[cl] = extract_group_fytd26(sub)
    print(f"  {cl}: univ={fytd26_base[cl]['total']}, "
          f"locao={safe_dn(fytd26_base[cl]['locao'],fytd26_base[cl]['total'])}%, "
          f"spray={safe_dn(fytd26_base[cl]['spray'],fytd26_base[cl]['total'])}%, "
          f"kids={safe_dn(fytd26_base[cl]['kids'],fytd26_base[cl]['total'])}%")

ol_vals = df_merged[ol_col].dropna().unique()
print("OL values in merged:", sorted(ol_vals))

for ol in OL_CLIENTS:
    sub = df_merged[df_merged[ol_col].astype(str).str.upper().str.strip() == ol.upper()]
    if len(sub) == 0:
        # Try partial match
        sub = df_merged[df_merged[ol_col].astype(str).str.upper().str.contains(ol.replace('OL ','').upper(), na=False)]
    fytd26_base[ol] = extract_group_fytd26(sub)
    print(f"  {ol}: univ={fytd26_base[ol]['total']}, "
          f"spray={safe_dn(fytd26_base[ol]['spray'],fytd26_base[ol]['total'])}%")

# =========================================================
# PART 2: DIRETO/OL sheets - FYTD25 and monthly
# =========================================================
print("\nReading DIRETO sheet...")
df_d = pd.read_excel(EXP_PATH, sheet_name='DIRETO', header=None)

# FY25: rows 6-26 (0-indexed), col D=3 (locao+kids), A=6 (aerossol proxy for spray)
# FY26 monthly: rows 109-129; each month: D=base_col, A=base_col+3
# Jul=col8, Aug=12, Sep=16, Oct=20, Nov=24, Dec=28, Jan=32, Feb=36, Mar=40, Apr=44
DIRETO_FY25_ROWS = list(range(6, 27))
DIRETO_FY26_ROWS = list(range(109, 130))
DIRETO_MONTHLY_COLS = {
    '202507': (8,11), '202508': (12,15), '202509': (16,19),
    '202510': (20,23), '202511': (24,27), '202512': (28,31),
    '202601': (32,35), '202602': (36,39), '202603': (40,43), '202604': (44,47)
}

def parse_direto_client_row(row, col_d, col_a, univ_col=2):
    univ_raw = row.iloc[univ_col] if univ_col < len(row) else 0
    univ = int(univ_raw) if pd.notna(univ_raw) and str(univ_raw).strip() not in ('nan','') else 0
    d_raw = row.iloc[col_d] if col_d < len(row) else 0
    a_raw = row.iloc[col_a] if col_a < len(row) else 0
    d_val = int(d_raw) if pd.notna(d_raw) and str(d_raw).strip() not in ('nan','') else 0
    a_val = int(a_raw) if pd.notna(a_raw) and str(a_raw).strip() not in ('nan','') else 0
    return univ, d_val, a_val

# FY25 DIRETO (col D=3, A=6)
direto_fy25 = {}
for i, row_idx in enumerate(DIRETO_FY25_ROWS):
    row = df_d.iloc[row_idx]
    client = DIRETO_CLIENTS[i] if i < len(DIRETO_CLIENTS) else None
    if client is None:
        break
    univ, d_val, a_val = parse_direto_client_row(row, 3, 6, 2)
    direto_fy25[client] = {'total': univ, 'locao': d_val, 'spray': a_val, 'kids': d_val}

# FY26 monthly DIRETO
direto_monthly = {cl: {} for cl in DIRETO_CLIENTS}
for mes, (col_d, col_a) in DIRETO_MONTHLY_COLS.items():
    for i, row_idx in enumerate(DIRETO_FY26_ROWS):
        if i >= len(DIRETO_CLIENTS):
            break
        client = DIRETO_CLIENTS[i]
        row = df_d.iloc[row_idx]
        univ, d_val, a_val = parse_direto_client_row(row, col_d, col_a, 2)
        # Use fytd26_base universe for monthly total
        total_base = fytd26_base[client]['total']
        if total_base == 0:
            total_base = univ
        direto_monthly[client][mes] = {
            'total': total_base,
            'locao': d_val,
            'spray': a_val,  # Note: A column = EAN 7894650130117 (aerossol proxy)
            'kids':  d_val
        }

print("\nReading OL sheet...")
df_ol_sheet = pd.read_excel(EXP_PATH, sheet_name='OL', header=None)

# OL sheet structure: FY25 rows 5-11, FY26 monthly rows 53-59
OL_FY25_ROWS = list(range(5, 12))
OL_FY26_ROWS = list(range(53, 60))
OL_MONTHLY_COLS = DIRETO_MONTHLY_COLS  # same col offsets

ol_fy25 = {}
for i, row_idx in enumerate(OL_FY25_ROWS):
    row = df_ol_sheet.iloc[row_idx]
    ol = OL_CLIENTS[i] if i < len(OL_CLIENTS) else None
    if ol is None:
        break
    univ, d_val, a_val = parse_direto_client_row(row, 3, 6, 2)
    ol_fy25[ol] = {'total': univ, 'locao': d_val, 'spray': a_val, 'kids': d_val}

ol_monthly = {ol: {} for ol in OL_CLIENTS}
for mes, (col_d, col_a) in OL_MONTHLY_COLS.items():
    for i, row_idx in enumerate(OL_FY26_ROWS):
        if i >= len(OL_CLIENTS):
            break
        ol = OL_CLIENTS[i]
        row = df_ol_sheet.iloc[row_idx]
        univ, d_val, a_val = parse_direto_client_row(row, col_d, col_a, 2)
        total_base = fytd26_base[ol]['total']
        if total_base == 0:
            total_base = univ
        ol_monthly[ol][mes] = {
            'total': total_base,
            'locao': d_val,
            'spray': a_val,
            'kids':  d_val
        }

# =========================================================
# PART 3: GAM group from sell-out files
# =========================================================
print("\nProcessing GAM data...")

def clean_ean(v):
    try:
        return int(round(float(v)))
    except:
        return None

def gam_period_stats(df_gam, ean_col='CD EAN MERCADORIA', cnpj_col='CNPJ CLIENTE'):
    df_gam = df_gam.copy()
    df_gam['EAN_int'] = df_gam[ean_col].apply(clean_ean)
    df_gam['CNPJ_str'] = df_gam[cnpj_col].astype(str).str.replace(r'\.0$','',regex=True)

    all_cnpjs = set(df_gam['CNPJ_str'].unique())
    total = len(all_cnpjs)

    def pdvs_for_ean(ean):
        mask = (df_gam['EAN_int'] == ean)
        if 'QUANTIDADES TOTAIS' in df_gam.columns:
            mask = mask & (df_gam['QUANTIDADES TOTAIS'] > 0)
        return len(set(df_gam.loc[mask, 'CNPJ_str'].unique()))

    return {
        'total': total,
        'locao': pdvs_for_ean(EAN_LOCAO),
        'spray': pdvs_for_ean(EAN_SPRAY),
        'kids':  pdvs_for_ean(EAN_KIDS)
    }

df_hist = pd.read_excel(GAM_HIST)
df_2026 = pd.read_excel(GAM_2026)

MES_MAP = {'jan':1,'fev':2,'mar':3,'abr':4,'mai':5,'jun':6,
           'jul':7,'ago':8,'set':9,'out':10,'nov':11,'dez':12}

def filter_gam(df, year=None, mes_list=None):
    mask = pd.Series([True]*len(df), index=df.index)
    if year is not None:
        mask = mask & (df['ANO'] == year)
    if mes_list is not None:
        mask = mask & (df['MES'].isin(mes_list))
    return df[mask]

# FYTD25 = Jul/24-Jun/25
fytd25_gam_parts = [
    filter_gam(df_hist, 2024, ['jul','ago','set','out','nov','dez']),
    filter_gam(df_hist, 2025, ['jan','fev','mar','abr','mai','jun'])
]
fytd25_gam_df = pd.concat(fytd25_gam_parts, ignore_index=True)
gam_fytd25 = gam_period_stats(fytd25_gam_df)

# FYTD26 = Jul/25-Apr/26
fytd26_gam_parts = [
    filter_gam(df_hist, 2025, ['jul','ago','set','out','nov','dez']),
    filter_gam(df_2026, 2026, ['jan','fev','mar','abr'])
]
fytd26_gam_df = pd.concat(fytd26_gam_parts, ignore_index=True)
gam_fytd26 = gam_period_stats(fytd26_gam_df)
print(f"GAM FYTD26: total={gam_fytd26['total']}, "
      f"locao={safe_dn(gam_fytd26['locao'],gam_fytd26['total'])}%, "
      f"spray={safe_dn(gam_fytd26['spray'],gam_fytd26['total'])}%, "
      f"kids={safe_dn(gam_fytd26['kids'],gam_fytd26['total'])}%")

# Monthly
MES_TO_PERIOD = {
    (2025,'jul'):'202507',(2025,'ago'):'202508',(2025,'set'):'202509',
    (2025,'out'):'202510',(2025,'nov'):'202511',(2025,'dez'):'202512',
    (2026,'jan'):'202601',(2026,'fev'):'202602',(2026,'mar'):'202603',
    (2026,'abr'):'202604'
}
gam_monthly = {}
for (year, mes), period in MES_TO_PERIOD.items():
    src = df_2026 if year == 2026 else df_hist
    sub = filter_gam(src, year, [mes])
    gam_monthly[period] = gam_period_stats(sub)
    print(f"  GAM {period}: total={gam_monthly[period]['total']}, "
          f"spray={safe_dn(gam_monthly[period]['spray'],gam_monthly[period]['total'])}%")

# =========================================================
# PART 4: Gaúcha Farma from positivação gaucha
# =========================================================
print("\nProcessing Gaúcha Farma data...")
df_g = pd.read_excel(GAUCHA_P, header=None)

# Month index mapping (0 = 2024/MAI)
GAUCHA_MONTHS = [
    '2024/MAI','2024/JUN','2024/JUL','2024/AGO','2024/SET','2024/OUT',
    '2024/NOV','2024/DEZ','2025/JAN','2025/FEV','2025/MAR','2025/ABR',
    '2025/MAI','2025/JUN','2025/JUL','2025/AGO','2025/SET','2025/OUT',
    '2025/NOV','2025/DEZ','2026/JAN','2026/FEV','2026/MAR','2026/ABR','2026/MAI'
]
# PDVs col for month index i = 9 + (i * 3)

GAUCHA_PERIOD_IDX = {
    '202507': 14, '202508': 15, '202509': 16, '202510': 17,
    '202511': 18, '202512': 19, '202601': 20, '202602': 21,
    '202603': 22, '202604': 23
}
FYTD25_IDX = list(range(2, 14))   # Jul/24-Jun/25 = indices 2..13
FYTD26_IDX = list(range(14, 24))  # Jul/25-Apr/26 = indices 14..23

def gaucha_pdvs_col(month_idx):
    return 9 + (month_idx * 3)

# EAN rows: spray=3, kids=14, locao=15, total=2
ROW_TOTAL = 2
ROW_SPRAY = 3
ROW_KIDS  = 14
ROW_LOCAO = 15

def get_val(row_idx, col_idx):
    try:
        v = df_g.iloc[row_idx, col_idx]
        if pd.isna(v):
            return 0
        return int(v)
    except:
        return 0

def gaucha_period(idx_list):
    # Universe = max total PDVs across period
    total_vals = [get_val(ROW_TOTAL, gaucha_pdvs_col(i)) for i in idx_list]
    total = max(total_vals) if total_vals else 0
    # PDVs = max across period for each EAN
    locao = max([get_val(ROW_LOCAO, gaucha_pdvs_col(i)) for i in idx_list]) if idx_list else 0
    spray = max([get_val(ROW_SPRAY, gaucha_pdvs_col(i)) for i in idx_list]) if idx_list else 0
    kids  = max([get_val(ROW_KIDS,  gaucha_pdvs_col(i)) for i in idx_list]) if idx_list else 0
    return {'total': total, 'locao': locao, 'spray': spray, 'kids': kids}

gaucha_fytd25 = gaucha_period(FYTD25_IDX)
gaucha_fytd26 = gaucha_period(FYTD26_IDX)
print(f"Gaúcha FYTD25: {gaucha_fytd25}")
print(f"Gaúcha FYTD26: {gaucha_fytd26}")

gaucha_monthly = {}
for period, idx in GAUCHA_PERIOD_IDX.items():
    col = gaucha_pdvs_col(idx)
    total = get_val(ROW_TOTAL, col)
    gaucha_monthly[period] = {
        'total': total,
        'locao': get_val(ROW_LOCAO, col),
        'spray': get_val(ROW_SPRAY, col),
        'kids':  get_val(ROW_KIDS, col)
    }
    print(f"  Gaúcha {period}: total={total}, "
          f"spray={safe_dn(gaucha_monthly[period]['spray'], total)}%")

# =========================================================
# PART 5: Build complete DN_INTOC_GRUPOS JS block
# =========================================================
print("\nBuilding JS block...")

def mk_fytd_obj(d25, d26):
    """Build fytd25/fytd26 entries from dicts with total/locao/spray/kids"""
    def mk_period(d):
        total = d['total']
        locao = d['locao']
        spray = d['spray']
        kids  = d['kids']
        # soma = algum (any of 3), dois (any 2), todos (all 3)
        # We approximate: algum ≈ max(locao, spray, kids), todos ≈ min(locao,spray,kids)
        # But we don't have exact combo data, so use rough approximation
        algum = max(locao, spray, kids)
        todos = min(locao, spray, kids)
        return {
            'soma': {
                'total': total, 'algum': algum,
                'dnAlgum': safe_dn(algum, total),
                'dois': algum,  # approx
                'dnDois': safe_dn(algum, total),
                'todos': todos,
                'dnTodos': safe_dn(todos, total)
            },
            'kids200':  {'total': total, 'pdvs': kids,  'dn': safe_dn(kids,  total)},
            'spray170': {'total': total, 'pdvs': spray, 'dn': safe_dn(spray, total)},
            'locao200': {'total': total, 'pdvs': locao, 'dn': safe_dn(locao, total)},
        }
    return mk_period(d25), mk_period(d26)

def mk_mes_obj(dm):
    total = dm['total']
    locao = dm['locao']
    spray = dm['spray']
    kids  = dm['kids']
    algum = max(locao, spray, kids)
    todos = min(locao, spray, kids)
    return {
        'total': total,
        'soma_dn': safe_dn(algum, total),
        'kids200':  {'total': total, 'pdvs': kids,  'dn': safe_dn(kids,  total)},
        'spray170': {'total': total, 'pdvs': spray, 'dn': safe_dn(spray, total)},
        'locao200': {'total': total, 'pdvs': locao, 'dn': safe_dn(locao, total)},
    }

groups = {}

# DIRETO groups
for cl in DIRETO_CLIENTS:
    d25 = direto_fy25.get(cl, {'total':0,'locao':0,'spray':0,'kids':0})
    d26 = fytd26_base[cl]  # From BASE tab (correct EANs for FYTD26)
    f25, f26 = mk_fytd_obj(d25, d26)
    meses = {}
    for mes in MESES:
        dm = direto_monthly[cl].get(mes, {'total': d26['total'], 'locao':0, 'spray':0, 'kids':0})
        # For FYTD26 monthly spray: override spray with 0 since A column is wrong EAN
        # Actually keep A column data as-is (it's for EAN 7894650130117 but better than 0)
        meses[mes] = mk_mes_obj(dm)
    groups[cl] = {'fytd25': f25, 'fytd26': f26, 'meses': meses}

# OL groups
for ol in OL_CLIENTS:
    d25 = ol_fy25.get(ol, {'total':0,'locao':0,'spray':0,'kids':0})
    d26 = fytd26_base[ol]  # From BASE tab
    f25, f26 = mk_fytd_obj(d25, d26)
    meses = {}
    for mes in MESES:
        dm = ol_monthly[ol].get(mes, {'total': d26['total'], 'locao':0, 'spray':0, 'kids':0})
        meses[mes] = mk_mes_obj(dm)
    groups[ol] = {'fytd25': f25, 'fytd26': f26, 'meses': meses}

# GAM group
gam_f25, gam_f26 = mk_fytd_obj(gam_fytd25, gam_fytd26)
gam_meses = {}
for mes in MESES:
    dm = gam_monthly.get(mes, {'total': gam_fytd26['total'], 'locao':0,'spray':0,'kids':0})
    gam_meses[mes] = mk_mes_obj(dm)
groups['GAM'] = {'fytd25': gam_f25, 'fytd26': gam_f26, 'meses': gam_meses}

# GAUCHA FARMA group
g_f25, g_f26 = mk_fytd_obj(gaucha_fytd25, gaucha_fytd26)
g_meses = {}
for mes in MESES:
    dm = gaucha_monthly.get(mes, {'total': gaucha_fytd26['total'], 'locao':0,'spray':0,'kids':0})
    g_meses[mes] = mk_mes_obj(dm)
groups['GAUCHA FARMA'] = {'fytd25': g_f25, 'fytd26': g_f26, 'meses': g_meses}

# =========================================================
# PART 6: Serialize to JS
# =========================================================
def obj_to_js(obj, indent=0):
    pad = '  ' * indent
    pad1 = '  ' * (indent + 1)
    if isinstance(obj, dict):
        items = []
        for k, v in obj.items():
            items.append(f'{pad1}{json.dumps(k)}: {obj_to_js(v, indent+1).lstrip()}')
        return '{\n' + ',\n'.join(items) + '\n' + pad + '}'
    elif isinstance(obj, float):
        return f'{obj}'
    elif isinstance(obj, int):
        return str(obj)
    else:
        return json.dumps(obj)

lines = ['const DN_INTOC_GRUPOS = {']
group_strs = []
for gname, gdata in groups.items():
    inner = obj_to_js(gdata, 1)
    group_strs.append(f'  {json.dumps(gname)}: {inner}')
lines.append(',\n'.join(group_strs))
lines.append('};')
js_block = '\n'.join(lines)

with open('_temp_intoc_grupos.js', 'w', encoding='utf-8') as f:
    f.write(js_block)
print(f"\nWrote JS block ({len(js_block):,} chars) to _temp_intoc_grupos.js")
print(f"Groups: {list(groups.keys())}")
