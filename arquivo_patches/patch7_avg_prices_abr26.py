"""
patch7_avg_prices_abr26.py
Adiciona ABR/26 (10º valor) nos arrays de AVG_DATA — gráfico PREÇO MÉDIO POR PRODUTO.
Fonte: Base Giovano (25-05).xlsx — coluna Avg Price (col7) — ABR/26.
"""
import os, shutil, datetime, re

BASE = r"C:\Users\valqu\OneDrive\Documentos\Claude\Projects\projeto Dashboard_farma_sul\Dashboard_farma_sul"
SRC  = os.path.join(BASE, "Dashboard_Farma_Sul_20260512_2220.html")

# [OFF! Family Loção 200ml PR, OFF! Family Spray 170ml PR, Xô Loção 200ml, Xô Spray 200ml]
APR26_PRICES = {
  'farmasul':          [22.35,22.1,20.04,20.27],
  'farma_co':          [21.21,22.58,21.24,20.96],
  'farma_gde_rj':      [20.05,21.95,18.03,19.44],
  'farma_gde_sp':      [21.0,23.31,20.8,22.91],
  'farma_int_sp':      [21.78,23.02,21.62,21.19],
  'farma_mg':          [21.1,22.33,19.38,20.03],
  'farma_ne':          [20.95,21.85,18.8,19.38],
  'farma_indep_co':    [22.01,23.3,21.02,21.23],
  'farma_indep_gde_rj':[20.05,21.04,17.32,19.07],
  'farma_indep_gde_sp':[24.0,25.14,20.88,25.54],
  'farma_indep_int_sp':[24.75,25.23,22.05,21.65],
  'farma_indep_mg':    [22.05,22.91,19.32,20.45],
  'farma_indep_ne':    [21.08,22.14,18.7,19.46],
  'farma_indep_sul':   [21.46,21.06,19.84,19.38],
  'farma_mod_co':      [19.99,21.95,23.12,20.02],
  'farma_mod_gde_rj':  [20.06,22.75,19.6,19.9],
  'farma_mod_gde_sp':  [20.2,22.78,20.65,20.12],
  'farma_mod_int_sp':  [19.96,21.1,20.07,20.24],
  'farma_mod_mg':      [19.8,21.78,19.57,19.11],
  'farma_mod_ne':      [20.65,21.49,19.61,19.08],
  'farma_mod_sul':     [23.36,23.75,20.35,21.51],
  'tbr_farma':         [21.2,22.36,19.62,20.3],
  'tbr_farma_indep':   [21.72,22.54,19.52,20.37],
  'tbr_farma_mod':     [20.56,22.18,20.01,20.14],
  'rs':                [22.3,23.34,19.55,20.19],
  'sc':                [23.1,21.22,20.39,20.31],
  'pr':                [21.73,21.82,20.18,20.29],
  'infc_cwb':          [22.24,22.69,20.68,22.05],
  'infc_poa':          [22.01,23.32,20.78,22.26],
  'infc_sul':          [22.35,22.1,20.04,20.27],
  'infc_int_pr':       [21.52,21.63,20.1,19.88],
  'infc_int_rs':       [22.76,23.36,18.88,19.53],
  'infc_cg_sul':       [22.48,23.34,20.86,22.05],
  'infc_cp_sul':       [22.34,21.8,19.92,19.96],
  'infc_mg':           [22.06,22.49,19.95,20.1],
  'infc_co':           [21.21,22.6,21.24,20.96],
  'infc_ba':           [21.02,22.54,18.13,18.98],
  'infc_bh':           [21.84,22.64,20.57,19.67],
  'infc_ce':           [20.68,20.57,17.84,18.12],
  'infc_cg_gde_rj':    [20.18,21.96,18.03,19.41],
  'infc_cg_co':        [20.85,22.11,24.62,21.36],
  'infc_cg_gde_sp':    [21.06,23.35,20.76,22.83],
  'infc_cg_int_sp':    [20.45,21.92,20.02,20.78],
  'infc_cg_mg':        [22.22,22.0,20.72,19.83],
  'infc_cg_ne':        [20.91,21.79,18.6,18.75],
  'infc_cp_co':        [21.45,23.02,20.73,20.87],
  'infc_cp_int_sp':    [21.98,23.19,21.75,21.21],
  'infc_cp_mg':        [21.07,22.58,19.18,20.06],
  'infc_cp_ne':        [20.96,21.89,18.88,19.59],
  'infc_df':           [20.27,22.43,24.13,21.84],
  'infc_for':          [20.61,20.29,20.78,20.14],
  'infc_go':           [21.05,21.72,21.81,21.6],
  'infc_gde_rj':       [20.16,21.95,18.03,19.43],
  'infc_gde_sp':       [20.99,23.32,20.75,22.77],
  'infc_int_ba':       [21.0,22.18,17.91,18.28],
  'infc_int_ce':       [20.74,21.07,17.25,17.57],
  'infc_int_mg':       [22.17,22.39,19.78,20.23],
  'infc_int_pe':       [19.73,20.42,17.74,17.81],
  'infc_int_sp':       [21.78,23.02,21.58,21.16],
  'infc_mapi':         [22.61,22.51,20.88,21.75],
  'infc_mg_es':        [21.33,22.45,19.38,20.03],
  'infc_man_bel':      [21.65,21.92,22.04,22.5],
  'infc_manaus':       [21.05,22.59,20.86,19.75],
  'infc_ne':           [20.95,21.85,18.81,19.38],
  'infc_pe':           [20.35,21.2,18.06,17.69],
  'infc_recife':       [20.92,22.25,18.4,17.57],
  'infc_sp':           [21.57,23.1,21.44,21.51],
  'infc_salvador':     [21.09,23.23,18.75,21.51],
  'tbr_infc':          [21.25,22.38,19.62,20.29],
}

SKUS = [
    'OFF! Family Loção 200ml PR',
    'OFF! Family Spray 170ml PR',
    'Xô Loção 200ml',
    'Xô Spray 200ml',
]

with open(SRC, 'r', encoding='utf-8') as f:
    html = f.read()

original_len = len(html)
total_patches = 0
fails = []

# Localizar bloco AVG_DATA
avg_start = html.find('AVG_DATA =')
print(f"AVG_DATA inicio: {avg_start}")
print(f"Markets a processar: {len(APR26_PRICES)}\n")

for mkt_key, prices in APR26_PRICES.items():
    # Recomputar avg_end a cada iteracao (html pode ter crescido)
    avg_end = html.find('\n};', avg_start) + 3

    # Localizar o market dentro do bloco
    mkt_tag = f'  {mkt_key}: {{'
    pos = html.find(mkt_tag, avg_start, avg_end)
    if pos == -1:
        fails.append(f'{mkt_key}: nao encontrado')
        continue

    next_pos = html.find('\n  },', pos + len(mkt_tag))
    if next_pos == -1:
        next_pos = html.find('\n};', pos + len(mkt_tag))
    if next_pos == -1:
        next_pos = pos + 2000  # fallback
    section = html[pos:next_pos]
    orig = section
    ok = 0

    for i, sku in enumerate(SKUS):
        apr_val = prices[i]
        if apr_val is None:
            continue
        sku_tag = f"'{sku}':"
        s_pos = section.find(sku_tag)
        if s_pos == -1:
            fails.append(f'{mkt_key}/{sku}: sku nao encontrado')
            continue

        arr_start = section.index('[', s_pos)
        arr_end   = section.index(']', arr_start) + 1
        arr_str   = section[arr_start:arr_end]
        vals_str  = arr_str[1:-1].strip()
        parts     = [v.strip() for v in vals_str.split(',')]

        if len(parts) != 9:
            fails.append(f'{mkt_key}/{sku}: {len(parts)} vals (exp 9)')
            continue

        new_arr = f'[{vals_str}, {apr_val}]'
        section = section[:arr_start] + new_arr + section[arr_end:]
        ok += 1
        total_patches += 1

    html = html[:pos] + section + html[pos + len(orig):]
    status = f'[OK {ok}/4]' if ok == 4 else f'[WARN {ok}/4]'
    print(f'  {mkt_key}: {status}')

print(f"\n=== RESUMO ===")
print(f"Patches: {total_patches}")
print(f"Original: {original_len:,} | Final: {len(html):,} | Diff: {len(html)-original_len:+,}")

if fails:
    print(f"\nFalhas ({len(fails)}):")
    for f in fails: print(f"  {f}")

with open(SRC, 'w', encoding='utf-8') as f:
    f.write(html)
print(f"\nSalvo: {SRC}")

VER = os.path.join(BASE, "versoes", f"Dashboard_Farma_Sul_{datetime.datetime.now().strftime('%Y%m%d_%H%M')}_AvgPriceAbr26.html")
shutil.copy2(SRC, VER)
print(f"Versao: {VER}")
