"""
PATCH 36 - CSS Theme com variaveis :root
Cor extraida das screenshots: #EBF2FA (RGB 235,242,250 - azul leitoso)
1. Bloco :root com todas as variaveis do tema
2. Body background refinado para #EBF2FA
3. Header com gradiente para preencher espaco vazio central
4. Cards, bordas, sombras, filtros atualizados com as variaveis
5. KPI chips, toggles, badges - consistencia visual completa
"""
import datetime

SRC = r'Dashboard_farma_sul\Dashboard_Farma_Sul_20260512_2220.html'
html = open(SRC, encoding='utf-8').read()
original_len = len(html)

ANCHOR = '/* FIM PATCH 35 */'

PATCH36 = '''/* FIM PATCH 35 */

/* ==========================================================================
   PATCH 36 - :root CSS Variables + Light Blue Theme (#EBF2FA)
   Cor extraida das screenshots: rgb(235,242,250) = #EBF2FA
   ========================================================================== */

:root {
  /* --- Fundos --- */
  --bg-base:       #EBF2FA;   /* fundo principal do dashboard */
  --bg-card:       #FFFFFF;   /* superficie dos cards */
  --bg-header:     #FFFFFF;   /* header + tabs */
  --bg-filter:     #F0F6FF;   /* barra de filtros */
  --bg-subtle:     #F4F8FD;   /* hover / row alternada / chip */
  --bg-hover:      #EAF2FF;   /* hover em linhas / botoes */
  --bg-accent:     rgba(59,130,246,0.07); /* fundo de chips ativos */

  /* --- Bordas --- */
  --border-strong: #C8D9EC;   /* bordas de destaque */
  --border-base:   #D6E4F0;   /* bordas normais */
  --border-light:  #E4EEF8;   /* bordas suaves */
  --border-faint:  #EDF3FA;   /* bordas quase invisiveis */

  /* --- Texto --- */
  --text-heading:  #0D1B2E;   /* titulos / h1 */
  --text-primary:  #1E293B;   /* texto principal */
  --text-body:     #334155;   /* corpo de texto */
  --text-muted:    #475569;   /* texto secundario */
  --text-faint:    #64748B;   /* texto fraco / labels */
  --text-placeholder: #94A3B8;

  /* --- Acento azul --- */
  --blue-700:      #1D4ED8;
  --blue-500:      #3B82F6;
  --blue-300:      #93C5FD;
  --blue-50:       rgba(59,130,246,0.07);

  /* --- Sombras --- */
  --shadow-card:   0 1px 4px rgba(10,40,80,0.07), 0 1px 2px rgba(10,40,80,0.04);
  --shadow-hover:  0 4px 16px rgba(10,40,80,0.10), 0 2px 6px rgba(10,40,80,0.06);
  --shadow-header: 0 1px 4px rgba(10,40,80,0.08);

  /* --- Radius --- */
  --radius-sm:   6px;
  --radius-md:   10px;
  --radius-lg:   14px;
}

/* ── Body ──────────────────────────────────────────────────────────────── */
body {
  background: var(--bg-base) !important;
  color: var(--text-body) !important;
}

/* ── Header ────────────────────────────────────────────────────────────── */
.header {
  background: var(--bg-header) !important;
  border-bottom: 1px solid var(--border-base) !important;
  box-shadow: var(--shadow-header) !important;
  /* Gradiente sutil que preenche visualmente o espaco central */
  background: linear-gradient(
    to right,
    #FFFFFF 0%,
    #F5F9FF 40%,
    #F0F6FF 60%,
    #FFFFFF 100%
  ) !important;
}
.header h1,
#dash-main-title {
  color: var(--text-heading) !important;
  font-weight: 700 !important;
}
.header-sub { color: var(--text-faint) !important; }

/* Badge Atualizado */
#dash-update-badge {
  color: #059669 !important;
  background: rgba(5,150,105,0.08) !important;
  border-color: rgba(5,150,105,0.25) !important;
}

/* Botoes do header */
#btn-update-data {
  color: #059669 !important;
  background: rgba(5,150,105,0.08) !important;
  border-color: rgba(5,150,105,0.25) !important;
}
#btn-save-dashboard {
  color: #B45309 !important;
  background: rgba(180,83,9,0.07) !important;
  border-color: rgba(180,83,9,0.2) !important;
}

/* ── Tabs ──────────────────────────────────────────────────────────────── */
.ctabs {
  background: var(--bg-header) !important;
  border-bottom: 1px solid var(--border-base) !important;
}
.ctab               { color: var(--text-faint) !important; }
.ctab:hover         { color: var(--text-muted) !important; background: var(--bg-subtle) !important; border-radius: 6px 6px 0 0; }
.ctab.active        { color: var(--blue-700) !important; border-bottom-color: var(--blue-700) !important; }
.cdot-live          { background: #10B981 !important; }
.cdot-empty         { background: #CBD5E1 !important; }

/* ── Filtros ───────────────────────────────────────────────────────────── */
.filters {
  background: var(--bg-filter) !important;
  border-bottom: 1px solid var(--border-light) !important;
}
.filter-label { color: var(--text-faint) !important; }
.fsel {
  background: var(--bg-card) !important;
  border: 1px solid var(--border-base) !important;
  color: var(--text-primary) !important;
  border-radius: var(--radius-sm) !important;
}
.fsel:focus { border-color: var(--blue-500) !important; box-shadow: 0 0 0 2px rgba(59,130,246,0.12) !important; }

/* ── Cards ─────────────────────────────────────────────────────────────── */
.card {
  background: var(--bg-card) !important;
  border: 1px solid var(--border-light) !important;
  box-shadow: var(--shadow-card) !important;
  border-radius: var(--radius-md) !important;
  backdrop-filter: none !important;
}
.card:hover {
  box-shadow: var(--shadow-hover) !important;
  border-color: var(--border-base) !important;
}

/* ── KPI cells ─────────────────────────────────────────────────────────── */
.kpi-cell {
  background: var(--bg-card) !important;
  border: 1px solid var(--border-light) !important;
  box-shadow: var(--shadow-card) !important;
  border-radius: var(--radius-md) !important;
}
.kpi-cell:hover { box-shadow: var(--shadow-hover) !important; }
.kpi-val   { color: var(--text-heading) !important; }
.kpi-tag   { color: var(--text-faint) !important; }
.kpi-sub   { color: var(--text-faint) !important; }

/* ── Tabelas ───────────────────────────────────────────────────────────── */
table th {
  background: #EBF0F8 !important;
  color: var(--text-muted) !important;
  border-bottom: 1px solid var(--border-base) !important;
}
table td {
  color: var(--text-primary) !important;
  border-bottom: 1px solid var(--border-faint) !important;
}
table tr:hover td { background: var(--bg-hover) !important; }

/* ── Toggles / botoes de filtro ────────────────────────────────────────── */
.toggle-group,
.tgl-group {
  background: #DDE8F5 !important;
  border-radius: var(--radius-md) !important;
  padding: 3px !important;
}
.tgl,
.toggle-btn {
  color: var(--text-muted) !important;
  background: transparent !important;
  border-radius: var(--radius-sm) !important;
}
.tgl.active,
.toggle-btn.active {
  background: var(--bg-card) !important;
  color: var(--blue-700) !important;
  box-shadow: var(--shadow-card) !important;
}

/* ── Bar de progresso genérica ─────────────────────────────────────────── */
.bar-track,
.hbar-outer,
.prog-bar-bg {
  background: #D6E4F0 !important;
  border-radius: 4px !important;
}

/* ── Painel principal (main) ───────────────────────────────────────────── */
.main {
  background: transparent !important;
}

/* ── Scrollbar ─────────────────────────────────────────────────────────── */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: var(--bg-base); }
::-webkit-scrollbar-thumb { background: #B8D0E8; border-radius: 4px; }
::-webkit-scrollbar-thumb:hover { background: var(--border-strong); }

/* ── Sell Out client selector ──────────────────────────────────────────── */
#sellout-client-selector {
  background: var(--bg-card) !important;
  border: 1px solid var(--border-base) !important;
  color: var(--text-primary) !important;
}
#sellout-client-selector:hover { border-color: var(--blue-500) !important; }
#sellout-client-selector:focus { border-color: var(--blue-500) !important; box-shadow: 0 0 0 3px rgba(59,130,246,0.12) !important; }

/* ── Diagnostico + secoes internas ─────────────────────────────────────── */
[id$="-diag"],
.diag-box {
  background: #EEF5FF !important;
  border-left-color: var(--blue-500) !important;
}

/* ── Paineis (IDs especificos) ─────────────────────────────────────────── */
#panel-plano     { background: var(--bg-base) !important; }
#panel-expd      { background: var(--bg-base) !important; }
#panel-nielsen   { background: var(--bg-base) !important; }
#panel-cobertura { background: var(--bg-base) !important; }

/* ── Nielsen KPI cards (schema proprios) ───────────────────────────────── */
#panel-nielsen .kpi-cell,
#panel-nielsen .ob-kpi-card {
  background: var(--bg-card) !important;
  border-color: rgba(59,130,246,0.18) !important;
}

/* FIM PATCH 36 */'''

if ANCHOR in html:
    html = html.replace(ANCHOR, PATCH36, 1)
    print('[OK] CSS patch36 injetado (:root + Light Blue Theme #EBF2FA)')
else:
    print('[MISS] ancora FIM PATCH 35 nao encontrada')

print('Diff: {:+,} bytes'.format(len(html) - original_len))

ts = datetime.datetime.now().strftime('%Y%m%d_%H%M')
ver = 'Dashboard_farma_sul/versoes/Dashboard_Farma_Sul_{}_RootTheme.html'.format(ts)
open(SRC, 'w', encoding='utf-8').write(html)
open(ver, 'w', encoding='utf-8').write(html)
print('Salvo: ' + SRC)
print('Versao: ' + ver)
