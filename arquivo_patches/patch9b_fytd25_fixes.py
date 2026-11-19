"""
patch9b_fytd25_fixes.py
Corrige os 3 problemas residuais do patch9:
  1. XO INSETO fytd25_val:26.6436 no mercado errado → reverter para 24.0848
  2. SBP fytd25_un:104.443 no mercado errado → reverter para 93.843
  3. Farma Sul XO INSETO fytd25_val:24.0848 → 26.6436 (não foi atualizado)
  4. Farma Sul SBP fytd25_un:93.843 → 104.443 (não foi atualizado)
  5. Label Excel "JUL–MAR" → "JUL–ABR" (escape \xb7 literal)
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
        print(f"  [!] {c}x: {desc}")
    html = html.replace(old, new, 1)
    patches += 1
    print(f"  [OK] {desc}")
    return True

print("=== PATCH 9b: correções pós-patch9 ===\n")

# 1. Reverter XO INSETO no mercado errado (fytd26_val:25.342975 não é Farma Sul)
patch(
    "'XO INSETO': {fytd25_val:26.6436,fytd26_val:25.342975,fytd25_un:1086.96,",
    "'XO INSETO': {fytd25_val:24.0848,fytd26_val:25.342975,fytd25_un:1086.96,",
    "Reverter XO INSETO mercado errado (fytd26_val:25.342975)"
)

# 2. Reverter SBP fytd25_un no mercado errado (fytd25_val:3.421218 não é Farma Sul que tem 3.8219)
patch(
    "'SBP': {fytd25_val:3.421218,fytd26_val:2.849149,fytd25_un:104.443,fytd26_un:72.775}",
    "'SBP': {fytd25_val:3.421218,fytd26_val:2.849149,fytd25_un:93.843,fytd26_un:72.775}",
    "Reverter SBP fytd25_un mercado errado (fytd25_val:3.421218)"
)

# 3. Farma Sul XO INSETO: agora tem fytd26_val:28.166 e fytd25_un:1186.5599 (correto)
patch(
    "'XO INSETO': {fytd25_val:24.0848,fytd26_val:28.166,fytd25_un:1186.5599,",
    "'XO INSETO': {fytd25_val:26.6436,fytd26_val:28.166,fytd25_un:1186.5599,",
    "Farma Sul XO INSETO fytd25_val:24.0848→26.6436"
)

# 4. Farma Sul SBP: fytd25_val:3.8219 (já correto), fytd25_un:93.843 → 104.443
# fytd26_val:3.1056 e fytd26_un:72.7749 são específicos de Farma Sul
patch(
    "fytd25_val:3.8219,fytd26_val:3.1056,fytd25_un:93.843,fytd26_un:72.7749",
    "fytd25_val:3.8219,fytd26_val:3.1056,fytd25_un:104.443,fytd26_un:72.7749",
    "Farma Sul SBP fytd25_un:93.843→104.443"
)

# 5. Label Excel JUL–MAR → JUL–ABR (string tem \xb7 literal, não middot real)
# O repr mostrou: UNIDADES FYTD JUL–MAR \xb7
# Buscar com a sequência exata
xls_old = 'UNIDADES FYTD JUL–MAR \\xb7 FY25 vs FY26 \\xb7'
xls_new = 'UNIDADES FYTD JUL–ABR \\xb7 FY25 vs FY26 \\xb7'
c5 = html.count(xls_old)
print(f"\nExcel label occurrences: {c5}")
if c5 > 0:
    html = html.replace(xls_old, xls_new)
    patches += c5
    print(f"  [OK] Label Excel JUL–MAR→JUL–ABR")
else:
    # Try ASCII en-dash
    xls_old2 = 'UNIDADES FYTD JUL–MAR'
    c6 = html.count(xls_old2)
    print(f"  fallback search count: {c6}")
    if c6 > 0:
        html = html.replace(xls_old2, 'UNIDADES FYTD JUL–ABR')
        patches += c6
        print(f"  [OK] Label Excel JUL–MAR→JUL–ABR (fallback)")
    else:
        print(f"  [X] Label Excel: ainda nao encontrado")

print(f"\n=== RESUMO ===")
print(f"Patches: {patches}")
print(f"Original: {original_len:,} | Final: {len(html):,} | Diff: {len(html)-original_len:+,}")

with open(SRC, 'w', encoding='utf-8') as f:
    f.write(html)
print(f"\nSalvo: {SRC}")

VER = os.path.join(BASE, "versoes", f"Dashboard_Farma_Sul_{datetime.datetime.now().strftime('%Y%m%d_%H%M')}_FYTD25Fix_final.html")
shutil.copy2(SRC, VER)
print(f"Versão: {VER}")
