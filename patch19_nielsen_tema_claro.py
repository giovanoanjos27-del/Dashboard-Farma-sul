"""
PATCH 19 — Nielsen Panel: Tema Claro (Opção D — Azul-gelo Corporativo)
Painel: #EBF0F5 | Card: #F7FAFE | Borda: rgba(59,130,246,0.20)
Escopo: CSS estrutural + charts (Chart.js) + textos inline gerados por JS
"""
import datetime, re

SRC = r'Dashboard_farma_sul\Dashboard_Farma_Sul_20260512_2220.html'
html = open(SRC, encoding='utf-8').read()
original_len = len(html)
patches = 0

# ──────────────────────────────────────────────────────────────────────────────
# HELPER: substituição dentro de uma função JS específica
# ──────────────────────────────────────────────────────────────────────────────
def replace_in_fn(h, fn_name, old, new, count=1):
    """Substitui `old` por `new` apenas dentro da função `fn_name`."""
    start = h.find('function ' + fn_name + '(')
    if start == -1: return h, False
    end = h.find('\nfunction ', start + 10)
    if end == -1: end = start + 200000
    chunk = h[start:end]
    if old not in chunk: return h, False
    new_chunk = chunk.replace(old, new, count)
    return h[:start] + new_chunk + h[end:], True

def replace_all_in_fn(h, fn_name, old, new):
    """Substitui TODAS as ocorrências de `old` dentro da função `fn_name`."""
    start = h.find('function ' + fn_name + '(')
    if start == -1: return h, 0
    end = h.find('\nfunction ', start + 10)
    if end == -1: end = start + 200000
    chunk = h[start:end]
    c = chunk.count(old)
    if c == 0: return h, 0
    new_chunk = chunk.replace(old, new)
    return h[:start] + new_chunk + h[end:], c

# ──────────────────────────────────────────────────────────────────────────────
# 1. CSS: SUBSTITUIR BLOCO #panel-nielsen (tema escuro → claro)
# ──────────────────────────────────────────────────────────────────────────────
OLD_CSS_BLOCK = '''/* ── Nielsen: KPI chips nos cards dinâmicos — igual MSO1 ── */
#panel-nielsen #reg-perf-kpis > div {
  background: #161B22 !important;
  border-radius: 10px !important;
  padding: 12px 14px !important;
  border: 0.5px solid rgba(255,255,255,0.05) !important;
}
/* SKU diagnóstico */
#panel-nielsen #sku-diagnostico {
  border-radius: 10px !important;
  border: 0.5px solid rgba(251,191,36,0.18) !important;
  background: rgba(251,191,36,0.04) !important;
}
/* ShrTrend diagnóstico */
#panel-nielsen #shr-diagnostico {
  border-radius: 10px !important;
  border: 0.5px solid rgba(251,191,36,0.18) !important;
  background: rgba(251,191,36,0.04) !important;
}
/* ShrTrend brand filter buttons */
#panel-nielsen #shr-brand-filters button {
  border-radius: 6px !important;
  font-size: 11px !important;
  font-weight: 700 !important;
  padding: 5px 12px !important;
  cursor: pointer !important;
}
/* Legenda ShrTrend — cor padronizada */
#panel-nielsen #shr-trend > div[style*="margin-top:10px"] {
  font-size: 10px !important;
  color: #64748b !important;
}
/* RegPerf KPI sub-labels */
#panel-nielsen #reg-perf-kpis > div > div:first-child {
  font-size: 9px !important;
  font-weight: 700 !important;
  letter-spacing: .1em !important;
  text-transform: uppercase !important;
  color: #3d6b63 !important;
  margin-bottom: 4px !important;
}
/* Tabela titles inside cards */
#panel-nielsen .card.full > div > div[style*="font-size:9px"][style*="font-weight:700"][style*="letter-spacing"] {
  color: #64748b !important;
  letter-spacing: .1em !important;
}
/* Diagnóstico Geral */
#panel-nielsen #diag-geral-card > div:first-child {
  margin-bottom: 16px !important;
  padding-bottom: 12px !important;
  border-bottom: 0.5px solid rgba(255,255,255,0.06) !important;
}

/* ════════════════════════════════════════════════════════
   NIELSEN PANEL — Padronização Visual v1.0 · 2026-05-15
   Scope: #panel-nielsen · Não altera dados/lógica.
   ════════════════════════════════════════════════════════ */

/* Premium dark para todos .card.full no painel Nielsen */
#panel-nielsen .card.full {
  background: #0D1117 !important;
  border: 1.5px solid rgba(251,191,36,0.35) !important;
  border-radius: 14px !important;
}

/* Card header: padding padrão + borda inferior sutil */
#panel-nielsen .card.full .card-header {
  padding: 16px 24px 12px !important;
  border-bottom: 0.5px solid rgba(255,255,255,0.06) !important;
  background: transparent !important;
  margin-bottom: 16px !important;
}

/* Card title e subtitle — hierarquia tipográfica uniforme */
#panel-nielsen .card.full .card-title {
  font-size: 14px !important;
  font-weight: 700 !important;
  color: #F1F5F9 !important;
  line-height: 1.3 !important;
}
#panel-nielsen .card.full .card-sub {
  font-size: 10px !important;
  color: #64748b !important;
  margin-top: 3px !important;
}

/* Odor Block — accent colors por data-ob */
#panel-nielsen .card.full[data-ob="1"] { border-color: rgba(96,165,250,0.45) !important; }
#panel-nielsen .card.full[data-ob="2"] { border-color: rgba(45,212,191,0.45) !important; }
#panel-nielsen .card.full[data-ob="3"] { border-color: rgba(52,211,153,0.45) !important; }

/* AvgPrice — accent verde */
#panel-nielsen .card.full[data-accent="green"] { border-color: rgba(52,211,153,0.45) !important; }

/* OB cards: selects com accent color matching */
#panel-nielsen .card.full[data-ob="1"] .card-header select {
  border: 1px solid rgba(96,165,250,0.35) !important;
}
#panel-nielsen .card.full[data-ob="2"] .card-header select {
  border: 1px solid rgba(45,212,191,0.35) !important;
}
#panel-nielsen .card.full[data-ob="3"] .card-header select {
  border: 0.5px solid rgba(52,211,153,0.3) !important;
}
#panel-nielsen .card.full[data-accent="green"] .card-header select {
  border: 0.5px solid rgba(52,211,153,0.3) !important;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='10' height='6'%3E%3Cpath d='M0 0l5 6 5-6z' fill='%2334d399'/%3E%3C/svg%3E") !important;
}

/* Select dropdowns padrão nas old-style cards */
#panel-nielsen .card.full[data-accent="amber"] .card-header select,
#panel-nielsen .card.full:not([data-ob]):not([data-accent]) .card-header select {
  font-size: 11px !important;
  padding: 6px 28px 6px 10px !important;
  border-radius: 7px !important;
  background: #161B22 !important;
  color: #e2e8f0 !important;
  border: 0.5px solid rgba(251,191,36,0.3) !important;
  appearance: none !important;
  -webkit-appearance: none !important;
}

/* KPI chips uniformes — altura mínima 72px */
#panel-nielsen #mso-kpis > div {
  background: #161B22 !important;
  border-radius: 10px !important;
  padding: 12px 14px !important;
}
#panel-nielsen #ob-share-kpis > div,
#panel-nielsen #ob-preco-kpis > div {
  min-height: 68px;
}

/* Diagnóstico blocks */
#panel-nielsen #ob-share-diag,
#panel-nielsen #ob-preco-diag,
#panel-nielsen #ob-mkt-diag {
  border-radius: 10px !important;
}
#panel-nielsen #avg-insight,
#panel-nielsen #mso-insight {
  border-radius: 10px !important;
}

/* RegPerf, SKU, ShrTrend — dark upgrade + border-radius uniforme */
#panel-nielsen #reg-perf-card {
  background: #0D1117 !important;
  border-radius: 14px !important;
}
#panel-nielsen #sku-shr-card {
  background: #0D1117 !important;
  border: 1.5px solid rgba(251,191,36,0.45) !important;
  border-radius: 14px !important;
}
#panel-nielsen #shr-trend {
  background: #0D1117 !important;
  border: 1.5px solid rgba(251,191,36,0.45) !important;
  border-radius: 14px !important;
}

/* Diagnóstico Geral */
#panel-nielsen #diag-geral-card {
  border-radius: 14px !important;
}

/* Fonte footer — padronizar cor e borda */
#panel-nielsen .dash-footer {
  font-size: 9px;
  color: #3d4451;
}

/* Odor Block section separator — mais sutil */
#panel-nielsen > div[style*="border-top:1px solid rgba(251,191,36"] {
  border-top: 0.5px solid rgba(251,191,36,0.12) !important;
}

/* Toggle group padronizado */
#panel-nielsen .card.full .toggle-group {
  border-radius: 7px !important;
  overflow: hidden !important;
}
#panel-nielsen .card.full .tgl {
  font-size: 11px !important;
  padding: 5px 12px !important;
  border: none !important;
  cursor: pointer !important;
  font-family: inherit !important;
  font-weight: 600 !important;
  background: #161B22 !important;
  color: #D1D5DB !important;
}
#panel-nielsen .card.full .tgl.active {
  background: rgba(251,191,36,0.12) !important;
  color: #fbbf24 !important;
  font-weight: 700 !important;
}

/* Scrollbar dentro dos cards Nielsen */
#panel-nielsen .card.full ::-webkit-scrollbar { height: 3px; width: 3px; }
#panel-nielsen .card.full ::-webkit-scrollbar-thumb { background: rgba(251,191,36,0.2); border-radius: 2px; }'''

NEW_CSS_BLOCK = '''/* ── Nielsen: KPI chips nos cards dinâmicos — igual MSO1 ── */
#panel-nielsen #reg-perf-kpis > div {
  background: #EDF2F9 !important;
  border-radius: 10px !important;
  padding: 12px 14px !important;
  border: 0.5px solid rgba(59,130,246,0.12) !important;
}
/* SKU diagnóstico */
#panel-nielsen #sku-diagnostico {
  border-radius: 10px !important;
  border: 0.5px solid rgba(59,130,246,0.25) !important;
  background: rgba(59,130,246,0.05) !important;
}
/* ShrTrend diagnóstico */
#panel-nielsen #shr-diagnostico {
  border-radius: 10px !important;
  border: 0.5px solid rgba(59,130,246,0.25) !important;
  background: rgba(59,130,246,0.05) !important;
}
/* ShrTrend brand filter buttons */
#panel-nielsen #shr-brand-filters button {
  border-radius: 6px !important;
  font-size: 11px !important;
  font-weight: 700 !important;
  padding: 5px 12px !important;
  cursor: pointer !important;
}
/* Legenda ShrTrend — cor padronizada */
#panel-nielsen #shr-trend > div[style*="margin-top:10px"] {
  font-size: 10px !important;
  color: #64748b !important;
}
/* RegPerf KPI sub-labels */
#panel-nielsen #reg-perf-kpis > div > div:first-child {
  font-size: 9px !important;
  font-weight: 700 !important;
  letter-spacing: .1em !important;
  text-transform: uppercase !important;
  color: #1d4ed8 !important;
  margin-bottom: 4px !important;
}
/* Tabela titles inside cards */
#panel-nielsen .card.full > div > div[style*="font-size:9px"][style*="font-weight:700"][style*="letter-spacing"] {
  color: #475569 !important;
  letter-spacing: .1em !important;
}
/* Diagnóstico Geral */
#panel-nielsen #diag-geral-card > div:first-child {
  margin-bottom: 16px !important;
  padding-bottom: 12px !important;
  border-bottom: 0.5px solid rgba(59,130,246,0.12) !important;
}

/* ════════════════════════════════════════════════════════
   NIELSEN PANEL — Tema Claro v2.0 · Opção D (Azul-gelo)
   Scope: #panel-nielsen · Não altera dados/lógica.
   ════════════════════════════════════════════════════════ */

/* Fundo do painel Nielsen */
#panel-nielsen {
  background: #EBF0F5 !important;
  min-height: 100vh;
}

/* Cards principais — fundo claro */
#panel-nielsen .card.full {
  background: #F7FAFE !important;
  border: 1.5px solid rgba(59,130,246,0.20) !important;
  border-radius: 14px !important;
  box-shadow: 0 2px 12px rgba(59,130,246,0.07) !important;
}

/* Card header */
#panel-nielsen .card.full .card-header {
  padding: 16px 24px 12px !important;
  border-bottom: 0.5px solid rgba(59,130,246,0.10) !important;
  background: transparent !important;
  margin-bottom: 16px !important;
}

/* Card title e subtitle */
#panel-nielsen .card.full .card-title {
  font-size: 14px !important;
  font-weight: 700 !important;
  color: #1e293b !important;
  line-height: 1.3 !important;
}
#panel-nielsen .card.full .card-sub {
  font-size: 10px !important;
  color: #64748b !important;
  margin-top: 3px !important;
}

/* Odor Block — accent colors por data-ob */
#panel-nielsen .card.full[data-ob="1"] { border-color: rgba(37,99,235,0.35) !important; }
#panel-nielsen .card.full[data-ob="2"] { border-color: rgba(13,148,136,0.35) !important; }
#panel-nielsen .card.full[data-ob="3"] { border-color: rgba(22,163,74,0.35)  !important; }

/* AvgPrice — accent verde */
#panel-nielsen .card.full[data-accent="green"] { border-color: rgba(22,163,74,0.35) !important; }

/* OB cards: selects */
#panel-nielsen .card.full[data-ob="1"] .card-header select { border: 1px solid rgba(37,99,235,0.3) !important; }
#panel-nielsen .card.full[data-ob="2"] .card-header select { border: 1px solid rgba(13,148,136,0.3) !important; }
#panel-nielsen .card.full[data-ob="3"] .card-header select { border: 0.5px solid rgba(22,163,74,0.3) !important; }
#panel-nielsen .card.full[data-accent="green"] .card-header select {
  border: 0.5px solid rgba(22,163,74,0.3) !important;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='10' height='6'%3E%3Cpath d='M0 0l5 6 5-6z' fill='%2316a34a'/%3E%3C/svg%3E") !important;
}

/* Select dropdowns padrão */
#panel-nielsen .card.full[data-accent="amber"] .card-header select,
#panel-nielsen .card.full:not([data-ob]):not([data-accent]) .card-header select {
  font-size: 11px !important;
  padding: 6px 28px 6px 10px !important;
  border-radius: 7px !important;
  background: #EDF2F9 !important;
  color: #1e293b !important;
  border: 0.5px solid rgba(59,130,246,0.3) !important;
  appearance: none !important;
  -webkit-appearance: none !important;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='10' height='6'%3E%3Cpath d='M0 0l5 6 5-6z' fill='%233b82f6'/%3E%3C/svg%3E") !important;
  background-repeat: no-repeat !important;
  background-position: right 8px center !important;
}

/* KPI chips */
#panel-nielsen #mso-kpis > div {
  background: #EDF2F9 !important;
  border-radius: 10px !important;
  padding: 12px 14px !important;
  border: 0.5px solid rgba(59,130,246,0.10) !important;
}
#panel-nielsen #ob-share-kpis > div,
#panel-nielsen #ob-preco-kpis > div {
  min-height: 68px;
  background: #EDF2F9 !important;
  border: 0.5px solid rgba(59,130,246,0.10) !important;
}

/* Diagnóstico blocks */
#panel-nielsen #ob-share-diag,
#panel-nielsen #ob-preco-diag,
#panel-nielsen #ob-mkt-diag,
#panel-nielsen #avg-insight,
#panel-nielsen #mso-insight,
#panel-nielsen #mso2-insight {
  border-radius: 10px !important;
}

/* RegPerf, SKU, ShrTrend — light upgrade */
#panel-nielsen #reg-perf-card {
  background: #F7FAFE !important;
  border: 1.5px solid rgba(59,130,246,0.20) !important;
  border-radius: 14px !important;
  box-shadow: 0 2px 12px rgba(59,130,246,0.07) !important;
}
#panel-nielsen #sku-shr-card {
  background: #F7FAFE !important;
  border: 1.5px solid rgba(59,130,246,0.20) !important;
  border-radius: 14px !important;
  box-shadow: 0 2px 12px rgba(59,130,246,0.07) !important;
}
#panel-nielsen #shr-trend {
  background: #F7FAFE !important;
  border: 1.5px solid rgba(59,130,246,0.20) !important;
  border-radius: 14px !important;
  box-shadow: 0 2px 12px rgba(59,130,246,0.07) !important;
}

/* Diagnóstico Geral */
#panel-nielsen #diag-geral-card {
  background: #F7FAFE !important;
  border: 1.5px solid rgba(59,130,246,0.20) !important;
  border-radius: 14px !important;
}

/* Fonte footer */
#panel-nielsen .dash-footer {
  font-size: 9px;
  color: #94a3b8;
}

/* Section separator */
#panel-nielsen > div[style*="border-top:1px solid rgba(251,191,36"] {
  border-top: 0.5px solid rgba(59,130,246,0.15) !important;
}

/* Toggle group */
#panel-nielsen .card.full .toggle-group {
  border-radius: 7px !important;
  overflow: hidden !important;
  background: rgba(59,130,246,0.07) !important;
}
#panel-nielsen .card.full .tgl {
  font-size: 11px !important;
  padding: 5px 12px !important;
  border: none !important;
  cursor: pointer !important;
  font-family: inherit !important;
  font-weight: 600 !important;
  background: transparent !important;
  color: #64748b !important;
}
#panel-nielsen .card.full .tgl.active {
  background: rgba(59,130,246,0.15) !important;
  color: #1d4ed8 !important;
  font-weight: 700 !important;
}

/* Scrollbar */
#panel-nielsen .card.full ::-webkit-scrollbar { height: 3px; width: 3px; }
#panel-nielsen .card.full ::-webkit-scrollbar-thumb { background: rgba(59,130,246,0.25); border-radius: 2px; }

/* ── Overrides para textos gerados por JS (inline styles) ── */
/* Textos quasi-brancos → escuro legível */
#panel-nielsen [style*="color:#e2e8f0"],
#panel-nielsen [style*="color:#E2E8F0"],
#panel-nielsen [style*="color:#F1F5F9"],
#panel-nielsen [style*="color:#f1f5f9"] { color: #1e293b !important; }

#panel-nielsen [style*="color:#D1D5DB"],
#panel-nielsen [style*="color:#d1d5db"],
#panel-nielsen [style*="color:#CBD5E1"],
#panel-nielsen [style*="color:#cbd5e1"] { color: #475569 !important; }

#panel-nielsen [style*="color:#94a3b8"],
#panel-nielsen [style*="color:#94A3B8"] { color: #64748b !important; }

/* Fundos escuros gerados por JS → claro */
#panel-nielsen [style*="background:#161B22"],
#panel-nielsen [style*="background:#161b22"],
#panel-nielsen [style*="background:#0D1117"],
#panel-nielsen [style*="background:#0d1117"],
#panel-nielsen [style*="background:#1F2937"],
#panel-nielsen [style*="background:#1f2937"],
#panel-nielsen [style*="background:#1e293b"],
#panel-nielsen [style*="background:#0a1a18"] { background: #EDF2F9 !important; }

/* Bordas quasi-brancas → azul sutil */
#panel-nielsen [style*="border-bottom:0.5px solid rgba(255,255,255,0.08)"],
#panel-nielsen [style*="border-bottom:1px solid rgba(255,255,255,0.1)"],
#panel-nielsen [style*="border-left:3px solid rgba(255,255,255,0.1)"] {
  border-color: rgba(59,130,246,0.15) !important;
}

/* Borda diagnóstico (border-left âmbar) — manter mas tornar mais sutil */
#panel-nielsen [style*="border-left:3px solid rgba(251,191,36"] {
  border-left-color: rgba(59,130,246,0.6) !important;
}

/* .mso2-br cards brancos com borda */
#panel-nielsen .mso2-br {
  background: #EDF2F9 !important;
  border-color: rgba(59,130,246,0.15) !important;
}
#panel-nielsen .mso2-br:hover {
  background: #E2EAF8 !important;
  border-color: rgba(59,130,246,0.3) !important;
}'''

if OLD_CSS_BLOCK in html:
    html = html.replace(OLD_CSS_BLOCK, NEW_CSS_BLOCK, 1)
    patches += 1
    print('[OK] CSS: bloco #panel-nielsen substituído (tema claro Opção D)')
else:
    print('[MISS] CSS: bloco #panel-nielsen não encontrado')

# ──────────────────────────────────────────────────────────────────────────────
# 2. JS — renderMSO: tooltip + GC/TC (grid/tick colors)
# ──────────────────────────────────────────────────────────────────────────────
fn = 'renderMSO'
# GC e TC
html, ok = replace_in_fn(html, fn, "var GC = 'rgba(255,255,255,0.09)', TC = '#4a6b65';",
                                     "var GC = 'rgba(59,130,246,0.10)', TC = '#64748b';")
if ok: patches += 1; print('[OK] renderMSO: GC/TC → light')

# Tooltip backgroundColor (3x)
h_new, c = replace_all_in_fn(html, fn, "backgroundColor:'#0a1a18'", "backgroundColor:'#F0F4FA'")
if c: html = h_new; patches += c; print(f'[OK] renderMSO: tooltip bg → #F0F4FA (x{c})')

# Tooltip text colors
h_new, c = replace_all_in_fn(html, fn, "titleColor:'#e2e8f0'", "titleColor:'#1e293b'")
if c: html = h_new; patches += c; print(f'[OK] renderMSO: titleColor → #1e293b (x{c})')

h_new, c = replace_all_in_fn(html, fn, "bodyColor:'#D1D5DB'", "bodyColor:'#475569'")
if c: html = h_new; patches += c; print(f'[OK] renderMSO: bodyColor → #475569 (x{c})')

h_new, c = replace_all_in_fn(html, fn, "borderColor:'rgba(255,255,255,0.12)'", "borderColor:'rgba(59,130,246,0.2)'")
if c: html = h_new; patches += c; print(f'[OK] renderMSO: tooltip borderColor → blue (x{c})')

# ──────────────────────────────────────────────────────────────────────────────
# 3. JS — renderMSO2: tooltip + scale colors (5 charts)
# ──────────────────────────────────────────────────────────────────────────────
fn = 'renderMSO2'
# Tooltip bg (#1e293b é usado SOMENTE em tooltip nesta função)
h_new, c = replace_all_in_fn(html, fn, "backgroundColor:'#1e293b'", "backgroundColor:'#F0F4FA'")
if c: html = h_new; patches += c; print(f'[OK] renderMSO2: tooltip bg → #F0F4FA (x{c})')

h_new, c = replace_all_in_fn(html, fn, "titleColor:'#94A3B8'", "titleColor:'#475569'")
if c: html = h_new; patches += c; print(f'[OK] renderMSO2: titleColor → #475569 (x{c})')

h_new, c = replace_all_in_fn(html, fn, "bodyColor:'#e2e8f0'", "bodyColor:'#1e293b'")
if c: html = h_new; patches += c; print(f'[OK] renderMSO2: bodyColor → #1e293b (x{c})')

# Scale colors — ticks
h_new, c = replace_all_in_fn(html, fn, "color:'#94A3B8'", "color:'#475569'")
if c: html = h_new; patches += c; print(f'[OK] renderMSO2: ticks color → #475569 (x{c})')

# Grid lines (rgba branco → azul sutil)
h_new, c = replace_all_in_fn(html, fn, "color:'rgba(255,255,255,0.08)'", "color:'rgba(59,130,246,0.10)'")
if c: html = h_new; patches += c; print(f'[OK] renderMSO2: grid color → blue (x{c})')

h_new, c = replace_all_in_fn(html, fn, "color:'rgba(255,255,255,0.07)'", "color:'rgba(59,130,246,0.10)'")
if c: html = h_new; patches += c; print(f'[OK] renderMSO2: grid color 0.07 → blue (x{c})')

# Tooltip border
h_new, c = replace_all_in_fn(html, fn, "borderColor:'rgba(255,255,255,0.12)'", "borderColor:'rgba(59,130,246,0.2)'")
if c: html = h_new; patches += c; print(f'[OK] renderMSO2: tooltip borderColor → blue (x{c})')

# ──────────────────────────────────────────────────────────────────────────────
# 4. JS — renderMSO3: scale colors (3 charts) + tooltip inject
# ──────────────────────────────────────────────────────────────────────────────
fn = 'renderMSO3'
h_new, c = replace_all_in_fn(html, fn, "color:'#94A3B8'", "color:'#475569'")
if c: html = h_new; patches += c; print(f'[OK] renderMSO3: ticks color → #475569 (x{c})')

h_new, c = replace_all_in_fn(html, fn, "color:'rgba(255,255,255,0.08)'", "color:'rgba(59,130,246,0.10)'")
if c: html = h_new; patches += c; print(f'[OK] renderMSO3: grid 0.08 → blue (x{c})')

h_new, c = replace_all_in_fn(html, fn, "color:'rgba(255,255,255,0.05)'", "color:'rgba(59,130,246,0.08)'")
if c: html = h_new; patches += c; print(f'[OK] renderMSO3: grid 0.05 → blue (x{c})')

h_new, c = replace_all_in_fn(html, fn, "color:'#64748b'", "color:'#475569'")
if c: html = h_new; patches += c; print(f'[OK] renderMSO3: secondary text → #475569 (x{c})')

# Axis border
h_new, c = replace_all_in_fn(html, fn, "color:'rgba(255,255,255,0.08)'", "color:'rgba(59,130,246,0.15)'")
# (already replaced above — skip if 0)

# Adicionar tooltip backgroundColor no MSO3 (tooltip não tem bg definido)
html, ok = replace_in_fn(html, fn, "tooltip:{callbacks:{label:function(ctx){return '  Total: '+fmtMkt3(ctx.raw);}}}",
                                    "tooltip:{backgroundColor:'#F0F4FA',titleColor:'#1e293b',bodyColor:'#475569',borderColor:'rgba(59,130,246,0.2)',borderWidth:1,callbacks:{label:function(ctx){return '  Total: '+fmtMkt3(ctx.raw);}}}")
if ok: patches += 1; print('[OK] renderMSO3: tooltip theme injetado')

# ──────────────────────────────────────────────────────────────────────────────
# 5. JS — renderShrTrend: scale colors + tooltip inject
# ──────────────────────────────────────────────────────────────────────────────
fn = 'renderShrTrend'
h_new, c = replace_all_in_fn(html, fn, "color:'#94A3B8'", "color:'#475569'")
if c: html = h_new; patches += c; print(f'[OK] renderShrTrend: ticks → #475569 (x{c})')

h_new, c = replace_all_in_fn(html, fn, "color:'rgba(255,255,255,0.04)'", "color:'rgba(59,130,246,0.08)'")
if c: html = h_new; patches += c; print(f'[OK] renderShrTrend: grid → blue (x{c})')

# Ticks com condicional (isSingle)
h_new, c = replace_all_in_fn(html, fn, "color:isSingle?'#6b7280':'#3d4451'", "color:isSingle?'#475569':'#64748b'")
if c: html = h_new; patches += c; print(f'[OK] renderShrTrend: ticks condicional → light (x{c})')

# Tooltip inject
html, ok = replace_in_fn(html, fn,
    "tooltip:{mode:'index',intersect:false,callbacks:{label:function(c){return c.dataset.label+': '+(c.raw!==null?c.raw.toFixed(2)+'%':'−');}}}",
    "tooltip:{mode:'index',intersect:false,backgroundColor:'#F0F4FA',titleColor:'#1e293b',bodyColor:'#475569',borderColor:'rgba(59,130,246,0.2)',borderWidth:1,callbacks:{label:function(c){return c.dataset.label+': '+(c.raw!==null?c.raw.toFixed(2)+'%':'−');}}}")
if ok: patches += 1; print('[OK] renderShrTrend: tooltip theme injetado')
else:
    # Tentar variante com caractere diferente
    html, ok = replace_in_fn(html, fn,
        "tooltip:{mode:'index',intersect:false,callbacks:",
        "tooltip:{mode:'index',intersect:false,backgroundColor:'#F0F4FA',titleColor:'#1e293b',bodyColor:'#475569',borderColor:'rgba(59,130,246,0.2)',borderWidth:1,callbacks:")
    if ok: patches += 1; print('[OK] renderShrTrend: tooltip theme injetado (v2)')

# ──────────────────────────────────────────────────────────────────────────────
# 6. JS — renderOBMercado / renderOBPreco / renderOBShare
# ──────────────────────────────────────────────────────────────────────────────
for fn in ['renderOBMercado', 'renderOBPreco', 'renderOBShare']:
    h_new, c = replace_all_in_fn(html, fn, "backgroundColor:'#1F2937'", "backgroundColor:'#F0F4FA'")
    if c: html = h_new; patches += c; print(f'[OK] {fn}: tooltip bg → #F0F4FA (x{c})')

    h_new, c = replace_all_in_fn(html, fn, "borderColor:'rgba(255,255,255,0.12)'", "borderColor:'rgba(59,130,246,0.2)'")
    if c: html = h_new; patches += c; print(f'[OK] {fn}: tooltip borderColor → blue (x{c})')

    h_new, c = replace_all_in_fn(html, fn, "color:'#D1D5DB'", "color:'#475569'")
    if c: html = h_new; patches += c; print(f'[OK] {fn}: tick color → #475569 (x{c})')

    h_new, c = replace_all_in_fn(html, fn, "color:'rgba(255,255,255,0.08)'", "color:'rgba(59,130,246,0.10)'")
    if c: html = h_new; patches += c; print(f'[OK] {fn}: grid → blue (x{c})')

    h_new, c = replace_all_in_fn(html, fn, "color:'rgba(255,255,255,0.09)'", "color:'rgba(59,130,246,0.10)'")
    if c: html = h_new; patches += c; print(f'[OK] {fn}: grid 0.09 → blue (x{c})')

# ──────────────────────────────────────────────────────────────────────────────
# 7. JS — renderMSOSkuJanMar: scale colors
# ──────────────────────────────────────────────────────────────────────────────
fn = 'renderMSOSkuJanMar'
h_new, c = replace_all_in_fn(html, fn, "color:'#94A3B8'", "color:'#475569'")
if c: html = h_new; patches += c; print(f'[OK] renderMSOSkuJanMar: ticks → #475569 (x{c})')

h_new, c = replace_all_in_fn(html, fn, "color:'rgba(52,211,153,0.05)'", "color:'rgba(59,130,246,0.08)'")
if c: html = h_new; patches += c; print(f'[OK] renderMSOSkuJanMar: grid → blue (x{c})')

h_new, c = replace_all_in_fn(html, fn, "color:'rgba(255,255,255,0.15)'", "color:'rgba(59,130,246,0.12)'")
if c: html = h_new; patches += c; print(f'[OK] renderMSOSkuJanMar: grid 0.15 → blue (x{c})')

h_new, c = replace_all_in_fn(html, fn, "color:'#e2e8f0'", "color:'#1e293b'")
if c: html = h_new; patches += c; print(f'[OK] renderMSOSkuJanMar: text → #1e293b (x{c})')

# ──────────────────────────────────────────────────────────────────────────────
# 8. SALVAR
# ──────────────────────────────────────────────────────────────────────────────
print(f'\nPatches aplicados : {patches}')
print(f'Diff              : {len(html) - original_len:+,} bytes')

ts = datetime.datetime.now().strftime('%Y%m%d_%H%M')
ver = f'Dashboard_farma_sul/versoes/Dashboard_Farma_Sul_{ts}_NielsenTemaClaro.html'
open(SRC, 'w', encoding='utf-8').write(html)
open(ver, 'w', encoding='utf-8').write(html)
print(f'\nSalvo : {SRC}')
print(f'Versao: {ver}')
