"""
patch_nielsen_total_mercado.py
==============================
Corrige FYTD_MARKET_TOTAL['T.BR Farma'] somando ALL OTHERS CAMP ao total.

PROBLEMA: O card "TOTAL MERCADO" exibia R$350.32MM (FY26) e R$419.62MM (FY25)
          pois FYTD_MARKET_TOTAL soma apenas as 5 marcas originais.

CORREÇÃO:  Adicionar ALL OTHERS CAMP a todos os campos numéricos do total:
           fytd26_val: 350.3181 + 81.4096 = 431.7277 MM  (→ R$431.73MM)
           fytd25_val: 419.6214 + 112.4675 = 532.0889 MM (→ R$532.09MM)

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

shutil.copy(DASH, VER / f'Dashboard_Farma_Sul_{ts}_PreNielsenTotal.html')
h = DASH.read_text(encoding='utf-8')
print(f'Backup: ...PreNielsenTotal.html  |  {len(h):,} chars')

def replace_once(html, old, new, label):
    cnt = html.count(old)
    assert cnt == 1, f'ERRO [{label}]: {cnt}x encontrado (esperado 1)'
    print(f'✓ {label}')
    return html.replace(old, new, 1)

# ═══════════════════════════════════════════════════════════════════════════════
# FYTD_MARKET_TOTAL['T.BR Farma'] — somar ALL OTHERS CAMP a todos os campos
#
# Valores adicionados de ALL OTHERS CAMP (Base Giovano 26-04.xlsx):
#   fytd25 = 112.4675M | fytd26 = 81.4096M
#   fytd25_un = 5361.2K | fytd26_un = 4136.5K
#   jan25_val=18.253 | fev25_val=18.037 | mar25_val=18.288 | janmar25=54.578
#   jan26_val=16.699 | fev26_val=12.124 | mar26_val=11.110 | janmar26=39.933
#   jan25_un=891.0   | fev25_un=856.5   | mar25_un=868.3   | janmar25_un=2615.8
#   jan26_un=864.3   | fev26_un=626.9   | mar26_un=557.3   | janmar26_un=2048.5
# ═══════════════════════════════════════════════════════════════════════════════
OLD = (
    "  'T.BR Farma': {fytd25_val:419.6214,fytd26_val:350.3181,"
    "fytd25_un:14946.3189,fytd26_un:12958.2505,"
    "jan25_val:72.6446,fev25_val:70.4104,mar25_val:71.6065,janmar25_val:214.6616,"
    "jan26_val:68.2291,fev26_val:55.5373,mar26_val:53.3038,janmar26_val:177.0701,"
    "jan25_un:2630.9657,fev25_un:2513.3262,mar25_un:2530.4982,janmar25_un:7674.7902,"
    "jan26_un:2473.7783,fev26_un:2149.9163,mar26_un:2001.1018,janmar26_un:6624.7964},"
)
NEW = (
    "  'T.BR Farma': {fytd25_val:532.0889,fytd26_val:431.7277,"
    "fytd25_un:20307.5189,fytd26_un:17094.7505,"
    "jan25_val:90.8976,fev25_val:88.4474,mar25_val:89.8945,janmar25_val:269.2395,"
    "jan26_val:84.9281,fev26_val:67.6613,mar26_val:64.4138,janmar26_val:217.0031,"
    "jan25_un:3521.9657,fev25_un:3369.8262,mar25_un:3398.7982,janmar25_un:10290.5902,"
    "jan26_un:3338.0783,fev26_un:2776.8163,mar26_un:2558.4018,janmar26_un:8673.2964},"
)
h = replace_once(h, OLD, NEW, 'FYTD_MARKET_TOTAL T.BR Farma + ALL OTHERS CAMP')

# ═══════════════════════════════════════════════════════════════════════════════
# Verificações
# ═══════════════════════════════════════════════════════════════════════════════
assert 'fytd26_val:431.7277' in h,  'ERRO: fytd26 total não atualizado'
assert 'fytd25_val:532.0889' in h,  'ERRO: fytd25 total não atualizado'
assert 'jan26_val:84.9281'  in h,   'ERRO: jan26 total não atualizado'
assert 'janmar26_val:217.0031' in h,'ERRO: janmar26 total não atualizado'
print('Verificações: OK')
print(f'Tamanho final: {len(h):,} chars')

# ═══════════════════════════════════════════════════════════════════════════════
# Salvar
# ═══════════════════════════════════════════════════════════════════════════════
DASH.write_text(h, encoding='utf-8')
shutil.copy(DASH, VER / f'Dashboard_Farma_Sul_{ts}_NielsenTotal.html')
shutil.copy(DASH, DL  / f'Dashboard_FarmaSul_Giovano_{ts}.html')
print(f'Versao:    Dashboard_Farma_Sul_{ts}_NielsenTotal.html')
print(f'Downloads: Dashboard_FarmaSul_Giovano_{ts}.html')
print('DONE.')
