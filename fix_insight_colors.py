"""fix_insight_colors.py — corrige cores verde/vermelho nos diagnósticos Nielsen e KPI chips"""
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

# ─── FIX 1: remover !important da regra * que mata cores inline em insight/diag ─
# Esta é a causa raiz: [id$="-insight"] * { color:#334155 !important }
# Com !important e mesma especificidade (0,1,0) vence sobre as exception rules
# Removendo o !important, inline styles e exception rules voltam a funcionar
rep(
    '[id$="-diag"] *,\n[id$="-insight"] * { color:#334155 !important; }',
    '[id$="-diag"] *,\n[id$="-insight"] * { color:#334155; }',
    'insight/diag * — remove !important (allows inline colors through)'
)

# ─── FIX 2: adicionar overrides de alta especificidade para cores delta no Nielsen ─
# #panel-nielsen [style*="color:X"] tem especificidade (1,1,0) — bate QUALQUER regra (0,x,x)
# Isso garante que ef4444/34d399/fbbf24 mostram corretos em TODA a aba Nielsen
# (KPI chips, headline, insight, shr-trend, mso-area, etc.)
insert_after = '/* FIM TEMA VISUAL v2.0 */'
new_rules = """
/* ─── PATCH 44 — Nielsen delta colors: alta especificidade (1,1,0) ───────────
   Garante que ef4444 (vermelho) e 34d399→059669 (verde) e fbbf24 (amber)
   mostram corretos em TODOS os elementos dentro de #panel-nielsen,
   incluindo #mso-insight, #mso2-insight, #avg-insight, KPI chips etc.
   Especificidade (1,1,0) vence sobre [id$="-insight"] * (0,1,0) com ou sem !important
   ──────────────────────────────────────────────────────────────────────────── */
#panel-nielsen [style*="color:#ef4444"]  { color: #ef4444 !important; }
#panel-nielsen [style*="color:#EF4444"]  { color: #ef4444 !important; }
#panel-nielsen [style*="color:#34d399"]  { color: #059669 !important; }
#panel-nielsen [style*="color:#34D399"]  { color: #059669 !important; }
#panel-nielsen [style*="color:#059669"]  { color: #059669 !important; }
#panel-nielsen [style*="color:#fbbf24"]  { color: #b45309 !important; }
#panel-nielsen [style*="color:#16a34a"]  { color: #16a34a !important; }
#panel-nielsen [style*="color:#dc2626"]  { color: #dc2626 !important; }
"""

if new_rules.strip() not in html:
    rep(
        insert_after,
        insert_after + new_rules,
        'Patch44 Nielsen delta color overrides (alta especificidade)'
    )
else:
    print('  [SKIP] Patch44 já existe')

# ─── FIX 3: corrigir mso-headline HTML estático — color:#D1D5DB → #334155 ─────
# O headline contém spans coloridos; o container em si deve ter cor base escura
rep(
    'id="mso-headline" style="font-size:13px;color:#D1D5DB;',
    'id="mso-headline" style="font-size:13px;color:#334155;',
    'mso-headline container color: D1D5DB → 334155 (texto base claro)'
)

# ─── FIX 4: mso-headline background — remover amber bg que fica errado no tema claro ─
rep(
    'margin-bottom:18px;line-height:1.6;padding:12px 16px;background:rgba(251,191,36,0.05);border-radius:8px;border-left:3px solid #fbbf24;">',
    'margin-bottom:18px;line-height:1.6;padding:12px 16px;background:rgba(45,90,142,0.06);border-radius:8px;border-left:3px solid rgba(45,90,142,0.40);">',
    'mso-headline bg: amber tint → blue tint (tema claro)'
)

print(f'\nTotal: {fixes} fixes | Diff: {len(html)-orig:+,} bytes')
src.write_text(html, encoding='utf-8')

ts = datetime.datetime.now().strftime('%Y%m%d_%H%M')
ver = Path(f'Dashboard_farma_sul/versoes/Dashboard_Farma_Sul_{ts}_InsightColorFix.html')
dl  = Path.home() / 'Downloads' / f'Dashboard_FarmaSul_Giovano_{ts}.html'
shutil.copy2(src, ver)
shutil.copy2(src, dl)
print('Versao:', ver.name)
print('Download:', dl.name)
