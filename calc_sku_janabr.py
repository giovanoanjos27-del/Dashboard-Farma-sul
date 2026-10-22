"""
Calcula share Jan-Abr/25 e Jan-Abr/26 por SKU usando:
  - janmar25/janmar26 já existentes no HTML (Jan-Mar, sabidamente corretos)
  - share de Abril extraído do Excel (mês isolado, filtrado por date exata)
  - totais de mercado do FYTD_MARKET_TOTAL (já confirmados corretos)

Fórmula acumulada correta:
  sku_janabr26_$ = (janmar26_share/100 * janmar26_total) + (abr26_share/100 * abr26_total)
  share_janabr26 = sku_janabr26_$ / (janmar26_total + abr26_total) * 100
"""
import sys, re, shutil, tempfile
sys.stdout.reconfigure(encoding='utf-8')

HTML = r"C:\Users\valqu\OneDrive\Documentos\Claude\Projects\projeto Dashboard_farma_sul\Dashboard_farma_sul\Dashboard_Farma_Sul_20260512_2220.html"
XLS  = r"C:\Users\valqu\OneDrive\Documentos\Claude\Projects\projeto Dashboard_farma_sul\Dashboard_farma_sul\_Recursos\Giovano SCJ\Base Giovano (25-05).xlsx"

# ── 1. LER SKU_MKT_MONTHLY do HTML ────────────────────────────────────────────
with open(HTML, 'r', encoding='utf-8') as f:
    html = f.read()

pos = html.find('SKU_MKT_MONTHLY')
print(f"SKU_MKT_MONTHLY @ {pos}")
# Read block T.BR Farma
for mkt in ['T.BR Farma', 'Farma Sul']:
    p = html.find(f'"{mkt}"', pos)
    if p == -1:
        p = html.find(f"'{mkt}'", pos)
    end = html.find('}', html.find('}', html.find('}', p) + 1) + 1) + 1
    block = html[p:p+1200]
    print(f"\n=== {mkt} (raw) ===")
    print(block[:800])

# ── 2. LER FYTD_MARKET_TOTAL para totais de mercado ──────────────────────────
def get_fytd_field(market, field):
    pos_fyt = html.find('const FYTD_MARKET_TOTAL')
    p = html.find(f"'{market}':", pos_fyt)
    m = re.search(field + r':([\d.]+)', html[p:p+600])
    return float(m.group(1)) if m else None

for mkt in ['T.BR Farma', 'Farma Sul']:
    jm26 = get_fytd_field(mkt, 'janmar26_val')
    ab26 = get_fytd_field(mkt, 'abr26_val')
    jm25 = get_fytd_field(mkt, 'janmar25_val')
    ab25 = get_fytd_field(mkt, 'abr25_val')
    print(f"\nFYTD_MARKET_TOTAL {mkt}:")
    print(f"  janmar26={jm26}, abr26={ab26}, total26={round(jm26+ab26,4) if jm26 and ab26 else '?'}")
    print(f"  janmar25={jm25}, abr25={ab25}, total25={round(jm25+ab25,4) if jm25 and ab25 else '?'}")

# ── 3. LER ABRIL por SKU do Excel (data exata, filtro por mkt+categoria) ──────
print("\n=== Lendo Excel para shares de ABRIL ===")
try:
    tmp = tempfile.mktemp(suffix='.xlsx')
    shutil.copy2(XLS, tmp)
    from openpyxl import load_workbook
    wb = load_workbook(tmp, read_only=True, data_only=True)
    ws = wb['1-Tabela-1']

    from datetime import datetime
    DATE_ABR26 = datetime(2026, 4, 22)
    DATE_ABR25 = datetime(2025, 4, 22)

    # Coletar: market, products, date, $ valor
    abr_data = {}  # {(mkt, products, year): $}
    for row in ws.iter_rows(min_row=2, values_only=True):
        mkt_v = row[0]
        cat   = row[1]
        brand = row[2]
        prod  = row[3]
        date  = row[4]
        val   = row[12]  # $

        if mkt_v not in ('T.BR Farma', 'Farma Sul'):
            continue
        if cat != 'PERSONAL REPELLENT':
            continue
        if date not in (DATE_ABR26, DATE_ABR25):
            continue
        if val is None:
            continue
        year = date.year
        # key: use Products if not None, else BRAND
        key_prod = prod if prod else brand
        if key_prod is None:
            key_prod = '__TOTAL__'
        abr_data[(mkt_v, key_prod, year)] = abr_data.get((mkt_v, key_prod, year), 0) + float(val)

    wb.close()

    # Computar share de Abril por SKU
    # Total mercado = linha __TOTAL__ ou soma de todos excluindo duplicatas
    # Usamos FYTD_MARKET_TOTAL abr_val como total mais confiável
    print("\nDados brutos ABRIL por mercado/SKU (top 20 por valor):")
    for mkt_v in ['T.BR Farma', 'Farma Sul']:
        print(f"\n  {mkt_v} — ABR/26:")
        items_26 = [(k[1], v) for k,v in abr_data.items() if k[0]==mkt_v and k[2]==2026]
        items_26.sort(key=lambda x: -x[1])
        for name, val in items_26[:20]:
            print(f"    {name}: R${val/1e6:.4f}MM")
        print(f"  {mkt_v} — ABR/25:")
        items_25 = [(k[1], v) for k,v in abr_data.items() if k[0]==mkt_v and k[2]==2025]
        items_25.sort(key=lambda x: -x[1])
        for name, val in items_25[:20]:
            print(f"    {name}: R${val/1e6:.4f}MM")

except Exception as e:
    print(f"Erro Excel: {e}")
    import traceback; traceback.print_exc()
