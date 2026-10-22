"""
fix_isadora_sellout.py
Correcoes no dashboard:
1. SJ_UNID 2026 e SJ_REC 2026 — Fev/Mar errados (divergem da Planilha Mestre)
2. Canvas 0px — 33 graficos salvos com height:0/width:0 nao renderizam

Fonte da verdade: Planilha_Mestre_FarmaSul_Giovano.xlsx
  SJ_UNID 2026 correto: [36113, 32606, 24361, 18774, null, ...]
  SJ_REC  2026 correto: [1119195, 969122, 731574, 588859, null, ...]
"""
import os, shutil, re
from datetime import datetime

BASE     = r"C:\Users\valqu\OneDrive\Documentos\Claude\Projects\projeto Dashboard_farma_sul"
HTML_DIR = os.path.join(BASE, "Dashboard_farma_sul")
SRC_HTML = os.path.join(HTML_DIR, "Dashboard_Farma_Sul_20260512_2220.html")
VER_DIR  = os.path.join(HTML_DIR, "versoes")

# ── Versao de backup ──────────────────────────────────────────────────────────
ts = datetime.now().strftime("%Y%m%d_%H%M")
os.makedirs(VER_DIR, exist_ok=True)
VER_HTML = os.path.join(VER_DIR, f"Dashboard_Farma_Sul_{ts}_PreIsadoraFix.html")
shutil.copy2(SRC_HTML, VER_HTML)
print(f"Backup: {VER_HTML}")

# ── Ler HTML ──────────────────────────────────────────────────────────────────
with open(SRC_HTML, "r", encoding="utf-8") as f:
    content = f.read()

original_len = len(content)
changes = []

# ═══════════════════════════════════════════════════════════════
# FIX 1: Dados SJ_UNID e SJ_REC para 2026
# ═══════════════════════════════════════════════════════════════

# SJ_UNID 2026 — Fev=27873->32606, Mar=26552->24361
old_unid = "  '2026':[36113,27873,26552,18774,null,null,null,null,null,null,null,null],"
new_unid = "  '2026':[36113,32606,24361,18774,null,null,null,null,null,null,null,null],"
if old_unid in content:
    content = content.replace(old_unid, new_unid, 1)
    changes.append("SJ_UNID 2026: Fev 27873->32606, Mar 26552->24361")
    print(f"[OK] SJ_UNID 2026 corrigido")
else:
    # Tentar variacao sem espacos
    old_unid2 = "'2026':[36113,27873,26552,18774,null,null,null,null,null,null,null,null]"
    new_unid2 = "'2026':[36113,32606,24361,18774,null,null,null,null,null,null,null,null]"
    if old_unid2 in content:
        content = content.replace(old_unid2, new_unid2, 1)
        changes.append("SJ_UNID 2026: Fev 27873->32606, Mar 26552->24361")
        print(f"[OK] SJ_UNID 2026 corrigido (variante)")
    else:
        print(f"[WARN] SJ_UNID 2026 nao encontrado — verificar manualmente")
        # Mostrar o que existe
        idx = content.find('const SJ_UNID')
        print(f"  Atual: {content[idx:idx+200]}")

# SJ_REC 2026 — Fev=843257->969122, Mar=778253->731574
old_rec = "  '2026':[1119195,843257,778253,588859,null,null,null,null,null,null,null,null],"
new_rec = "  '2026':[1119195,969122,731574,588859,null,null,null,null,null,null,null,null],"
if old_rec in content:
    content = content.replace(old_rec, new_rec, 1)
    changes.append("SJ_REC 2026: Fev 843257->969122, Mar 778253->731574")
    print(f"[OK] SJ_REC 2026 corrigido")
else:
    old_rec2 = "'2026':[1119195,843257,778253,588859,null,null,null,null,null,null,null,null]"
    new_rec2 = "'2026':[1119195,969122,731574,588859,null,null,null,null,null,null,null,null]"
    if old_rec2 in content:
        content = content.replace(old_rec2, new_rec2, 1)
        changes.append("SJ_REC 2026: Fev 843257->969122, Mar 778253->731574")
        print(f"[OK] SJ_REC 2026 corrigido (variante)")
    else:
        print(f"[WARN] SJ_REC 2026 nao encontrado — verificar manualmente")
        idx = content.find('const SJ_REC')
        print(f"  Atual: {content[idx:idx+300]}")

# ═══════════════════════════════════════════════════════════════
# FIX 2: Canvas 0-dimension — limpar style inline antes de new Chart()
# ═══════════════════════════════════════════════════════════════
# Adicionar reset de canvas em renderLineChart (antes de "var chart = new Chart(ctx,")
# e em renderAnoChart (antes de "var existingChart = Chart.getChart(canvas)")

CANVAS_RESET = """  // Fix: reset canvas para nao herdlar height:0px/width:0px do estado salvo
  ctx.removeAttribute('width'); ctx.removeAttribute('height');
  if(ctx.style) { ctx.style.width=''; ctx.style.height=''; }
"""

CANVAS_RESET_ANO = """  // Fix: reset canvas para nao herdar height:0px/width:0px do estado salvo
  canvas.removeAttribute('width'); canvas.removeAttribute('height');
  if(canvas.style) { canvas.style.width=''; canvas.style.height=''; }
"""

# renderLineChart: inserir antes de "var chart = new Chart(ctx,"
anchor_line = "  var chart = new Chart(ctx, {"
if CANVAS_RESET.strip() not in content:
    if anchor_line in content:
        content = content.replace(anchor_line, CANVAS_RESET + anchor_line, 1)
        changes.append("renderLineChart: canvas reset antes de new Chart()")
        print(f"[OK] renderLineChart: canvas reset adicionado")
    else:
        print(f"[WARN] anchor renderLineChart nao encontrado")
else:
    print(f"[INFO] renderLineChart: canvas reset ja existe")

# renderAnoChart: inserir antes de "var existingChart = Chart.getChart(canvas)"
anchor_ano = "  var existingChart = Chart.getChart(canvas);"
if CANVAS_RESET_ANO.strip() not in content:
    if anchor_ano in content:
        content = content.replace(anchor_ano, CANVAS_RESET_ANO + anchor_ano, 1)
        changes.append("renderAnoChart: canvas reset antes de Chart.getChart()")
        print(f"[OK] renderAnoChart: canvas reset adicionado")
    else:
        print(f"[WARN] anchor renderAnoChart nao encontrado")
else:
    print(f"[INFO] renderAnoChart: canvas reset ja existe")

# ═══════════════════════════════════════════════════════════════
# FIX 3: Melhorar contraste das legendas do line chart
# ═══════════════════════════════════════════════════════════════
# A legenda estatica no HTML tem cores fracas — tornar mais vibrante
OLD_LEGEND = (
    '<span style="display:flex;align-items:center;gap:5px;font-size:10px;font-weight:500;color:#D1D5DB;">'
    '<span style="width:14px;height:2px;background:#3b82f6;display:inline-block;border-radius:2px;"></span>2024</span>'
    '<span style="display:flex;align-items:center;gap:5px;font-size:10px;font-weight:500;color:#D1D5DB;">'
    '<span style="width:14px;height:2px;background:#2dd4bf;display:inline-block;border-radius:2px;"></span>2025</span>'
    '<span style="display:flex;align-items:center;gap:5px;font-size:10px;font-weight:700;color:#34d399;">'
    '<span style="width:20px;height:3px;background:#34d399;display:inline-block;border-radius:2px;'
    'background:repeating-linear-gradient(90deg,#34d399 0px,#34d399 4px,transparent 4px,transparent 8px);"></span>2026</span>'
)
NEW_LEGEND = (
    '<span style="display:flex;align-items:center;gap:5px;font-size:11px;font-weight:700;color:#60a5fa;">'
    '<span style="width:16px;height:2.5px;background:#3b82f6;display:inline-block;border-radius:2px;"></span>2024</span>'
    '<span style="display:flex;align-items:center;gap:5px;font-size:11px;font-weight:700;color:#2dd4bf;">'
    '<span style="width:16px;height:2.5px;background:#2dd4bf;display:inline-block;border-radius:2px;"></span>2025</span>'
    '<span style="display:flex;align-items:center;gap:5px;font-size:11px;font-weight:800;color:#34d399;">'
    '<span style="width:20px;height:3px;display:inline-block;border-radius:2px;'
    'background:repeating-linear-gradient(90deg,#34d399 0px,#34d399 5px,transparent 5px,transparent 9px);"></span>2026</span>'
)
if OLD_LEGEND in content:
    content = content.replace(OLD_LEGEND, NEW_LEGEND, 1)
    changes.append("Legenda sj-line: cores mais vibrantes (11px/700/800)")
    print(f"[OK] Legenda sj-line melhorada")
else:
    print(f"[INFO] Legenda sj-line: nao encontrado exato, pulando")

# ═══════════════════════════════════════════════════════════════
# GRAVAR
# ═══════════════════════════════════════════════════════════════
print(f"\nAlteracoes: {len(changes)}")
for c in changes:
    print(f"  - {c}")

with open(SRC_HTML, "w", encoding="utf-8") as f:
    f.write(content)

new_len = len(content)
print(f"\nGravado: {SRC_HTML}")
print(f"Tamanho: {new_len:,} bytes ({new_len/1024/1024:.1f} MB)")

# ── Versao pos-fix ────────────────────────────────────────────────────────────
ts2 = datetime.now().strftime("%Y%m%d_%H%M")
VER_HTML2 = os.path.join(VER_DIR, f"Dashboard_Farma_Sul_{ts2}_IsadoraFix.html")
shutil.copy2(SRC_HTML, VER_HTML2)
print(f"Versao pos-fix: {VER_HTML2}")

# ── Verificacao rapida ────────────────────────────────────────────────────────
print("\n=== VERIFICACAO ===")
with open(SRC_HTML, "r", encoding="utf-8") as f:
    c2 = f.read()

# SJ_UNID
m = re.search(r"const SJ_UNID\s*=\s*\{([^}]+)\}", c2, re.DOTALL)
if m:
    print(f"SJ_UNID: {m.group(1)[:300]}")

# SJ_REC
m2 = re.search(r"const SJ_REC\s*=\s*\{([^}]+)\}", c2, re.DOTALL)
if m2:
    print(f"\nSJ_REC: {m2.group(1)[:300]}")

# Canvas reset em renderLineChart
has_reset = 'ctx.removeAttribute' in c2[c2.find('function renderLineChart'):c2.find('function renderLineChart')+3000]
print(f"\nCanvas reset em renderLineChart: {has_reset}")
