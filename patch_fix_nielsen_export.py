"""
patch_fix_nielsen_export.py
Corrige bug "Cannot merge already merged cells" no botão Exportar Nielsen Excel.

Causa: sheetFYTD() tinha um forEach que fazia ws.mergeCells(C2:E2, F2:H2, I2:K2)
e logo abaixo o código fazia os mesmos merges explicitamente → double-merge → erro.
Fix: remover o bloco forEach duplicado.
"""
import sys
from pathlib import Path
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

BASE = Path(r'C:\Users\valqu\OneDrive\Documentos\Claude\Projects\projeto Dashboard_farma_sul\Dashboard_farma_sul')
SRC  = BASE / 'Dashboard_Farma_Sul_20260512_2220.html'
VER  = BASE / 'versoes' / f'Dashboard_Farma_Sul_{datetime.now().strftime("%Y%m%d_%H%M")}_FixNielsenExport.html'

print('Lendo dashboard…')
h = SRC.read_text(encoding='utf-8')
orig_len = len(h)

# ── Remover o bloco forEach que causava double-merge ──
OLD = """  /* Sub-grupos */
  var grpBg=C.card;
  [[3,3,5,'─── SHARE % ───',C.green],[6,3,8,'─── VALOR R$M ───',C.blue],[9,3,11,'─── VOL Kun ───',C.amber]].forEach(function(g){
    ws.mergeCells(2,g[0],2,g[4]===C.amber?11:g[2]);
    /* fix: indices wrong, do individually */
  });
  /* Simpler: just write group labels */
  for(var c=1;c<=12;c++) cell(ws,2,c,'',{bg:C.card});"""

NEW = """  /* Sub-grupos */
  var grpBg=C.card;
  for(var c=1;c<=12;c++) cell(ws,2,c,'',{bg:C.card});"""

count = h.count(OLD)
assert count == 1, f'Bloco forEach: encontrei {count} ocorrências (esperava 1). Verifique o HTML.'
h = h.replace(OLD, NEW)
print('✅ Bloco forEach duplicado removido de sheetFYTD')

# ── Verificações ──
assert 'ws.mergeCells(\'C2:E2\')' in h, '❌ merge C2:E2 sumiu'
assert 'ws.mergeCells(\'F2:H2\')' in h, '❌ merge F2:H2 sumiu'
assert 'ws.mergeCells(\'I2:K2\')' in h, '❌ merge I2:K2 sumiu'
assert h.count('ws.mergeCells(\'C2:E2\')') == 1, '❌ merge C2:E2 duplicado ainda presente'
assert 'btn-nielsen-xls' in h, '❌ botão não encontrado'
print('✅ Verificações OK — merges únicos confirmados')

print(f'\nTamanho original: {orig_len:,} | Novo: {len(h):,} | Δ: {len(h)-orig_len:+,}')

VER.parent.mkdir(parents=True, exist_ok=True)
VER.write_text(h, encoding='utf-8')
print(f'✅ Versão salva: {VER.name}')

SRC.write_text(h, encoding='utf-8')
print(f'✅ Base ativa atualizada: {SRC.name}')
print('DONE.')
