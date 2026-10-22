"""
patch9_fytd25_abr25.py
Atualiza fytd25_val e fytd25_un de 9 meses (Jul/24–Mar/25) para 10 meses (Jul/24–Abr/25)
em FYTD_MARKET_TOTAL e NIELSEN_BRAND_VAL — Farma Sul e T.BR Farma.

Fórmula: new_fytd25 = old_fytd25 + abr25_val (já disponível nos dados)

Valores extraídos de Base Giovano (25-05).xlsx / check_fytd25.py:

T.BR Farma FYTD_MARKET_TOTAL:
  fytd25_val: 532.0889 → 595.2652 (+63.1763 = abr25_val)
  fytd25_un:  20307.5189 → 22670.8189 (+2363.3 = soma abr25_un das marcas)

Farma Sul FYTD_MARKET_TOTAL:
  fytd25_val: 111.5341 → 123.4947 (+11.9606 = abr25_val)
  fytd25_un:  4876.0369 → 5361.0369 (+485.0 = soma abr25_un das marcas)

NIELSEN_BRAND_VAL T.BR Farma + Farma Sul: ver dicionário abaixo.

Labels JUL→MAR no diagnóstico e Excel: atualizados para JUL→ABR.
"""
import os, shutil, datetime, sys
sys.stdout.reconfigure(encoding='utf-8')

BASE = r"C:\Users\valqu\OneDrive\Documentos\Claude\Projects\projeto Dashboard_farma_sul\Dashboard_farma_sul"
SRC  = os.path.join(BASE, "Dashboard_Farma_Sul_20260512_2220.html")

with open(SRC, 'r', encoding='utf-8') as f:
    html = f.read()

original_len = len(html)
patches = 0
fails = []

def patch(old, new, desc):
    global html, patches
    c = html.count(old)
    if c == 0:
        fails.append(f"[X] NAO ENCONTRADO: {desc}")
        return False
    if c > 1:
        print(f"  [!] {c}x: {desc}")
    html = html.replace(old, new, 1)  # só 1 substituição p/ segurança
    patches += 1
    print(f"  [OK] {desc}")
    return True

print("=== PATCH 9: fytd25 ABR/25 + labels JUL→ABR ===\n")

# ── FYTD_MARKET_TOTAL ──────────────────────────────────────────────────────────
print("--- FYTD_MARKET_TOTAL ---")

# T.BR Farma — fytd25_val e fytd25_un
patch(
    "'T.BR Farma': {fytd25_val:532.0889,fytd26_val:490.7745,fytd25_un:20307.5189,",
    "'T.BR Farma': {fytd25_val:595.2652,fytd26_val:490.7745,fytd25_un:22670.8189,",
    "FYTD_MARKET_TOTAL T.BR Farma fytd25_val+un"
)

# Farma Sul — fytd25_val e fytd25_un
patch(
    "'Farma Sul': {fytd25_val:111.5341,fytd26_val:118.4166,fytd25_un:4876.0369,",
    "'Farma Sul': {fytd25_val:123.4947,fytd26_val:118.4166,fytd25_un:5361.0369,",
    "FYTD_MARKET_TOTAL Farma Sul fytd25_val+un"
)

# ── NIELSEN_BRAND_VAL T.BR Farma ───────────────────────────────────────────────
print("\n--- NIELSEN_BRAND_VAL T.BR Farma ---")

# OFF!
patch(
    "    'OFF!': {fytd25_val:141.3245,fytd26_val:146.90,fytd25_un:5647.7135,fytd26_un:5178.2677,",
    "    'OFF!': {fytd25_val:158.8644,fytd26_val:146.90,fytd25_un:6362.2135,fytd26_un:5178.2677,",
    "NBV T.BR Farma OFF! fytd25_val+un"
)
# EXPOSIS
patch(
    "    'EXPOSIS': {fytd25_val:97.244,fytd26_val:84.11,fytd25_un:1537.4898,fytd26_un:1223.861,",
    "    'EXPOSIS': {fytd25_val:109.3124,fytd26_val:84.11,fytd25_un:1731.7898,fytd26_un:1223.861,",
    "NBV T.BR Farma EXPOSIS fytd25_val+un"
)
# XO INSETO
patch(
    "    'XO INSETO': {fytd25_val:126.421,fytd26_val:123.04,fytd25_un:5658.9708,fytd26_un:5013.7607,",
    "    'XO INSETO': {fytd25_val:141.1822,fytd26_val:123.04,fytd25_un:6280.0708,fytd26_un:5013.7607,",
    "NBV T.BR Farma XO INSETO fytd25_val+un"
)
# SUPER REPELEX
patch(
    "    'SUPER REPELEX': {fytd25_val:30.7062,fytd26_val:26.44,fytd25_un:1409.3829,fytd26_un:1061.6747,",
    "    'SUPER REPELEX': {fytd25_val:34.3653,fytd26_val:26.44,fytd25_un:1576.7829,fytd26_un:1061.6747,",
    "NBV T.BR Farma SUPER REPELEX fytd25_val+un"
)
# SBP
patch(
    "    'SBP': {fytd25_val:23.9257,fytd26_val:19.19,fytd25_un:692.7618,fytd26_un:480.6864,",
    "    'SBP': {fytd25_val:26.8468,fytd26_val:19.19,fytd25_un:776.0618,fytd26_un:480.6864,",
    "NBV T.BR Farma SBP fytd25_val+un"
)
# ALL OTHERS CAMP
patch(
    "    'ALL OTHERS CAMP': {fytd25_val:112.467,fytd26_val:91.10,fytd25_un:5361.2,fytd26_un:4136.5,",
    "    'ALL OTHERS CAMP': {fytd25_val:124.6936,fytd26_val:91.10,fytd25_un:5943.9,fytd26_un:4136.5,",
    "NBV T.BR Farma ALL OTHERS CAMP fytd25_val+un"
)

# ── NIELSEN_BRAND_VAL Farma Sul ────────────────────────────────────────────────
print("\n--- NIELSEN_BRAND_VAL Farma Sul ---")

# OFF!
patch(
    "    'OFF!': {fytd25_val:26.8083,fytd26_val:",
    "    'OFF!': {fytd25_val:29.7777,fytd26_val:",
    "NBV Farma Sul OFF! fytd25_val"
)
patch(
    "fytd25_un:1097.7409,fytd26_un:",
    "fytd25_un:1216.6409,fytd26_un:",
    "NBV Farma Sul OFF! fytd25_un"
)
# EXPOSIS
patch(
    "    'EXPOSIS': {fytd25_val:13.5798,fytd26_val:",
    "    'EXPOSIS': {fytd25_val:15.3394,fytd26_val:",
    "NBV Farma Sul EXPOSIS fytd25_val"
)
patch(
    "fytd25_un:211.9125,fytd26_un:",
    "fytd25_un:239.0125,fytd26_un:",
    "NBV Farma Sul EXPOSIS fytd25_un"
)
# XO INSETO
patch(
    "    'XO INSETO': {fytd25_val:24.0848,fytd26_val:",
    "    'XO INSETO': {fytd25_val:26.6436,fytd26_val:",
    "NBV Farma Sul XO INSETO fytd25_val"
)
patch(
    "fytd25_un:1086.9599,fytd26_un:",
    "fytd25_un:1186.5599,fytd26_un:",
    "NBV Farma Sul XO INSETO fytd25_un"
)
# SUPER REPELEX
patch(
    "    'SUPER REPELEX': {fytd25_val:7.834,fytd26_val:",
    "    'SUPER REPELEX': {fytd25_val:8.6594,fytd26_val:",
    "NBV Farma Sul SUPER REPELEX fytd25_val"
)
patch(
    "fytd25_un:353.5803,fytd26_un:",
    "fytd25_un:389.9803,fytd26_un:",
    "NBV Farma Sul SUPER REPELEX fytd25_un"
)
# SBP
patch(
    "    'SBP': {fytd25_val:3.4212,fytd26_val:",
    "    'SBP': {fytd25_val:3.8219,fytd26_val:",
    "NBV Farma Sul SBP fytd25_val"
)
patch(
    "fytd25_un:93.843,fytd26_un:",
    "fytd25_un:104.443,fytd26_un:",
    "NBV Farma Sul SBP fytd25_un"
)
# ALL OTHERS CAMP
patch(
    "    'ALL OTHERS CAMP': {fytd25_val:35.806,fytd26_val:",
    "    'ALL OTHERS CAMP': {fytd25_val:39.2527,fytd26_val:",
    "NBV Farma Sul ALL OTHERS CAMP fytd25_val"
)
patch(
    "fytd25_un:2032.0004,fytd26_un:",
    "fytd25_un:2224.4004,fytd26_un:",
    "NBV Farma Sul ALL OTHERS CAMP fytd25_un"
)

# ── Labels JUL→MAR no diagnóstico e Excel ────────────────────────────────────
print("\n--- Labels JUL→MAR → JUL→ABR ---")

# Diagnóstico card 3 (pos ~12514005)
patch(
    'ACUM. FY25 · JUL/24→MAR/25',
    'ACUM. FY25 · JUL/24→ABR/25',
    "Diagnóstico card3 ACUM FY25 label"
)
patch(
    'ACUM. FY26 · JUL/25→MAR/26',
    'ACUM. FY26 · JUL/25→ABR/26',
    "Diagnóstico card3 ACUM FY26 label"
)

# Excel export function names
patch(
    'UNIDADES FYTD JUL-MAR CONSOLIDADO',
    'UNIDADES FYTD JUL-ABR CONSOLIDADO',
    "Excel sheetFn name JUL-MAR"
)
patch(
    'UNIDADES FYTD JUL–MAR \xb7',
    'UNIDADES FYTD JUL–ABR \xb7',
    "Excel sheet label JUL–MAR"
)

# ── RESUMO ────────────────────────────────────────────────────────────────────
print(f"\n=== RESUMO ===")
print(f"Patches OK:  {patches}")
if fails:
    print(f"Falhas ({len(fails)}):")
    for f in fails: print(f"  {f}")
print(f"Original: {original_len:,} | Final: {len(html):,} | Diff: {len(html)-original_len:+,}")

with open(SRC, 'w', encoding='utf-8') as f:
    f.write(html)
print(f"\nSalvo: {SRC}")

VER = os.path.join(BASE, "versoes", f"Dashboard_Farma_Sul_{datetime.datetime.now().strftime('%Y%m%d_%H%M')}_FYTD25Abr25Fix.html")
shutil.copy2(SRC, VER)
print(f"Versão: {VER}")
