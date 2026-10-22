"""
extrair_abr25_mso2.py — v3
Filtra apenas linhas brand-level (Products = None) para evitar dupla contagem.
Header linha 9: market=0, brand=2, products=3, date=4, val=5, un=10, shr=8
"""
import openpyxl, datetime, json, os
from collections import defaultdict

EXCEL_PATH = r"C:\Users\valqu\OneDrive\Documentos\Claude\Projects\projeto Dashboard_farma_sul\Dashboard_farma_sul\_Recursos\Giovano SCJ\Base Giovano (25-05).xlsx"

TARGET_MARKETS = {'Farma Sul', 'T.BR Farma'}

C_MKT   = 0  # Markets
C_BRAND = 2  # BRAND
C_PROD  = 3  # Products
C_DATE  = 4  # Data
C_VAL   = 5  # $
C_UN    = 10 # (UNID)
C_SHR   = 8  # $ Shr - Product

def is_apr25(v):
    return isinstance(v, datetime.datetime) and v.year == 2025 and v.month == 4

def norm_brand(b):
    if b is None: return None
    b = str(b).strip().upper()
    if 'OFF!' in b or 'OFF FAMILY' in b: return 'OFF!'
    if 'EXPOSIS' in b: return 'EXPOSIS'
    if 'XO INSETO' in b or 'XO-INSETO' in b: return 'XO INSETO'
    if 'SUPER REPELEX' in b or 'REPELEX' in b: return 'SUPER REPELEX'
    if 'SBP' in b: return 'SBP'
    if 'ALL OTHERS' in b or 'OUTROS' in b: return 'ALL OTHERS CAMP'
    return b  # retorna o nome original para entender o que há

print("Abrindo Excel...")
wb = openpyxl.load_workbook(EXCEL_PATH, read_only=True, data_only=True)
ws = wb['1-Tabela-1']

# data[market][brand] = [val, un, shr]
data = defaultdict(dict)
unknowns = set()
n_total = 0

for row in ws.iter_rows(min_row=10, max_col=12, values_only=True):
    market = row[C_MKT]
    if market not in TARGET_MARKETS:
        continue
    date_val = row[C_DATE]
    if not is_apr25(date_val):
        continue

    brand_raw = row[C_BRAND]
    prod_raw  = row[C_PROD]

    # Apenas linhas brand-level: Products = None
    if prod_raw is not None:
        continue

    n_total += 1
    val = float(row[C_VAL] or 0)
    un  = float(row[C_UN]  or 0)
    shr = float(row[C_SHR] or 0)

    brand = norm_brand(brand_raw)

    if brand is None:
        # categoria total (brand=None) → total mercado
        data[market]['__TOTAL__'] = [val, un, shr]
    else:
        data[market][brand] = [val, un, shr]
        if brand not in ('OFF!','EXPOSIS','XO INSETO','SUPER REPELEX','SBP','ALL OTHERS CAMP','__TOTAL__'):
            unknowns.add(brand)

wb.close()
print(f"Linhas brand-level Abr/25 encontradas: {n_total}")
if unknowns:
    print(f"Brands não mapeados: {unknowns}")

# ── RESULTADO ──
TARGET_BRANDS = ['OFF!', 'EXPOSIS', 'XO INSETO', 'SUPER REPELEX', 'SBP', 'ALL OTHERS CAMP']

result = {}
print("\n=== RESULTADOS ABR/25 ===")
for mkt in ['Farma Sul', 'T.BR Farma']:
    tot = data[mkt].get('__TOTAL__', [0,0,0])
    print(f"\n{mkt}")
    print(f"  Total mercado: R${tot[0]/1e6:.4f}MM | {tot[1]/1e3:.1f}K un | shr={tot[2]:.2f}%")
    result[mkt] = {
        'total_abr25_val': round(tot[0]/1e6, 4),
        'total_abr25_un':  round(tot[1]/1e3, 1),
        'brands': {}
    }
    for b in TARGET_BRANDS:
        bd = data[mkt].get(b, [0,0,0])
        val_mm = round(bd[0]/1e6, 4)
        un_k   = round(bd[1]/1e3, 1)
        shr    = round(bd[2], 4) if bd[2] else (round(bd[0]/tot[0]*100, 4) if tot[0] else 0)
        print(f"  {b:22s}: R${val_mm:.4f}MM | {un_k:7.1f}K un | shr={shr:.4f}%")
        result[mkt]['brands'][b] = {'abr25_val': val_mm, 'abr25_un': un_k, 'abr25_shr': shr}

# Verificação: soma das brands vs total
for mkt in ['Farma Sul', 'T.BR Farma']:
    soma = sum(result[mkt]['brands'][b]['abr25_val'] for b in TARGET_BRANDS)
    tot  = result[mkt]['total_abr25_val']
    print(f"\n{mkt} — Soma brands: {soma:.4f}MM | Total: {tot:.4f}MM | diff: {abs(soma-tot):.4f}MM")

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'abr25_data.json')
with open(out, 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=2)
print(f"\nJSON: {out}")
