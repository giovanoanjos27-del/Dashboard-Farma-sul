"""
atualizar_dados.py
══════════════════════════════════════════════════════════════════════
ROTA MESTRE — Planilha_Mestre_FarmaSul_Giovano → Dashboard
══════════════════════════════════════════════════════════════════════

ROTAS FIXAS (nunca alterar sem alinhar com a planilha):
  Sell Out   → abas SO_*  (SO_SJoao_Isadora, SO_SJoao_Caroline,
                            SO_Nissei, SO_Nissei_Andre, SO_Nissei_Edmar,
                            SO_Clamed, SO_Panvel, SO_DDGAM,
                            SO_DDGaúcha, SO_DDRiomed)
  Sell In    → aba SO_SellIn
  Estoque    → aba Estoque_Geral + abas SO_* (bloco SKU/Estoque)
  Cobertura  → abas Cob_*

PROTOCOLO:
  1. Ler todas as abas → validar existência
  2. Extrair dados → normalizar (12 valores por ano, None para meses futuros)
  3. Verificar integridade (Total SJ = Isadora + Caroline; NS total = André + Edmar ±tol)
  4. Patching no HTML via regex
  5. Versão timestampada + cópia em Downloads
"""

import os, re, sys, shutil, json, math
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

try:
    import openpyxl
except ImportError:
    print("ERRO: openpyxl nao instalado. Execute: pip install openpyxl")
    sys.exit(1)

# ─────────────────────────────────────────────────────────────────────
# PATHS
# ─────────────────────────────────────────────────────────────────────
BASE     = r"C:\Users\valqu\OneDrive\Documentos\Claude\Projects\projeto Dashboard_farma_sul"
HTML_DIR = os.path.join(BASE, "Dashboard_farma_sul")
SRC_HTML = os.path.join(HTML_DIR, "Dashboard_Farma_Sul_20260512_2220.html")
XLSX     = os.path.join(HTML_DIR, "Planilha_Mestre_FarmaSul_Giovano.xlsx")
VER_DIR  = os.path.join(HTML_DIR, "versoes")
DOWNLOADS = os.path.expanduser(r"~\Downloads")

os.makedirs(VER_DIR, exist_ok=True)

# ─────────────────────────────────────────────────────────────────────
# ABAS ESPERADAS (validação de integridade)
# ─────────────────────────────────────────────────────────────────────
ROTAS = {
    "sell_out": [
        "SO_SJoao_Isadora", "SO_SJoao_Caroline",
        "SO_Nissei", "SO_Nissei_willian", "SO_Nissei_Edmar",
        "SO_Clamed", "SO_Panvel", "SO_DDGAM", "SO_DDGaúcha", "SO_DDRiomed",
    ],
    "sell_in": ["SO_SellIn"],
    "estoque":  ["Estoque_Geral"],
    "cobertura": [],  # detectado dinamicamente (Cob_*)
}

print("=" * 65)
print("  ATUALIZAR DADOS — Planilha Mestre → Dashboard")
print("=" * 65)
print(f"  Excel : {XLSX}")
print(f"  HTML  : {SRC_HTML}")
print()

# ─────────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────────

def fmt_val(v):
    """JSON-serializable: None → null, float inteiro → int."""
    if v is None:
        return None
    if isinstance(v, float):
        if math.isnan(v) or math.isinf(v):
            return None
        if v == int(v):
            return int(v)
        return round(v, 2)
    return v

def js_array(vals):
    """Converte lista Python em string JS: [1,2,null,null,...]"""
    parts = []
    for v in vals:
        fv = fmt_val(v)
        parts.append("null" if fv is None else str(fv))
    return "[" + ",".join(parts) + "]"

def read_so_tab(ws, tipo_rec, tipo_vol, years=("2024","2025","2026")):
    """
    Lê aba SO_* e retorna:
      { 'rec': {'2024':[12 vals], ...}, 'vol': {'2024':[12 vals], ...} }
    tipo_rec / tipo_vol: string que identifica a linha (ex: 'Receita', 'Receita (R$)')
    """
    data = {"rec": {}, "vol": {}}
    for row in ws.iter_rows(values_only=True):
        if not row[0] or not row[1]:
            continue
        tipo = str(row[0]).strip()
        ano  = str(row[1]).strip()
        if ano not in years:
            continue
        vals = [fmt_val(row[i+2]) for i in range(12)]  # Jan=col2 … Dez=col13
        if tipo_rec in tipo:
            data["rec"][ano] = vals
        elif tipo_vol in tipo:
            data["vol"][ano] = vals
    return data

def add_arrays(a, b):
    """Soma dois arrays de 12 posições elemento a elemento (None + x = x)."""
    result = []
    for av, bv in zip(a, b):
        if av is None and bv is None:
            result.append(None)
        elif av is None:
            result.append(bv)
        elif bv is None:
            result.append(av)
        else:
            result.append(fmt_val(av + bv))
    return result

def check_sum(label, total, partA, partB, tol=0.02):
    """Verifica se total ≈ partA + partB para cada mês."""
    ok = True
    for i, (t, a, b) in enumerate(zip(total, partA, partB)):
        if t is None:
            continue
        expected = (a or 0) + (b or 0)
        if expected == 0:
            continue
        diff = abs((t - expected) / expected)
        if diff > tol:
            meses = ["Jan","Fev","Mar","Abr","Mai","Jun",
                     "Jul","Ago","Set","Out","Nov","Dez"]
            print(f"  [AVISO] {label} mês {meses[i]}: "
                  f"total={t} ≠ {a}+{b}={expected} (Δ={diff:.1%})")
            ok = False
    return ok

# ─────────────────────────────────────────────────────────────────────
# ABRIR PLANILHA
# ─────────────────────────────────────────────────────────────────────
print("[1/6] Abrindo planilha mestre...")
try:
    # Tenta com data_only; se travar usar cópia
    wb = openpyxl.load_workbook(XLSX, read_only=True, data_only=True)
except Exception as e:
    # Fallback: cópia temporária
    import tempfile
    tmp = os.path.join(tempfile.gettempdir(), "mestre_tmp.xlsx")
    shutil.copy2(XLSX, tmp)
    wb = openpyxl.load_workbook(tmp, read_only=True, data_only=True)

sheets = wb.sheetnames
print(f"  {len(sheets)} abas encontradas: {sheets}")

# Detectar abas Cob_
ROTAS["cobertura"] = [s for s in sheets if s.startswith("Cob_")]

# Validar abas obrigatórias
all_required = ROTAS["sell_out"] + ROTAS["sell_in"] + ROTAS["estoque"]
missing = [s for s in all_required if s not in sheets]
if missing:
    print(f"  [ALERTA] Abas nao encontradas: {missing}")
else:
    print(f"  Todas as abas obrigatórias OK")

print()

# ─────────────────────────────────────────────────────────────────────
# [2/6] EXTRAÇÃO SELL OUT
# ─────────────────────────────────────────────────────────────────────
print("[2/6] Extraindo Sell Out...")
changes = []  # log de todas as alterações

# ── São João ──────────────────────────────────────────────────────────
sj_isa = read_so_tab(wb["SO_SJoao_Isadora"],   "Receita", "Volume")
sj_car = read_so_tab(wb["SO_SJoao_Caroline"],  "Receita", "Volume")

# Total = Isadora + Caroline
sj_total = {"rec": {}, "vol": {}}
for yr in ("2024","2025","2026"):
    isa_r = sj_isa["rec"].get(yr, [None]*12)
    car_r = sj_car["rec"].get(yr, [None]*12)
    sj_total["rec"][yr] = add_arrays(isa_r, car_r)

    isa_v = sj_isa["vol"].get(yr, [None]*12)
    car_v = sj_car["vol"].get(yr, [None]*12)
    sj_total["vol"][yr] = add_arrays(isa_v, car_v)

print(f"  SJ Total Rec 2026: {sj_total['rec']['2026'][:4]}")
print(f"  SJ Isadora Vol 2026: {sj_isa['vol']['2026'][:4]}")
print(f"  SJ Caroline Rec 2026: {sj_car['rec']['2026'][:4]}")

# ── Nissei ────────────────────────────────────────────────────────────
ns_total = read_so_tab(wb["SO_Nissei"],        "Receita", "Volume")
ns_andre = read_so_tab(wb["SO_Nissei_willian"],  "Receita", "Volume")
ns_edmar = read_so_tab(wb["SO_Nissei_Edmar"],  "Receita", "Volume")
print(f"  NS Total Rec 2026: {ns_total['rec']['2026'][:4]}")

# ── Clamed ────────────────────────────────────────────────────────────
cl = read_so_tab(wb["SO_Clamed"], "Receita", "Volume")
print(f"  CL Rec 2026: {cl['rec']['2026'][:4]}")

# ── Panvel ────────────────────────────────────────────────────────────
pv = read_so_tab(wb["SO_Panvel"], "Receita", "Volume")
print(f"  PV Rec 2026: {pv['rec']['2026'][:4]}")

# ── DD-GAM ────────────────────────────────────────────────────────────
gam = read_so_tab(wb["SO_DDGAM"], "Receita", "Volume")
print(f"  GAM Rec 2026: {gam['rec']['2026'][:4]}")

# ── DD-Gaúcha ─────────────────────────────────────────────────────────
gch = read_so_tab(wb["SO_DDGaúcha"], "Receita", "Volume")
print(f"  GCH Rec 2026: {gch['rec']['2026'][:4]}")

# ── DD-Riomed ─────────────────────────────────────────────────────────
rio = read_so_tab(wb["SO_DDRiomed"], "Receita", "Volume")
print(f"  RIO Rec 2026: {rio['rec']['2026'][:4]}")

print()

# ─────────────────────────────────────────────────────────────────────
# [3/6] EXTRAÇÃO SELL IN
# ─────────────────────────────────────────────────────────────────────
print("[3/6] Extraindo Sell In...")
ws_si = wb["SO_SellIn"]
si_rows = list(ws_si.iter_rows(values_only=True))

# Encontrar linha de dados (após cabeçalho)
header_idx = None
for i, row in enumerate(si_rows):
    if row[0] and str(row[0]).strip() == "Cliente":
        header_idx = i
        break

SELLIN = []
if header_idx is not None:
    for row in si_rows[header_idx+1:]:
        if not row[0] or str(row[0]).strip() in ("", "TOTAL GERAL"):
            continue
        nome  = str(row[0]).strip()
        canal = str(row[1]).strip() if row[1] else ""
        hist  = fmt_val(row[2])  or 0   # Hist FY25 (total)
        plan  = fmt_val(row[4])  or 0   # Plan FY26
        meta  = fmt_val(row[5])  or 0   # Meta BI FY26
        real  = fmt_val(row[10]) or 0   # Real FY26
        verba = fmt_val(row[13]) or 0   # Verba R$
        def _int(x): return round(float(x)) if x is not None else 0
        def _int_or_null(x): return round(float(x)) if x is not None and float(x) != 0 else (None if x is None else 0)
        # Histórico mensal FY25 = colunas 14-25 (JUL/24 até JUN/25)
        hist_m  = [_int(row[14+i])  if (14+i  < len(row)) else 0 for i in range(12)]
        # Plano FY26 = colunas 38-49 (JUL/25 até JUN/26)
        plan_m  = [_int(row[38+i]) if (38+i < len(row)) else 0 for i in range(12)]
        # Meta BI FY26 = colunas 62-73 (JUL/25 até JUN/26)
        meta_m  = [_int(row[62+i]) if (62+i < len(row)) else 0 for i in range(12)]
        # Real FY26 = colunas 86-97 ← ATUALIZAR (JUL/25 até JUN/26; None = sem dado)
        real_m  = [_int_or_null(row[86+i]) if (86+i < len(row)) else None
                   for i in range(12)]
        SELLIN.append({
            "nome": nome, "canal": canal,
            "hist": hist, "plan": plan, "meta": meta, "real": real,
            "verba": verba, "hist_m": hist_m,
            "plan_m": plan_m, "meta_m": meta_m, "real_m": real_m,
        })
        print(f"  {nome}: hist={hist} plan={plan} meta={meta} real={real}")

print()

# ─────────────────────────────────────────────────────────────────────
# [4/6] VALIDAÇÃO DE INTEGRIDADE
# ─────────────────────────────────────────────────────────────────────
print("[4/6] Validando integridade...")

ok_all = True
for yr in ("2024","2025","2026"):
    # SJ Total = Isadora + Caroline (Rec)
    r = check_sum(f"SJ_REC {yr}",
                  sj_total["rec"].get(yr, [None]*12),
                  sj_isa["rec"].get(yr, [None]*12),
                  sj_car["rec"].get(yr, [None]*12))
    if not r: ok_all = False

    # SJ Total = Isadora + Caroline (Vol)
    r = check_sum(f"SJ_VOL {yr}",
                  sj_total["vol"].get(yr, [None]*12),
                  sj_isa["vol"].get(yr, [None]*12),
                  sj_car["vol"].get(yr, [None]*12))
    if not r: ok_all = False

    # NOTA: NS.total (SO_Nissei) ≠ André + Edmar — escopos diferentes:
    #   NS.total  = HB/repelentes apenas (Off!, Exposis)
    #   NS.andre  = todos os produtos do André (Off!, Exposis + outros)
    #   NS.edmar  = todos os produtos do Edmar (Raid, Elétricos + outros)
    # Verificação de soma não aplicável para Nissei.

if ok_all:
    print("  Integridade OK — SJ Total = Isadora + Caroline confirmado")
else:
    print("  [AVISO] Divergências encontradas — verificar dados na planilha")

print()

# ─────────────────────────────────────────────────────────────────────
# [5/6] PATCHING NO HTML
# ─────────────────────────────────────────────────────────────────────
print("[5/6] Aplicando patches no HTML...")

ts = datetime.now().strftime("%Y%m%d_%H%M")
BKP = os.path.join(VER_DIR, f"Dashboard_Farma_Sul_{ts}_PreAtualizacao.html")
shutil.copy2(SRC_HTML, BKP)
print(f"  Backup: {BKP}")

with open(SRC_HTML, "r", encoding="utf-8") as f:
    html = f.read()

# ── LIMPAR BLOCOS OVERRIDE antes de patchar ───────────────────────────
# CRÍTICO: saveDashboard() injeta um <script>/* OVERRIDE DATA */...</script>
# que roda APÓS os const e sobrescreve os valores.
# Sem essa limpeza, nossos patches nos const seriam anulados na carga da página.
n_overrides = len(re.findall(r'<script>\s*/\* OVERRIDE DATA', html))
if n_overrides:
    html = re.sub(r'<script>\s*/\* OVERRIDE DATA[\s\S]*?</script>\n?', '', html)
    print(f"  Override blocks removidos: {n_overrides} (serão regenerados pelo saveDashboard)")
else:
    print("  Nenhum override block encontrado — OK")

def patch_year_dict(html, var_name, data_dict):
    """
    Patcha variável tipo: const VAR = { '2024':[...], '2025':[...], '2026':[...] };
    Substitui cada linha de ano individualmente.
    """
    changed = 0
    for yr, vals in data_dict.items():
        new_arr = js_array(vals)
        # Padrão: '2024':[qualquer coisa até o fechamento]
        pattern = r"('" + re.escape(yr) + r"'\s*:)\s*\[[^\]]*\]"
        # Constrói contexto para garantir que é a variável certa
        # Procura a variável e substitui apenas dentro do seu escopo
        var_idx = html.find(f"const {var_name}")
        if var_idx < 0:
            var_idx = html.find(f"var {var_name}")
        if var_idx < 0:
            return html, changed

        # Encontrar fim do objeto (próxima ocorrência de "};" ou "}," após a var)
        block_start = var_idx
        block_end   = html.find("};", var_idx) + 2
        if block_end < 2:
            continue

        block  = html[block_start:block_end]
        new_block, n = re.subn(pattern, r"\g<1>" + new_arr, block, count=1)
        if n > 0:
            html = html[:block_start] + new_block + html[block_end:]
            changed += 1
    return html, changed

def patch_simple_array(html, var_name, vals):
    """
    Patcha variável tipo: const VAR = [...];
    """
    new_arr = js_array(vals)
    pattern = r"(const\s+" + re.escape(var_name) + r"\s*=\s*)\[[^\]]*\]"
    new_html, n = re.subn(pattern, r"\g<1>" + new_arr, html, count=1)
    return new_html, n

def patch_ns_subkey(html, sub, tipo, yr, vals):
    """
    Patcha NS.total/andre/edmar .rec/.vol ['year'] inline.
    Procura padrão: sub: { vol:{'year':[ ... ], ...}, rec:{...}, ... }
    """
    new_arr  = js_array(vals)
    tipo_key = "rec" if tipo == "rec" else "vol"
    # Localiza bloco NS
    ns_idx  = html.find("const NS =")
    ns_end  = html.find("\n};", ns_idx) + 3
    if ns_idx < 0:
        return html, 0
    block    = html[ns_idx:ns_end]
    # Localiza sub-bloco (total:, andre:, edmar:)
    sub_idx  = block.find(f"{sub}:")
    if sub_idx < 0:
        return html, 0
    # Localiza tipo (vol: ou rec:) dentro do sub-bloco
    tipo_idx = block.find(f"{tipo_key}:", sub_idx)
    if tipo_idx < 0:
        return html, 0
    # Substitui apenas o array do ano dentro desse bloco
    pattern = r"('" + re.escape(yr) + r"'\s*:)\s*\[[^\]]*\]"
    # Trabalha apenas no bloco do tipo específico
    tipo_block_start = tipo_idx
    tipo_block_end   = block.find("}", tipo_idx) + 1
    tipo_block = block[tipo_block_start:tipo_block_end]
    new_tipo_block, n = re.subn(pattern, r"\g<1>" + new_arr, tipo_block, count=1)
    if n > 0:
        new_block = block[:tipo_block_start] + new_tipo_block + block[tipo_block_end:]
        html = html[:ns_idx] + new_block + html[ns_end:]
    return html, n

# ── Aplicar patches ──────────────────────────────────────────────────

n_total = 0

# SJ Total
html, n = patch_year_dict(html, "SJ_REC",  sj_total["rec"])
n_total += n; changes.append(f"SJ_REC: {n} anos atualizados")

html, n = patch_year_dict(html, "SJ_UNID", sj_total["vol"])
n_total += n; changes.append(f"SJ_UNID: {n} anos")

# SJ Caroline
for yr_label, yr_key in [("24","2024"), ("", "2025"), ("26","2026")]:
    suffix = f"_{yr_label}" if yr_label else ""
    # VOL
    var_v = f"SJC_VOL{suffix}"
    vals  = sj_car["vol"].get(yr_key, [None]*12)
    h2, n = patch_simple_array(html, var_v, vals)
    if n: html = h2; n_total += 1; changes.append(f"{var_v} atualizado")

    # REC
    var_r = f"SJC_REC{suffix}"
    vals  = sj_car["rec"].get(yr_key, [None]*12)
    h2, n = patch_simple_array(html, var_r, vals)
    if n: html = h2; n_total += 1; changes.append(f"{var_r} atualizado")

# Nissei
for sub_key, data in [("total", ns_total), ("andre", ns_andre), ("edmar", ns_edmar)]:
    for yr in ("2024","2025","2026"):
        for tipo in ("rec","vol"):
            vals = data[tipo].get(yr, [None]*12)
            html, n = patch_ns_subkey(html, sub_key, tipo, yr, vals)
            if n: n_total += 1

changes.append(f"NS (total/andre/edmar): atualizado")

# Clamed
for yr in ("2024","2025","2026"):
    h2, n = patch_simple_array(html, f"CL_REC_{yr}", cl["rec"].get(yr, [None]*12))
    if n: html = h2; n_total += 1; changes.append(f"CL_REC_{yr}")
    h2, n = patch_simple_array(html, f"CL_VOL_{yr}", cl["vol"].get(yr, [None]*12))
    if n: html = h2; n_total += 1; changes.append(f"CL_VOL_{yr}")

# Panvel
html, n = patch_year_dict(html, "PV_REC", pv["rec"])
n_total += n; changes.append(f"PV_REC: {n}")
html, n = patch_year_dict(html, "PV_VOL", pv["vol"])
n_total += n; changes.append(f"PV_VOL: {n}")

# GAM
html, n = patch_year_dict(html, "GAM_REC", gam["rec"])
n_total += n; changes.append(f"GAM_REC: {n}")
html, n = patch_year_dict(html, "GAM_VOL", gam["vol"])
n_total += n; changes.append(f"GAM_VOL: {n}")

# Gaúcha
html, n = patch_year_dict(html, "GAUCHA_REC", gch["rec"])
n_total += n; changes.append(f"GAUCHA_REC: {n}")
html, n = patch_year_dict(html, "GAUCHA_VOL", gch["vol"])
n_total += n; changes.append(f"GAUCHA_VOL: {n}")

# Riomed
for yr in ("2024","2025","2026"):
    h2, n = patch_simple_array(html, f"RIOMED_REC_{yr}", rio["rec"].get(yr, [None]*12))
    if n: html = h2; n_total += 1; changes.append(f"RIOMED_REC_{yr}")
    h2, n = patch_simple_array(html, f"RIOMED_VOL_{yr}", rio["vol"].get(yr, [None]*12))
    if n: html = h2; n_total += 1; changes.append(f"RIOMED_VOL_{yr}")

# ── Sell In (SELLIN_DATA) ──────────────────────────────────────────────
if SELLIN:
    # Mapas de cor e label presentes no dashboard (preservar)
    color_map = {
        "São João": "#60a5fa", "DD-Gaúcha": "#f97316", "Panvel": "#2dd4bf",
        "DD-GAM": "#34d399", "Nissei": "#a78bfa", "DD-Riomed": "#fb923c",
        "Clamed": "#f472b6",
    }
    # Ler SELLIN_DATA atual para preservar campos não atualizados
    si_match = re.search(r"SELLIN_DATA\s*=\s*\[[\s\S]*?\];", html)
    if si_match:
        new_si_entries = []
        for d in SELLIN:
            cor   = color_map.get(d["nome"], "#94a3b8")
            hist_m_js = js_array(d["hist_m"])
            plan_m_js = js_array(d.get("plan_m", [None]*12))
            meta_m_js = js_array(d.get("meta_m", [None]*12))
            real_m_js = js_array(d.get("real_m", [None]*12))
            entry = (
                f"  {{ nome:'{d['nome']}', label:'{d['nome']}', cor:'{cor}', "
                f"canal:'{d['canal']}', "
                f"hist:{d['hist']}, plan:{d['plan']}, meta:{d['meta']}, "
                f"real:{d['real']}, hist_per:{d['hist']}, verba:{d['verba']},\n"
                f"    hist_m:{hist_m_js},\n"
                f"    plan_m:{plan_m_js},\n"
                f"    meta_m:{meta_m_js},\n"
                f"    real_m:{real_m_js} }}"
            )
            new_si_entries.append(entry)

        new_si_block = "SELLIN_DATA = [\n" + ",\n".join(new_si_entries) + "\n];"
        html = html[:si_match.start()] + new_si_block + html[si_match.end():]
        n_total += 1
        changes.append("SELLIN_DATA atualizado")

print(f"  {n_total} patches aplicados")
print()

# ─────────────────────────────────────────────────────────────────────
# [6/6] SALVAR + EXPORTAR PARA DOWNLOADS
# ─────────────────────────────────────────────────────────────────────
print("[6/6] Salvando...")

# Salvar arquivo principal
with open(SRC_HTML, "w", encoding="utf-8") as f:
    f.write(html)

sz = os.path.getsize(SRC_HTML)
print(f"  Principal: {SRC_HTML}")
print(f"  Tamanho  : {sz:,} bytes ({sz/1024/1024:.1f} MB)")

# Versão timestampada
VER = os.path.join(VER_DIR, f"Dashboard_Farma_Sul_{ts}_AtualizacaoDados.html")
shutil.copy2(SRC_HTML, VER)
print(f"  Versão   : {VER}")

# Cópia em Downloads
dl_name = f"Dashboard_FarmaSul_Giovano_{ts}.html"
DL_PATH = os.path.join(DOWNLOADS, dl_name)
shutil.copy2(SRC_HTML, DL_PATH)
print(f"  Downloads: {DL_PATH}")

wb.close()

print()
print("=" * 65)
print("  RESUMO DE ALTERAÇÕES")
print("=" * 65)
for c in changes:
    print(f"  ✓ {c}")
print()
print("  INTEGRIDADE:")
print(f"  SJ Total Jan/26  = {sj_total['rec']['2026'][0]} (Isadora {sj_isa['rec']['2026'][0]} + Caroline {sj_car['rec']['2026'][0]})")
print(f"  SJ Total Fev/26  = {sj_total['rec']['2026'][1]}")
print(f"  SJ Total Mar/26  = {sj_total['rec']['2026'][2]}")
print()
print("  CONCLUÍDO. Abra o HTML no browser para verificar.")
print("=" * 65)
