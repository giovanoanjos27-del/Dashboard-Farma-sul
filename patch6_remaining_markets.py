"""
patch6_remaining_markets.py
Insere ABR/26 nos 29 markets que ainda estavam com fy26[9]=null.
Atualiza:
  1. MKTSHARE_OVERVIEW  — monthly[9] (share ABR/26)
  2. SHR_TREND_DATA     — fy26[9]    (share ABR/26)
Fonte: Base Giovano (25-05).xlsx — coluna col8 ($ Shr - Product) ja em %
"""
import os, shutil, datetime, re

BASE = r"C:\Users\valqu\OneDrive\Documentos\Claude\Projects\projeto Dashboard_farma_sul\Dashboard_farma_sul"
SRC  = os.path.join(BASE, "Dashboard_Farma_Sul_20260512_2220.html")

APR26 = {
  'INFC Cidade Gde MG+ES+Int RJ': {'OFF!':31.85,'EXPOSIS':24.33,'XO INSETO':21.88,'SUPER REPELEX':5.01,'SBP':5.23,'ALL OTHERS CAMP':11.69},
  'INFC Cidade Gde NE':           {'OFF!':36.08,'EXPOSIS':17.02,'XO INSETO':27.43,'SUPER REPELEX':3.79,'SBP':3.90,'ALL OTHERS CAMP':11.78},
  'INFC Cidade Peq+Med CO':       {'OFF!':20.89,'EXPOSIS':18.37,'XO INSETO':24.97,'SUPER REPELEX':8.03,'SBP':3.68,'ALL OTHERS CAMP':24.06},
  'INFC Cidade Peq+Med Int SP':   {'OFF!':29.82,'EXPOSIS':17.21,'XO INSETO':27.43,'SUPER REPELEX':5.21,'SBP':3.94,'ALL OTHERS CAMP':16.40},
  'INFC Cidade Peq+Med MG+ES+Int RJ': {'OFF!':29.53,'EXPOSIS':17.01,'XO INSETO':30.48,'SUPER REPELEX':4.31,'SBP':2.85,'ALL OTHERS CAMP':15.84},
  'INFC Cidade Peq+Med NE':       {'OFF!':36.39,'EXPOSIS':10.08,'XO INSETO':37.67,'SUPER REPELEX':2.56,'SBP':2.39,'ALL OTHERS CAMP':10.92},
  'INFC DF':                      {'OFF!':30.27,'EXPOSIS':26.83,'XO INSETO':12.89,'SUPER REPELEX':6.73,'SBP':3.17,'ALL OTHERS CAMP':20.11},
  'INFC Fortaleza':               {'OFF!':43.41,'EXPOSIS':20.36,'XO INSETO':14.74,'SUPER REPELEX':4.65,'SBP':4.22,'ALL OTHERS CAMP':12.63},
  'INFC GO':                      {'OFF!':25.73,'EXPOSIS':17.65,'XO INSETO':15.07,'SUPER REPELEX':7.96,'SBP':2.60,'ALL OTHERS CAMP':30.99},
  'INFC Gde RJ':                  {'OFF!':43.03,'EXPOSIS':25.47,'XO INSETO':16.68,'SUPER REPELEX':4.55,'SBP':2.96,'ALL OTHERS CAMP':7.31},
  'INFC Gde SP':                  {'OFF!':29.93,'EXPOSIS':29.71,'XO INSETO':17.15,'SUPER REPELEX':6.14,'SBP':4.34,'ALL OTHERS CAMP':12.73},
  'INFC Int BA':                  {'OFF!':35.97,'EXPOSIS':11.03,'XO INSETO':34.34,'SUPER REPELEX':3.02,'SBP':2.92,'ALL OTHERS CAMP':12.72},
  'INFC Int CE':                  {'OFF!':34.79,'EXPOSIS':11.40,'XO INSETO':39.42,'SUPER REPELEX':1.99,'SBP':1.38,'ALL OTHERS CAMP':11.02},
  'INFC Int MG':                  {'OFF!':24.97,'EXPOSIS':19.63,'XO INSETO':31.38,'SUPER REPELEX':3.94,'SBP':2.51,'ALL OTHERS CAMP':17.56},
  'INFC Int PE':                  {'OFF!':38.95,'EXPOSIS':9.90,'XO INSETO':31.51,'SUPER REPELEX':2.62,'SBP':2.56,'ALL OTHERS CAMP':14.46},
  'INFC Int SP':                  {'OFF!':29.82,'EXPOSIS':19.06,'XO INSETO':26.21,'SUPER REPELEX':5.25,'SBP':3.90,'ALL OTHERS CAMP':15.76},
  'INFC MA+PI':                   {'OFF!':36.94,'EXPOSIS':9.62,'XO INSETO':38.14,'SUPER REPELEX':2.93,'SBP':2.41,'ALL OTHERS CAMP':9.96},
  'INFC MG+ES+Int RJ':            {'OFF!':30.01,'EXPOSIS':18.60,'XO INSETO':28.63,'SUPER REPELEX':4.47,'SBP':3.35,'ALL OTHERS CAMP':14.94},
  'INFC Man+Bel+Ana':             {'OFF!':32.19,'EXPOSIS':17.45,'XO INSETO':18.70,'SUPER REPELEX':8.07,'SBP':5.36,'ALL OTHERS CAMP':18.23},
  'INFC Manaus':                  {'OFF!':31.96,'EXPOSIS':27.21,'XO INSETO':16.42,'SUPER REPELEX':5.99,'SBP':4.13,'ALL OTHERS CAMP':14.29},
  'INFC NE':                      {'OFF!':36.28,'EXPOSIS':11.91,'XO INSETO':35.05,'SUPER REPELEX':2.87,'SBP':2.73,'ALL OTHERS CAMP':11.16},
  'INFC PE':                      {'OFF!':43.01,'EXPOSIS':10.57,'XO INSETO':30.06,'SUPER REPELEX':2.74,'SBP':2.63,'ALL OTHERS CAMP':11.00},
  'INFC Recife':                  {'OFF!':47.55,'EXPOSIS':11.31,'XO INSETO':28.43,'SUPER REPELEX':2.88,'SBP':2.72,'ALL OTHERS CAMP':7.11},
  'INFC SP':                      {'OFF!':29.85,'EXPOSIS':22.21,'XO INSETO':23.54,'SUPER REPELEX':5.51,'SBP':4.03,'ALL OTHERS CAMP':14.87},
  'INFC Salvador':                {'OFF!':36.93,'EXPOSIS':17.05,'XO INSETO':27.56,'SUPER REPELEX':3.46,'SBP':4.15,'ALL OTHERS CAMP':10.84},
  'T.BR INFC':                    {'OFF!':31.05,'EXPOSIS':17.38,'XO INSETO':26.77,'SUPER REPELEX':5.03,'SBP':3.18,'ALL OTHERS CAMP':16.58},
  'INA MG':                       {'OFF!':50.37,'EXPOSIS':0.22,'XO INSETO':10.80,'SUPER REPELEX':15.92,'SBP':2.87,'ALL OTHERS CAMP':19.83},
  'INA Int MG':                   {'OFF!':49.18,'EXPOSIS':0.29,'XO INSETO':9.46,'SUPER REPELEX':15.66,'SBP':2.38,'ALL OTHERS CAMP':23.02},
  'INA MG+ES+Int RJ':             {'OFF!':55.15,'EXPOSIS':0.20,'XO INSETO':9.66,'SUPER REPELEX':17.33,'SBP':2.37,'ALL OTHERS CAMP':15.29},
}

BRANDS = ['OFF!', 'EXPOSIS', 'XO INSETO', 'SUPER REPELEX', 'SBP', 'ALL OTHERS CAMP']

with open(SRC, 'r', encoding='utf-8') as f:
    html = f.read()

original_len = len(html)
ok_mso = ok_shr = 0
fail_mso = []
fail_shr = []

# ─── Helper ────────────────────────────────────────────────────────────────
def update_section(html, mkt_name, brands_apr26, search_from, search_to, field, null_suffix):
    """Atualiza monthly[] ou fy26[] dentro do bloco delimitado por search_from/search_to."""
    mkt_tag = f"  '{mkt_name}': {{"
    pos = html.find(mkt_tag, search_from, search_to)
    if pos == -1:
        return html, 0, [f'{mkt_name}: nao encontrado']

    next_pos = html.find("\n  '", pos + len(mkt_tag))
    if next_pos == -1 or next_pos > search_to:
        next_pos = search_to
    section = html[pos:next_pos]
    orig = section
    ok = 0
    fails = []

    for brand in BRANDS:
        if brand not in brands_apr26:
            continue
        apr_val = brands_apr26[brand]
        brand_tag = f"'{brand}':"
        b_pos = section.find(brand_tag)
        if b_pos == -1:
            fails.append(f'{mkt_name}/{brand}: brand nao encontrada')
            continue

        field_tag = f'{field}:['
        f_pos = section.find(field_tag, b_pos)
        if f_pos == -1:
            fails.append(f'{mkt_name}/{brand}: campo {field} nao encontrado')
            continue

        arr_end = section.index(']', f_pos) + 1
        arr_str = section[f_pos:arr_end]
        values_str = arr_str[len(field_tag):-1]

        if null_suffix:
            if not arr_str.endswith(',null,null,null]'):
                fails.append(f'{mkt_name}/{brand}: sufixo inesperado: {arr_str[-20:]}')
                continue
            parts = values_str.split(',')
            if len(parts) != 12:
                fails.append(f'{mkt_name}/{brand}: {len(parts)} vals (exp 12)')
                continue
            if parts[9] != 'null':
                fails.append(f'{mkt_name}/{brand}: fy26[9] ja={parts[9]}, skip')
                continue
            parts[9] = str(apr_val)
            new_arr = f'{field}:[{",".join(parts)}]'
        else:
            if 'null' in values_str:
                fails.append(f'{mkt_name}/{brand}: monthly ja tem null, skip')
                continue
            parts = values_str.split(',')
            if len(parts) != 9:
                fails.append(f'{mkt_name}/{brand}: {len(parts)} vals (exp 9)')
                continue
            new_arr = f'{field}:[{values_str},{apr_val}]'

        section = section[:f_pos] + new_arr + section[arr_end:]
        ok += 1

    html = html[:pos] + section + html[pos + len(orig):]
    return html, ok, fails

# ─── Localizar blocos ───────────────────────────────────────────────────────
mso_start = html.find('const MKTSHARE_OVERVIEW')
mso_end   = html.find('\nconst ', mso_start + 100)
shr_start = html.find('SHR_TREND_DATA =')
shr_end   = html.find('\nconst ', shr_start + 100)

print("=== PATCH 6: 29 markets restantes ===\n")
print(f"MSO bloco: {mso_start}–{mso_end}")
print(f"SHR bloco: {shr_start}–{shr_end}")
print()

for mkt_name, brands_apr26 in APR26.items():
    # 1. MKTSHARE_OVERVIEW monthly[9]
    html, n1, f1 = update_section(html, mkt_name, brands_apr26, mso_start, mso_end, 'monthly', '')
    ok_mso += n1
    if f1: fail_mso.extend(f1)

    # 2. SHR_TREND_DATA fy26[9] (5 marcas — ALL OTHERS CAMP nao existe aqui)
    html, n2, f2 = update_section(html, mkt_name, brands_apr26, shr_start, shr_end, 'fy26', ',null,null,null]')
    ok_shr += n2
    if f2: fail_shr.extend(f2)

    m1 = f'[OK {n1}/6]' if n1 == 6 else f'[WARN {n1}/6]'
    m2 = f'[OK {n2}/5]' if n2 == 5 else f'[WARN {n2}/5]'
    print(f"  {mkt_name}: MSO {m1} | SHR {m2}")

print()
print(f"=== RESUMO ===")
print(f"MSO monthly[9]:  {ok_mso} patches")
print(f"SHR fy26[9]:     {ok_shr} patches")
print(f"Total:           {ok_mso + ok_shr}")
print(f"Original: {original_len:,} | Final: {len(html):,} | Diff: {len(html)-original_len:+,}")

if fail_mso:
    print(f"\nFalhas MSO ({len(fail_mso)}):")
    for f in fail_mso: print(f"  {f}")
if fail_shr:
    print(f"\nFalhas SHR ({len(fail_shr)}):")
    for f in fail_shr: print(f"  {f}")

with open(SRC, 'w', encoding='utf-8') as f:
    f.write(html)
print(f"\nSalvo: {SRC}")

VER = os.path.join(BASE, "versoes", f"Dashboard_Farma_Sul_{datetime.datetime.now().strftime('%Y%m%d_%H%M')}_AllMkts72_Abr26.html")
shutil.copy2(SRC, VER)
print(f"Versao: {VER}")
