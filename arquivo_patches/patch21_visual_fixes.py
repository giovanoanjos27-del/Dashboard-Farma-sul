"""
PATCH 21 - Nielsen Tema Claro: fixes visuais cirurgicos
8 correcoes de contraste, barras invisiveis, sombras canvas, filtros
SEM alterar logica, calculos, interacoes ou estrutura.

1. renderMSO: FYTD25 barras invisiveis (rgba 12%) -> #CBD5E1 visivel
2. renderMSO2: sombra canvas, pointBorderColor, grids, bar 2025
3. renderMSO3: sombras canvas, barras FYTD25 opacas, brand bars
4. renderSkuShrCard: brand colors, varColors, FYTD25 opacity, ticks/grid
5. renderOBMercado: KPI cards white bg, dark text
6. avgMarketSel: remove dark/green theme
7. CSS: text-shadow none no #panel-nielsen
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
# 1. renderMSO -- FYTD25 barras invisiveis
# ==============================================================================
html, ok = replace_in_fn(html, 'renderMSO',
    "backgroundColor:'rgba(255,255,255,0.12)', borderColor:'rgba(255,255,255,0.25)', borderWidth:1.5, borderRadius:8, borderDash:[4,3]",
    "backgroundColor:'#CBD5E1', borderColor:'#94A3B8', borderWidth:1.5, borderRadius:8")
if ok: patches += 1; print('[OK] renderMSO FYTD25 bars -> #CBD5E1 visivel')
else: print('[MISS] renderMSO FYTD25 bars anchor not found')

# 2. renderMSO -- legend color escuro
html, ok = replace_in_fn(html, 'renderMSO',
    "labels:{color:'#7aa89e',font:{size:9},boxWidth:8}",
    "labels:{color:'#334155',font:{size:9},boxWidth:8}")
if ok: patches += 1; print('[OK] renderMSO legend -> #334155')
else: print('[MISS] renderMSO legend color')

# ==============================================================================
# 3. renderMSO2 -- grid colors (rgba branco 5% -> azul 10%)
# ==============================================================================
html, ok = replace_in_fn(html, 'renderMSO2',
    "grid:{color:'rgba(255,255,255,0.05)'}",
    "grid:{color:'rgba(59,130,246,0.10)'}",
    count=10)
if ok: patches += 1; print('[OK] renderMSO2 grid colors -> azul')
else: print('[MISS] renderMSO2 grid color anchor not found')

# 4. renderMSO2 -- canvas shadow (contorno preto texto percentual)
html, ok = replace_in_fn(html, 'renderMSO2',
    "ctx5.shadowColor='rgba(0,0,0,0.7)';ctx5.shadowBlur=4;",
    "ctx5.shadowColor='rgba(0,0,0,0)';ctx5.shadowBlur=0;")
if ok: patches += 1; print('[OK] renderMSO2 canvas shadow zeroed')
else: print('[MISS] renderMSO2 canvas shadow anchor not found')

# 5. renderMSO2 -- pointBorderColor escuro -> transparente
html, ok = replace_in_fn(html, 'renderMSO2',
    "pointBorderColor:'#0D1117',pointBorderWidth:2,",
    "pointBorderColor:'rgba(59,130,246,0.2)',pointBorderWidth:1,")
if ok: patches += 1; print('[OK] renderMSO2 pointBorderColor -> azul claro')
else: print('[MISS] renderMSO2 pointBorderColor anchor not found')

# 6. renderMSO2 -- bar 2025 dataset (washed out)
html, ok = replace_in_fn(html, 'renderMSO2',
    "backgroundColor:'rgba(100,116,139,0.3)',",
    "backgroundColor:'rgba(148,163,184,0.7)',")
if ok: patches += 1; print('[OK] renderMSO2 bar 2025 backgroundColor -> visivel')
else: print('[MISS] renderMSO2 bar 2025 bg anchor not found')

html, ok = replace_in_fn(html, 'renderMSO2',
    "borderColor:'rgba(100,116,139,0.45)',\n              borderWidth:1,\n              borderRadius:4,",
    "borderColor:'rgba(148,163,184,0.85)',\n              borderWidth:1,\n              borderRadius:4,")
if ok: patches += 1; print('[OK] renderMSO2 bar 2025 borderColor -> visivel')
else:
    html, ok = replace_in_fn(html, 'renderMSO2',
        "borderColor:'rgba(100,116,139,0.45)',",
        "borderColor:'rgba(148,163,184,0.85)',")
    if ok: patches += 1; print('[OK] renderMSO2 bar 2025 borderColor -> visivel (v2)')
    else: print('[MISS] renderMSO2 bar 2025 borderColor anchor not found')

# ==============================================================================
# 7. renderMSO3 -- canvas shadows (dois ctx diferentes)
# ==============================================================================
html, ok = replace_in_fn(html, 'renderMSO3',
    "ctx3.shadowColor='rgba(0,0,0,0.7)';ctx3.shadowBlur=4;",
    "ctx3.shadowColor='rgba(0,0,0,0)';ctx3.shadowBlur=0;")
if ok: patches += 1; print('[OK] renderMSO3 ctx3 shadow zeroed')
else: print('[MISS] renderMSO3 ctx3 shadow anchor not found')

html, ok = replace_in_fn(html, 'renderMSO3',
    "ctx4.shadowColor='rgba(0,0,0,0.7)';ctx4.shadowBlur=4;",
    "ctx4.shadowColor='rgba(0,0,0,0)';ctx4.shadowBlur=0;")
if ok: patches += 1; print('[OK] renderMSO3 ctx4 shadow zeroed')
else: print('[MISS] renderMSO3 ctx4 shadow anchor not found')

# 8. renderMSO3 -- total market FYTD25 bg (ambas as barras: mktotal e HB)
html, ok = replace_in_fn(html, 'renderMSO3',
    "'rgba(100,116,139,0.45)'",
    "'#94A3B8'",
    count=10)
if ok: patches += 1; print('[OK] renderMSO3 FYTD25 bg rgba -> #94A3B8')
else: print('[MISS] renderMSO3 FYTD25 bg anchor not found')

html, ok = replace_in_fn(html, 'renderMSO3',
    "'rgba(100,116,139,0.75)'",
    "'#64748B'",
    count=10)
if ok: patches += 1; print('[OK] renderMSO3 FYTD25 border rgba -> #64748B')
else: print('[MISS] renderMSO3 FYTD25 border anchor not found')

# 9. renderMSO3 -- total market FYTD26 ambar -> azul
html, ok = replace_in_fn(html, 'renderMSO3',
    "'rgba(251,191,36,0.55)'",
    "'#3B82F6'")
if ok: patches += 1; print('[OK] renderMSO3 FYTD26 total ambar -> #3B82F6')
else: print('[MISS] renderMSO3 FYTD26 ambar anchor not found')

html, ok = replace_in_fn(html, 'renderMSO3',
    "borderColor:['rgba(100,116,139,0.75)','#fbbf24'],",
    "borderColor:['#64748B','#1D4ED8'],")
if ok: patches += 1; print('[OK] renderMSO3 total market borders -> #1D4ED8')
else: print('[MISS] renderMSO3 total market border anchor (fbbf24)')

# 10. renderMSO3 -- borderWidth 1 -> 2 nas barras single-dataset (mktotal e HB)
html, ok = replace_in_fn(html, 'renderMSO3',
    "borderWidth:1,borderRadius:5,barPercentage:0.55}]},",
    "borderWidth:2,borderRadius:5,barPercentage:0.55}]},",
    count=10)
if ok: patches += 1; print('[OK] renderMSO3 borderWidth single-bar -> 2')
else: print('[MISS] renderMSO3 borderWidth anchor not found')

# 11. renderMSO3 -- brand FYTD bars (opacidade e FYTD26 mais solido)
html, ok = replace_in_fn(html, 'renderMSO3',
    "backgroundColor:'rgba(100,116,139,0.35)',borderColor:'rgba(100,116,139,0.6)',",
    "backgroundColor:'rgba(148,163,184,0.7)',borderColor:'rgba(148,163,184,0.85)',")
if ok: patches += 1; print('[OK] renderMSO3 brand FYTD25 bars -> visivel')
else: print('[MISS] renderMSO3 brand FYTD25 anchor not found')

html, ok = replace_in_fn(html, 'renderMSO3',
    "backgroundColor:bCols.map(function(c){return c+'99';}),",
    "backgroundColor:bCols.map(function(c){return c+'dd';}),")
if ok: patches += 1; print('[OK] renderMSO3 brand FYTD26 opacity -> dd')
else: print('[MISS] renderMSO3 brand FYTD26 opacity anchor not found')

# ==============================================================================
# 12. _skuShrBrandColors -- atualizar cores para o tema claro
# ==============================================================================
OLD_SKU_COLORS = """var _skuShrBrandColors = {
  'OFF! Family':'#f97316','OFF! Kids ':'#fb923c','OFF! Baby':'#fdba74',
  'OFF! Family Loção 200ml PR':'#f97316','OFF! Family Spray 170ml PR':'#fb923c',
  'OFF! Family Spray 100ml RG':'#fdba74','OFF! Family Loção 200ml RG':'#fdba74',
  'OFF! Family 170ml RG':'#fdba74','OFF! Family Spray 170+200  RG':'#fdba74',
  'OFF! Family Loção 100ml RG':'#fdba74',
  'Xô Spray 200ml':'#38bdf8','Xô Loção 200ml':'#7dd3fc','Xô Aerossol':'#7dd3fc',
  'Exposis Infantil':'#a78bfa',
  'All Others Aero':'#374151','All Others Loção':'#374151','All Others Spray':'#374151',
  'Repelex Super Spray 100ml PR':'#4b5563','Repelex Super Loção 200ml':'#4b5563',
  'Repelex Super Loção 100ml':'#4b5563','Repelex Super Loção 200ml Promo':'#4b5563'
};"""

NEW_SKU_COLORS = """var _skuShrBrandColors = {
  'OFF! Family':'#F59E0B','OFF! Kids ':'#FBBF24','OFF! Baby':'#FCD34D',
  'OFF! Family Loção 200ml PR':'#F59E0B','OFF! Family Spray 170ml PR':'#FBBF24',
  'OFF! Family Spray 100ml RG':'#FCD34D','OFF! Family Loção 200ml RG':'#FCD34D',
  'OFF! Family 170ml RG':'#FCD34D','OFF! Family Spray 170+200  RG':'#FCD34D',
  'OFF! Family Loção 100ml RG':'#FCD34D',
  'Xô Spray 200ml':'#0EA5E9','Xô Loção 200ml':'#38BDF8','Xô Aerossol':'#38BDF8',
  'Exposis Infantil':'#8B5CF6',
  'All Others Aero':'#475569','All Others Loção':'#475569','All Others Spray':'#475569',
  'Repelex Super Spray 100ml PR':'#64748B','Repelex Super Loção 200ml':'#64748B',
  'Repelex Super Loção 100ml':'#64748B','Repelex Super Loção 200ml Promo':'#64748B'
};"""

if OLD_SKU_COLORS in html:
    html = html.replace(OLD_SKU_COLORS, NEW_SKU_COLORS, 1)
    patches += 1; print('[OK] _skuShrBrandColors -> novas cores tema claro')
else: print('[MISS] _skuShrBrandColors anchor not found')

# 13. renderSkuShrCard -- varColors e varBorders (verde apagado -> solido)
html, ok = replace_in_fn(html, 'renderSkuShrCard',
    "var varColors = vars.map(function(v){return v>=0?'rgba(52,211,153,0.85)':'rgba(239,68,68,0.85)';});",
    "var varColors = vars.map(function(v){return v>=0?'#10B981':'#EF4444';});")
if ok: patches += 1; print('[OK] renderSkuShrCard varColors -> solido')
else: print('[MISS] renderSkuShrCard varColors anchor not found')

html, ok = replace_in_fn(html, 'renderSkuShrCard',
    "var varBorders= vars.map(function(v){return v>=0?'#34d399':'#ef4444';});",
    "var varBorders= vars.map(function(v){return v>=0?'#10B981':'#EF4444';});")
if ok: patches += 1; print('[OK] renderSkuShrCard varBorders -> solido')
else: print('[MISS] renderSkuShrCard varBorders anchor not found')

# 14. renderSkuShrCard -- FYTD25 opacity + FYTD26 borderWidth
html, ok = replace_in_fn(html, 'renderSkuShrCard',
    "{label:'FYTD25',data:sh25,backgroundColor:'rgba(156,163,175,0.18)',borderColor:'rgba(156,163,175,0.4)',borderWidth:1,borderRadius:2},",
    "{label:'FYTD25',data:sh25,backgroundColor:'rgba(148,163,184,0.8)',borderColor:'rgba(148,163,184,0.9)',borderWidth:1.5,borderRadius:2},")
if ok: patches += 1; print('[OK] renderSkuShrCard FYTD25 -> visivel')
else: print('[MISS] renderSkuShrCard FYTD25 bars anchor not found')

html, ok = replace_in_fn(html, 'renderSkuShrCard',
    "{label:'FYTD26',data:sh26,backgroundColor:bgColors,borderColor:bgColors,borderWidth:0,borderRadius:3}",
    "{label:'FYTD26',data:sh26,backgroundColor:bgColors,borderColor:bgColors,borderWidth:1.5,borderRadius:3}")
if ok: patches += 1; print('[OK] renderSkuShrCard FYTD26 borderWidth -> 1.5')
else: print('[MISS] renderSkuShrCard FYTD26 borderWidth anchor not found')

# 15. renderSkuShrCard -- Y-ticks (#e2e8f0 invisivel) + X-grid (ambar 5%)
html, ok = replace_in_fn(html, 'renderSkuShrCard',
    "grid:{color:'rgba(245,225,164,0.05)'}}",
    "grid:{color:'rgba(59,130,246,0.10)'}}")
if ok: patches += 1; print('[OK] renderSkuShrCard X-grid -> azul')
else: print('[MISS] renderSkuShrCard X-grid anchor not found')

html, ok = replace_in_fn(html, 'renderSkuShrCard',
    "y:{ticks:{color:'#e2e8f0',font:{size:10,weight:'600'}},grid:{display:false}}",
    "y:{ticks:{color:'#475569',font:{size:10,weight:'600'}},grid:{display:false}}")
if ok: patches += 1; print('[OK] renderSkuShrCard Y-ticks -> #475569')
else: print('[MISS] renderSkuShrCard Y-ticks anchor not found')

# ==============================================================================
# 16. renderOBMercado -- KPI cards: white bg, dark text
# ==============================================================================
OLD_OB_KPI = (
    '    return \'<div style="background:rgba(59,130,246,0.06);border-radius:8px;'
    'padding:10px 12px;border-top:1.5px solid \'+item.cor+\';">\'\n'
    '      +\'<div style="font-size:9px;font-weight:700;letter-spacing:0.08em;'
    'color:#3d6b63;margin-bottom:3px;">\'+item.label+\'</div>\'\n'
    '      +\'<div style="font-size:17px;font-weight:800;color:\'+item.cor+\';'
    'line-height:1;">\'+fmtV(cur)+\'</div>\'\n'
    '      +(shr ? \'<div style="font-size:9px;color:\'+item.cor+\';'
    'margin-top:2px;font-weight:600;">\'+shr+\' share</div>\' : \'\')\n'
    '      +\'<div style="font-size:9px;color:#94A3B8;margin-top:1px;">\'+'
    '(dlt!=null?(dlt>=0?\'▲+\':\'▼\')+Math.abs(dlt).toFixed(1)+\'% vs mês ant.\':\'—\')+\'</div>\'\n'
    '      +\'</div>\';'
)

NEW_OB_KPI = (
    '    return \'<div style="background:#FFFFFF;border-radius:8px;'
    'padding:10px 12px;border:1px solid #D9E2EC;border-top:1.5px solid \'+item.cor+'
    '\';box-shadow:0 1px 3px rgba(15,23,42,0.06);">\'\n'
    '      +\'<div style="font-size:9px;font-weight:700;letter-spacing:0.08em;'
    'color:#334155;margin-bottom:3px;">\'+item.label+\'</div>\'\n'
    '      +\'<div style="font-size:17px;font-weight:800;color:#0F172A;'
    'line-height:1;">\'+fmtV(cur)+\'</div>\'\n'
    '      +(shr ? \'<div style="font-size:9px;color:#475569;'
    'margin-top:2px;font-weight:600;">\'+shr+\' share</div>\' : \'\')\n'
    '      +\'<div style="font-size:9px;color:#94A3B8;margin-top:1px;">\'+'
    '(dlt!=null?(dlt>=0?\'▲+\':\'▼\')+Math.abs(dlt).toFixed(1)+\'% vs mês ant.\':\'—\')+\'</div>\'\n'
    '      +\'</div>\';'
)

if OLD_OB_KPI in html:
    html = html.replace(OLD_OB_KPI, NEW_OB_KPI, 1)
    patches += 1; print('[OK] renderOBMercado KPI cards -> white bg dark text')
else:
    # Fallback: target individual sub-strings
    print('[MISS] renderOBMercado KPI full block -- tentando sub-patches')
    html, ok = replace_in_fn(html, 'renderOBMercado',
        'background:rgba(59,130,246,0.06);border-radius:8px;padding:10px 12px;border-top:1.5px solid \'',
        'background:#FFFFFF;border-radius:8px;padding:10px 12px;border:1px solid #D9E2EC;border-top:1.5px solid \'')
    if ok: patches += 1; print('[OK] renderOBMercado KPI bg sub-patch')
    else: print('[MISS] renderOBMercado KPI bg sub-patch')

    html, ok = replace_in_fn(html, 'renderOBMercado',
        'color:#3d6b63;margin-bottom:3px;"',
        'color:#334155;margin-bottom:3px;"')
    if ok: patches += 1; print('[OK] renderOBMercado KPI title color')
    else: print('[MISS] renderOBMercado KPI title color')

    html, ok = replace_in_fn(html, 'renderOBMercado',
        '\'<div style="font-size:17px;font-weight:800;color:\'+item.cor+\';line-height:1;">\'',
        '\'<div style="font-size:17px;font-weight:800;color:#0F172A;line-height:1;">\'')
    if ok: patches += 1; print('[OK] renderOBMercado KPI value color -> #0F172A')
    else: print('[MISS] renderOBMercado KPI value color')

    html, ok = replace_in_fn(html, 'renderOBMercado',
        '\'<div style="font-size:9px;color:\'+item.cor+\';margin-top:2px;font-weight:600;">\'',
        '\'<div style="font-size:9px;color:#475569;margin-top:2px;font-weight:600;">\'')
    if ok: patches += 1; print('[OK] renderOBMercado KPI share color -> #475569')
    else: print('[MISS] renderOBMercado KPI share color')

# ==============================================================================
# 17. avgMarketSel -- remover dark/green theme
# ==============================================================================
OLD_AVG_SEL = (
    'style="font-size:11px;padding:6px 28px 6px 10px;border-radius:7px;'
    'border:0.5px solid rgba(52,211,153,0.3);background:#161B22;color:#e2e8f0;'
    "cursor:pointer;font-family:inherit;appearance:none;background-image:url(&quot;"
    "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='10' height='6'%3E"
    "%3Cpath d='M0 0l5 6 5-6z' fill='%2334d399'/%3E%3C/svg%3E&quot;);"
    'background-repeat:no-repeat;background-position:right 10px center;"'
)

NEW_AVG_SEL = (
    'style="font-size:11px;padding:6px 28px 6px 10px;border-radius:7px;'
    'border:1px solid #CBD5E1;background:#FFFFFF;color:#1E293B;'
    "cursor:pointer;font-family:inherit;appearance:none;background-image:url(&quot;"
    "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='10' height='6'%3E"
    "%3Cpath d='M0 0l5 6 5-6z' fill='%231E293B'/%3E%3C/svg%3E&quot;);"
    'background-repeat:no-repeat;background-position:right 10px center;"'
)

if OLD_AVG_SEL in html:
    html = html.replace(OLD_AVG_SEL, NEW_AVG_SEL, 1)
    patches += 1; print('[OK] avgMarketSel -> light theme')
else: print('[MISS] avgMarketSel anchor not found')

# ==============================================================================
# 18. CSS global -- text-shadow none para todo #panel-nielsen
# ==============================================================================
OLD_CSS_ANCHOR = '.u-badge-cyan{font-size:9px;font-weight:700;background:#06b6d422;color:#06b6d4;border-radius:3px;padding:1px 5px;}'
NEW_CSS_EXTRA = '''
/* ================================================================
   PATCH 21 -- Remove text-shadow/filter artefatos tema claro Nielsen
   ================================================================ */
#panel-nielsen * { text-shadow: none !important; }
/* avgMarketSel option hover/selected no tema claro */
body.nielsen-theme #avgMarketSel option:checked,
body.nielsen-theme #avgMarketSel option:focus {
  background: #2563EB !important;
  color: #FFFFFF !important;
}
'''

if OLD_CSS_ANCHOR in html:
    html = html.replace(OLD_CSS_ANCHOR, OLD_CSS_ANCHOR + NEW_CSS_EXTRA, 1)
    patches += 1; print('[OK] CSS text-shadow:none + avgMarketSel option styles')
else: print('[MISS] CSS anchor u-badge-cyan not found')

# ==============================================================================
# Save
# ==============================================================================
print(f'\nPatches aplicados: {patches}')
print(f'Diff             : {len(html) - original_len:+,} bytes')

ts = datetime.datetime.now().strftime('%Y%m%d_%H%M')
ver = f'Dashboard_farma_sul/versoes/Dashboard_Farma_Sul_{ts}_NielsenVisualFixes.html'
open(SRC, 'w', encoding='utf-8').write(html)
open(ver, 'w', encoding='utf-8').write(html)
print(f'\nSalvo : {SRC}')
print(f'Versao: {ver}')
