"""
PATCH 35 — Chart color visibility fix (tema claro)
Problema: cores rgba(255,255,255,...) usadas em bars/lines se tornam invisíveis
no tema claro (branco sobre branco).

Fixes JS diretos:
1. renderSellinBarGeral: 'Hist FY25' bar  rgba(255,255,255,0.1) → slate gray
2. renderSellinMensalChart: 'Histórico FY25' bar rgba(255,255,255,0.12) → slate gray
3. renderSellinBarGeral: Planejado bar rgba(103,232,249,0.4) → ciano sólido mais visível
4. Todas as legendas Chart.js color:'#7aa89e' (teal claro) → '#334155' (escuro legível)

Fixes CSS:
5. Tracks de progress bar rgba(255,255,255,0.1) → light slate
6. Bordas de tabela rgba(255,255,255,0.1) → DCE3EC
7. Tooltip borders rgba(255,255,255,0.13) → rgba(148,163,184,0.25)
"""
import datetime

SRC = r'Dashboard_farma_sul\Dashboard_Farma_Sul_20260512_2220.html'
html = open(SRC, encoding='utf-8').read()
original_len = len(html)

fixes = 0

# 1 — renderSellinBarGeral: 'Hist FY25' bar INVISÍVEL
OLD1 = "backgroundColor:'rgba(255,255,255,0.1)', borderColor:'rgba(255,255,255,0.25)',borderWidth:1.5,borderRadius:8}"
NEW1 = "backgroundColor:'rgba(148,163,184,0.45)', borderColor:'#94A3B8',borderWidth:1.5,borderRadius:8,borderDash:[4,4]}"
if OLD1 in html:
    html = html.replace(OLD1, NEW1, 1)
    fixes += 1
    print('[OK1] Hist FY25 bar: rgba(255,255,255,0.1) -> slate 0.45 + dashed border')
else:
    print('[MISS1] Hist FY25 bar anchor not found')

# 2 — renderSellinMensalChart: 'Histórico FY25' bar INVISÍVEL
OLD2 = "backgroundColor:'rgba(255,255,255,0.12)', borderColor:'rgba(255,255,255,0.3)', borderWidth:1.5, borderRadius:8, order:5}"
NEW2 = "backgroundColor:'rgba(148,163,184,0.45)', borderColor:'#94A3B8', borderWidth:1.5, borderRadius:8, order:5}"
if OLD2 in html:
    html = html.replace(OLD2, NEW2, 1)
    fixes += 1
    print('[OK2] Histórico FY25 bar (mensal): rgba(255,255,255,0.12) → slate 0.45')
else:
    print('[MISS2] Histórico FY25 mensal anchor not found')

# 3 — renderSellinBarGeral: Planejado bar — cyan 0.4 lavado → cyan sólido
OLD3 = "backgroundColor:'rgba(103,232,249,0.4)',  borderColor:'#67e8f9',borderWidth:1.5,borderRadius:8},"
NEW3 = "backgroundColor:'rgba(6,182,212,0.65)',   borderColor:'#0891B2',borderWidth:1.5,borderRadius:8},"
if OLD3 in html:
    html = html.replace(OLD3, NEW3, 1)
    fixes += 1
    print('[OK3] Planejado bar: rgba(103,232,249,0.4) → rgba(6,182,212,0.65)')
else:
    # tenta variante sem duplo espaço
    OLD3b = "backgroundColor:'rgba(103,232,249,0.4)', borderColor:'#67e8f9',borderWidth:1.5,borderRadius:8},"
    if OLD3b in html:
        html = html.replace(OLD3b, NEW3.replace('   ', ' '), 1)
        fixes += 1
        print('[OK3b] Planejado bar (variante): atualizado')
    else:
        print('[MISS3] Planejado bar anchor not found')

# 4 — Todas as legendas Chart.js color:'#7aa89e' → '#334155'
# São ~20 ocorrências em labels de legend ao longo do arquivo
count4 = html.count("color:'#7aa89e'")
if count4 > 0:
    html = html.replace("color:'#7aa89e'", "color:'#334155'")
    fixes += count4
    print('[OK4] Legend color #7aa89e → #334155 ({} ocorrências)'.format(count4))
else:
    print('[MISS4] color:#7aa89e not found')

# 5 — SVG legend text fill="#7aa89e"
count5 = html.count('fill="#7aa89e"')
if count5 > 0:
    html = html.replace('fill="#7aa89e"', 'fill="#334155"')
    fixes += count5
    print('[OK5] SVG fill #7aa89e → #334155 ({} ocorrências)'.format(count5))

# 6 — CSS: patch35 — inline backgrounds/borders
ANCHOR35 = '/* FIM PATCH 34 */'
CSS35 = '''/* FIM PATCH 34 */

/* ==========================================================================
   PATCH 35 - Chart color visibility + table borders no tema claro
   ========================================================================== */

/* Progress bar tracks invisíveis (rgba branco sobre branco) */
[style*="background:rgba(255,255,255,0.1)"][style*="border-radius:3px"] {
  background: rgba(148,163,184,0.2) !important;
}
/* Bordas de tabela branco-transparente → cinza sutil */
[style*="border-bottom:1px solid rgba(255,255,255,0.1)"] {
  border-bottom-color: rgba(148,163,184,0.25) !important;
}
[style*="border-top:1px solid rgba(255,255,255,0.1)"] {
  border-top-color: rgba(148,163,184,0.25) !important;
}
[style*="border:0.5px solid rgba(255,255,255,0.1)"] {
  border-color: rgba(148,163,184,0.35) !important;
}
/* Tooltip borders branco-transparente → slate */
[style*="borderColor:'rgba(255,255,255,0.13)'"] {
  border-color: rgba(148,163,184,0.3) !important;
}
/* Sell In verbas: mini-cards de quotas */
[style*="background:rgba(255,255,255,0.03)"] {
  background: #F8FAFC !important;
}
/* Rodapé totais de tabela */
[style*="background:rgba(255,255,255,0.02)"] {
  background: rgba(148,163,184,0.06) !important;
}

/* FIM PATCH 35 */'''

if ANCHOR35 in html:
    html = html.replace(ANCHOR35, CSS35, 1)
    fixes += 1
    print('[OK6] CSS patch35 injetado (progress tracks + table borders)')
else:
    print('[MISS6] ancora FIM PATCH 34 nao encontrada')

print('\nTotal fixes aplicados: {}'.format(fixes))
print('Diff: {:+,} bytes'.format(len(html) - original_len))

ts = datetime.datetime.now().strftime('%Y%m%d_%H%M')
ver = 'Dashboard_farma_sul/versoes/Dashboard_Farma_Sul_{}_ChartColorsFix.html'.format(ts)

open(SRC, 'w', encoding='utf-8').write(html)
open(ver, 'w', encoding='utf-8').write(html)
print('Salvo: ' + SRC)
print('Versao: ' + ver)
