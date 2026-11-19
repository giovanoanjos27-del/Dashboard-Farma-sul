"""fix_diag_bg3.py — fixes restantes: títulos fbbf24→1D6FA8 e bordas sections"""
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
    else:
        html = html.replace(old, new)
        fixes += c
        print(f'  [OK]   {label} ({c}x)')

# Fix 1: titulo diagnostico modo enriquecido (JAN-ABR)
rep(
    'margin-bottom:12px;">📊 DIAGNÓSTICO · \'+mkt+\' · \'+(isValI?\'R$ MM\':\'Unidades\')+\' JAN–4BR/26</div>\'',
    'margin-bottom:12px;">📊 DIAGNÓSTICO · \'+mkt+\' · \'+(isValI?\'R$ MM\':\'Unidades\')+\' JAN–4BR/26</div>\'',
    'placeholder'
)

# Abordagem alternativa: substituir diretamente no texto
old_a = 'letter-spacing:.14em;color:#fbbf24;text-transform:uppercase;margin-bottom:12px;">\xf0\x9f\x93\x8a DIAGN\xc3\x93STICO'
old_a = 'color:#fbbf24;text-transform:uppercase;margin-bottom:12px;">📊 DIAGNÓSTICO'
new_a = 'color:#1D6FA8;text-transform:uppercase;margin-bottom:12px;">📊 DIAGNÓSTICO'
c = html.count(old_a)
if c > 0:
    html = html.replace(old_a, new_a)
    fixes += c
    print(f'  [OK]   titulo fbbf24→1D6FA8 (diagnostico): {c}x')
else:
    print(f'  [MISS] titulo diagnostico')

# Fix 2: DIAGNOSTICO com entidade HTML (outro render)
old_b = 'color:#fbbf24;text-transform:uppercase;margin-bottom:12px;">&#128202; DIAGNOSTICO'
new_b = 'color:#1D6FA8;text-transform:uppercase;margin-bottom:12px;">&#128202; DIAGNOSTICO'
c2 = html.count(old_b)
if c2 > 0:
    html = html.replace(old_b, new_b)
    fixes += c2
    print(f'  [OK]   titulo fbbf24→1D6FA8 (DIAGNOSTICO entidade): {c2}x')
else:
    print(f'  [MISS] titulo DIAGNOSTICO entidade')

# Fix 3: section border-bottom dark dentro dos JS renders (rgba 255 0.06)
old_c = 'border-bottom:0.5px solid rgba(255,255,255,0.06);">'
new_c = 'border-bottom:0.5px solid rgba(147,187,235,0.30);">'
c3 = html.count(old_c)
if c3 > 0:
    html = html.replace(old_c, new_c)
    fixes += c3
    print(f'  [OK]   section border dark rgba(255,255,255,0.06) → blue: {c3}x')
else:
    print(f'  [MISS] section border')

print(f'\nTotal: {fixes} fixes | Diff: {len(html)-orig:+,} bytes')
src.write_text(html, encoding='utf-8')

ts = datetime.datetime.now().strftime('%Y%m%d_%H%M')
ver = Path(f'Dashboard_farma_sul/versoes/Dashboard_Farma_Sul_{ts}_DiagBg3.html')
dl  = Path.home() / 'Downloads' / f'Dashboard_FarmaSul_Giovano_{ts}.html'
shutil.copy2(src, ver)
shutil.copy2(src, dl)
print('Versao:', ver.name)
print('Download:', dl.name)
