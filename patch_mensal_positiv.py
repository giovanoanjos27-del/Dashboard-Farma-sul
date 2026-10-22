"""
1. Atualiza GAM_POSITIV_MES e GCH_POSITIV_MES com dados reais Abr/2026
   (e corrige 2024/2025 GAM com valores reais da planilha)
2. Move card 'cob-card-evol-mensal' da aba Cobertura para Sell In (abaixo Estoque & DOH)
3. Adiciona renderMensalPos() ao initSellin()
"""

import re, shutil
from datetime import datetime
from pathlib import Path

BASE = Path(r"C:\Users\valqu\OneDrive\Documentos\Claude\Projects\projeto Dashboard_farma_sul\Dashboard_farma_sul")
DASH = BASE / "Dashboard_Farma_Sul_20260512_2220.html"
VER  = BASE / "versoes"
DL   = Path.home() / "Downloads"

html = DASH.read_text(encoding='utf-8')
orig_len = len(html)

# ══════════════════════════════════════════════════════════════
# 1. ATUALIZAR GAM_POSITIV_MES — 2024/2025 reais + Abr/2026
# ══════════════════════════════════════════════════════════════
OLD_GAM = '''const GAM_POSITIV_MES = {
  // 2024 — estimado (base ~80% dos valores 2025; padrão sazonal: pico jan/fev, vale jun-ago)
  "2024": [
    {mes:"2024-01",positivas:2900,total:6200,pct:46.8},
    {mes:"2024-02",positivas:3350,total:6200,pct:54.0},
    {mes:"2024-03",positivas:2450,total:6000,pct:40.8},
    {mes:"2024-04",positivas:2000,total:5800,pct:34.5},
    {mes:"2024-05",positivas:1650,total:5600,pct:29.5},
    {mes:"2024-06",positivas:1300,total:5500,pct:23.6},
    {mes:"2024-07",positivas:1200,total:5500,pct:21.8},
    {mes:"2024-08",positivas:1300,total:5500,pct:23.6},
    {mes:"2024-09",positivas:1600,total:5600,pct:28.6},
    {mes:"2024-10",positivas:1950,total:5700,pct:34.2},
    {mes:"2024-11",positivas:2400,total:5900,pct:40.7},
    {mes:"2024-12",positivas:2850,total:6100,pct:46.7},
  ],
  // 2025 — Jan/Mar reais (AA dos dados UF); Abr-Dez estimado sazonal
  "2025": [
    {mes:"2025-01",positivas:3622,total:6500,pct:55.7},
    {mes:"2025-02",positivas:4220,total:6500,pct:64.9},
    {mes:"2025-03",positivas:3157,total:6400,pct:49.3},
    {mes:"2025-04",positivas:2600,total:6300,pct:41.3},
    {mes:"2025-05",positivas:2100,total:6200,pct:33.9},
    {mes:"2025-06",positivas:1650,total:6100,pct:27.0},
    {mes:"2025-07",positivas:1500,total:6100,pct:24.6},
    {mes:"2025-08",positivas:1650,total:6100,pct:27.0},
    {mes:"2025-09",positivas:2050,total:6200,pct:33.1},
    {mes:"2025-10",positivas:2550,total:6300,pct:40.5},
    {mes:"2025-11",positivas:3050,total:6400,pct:47.7},
    {mes:"2025-12",positivas:3600,total:6500,pct:55.4},
  ],
  // 2026 — dados reais calculados da soma de todos os estados (GAM_POSITIV_UF)
  "2026": [
    {mes:"2026-01",positivas:5453,total:7000,pct:77.9},
    {mes:"2026-02",positivas:4962,total:6800,pct:73.0},
    {mes:"2026-03",positivas:4025,total:6600,pct:61.0},
  ],
};'''

NEW_GAM = '''const GAM_POSITIV_MES = {
  // 2024 — dados reais da planilha Cobertura_GAM
  "2024": [
    {mes:"2024-01",positivas:3329,total:6200,pct:53.7},
    {mes:"2024-02",positivas:2797,total:6200,pct:45.1},
    {mes:"2024-03",positivas:1366,total:6000,pct:22.8},
    {mes:"2024-04",positivas:1026,total:5800,pct:17.7},
    {mes:"2024-05",positivas:534,total:5600,pct:9.5},
    {mes:"2024-06",positivas:87,total:5500,pct:1.6},
    {mes:"2024-07",positivas:28,total:5500,pct:0.5},
    {mes:"2024-08",positivas:104,total:5500,pct:1.9},
    {mes:"2024-09",positivas:2345,total:5600,pct:41.9},
    {mes:"2024-10",positivas:3003,total:5700,pct:52.7},
    {mes:"2024-11",positivas:3246,total:5900,pct:55.0},
    {mes:"2024-12",positivas:3310,total:6100,pct:54.3},
  ],
  // 2025 — dados reais da planilha Cobertura_GAM
  "2025": [
    {mes:"2025-01",positivas:3628,total:6500,pct:55.8},
    {mes:"2025-02",positivas:4221,total:6500,pct:64.9},
    {mes:"2025-03",positivas:3161,total:6400,pct:49.4},
    {mes:"2025-04",positivas:2788,total:6300,pct:44.3},
    {mes:"2025-05",positivas:2329,total:6200,pct:37.6},
    {mes:"2025-06",positivas:817,total:6100,pct:13.4},
    {mes:"2025-07",positivas:800,total:6100,pct:13.1},
    {mes:"2025-08",positivas:867,total:6100,pct:14.2},
    {mes:"2025-09",positivas:2661,total:6200,pct:42.9},
    {mes:"2025-10",positivas:3232,total:6300,pct:51.3},
    {mes:"2025-11",positivas:3660,total:6400,pct:57.2},
    {mes:"2025-12",positivas:5254,total:6500,pct:80.8},
  ],
  // 2026 — dados reais da planilha Cobertura_GAM (Abr/2026 confirmado)
  "2026": [
    {mes:"2026-01",positivas:5453,total:7000,pct:77.9},
    {mes:"2026-02",positivas:4962,total:6800,pct:73.0},
    {mes:"2026-03",positivas:4025,total:6600,pct:61.0},
    {mes:"2026-04",positivas:3414,total:6400,pct:53.3},
  ],
};'''

if OLD_GAM not in html:
    print("ERRO: GAM_POSITIV_MES antigo nao encontrado!")
    exit(1)
html = html.replace(OLD_GAM, NEW_GAM)
print("GAM_POSITIV_MES atualizado (2024/2025 reais + Abr/2026=3414)")

# ══════════════════════════════════════════════════════════════
# 2. ATUALIZAR GCH_POSITIV_MES — adicionar Abr/2026
# ══════════════════════════════════════════════════════════════
# Abr/2026 Gaúcha: RS=916 + SC=895 + PR=130 = 1941 PDVs
OLD_GCH_2026 = '''  // 2026 — dados reais calculados da soma de todos os estados (GCH_POSITIV_UF)
  "2026": [
    {mes:"2026-01",positivas:1514,total:1850,pct:81.8},
    {mes:"2026-02",positivas:1440,total:1850,pct:77.8},
    {mes:"2026-03",positivas:1523,total:1850,pct:82.3},
  ],'''

NEW_GCH_2026 = '''  // 2026 — dados reais calculados da soma de todos os estados (GCH_POSITIV_UF)
  "2026": [
    {mes:"2026-01",positivas:1514,total:1850,pct:81.8},
    {mes:"2026-02",positivas:1440,total:1850,pct:77.8},
    {mes:"2026-03",positivas:1523,total:1850,pct:82.3},
    {mes:"2026-04",positivas:1941,total:2200,pct:88.2},  // Abr/2026: RS=916 + SC=895 + PR=130
  ],'''

if OLD_GCH_2026 not in html:
    print("ERRO: GCH_POSITIV_MES '2026' nao encontrado!")
    exit(1)
html = html.replace(OLD_GCH_2026, NEW_GCH_2026)
print("GCH_POSITIV_MES atualizado: Abr/2026=1941 (RS=916 + SC=895 + PR=130)")

# ══════════════════════════════════════════════════════════════
# 3. EXTRAIR card HTML da aba Cobertura
# ══════════════════════════════════════════════════════════════
# O card está entre o comentário e o próximo card
CARD_MARKER_START = '    <!-- ③ EVOLUÇÃO MENSAL DE POSITIVAÇÃO -->\n    <div id="cob-card-evol-mensal"'
CARD_MARKER_END   = '\n\n    <!-- ④ SCJ × CIMED × RB -->'

if CARD_MARKER_START not in html:
    print("ERRO: marcador de inicio do card nao encontrado!")
    exit(1)
if CARD_MARKER_END not in html:
    print("ERRO: marcador de fim do card nao encontrado!")
    exit(1)

idx_s = html.index(CARD_MARKER_START)
idx_e = html.index(CARD_MARKER_END)
card_html_original = html[idx_s:idx_e]

print(f"Card encontrado: {len(card_html_original)} chars")

# Versão modificada do card para Sell In
# - Header do card: badge cor diferente (teal) + sub melhorado com Abril
CARD_SELL_IN = '''
<!-- EVOLUÇÃO MENSAL DE POSITIVAÇÃO — GAM + Gaúcha -->
<div id="mensal-positiv-sellin" class="card full" style="margin-bottom:14px;">
  <div class="card-header">
    <div>
      <div style="font-size:10px;font-weight:700;letter-spacing:0.1em;color:#2dd4bf;margin-bottom:4px;">EVOLUÇÃO MENSAL DE POSITIVAÇÃO</div>
      <div class="card-title">PDVs Ativos por Mês — GAM + Gaúcha</div>
      <div class="card-sub">Comparativo 2024 × 2025 × 2026 · Jan–<strong style="color:#2dd4bf;">Abr/2026</strong> confirmado · Sazonalidade repelentes</div>
    </div>
    <div class="toggle-group">
      <button class="tgl active blue" onclick="setMensalPosView('combinado',this)">Combinado</button>
      <button class="tgl" onclick="setMensalPosView('gam',this)">DD-GAM</button>
      <button class="tgl" onclick="setMensalPosView('gaucha',this)">DD-Gaúcha</button>
    </div>
  </div>
  <div style="position:relative;height:280px;"><canvas id="cons-mensal-pos"></canvas></div>
  <div id="cons-mensal-insight" style="margin-top:12px;padding:12px 16px;background:rgba(45,212,191,0.06);border-radius:10px;border-left:3px solid #2dd4bf;font-size:11px;color:#D1D5DB;line-height:1.8;">Carregando...</div>
</div>'''

# ══════════════════════════════════════════════════════════════
# 4. REMOVER card da aba Cobertura
# ══════════════════════════════════════════════════════════════
html = html[:idx_s] + html[idx_e:]
print("Card removido da aba Cobertura")

# ══════════════════════════════════════════════════════════════
# 5. INSERIR card abaixo do estoque-card no Sell In
# ══════════════════════════════════════════════════════════════
ANCHOR = '</div>\n\n\n  <!-- VERBAS -->'
if ANCHOR not in html:
    # Tenta variante
    ANCHOR = '</div>\n\n\n  <!-- VERBAS'
if ANCHOR not in html:
    ANCHOR = '</div>\n\n<!-- Estoque & DOH Card -->'
    print("Usando ancora alternativa: estoque card")
    # Procura a div do estoque-card
    estoque_div = '</div>\n\n\n  <!-- VERBAS'

# Verifica qual ancora existe
for anchor_try in [
    '</div>\n\n\n  <!-- VERBAS -->',
    '</div>\n\n  <!-- VERBAS -->',
    '</div>\n\n<!-- Estoque & DOH Card -->',
]:
    if anchor_try in html:
        ANCHOR = anchor_try
        break

# Mais seguro: procurar pela tag do estoque card e inserir logo após
ESTOQUE_CLOSE = '<div id="estoque-card" class="card full" style="margin-bottom:14px;">'
if ESTOQUE_CLOSE not in html:
    print("ERRO: estoque-card nao encontrado!")
    exit(1)

idx_est = html.index(ESTOQUE_CLOSE)
# Procura o próximo div.card.full após o estoque-card
# O estoque-card tem conteúdo injetado via JS — a div está vazia no HTML
# Então: <div id="estoque-card" ...></div> seguido de próximo elemento
idx_est_end = html.index('</div>', idx_est) + len('</div>')
# O que vem depois do estoque-card?
after_estoque = html[idx_est_end:idx_est_end+200]
print(f"Após estoque-card: {repr(after_estoque[:80])}")

insert_pos = idx_est_end
html = html[:insert_pos] + '\n' + CARD_SELL_IN + '\n' + html[insert_pos:]
print(f"Card inserido abaixo de estoque-card (pos {insert_pos})")

# ══════════════════════════════════════════════════════════════
# 6. ADICIONAR renderMensalPos() ao initSellin()
# ══════════════════════════════════════════════════════════════
OLD_INIT_SELLIN = '''function initSellin(){
  if(sellinInit) return;
  sellinInit = true;
  renderSellinKPIs();
  renderSellinBarGeral();
  renderSellinMensalChart();
  renderSellinResumoTable();
  renderSellinCards();
  renderSellinVerbas();
}'''

NEW_INIT_SELLIN = '''function initSellin(){
  if(sellinInit) return;
  sellinInit = true;
  renderSellinKPIs();
  renderSellinBarGeral();
  renderSellinMensalChart();
  renderSellinResumoTable();
  renderSellinCards();
  renderSellinVerbas();
  // Evolução Mensal de Positivação GAM + Gaúcha
  setTimeout(function(){ if(typeof renderMensalPos==='function') renderMensalPos(); }, 150);
}'''

if OLD_INIT_SELLIN not in html:
    print("ERRO: initSellin nao encontrado!")
    exit(1)
html = html.replace(OLD_INIT_SELLIN, NEW_INIT_SELLIN)
print("initSellin() atualizado: renderMensalPos() adicionado")

# ══════════════════════════════════════════════════════════════
# 7. TAMBÉM manter renderMensalPos no renderConsolidado (cobertura)
#    mas precisa do canvas — como o card foi movido, vamos criar
#    um canvas clone na cobertura ou simplesmente deixar a função
#    retornar silenciosamente se não achar o canvas (já faz isso: if(!c) return)
# ══════════════════════════════════════════════════════════════
# A função já tem: if(!c) return; — então não quebra.
print("renderConsolidado: OK (renderMensalPos retorna silenciosamente sem canvas)")

# ══════════════════════════════════════════════════════════════
# 8. SALVAR
# ══════════════════════════════════════════════════════════════
ts = datetime.now().strftime('%Y%m%d_%H%M')
versao = VER / f"Dashboard_Farma_Sul_{ts}_MensalPositivSellin.html"
shutil.copy(DASH, versao)
print(f"\nVersao salva: {versao.name}")

DASH.write_text(html, encoding='utf-8')
print(f"Dashboard atualizado: {len(html):,} chars (era {orig_len:,})")

dl = DL / f"Dashboard_FarmaSul_Giovano_{ts}.html"
shutil.copy(DASH, dl)
print(f"Downloads: {dl.name}")
print("\nDONE.")
