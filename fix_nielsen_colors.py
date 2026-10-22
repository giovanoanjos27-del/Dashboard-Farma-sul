"""fix_nielsen_colors.py — varredura completa das cores positivo/negativo em Nielsen"""
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

# ─── FIX 1: table td — remover !important do color para inline styles passarem ───
rep(
    'table td {\n  background:    #EAEEF4 !important;\n  color:         #1E293B !important;',
    'table td {\n  background:    #EAEEF4 !important;\n  color:         #1E293B;',
    'table td color !important removido — inline verde/vermelho vai passar'
)

# ─── FIX 2: mso-insight container — inline dark → light ──────────────────────
rep(
    'background:rgba(255,255,255,0.03);border-radius:8px;border-left:3px solid rgba(255,255,255,0.1);font-size:11px;color:#D1D5DB',
    'background:rgba(45,90,142,0.06);border-radius:10px;border-left:3px solid rgba(45,90,142,0.45);font-size:11px;color:#1E293B',
    'mso-insight bg+border+color: dark → light'
)

# ─── FIX 3: diagnóstico title — letter-spacing+#fbbf24 interceptado por patch27 → remover letter-spacing ───
rep(
    'color:#fbbf24;font-size:10px;letter-spacing:0.08em;">',
    'color:#1D6FA8;font-size:10px;font-weight:700;">',
    'diag title: fbbf24+letter-spacing → 1D6FA8 sem letter-spacing (evita patch27 intercept)'
)

# ─── FIX 4: diagnóstico — market name e2e8f0 → 334155 ───────────────────────
rep(
    'em <strong style="color:#e2e8f0;">',
    'em <strong style="color:#334155;">',
    'diag market name: e2e8f0 → 334155'
)

# ─── FIX 5: diagnóstico — scj_f26 e2e8f0 → 1E293B ───────────────────────────
# Encontrar a linha do SCJ no diagnóstico que usa color:#e2e8f0
rep(
    'FYTD26\' +\' <span style="color:\'+scjDc',
    'FYTD26 <span style="color:\'+scjDc',
    'diag SCJ FYTD26 text spacing fix'
)

# ─── FIX 6: .d-table td — também remover !important ─────────────────────────
rep(
    '.d-table td                 { background: #EAEEF4 !important; color: #1E293B !important; }',
    '.d-table td                 { background: #EAEEF4 !important; color: #1E293B; }',
    '.d-table td color !important removido'
)

# ─── FIX 7: mso2-insight shr-st-wrap2 border dark → light ────────────────────
rep(
    'border-top:1px solid rgba(255,255,255,0.06);display:none;">',
    'border-top:1px solid rgba(45,90,142,0.2);display:none;">',
    'shr-st-wrap border dark → blue (2x)'
)

print(f'\nTotal: {fixes} fixes | Diff: {len(html)-orig:+,} bytes')
src.write_text(html, encoding='utf-8')
ts = datetime.datetime.now().strftime('%Y%m%d_%H%M')
ver = Path(f'Dashboard_farma_sul/versoes/Dashboard_Farma_Sul_{ts}_NielsenColorFix.html')
dl  = Path.home() / 'Downloads' / f'Dashboard_FarmaSul_Giovano_{ts}.html'
shutil.copy2(src, ver)
shutil.copy2(src, dl)
print('Versao:', ver.name)
print('Download:', dl.name)
