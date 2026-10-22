import sys, shutil
sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path; from datetime import datetime
DASH = Path(r'C:\Users\valqu\OneDrive\Documentos\Claude\Projects\projeto Dashboard_farma_sul\Dashboard_farma_sul\Dashboard_Farma_Sul_20260512_2220.html')
VER=DASH.parent/'versoes'; DL=Path.home()/'Downloads'
h=DASH.read_text(encoding='utf-8'); ts=datetime.now().strftime('%Y%m%d_%H%M')

fn_start=h.find('function renderMSOSkuJanMar()'); fn_end=h.find('\nfunction fN(n){',fn_start)
fn=h[fn_start:fn_end]

# Remover chip MAIOR GANHO (primeiro chip do array de 3)
OLD_CHIP1 = "{l:'MAIOR GANHO Δpp',v:gA.length?'+'+gA[0].v.toFixed(2)+'pp':'—',s:gA.length?d.skus[gA[0].i].trim().substring(0,22):'',c:'#3b82f6'},\n      "
NEW_CHIP1 = ''

# Grid 3 -> 2 colunas
OLD_GRID = "display:grid;grid-template-columns:repeat(3,1fr);gap:8px;overflow:hidden;"
NEW_GRID = "display:grid;grid-template-columns:repeat(2,1fr);gap:8px;overflow:hidden;"

assert OLD_CHIP1 in fn, f'chip MAIOR GANHO nao encontrado\n{repr(fn[fn.find("MAIOR GANHO"):fn.find("MAIOR GANHO")+200])}'
fn = fn.replace(OLD_CHIP1, NEW_CHIP1, 1)
print('OK: chip MAIOR GANHO removido')

assert OLD_GRID in fn, 'grid nao encontrado'
fn = fn.replace(OLD_GRID, NEW_GRID, 1)
print('OK: grid 3 -> 2 colunas')

# Remover gA (nao mais usado nos chips, mas ainda usado no diagnostico? nao)
# gA era usado no chip MAIOR GANHO -- verificar se ainda e usado em outro lugar
if 'gA' not in fn.replace('var gA=', '').replace('gA.length', ''):
    fn = fn.replace("    var gA=d.var.map(function(v,i){return{v:v,i:i};}).filter(function(x){return x.v>0;}).sort(function(a,b){return b.v-a.v;});\n", '')
    print('OK: var gA removido (nao mais usado)')
else:
    print('INFO: gA ainda referenciado, mantendo')

h = h[:fn_start] + fn + h[fn_end:]
DASH.write_text(h, encoding='utf-8')
shutil.copy(DASH, VER / f'Dashboard_Farma_Sul_{ts}_RmChipGanho.html')
shutil.copy(DASH, DL  / f'Dashboard_FarmaSul_Giovano_{ts}.html')
print(f'Downloads: Dashboard_FarmaSul_Giovano_{ts}.html')
print('DONE.')
