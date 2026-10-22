"""
PATCH 25 - PADRONIZACAO VISUAL GLOBAL
Aplica tema claro Nielsen em TODOS os paineis do dashboard.

Alteracoes:
  CSS  : body, header, tabs, filters, cards, kpi, toggles, hbars, tables,
         diagnostics, selects — overrides globais !important
  CSS  : attribute selectors para fundos/textos inline injetados pelo JS
  Chart: Chart.defaults tooltip dark, legend claro, color ticks
  JS   : GC grid lines -> azul sutil em todas as funcoes de render
  JS   : TC tick color -> #475569 onde estava dark-teal invisivel
  JS   : ticks inline #D1D5DB / #e2e8f0 -> #475569
  JS   : CO tooltip titleColor/bodyColor -> branco/claro
  JS   : grid rgba(255,255,255,0.03) -> rgba(148,163,184,0.08)
"""
import datetime

SRC = r'Dashboard_farma_sul\Dashboard_Farma_Sul_20260512_2220.html'
html = open(SRC, encoding='utf-8').read()
original_len = len(html)
patches = 0

def do_replace(old, new, desc, count=None):
    global html, patches
    if old not in html:
        print('[MISS] ' + desc)
        return False
    if count is None:
        # replace all
        n = html.count(old)
        html = html.replace(old, new)
        patches += 1
        print('[OK x{}] {}'.format(n, desc))
    else:
        html = html.replace(old, new, count)
        patches += 1
        print('[OK] ' + desc)
    return True

# ==============================================================================
# 1. CSS — BLOCO GLOBAL (injeta antes de /* == END UTILITY == */)
# ==============================================================================
CSS_ANCHOR = '/* ═══ END UTILITY ═══ */'

NEW_CSS = r"""
/* ================================================================
   PATCH 25 -- PADRONIZACAO VISUAL GLOBAL -- Tema Claro todos os paineis
   ================================================================ */

/* ── Base ─────────────────────────────────────────────────────── */
body { background:#F4F7FB !important; color:#334155 !important; }

/* ── Header ───────────────────────────────────────────────────── */
.header {
  background:#FFFFFF !important;
  border-bottom:1px solid #DCE3EC !important;
  box-shadow:0 1px 3px rgba(15,23,42,0.06) !important;
}
.header h1,.header .header-title { color:#0F172A !important; }
.header-sub { color:#64748B !important; }

/* ── Tabs ─────────────────────────────────────────────────────── */
.ctabs {
  background:#FFFFFF !important;
  border-bottom:1px solid #DCE3EC !important;
}
.ctabs::-webkit-scrollbar-thumb { background:rgba(59,130,246,0.30) !important; }
.ctab { color:#64748B !important; }
.ctab:hover { color:#334155 !important; }
.ctab.active { color:#1D4ED8 !important; border-bottom-color:#1D4ED8 !important; }
.cdot-live { background:#10B981 !important; }
.cdot-empty { background:#CBD5E1 !important; }

/* ── Filters ──────────────────────────────────────────────────── */
.filters {
  background:#F8FAFC !important;
  border-bottom:1px solid #EEF2F7 !important;
}
.filter-label { color:#64748B !important; }
#panel-sellout .filter-label { color:#64748B !important; }
.fsel {
  background:#FFFFFF !important;
  border:1px solid #CBD5E1 !important;
  color:#334155 !important;
  background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='10' height='6'%3E%3Cpath d='M0 0l5 6 5-6z' fill='%2364748B'/%3E%3C/svg%3E") !important;
}
.fsel:focus { border-color:#3B82F6 !important; outline:none !important; }

/* ── Sellout client selector ──────────────────────────────────── */
#sellout-client-selector {
  background:#FFFFFF !important;
  border:1px solid #CBD5E1 !important;
  color:#1E293B !important;
  background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='10' height='6'%3E%3Cpath d='M0 0l5 6 5-6z' fill='%2364748B'/%3E%3C/svg%3E") !important;
  box-shadow:none !important;
}
#sellout-client-selector:hover { border-color:#94A3B8 !important; box-shadow:0 0 0 2px rgba(59,130,246,0.08) !important; }
#sellout-client-selector:focus { border-color:#3B82F6 !important; box-shadow:0 0 0 3px rgba(59,130,246,0.15) !important; }
#sellout-client-selector option { background:#FFFFFF !important; color:#1E293B !important; }

/* ── Cards ────────────────────────────────────────────────────── */
.card {
  background:#FFFFFF !important;
  border:1px solid #DCE3EC !important;
  border-radius:14px !important;
  box-shadow:0 1px 3px rgba(15,23,42,0.05) !important;
  backdrop-filter:none !important;
}
.card-title { color:#1E293B !important; }
.card-sub   { color:#64748B !important; }
.section-label { color:#64748B !important; }
.card.full { grid-column:1/-1; }

/* ── KPI grid ─────────────────────────────────────────────────── */
.kpi-grid {
  background:#DCE3EC !important;
  border:1px solid #DCE3EC !important;
}
.kpi-cell { background:#FFFFFF !important; }
.kpi-tag  { color:#64748B !important; }
.kpi-val  { color:#0F172A !important; }
.kpi-sub  { color:#94A3B8 !important; }
.kpi-delta { }
.delta-up   { background:rgba(16,185,129,0.10) !important; color:#10B981 !important; }
.delta-down { background:rgba(239,68,68,0.10)  !important; color:#EF4444 !important; }

/* ── Toggle group ─────────────────────────────────────────────── */
.toggle-group {
  background:#EEF2F7 !important;
  border:1px solid #DCE3EC !important;
}
.tgl { color:#64748B !important; background:transparent !important; }
.tgl:hover { color:#334155 !important; }
.tgl.active {
  background:#FFFFFF !important;
  color:#1E293B !important;
  box-shadow:0 1px 2px rgba(15,23,42,0.08) !important;
}
.tgl.active.blue   { background:rgba(59,130,246,0.12) !important; color:#1D4ED8 !important; box-shadow:none !important; }
.tgl.active.purple { background:rgba(139,92,246,0.12) !important; color:#7C3AED !important; box-shadow:none !important; }
.tgl.active.green  { background:rgba(16,185,129,0.12) !important; color:#059669 !important; box-shadow:none !important; }

/* ── H-bars ───────────────────────────────────────────────────── */
.hbar-label { color:#334155 !important; }
.hbar-outer { background:#EEF2F7 !important; }
.hbar-right { color:#64748B !important; }

/* ── Bar list ─────────────────────────────────────────────────── */
.bar-name { color:#334155 !important; }
.bar-item:hover    { background:rgba(59,130,246,0.04) !important; }
.bar-item.selected { background:rgba(59,130,246,0.06) !important; border-color:rgba(59,130,246,0.20) !important; }
.bar-track { background:#EEF2F7 !important; }

/* ── Compradora buttons (sell out header) ─────────────────────── */
#sj-compradora-row .tgl,
#ns-compradora-row .tgl { color:#64748B !important; }
#sj-compradora-row .tgl.active,
#ns-compradora-row .tgl.active {
  background:rgba(59,130,246,0.12) !important;
  color:#1D4ED8 !important;
  box-shadow:none !important;
}

/* ── Tables ───────────────────────────────────────────────────── */
table { border-collapse:collapse !important; }
thead tr { background:#E2E8F0 !important; }
thead tr th { color:#1E293B !important; background:#E2E8F0 !important; }
tbody tr td { color:#334155 !important; }
tbody tr:nth-child(even) td { background:rgba(241,245,249,0.50) !important; }
tbody tr:hover td { background:#F8FAFC !important; }

/* ── Diagnosticos / insight blocks ───────────────────────────── */
[id$="-diag"]    {
  background:#F0F6FF !important;
  border-left-color:#2563EB !important;
  color:#334155 !important;
}
[id$="-insight"] {
  background:#F0F6FF !important;
  border-left-color:#2563EB !important;
  color:#334155 !important;
}
[id$="-diag"] *,
[id$="-insight"] * { color:#334155 !important; }

/* ── Global selects ───────────────────────────────────────────── */
select {
  background:#FFFFFF !important;
  border:1px solid #CBD5E1 !important;
  color:#334155 !important;
}
select option { background:#FFFFFF !important; color:#334155 !important; }

/* ── Scrollbars ───────────────────────────────────────────────── */
::-webkit-scrollbar-track { background:#EEF2F7 !important; }
::-webkit-scrollbar-thumb { background:#CBD5E1 !important; }
::-webkit-scrollbar-thumb:hover { background:#94A3B8 !important; }

/* ── Misc buttons ─────────────────────────────────────────────── */
.btn-clear {
  background:rgba(239,68,68,0.07) !important;
  border-color:rgba(239,68,68,0.25) !important;
  color:#EF4444 !important;
}

/* ── Inline dark backgrounds injetados pelo JS -> branco ─────── */
[style*="background:#0D1117"],[style*="background: #0D1117"],
[style*="background:#161B22"],[style*="background: #161B22"],
[style*="background:#0F172A"],[style*="background: #0F172A"],
[style*="background:#1E293B"],[style*="background: #1E293B"],
[style*="background:#1f2937"],[style*="background: #1f2937"],
[style*="background:#111827"],[style*="background: #111827"],
[style*="background:#0a1a18"],[style*="background: #0a1a18"],
[style*="background:#141B24"],[style*="background: #141B24"],
[style*="background:rgb(13, 17, 23)"],
[style*="background:rgb(22, 27, 34)"],
[style*="background:rgb(31, 41, 55)"] {
  background:#FFFFFF !important;
}

/* ── Inline textos claros -> escuros ─────────────────────────── */
[style*="color:#e2e8f0"],[style*="color: #e2e8f0"] { color:#1E293B !important; }
[style*="color:#D1D5DB"],[style*="color: #D1D5DB"] { color:#334155 !important; }
[style*="color:#94A3B8"],[style*="color: #94A3B8"] { color:#64748B !important; }
[style*="color:#F5E1A4"],[style*="color: #F5E1A4"] { color:#1E293B !important; }
[style*="color:#7aa89e"],[style*="color: #7aa89e"] { color:#475569 !important; }
[style*="color:#4a6b65"],[style*="color: #4a6b65"] { color:#475569 !important; }

/* ── Remover text-shadow global ──────────────────────────────── */
* { text-shadow:none !important; }

"""

do_replace(CSS_ANCHOR, NEW_CSS + CSS_ANCHOR, 'CSS global override block', count=1)

# ==============================================================================
# 2. Chart.defaults — actualizar cores para tema claro
# ==============================================================================

# 2a. Tooltip: titleColor cyan -> branco, bodyColor cinza -> claro
do_replace(
    "backgroundColor: 'rgba(10,14,26,0.95)',\n    borderColor: 'rgba(103,232,249,0.3)',\n    borderWidth: 1,\n    titleColor: '#67e8f9',",
    "backgroundColor: '#0F172A',\n    borderColor: 'rgba(148,163,184,0.25)',\n    borderWidth: 1,\n    titleColor: '#FFFFFF',",
    "Chart.defaults tooltip: titleColor -> branco, borderColor -> neutro", count=1
)

do_replace(
    "    bodyColor: '#cbd5e1',",
    "    bodyColor: '#E2E8F0',",
    "Chart.defaults tooltip bodyColor -> claro", count=1
)

# 2b. Legend labels color
do_replace(
    "    color: '#94A3B8',\n    font: { size: 11, family: \"'Inter','Segoe UI',sans-serif\" },",
    "    color: '#334155',\n    font: { size: 11, family: \"'Inter','Segoe UI',sans-serif\" },",
    "Chart.defaults legend labels color -> #334155", count=1
)

# 2c. Global color (ticks fallback)
do_replace(
    "  Chart.defaults.color = '#94A3B8';",
    "  Chart.defaults.color = '#475569';",
    "Chart.defaults.color -> #475569", count=1
)

# ==============================================================================
# 3. GC/TC variaveis em funcoes de render nao-Nielsen
#    Padrao A: var GC='rgba(255,255,255,0.09)', TC='#4a6b65'; (mais comum)
#    Padrao B: var GC='rgba(255,255,255,0.07)',TC='#4a6b65'; (_mkChart)
#    Padrao C: var GC = 'rgba(255,255,255,0.09)', TC = '#4a6b65'; (espaco em =)
#    Padrao D: var GC  = 'rgba(255,255,255,0.09)'; (renderEvMensal)
#    Padrao E: var TC  = '#3d5a56'; (renderEvMensal)
# ==============================================================================

do_replace(
    "'rgba(255,255,255,0.09)', TC='#4a6b65'",
    "'rgba(148,163,184,0.12)', TC='#475569'",
    "GC/TC padrao A (0.09 sem espaco em =) -> azul/escuro"
    # replace_all
)

do_replace(
    "'rgba(255,255,255,0.07)',TC='#4a6b65'",
    "'rgba(148,163,184,0.12)',TC='#475569'",
    "GC/TC padrao B (_mkChart 0.07) -> azul/escuro"
)

do_replace(
    "'rgba(255,255,255,0.09)', TC = '#4a6b65'",
    "'rgba(148,163,184,0.12)', TC = '#475569'",
    "GC/TC padrao C (espaco em = ) -> azul/escuro"
)

do_replace(
    "var GC  = 'rgba(255,255,255,0.09)';",
    "var GC  = 'rgba(148,163,184,0.12)';",
    "GC padrao D (renderEvMensal linha separada) -> azul"
)

do_replace(
    "var TC  = '#3d5a56';",
    "var TC  = '#475569';",
    "TC padrao E (renderEvMensal) -> #475569"
)

# renderAnoChart (plano de negocios area) – GC separado
do_replace(
    "  var GC = 'rgba(255,255,255,0.09)', TC = '#4a6b65';",
    "  var GC = 'rgba(148,163,184,0.12)', TC = '#475569';",
    "GC/TC renderAnoChart (2 espacos, espaco em =) -> azul/escuro"
)

# ==============================================================================
# 4. Tick colors hardcoded inline nos charts nao-Nielsen
# ==============================================================================

do_replace(
    "ticks:{color:'#D1D5DB',font:",
    "ticks:{color:'#475569',font:",
    "ticks inline #D1D5DB -> #475569 (replace_all)"
)

do_replace(
    "ticks:{color:'#e2e8f0',font:",
    "ticks:{color:'#475569',font:",
    "ticks inline #e2e8f0 -> #475569 (replace_all)"
)

# Axis title color #D1D5DB nos graficos de estoque
do_replace(
    "color:'#D1D5DB',font:{size:9}}",
    "color:'#475569',font:{size:9}}",
    "axis title color #D1D5DB -> #475569 (replace_all)"
)

# Ticks com font size 10 e 11 (cobertura, ol, outros)
do_replace(
    "ticks:{color:'#e2e8f0',font:{size:10}}",
    "ticks:{color:'#475569',font:{size:10}}",
    "ticks #e2e8f0 size:10 -> #475569"
)

do_replace(
    "ticks:{color:'#e2e8f0',font:{size:11}}",
    "ticks:{color:'#475569',font:{size:11}}",
    "ticks #e2e8f0 size:11 -> #475569"
)

# Ticks sem font key (formato curto)
do_replace(
    "ticks:{color:'#e2e8f0'}",
    "ticks:{color:'#475569'}",
    "ticks #e2e8f0 sem font -> #475569"
)

# ==============================================================================
# 5. Grid colors rgba(255,255,255,0.03) nos charts de estoque/outros
# ==============================================================================

do_replace(
    "grid:{color:'rgba(255,255,255,0.03)'}",
    "grid:{color:'rgba(148,163,184,0.08)'}",
    "grid rgba(0.03) -> azul sutil (replace_all)"
)

# ==============================================================================
# 6. CO tooltip objects nas funcoes nao-Nielsen
#    {backgroundColor:'#0a1a18',titleColor:'#e2e8f0',bodyColor:'#D1D5DB',borderColor:'rgba(255,255,255,0.13)',...}
# ==============================================================================

do_replace(
    "{backgroundColor:'#0a1a18',titleColor:'#e2e8f0',bodyColor:'#D1D5DB',borderColor:'rgba(255,255,255,0.13)',borderWidth:1,padding:10}",
    "{backgroundColor:'#0F172A',titleColor:'#FFFFFF',bodyColor:'#E2E8F0',borderColor:'rgba(148,163,184,0.20)',borderWidth:1,padding:10}",
    "CO tooltip dark -> padrao spec (replace_all)"
)

# Variante sem padding ou com espaco diferente
do_replace(
    "backgroundColor:'#0a1a18',titleColor:'#e2e8f0',bodyColor:'#D1D5DB',borderColor:'rgba(255,255,255,0.13)'",
    "backgroundColor:'#0F172A',titleColor:'#FFFFFF',bodyColor:'#E2E8F0',borderColor:'rgba(148,163,184,0.20)'",
    "CO tooltip dark variante parcial (replace_all)"
)

# ==============================================================================
# 7. Remover backdrop-filter no CSS original (causa blur em fundos claros)
# ==============================================================================
do_replace(
    "backdrop-filter:blur(10px);",
    "backdrop-filter:none;",
    "card backdrop-filter blur -> none (replace_all)"
)

# ==============================================================================
# Save
# ==============================================================================
print('\nPatches aplicados: {}'.format(patches))
print('Diff             : {:+,} bytes'.format(len(html) - original_len))

ts = datetime.datetime.now().strftime('%Y%m%d_%H%M')
ver = 'Dashboard_farma_sul/versoes/Dashboard_Farma_Sul_{}_GlobalTemaClaro.html'.format(ts)
open(SRC, 'w', encoding='utf-8').write(html)
open(ver, 'w', encoding='utf-8').write(html)
print('\nSalvo : {}'.format(SRC))
print('Versao: {}'.format(ver))
