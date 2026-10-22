"""
Auditoria e correção completa dos dados de Market Share no Dashboard.
Fonte oficial: 1-Tabela-1 do arquivo Base Giovano 26-04.xlsx
Corrige: MKTSHARE_OVERVIEW (69→72 markets) + SHR_TREND_DATA (fy24/fy25)
"""
import sys, shutil, os, re
sys.stdout.reconfigure(encoding='utf-8')
import openpyxl
from datetime import datetime

BASE  = r'C:\Users\valqu\OneDrive\Documentos\Claude\Projects\projeto Dashboard_farma_sul'
XL    = BASE + r'\base_giovano_tmp.xlsx'
SRC   = BASE + r'\Dashboard_farma_sul\Dashboard_Farma_Sul_20260512_2220.html'
BKP   = BASE + r'\Dashboard_farma_sul\versoes\Dashboard_Farma_Sul_20260513_1300_PreNielsenFix.html'
OUT   = BASE + r'\Dashboard_farma_sul\versoes\Dashboard_Farma_Sul_20260513_1305_NielsenFix.html'

# ── Período map ──────────────────────────────────────────────────────────────
FY24 = ['2023-07-23','2023-08-23','2023-09-22','2023-10-23','2023-11-22','2023-12-23',
        '2024-01-23','2024-02-21','2024-03-23','2024-04-22','2024-05-23','2024-06-22']
FY25 = ['2024-07-23','2024-08-23','2024-09-22','2024-10-23','2024-11-22','2024-12-23',
        '2025-01-23','2025-02-20','2025-03-23','2025-04-22','2025-05-23','2025-06-22']
FY26 = ['2025-07-23','2025-08-23','2025-09-22','2025-10-23','2025-11-22','2025-12-23',
        '2026-01-23','2026-02-20','2026-03-23']

BRANDS = ['OFF!', 'EXPOSIS', 'XO INSETO', 'SUPER REPELEX', 'SBP']
BRAND_SET = set(BRANDS)

# ════════════════════════════════════════════════════════════════════════════
# 1. Extrair dados da 1-Tabela-1
# ════════════════════════════════════════════════════════════════════════════
print('Lendo 1-Tabela-1...')
wb = openpyxl.load_workbook(XL, read_only=True, data_only=True)
ws = wb['1-Tabela-1']

xl = {}   # xl[market][brand][period_key] = share%
for i, row in enumerate(ws.iter_rows(values_only=True)):
    if i < 9: continue
    mkt, brand, prod, period, shr = row[0], row[2], row[3], row[4], row[8]
    if mkt is None or brand not in BRAND_SET: continue
    if prod is not None: continue          # brand-level only
    if shr is None: continue
    if mkt not in xl: xl[mkt] = {}
    if brand not in xl[mkt]: xl[mkt][brand] = {}
    key = period.strftime('%Y-%m-%d') if isinstance(period, datetime) else str(period)
    xl[mkt][brand][key] = shr
wb.close()
print(f'  {len(xl)} markets lidos do Excel')

# ── helpers ──────────────────────────────────────────────────────────────────
def v(mkt, brand, key, dp=2):
    """Retorna valor arredondado ou None."""
    val = xl.get(mkt, {}).get(brand, {}).get(key)
    if val is None: return None
    return round(val, dp)

def arr(mkt, brand, dates, dp=2):
    d = xl.get(mkt, {}).get(brand, {})
    return [round(d[k], dp) if k in d else 'null' for k in dates]

def js_val(x):
    return 'null' if x is None else str(x)

def js_arr(lst):
    return '[' + ','.join('null' if x == 'null' else str(x) for x in lst) + ']'

# ════════════════════════════════════════════════════════════════════════════
# 2. Construir novo MKTSHARE_OVERVIEW
# ════════════════════════════════════════════════════════════════════════════
# Ordem de markets: mantém os 69 existentes + adiciona 3 novos INA no fim
MARKET_ORDER = [
    'Farma Sul',
    'Farma CO','Farma Gde RJ','Farma Gde SP','Farma Int SP',
    'Farma MG+ES+Int RJ','Farma NE',
    'Farma Indep Sul','Farma Indep CO','Farma Indep Gde RJ',
    'Farma Indep Gde SP','Farma Indep Int SP','Farma Indep MG+ES+Int RJ','Farma Indep NE',
    'Farma Moderno Sul','Farma Moderno CO','Farma Moderno Gde RJ',
    'Farma Moderno Gde SP','Farma Moderno Int SP','Farma Moderno MG+ES+Int RJ','Farma Moderno NE',
    'T.BR Farma','T.BR Farma Indep','T.BR Farma Moderno',
    'INFC RS','INFC SC','INFC PR','INFC Curitiba','INFC Porto Alegre','INFC Sul',
    'INFC Int PR','INFC Int RS','INFC Cidade Gde Sul','INFC Cidade Peq+Med Sul',
    'INFC MG','INFC CO','INFC BA','INFC Belo Horizonte','INFC CE',
    'INFC Cidade Gde Gde RJ','INFC Cidade Gde CO','INFC Cidade Gde Gde SP',
    'INFC Cidade Gde Int SP','INFC Cidade Gde MG+ES+Int RJ','INFC Cidade Gde NE',
    'INFC Cidade Peq+Med CO','INFC Cidade Peq+Med Int SP',
    'INFC Cidade Peq+Med MG+ES+Int RJ','INFC Cidade Peq+Med NE',
    'INFC DF','INFC Fortaleza','INFC GO','INFC Gde RJ','INFC Gde SP',
    'INFC Int BA','INFC Int CE','INFC Int MG','INFC Int PE','INFC Int SP',
    'INFC MA+PI','INFC MG+ES+Int RJ','INFC Man+Bel+Ana','INFC Manaus',
    'INFC NE','INFC PE','INFC Recife','INFC SP','INFC Salvador',
    'T.BR INFC',
    # 3 novos
    'INA MG','INA Int MG','INA MG+ES+Int RJ',
]

def build_mso_entry(mkt):
    lines = []
    lines.append(f"  '{mkt}': {{")
    for b in BRANDS:
        f25  = v(mkt, b, 'FYTD25')
        f26  = v(mkt, b, 'FYTD26')
        if f25 is None and f26 is None:
            continue
        delta = round((f26 or 0) - (f25 or 0), 2) if f25 is not None and f26 is not None else 'null'
        monthly = arr(mkt, b, FY26)
        j25  = v(mkt, b, '2025-01-23')
        jf25 = v(mkt, b, '2025-02-20')
        mar25= v(mkt, b, '2025-03-23')

        # SBP mantém jan25/feb25 null (comportamento atual do dashboard)
        if b == 'SBP':
            j25 = None; jf25 = None; mar25 = None

        entry = (
            f"    '{b}': {{fytd25:{js_val(f25)}, fytd26:{js_val(f26)}, "
            f"delta:{js_val(delta)}, monthly:{js_arr(monthly)}, "
            f"jan25:{js_val(j25)}, feb25:{js_val(jf25)}"
        )
        # OFF! always includes mar25
        if b == 'OFF!':
            entry += f", mar25:{js_val(mar25)}"
        entry += '},'
        lines.append(entry)
    lines.append('  },')
    return '\n'.join(lines)

print('Gerando MKTSHARE_OVERVIEW...')
mso_lines = ['const MKTSHARE_OVERVIEW = {']
missing_mso = []
for mkt in MARKET_ORDER:
    if mkt not in xl:
        missing_mso.append(mkt)
        continue
    mso_lines.append(build_mso_entry(mkt))
mso_lines.append('};')
new_mso = '\n'.join(mso_lines)
if missing_mso:
    print(f'  AVISO: {len(missing_mso)} markets sem dados Excel: {missing_mso}')
print(f'  {len(MARKET_ORDER)-len(missing_mso)} markets gerados')

# ════════════════════════════════════════════════════════════════════════════
# 3. Construir novo SHR_TREND_DATA
# ════════════════════════════════════════════════════════════════════════════
def build_shr_entry(mkt):
    lines = []
    lines.append(f"  '{mkt}': {{")
    b_labels = {'OFF!': 'OFF!         ', 'EXPOSIS': 'EXPOSIS      ',
                'XO INSETO': 'XO INSETO    ', 'SUPER REPELEX': 'SUPER REPELEX',
                'SBP': 'SBP          '}
    for b in BRANDS:
        fy24 = arr(mkt, b, FY24)
        fy25 = arr(mkt, b, FY25)
        lines.append(f"    '{b}':          {{fy24:{js_arr(fy24)},fy25:{js_arr(fy25)}}},")
    lines.append('  },')
    return '\n'.join(lines)

print('Gerando SHR_TREND_DATA...')
shr_lines = ['const SHR_TREND_DATA = {']
missing_shr = []
for mkt in MARKET_ORDER:
    if mkt not in xl:
        missing_shr.append(mkt)
        continue
    shr_lines.append(build_shr_entry(mkt))
shr_lines.append('};')
new_shr = '\n'.join(shr_lines)
print(f'  {len(MARKET_ORDER)-len(missing_shr)} markets gerados')

# ════════════════════════════════════════════════════════════════════════════
# 4. Aplicar no dashboard
# ════════════════════════════════════════════════════════════════════════════
print(f'\nBacking up: {os.path.basename(BKP)}')
shutil.copy2(SRC, BKP)

with open(SRC, encoding='utf-8') as f:
    content = f.read()

orig_lines = len(content.splitlines())
c = content

# ── 4a. Substituir MKTSHARE_OVERVIEW ────────────────────────────────────────
mso_start_marker = 'const MKTSHARE_OVERVIEW = {'
mso_end_marker   = 'const MSO_MONTHS'

idx_mso_start = c.find(mso_start_marker)
idx_mso_end   = c.find(mso_end_marker, idx_mso_start)

# Find the '};\n' just before MSO_MONTHS
idx_close = c.rfind('\n};\n', idx_mso_start, idx_mso_end) + 1  # include \n
old_mso_block = c[idx_mso_start : idx_close + 3]  # '};' + \n

c = c.replace(old_mso_block, new_mso + '\n', 1)
print('MKTSHARE_OVERVIEW substituído ✓')

# ── 4b. Substituir SHR_TREND_DATA ────────────────────────────────────────────
shr_start_marker = 'const SHR_TREND_DATA = {'
shr_end_marker   = 'var _shrActiveBrand'

idx_shr_start = c.find(shr_start_marker)
idx_shr_end   = c.find(shr_end_marker, idx_shr_start)

idx_shr_close = c.rfind('\n};\n', idx_shr_start, idx_shr_end) + 1
old_shr_block = c[idx_shr_start : idx_shr_close + 3]

c = c.replace(old_shr_block, new_shr + '\n', 1)
print('SHR_TREND_DATA substituído ✓')

# ── 4c. Adicionar 3 novos markets ao dropdown ────────────────────────────────
old_infc_end = '          </optgroup>\n          <optgroup label="─ T.BR INFC ─">'
new_infc_end = (
    '          </optgroup>\n'
    '          <optgroup label="─ INA ─">\n'
    '          <option value="INA MG">INA MG</option>\n'
    '          <option value="INA Int MG">INA Int MG</option>\n'
    '          <option value="INA MG+ES+Int RJ">INA MG+ES+Int RJ</option>\n'
    '          </optgroup>\n'
    '          <optgroup label="─ T.BR INFC ─">'
)
if old_infc_end in c:
    c = c.replace(old_infc_end, new_infc_end, 1)
    print('Dropdown INA adicionado ✓')
else:
    print('AVISO: anchor dropdown INA não encontrado')

# ── 4d. Gravar ───────────────────────────────────────────────────────────────
with open(OUT, 'w', encoding='utf-8') as f:
    f.write(c)
shutil.copy2(OUT, SRC)
print(f'\nCopied to active: {os.path.basename(SRC)}')

new_lines_count = len(c.splitlines())
print(f'Linhas: {orig_lines} → {new_lines_count} ({new_lines_count-orig_lines:+d})')
print(f'Versão: {os.path.basename(OUT)}')

# ════════════════════════════════════════════════════════════════════════════
# 5. Log de divergências (Dashboard antigo vs Excel)
# ════════════════════════════════════════════════════════════════════════════
print('\n' + '='*70)
print('AUDIT LOG — Divergências corrigidas (amostra T.BR Farma)')
print('='*70)

# Parse original MKTSHARE_OVERVIEW from backup
with open(BKP, encoding='utf-8') as f:
    orig = f.read()

orig_tbrf = re.search(r"'T\.BR Farma':\s*\{.*?\},\s*'T\.BR Farma Indep'", orig, re.DOTALL)
if orig_tbrf:
    block = orig_tbrf.group(0)
    old_vals = {}
    for b in BRANDS:
        m = re.search(r"'"+re.escape(b)+r"':\s*\{fytd25:([\d.]+),\s*fytd26:([\d.]+),\s*delta:([-\d.]+)", block)
        if m: old_vals[b] = (float(m.group(1)), float(m.group(2)), float(m.group(3)))

print(f'{"Brand":<15} {"Old F25":>8} {"New F25":>8} {"ΔF25":>7} | {"Old F26":>8} {"New F26":>8} {"ΔF26":>7} | {"Old Δ":>7} {"New Δ":>7}')
print('-'*70)
for b in BRANDS:
    xf25 = round(xl.get('T.BR Farma',{}).get(b,{}).get('FYTD25',0), 2)
    xf26 = round(xl.get('T.BR Farma',{}).get(b,{}).get('FYTD26',0), 2)
    xd   = round(xf26 - xf25, 2)
    old  = old_vals.get(b, (0,0,0))
    print(f'{b:<15} {old[0]:>8.2f} {xf25:>8.2f} {xf25-old[0]:>+7.2f} | {old[1]:>8.2f} {xf26:>8.2f} {xf26-old[1]:>+7.2f} | {old[2]:>7.2f} {xd:>7.2f}')

# Verify T.BR Farma in new file
print('\n\nVERIFICAÇÃO — T.BR Farma no dashboard corrigido:')
new_tbrf = re.search(r"'T\.BR Farma':\s*\{.*?\},\s*'T\.BR Farma Indep'", c, re.DOTALL)
if new_tbrf:
    block = new_tbrf.group(0)
    for b in BRANDS:
        m = re.search(r"'"+re.escape(b)+r"':\s*\{fytd25:([\d.]+),\s*fytd26:([\d.]+),\s*delta:([-\d.]+)", block)
        if m:
            xf25_expected = round(xl.get('T.BR Farma',{}).get(b,{}).get('FYTD25',0), 2)
            xf26_expected = round(xl.get('T.BR Farma',{}).get(b,{}).get('FYTD26',0), 2)
            status = '✓' if abs(float(m.group(1))-xf25_expected)<0.01 and abs(float(m.group(2))-xf26_expected)<0.01 else '✗'
            print(f'  {status} {b}: fytd25={m.group(1)} (expected {xf25_expected}) | fytd26={m.group(2)} (expected {xf26_expected})')

print('\n✅ Correção completa aplicada.')
print(f'   Versão salva: {os.path.basename(OUT)}')
