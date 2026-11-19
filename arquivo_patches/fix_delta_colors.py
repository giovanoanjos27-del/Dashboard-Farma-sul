"""fix_delta_colors.py — remove !important das 2 regras que bloqueiam cores inline verde/vermelho"""
import sys, datetime, shutil
sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path

src = Path('Dashboard_farma_sul/Dashboard_Farma_Sul_20260512_2220.html')
html = src.read_text(encoding='utf-8')
orig = len(html)
fixes = 0

def rep(old, new, label):
    global html, fixes
    c = html.count(old)
    if c == 0:
        print(f'  [MISS] {label}')
        return
    html = html.replace(old, new)
    fixes += c
    print(f'  [OK]   {label} ({c}x)')

# FIX 1: patch19 NielsenTemaClaro — regra alta especificidade que bloqueia inline colors
rep(
    '#panel-nielsen table tbody td { color: #475569 !important; }',
    '#panel-nielsen table tbody td { color: #475569; }',
    '#panel-nielsen tbody td: remove !important do color'
)

# FIX 2: regra genérica tbody tr td — bloqueia inline colors em todas as tabelas
rep(
    'tbody tr td { color:#334155 !important; }',
    'tbody tr td { color:#334155; }',
    'tbody tr td: remove !important do color'
)

# FIX 3: garantir que as exception rules de cor estao presentes apos a secao 15
# Verificar se ja existem
has_green = '[style*="color:#16a34a"]  { color: #16a34a !important; }' in html
has_red   = '[style*="color:#dc2626"]  { color: #dc2626 !important; }' in html
print(f'  [CHECK] Exception verde presente: {has_green}')
print(f'  [CHECK] Exception vermelho presente: {has_red}')

# Se nao existirem, adicionar antes do </style> do bloco consolidado
if not has_green or not has_red:
    # Localizar o bloco de excecoes existente ou inserir apos a secao 15b
    marker = '/* 15b. Cor de delta — exceções explícitas */'
    if marker in html:
        # Substituir o bloco inteiro para garantir as regras
        old_block = marker + '\n[style*="color:#16a34a"]  { color: #16a34a !important; }\n[style*="color:#dc2626"]  { color: #dc2626 !important; }\n[style*="color:#059669"]  { color: #059669 !important; }\n[style*="color:#ef4444"]  { color: #ef4444 !important; }'
        new_block = marker + '\n[style*="color:#16a34a"]  { color: #16a34a !important; }\n[style*="color:#dc2626"]  { color: #dc2626 !important; }\n[style*="color:#059669"]  { color: #059669 !important; }\n[style*="color:#ef4444"]  { color: #ef4444 !important; }'
        # Ja existe, nao precisa mudar
        print('  [CHECK] Bloco 15b ja existe no HTML')

print(f'\nTotal: {fixes} fixes | Diff: {len(html)-orig:+,} bytes')
src.write_text(html, encoding='utf-8')

ts = datetime.datetime.now().strftime('%Y%m%d_%H%M')
ver = Path(f'Dashboard_farma_sul/versoes/Dashboard_Farma_Sul_{ts}_DeltaColorFix.html')
dl  = Path.home() / 'Downloads' / f'Dashboard_FarmaSul_Giovano_{ts}.html'
shutil.copy2(src, ver)
shutil.copy2(src, dl)
print('Versao:', ver.name)
print('Download:', dl.name)
