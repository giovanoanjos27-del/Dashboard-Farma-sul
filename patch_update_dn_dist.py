"""
patch_update_dn_dist.py
=======================
Atualiza card INTOCÁVEIS × GRUPO PROVEDOR:
  - Cria DN_INTOC_DIST com dados IQVIA 2026 para DD-GAM e DD-GAÚCHA
  - Corrige bug window[src] (const não é propriedade de window)
  - renderGrupo agora aceita o objeto 'd' diretamente (sem lookup por nome)
  - Para distribuidores: usa DN_INTOC_DIST; para grupos: usa DN_INTOC_GRUPOS
  Fonte IQVIA: Revisão Dados IQVIA 2026.xlsx — aba Base
  DN% = PDV-meses positivos / total PDV-meses ativos (soma mensal acumulada)
  Soma estimada via P(≥1) = 1 - ∏(1-dni) (independência)
"""
import sys, shutil
sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path
from datetime import datetime

DASH = Path(r'C:\Users\valqu\OneDrive\Documentos\Claude\Projects\projeto Dashboard_farma_sul\Dashboard_farma_sul\Dashboard_Farma_Sul_20260512_2220.html')
JS_SRC = Path(r'C:\Users\valqu\OneDrive\Documentos\Claude\Projects\projeto Dashboard_farma_sul\dn_intoc_grupos.js')
VER  = DASH.parent / 'versoes'
DL   = Path.home() / 'Downloads'
ts   = datetime.now().strftime('%Y%m%d_%H%M')

shutil.copy(DASH, VER / f'Dashboard_Farma_Sul_{ts}_PreDistData.html')
print(f'Backup: Dashboard_Farma_Sul_{ts}_PreDistData.html')

h  = DASH.read_text(encoding='utf-8')
js = JS_SRC.read_text(encoding='utf-8')

# ── Remover bloco existente ───────────────────────────────────────────────────
OLD_START = '<!-- INTOCÁVEIS × GRUPO PROVEDOR — SELL OUT -->'
OLD_END   = '\n  <!-- VERBAS -->'
assert OLD_START in h, 'Marcador de início não encontrado'
assert OLD_END   in h, 'Marcador <!-- VERBAS --> não encontrado'
i_start = h.find(OLD_START)
i_end   = h.find(OLD_END, i_start)
print(f'Bloco removido: {i_end - i_start:,} chars')

# ── DN_INTOC_DIST — dados IQVIA ───────────────────────────────────────────────
# Estrutura idêntica a DN_INTOC_GRUPOS para reutilizar renderGrupo
DN_INTOC_DIST_JS = r"""const DN_INTOC_DIST = {
  '__GAM__': {
    nome: 'DD-GAM (Grupo GAM)', fonte: 'IQVIA',
    fytd25: {
      soma:    {total:23115, algum:15372, dnAlgum:66.5, dois:5062,  dnDois:21.9, todos:620,  dnTodos:2.7},
      kids200: {total:23115, pdvs:5594,  dn:24.2},
      spray170:{total:23115, pdvs:7072,  dn:30.6},
      locao200:{total:23115, pdvs:8373,  dn:36.2},
    },
    fytd26: {
      soma:    {total:31082, algum:23280, dnAlgum:74.9, dois:9573,  dnDois:30.8, todos:1561, dnTodos:5.0},
      kids200: {total:31082, pdvs:10876, dn:35.0},
      spray170:{total:31082, pdvs:11362, dn:36.6},
      locao200:{total:31082, pdvs:12196, dn:39.2},
    },
    meses: {
      "202407":{total:28,   soma_dn:0.0,  kids200:{total:28,   pdvs:0,    dn:0.0},  spray170:{total:28,   pdvs:0,    dn:0.0},  locao200:{total:28,   pdvs:0,    dn:0.0}},
      "202408":{total:104,  soma_dn:11.2, kids200:{total:104,  pdvs:7,    dn:6.7},  spray170:{total:104,  pdvs:0,    dn:0.0},  locao200:{total:104,  pdvs:5,    dn:4.8}},
      "202409":{total:2352, soma_dn:57.4, kids200:{total:2352, pdvs:235,  dn:10.0}, spray170:{total:2352, pdvs:523,  dn:22.2}, locao200:{total:2352, pdvs:921,  dn:39.2}},
      "202410":{total:3018, soma_dn:63.2, kids200:{total:3018, pdvs:485,  dn:16.1}, spray170:{total:3018, pdvs:739,  dn:24.5}, locao200:{total:3018, pdvs:1265, dn:41.9}},
      "202411":{total:3254, soma_dn:64.0, kids200:{total:3254, pdvs:418,  dn:12.8}, spray170:{total:3254, pdvs:1114, dn:34.2}, locao200:{total:3254, pdvs:1209, dn:37.2}},
      "202412":{total:3319, soma_dn:72.2, kids200:{total:3319, pdvs:1194, dn:36.0}, spray170:{total:3319, pdvs:941,  dn:28.4}, locao200:{total:3319, pdvs:1303, dn:39.3}},
      "202501":{total:3638, soma_dn:67.9, kids200:{total:3638, pdvs:982,  dn:27.0}, spray170:{total:3638, pdvs:1187, dn:32.6}, locao200:{total:3638, pdvs:1262, dn:34.7}},
      "202502":{total:4232, soma_dn:75.5, kids200:{total:4232, pdvs:1747, dn:41.3}, spray170:{total:4232, pdvs:1433, dn:33.9}, locao200:{total:4232, pdvs:1559, dn:36.8}},
      "202503":{total:3170, soma_dn:60.8, kids200:{total:3170, pdvs:526,  dn:16.6}, spray170:{total:3170, pdvs:1135, dn:35.8}, locao200:{total:3170, pdvs:849,  dn:26.8}},
      "202507":{total:801,  soma_dn:50.9, kids200:{total:801,  pdvs:97,   dn:12.1}, spray170:{total:801,  pdvs:161,  dn:20.1}, locao200:{total:801,  pdvs:240,  dn:30.0}},
      "202508":{total:866,  soma_dn:52.9, kids200:{total:866,  pdvs:148,  dn:17.1}, spray170:{total:866,  pdvs:186,  dn:21.5}, locao200:{total:866,  pdvs:240,  dn:27.7}},
      "202509":{total:2665, soma_dn:70.7, kids200:{total:2665, pdvs:721,  dn:27.1}, spray170:{total:2665, pdvs:879,  dn:33.0}, locao200:{total:2665, pdvs:1067, dn:40.0}},
      "202510":{total:3238, soma_dn:77.6, kids200:{total:3238, pdvs:1252, dn:38.7}, spray170:{total:3238, pdvs:1178, dn:36.4}, locao200:{total:3238, pdvs:1379, dn:42.6}},
      "202511":{total:3674, soma_dn:73.3, kids200:{total:3674, pdvs:1419, dn:38.6}, spray170:{total:3674, pdvs:1087, dn:29.6}, locao200:{total:3674, pdvs:1404, dn:38.2}},
      "202512":{total:5263, soma_dn:81.3, kids200:{total:5263, pdvs:2018, dn:38.3}, spray170:{total:5263, pdvs:2215, dn:42.1}, locao200:{total:5263, pdvs:2508, dn:47.7}},
      "202601":{total:5505, soma_dn:76.9, kids200:{total:5505, pdvs:2049, dn:37.2}, spray170:{total:5505, pdvs:2178, dn:39.6}, locao200:{total:5505, pdvs:2146, dn:39.0}},
      "202602":{total:4999, soma_dn:77.6, kids200:{total:4999, pdvs:1972, dn:39.4}, spray170:{total:4999, pdvs:2085, dn:41.7}, locao200:{total:4999, pdvs:1835, dn:36.7}},
      "202603":{total:4071, soma_dn:69.3, kids200:{total:4071, pdvs:1200, dn:29.5}, spray170:{total:4071, pdvs:1393, dn:34.2}, locao200:{total:4071, pdvs:1377, dn:33.8}},
    },
  },
  '__GCH__': {
    nome: 'DD-GAÚCHA (Gaúcha Farma)', fonte: 'IQVIA',
    fytd25: {
      soma:    {total:10455, algum:6053, dnAlgum:57.9, dois:1620, dnDois:15.5, todos:159, dnTodos:1.5},
      kids200: {total:10455, pdvs:2913, dn:27.9},
      spray170:{total:10455, pdvs:2196, dn:21.0},
      locao200:{total:10455, pdvs:2714, dn:26.0},
    },
    fytd26: {
      soma:    {total:8672, algum:4969, dnAlgum:57.3, dois:1318, dnDois:15.2, todos:128, dnTodos:1.5},
      kids200: {total:8672, pdvs:1908, dn:22.0},
      spray170:{total:8672, pdvs:2293, dn:26.4},
      locao200:{total:8672, pdvs:2210, dn:25.5},
    },
    meses: {
      "202407":{total:728,  soma_dn:21.6, kids200:{total:728,  pdvs:111, dn:15.2}, spray170:{total:728,  pdvs:5,   dn:0.7},  locao200:{total:728,  pdvs:51,  dn:7.0}},
      "202408":{total:1091, soma_dn:54.7, kids200:{total:1091, pdvs:304, dn:27.9}, spray170:{total:1091, pdvs:213, dn:19.5}, locao200:{total:1091, pdvs:239, dn:21.9}},
      "202409":{total:1467, soma_dn:82.4, kids200:{total:1467, pdvs:647, dn:44.1}, spray170:{total:1467, pdvs:591, dn:40.3}, locao200:{total:1467, pdvs:696, dn:47.4}},
      "202410":{total:1139, soma_dn:60.5, kids200:{total:1139, pdvs:381, dn:33.5}, spray170:{total:1139, pdvs:294, dn:25.8}, locao200:{total:1139, pdvs:227, dn:19.9}},
      "202411":{total:1207, soma_dn:53.4, kids200:{total:1207, pdvs:362, dn:30.0}, spray170:{total:1207, pdvs:255, dn:21.1}, locao200:{total:1207, pdvs:189, dn:15.7}},
      "202412":{total:992,  soma_dn:52.1, kids200:{total:992,  pdvs:277, dn:27.9}, spray170:{total:992,  pdvs:145, dn:14.6}, locao200:{total:992,  pdvs:219, dn:22.1}},
      "202501":{total:1374, soma_dn:50.4, kids200:{total:1374, pdvs:346, dn:25.2}, spray170:{total:1374, pdvs:207, dn:15.1}, locao200:{total:1374, pdvs:299, dn:21.8}},
      "202502":{total:1193, soma_dn:51.2, kids200:{total:1193, pdvs:217, dn:18.2}, spray170:{total:1193, pdvs:222, dn:18.6}, locao200:{total:1193, pdvs:318, dn:26.7}},
      "202503":{total:1264, soma_dn:61.2, kids200:{total:1264, pdvs:268, dn:21.2}, spray170:{total:1264, pdvs:264, dn:20.9}, locao200:{total:1264, pdvs:476, dn:37.7}},
      "202507":{total:188,  soma_dn:16.7, kids200:{total:188,  pdvs:6,   dn:3.2},  spray170:{total:188,  pdvs:12,  dn:6.4},  locao200:{total:188,  pdvs:15,  dn:8.0}},
      "202508":{total:169,  soma_dn:22.4, kids200:{total:169,  pdvs:14,  dn:8.3},  spray170:{total:169,  pdvs:14,  dn:8.3},  locao200:{total:169,  pdvs:13,  dn:7.7}},
      "202509":{total:734,  soma_dn:59.9, kids200:{total:734,  pdvs:163, dn:22.2}, spray170:{total:734,  pdvs:200, dn:27.2}, locao200:{total:734,  pdvs:214, dn:29.2}},
      "202510":{total:1070, soma_dn:59.8, kids200:{total:1070, pdvs:247, dn:23.1}, spray170:{total:1070, pdvs:262, dn:24.5}, locao200:{total:1070, pdvs:328, dn:30.7}},
      "202511":{total:1243, soma_dn:59.8, kids200:{total:1243, pdvs:214, dn:17.2}, spray170:{total:1243, pdvs:363, dn:29.2}, locao200:{total:1243, pdvs:392, dn:31.5}},
      "202512":{total:1369, soma_dn:58.5, kids200:{total:1369, pdvs:417, dn:30.5}, spray170:{total:1369, pdvs:410, dn:29.9}, locao200:{total:1369, pdvs:201, dn:14.7}},
      "202601":{total:1302, soma_dn:56.3, kids200:{total:1302, pdvs:292, dn:22.4}, spray170:{total:1302, pdvs:323, dn:24.8}, locao200:{total:1302, pdvs:328, dn:25.2}},
      "202602":{total:1063, soma_dn:51.6, kids200:{total:1063, pdvs:160, dn:15.1}, spray170:{total:1063, pdvs:293, dn:27.6}, locao200:{total:1063, pdvs:226, dn:21.3}},
      "202603":{total:1534, soma_dn:63.3, kids200:{total:1534, pdvs:395, dn:25.7}, spray170:{total:1534, pdvs:416, dn:27.1}, locao200:{total:1534, pdvs:493, dn:32.1}},
    },
  },
};"""

# ── Labels e listas de meses ──────────────────────────────────────────────────
MESES_LABEL = {
    '202407':'Jul/24','202408':'Ago/24','202409':'Set/24',
    '202410':'Out/24','202411':'Nov/24','202412':'Dez/24',
    '202501':'Jan/25','202502':'Fev/25','202503':'Mar/25',
    '202507':'Jul/25','202508':'Ago/25','202509':'Set/25',
    '202510':'Out/25','202511':'Nov/25','202512':'Dez/25',
    '202601':'Jan/26','202602':'Fev/26','202603':'Mar/26',
}
FYTD25_MESES = ['202407','202408','202409','202410','202411','202412','202501','202502','202503']
FYTD26_MESES = ['202507','202508','202509','202510','202511','202512','202601','202602','202603']
TODOS_MESES  = FYTD25_MESES + FYTD26_MESES

mes_options = '<optgroup label="── FYTD25 (Jul/24–Mar/25) ──">'
for m in FYTD25_MESES:
    mes_options += f'<option value="{m}">{MESES_LABEL[m]}</option>'
mes_options += '</optgroup><optgroup label="── FYTD26 (Jul/25–Mar/26) ──">'
for m in FYTD26_MESES:
    sel = ' selected' if m == '202603' else ''
    mes_options += f'<option value="{m}"{sel}>{MESES_LABEL[m]}</option>'
mes_options += '</optgroup>'

js_fytd25 = str(FYTD25_MESES).replace("'", '"')
js_fytd26 = str(FYTD26_MESES).replace("'", '"')
js_todos  = str(TODOS_MESES).replace("'", '"')
js_labels = '{' + ','.join([f'"{m}":"{MESES_LABEL[m]}"' for m in TODOS_MESES]) + '}'

# ── Novo bloco ────────────────────────────────────────────────────────────────
NEW_BLOCK = f"""<!-- INTOCÁVEIS × GRUPO PROVEDOR — SELL OUT -->
<script>
{js}
</script>
<script>
{DN_INTOC_DIST_JS}
</script>

<div id="intoc-grupos-card" class="card full" style="margin-bottom:14px;">
  <div class="card-header" style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:12px;margin-bottom:16px;">
    <div>
      <div style="font-size:10px;font-weight:700;letter-spacing:0.1em;color:#fbbf24;margin-bottom:4px;">&#127942; INTOC&#193;VEIS &times; GRUPO PROVEDOR &mdash; SELL OUT</div>
      <div class="card-title">Distribui&#231;&#227;o Num&#233;rica dos 3 SKUs Intoc&#225;veis</div>
      <div class="card-sub" id="intoc-g-sub">OFF Lo&#231;&#227;o 200ml &middot; OFF Spray 170ml &middot; OFF Kids 200ml &middot; Fonte: vendas por EAN / IQVIA</div>
    </div>
    <div style="display:flex;gap:8px;align-items:center;flex-wrap:wrap;">
      <div id="intoc-g-toggle-wrap" style="display:flex;gap:4px;">
        <button id="ig-btn-fytd25" class="tgl" onclick="window._igSetPeriodo('fytd25')">FYTD25</button>
        <button id="ig-btn-fytd26" class="tgl active blue" onclick="window._igSetPeriodo('fytd26')">FYTD26</button>
        <button id="ig-btn-mes"    class="tgl"             onclick="window._igSetPeriodo('mes')">Por M&#234;s</button>
      </div>
      <select id="intoc-g-mes-sel" onchange="window._igRender()"
        style="display:none;font-size:11px;padding:5px 22px 5px 8px;border-radius:7px;
               border:0.5px solid rgba(251,191,36,0.3);background:#161B22;color:#e2e8f0;
               cursor:pointer;font-family:inherit;appearance:none;
               background-image:url('data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 width=%2210%22 height=%226%22%3E%3Cpath d=%22M0 0l5 6 5-6z%22 fill=%22%23fbbf24%22/%3E%3C/svg%3E');
               background-repeat:no-repeat;background-position:right 8px center;">
        {mes_options}
      </select>
    </div>
  </div>
  <div style="display:flex;align-items:center;gap:10px;margin-bottom:14px;flex-wrap:wrap;">
    <span style="font-size:9px;font-weight:700;color:#475569;text-transform:uppercase;letter-spacing:0.06em;white-space:nowrap;">GRUPO:</span>
    <select id="intoc-g-grupo-sel" onchange="window._igRender()"
      style="font-size:11px;padding:5px 28px 5px 10px;border-radius:7px;
             border:0.5px solid rgba(251,191,36,0.3);background:#161B22;color:#e2e8f0;
             cursor:pointer;font-family:inherit;appearance:none;min-width:220px;
             background-image:url('data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 width=%2210%22 height=%226%22%3E%3Cpath d=%22M0 0l5 6 5-6z%22 fill=%22%23fbbf24%22/%3E%3C/svg%3E');
             background-repeat:no-repeat;background-position:right 10px center;">
    </select>
    <span id="intoc-g-badge" style="font-size:10px;font-weight:700;padding:3px 10px;border-radius:6px;background:rgba(251,191,36,0.1);color:#fbbf24;border:0.5px solid rgba(251,191,36,0.3);"></span>
  </div>
  <div id="intoc-g-tabs" style="display:flex;gap:6px;margin-bottom:14px;flex-wrap:wrap;"></div>
  <div id="intoc-g-body"></div>
</div>

<script>
(function() {{
  var _periodo  = 'fytd26';
  var _sku      = 'soma';
  var _grupo    = null;
  var _populated = false;

  var MESES_LBL = {js_labels};
  var FYTD25    = {js_fytd25};
  var FYTD26    = {js_fytd26};
  var TODOS     = {js_todos};

  var SKU_NOMES = {{soma:'Somatório', kids200:'Kids 200ML', spray170:'Spray 170ML', locao200:'Loção 200ML'}};
  var SKU_CORES = {{kids200:'#fbbf24', spray170:'#34d399', locao200:'#60a5fa'}};

  // ── Preencher dropdown ────────────────────────────────────────────────────
  function populateGrupos() {{
    if (_populated) return;
    var sel = document.getElementById('intoc-g-grupo-sel');
    if (!sel) return;

    var html = '<optgroup label="── Distribuidores (Fonte IQVIA) ──">';
    html += '<option value="__GAM__">DD-GAM (Grupo GAM) — 31.082 PDV-meses FY26</option>';
    html += '<option value="__GCH__">DD-GAÚCHA (Gaúcha Farma) — 8.672 PDV-meses FY26</option>';
    html += '</optgroup>';

    var grupos = Object.keys(DN_INTOC_GRUPOS).sort();
    var big = [], small = [];
    grupos.forEach(function(g) {{
      var tot = (DN_INTOC_GRUPOS[g].fytd26 && DN_INTOC_GRUPOS[g].fytd26.kids200)
                ? DN_INTOC_GRUPOS[g].fytd26.kids200.total : 0;
      if (tot >= 10) big.push(g); else small.push(g);
    }});
    big.sort(function(a, b) {{
      return DN_INTOC_GRUPOS[b].fytd26.kids200.total - DN_INTOC_GRUPOS[a].fytd26.kids200.total;
    }});

    html += '<optgroup label="── Grupos Sell-Out (≥10 PDVs) ──">';
    big.forEach(function(g) {{
      var tot = DN_INTOC_GRUPOS[g].fytd26.kids200.total;
      html += '<option value="' + g + '">' + g + ' (' + tot.toLocaleString('pt-BR') + ' PDVs)</option>';
    }});
    html += '</optgroup>';
    if (small.length) {{
      html += '<optgroup label="── Grupos menores ──">';
      small.forEach(function(g) {{ html += '<option value="' + g + '">' + g + '</option>'; }});
      html += '</optgroup>';
    }}

    sel.innerHTML = html;
    _grupo = big[0] || grupos[0];
    sel.value = _grupo;
    _populated = true;
  }}

  // ── Lookup de dados ───────────────────────────────────────────────────────
  function getGrupoData(g) {{
    if ((g === '__GAM__' || g === '__GCH__') && typeof DN_INTOC_DIST !== 'undefined')
      return DN_INTOC_DIST[g] || null;
    return DN_INTOC_GRUPOS[g] || null;
  }}

  // ── Atualizar botões de período ───────────────────────────────────────────
  function _atualizarBotoes(p) {{
    var btns = {{fytd25:'ig-btn-fytd25', fytd26:'ig-btn-fytd26', mes:'ig-btn-mes'}};
    Object.keys(btns).forEach(function(k) {{
      var b = document.getElementById(btns[k]);
      if (!b) return;
      b.classList.remove('active', 'blue');
      if (k === p) b.classList.add('active', 'blue');
    }});
    var mesSel = document.getElementById('intoc-g-mes-sel');
    if (mesSel) mesSel.style.display = p === 'mes' ? 'inline-block' : 'none';
  }}

  // ── Render de um grupo/distribuidor ──────────────────────────────────────
  function renderGrupo(bodyEl, tabsEl, badge, d) {{
    var isDist = (d.fonte === 'IQVIA');

    // Badge
    if (badge) {{
      var tot26 = (d.fytd26 && d.fytd26.kids200) ? d.fytd26.kids200.total : 0;
      badge.textContent = tot26.toLocaleString('pt-BR') + (isDist ? ' PDV-meses FY26 (IQVIA)' : ' PDVs (FYTD26)');
    }}

    // Sub-tabs SKU
    if (tabsEl) {{
      var tabHtml = '';
      ['soma','kids200','spray170','locao200'].forEach(function(k) {{
        var isAct = k === _sku;
        var nome  = SKU_NOMES[k];
        tabHtml += '<button data-igsku="' + k + '" onclick="window._igSkuSet(this.dataset.igsku)" style="font-size:10px;font-weight:700;'
          + 'padding:4px 12px;border-radius:6px;cursor:pointer;font-family:inherit;'
          + 'border:0.5px solid ' + (isAct ? 'rgba(251,191,36,0.4)' : 'rgba(255,255,255,0.07)') + ';'
          + 'background:' + (isAct ? 'rgba(251,191,36,0.15)' : 'transparent') + ';'
          + 'color:' + (isAct ? '#fbbf24' : '#64748b') + ';">' + nome + '</button>';
      }});
      tabsEl.innerHTML = tabHtml;
    }}

    // Dados do período
    var periodoData;
    if (_periodo === 'fytd25') {{
      periodoData = d.fytd25;
    }} else if (_periodo === 'fytd26') {{
      periodoData = d.fytd26;
    }} else {{
      var mesEl = document.getElementById('intoc-g-mes-sel');
      var mes   = mesEl ? mesEl.value : '202603';
      periodoData = (d.meses && d.meses[mes]) ? d.meses[mes] : null;
    }}

    var html = '';

    if (_sku === 'soma') {{
      var skus   = ['kids200','spray170','locao200'];
      var nomes  = {{kids200:'Kids 200ML', spray170:'Spray 170ML', locao200:'Loção 200ML'}};

      html += '<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-bottom:16px;">';
      skus.forEach(function(sk) {{
        var cor  = SKU_CORES[sk];
        var cur  = periodoData ? periodoData[sk] : null;
        var comp = _periodo === 'fytd26' ? (d.fytd25 ? d.fytd25[sk] : null) :
                   _periodo === 'fytd25' ? (d.fytd26 ? d.fytd26[sk] : null) : null;
        var dn   = cur  ? cur.dn   : 0;
        var pdvs = cur  ? cur.pdvs : 0;
        var tot  = cur  ? cur.total: 0;
        var dnC  = comp ? comp.dn  : null;
        var delta    = dnC !== null ? dn - dnC : null;
        var deltaStr = delta !== null ? (delta >= 0 ? '+' : '') + delta.toFixed(1) + 'pp vs '
                       + (_periodo === 'fytd26' ? 'FYTD25' : 'FYTD26') : '';
        var deltaCor = delta !== null ? (delta >= 0 ? '#34d399' : '#ef4444') : '#94a3b8';
        var dnCor    = dn >= 50 ? '#34d399' : dn >= 30 ? '#fbbf24' : '#ef4444';

        html += '<div style="background:#161B22;border-radius:10px;padding:14px;border-top:2px solid ' + cor + ';">';
        html += '<div style="font-size:9px;font-weight:700;color:#475569;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:8px;">' + nomes[sk] + '</div>';
        html += '<div style="font-size:28px;font-weight:800;color:' + dnCor + ';line-height:1;">' + dn.toFixed(1) + '%</div>';
        html += '<div style="font-size:10px;color:#94a3b8;margin-top:4px;">' + pdvs.toLocaleString('pt-BR') + ' / ' + tot.toLocaleString('pt-BR') + (isDist ? ' PDV-meses' : ' PDVs') + '</div>';
        if (delta !== null) html += '<div style="font-size:10px;font-weight:700;color:' + deltaCor + ';margin-top:6px;">' + deltaStr + '</div>';
        html += '<div style="margin-top:10px;height:4px;background:rgba(255,255,255,0.06);border-radius:2px;">';
        html += '<div style="width:' + Math.min(dn,100).toFixed(1) + '%;height:4px;background:' + cor + ';border-radius:2px;"></div></div>';
        html += '</div>';
      }});
      html += '</div>';

      // Evolução mensal
      html += '<div style="margin-top:4px;overflow-x:auto;">';
      html += '<div style="font-size:9px;font-weight:700;color:#475569;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:8px;">EVOLUÇÃO MENSAL</div>';
      html += '<div style="display:grid;grid-template-columns:80px repeat(18,1fr);gap:2px;font-size:9px;min-width:600px;">';
      html += '<div></div>';
      TODOS.forEach(function(m) {{
        var isFY26 = FYTD26.indexOf(m) >= 0;
        html += '<div style="text-align:center;color:' + (isFY26 ? '#60a5fa' : '#94a3b8') + ';font-weight:700;white-space:nowrap;padding-bottom:2px;">' + (MESES_LBL[m]||m) + '</div>';
      }});
      skus.forEach(function(sk) {{
        html += '<div style="color:' + SKU_CORES[sk] + ';font-weight:700;padding:4px 0;">' + nomes[sk] + '</div>';
        TODOS.forEach(function(m) {{
          var md   = (d.meses && d.meses[m]) ? d.meses[m][sk] : null;
          var dn_m = md ? md.dn : null;
          var bg = dn_m === null ? 'transparent' : dn_m >= 50 ? 'rgba(52,211,153,0.15)' : dn_m >= 30 ? 'rgba(251,191,36,0.1)' : 'rgba(239,68,68,0.1)';
          var tc = dn_m === null ? '#475569' : dn_m >= 50 ? '#34d399' : dn_m >= 30 ? '#fbbf24' : '#ef4444';
          html += '<div style="text-align:center;background:' + bg + ';border-radius:3px;padding:3px 1px;color:' + tc + ';font-weight:600;">' + (dn_m !== null ? dn_m.toFixed(0) + '%' : '—') + '</div>';
        }});
      }});
      html += '</div></div>';

    }} else {{
      // SKU único
      var cur   = periodoData ? periodoData[_sku] : null;
      var dn    = cur ? cur.dn    : 0;
      var pdvs  = cur ? cur.pdvs  : 0;
      var tot   = cur ? cur.total : 0;
      var gap   = tot - pdvs;
      var dnCor = dn >= 50 ? '#34d399' : dn >= 30 ? '#fbbf24' : '#ef4444';
      var unid  = isDist ? 'PDV-meses' : 'PDVs';

      html += '<div style="display:flex;align-items:center;gap:20px;margin-bottom:16px;flex-wrap:wrap;">';
      html += '<div style="font-size:48px;font-weight:800;color:' + dnCor + ';line-height:1;">' + dn.toFixed(1) + '%</div>';
      html += '<div>';
      html += '<div style="font-size:12px;color:#94a3b8;">' + pdvs.toLocaleString('pt-BR') + ' ' + unid + ' positivaram o SKU</div>';
      html += '<div style="font-size:12px;color:#94a3b8;">' + tot.toLocaleString('pt-BR') + ' ' + unid + ' total no grupo</div>';
      html += '<div style="font-size:12px;color:#ef4444;font-weight:700;">' + gap.toLocaleString('pt-BR') + ' ' + unid + ' SEM o SKU</div>';
      html += '</div></div>';
      html += '<div style="background:rgba(255,255,255,0.05);border-radius:8px;height:12px;margin-bottom:16px;">';
      html += '<div style="width:' + Math.min(dn,100).toFixed(1) + '%;height:12px;background:' + dnCor + ';border-radius:8px;transition:width 0.4s;"></div></div>';

      html += '<div style="font-size:9px;font-weight:700;color:#475569;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:8px;">EVOLUÇÃO MENSAL — ' + SKU_NOMES[_sku] + '</div>';
      html += '<div style="display:grid;grid-template-columns:repeat(9,1fr);gap:6px;">';
      [{{meses:FYTD25,cor:'#94a3b8'}},{{meses:FYTD26,cor:'#60a5fa'}}].forEach(function(grp) {{
        grp.meses.forEach(function(m) {{
          var md   = (d.meses && d.meses[m]) ? d.meses[m][_sku] : null;
          var dn_m = md ? md.dn : null;
          var bg = dn_m === null ? 'rgba(255,255,255,0.03)' : dn_m >= 50 ? 'rgba(52,211,153,0.12)' : dn_m >= 30 ? 'rgba(251,191,36,0.1)' : 'rgba(239,68,68,0.1)';
          var tc = dn_m === null ? '#475569' : dn_m >= 50 ? '#34d399' : dn_m >= 30 ? '#fbbf24' : '#ef4444';
          html += '<div style="background:' + bg + ';border-radius:6px;padding:8px 4px;text-align:center;">';
          html += '<div style="font-size:8px;color:' + grp.cor + ';font-weight:700;margin-bottom:4px;">' + (MESES_LBL[m]||m) + '</div>';
          html += '<div style="font-size:14px;font-weight:800;color:' + tc + ';line-height:1;">' + (dn_m !== null ? dn_m.toFixed(0) + '%' : '—') + '</div>';
          if (md) html += '<div style="font-size:8px;color:#475569;margin-top:2px;">' + md.pdvs + '/' + md.total + '</div>';
          html += '</div>';
        }});
      }});
      html += '</div>';
    }}

    if (isDist) {{
      html += '<div style="margin-top:10px;font-size:9px;color:#475569;font-style:italic;">* Fonte: IQVIA 2026. DN% = PDVs positivos / base ativa por mês (soma acumulada). Soma estimada via probabilidade de independência.</div>';
    }}

    bodyEl.innerHTML = html;
  }}

  // ── Render principal ──────────────────────────────────────────────────────
  function render() {{
    populateGrupos();
    var sel = document.getElementById('intoc-g-grupo-sel');
    if (sel && sel.value) _grupo = sel.value;
    if (!_grupo) return;

    var bodyEl = document.getElementById('intoc-g-body');
    var tabsEl = document.getElementById('intoc-g-tabs');
    var badge  = document.getElementById('intoc-g-badge');
    if (!bodyEl) return;

    _atualizarBotoes(_periodo);

    var d = getGrupoData(_grupo);
    if (!d) {{
      bodyEl.innerHTML = '<p style="color:#ef4444;font-size:11px;">Dados não encontrados para: ' + _grupo + '</p>';
      return;
    }}
    renderGrupo(bodyEl, tabsEl, badge, d);
  }}

  // ── API pública ───────────────────────────────────────────────────────────
  window._igRender     = render;
  window._igSetPeriodo = function(p) {{ _periodo = p; render(); }};
  window._igSkuSet     = function(k) {{ _sku = k; render(); }};

  // ── Init ──────────────────────────────────────────────────────────────────
  function init() {{
    if (typeof DN_INTOC_GRUPOS !== 'undefined') render();
  }}
  if (document.readyState === 'loading') {{
    document.addEventListener('DOMContentLoaded', init);
  }} else {{
    init();
  }}
  // Fallback: tenta novamente após 300ms caso DOMContentLoaded já tenha disparado
  setTimeout(function() {{
    if (!_populated && typeof DN_INTOC_GRUPOS !== 'undefined') render();
  }}, 300);
}})();
</script>
"""

# ── Substituir no HTML ────────────────────────────────────────────────────────
h = h[:i_start] + NEW_BLOCK + h[i_end:]
print(f'Novo bloco injetado: {len(NEW_BLOCK):,} chars')

# ── Verificações ──────────────────────────────────────────────────────────────
assert h.count('const DN_INTOC_GRUPOS') == 1, 'ERRO: múltiplas declarações DN_INTOC_GRUPOS'
assert h.count('const DN_INTOC_DIST')   == 1, 'ERRO: múltiplas declarações DN_INTOC_DIST'
assert h.count('dataset.igsku')         >= 1, 'ERRO: onclicks incorretos'
print('Verificações: OK')

# ── Salvar ────────────────────────────────────────────────────────────────────
DASH.write_text(h, encoding='utf-8')
shutil.copy(DASH, VER / f'Dashboard_Farma_Sul_{ts}_DistData.html')
shutil.copy(DASH, DL  / f'Dashboard_FarmaSul_Giovano_{ts}.html')
print(f'\nSalvo:     Dashboard_Farma_Sul_20260512_2220.html')
print(f'Versao:    Dashboard_Farma_Sul_{ts}_DistData.html')
print(f'Downloads: Dashboard_FarmaSul_Giovano_{ts}.html')
print('DONE.')
