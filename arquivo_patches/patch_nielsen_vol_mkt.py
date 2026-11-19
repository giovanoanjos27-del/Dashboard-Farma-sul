"""
patch_nielsen_vol_mkt.py
========================
Corrige VOL_MKT_DATA['T.BR Farma'] somando ALL OTHERS CAMP ao total.

PROBLEMA: VOL_MKT_DATA['T.BR Farma'] ainda exibia os valores antigos
          fytd25_val:419.62 / fytd26_val:350.32 sem ALL OTHERS CAMP.

CORREÇÃO:
  fytd25_val: 419.62 + 112.4675 = 532.09
  fytd26_val: 350.32 + 81.4096  = 431.73
  fytd25_un:  14946.3 + 5361.2  = 20307.5
  fytd26_un:  12958.3 + 4136.5  = 17094.8
  monthly_val (Jul–Mar, 9 meses):
    [20.308+4.112, 17.772+3.688, 23.247+5.390, 27.268+6.622,
     33.373+8.334, 51.28+13.332, 68.229+16.699, 55.537+12.124, 53.304+11.110]
    = [24.420, 21.460, 28.637, 33.890, 41.707, 64.612, 84.928, 67.661, 64.414]
  monthly_un (Jul–Mar, 9 meses):
    [732.5+195.8, 631.2+172.7, 818.2+255.6, 957.9+326.1,
     1287.0+425.7, 1906.6+712.1, 2473.8+864.3, 2149.9+626.9, 2001.1+557.3]
    = [928.3, 803.9, 1073.8, 1284.0, 1712.7, 2618.7, 3338.1, 2776.8, 2558.4]

Fonte ALL OTHERS CAMP: Base Giovano 26-04.xlsx > T.BR Farma
"""
import sys, shutil
sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path
from datetime import datetime

DASH = Path(r'C:\Users\valqu\OneDrive\Documentos\Claude\Projects\projeto Dashboard_farma_sul\Dashboard_farma_sul\Dashboard_Farma_Sul_20260512_2220.html')
VER  = DASH.parent / 'versoes'
DL   = Path.home() / 'Downloads'
ts   = datetime.now().strftime('%Y%m%d_%H%M')

shutil.copy(DASH, VER / f'Dashboard_Farma_Sul_{ts}_PreVolMkt.html')
h = DASH.read_text(encoding='utf-8')
print(f'Backup: ...PreVolMkt.html  |  {len(h):,} chars')

def replace_once(html, old, new, label):
    cnt = html.count(old)
    assert cnt == 1, f'ERRO [{label}]: {cnt}x encontrado (esperado 1)'
    print(f'✓ {label}')
    return html.replace(old, new, 1)

# ═══════════════════════════════════════════════════════════════════════════════
# VOL_MKT_DATA['T.BR Farma'] — somar ALL OTHERS CAMP
# ═══════════════════════════════════════════════════════════════════════════════
OLD = (
    "  'T.BR Farma': {fytd25_val:419.62,fytd26_val:350.32,"
    "fytd25_un:14946.3,fytd26_un:12958.3,"
    "monthly_val:[20.308,17.772,23.247,27.268,33.373,51.28,68.229,55.537,53.304],"
    "monthly_un:[732.5,631.2,818.2,957.9,1287.0,1906.6,2473.8,2149.9,2001.1]},"
)
NEW = (
    "  'T.BR Farma': {fytd25_val:532.09,fytd26_val:431.73,"
    "fytd25_un:20307.5,fytd26_un:17094.8,"
    "monthly_val:[24.420,21.460,28.637,33.890,41.707,64.612,84.928,67.661,64.414],"
    "monthly_un:[928.3,803.9,1073.8,1284.0,1712.7,2618.7,3338.1,2776.8,2558.4]},"
)
h = replace_once(h, OLD, NEW, 'VOL_MKT_DATA T.BR Farma + ALL OTHERS CAMP')

# ═══════════════════════════════════════════════════════════════════════════════
# Verificações
# ═══════════════════════════════════════════════════════════════════════════════
assert "fytd26_val:431.73,fytd25_un:20307.5" in h, 'ERRO: valores novos não encontrados'
assert "monthly_val:[24.420,21.460" in h,           'ERRO: monthly_val não atualizado'
print('Verificações: OK')
print(f'Tamanho final: {len(h):,} chars')

# ═══════════════════════════════════════════════════════════════════════════════
# Salvar
# ═══════════════════════════════════════════════════════════════════════════════
DASH.write_text(h, encoding='utf-8')
shutil.copy(DASH, VER / f'Dashboard_Farma_Sul_{ts}_VolMkt.html')
shutil.copy(DASH, DL  / f'Dashboard_FarmaSul_Giovano_{ts}.html')
print(f'Versao:    Dashboard_Farma_Sul_{ts}_VolMkt.html')
print(f'Downloads: Dashboard_FarmaSul_Giovano_{ts}.html')
print('DONE.')
