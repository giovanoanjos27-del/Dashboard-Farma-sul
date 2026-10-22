"""
PATCH 37 - Fundo Opcao 5: #93BBEB
Atualiza todas as variaveis de cor proporcional ao novo tom mais intenso.
"""
import datetime, re

SRC = r'Dashboard_farma_sul\Dashboard_Farma_Sul_20260512_2220.html'
html = open(SRC, encoding='utf-8').read()
orig = len(html)

fixes = 0

def rep(old, new, count=0):
    global html, fixes
    if count:
        html = html.replace(old, new, count)
    else:
        html = html.replace(old, new)
    n = html.count(new)
    fixes += 1
    print('  {} -> {} (ok)'.format(old[:50], new[:50]))

print('[PATCH 37] Fundo Opcao 5 (#93BBEB)')

# 1 - :root --bg-base
rep('--bg-base:       #EBF2FA;   /* fundo principal do dashboard */',
    '--bg-base:       #93BBEB;   /* fundo principal do dashboard */')

# 2 - :root --bg-filter (filtros ligeiramente mais escuro que o fundo)
rep('--bg-filter:     #F0F6FF;   /* filter bar */',
    '--bg-filter:     #7BAAD8;   /* filter bar */')

# 3 - :root --bg-subtle
rep('--bg-subtle:     #F4F8FD;   /* hover / row alternada / chip */',
    '--bg-subtle:     #A8C8F0;   /* hover / row alternada / chip */')

# 4 - :root --bg-hover
rep('--bg-hover:      #EAF2FF;   /* hover em linhas / botoes */',
    '--bg-hover:      #A0C4E8;   /* hover em linhas / botoes */')

# 5 - :root bordas (proporcional ao azul mais intenso)
rep('--border-strong: #C8D9EC;   /* bordas de destaque */',
    '--border-strong: #4D8FCC;   /* bordas de destaque */')
rep('--border-base:   #D6E4F0;   /* bordas normais */',
    '--border-base:   #5E99D0;   /* bordas normais */')
rep('--border-light:  #E4EEF8;   /* bordas suaves */',
    '--border-light:  #7BAAD8;   /* bordas suaves */')
rep('--border-faint:  #EDF3FA;   /* bordas quase invisiveis */',
    '--border-faint:  #8DB8DE;   /* bordas quase invisiveis */')

# 6 - body background (patch25 L1068)
rep('body { background:#F4F7FB !important; color:#334155 !important; }',
    'body { background:#93BBEB !important; color:#334155 !important; }')

# 7 - body background (patch25 L32245)
rep('body { background: #F4F7FB !important; color: #334155 !important; }',
    'body { background: #93BBEB !important; color: #334155 !important; }')

# 8 - #panel-expd (patch31)
rep('#panel-expd  { background: #F4F7FB !important; }',
    '#panel-expd  { background: #93BBEB !important; }')

# 9 - #panel-plano (patch34)
rep('#panel-plano { background: #F4F7FB !important; }',
    '#panel-plano { background: #93BBEB !important; }')

# 10 - atrib selector #0b1220
rep('[style*="background:#0b1220"]  { background: #F4F7FB !important; }',
    '[style*="background:#0b1220"]  { background: #93BBEB !important; }')

# 11 - Toggle track (patch36)
rep('background: #DDE8F5 !important;',
    'background: #7BAAD8 !important;')

# 12 - Filtros border (patch36)
rep('.filters {\n  background: var(--bg-filter) !important;\n  border-bottom: 1px solid var(--border-light) !important;\n}',
    '.filters {\n  background: var(--bg-filter) !important;\n  border-bottom: 1px solid var(--border-base) !important;\n}')

# 13 - :root --bg-accent (chip ativo) — tornar mais visivel no azul
rep('--bg-accent:     rgba(59,130,246,0.07); /* fundo de chips ativos */',
    '--bg-accent:     rgba(255,255,255,0.25); /* fundo de chips ativos */')

# 14 - Scrollbar thumb
rep('::-webkit-scrollbar-thumb { background: #B8D0E8; border-radius: 4px; }',
    '::-webkit-scrollbar-thumb { background: #4D8FCC; border-radius: 4px; }')
rep('::-webkit-scrollbar-thumb:hover { background: var(--border-strong); }',
    '::-webkit-scrollbar-thumb:hover { background: #2563EB; }')

print('\nTotal: {} fixes'.format(fixes))
print('Diff: {:+,} bytes'.format(len(html) - orig))

ts = datetime.datetime.now().strftime('%Y%m%d_%H%M')
ver = 'Dashboard_farma_sul/versoes/Dashboard_Farma_Sul_{}_BgOp5.html'.format(ts)
open(SRC, 'w', encoding='utf-8').write(html)
open(ver, 'w', encoding='utf-8').write(html)
print('Salvo: ' + SRC)
print('Versao: ' + ver)
