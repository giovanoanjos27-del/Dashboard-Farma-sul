import sys, shutil
sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path; from datetime import datetime
DASH = Path(r'C:\Users\valqu\OneDrive\Documentos\Claude\Projects\projeto Dashboard_farma_sul\Dashboard_farma_sul\Dashboard_Farma_Sul_20260512_2220.html')
VER=DASH.parent/'versoes'; DL=Path.home()/'Downloads'
h=DASH.read_text(encoding='utf-8'); ts=datetime.now().strftime('%Y%m%d_%H%M')

fn_start=h.find('function renderMSOSkuJanMar()'); fn_end=h.find('\nfunction fN(n){',fn_start)
fn=h[fn_start:fn_end]

# Remover linha SKU Lider no diagnostico
import re

# linha que começa com dh+='🏆 ... SKU Líder ... <br>';
fn = re.sub(r"dh\+='[^']*SKU L[íi]der[^;]+;<br>';\n", '', fn)
fn = re.sub(r"dh\+='[^']*SKU L[íi]der.*?';\n", '', fn)

# linha Top 3 SKUs
fn = re.sub(r"dh\+='[^']*Top 3 SKUs[^;]+;\n", '', fn)

# Remover tI2 e top3 que nao sao mais usados
fn = re.sub(r"var tI2=[^;]+;\n", '', fn)
fn = re.sub(r"var top3=[^;]+;\n", '', fn)

h = h[:fn_start] + fn + h[fn_end:]
DASH.write_text(h, encoding='utf-8')
shutil.copy(DASH, VER / f'Dashboard_Farma_Sul_{ts}_RmDiagLines.html')
shutil.copy(DASH, DL  / f'Dashboard_FarmaSul_Giovano_{ts}.html')
print(f'Downloads: Dashboard_FarmaSul_Giovano_{ts}.html')
print('DONE.')
