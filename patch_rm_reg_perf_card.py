"""
patch_rm_reg_perf_card.py
Remove o card PERFORMANCE POR REGIÃO — FYTD JUL–MAR:
 1. Bloco HTML do card (reg-perf-card)
 2. Função JS window.renderRegPerfCard
 3. Qualquer chamada renderRegPerfCard() no código de inicialização
"""
import sys, shutil, re
sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path
from datetime import datetime

DASH = Path(r'C:\Users\valqu\OneDrive\Documentos\Claude\Projects\projeto Dashboard_farma_sul\Dashboard_farma_sul\Dashboard_Farma_Sul_20260512_2220.html')
VER  = DASH.parent / 'versoes'
DL   = Path.home() / 'Downloads'
ts   = datetime.now().strftime('%Y%m%d_%H%M')
shutil.copy(DASH, VER / f'Dashboard_Farma_Sul_{ts}_PreRmRegPerf.html')
print(f'Backup: Dashboard_Farma_Sul_{ts}_PreRmRegPerf.html')

h = DASH.read_text(encoding='utf-8')
orig_len = len(h)

# ── 1. Remover bloco HTML do card ─────────────────────────────────────────────
HTML_START = '\n<!-- PERFORMANCE POR REGIÃO -->'
HTML_END   = '\n<!-- MARKET SHARE POR SKU -->'

assert HTML_START in h, 'ERRO: comentário PERFORMANCE POR REGIÃO não encontrado'
assert HTML_END   in h, 'ERRO: comentário MARKET SHARE POR SKU não encontrado'

idx_s = h.index(HTML_START)
idx_e = h.index(HTML_END)
removed_html = h[idx_s:idx_e]
h = h[:idx_s] + h[idx_e:]
print(f'OK: HTML removido ({len(removed_html):,} chars)')

# ── 2. Remover função JS window.renderRegPerfCard ─────────────────────────────
FN_ANCHOR = 'window.renderRegPerfCard = function(){'
assert FN_ANCHOR in h, 'ERRO: window.renderRegPerfCard não encontrada'

fn_start = h.index(FN_ANCHOR)
# contar chaves para achar o fim
depth = 0
fn_end = fn_start
for i in range(fn_start, min(fn_start + 20000, len(h))):
    if h[i] == '{': depth += 1
    elif h[i] == '}':
        depth -= 1
        if depth == 0:
            fn_end = i + 1
            break

# incluir o ;\n final se existir
if h[fn_end:fn_end+2] == ';\n':
    fn_end += 2

removed_fn = h[fn_start:fn_end]
h = h[:fn_start] + h[fn_end:]
print(f'OK: window.renderRegPerfCard removida ({len(removed_fn):,} chars)')

# ── 3. Remover chamadas renderRegPerfCard() ───────────────────────────────────
calls_removed = 0
for pattern in [
    r'renderRegPerfCard\(\s*\);\s*\n',
    r'renderRegPerfCard\(\s*\),?\s*\n',
]:
    new_h, n = re.subn(pattern, '', h)
    if n:
        h = new_h
        calls_removed += n
        print(f'OK: {n} chamada(s) renderRegPerfCard() removida(s)')

if calls_removed == 0:
    print('INFO: nenhuma chamada direta a renderRegPerfCard() encontrada')

# ── 4. Salvar ─────────────────────────────────────────────────────────────────
DASH.write_text(h, encoding='utf-8')
shutil.copy(DASH, VER / f'Dashboard_Farma_Sul_{ts}_RmRegPerf.html')
shutil.copy(DASH, DL  / f'Dashboard_FarmaSul_Giovano_{ts}.html')
print(f'\nVersao:    Dashboard_Farma_Sul_{ts}_RmRegPerf.html')
print(f'Downloads: Dashboard_FarmaSul_Giovano_{ts}.html')
print(f'Delta: {len(h) - orig_len:+,} chars')
print('DONE.')
