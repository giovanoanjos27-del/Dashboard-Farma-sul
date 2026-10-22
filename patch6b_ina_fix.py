"""
patch6b_ina_fix.py
Correções nos 3 casos INA que o patch6 nao conseguiu:
  1. INA MG / EXPOSIS monthly    — array com nulls internos, adiciona Abr/26
  2. INA Int MG / EXPOSIS monthly — idem
  3. INA MG+ES+Int RJ            — market fora do limite de busca MSO, 6 marcas
"""
import os, shutil, datetime, re

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
    html = html.replace(old, new)
    patches += c
    print(f"  [OK] ({c}x) {desc}")
    return True

print("=== PATCH 6b: INA edge cases ===\n")

# ── 1. INA MG / EXPOSIS monthly (null,null,...,null → append 0.22) ──────────
# monthly:[null,null,null,null,null,0.17,null,0.19,null]
patch(
    "'INA MG': {\n    'OFF!': {fytd25:50.37",
    "'INA MG': {\n    'OFF!': {fytd25:50.37",
    "INA MG sanity check"
)

# Localizar exatamente e substituir monthly de EXPOSIS em INA MG
# Busca: dentro do bloco INA MG em MKTSHARE_OVERVIEW
mso_start = html.find('const MKTSHARE_OVERVIEW')
pos_ina_mg = html.find("'INA MG': {", mso_start)
end_ina_mg = html.find("\n  '", pos_ina_mg + 10)
sec = html[pos_ina_mg:end_ina_mg]

# INA MG / EXPOSIS monthly: 9 valores com nulls internos
old_exposis_ina_mg = re.search(r"('EXPOSIS': \{[^}]*?monthly:\[)([^\]]+)(\])", sec)
if old_exposis_ina_mg:
    full_match = old_exposis_ina_mg.group(0)
    prefix = old_exposis_ina_mg.group(1)
    vals = old_exposis_ina_mg.group(2)
    suffix = old_exposis_ina_mg.group(3)
    parts = vals.split(',')
    if len(parts) == 9:
        new_vals = vals + ',0.22'
        new_match = prefix + new_vals + suffix
        sec_new = sec[:old_exposis_ina_mg.start()] + new_match + sec[old_exposis_ina_mg.end():]
        html = html[:pos_ina_mg] + sec_new + html[end_ina_mg:]
        patches += 1
        print(f"  [OK] INA MG / EXPOSIS monthly: {parts} + 0.22")
    else:
        print(f"  [X] INA MG / EXPOSIS monthly: {len(parts)} vals")
else:
    print(f"  [X] INA MG / EXPOSIS monthly: nao encontrado")

# ── 2. INA Int MG / EXPOSIS monthly ─────────────────────────────────────────
pos_ina_intmg = html.find("'INA Int MG': {", mso_start)
end_ina_intmg = html.find("\n  '", pos_ina_intmg + 10)
sec2 = html[pos_ina_intmg:end_ina_intmg]

old_e2 = re.search(r"('EXPOSIS': \{[^}]*?monthly:\[)([^\]]+)(\])", sec2)
if old_e2:
    prefix2 = old_e2.group(1)
    vals2 = old_e2.group(2)
    suffix2 = old_e2.group(3)
    parts2 = vals2.split(',')
    if len(parts2) == 9:
        new_vals2 = vals2 + ',0.29'
        new_match2 = prefix2 + new_vals2 + suffix2
        sec2_new = sec2[:old_e2.start()] + new_match2 + sec2[old_e2.end():]
        html = html[:pos_ina_intmg] + sec2_new + html[end_ina_intmg:]
        patches += 1
        print(f"  [OK] INA Int MG / EXPOSIS monthly: {parts2} + 0.29")
    else:
        print(f"  [X] INA Int MG / EXPOSIS monthly: {len(parts2)} vals")
else:
    print(f"  [X] INA Int MG / EXPOSIS monthly: nao encontrado")

# ── 3. INA MG+ES+Int RJ — todas as 6 marcas monthly[9] ─────────────────────
# O market esta apos o mso_end anterior. Busca sem limite.
APR26_INA_MG_ES = {
    'OFF!': 55.15, 'EXPOSIS': 0.20, 'XO INSETO': 9.66,
    'SUPER REPELEX': 17.33, 'SBP': 2.37, 'ALL OTHERS CAMP': 15.29
}
BRANDS_ALL = ['OFF!', 'EXPOSIS', 'XO INSETO', 'SUPER REPELEX', 'SBP', 'ALL OTHERS CAMP']

pos3 = html.find("'INA MG+ES+Int RJ': {", mso_start)
end3 = html.find("\n  '", pos3 + 10)
sec3 = html[pos3:end3]

ok3 = 0
for brand in BRANDS_ALL:
    apr_val = APR26_INA_MG_ES[brand]
    brand_tag = f"'{brand}':"
    b_pos = sec3.find(brand_tag)
    if b_pos == -1:
        print(f"  [X] INA MG+ES+Int RJ / {brand}: nao encontrado")
        continue
    field_tag = 'monthly:['
    f_pos = sec3.find(field_tag, b_pos)
    if f_pos == -1:
        print(f"  [X] INA MG+ES+Int RJ / {brand}: monthly nao encontrado")
        continue
    arr_end = sec3.index(']', f_pos) + 1
    arr_str = sec3[f_pos:arr_end]
    values_str = arr_str[len(field_tag):-1]
    parts3 = values_str.split(',')
    if len(parts3) != 9:
        print(f"  [X] INA MG+ES+Int RJ / {brand}: {len(parts3)} vals")
        continue
    new_arr = f'monthly:[{values_str},{apr_val}]'
    sec3 = sec3[:f_pos] + new_arr + sec3[arr_end:]
    ok3 += 1
    patches += 1

html = html[:pos3] + sec3 + html[end3:]
print(f"  [OK] INA MG+ES+Int RJ: {ok3}/6 marcas MSO monthly")

# ── RESUMO ───────────────────────────────────────────────────────────────────
print(f"\n=== RESUMO ===")
print(f"Patches: {patches}")
print(f"Original: {original_len:,} | Final: {len(html):,} | Diff: {len(html)-original_len:+,}")

with open(SRC, 'w', encoding='utf-8') as f:
    f.write(html)
print(f"Salvo: {SRC}")

VER = os.path.join(BASE, "versoes", f"Dashboard_Farma_Sul_{datetime.datetime.now().strftime('%Y%m%d_%H%M')}_AllMkts72_Abr26_final.html")
shutil.copy2(SRC, VER)
print(f"Versao final: {VER}")
