"""
PATCH 41 - Border-radius uniforme + Nielsen gray cards
1. vol-kpis JS template: rgba transparente → #EAEEF4 + border-radius uniforme
2. Nielsen: #EDF2F9 → #EAEEF4 em todos os KPI containers
3. CSS override final: border-radius padronizado + Nielsen unificado
4. Filtro compradora: borda gold → azul
"""
import datetime

SRC = r'Dashboard_farma_sul\Dashboard_Farma_Sul_20260512_2220.html'
html = open(SRC, encoding='utf-8').read()
orig = len(html)

fixes = 0
def rep(old, new, label=''):
    global html, fixes
    if old not in html:
        print(f'  [MISS] {label or old[:70]}')
        return
    c = html.count(old)
    html = html.replace(old, new)
    fixes += 1
    print(f'  [OK]   {label or old[:70]} ({c}x)')

print('[PATCH 41] Radius uniforme + Nielsen Gray')
print()

# ── 1. vol-kpis JS template: rgba transparente → cinza sólido ─────────────
rep(
    "return '<div style=\"background:'+k.bg+';border-radius:10px;padding:12px 14px;border:1px solid '+k.bdr+';border-top-width:2px;\">'\n      +'<div style=\"font-size:9px;font-weight:700;color:#94A3B8;letter-spacing:.08em;margin-bottom:4px;\">'+k.yr+'</div>'\n      +'<div style=\"font-size:17px;font-weight:800;color:'+k.bdr+';line-height:1;margin-bottom:3px;\">'+k.val+'</div>'\n      +dStr+'</div>';",
    "return '<div style=\"background:#EAEEF4;border-radius:12px;padding:14px 16px;border-top:3px solid '+k.bdr+';border-left:1px solid rgba(147,187,235,0.50);border-right:1px solid rgba(147,187,235,0.50);border-bottom:1px solid rgba(147,187,235,0.50);box-shadow:0 2px 8px rgba(10,40,80,0.12),0 1px 3px rgba(10,40,80,0.07);\">'\n      +'<div style=\"font-size:9px;font-weight:700;color:#475569;letter-spacing:.08em;text-transform:uppercase;margin-bottom:4px;\">'+k.yr+'</div>'\n      +'<div style=\"font-size:17px;font-weight:800;color:'+k.bdr+';line-height:1;margin-bottom:3px;\">'+k.val+'</div>'\n      +dStr+'</div>';",
    'vol-kpis JS template → cinza #EAEEF4 + radius 12px'
)

# ── 2. Nielsen: #EDF2F9 → #EAEEF4 (todos os KPI containers do painel) ──────
rep('#EDF2F9', '#EAEEF4', '#EDF2F9 → #EAEEF4 (Nielsen KPI containers)')

# ── 3. Borda gold no filtro compradora → azul ───────────────────────────────
rep('border-left:1px solid rgba(245,225,164,0.4)',
    'border-left:2px solid rgba(94,153,208,0.6)',
    'compradora-row borda gold → azul')

# ── 4. CSS final padronizando tudo ───────────────────────────────────────────
ANCHOR = '/* FIM PATCH 40 */'
if ANCHOR not in html:
    ANCHOR = '/* FIM PATCH 39 */'

assert ANCHOR in html, 'Ancora não encontrada!'

CSS = """
/* ═══════════════════════════════════════════════════════════════════════
   PATCH 41 — Border-radius uniforme + Nielsen Gray Cards
   ═══════════════════════════════════════════════════════════════════════ */

/* ── 1. Border-radius universal padronizado em 12px ────────────────────── */
.card,
.kpi-cell,
.d-kpi,
[id*="kpis"] > div,
.mso2-br,
.pln-kpi-card,
.ol-kpi,
.e2-kpi,
.x-kcard,
.xcard,
.diag-group-wrap {
  border-radius: 12px !important;
}

/* Cards full-width: radius maior nos cantos externos */
.card.full {
  border-radius: 14px !important;
}

/* Containers de KPI grid: espaçamento e alinhamento uniformes */
.kpi-grid,
[id$="-kpis"],
[id$="-kpis-total"],
[id*="kpis"] {
  gap: 10px !important;
}

/* ── 2. Nielsen: todos os KPI containers → cinza padrão ─────────────────── */
#panel-nielsen [id*="kpis"] > div,
#panel-nielsen .kpi-cell,
#panel-nielsen .mso2-br {
  background:    #EAEEF4 !important;
  border:        1px solid rgba(147,187,235,0.50) !important;
  border-radius: 12px !important;
  box-shadow:    0 2px 8px rgba(10,40,80,0.12), 0 1px 3px rgba(10,40,80,0.07) !important;
  padding:       12px 14px !important;
  color:         #1E293B !important;
}

/* Valores e labels dentro dos KPI nielsen */
#panel-nielsen [id*="kpis"] > div [style*="color:#94A3B8"],
#panel-nielsen [id*="kpis"] > div [style*="color:#94a3b8"] {
  color: #64748B !important;
}

/* ── 3. Nielsen: cards e seções → cinza padrão ───────────────────────────── */
#panel-nielsen .card {
  background:    #EAEEF4 !important;
  border:        1px solid rgba(147,187,235,0.50) !important;
  border-radius: 12px !important;
}

/* Cards dentro do Nielsen que ainda têm bg #EDF2F9 ou similar */
#panel-nielsen [style*="background:#EDF2F9"],
#panel-nielsen [style*="background: #EDF2F9"],
#panel-nielsen [style*="background:#EEF5FF"],
#panel-nielsen [style*="background:#EBF0F5"] {
  background: #EAEEF4 !important;
}

/* ── 4. Sell-Out: vol-kpis override via CSS ──────────────────────────────── */
#vol-kpis > div,
[id*="vol-kpis"] > div {
  background:    #EAEEF4 !important;
  border-radius: 12px !important;
  border:        1px solid rgba(147,187,235,0.50) !important;
  box-shadow:    0 2px 8px rgba(10,40,80,0.12) !important;
}

/* ── 5. Filtro compradora-row: remover visual gold ───────────────────────── */
#sj-compradora-row,
#ns-compradora-row,
[id*="compradora-row"] {
  border-left: 2px solid rgba(94,153,208,0.55) !important;
  padding-left: 10px !important;
}

/* ── 6. Filter pills / .tgl buttons: arredondamento e cor padrão ─────────── */
.tgl {
  border-radius: 8px !important;
}
.tgl.active {
  border-radius: 8px !important;
}

/* ── 7. Card .full overflow: garantir que radius apareça visualmente ──────── */
.card.full {
  overflow: hidden !important;
  position: relative !important;
}

/* ── 8. ESTUDO ED header label: ciano → azul padrão ─────────────────────── */
[style*="color:#2dd4bf"] {
  color: #1D6FA8 !important;
}

/* FIM PATCH 41 */
"""

html = html.replace(ANCHOR, ANCHOR + '\n<style>' + CSS + '</style>')
fixes += 1
print('  [OK]   CSS patch41 injetado')

print(f'\nTotal: {fixes} fixes')
print('Diff: {:+,} bytes'.format(len(html) - orig))

ts = datetime.datetime.now().strftime('%Y%m%d_%H%M')
ver = 'Dashboard_farma_sul/versoes/Dashboard_Farma_Sul_{}_RadiusNielsen.html'.format(ts)
open(SRC, 'w', encoding='utf-8').write(html)
open(ver, 'w', encoding='utf-8').write(html)
print('Salvo:', SRC)
print('Versao:', ver)
