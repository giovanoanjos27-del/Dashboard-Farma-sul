"""patch46_bg3c.py — Fundo azul: #93BBEB → #DFECFB (Opção 3C) + cores derivadas"""
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

# ── Cor principal: fundo #93BBEB → #DFECFB ─────────────────────────────────
rep('--bg-base:#93BBEB',          '--bg-base:#DFECFB',          '--bg-base')
rep('--bg-base: #93BBEB',         '--bg-base: #DFECFB',         '--bg-base (espaço)')
rep('background:#93BBEB',         'background:#DFECFB',         'background direto')
rep('background: #93BBEB',        'background: #DFECFB',        'background direto (espaço)')

# ── Cores derivadas (ajustadas proporcionalmente ao novo tom) ───────────────
# Filter bar: era #7BAAD8 (mais escuro que bg), agora #C5D5EC
rep('--bg-filter:#7BAAD8',        '--bg-filter:#C5D5EC',        '--bg-filter')
rep('--bg-filter: #7BAAD8',       '--bg-filter: #C5D5EC',       '--bg-filter (espaço)')
rep('background:#7BAAD8',         'background:#C5D5EC',         'bg-filter direto')

# Subtle/hover: eram #A8C8F0/#A0C4E8, agora #E5F0FC/#E1ECFB
rep('--bg-subtle:#A8C8F0',        '--bg-subtle:#E5F0FC',        '--bg-subtle')
rep('--bg-subtle: #A8C8F0',       '--bg-subtle: #E5F0FC',       '--bg-subtle (espaço)')
rep('--bg-hover:#A0C4E8',         '--bg-hover:#E1ECFB',         '--bg-hover')
rep('--bg-hover: #A0C4E8',        '--bg-hover: #E1ECFB',        '--bg-hover (espaço)')

# Toggle track: era #7BAAD8
rep('background:#7BAAD8;',        'background:#C5D5EC;',        'toggle track')

# Scrollbar thumb: era #4D8FCC
rep('--scrollbar-thumb:#4D8FCC',  '--scrollbar-thumb:#8BAEC8',  '--scrollbar-thumb')
rep('background:#4D8FCC',         'background:#8BAEC8',         'scrollbar thumb direto')

# Patch45 panel backgrounds que usam #93BBEB diretamente
rep("background:#93BBEB !important",  "background:#DFECFB !important",  'patch45 panel bg !important')
rep("background: #93BBEB !important", "background: #DFECFB !important", 'patch45 panel bg !important (espaço)')

print(f'\nTotal: {fixes} fixes | Diff: {len(html)-orig:+,} bytes')
src.write_text(html, encoding='utf-8')

ts = datetime.datetime.now().strftime('%Y%m%d_%H%M')
ver = Path(f'Dashboard_farma_sul/versoes/Dashboard_Farma_Sul_{ts}_Bg3C.html')
dl  = Path.home() / 'Downloads' / f'Dashboard_FarmaSul_Giovano_{ts}.html'
shutil.copy2(src, ver)
shutil.copy2(src, dl)
print('Versao:', ver.name)
print('Download:', dl.name)
