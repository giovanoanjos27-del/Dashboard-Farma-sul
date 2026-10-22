"""
calcula_dn_intoc_grupos.py  v2
==============================
Calcula DN% dos 3 SKUs Intocáveis por Grupo_Provedor com:
  - FYTD25: Jul/2024–Mar/2025
  - FYTD26: Jul/2025–Mar/2026
  - Por mês individual (todos os meses disponíveis nos períodos FYTD)

Fórmula DN%:
  total    = PDVs (CNPJs) do grupo com qualquer venda naquele período
  posit    = PDVs que venderam o SKU naquele período (soma > 0)
  DN%      = posit / total × 100

Saída: dn_intoc_grupos.js  (constante JS pronta para o dashboard)
"""
import sys, json
sys.stdout.reconfigure(encoding='utf-8')
import pandas as pd
from pathlib import Path

# ── Caminhos ──────────────────────────────────────────────────────────────────
XLSX = Path(r'C:\Users\valqu\OneDrive\Documentos\Claude\Projects\projeto Dashboard_farma_sul\Dashboard_farma_sul\_Recursos\Giovano SCJ\vendas por EAN novo.xlsx')
OUT  = Path(r'C:\Users\valqu\OneDrive\Documentos\Claude\Projects\projeto Dashboard_farma_sul\dn_intoc_grupos.js')

# ── SKUs Intocáveis ───────────────────────────────────────────────────────────
SKUS = {
    'kids200':  'OFF REPELENTE LOCAO REPELENTE KIDS GRATIS 83ML 200.0 ML X 1.0',
    'spray170': 'OFF REPELENTE SPRAY FAMILY OFERTA ESPECIAL 170.0 ML X 1.0',
    'locao200': 'OFF REPELENTE LOCAO FAMILY 30% DESCONTO 200.0 ML X 1.0',
}
SKU_KEYS = list(SKUS.keys())

# ── Períodos ──────────────────────────────────────────────────────────────────
FYTD25_MESES = ['202407','202408','202409','202410','202411','202412',
                '202501','202502','202503']
FYTD26_MESES = ['202507','202508','202509','202510','202511','202512',
                '202601','202602','202603']
TODOS_MESES  = FYTD25_MESES + FYTD26_MESES

def col(m): return f'Mês_{m}_Unidade'

ALL_COLS = [col(m) for m in TODOS_MESES]

# ── Leitura ───────────────────────────────────────────────────────────────────
print('Lendo arquivo (1M+ linhas)...')
df = pd.read_excel(XLSX, dtype=str,
                   usecols=['Grupo_Provedor','CNPJ','Apresentacao_Longa'] + ALL_COLS)
print(f'  Total linhas: {len(df):,}')

# Converter meses para numérico
for c in ALL_COLS:
    df[c] = pd.to_numeric(df[c], errors='coerce').fillna(0)

# Flag por mês e por SKU (se o PDV vendeu aquele SKU naquele mês)
for m in TODOS_MESES:
    df[f'_v_{m}'] = df[col(m)] > 0

# Flag por período FYTD
df['_v_fytd25'] = df[[f'_v_{m}' for m in FYTD25_MESES]].any(axis=1)
df['_v_fytd26'] = df[[f'_v_{m}' for m in FYTD26_MESES]].any(axis=1)

# Flag "ativo" por mês = qualquer produto com venda > 0
for m in TODOS_MESES:
    df[f'_ativo_{m}'] = df[col(m)] > 0

# Ativo no FYTD (qualquer mês)
df['_ativo_fytd25'] = df[[f'_ativo_{m}' for m in FYTD25_MESES]].any(axis=1)
df['_ativo_fytd26'] = df[[f'_ativo_{m}' for m in FYTD26_MESES]].any(axis=1)

# ── Função auxiliar ───────────────────────────────────────────────────────────
def calc_dn(grupo_df, sku_nome, periodo_flag, ativo_flag):
    """Retorna (total_pdvs, posit_pdvs, dn_pct) para um grupo/SKU/período."""
    total = grupo_df.loc[grupo_df[ativo_flag], 'CNPJ'].nunique()
    if total == 0:
        return 0, 0, 0.0
    posit = grupo_df.loc[(grupo_df['Apresentacao_Longa'] == sku_nome) &
                          grupo_df[periodo_flag], 'CNPJ'].nunique()
    dn = round(posit / total * 100, 1)
    return total, posit, dn

def calc_soma(grupo_df, periodo_flag, ativo_flag):
    """Calcula somatório: algum, dois, todos os 3 SKUs."""
    total = grupo_df.loc[grupo_df[ativo_flag], 'CNPJ'].nunique()
    if total == 0:
        return {'total': 0, 'algum': 0, 'dnAlgum': 0,
                'dois': 0, 'dnDois': 0, 'todos': 0, 'dnTodos': 0}

    sets = {}
    for sku_key, sku_nome in SKUS.items():
        mask = (grupo_df['Apresentacao_Longa'] == sku_nome) & grupo_df[periodo_flag]
        sets[sku_key] = set(grupo_df[mask]['CNPJ'].unique())

    algum = len(sets['kids200'] | sets['spray170'] | sets['locao200'])
    dois  = len((sets['kids200'] & sets['spray170']) |
                (sets['kids200'] & sets['locao200']) |
                (sets['spray170'] & sets['locao200']))
    todos = len(sets['kids200'] & sets['spray170'] & sets['locao200'])

    return {
        'total': total,
        'algum':  algum,  'dnAlgum':  round(algum  / total * 100, 1),
        'dois':   dois,   'dnDois':   round(dois   / total * 100, 1),
        'todos':  todos,  'dnTodos':  round(todos  / total * 100, 1),
    }

# ── Cálculo por grupo ─────────────────────────────────────────────────────────
print('\nCalculando...')
grupos = sorted(df['Grupo_Provedor'].dropna().unique())
result = {}

for i, grupo in enumerate(grupos):
    if (i + 1) % 10 == 0:
        print(f'  {i+1}/{len(grupos)} grupos...')

    g = df[df['Grupo_Provedor'] == grupo].copy()

    entry = {}

    # FYTD25 e FYTD26
    for periodo, pflag, aflag in [
        ('fytd25', '_v_fytd25', '_ativo_fytd25'),
        ('fytd26', '_v_fytd26', '_ativo_fytd26'),
    ]:
        skus_data = {}
        for sku_key, sku_nome in SKUS.items():
            tot, pos, dn = calc_dn(g, sku_nome, pflag, aflag)
            skus_data[sku_key] = {'total': tot, 'pdvs': pos, 'dn': dn}
        soma = calc_soma(g, pflag, aflag)
        entry[periodo] = {'soma': soma, **skus_data}

    # Por mês individual
    entry['meses'] = {}
    for m in TODOS_MESES:
        pflag = f'_v_{m}'
        aflag = f'_ativo_{m}'
        mes_data = {}
        for sku_key, sku_nome in SKUS.items():
            tot, pos, dn = calc_dn(g, sku_nome, pflag, aflag)
            mes_data[sku_key] = {'total': tot, 'pdvs': pos, 'dn': dn}
        # soma do mês
        total_m = g.loc[g[aflag], 'CNPJ'].nunique()
        sets_m = {}
        for sku_key, sku_nome in SKUS.items():
            mask = (g['Apresentacao_Longa'] == sku_nome) & g[pflag]
            sets_m[sku_key] = set(g.loc[mask, 'CNPJ'].unique())
        algum_m = len(sets_m['kids200'] | sets_m['spray170'] | sets_m['locao200'])
        entry['meses'][m] = {
            'total':   total_m,
            'soma_dn': round(algum_m / total_m * 100, 1) if total_m > 0 else 0,
            **mes_data,
        }

    result[grupo] = entry

# ── Console: resumo FYTD26 ────────────────────────────────────────────────────
print(f'\n{"GRUPO":35} {"PDVs26":>7} {"Kids26":>7} {"Spray26":>8} {"Loção26":>8} {"Kids25":>7} {"Spray25":>8}')
print('-' * 88)
for grupo, d in sorted(result.items()):
    tot26 = d['fytd26']['kids200']['total']
    if tot26 < 10:
        continue   # pular grupos muito pequenos no resumo
    k26 = d['fytd26']['kids200']['dn']
    s26 = d['fytd26']['spray170']['dn']
    l26 = d['fytd26']['locao200']['dn']
    k25 = d['fytd25']['kids200']['dn']
    s25 = d['fytd25']['spray170']['dn']
    print(f'{grupo:35} {tot26:>7,} {k26:>6.1f}% {s26:>7.1f}% {l26:>7.1f}%  {k25:>6.1f}% {s25:>7.1f}%')

# ── Gerar JS ──────────────────────────────────────────────────────────────────
print(f'\nGerando {OUT.name}...')

lines = [
    '/* ─── DN INTOCÁVEIS × GRUPO PROVEDOR ────────────────────────────────────────',
    '   Gerado por calcula_dn_intoc_grupos.py  v2',
    '   Fonte: vendas por EAN novo.xlsx',
    '   FYTD25 = Jul/2024–Mar/2025 | FYTD26 = Jul/2025–Mar/2026',
    '   total  = PDVs ativos no período (qualquer produto com venda > 0)',
    '   pdvs   = PDVs que venderam o SKU Intocável no período',
    '   dn     = pdvs / total × 100',
    '────────────────────────────────────────────────────────────────────────────── */',
    'const DN_INTOC_GRUPOS = {'
]

for grupo, d in sorted(result.items()):
    lines.append(f'  {json.dumps(grupo)}: {{')

    for periodo in ['fytd25', 'fytd26']:
        pd_data = d[periodo]
        soma = pd_data['soma']
        lines.append(f'    {periodo}: {{')
        lines.append(f'      soma:    {{total:{soma["total"]},algum:{soma["algum"]},dnAlgum:{soma["dnAlgum"]},dois:{soma["dois"]},dnDois:{soma["dnDois"]},todos:{soma["todos"]},dnTodos:{soma["dnTodos"]}}},')
        for sk in SKU_KEYS:
            s = pd_data[sk]
            lines.append(f'      {sk}: {{total:{s["total"]},pdvs:{s["pdvs"]},dn:{s["dn"]}}},')
        lines.append(f'    }},')

    lines.append(f'    meses: {{')
    for m in TODOS_MESES:
        md = d['meses'][m]
        sk_str = ', '.join(f'{sk}:{{total:{md[sk]["total"]},pdvs:{md[sk]["pdvs"]},dn:{md[sk]["dn"]}}}' for sk in SKU_KEYS)
        lines.append(f'      "{m}": {{total:{md["total"]},soma_dn:{md["soma_dn"]},{sk_str}}},')
    lines.append(f'    }},')
    lines.append(f'  }},')

lines.append('};')

OUT.write_text('\n'.join(lines), encoding='utf-8')
print(f'✅ Salvo em {OUT}')
print('DONE.')
