"""
gerar_cobertura_estado.py
=========================
Extrai dados de cobertura por UF e por Cidade a partir de:
  - positivação ano 2024x2025x2026.xlsx  (QUERY sheet)

FY25 = Jul/24–Abr/25 = colunas Mês202407 a Mês202504
FY26 = Jul/25–Abr/26 = colunas Mês202507 a Mês202604

Métricas por CNPJ (deduplicado):
  - is_fy25 : teve PDV > 0 em qualquer mês FY25
  - is_fy26 : teve PDV > 0 em qualquer mês FY26
  - reconq  : is_fy25 AND NOT is_fy26
  - ws_puro : NOT is_fy25 AND NOT is_fy26

Saída: dois blocos JS injetados no HTML via patch
  const UF_COB_DATA  = { ... }   (27 UFs)
  const CITY_COB_DATA = { ... }  (top 20 cidades por UF, ordenadas por universo)
"""
import sys, time, json
sys.stdout.reconfigure(encoding='utf-8')
import pandas as pd
from pathlib import Path
from datetime import datetime

BASE = Path(r'C:\Users\valqu\OneDrive\Documentos\Claude\Projects\projeto Dashboard_farma_sul\Dashboard_farma_sul\_Recursos\Giovano SCJ')
OUT  = Path(r'C:\Users\valqu\OneDrive\Documentos\Claude\Projects\projeto Dashboard_farma_sul')

t0 = time.time()

# ─────────────────────────────────────────────────────────────────────────────
# 1. Ler positivação QUERY
# ─────────────────────────────────────────────────────────────────────────────
fp = BASE / 'positivação ano 2024x2025x2026.xlsx'
print(f'Lendo {fp.name}...')

# Colunas: CNPJ(0), UF(3), Cidade(4) + FY25[10:20] + FY26[22:32]
# (os índices foram confirmados no script de inspeção)
cols_idx = [0, 3, 4] + list(range(10, 20)) + list(range(22, 32))

df = pd.read_excel(fp, sheet_name='QUERY', header=0,
                   usecols=cols_idx, dtype={0: str})

# Renomear colunas
fy25_cols = [f'f25_{i}' for i in range(10)]
fy26_cols = [f'f26_{i}' for i in range(10)]
df.columns = ['CNPJ', 'UF', 'Cidade'] + fy25_cols + fy26_cols

print(f'  {len(df):,} linhas lidas em {time.time()-t0:.1f}s')

# Limpar dados
df['CNPJ'] = df['CNPJ'].str.strip().str.zfill(14)
df['UF']   = df['UF'].str.strip().str.upper()
df['Cidade'] = df['Cidade'].str.strip()

# Flags de positivação
df['is_fy25'] = df[fy25_cols].fillna(0).gt(0).any(axis=1)
df['is_fy26'] = df[fy26_cols].fillna(0).gt(0).any(axis=1)

# ─────────────────────────────────────────────────────────────────────────────
# 2. Dedup por CNPJ (pode aparecer várias vezes por provedor)
# ─────────────────────────────────────────────────────────────────────────────
cnpj_df = df.groupby('CNPJ').agg(
    UF      =('UF',     'first'),
    Cidade  =('Cidade', 'first'),
    is_fy25 =('is_fy25','any'),
    is_fy26 =('is_fy26','any')
).reset_index()

print(f'  CNPJs únicos: {len(cnpj_df):,}')

# ─────────────────────────────────────────────────────────────────────────────
# 3. Métricas por UF
# ─────────────────────────────────────────────────────────────────────────────
def uf_metrics(g):
    tot   = len(g)
    fy25  = int(g.is_fy25.sum())
    fy26  = int(g.is_fy26.sum())
    reconq = int((g.is_fy25 & ~g.is_fy26).sum())
    ws_puro = int((~g.is_fy25 & ~g.is_fy26).sum())
    white_sp = tot - fy26
    return pd.Series({'universe': tot, 'fy25': fy25, 'fy26': fy26,
                      'reconq': reconq, 'ws_puro': ws_puro, 'white_sp': white_sp})

uf_data = cnpj_df.groupby('UF').apply(uf_metrics).reset_index()

print('\n=== UF_COB_DATA ===')
print(f'{"UF":>3} | {"Univ":>6} | {"FY25":>5} | {"FY26":>5} | {"Reconq":>6} | {"WS":>6} | {"Cob%":>5}')
for _, r in uf_data.sort_values('universe', ascending=False).iterrows():
    pct = round(r.fy26/r.universe*100) if r.universe else 0
    print(f'  {r.UF:>3} | {int(r.universe):>6} | {int(r.fy25):>5} | {int(r.fy26):>5} | {int(r.reconq):>6} | {int(r.ws_puro):>6} | {pct:>4}%')

# ─────────────────────────────────────────────────────────────────────────────
# 4. Métricas por Cidade — top 20 por UF (por universo desc)
# ─────────────────────────────────────────────────────────────────────────────
# Limpar nome cidade (remover " - UF" do final)
def clean_city(c):
    if not c: return ''
    c = str(c).strip()
    if ' - ' in c:
        c = c.rsplit(' - ', 1)[0]
    return c.title()

cnpj_df['CidadeClean'] = cnpj_df['Cidade'].apply(clean_city)

city_data_raw = cnpj_df.groupby(['UF','CidadeClean']).apply(
    lambda g: pd.Series({
        'universe': len(g),
        'fy25':    int(g.is_fy25.sum()),
        'fy26':    int(g.is_fy26.sum()),
        'reconq':  int((g.is_fy25 & ~g.is_fy26).sum()),
        'ws_puro': int((~g.is_fy25 & ~g.is_fy26).sum()),
        'white_sp': len(g) - int(g.is_fy26.sum()),
    })
).reset_index()

# Top 20 por UF
city_top20 = (city_data_raw
    .sort_values('universe', ascending=False)
    .groupby('UF', group_keys=False)
    .head(20)
)

print(f'\nCidades extraídas (top 20/UF): {len(city_top20)}')
# Sample SP
print('\nAmostra SP (top 5):')
for _, r in city_top20[city_top20.UF=='SP'].head(5).iterrows():
    pct = round(r.fy26/r.universe*100) if r.universe else 0
    print(f'  {r.CidadeClean:<25} uni={int(r.universe):>5} fy26={int(r.fy26):>5} {pct}%')

# ─────────────────────────────────────────────────────────────────────────────
# 5. Gerar JS constants
# ─────────────────────────────────────────────────────────────────────────────
def js_uf(uf_data):
    """Gera const UF_COB_DATA = { ... }"""
    lines = []
    for _, r in uf_data.iterrows():
        uf = r.UF
        pct = round(r.fy26/r.universe*100) if r.universe else 0
        lines.append(
            f'  "{uf}":{{'
            f'universe:{int(r.universe)},'
            f'fy25:{int(r.fy25)},'
            f'fy26:{int(r.fy26)},'
            f'reconq:{int(r.reconq)},'
            f'ws_puro:{int(r.ws_puro)},'
            f'white_sp:{int(r.white_sp)},'
            f'pct:{pct}}}'
        )
    return 'const UF_COB_DATA = {\n' + ',\n'.join(lines) + '\n};'

def js_city(city_top20):
    """Gera const CITY_COB_DATA = { "SP": [{cidade,metrics...}, ...], ... }"""
    result = {}
    for uf, grp in city_top20.groupby('UF'):
        cities = []
        for _, r in grp.sort_values('universe', ascending=False).iterrows():
            pct = round(r.fy26/r.universe*100) if r.universe else 0
            cities.append({
                'n': r.CidadeClean,
                'u': int(r.universe),
                'f25': int(r.fy25),
                'f26': int(r.fy26),
                'rq': int(r.reconq),
                'ws': int(r.ws_puro),
                'wsp': int(r.white_sp),
                'p': pct
            })
        result[uf] = cities

    # Formato compacto para JS
    city_str = 'const CITY_COB_DATA = ' + json.dumps(result, ensure_ascii=False, separators=(',', ':')) + ';'
    return city_str

uf_js   = js_uf(uf_data)
city_js = js_city(city_top20)

# Salvar em arquivo auxiliar
out_js = OUT / 'cobertura_data.js'
out_js.write_text(uf_js + '\n\n' + city_js, encoding='utf-8')
print(f'\n✓ Dados JS salvos em {out_js.name} ({out_js.stat().st_size:,} bytes)')
print(f'  UF_COB_DATA:   {len(uf_data)} estados')
print(f'  CITY_COB_DATA: {len(city_top20)} cidades (top 20/UF)')
print(f'Tempo total: {time.time()-t0:.1f}s')
