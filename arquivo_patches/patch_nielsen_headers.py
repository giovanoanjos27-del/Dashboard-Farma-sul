"""
patch_nielsen_headers.py
Padroniza headers, selects e KPI chips de todos os cards Nielsen
para igualar o estilo do card MSO1 (referência).

Hierarquia adotada (igual MSO2/MSO3 premium):
  Label:  9px · 700 · letter-spacing:.18em · uppercase · color accent
  Título: 15px · 700 · color:#f1f5f9
  Sub:    11px · color:#475569

NÃO altera: dados, arrays, funções JS, gráficos, cálculos.
"""

import shutil, re
from datetime import datetime

SRC  = r"C:\Users\valqu\OneDrive\Documentos\Claude\Projects\projeto Dashboard_farma_sul\Dashboard_farma_sul\Dashboard_Farma_Sul_20260512_2220.html"
VERS_DIR = r"C:\Users\valqu\OneDrive\Documentos\Claude\Projects\projeto Dashboard_farma_sul\Dashboard_farma_sul\versoes"
DL_DIR   = r"C:\Users\valqu\Downloads"

ts   = datetime.now().strftime('%Y%m%d_%H%M')
VERS = fr"{VERS_DIR}\Dashboard_Farma_Sul_{ts}_NielsenHeaders.html"
DL   = fr"{DL_DIR}\Dashboard_FarmaSul_Giovano_{ts}.html"

with open(SRC, 'r', encoding='utf-8') as f:
    html = f.read()

ok = []
err = []

def rep(old, new, label):
    global html
    if old in html:
        html = html.replace(old, new, 1)
        ok.append(label)
    else:
        err.append(label)

# ─── SELECT style padrão (amber) ───────────────────────────────────────────
SEL_STD = ('background:#161B22;color:#e2e8f0;'
           'border:0.5px solid rgba(251,191,36,0.3);'
           'border-radius:7px;padding:6px 28px 6px 10px;'
           'font-size:11px;cursor:pointer;font-family:inherit;'
           'appearance:none;-webkit-appearance:none;'
           'background-image:url("data:image/svg+xml,%3Csvg xmlns=\'http://www.w3.org/2000/svg\' width=\'10\' height=\'6\'%3E%3Cpath d=\'M0 0l5 6 5-6z\' fill=\'%23fbbf24\'/%3E%3C/svg%3E");'
           'background-repeat:no-repeat;background-position:right 10px center')

# ─── LABEL STYLE helpers ────────────────────────────────────────────────────
def lbl(color, text):
    return (f'<div style="font-size:9px;font-weight:700;letter-spacing:.18em;'
            f'color:{color};text-transform:uppercase;margin-bottom:5px;">{text}</div>')

def ttl(text):
    return f'<div style="font-size:15px;font-weight:700;color:#f1f5f9;line-height:1.2;">{text}</div>'

def sub(text, id_=''):
    id_attr = f' id="{id_}"' if id_ else ''
    return f'<div{id_attr} style="font-size:11px;color:#475569;margin-top:3px;">{text}</div>'

# ════════════════════════════════════════════════════════════════════════════
# 1. PERFORMANCE POR REGIÃO — header
# ════════════════════════════════════════════════════════════════════════════
rep(
    '      <div style="font-size:13px;font-weight:800;color:#a5b4fc;letter-spacing:.5px;">📍 PERFORMANCE POR REGIÃO &mdash; FYTD JUL&ndash;MAR</div>\n'
    '      <div id="reg-perf-sub" style="font-size:11px;color:#94A3B8;margin-top:2px;">Vendas Total Mercado R$MM &middot; Contribuição Δ Share por Marca</div>',

    '      ' + lbl('#a5b4fc', 'PERFORMANCE POR REGIÃO — FYTD JUL–MAR') + '\n'
    '      ' + ttl('Vendas Total Mercado R$MM · Δ Share por Marca') + '\n'
    '      ' + sub('NielsenIQ · 72 Mercados · Jul/25–Mar/26', 'reg-perf-sub'),
    'RegPerf header'
)

# Selects do RegPerf — padronizar
rep(
    'style="background:#161B22;color:#e2e8f0;border:1px solid rgba(99,102,241,0.35);border-radius:8px;padding:5px 10px;font-size:11px;cursor:pointer;">',
    f'style="{SEL_STD}">',
    'RegPerf select grupo'
)
rep(
    'style="background:#161B22;color:#fbbf24;border:1px solid rgba(251,191,36,0.35);border-radius:8px;padding:5px 10px;font-size:11px;cursor:pointer;">',
    f'style="{SEL_STD}">',
    'RegPerf select brand'
)

# ════════════════════════════════════════════════════════════════════════════
# 2. MARKET SHARE POR SKU — header
# ════════════════════════════════════════════════════════════════════════════
rep(
    '      <div style="font-size:13px;font-weight:800;color:#fbbf24;letter-spacing:.5px;">📦 MARKET SHARE POR SKU — FYTD26</div>\n'
    '      <div id="sku-shr-sub" style="font-size:11px;color:#94A3B8;margin-top:2px;">Share por SKU · FYTD26 vs FYTD25 · Personal Repellent</div>',

    '      ' + lbl('#fbbf24', 'MARKET SHARE POR SKU — FYTD26') + '\n'
    '      ' + ttl('$ Share por SKU · FYTD26 vs FYTD25') + '\n'
    '      ' + sub('Personal Repellent · NielsenIQ', 'sku-shr-sub'),
    'SKU Share header'
)

# Select SKU Share
rep(
    'style="background:#161B22;color:#e2e8f0;border:1px solid rgba(234,179,8,0.22);border-radius:8px;padding:6px 12px;font-size:12px;cursor:pointer;">\n'
    '      <option value="T.BR Farma">T.BR Farma</option>\n'
    '      <option value="Farma Sul">Farma Sul</option>\n'
    '      <option value="INFC Sul">INFC Sul</option>',

    f'style="{SEL_STD}">\n'
    '      <option value="T.BR Farma">T.BR Farma</option>\n'
    '      <option value="Farma Sul">Farma Sul</option>\n'
    '      <option value="INFC Sul">INFC Sul</option>',
    'SKU select'
)

# ════════════════════════════════════════════════════════════════════════════
# 3. SHARE MENSAL POR MARCA — header
# ════════════════════════════════════════════════════════════════════════════
rep(
    '      <div style="font-size:13px;font-weight:800;color:#fbbf24;letter-spacing:.5px;">📈 SHARE MENSAL POR MARCA</div>\n'
    '      <div id="shr-trend-sub" style="font-size:11px;color:#94A3B8;margin-top:2px;">Série mensal por marca · Personal Repellent</div>',

    '      ' + lbl('#fbbf24', 'SHARE MENSAL POR MARCA') + '\n'
    '      ' + ttl('Evolução mensal de $ Share · FY24 · FY25 · FY26') + '\n'
    '      ' + sub('Personal Repellent · NielsenIQ', 'shr-trend-sub'),
    'ShrTrend header'
)

# Select ShrTrend
rep(
    'style="background:#161B22;color:#e2e8f0;border:1px solid rgba(234,179,8,0.22);border-radius:8px;padding:6px 12px;font-size:12px;cursor:pointer;">\n'
    '              <optgroup label="── Total Brasil ──">',

    f'style="{SEL_STD}">\n'
    '              <optgroup label="── Total Brasil ──">',
    'ShrTrend select'
)

# ════════════════════════════════════════════════════════════════════════════
# 4. ODOR BLOCK section separator
# ════════════════════════════════════════════════════════════════════════════
rep(
    '    <div style="font-size:10px;font-weight:700;letter-spacing:0.12em;color:#fbbf24;margin-bottom:14px;">\n'
    '      🧴 ODOR BLOCK — ANÁLISE NIELSEN · PATO BLOCK vs MARCAS\n'
    '    </div>',

    '    <div style="margin-bottom:18px;">\n'
    '      <div style="font-size:9px;font-weight:700;letter-spacing:.18em;color:#fbbf24;text-transform:uppercase;margin-bottom:5px;">ODOR BLOCK — ANÁLISE NIELSEN</div>\n'
    '      <div style="font-size:15px;font-weight:700;color:#f1f5f9;line-height:1.2;">Pato Block vs Marcas · Participação em Valor e Preço</div>\n'
    '    </div>',
    'OdorBlock section header'
)

# ════════════════════════════════════════════════════════════════════════════
# 5. DIAGNÓSTICO GERAL — header + card bg
# ════════════════════════════════════════════════════════════════════════════

# Upgrade card container (gradient → #0D1117 dark)
rep(
    'id="diag-geral-card" style="background:linear-gradient(135deg,#0f1e38 0%,#1F2937 100%);border:1px solid rgba(251,191,36,0.25);border-radius:14px;padding:24px 28px;margin:16px 0;"',
    'id="diag-geral-card" style="background:#0D1117;border:1.5px solid rgba(251,191,36,0.35);border-radius:14px;padding:20px 24px;margin:16px 0;"',
    'DiagGeral card bg'
)

# Header text
rep(
    '      <div style="font-size:13px;font-weight:800;color:#fbbf24;letter-spacing:.5px;">🧠 DIAGNÓSTICO GERAL — PERSONAL REPELLENT · NielsenIQ</div>\n'
    '      <div style="font-size:10px;color:#94A3B8;margin-top:3px;">Análise estratégica por marca e mercado · FYTD26 vs FYTD25 · Recomendações para ganho/manutenção de share</div>',

    '      ' + lbl('#fbbf24', 'DIAGNÓSTICO GERAL — PERSONAL REPELLENT') + '\n'
    '      ' + ttl('Análise Estratégica por Marca e Mercado') + '\n'
    '      <div style="font-size:11px;color:#475569;margin-top:3px;">FYTD26 vs FYTD25 · NielsenIQ · Recomendações para ganho/manutenção de share</div>',
    'DiagGeral header'
)

# Select DiagGeral
rep(
    'style="background:#161B22;color:#e2e8f0;border:1px solid rgba(251,191,36,0.35);border-radius:8px;padding:6px 14px;font-size:12px;cursor:pointer;">\n'
    '        <option value="T.BR Farma">T.BR Farma</option>\n'
    '        <option value="Farma Sul">Farma Sul</option>\n'
    '        <option value="INFC Sul">INFC Sul</option>',

    f'style="{SEL_STD}">\n'
    '        <option value="T.BR Farma">T.BR Farma</option>\n'
    '        <option value="Farma Sul">Farma Sul</option>\n'
    '        <option value="INFC Sul">INFC Sul</option>',
    'DiagGeral select'
)

# ════════════════════════════════════════════════════════════════════════════
# 6. CSS additions — KPI chips dos cards não-.card.full
# ════════════════════════════════════════════════════════════════════════════

CSS_ADD = """
/* ── Nielsen: KPI chips nos cards dinâmicos — igual MSO1 ── */
#panel-nielsen #reg-perf-kpis > div {
  background: #161B22 !important;
  border-radius: 10px !important;
  padding: 12px 14px !important;
  border: 0.5px solid rgba(255,255,255,0.05) !important;
}
/* SKU diagnóstico */
#panel-nielsen #sku-diagnostico {
  border-radius: 10px !important;
  border: 0.5px solid rgba(251,191,36,0.18) !important;
  background: rgba(251,191,36,0.04) !important;
}
/* ShrTrend diagnóstico */
#panel-nielsen #shr-diagnostico {
  border-radius: 10px !important;
  border: 0.5px solid rgba(251,191,36,0.18) !important;
  background: rgba(251,191,36,0.04) !important;
}
/* ShrTrend brand filter buttons */
#panel-nielsen #shr-brand-filters button {
  border-radius: 6px !important;
  font-size: 11px !important;
  font-weight: 700 !important;
  padding: 5px 12px !important;
  cursor: pointer !important;
}
/* Legenda ShrTrend — cor padronizada */
#panel-nielsen #shr-trend > div[style*="margin-top:10px"] {
  font-size: 10px !important;
  color: #64748b !important;
}
/* RegPerf KPI sub-labels */
#panel-nielsen #reg-perf-kpis > div > div:first-child {
  font-size: 9px !important;
  font-weight: 700 !important;
  letter-spacing: .1em !important;
  text-transform: uppercase !important;
  color: #3d6b63 !important;
  margin-bottom: 4px !important;
}
/* Tabela titles inside cards */
#panel-nielsen .card.full > div > div[style*="font-size:9px"][style*="font-weight:700"][style*="letter-spacing"] {
  color: #64748b !important;
  letter-spacing: .1em !important;
}
/* Diagnóstico Geral */
#panel-nielsen #diag-geral-card > div:first-child {
  margin-bottom: 16px !important;
  padding-bottom: 12px !important;
  border-bottom: 0.5px solid rgba(255,255,255,0.06) !important;
}
"""

INJECT = '.mso2-tc:first-child{text-align:left;padding-left:4px;}'
if INJECT in html:
    html = html.replace(INJECT, INJECT + CSS_ADD, 1)
    ok.append('CSS KPI chips + misc adicionado')
else:
    # fallback: já foi injetado antes — tentar após NielsenStd block
    INJECT2 = '/* ── Nielsen: KPI chips nos cards dinâmicos — igual MSO1 ── */'
    if INJECT2 not in html:
        # inject before </style>
        idx = html.find('</style>')
        if idx > 0:
            html = html[:idx] + CSS_ADD + html[idx:]
            ok.append('CSS adicionado (fallback)</style>)')

# ════════════════════════════════════════════════════════════════════════════
# SAVE
# ════════════════════════════════════════════════════════════════════════════
with open(SRC, 'w', encoding='utf-8') as f:
    f.write(html)

shutil.copy2(SRC, VERS)
shutil.copy2(SRC, DL)

print()
print("=" * 58)
print("NIELSEN HEADERS PATCH — RESULTADO")
print("=" * 58)
for c in ok:
    print(f"  OK   {c}")
for c in err:
    print(f"  MISS {c}")
print()
print(f"  Versao: {VERS.split(chr(92))[-1]}")
print(f"  DL:     {DL.split(chr(92))[-1]}")
print("=" * 58)
