#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
extract_market_total_v2.py
Extrai total REAL do mercado Personal Repellent por market usando linhas brand=None
(Shr=100 = total categoria), diferente da v1 que somava todas as linhas de brand.
Salva em fytd_market_total_v2.json e imprime verificação.
"""
import json, sys
from pathlib import Path

try:
    import openpyxl
except ImportError:
    sys.exit("pip install openpyxl")

EXCEL_PATH = Path(r"C:\Users\valqu\OneDrive\Documentos\Claude\Projects\projeto Dashboard_farma_sul\Dashboard_farma_sul\_Recursos\Giovano SCJ\Base Giovano 26-04.xlsx")
OUT_JSON   = Path(r"C:\Users\valqu\OneDrive\Documentos\Claude\Projects\projeto Dashboard_farma_sul\fytd_market_total_v2.json")
SHEET_NAME = "1-Tabela-1"

print(f"Abrindo {EXCEL_PATH.name} ...")
wb = openpyxl.load_workbook(str(EXCEL_PATH), read_only=True, data_only=True)
if SHEET_NAME not in wb.sheetnames:
    sys.exit(f"Aba '{SHEET_NAME}' nao encontrada.")

ws = wb[SHEET_NAME]

# --- detectar cabecalho ---
col_market = col_category = col_brand = col_period = col_val = col_un = None
header_found = False
for row in ws.iter_rows(min_row=1, max_row=20, values_only=True):
    for i, cell in enumerate(row):
        if cell is None: continue
        s = str(cell).strip().upper()
        if s in ("MARKETS", "MARKET"):   col_market   = i
        elif s == "CATEGORY":            col_category = i
        elif s == "BRAND":               col_brand    = i
        elif s in ("DATA", "DATE", "PERIOD"): col_period = i
        elif s == "$":                   col_val      = i
        elif s in ("(UNID)", "UNID", "UNITS"): col_un = i
    if col_market is not None and col_period is not None and col_val is not None:
        header_found = True
        print(f"Header detectado: market={col_market}, cat={col_category}, "
              f"brand={col_brand}, period={col_period}, val={col_val}, un={col_un}")
        break

if not header_found:
    sys.exit("Cabecalho nao encontrado")

PERIODS = {"FYTD25", "FYTD26"}
TARGET_CAT = "PERSONAL REPELLENT"
totals = {}
rows_total = 0
rows_brand_none = 0

for row in ws.iter_rows(min_row=2, values_only=True):
    rows_total += 1
    if not any(c is not None for c in row[:max(col_market, col_period, col_val)+1]):
        continue

    # filtro categoria
    cat = row[col_category] if col_category is not None else None
    if cat is None or str(cat).strip().upper() != TARGET_CAT:
        continue

    # FILTRO CHAVE: brand deve ser None/vazio → linha de total mercado (Shr=100)
    brand = row[col_brand] if col_brand is not None else None
    if brand is not None and str(brand).strip() != "":
        continue   # pula linhas de marcas individuais

    rows_brand_none += 1

    # filtro período
    period = row[col_period]
    if period is None: continue
    p = str(period).strip().upper()
    if p not in PERIODS: continue

    mkt = row[col_market]
    if mkt is None: continue
    mkt = str(mkt).strip()
    if not mkt: continue

    try:    val = float(row[col_val]) / 1e6 if row[col_val] is not None else 0.0
    except: val = 0.0
    try:    un  = float(row[col_un])  / 1e3 if col_un is not None and row[col_un] is not None else 0.0
    except: un  = 0.0

    if mkt not in totals:
        totals[mkt] = {}
    if p not in totals[mkt]:
        totals[mkt][p] = {"val": 0.0, "un": 0.0}
    totals[mkt][p]["val"] += val
    totals[mkt][p]["un"]  += un

wb.close()
print(f"Total linhas: {rows_total} | brand=None (total mercado): {rows_brand_none} | mercados: {len(totals)}")

if not totals:
    print("ATENCAO: nenhuma linha brand=None encontrada!")
    print("Tentando approach alternativo: linhas com '(Total)' ou Shr=100 ...")
    sys.exit("Verifique estrutura da aba 1-Tabela-1 manualmente")

# Arredonda
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

# Verificação amostral
print("\n--- Verificacao amostral (FYTD26 R$MM) ---")
for mkt in ["T.BR Farma", "Farma Sul", "Farma Indep Sul", "Farma Moderno Sul"]:
    if mkt in output:
        d = output[mkt]
        cres = (d["fytd26_val"]/d["fytd25_val"]-1)*100 if d["fytd25_val"] > 0 else 0
        print(f"  {mkt:<30} F25={d['fytd25_val']:>10.3f}MM  "
              f"F26={d['fytd26_val']:>10.3f}MM  Cres={cres:+.2f}%")
    else:
        print(f"  {mkt:<30} NAO ENCONTRADO")

print("\nEsperado Farma Sul: F25≈349.25MM  F26≈339.82MM  Cres≈-2.70%")
print("Esperado T.BR Farma: F25≈1653.47MM  F26≈1362.38MM  Cres≈-17.60%")

with open(str(OUT_JSON), "w", encoding="utf-8") as f:
    json.dump(output, f, indent=2, ensure_ascii=False)
print(f"\nSalvo: {OUT_JSON.name}  ({len(output)} mercados)")
