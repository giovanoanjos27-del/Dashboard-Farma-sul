"""
patch43_css_consolidation.py
Consolida os blocos <style> dos patches 38-42 em um único bloco organizado.
"""

import re
import shutil
from datetime import datetime
from pathlib import Path

# ── Caminhos ──────────────────────────────────────────────────────────────────
BASE_DIR   = Path(r"C:\Users\valqu\OneDrive\Documentos\Claude\Projects\projeto Dashboard_farma_sul")
DASH_DIR   = BASE_DIR / "Dashboard_farma_sul"
VERSOES    = DASH_DIR / "versoes"
HTML_FILE  = DASH_DIR / "Dashboard_Farma_Sul_20260512_2220.html"
DOWNLOADS  = Path.home() / "Downloads"

VERSOES.mkdir(parents=True, exist_ok=True)

# ── CSS Consolidado ───────────────────────────────────────────────────────────
CONSOLIDATED_CSS = """\
<style>
/* ═══════════════════════════════════════════════════════════════════════
   TEMA VISUAL — DASHBOARD FARMA SUL v2.0
   Consolidação dos patches 38-42 em padrão único organizado
   ═══════════════════════════════════════════════════════════════════════ */

/* ── 01. VARIÁVEIS DE TEMA (atualização :root) ──────────────────────────── */
:root {
  --bg-card:      #EAEEF4;
  --bg-card-alt:  #E2E7EF;
  --bg-subtle:    #DDE3ED;
  --bg-hover:     #D6DCE8;
  --card:         #EAEEF4;
  --border-card:  rgba(147,187,235,0.55);
  --shadow-card:  0 2px 8px rgba(10,40,80,0.14), 0 1px 3px rgba(10,40,80,0.08);
  --shadow-hover: 0 6px 22px rgba(10,40,80,0.18), 0 2px 8px rgba(10,40,80,0.10);
  --shadow-sm:    0 1px 4px rgba(10,40,80,0.10);
  --shadow-header: 0 2px 8px rgba(10,40,80,0.08);
  --radius-sm:    6px;
  --radius-md:    12px;
  --radius-lg:    16px;
  --card-text-heading: #0D1B2E;
  --card-text-primary: #1E293B;
  --card-text-body:    #334155;
  --card-text-muted:   #475569;
  --card-text-faint:   #64748B;
}

/* ── 02. BODY / BASE ────────────────────────────────────────────────────── */
body {
  background: var(--bg-base) !important;
  color: var(--text-body) !important;
}
.main           { background: transparent !important; }
.main.active    { padding: 20px 24px !important; }

/* ── 03. HEADER ─────────────────────────────────────────────────────────── */
.header {
  background: linear-gradient(to right,#FFFFFF 0%,#F5F9FF 38%,#EEF5FF 55%,#FFFFFF 100%) !important;
  border-bottom: 1px solid rgba(94,153,208,0.5) !important;
  box-shadow: var(--shadow-header) !important;
}
.header h1,
#dash-main-title  { color: #0D1B2E !important; font-weight: 800 !important; }
.header-sub       { color: #475569 !important; }
#dash-update-badge {
  background:   rgba(5,150,105,0.10) !important;
  border:       1px solid rgba(5,150,105,0.25) !important;
  color:        #059669 !important;
  border-radius: var(--radius-sm) !important;
  font-weight:  700 !important;
  padding:      4px 10px !important;
  box-shadow:   0 1px 4px rgba(5,150,105,0.20) !important;
}
#btn-update-data {
  background:   rgba(5,150,105,0.10) !important;
  border:       1px solid rgba(5,150,105,0.30) !important;
  color:        #059669 !important;
  border-radius: var(--radius-sm) !important;
  font-weight:  700 !important;
  padding:      6px 14px !important;
}
#btn-save-dashboard {
  background:   rgba(180,83,9,0.09) !important;
  border:       1px solid rgba(180,83,9,0.25) !important;
  color:        #B45309 !important;
  border-radius: var(--radius-sm) !important;
  font-weight:  700 !important;
  padding:      6px 14px !important;
}

/* ── 04. TABS DE NAVEGAÇÃO ──────────────────────────────────────────────── */
.ctabs {
  background:    rgba(255,255,255,0.95) !important;
  border-bottom: 1px solid rgba(94,153,208,0.45) !important;
  box-shadow:    0 1px 4px rgba(10,40,80,0.06) !important;
}
.ctab           { color: #475569 !important; font-size: 12px !important; font-weight: 600 !important; padding: 10px 14px !important; }
.ctab:hover     { color: #1D4ED8 !important; background: rgba(59,130,246,0.06) !important; border-radius: 6px 6px 0 0 !important; }
.ctab.active    { color: #1D4ED8 !important; border-bottom-color: #1D4ED8 !important; font-weight: 700 !important; }
.cdot-live      { background: #10B981 !important; }
.cdot-empty     { background: #CBD5E1 !important; }

/* ── 05. BARRA DE FILTROS ───────────────────────────────────────────────── */
.filters {
  background:    rgba(255,255,255,0.52) !important;
  border-bottom: 1px solid rgba(94,153,208,0.5) !important;
  backdrop-filter: blur(10px) !important;
  padding:       10px 20px !important;
}
.filter-label {
  font-size:     10px !important;
  font-weight:   700 !important;
  letter-spacing: .08em !important;
  color:         #1E293B !important;
  text-transform: uppercase !important;
}
.fsel {
  background:   #EAEEF4 !important;
  border:       1px solid rgba(94,153,208,0.6) !important;
  color:        #1E293B !important;
  border-radius: var(--radius-sm) !important;
  font-size:    12px !important;
  font-weight:  600 !important;
  padding:      6px 28px 6px 10px !important;
  box-shadow:   0 1px 3px rgba(10,40,80,0.08) !important;
}
.fsel:focus {
  border-color: var(--blue-500) !important;
  box-shadow:   0 0 0 3px rgba(59,130,246,0.15) !important;
  outline:      none !important;
}

/* ── 06. CARDS — REGRAS UNIVERSAIS ─────────────────────────────────────── */
.card,
.d-kpi,
.d-card {
  background:    var(--bg-card) !important;
  border:        1px solid var(--border-card) !important;
  border-radius: var(--radius-md) !important;
  box-shadow:    var(--shadow-card) !important;
  color:         var(--card-text-body) !important;
  padding:       16px 18px !important;
  position:      relative !important;
  overflow:      hidden !important;
}
.card.full      { border-radius: var(--radius-lg) !important; }
.card:hover,
.d-kpi:hover    { box-shadow: var(--shadow-hover) !important; border-color: var(--border-base) !important; transform: translateY(-1px); transition: box-shadow .2s, transform .2s, border-color .2s; }
.card::before   { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 0; background: var(--blue-500); border-radius: var(--radius-md) var(--radius-md) 0 0; transition: height .18s; }
.card:hover::before { height: 3px; }
.card-title,
.ct             { font-size: 13px !important; font-weight: 700 !important; color: #0D1B2E !important; margin-bottom: 4px !important; }
.card-sub       { font-size: 11px !important; color: #64748B !important; }
.card-header    { border-bottom: 1px solid rgba(147,187,235,0.35) !important; padding-bottom: 10px !important; margin-bottom: 14px !important; display: flex !important; align-items: center !important; justify-content: space-between !important; }

/* ── 07. KPI CELLS — TODAS AS ABAS ─────────────────────────────────────── */
.kpi-cell,
[id*="kpis"] > div {
  background:    #EAEEF4 !important;
  border:        1px solid rgba(147,187,235,0.50) !important;
  border-radius: var(--radius-md) !important;
  box-shadow:    var(--shadow-card) !important;
  padding:       16px 18px !important;
}
.kpi-cell:hover,
[id*="kpis"] > div:hover { box-shadow: var(--shadow-hover) !important; }
.kpi-tag, .kl   { color: #475569 !important; }
.kpi-val, .kv   { color: var(--text-heading) !important; }
.kpi-sub, .ks   { color: #64748B !important; }

/* ── 08. TABELAS ────────────────────────────────────────────────────────── */
table           { border-collapse: collapse !important; width: 100% !important; }
table th {
  background:    #2D5A8E !important;
  color:         #FFFFFF !important;
  font-size:     10.5px !important;
  font-weight:   700 !important;
  letter-spacing: .05em !important;
  text-transform: uppercase !important;
  padding:       9px 12px !important;
  border:        none !important;
}
table td {
  background:    #EAEEF4 !important;
  color:         #1E293B !important;
  font-size:     12px !important;
  padding:       8px 12px !important;
  border-bottom: 1px solid rgba(147,187,235,0.25) !important;
}
table tr:nth-child(even) td { background: #E2E7EF !important; }
table tr:hover td           { background: #D6DCE8 !important; }
.d-table th                 { background: #2D5A8E !important; color: #FFFFFF !important; border-bottom: none !important; }
.d-table td                 { background: #EAEEF4 !important; color: #1E293B !important; }

/* ── 09. TOGGLES E GRUPOS DE BOTÕES ────────────────────────────────────── */
.toggle-group,
.tgl-group {
  background:    rgba(255,255,255,0.40) !important;
  border:        1px solid rgba(94,153,208,0.45) !important;
  border-radius: var(--radius-md) !important;
  padding:       3px !important;
  box-shadow:    inset 0 1px 3px rgba(10,40,80,0.07) !important;
}
.tgl,
.toggle-btn {
  color:         #334155 !important;
  background:    transparent !important;
  border-radius: 8px !important;
  font-size:     11px !important;
  font-weight:   600 !important;
  padding:       4px 10px !important;
  transition:    background .15s, color .15s, box-shadow .15s !important;
}
.tgl.active,
.toggle-btn.active,
.tgl.active.blue {
  background:  #FFFFFF !important;
  color:       #1D4ED8 !important;
  box-shadow:  0 1px 5px rgba(10,40,80,0.14) !important;
  font-weight: 700 !important;
}
.tgl:hover:not(.active) { background: rgba(255,255,255,0.30) !important; color: #0F172A !important; }

/* ── 10. SECTION HEADER PANELS ─────────────────────────────────────────── */
[style*="rgba(52,211,153,0.08)"],
[style*="rgba(52,211,153,0.02)"],
[style*="rgba(251,191,36,0.08)"],
[style*="rgba(251,191,36,0.02)"] {
  background:    rgba(255,255,255,0.78) !important;
  border:        1px solid rgba(94,153,208,0.45) !important;
  backdrop-filter: blur(6px) !important;
  box-shadow:    0 2px 10px rgba(10,40,80,0.09) !important;
  border-radius: var(--radius-lg) !important;
}
.section-label {
  border-left:  3px solid var(--blue-500) !important;
  padding-left: 10px !important;
  color:        var(--text-heading) !important;
}

/* ── 11. PAINEL NIELSEN — OVERRIDES ESPECÍFICOS ─────────────────────────── */
#panel-nielsen                          { background: transparent !important; }
#panel-nielsen .card,
#panel-nielsen .card.full,
#panel-nielsen #reg-perf-card,
#panel-nielsen #sku-shr-card,
#panel-nielsen #shr-trend,
#panel-nielsen #diag-geral-card {
  background:    #EAEEF4 !important;
  border:        1px solid rgba(147,187,235,0.50) !important;
  border-radius: var(--radius-md) !important;
  box-shadow:    var(--shadow-card) !important;
}
#panel-nielsen [id*="kpis"] > div,
#panel-nielsen .kpi-cell,
#panel-nielsen .mso2-br {
  background:    #EAEEF4 !important;
  border:        1px solid rgba(147,187,235,0.50) !important;
  border-radius: var(--radius-md) !important;
  box-shadow:    var(--shadow-card) !important;
  padding:       12px 14px !important;
  color:         #1E293B !important;
}
#panel-nielsen [style*="background:#EAEEF4"],
#panel-nielsen [style*="background:#EBF0F5"],
#panel-nielsen [style*="background:#EEF5FF"] { background: #EAEEF4 !important; }

/* ── 12. OUTROS PAINÉIS ─────────────────────────────────────────────────── */
#panel-expd  { background: var(--bg-base) !important; }
#panel-plano { background: var(--bg-base) !important; }
[style*="background:linear-gradient(135deg,#0D1117"],
[style*="rgba(245,225,164,0.35)"]        { background: #EAEEF4 !important; border-color: var(--border-card) !important; }
.diag-group-wrap,
.pln-kpi-card,
.ol-kpi,
.e2-kpi,
.x-kcard,
.xcard                                   { background: #EAEEF4 !important; border-radius: var(--radius-md) !important; }

/* ── 13. SCROLLBAR ──────────────────────────────────────────────────────── */
::-webkit-scrollbar          { width: 6px; height: 6px; }
::-webkit-scrollbar-track    { background: rgba(147,187,235,0.25); border-radius: 4px; }
::-webkit-scrollbar-thumb    { background: #4D8FCC; border-radius: 4px; }
::-webkit-scrollbar-thumb:hover { background: #2563EB; }

/* ── 14. TELA DE LOGIN ──────────────────────────────────────────────────── */
#login-overlay > div > div[style*="background:#FFFFFF"],
#login-overlay > div > div[style*="background: #FFFFFF"] {
  background:    rgba(255,255,255,0.95) !important;
  backdrop-filter: blur(8px) !important;
}

/* ── 15. OVERRIDES — CORES INLINE RESIDUAIS ─────────────────────────────── */
[style*="color:#34d399"]  { color: #059669 !important; }
[style*="color:#34D399"]  { color: #059669 !important; }
[style*="color:#2dd4bf"]  { color: #1D6FA8 !important; }
[style*="color:#e2e8f0"]  { color: #1E293B !important; }
[style*="color:#E2E8F0"]  { color: #1E293B !important; }
[style*="background:linear-gradient(135deg,#0D1117"] { background: #EAEEF4 !important; }

/* ── 16. BARRAS E PROGRESSOS ────────────────────────────────────────────── */
.bar-track, .hbar-outer, .prog-bar-bg {
  background:    rgba(147,187,235,0.35) !important;
  border-radius: 4px !important;
}

/* FIM TEMA VISUAL v2.0 */
</style>"""

ANCHOR = "/* FIM PATCH 36 */"

# ── Regex para localizar blocos <style> dos patches 38-42 ─────────────────────
# Captura qualquer bloco <style>...</style> que contenha "FIM PATCH 3[89]" ou
# "FIM PATCH 4[012]".
PATCH_STYLE_RE = re.compile(
    r"<style[^>]*>(?:(?!</style>).)*?/\*\s*FIM PATCH (?:38|39|40|41|42)\s*\*/(?:(?!</style>).)*?</style>",
    re.DOTALL | re.IGNORECASE,
)


def main():
    print(f"Lendo: {HTML_FILE}")
    original = HTML_FILE.read_text(encoding="utf-8")

    # ── 1. Verificar âncora ───────────────────────────────────────────────────
    if ANCHOR not in original:
        raise ValueError(f"Âncora '{ANCHOR}' não encontrada no HTML. Abortando.")
    print(f"Âncora encontrada: '{ANCHOR}'")

    # ── 2. Encontrar blocos dos patches 38-42 ─────────────────────────────────
    matches = list(PATCH_STYLE_RE.finditer(original))
    found_patches = set()
    for m in matches:
        for num in ("38", "39", "40", "41", "42"):
            if f"FIM PATCH {num}" in m.group():
                found_patches.add(num)

    print(f"Blocos encontrados: patches {sorted(found_patches)}")
    if len(matches) == 0:
        raise ValueError("Nenhum bloco <style> de patch 38-42 encontrado. Verifique o HTML.")
    if len(found_patches) < 5:
        missing = {str(n) for n in range(38, 43)} - found_patches
        print(f"AVISO: patches não encontrados: {missing}")

    # ── 3. Remover os blocos (de trás para frente para preservar índices) ─────
    working = original
    for m in reversed(matches):
        working = working[: m.start()] + working[m.end():]
        print(f"  Removido bloco patch ({m.start()}:{m.end()})")

    # ── 4. Injetar CSS consolidado logo APÓS a âncora ─────────────────────────
    inject_pos = working.find(ANCHOR) + len(ANCHOR)
    working = working[:inject_pos] + "\n" + CONSOLIDATED_CSS + "\n" + working[inject_pos:]
    print("CSS consolidado (patch 43) injetado após a âncora.")

    # ── 5. Salvar arquivo principal ───────────────────────────────────────────
    HTML_FILE.write_text(working, encoding="utf-8")
    print(f"Arquivo principal salvo: {HTML_FILE}")

    # ── 6. Criar versão com timestamp ─────────────────────────────────────────
    ts = datetime.now().strftime("%Y%m%d_%H%M")
    versao = VERSOES / f"Dashboard_Farma_Sul_{ts}.html"
    versao.write_text(working, encoding="utf-8")
    print(f"Versão criada: {versao}")

    # ── 7. Exportar para Downloads ────────────────────────────────────────────
    download_dest = DOWNLOADS / f"Dashboard_FarmaSul_Giovano_{ts}.html"
    shutil.copy2(HTML_FILE, download_dest)
    print(f"Cópia exportada: {download_dest}")

    print("\nPatch 43 — consolidação CSS concluída com sucesso.")


if __name__ == "__main__":
    main()
