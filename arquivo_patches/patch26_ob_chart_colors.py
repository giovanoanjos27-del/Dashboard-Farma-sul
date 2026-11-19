"""
PATCH 26 - OB Chart Colors / Contraste no Tema Claro
Corrige elementos Odor Block invisiveis no fundo branco:

1. OB_COLORS: 'T. Odor Block' #e2e8f0 -> #475569 (invislvel -> cinza escuro)
2. ob-mkt-chart bars: c+'BB' (73% opacity) -> c (solido, mais vivos)
3. ob-mkt KPI chip 'Total Mercado': cor #e2e8f0 -> #64748B
4. renderOBShare/Preco/Vendas KPI chips: bg rgba(0,0,0,0.2) -> #FFFFFF
5. renderOBShare/Preco/Vendas: label color #3d6b63 -> #334155
6. renderOBShare/Preco: pointBorderColor #101828 -> rgba(59,130,246,0.3)
7. OB table TOTAL row: text color #34d399 -> #0F172A (verde fraco -> escuro)
8. OB table Share column: Total row cor #34d399 -> #0F172A
"""
import datetime

SRC = r'Dashboard_farma_sul\Dashboard_Farma_Sul_20260512_2220.html'
html = open(SRC, encoding='utf-8').read()
original_len = len(html)
patches = 0

def do_replace(old, new, desc, count=1):
    global html, patches
    if old not in html:
        print('[MISS] ' + desc)
        return False
    n = html.count(old)
    html = html.replace(old, new, count)
    patches += 1
    if count == 1:
        print('[OK] ' + desc)
    else:
        print('[OK x{}] {}'.format(n if count is None else count, desc))
    return True

# ==============================================================================
# 1. OB_COLORS: T. Odor Block #e2e8f0 (branco-cinza) -> #64748B (cinza medio)
# ==============================================================================
do_replace(
    '"T. Odor Block": "#e2e8f0"',
    '"T. Odor Block": "#64748B"',
    'OB_COLORS T.Odor Block #e2e8f0 -> #64748B'
)

# ==============================================================================
# 2. ob-mkt-chart: remover BB de opacity das barras (solido no fundo branco)
# ==============================================================================
do_replace(
    "backgroundColor: cSorted.map(function(c){return c+'BB';}),",
    "backgroundColor: cSorted,",
    'ob-mkt-chart backgroundColor c+BB -> solido'
)

# ==============================================================================
# 3. ob-mkt KPI chip 'Total Mercado': cor #e2e8f0 -> #64748B
#    (borda do chip era quase invisivel no branco)
# ==============================================================================
do_replace(
    "{label:'Total Mercado', key:'T. Odor Block', cor:'#e2e8f0'}",
    "{label:'Total Mercado', key:'T. Odor Block', cor:'#64748B'}",
    'ob-mkt KPI chip Total Mercado cor -> #64748B'
)

# ==============================================================================
# 4+5. renderOBShare/Preco/Vendas KPI chips:
#       bg rgba(0,0,0,0.2) -> #FFFFFF
#       label color #3d6b63 -> #334155
# ==============================================================================
do_replace(
    "'<div style=\"background:rgba(0,0,0,0.2);border-radius:8px;padding:10px 12px;border-top:1.5px solid '+cor+';\">'"
    "+'<div style=\"font-size:9px;font-weight:700;letter-spacing:0.08em;color:#3d6b63;margin-bottom:3px;\">'+p.replace('Pato ','')",
    "'<div style=\"background:#FFFFFF;border-radius:8px;padding:10px 12px;border:1px solid #DCE3EC;border-top:2px solid '+cor+';\">'"
    "+'<div style=\"font-size:9px;font-weight:700;letter-spacing:0.08em;color:#334155;margin-bottom:3px;\">'+p.replace('Pato ','')",
    'OB Share KPI chips: bg rgba(0,0,0,0.2)->branco, label #3d6b63->#334155'
)

# Variante em renderOBPreco (mesmo padrao)
do_replace(
    "'<div style=\"background:rgba(0,0,0,0.2);border-radius:8px;padding:10px 12px;border-top:1.5px solid '+cor+';\">'"
    "+'<div style=\"font-size:9px;font-weight:700;letter-spacing:0.08em;color:#3d6b63;margin-bottom:3px;\">'+p.replace('Pato ','')",
    "'<div style=\"background:#FFFFFF;border-radius:8px;padding:10px 12px;border:1px solid #DCE3EC;border-top:2px solid '+cor+';\">'"
    "+'<div style=\"font-size:9px;font-weight:700;letter-spacing:0.08em;color:#334155;margin-bottom:3px;\">'+p.replace('Pato ','')",
    'OB Preco KPI chips: bg->branco, label->#334155 (2a ocorrencia)'
)

# Variante em renderOBVendas (mesmo padrao)
do_replace(
    "'<div style=\"background:rgba(0,0,0,0.2);border-radius:8px;padding:10px 12px;border-top:1.5px solid '+cor+';\">'"
    "+'<div style=\"font-size:9px;font-weight:700;letter-spacing:0.08em;color:#3d6b63;margin-bottom:3px;\">'+p.replace('Pato ','')",
    "'<div style=\"background:#FFFFFF;border-radius:8px;padding:10px 12px;border:1px solid #DCE3EC;border-top:2px solid '+cor+';\">'"
    "+'<div style=\"font-size:9px;font-weight:700;letter-spacing:0.08em;color:#334155;margin-bottom:3px;\">'+p.replace('Pato ','')",
    'OB Vendas KPI chips: bg->branco, label->#334155 (3a ocorrencia)'
)

# ==============================================================================
# 6. OB table TOTAL row: text #34d399 (verde) -> #0F172A (escuro legivel)
# ==============================================================================
do_replace(
    "'<td style=\"padding:6px 10px;color:'+(isTotal?'#34d399':r.cor)+';font-weight:'+(isTotal?'700':'500')+';\">'",
    "'<td style=\"padding:6px 10px;color:'+(isTotal?'#0F172A':r.cor)+';font-weight:'+(isTotal?'700':'500')+';\">'",
    'OB table brand td: TOTAL #34d399 -> #0F172A'
)

# Share column TOTAL row: #34d399 -> #0F172A
do_replace(
    "'<td style=\"padding:6px 10px;text-align:right;color:'+(r.shr?r.cor:'#94A3B8')+';font-weight:600;\">'",
    "'<td style=\"padding:6px 10px;text-align:right;color:'+(r.shr?r.cor:'#64748B')+';font-weight:600;\">'",
    'OB table share td: fallback #94A3B8 -> #64748B'
)

# ==============================================================================
# 7. OB delta text #94A3B8 -> #64748B nos KPI chips (mais legivel)
# ==============================================================================
do_replace(
    "'<div style=\"font-size:9px;color:#94A3B8;margin-top:2px;\">'+(delta!=null",
    "'<div style=\"font-size:9px;color:#64748B;margin-top:2px;\">'+(delta!=null",
    'OB KPI chips delta color #94A3B8 -> #64748B (replace_all)',
    count=10  # ate 10 ocorrencias
)

# ==============================================================================
# 8. OB Share/Preco chart: pointBorderColor dark #101828 -> light azul
#    (no fundo branco o ponto preto fica duro)
# ==============================================================================
do_replace(
    "pointBorderColor:'#101828', pointBorderWidth:2,",
    "pointBorderColor:'rgba(59,130,246,0.25)', pointBorderWidth:1.5,",
    'OB charts pointBorderColor #101828 -> azul transparente (replace_all)',
    count=10
)

# ==============================================================================
# 9. OB Share/Preco/Vendas: delta #94A3B8 no KPI chip renderOBPreco/Vendas
# ==============================================================================
do_replace(
    "'<div style=\"font-size:9px;color:#94A3B8;margin-top:2px;\">'+(delta!=null?(parseFloat(delta)>=0?'",
    "'<div style=\"font-size:9px;color:#64748B;margin-top:2px;\">'+(delta!=null?(parseFloat(delta)>=0?'",
    'OB Preco/Vendas delta color -> #64748B',
    count=5
)

# ==============================================================================
# Save
# ==============================================================================
print('\nPatches: {}'.format(patches))
print('Diff   : {:+,} bytes'.format(len(html) - original_len))

ts = datetime.datetime.now().strftime('%Y%m%d_%H%M')
ver = 'Dashboard_farma_sul/versoes/Dashboard_Farma_Sul_{}_OBChartColors.html'.format(ts)
open(SRC, 'w', encoding='utf-8').write(html)
open(ver, 'w', encoding='utf-8').write(html)
print('\nSalvo : {}'.format(SRC))
print('Versao: {}'.format(ver))
