"""
Patch Mobile Responsive — Dashboard Farma Sul
Injeta CSS para funcionamento em desktop e celular.
"""
import re
from datetime import datetime

SRC  = "Dashboard_farma_sul/Dashboard_Farma_Sul_20260512_2220.html"
VER_DIR = "Dashboard_farma_sul/versoes"

# ── CSS mobile a injetar ─────────────────────────────────────────────────────
MOBILE_CSS = """
/* ═══════════════════════════════════════════════════════════════════════
   MOBILE RESPONSIVE PATCH — Dashboard Farma Sul
   Breakpoints: 900px (tablet) · 768px (phone) · 480px (phone pequeno)
   ═══════════════════════════════════════════════════════════════════════ */

/* Scroll horizontal para tabelas em qualquer tela */
.tbl-scroll { overflow-x: auto; -webkit-overflow-scrolling: touch; }

/* ── TABLET (≤ 900px) ── */
@media (max-width: 900px) {
  .main     { padding: 14px 16px; }
  .header   { padding: 12px 16px 8px; }
  .ctabs    { padding: 0 16px; }
  .filters  { padding: 8px 16px; }
  .kpi-grid { grid-template-columns: repeat(3, 1fr); }
}

/* ── PHONE (≤ 768px) ── */
@media (max-width: 768px) {
  /* Layout base */
  .main            { padding: 10px 12px; }
  .header          { padding: 10px 12px 8px; }
  .header h1       { font-size: 16px; }
  .header-sub      { font-size: 10px; }
  .ctabs           { padding: 0 8px; }
  .ctab            { font-size: 11px; padding: 9px 10px; min-height: 40px; }
  .filters         { padding: 7px 12px; gap: 6px; }
  .main            { padding: 10px 12px; }

  /* Client selector */
  #sellout-client-selector { min-width: 0; width: 100%; }

  /* KPI: 3 colunas no phone */
  .kpi-grid  { grid-template-columns: repeat(3, 1fr); }
  .kpi-cell  { padding: 12px 10px; }
  .kpi-val   { font-size: 1.05rem; }
  .kpi-delta { font-size: 9px; }

  /* Cards sempre em coluna única */
  .cards-row { grid-template-columns: 1fr; gap: 10px; }

  /* Tabelas — scroll horizontal */
  #cpt2-wrap,
  .so-table-wrap,
  .nielsen-tbl-wrap,
  .u-tbl-outer,
  [id$="-tbl-wrap"],
  [id$="-table-outer"] {
    overflow-x: auto;
    -webkit-overflow-scrolling: touch;
  }

  /* Gráficos — scroll se ultrapassar container */
  .card { overflow-x: auto; }

  /* Layouts multi-coluna que devem colapsar */
  [class*="op1-row"],
  [class*="diag-row"],
  [class*="stat-row"],
  .kpi-row-inline {
    grid-template-columns: 1fr !important;
    flex-wrap: wrap !important;
  }

  /* Botões com alvo de toque maior */
  button, .btn-clear, select { min-height: 36px; }
}

/* ── PHONE PEQUENO (≤ 480px) ── */
@media (max-width: 480px) {
  .kpi-grid  { grid-template-columns: repeat(2, 1fr); }
  .kpi-val   { font-size: 0.9rem; }
  .kpi-tag   { font-size: 9px; }
  .kpi-cell  { padding: 10px 8px; }

  .header h1   { font-size: 14px; }
  .header-sub  { display: none; }

  .card        { padding: 14px 10px; }
  .section-label { font-size: 9px; }

  /* Filtros em coluna */
  .filters { flex-direction: column; align-items: flex-start; }
  .fsel, #sellout-client-selector { width: 100%; }

  /* Tabs: texto menor e rolagem fácil */
  .ctab { font-size: 10px; padding: 8px 9px; }
}
"""

# ── JS: wraps automático de tabelas grandes no DOM ───────────────────────────
MOBILE_JS = """
/* Mobile: wraps automático de tabelas largas */
(function(){
  function wrapTables(){
    document.querySelectorAll('table').forEach(function(t){
      var p = t.parentElement;
      if(p && p.style && !p.classList.contains('tbl-scroll')){
        var cs = window.getComputedStyle(p);
        if(cs.overflowX === 'auto' || cs.overflowX === 'scroll') return;
        var wrap = document.createElement('div');
        wrap.className = 'tbl-scroll';
        p.insertBefore(wrap, t);
        wrap.appendChild(t);
      }
    });
  }
  if(document.readyState === 'loading'){
    document.addEventListener('DOMContentLoaded', wrapTables);
  } else {
    wrapTables();
  }
  // Também executa após renders dinâmicos (tabs)
  setTimeout(wrapTables, 800);
  setTimeout(wrapTables, 2000);
})();
"""

def main():
    with open(SRC, encoding="utf-8") as f:
        html = f.read()

    original_len = len(html)

    # 1. Injeta CSS antes de </head>
    css_block = f"<style id='mobile-patch'>\n{MOBILE_CSS}\n</style>\n"
    if "id='mobile-patch'" in html:
        # re-injeta (substitui patch anterior)
        html = re.sub(
            r"<style id='mobile-patch'>.*?</style>",
            css_block.strip(),
            html, flags=re.DOTALL
        )
        print("CSS mobile: atualizado.")
    elif "</head>" in html:
        html = html.replace("</head>", css_block + "</head>", 1)
        print("CSS mobile: injetado antes de </head>.")
    else:
        # fallback: coloca antes do primeiro </style>
        html = html.replace("</style>", css_block + "</style>", 1)
        print("CSS mobile: injetado (fallback).")

    # 2. Wraps o cpt2-table em div scrollável (tabela estática)
    CPT2_FIND = '<table id="cpt2-table"'
    CPT2_END  = '</table>'
    if CPT2_FIND in html and 'id="cpt2-wrap"' not in html:
        idx_start = html.index(CPT2_FIND)
        idx_end   = html.index(CPT2_END, idx_start) + len(CPT2_END)
        old_tbl   = html[idx_start:idx_end]
        new_tbl   = f'<div id="cpt2-wrap" class="tbl-scroll">{old_tbl}</div>'
        html      = html[:idx_start] + new_tbl + html[idx_end:]
        print("cpt2-table: envolvida em div scroll.")
    elif 'id="cpt2-wrap"' in html:
        print("cpt2-table: já estava envolvida.")
    else:
        print("cpt2-table: não encontrada.")

    # 3. Injeta JS de wrap automático antes de </body>
    js_block = f"<script id='mobile-wrap-js'>\n{MOBILE_JS}\n</script>\n"
    if "id='mobile-wrap-js'" in html:
        html = re.sub(
            r"<script id='mobile-wrap-js'>.*?</script>",
            js_block.strip(),
            html, flags=re.DOTALL
        )
        print("JS de wrap: atualizado.")
    elif "</body>" in html:
        html = html.replace("</body>", js_block + "</body>", 1)
        print("JS de wrap: injetado antes de </body>.")
    else:
        print("JS de wrap: </body> não encontrado — não injetado.")

    # 4. Salva arquivo principal
    with open(SRC, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"\nArquivo principal salvo: {SRC}")
    print(f"Tamanho: {len(html):,} bytes (era {original_len:,})")

    # 5. Cria versão com timestamp
    ts = datetime.now().strftime("%Y%m%d_%H%M")
    ver_path = f"{VER_DIR}/Dashboard_Farma_Sul_{ts}.html"
    with open(ver_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Versão criada: {ver_path}")

if __name__ == "__main__":
    main()
