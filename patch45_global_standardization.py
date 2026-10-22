"""
patch45_global_standardization.py
Padronização visual global — todos os painéis no padrão visual Nielsen
APENAS CSS: nenhuma lógica, dado ou funcionalidade alterada
"""
import sys, datetime, shutil
sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path

src = Path('Dashboard_farma_sul/Dashboard_Farma_Sul_20260512_2220.html')
html = src.read_text(encoding='utf-8')
orig = len(html)

CSS_PATCH45 = """
/* ═══════════════════════════════════════════════════════════════════════
   PATCH 45 — Padronização Visual Global · Todos os painéis → padrão Nielsen
   Cobre: panel-sellin, panel-sellout, panel-saojoao-inner,
          panel-nissei-inner, panel-clamed-inner, panel-panvel-inner,
          panel-ddgam-inner, panel-ddgaucha-inner, panel-ddriomed-inner,
          panel-cobertura, panel-ol, panel-plano, panel-expd, panel-diagnostico
   NÃO altera panel-nielsen nem lógica/dados do dashboard.
   ═══════════════════════════════════════════════════════════════════════ */

/* ── 01. FUNDO DE TODOS OS PAINÉIS → #93BBEB (padrão Nielsen) ────────── */
#panel-sellout,
#panel-sellin,
#panel-diagnostico,
#panel-cobertura,
#panel-ol         { background: var(--bg-base, #93BBEB) !important; min-height: 100vh; }

#panel-plano { background: var(--bg-base, #93BBEB) !important; }
#panel-expd  { background: var(--bg-base, #93BBEB) !important; min-height: calc(100vh - 60px); }

/* Sub-painéis Sell Out */
#panel-saojoao-inner,
#panel-nissei-inner,
#panel-clamed-inner,
#panel-panvel-inner,
#panel-ddgam-inner,
#panel-ddgaucha-inner,
#panel-ddriomed-inner { background: var(--bg-base, #93BBEB) !important; }

/* ── 02. CARDS — todos os painéis → estilo Nielsen ───────────────────── */
#panel-sellout .card, #panel-saojoao-inner .card, #panel-nissei-inner .card,
#panel-clamed-inner .card, #panel-panvel-inner .card,
#panel-ddgam-inner .card, #panel-ddgaucha-inner .card, #panel-ddriomed-inner .card,
#panel-sellin .card, #panel-diagnostico .card,
#panel-cobertura .card, #panel-ol .card, #panel-plano .card, #panel-expd .card {
  background:    #EAEEF4 !important;
  border:        1px solid rgba(147,187,235,0.45) !important;
  border-radius: 12px !important;
  box-shadow:    0 2px 8px rgba(10,40,80,0.14) !important;
}
#panel-sellout .card:hover, #panel-saojoao-inner .card:hover, #panel-nissei-inner .card:hover,
#panel-clamed-inner .card:hover, #panel-panvel-inner .card:hover,
#panel-ddgam-inner .card:hover, #panel-ddgaucha-inner .card:hover, #panel-ddriomed-inner .card:hover,
#panel-sellin .card:hover, #panel-diagnostico .card:hover,
#panel-cobertura .card:hover, #panel-ol .card:hover, #panel-plano .card:hover, #panel-expd .card:hover {
  box-shadow:   0 6px 22px rgba(10,40,80,0.18) !important;
  border-color: rgba(94,153,208,0.60) !important;
}

/* ── 03. KPI CELLS — todos os painéis ────────────────────────────────── */
#panel-sellout .kpi-cell, #panel-saojoao-inner .kpi-cell, #panel-nissei-inner .kpi-cell,
#panel-clamed-inner .kpi-cell, #panel-panvel-inner .kpi-cell,
#panel-ddgam-inner .kpi-cell, #panel-ddgaucha-inner .kpi-cell, #panel-ddriomed-inner .kpi-cell,
#panel-sellin .kpi-cell, #panel-diagnostico .kpi-cell, #panel-cobertura .kpi-cell,
#panel-ol .kpi-cell {
  background:    #FFFFFF !important;
  border:        1px solid rgba(94,153,208,0.50) !important;
  border-radius: 10px !important;
  box-shadow:    0 2px 8px rgba(10,40,80,0.10) !important;
}

/* ── 04. TOGGLE GROUPS — todos os painéis ──────────────────────────── */
#panel-sellout .toggle-group, #panel-saojoao-inner .toggle-group, #panel-nissei-inner .toggle-group,
#panel-clamed-inner .toggle-group, #panel-panvel-inner .toggle-group,
#panel-ddgam-inner .toggle-group, #panel-ddgaucha-inner .toggle-group,
#panel-ddriomed-inner .toggle-group, #panel-sellin .toggle-group,
#panel-diagnostico .toggle-group, #panel-cobertura .toggle-group,
#panel-ol .toggle-group, #panel-plano .toggle-group, #panel-expd .toggle-group {
  background: rgba(255,255,255,0.45) !important;
  border: 1px solid rgba(94,153,208,0.45) !important;
  border-radius: 8px !important;
}
#panel-sellout .tgl.active, #panel-saojoao-inner .tgl.active, #panel-nissei-inner .tgl.active,
#panel-clamed-inner .tgl.active, #panel-panvel-inner .tgl.active,
#panel-ddgam-inner .tgl.active, #panel-ddgaucha-inner .tgl.active,
#panel-ddriomed-inner .tgl.active, #panel-sellin .tgl.active,
#panel-diagnostico .tgl.active, #panel-cobertura .tgl.active,
#panel-ol .tgl.active, #panel-plano .tgl.active, #panel-expd .tgl.active {
  background: #FFFFFF !important;
  color:      #1D4ED8 !important;
  box-shadow: 0 1px 5px rgba(10,40,80,0.14) !important;
  font-weight: 700 !important;
}

/* ── 05. STABS (sub-abas internas) — todos os painéis ──────────────── */
#panel-sellout .stab, #panel-saojoao-inner .stab, #panel-nissei-inner .stab,
#panel-clamed-inner .stab, #panel-panvel-inner .stab,
#panel-ddgam-inner .stab, #panel-ddgaucha-inner .stab, #panel-ddriomed-inner .stab,
#panel-sellin .stab, #panel-diagnostico .stab, #panel-cobertura .stab, #panel-ol .stab {
  background: rgba(255,255,255,0.50) !important;
  border:     1px solid rgba(94,153,208,0.40) !important;
  color:      #475569 !important;
}
#panel-sellout .stab.active, #panel-saojoao-inner .stab.active, #panel-nissei-inner .stab.active,
#panel-clamed-inner .stab.active, #panel-panvel-inner .stab.active,
#panel-ddgam-inner .stab.active, #panel-ddgaucha-inner .stab.active,
#panel-ddriomed-inner .stab.active, #panel-sellin .stab.active,
#panel-diagnostico .stab.active, #panel-cobertura .stab.active, #panel-ol .stab.active {
  background:   rgba(29,78,216,0.10) !important;
  color:        #1D4ED8 !important;
  border-color: rgba(29,78,216,0.30) !important;
  box-shadow:   0 1px 4px rgba(29,78,216,0.10) !important;
}

/* ── 06. CLASSES OL — painel Sell-Out Tracking ──────────────────────── */
.ol-kpi {
  background: #EAEEF4 !important;
  border-radius: 10px !important;
  border: 1px solid rgba(147,187,235,0.50) !important;
  box-shadow: 0 2px 8px rgba(10,40,80,0.10) !important;
}
.ol-card {
  background: #EAEEF4 !important;
  border: 1px solid rgba(147,187,235,0.45) !important;
  border-radius: 12px !important;
  box-shadow: 0 2px 8px rgba(10,40,80,0.10) !important;
}
.ol-card:hover { box-shadow: 0 4px 16px rgba(10,40,80,0.15) !important; }
.ol-fsel {
  background:    #EAEEF4 !important;
  border:        1px solid rgba(94,153,208,0.50) !important;
  color:         #1E293B !important;
  border-radius: 6px !important;
}
.ol-kpi .tag { color: #475569 !important; }
.ol-kpi .sub { color: #64748B !important; }

/* ── 07. CLASSES PLANO DE NEGÓCIOS ─────────────────────────────────── */
.pln-kpi-card {
  background: #EAEEF4 !important;
  border-radius: 10px !important;
  box-shadow: 0 2px 8px rgba(10,40,80,0.10) !important;
}
.pln-kpi-card .pk-tag  { color: #475569 !important; }
.pln-kpi-card .pk-sub  { color: #64748B !important; }
.pln-dc {
  background: #EAEEF4 !important;
  border-color: rgba(147,187,235,0.50) !important;
  border-radius: 12px !important;
}
.pln-dc:hover { box-shadow: 0 4px 14px rgba(10,40,80,0.15) !important; }
.pln-dc-nome  { color: #1E293B !important; }
.pln-dc-iqvia { color: #64748B !important; }
.pln-mg-title { color: #475569 !important; }
.pln-mlbl     { color: #64748B !important; }
.pln-mpct     { color: #334155 !important; }
.pln-mvals    { color: #64748B !important; }
.pln-mpts     { color: #B45309 !important; }
.pln-pts-sub  { color: #64748B !important; }
.pln-fbar {
  background: rgba(255,255,255,0.55) !important;
  border:     1px solid rgba(147,187,235,0.40) !important;
  border-radius: 10px !important;
  backdrop-filter: blur(8px) !important;
}
.pln-fbar label { color: #475569 !important; }
.pln-ftab {
  background:   rgba(255,255,255,0.45) !important;
  border:       1px solid rgba(147,187,235,0.40) !important;
  color:        #475569 !important;
  border-radius: 20px !important;
}
.pln-ftab:hover  { background: rgba(255,255,255,0.65) !important; color: #1D4ED8 !important; }
.pln-ftab.pln-on {
  background:   rgba(29,78,216,0.12) !important;
  border-color: rgba(29,78,216,0.35) !important;
  color:        #1D4ED8 !important;
  font-weight:  700 !important;
}
.pln-tw th {
  color:       #475569 !important;
  border-bottom: 1px solid rgba(147,187,235,0.30) !important;
}
.pln-tw td {
  color:       #334155 !important;
  border-bottom: 1px solid rgba(147,187,235,0.15) !important;
}
.pln-pbwrap { background: rgba(147,187,235,0.30) !important; }

/* ── 08. CLASSES EXPANDINDO DISTRIBUIÇÃO (e2-*, x-*, xbn-*) ────────── */
.e2-filterbar {
  background:      rgba(255,255,255,0.55) !important;
  border:          1px solid rgba(147,187,235,0.45) !important;
  border-radius:   12px !important;
  backdrop-filter: blur(10px) !important;
}
.e2-kpi {
  background:    #EAEEF4 !important;
  border:        1px solid rgba(147,187,235,0.50) !important;
  border-radius: 10px !important;
  box-shadow:    0 2px 8px rgba(10,40,80,0.10) !important;
}
.e2-kpi:hover { box-shadow: 0 4px 16px rgba(10,40,80,0.15) !important; }
.e2k-lbl  { color: #475569 !important; }
.e2k-val  { color: #0D1B2E !important; }
.e2k-sub  { color: #64748B !important; }
.e2-chart-box {
  background:    #EAEEF4 !important;
  border:        1px solid rgba(147,187,235,0.45) !important;
  border-radius: 12px !important;
  box-shadow:    0 2px 8px rgba(10,40,80,0.10) !important;
}
.e2-chart-title { color: #0D1B2E !important; }
.e2-tbl-section {
  background:    #EAEEF4 !important;
  border:        1px solid rgba(147,187,235,0.45) !important;
  border-radius: 12px !important;
  box-shadow:    0 2px 8px rgba(10,40,80,0.10) !important;
}
.e2-tbl th {
  background: #E2E8F0 !important;
  color:      #1E293B !important;
}
.e2-tbl td { color: #334155 !important; }
.e2-tbl tr:nth-child(even) td { background: rgba(147,187,235,0.12) !important; }
.e2-tbl tr:hover td           { background: rgba(147,187,235,0.22) !important; }
.e2-ol15-section {
  background:    #EAEEF4 !important;
  border:        1px solid rgba(147,187,235,0.45) !important;
  border-radius: 12px !important;
}
.e2-ol15-tbl th { background: #E2E8F0 !important; color: #1E293B !important; }
.e2-ol15-tbl td { color: #334155 !important; }
.e2-ol15-tab {
  background:  rgba(255,255,255,0.45) !important;
  border:      1px solid rgba(147,187,235,0.50) !important;
  color:       #475569 !important;
}
.e2-ol15-tab.active {
  background:   rgba(29,78,216,0.10) !important;
  color:        #1D4ED8 !important;
  border-color: rgba(29,78,216,0.30) !important;
}
.x-kcard {
  background: #EAEEF4 !important;
  border:     1px solid rgba(147,187,235,0.40) !important;
  border-radius: 8px !important;
  box-shadow: 0 2px 8px rgba(10,40,80,0.10) !important;
}
.xcard {
  background: #EAEEF4 !important;
  border:     1px solid rgba(147,187,235,0.40) !important;
  border-radius: 8px !important;
}
.xcard:hover, .x-kcard:hover { box-shadow: 0 4px 16px rgba(10,40,80,0.16) !important; }
.xkl { color: #475569 !important; }
.xkv { color: #0D1B2E !important; }
.xks { color: #64748B !important; }
.xtbl th { color: #475569 !important; border-bottom: 1px solid rgba(147,187,235,0.35) !important; }
.xtbl td { color: #334155 !important; border-bottom: 1px solid rgba(147,187,235,0.20) !important; }
.xbn-info { color: #475569 !important; }
.xbn-leg-item { color: #475569 !important; }
.xsec { color: #0D1B2E !important; border-left-color: rgba(29,78,216,0.6) !important; }
.xct  { color: #475569 !important; }
.xh   { color: #0D1B2E !important; }
.xs   { color: #475569 !important; }
/* Filtro de botões Expandindo */
.x-fbtn {
  background:    rgba(255,255,255,0.50) !important;
  border:        1px solid rgba(147,187,235,0.40) !important;
  color:         #475569 !important;
  border-radius: 6px !important;
}
.x-fbtn:hover { background: rgba(255,255,255,0.75) !important; color: #1D4ED8 !important; }
.x-fbtn.xon   { background: rgba(29,78,216,0.12) !important; color: #1D4ED8 !important; border-color: rgba(29,78,216,0.35) !important; }
/* xbn-tbl header */
.xbn-tbl { background: #EAEEF4 !important; border-radius: 8px !important; }

/* ── 09. CLASSES UTILITÁRIAS RESIDUAIS (u-*) ────────────────────────── */
.u-kpi-lbl  { color: #475569 !important; }
.u-txt-body { color: #334155 !important; }
.u-td-hdr   { color: #0D1B2E !important; font-weight: 700 !important; }
.u-td-val   { color: #334155 !important; }
.u-td-old   { color: #94A3B8 !important; }
.u-lbl-muted { color: #64748B !important; }
.u-bar-bg    { background: rgba(147,187,235,0.30) !important; border-radius: 2px !important; }
.u-prog-track { background: rgba(147,187,235,0.30) !important; border-radius: 2px !important; }
.u-txt-ok  { color: #059669 !important; }
.u-txt-bad { color: #dc2626 !important; }
.u-icon-ok { color: #059669 !important; }
.u-badge-cyan { background: rgba(6,182,212,0.12) !important; color: #0891B2 !important; }
.u-row-hover { border-bottom: 0.5px solid rgba(147,187,235,0.25) !important; }
.u-row-hover:hover { background: rgba(147,187,235,0.12) !important; }
.u-row-sep  { border-bottom: 0.5px solid rgba(147,187,235,0.25) !important; }

/* ── 10. DIAGNÓSTICO — componentes específicos ──────────────────────── */
.diag-group-wrap {
  background:    #EAEEF4 !important;
  border:        1px solid rgba(147,187,235,0.45) !important;
  border-radius: 12px !important;
  box-shadow:    0 2px 8px rgba(10,40,80,0.10) !important;
}
.diag-card {
  background:    #EAEEF4 !important;
  border:        1px solid rgba(147,187,235,0.35) !important;
  border-radius: 10px !important;
}
#diag-cobertura-card {
  background:    #EAEEF4 !important;
  border:        1px solid rgba(147,187,235,0.45) !important;
  border-radius: 12px !important;
}

/* Acumulado FY cards */
.acum-diag-card {
  background:    #EAEEF4 !important;
  border:        1px solid rgba(147,187,235,0.40) !important;
  border-radius: 10px !important;
  box-shadow:    0 2px 8px rgba(10,40,80,0.10) !important;
}

/* ── 11. COBERTURA — componentes específicos ────────────────────────── */
.cov-badge-green  { background: rgba(5,150,105,0.12)  !important; color: #059669 !important; border: 0.5px solid rgba(5,150,105,0.30)   !important; }
.cov-badge-yellow { background: rgba(180,83,9,0.10)   !important; color: #B45309 !important; border: 0.5px solid rgba(180,83,9,0.25)    !important; }
.cov-badge-orange { background: rgba(234,88,12,0.10)  !important; color: #EA580C !important; border: 0.5px solid rgba(234,88,12,0.25)   !important; }
.cov-badge-red    { background: rgba(220,38,38,0.10)  !important; color: #dc2626 !important; border: 0.5px solid rgba(220,38,38,0.25)   !important; }

/* ── 12. RISCO/STATUS — classes utilitárias ─────────────────────────── */
.risco-critico { color: #dc2626 !important; font-weight: 700 !important; }
.risco-atencao { color: #B45309 !important; font-weight: 600 !important; }
.risco-ok      { color: #059669 !important; font-weight: 600 !important; }
tr.risco-critico-row     { background: rgba(220,38,38,0.04) !important; }
tr.risco-critico-row:hover { background: rgba(220,38,38,0.08) !important; }

/* ── 13. META TABLE ─────────────────────────────────────────────────── */
.meta-table th { background: #E2E8F0 !important; color: #1E293B !important; border-bottom: 1px solid rgba(147,187,235,0.35) !important; }
.meta-table td { color: #334155 !important; border-bottom: 1px solid rgba(147,187,235,0.20) !important; }
.meta-table tr:hover td { background: rgba(59,130,246,0.04) !important; }

/* ── 14. MSO2 — tabela e componentes (escopo geral) ────────────────── */
.mso2-tbl { width: 100% !important; border-collapse: collapse !important; }
.mso2-th { color: #475569 !important; border-bottom: 0.5px solid rgba(147,187,235,0.25) !important; }
.mso2-tc { color: #334155 !important; border-bottom: 0.5px solid rgba(147,187,235,0.15) !important; }
.mso2-bval26 { color: #0D1B2E !important; font-weight: 700 !important; }
.mso2-bar-yr { color: #64748B !important; }
.mso2-bar-track { background: rgba(147,187,235,0.25) !important; }
.mso2-fill25 { background: rgba(147,187,235,0.35) !important; }
.mso2-bar-val { color: #475569 !important; }
.mso2-tip-lbl { color: #64748B !important; }
.mso2-tip-val { color: #334155 !important; }

/* ── 15. INLINE RESIDUAIS — cores dark não cobertas pelos patches anteriores */

/* Backgrounds dark extras */
[style*="background:#111e35"],[style*="background: #111e35"]         { background: #EAEEF4 !important; }
[style*="background:#0a1a26"],[style*="background: #0a1a26"]         { background: #EAEEF4 !important; }
[style*="background:#10172a"],[style*="background: #10172a"]         { background: #EAEEF4 !important; }
[style*="background:#0c1824"],[style*="background: #0c1824"]         { background: #EAEEF4 !important; }
[style*="background:#0b1220"],[style*="background: #0b1220"]         { background: #EAEEF4 !important; }
[style*="background:#080e1b"],[style*="background: #080e1b"]         { background: #EAEEF4 !important; }
[style*="background:rgb(17, 30, 53)"] { background: #EAEEF4 !important; }
[style*="background:rgb(10, 26, 38)"] { background: #EAEEF4 !important; }
[style*="background:rgb(11, 18, 32)"] { background: #EAEEF4 !important; }

/* Rgba quasi-transparente usados como grid-bg ficam invisíveis no fundo claro */
[style*="background:rgba(255,255,255,0.03)"] { background: rgba(147,187,235,0.15) !important; }
[style*="background:rgba(255,255,255,0.04)"] { background: rgba(147,187,235,0.18) !important; }
[style*="background:rgba(255,255,255,0.05)"] { background: rgba(147,187,235,0.20) !important; }
[style*="background:rgba(255,255,255,0.07)"] { background: rgba(147,187,235,0.22) !important; }
[style*="background:rgba(255,255,255,0.08)"] { background: rgba(147,187,235,0.22) !important; }
[style*="background:rgba(255,255,255,0.09)"] { background: rgba(147,187,235,0.25) !important; }
[style*="background:rgba(255,255,255,0.10)"] { background: rgba(147,187,235,0.25) !important; }
[style*="background:rgba(255,255,255,0.12)"] { background: rgba(147,187,235,0.28) !important; }

/* Bordas quasi-brancas residuais → azul sutil */
[style*="border:0.5px solid rgba(255,255,255,0.07)"]  { border-color: rgba(147,187,235,0.30) !important; }
[style*="border:0.5px solid rgba(255,255,255,0.08)"]  { border-color: rgba(147,187,235,0.30) !important; }
[style*="border:0.5px solid rgba(255,255,255,0.10)"]  { border-color: rgba(147,187,235,0.35) !important; }
[style*="border:1px solid rgba(255,255,255,0.04)"]    { border-color: rgba(147,187,235,0.25) !important; }
[style*="border:1px solid rgba(255,255,255,0.05)"]    { border-color: rgba(147,187,235,0.25) !important; }
[style*="border:1px solid rgba(255,255,255,0.07)"]    { border-color: rgba(147,187,235,0.30) !important; }
[style*="border:1px solid rgba(255,255,255,0.08)"]    { border-color: rgba(147,187,235,0.30) !important; }
[style*="border:1px solid rgba(255,255,255,0.10)"]    { border-color: rgba(147,187,235,0.35) !important; }
[style*="border:1px solid rgba(255,255,255,0.12)"]    { border-color: rgba(147,187,235,0.35) !important; }
[style*="border:1.5px solid rgba(255,255,255,0.08)"]  { border-color: rgba(147,187,235,0.35) !important; }
[style*="border:1.5px solid rgba(255,255,255,0.10)"]  { border-color: rgba(147,187,235,0.40) !important; }

/* Cores de texto claras residuais não cobertas */
[style*="color:#E2E8F0"],[style*="color: #E2E8F0"] { color: #1E293B !important; }
[style*="color:#CBD5E1"],[style*="color: #CBD5E1"] { color: #475569 !important; }
[style*="color:#F1F5F9"],[style*="color: #F1F5F9"] { color: #1E293B !important; }
[style*="color:#F8FAFC"],[style*="color: #F8FAFC"] { color: #334155 !important; }
[style*="color:#FAFAFA"],[style*="color: #FAFAFA"] { color: #334155 !important; }
[style*="color:#FFFFFF"],[style*="color: #FFFFFF"] { color: #334155 !important; }
[style*="color: rgb(226, 232, 240)"] { color: #1E293B !important; }
[style*="color: rgb(209, 213, 219)"] { color: #334155 !important; }
[style*="color: rgb(248, 250, 252)"] { color: #334155 !important; }
[style*="color: rgb(241, 245, 249)"] { color: #1E293B !important; }

/* ── 16. ACUM (Acumulado FY) — seção de gráficos acumulados ─────────── */
[id^="acum-diag-"] {
  background:    #EAEEF4 !important;
  border:        1px solid rgba(147,187,235,0.40) !important;
  border-radius: 10px !important;
  box-shadow:    0 2px 8px rgba(10,40,80,0.08) !important;
}
[id^="acum-"] [style*="background:#FFFFFF"],
[id^="acum-"] [style*="background: #FFFFFF"] { background: #EAEEF4 !important; }

/* ── 17. OL — INSIGHTS E DIAGNÓSTICOS ──────────────────────────────── */
#ol-gc-insights {
  background:    #EAEEF4 !important;
  border:        1px solid rgba(147,187,235,0.40) !important;
  border-radius: 10px !important;
}
#ol-diag-share, #ol-diag-so {
  background:    #EAEEF4 !important;
  border-left:   3px solid rgba(45,90,142,0.50) !important;
  border-radius: 8px !important;
}

/* ── 18. SECTION LABELS — unificar hierarquia visual ────────────────── */
#panel-sellout .section-label, #panel-saojoao-inner .section-label,
#panel-nissei-inner .section-label, #panel-clamed-inner .section-label,
#panel-panvel-inner .section-label, #panel-ddgam-inner .section-label,
#panel-ddgaucha-inner .section-label, #panel-ddriomed-inner .section-label,
#panel-sellin .section-label, #panel-diagnostico .section-label,
#panel-cobertura .section-label, #panel-ol .section-label,
#panel-plano .section-label, #panel-expd .section-label {
  color:       #475569 !important;
  border-left: 3px solid #3b82f6 !important;
  padding-left: 10px !important;
}

/* ── 19. PARCIAL/ALERT — padronizar badges ──────────────────────────── */
.partial-alert {
  background: rgba(180,83,9,0.06) !important;
  border:     1px solid rgba(180,83,9,0.20) !important;
  color:      #B45309 !important;
  border-radius: 8px !important;
}

/* ── 20. INTOCÁVEIS X PROVEDOR — remover dark bg inline ─────────────── */
#intoc-g-badge { background: rgba(29,78,216,0.10) !important; color: #1D4ED8 !important; border-color: rgba(29,78,216,0.30) !important; }

/* ── 21. FILTROS GLOBAIS DE BACKGROUND — painéis sem cobertura ──────── */
/* Qualquer card gerado por JS com bg escuro dentro dos paineis SO/SI/Cob/Diag */
#panel-saojoao-inner [style*="background:#161B22"],
#panel-saojoao-inner [style*="background:#0D1117"],
#panel-saojoao-inner [style*="background:#1f2937"],
#panel-saojoao-inner [style*="background:#1E293B"],
#panel-nissei-inner  [style*="background:#161B22"],
#panel-nissei-inner  [style*="background:#0D1117"],
#panel-clamed-inner  [style*="background:#161B22"],
#panel-panvel-inner  [style*="background:#161B22"],
#panel-panvel-inner  [style*="background:#0D1117"],
#panel-ddgam-inner   [style*="background:#161B22"],
#panel-ddgaucha-inner [style*="background:#161B22"],
#panel-ddgaucha-inner [style*="background:#0D1117"],
#panel-ddriomed-inner [style*="background:#161B22"],
#panel-sellin        [style*="background:#161B22"],
#panel-sellin        [style*="background:#1E293B"],
#panel-cobertura     [style*="background:#161B22"],
#panel-cobertura     [style*="background:#0D1117"],
#panel-diagnostico   [style*="background:#161B22"],
#panel-diagnostico   [style*="background:#1E293B"] { background: #EAEEF4 !important; }

/* Textos claros nesses painéis */
#panel-saojoao-inner [style*="color:#D1D5DB"],
#panel-nissei-inner  [style*="color:#D1D5DB"],
#panel-clamed-inner  [style*="color:#D1D5DB"],
#panel-panvel-inner  [style*="color:#D1D5DB"],
#panel-ddgam-inner   [style*="color:#D1D5DB"],
#panel-ddgaucha-inner [style*="color:#D1D5DB"],
#panel-ddriomed-inner [style*="color:#D1D5DB"],
#panel-cobertura     [style*="color:#D1D5DB"],
#panel-sellin        [style*="color:#D1D5DB"],
#panel-diagnostico   [style*="color:#D1D5DB"] { color: #334155 !important; }

#panel-saojoao-inner [style*="color:#e2e8f0"],
#panel-nissei-inner  [style*="color:#e2e8f0"],
#panel-clamed-inner  [style*="color:#e2e8f0"],
#panel-panvel-inner  [style*="color:#e2e8f0"],
#panel-ddgam-inner   [style*="color:#e2e8f0"],
#panel-ddgaucha-inner [style*="color:#e2e8f0"],
#panel-ddriomed-inner [style*="color:#e2e8f0"],
#panel-cobertura     [style*="color:#e2e8f0"],
#panel-sellin        [style*="color:#e2e8f0"],
#panel-diagnostico   [style*="color:#e2e8f0"] { color: #1E293B !important; }

#panel-saojoao-inner [style*="color:#94A3B8"],
#panel-nissei-inner  [style*="color:#94A3B8"],
#panel-clamed-inner  [style*="color:#94A3B8"],
#panel-panvel-inner  [style*="color:#94A3B8"],
#panel-ddgam-inner   [style*="color:#94A3B8"],
#panel-ddgaucha-inner [style*="color:#94A3B8"],
#panel-ddriomed-inner [style*="color:#94A3B8"],
#panel-cobertura     [style*="color:#94A3B8"],
#panel-sellin        [style*="color:#94A3B8"],
#panel-diagnostico   [style*="color:#94A3B8"] { color: #64748B !important; }

/* FIM PATCH 45 */
"""

# Inserir o CSS no bloco 1 (antes do </style> do primeiro bloco, após o patch44)
marker = '/* FIM TEMA VISUAL v2.0 */'
if marker not in html:
    print('[ERRO] Marcador não encontrado!')
else:
    html = html.replace(
        marker,
        CSS_PATCH45.strip() + '\n\n' + marker
    )
    print(f'[OK] CSS patch45 injetado: {len(CSS_PATCH45):,} chars')

diff = len(html) - orig
print(f'Diff: {diff:+,} bytes')

src.write_text(html, encoding='utf-8')

ts = datetime.datetime.now().strftime('%Y%m%d_%H%M')
ver = Path(f'Dashboard_farma_sul/versoes/Dashboard_Farma_Sul_{ts}_Patch45Global.html')
dl  = Path.home() / 'Downloads' / f'Dashboard_FarmaSul_Giovano_{ts}.html'
shutil.copy2(src, ver)
shutil.copy2(src, dl)
print('Versao:', ver.name)
print('Download:', dl.name)
