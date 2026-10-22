"""patch46b_bg3c.py — Aplica fundo 3C #DFECFB corretamente via --bg-base + fallbacks"""
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

# ── Fix 1: injetar --bg-base no :root (não existia definido) ──────────────
rep(
    ':root {\n  --bg-card:      #EAEEF4;',
    ':root {\n  --bg-base:      #DFECFB;\n  --bg-base-filter: #C5D5EC;\n  --bg-card:      #EAEEF4;',
    ':root — injetar --bg-base + --bg-base-filter'
)

# ── Fix 2: fallbacks var(--bg-base, #93BBEB) → atualizar fallback ─────────
rep(
    'var(--bg-base, #93BBEB)',
    'var(--bg-base, #DFECFB)',
    'fallback var(--bg-base, #93BBEB) → #DFECFB'
)

# ── Fix 3: scrollbar thumb #4D8FCC → mais suave para o novo bg ────────────
rep(
    'background: #4D8FCC; border-radius: 4px;',
    'background: #8BAEC8; border-radius: 4px;',
    'scrollbar thumb #4D8FCC → #8BAEC8'
)

# ── Fix 4: qualquer body background direto que ainda use cor antiga ────────
rep('background:#93BBEB',  'background:#DFECFB', 'bg direto #93BBEB (sem espaço)')
rep('background: #93BBEB', 'background: #DFECFB', 'bg direto #93BBEB (com espaço)')

print(f'\nTotal: {fixes} fixes | Diff: {len(html)-orig:+,} bytes')
src.write_text(html, encoding='utf-8')

ts = datetime.datetime.now().strftime('%Y%m%d_%H%M')
ver = Path(f'Dashboard_farma_sul/versoes/Dashboard_Farma_Sul_{ts}_Bg3C.html')
dl  = Path.home() / 'Downloads' / f'Dashboard_FarmaSul_Giovano_{ts}.html'
shutil.copy2(src, ver)
shutil.copy2(src, dl)
print('Versao:', ver.name)
print('Download:', dl.name)
