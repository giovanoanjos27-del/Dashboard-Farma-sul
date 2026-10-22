"""
PATCH 19b — Nielsen Tema Claro: correções JS inline
- renderOBMercado: tabela de marcas (thead dark + textos + linhas alternadas)
- renderAvgPriceChart: tooltip + legenda customizada + ticks + grid
- renderAvgInsight: textos diagnosis claros
"""
import datetime, re

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

def replace_all_in_fn(h, fn_name, old, new):
    start = h.find('function ' + fn_name + '(')
    if start == -1: return h, 0
    end = h.find('\nfunction ', start + 10)
    if end == -1: end = start + 200000
    chunk = h[start:end]
    c = chunk.count(old)
    if c == 0: return h, 0
    return h[:start] + chunk.replace(old, new) + h[end:], c

# ──────────────────────────────────────────────────────────────────────────────
# 1. renderOBMercado — tabela marcas inline
# ──────────────────────────────────────────────────────────────────────────────
fn = 'renderOBMercado'

# thead row background escuro
html, ok = replace_in_fn(html, fn,
    "'<thead><tr style=\"background:#161B22;\">'",
    "'<thead><tr style=\"background:#EDF2F9;\">'")
if ok: patches+=1; print('[OK] OBMercado: thead bg -> #EDF2F9')

# th text color
h_new, c = replace_all_in_fn(html, fn,
    'color:#94A3B8;font-weight:600;">Brand</th>',
    'color:#64748b;font-weight:700;">Brand</th>')
if c: html=h_new; patches+=c; print(f'[OK] OBMercado: th Brand -> #64748b (x{c})')

h_new, c = replace_all_in_fn(html, fn,
    'color:#94A3B8;font-weight:600;">',
    'color:#64748b;font-weight:700;">')
if c: html=h_new; patches+=c; print(f'[OK] OBMercado: th outros -> #64748b (x{c})')

# Linhas alternadas — substituir rgba branco por azul ultra-suave
html, ok = replace_in_fn(html, fn,
    "var bg = isTotal?'rgba(52,211,153,0.06)':i%2===0?'transparent':'rgba(255,255,255,0.02)';",
    "var bg = isTotal?'rgba(59,130,246,0.08)':i%2===0?'transparent':'rgba(59,130,246,0.03)';")
if ok: patches+=1; print('[OK] OBMercado: row alternating bg -> azul')

# Bordas de linha
html, ok = replace_in_fn(html, fn,
    'border-bottom:1px solid rgba(255,255,255,0.05)',
    'border-bottom:1px solid rgba(59,130,246,0.10)')
if ok: patches+=1; print('[OK] OBMercado: row border -> azul sutil')

# Texto das células (valores) — #e2e8f0 e #D1D5DB
h_new, c = replace_all_in_fn(html, fn, 'color:#e2e8f0', 'color:#1e293b')
if c: html=h_new; patches+=c; print(f'[OK] OBMercado: cell color #e2e8f0 -> #1e293b (x{c})')

h_new, c = replace_all_in_fn(html, fn, 'color:#D1D5DB', 'color:#475569')
if c: html=h_new; patches+=c; print(f'[OK] OBMercado: cell color #D1D5DB -> #475569 (x{c})')

# Diagnóstico inline (background escuro dentro do card)
html, ok = replace_in_fn(html, fn, 'background:rgba(0,0,0,0.2)', 'background:rgba(59,130,246,0.06)')
if ok: patches+=1; print('[OK] OBMercado: diag bg -> azul')

# Grid ainda branco no OBMercado chart (color rgba(255,255,255,0.07))
h_new, c = replace_all_in_fn(html, fn, "color:'rgba(255,255,255,0.07)'", "color:'rgba(59,130,246,0.10)'")
if c: html=h_new; patches+=c; print(f'[OK] OBMercado: chart grid -> blue (x{c})')

# Tooltip borderColor residual
html, ok = replace_in_fn(html, fn,
    "borderColor:'rgba(255,255,255,0",
    "borderColor:'rgba(59,130,246,0.2)',borderWidth:1,_unused:'rgba(255,255,255,0")
# Abordagem alternativa — substituir diretamente
h_new, c = replace_all_in_fn(html, fn,
    "borderColor:'rgba(255,255,255,0.12)'",
    "borderColor:'rgba(59,130,246,0.2)'")
if c: html=h_new; patches+=c; print(f'[OK] OBMercado: tooltip borderColor (x{c})')

# ──────────────────────────────────────────────────────────────────────────────
# 2. renderAvgPriceChart — tooltip + legenda customizada + ticks + grid
# ──────────────────────────────────────────────────────────────────────────────
fn = 'renderAvgPriceChart'

# Tooltip bg
html, ok = replace_in_fn(html, fn,
    "backgroundColor: '#1F2937'",
    "backgroundColor: '#F0F4FA'")
if ok: patches+=1; print('[OK] AvgPriceChart: tooltip bg -> #F0F4FA')

html, ok = replace_in_fn(html, fn,
    "titleColor: '#e2e8f0'",
    "titleColor: '#1e293b'")
if ok: patches+=1; print('[OK] AvgPriceChart: tooltip titleColor -> #1e293b')

html, ok = replace_in_fn(html, fn,
    "bodyColor: '#D1D5DB'",
    "bodyColor: '#475569'")
if ok: patches+=1; print('[OK] AvgPriceChart: tooltip bodyColor -> #475569')

html, ok = replace_in_fn(html, fn,
    "borderColor: 'rgba(255,255,255,0.13)'",
    "borderColor: 'rgba(59,130,246,0.2)'")
if ok: patches+=1; print('[OK] AvgPriceChart: tooltip borderColor -> blue')

# Legenda customizada — span color
html, ok = replace_in_fn(html, fn,
    'color:#D1D5DB;">'
    + '\'<span style="width:20px;height:2.5px',
    'color:#475569;">'
    + '\'<span style="width:20px;height:2.5px')
if ok: patches+=1; print('[OK] AvgPriceChart: custom legend color -> #475569')
else:
    # Tentar variante direta
    html, ok = replace_in_fn(html, fn,
        'gap:5px;color:#D1D5DB;"',
        'gap:5px;color:#475569;"')
    if ok: patches+=1; print('[OK] AvgPriceChart: custom legend color (v2) -> #475569')

# Ticks color no eixo X
h_new, c = replace_all_in_fn(html, fn, "color:'#D1D5DB'", "color:'#475569'")
if c: html=h_new; patches+=c; print(f'[OK] AvgPriceChart: tick color -> #475569 (x{c})')

h_new, c = replace_all_in_fn(html, fn, "color:'#D1D5DB'", "color:'#475569'")
if c: html=h_new; patches+=c

# Grid lines
h_new, c = replace_all_in_fn(html, fn, "color:'rgba(255,255,255,0.08)'", "color:'rgba(59,130,246,0.10)'")
if c: html=h_new; patches+=c; print(f'[OK] AvgPriceChart: grid -> blue (x{c})')

h_new, c = replace_all_in_fn(html, fn, "color:'rgba(255,255,255,0.09)'", "color:'rgba(59,130,246,0.10)'")
if c: html=h_new; patches+=c; print(f'[OK] AvgPriceChart: grid 0.09 -> blue (x{c})')

h_new, c = replace_all_in_fn(html, fn, "color: 'rgba(255,255,255,0.08)'", "color: 'rgba(59,130,246,0.10)'")
if c: html=h_new; patches+=c; print(f'[OK] AvgPriceChart: grid (space) -> blue (x{c})')

# ──────────────────────────────────────────────────────────────────────────────
# 3. renderAvgInsight — textos diagnóstico
# ──────────────────────────────────────────────────────────────────────────────
fn = 'renderAvgInsight'
h_new, c = replace_all_in_fn(html, fn, 'color:#e2e8f0', 'color:#1e293b')
if c: html=h_new; patches+=c; print(f'[OK] renderAvgInsight: #e2e8f0 -> #1e293b (x{c})')

# Fundo do diagnóstico
h_new, c = replace_all_in_fn(html, fn, 'background:#161B22', 'background:#EDF2F9')
if c: html=h_new; patches+=c; print(f'[OK] renderAvgInsight: bg -> #EDF2F9 (x{c})')

h_new, c = replace_all_in_fn(html, fn, 'background:#1F2937', 'background:#EDF2F9')
if c: html=h_new; patches+=c; print(f'[OK] renderAvgInsight: bg 1F2937 -> #EDF2F9 (x{c})')

# ──────────────────────────────────────────────────────────────────────────────
# 4. renderOBShare / renderOBPreco — corrigir grid que ficou branco
# ──────────────────────────────────────────────────────────────────────────────
for fn in ['renderOBShare', 'renderOBPreco']:
    h_new, c = replace_all_in_fn(html, fn, "color: 'rgba(255,255,255,", "color: 'rgba(59,130,246,")
    if c:
        # Desfazer — substituicao muito ampla, fazer de forma segura
        pass
    # Apenas o grid específico
    h_new, c = replace_all_in_fn(html, fn, "color:'rgba(255,255,255,0.12)'", "color:'rgba(59,130,246,0.10)'")
    if c: html=h_new; patches+=c; print(f'[OK] {fn}: grid 0.12 -> blue (x{c})')

    h_new, c = replace_all_in_fn(html, fn, "color: 'rgba(255,255,255,0.12)'", "color: 'rgba(59,130,246,0.10)'")
    if c: html=h_new; patches+=c; print(f'[OK] {fn}: grid 0.12 (space) -> blue (x{c})')

# ──────────────────────────────────────────────────────────────────────────────
# 5. CSS: reforçar o [style*=] com versão mais precisa para a tabela OB
# ──────────────────────────────────────────────────────────────────────────────
# Adicionar regra específica para thead da tabela OB (caso o JS inline não pegue)
OLD_CSS_ANCHOR = '/* .mso2-br cards brancos com borda */'
NEW_CSS_EXTRA = '''/* Tabela marcas OB — thead e rows */
#panel-nielsen table thead tr { background: #EDF2F9 !important; }
#panel-nielsen table thead th { color: #475569 !important; }
#panel-nielsen table tbody td { color: #475569 !important; }
#panel-nielsen table tbody tr:nth-child(even) { background: rgba(59,130,246,0.03) !important; }

/* Diagnóstico OB */
#panel-nielsen [style*="background:rgba(0,0,0,0.2)"] { background: rgba(59,130,246,0.06) !important; }

/* Bordas de tabela */
#panel-nielsen [style*="border-bottom:1px solid rgba(255,255,255,0.05)"] {
  border-bottom-color: rgba(59,130,246,0.10) !important;
}

/* AvgPrice legenda customizada */
#panel-nielsen #avg-legend span[style*="color:#D1D5DB"],
#panel-nielsen [id*="avg"] [style*="color:#D1D5DB"] { color: #475569 !important; }

/* Diagnóstico geral — text colors */
#panel-nielsen [style*="color:#3d6b63"] { color: #1d4ed8 !important; }

/* ── Reforço: qualquer background muito escuro dentro do painel ── */
#panel-nielsen [style*="background:#0a1a18"] { background: #EDF2F9 !important; }
#panel-nielsen [style*="background:#10172a"] { background: #EDF2F9 !important; }

'''
OLD_CSS_ANCHOR2 = '/* .mso2-br cards brancos com borda */'
if OLD_CSS_ANCHOR2 in html:
    html = html.replace(OLD_CSS_ANCHOR2, NEW_CSS_EXTRA + OLD_CSS_ANCHOR2, 1)
    patches += 1
    print('[OK] CSS: regras de reforço para tabela OB + AvgPrice adicionadas')

# ──────────────────────────────────────────────────────────────────────────────
# 6. Salvar
# ──────────────────────────────────────────────────────────────────────────────
print(f'\nPatches: {patches}')
print(f'Diff   : {len(html) - original_len:+,} bytes')

ts = datetime.datetime.now().strftime('%Y%m%d_%H%M')
ver = f'Dashboard_farma_sul/versoes/Dashboard_Farma_Sul_{ts}_NielsenClaroFix.html'
open(SRC, 'w', encoding='utf-8').write(html)
open(ver, 'w', encoding='utf-8').write(html)
print(f'\nSalvo : {SRC}')
print(f'Versao: {ver}')
