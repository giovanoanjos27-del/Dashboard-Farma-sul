"""
Gera ESTOQUE_DATA com valores em CAIXAS (coluna E do Excel)
e aplica patch no dashboard HTML principal.

Estrutura do Estoque_Geral (linha 2 = cabecalhos, dados da linha 3):
  A(0) = Cliente
  B(1) = Marca
  C(2) = SKU
  D(3) = FATOR CX  (integer hardcoded)
  E(4) = Estoque Atual CAIXAS  (formula = F/D)
  F(5) = Estoque Atual Unidades
  G(6) = Venda Ref (Cx/mes) -- na pratica em unidades/mes
  H(7) = Cobertura (dias)
  I(8) = Status
  L(11) = Data Ref
"""

import openpyxl, warnings, math, re, shutil
from datetime import datetime
from pathlib import Path

warnings.filterwarnings('ignore')

# ── Paths ────────────────────────────────────────────────────────────────────
BASE = Path(r"C:\Users\valqu\OneDrive\Documentos\Claude\Projects\projeto Dashboard_farma_sul\Dashboard_farma_sul")
XLSX_TEMP = Path(r"C:\Users\valqu\AppData\Local\Temp\Planilha_Mestre_temp.xlsx")
DASH = BASE / "Dashboard_Farma_Sul_20260512_2220.html"
VERSOES = BASE / "versoes"
DOWNLOADS = Path.home() / "Downloads"

# ── Ler Estoque_Geral ────────────────────────────────────────────────────────
wb = openpyxl.load_workbook(XLSX_TEMP, data_only=True)
ws = wb['Estoque_Geral']

# Mapeamento nome Excel -> label JS
CLIENT_MAP = {
    'DD-GAM':    'DD-GAM',
    'São João':  'São João',
    'Nissei':    'Nissei',
    'Clamed':    'Clamed',
    'Panvel':    'Panvel',
    'DD-Gaúcha': 'DD-Gaúcha',
    'DD-Riomed': 'DD-Riomed',
}

STATUS_MAP = {
    '🔴 CRÍTICO':  '🔴 CRÍTICO',
    '⚠ ATENÇÃO':  '⚠ ATENÇÃO',
    '✅ OK':       '✅ OK',
    '🔴 CRÍTICO': '🔴 CRÍTICO',  # variações de encoding
    '⚠ ATENÇÃO': '⚠ ATENÇÃO',
    '✅ OK': '✅ OK',
}

def clean_status(s):
    if not s: return '✅ OK'
    s = str(s).strip()
    # normaliza: remove emoji encoding issues
    if 'CR' in s.upper() and ('TICO' in s.upper() or 'TICO' in s):
        return '🔴 CRÍTICO'
    if 'ATEN' in s.upper():
        return '⚠ ATENÇÃO'
    if 'OK' in s.upper():
        return '✅ OK'
    return s

def safe_round(v, d=1):
    if v is None: return 0
    try:
        return round(float(v), d)
    except (ValueError, TypeError):
        return 0

def safe_int(v):
    if v is None: return 0
    try:
        return int(round(float(v)))
    except (ValueError, TypeError):
        return 0

# Coleta dados por cliente
data = {}
for row in ws.iter_rows(min_row=3, values_only=True):
    cliente_raw = row[0]
    if not cliente_raw:
        continue
    cliente_raw = str(cliente_raw).strip()
    # Normaliza nome
    label = CLIENT_MAP.get(cliente_raw)
    if label is None:
        # tentativa fuzzy
        for k in CLIENT_MAP:
            if k.lower() in cliente_raw.lower() or cliente_raw.lower() in k.lower():
                label = CLIENT_MAP[k]
                break
    if label is None:
        label = cliente_raw

    marca     = str(row[1]).strip() if row[1] else ''
    sku       = str(row[2]).strip() if row[2] else ''
    fator     = row[3]   # D - FATOR CX
    est_cx    = row[4]   # E - Estoque CAIXAS (formula)
    est_un    = row[5]   # F - Estoque Unidades
    so_ref    = row[6]   # G - Venda Ref (unidades/mes)
    doh_val   = row[7]   # H - Cobertura dias
    status    = row[8]   # I - Status
    data_ref  = row[11]  # L - Data Ref

    if not sku:
        continue

    # CAIXAS: usar coluna E diretamente (arredonda para int)
    est = safe_int(est_cx)
    # SO em caixas = Venda Ref (unidades) / FATOR
    fator_val = float(fator) if fator else 12.0
    so_cx = safe_int(so_ref / fator_val) if so_ref else 0
    doh = safe_round(doh_val, 1)
    st  = clean_status(status)
    dr  = str(data_ref).strip() if data_ref else 'Abr/2026'

    if label not in data:
        data[label] = {'skus': [], 'data_ref': dr}
    data[label]['skus'].append({
        'marca': marca,
        'sku':   sku,
        'est':   est,
        'so':    so_cx,
        'doh':   doh,
        'status': st,
    })

# ── Gerar totais por cliente ──────────────────────────────────────────────────
def count_status(skus, target):
    return sum(1 for s in skus if target in s['status'])

result = {}
for label, d in data.items():
    skus = d['skus']
    est_total = sum(s['est'] for s in skus)
    so_total  = sum(s['so']  for s in skus)
    doh_medio = safe_round(sum(s['doh'] for s in skus) / len(skus), 1) if skus else 0
    result[label] = {
        'data_ref':  d['data_ref'],
        'est_total': est_total,
        'so_mes':    so_total,
        'doh':       doh_medio,
        'critico':   count_status(skus, 'CRÍTICO'),
        'atencao':   count_status(skus, 'ATENÇÃO'),
        'ok':        count_status(skus, 'OK'),
        'skus':      skus,
    }

# ── Gerar bloco JS ─────────────────────────────────────────────────────────────
def js_str(s):
    return '"' + str(s).replace('\\','\\\\').replace('"','\\"') + '"'

def js_sku(s):
    return (
        '{marca:' + js_str(s['marca']) +
        ',sku:'   + js_str(s['sku'])   +
        ',est:'   + str(s['est'])      +
        ',so:'    + str(s['so'])       +
        ',doh:'   + str(s['doh'])      +
        ',status:'+ js_str(s['status'])+
        '}'
    )

lines = ['const ESTOQUE_DATA = {']
client_order = ['DD-GAM','São João','Nissei','Clamed','Panvel','DD-Gaúcha','DD-Riomed']
for label in client_order:
    if label not in result:
        continue
    r = result[label]
    lines.append(f'  {js_str(label)}: {{')
    lines.append(f'    data_ref:{js_str(r["data_ref"])},')
    lines.append(f'    est_total:{r["est_total"]},')
    lines.append(f'    so_mes:{r["so_mes"]},')
    lines.append(f'    doh:{r["doh"]},')
    lines.append(f'    critico:{r["critico"]},atencao:{r["atencao"]},ok:{r["ok"]},')
    skus_js = ',\n      '.join(js_sku(s) for s in r['skus'])
    lines.append(f'    skus:[')
    lines.append(f'      {skus_js}')
    lines.append(f'    ]')
    lines.append(f'  }},')
lines.append('};')
new_block = '\n'.join(lines)

# ── Resumo para conferencia ─────────────────────────────────────────────────
print("=== RESUMO ESTOQUE_DATA (CAIXAS) ===")
for label in client_order:
    if label not in result:
        continue
    r = result[label]
    lbl = str(label).encode('ascii','replace').decode()
    print(f"\n{lbl}:")
    print(f"  est_total={r['est_total']} cx  |  so_mes={r['so_mes']} cx/mes  |  doh={r['doh']}d")
    print(f"  critico={r['critico']}  atencao={r['atencao']}  ok={r['ok']}")
    for s in r['skus'][:3]:
        nm = s['sku'][:40].encode('ascii','replace').decode()
        st = s['status'].encode('ascii','replace').decode()
        print(f"  SKU: {nm}  est={s['est']}cx  so={s['so']}cx/mes  doh={s['doh']}d  {st}")
    if len(r['skus']) > 3:
        print(f"  ... +{len(r['skus'])-3} SKUs")

print(f"\n=== BLOCO JS ({len(new_block)} chars) gerado OK ===")

# ── Patch no HTML ─────────────────────────────────────────────────────────────
print("\n=== APLICANDO PATCH NO DASHBOARD ===")
html = DASH.read_text(encoding='utf-8')

# Localiza bloco existente
pat = r'const ESTOQUE_DATA\s*=\s*\{.*?\};'
m = re.search(pat, html, re.DOTALL)
if not m:
    print("ERRO: ESTOQUE_DATA nao encontrado no HTML!")
    exit(1)

old_block = m.group(0)
print(f"Bloco antigo encontrado: {len(old_block)} chars")
print(f"Novo bloco: {len(new_block)} chars")

# Criar versao antes de editar
ts = datetime.now().strftime('%Y%m%d_%H%M')
versao = VERSOES / f"Dashboard_Farma_Sul_{ts}_EstoqueCaixas.html"
shutil.copy(DASH, versao)
print(f"Versao salva: {versao.name}")

# Substituir
new_html = html[:m.start()] + new_block + html[m.end():]
DASH.write_text(new_html, encoding='utf-8')
print(f"Dashboard atualizado: {DASH.name}")

# Copiar para Downloads
dl = DOWNLOADS / f"Dashboard_FarmaSul_Giovano_{ts}.html"
shutil.copy(DASH, dl)
print(f"Copia em Downloads: {dl.name}")
print("\nDONE.")
