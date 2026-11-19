"""
patch49_remove_panels.py
────────────────────────
Remove PERMANENTEMENTE os 3 painéis desativados:
  • panel-diagnostico  (HTML L2641-2667 + refs JS)
  • panel-plano        (HTML L32712-32996 incl. renderPlanoNegocios)
  • panel-expd         (HTML L32997-33139 + IIFE L33141-34068)

Remove também todas as referências nas funções switchClient, post-login e upload.
Mantém intactos: Script2 (UX improvements) e Script3 (Nielsen Excel Export).
"""
import sys, re, datetime, shutil
sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path

src = Path('Dashboard_farma_sul/Dashboard_Farma_Sul_20260512_2220.html')
html = src.read_text(encoding='utf-8')
orig_len = len(html)
orig_lines = html.count('\n')
fixes = []

def rep(old, new, label):
    c = html.count(old)
    if c == 0:
        print(f'  [MISS] {label}')
        return html
    result = html.replace(old, new)
    fixes.append((label, c))
    print(f'  [OK]   {label} ({c}x)')
    return result

# ══════════════════════════════════════════════════════════════════════
# BLOCO 1 — Remover HTML do panel-diagnostico (pequeno, 27 linhas)
# ══════════════════════════════════════════════════════════════════════
DIAG_START = '<div class="main" id="panel-diagnostico">'
DIAG_END   = '<div class="main" id="panel-sellin">'

if DIAG_START in html and DIAG_END in html:
    i_start = html.index(DIAG_START)
    i_end   = html.index(DIAG_END)
    removed = html[i_start:i_end]
    html = html[:i_start] + html[i_end:]
    fixes.append(('panel-diagnostico HTML', 1))
    print(f'  [OK]   panel-diagnostico HTML removido ({removed.count(chr(10))} linhas)')
else:
    print(f'  [MISS] panel-diagnostico HTML')

# ══════════════════════════════════════════════════════════════════════
# BLOCO 2 — Remover HTML+JS do panel-plano
# ══════════════════════════════════════════════════════════════════════
PLANO_START = '<div class="main" id="panel-plano">'
PLANO_END   = '<div class="main" id="panel-expd">'

if PLANO_START in html and PLANO_END in html:
    i_start = html.index(PLANO_START)
    i_end   = html.index(PLANO_END)
    removed = html[i_start:i_end]
    html = html[:i_start] + html[i_end:]
    fixes.append(('panel-plano HTML+JS', 1))
    print(f'  [OK]   panel-plano HTML+JS removido ({removed.count(chr(10))} linhas)')
else:
    print(f'  [MISS] panel-plano HTML+JS')

# ══════════════════════════════════════════════════════════════════════
# BLOCO 3 — Remover HTML do panel-expd + IIFE de renderExpandindoDist
# O HTML do div fecha antes de <script> (UX improvements vem depois)
# Removemos: <div class="main" id="panel-expd"> ... </script>\n\n<script>\n/* ═══ MELHORIAS UX
# ══════════════════════════════════════════════════════════════════════
EXPD_START = '<div class="main" id="panel-expd">'
EXPD_END   = '<script>\n/* ═══════════ MELHORIAS UX'

if EXPD_START in html and EXPD_END in html:
    i_start = html.index(EXPD_START)
    i_end   = html.index(EXPD_END)
    removed = html[i_start:i_end]
    html = html[:i_start] + html[i_end:]
    fixes.append(('panel-expd HTML + IIFE renderExpandindoDist', 1))
    print(f'  [OK]   panel-expd HTML+IIFE removido ({removed.count(chr(10))} linhas)')
else:
    print(f'  [MISS] panel-expd HTML+IIFE')

# ══════════════════════════════════════════════════════════════════════
# BLOCO 4 — Remover blocos else-if no post-login (doLogin)
# ══════════════════════════════════════════════════════════════════════
# Bloco diagnostico
html = rep(
    "        } else if(_ap==='diagnostico'){\n"
    "          if(typeof initialized!=='undefined') delete initialized['diagnostico'];\n"
    "          if(typeof initDiagnostico==='function') initDiagnostico();\n"
    "        } else if(_ap==='plano'){\n"
    "          if(typeof renderPlanoNegocios==='function') renderPlanoNegocios();\n"
    "        } else if(_ap==='expd'){\n"
    "          if(typeof window.__resetExpandindoDist==='function') window.__resetExpandindoDist();\n"
    "          if(typeof renderExpandindoDist==='function') renderExpandindoDist(true);\n"
    "        } else {",
    "        } else {",
    'post-login else-if diagnostico/plano/expd'
)

# ══════════════════════════════════════════════════════════════════════
# BLOCO 5 — Remover else-if no switchClient
# ══════════════════════════════════════════════════════════════════════
html = rep(
    "      else if(id==='diagnostico') initDiagnostico();\n"
    "      else if(id==='plano') renderPlanoNegocios();\n"
    "      else if(id==='expd') renderExpandindoDist();\n",
    "",
    'switchClient else-if diagnostico/plano/expd'
)

# ══════════════════════════════════════════════════════════════════════
# BLOCO 6 — Remover blocos no upload/re-render
# ══════════════════════════════════════════════════════════════════════
html = rep(
    "          } else if(_ap === 'diagnostico'){\n"
    "            delete initialized['diagnostico'];\n"
    "            if(typeof initDiagnostico === 'function') initDiagnostico();\n"
    "            console.log('[upload] Diagnóstico re-renderizado');\n",
    "",
    'upload re-render diagnostico'
)
html = rep(
    "          } else if(_ap === 'plano'){\n"
    "            if(typeof renderPlanoNegocios === 'function') renderPlanoNegocios();\n"
    "            console.log('[upload] Plano Negócios re-renderizado');\n"
    "\n"
    "          } else if(_ap === 'expd'){\n"
    "            /* _e2Inited é local da IIFE — usar helper exposto no window */\n"
    "            if(typeof window.__resetExpandindoDist === 'function') window.__resetExpandindoDist();\n"
    "            if(typeof renderExpandindoDist === 'function') renderExpandindoDist(true);\n"
    "            console.log('[upload] Expandindo Dist. re-renderizado');\n"
    "          }",
    "          }",
    'upload re-render plano+expd'
)

# ══════════════════════════════════════════════════════════════════════
# BLOCO 7 — Remover CSS residual dos 3 painéis
# ══════════════════════════════════════════════════════════════════════
# Patch 48 display:none
html = rep(
    "/* ── PATCH 48 — Ocultar painéis removidos (27/05/2026) ─────────────────── */\n"
    "#panel-diagnostico,\n"
    "#panel-plano,\n"
    "#panel-expd { display: none !important; }\n"
    "/* ── FIM PATCH 47/48 ────────────────────────────────────────────────────── */",
    "/* ── FIM PATCH 47 ───────────────────────────────────────────────────────── */",
    'CSS PATCH48 display:none (painéis já removidos)'
)

# CSS panel backgrounds em patch45 — remover referências aos 3 painéis removidos
html = rep(
    "#panel-ol         { background: var(--bg-base, #DFECFB) !important; min-height: 100vh; }\n"
    "#panel-sellin     { background: var(--bg-base, #DFECFB) !important; min-height: 100vh; }\n"
    "#panel-diagnostico,\n"
    "#panel-cobertura  { background: var(--bg-base, #DFECFB) !important; min-height: 100vh; }\n"
    "#panel-plano { background: var(--bg-base, #DFECFB) !important; }\n"
    "#panel-expd  { background: var(--bg-base, #DFECFB) !important; min-height: calc(100vh - 60px); }",
    "#panel-ol         { background: var(--bg-base, #DFECFB) !important; min-height: 100vh; }\n"
    "#panel-sellin     { background: var(--bg-base, #DFECFB) !important; min-height: 100vh; }\n"
    "#panel-cobertura  { background: var(--bg-base, #DFECFB) !important; min-height: 100vh; }",
    'CSS patch45 backgrounds: remover plano/expd/diagnostico'
)

# Remover comentário de abas removidas no ctabs
html = rep(
    "\n  <!-- abas Diagnóstico, Plano Negócios e Expandindo Dist. removidas a pedido 27/05/2026 -->",
    "",
    'comentário abas removidas no ctabs'
)

# ══════════════════════════════════════════════════════════════════════
# BLOCO 8 — Limpar array de painéis no CSS panel-saojoao-inner etc.
# ══════════════════════════════════════════════════════════════════════
# Remover panel-diagnostico/plano/expd de seletores CSS groupados
html = rep(
    "          panel-cobertura, panel-ol, panel-plano, panel-expd, panel-diagnostico",
    "          panel-cobertura, panel-ol",
    'CSS seletor agrupado: remover plano/expd/diagnostico'
)

html = rep(
    "#panel-diagnostico,\n"
    "#panel-cobertura  { background:",
    "#panel-cobertura  { background:",
    'CSS seletor agrupado diagnostico+cobertura'
)

html = rep(
    "#panel-sellin .card, #panel-diagnostico .card,\n"
    "#panel-cobertura .card, #panel-ol .card, #panel-plano .card, #panel-expd .card {",
    "#panel-sellin .card,\n"
    "#panel-cobertura .card, #panel-ol .card {",
    'CSS .card seletores: remover plano/expd/diagnostico'
)

html = rep(
    "#panel-sellin .card:hover, #panel-diagnostico .card:hover,\n"
    "#panel-cobertura .card:hover, #panel-ol .card:hover, #panel-plano .card:hover, #panel-expd .card:hover {",
    "#panel-sellin .card:hover,\n"
    "#panel-cobertura .card:hover, #panel-ol .card:hover {",
    'CSS .card:hover seletores: remover plano/expd/diagnostico'
)

html = rep(
    "#panel-sellin .kpi-cell, #panel-diagnostico .kpi-cell, #panel-cobertura .kpi-cell,",
    "#panel-sellin .kpi-cell, #panel-cobertura .kpi-cell,",
    'CSS .kpi-cell seletores: remover diagnostico'
)

html = rep(
    "#panel-diagnostico .toggle-group, #panel-cobertura .toggle-group,\n"
    "#panel-ol .toggle-group, #panel-plano .toggle-group, #panel-expd .toggle-group {",
    "#panel-cobertura .toggle-group,\n"
    "#panel-ol .toggle-group {",
    'CSS .toggle-group seletores: remover 3 painéis'
)

html = rep(
    "#panel-diagnostico .tgl.active, #panel-cobertura .tgl.active,\n"
    "#panel-ol .tgl.active, #panel-plano .tgl.active, #panel-expd .tgl.active {",
    "#panel-cobertura .tgl.active,\n"
    "#panel-ol .tgl.active {",
    'CSS .tgl.active seletores: remover 3 painéis'
)

html = rep(
    "#panel-sellin .stab, #panel-diagnostico .stab, #panel-cobertura .stab, #panel-ol .stab {",
    "#panel-sellin .stab, #panel-cobertura .stab, #panel-ol .stab {",
    'CSS .stab seletores: remover diagnostico'
)

html = rep(
    "#panel-diagnostico .stab.active, #panel-cobertura .stab.active, #panel-ol .stab.active {",
    "#panel-cobertura .stab.active, #panel-ol .stab.active {",
    'CSS .stab.active seletores: remover diagnostico'
)

html = rep(
    "#panel-sellin .section-label, #panel-diagnostico .section-label,\n"
    "#panel-cobertura .section-label, #panel-ol .section-label,\n"
    "#panel-plano .section-label, #panel-expd .section-label {",
    "#panel-sellin .section-label,\n"
    "#panel-cobertura .section-label, #panel-ol .section-label {",
    'CSS .section-label seletores: remover 3 painéis'
)

# ══════════════════════════════════════════════════════════════════════
# RESULTADO
# ══════════════════════════════════════════════════════════════════════
new_lines = html.count('\n')
print(f'\nLinhas removidas: {orig_lines - new_lines:,}')
print(f'Tamanho: {orig_len/1024/1024:.2f} MB → {len(html)/1024/1024:.2f} MB')
print(f'Redução: {(orig_len - len(html))/1024:.0f} KB')

src.write_text(html, encoding='utf-8')

ts = datetime.datetime.now().strftime('%Y%m%d_%H%M')
ver = Path(f'Dashboard_farma_sul/versoes/Dashboard_Farma_Sul_{ts}_PanelsRemoved.html')
dl  = Path.home() / 'Downloads' / f'Dashboard_FarmaSul_Giovano_{ts}.html'
shutil.copy2(src, ver)
shutil.copy2(src, dl)
print('Versao:', ver.name)
print('Download:', dl.name)
