"""
patch5b_shr_allmarkets.py
Insere fy26[9] (ABR/26) em SHR_TREND_DATA para todos os markets ainda em null.
Patch5 ja atualizou MKTSHARE_OVERVIEW (246 patches).
Este script completa o SHR_TREND_DATA.
"""
import os, shutil, datetime

BASE = r"C:\Users\valqu\OneDrive\Documentos\Claude\Projects\projeto Dashboard_farma_sul\Dashboard_farma_sul"
SRC  = os.path.join(BASE, "Dashboard_Farma_Sul_20260512_2220.html")

APR26 = {
  'Farma CO': {
    'OFF!':23.23,'EXPOSIS':20.79,'XO INSETO':21.61,'SUPER REPELEX':7.87,'SBP':3.76,'ALL OTHERS CAMP':22.74},
  'Farma Gde RJ': {
    'OFF!':42.86,'EXPOSIS':25.87,'XO INSETO':16.94,'SUPER REPELEX':4.10,'SBP':3.00,'ALL OTHERS CAMP':7.23},
  'Farma Gde SP': {
    'OFF!':29.84,'EXPOSIS':30.24,'XO INSETO':16.87,'SUPER REPELEX':6.20,'SBP':4.43,'ALL OTHERS CAMP':12.42},
  'Farma Int SP': {
    'OFF!':29.89,'EXPOSIS':19.13,'XO INSETO':26.14,'SUPER REPELEX':5.26,'SBP':3.92,'ALL OTHERS CAMP':15.65},
  'Farma MG+ES+Int RJ': {
    'OFF!':29.63,'EXPOSIS':18.93,'XO INSETO':29.19,'SUPER REPELEX':4.56,'SBP':3.42,'ALL OTHERS CAMP':14.28},
  'Farma NE': {
    'OFF!':36.31,'EXPOSIS':11.93,'XO INSETO':35.04,'SUPER REPELEX':2.87,'SBP':2.74,'ALL OTHERS CAMP':11.12},
  'Farma Indep Sul': {
    'OFF!':25.57,'EXPOSIS':7.46,'XO INSETO':26.17,'SUPER REPELEX':4.75,'SBP':1.19,'ALL OTHERS CAMP':34.85},
  'Farma Indep CO': {
    'OFF!':19.64,'EXPOSIS':13.87,'XO INSETO':26.82,'SUPER REPELEX':7.80,'SBP':3.20,'ALL OTHERS CAMP':28.68},
  'Farma Indep Gde RJ': {
    'OFF!':54.70,'EXPOSIS':11.64,'XO INSETO':24.74,'SUPER REPELEX':1.62,'SBP':0.67,'ALL OTHERS CAMP':6.62},
  'Farma Indep Gde SP': {
    'OFF!':30.55,'EXPOSIS':8.80,'XO INSETO':32.41,'SUPER REPELEX':6.66,'SBP':3.42,'ALL OTHERS CAMP':18.16},
  'Farma Indep Int SP': {
    'OFF!':26.30,'EXPOSIS':11.76,'XO INSETO':34.50,'SUPER REPELEX':5.40,'SBP':3.55,'ALL OTHERS CAMP':18.48},
  'Farma Indep MG+ES+Int RJ': {
    'OFF!':27.94,'EXPOSIS':11.73,'XO INSETO':36.06,'SUPER REPELEX':4.09,'SBP':1.81,'ALL OTHERS CAMP':18.37},
  'Farma Indep NE': {
    'OFF!':35.90,'EXPOSIS':6.19,'XO INSETO':44.32,'SUPER REPELEX':1.71,'SBP':1.25,'ALL OTHERS CAMP':10.63},
  'Farma Moderno Sul': {
    'OFF!':26.53,'EXPOSIS':18.32,'XO INSETO':23.75,'SUPER REPELEX':8.04,'SBP':3.32,'ALL OTHERS CAMP':20.03},
  'Farma Moderno CO': {
    'OFF!':30.60,'EXPOSIS':34.95,'XO INSETO':10.93,'SUPER REPELEX':8.03,'SBP':4.91,'ALL OTHERS CAMP':10.57},
  'Farma Moderno Gde RJ': {
    'OFF!':35.69,'EXPOSIS':34.48,'XO INSETO':12.22,'SUPER REPELEX':5.59,'SBP':4.41,'ALL OTHERS CAMP':7.60},
  'Farma Moderno Gde SP': {
    'OFF!':29.52,'EXPOSIS':39.93,'XO INSETO':9.85,'SUPER REPELEX':5.99,'SBP':4.88,'ALL OTHERS CAMP':9.83},
  'Farma Moderno Int SP': {
    'OFF!':33.98,'EXPOSIS':27.53,'XO INSETO':16.61,'SUPER REPELEX':5.11,'SBP':4.35,'ALL OTHERS CAMP':12.42},
  'Farma Moderno MG+ES+Int RJ': {
    'OFF!':31.88,'EXPOSIS':28.54,'XO INSETO':20.01,'SUPER REPELEX':5.18,'SBP':5.57,'ALL OTHERS CAMP':8.82},
  'Farma Moderno NE': {
    'OFF!':37.16,'EXPOSIS':23.91,'XO INSETO':15.65,'SUPER REPELEX':5.30,'SBP':5.83,'ALL OTHERS CAMP':12.14},
  'T.BR Farma Indep': {
    'OFF!':30.11,'EXPOSIS':9.36,'XO INSETO':34.94,'SUPER REPELEX':4.10,'SBP':2.01,'ALL OTHERS CAMP':19.47},
  'T.BR Farma Moderno': {
    'OFF!':32.08,'EXPOSIS':27.50,'XO INSETO':16.95,'SUPER REPELEX':6.15,'SBP':4.67,'ALL OTHERS CAMP':12.65},
  'INFC RS': {
    'OFF!':26.71,'EXPOSIS':10.61,'XO INSETO':26.21,'SUPER REPELEX':8.23,'SBP':3.05,'ALL OTHERS CAMP':25.19},
  'INFC SC': {
    'OFF!':25.89,'EXPOSIS':14.33,'XO INSETO':17.47,'SUPER REPELEX':5.76,'SBP':1.80,'ALL OTHERS CAMP':34.75},
  'INFC PR': {
    'OFF!':25.57,'EXPOSIS':13.60,'XO INSETO':30.33,'SUPER REPELEX':5.47,'SBP':2.03,'ALL OTHERS CAMP':23.01},
  'INFC Curitiba': {
    'OFF!':26.30,'EXPOSIS':17.38,'XO INSETO':20.05,'SUPER REPELEX':7.41,'SBP':2.04,'ALL OTHERS CAMP':26.81},
  'INFC Porto Alegre': {
    'OFF!':32.44,'EXPOSIS':13.69,'XO INSETO':19.80,'SUPER REPELEX':8.96,'SBP':3.36,'ALL OTHERS CAMP':21.74},
  'INFC Sul': {
    'OFF!':26.02,'EXPOSIS':12.93,'XO INSETO':24.91,'SUPER REPELEX':6.40,'SBP':2.26,'ALL OTHERS CAMP':27.47},
  'INFC Int PR': {
    'OFF!':25.28,'EXPOSIS':12.10,'XO INSETO':34.42,'SUPER REPELEX':4.70,'SBP':2.02,'ALL OTHERS CAMP':21.50},
  'INFC Int RS': {
    'OFF!':22.93,'EXPOSIS':8.57,'XO INSETO':30.45,'SUPER REPELEX':7.74,'SBP':2.84,'ALL OTHERS CAMP':27.47},
  'INFC Cidade Gde Sul': {
    'OFF!':27.42,'EXPOSIS':19.52,'XO INSETO':18.54,'SUPER REPELEX':6.78,'SBP':2.75,'ALL OTHERS CAMP':24.99},
  'INFC Cidade Peq+Med Sul': {
    'OFF!':25.80,'EXPOSIS':11.01,'XO INSETO':27.53,'SUPER REPELEX':6.17,'SBP':2.04,'ALL OTHERS CAMP':27.44},
  'INFC MG': {
    'OFF!':26.50,'EXPOSIS':20.99,'XO INSETO':29.23,'SUPER REPELEX':3.70,'SBP':3.16,'ALL OTHERS CAMP':16.42},
  'INFC CO': {
    'OFF!':23.24,'EXPOSIS':20.70,'XO INSETO':21.51,'SUPER REPELEX':7.94,'SBP':3.74,'ALL OTHERS CAMP':22.87},
  'INFC BA': {
    'OFF!':36.24,'EXPOSIS':12.69,'XO INSETO':32.47,'SUPER REPELEX':3.14,'SBP':3.26,'ALL OTHERS CAMP':12.20},
  'INFC Belo Horizonte': {
    'OFF!':30.55,'EXPOSIS':24.57,'XO INSETO':23.51,'SUPER REPELEX':3.08,'SBP':4.88,'ALL OTHERS CAMP':13.41},
  'INFC CE': {
    'OFF!':38.67,'EXPOSIS':15.43,'XO INSETO':28.31,'SUPER REPELEX':3.19,'SBP':2.66,'ALL OTHERS CAMP':11.74},
  'INFC Cidade Gde Gde RJ': {
    'OFF!':42.97,'EXPOSIS':25.52,'XO INSETO':16.73,'SUPER REPELEX':4.55,'SBP':2.92,'ALL OTHERS CAMP':7.31},
  'INFC Cidade Gde CO': {
    'OFF!':29.14,'EXPOSIS':26.43,'XO INSETO':13.01,'SUPER REPELEX':7.69,'SBP':3.89,'ALL OTHERS CAMP':19.85},
  'INFC Cidade Gde Gde SP': {
    'OFF!':29.87,'EXPOSIS':29.62,'XO INSETO':17.30,'SUPER REPELEX':6.11,'SBP':4.32,'ALL OTHERS CAMP':12.77},
  'INFC Cidade Gde Int SP': {
    'OFF!':29.85,'EXPOSIS':30.24,'XO INSETO':18.88,'SUPER REPELEX':5.47,'SBP':3.69,'ALL OTHERS CAMP':11.87},
}

BRANDS = ['OFF!', 'EXPOSIS', 'XO INSETO', 'SUPER REPELEX', 'SBP', 'ALL OTHERS CAMP']

with open(SRC, 'r', encoding='utf-8') as f:
    html = f.read()

original_len = len(html)
total_patches = 0
ok_count = 0
fails = []

# Localizar o bloco SHR_TREND_DATA no HTML
shr_start = html.find('SHR_TREND_DATA =')
if shr_start == -1:
    shr_start = html.find('SHR_TREND_DATA=')
# Fim do bloco: proxima declaracao const
shr_end = html.find('\nconst ', shr_start + 100)
print(f"SHR_TREND_DATA bloco: {shr_start} → {shr_end} ({shr_end - shr_start:,} chars)")

print("=== PATCH 5b: SHR_TREND_DATA ABR/26 — TODOS OS MARKETS ===\n")

for mkt_name, brands_apr26 in APR26.items():
    # Buscar o market DENTRO do bloco SHR_TREND_DATA
    mkt_tag = f"  '{mkt_name}': {{"
    pos = html.find(mkt_tag, shr_start, shr_end)
    if pos == -1:
        fails.append(f'{mkt_name}: market nao encontrado em SHR_TREND_DATA')
        print(f"  {mkt_name}: [X] nao encontrado")
        continue

    # Fim da secao desse market
    next_pos = html.find("\n  '", pos + len(mkt_tag))
    if next_pos == -1 or next_pos > shr_end:
        next_pos = shr_end
    section = html[pos:next_pos]
    original_section = section
    ok = 0

    for brand in BRANDS:
        if brand not in brands_apr26:
            continue
        apr_val = brands_apr26[brand]

        # Encontrar a tag do brand na secao
        brand_tag = f"'{brand}':"
        b_pos = section.find(brand_tag)
        if b_pos == -1:
            fails.append(f'{mkt_name}/{brand}: brand tag nao encontrada')
            continue

        # Encontrar fy26:[ apos a tag do brand
        field_tag = 'fy26:['
        f_pos = section.find(field_tag, b_pos)
        if f_pos == -1:
            fails.append(f'{mkt_name}/{brand}: fy26 nao encontrado')
            continue

        # Encontrar fim do array fy26
        arr_end = section.index(']', f_pos) + 1
        arr_str = section[f_pos:arr_end]          # ex: fy26:[21.0,...,null,null,null]
        values_str = arr_str[len(field_tag):-1]    # ex: 21.0,...,null,null,null

        # Verificar sufixo esperado
        if not arr_str.endswith(',null,null,null]'):
            fails.append(f'{mkt_name}/{brand}: sufixo inesperado: {arr_str[-25:]}')
            continue

        parts = values_str.split(',')
        if len(parts) != 12:
            fails.append(f'{mkt_name}/{brand}: {len(parts)} valores (esperado 12)')
            continue
        if parts[9] != 'null':
            fails.append(f'{mkt_name}/{brand}: fy26[9] ja={parts[9]}, skip')
            continue

        parts[9] = str(apr_val)
        new_arr = f'fy26:[{",".join(parts)}]'
        section = section[:f_pos] + new_arr + section[arr_end:]
        ok += 1
        total_patches += 1

    # Aplicar secao atualizada no HTML
    html = html[:pos] + section + html[pos + len(original_section):]
    ok_count += ok
    status = f'[OK {ok}/6]' if ok == 6 else f'[WARN {ok}/6]'
    print(f"  {mkt_name}: SHR {status}")

print()
print(f"=== RESUMO ===")
print(f"Markets processados: {len(APR26)}")
print(f"Brands atualizadas:  {ok_count}")
print(f"Total patches:       {total_patches}")
print(f"Tamanho original:    {original_len:,} chars")
print(f"Tamanho final:       {len(html):,} chars")
print(f"Diferenca:           {len(html)-original_len:+,} chars")

if fails:
    print(f"\nFalhas ({len(fails)}):")
    for f in fails: print(f"  {f}")

with open(SRC, 'w', encoding='utf-8') as f:
    f.write(html)
print(f"\nSalvo em: {SRC}")

VER = os.path.join(BASE, "versoes", f"Dashboard_Farma_Sul_{datetime.datetime.now().strftime('%Y%m%d_%H%M')}_AllMarketsAbr26_v2.html")
shutil.copy2(SRC, VER)
print(f"Versao: {VER}")
