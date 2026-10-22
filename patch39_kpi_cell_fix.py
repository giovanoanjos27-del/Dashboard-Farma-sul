"""
PATCH 39 - KPI Cell Fix
Root cause: var(--card) nao definido → fundo transparente → mostra azul da página
Fix:
1. JS: var(--card) → #FFFFFF + border correto (top colorida + lados suaves) + label color
2. CSS: --card definido + #sellin-kpis-total > div override forte
3. Mesmo fix para outros painéis que usem var(--card)
"""
import datetime

SRC = r'Dashboard_farma_sul\Dashboard_Farma_Sul_20260512_2220.html'
html = open(SRC, encoding='utf-8').read()
orig = len(html)

fixes = 0

def rep(old, new, label=''):
    global html, fixes
    if old not in html:
        print(f'  NAO ENCONTRADO: {label or old[:60]}')
        return
    html = html.replace(old, new)
    fixes += 1
    print(f'  OK: {label or old[:60]}')

print('[PATCH 39] KPI Cell Fix')

# ── 1. Fix JS template: var(--card) → #FFFFFF + border correto + label cor ──
rep(
    '<div style="background:var(--card);border-radius:12px;padding:16px;border-top:2px solid \'+k.ac+\';border:0.5px solid \'+k.ac+\'33;">\'',
    '<div style="background:#FFFFFF;border-radius:12px;padding:16px 18px;border-top:3px solid \'+k.ac+\';border-left:1px solid rgba(94,153,208,0.35);border-right:1px solid rgba(94,153,208,0.35);border-bottom:1px solid rgba(94,153,208,0.35);box-shadow:0 2px 10px rgba(10,40,80,0.13),0 1px 3px rgba(10,40,80,0.07);">\'',
    'KPI cell template: background + border'
)

rep(
    '<div style="font-size:9px;font-weight:700;letter-spacing:0.1em;color:#3d6b63;margin-bottom:6px;">\'',
    '<div style="font-size:9px;font-weight:700;letter-spacing:0.1em;color:#475569;text-transform:uppercase;margin-bottom:6px;">\'',
    'KPI cell label color #3d6b63 → #475569'
)

# ── 2. Também corrigir outros var(--card) que possam existir no HTML ──
count_card_var = html.count('var(--card)')
if count_card_var > 0:
    html = html.replace('var(--card)', '#FFFFFF')
    fixes += 1
    print(f'  OK: var(--card) → #FFFFFF ({count_card_var} ocorrencias)')

# ── 3. CSS: definir --card + override forte para KPI rows ──
CSS_INJECT = """
/* ═══════════════════════════════════════════════════════════════════════
   PATCH 39 — KPI Cell Fix: var(--card) definido + overrides
   ═══════════════════════════════════════════════════════════════════════ */

/* Define --card (alias de --bg-card) para compatibilidade com JS legado */
:root { --card: #FFFFFF; }

/* Override forte: todos os filhos diretos dos containers KPI */
#sellin-kpis-total > div,
#sellin-kpis-cli  > div,
[id$="-kpis"] > div,
[id$="-kpis-total"] > div {
  background: #FFFFFF !important;
  box-shadow: 0 2px 10px rgba(10,40,80,0.13), 0 1px 3px rgba(10,40,80,0.07) !important;
  border-left: 1px solid rgba(94,153,208,0.35) !important;
  border-right: 1px solid rgba(94,153,208,0.35) !important;
  border-bottom: 1px solid rgba(94,153,208,0.35) !important;
}

/* Sub-elementos dentro dos KPI cells */
#sellin-kpis-total > div > div[style*="color:#94A3B8"],
#sellin-kpis-total > div > div[style*="color:#94a3b8"] {
  color: #64748B !important;
}

/* Sellin container grid gap */
#sellin-kpis-total {
  gap: 10px !important;
  margin-bottom: 20px !important;
}

/* FIM PATCH 39 */
"""

ANCHOR = '/* FIM PATCH 38 */\n</style>'
if ANCHOR in html:
    html = html.replace(ANCHOR, '/* FIM PATCH 38 */\n</style>\n<style>' + CSS_INJECT)
    fixes += 1
    print('  OK: CSS patch39 injetado apos patch38')
else:
    # Fallback: inject after patch36
    ANCHOR2 = '/* FIM PATCH 36 */'
    html = html.replace(ANCHOR2, ANCHOR2 + '\n<style>' + CSS_INJECT)
    fixes += 1
    print('  OK: CSS patch39 injetado (fallback apos patch36)')

print(f'\nTotal: {fixes} fixes')
print('Diff: {:+,} bytes'.format(len(html) - orig))

ts = datetime.datetime.now().strftime('%Y%m%d_%H%M')
ver = 'Dashboard_farma_sul/versoes/Dashboard_Farma_Sul_{}_KpiCellFix.html'.format(ts)
open(SRC, 'w', encoding='utf-8').write(html)
open(ver, 'w', encoding='utf-8').write(html)
print('Salvo:', SRC)
print('Versao:', ver)
