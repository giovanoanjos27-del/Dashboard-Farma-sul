"""
patch_nielsen_tbr.py
====================
Atualiza a aba Nielsen com dados T.BR Farma de Base Giovano 26-04.xlsx.

Alterações:
  1. MSO_BRANDS — adiciona 'ALL OTHERS CAMP'
  2. MSO_COLORS — adiciona cor cinza para 'ALL OTHERS CAMP' (#94a3b8)
  3. MKTSHARE_OVERVIEW['T.BR Farma'] — adiciona entrada de share % para ALL OTHERS CAMP
  4. NIELSEN_BRAND_VAL['T.BR Farma'] — adiciona entrada de valor/unidades para ALL OTHERS CAMP

Fonte dos dados: Base Giovano 26-04.xlsx > aba 1-Tabela-1 > filtro T.BR Farma
FY26 = Jul/25–Mar/26 (9 meses) | FY25 = Jul/24–Mar/25 (9 meses)
"""
import sys, shutil
sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path
from datetime import datetime

DASH = Path(r'C:\Users\valqu\OneDrive\Documentos\Claude\Projects\projeto Dashboard_farma_sul\Dashboard_farma_sul\Dashboard_Farma_Sul_20260512_2220.html')
VER  = DASH.parent / 'versoes'
DL   = Path.home() / 'Downloads'
ts   = datetime.now().strftime('%Y%m%d_%H%M')

shutil.copy(DASH, VER / f'Dashboard_Farma_Sul_{ts}_PreNielsenTBR.html')
h = DASH.read_text(encoding='utf-8')
print(f'Backup: ...PreNielsenTBR.html  |  {len(h):,} chars')

def replace_once(html, old, new, label):
    cnt = html.count(old)
    assert cnt == 1, f'ERRO [{label}]: encontrado {cnt}x (esperado 1)'
    print(f'✓ {label}')
    return html.replace(old, new, 1)

# ═══════════════════════════════════════════════════════════════════════════════
# 1. MSO_BRANDS — adicionar ALL OTHERS CAMP
# ═══════════════════════════════════════════════════════════════════════════════
OLD1 = "const MSO_BRANDS = ['OFF!','EXPOSIS','XO INSETO','SUPER REPELEX','SBP'];"
NEW1 = "const MSO_BRANDS = ['OFF!','EXPOSIS','XO INSETO','SUPER REPELEX','SBP','ALL OTHERS CAMP'];"
h = replace_once(h, OLD1, NEW1, 'MSO_BRANDS + ALL OTHERS CAMP')

# ═══════════════════════════════════════════════════════════════════════════════
# 2. MSO_COLORS — adicionar cor para ALL OTHERS CAMP
# ═══════════════════════════════════════════════════════════════════════════════
OLD2 = "const MSO_COLORS = {'OFF!':'#fbbf24','EXPOSIS':'#3b82f6','XO INSETO':'#ef4444','SUPER REPELEX':'#f97316','SBP':'#06b6d4'};"
NEW2 = "const MSO_COLORS = {'OFF!':'#fbbf24','EXPOSIS':'#3b82f6','XO INSETO':'#ef4444','SUPER REPELEX':'#f97316','SBP':'#06b6d4','ALL OTHERS CAMP':'#94a3b8'};"
h = replace_once(h, OLD2, NEW2, 'MSO_COLORS + ALL OTHERS CAMP (#94a3b8 cinza)')

# ═══════════════════════════════════════════════════════════════════════════════
# 3. MKTSHARE_OVERVIEW['T.BR Farma'] — adicionar ALL OTHERS CAMP (share %)
#    FY25 share = 21.14% | FY26 share = 18.86% | delta = -2.28pp
#    monthly FY26 [Jul25–Mar26] calculados como 100% menos as outras marcas
#    jan25=20.09%, feb25=20.38%, mar25=20.35%
# ═══════════════════════════════════════════════════════════════════════════════
OLD3 = (
    "    'SBP': {fytd25:4.5, fytd26:4.0, delta:-0.5, monthly:[4.59,4.8,4.83,4.61,3.96,4.05,3.83,3.62,3.46], jan25:null, feb25:null},\n"
    "  },\n"
    "  'T.BR Farma Indep': {"
)
NEW3 = (
    "    'SBP': {fytd25:4.5, fytd26:4.0, delta:-0.5, monthly:[4.59,4.8,4.83,4.61,3.96,4.05,3.83,3.62,3.46], jan25:null, feb25:null},\n"
    "    'ALL OTHERS CAMP': {fytd25:21.14, fytd26:18.86, delta:-2.28, monthly:[16.83,17.19,18.81,19.54,19.98,20.64,19.67,17.92,17.24], jan25:20.09, feb25:20.38, mar25:20.35},\n"
    "  },\n"
    "  'T.BR Farma Indep': {"
)
h = replace_once(h, OLD3, NEW3, 'MKTSHARE_OVERVIEW T.BR Farma + ALL OTHERS CAMP share')

# ═══════════════════════════════════════════════════════════════════════════════
# 4. NIELSEN_BRAND_VAL['T.BR Farma'] — adicionar ALL OTHERS CAMP (valor + unidades)
#    Dados extraídos de Base Giovano 26-04.xlsx > T.BR Farma
#
#    fytd25_val = 112.467M | fytd26_val = 81.410M
#    fytd25_un  = 5361.2K  | fytd26_un  = 4136.5K
#
#    FY26 monthly_val [Jul25–Mar26]:
#      [4.112, 3.688, 5.390, 6.622, 8.334, 13.332, 16.699, 12.124, 11.110, 11.110]
#      (10 elementos — mantém padrão T.BR Farma existente)
#
#    FY25 jan/fev/mar: jan25=18.253M, fev25=18.037M, mar25=18.288M
#    FY26 jan/fev/mar: jan=16.699M, fev=12.124M, mar=11.110M
# ═══════════════════════════════════════════════════════════════════════════════
OLD4 = (
    "    'SBP': {fytd25_val:23.9257,fytd26_val:17.2908,fytd25_un:692.7618,fytd26_un:480.6864,"
    "jan_val:3.2554,fev_val:2.4483,mar_val:2.2278,jan_un:88.3287,fev_un:68.9299,mar_un:62.683,"
    "monthly_val:[1.12, 1.03, 1.383, 1.562, 1.65, 2.615, 3.255, 2.448, 2.227, 2.228],"
    "monthly_un:[31.6, 28.4, 38.6, 43.8, 45.7, 72.5, 88.3, 68.9, 63.0, 62.7],"
    "jan25_val:4.1294,fev25_val:4.2971,mar25_val:4.373,jan25_un:119.6487,fev25_un:123.9091,mar25_un:129.6222},\n"
    "  },\n"
    "  'T.BR Farma Indep': {"
)
NEW4 = (
    "    'SBP': {fytd25_val:23.9257,fytd26_val:17.2908,fytd25_un:692.7618,fytd26_un:480.6864,"
    "jan_val:3.2554,fev_val:2.4483,mar_val:2.2278,jan_un:88.3287,fev_un:68.9299,mar_un:62.683,"
    "monthly_val:[1.12, 1.03, 1.383, 1.562, 1.65, 2.615, 3.255, 2.448, 2.227, 2.228],"
    "monthly_un:[31.6, 28.4, 38.6, 43.8, 45.7, 72.5, 88.3, 68.9, 63.0, 62.7],"
    "jan25_val:4.1294,fev25_val:4.2971,mar25_val:4.373,jan25_un:119.6487,fev25_un:123.9091,mar25_un:129.6222},\n"
    "    'ALL OTHERS CAMP': {fytd25_val:112.467,fytd26_val:81.410,fytd25_un:5361.2,fytd26_un:4136.5,"
    "jan_val:16.699,fev_val:12.124,mar_val:11.110,jan_un:864.3,fev_un:626.9,mar_un:557.3,"
    "monthly_val:[4.112, 3.688, 5.390, 6.622, 8.334, 13.332, 16.699, 12.124, 11.110, 11.110],"
    "monthly_un:[195.8, 172.7, 255.6, 326.1, 425.7, 712.1, 864.3, 626.9, 557.3, 557.3],"
    "jan25_val:18.253,fev25_val:18.037,mar25_val:18.288,jan25_un:891.0,fev25_un:856.5,mar25_un:868.3},\n"
    "  },\n"
    "  'T.BR Farma Indep': {"
)
h = replace_once(h, OLD4, NEW4, 'NIELSEN_BRAND_VAL T.BR Farma + ALL OTHERS CAMP dados')

# ═══════════════════════════════════════════════════════════════════════════════
# Verificações
# ═══════════════════════════════════════════════════════════════════════════════
assert "'ALL OTHERS CAMP'" in h,     'ERRO: ALL OTHERS CAMP não inserido'
assert "MSO_BRANDS = ['OFF!','EXPOSIS','XO INSETO','SUPER REPELEX','SBP','ALL OTHERS CAMP']" in h, 'ERRO: MSO_BRANDS incompleto'
assert "'ALL OTHERS CAMP':'#94a3b8'" in h, 'ERRO: cor ALL OTHERS CAMP ausente'
assert 'fytd25:21.14' in h,          'ERRO: share fytd25 ausente'
assert 'fytd25_val:112.467' in h,    'ERRO: valor fytd25 ausente'
assert 'fytd26_val:81.410' in h,     'ERRO: valor fytd26 ausente'
print('Verificações: OK')
print(f'Tamanho final: {len(h):,} chars')

# ═══════════════════════════════════════════════════════════════════════════════
# Salvar
# ═══════════════════════════════════════════════════════════════════════════════
DASH.write_text(h, encoding='utf-8')
shutil.copy(DASH, VER / f'Dashboard_Farma_Sul_{ts}_NielsenTBR.html')
shutil.copy(DASH, DL  / f'Dashboard_FarmaSul_Giovano_{ts}.html')
print(f'Versao:    Dashboard_Farma_Sul_{ts}_NielsenTBR.html')
print(f'Downloads: Dashboard_FarmaSul_Giovano_{ts}.html')
print('DONE.')
