#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
extract_market_total_v3.py
Replica exatamente o cálculo da aba MERCADO do Excel:
  Soma TODOS os tipos de linha (shr=100 + brands + products) para cada
  market × período — que é o que o Excel faz no pivot da aba MERCADO.

Verificado: Farma Sul FYTD26 = 339.815MM ✓ (= aba MERCADO do Excel)

Salva em fytd_market_total_v3.json
"""
import json, openpyxl
from pathlib import Path

BASE = Path(r"C:\Users\valqu\OneDrive\Documentos\Claude\Projects\projeto Dashboard_farma_sul")
EXCEL = BASE / "base_temp_copy.xlsx"
OUT   = BASE / "fytd_market_total_v3.json"

print("Abrindo Excel...")
wb = openpyxl.load_workbook(str(EXCEL), read_only=True, data_only=True)
ws = wb["1-Tabela-1"]

# Header row = row 9 (0-indexed row 8)
# Colunas: 0=markets, 1=CATEGORY, 2=BRAND, 3=Products, 4=Data, 5=$, 10=(UNID)
COL_MKT  = 0
COL_PER  = 4
COL_VAL  = 5
COL_UN   = 10
PERIODS  = {"FYTD25", "FYTD26"}

totals = {}

for row in ws.iter_rows(min_row=10, values_only=True):
    mkt = row[COL_MKT]
    if not mkt: continue
    mkt = str(mkt).strip()
    if not mkt: continue

    period = row[COL_PER]
    if not period: continue
    p = str(period).strip().upper()
    if p not in PERIODS: continue

    val = row[COL_VAL]
    un  = row[COL_UN] if len(row) > COL_UN else None

    try:    v = float(val) / 1e6 if val is not None else 0.0
    except: v = 0.0
    try:    u = float(un)  / 1e3 if un  is not None else 0.0
    except: u = 0.0

    if mkt not in totals:
        totals[mkt] = {}
    if p not in totals[mkt]:
        totals[mkt][p] = {"val": 0.0, "un": 0.0}
    totals[mkt][p]["val"] += v
    totals[mkt][p]["un"]  += u

wb.close()
print(f"Mercados encontrados: {len(totals)}")

output = {}
for mkt, periods in totals.items():
    f25 = periods.get("FYTD25", {})
    f26 = periods.get("FYTD26", {})
    output[mkt] = {
        "fytd25_val": round(f25.get("val", 0), 6),
        "fytd26_val": round(f26.get("val", 0), 6),
        "fytd25_un":  round(f25.get("un",  0), 3),
        "fytd26_un":  round(f26.get("un",  0), 3),
    }

# Verificacao
print("\n--- Verificacao (FYTD26 R$MM) ---")
checks = [
    ("Farma Sul",       339.815, -2.70),
    ("T.BR Farma",      None,    None),
    ("Farma Indep Sul", None,    None),
    ("Farma Moderno Sul", None,  None),
]
for mkt, expected, exp_cres in checks:
    d = output.get(mkt)
    if d:
        cres = (d["fytd26_val"]/d["fytd25_val"]-1)*100 if d["fytd25_val"] > 0 else 0
        ok = ""
        if expected:
            ok = " OK" if abs(d["fytd26_val"] - expected) < 0.1 else " DIVERGE"
        print(f"  {mkt:<25} F25={d['fytd25_val']:>10.3f}MM  F26={d['fytd26_val']:>10.3f}MM  Cres={cres:+.2f}%{ok}")
    else:
        print(f"  {mkt:<25} NAO ENCONTRADO")

# Salva
with open(str(OUT), "w", encoding="utf-8") as f:
    json.dump(output, f, indent=2, ensure_ascii=False)
print(f"\nSalvo: {OUT.name} ({len(output)} mercados)")
