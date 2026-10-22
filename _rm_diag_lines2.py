import sys, shutil, re
sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path; from datetime import datetime
DASH = Path(r'C:\Users\valqu\OneDrive\Documentos\Claude\Projects\projeto Dashboard_farma_sul\Dashboard_farma_sul\Dashboard_Farma_Sul_20260512_2220.html')
VER=DASH.parent/'versoes'; DL=Path.home()/'Downloads'
h=DASH.read_text(encoding='utf-8'); ts=datetime.now().strftime('%Y%m%d_%H%M')

fn_start=h.find('function renderMSOSkuJanMar()'); fn_end=h.find('\nfunction fN(n){',fn_start)
fn=h[fn_start:fn_end]

# Mostrar bloco de diagnostico para identificar exatamente o que sobrou
diag_s = fn.find("var dh='")
diag_e = fn.find("dEl.innerHTML=", diag_s)
diag_block = fn[diag_s:diag_e]
print("=== DIAGNOSTICO ATUAL ===")
print(repr(diag_block))
print()

# Remover qualquer linha dh+= que contenha 'Top 3' ou 'toFixed(1)' ou 'SKU Lider' ou 'tI2'
lines = diag_block.split('\n')
clean_lines = []
for l in lines:
    if 'Top 3' in l or 'top3' in l or 'SKU L' in l or 'tI2' in l or 'esentam' in l:
        print(f'REMOVENDO: {repr(l)}')
    else:
        clean_lines.append(l)

new_diag_block = '\n'.join(clean_lines)
fn = fn[:diag_s] + new_diag_block + fn[diag_s+len(diag_block):]

# Remover variaveis nao usadas: tI2, top3
fn = re.sub(r'\n\s*var tI2\s*=[^;]+;', '', fn)
fn = re.sub(r'\n\s*var top3\s*=[^;]+;', '', fn)

# Verificar resultado
diag_s2 = fn.find("var dh='")
diag_e2 = fn.find("dEl.innerHTML=", diag_s2)
print("\n=== DIAGNOSTICO FINAL ===")
print(repr(fn[diag_s2:diag_e2]))

h = h[:fn_start] + fn + h[fn_end:]
DASH.write_text(h, encoding='utf-8')
shutil.copy(DASH, VER / f'Dashboard_Farma_Sul_{ts}_RmDiagLines2.html')
shutil.copy(DASH, DL  / f'Dashboard_FarmaSul_Giovano_{ts}.html')
print(f'\nDownloads: Dashboard_FarmaSul_Giovano_{ts}.html')
print('DONE.')
