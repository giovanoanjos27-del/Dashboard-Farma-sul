"""fix_diag_bg2.py — corrige fundo dos diagnósticos: rgba branco → EAEEF4 cinza"""
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

# ─── FIX 1: CSS [id$="-diag"] e [id$="-insight"]: rgba branco → #EAEEF4 ────────
rep(
    '[id$="-diag"]    {\n  background: rgba(255,255,255,0.72) !important;',
    '[id$="-diag"]    {\n  background: #EAEEF4 !important;',
    '[id$="-diag"] bg: rgba(255,255,255,0.72) → #EAEEF4'
)
rep(
    '[id$="-insight"] {\n  background: rgba(255,255,255,0.72) !important;',
    '[id$="-insight"] {\n  background: #EAEEF4 !important;',
    '[id$="-insight"] bg: rgba(255,255,255,0.72) → #EAEEF4'
)

# ─── FIX 2: mso-area-highlights — bg cyan/transparente + cor/borda dark → light ──
rep(
    'id="mso-area-highlights" style="margin-top:14px;padding:12px 16px;background:rgba(103,232,249,0.05);border-radius:8px;border-left:3px solid #67e8f9;font-size:12px;color:#D1D5DB;line-height:1.8;"',
    'id="mso-area-highlights" style="margin-top:14px;padding:12px 16px;background:#EAEEF4;border-radius:10px;border:1px solid rgba(147,187,235,0.40);border-left:3px solid rgba(45,90,142,0.50);font-size:12px;color:#334155;line-height:1.8;"',
    'mso-area-highlights: bg cyan/dark → #EAEEF4 + borda azul sutil'
)

# ─── FIX 3: renderMSO2Insight — inner div bg dark → light ──────────────────────
# O JS gera <div style="background:#161B22;...border-left:3px solid rgba(251,191,36,0.6)...">
# Converter direto no JS para tema claro
rep(
    '\'<div style="background:#161B22;border-radius:10px;border-left:3px solid rgba(251,191,36,0.6);padding:14px 16px;">\'',
    '\'<div style="background:#EAEEF4;border-radius:10px;border:1px solid rgba(147,187,235,0.40);border-left:3px solid rgba(45,90,142,0.50);padding:14px 16px;">\'',
    'renderMSO2Insight JS inner div: #161B22 → #EAEEF4'
)

# ─── FIX 4: renderMSO2Insight — title color fbbf24+letter-spacing → light theme ─
# O titulo tem letter-spacing+fbbf24 que patch27 converte para #1E293B
# Melhor já converter no JS para evitar conflito
rep(
    "'<div style=\"font-size:9px;font-weight:700;letter-spacing:.14em;color:#fbbf24;text-transform:uppercase;margin-bottom:12px;\">📊 DIAGNÓSTICO · '+mkt+' · '+(isValI?'R$ MM':'Unidades')+' FYTD JUL-ABR/26</div>'",
    "'<div style=\"font-size:9px;font-weight:700;letter-spacing:.14em;color:#1D6FA8;text-transform:uppercase;margin-bottom:12px;\">📊 DIAGNÓSTICO · '+mkt+' · '+(isValI?'R$ MM':'Unidades')+' FYTD JUL-ABR/26</div>'",
    'renderMSO2Insight JS title: fbbf24 → 1D6FA8 (evita patch27 intercept)'
)

# ─── FIX 5: renderMSO2Insight share mode — title color fbbf24 → 1D6FA8 ─────────
rep(
    "'<div style=\"font-size:9px;font-weight:700;letter-spacing:.14em;color:#fbbf24;text-transform:uppercase;margin-bottom:9px;\">📊 DIAGNÓSTICO · '+mkt+' · Jan–Abr/26</div>'",
    "'<div style=\"font-size:9px;font-weight:700;letter-spacing:.14em;color:#1D6FA8;text-transform:uppercase;margin-bottom:9px;\">📊 DIAGNÓSTICO · '+mkt+' · Jan–Abr/26</div>'",
    'renderMSO2Insight share mode title: fbbf24 → 1D6FA8'
)

# ─── FIX 6: renderMSO2Insight — border-bottom dark rgba → azul sutil ─────────
rep(
    'border-bottom:0.5px solid rgba(255,255,255,0.06);">\n',
    'border-bottom:0.5px solid rgba(147,187,235,0.30);">\n',
    'renderMSO2Insight section border: dark rgba → blue'
)

# ─── FIX 7: renderMSO2Insight — row border dark rgba → azul ─────────────────
rep(
    'border-bottom:0.5px solid rgba(255,255,255,0.04);">\'',
    'border-bottom:0.5px solid rgba(147,187,235,0.25);">\'',
    'renderMSO2Insight row border: rgba(255,255,255,0.04) → blue'
)

# ─── FIX 8: renderMSO2Insight — shr badge bg dark → light ───────────────────
rep(
    "background:rgba(255,255,255,0.04);padding:1px 5px;border-radius:3px;\">shr '",
    "background:rgba(45,90,142,0.08);padding:1px 5px;border-radius:3px;\">shr '",
    'renderMSO2Insight shr badge: dark bg → blue sutil'
)

# ─── FIX 9: mso-area-highlights content — color #D1D5DB (via patch30 fica #334155) ─
# Ja coberto pelo FIX 2, mas checar se o STRONG dentro tem cor dark
# As cores internas geradas pelo JS de highlights vao ser cobertas pelas regras gerais

print(f'\nTotal: {fixes} fixes | Diff: {len(html)-orig:+,} bytes')
src.write_text(html, encoding='utf-8')

ts = datetime.datetime.now().strftime('%Y%m%d_%H%M')
ver = Path(f'Dashboard_farma_sul/versoes/Dashboard_Farma_Sul_{ts}_DiagBg2.html')
dl  = Path.home() / 'Downloads' / f'Dashboard_FarmaSul_Giovano_{ts}.html'
shutil.copy2(src, ver)
shutil.copy2(src, dl)
print('Versao:', ver.name)
print('Download:', dl.name)
