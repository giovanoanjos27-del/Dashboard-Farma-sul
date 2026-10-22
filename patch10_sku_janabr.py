"""
patch10_sku_janabr.py
Atualiza o card MARKET SHARE POR SKU de Jan-Mar para Jan-Abr.

Metodologia (correta):
  sku_janabr26_$ = (janmar26[i]/100 * janmar26_total) + (abr26_share[i]/100 * abr26_total)
  share_janabr26 = sku_janabr26_$ / (janmar26_total + abr26_total) * 100

Totais de mercado (FYTD_MARKET_TOTAL, já confirmados):
  T.BR Farma: janmar26=217.0031, abr26=59.0468, total26=276.0499
              janmar25=269.2395, abr25=63.1763, total25=332.4158
  Farma Sul:  janmar26=52.8906,  abr26=11.3150, total26=64.2056
              janmar25=56.7043,  abr25=11.9606, total25=68.6649

Shares de Abril por SKU extraídos de Base Giovano (25-05).xlsx (filtro:
  Markets='T.BR Farma'/'Farma Sul', CATEGORY='PERSONAL REPELLENT',
  Data=2026-04-22 / 2025-04-22, denominador = total de mercado do mesmo
  mercado/categoria/data confirmado via FYTD_MARKET_TOTAL.abr_val.
"""
import os, shutil, datetime, sys
sys.stdout.reconfigure(encoding='utf-8')

BASE = r"C:\Users\valqu\OneDrive\Documentos\Claude\Projects\projeto Dashboard_farma_sul\Dashboard_farma_sul"
SRC  = os.path.join(BASE, "Dashboard_Farma_Sul_20260512_2220.html")

with open(SRC, 'r', encoding='utf-8') as f:
    html = f.read()

original_len = len(html)
patches = 0

def patch(old, new, desc):
    global html, patches
    c = html.count(old)
    if c == 0:
        print(f"  [X] NAO ENCONTRADO: {desc}")
        return False
    if c > 1:
        print(f"  [!] {c}x (substituindo 1): {desc}")
    html = html.replace(old, new, 1)
    patches += 1
    print(f"  [OK] {desc}")
    return True

def patch_all(old, new, desc):
    global html, patches
    c = html.count(old)
    if c == 0:
        print(f"  [X] NAO ENCONTRADO: {desc}")
        return 0
    html = html.replace(old, new)
    patches += c
    print(f"  [OK] ({c}x) {desc}")
    return c

print("=== PATCH 10: SKU card Jan-Mar → Jan-Abr ===\n")

# ══════════════════════════════════════════════════════════════════════
# 1. DADOS SKU_MKT_MONTHLY — T.BR Farma
# ══════════════════════════════════════════════════════════════════════
print("--- SKU_MKT_MONTHLY T.BR Farma ---")

# Arrays calculados (fórmula weighted $ acumulado):
# SKU order: ALL OTHERS CAMP, OFF! Family, Exposis Infantil, Xô Spray 200ml,
#            Xô Loção 200ml, OFF! Family Loção 200ml PR, OFF! Kids,
#            All Others Loção, OFF! Baby, OFF! Family Spray 170ml PR

patch(
    '"janmar25":[20.27,14.46,15.09,9.72,7.92,6.79,6.14,6.75,3.28,3.11],'
    '"janmar26":[18.4,15.8,13.16,10.58,8.05,7.33,6.22,5.62,4.39,3.95],'
    '"var":[-1.87,1.34,-1.93,0.86,0.13,0.54,0.08,-1.13,1.12,0.84]}',
    '"janmar25":[20.10,14.50,15.24,9.56,7.94,6.89,6.18,6.69,3.31,3.02],'
    '"janmar26":[17.97,15.84,13.34,10.59,8.21,7.45,6.31,5.49,4.53,3.93],'
    '"var":[-2.13,1.34,-1.90,1.03,0.27,0.56,0.13,-1.20,1.22,0.91]}',
    "T.BR Farma janmar arrays → janaabr"
)

# ══════════════════════════════════════════════════════════════════════
# 2. DADOS SKU_MKT_MONTHLY — Farma Sul
# ══════════════════════════════════════════════════════════════════════
print("\n--- SKU_MKT_MONTHLY Farma Sul ---")

# SKU order: ALL OTHERS CAMP, OFF! Family, Xô Spray 200ml, All Others Aero,
#            Exposis Infantil, All Others Loção, Xô Loção 200ml,
#            OFF! Family Loção 200ml PR, OFF! Family Spray 170ml PR, OFF! Kids

patch(
    '"janmar25":[31.45,14.07,10.78,11.09,9.22,10.95,5.73,5.59,4.12,6.05],'
    '"janmar26":[29.07,15.04,12.43,12.06,8.24,8.07,5.98,5.75,5.19,4.97],'
    '"var":[-2.38,0.97,1.65,0.97,-0.97,-2.88,0.25,0.16,1.07,-1.08]}',
    '"janmar25":[30.98,13.99,10.55,10.76,9.75,10.78,5.75,5.56,4.07,6.04],'
    '"janmar26":[28.77,15.04,12.24,11.63,8.57,8.00,5.95,5.65,5.14,4.97],'
    '"var":[-2.21,1.05,1.69,0.87,-1.18,-2.78,0.20,0.09,1.07,-1.07]}',
    "Farma Sul janmar arrays → janaabr"
)

# ══════════════════════════════════════════════════════════════════════
# 3. LABELS — Card título, subtítulos, gráficos, diagnóstico
# ══════════════════════════════════════════════════════════════════════
print("\n--- Labels Jan-Mar → Jan-Abr ---")

# Card title (HTML/JS estático ou gerado por renderMSOSkuJanMar)
patch_all('JAN-FEV-MAR’', 'JAN-FEV-MAR-ABR’', "Card title JAN-FEV-MAR'")  # unicode apóstrofo
patch_all('JAN-FEV-MAR&#8217;', 'JAN-FEV-MAR-ABR&#8217;', "Card title JAN-FEV-MAR html entity")
patch_all('MARKET SHARE POR SKU — JAN-FEV-MAR', 'MARKET SHARE POR SKU — JAN-FEV-MAR-ABR', "Card title em dash")
patch_all("'MARKET SHARE POR SKU — JAN-FEV-MAR'", "'MARKET SHARE POR SKU — JAN-FEV-MAR-ABR'", "Card title quoted")

# Subtitle h2
patch_all('$ Share por SKU \xb7 Jan-Mar/26 vs Jan-Mar/25', '$ Share por SKU \xb7 Jan-Abr/26 vs Jan-Abr/25', "h2 subtitle Jan-Mar")
patch_all('Jan-Mar/26 vs Jan-Mar/25', 'Jan-Abr/26 vs Jan-Abr/25', "Jan-Mar vs label")
patch_all('Jan-Mar/26', 'Jan-Abr/26', "Jan-Mar/26 label")
patch_all('Jan-Mar/25', 'Jan-Abr/25', "Jan-Mar/25 label")
patch_all('Jan-Mar', 'Jan-Abr', "Generic Jan-Mar label")

# Chart labels internos
patch_all('MARKET SHARE SKU — Jan-Abr/26', 'MARKET SHARE SKU — Jan-Abr/26', "noop chart label (already updated)")  # skip if already done
patch_all("'MARKET SHARE SKU \\u2014 Jan-Abr/26'", "'MARKET SHARE SKU \\u2014 Jan-Abr/26'", "noop")

# Diagnóstico
patch_all('DIAGNÓSTICO SKU JAN-MAR', 'DIAGNÓSTICO SKU JAN-ABR', "Diagnóstico header JAN-MAR")
patch_all('DIAGN\xd3STICO SKU JAN-MAR', 'DIAGN\xd3STICO SKU JAN-ABR', "Diagnóstico header latin1")

# renderMSOSkuJanMar subtitle/labels
patch_all("Jan·Abr/26 vs Jan·Abr/25", "Jan·Abr/26 vs Jan·Abr/25", "noop já correto")
patch_all("Jan·Mar/26 vs Jan·Mar/25", "Jan·Abr/26 vs Jan·Abr/25", "subtitle Jan·Mar → Jan·Abr")
patch_all("Jan·Mar/26", "Jan·Abr/26", "Jan·Mar/26 label")
patch_all("Jan·Mar/25", "Jan·Abr/25", "Jan·Mar/25 label")

# Botão Exportar (se houver referência JAN-MAR no botão do card SKU)
patch_all('Jan-Mar SKU', 'Jan-Abr SKU', "Export btn Jan-Mar SKU")
patch_all('JAN-MAR SKU', 'JAN-ABR SKU', "Export header JAN-MAR SKU")

print(f"\n=== RESUMO ===")
print(f"Patches: {patches}")
print(f"Original: {original_len:,} | Final: {len(html):,} | Diff: {len(html)-original_len:+,}")

with open(SRC, 'w', encoding='utf-8') as f:
    f.write(html)
print(f"\nSalvo: {SRC}")

VER = os.path.join(BASE, "versoes", f"Dashboard_Farma_Sul_{datetime.datetime.now().strftime('%Y%m%d_%H%M')}_SKUJanAbr.html")
shutil.copy2(SRC, VER)
print(f"Versão: {VER}")
