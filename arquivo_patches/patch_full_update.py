"""
patch_full_update.py — Atualiza Sell In (plan/meta/real mensais) + todos Estoques
Fonte: Planilha_Mestre_FarmaSul_Giovano.xlsx
"""
import openpyxl, re, sys, os, shutil
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR  = os.path.dirname(os.path.abspath(__file__))
EXCEL_PATH = os.path.join(BASE_DIR, 'Dashboard_farma_sul', 'Planilha_Mestre_FarmaSul_Giovano.xlsx')
HTML_PATH  = os.path.join(BASE_DIR, 'Dashboard_farma_sul', 'Dashboard_Farma_Sul_20260512_2220.html')
VER_DIR    = os.path.join(BASE_DIR, 'Dashboard_farma_sul', 'versoes')

wb = openpyxl.load_workbook(EXCEL_PATH, data_only=True)

def get_rows(sheet_name):
    ws = wb[sheet_name]
    return [list(r) for r in ws.iter_rows(values_only=True)]

# ── helpers ──────────────────────────────────────────────────────────────────
def fv(x):
    """Format JS value: None→null, int float→int, float→float"""
    if x is None: return 'null'
    if isinstance(x, float):
        r = round(x)
        return str(r) if abs(x - r) < 0.5 else str(round(x, 2))
    return str(x)

def js_arr(vals):
    return '[' + ','.join(fv(x) for x in vals) + ']'

def risco(status):
    if not isinstance(status, str): return 'ok'
    if '🔴' in status or 'CRÍT' in status.upper(): return 'critico'
    if '⚠'  in status or 'ATEN' in status.upper(): return 'atencao'
    return 'ok'

def cob_int(c):
    if c is None or c == '-' or c == '': return 999
    try:
        v = float(c)
        return int(round(v)) if v < 9000 else 999
    except: return 999

# ── 1. SELL IN — plan_m / meta_m / real_m ────────────────────────────────────
print('\n[1] Lendo SO_SellIn...')
si = get_rows('SO_SellIn')

# client_name → (plan_m, meta_m, real_m)
SI_MAP = {
    'São João':   si[3],
    'DD-Gaúcha':  si[4],
    'Panvel':     si[5],
    'DD-GAM':     si[6],
    'Nissei':     si[7],
    'DD-Riomed':  si[8],
    'Clamed':     si[9],
}

def pad12(lst):
    out = list(lst)
    while len(out) < 12: out.append(None)
    return out[:12]

si_data = {}
for nome, row in SI_MAP.items():
    plan_m  = pad12(row[21:33])
    meta_m  = pad12(row[33:45])
    real_m  = pad12(row[45:57])
    si_data[nome] = {
        'plan_m': js_arr(plan_m),
        'meta_m': js_arr(meta_m),
        'real_m': js_arr(real_m),
    }
    print(f'  {nome}: real_m={js_arr(real_m)}')

# Total Geral (L11 = index 10)
total_row = si[10]
si_real_total = int(total_row[5]) if total_row[5] else 119743
si_meta_total = int(total_row[4]) if total_row[4] else 82473
print(f'  TOTAL real={si_real_total} meta={si_meta_total}')

# ── 2. ESTOQUE — ler Estoque_Geral consolidado ───────────────────────────────
print('\n[2] Lendo Estoque_Geral...')
eg = get_rows('Estoque_Geral')

by_client = {}
for row in eg:
    if row[0] is None or not isinstance(row[0], str): continue
    cli  = row[0].strip()
    marc = (row[1] or '').strip()
    sku  = (row[2] or '').strip()
    est  = row[3] if isinstance(row[3], (int, float)) else 0
    vnd  = row[4] if isinstance(row[4], (int, float)) else 0
    cob  = cob_int(row[5])
    sta  = row[6]
    if cli not in by_client:
        by_client[cli] = []
    by_client[cli].append({'marc': marc, 'sku': sku, 'est': int(round(est)),
                            'vnd': int(round(vnd)), 'cob': cob, 'risco': risco(sta)})

for cli, rows in by_client.items():
    print(f'  {cli}: {len(rows)} SKUs')

# ── helpers para gerar JS arrays de estoque ──────────────────────────────────
def fmt_sj(rows, marcas_filter):
    """SJ_ESTOQUE / SJ format: {sku, marca, estoque, venda, cob, risco}"""
    out = '[\n'
    for r in rows:
        if r['marc'] not in marcas_filter: continue
        out += (f"  {{sku:{json_str(r['sku'])},marca:{json_str(r['marc'])},"
                f"estoque:{r['est']},venda:{r['vnd']},cob:{r['cob']},risco:{json_str(r['risco'])}}},\n")
    return out.rstrip(',\n') + '\n]'

def fmt_sjc(rows):
    """SJC_ESTOQUE format: {sku, marca, estoque, giro, cob, risco}"""
    marcas = ['LYSOFORM','GLADE','PATO']
    out = '[\n'
    for r in rows:
        if r['marc'] not in marcas: continue
        out += (f"  {{sku:{json_str(r['sku'])},marca:{json_str(r['marc'])},"
                f"estoque:{r['est']},giro:{r['vnd']},cob:{r['cob']},risco:{json_str(r['risco'])}}},\n")
    return out.rstrip(',\n') + '\n]'

def fmt_ns_hb(rows):
    """NS_ESTOQUE_HB: {sku, estoque, venda, venda_abr, dem, cob, risco}"""
    out = '[\n'
    for r in rows:
        out += (f"  {{sku:{json_str(r['sku'])},estoque:{r['est']},"
                f"venda:{r['vnd']},venda_abr:{r['vnd']},dem:{r['vnd']},cob:0,risco:{json_str(r['risco'])}}},\n")
    return out.rstrip(',\n') + '\n]'

def fmt_cl(rows):
    """CL_ESTOQUE: {sku, estoque, venda, cob, risco}"""
    out = '[\n'
    for r in rows:
        out += (f"  {{sku:{json_str(r['sku'])},estoque:{r['est']},"
                f"venda:{r['vnd']},cob:{r['cob']},risco:{json_str(r['risco'])}}},\n")
    return out.rstrip(',\n') + '\n]'

def fmt_pv(rows):
    """PV_ESTOQUE simplified: {sku, marca, estoque, venda_abr, cob, risco} (outros campos=0)"""
    out = '[\n'
    for r in rows:
        out += (f"  {{sku:{json_str(r['sku'])},marca:{json_str(r['marc'])},"
                f"estoque:{r['est']},cdRS:0,cdPR:0,pend:0,lojas:0,lojasCount:0,totalLojas:650,"
                f"dias:{r['cob']},venda_abr:{r['vnd']},fev26:0,mar26:0,dem:{r['vnd']},cob:{r['cob']},risco:{json_str(r['risco'])}}},\n")
    return out.rstrip(',\n') + '\n]'

def fmt_gam(rows):
    """GAM_ESTOQUE: {sku, marca, estoque, giro, pend, risco}"""
    out = '[\n'
    for r in rows:
        out += (f"  {{sku:{json_str(r['sku'])},marca:{json_str(r['marc'])},"
                f"estoque:{r['est']},giro:{r['vnd']},pend:0,risco:{json_str(r['risco'])}}},\n")
    return out.rstrip(',\n') + '\n]'

def fmt_gch(rows):
    """GCH_ESTOQUE: {sku, marca, estoque, dem, cob, risco}"""
    out = '[\n'
    for r in rows:
        out += (f"  {{sku:{json_str(r['sku'])},marca:{json_str(r['marc'])},"
                f"estoque:{r['est']},dem:{r['vnd']},cob:0,risco:{json_str(r['risco'])}}},\n")
    return out.rstrip(',\n') + '\n]'

def fmt_rio(rows):
    """RIO_ESTOQUE: {sku, marca, estoque, vendaMar, vendaAbr, cob, risco}"""
    out = '[\n'
    for r in rows:
        out += (f"  {{sku:{json_str(r['sku'])},marca:{json_str(r['marc'])},"
                f"estoque:{r['est']},vendaMar:{r['vnd']},vendaAbr:{r['vnd']},cob:0,risco:{json_str(r['risco'])}}},\n")
    return out.rstrip(',\n') + '\n]'

def json_str(s):
    return "'" + str(s).replace("'", "\\'") + "'"

# ── 3. Ler NS estoque de SO_Nissei_Andre e SO_Nissei_Edmar ───────────────────
print('\n[3] Lendo NS estoque (André + Edmar)...')

def read_ns_estoque(sheet_name):
    ws = wb[sheet_name]
    rows_data = []
    in_estoque = False
    for row in ws.iter_rows(values_only=True):
        row = list(row)
        if row[0] is None: continue
        if isinstance(row[0], str) and 'GESTÃO DE ESTOQUE' in row[0]:
            in_estoque = True
            continue
        if in_estoque and row[0] in ('Marca', 'marca', None): continue
        if in_estoque and isinstance(row[0], str) and row[1] is not None:
            marc = row[0].strip()
            sku  = (row[1] or '').strip()
            est  = row[2] if isinstance(row[2], (int, float)) else 0
            vnd  = row[3] if isinstance(row[3], (int, float)) else 0
            cob  = cob_int(row[4])
            sta  = row[5]
            rows_data.append({'marc': marc, 'sku': sku, 'est': int(round(est)),
                               'vnd': int(round(vnd)), 'cob': cob, 'risco': risco(sta)})
    return rows_data

ns_hb = read_ns_estoque('SO_Nissei_Andre')
ns_ed = read_ns_estoque('SO_Nissei_Edmar')
print(f'  NS HB (André): {len(ns_hb)} SKUs')
print(f'  NS ED (Edmar): {len(ns_ed)} SKUs')

# ── 4. Aplicar patches no HTML ───────────────────────────────────────────────
print('\n[4] Aplicando patches...')

with open(HTML_PATH, encoding='utf-8') as f:
    html = f.read()

patches = 0

# ── 4a. SELLIN_DATA plan_m / meta_m / real_m ─────────────────────────────────
# Mapping: nome no HTML → nome na planilha
SI_NOME_MAP = {
    'São João':  'São João',
    'DD-Gaúcha': 'DD-Gaúcha',
    'Panvel':    'Panvel',
    'DD-GAM':    'DD-GAM',
    'Nissei':    'Nissei',
    'DD-Riomed': 'DD-Riomed',
    'Clamed':    'Clamed',
}

for js_name, xl_name in SI_NOME_MAP.items():
    d = si_data[xl_name]
    # Match the specific client block: { nome:'NNN',...plan_m:[...],...meta_m:[...],...real_m:[...] }
    # We replace plan_m, meta_m and real_m arrays
    pattern = (
        r"(nome:'" + re.escape(js_name) + r"'[\s\S]*?plan_m:)\[[^\]]*\]"
        r"([\s\S]*?meta_m:)\[[^\]]*\]"
        r"([\s\S]*?real_m:)\[[^\]]*\]"
    )
    repl = r'\g<1>' + d['plan_m'] + r'\g<2>' + d['meta_m'] + r'\g<3>' + d['real_m']
    new_html, n = re.subn(pattern, repl, html)
    if n:
        html = new_html
        patches += 1
        print(f'  ✅ SELLIN_DATA {js_name}: plan/meta/real atualizados')
    else:
        print(f'  ⚠️  SELLIN_DATA {js_name}: padrão não encontrado')

# ── 4b. SELLIN_TOTAL real e meta ──────────────────────────────────────────────
for field, val in [('real', si_real_total), ('meta', si_meta_total)]:
    pattern = r'(SELLIN_TOTAL\s*=\s*\{[\s\S]*?' + field + r':)\d+'
    new_html, n = re.subn(pattern, r'\g<1>' + str(val), html)
    if n:
        html = new_html
        patches += 1
        print(f'  ✅ SELLIN_TOTAL.{field} → {val}')

# ── 4c. SJ_ESTOQUE ───────────────────────────────────────────────────────────
sj_rows = by_client.get('São João', [])
sj_hb_rows = [r for r in sj_rows if r['marc'] in ('OFF!','EXPOSIS','RAID')]
new_sj = fmt_sj(sj_rows, ('OFF!','EXPOSIS','RAID'))
pattern = r'const SJ_ESTOQUE\s*=\s*\[[\s\S]*?\];'
new_html, n = re.subn(pattern, 'const SJ_ESTOQUE = ' + new_sj + ';', html)
if n:
    html = new_html
    patches += 1
    print(f'  ✅ SJ_ESTOQUE: {len(sj_hb_rows)} SKUs')
else:
    print('  ⚠️  SJ_ESTOQUE não encontrado')

# ── 4d. SJC_ESTOQUE ──────────────────────────────────────────────────────────
sjc_rows = [r for r in sj_rows if r['marc'] in ('LYSOFORM','GLADE','PATO')]
new_sjc = fmt_sjc(sj_rows)
pattern = r'const SJC_ESTOQUE\s*=\s*\[[\s\S]*?\];'
new_html, n = re.subn(pattern, 'const SJC_ESTOQUE = ' + new_sjc + ';', html)
if n:
    html = new_html
    patches += 1
    print(f'  ✅ SJC_ESTOQUE: {len(sjc_rows)} SKUs')
else:
    print('  ⚠️  SJC_ESTOQUE não encontrado')

# ── 4e. NS_ESTOQUE_HB / NS_ESTOQUE_ED ────────────────────────────────────────
new_ns_hb = fmt_ns_hb(ns_hb)
pattern = r'const NS_ESTOQUE_HB\s*=\s*\[[\s\S]*?\];'
new_html, n = re.subn(pattern, 'const NS_ESTOQUE_HB = ' + new_ns_hb + ';', html)
if n:
    html = new_html
    patches += 1
    print(f'  ✅ NS_ESTOQUE_HB: {len(ns_hb)} SKUs')
else:
    print('  ⚠️  NS_ESTOQUE_HB não encontrado')

new_ns_ed = fmt_ns_hb(ns_ed)  # mesmo formato
pattern = r'const NS_ESTOQUE_ED\s*=\s*\[[\s\S]*?\];'
new_html, n = re.subn(pattern, 'const NS_ESTOQUE_ED = ' + new_ns_ed + ';', html)
if n:
    html = new_html
    patches += 1
    print(f'  ✅ NS_ESTOQUE_ED: {len(ns_ed)} SKUs')
else:
    print('  ⚠️  NS_ESTOQUE_ED não encontrado')

# ── 4f. CL_ESTOQUE ───────────────────────────────────────────────────────────
cl_rows = by_client.get('Clamed', [])
new_cl = fmt_cl(cl_rows)
pattern = r'const CL_ESTOQUE\s*=\s*\[[\s\S]*?\];'
new_html, n = re.subn(pattern, 'const CL_ESTOQUE = ' + new_cl + ';', html)
if n:
    html = new_html
    patches += 1
    print(f'  ✅ CL_ESTOQUE: {len(cl_rows)} SKUs')
else:
    print('  ⚠️  CL_ESTOQUE não encontrado')

# ── 4g. PV_ESTOQUE ───────────────────────────────────────────────────────────
pv_rows = by_client.get('Panvel', [])
new_pv = fmt_pv(pv_rows)
pattern = r'const PV_ESTOQUE\s*=\s*\[[\s\S]*?\];'
new_html, n = re.subn(pattern, 'const PV_ESTOQUE = ' + new_pv + ';', html)
if n:
    html = new_html
    patches += 1
    print(f'  ✅ PV_ESTOQUE: {len(pv_rows)} SKUs')
else:
    print('  ⚠️  PV_ESTOQUE não encontrado')

# ── 4h. GAM_ESTOQUE ──────────────────────────────────────────────────────────
gam_rows = by_client.get('DD-GAM', [])
new_gam = fmt_gam(gam_rows)
pattern = r'const GAM_ESTOQUE\s*=\s*\[[\s\S]*?\];'
new_html, n = re.subn(pattern, 'const GAM_ESTOQUE = ' + new_gam + ';', html)
if n:
    html = new_html
    patches += 1
    print(f'  ✅ GAM_ESTOQUE: {len(gam_rows)} SKUs')
else:
    print('  ⚠️  GAM_ESTOQUE não encontrado')

# ── 4i. GCH_ESTOQUE ──────────────────────────────────────────────────────────
gch_rows = by_client.get('DD-Gaúcha', [])
new_gch = fmt_gch(gch_rows)
pattern = r'const GCH_ESTOQUE\s*=\s*\[[\s\S]*?\];'
new_html, n = re.subn(pattern, 'const GCH_ESTOQUE = ' + new_gch + ';', html)
if n:
    html = new_html
    patches += 1
    print(f'  ✅ GCH_ESTOQUE: {len(gch_rows)} SKUs')
else:
    print('  ⚠️  GCH_ESTOQUE não encontrado')

# ── 4j. RIO_ESTOQUE ──────────────────────────────────────────────────────────
rio_rows = by_client.get('DD-Riomed', [])
new_rio = fmt_rio(rio_rows)
pattern = r'const RIO_ESTOQUE\s*=\s*\[[\s\S]*?\];'
new_html, n = re.subn(pattern, 'const RIO_ESTOQUE = ' + new_rio + ';', html)
if n:
    html = new_html
    patches += 1
    print(f'  ✅ RIO_ESTOQUE: {len(rio_rows)} SKUs')
else:
    print('  ⚠️  RIO_ESTOQUE não encontrado')

# ── 5. Salvar ─────────────────────────────────────────────────────────────────
ts = datetime.now().strftime('%Y%m%d_%H%M')
ver_path = os.path.join(VER_DIR, f'Dashboard_Farma_Sul_{ts}_FullUpdate.html')
shutil.copy2(HTML_PATH, ver_path)
print(f'\n[5] Backup criado: {os.path.basename(ver_path)}')

with open(HTML_PATH, 'w', encoding='utf-8') as f:
    f.write(html)
print(f'     Principal salvo: Dashboard_Farma_Sul_20260512_2220.html')
print(f'\n✅ Total patches aplicados: {patches}')

# Downloads
try:
    dl = os.path.join(os.path.expanduser('~'), 'Downloads',
                      f'Dashboard_FarmaSul_Giovano_{ts}.html')
    shutil.copy2(HTML_PATH, dl)
    print(f'     Cópia Downloads: {os.path.basename(dl)}')
except Exception as e:
    print(f'     Downloads: {e}')
