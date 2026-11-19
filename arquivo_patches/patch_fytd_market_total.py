"""
patch_fytd_market_total.py
Recalcula FYTD_MARKET_TOTAL usando SOMENTE linhas de Brand-level
(Products=NaN, BRAND not NaN) — exclui o (vazio) / linhas SKU.

Afeta todos os mercados e reflete em:
 - VENDA VALOR FYTD · JUL-MAR  (fytd25_val/fytd26_val/fytd25_un/fytd26_un)
 - MARKET SHARE — JAN·FEV·MAR  (janmar25_val/janmar26_val/janmar25_un/janmar26_un)
"""
import sys, shutil
sys.stdout.reconfigure(encoding='utf-8')
import pandas as pd
from datetime import datetime
from pathlib import Path

BASE = Path(r"C:\Users\valqu\OneDrive\Documentos\Claude\Projects\projeto Dashboard_farma_sul\Dashboard_farma_sul")
XLS  = BASE / r"_Recursos\Giovano SCJ\Base Giovano 26-04.xlsx"
DASH = BASE / "Dashboard_Farma_Sul_20260512_2220.html"
VER  = BASE / "versoes"
DL   = Path.home() / "Downloads"

ts = datetime.now().strftime('%Y%m%d_%H%M')
shutil.copy(DASH, VER / f"Dashboard_Farma_Sul_{ts}_PreFytdMktFix.html")
print(f"Backup: Dashboard_Farma_Sul_{ts}_PreFytdMktFix.html")

# ── 1. Ler Excel ──────────────────────────────────────────────────────────────
print("\n1. Lendo Excel...")
df = pd.read_excel(XLS, sheet_name='1-Tabela-1', header=8)
df.columns = ['markets','CATEGORY','BRAND','Products','Data','val','WDR','price','shr','TDP','unid','ROS']

# Filtro: brand-level apenas (Products NaN, BRAND notna, val > 0)
brand = df[df['Products'].isna() & df['BRAND'].notna() & df['val'].notna() & (df['val']>0)].copy()
print(f"   Brand rows: {len(brand):,}  Brands: {sorted(brand['BRAND'].unique())}")

def norm_date(v):
    if pd.isna(v): return ''
    s = str(v).strip()
    if 'FYTD' in s.upper(): return s.upper()
    try: return pd.to_datetime(v).strftime('%Y-%m-%d')
    except: return s

brand['ds'] = brand['Data'].apply(norm_date)

PERIODS = {
    'fytd25':    'FYTD25',
    'fytd26':    'FYTD26',
    'jan25':     '2025-01-23',
    'fev25':     '2025-02-20',
    'mar25':     '2025-03-23',
    'jan26':     '2026-01-23',
    'fev26':     '2026-02-20',
    'mar26':     '2026-03-23',
}

# ── 2. Somar por mercado + periodo ─────────────────────────────────────────────
print("\n2. Calculando totais brand-only por mercado...")

all_dates = list(PERIODS.values())
sub = brand[brand['ds'].isin(all_dates)].copy()

# Somar val e unid por mercado + periodo
agg = sub.groupby(['markets','ds'])[['val','unid']].sum().reset_index()

markets = [str(m).strip() for m in sub['markets'].dropna().unique()]
print(f"   Mercados: {len(markets)}")

def get(mkt, ds, col):
    row = agg[(agg['markets']==mkt) & (agg['ds']==ds)]
    if len(row) > 0:
        v = row.iloc[0][col]
        return float(v) if pd.notna(v) else 0.0
    return 0.0

result = {}
for mkt in markets:
    f25v = get(mkt, PERIODS['fytd25'], 'val') / 1e6
    f26v = get(mkt, PERIODS['fytd26'], 'val') / 1e6
    f25u = get(mkt, PERIODS['fytd25'], 'unid') / 1e3
    f26u = get(mkt, PERIODS['fytd26'], 'unid') / 1e3

    j25_vals = [get(mkt, PERIODS[k], 'val')/1e6 for k in ['jan25','fev25','mar25']]
    j26_vals = [get(mkt, PERIODS[k], 'val')/1e6 for k in ['jan26','fev26','mar26']]
    j25_uns  = [get(mkt, PERIODS[k], 'unid')/1e3 for k in ['jan25','fev25','mar25']]
    j26_uns  = [get(mkt, PERIODS[k], 'unid')/1e3 for k in ['jan26','fev26','mar26']]

    result[mkt] = {
        'fytd25_val':   round(f25v, 4),
        'fytd26_val':   round(f26v, 4),
        'fytd25_un':    round(f25u, 4),
        'fytd26_un':    round(f26u, 4),
        'jan25_val':    round(j25_vals[0], 4),
        'fev25_val':    round(j25_vals[1], 4),
        'mar25_val':    round(j25_vals[2], 4),
        'janmar25_val': round(sum(j25_vals), 4),
        'jan26_val':    round(j26_vals[0], 4),
        'fev26_val':    round(j26_vals[1], 4),
        'mar26_val':    round(j26_vals[2], 4),
        'janmar26_val': round(sum(j26_vals), 4),
        'jan25_un':     round(j25_uns[0], 4),
        'fev25_un':     round(j25_uns[1], 4),
        'mar25_un':     round(j25_uns[2], 4),
        'janmar25_un':  round(sum(j25_uns), 4),
        'jan26_un':     round(j26_uns[0], 4),
        'fev26_un':     round(j26_uns[1], 4),
        'mar26_un':     round(j26_uns[2], 4),
        'janmar26_un':  round(sum(j26_uns), 4),
    }

# Validacao T.BR Farma
v = result.get('T.BR Farma', {})
print(f"\n   VALIDACAO T.BR Farma:")
print(f"     fytd25_val: {v.get('fytd25_val'):.4f}MM  (esperado: ~419.62)")
print(f"     fytd26_val: {v.get('fytd26_val'):.4f}MM  (esperado: ~350.32)")
print(f"     janmar25_val: {v.get('janmar25_val'):.4f}MM  (esperado: ~214.66)")
print(f"     janmar26_val: {v.get('janmar26_val'):.4f}MM  (esperado: ~177.07)")

# ── 3. Gerar nova const JS ─────────────────────────────────────────────────────
print("\n3. Gerando nova const FYTD_MARKET_TOTAL...")

def fmt(v): return str(round(v,4))

lines = ["const FYTD_MARKET_TOTAL = {"]
items = list(result.items())
for i, (mkt, d) in enumerate(items):
    comma = '' if i==len(items)-1 else ','
    mkt_e = mkt.replace("'","\\'")
    fields = ','.join(f"{k}:{fmt(d[k])}" for k in [
        'fytd25_val','fytd26_val','fytd25_un','fytd26_un',
        'jan25_val','fev25_val','mar25_val','janmar25_val',
        'jan26_val','fev26_val','mar26_val','janmar26_val',
        'jan25_un','fev25_un','mar25_un','janmar25_un',
        'jan26_un','fev26_un','mar26_un','janmar26_un'
    ])
    lines.append(f"  '{mkt_e}': {{{fields}}}{comma}")
lines.append("};")
NEW_CONST = '\n'.join(lines)
print(f"   Nova const: {len(NEW_CONST):,} chars, {len(result)} mercados")

# ── 4. Substituir no HTML ──────────────────────────────────────────────────────
print("\n4. Atualizando dashboard...")
html = DASH.read_text(encoding='utf-8')
orig = len(html)

ANCHOR = 'const FYTD_MARKET_TOTAL ='
assert ANCHOR in html, "ERRO: FYTD_MARKET_TOTAL nao encontrado"
idx_s = html.index(ANCHOR)

# Encontrar fim do bloco (contar chaves)
depth=0; pos=idx_s+len(ANCHOR); idx_e=pos
for i in range(pos, min(pos+2000000, len(html))):
    if html[i]=='{': depth+=1
    elif html[i]=='}':
        depth-=1
        if depth==0: idx_e=i+1; break

old_block = html[idx_s:idx_e]
print(f"   Bloco antigo: {len(old_block):,} chars")
html = html[:idx_s] + NEW_CONST + html[idx_e:]
print(f"   Bloco novo: {len(NEW_CONST):,} chars  (delta {len(NEW_CONST)-len(old_block):+,})")

# ── 5. Salvar ──────────────────────────────────────────────────────────────────
DASH.write_text(html, encoding='utf-8')
versao = VER / f"Dashboard_Farma_Sul_{ts}_FytdMktFix.html"
shutil.copy(DASH, versao)
dl = DL / f"Dashboard_FarmaSul_Giovano_{ts}.html"
shutil.copy(DASH, dl)
print(f"\nVersao:    {versao.name}")
print(f"Downloads: {dl.name}")
print(f"Dashboard: {len(html):,} chars (delta {len(html)-orig:+,})")
print("DONE.")
