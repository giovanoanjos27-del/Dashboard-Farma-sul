"""
PATCH 40 - Gray Cards & Visual Standardization
Fundo: mantém #93BBEB
Cards: branco → cinza elegante #EAEEf4
Padronização completa: altura, espaçamento, bordas, sombras, tabelas, filtros
"""
import datetime

SRC = r'Dashboard_farma_sul\Dashboard_Farma_Sul_20260512_2220.html'
html = open(SRC, encoding='utf-8').read()
orig = len(html)

fixes = 0
def rep(old, new, label=''):
    global html, fixes
    if old not in html:
        print(f'  [MISS] {label or old[:60]}')
        return
    html = html.replace(old, new)
    fixes += 1
    print(f'  [OK]   {label or old[:60]}')

print('[PATCH 40] Gray Cards & Visual Standardization')
print()

# ── 1. Variável CSS --bg-card: branco → cinza ─────────────────────────────
rep('--bg-card:       #FFFFFF;   /* superficie dos cards */',
    '--bg-card:       #EAEEf4;   /* superficie dos cards — cinza elegante */',
    '--bg-card #FFFFFF → #EAEEf4')

# ── 2. KPI cell template JS: #FFFFFF → cinza ─────────────────────────────
rep("background:#FFFFFF;border-radius:12px;padding:16px 18px;border-top:3px solid '+k.ac+';border-left:1px solid rgba(94,153,208,0.35);border-right:1px solid rgba(94,153,208,0.35);border-bottom:1px solid rgba(94,153,208,0.35);box-shadow:0 2px 10px rgba(10,40,80,0.13),0 1px 3px rgba(10,40,80,0.07);",
    "background:#EAEEF4;border-radius:12px;padding:16px 18px;border-top:3px solid '+k.ac+';border-left:1px solid rgba(94,153,208,0.3);border-right:1px solid rgba(94,153,208,0.3);border-bottom:1px solid rgba(94,153,208,0.3);box-shadow:0 2px 10px rgba(10,40,80,0.13),0 1px 3px rgba(10,40,80,0.07);",
    'KPI template background')

# ── 3. CSS patch39 override para KPI cells ────────────────────────────────
rep('[id*="kpis"] > div {\n  background: #FFFFFF !important;',
    '[id*="kpis"] > div {\n  background: #EAEEF4 !important;',
    'CSS KPI override #FFFFFF → cinza')

# ── 4. Injetar CSS completo de padronização ───────────────────────────────
ANCHOR = '/* FIM PATCH 39 */'
assert ANCHOR in html, 'Ancora FIM PATCH 39 não encontrada!'

CSS = """
/* ═══════════════════════════════════════════════════════════════════════
   PATCH 40 — Gray Cards & Visual Standardization Premium
   Fundo: #93BBEB  |  Cards: #EAEEF4  |  Paleta uniforme em todas as abas
   ═══════════════════════════════════════════════════════════════════════ */

/* ── Variáveis atualizadas ─────────────────────────────────────────────── */
:root {
  --bg-card:      #EAEEF4;   /* cards cinza-azulado elegante */
  --bg-card-alt:  #E2E7EF;   /* zebra alternada em tabelas */
  --bg-subtle:    #DDE3ED;   /* hover forte / linha selecionada */
  --bg-hover:     #D6DCE8;   /* hover direto */
  --card:         #EAEEF4;   /* alias JS legado */

  /* Bordas harmoniosas sobre cinza */
  --border-card:  rgba(147,187,235,0.55);

  /* Sombra padronizada (uniforme em todas as abas) */
  --shadow-card:  0 2px 8px rgba(10,40,80,0.13), 0 1px 3px rgba(10,40,80,0.07);
  --shadow-hover: 0 6px 20px rgba(10,40,80,0.17), 0 2px 7px rgba(10,40,80,0.09);

  /* Radius padronizado */
  --radius-sm:  6px;
  --radius-md:  12px;
  --radius-lg:  16px;

  /* Texto nos cards cinza */
  --card-text-heading: #0D1B2E;
  --card-text-primary: #1E293B;
  --card-text-body:    #334155;
  --card-text-muted:   #475569;
  --card-text-faint:   #64748B;
}

/* ── CARDS: padronização universal ────────────────────────────────────── */
.card,
.d-kpi,
.kpi-cell,
.d-card {
  background:    var(--bg-card) !important;
  border:        1px solid var(--border-card) !important;
  border-radius: var(--radius-md) !important;
  box-shadow:    var(--shadow-card) !important;
  color:         var(--card-text-body) !important;
  padding:       16px 18px !important;
}

.card:hover,
.kpi-cell:hover {
  box-shadow:    var(--shadow-hover) !important;
  border-color:  var(--border-base) !important;
  transform:     translateY(-1px);
  transition:    box-shadow .2s, transform .2s, border-color .2s;
}

/* Linha azul no topo dos cards no hover */
.card::before {
  content: '';
  position: absolute; top: 0; left: 0; right: 0; height: 0;
  background: var(--blue-500);
  border-radius: var(--radius-md) var(--radius-md) 0 0;
  transition: height .18s;
}
.card:hover::before { height: 3px; }

/* ── KPI CELLS: override completo ──────────────────────────────────────── */
[id*="kpis"] > div,
.kpi-cell {
  background:    #EAEEF4 !important;
  border:        1px solid rgba(147,187,235,0.50) !important;
  border-radius: var(--radius-md) !important;
  box-shadow:    var(--shadow-card) !important;
  padding:       16px 18px !important;
}

.kpi-tag, .kl { color: #475569 !important; }
.kpi-val, .kv { color: var(--text-heading) !important; }
.kpi-sub, .ks { color: #64748B !important; }

/* ── TÍTULOS DOS CARDS ─────────────────────────────────────────────────── */
.card-title, .ct, .card-header .card-title {
  font-size:   13px !important;
  font-weight: 700 !important;
  color:       #0D1B2E !important;
  margin-bottom: 4px !important;
}
.card-sub {
  font-size: 11px !important;
  color:     #64748B !important;
}
.card-header {
  border-bottom: 1px solid rgba(147,187,235,0.35) !important;
  padding-bottom: 10px !important;
  margin-bottom: 14px !important;
  display: flex !important;
  align-items: center !important;
  justify-content: space-between !important;
}

/* ── TABELAS: cabeçalho azul + zebra ──────────────────────────────────── */
table {
  border-collapse: collapse !important;
  width: 100% !important;
  border-radius: var(--radius-sm) !important;
  overflow: hidden !important;
}
table thead tr,
table th {
  background: #2D5A8E !important;
  color:      #FFFFFF !important;
  font-size:  10.5px !important;
  font-weight: 700 !important;
  letter-spacing: .05em !important;
  text-transform: uppercase !important;
  padding:    9px 12px !important;
  border:     none !important;
  white-space: nowrap !important;
}
table td {
  background: #EAEEF4 !important;
  color:      #1E293B !important;
  font-size:  12px !important;
  padding:    8px 12px !important;
  border-bottom: 1px solid rgba(147,187,235,0.25) !important;
}
table tr:nth-child(even) td {
  background: #E2E7EF !important;
}
table tr:hover td {
  background: #D6DCE8 !important;
}
.d-table th {
  background: #2D5A8E !important;
  color:      #FFFFFF !important;
  border-bottom: none !important;
}
.d-table td {
  background: #EAEEF4 !important;
  color:      #1E293B !important;
}

/* ── FILTROS: modernos e uniformes ─────────────────────────────────────── */
.filters {
  background:    rgba(255,255,255,0.52) !important;
  border-bottom: 1px solid rgba(94,153,208,0.5) !important;
  backdrop-filter: blur(10px) !important;
  padding:       10px 20px !important;
}
.filter-label {
  font-size:    10px !important;
  font-weight:  700 !important;
  letter-spacing: .08em !important;
  color:        #1E293B !important;
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
  transition:   border-color .15s, box-shadow .15s !important;
}
.fsel:focus {
  border-color: var(--blue-500) !important;
  box-shadow:   0 0 0 3px rgba(59,130,246,0.15) !important;
  outline:      none !important;
}

/* ── TOGGLES: uniformes em todas as abas ──────────────────────────────── */
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
  border-radius: var(--radius-sm) !important;
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
.tgl:hover:not(.active) {
  background: rgba(255,255,255,0.3) !important;
  color: #0F172A !important;
}

/* ── SECTION HEADER PANELS (Sell In, Diag, etc.) ──────────────────────── */
[style*="rgba(52,211,153,0.08)"],
[style*="rgba(251,191,36,0.08)"],
[style*="rgba(52,211,153,0.02)"],
[style*="rgba(251,191,36,0.02)"] {
  background:    rgba(255,255,255,0.78) !important;
  border:        1px solid rgba(94,153,208,0.45) !important;
  backdrop-filter: blur(6px) !important;
  box-shadow:    0 2px 10px rgba(10,40,80,0.09) !important;
  border-radius: var(--radius-lg) !important;
}

/* ── HEADER ────────────────────────────────────────────────────────────── */
.header {
  background: linear-gradient(
    to right,
    #FFFFFF 0%, #F5F9FF 38%, #EEF5FF 55%, #FFFFFF 100%
  ) !important;
  border-bottom: 1px solid rgba(94,153,208,0.5) !important;
  box-shadow:    0 2px 8px rgba(10,40,80,0.08) !important;
}
.header h1, #dash-main-title {
  color:       #0D1B2E !important;
  font-weight: 800 !important;
}
.header-sub { color: #475569 !important; }

/* ── TABS ──────────────────────────────────────────────────────────────── */
.ctabs {
  background:    rgba(255,255,255,0.95) !important;
  border-bottom: 1px solid rgba(94,153,208,0.45) !important;
  box-shadow:    0 1px 4px rgba(10,40,80,0.06) !important;
}
.ctab {
  color:      #475569 !important;
  font-size:  12px !important;
  font-weight: 600 !important;
  padding:    10px 14px !important;
}
.ctab:hover {
  color:       #1D4ED8 !important;
  background:  rgba(59,130,246,0.06) !important;
  border-radius: 6px 6px 0 0 !important;
}
.ctab.active {
  color:             #1D4ED8 !important;
  border-bottom-color: #1D4ED8 !important;
  font-weight:       700 !important;
}

/* ── BOTÕES HEADER ─────────────────────────────────────────────────────── */
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

/* ── BADGE ATUALIZADO ──────────────────────────────────────────────────── */
#dash-update-badge {
  background:  rgba(5,150,105,0.10) !important;
  border:      1px solid rgba(5,150,105,0.25) !important;
  color:       #059669 !important;
  border-radius: var(--radius-sm) !important;
  font-weight: 700 !important;
  padding:     4px 10px !important;
}

/* ── SCROLLBAR ─────────────────────────────────────────────────────────── */
::-webkit-scrollbar       { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: rgba(147,187,235,0.25); border-radius: 4px; }
::-webkit-scrollbar-thumb { background: #4D8FCC; border-radius: 4px; }
::-webkit-scrollbar-thumb:hover { background: #2563EB; }

/* ── DELTAS / PILLS ─────────────────────────────────────────────────────── */
.delta-up,
[style*="color:#34d399"],
[style*="color:#10B981"],
[style*="color:#059669"] {
  color: #059669 !important;
}
.delta-down,
[style*="color:#ef4444"],
[style*="color:#DC2626"] {
  color: #DC2626 !important;
}

/* ── BARRAS DE PROGRESSO ────────────────────────────────────────────────── */
.bar-track, .hbar-outer, .prog-bar-bg {
  background:   rgba(147,187,235,0.35) !important;
  border-radius: 4px !important;
}

/* ── PAINEL PRINCIPAL ───────────────────────────────────────────────────── */
.main { background: transparent !important; }
.main.active { padding: 20px 24px !important; }

/* ── OL card escuro → cinza ─────────────────────────────────────────────── */
[style*="background:linear-gradient(135deg,#0D1117"],
[style*="background: linear-gradient(135deg, #0D1117"],
[style*="rgba(245,225,164,0.35)"] {
  background:   #EAEEF4 !important;
  border-color: rgba(147,187,235,0.55) !important;
}

/* ── TELA DE LOGIN: card branco sobre fundo azul ────────────────────────── */
#login-overlay > div > div[style*="background:#FFFFFF"],
#login-overlay > div > div[style*="background: #FFFFFF"] {
  background: rgba(255,255,255,0.95) !important;
  backdrop-filter: blur(8px) !important;
}

/* FIM PATCH 40 */
"""

html = html.replace(ANCHOR, ANCHOR + '\n<style>' + CSS + '</style>')
fixes += 1
print('  [OK]   CSS patch40 injetado')

print(f'\nTotal: {fixes} alterações')
print('Diff: {:+,} bytes'.format(len(html) - orig))

ts = datetime.datetime.now().strftime('%Y%m%d_%H%M')
ver = 'Dashboard_farma_sul/versoes/Dashboard_Farma_Sul_{}_GrayCards.html'.format(ts)
open(SRC, 'w', encoding='utf-8').write(html)
open(ver, 'w', encoding='utf-8').write(html)
print('Salvo:', SRC)
print('Versao:', ver)
