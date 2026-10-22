"""
extract_janmar_totals.py  v2
Extrai TOTAL REAL DO MERCADO somando TODAS as linhas (SCJ + competidores)
para Jan/Fev/Mar 2025/2026 e FYTD25/FYTD26 de todos os mercados.

Saida: janmar_market_totals.json
"""

import json
import pandas as pd
import numpy as np

XLS  = r"C:\Users\valqu\OneDrive\Documentos\Claude\Projects\projeto Dashboard_farma_sul\Dashboard_farma_sul\_Recursos\Giovano SCJ\Base Giovano 26-04.xlsx"
OUT  = r"C:\Users\valqu\OneDrive\Documentos\Claude\Projects\projeto Dashboard_farma_sul\janmar_market_totals.json"

print("Lendo 1-Tabela-1...")
df = pd.read_excel(XLS, sheet_name="1-Tabela-1", header=8)
df.columns = ['markets','CATEGORY','BRAND','Products','Data','val','WDR','price','shr','TDP','unid','ROS']
print(f"  Total linhas: {len(df):,}")

# Normalizar datas
def norm_date(v):
    if pd.isna(v): return ''
    s = str(v).strip()
    if 'FYTD' in s.upper() or 'FY' in s.upper(): return s.upper()
    try:
        dt = pd.to_datetime(v)
        return dt.strftime('%Y-%m-%d')
    except:
        return s

df['data_str'] = df['Data'].apply(norm_date)

# Periodos que queremos
JAN25 = '2025-01-23'
FEV25 = '2025-02-20'
MAR25 = '2025-03-23'
JAN26 = '2026-01-23'
FEV26 = '2026-02-20'
MAR26 = '2026-03-23'
PERIODS = [JAN25, FEV25, MAR25, JAN26, FEV26, MAR26, 'FYTD25', 'FYTD26']

# Remover linhas de footer/metadata (sem mercado real)
SKIP_MKTS = {'', 'nan'}
meta_patterns = ['Dataset:', 'Direitos de', 'Exportado:', 'Terms &', 'nan']
def is_real_market(m):
    m = str(m).strip()
    if m in SKIP_MKTS: return False
    if m.lower().startswith('dataset'): return False
    if m.lower().startswith('direitos'): return False
    if m.lower().startswith('exportado'): return False
    if m.lower().startswith('terms'): return False
    return True

df = df[df['markets'].apply(lambda m: is_real_market(str(m)))]
df = df[df['val'].notna() & (df['val'] > 0)]

# Agrupar por mercado + data_str - SOMA TOTAL (todas as linhas)
agg = df.groupby(['markets','data_str'])[['val','unid']].sum().reset_index()

print(f"  Mercados unicos: {df['markets'].nunique()}")

result = {}
for mkt in df['markets'].unique():
    sub = agg[agg['markets']==mkt].set_index('data_str')

    def g(d, col):
        if d in sub.index:
            v = sub.loc[d, col]
            return float(v) if pd.notna(v) else 0.0
        return 0.0

    jan25_v = g(JAN25, 'val') / 1e6
    fev25_v = g(FEV25, 'val') / 1e6
    mar25_v = g(MAR25, 'val') / 1e6
    jan26_v = g(JAN26, 'val') / 1e6
    fev26_v = g(FEV26, 'val') / 1e6
    mar26_v = g(MAR26, 'val') / 1e6
    fytd25_v = g('FYTD25', 'val') / 1e6
    fytd26_v = g('FYTD26', 'val') / 1e6

    jan25_u = g(JAN25, 'unid') / 1e3
    fev25_u = g(FEV25, 'unid') / 1e3
    mar25_u = g(MAR25, 'unid') / 1e3
    jan26_u = g(JAN26, 'unid') / 1e3
    fev26_u = g(FEV26, 'unid') / 1e3
    mar26_u = g(MAR26, 'unid') / 1e3
    fytd25_u = g('FYTD25', 'unid') / 1e3
    fytd26_u = g('FYTD26', 'unid') / 1e3

    result[mkt] = {
        'jan25_val':    round(jan25_v,  4),
        'fev25_val':    round(fev25_v,  4),
        'mar25_val':    round(mar25_v,  4),
        'janmar25_val': round(jan25_v+fev25_v+mar25_v, 4),
        'jan26_val':    round(jan26_v,  4),
        'fev26_val':    round(fev26_v,  4),
        'mar26_val':    round(mar26_v,  4),
        'janmar26_val': round(jan26_v+fev26_v+mar26_v, 4),
        'fytd25_val':   round(fytd25_v, 4),
        'fytd26_val':   round(fytd26_v, 4),
        'jan25_un':     round(jan25_u,  4),
        'fev25_un':     round(fev25_u,  4),
        'mar25_un':     round(mar25_u,  4),
        'janmar25_un':  round(jan25_u+fev25_u+mar25_u, 4),
        'jan26_un':     round(jan26_u,  4),
        'fev26_un':     round(fev26_u,  4),
        'mar26_un':     round(mar26_u,  4),
        'janmar26_un':  round(jan26_u+fev26_u+mar26_u, 4),
        'fytd25_un':    round(fytd25_u, 4),
        'fytd26_un':    round(fytd26_u, 4),
    }

print(f"  Mercados extraidos: {len(result)}")

# Validacao T.BR Farma
tbr = result.get('T.BR Farma', {})
print("\n=== VALIDACAO T.BR Farma ===")
print(f"  Jan/25:     R${tbr.get('jan25_val',0):.3f}MM  | esperado: 283.815")
print(f"  Fev/25:     R${tbr.get('fev25_val',0):.3f}MM  | esperado: 274.875")
print(f"  Mar/25:     R${tbr.get('mar25_val',0):.3f}MM  | esperado: 279.690")
print(f"  JanMar/25:  R${tbr.get('janmar25_val',0):.3f}MM  | esperado: 838.379")
print(f"  Jan/26:     R${tbr.get('jan26_val',0):.3f}MM  | esperado: 266.395")
print(f"  Fev/26:     R${tbr.get('fev26_val',0):.3f}MM  | esperado: 214.775")
print(f"  Mar/26:     R${tbr.get('mar26_val',0):.3f}MM  | esperado: 204.890")
print(f"  JanMar/26:  R${tbr.get('janmar26_val',0):.3f}MM  | esperado: 686.060")
print(f"  FYTD25:     R${tbr.get('fytd25_val',0):.3f}MM")
print(f"  FYTD26:     R${tbr.get('fytd26_val',0):.3f}MM")
print("=" * 40)

# Listar todos
print("\nTodos os mercados (Jan-Mar/25 vs Jan-Mar/26):")
for k in sorted(result.keys()):
    r = result[k]
    a25 = r['janmar25_val']
    a26 = r['janmar26_val']
    pct = ((a26/a25)-1)*100 if a25 else 0
    print(f"  {k:<45} 25:R${a25:8.3f}MM  26:R${a26:8.3f}MM  {pct:+.1f}%")

with open(OUT, 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print(f"\nSalvo: {OUT}")
