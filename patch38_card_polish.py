"""
PATCH 38 - Card Polish: melhoria visual de todos os cards, seções e abas
- Sombras mais fortes nos cards (visíveis sobre #93BBEB)
- Section header panels com glass/white treatment
- Fix de cores neon remanescentes nas section info bars
- OL card escuro → claro
- Efeito hover azul nos cards (era gold)
- Tabelas: thead mais elegante
- KPI cells: sombra e borda refinadas
- Filtros: background ligeiramente mais escuro p/ contraste
"""
import datetime, re

SRC = r'Dashboard_farma_sul\Dashboard_Farma_Sul_20260512_2220.html'
html = open(SRC, encoding='utf-8').read()
orig = len(html)

ANCHOR = '/* FIM PATCH 36 */'
assert ANCHOR in html, 'Ancora nao encontrada!'

CSS = """
/* ═══════════════════════════════════════════════════════════════════════
   PATCH 38 — Card Polish & Section Glass
   Melhoria visual: sombras, section panels, cores residuais
   ═══════════════════════════════════════════════════════════════════════ */

/* ── 1. Sombras mais fortes nos cards (fundo #93BBEB exige mais profundidade) ── */
:root {
  --shadow-card:  0 2px 8px rgba(10,40,80,0.14), 0 1px 3px rgba(10,40,80,0.08) !important;
  --shadow-hover: 0 6px 22px rgba(10,40,80,0.18), 0 2px 8px rgba(10,40,80,0.10) !important;
  --shadow-sm:    0 1px 4px rgba(10,40,80,0.10);
}

.card {
  box-shadow: 0 2px 8px rgba(10,40,80,0.14), 0 1px 3px rgba(10,40,80,0.08) !important;
  border: 1px solid var(--border-light) !important;
}
.card:hover {
  box-shadow: 0 6px 22px rgba(10,40,80,0.18), 0 2px 8px rgba(10,40,80,0.10) !important;
  border-color: var(--border-base) !important;
}

/* ── 2. Efeito hover nos cards: linha azul no topo (era gold) ── */
.card { position: relative; overflow: hidden; }
.card::before {
  content: '';
  position: absolute; top: 0; left: 0; right: 0; height: 0;
  background: var(--blue-500);
  border-radius: var(--radius-md) var(--radius-md) 0 0;
  transition: height .2s;
  z-index: 1;
}
.card:hover::before { height: 3px; }

/* ── 3. KPI cells com sombra ajustada ── */
.kpi-cell {
  box-shadow: 0 2px 8px rgba(10,40,80,0.13), 0 1px 3px rgba(10,40,80,0.07) !important;
  border: 1px solid rgba(94,153,208,0.5) !important;
  background: #FFFFFF !important;
}
.kpi-cell:hover {
  box-shadow: 0 5px 18px rgba(10,40,80,0.17) !important;
  border-color: var(--border-base) !important;
}

/* ── 4. Section header panels: green/amber tint → glass white ── */
/* Sell In / Cobertura / qualquer painel com tint verde */
[style*="rgba(52,211,153,0.08)"],
[style*="rgba(52,211,153,0.02)"] {
  background: rgba(255,255,255,0.82) !important;
  border: 1px solid rgba(94,153,208,0.45) !important;
  backdrop-filter: blur(4px) !important;
  box-shadow: 0 2px 10px rgba(10,40,80,0.10) !important;
}

/* Diagnóstico / qualquer painel com tint âmbar */
[style*="rgba(251,191,36,0.08)"],
[style*="rgba(251,191,36,0.02)"] {
  background: rgba(255,255,255,0.82) !important;
  border: 1px solid rgba(94,153,208,0.45) !important;
  backdrop-filter: blur(4px) !important;
  box-shadow: 0 2px 10px rgba(10,40,80,0.10) !important;
}

/* ── 5. Textos neon remanescentes nos section headers ── */
/* Label superior das sections (era #34d399 verde neon) */
[style*="color:#34d399"] { color: #059669 !important; }
[style*="color:#34D399"] { color: #059669 !important; }
/* Título principal das sections (era #e2e8f0 branco) */
[style*="color:#e2e8f0"]  { color: #1E293B !important; }
[style*="color:#E2E8F0"]  { color: #1E293B !important; }
/* Sub-título (era #94A3B8 branco-acinzentado) — só em section headers */
[style*="margin-bottom:20px"] > [style*="color:#94A3B8"] { color: #475569 !important; }

/* ── 6. OL card escuro → claro ── */
[style*="background:linear-gradient(135deg,#0D1117"],
[style*="background: linear-gradient(135deg, #0D1117"] {
  background: #FFFFFF !important;
  border-color: var(--border-light) !important;
}
[style*="rgba(245,225,164,0.35)"] {
  border-color: var(--border-base) !important;
  background: #FFFFFF !important;
}

/* ── 7. Tabelas: thead elegante com gradiente sutil ── */
table thead tr,
table tr:first-child { background: transparent !important; }
table th {
  background: linear-gradient(180deg, #EEF4FC 0%, #E6EFF9 100%) !important;
  color: var(--text-muted) !important;
  border-bottom: 1.5px solid var(--border-base) !important;
  font-size: 10.5px !important;
  letter-spacing: 0.04em !important;
  padding: 8px 10px !important;
}
table td {
  color: var(--text-primary) !important;
  border-bottom: 1px solid rgba(147,187,235,0.3) !important;
}
table tr:hover td {
  background: rgba(255,255,255,0.55) !important;
}

/* ── 8. Filtros: glass mais contrastante ── */
.filters {
  background: rgba(255,255,255,0.55) !important;
  border-bottom: 1px solid var(--border-base) !important;
  backdrop-filter: blur(8px) !important;
}

/* ── 9. Card header (título + toggle) ── */
.card-header {
  border-bottom: 1px solid rgba(147,187,235,0.35) !important;
  padding-bottom: 10px !important;
  margin-bottom: 12px !important;
}
.card-title  { color: var(--text-heading) !important; font-weight: 700 !important; }
.card-sub    { color: var(--text-faint)   !important; font-size: 11px !important; }

/* ── 10. Toggle group sobre fundo azul ── */
.toggle-group,
.tgl-group {
  background: rgba(255,255,255,0.45) !important;
  border: 1px solid rgba(94,153,208,0.4) !important;
  box-shadow: inset 0 1px 3px rgba(10,40,80,0.07) !important;
}
.tgl.active,
.toggle-btn.active {
  background: #FFFFFF !important;
  color: var(--blue-700) !important;
  box-shadow: 0 1px 4px rgba(10,40,80,0.12) !important;
  font-weight: 700 !important;
}
.tgl { color: var(--text-muted) !important; }

/* ── 11. Main panel padding ligeiramente maior ── */
.main.active {
  padding: 20px 24px !important;
}

/* ── 12. Scrollbar refinada p/ fundo azul ── */
::-webkit-scrollbar-track {
  background: rgba(147,187,235,0.3) !important;
  border-radius: 4px !important;
}

/* ── 13. Section-label linha lateral ── */
.section-label {
  border-left: 3px solid var(--blue-500) !important;
  padding-left: 10px !important;
  color: var(--text-heading) !important;
}

/* ── 14. Badge "Atualizado" mais visível ── */
#dash-update-badge {
  box-shadow: 0 1px 4px rgba(5,150,105,0.2) !important;
}

/* FIM PATCH 38 */
"""

html = html.replace(ANCHOR, ANCHOR + '\n<style>' + CSS + '</style>')

print('[PATCH 38] Card Polish aplicado')
print('CSS inserido: {} chars'.format(len(CSS)))
print('Diff: {:+,} bytes'.format(len(html) - orig))

ts = datetime.datetime.now().strftime('%Y%m%d_%H%M')
ver = 'Dashboard_farma_sul/versoes/Dashboard_Farma_Sul_{}_CardPolish.html'.format(ts)
open(SRC, 'w', encoding='utf-8').write(html)
open(ver, 'w', encoding='utf-8').write(html)
print('Salvo:', SRC)
print('Versao:', ver)
