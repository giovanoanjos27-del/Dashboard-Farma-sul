"""
patch_rm_diag_geral.py
Remove o card DIAGNÓSTICO GERAL — PERSONAL REPELLENT (Análise Estratégica)
 1. Bloco HTML + <script> do card (diag-geral-card + renderDiagGeral)
 2. Todas as chamadas renderDiagGeral() no código de inicialização
"""
import sys, shutil, re
sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path
from datetime import datetime

DASH = Path(r'C:\Users\valqu\OneDrive\Documentos\Claude\Projects\projeto Dashboard_farma_sul\Dashboard_farma_sul\Dashboard_Farma_Sul_20260512_2220.html')
VER  = DASH.parent / 'versoes'
DL   = Path.home() / 'Downloads'
ts   = datetime.now().strftime('%Y%m%d_%H%M')
shutil.copy(DASH, VER / f'Dashboard_Farma_Sul_{ts}_PreRmDiagGeral.html')
print(f'Backup: Dashboard_Farma_Sul_{ts}_PreRmDiagGeral.html')

h = DASH.read_text(encoding='utf-8')
orig_len = len(h)

# ── 1. Remover bloco HTML + script do card ────────────────────────────────────
HTML_START = '\n<!-- DIAGNÓSTICO GERAL -->'
NEXT_SECTION = '\n<!-- ═══════════ ACOMPANHAMENTO OLs ═══════════ -->'

assert HTML_START in h,   'ERRO: comentário DIAGNÓSTICO GERAL não encontrado'
assert NEXT_SECTION in h, 'ERRO: seção ACOMPANHAMENTO OLs não encontrada'

idx_s = h.index(HTML_START)
idx_e = h.index(NEXT_SECTION)
removed = h[idx_s:idx_e]
h = h[:idx_s] + h[idx_e:]
print(f'OK: HTML + script removidos ({len(removed):,} chars)')

# ── 2. Remover todas as chamadas renderDiagGeral ──────────────────────────────
total = 0
patterns = [
    # try { if(typeof renderDiagGeral==='function'){ renderDiagGeral(); } } catch(e){ ... }
    (r"\n?\s*try\s*\{\s*if\s*\(typeof\s+renderDiagGeral\s*===\s*'function'\)\s*\{\s*renderDiagGeral\(\s*\);\s*\}\s*\}\s*catch\(e\)\{\s*\}", ''),
    # try{ renderDiagGeral(); }catch(e){ console.warn(...) }
    (r"\n?\s*try\s*\{\s*renderDiagGeral\(\s*\);\s*\}catch\(e\)\{[^}]*\}", ''),
    # if(typeof renderDiagGeral==='function') renderDiagGeral();
    (r"\n?\s*if\s*\(typeof\s+renderDiagGeral\s*===\s*'function'\)\s*renderDiagGeral\(\s*\);\s*", '\n'),
    # renderDiagGeral(); sozinho
    (r"\n?\s*renderDiagGeral\(\s*\);\s*", '\n'),
]
for pat, repl in patterns:
    new_h, n = re.subn(pat, repl, h)
    if n:
        print(f'OK ({n}x): {repr(pat[:70])}')
        h = new_h
        total += n

# Verificar
remaining = list(re.finditer('renderDiagGeral|diag-geral', h))
print(f'\nReferências restantes: {len(remaining)}')
for m in remaining:
    print(f'  pos {m.start()}: {repr(h[m.start()-20:m.start()+60])}')

# ── 3. Salvar ─────────────────────────────────────────────────────────────────
DASH.write_text(h, encoding='utf-8')
shutil.copy(DASH, VER / f'Dashboard_Farma_Sul_{ts}_RmDiagGeral.html')
shutil.copy(DASH, DL  / f'Dashboard_FarmaSul_Giovano_{ts}.html')
print(f'\n✅ Total: {total} chamadas removidas')
print(f'Delta: {len(h) - orig_len:+,} chars')
print(f'Downloads: Dashboard_FarmaSul_Giovano_{ts}.html')
print('DONE.')
