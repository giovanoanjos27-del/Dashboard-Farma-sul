"""
PATCH 22 - Fixes residuais: SKU Y-labels + OB table background

1. renderSkuShrCard direito (VAR): Y-ticks #e2e8f0 -> #1e293b, grid azul, zero line azul
2. renderSkuShrCard esquerdo: Y-ticks #475569 -> #1e293b (mais escuro como pedido)
3. ob-mkt-table: background:#0F172A -> transparent (HTML inline)
4. ob-mkt-diag: background:#161B22 -> #F0F4FA (HTML inline)
5. obMarketSel4: dark -> light (HTML inline)
6. CSS: seletores OB, diag e toggles no tema claro
"""
import datetime

SRC = r'Dashboard_farma_sul\Dashboard_Farma_Sul_20260512_2220.html'
html = open(SRC, encoding='utf-8').read()
original_len = len(html)
patches = 0

def replace_in_fn(h, fn_name, old, new, count=1):
    start = h.find('function ' + fn_name + '(')
    if start == -1: return h, False
    end = h.find('\nfunction ', start + 10)
    if end == -1: end = start + 200000
    chunk = h[start:end]
    if old not in chunk: return h, False
    new_chunk = chunk.replace(old, new, count)
    return h[:start] + new_chunk + h[end:], True

# ==============================================================================
# 1. renderSkuShrCard -- LEFT chart: Y-ticks #475569 -> #1e293b (mais escuro)
# ==============================================================================
html, ok = replace_in_fn(html, 'renderSkuShrCard',
    "y:{ticks:{color:'#475569',font:{size:10,weight:'600'}},grid:{display:false}}",
    "y:{ticks:{color:'#1e293b',font:{size:10,weight:'600'}},grid:{display:false}}")
if ok: patches += 1; print('[OK] SKU LEFT chart Y-ticks -> #1e293b')
else: print('[MISS] SKU LEFT chart Y-ticks anchor not found')

# ==============================================================================
# 2. renderSkuShrCard -- RIGHT chart (VAR): Y-ticks e2e8f0 -> #1e293b
# ==============================================================================
html, ok = replace_in_fn(html, 'renderSkuShrCard',
    "y:{ticks:{color:'#e2e8f0',font:{size:10,weight:'600'}},grid:{display:false}}",
    "y:{ticks:{color:'#1e293b',font:{size:10,weight:'600'}},grid:{display:false}}")
if ok: patches += 1; print('[OK] SKU RIGHT chart Y-ticks -> #1e293b')
else: print('[MISS] SKU RIGHT chart Y-ticks anchor not found')

# 3. RIGHT chart: X-grid amber 5% -> azul + border visivel
html, ok = replace_in_fn(html, 'renderSkuShrCard',
    "grid:{color:'rgba(245,225,164,0.05)'},\n             border:{color:'rgba(255,255,255,0.15)'}},",
    "grid:{color:'rgba(59,130,246,0.10)'},\n             border:{color:'rgba(59,130,246,0.10)'}},")
if ok: patches += 1; print('[OK] SKU RIGHT chart X-grid/border -> azul')
else:
    # try without newline variant
    html, ok = replace_in_fn(html, 'renderSkuShrCard',
        "grid:{color:'rgba(245,225,164,0.05)'},\n             border:{color:'rgba(255,255,255,0.15)'}",
        "grid:{color:'rgba(59,130,246,0.10)'},\n             border:{color:'rgba(59,130,246,0.10)'}")
    if ok: patches += 1; print('[OK] SKU RIGHT chart X-grid/border -> azul (v2)')
    else: print('[MISS] SKU RIGHT chart X-grid/border anchor not found')

# 4. RIGHT chart: zero line white -> azul visivel
html, ok = replace_in_fn(html, 'renderSkuShrCard',
    "ctx2.strokeStyle='rgba(255,255,255,0.25)';",
    "ctx2.strokeStyle='rgba(59,130,246,0.35)';")
if ok: patches += 1; print('[OK] SKU RIGHT chart zero line -> azul')
else: print('[MISS] SKU RIGHT chart zero line anchor not found')

# ==============================================================================
# 5. ob-mkt-table: fundo escuro #0F172A -> transparente (HTML inline)
# ==============================================================================
OLD_OB_TABLE_DIV = '<div id="ob-mkt-table" style="background:#0F172A;border-radius:10px;overflow:hidden;"></div>'
NEW_OB_TABLE_DIV = '<div id="ob-mkt-table" style="background:transparent;border-radius:10px;overflow:hidden;"></div>'

if OLD_OB_TABLE_DIV in html:
    html = html.replace(OLD_OB_TABLE_DIV, NEW_OB_TABLE_DIV, 1)
    patches += 1; print('[OK] ob-mkt-table background -> transparent')
else: print('[MISS] ob-mkt-table anchor not found')

# ==============================================================================
# 6. ob-mkt-diag: fundo escuro #161B22 -> claro (HTML inline)
# ==============================================================================
OLD_OB_DIAG = 'style="margin-top:14px;padding:12px 16px;background:#161B22;border-radius:10px;border-left:3px solid #34d399;font-size:11px;line-height:1.7;"'
NEW_OB_DIAG = 'style="margin-top:14px;padding:12px 16px;background:#EEF5FF;border-radius:10px;border-left:3px solid #3b82f6;font-size:11px;line-height:1.7;"'

if OLD_OB_DIAG in html:
    html = html.replace(OLD_OB_DIAG, NEW_OB_DIAG, 1)
    patches += 1; print('[OK] ob-mkt-diag -> fundo claro azul')
else: print('[MISS] ob-mkt-diag anchor not found')

# ==============================================================================
# 7. obMarketSel4: dark -> light (HTML inline)
# ==============================================================================
OLD_OB_SEL4 = 'style="font-size:11px;padding:6px 28px 6px 10px;border-radius:7px;border:1px solid rgba(52,211,153,0.3);background:#161B22;color:#e2e8f0;cursor:pointer;outline:none;min-width:140px;"'
NEW_OB_SEL4 = 'style="font-size:11px;padding:6px 10px;border-radius:7px;border:1px solid #CBD5E1;background:#FFFFFF;color:#1E293B;cursor:pointer;outline:none;min-width:140px;"'

if OLD_OB_SEL4 in html:
    html = html.replace(OLD_OB_SEL4, NEW_OB_SEL4, 1)
    patches += 1; print('[OK] obMarketSel4 -> light theme')
else: print('[MISS] obMarketSel4 anchor not found')

# ==============================================================================
# 8. CSS: cobrir OB selects, table total row, diagnóstico texto e toggles
# ==============================================================================
OLD_CSS_ANCHOR = '.u-badge-cyan{font-size:9px;font-weight:700;background:#06b6d422;color:#06b6d4;border-radius:3px;padding:1px 5px;}'
NEW_CSS_EXTRA = '''
/* ================================================================
   PATCH 22 -- OB table + SKU labels + selects tema claro
   ================================================================ */

/* OB table container: sobrescreve background residual via JS */
body.nielsen-theme #ob-mkt-table {
  background: #FFFFFF !important;
  border: 1px solid #D9E2EC !important;
  border-radius: 10px !important;
}
/* OB table thead */
body.nielsen-theme #ob-mkt-table thead tr {
  background: #EDF2F9 !important;
}
/* OB table total row */
body.nielsen-theme #ob-mkt-table tbody tr:first-child {
  background: rgba(59,130,246,0.06) !important;
}
/* OB diagnóstico texto escuro */
body.nielsen-theme #ob-mkt-diag,
body.nielsen-theme #ob-share-diag,
body.nielsen-theme #ob-preco-diag {
  background: #EEF5FF !important;
  border-left-color: #3b82f6 !important;
}
body.nielsen-theme #ob-mkt-diag * { color: #1e293b; }

/* OB selects restantes (obMarketSel, obMarketSel2) */
body.nielsen-theme select[id^="obMarket"] {
  background: #FFFFFF !important;
  border: 1px solid #CBD5E1 !important;
  color: #1E293B !important;
}
/* OB toggle-group buttons */
body.nielsen-theme #panel-nielsen [data-ob] .toggle-group {
  border-color: rgba(59,130,246,0.3) !important;
}
body.nielsen-theme #panel-nielsen [data-ob] .tgl {
  background: transparent !important;
  color: #64748b !important;
}
body.nielsen-theme #panel-nielsen [data-ob] .tgl.active {
  background: rgba(59,130,246,0.12) !important;
  color: #1d4ed8 !important;
}
/* Card-title e card-sub da OB section */
body.nielsen-theme #panel-nielsen [data-ob] .card-title { color: #1e293b !important; }
body.nielsen-theme #panel-nielsen [data-ob] .card-sub   { color: #475569 !important; }
'''

if OLD_CSS_ANCHOR in html:
    html = html.replace(OLD_CSS_ANCHOR, OLD_CSS_ANCHOR + NEW_CSS_EXTRA, 1)
    patches += 1; print('[OK] CSS: OB table + SKU labels + selects no tema claro')
else: print('[MISS] CSS anchor u-badge-cyan not found')

# ==============================================================================
# Save
# ==============================================================================
print(f'\nPatches: {patches}')
print(f'Diff   : {len(html) - original_len:+,} bytes')

ts = datetime.datetime.now().strftime('%Y%m%d_%H%M')
ver = f'Dashboard_farma_sul/versoes/Dashboard_Farma_Sul_{ts}_NielsenSKUObFixes.html'
open(SRC, 'w', encoding='utf-8').write(html)
open(ver, 'w', encoding='utf-8').write(html)
print(f'\nSalvo : {SRC}')
print(f'Versao: {ver}')
