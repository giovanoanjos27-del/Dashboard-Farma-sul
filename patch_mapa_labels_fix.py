"""
patch_mapa_labels_fix.py
========================
Corrige erro JS introduzido pelo patch_mapa_labels.py:
  +'transform:translate(-50%,-50%);line-height:1.25;'>'
A aspa dupla (") que fecha style="..." estava faltando,
causando erro de sintaxe que quebrava TODOS os gráficos.
  +'transform:translate(-50%,-50%);line-height:1.25;">'
"""
import sys, shutil
sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path
from datetime import datetime

DASH = Path(r'C:\Users\valqu\OneDrive\Documentos\Claude\Projects\projeto Dashboard_farma_sul\Dashboard_farma_sul\Dashboard_Farma_Sul_20260512_2220.html')
VER  = DASH.parent / 'versoes'
DL   = Path.home() / 'Downloads'
ts   = datetime.now().strftime('%Y%m%d_%H%M')

shutil.copy(DASH, VER / f'Dashboard_Farma_Sul_{ts}_PreLabelsFix.html')
h = DASH.read_text(encoding='utf-8')
print(f'Backup: ...PreLabelsFix.html  |  {len(h):,} chars')

# A string com bug: fecha o JS string sem a " que fecha style="..."
OLD = "          +'transform:translate(-50%,-50%);line-height:1.25;'>'"
# Correto: \" fecha o atributo HTML style="...", > fecha a tag <div>
NEW = "          +'transform:translate(-50%,-50%);line-height:1.25;\">'"

cnt = h.count(OLD)
assert cnt == 1, f'ERRO: {cnt}x encontrado (esperado 1)'
h = h.replace(OLD, NEW, 1)
print('✓ line-height:1.25;\'> → line-height:1.25;">')

# Verificação: deve haver apenas a versão correta
assert 'line-height:1.25;">' in h,  'ERRO: correção não aplicada'
assert "line-height:1.25;'>" not in h, 'ERRO: versão com bug ainda presente'
print('Verificações: OK')
print(f'Tamanho final: {len(h):,} chars')

DASH.write_text(h, encoding='utf-8')
shutil.copy(DASH, VER / f'Dashboard_Farma_Sul_{ts}_MapaLabelsFix.html')
shutil.copy(DASH, DL  / f'Dashboard_FarmaSul_Giovano_{ts}.html')
print(f'Versao:    Dashboard_Farma_Sul_{ts}_MapaLabelsFix.html')
print(f'Downloads: Dashboard_FarmaSul_Giovano_{ts}.html')
print('DONE.')
