"""
patch_remove_intoc_carteira.py
==============================
Remove CIRURGICAMENTE dois cards do dashboard:
  1) "🏆 INTOCÁVEIS × CARTEIRA DE CLIENTES" da área Sell In
     (div#intoc-sellin-card + bloco JS dedicado)
  2) "🏆 INTOCÁVEIS × CARTEIRA DE CLIENTES" da área Cobertura
     (div#cob-card-intocaveis — HTML estático, sem JS próprio)

NÃO altera nenhuma outra visualização, filtro, métrica ou estrutura.
"""
import sys, shutil
sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path
from datetime import datetime

DASH = Path(r'C:\Users\valqu\OneDrive\Documentos\Claude\Projects\projeto Dashboard_farma_sul\Dashboard_farma_sul\Dashboard_Farma_Sul_20260512_2220.html')
VER  = DASH.parent / 'versoes'
DL   = Path.home() / 'Downloads'
ts   = datetime.now().strftime('%Y%m%d_%H%M')

# ── Backup preventivo ─────────────────────────────────────────────────────────
shutil.copy(DASH, VER / f'Dashboard_Farma_Sul_{ts}_PreRemoveIntocCarteira.html')
print(f'Backup: Dashboard_Farma_Sul_{ts}_PreRemoveIntocCarteira.html')

h = DASH.read_text(encoding='utf-8')
original_len = len(h)
print(f'Tamanho original: {original_len:,} chars')

# ═══════════════════════════════════════════════════════════════════════════════
# Localizar Card 1 HTML — div#intoc-sellin-card
# ═══════════════════════════════════════════════════════════════════════════════
C1_COMMENT = '\n<!-- INTOCÁVEIS × DISTRIBUIÇÃO NUMÉRICA — SELL IN -->'
c1_s = h.find(C1_COMMENT)
assert c1_s != -1, 'Card1: marcador de inicio nao encontrado'

c1_div_s = h.find('<div id="intoc-sellin-card"')
assert c1_div_s != -1, 'Card1: div nao encontrado'

# Contar divs para achar o fechamento exato
depth = 0
i = c1_div_s
while i < len(h):
    if h[i:i+4] == '<div':   depth += 1; i += 4
    elif h[i:i+6] == '</div>': depth -= 1; i += 6
    else: i += 1
    if depth == 0: c1_e = i; break
else:
    raise AssertionError('Card1: fechamento </div> nao encontrado')

# Incluir newlines extras após o card (de 5 reduzir para 1)
while c1_e < len(h) - 1 and h[c1_e] == '\n':
    c1_e += 1
# Manter 1 newline (recuar um)
c1_e -= 1

print(f'Card1 HTML: [{c1_s} .. {c1_e}] = {c1_e - c1_s:,} chars removidos')
assert 'intoc-sellin-card' in h[c1_s:c1_e], 'Card1: sanidade — id nao encontrado no trecho'

# ═══════════════════════════════════════════════════════════════════════════════
# Localizar Card 2 HTML — div#cob-card-intocaveis
# ═══════════════════════════════════════════════════════════════════════════════
C2_COMMENT = '\n    <!-- ⑤ INTOCÁVEIS × CARTEIRA -->'
c2_s = h.find(C2_COMMENT)
assert c2_s != -1, 'Card2: marcador de inicio nao encontrado'

c2_div_s = h.find('<div id="cob-card-intocaveis"')
assert c2_div_s != -1, 'Card2: div nao encontrado'

depth = 0
i = c2_div_s
while i < len(h):
    if h[i:i+4] == '<div':   depth += 1; i += 4
    elif h[i:i+6] == '</div>': depth -= 1; i += 6
    else: i += 1
    if depth == 0: c2_e = i; break
else:
    raise AssertionError('Card2: fechamento </div> nao encontrado')

print(f'Card2 HTML: [{c2_s} .. {c2_e}] = {c2_e - c2_s:,} chars removidos')
assert 'cob-card-intocaveis' in h[c2_s:c2_e], 'Card2: sanidade — id nao encontrado no trecho'

# ═══════════════════════════════════════════════════════════════════════════════
# Localizar bloco JS — funções dedicadas ao Card 1 (intoc-sellin)
# ═══════════════════════════════════════════════════════════════════════════════
JS_MARKER = '\n\n/* ═══════ INTOCÁVEIS — SELL IN (com filtro UF) ═══════ */'
js_s = h.find(JS_MARKER)
assert js_s != -1, 'JS block: marcador nao encontrado'

# Achar a última função do bloco: renderIntocSellinCard
last_def = h.rfind('function renderIntocSellinCard')
assert last_def != -1 and last_def > js_s, 'JS block: renderIntocSellinCard nao encontrado apos marcador'

# Fechar a função contando chaves
depth = 0
i = last_def
in_func = False
js_e = -1
while i < len(h):
    if h[i] == '{':   depth += 1; in_func = True
    elif h[i] == '}':
        depth -= 1
        if in_func and depth == 0:
            js_e = i + 1
            break
    i += 1
assert js_e != -1, 'JS block: fechamento de renderIntocSellinCard nao encontrado'

print(f'JS block:  [{js_s} .. {js_e}] = {js_e - js_s:,} chars removidos')
assert 'renderIntocSellinCard' in h[js_s:js_e], 'JS block: sanidade'
assert '_intocSellinDist'      in h[js_s:js_e], 'JS block: sanidade variavel'

# ═══════════════════════════════════════════════════════════════════════════════
# Localizar chamada órfã em initSellin() — setTimeout renderIntocSellinCard
# ═══════════════════════════════════════════════════════════════════════════════
INIT_REF = '\n  // Intocáveis × Distribuição Numérica\n  setTimeout(function(){ if(typeof renderIntocSellinCard===\'function\') renderIntocSellinCard(); }, 200);'
init_s = h.find(INIT_REF)
assert init_s != -1, 'initSellin ref: linha nao encontrada'
init_e = init_s + len(INIT_REF)
print(f'initSellin ref: [{init_s} .. {init_e}] = {init_e - init_s:,} chars removidos')

# ═══════════════════════════════════════════════════════════════════════════════
# Sanidade: as 4 regiões não se sobrepõem e estão em ordem crescente
# ═══════════════════════════════════════════════════════════════════════════════
assert c1_e  < c2_s,   f'ERRO: Card1 sobrepõe Card2'
assert c2_e  < js_s,   f'ERRO: Card2 sobrepõe JS block'
assert js_e  < init_s, f'ERRO: JS block sobrepõe initSellin ref'
print('Sanidade de ordem: OK')

# ═══════════════════════════════════════════════════════════════════════════════
# Aplicar remoções (de trás para frente para manter offsets válidos)
# ═══════════════════════════════════════════════════════════════════════════════
h = h[:init_s] + h[init_e:]  # 4) chamada em initSellin
h = h[:js_s]   + h[js_e:]    # 3) JS block
h = h[:c2_s]   + h[c2_e:]    # 2) Card2 HTML
h = h[:c1_s]   + h[c1_e:]    # 1) Card1 HTML

removed = original_len - len(h)
print(f'\nTotal removido: {removed:,} chars')
print(f'Tamanho final:  {len(h):,} chars')

# ═══════════════════════════════════════════════════════════════════════════════
# Verificações pós-remoção
# ═══════════════════════════════════════════════════════════════════════════════
assert 'intoc-sellin-card'    not in h, 'ERRO: intoc-sellin-card ainda presente!'
assert 'cob-card-intocaveis'  not in h or h.count('cob-card-intocaveis') <= 1, \
    'AVISO: cob-card-intocaveis ainda presente mais de 1x'
assert 'renderIntocSellinCard' not in h, 'ERRO: renderIntocSellinCard ainda presente!'
assert '_intocSellinDist'      not in h, 'ERRO: _intocSellinDist ainda presente!'

# Verificar que cards que devem permanecer ainda existem
for must_have in ['intoc-grupos-card', 'DN_INTOC_GRUPOS', 'DN_INTOC_DIST',
                  'gpf-wrap', 'initSellin', 'panel-sellin', 'panel-cobertura']:
    assert must_have in h, f'ERRO: elemento obrigatório ausente: {must_have}'

# O cob-card-intocaveis ainda aparece 1x na lista de IDs ocultos (if(el) — seguro)
cob_refs = h.count('cob-card-intocaveis')
print(f'Referencias restantes a cob-card-intocaveis: {cob_refs} (esperado: 1 — lista forEach segura)')

print('Verificações: OK')

# ═══════════════════════════════════════════════════════════════════════════════
# Salvar
# ═══════════════════════════════════════════════════════════════════════════════
DASH.write_text(h, encoding='utf-8')
shutil.copy(DASH, VER / f'Dashboard_Farma_Sul_{ts}_RemoveIntocCarteira.html')
shutil.copy(DASH, DL  / f'Dashboard_FarmaSul_Giovano_{ts}.html')

print(f'\nSalvo:     {DASH.name}')
print(f'Versao:    Dashboard_Farma_Sul_{ts}_RemoveIntocCarteira.html')
print(f'Downloads: Dashboard_FarmaSul_Giovano_{ts}.html')
print('DONE.')
