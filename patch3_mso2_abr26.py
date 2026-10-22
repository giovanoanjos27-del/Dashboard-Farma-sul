"""
patch3_mso2_abr26.py
Ultimas correcoes visiveis: mktChartTitle, labels chart, export Excel
"""
import os, shutil, datetime

BASE = r"C:\Users\valqu\OneDrive\Documentos\Claude\Projects\projeto Dashboard_farma_sul\Dashboard_farma_sul"
SRC  = os.path.join(BASE, "Dashboard_Farma_Sul_20260512_2220.html")

with open(SRC, 'r', encoding='utf-8') as f:
    html = f.read()

original_len = len(html)
patches_applied = 0

def patch(old, new, desc):
    global html, patches_applied
    count = html.count(old)
    if count == 0:
        print(f"  [X] NAO ENCONTRADO: {desc}")
        return False
    if count > 1:
        print(f"  [!] MULTIPLOS ({count}x): {desc} — aplicando todos")
    html = html.replace(old, new)
    patches_applied += count
    print(f"  [OK] ({count}x) {desc}")
    return True

print("=== PATCH 3: Ultimas correcoes visiveis MSO2 ===\n")

# 1. mktChartTitle TOTAL MERCADO (linha 14573)
patch(
    "'TOTAL MERCADO &middot; ACUM JAN&ndash;MAR &middot; '+mktUnit;",
    "'TOTAL MERCADO &middot; ACUM JAN&ndash;ABR &middot; '+mktUnit;",
    "mktChartTitle ACUM JAN-MAR → JAN-ABR"
)

# 2. Labels do grafico TOTAL MERCADO (linha 14590)
patch(
    "labels: ['JAN–MAR / 25', 'JAN–MAR / 26'],",
    "labels: ['JAN–ABR / 25', 'JAN–ABR / 26'],",
    "Labels chart mercado JAN-MAR → JAN-ABR"
)

# 3. Export Excel: header titulo (linha 33310)
patch(
    "'NIELSEN PERFORMANCE — JAN \xb7 FEV \xb7 MAR — '+_jmLbl",
    "'NIELSEN PERFORMANCE — JAN \xb7 FEV \xb7 MAR \xb7 ABR — '+_jmLbl",
    "Export Excel titulo JAN-FEV-MAR → JAN-FEV-MAR-ABR"
)

# 4. Export Excel: subtitulo (linha 33318)
patch(
    "'Acumulado Jan–Mar \xb7 '+_jmLbl",
    "'Acumulado Jan–Abr \xb7 '+_jmLbl",
    "Export Excel subtitulo Jan-Mar → Jan-Abr"
)

print(f"\n=== RESUMO ===")
print(f"Patches aplicados: {patches_applied}")
print(f"Tamanho original: {original_len:,} chars")
print(f"Tamanho final:    {len(html):,} chars")
print(f"Diferenca:        {len(html)-original_len:+,} chars")

with open(SRC, 'w', encoding='utf-8') as f:
    f.write(html)
print(f"\nSalvo em: {SRC}")

VER = os.path.join(BASE, "versoes", f"Dashboard_Farma_Sul_{datetime.datetime.now().strftime('%Y%m%d_%H%M')}_MSO2Abr26_final3.html")
shutil.copy2(SRC, VER)
print(f"Versao final: {VER}")
