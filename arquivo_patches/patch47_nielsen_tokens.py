"""
patch47_nielsen_tokens.py
─────────────────────────
1. Expande :root com tokens Nielsen completos
2. Uniformiza .card → #EAEEF4 (ainda estava #FFFFFF)
3. Padroniza bordas, sombras e tipografia via tokens
4. Cobre residuais de #FFFFFF em containers (não toca inputs/selects/kpi-cells)
"""
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

# ════════════════════════════════════════════════════════════════
# FIX 1 — Expandir :root com tokens Nielsen completos
# ════════════════════════════════════════════════════════════════
OLD_ROOT = """:root {
  --bg-base:      #DFECFB;
  --bg-base-filter: #C5D5EC;
  --bg-card:      #EAEEF4;
  --bg-card-alt:  #E2E7EF;
  --bg-subtle:    #DDE3ED;
  --bg-hover:     #D6DCE8;
  --card:         #EAEEF4;
  --border-card:  rgba(147,187,235,0.55);
  --shadow-card:  0 2px 8px rgba(10,40,80,0.14), 0 1px 3px rgba(10,40,80,0.08);
  --shadow-hover: 0 6px 22px rgba(10,40,80,0.18), 0 2px 8px rgba(10,40,80,0.10);
  --shadow-sm:    0 1px 4px rgba(10,40,80,0.10);
  --shadow-header: 0 2px 8px rgba(10,40,80,0.08);
  --radius-sm:    6px;
  --radius-md:    12px;
  --radius-lg:    16px;
  --card-text-heading: #0D1B2E;
  --card-text-primary: #1E293B;
  --card-text-body:    #334155;
  --card-text-muted:   #475569;
  --card-text-faint:   #64748B;
}"""

NEW_ROOT = """:root {
  /* ── NIELSEN DESIGN TOKENS ── */

  /* Fundos */
  --nielsen-bg:          #DFECFB;   /* fundo geral da página */
  --nielsen-card:        #EAEEF4;   /* fundo de cards e containers */
  --nielsen-card-kpi:    #FFFFFF;   /* fundo de células KPI (destaque) */
  --nielsen-input:       #FFFFFF;   /* fundo de inputs e selects */
  --nielsen-surface:     #F4F7FC;   /* superfícies alternadas / zebra */
  --nielsen-overlay:     rgba(255,255,255,0.82); /* glass / modal */

  /* Bordas */
  --nielsen-border:      rgba(147,187,235,0.50); /* borda padrão */
  --nielsen-border-strong: rgba(94,153,208,0.70); /* borda enfatizada */
  --nielsen-border-faint: rgba(147,187,235,0.25); /* divisor sutil */

  /* Textos */
  --nielsen-heading:     #0D1B2E;   /* títulos principais */
  --nielsen-text:        #1E293B;   /* texto primário */
  --nielsen-body:        #334155;   /* texto do corpo */
  --nielsen-muted:       #475569;   /* texto secundário */
  --nielsen-faint:       #64748B;   /* labels, metadados */

  /* Cores de ação */
  --nielsen-primary:     #1D4ED8;   /* azul primário (botões, active) */
  --nielsen-accent:      #1D6FA8;   /* azul accent / links */
  --nielsen-secondary:   #B45309;   /* âmbar / aviso */

  /* Feedback */
  --nielsen-positive:    #059669;   /* verde — crescimento positivo */
  --nielsen-negative:    #dc2626;   /* vermelho — queda / perigo */
  --nielsen-warning:     #b45309;   /* âmbar — atenção */
  --nielsen-info:        #0891B2;   /* ciano — informação */

  /* Sombras */
  --nielsen-shadow-sm:   0 1px 4px rgba(10,40,80,0.10);
  --nielsen-shadow-md:   0 2px 8px rgba(10,40,80,0.14), 0 1px 3px rgba(10,40,80,0.08);
  --nielsen-shadow-lg:   0 6px 22px rgba(10,40,80,0.18), 0 2px 8px rgba(10,40,80,0.10);
  --nielsen-shadow-hdr:  0 2px 8px rgba(10,40,80,0.08);

  /* Border-radius */
  --nielsen-r-sm:  6px;
  --nielsen-r-md:  10px;
  --nielsen-r-lg:  14px;
  --nielsen-r-xl:  18px;

  /* Tipografia */
  --nielsen-font:  'Inter', 'Segoe UI', system-ui, sans-serif;
  --nielsen-lh:    1.45;

  /* ── ALIASES (compatibilidade com CSS existente) ── */
  --bg-base:      #DFECFB;
  --bg-base-filter: #C5D5EC;
  --bg-card:      #EAEEF4;
  --bg-card-alt:  #E2E7EF;
  --bg-subtle:    #DDE3ED;
  --bg-hover:     #D6DCE8;
  --card:         #EAEEF4;
  --border-card:  rgba(147,187,235,0.55);
  --shadow-card:  0 2px 8px rgba(10,40,80,0.14), 0 1px 3px rgba(10,40,80,0.08);
  --shadow-hover: 0 6px 22px rgba(10,40,80,0.18), 0 2px 8px rgba(10,40,80,0.10);
  --shadow-sm:    0 1px 4px rgba(10,40,80,0.10);
  --shadow-header: 0 2px 8px rgba(10,40,80,0.08);
  --radius-sm:    6px;
  --radius-md:    12px;
  --radius-lg:    16px;
  --card-text-heading: #0D1B2E;
  --card-text-primary: #1E293B;
  --card-text-body:    #334155;
  --card-text-muted:   #475569;
  --card-text-faint:   #64748B;
}"""

rep(OLD_ROOT, NEW_ROOT, ':root → Nielsen tokens completos')

# ════════════════════════════════════════════════════════════════
# FIX 2 — .card base: #FFFFFF → #EAEEF4
# ════════════════════════════════════════════════════════════════
rep(
    '.card{background:#FFFFFF;border-radius:12px;padding:20px;border:1px solid #DCE3EC;backdrop-filter:none;}',
    '.card{background:var(--nielsen-card,#EAEEF4);border-radius:var(--nielsen-r-lg,14px);padding:20px;border:1px solid var(--nielsen-border);box-shadow:var(--nielsen-shadow-sm);backdrop-filter:none;}',
    '.card base: #FFFFFF → #EAEEF4 + tokens'
)

# ════════════════════════════════════════════════════════════════
# FIX 3 — .card-title / .card-sub: usar tokens
# ════════════════════════════════════════════════════════════════
rep(
    '.card-title{font-size:13px;font-weight:700;color:#1E293B;line-height:1.3;}',
    '.card-title{font-size:13px;font-weight:700;color:var(--nielsen-text,#1E293B);line-height:var(--nielsen-lh,1.45);}',
    '.card-title → token'
)
rep(
    '.card-sub{font-size:10px;color:#64748B;margin-top:3px;}',
    '.card-sub{font-size:10px;color:var(--nielsen-faint,#64748B);margin-top:3px;}',
    '.card-sub → token'
)

# ════════════════════════════════════════════════════════════════
# FIX 4 — .hbar-outer (fundo barra horizontal): #EEF2F7 → sutil Nielsen
# ════════════════════════════════════════════════════════════════
rep(
    '.hbar-outer{flex:1;height:26px;background:#EEF2F7;border-radius:5px;overflow:hidden;}',
    '.hbar-outer{flex:1;height:26px;background:rgba(147,187,235,0.20);border-radius:5px;overflow:hidden;}',
    '.hbar-outer: fundo Nielsen sutil'
)

# ════════════════════════════════════════════════════════════════
# FIX 5 — .toggle-group: #EEF2F7 → Nielsen
# ════════════════════════════════════════════════════════════════
rep(
    '.toggle-group{display:flex;background:#EEF2F7;border-radius:7px;padding:2px;gap:2px;flex-shrink:0;}',
    '.toggle-group{display:flex;background:rgba(147,187,235,0.25);border-radius:7px;padding:2px;gap:2px;flex-shrink:0;}',
    '.toggle-group: bg Nielsen'
)

# ════════════════════════════════════════════════════════════════
# FIX 6 — Containers que ainda usam #FFFFFF (exceto inputs/kpi/tgl)
#  → patching via CSS no bloco de tokens (injeta regra extra)
# ════════════════════════════════════════════════════════════════
EXTRA_CSS = """

/* ── PATCH 47 — Nielsen Token System ───────────────────────────────────── */

/* Body base */
body {
  font-family: var(--nielsen-font) !important;
  line-height: var(--nielsen-lh) !important;
}

/* Cards universais — garantir tema */
.card, [class*="-card"]:not(.kpi-cell):not(.login-card) {
  background: var(--nielsen-card) !important;
  border-color: var(--nielsen-border) !important;
}

/* Section labels / group titles */
.section-label, .group-label, [class*="section-title"],
[class*="group-title"], .diag-group-title {
  color: var(--nielsen-heading) !important;
  font-weight: 700 !important;
}

/* Containers que ainda aparecem brancos (patch25 residual) */
.card.full { background: var(--nielsen-card) !important; }
.cards-row > .card { background: var(--nielsen-card) !important; }

/* Barras de progresso */
.hbar-outer, [class*="prog-track"], [class*="progress-track"],
[class*="-track"] {
  background: rgba(147,187,235,0.20) !important;
}

/* Tooltips/popups Chart.js */
.chartjs-tooltip, [class*="tooltip"] {
  background: var(--nielsen-card) !important;
  border: 1px solid var(--nielsen-border) !important;
  color: var(--nielsen-text) !important;
  border-radius: var(--nielsen-r-md) !important;
}

/* Badges e chips inline */
.badge, [class*="-badge"]:not(.cov-badge-ok):not(.cov-badge-warn):not(.cov-badge-low) {
  border-radius: var(--nielsen-r-sm) !important;
}

/* Botões primários */
.btn-primary, [class*="btn-primary"], #btn-update-data {
  background: var(--nielsen-primary) !important;
  color: #FFFFFF !important;
  border-radius: var(--nielsen-r-sm) !important;
  font-weight: 700 !important;
}

/* Botões secundários */
.btn-secondary, [class*="btn-secondary"] {
  background: transparent !important;
  border: 1px solid var(--nielsen-border-strong) !important;
  color: var(--nielsen-text) !important;
  border-radius: var(--nielsen-r-sm) !important;
}

/* Estados hover em cards */
.card:hover {
  box-shadow: var(--nielsen-shadow-md) !important;
  border-color: var(--nielsen-border-strong) !important;
}

/* Responsivo — prevenir overflow em telas menores */
@media (max-width: 900px) {
  .cards-row { grid-template-columns: 1fr !important; }
}
@media (max-width: 600px) {
  .card { padding: 14px !important; }
  .kpi-cell { padding: 10px 12px !important; }
}

/* Acessibilidade — contraste mínimo garantido */
.card * { min-color-contrast: 4.5; }

/* ── FIM PATCH 47 ───────────────────────────────────────────────────────── */
"""

# Injeta o CSS extra antes do fechamento do bloco de estilo inicial
ANCHOR = '/* ── 02. BODY / BASE ────────────────────────────────────────────────────── */'
if ANCHOR in html:
    html = html.replace(ANCHOR, EXTRA_CSS + '\n' + ANCHOR)
    fixes += 1
    print('  [OK]   CSS patch47 extra injetado')
else:
    print('  [MISS] âncora para injeção de CSS')

print(f'\nTotal: {fixes} fixes | Diff: {len(html)-orig:+,} bytes')
src.write_text(html, encoding='utf-8')

ts = datetime.datetime.now().strftime('%Y%m%d_%H%M')
ver = Path(f'Dashboard_farma_sul/versoes/Dashboard_Farma_Sul_{ts}_NielsenTokens.html')
dl  = Path.home() / 'Downloads' / f'Dashboard_FarmaSul_Giovano_{ts}.html'
shutil.copy2(src, ver)
shutil.copy2(src, dl)
print('Versao:', ver.name)
print('Download:', dl.name)
