import sys, shutil
sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path; from datetime import datetime
DASH = Path(r'C:\Users\valqu\OneDrive\Documentos\Claude\Projects\projeto Dashboard_farma_sul\Dashboard_farma_sul\Dashboard_Farma_Sul_20260512_2220.html')
VER=DASH.parent/'versoes'; DL=Path.home()/'Downloads'
h=DASH.read_text(encoding='utf-8'); ts=datetime.now().strftime('%Y%m%d_%H%M')

fn_start=h.find('function renderMSOSkuJanMar()'); fn_end=h.find('\nfunction fN(n){',fn_start)
fn=h[fn_start:fn_end]

# ── Linha 1: SKU Líder ────────────────────────────────────────────────────────
LINE1 = (
    "\n    dh+='🏆 <strong style=\"color:#e2e8f0;\">SKU Líder:</strong> "
    "<strong style=\"color:#34d399;\">'+d.skus[tI2]+'</strong> — "
    "'+d.janmar26[tI2].toFixed(2)+'% Jan-Mar/26 <span style=\"color:'"
    "+(d.var[tI2]>=0?'#34d399':'#ef4444')+'\">'+(d.var[tI2]>=0?'▲ +':'▼ ')"
    "+Math.abs(d.var[tI2]).toFixed(2)+'pp</span> vs Jan-Mar/25.<br>';"
)

# ── Linha 2: Top 3 SKUs ───────────────────────────────────────────────────────
LINE2 = (
    "\n    dh+='📊 <strong style=\"color:#e2e8f0;\">Top 3 SKUs</strong> "
    "representam <strong style=\"color:#67e8f9;\">'+top3.toFixed(1)+'%</strong>"
    " do mercado.<br>';"
)

assert LINE1 in fn, f'ERRO linha1 nao encontrada'
assert LINE2 in fn, f'ERRO linha2 nao encontrada'

fn = fn.replace(LINE1, '', 1)
fn = fn.replace(LINE2, '', 1)
print('OK: linha SKU Lider removida')
print('OK: linha Top 3 SKUs removida')

# Verificar resultado do diagnostico
diag_s = fn.find("var dh='")
diag_e = fn.find('dEl.innerHTML=', diag_s)
print('\nDiagnostico final:')
print(repr(fn[diag_s:diag_e]))

h = h[:fn_start] + fn + h[fn_end:]
DASH.write_text(h, encoding='utf-8')
shutil.copy(DASH, VER / f'Dashboard_Farma_Sul_{ts}_RmDiagSurgical.html')
shutil.copy(DASH, DL  / f'Dashboard_FarmaSul_Giovano_{ts}.html')
print(f'\nDownloads: Dashboard_FarmaSul_Giovano_{ts}.html')
print('DONE.')
