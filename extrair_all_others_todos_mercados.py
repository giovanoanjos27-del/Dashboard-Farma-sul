"""
extrair_all_others_todos_mercados.py v3
Datas REAIS encontradas na aba 1-Tabela-1 (corrigidas após inspeção):
  FY26: 23/07/2025 | 23/08/2025 | 22/09/2025 | 23/10/2025 | 22/11/2025
        23/12/2025 | 23/01/2026 | 20/02/2026 | 23/03/2026
  FY25: 23/07/2024 | 23/08/2024 | 22/09/2024 | 23/10/2024 | 22/11/2024
        23/12/2024 | 23/01/2025 | 20/02/2025 | 23/03/2025
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path
from collections import defaultdict
import openpyxl
from datetime import datetime, date

XLSX = Path(r'C:\Users\valqu\OneDrive\Documentos\Claude\Projects\projeto Dashboard_farma_sul\Dashboard_farma_sul\_Recursos\Giovano SCJ\Base Giovano 26-04.xlsx')

wb = openpyxl.load_workbook(XLSX, data_only=True)
ws = wb['1-Tabela-1']
rows = list(ws.iter_rows(values_only=True))

# Cabeçalho na linha 9 (index 8)
header_idx = None
for i, row in enumerate(rows):
    if row[0] == 'Markets' and row[2] == 'BRAND':
        header_idx = i
        break
assert header_idx is not None, 'Header não encontrado'
print(f'Header linha {header_idx+1}')

COL_MKT = 0; COL_BRD = 2; COL_DAT = 4; COL_VAL = 5; COL_UN = 10

DATE_MAP = {
    # FYTD
    'FYTD25':'fytd25', 'FYTD26':'fytd26',
    # FY26 monthly (Jul25-Mar26) — datas reais do Excel
    '23/07/2025':'jul26', '23/08/2025':'ago26', '22/09/2025':'set26',
    '23/10/2025':'out26', '22/11/2025':'nov26', '23/12/2025':'dez26',
    '23/01/2026':'jan26', '20/02/2026':'fev26', '23/03/2026':'mar26',
    # FY25 monthly (Jul24-Mar25)
    '23/07/2024':'jul25', '23/08/2024':'ago25', '22/09/2024':'set25',
    '23/10/2024':'out25', '22/11/2024':'nov25', '23/12/2024':'dez25',
    '23/01/2025':'jan25', '20/02/2025':'fev25', '23/03/2025':'mar25',
}

def to_str(d):
    if isinstance(d, (datetime, date)):
        return d.strftime('%d/%m/%Y')
    return str(d).strip()

# Acumular: data_agg[mkt][brand][periodo] = [val, un]
data_agg = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: [0.0, 0.0])))
cur_mkt = None
for row in rows[header_idx+1:]:
    if row[COL_MKT] and str(row[COL_MKT]).strip():
        cur_mkt = str(row[COL_MKT]).strip()
    if not cur_mkt: continue
    brand = row[COL_BRD]
    if not brand: continue
    brand = str(brand).strip()
    if not brand: continue
    dat_str = to_str(row[COL_DAT]) if row[COL_DAT] else ''
    periodo = DATE_MAP.get(dat_str)
    if not periodo: continue
    val = float(row[COL_VAL]) if row[COL_VAL] else 0.0
    un  = float(row[COL_UN])  if row[COL_UN]  else 0.0
    data_agg[cur_mkt][brand][periodo][0] += val
    data_agg[cur_mkt][brand][periodo][1] += un

TARGET = 'ALL OTHERS CAMP'
mercados = sorted(m for m in data_agg if TARGET in data_agg[m])
print(f'Mercados com ALL OTHERS CAMP: {len(mercados)}')

FY26_MONTHS = ['jul26','ago26','set26','out26','nov26','dez26','jan26','fev26','mar26']
FY25_MONTHS = ['jul25','ago25','set25','out25','nov25','dez25','jan25','fev25','mar25']

def gv(d, k): return d[k][0] if k in d else 0.0
def gu(d, k): return d[k][1] if k in d else 0.0

results = {}
for mkt in mercados:
    aoc = data_agg[mkt][TARGET]
    # Somar todas as marcas (não de total) para totais
    all_brands = [b for b in data_agg[mkt] if b not in ('Total','Grand Total')]

    def total_v(k):
        return sum(data_agg[mkt][b][k][0] for b in all_brands if k in data_agg[mkt][b])
    def total_u(k):
        return sum(data_agg[mkt][b][k][1] for b in all_brands if k in data_agg[mkt][b])

    r = dict(
        # ALL OTHERS CAMP
        aoc_fytd25_v=gv(aoc,'fytd25')/1e6, aoc_fytd26_v=gv(aoc,'fytd26')/1e6,
        aoc_fytd25_u=gu(aoc,'fytd25')/1e3, aoc_fytd26_u=gu(aoc,'fytd26')/1e3,
        aoc_jan25_v=gv(aoc,'jan25')/1e6, aoc_fev25_v=gv(aoc,'fev25')/1e6,
        aoc_mar25_v=gv(aoc,'mar25')/1e6,
        aoc_jan26_v=gv(aoc,'jan26')/1e6, aoc_fev26_v=gv(aoc,'fev26')/1e6,
        aoc_mar26_v=gv(aoc,'mar26')/1e6,
        aoc_jan25_u=gu(aoc,'jan25')/1e3, aoc_fev25_u=gu(aoc,'fev25')/1e3,
        aoc_mar25_u=gu(aoc,'mar25')/1e3,
        aoc_jan26_u=gu(aoc,'jan26')/1e3, aoc_fev26_u=gu(aoc,'fev26')/1e3,
        aoc_mar26_u=gu(aoc,'mar26')/1e3,
        aoc_monthly_v26=[gv(aoc,m)/1e6 for m in FY26_MONTHS],
        aoc_monthly_u26=[gu(aoc,m)/1e3 for m in FY26_MONTHS],
        aoc_monthly_v25=[gv(aoc,m)/1e6 for m in FY25_MONTHS],
        # TOTAIS (para calcular share)
        tot_fytd25_v=total_v('fytd25')/1e6, tot_fytd26_v=total_v('fytd26')/1e6,
        tot_jan25_v=total_v('jan25')/1e6, tot_fev25_v=total_v('fev25')/1e6,
        tot_mar25_v=total_v('mar25')/1e6,
        tot_jan26_v=total_v('jan26')/1e6, tot_fev26_v=total_v('fev26')/1e6,
        tot_mar26_v=total_v('mar26')/1e6,
        tot_monthly_v26=[total_v(m)/1e6 for m in FY26_MONTHS],
        tot_monthly_u26=[total_u(m)/1e3 for m in FY26_MONTHS],
    )
    results[mkt] = r

# Validar Farma Sul vs screenshot
fs = results['Farma Sul']
print(f'\n=== VALIDAÇÃO Farma Sul vs Screenshot ===')
print(f'AOC fytd25={fs["aoc_fytd25_v"]:.4f}M  (esperado 35.806)')
print(f'AOC fytd26={fs["aoc_fytd26_v"]:.4f}M  (esperado 32.936)')
print(f'AOC jan25={fs["aoc_jan25_v"]:.4f}  fev25={fs["aoc_fev25_v"]:.4f}  mar25={fs["aoc_mar25_v"]:.4f}')
print(f'AOC jan26={fs["aoc_jan26_v"]:.4f}  fev26={fs["aoc_fev26_v"]:.4f}  mar26={fs["aoc_mar26_v"]:.4f}')
print(f'AOC monthly_v26: {[round(x,3) for x in fs["aoc_monthly_v26"]]}')
print(f'TOT fytd26={fs["tot_fytd26_v"]:.4f}M  (esperado 107.10)')
print(f'TOT monthly_v26: {[round(x,3) for x in fs["tot_monthly_v26"]]}')

# Validar T.BR Farma
tbr = results['T.BR Farma']
print(f'\n=== VALIDAÇÃO T.BR Farma ===')
print(f'AOC fytd25={tbr["aoc_fytd25_v"]:.4f}M  (esperado 112.467)')
print(f'AOC fytd26={tbr["aoc_fytd26_v"]:.4f}M  (esperado 81.410)')
print(f'AOC jan26={tbr["aoc_jan26_v"]:.4f}  fev26={tbr["aoc_fev26_v"]:.4f}  mar26={tbr["aoc_mar26_v"]:.4f}')
print(f'AOC monthly_v26: {[round(x,3) for x in tbr["aoc_monthly_v26"]]}')
print(f'TOT fytd26={tbr["tot_fytd26_v"]:.4f}M  (esperado 431.73)')

# ── Gerar arquivo de saída completo ─────────────────────────────────────────
out = Path(r'C:\Users\valqu\OneDrive\Documentos\Claude\Projects\projeto Dashboard_farma_sul\all_others_data.py')
lines = [
    '# all_others_data.py — ALL OTHERS CAMP + totais por mercado\n',
    '# Gerado por extrair_all_others_todos_mercados.py v3\n',
    '# Unidades: valores em R$ Milhões, unidades em Mil\n\n',
    'DATA = {\n'
]
for mkt, r in sorted(results.items()):
    lines.append(f"  '{mkt}': dict(\n")
    # AOC
    lines.append(f"    aoc_fytd25_v={r['aoc_fytd25_v']:.4f}, aoc_fytd26_v={r['aoc_fytd26_v']:.4f},\n")
    lines.append(f"    aoc_fytd25_u={r['aoc_fytd25_u']:.4f}, aoc_fytd26_u={r['aoc_fytd26_u']:.4f},\n")
    lines.append(f"    aoc_jan25_v={r['aoc_jan25_v']:.4f}, aoc_fev25_v={r['aoc_fev25_v']:.4f}, aoc_mar25_v={r['aoc_mar25_v']:.4f},\n")
    lines.append(f"    aoc_jan26_v={r['aoc_jan26_v']:.4f}, aoc_fev26_v={r['aoc_fev26_v']:.4f}, aoc_mar26_v={r['aoc_mar26_v']:.4f},\n")
    lines.append(f"    aoc_jan25_u={r['aoc_jan25_u']:.4f}, aoc_fev25_u={r['aoc_fev25_u']:.4f}, aoc_mar25_u={r['aoc_mar25_u']:.4f},\n")
    lines.append(f"    aoc_jan26_u={r['aoc_jan26_u']:.4f}, aoc_fev26_u={r['aoc_fev26_u']:.4f}, aoc_mar26_u={r['aoc_mar26_u']:.4f},\n")
    lines.append(f"    aoc_monthly_v26={[round(x,4) for x in r['aoc_monthly_v26']]},\n")
    lines.append(f"    aoc_monthly_u26={[round(x,4) for x in r['aoc_monthly_u26']]},\n")
    lines.append(f"    aoc_monthly_v25={[round(x,4) for x in r['aoc_monthly_v25']]},\n")
    # Totais
    lines.append(f"    tot_fytd25_v={r['tot_fytd25_v']:.4f}, tot_fytd26_v={r['tot_fytd26_v']:.4f},\n")
    lines.append(f"    tot_jan25_v={r['tot_jan25_v']:.4f}, tot_fev25_v={r['tot_fev25_v']:.4f}, tot_mar25_v={r['tot_mar25_v']:.4f},\n")
    lines.append(f"    tot_jan26_v={r['tot_jan26_v']:.4f}, tot_fev26_v={r['tot_fev26_v']:.4f}, tot_mar26_v={r['tot_mar26_v']:.4f},\n")
    lines.append(f"    tot_monthly_v26={[round(x,4) for x in r['tot_monthly_v26']]},\n")
    lines.append(f"    tot_monthly_u26={[round(x,4) for x in r['tot_monthly_u26']]},\n")
    lines.append(f"  ),\n")
lines.append('}\n')
out.write_text(''.join(lines), encoding='utf-8')
print(f'\nSalvo: {out}')
print('DONE.')
