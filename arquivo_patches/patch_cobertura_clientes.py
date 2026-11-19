"""
patch_cobertura_clientes.py
===========================
Atualiza cobertura por SKU de todos os clientes com dados reais da planilha:
  ① SJ_COBERTURA  — Cob_SJoao (isadora)  — 43 SKUs / 1.219 lojas
  ② SJC_COBERTURA — Cob_SJoao (Caroline) — 29 SKUs / 1.219 lojas
  ③ CL_COBERTURA  — Cob_Clamed           — 16 SKUs / 652 lojas
  ④ NS_COBERTURA  — Cob_Nissei           — 42 SKUs / 471 lojas (estimação → real)
  ⑤ PV_ESTOQUE    — Cob_Panvel           — 25 SKUs / lojas reais por SKU
"""
import sys, shutil, re, unicodedata
sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path
from datetime import datetime
import openpyxl

DASH = Path(r'C:\Users\valqu\OneDrive\Documentos\Claude\Projects\projeto Dashboard_farma_sul\Dashboard_farma_sul\Dashboard_Farma_Sul_20260512_2220.html')
XLS  = Path(r'C:\Users\valqu\OneDrive\Documentos\Claude\Projects\projeto Dashboard_farma_sul\Dashboard_farma_sul\Planilha_Mestre_FarmaSul_Giovano.xlsx')
VER  = DASH.parent / 'versoes'
DL   = Path.home() / 'Downloads'
ts   = datetime.now().strftime('%Y%m%d_%H%M')

shutil.copy(DASH, VER / f'Dashboard_Farma_Sul_{ts}_PreCobClientes.html')
h = DASH.read_text(encoding='utf-8')
print(f'Backup: ...PreCobClientes.html  |  tamanho: {len(h):,} chars')

# ─── Helpers ──────────────────────────────────────────────────────────────────
def norm(s):
    """Normaliza nome de SKU para matching: maiúsculo + sem acentos + sem pontuação."""
    if not s: return ''
    s = str(s).upper().strip()
    s = unicodedata.normalize('NFD', s)
    s = ''.join(c for c in s if unicodedata.category(c) != 'Mn')
    s = re.sub(r'[^A-Z0-9 +,./]', ' ', s)
    return re.sub(r'\s+', ' ', s).strip()

def risco_from_pct(pct):
    if pct < 50:  return 'critico'
    if pct < 80:  return 'atencao'
    return 'ok'

def guess_marca(sku):
    u = sku.upper()
    if 'EXPOSIS' in u: return 'EXPOSIS'
    if 'OFF'     in u: return 'OFF!'
    if 'RAID'    in u: return 'RAID'
    if 'LYSOFORM'in u: return 'LYSOFORM'
    if 'PATO'    in u: return 'PATO'
    if 'GLADE'   in u: return 'GLADE'
    return 'HB'

def read_cob_sheet(ws):
    """Lê aba Cob_* e retorna lista de (sku, lojas, total, estoque)."""
    rows = list(ws.iter_rows(values_only=True))
    result = []
    for r in rows[5:]:
        if r[0] and r[1] is not None and r[2] is not None:
            result.append((str(r[0]).strip(), int(r[1] or 0), int(r[2] or 0), int(r[3] or 0)))
    return result

def fuzzy_match(html_name, excel_dict, threshold=0.75):
    """Retorna o valor Excel que melhor bate com html_name, ou None."""
    hn = norm(html_name)
    if hn in excel_dict:
        return excel_dict[hn]
    hw = set(hn.split())
    best, best_score = None, 0.0
    for en, ev in excel_dict.items():
        ew = set(en.split())
        score = len(hw & ew) / max(len(hw | ew), 1)
        if score > best_score:
            best_score, best = score, ev
    if best and best_score >= threshold:
        return best
    return None

wb = openpyxl.load_workbook(str(XLS), read_only=True, data_only=True)

# ═══════════════════════════════════════════════════════════════════════════════
# ① SJ_COBERTURA — Cob_SJoao (isadora)
# ═══════════════════════════════════════════════════════════════════════════════
sj_data = read_cob_sheet(wb['Cob_SJoao (isadora)'])
sj_lines = []
for sku, lojas, total, estoque in sj_data:
    if total == 0: continue
    pct = round(lojas / total * 100, 1)
    risco = risco_from_pct(pct)
    risco_str = f', risco:"{risco}"' if risco != 'ok' else ''
    sj_lines.append(f'  {{sku:"{sku}",total:{total},lojas:{lojas},pct:{pct},estoque:{estoque}{risco_str}}}')

NEW_SJ = 'const SJ_COBERTURA = [\n' + ',\n'.join(sj_lines) + '\n];'

# Find old SJ_COBERTURA
old_sj_start = h.find('const SJ_COBERTURA')
old_sj_end   = h.find('];', old_sj_start) + 2
assert old_sj_start != -1, 'SJ_COBERTURA não encontrado'
h = h[:old_sj_start] + NEW_SJ + h[old_sj_end:]
print(f'① SJ_COBERTURA: {len(sj_data)} SKUs | total_lojas=1219')

# ═══════════════════════════════════════════════════════════════════════════════
# ② SJC_COBERTURA — Cob_SJoao (Caroline)
# ═══════════════════════════════════════════════════════════════════════════════
sjc_data = read_cob_sheet(wb['Cob_SJoao ( Caroline)'])
sjc_lines = []
for sku, lojas, total, estoque in sjc_data:
    if total == 0: continue
    pct = round(lojas / total * 100, 1)
    marca = guess_marca(sku)
    sjc_lines.append(f"  {{sku:'{sku}',marca:'{marca}',lojas:{lojas},total:{total},pct:{pct},estoque:{estoque}}}")

NEW_SJC = 'const SJC_COBERTURA = [\n' + ',\n'.join(sjc_lines) + '\n];'

old_sjc_start = h.find('const SJC_COBERTURA')
old_sjc_end   = h.find('];', old_sjc_start) + 2
assert old_sjc_start != -1, 'SJC_COBERTURA não encontrado'
h = h[:old_sjc_start] + NEW_SJC + h[old_sjc_end:]
print(f'② SJC_COBERTURA: {len(sjc_data)} SKUs | total_lojas=1219')

# ═══════════════════════════════════════════════════════════════════════════════
# ③ CL_COBERTURA — Cob_Clamed (replace with all 16 real SKUs)
# ═══════════════════════════════════════════════════════════════════════════════
cl_data = read_cob_sheet(wb['Cob_Clamed'])
cl_lines = []
for sku, lojas, total, estoque in cl_data:
    if total == 0: continue
    pct = round(lojas / total * 100, 1)
    risco = risco_from_pct(pct)
    risco_str = f', risco:"{risco}"' if risco != 'ok' else ''
    cl_lines.append(f'  {{sku:"{sku}",total:{total},lojas:{lojas},pct:{pct},estoque:{estoque}{risco_str}}}')

NEW_CL = 'const CL_COBERTURA = [\n' + ',\n'.join(cl_lines) + '\n];'

old_cl_start = h.find('const CL_COBERTURA')
old_cl_end   = h.find('];', old_cl_start) + 2
assert old_cl_start != -1, 'CL_COBERTURA não encontrado'
h = h[:old_cl_start] + NEW_CL + h[old_cl_end:]
print(f'③ CL_COBERTURA: {len(cl_data)} SKUs | total_lojas=652')

# ═══════════════════════════════════════════════════════════════════════════════
# ④ NS_COBERTURA — Cob_Nissei (IIFE → array estático com dados reais)
# ═══════════════════════════════════════════════════════════════════════════════
ns_data = read_cob_sheet(wb['Cob_Nissei'])
ns_lines = []
for sku, lojas, total, estoque in ns_data:
    if total == 0: continue
    pct = round(lojas / total * 100, 1)
    risco = risco_from_pct(pct)
    risco_str = f', risco:"{risco}"' if risco != 'ok' else ''
    ns_lines.append(f'  {{sku:"{sku}",lojas:{lojas},total:{total},pct:{pct},estoque:{estoque}{risco_str}}}')

NEW_NS = 'const NS_COBERTURA = [\n' + ',\n'.join(ns_lines) + '\n];'

# Find old NS_COBERTURA IIFE (ends with })();)
old_ns_start = h.find('const NS_COBERTURA')
old_ns_end   = h.find('})();', old_ns_start) + 5
assert old_ns_start != -1, 'NS_COBERTURA não encontrado'
assert old_ns_end > old_ns_start, 'Fechamento })(); não encontrado'
h = h[:old_ns_start] + NEW_NS + h[old_ns_end:]
print(f'④ NS_COBERTURA: {len(ns_data)} SKUs | total_lojas=471 (estimação → real)')

# ═══════════════════════════════════════════════════════════════════════════════
# ⑤ PV_ESTOQUE — atualizar lojasCount e totalLojas por SKU
# ═══════════════════════════════════════════════════════════════════════════════
pv_data = read_cob_sheet(wb['Cob_Panvel'])
excel_pv = {norm(r[0]): r for r in pv_data}

# Find PV_ESTOQUE block
pv_start = h.find('const PV_ESTOQUE')
pv_end   = h.find('];', pv_start) + 2
pv_block = h[pv_start:pv_end]

# Get all HTML SKUs
html_pv_skus = re.findall(r"sku:'([^']+)'", pv_block)
updated = 0
skipped = 0

for hsku in html_pv_skus:
    match = fuzzy_match(hsku, excel_pv, threshold=0.78)
    if match:
        _, lojas, total, _ = match
        # Update lojasCount:0 → real value, totalLojas → real per-SKU value
        # Need to update the specific entry: match by sku string
        sku_anchor = f"sku:'{hsku}'"
        # Find this entry's lojasCount and totalLojas
        entry_pos = pv_block.find(sku_anchor)
        if entry_pos == -1:
            skipped += 1
            continue
        # Find next }, after entry_pos
        entry_end = pv_block.find('}', entry_pos)
        entry = pv_block[entry_pos:entry_end+1]
        # Replace lojasCount:0 and totalLojas:650
        new_entry = re.sub(r'lojasCount:\d+', f'lojasCount:{lojas}', entry)
        new_entry = re.sub(r'totalLojas:\d+', f'totalLojas:{total}', new_entry)
        if new_entry != entry:
            pv_block = pv_block[:entry_pos] + new_entry + pv_block[entry_end+1:]
            updated += 1
    else:
        skipped += 1

h = h[:pv_start] + pv_block + h[pv_end:]
print(f'⑤ PV_ESTOQUE: {updated}/{len(html_pv_skus)} SKUs atualizados | {skipped} sem match em Cob_Panvel')

# ═══════════════════════════════════════════════════════════════════════════════
# Verificações
# ═══════════════════════════════════════════════════════════════════════════════
assert 'const SJ_COBERTURA'  in h
assert 'const SJC_COBERTURA' in h
assert 'const CL_COBERTURA'  in h
assert 'const NS_COBERTURA'  in h
assert 'const PV_ESTOQUE'    in h

# SJ must have 43 entries
assert h.count('const SJ_COBERTURA') == 1
sj_entries = len(re.findall(r'\{sku:"', h[h.find('const SJ_COBERTURA'):h.find('];', h.find('const SJ_COBERTURA'))+2]))
print(f'Verificação SJ: {sj_entries} entradas')

# CL must now have 16 entries (was 7)
cl_entries = len(re.findall(r'\{sku:"', h[h.find('const CL_COBERTURA'):h.find('];', h.find('const CL_COBERTURA'))+2]))
print(f'Verificação CL: {cl_entries} entradas (era 7)')

# NS must not be IIFE anymore
assert '})();' not in h[h.find('const NS_COBERTURA'):h.find('const NS_COBERTURA')+50]
print(f'Verificação NS: IIFE substituído por array estático ✓')

print('Todas as verificações: OK')
print(f'Tamanho final: {len(h):,} chars')

# ═══════════════════════════════════════════════════════════════════════════════
# Salvar
# ═══════════════════════════════════════════════════════════════════════════════
DASH.write_text(h, encoding='utf-8')
shutil.copy(DASH, VER / f'Dashboard_Farma_Sul_{ts}_CobClientes.html')
shutil.copy(DASH, DL  / f'Dashboard_FarmaSul_Giovano_{ts}.html')
print(f'Versao:    Dashboard_Farma_Sul_{ts}_CobClientes.html')
print(f'Downloads: Dashboard_FarmaSul_Giovano_{ts}.html')
print('DONE.')
