"""
PATCH 16 — Odor Block: adicionar todos os 42 novos markets ao OB_DATA e dropdowns
Fonte: Base Giovano Odor Block (25-05).xlsx
"""

import pandas as pd, shutil, os, sys, json, datetime, re

SRC = r'Dashboard_farma_sul\Dashboard_Farma_Sul_20260512_2220.html'

# ─── 1. LER EXCEL ────────────────────────────────────────────────────────────
src_xl = r'Dashboard_farma_sul\_Recursos\Giovano SCJ\Base Giovano Odor Block (25-05).xlsx'
tmp_xl = r'Dashboard_farma_sul\_Recursos\Giovano SCJ\Base_OB_tmp.xlsx'
shutil.copy2(src_xl, tmp_xl)

df = pd.read_excel(tmp_xl, sheet_name='1-Tabela-1', header=4)
os.remove(tmp_xl)

df.columns = ['Markets','Data','Products','Valor','DistNum','DistPond','Share','PrecMed','TaxaV','Unid','PrecMedUnid']
df = df[df['Markets'].notna() & (df['Data'] != 'DATA')]
df['Markets']  = df['Markets'].astype(str).str.strip()
df['Products'] = df['Products'].astype(str).str.strip()
df['DataStr']  = df['Data'].astype(str).str[:7]
for col in ['Share','PrecMed','Valor','Unid']:
    df[col] = pd.to_numeric(df[col], errors='coerce')

FY26_MONTHS = ['2025-07','2025-08','2025-09','2025-10','2025-11','2025-12',
               '2026-01','2026-02','2026-03','2026-04']
df26 = df[df['DataStr'].isin(FY26_MONTHS)].copy()

PRODUCTS = ['T. Odor Block','Pato','Pato Block Algodão','Pato Block Lavanda',
            'Pato Block Eucalipto','Freeco','All Others']

# ─── 2. MARKETS JÁ NO DASHBOARD ──────────────────────────────────────────────
EXISTING = {
    'T.BR Farma','AS+C&C+Farma Sul','AS+C&C+Farma Gde SP','AS+C&C+Farma Gde RJ',
    'AS+C&C+Farma NE','AS+C&C+Farma CO','AS+C&C+Farma MG+ES+Int RJ'
}

# Markets Farma/T.BR com 10 meses FY26
months_per = df26.groupby('Markets')['DataStr'].nunique()
complete10  = months_per[months_per == 10].index.tolist()
new_markets = sorted([m for m in complete10
                      if ('Farma' in m or 'T.BR Farma' == m)
                      and m not in EXISTING])

print(f'Novos markets a adicionar: {len(new_markets)}')
for m in new_markets:
    print(f'  {m}')
print()

# ─── 3. EXTRAIR DADOS POR MARKET ──────────────────────────────────────────────
def extract_market(mkt):
    """Retorna dict {produto: {share,preco,valor,unid}} para os 10 meses FY26."""
    sub = df26[df26['Markets'] == mkt]
    data = {}
    for prod in PRODUCTS:
        ps = sub[sub['Products'] == prod].copy()
        ps = ps.sort_values('DataStr')

        def arr(col):
            vals = []
            for m in FY26_MONTHS:
                row = ps[ps['DataStr'] == m]
                if len(row) == 0 or pd.isna(row.iloc[0][col]):
                    vals.append(None)
                else:
                    v = row.iloc[0][col]
                    vals.append(round(float(v), 4))
            return vals

        share = arr('Share')
        preco = arr('PrecMedUnid')  # coluna K = Preco Medio por Unidade (R$17-20)
        valor = arr('Valor')
        unid  = arr('Unid')

        # Converter unid para int quando possível
        unid_int = [int(v) if v is not None else None for v in unid]
        # Arredondar preco para 2 casas
        preco2 = [round(v, 2) if v is not None else None for v in preco]
        share2 = [round(v, 4) if v is not None else None for v in share]
        valor2 = [round(v, 2) if v is not None else None for v in valor]

        data[prod] = {'share': share2, 'preco': preco2, 'valor': valor2, 'unid': unid_int}
    return data

# ─── 4. LABEL MAP ─────────────────────────────────────────────────────────────
def make_label(mkt):
    """Gera label limpo para o dropdown."""
    m = mkt
    m = m.replace('AS+C&C+Farma ', '').replace('AS+Farma ', 'AS+F ')
    return m

# ─── 5. CONSTRUIR JS PARA OB_DATA ─────────────────────────────────────────────
COR_MAP = {
    'T. Odor Block':       '#e2e8f0',
    'Pato':                '#fbbf24',
    'Pato Block Algodão':  '#60a5fa',
    'Pato Block Lavanda':  '#2dd4bf',
    'Pato Block Eucalipto':'#34d399',
    'Freeco':              '#a78bfa',
    'All Others':          '#94a3b8',
}

def js_arr(lst):
    parts = []
    for v in lst:
        if v is None:
            parts.append('null')
        elif isinstance(v, float):
            parts.append(str(v))
        else:
            parts.append(str(v))
    return '[' + ', '.join(parts) + ']'

js_entries = []
for mkt in new_markets:
    data = extract_market(mkt)
    lines = [f'"{mkt}": {{']
    for prod in PRODUCTS:
        d = data[prod]
        cor = COR_MAP.get(prod, '#94a3b8')
        line = (f'  "{prod}": {{"share": {js_arr(d["share"])}, '
                f'"preco": {js_arr(d["preco"])}, '
                f'"valor": {js_arr(d["valor"])}, '
                f'"unid": {js_arr(d["unid"])}, '
                f'"cor": "{cor}"}}')
        lines.append(line + ',')
    # remover última vírgula
    lines[-1] = lines[-1].rstrip(',')
    lines.append('}')
    js_entries.append('\n'.join(lines))

print(f'Entradas JS geradas: {len(js_entries)}')
if js_entries:
    print('Amostra (primeiro market):')
    print(js_entries[0][:300])
    print('...')
    print()

# ─── 6. LER HTML E APLICAR PATCH ──────────────────────────────────────────────
html = open(SRC, encoding='utf-8').read()
original_len = len(html)
patches = 0

# 6a — Adicionar entradas no OB_DATA (antes do }; final)
ob_data_start = html.find('OB_DATA = {')
ob_data_end   = html.find('};', ob_data_start)   # }; que fecha OB_DATA
if ob_data_end == -1:
    # tentar fechar com só }
    ob_data_end = html.find('\n}', ob_data_start)

# Verificar que a posição é correta (próxima ao OB_DATA_start)
print(f'OB_DATA start: {ob_data_start}, end: {ob_data_end}')
print(repr(html[ob_data_end-30:ob_data_end+10]))

# Inserir todas as entradas antes do }; final
insert_str = ''
for entry in js_entries:
    insert_str += ',\n' + entry

old_close = html[ob_data_end:ob_data_end+2]  # '};' ou '}\n'
html = html[:ob_data_end] + insert_str + '\n' + html[ob_data_end:]
patches += len(js_entries)
print(f'[OK] {len(js_entries)} markets inseridos no OB_DATA')

# 6b — Adicionar options nos 3 selects
options_html = ''
for mkt in new_markets:
    lbl = make_label(mkt)
    # escapar & para &amp; no HTML
    val = mkt.replace('&', '&amp;')
    options_html += f'<option value="{val}">{lbl}</option>'

for sel_id in ['obMarketSel', 'obMarketSel2', 'obMarketSel4']:
    sel_idx = html.find(f'id="{sel_id}"')
    if sel_idx == -1:
        print(f'[MISS] {sel_id} não encontrado')
        continue
    # Encontrar </select> correspondente
    sel_end = html.find('</select>', sel_idx)
    if sel_end == -1:
        print(f'[MISS] </select> não encontrado para {sel_id}')
        continue
    # Inserir antes do </select>
    html = html[:sel_end] + options_html + html[sel_end:]
    patches += 1
    print(f'[OK] {sel_id}: {len(new_markets)} options adicionadas')

print(f'\nTotal patches: {patches}')
print(f'Diff: {len(html) - original_len:+,} bytes')

# ─── 7. SALVAR ────────────────────────────────────────────────────────────────
ts = datetime.datetime.now().strftime('%Y%m%d_%H%M')
ver = f'Dashboard_farma_sul/versoes/Dashboard_Farma_Sul_{ts}_OBTodosMarkets.html'
open(SRC, 'w', encoding='utf-8').write(html)
open(ver, 'w', encoding='utf-8').write(html)
print(f'\nSalvo : {SRC}')
print(f'Versao: {ver}')
