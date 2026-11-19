"""
PATCH 34 — Fix #panel-plano background + Cobertura map lowercase hex
1. #panel-plano{background:#0F172A} nao estava sobrescrito → claro
2. [style*="background:#0a1218"] (lowercase) → branco (mapa YoY + GPF)
3. .pln-dc-nome color fix (era #F1F5F9, quase branco sobre branco)
4. .pln-pbwrap track fix (era rgba(255,255,255,0.06), invisivel no claro)
"""
import datetime, os

SRC = r'Dashboard_farma_sul\Dashboard_Farma_Sul_20260512_2220.html'
html = open(SRC, encoding='utf-8').read()
original_len = len(html)

ANCHOR = '/* FIM PATCH 33 */'

EXTRA_CSS = '''/* FIM PATCH 33 */

/* ==========================================================================
   PATCH 34 - #panel-plano bg fix + Cobertura map lowercase hex + pln text
   ========================================================================== */

/* --- Plano de Negócios: panel background estava #0F172A, sem override ---*/
#panel-plano { background: #F4F7FB !important; }

/* --- Plano de Negócios: textos escuros que ainda faltavam --- */
.pln-dc-nome   { color: #1E293B !important; }
.pln-dc-hd     { background: rgba(234,179,8,0.06) !important; }
.pln-pbwrap    { background: rgba(148,163,184,0.18) !important; }
.pln-mpts      { color: #B45309 !important; }

/* --- Cobertura: mapa YoY e GPF geram background:#0a1218 (lowercase) --- */
/* Patch30 tinha #0A1218 (uppercase) — CSS attr selectors sao case-sensitive */
[style*="background:#0a1218"] { background: #FFFFFF !important; }

/* --- GAM/Riomed/Cobertura: outros escuros encontrados --- */
[style*="background:#0b1220"]  { background: #F4F7FB !important; }
[style*="background:#111827"]  { background: #F8FAFC !important; }
[style*="background:#1f2937"]  { background: #F1F5F9 !important; }
[style*="background:#111e35"]  { background: #FFFFFF !important; }

/* FIM PATCH 34 */'''

if ANCHOR in html:
    html = html.replace(ANCHOR, EXTRA_CSS, 1)
    print('[OK] CSS patch34 injetado (panel-plano bg + map lowercase + pln text)')
else:
    print('[MISS] ancora "/* FIM PATCH 33 */" nao encontrada — verificar')

print('Diff: {:+,} bytes'.format(len(html) - original_len))

ts = datetime.datetime.now().strftime('%Y%m%d_%H%M')
ver = 'Dashboard_farma_sul/versoes/Dashboard_Farma_Sul_{}_PlanoMapFix.html'.format(ts)

open(SRC, 'w', encoding='utf-8').write(html)
open(ver, 'w', encoding='utf-8').write(html)
print('Salvo: ' + SRC)
print('Versao: ' + ver)
