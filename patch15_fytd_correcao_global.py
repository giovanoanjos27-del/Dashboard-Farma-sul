"""
PATCH 15 — Correção global fytd25/fytd26/delta em MKTSHARE_OVERVIEW
Fonte: Base Giovano (25-05).xlsx
Escopo: todos os markets × 6 brands (OFF!, EXPOSIS, XO INSETO, SUPER REPELEX, SBP, ALL OTHERS CAMP)
"""

import pandas as pd, re, shutil, datetime

SRC = r'Dashboard_farma_sul\Dashboard_Farma_Sul_20260512_2220.html'

# --- 1. Ler Excel e montar pivot fytd25/fytd26 ---
path = r'Dashboard_farma_sul\_Recursos\Giovano SCJ\Base Giovano (25-05).xlsx'
df = pd.read_excel(path, sheet_name='1-Tabela-1', header=7, skiprows=[8,9,10])
df.columns = ['Markets','CATEGORY','BRAND','Products','Data','Valor','DistNum','DistPond','Share','TDP','Unid','ROS']
df = df[df['Markets'].notna() & df['Data'].notna()]
df['Data'] = df['Data'].astype(str).str.strip()
brands_ok = ['OFF!','EXPOSIS','XO INSETO','SUPER REPELEX','SBP','ALL OTHERS CAMP']
df = df[df['BRAND'].isin(brands_ok)]
df['PeriodKey'] = df['Data'].map({'FYTD25':'fytd25','FYTD26':'fytd26'})
df = df[df['PeriodKey'].isin(['fytd25','fytd26'])]
df['Share'] = pd.to_numeric(df['Share'], errors='coerce')
pvt = df.groupby(['Markets','BRAND','PeriodKey'])['Share'].mean().round(2).unstack('PeriodKey')

print(f'Tabela Excel: {len(pvt)} market×brand combinations\n')

# --- 2. Ler HTML ---
html = open(SRC, encoding='utf-8').read()
original_len = len(html)
patches_ok = 0
patches_skip = 0
patches_miss = 0

mso_start = html.find('MKTSHARE_OVERVIEW = {')

# --- 3. Para cada market no Excel que existe no dashboard ---
xl_markets = pvt.index.get_level_values('Markets').unique()

for mkt in xl_markets:
    mkt_key = f"'{mkt}':"
    mkt_pos = html.find(mkt_key, mso_start)
    if mkt_pos == -1:
        continue

    for brand in ['OFF!','EXPOSIS','XO INSETO','SUPER REPELEX','SBP','ALL OTHERS CAMP']:
        try:
            xl_f25 = pvt.loc[(mkt, brand), 'fytd25']
            xl_f26 = pvt.loc[(mkt, brand), 'fytd26']
        except (KeyError, TypeError):
            continue

        if pd.isna(xl_f25) or pd.isna(xl_f26):
            continue

        xl_delta = round(xl_f26 - xl_f25, 2)
        xl_f25 = round(xl_f25, 2)
        xl_f26 = round(xl_f26, 2)

        # Encontrar brand dentro do bloco do market
        brand_search = f"'{brand}':"
        brand_pos = html.find(brand_search, mkt_pos)
        if brand_pos == -1 or brand_pos > mkt_pos + 2000:
            patches_miss += 1
            continue

        # Extrair chunk do brand entry (até fim da linha)
        line_end = html.find('\n', brand_pos)
        if line_end == -1:
            line_end = brand_pos + 500
        chunk = html[brand_pos:line_end]

        # Extrair valores atuais de fytd25, fytd26, delta
        m25 = re.search(r'fytd25:([\d.]+)', chunk)
        m26 = re.search(r'fytd26:([\d.]+)', chunk)
        md  = re.search(r'delta:(-?[\d.]+)', chunk)
        if not m25 or not m26 or not md:
            patches_miss += 1
            continue

        dash_f25 = float(m25.group(1))
        dash_f26 = float(m26.group(1))
        dash_delta = float(md.group(1))

        # Se já correto, pular
        if abs(dash_f25 - xl_f25) < 0.005 and abs(dash_f26 - xl_f26) < 0.005:
            patches_skip += 1
            continue

        # Substituir apenas os três valores dentro do chunk
        old_chunk = chunk
        new_chunk = chunk
        new_chunk = re.sub(r'fytd25:[\d.]+',   f'fytd25:{xl_f25}',   new_chunk, count=1)
        new_chunk = re.sub(r'fytd26:[\d.]+',   f'fytd26:{xl_f26}',   new_chunk, count=1)
        new_chunk = re.sub(r'delta:-?[\d.]+',  f'delta:{xl_delta}',  new_chunk, count=1)

        if old_chunk == new_chunk:
            patches_miss += 1
            continue

        html = html[:brand_pos] + new_chunk + html[line_end:]
        patches_ok += 1

print(f'Patches aplicados : {patches_ok}')
print(f'Ja corretos (skip): {patches_skip}')
print(f'Nao encontrados   : {patches_miss}')
print(f'Diff              : {len(html) - original_len:+d} bytes')

# --- 4. Salvar ---
ts = datetime.datetime.now().strftime('%Y%m%d_%H%M')
ver = f'Dashboard_farma_sul/versoes/Dashboard_Farma_Sul_{ts}_FytdCorrecaoGlobal.html'
open(SRC, 'w', encoding='utf-8').write(html)
open(ver, 'w', encoding='utf-8').write(html)
print(f'\nSalvo  : {SRC}')
print(f'Versao : {ver}')
