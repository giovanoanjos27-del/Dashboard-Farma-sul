"""
patch_nielsen_standardize.py
Padronização visual completa do painel Nielsen Farma Sul.
Versão alvo: NielsenStd (2026-05-15)

O QUE FAZ:
  1. Injeta bloco CSS premium-dark com escopo #panel-nielsen
  2. Adiciona data-attributes nos cards antigos (AvgPrice, OB1/2/3)
  3. Faz upgrade de background/border em RegPerf, SKU Share, ShrTrend
  4. Salva versão + cópia Downloads

O QUE NÃO TOCA:
  - Dados, arrays, cálculos
  - Funções JS de renderização
  - Filtros/selects de mercado
  - Gráficos e canvas
"""

import re, shutil
from datetime import datetime

SRC  = r"C:\Users\valqu\OneDrive\Documentos\Claude\Projects\projeto Dashboard_farma_sul\Dashboard_farma_sul\Dashboard_Farma_Sul_20260512_2220.html"
VERS_DIR = r"C:\Users\valqu\OneDrive\Documentos\Claude\Projects\projeto Dashboard_farma_sul\Dashboard_farma_sul\versoes"
DL_DIR   = r"C:\Users\valqu\Downloads"

ts   = datetime.now().strftime('%Y%m%d_%H%M')
VERS = fr"{VERS_DIR}\Dashboard_Farma_Sul_{ts}_NielsenStd.html"
DL   = fr"{DL_DIR}\Dashboard_FarmaSul_Giovano_{ts}.html"

with open(SRC, 'r', encoding='utf-8') as f:
    html = f.read()

changes = []

# ══════════════════════════════════════════════════════════════════
# 1. CSS INJECTION — após .mso2-tc:first-child (linha ~603)
# ══════════════════════════════════════════════════════════════════

CSS_BLOCK = """
/* ════════════════════════════════════════════════════════
   NIELSEN PANEL — Padronização Visual v1.0 · 2026-05-15
   Scope: #panel-nielsen · Não altera dados/lógica.
   ════════════════════════════════════════════════════════ */

/* Premium dark para todos .card.full no painel Nielsen */
#panel-nielsen .card.full {
  background: #0D1117 !important;
  border: 1.5px solid rgba(251,191,36,0.35) !important;
  border-radius: 14px !important;
}

/* Card header: padding padrão + borda inferior sutil */
#panel-nielsen .card.full .card-header {
  padding: 16px 24px 12px !important;
  border-bottom: 0.5px solid rgba(255,255,255,0.06) !important;
  background: transparent !important;
  margin-bottom: 16px !important;
}

/* Card title e subtitle — hierarquia tipográfica uniforme */
#panel-nielsen .card.full .card-title {
  font-size: 14px !important;
  font-weight: 700 !important;
  color: #F1F5F9 !important;
  line-height: 1.3 !important;
}
#panel-nielsen .card.full .card-sub {
  font-size: 10px !important;
  color: #64748b !important;
  margin-top: 3px !important;
}

/* Odor Block — accent colors por data-ob */
#panel-nielsen .card.full[data-ob="1"] { border-color: rgba(96,165,250,0.45) !important; }
#panel-nielsen .card.full[data-ob="2"] { border-color: rgba(45,212,191,0.45) !important; }
#panel-nielsen .card.full[data-ob="3"] { border-color: rgba(52,211,153,0.45) !important; }

/* AvgPrice — accent verde */
#panel-nielsen .card.full[data-accent="green"] { border-color: rgba(52,211,153,0.45) !important; }

/* OB cards: selects com accent color matching */
#panel-nielsen .card.full[data-ob="1"] .card-header select {
  border: 1px solid rgba(96,165,250,0.35) !important;
}
#panel-nielsen .card.full[data-ob="2"] .card-header select {
  border: 1px solid rgba(45,212,191,0.35) !important;
}
#panel-nielsen .card.full[data-ob="3"] .card-header select {
  border: 0.5px solid rgba(52,211,153,0.3) !important;
}
#panel-nielsen .card.full[data-accent="green"] .card-header select {
  border: 0.5px solid rgba(52,211,153,0.3) !important;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='10' height='6'%3E%3Cpath d='M0 0l5 6 5-6z' fill='%2334d399'/%3E%3C/svg%3E") !important;
}

/* Select dropdowns padrão nas old-style cards */
#panel-nielsen .card.full[data-accent="amber"] .card-header select,
#panel-nielsen .card.full:not([data-ob]):not([data-accent]) .card-header select {
  font-size: 11px !important;
  padding: 6px 28px 6px 10px !important;
  border-radius: 7px !important;
  background: #161B22 !important;
  color: #e2e8f0 !important;
  border: 0.5px solid rgba(251,191,36,0.3) !important;
  appearance: none !important;
  -webkit-appearance: none !important;
}

/* KPI chips uniformes — altura mínima 72px */
#panel-nielsen #mso-kpis > div {
  background: #161B22 !important;
  border-radius: 10px !important;
  padding: 12px 14px !important;
}
#panel-nielsen #ob-share-kpis > div,
#panel-nielsen #ob-preco-kpis > div {
  min-height: 68px;
}

/* Diagnóstico blocks */
#panel-nielsen #ob-share-diag,
#panel-nielsen #ob-preco-diag,
#panel-nielsen #ob-mkt-diag {
  border-radius: 10px !important;
}
#panel-nielsen #avg-insight,
#panel-nielsen #mso-insight {
  border-radius: 10px !important;
}

/* RegPerf, SKU, ShrTrend — dark upgrade + border-radius uniforme */
#panel-nielsen #reg-perf-card {
  background: #0D1117 !important;
  border-radius: 14px !important;
}
#panel-nielsen #sku-shr-card {
  background: #0D1117 !important;
  border: 1.5px solid rgba(251,191,36,0.45) !important;
  border-radius: 14px !important;
}
#panel-nielsen #shr-trend {
  background: #0D1117 !important;
  border: 1.5px solid rgba(251,191,36,0.45) !important;
  border-radius: 14px !important;
}

/* Diagnóstico Geral */
#panel-nielsen #diag-geral-card {
  border-radius: 14px !important;
}

/* Fonte footer — padronizar cor e borda */
#panel-nielsen .dash-footer {
  font-size: 9px;
  color: #3d4451;
}

/* Odor Block section separator — mais sutil */
#panel-nielsen > div[style*="border-top:1px solid rgba(251,191,36"] {
  border-top: 0.5px solid rgba(251,191,36,0.12) !important;
}

/* Toggle group padronizado */
#panel-nielsen .card.full .toggle-group {
  border-radius: 7px !important;
  overflow: hidden !important;
}
#panel-nielsen .card.full .tgl {
  font-size: 11px !important;
  padding: 5px 12px !important;
  border: none !important;
  cursor: pointer !important;
  font-family: inherit !important;
  font-weight: 600 !important;
  background: #161B22 !important;
  color: #D1D5DB !important;
}
#panel-nielsen .card.full .tgl.active {
  background: rgba(251,191,36,0.12) !important;
  color: #fbbf24 !important;
  font-weight: 700 !important;
}

/* Scrollbar dentro dos cards Nielsen */
#panel-nielsen .card.full ::-webkit-scrollbar { height: 3px; width: 3px; }
#panel-nielsen .card.full ::-webkit-scrollbar-thumb { background: rgba(251,191,36,0.2); border-radius: 2px; }
"""

INJECT_AFTER = '.mso2-tc:first-child{text-align:left;padding-left:4px;}'
if INJECT_AFTER in html:
    html = html.replace(INJECT_AFTER, INJECT_AFTER + CSS_BLOCK, 1)
    changes.append('CSS Nielsen Std block injetado após .mso2-tc:first-child')
else:
    # fallback: inject before first </style>
    idx = html.find('</style>')
    if idx > 0:
        html = html[:idx] + CSS_BLOCK + '\n' + html[idx:]
        changes.append('CSS Nielsen Std block injetado (fallback antes de </style>)')
    else:
        changes.append('❌ CSS injection point NOT found')

# ══════════════════════════════════════════════════════════════════
# 2. DATA-ATTRIBUTES nos cards antigos
# ══════════════════════════════════════════════════════════════════

# ─ AvgPrice (verde accent, 2 espaços de indent) ─
OLD_AVG = (
    '  <div class="card full" style="margin-bottom:14px;">\n'
    '    <div class="card-header">\n'
    '      <div>\n'
    '        <div style="font-size:10px;font-weight:700;letter-spacing:0.1em;color:#34d399;margin-bottom:4px;">'
    'PREÇO MÉDIO POR PRODUTO</div>'
)
NEW_AVG = (
    '  <div class="card full" style="margin-bottom:14px;" data-accent="green">\n'
    '    <div class="card-header">\n'
    '      <div>\n'
    '        <div style="font-size:10px;font-weight:700;letter-spacing:0.1em;color:#34d399;margin-bottom:4px;">'
    'PREÇO MÉDIO POR PRODUTO</div>'
)
if OLD_AVG in html:
    html = html.replace(OLD_AVG, NEW_AVG, 1)
    changes.append('AvgPrice: data-accent="green" adicionado')
else:
    changes.append('⚠ AvgPrice container: string não encontrada')

# ─ OB Card 1 (blue · 4 espaços indent) ─
OLD_OB1 = (
    '    <div class="card full" style="margin-bottom:14px;">\n'
    '      <div class="card-header">\n'
    '        <div>\n'
    '          <div style="font-size:10px;font-weight:700;letter-spacing:0.1em;color:#60a5fa;margin-bottom:4px;">'
    'MARKET SHARE OVERVIEW — PARTICIPAÇÃO EM VALOR</div>'
)
NEW_OB1 = (
    '    <div class="card full" style="margin-bottom:14px;" data-ob="1">\n'
    '      <div class="card-header">\n'
    '        <div>\n'
    '          <div style="font-size:10px;font-weight:700;letter-spacing:0.1em;color:#60a5fa;margin-bottom:4px;">'
    'MARKET SHARE OVERVIEW — PARTICIPAÇÃO EM VALOR</div>'
)
if OLD_OB1 in html:
    html = html.replace(OLD_OB1, NEW_OB1, 1)
    changes.append('OB Card 1: data-ob="1" adicionado')
else:
    changes.append('⚠ OB Card 1: string não encontrada')

# ─ OB Card 2 (teal · 4 espaços) ─
OLD_OB2 = (
    '    <div class="card full" style="margin-bottom:14px;">\n'
    '      <div class="card-header">\n'
    '        <div>\n'
    '          <div style="font-size:10px;font-weight:700;letter-spacing:0.1em;color:#2dd4bf;margin-bottom:4px;">'
    'PREÇO MÉDIO POR PRODUTO — ANÁLISE EM PREÇO MÉDIO UNIDADES</div>'
)
NEW_OB2 = (
    '    <div class="card full" style="margin-bottom:14px;" data-ob="2">\n'
    '      <div class="card-header">\n'
    '        <div>\n'
    '          <div style="font-size:10px;font-weight:700;letter-spacing:0.1em;color:#2dd4bf;margin-bottom:4px;">'
    'PREÇO MÉDIO POR PRODUTO — ANÁLISE EM PREÇO MÉDIO UNIDADES</div>'
)
if OLD_OB2 in html:
    html = html.replace(OLD_OB2, NEW_OB2, 1)
    changes.append('OB Card 2: data-ob="2" adicionado')
else:
    changes.append('⚠ OB Card 2: string não encontrada')

# ─ OB Card 3 (green · 4 espaços) ─
OLD_OB3 = (
    '    <div class="card full" style="margin-bottom:14px;">\n'
    '      <div class="card-header">\n'
    '        <div>\n'
    '          <div style="font-size:10px;font-weight:700;letter-spacing:0.1em;color:#34d399;margin-bottom:4px;">'
    'TAMANHO DO MERCADO — ODOR BLOCK</div>'
)
NEW_OB3 = (
    '    <div class="card full" style="margin-bottom:14px;" data-ob="3">\n'
    '      <div class="card-header">\n'
    '        <div>\n'
    '          <div style="font-size:10px;font-weight:700;letter-spacing:0.1em;color:#34d399;margin-bottom:4px;">'
    'TAMANHO DO MERCADO — ODOR BLOCK</div>'
)
if OLD_OB3 in html:
    html = html.replace(OLD_OB3, NEW_OB3, 1)
    changes.append('OB Card 3: data-ob="3" adicionado')
else:
    changes.append('⚠ OB Card 3: string não encontrada')

# ══════════════════════════════════════════════════════════════════
# 3. RegPerf, SKU, ShrTrend — upgrade background inline
# ══════════════════════════════════════════════════════════════════

# RegPerf: #161B22 → #0D1117 (manter border indigo)
old_reg = 'id="reg-perf-card" style="background:#161B22;border:1.5px solid rgba(99,102,241,0.55);'
new_reg = 'id="reg-perf-card" style="background:#0D1117;border:1.5px solid rgba(99,102,241,0.55);'
if old_reg in html:
    html = html.replace(old_reg, new_reg, 1)
    changes.append('RegPerf: background #161B22 → #0D1117')
else:
    changes.append('⚠ RegPerf container: string não encontrada')

# SKU Share: #161B22 → #0D1117, border solid #EAB308 → rgba suave
old_sku = 'id="sku-shr-card" style="background:#161B22;border:1.5px solid #EAB308;'
new_sku = 'id="sku-shr-card" style="background:#0D1117;border:1.5px solid rgba(251,191,36,0.45);'
if old_sku in html:
    html = html.replace(old_sku, new_sku, 1)
    changes.append('SKU Share: bg #0D1117 + border suavizado')
else:
    changes.append('⚠ SKU Share container: string não encontrada')

# ShrTrend: #161B22 → #0D1117, border solid #EAB308 → rgba suave
old_shr = 'id="shr-trend" style="background:#161B22;border:1.5px solid #EAB308;'
new_shr = 'id="shr-trend" style="background:#0D1117;border:1.5px solid rgba(251,191,36,0.45);'
if old_shr in html:
    html = html.replace(old_shr, new_shr, 1)
    changes.append('ShrTrend: bg #0D1117 + border suavizado')
else:
    changes.append('⚠ ShrTrend container: string não encontrada')

# ══════════════════════════════════════════════════════════════════
# 4. SALVAR
# ══════════════════════════════════════════════════════════════════

with open(SRC, 'w', encoding='utf-8') as f:
    f.write(html)

shutil.copy2(SRC, VERS)
shutil.copy2(SRC, DL)

print()
print("=" * 62)
print("NIELSEN STANDARDIZATION — RESULTADO")
print("=" * 62)
for c in changes:
    icon = '✅' if not c.startswith('⚠') and not c.startswith('❌') else c[:2]
    msg  = c[2:].strip() if c.startswith(('⚠','❌')) else c
    print(f"  {icon}  {msg}")
print()
print(f"  Principal : Dashboard_Farma_Sul_20260512_2220.html")
print(f"  Versão    : {VERS.split(chr(92))[-1]}")
print(f"  Downloads : {DL.split(chr(92))[-1]}")
print("=" * 62)
