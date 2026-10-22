"""
extract_shr_trend_fy26.py
Extrai os shares mensais FY26 (Jul/25–Mar/26) por mercado × marca
a partir da 1-Tabela-1 (col 8 = $ Shr - Product, brand-level rows).
Gera shr_trend_fy26.json pronto para injetar no dashboard.
"""
import openpyxl, os, json, datetime
from collections import defaultdict

BASE = r"C:\Users\valqu\OneDrive\Documentos\Claude\Projects\projeto Dashboard_farma_sul"
XLSX = os.path.join(BASE, "base_temp_copy.xlsx")
SHEET = "1-Tabela-1"

BRANDS = ['OFF!', 'EXPOSIS', 'XO INSETO', 'SUPER REPELEX', 'SBP']

# FY26 = Jul/25–Jun/26 (fiscal year começa em Julho)
# índice 0=Jul, 1=Ago, 2=Set, 3=Out, 4=Nov, 5=Dez, 6=Jan, 7=Fev, 8=Mar, 9=Abr, 10=Mai, 11=Jun
def get_fy26_index(dt):
    """Retorna o índice FY (0=Jul, ..., 11=Jun) para um datetime do FY26 (Jul/25–Jun/26)."""
    if not isinstance(dt, datetime.datetime):
        return None
    y, m = dt.year, dt.month
    # FY26: Jul/25(7,2025) a Jun/26(6,2026)
    if y == 2025 and m >= 7:
        return m - 7        # Jul=0, Ago=1, ..., Dez=5
    elif y == 2026 and m <= 6:
        return m + 5        # Jan=6, Fev=7, Mar=8, Abr=9, Mai=10, Jun=11
    return None

# Estrutura: data[market][brand][fy26_index] = shr_value
data = defaultdict(lambda: defaultdict(lambda: [None]*12))

print(f"Abrindo {XLSX}...")
wb = openpyxl.load_workbook(XLSX, read_only=True, data_only=True)
ws = wb[SHEET]

rows_processed = 0
rows_matched = 0

for row in ws.iter_rows(min_row=10, values_only=True):
    mkt    = row[0]
    cat    = row[1]
    brand  = row[2]
    prod   = row[3]
    period = row[4]
    shr    = row[8]   # $ Shr - Product

    if not mkt or not brand:
        continue

    # Apenas brand-level (sem produto específico) e categoria Personal Repellent
    if prod is not None:
        continue
    if cat != 'PERSONAL REPELLENT':
        continue
    if brand not in BRANDS:
        continue

    rows_processed += 1

    # Verificar se é um mês do FY26
    idx = get_fy26_index(period)
    if idx is None:
        continue

    if shr is None:
        continue

    data[mkt][brand][idx] = round(float(shr), 2)
    rows_matched += 1

wb.close()

print(f"Linhas brand-level processadas: {rows_processed}")
print(f"Valores FY26 extraídos: {rows_matched}")
print(f"Mercados com dados: {len(data)}")

# Resumo de mercados
print("\n=== MERCADOS EXTRAÍDOS ===")
for mkt in sorted(data.keys()):
    brands_found = list(data[mkt].keys())
    # Contar índices não-nulos
    counts = {br: sum(1 for v in data[mkt][br] if v is not None) for br in brands_found}
    print(f"  {mkt}: {counts}")

# Salvar JSON
out = {}
for mkt in data:
    out[mkt] = {}
    for brand in BRANDS:
        arr = data[mkt][brand]
        # Índices 9, 10, 11 ainda são null (Abr/Mai/Jun não disponíveis)
        # Garantir que índices 9-11 são sempre None
        arr[9] = None
        arr[10] = None
        arr[11] = None
        out[mkt][brand] = arr

out_path = os.path.join(BASE, "shr_trend_fy26.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=2)

print(f"\nSalvo em: {out_path}")

# Verificação: Farma Sul
print("\n=== VERIFICAÇÃO: Farma Sul ===")
fs = out.get('Farma Sul', {})
for br in BRANDS:
    print(f"  {br}: {fs.get(br, 'AUSENTE')}")
