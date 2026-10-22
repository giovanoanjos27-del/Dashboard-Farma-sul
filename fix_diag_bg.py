"""fix_diag_bg.py — padroniza fundo de TODOS os cards de diagnóstico/insight"""
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

# ─── FIX 1: CSS rule [id$="-diag"] e [id$="-insight"] — padronizar visual ─────
# Fundo: rgba(255,255,255,0.72) + border-radius + borda + sombra
rep(
    '[id$="-diag"]    {\n  background:#F0F6FF !important;\n  border-left-color:#2563EB !important;\n  color:#334155 !important;\n}\n[id$="-insight"] {\n  background:#F0F6FF !important;\n  border-left-color:#2563EB !important;\n  color:#334155 !important;\n}',
    '[id$="-diag"]    {\n  background: rgba(255,255,255,0.72) !important;\n  border-radius: 10px !important;\n  border: 1px solid rgba(147,187,235,0.40) !important;\n  border-left: 3px solid rgba(45,90,142,0.50) !important;\n  box-shadow: 0 1px 6px rgba(10,40,80,0.08) !important;\n  padding: 12px 16px !important;\n  color:#334155 !important;\n}\n[id$="-insight"] {\n  background: rgba(255,255,255,0.72) !important;\n  border-radius: 10px !important;\n  border: 1px solid rgba(147,187,235,0.40) !important;\n  border-left: 3px solid rgba(45,90,142,0.50) !important;\n  box-shadow: 0 1px 6px rgba(10,40,80,0.08) !important;\n  padding: 12px 16px !important;\n  color:#334155 !important;\n}',
    '[id$="-diag"] e [id$="-insight"]: bg padronizado rgba(255,255,255,0.72)'
)

# ─── FIX 2: inline style do mso-insight — remover background/border-radius conflitantes ─
# CSS já cobre com !important, mas limpar o inline deixa mais limpo
rep(
    'id="mso-insight" style="margin-top:14px;padding:14px 16px;background:rgba(45,90,142,0.06);border-radius:10px;border-left:3px solid rgba(45,90,142,0.45);font-size:11px;color:#1E293B;line-height:1.9;"',
    'id="mso-insight" style="margin-top:14px;font-size:11px;color:#1E293B;line-height:1.9;"',
    'mso-insight inline: remove bg/border/radius (CSS cobre)'
)

# ─── FIX 3: mso2-insight — mesmo padrão ─────────────────────────────────────
rep(
    'id="mso2-insight" style="margin-top:12px;padding:12px 16px;background:rgba(45,90,142,0.06);border-radius:10px;border-left:3px solid rgba(45,90,142,0.45);font-size:11px;color:#1E293B;line-height:1.9;display:none;"',
    'id="mso2-insight" style="margin-top:12px;font-size:11px;color:#1E293B;line-height:1.9;display:none;"',
    'mso2-insight inline: remove bg/border/radius (CSS cobre)'
)

# ─── FIX 4: avg-insight se tiver inline bg ───────────────────────────────────
# Procurar e limpar qualquer avg-insight com inline bg
import re
def fix_insight_inline(id_name):
    global html, fixes
    pattern = f'id="{id_name}" style="([^"]*)"'
    match = re.search(pattern, html)
    if not match:
        print(f'  [MISS] {id_name} não encontrado')
        return
    old_style = match.group(1)
    # Remover background, border-left, border-radius do inline style
    new_style = re.sub(r'background:[^;]+;?\s*', '', old_style)
    new_style = re.sub(r'border-left:[^;]+;?\s*', '', new_style)
    new_style = re.sub(r'border-radius:[^;]+;?\s*', '', new_style)
    new_style = re.sub(r'padding:[^;]+;?\s*', '', new_style)
    new_style = new_style.strip().strip(';')
    if old_style != new_style:
        old_full = f'id="{id_name}" style="{old_style}"'
        new_full = f'id="{id_name}" style="{new_style}"'
        c = html.count(old_full)
        if c > 0:
            html = html.replace(old_full, new_full)
            fixes += c
            print(f'  [OK]   {id_name} inline: bg/border removidos ({c}x)')
        else:
            print(f'  [MISS] {id_name} (match nao encontrado para replace)')
    else:
        print(f'  [SKIP] {id_name} sem inline bg/border')

fix_insight_inline('avg-insight')
fix_insight_inline('ob-share-diag')
fix_insight_inline('ob-preco-diag')
fix_insight_inline('ob-mkt-diag')
fix_insight_inline('shr-st-diag')
fix_insight_inline('shr-st2-diag')

print(f'\nTotal: {fixes} fixes | Diff: {len(html)-orig:+,} bytes')
src.write_text(html, encoding='utf-8')

ts = datetime.datetime.now().strftime('%Y%m%d_%H%M')
ver = Path(f'Dashboard_farma_sul/versoes/Dashboard_Farma_Sul_{ts}_DiagBgFix.html')
dl  = Path.home() / 'Downloads' / f'Dashboard_FarmaSul_Giovano_{ts}.html'
shutil.copy2(src, ver)
shutil.copy2(src, dl)
print('Versao:', ver.name)
print('Download:', dl.name)
