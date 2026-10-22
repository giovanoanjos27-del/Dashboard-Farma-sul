"""
fix_reg_perf_calls.py
Corrige o JS quebrado deixado pelo patch anterior:
Remove TODAS as referências restantes a renderRegPerfCard
(guards if+typeof, try/catch wrappers, chamadas diretas)
"""
import sys, shutil, re
sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path
from datetime import datetime

DASH = Path(r'C:\Users\valqu\OneDrive\Documentos\Claude\Projects\projeto Dashboard_farma_sul\Dashboard_farma_sul\Dashboard_Farma_Sul_20260512_2220.html')
VER  = DASH.parent / 'versoes'
DL   = Path.home() / 'Downloads'
ts   = datetime.now().strftime('%Y%m%d_%H%M')
shutil.copy(DASH, VER / f'Dashboard_Farma_Sul_{ts}_PreFixRegCalls.html')

h = DASH.read_text(encoding='utf-8')
orig_len = len(h)
total_fixes = 0

# ── Padrões a remover (ordem do mais específico ao mais geral) ────────────────

patterns = [
    # try{ renderRegPerfCard(); }catch(e){ ... }
    (r"\n\s*try\s*\{\s*renderRegPerfCard\(\s*\);\s*\}catch\(e\)\{[^}]*\}", ''),
    # try { if(typeof renderRegPerfCard==='function'){ renderRegPerfCard(); } } catch(e){ ... }
    (r"\n\s*try\s*\{\s*if\s*\(typeof\s+renderRegPerfCard\s*===\s*'function'\)\s*\{\s*renderRegPerfCard\(\s*\);\s*\}\s*\}\s*catch\(e\)\{[^}]*\}", ''),
    # if(typeof renderRegPerfCard === 'function') renderRegPerfCard();   (com ou sem espaços)
    (r"\n?\s*if\s*\(typeof\s+renderRegPerfCard\s*===\s*'function'\)\s*renderRegPerfCard\(\s*\);\s*", '\n'),
    # if(typeof renderRegPerfCard==='function')   SEM CORPO (ja quebrado pelo patch anterior)
    (r"\n?\s*if\s*\(typeof\s+renderRegPerfCard\s*===\s*'function'\)\s*", ''),
    # renderRegPerfCard(); sozinho
    (r"\n?\s*renderRegPerfCard\(\s*\);\s*", '\n'),
    # renderRegPerfCard()  sem ; (improvável mas por garantia)
    (r"renderRegPerfCard\(\s*\)", ''),
]

for pat, repl in patterns:
    new_h, n = re.subn(pat, repl, h)
    if n:
        print(f'OK ({n}x): {repr(pat[:60])}')
        h = new_h
        total_fixes += n

# Verificar se ainda restou algo
remaining = list(re.finditer('renderRegPerfCard', h))
print(f'\nReferencias restantes: {len(remaining)}')
for m in remaining:
    print(f'  pos {m.start()}: {repr(h[m.start()-40:m.start()+80])}')

# ── Salvar ────────────────────────────────────────────────────────────────────
DASH.write_text(h, encoding='utf-8')
shutil.copy(DASH, VER / f'Dashboard_Farma_Sul_{ts}_FixRegCalls.html')
shutil.copy(DASH, DL  / f'Dashboard_FarmaSul_Giovano_{ts}.html')
print(f'\n✅ {total_fixes} correções aplicadas')
print(f'Delta: {len(h) - orig_len:+,} chars')
print(f'Downloads: Dashboard_FarmaSul_Giovano_{ts}.html')
print('DONE.')
