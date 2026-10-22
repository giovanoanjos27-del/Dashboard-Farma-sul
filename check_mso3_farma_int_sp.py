import sys, io, json, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

with open('janmar_market_totals.json', encoding='utf-8') as f:
    totals = json.load(f)

mkt = 'Farma Moderno Int SP'
d = totals.get(mkt, {})
print(f'=== {mkt} — Jan-Mar (3 meses) ===')
print(f'  Jan-Mar/25 Total Mkt: R${d["janmar25_val"]:.3f}MM')
print(f'  Jan-Mar/26 Total Mkt: R${d["janmar26_val"]:.3f}MM')
pct = (d["janmar26_val"]/d["janmar25_val"]-1)*100 if d["janmar25_val"] else 0
print(f'  Delta JanMar:         {pct:.1f}%')
print()

# Verificar FYTD no HTML
with open(r'Dashboard_farma_sul\Dashboard_Farma_Sul_20260512_2220.html', encoding='utf-8') as f:
    html = f.read()

escaped = re.escape(mkt)
pat = rf"'{escaped}': \{{([^}}]*)\}}"
m = re.search(pat, html)
if m:
    content = m.group(1)
    v25 = re.search(r'fytd25_val:([\d.]+)', content)
    v26 = re.search(r'fytd26_val:([\d.]+)', content)
    u25 = re.search(r'fytd25_un:([\d.]+)', content)
    u26 = re.search(r'fytd26_un:([\d.]+)', content)
    fv25 = float(v25.group(1)) if v25 else 0
    fv26 = float(v26.group(1)) if v26 else 0
    pct_fytd = (fv26/fv25-1)*100 if fv25 else 0
    print('FYTD no HTML (FYTD_MARKET_TOTAL):')
    print(f'  fytd25_val: R${fv25:.3f}MM  (dashboard mostra R$172.93MM)')
    print(f'  fytd26_val: R${fv26:.3f}MM  (dashboard mostra R$117.84MM)')
    print(f'  Delta FYTD: {pct_fytd:.1f}%  (dashboard mostra -31.9%)')
    print(f'  fytd25_un:  {u25.group(1) if u25 else "?"}k')
    print(f'  fytd26_un:  {u26.group(1) if u26 else "?"}k')
else:
    print('Nao encontrado no HTML')

# Verificar as SCJ brands (o que renderMSO3 usa para TOTAL ACUM)
nbv_pat = rf"NIELSEN_BRAND_VAL\['{re.escape(mkt)}'\]"
idx_nbv = html.find(f"'{mkt}': {{")
# Encontrar dentro do NIELSEN_BRAND_VAL
idx_start = html.find('NIELSEN_BRAND_VAL = {')
idx_end = html.find('var FYTD_MARKET_TOTAL', idx_start)
chunk = html[idx_start:idx_end]
idx_mkt = chunk.find(f"'{mkt}':")
if idx_mkt >= 0:
    mkt_chunk = chunk[idx_mkt:idx_mkt+800]
    print()
    print('NIELSEN_BRAND_VAL para', mkt, '(primeiros 500 chars):')
    # Extrair fytd26_val por brand
    for brand in ["OFF!", "EXPOSIS", "XO INSETO", "SUPER REPELEX", "SBP"]:
        br = re.escape(brand)
        b_pat = rf"'{br}': \{{([^}}]*)\}}"
        bm = re.search(b_pat, mkt_chunk)
        if bm:
            bc = bm.group(1)
            fv26b = re.search(r'fytd26_val:([\d.]+)', bc)
            fv25b = re.search(r'fytd25_val:([\d.]+)', bc)
            v26b = float(fv26b.group(1)) if fv26b else 0
            v25b = float(fv25b.group(1)) if fv25b else 0
            print(f'  {brand:<20} FYTD25: R${v25b:.3f}MM  FYTD26: R${v26b:.3f}MM')
