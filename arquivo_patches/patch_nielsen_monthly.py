#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
patch_nielsen_monthly.py
Atualiza NIELSEN_BRAND_VAL no Dashboard HTML com dados mensais Jan/Fev/Mar
de 2025 e 2026 vindos do Excel NielsenIQ "Base Giovano 26-04.xlsx"
"""

import re
import sys
import pandas as pd
from datetime import datetime
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

# ─── CAMINHOS ────────────────────────────────────────────────────────────────
BASE_DIR   = Path(r'C:\Users\valqu\OneDrive\Documentos\Claude\Projects\projeto Dashboard_farma_sul\Dashboard_farma_sul')
EXCEL_PATH = BASE_DIR / r'_Recursos\Giovano SCJ\Base Giovano 26-04.xlsx'
HTML_PATH  = BASE_DIR / 'Dashboard_Farma_Sul_20260512_2220.html'
VERSOES    = BASE_DIR / 'versoes'
VERSOES.mkdir(exist_ok=True)

TS = datetime.now().strftime('%Y%m%d_%H%M')
BACKUP_PATH = VERSOES / f'Dashboard_Farma_Sul_{TS}_NielsenMonthlyFix.html'

BRANDS = ['OFF!', 'EXPOSIS', 'XO INSETO', 'SUPER REPELEX', 'SBP']

# ─── 1. LER EXCEL ────────────────────────────────────────────────────────────
print('=' * 60)
print('1. Lendo Excel: 1-Tabela-1')
df = pd.read_excel(EXCEL_PATH, sheet_name='1-Tabela-1', header=8)
print(f'   Shape: {df.shape}')

# Filtrar apenas linhas de brand-level (Products = NaN, BRAND válida)
df_brand = df[
    df['Products'].isna() &
    df['BRAND'].isin(BRANDS) &
    df['markets'].notna() &
    ~df['markets'].str.startswith('Dataset', na=True) &
    ~df['markets'].str.startswith('Direitos', na=True) &
    ~df['markets'].str.startswith('Exportado', na=True) &
    ~df['markets'].str.startswith('Terms', na=True)
].copy()

print(f'   Linhas brand-level: {len(df_brand)}')

# ─── 2. CONSTRUIR DICIONÁRIO DE DADOS ────────────────────────────────────────
print('\n2. Construindo dicionário de dados...')

def parse_period(val):
    """Retorna tuple para identificar o período."""
    if isinstance(val, str):
        if 'FYTD25' in str(val):
            return ('FYTD', '25')
        if 'FYTD26' in str(val):
            return ('FYTD', '26')
        return None
    if isinstance(val, datetime):
        return (val.year, val.month)
    # pandas Timestamp
    try:
        return (val.year, val.month)
    except Exception:
        return None

TARGET_PERIODS = {
    (2025, 1): 'jan25',
    (2025, 2): 'fev25',
    (2025, 3): 'mar25',
    (2026, 1): 'jan26',
    (2026, 2): 'fev26',
    (2026, 3): 'mar26',
    ('FYTD', '25'): 'fytd25',
    ('FYTD', '26'): 'fytd26',
}

data = {}  # data[market][brand][field] = value

for _, row in df_brand.iterrows():
    market = str(row['markets']).strip()
    brand  = str(row['BRAND']).strip()
    period_raw = row['Data']
    period_key = parse_period(period_raw)

    if period_key not in TARGET_PERIODS:
        continue

    label = TARGET_PERIODS[period_key]

    val_dol = row['$']
    val_un  = row['(UNID)']
    val_shr = row['$ Shr - Product']

    # Converter $ para R$ MM (÷ 1.000.000 — Excel está em R$ bruto)
    try:
        val_mm = round(float(val_dol) / 1_000_000, 4) if pd.notna(val_dol) else None
    except Exception:
        val_mm = None

    # Converter UNID para milhares (÷ 1000 — Excel está em unidades brutas)
    try:
        un_val = round(float(val_un) / 1000, 4) if pd.notna(val_un) else None
    except Exception:
        un_val = None

    if market not in data:
        data[market] = {}
    if brand not in data[market]:
        data[market][brand] = {}

    b = data[market][brand]

    if label == 'jan26':
        b['jan_val'] = val_mm
        b['jan_un']  = un_val
    elif label == 'fev26':
        b['fev_val'] = val_mm
        b['fev_un']  = un_val
    elif label == 'mar26':
        b['mar_val'] = val_mm
        b['mar_un']  = un_val
    elif label == 'jan25':
        b['jan25_val'] = val_mm
        b['jan25_un']  = un_val
    elif label == 'fev25':
        b['fev25_val'] = val_mm
        b['fev25_un']  = un_val
    elif label == 'mar25':
        b['mar25_val'] = val_mm
        b['mar25_un']  = un_val
    elif label == 'fytd25':
        b['fytd25_val'] = val_mm
        b['fytd25_un']  = un_val
    elif label == 'fytd26':
        b['fytd26_val'] = val_mm
        b['fytd26_un']  = un_val

print(f'   Mercados com dados: {len(data)}')

# SANIDADE
if 'Farma MG+ES+Int RJ' in data and 'OFF!' in data['Farma MG+ES+Int RJ']:
    val = data['Farma MG+ES+Int RJ']['OFF!'].get('jan25_val')
    print(f'\n   SANIDADE: Farma MG+ES+Int RJ > OFF! jan25_val = {val}')
    print(f'   (esperado ~3.7778 R$ MM)')

# ─── 3. LER HTML ─────────────────────────────────────────────────────────────
print('\n3. Lendo HTML...')
with open(HTML_PATH, 'r', encoding='utf-8') as f:
    content = f.read()
print(f'   HTML size: {len(content):,} chars')

# ─── 4. LOCALIZAR O BLOCO NIELSEN_BRAND_VAL ──────────────────────────────────
idx_start = content.find('const NIELSEN_BRAND_VAL =')
if idx_start == -1:
    raise ValueError('NIELSEN_BRAND_VAL não encontrado no HTML!')

# Encontrar fim do bloco
depth = 0
pos = idx_start + len('const NIELSEN_BRAND_VAL =')
idx_end = pos
for i in range(pos, min(pos + 2000000, len(content))):
    if content[i] == '{':
        depth += 1
    elif content[i] == '}':
        depth -= 1
        if depth == 0:
            idx_end = i + 1
            break

block = content[idx_start:idx_end]
print(f'   NIELSEN_BRAND_VAL block: {len(block):,} chars')

# ─── 5. PATCH ────────────────────────────────────────────────────────────────
print('\n4. Aplicando patches...')

FIELDS_TO_UPDATE = [
    'jan_val', 'fev_val', 'mar_val',
    'jan_un',  'fev_un',  'mar_un',
    'jan25_val', 'fev25_val', 'mar25_val',
    'jan25_un',  'fev25_un',  'mar25_un',
    'fytd25_val', 'fytd26_val',
    'fytd25_un',  'fytd26_un',
]

markets_updated  = []
markets_notfound = []

# Extrair mercados do HTML
html_market_names = re.findall(r"^\s+'([^']+)':\s*\{", block, re.MULTILINE)
html_market_names = [m for m in html_market_names if m not in BRANDS]
html_market_names = list(dict.fromkeys(html_market_names))
print(f'   Mercados no dashboard: {len(html_market_names)}')

def update_block_fields(brand_content, fields_dict):
    """Atualiza campos numéricos em uma string de conteúdo JS."""
    result = brand_content
    for field in FIELDS_TO_UPDATE:
        if field not in fields_dict or fields_dict[field] is None:
            continue
        new_val = fields_dict[field]
        # Pattern: campo:número (int ou float, possivelmente negativo)
        fp = re.compile(r'(?<![a-zA-Z_])' + re.escape(field) + r':(-?\d+(?:\.\d+)?)')
        if fp.search(result):
            result = fp.sub(lambda m, f=field, v=new_val: f'{f}:{v}', result)
    return result

def patch_market_in_block(block_str, market, brands_data):
    """
    Encontra o bloco do mercado e substitui os campos de cada brand.
    Retorna (new_block_str, list_of_updated_brands).
    """
    mkt_esc = re.escape(market)
    # Encontrar início do mercado
    mkt_pat = re.compile(rf"'{mkt_esc}':\s*\{{")
    mkt_m = mkt_pat.search(block_str)
    if not mkt_m:
        return block_str, []

    mkt_start = mkt_m.start()

    # Encontrar fim do bloco do mercado (contar chaves desde o { que abre)
    open_brace_pos = mkt_m.end() - 1  # posição do '{'
    depth = 0
    mkt_end = open_brace_pos
    for i in range(open_brace_pos, len(block_str)):
        if block_str[i] == '{':
            depth += 1
        elif block_str[i] == '}':
            depth -= 1
            if depth == 0:
                mkt_end = i + 1
                break

    mkt_block = block_str[mkt_start:mkt_end]
    original_mkt_block = mkt_block

    updated_brands = []

    for brand, fields in brands_data.items():
        if not fields:
            continue

        brand_esc = re.escape(brand)
        # Encontrar o conteúdo do brand: 'BRAND':{...}
        # O conteúdo pode ter arrays [...] mas não objetos aninhados
        bp = re.compile(rf"'{brand_esc}':\s*\{{([^{{}}]*)\}}")
        bm = bp.search(mkt_block)
        if not bm:
            continue

        original_content = bm.group(1)
        new_content = update_block_fields(original_content, fields)

        if new_content != original_content:
            # Fazer a substituição usando os índices do match
            start, end = bm.span(1)  # span do grupo 1 (o conteúdo dentro de {})
            mkt_block = mkt_block[:start] + new_content + mkt_block[end:]
            updated_brands.append(brand)

    if mkt_block != original_mkt_block:
        new_block_str = block_str[:mkt_start] + mkt_block + block_str[mkt_end:]
        return new_block_str, updated_brands
    else:
        return block_str, []

# Aplicar patches para cada mercado
for market_excel in sorted(data.keys()):
    # Match exato ou com strip
    market_html = None
    if market_excel in html_market_names:
        market_html = market_excel
    else:
        for hm in html_market_names:
            if hm.strip() == market_excel.strip():
                market_html = hm
                break

    if market_html is None:
        markets_notfound.append(market_excel)
        continue

    block, brands_updated = patch_market_in_block(block, market_html, data[market_excel])

    if brands_updated:
        off_jan25 = data[market_excel].get('OFF!', {}).get('jan25_val')
        off_jan26 = data[market_excel].get('OFF!', {}).get('jan_val')
        markets_updated.append((market_html, brands_updated, off_jan25, off_jan26))
        print(f'   OK: {market_html} -> {brands_updated}')
    else:
        # Market found but no changes — check why
        pass

# ─── 6. MONTAR NOVO CONTEÚDO ─────────────────────────────────────────────────
print('\n5. Montando novo HTML...')
new_content = content[:idx_start] + block + content[idx_end:]
print(f'   HTML original: {len(content):,} chars')
print(f'   HTML novo: {len(new_content):,} chars')
print(f'   Diferença: {len(new_content) - len(content):+,} chars')

# ─── 7. SALVAR ───────────────────────────────────────────────────────────────
print('\n6. Salvando arquivos...')

with open(BACKUP_PATH, 'w', encoding='utf-8') as f:
    f.write(new_content)
print(f'   Backup: {BACKUP_PATH}')

with open(HTML_PATH, 'w', encoding='utf-8') as f:
    f.write(new_content)
print(f'   Principal: {HTML_PATH}')

# ─── 8. RELATÓRIO ────────────────────────────────────────────────────────────
print('\n' + '=' * 60)
print('RELATÓRIO FINAL')
print('=' * 60)
print(f'  Mercados atualizados: {len(markets_updated)}')
print(f'  Mercados Excel nao encontrados no HTML: {len(markets_notfound)}')

print('\n---- Mercados Atualizados ----')
for mkt, brands_list, off_jan25, off_jan26 in markets_updated:
    print(f'  OK {mkt}')
    print(f'     Brands: {brands_list}')
    if off_jan25 is not None:
        print(f'     OFF! jan25_val: {off_jan25}  |  jan26_val: {off_jan26}')

if markets_notfound:
    print('\n---- Mercados NO Excel, NAO encontrados no HTML ----')
    for m in markets_notfound:
        print(f'  X {m}')

excel_markets = set(data.keys())
notfound_in_excel = [hm for hm in html_market_names if hm not in excel_markets]
if notfound_in_excel:
    print('\n---- Mercados NO HTML, NAO encontrados no Excel ----')
    for m in notfound_in_excel:
        print(f'  DELTA {m}')

# ─── 9. VERIFICAÇÃO FINAL ────────────────────────────────────────────────────
print('\n---- Verificacao Final (re-lendo arquivo) ----')
with open(HTML_PATH, 'r', encoding='utf-8') as f:
    saved = f.read()

idx2 = saved.find('const NIELSEN_BRAND_VAL =')
depth2 = 0
pos2 = idx2 + len('const NIELSEN_BRAND_VAL =')
idx_end2 = pos2
for i in range(pos2, min(pos2 + 2000000, len(saved))):
    if saved[i] == '{':
        depth2 += 1
    elif saved[i] == '}':
        depth2 -= 1
        if depth2 == 0:
            idx_end2 = i + 1
            break

saved_block = saved[idx2:idx_end2]
mkt_idx = saved_block.find("'Farma MG+ES+Int RJ'")
if mkt_idx != -1:
    snippet = saved_block[mkt_idx:mkt_idx+800]
    match = re.search(r"'OFF!':[^{]*\{[^}]*jan25_val:(-?\d+(?:\.\d+)?)", snippet)
    if match:
        val_saved = float(match.group(1))
        status = 'CORRETO' if val_saved > 3.5 else 'AINDA ERRADO (esperado ~3.7778)'
        print(f'  Farma MG+ES+Int RJ > OFF! jan25_val: {val_saved}  [{status}]')
    else:
        # Try simpler
        match2 = re.search(r'jan25_val:(-?\d+(?:\.\d+)?)', snippet)
        if match2:
            print(f'  jan25_val encontrado: {match2.group(1)}')
        else:
            print('  ERRO: jan25_val nao encontrado no snippet')
else:
    print('  ERRO: Farma MG+ES+Int RJ nao encontrado')

print('\n====== Script concluido! ======')
print(f'  Arquivo principal: {HTML_PATH}')
print(f'  Backup: {BACKUP_PATH}')
