"""
Compacta visualmente a tabela de UFs no card ESTUDO ED NACIONAL:
- Reduz padding das linhas (7px → 4px)
- Reduz badge Prioridade (padding + font-size)
- Reduz barra de Penetração (height + width)
- Compacta header da tabela (padding + font)
- Compacta KPI cards (padding + font)
- Reduz espaçamento entre KPI grids
"""
import sys
import shutil
sys.stdout.reconfigure(encoding="utf-8")
from datetime import datetime
from pathlib import Path

BASE = Path(r"C:\Users\valqu\OneDrive\Documentos\Claude\Projects\projeto Dashboard_farma_sul\Dashboard_farma_sul")
DASH = BASE / "Dashboard_Farma_Sul_20260512_2220.html"
VER  = BASE / "versoes"
DL   = Path.home() / "Downloads"

html = DASH.read_text(encoding='utf-8')
orig = len(html)
applied = []

# ── Backup ────────────────────────────────────────────────────────────────────
ts = datetime.now().strftime('%Y%m%d_%H%M')
shutil.copy(DASH, VER / f"Dashboard_Farma_Sul_{ts}_PreCompactUF.html")
print(f"Backup: Dashboard_Farma_Sul_{ts}_PreCompactUF.html")

# ─────────────────────────────────────────────────────────────────────────────
# 1. Linhas da tabela: padding 7px → 4px  (todas as colunas de dado)
# ─────────────────────────────────────────────────────────────────────────────
replacements_row = [
    # Universe
    ('padding:7px 8px;text-align:right;color:#67e8f9;font-weight:700',
     'padding:4px 8px;text-align:right;color:#67e8f9;font-weight:700'),
    # SCJ FY25 (zero)
    ('padding:7px 8px;text-align:right;color:#94A3B8',
     'padding:4px 8px;text-align:right;color:#94A3B8'),
    # SCJ FY26
    ('padding:7px 8px;text-align:right;color:#34d399;font-weight:700',
     'padding:4px 8px;text-align:right;color:#34d399;font-weight:700'),
    # CIMED
    ('padding:7px 8px;text-align:right;color:#3b82f6',
     'padding:4px 8px;text-align:right;color:#3b82f6'),
    # RB
    ('padding:7px 8px;text-align:right;color:#f97316',
     'padding:4px 8px;text-align:right;color:#f97316'),
    # Oportunidade
    ('padding:7px 8px;text-align:right;color:#06b6d4;font-weight:700',
     'padding:4px 8px;text-align:right;color:#06b6d4;font-weight:700'),
    # Reconquista
    ('padding:7px 8px;text-align:right;color:#2dd4bf',
     'padding:4px 8px;text-align:right;color:#2dd4bf'),
    # Novos PDVs
    ('padding:7px 8px;text-align:right;color:#fbbf24',
     'padding:4px 8px;text-align:right;color:#fbbf24'),
]
for old, new in replacements_row:
    if old in html:
        html = html.replace(old, new)
        applied.append(f"Row padding: ...{old[-30:]}")

# ── 2. td Prioridade: padding 7px → 4px + badge compacto ─────────────────────
OLD_PRIO_TD  = 'padding:7px 8px;">\'\n        +\'<span style="padding:2px 7px;border-radius:4px;font-size:9px;font-weight:700'
NEW_PRIO_TD  = 'padding:4px 6px;">\'\n        +\'<span style="padding:1px 5px;border-radius:3px;font-size:8px;font-weight:700'
if OLD_PRIO_TD in html:
    html = html.replace(OLD_PRIO_TD, NEW_PRIO_TD, 1)
    applied.append("Badge Prioridade compactado")
else:
    print("AVISO: badge Prioridade nao encontrado exatamente, tentando fallback")
    # Fallback: só o td padding
    html = html.replace(
        '\'<td style="padding:7px 8px;">\'\n        +\'<span style="padding:2px 7px',
        '\'<td style="padding:4px 6px;">\'\n        +\'<span style="padding:1px 5px',
        1
    )

# ── 3. td Penetração: padding 7px → 4px ──────────────────────────────────────
OLD_PEN_TD = 'padding:7px 8px;">\'\n        +\'<div style="display:flex;align-items:center;gap:5px'
NEW_PEN_TD = 'padding:4px 6px;">\'\n        +\'<div style="display:flex;align-items:center;gap:4px'
if OLD_PEN_TD in html:
    html = html.replace(OLD_PEN_TD, NEW_PEN_TD, 1)
    applied.append("td Penetração compactado")
else:
    print("AVISO: td Penetracao nao encontrado")

# ── 4. Barra penetração: height:7px → 5px, width:60px → 50px ─────────────────
OLD_BAR = 'background:rgba(52,211,153,0.12);border-radius:3px;height:7px;width:60px;overflow:hidden'
NEW_BAR = 'background:rgba(52,211,153,0.12);border-radius:3px;height:5px;width:50px;overflow:hidden'
if OLD_BAR in html:
    html = html.replace(OLD_BAR, NEW_BAR)
    applied.append("Barra penetracao: 7px/60px -> 5px/50px")
else:
    print("AVISO: barra penetracao nao encontrada")

# ── 5. Header thead: font-size:10px → 9px, padding:8px → 5px 8px ─────────────
OLD_HEAD = '<thead><tr style="color:#94A3B8;border-bottom:1px solid rgba(255,255,255,0.1);font-size:10px;">'
NEW_HEAD = '<thead><tr style="color:#94A3B8;border-bottom:1px solid rgba(255,255,255,0.08);font-size:9px;">'
if OLD_HEAD in html:
    html = html.replace(OLD_HEAD, NEW_HEAD)
    applied.append("thead: font 10->9px, border mais suave")
else:
    print("AVISO: thead nao encontrado")

OLD_TH_PAD = '<th style="padding:8px;text-align:left;">UF</th>'
NEW_TH_PAD = '<th style="padding:5px 8px;text-align:left;">UF</th>'
if OLD_TH_PAD in html:
    html = html.replace(OLD_TH_PAD, NEW_TH_PAD)
    applied.append("TH UF padding: 8px -> 5px 8px")

# Todas as demais th com padding:8px
html = html.replace(
    '<th style="padding:8px;text-align:right;',
    '<th style="padding:5px 8px;text-align:right;'
)
html = html.replace(
    '<th style="padding:8px;text-align:left;">Prioridade</th>',
    '<th style="padding:5px 8px;text-align:left;">Prioridade</th>'
)
applied.append("TH padding geral: 8px -> 5px 8px")

# ── 6. Tabela font-size: 11px → 10.5px ────────────────────────────────────────
OLD_TBL = '<table style="width:100%;border-collapse:collapse;font-size:11px;min-width:780px;">'
NEW_TBL = '<table style="width:100%;border-collapse:collapse;font-size:10.5px;min-width:780px;">'
if OLD_TBL in html:
    html = html.replace(OLD_TBL, NEW_TBL)
    applied.append("Tabela font-size: 11px -> 10.5px")
else:
    print("AVISO: tabela font-size nao encontrado")

# ── 7. KPI cards: padding:14px → 10px, font 20px → 16px ─────────────────────
# KPI card padding (dentro do grid de KPIs do renderIqviaNacional)
# Substitui apenas no contexto do kpiHtml (border-radius:10px;padding:14px;border-top:2px)
OLD_KPI_DIV = 'background:#161B22;border-radius:10px;padding:14px;border-top:2px solid '
NEW_KPI_DIV = 'background:#161B22;border-radius:10px;padding:10px 12px;border-top:2px solid '
count_kpi = html.count(OLD_KPI_DIV)
if count_kpi > 0:
    html = html.replace(OLD_KPI_DIV, NEW_KPI_DIV)
    applied.append(f"KPI card padding: 14px -> 10px 12px ({count_kpi} cards)")
else:
    print("AVISO: KPI card padding nao encontrado")

OLD_KPI_VAL = 'font-size:20px;font-weight:800;color:'
NEW_KPI_VAL = 'font-size:16px;font-weight:800;color:'
cnt = html.count(OLD_KPI_VAL)
if cnt:
    html = html.replace(OLD_KPI_VAL, NEW_KPI_VAL)
    applied.append(f"KPI valor font: 20px -> 16px ({cnt} ocorrencias)")

# ── 8. KPI grid margin-bottom: 18px → 12px ────────────────────────────────────
# Dentro do kpiHtml de renderIqviaNacional há margin-bottom:18px no grid
# Só substituir nos 2 grids de KPI (repeat(4,1fr))
OLD_GRID_MB = 'grid-template-columns:repeat(4,1fr);gap:10px;margin-bottom:18px'
NEW_GRID_MB = 'grid-template-columns:repeat(4,1fr);gap:8px;margin-bottom:10px'
if OLD_GRID_MB in html:
    html = html.replace(OLD_GRID_MB, NEW_GRID_MB)
    applied.append("KPI grid margin + gap compactados")

# ── 9. Barra Universe: height:26px → 20px, padding:16px → 10px ───────────────
html = html.replace(
    'border:0.5px solid rgba(103,232,249,0.15);">\n    +\'<div style="font-size:10px;font-weight:700;letter-spacing:0.1em;color:#67e8f9;margin-bottom:10px;">📊 COMPOSIÇÃO',
    'border:0.5px solid rgba(103,232,249,0.15);">\n    +\'<div style="font-size:9px;font-weight:700;letter-spacing:0.1em;color:#67e8f9;margin-bottom:8px;">📊 COMPOSIÇÃO'
)
html = html.replace(
    'display:flex;height:26px;border-radius:6px;overflow:hidden;margin-bottom:8px',
    'display:flex;height:20px;border-radius:5px;overflow:hidden;margin-bottom:6px'
)
applied.append("Barra Universe: 26px -> 20px")

# ── Relatório ──────────────────────────────────────────────────────────────────
for a in applied:
    print("OK:", a)

# ── Salvar ─────────────────────────────────────────────────────────────────────
DASH.write_text(html, encoding='utf-8')
versao = VER / f"Dashboard_Farma_Sul_{ts}_CompactUF.html"
shutil.copy(DASH, versao)
print(f"\nVersao: {versao.name}")
dl = DL / f"Dashboard_FarmaSul_Giovano_{ts}.html"
shutil.copy(DASH, dl)
print(f"Downloads: {dl.name}")
print(f"Dashboard: {len(html):,} chars (delta {len(html)-orig:+,})")
print("DONE.")
