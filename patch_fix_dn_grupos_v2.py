"""
patch_fix_dn_grupos_v2.py
=========================
Substitui o card INTOCÁVEIS × GRUPO PROVEDOR por versão corrigida:
  - Filtros de período (FYTD25/FYTD26/Por Mês) agora atualizam corretamente
  - DD-GAM e DD-Gaúcha adicionados como primeiras opções (fonte: DN_INTOC_GAM / DN_INTOC_GCH)
  - JS completamente reescrito para evitar problemas de escopo/closure
"""
import sys, shutil
sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path
from datetime import datetime

DASH   = Path(r'C:\Users\valqu\OneDrive\Documentos\Claude\Projects\projeto Dashboard_farma_sul\Dashboard_farma_sul\Dashboard_Farma_Sul_20260512_2220.html')
JS_SRC = Path(r'C:\Users\valqu\OneDrive\Documentos\Claude\Projects\projeto Dashboard_farma_sul\dn_intoc_grupos.js')
VER    = DASH.parent / 'versoes'
DL     = Path.home() / 'Downloads'
ts     = datetime.now().strftime('%Y%m%d_%H%M')

# ── Backup ────────────────────────────────────────────────────────────────────
shutil.copy(DASH, VER / f'Dashboard_Farma_Sul_{ts}_PreFixDnGrupos.html')
print(f'Backup: Dashboard_Farma_Sul_{ts}_PreFixDnGrupos.html')

h  = DASH.read_text(encoding='utf-8')
js = JS_SRC.read_text(encoding='utf-8')

# ── Remover bloco existente ───────────────────────────────────────────────────
OLD_ANCHOR_START = '<!-- INTOCÁVEIS × GRUPO PROVEDOR — SELL OUT -->'
OLD_ANCHOR_END   = '\n  <!-- VERBAS -->'
assert OLD_ANCHOR_START in h, 'ERRO: marcador de início não encontrado'
assert OLD_ANCHOR_END in h,   'ERRO: marcador <!-- VERBAS --> não encontrado'
i_start = h.find(OLD_ANCHOR_START)
i_end   = h.find(OLD_ANCHOR_END, i_start)
old_block = h[i_start:i_end]
print(f'Bloco removido: {len(old_block):,} chars')

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

# Opções seletor de mês
mes_options = '<optgroup label="── FYTD25 (Jul/24–Mar/25) ──">'
for m in FYTD25_MESES:
    mes_options += f'<option value="{m}">{MESES_LABEL[m]}</option>'
mes_options += '</optgroup><optgroup label="── FYTD26 (Jul/25–Mar/26) ──">'
for m in FYTD26_MESES:
    sel = ' selected' if m == '202603' else ''
    mes_options += f'<option value="{m}"{sel}>{MESES_LABEL[m]}</option>'
mes_options += '</optgroup>'

# JS arrays inline
js_fytd25 = str(FYTD25_MESES).replace("'", '"')
js_fytd26 = str(FYTD26_MESES).replace("'", '"')
js_todos  = str(TODOS_MESES).replace("'", '"')
js_labels = '{' + ','.join([f'"{m}":"{MESES_LABEL[m]}"' for m in TODOS_MESES]) + '}'

# ── Novo bloco ────────────────────────────────────────────────────────────────
NEW_BLOCK = f"""<!-- INTOCÁVEIS × GRUPO PROVEDOR — SELL OUT -->
<script>
{js}
</script>

<div id="intoc-grupos-card" class="card full" style="margin-bottom:14px;">
  <div class="card-header" style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:12px;margin-bottom:16px;">
    <div>
      <div style="font-size:10px;font-weight:700;letter-spacing:0.1em;color:#fbbf24;margin-bottom:4px;">&#127942; INTOC&#193;VEIS &times; GRUPO PROVEDOR &mdash; SELL OUT</div>
      <div class="card-title">Distribui&#231;&#227;o Num&#233;rica dos 3 SKUs Intoc&#225;veis</div>
      <div class="card-sub" id="intoc-g-sub">OFF Lo&#231;&#227;o 200ml &middot; OFF Spray 170ml &middot; OFF Kids 200ml &middot; Fonte: vendas por EAN</div>
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
  // ── Estado ──────────────────────────────────────────────────────────────────
  var _periodo  = 'fytd26';
  var _sku      = 'soma';
  var _grupo    = null;
  var _populated = false;

  var MESES_LBL  = {js_labels};
  var FYTD25     = {js_fytd25};
  var FYTD26     = {js_fytd26};
  var TODOS      = {js_todos};

  var SKU_NOMES = {{
    soma:     'Somatório',
    kids200:  'Kids 200ML',
    spray170: 'Spray 170ML',
    locao200: 'Loção 200ML'
  }};
  var SKU_CORES = {{
    kids200: '#fbbf24',
    spray170: '#34d399',
    locao200: '#60a5fa'
  }};

  // Grupos distribuidores especiais (usam DN_INTOC_GAM / DN_INTOC_GCH)
  var DIST_MAP = {{
    '__GAM__': {{ label:'DD-GAM (Grupo GAM)',    src:'DN_INTOC_GAM', total:4962 }},
    '__GCH__': {{ label:'DD-GAÚCHA (Gaúcha Farma)', src:'DN_INTOC_GCH', total:4372 }}
  }};

  // ── Preencher dropdown ──────────────────────────────────────────────────────
  function populateGrupos() {{
    if (_populated) return;
    var sel = document.getElementById('intoc-g-grupo-sel');
    if (!sel) return;

    // Adicionar distribuidores especiais primeiro
    var html = '<optgroup label="── Distribuidores (Sell-In) ──">';
    html += '<option value="__GAM__">DD-GAM (Grupo GAM) — 4.962 PDVs</option>';
    html += '<option value="__GCH__">DD-GAÚCHA (Gaúcha Farma) — 4.372 PDVs</option>';
    html += '</optgroup>';

    // Grupos do sell-out
    var grupos  = Object.keys(DN_INTOC_GRUPOS).sort();
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
    // Selecionar o maior grupo sell-out por padrão
    _grupo = big[0] || grupos[0];
    sel.value = _grupo;
    _populated = true;
  }}

  // ── Atualizar botões de período ──────────────────────────────────────────────
  function _atualizarBotoes(p) {{
    var btns = {{ fytd25:'ig-btn-fytd25', fytd26:'ig-btn-fytd26', mes:'ig-btn-mes' }};
    Object.keys(btns).forEach(function(k) {{
      var b = document.getElementById(btns[k]);
      if (!b) return;
      b.classList.remove('active', 'blue');
      if (k === p) b.classList.add('active', 'blue');
    }});
    var mesSel = document.getElementById('intoc-g-mes-sel');
    if (mesSel) mesSel.style.display = p === 'mes' ? 'inline-block' : 'none';
  }}

  // ── Render distribuidor (GAM / Gaúcha) ─────────────────────────────────────
  function renderDistribuidor(bodyEl, tabsEl, badge, src) {{
    // Para distribuidores não há toggle FYTD25/26/mês — dados são de campanha única
    var d = window[src];
    if (!d) {{ bodyEl.innerHTML = '<p style="color:#ef4444">Dados não encontrados: ' + src + '</p>'; return; }}

    // Badge
    var soma = d.soma;
    if (badge) badge.textContent = (soma.total||0).toLocaleString('pt-BR') + ' PDVs';

    // Tabs SKU (sem "Somatório" para distribuidores pois soma não tem UFs individuais)
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

    var html = '';
    if (_sku === 'soma') {{
      // Mostrar KPIs de soma
      var pcts = [
        {{ label:'Algum Intocável', val:soma.dnAlgum, sub:soma.algum+' PDVs', cor:'#34d399' }},
        {{ label:'2 ou mais', val:soma.dnDois, sub:soma.dois+' PDVs', cor:'#fbbf24' }},
        {{ label:'Todos os 3', val:soma.dnTodos, sub:soma.todos+' PDVs', cor:'#60a5fa' }}
      ];
      html += '<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-bottom:16px;">';
      pcts.forEach(function(p) {{
        var dnCor = p.val >= 50 ? '#34d399' : p.val >= 30 ? '#fbbf24' : '#ef4444';
        html += '<div style="background:#161B22;border-radius:10px;padding:14px;border-top:2px solid ' + p.cor + ';">';
        html += '<div style="font-size:9px;font-weight:700;color:#475569;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:8px;">' + p.label + '</div>';
        html += '<div style="font-size:28px;font-weight:800;color:' + dnCor + ';line-height:1;">' + p.val.toFixed(1) + '%</div>';
        html += '<div style="font-size:10px;color:#94a3b8;margin-top:4px;">' + p.sub + ' / ' + soma.total.toLocaleString('pt-BR') + ' PDVs</div>';
        html += '<div style="margin-top:10px;height:4px;background:rgba(255,255,255,0.06);border-radius:2px;">';
        html += '<div style="width:' + Math.min(p.val,100).toFixed(1) + '%;height:4px;background:' + p.cor + ';border-radius:2px;"></div></div>';
        html += '</div>';
      }});
      html += '</div>';
      // Barras por UF
      html += '<div style="font-size:9px;font-weight:700;color:#475569;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:8px;">ALGUM INTOCÁVEL — POR UF</div>';
      soma.ufs.forEach(function(u) {{
        var cor = u.dn >= 50 ? '#34d399' : u.dn >= 30 ? '#fbbf24' : '#ef4444';
        html += '<div style="display:flex;align-items:center;gap:8px;margin-bottom:6px;">';
        html += '<span style="font-size:10px;font-weight:700;color:#94a3b8;width:24px;">' + u.uf + '</span>';
        html += '<div style="flex:1;background:rgba(255,255,255,0.05);border-radius:4px;height:18px;position:relative;">';
        html += '<div style="width:' + Math.min(u.dn,100).toFixed(1) + '%;height:18px;background:' + cor + ';border-radius:4px;opacity:0.7;"></div>';
        html += '<span style="position:absolute;left:8px;top:2px;font-size:10px;font-weight:700;color:#fff;">' + u.dn.toFixed(1) + '% &nbsp;(' + u.pdvs + '/' + u.total + ')</span>';
        html += '</div></div>';
      }});
    }} else {{
      // SKU individual
      var skuData = d[_sku];
      if (!skuData) {{ html = '<p style="color:#475569">Sem dados para este SKU neste distribuidor.</p>'; bodyEl.innerHTML = html; return; }}
      var totalPDVs = soma.total;
      var posit = skuData.ufs.reduce(function(s,u){{ return s+u.pdvs; }}, 0);
      var dnGlobal = totalPDVs > 0 ? (posit/totalPDVs*100) : 0;
      var dnCor = dnGlobal >= 50 ? '#34d399' : dnGlobal >= 30 ? '#fbbf24' : '#ef4444';
      var cor = SKU_CORES[_sku] || '#fbbf24';

      html += '<div style="display:flex;align-items:center;gap:20px;margin-bottom:16px;flex-wrap:wrap;">';
      html += '<div style="font-size:48px;font-weight:800;color:' + dnCor + ';line-height:1;">' + dnGlobal.toFixed(1) + '%</div>';
      html += '<div>';
      html += '<div style="font-size:12px;color:#94a3b8;">' + posit.toLocaleString('pt-BR') + ' PDVs positivaram o SKU</div>';
      html += '<div style="font-size:12px;color:#94a3b8;">' + totalPDVs.toLocaleString('pt-BR') + ' PDVs total</div>';
      html += '<div style="font-size:12px;color:#ef4444;font-weight:700;">' + (totalPDVs-posit).toLocaleString('pt-BR') + ' PDVs SEM o SKU</div>';
      html += '</div></div>';
      html += '<div style="background:rgba(255,255,255,0.05);border-radius:8px;height:12px;margin-bottom:16px;">';
      html += '<div style="width:' + Math.min(dnGlobal,100).toFixed(1) + '%;height:12px;background:' + dnCor + ';border-radius:8px;"></div></div>';

      html += '<div style="font-size:9px;font-weight:700;color:#475569;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:8px;">POR UF — ' + SKU_NOMES[_sku] + '</div>';
      skuData.ufs.forEach(function(u) {{
        var uc = u.dn >= 50 ? '#34d399' : u.dn >= 30 ? '#fbbf24' : '#ef4444';
        html += '<div style="display:flex;align-items:center;gap:8px;margin-bottom:6px;">';
        html += '<span style="font-size:10px;font-weight:700;color:#94a3b8;width:24px;">' + u.uf + '</span>';
        html += '<div style="flex:1;background:rgba(255,255,255,0.05);border-radius:4px;height:18px;position:relative;">';
        html += '<div style="width:' + Math.min(u.dn,100).toFixed(1) + '%;height:18px;background:' + uc + ';border-radius:4px;opacity:0.7;"></div>';
        html += '<span style="position:absolute;left:8px;top:2px;font-size:10px;font-weight:700;color:#fff;">' + u.dn.toFixed(1) + '% &nbsp;(' + u.pdvs + '/' + u.total + ')</span>';
        html += '</div></div>';
      }});
    }}

    // Nota de fonte
    html += '<div style="margin-top:12px;font-size:9px;color:#475569;font-style:italic;">* Dados de distribuidor baseados em Sell-In. Sem histórico mensal disponível.</div>';
    bodyEl.innerHTML = html;
  }}

  // ── Render grupo sell-out ───────────────────────────────────────────────────
  function renderGrupo(bodyEl, tabsEl, badge, grupo) {{
    var d = DN_INTOC_GRUPOS[grupo];
    if (!d) {{ bodyEl.innerHTML = '<p style="color:#ef4444">Grupo não encontrado: ' + grupo + '</p>'; return; }}

    // Badge total FYTD26
    var tot26 = (d.fytd26 && d.fytd26.kids200) ? d.fytd26.kids200.total : 0;
    if (badge) badge.textContent = tot26.toLocaleString('pt-BR') + ' PDVs (FYTD26)';

    // Tabs SKU
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

    var html = '';

    // Obter dados do período
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

    if (_sku === 'soma') {{
      // 3 KPI cards lado a lado
      var skus  = ['kids200','spray170','locao200'];
      var nomes = {{ kids200:'Kids 200ML', spray170:'Spray 170ML', locao200:'Loção 200ML' }};
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
        html += '<div style="font-size:10px;color:#94a3b8;margin-top:4px;">' + pdvs.toLocaleString('pt-BR') + ' / ' + tot.toLocaleString('pt-BR') + ' PDVs</div>';
        if (delta !== null) html += '<div style="font-size:10px;font-weight:700;color:' + deltaCor + ';margin-top:6px;">' + deltaStr + '</div>';
        html += '<div style="margin-top:10px;height:4px;background:rgba(255,255,255,0.06);border-radius:2px;">';
        html += '<div style="width:' + Math.min(dn,100).toFixed(1) + '%;height:4px;background:' + cor + ';border-radius:2px;"></div></div>';
        html += '</div>';
      }});
      html += '</div>';

      // Tabela de evolução mensal
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

      html += '<div style="display:flex;align-items:center;gap:20px;margin-bottom:16px;flex-wrap:wrap;">';
      html += '<div style="font-size:48px;font-weight:800;color:' + dnCor + ';line-height:1;">' + dn.toFixed(1) + '%</div>';
      html += '<div>';
      html += '<div style="font-size:12px;color:#94a3b8;">' + pdvs.toLocaleString('pt-BR') + ' PDVs positivaram o SKU</div>';
      html += '<div style="font-size:12px;color:#94a3b8;">' + tot.toLocaleString('pt-BR') + ' PDVs total no grupo</div>';
      html += '<div style="font-size:12px;color:#ef4444;font-weight:700;">' + gap.toLocaleString('pt-BR') + ' PDVs SEM o SKU</div>';
      html += '</div></div>';
      html += '<div style="background:rgba(255,255,255,0.05);border-radius:8px;height:12px;margin-bottom:16px;">';
      html += '<div style="width:' + Math.min(dn,100).toFixed(1) + '%;height:12px;background:' + dnCor + ';border-radius:8px;transition:width 0.4s;"></div></div>';

      // Grid mensal 9+9
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

    bodyEl.innerHTML = html;
  }}

  // ── Render principal ────────────────────────────────────────────────────────
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

    // Distribuidor especial?
    if (_grupo === '__GAM__') {{
      if (badge) badge.textContent = '4.962 PDVs (Sell-In)';
      renderDistribuidor(bodyEl, tabsEl, badge, 'DN_INTOC_GAM');
    }} else if (_grupo === '__GCH__') {{
      if (badge) badge.textContent = '4.372 PDVs (Sell-In)';
      renderDistribuidor(bodyEl, tabsEl, badge, 'DN_INTOC_GCH');
    }} else {{
      renderGrupo(bodyEl, tabsEl, badge, _grupo);
    }}
  }}

  // ── API pública ─────────────────────────────────────────────────────────────
  window._igRender = render;

  window._igSetPeriodo = function(p) {{
    _periodo = p;
    // Ocultar/exibir toggle de distribuidores
    var wrap = document.getElementById('intoc-g-toggle-wrap');
    if (_grupo === '__GAM__' || _grupo === '__GCH__') {{
      // Distribuidores não têm histórico — ignorar toggle de período
    }}
    render();
  }};

  window._igSkuSet = function(k) {{
    _sku = k;
    render();
  }};

  // ── Init ────────────────────────────────────────────────────────────────────
  function init() {{
    if (typeof DN_INTOC_GRUPOS !== 'undefined') render();
  }}
  if (document.readyState === 'loading') {{
    document.addEventListener('DOMContentLoaded', init);
  }} else {{
    init();
  }}
}})();
</script>
"""

# ── Substituir bloco no HTML ──────────────────────────────────────────────────
h = h[:i_start] + NEW_BLOCK + h[i_end:]
print(f'Novo bloco injetado: {len(NEW_BLOCK):,} chars')

# ── Salvar ────────────────────────────────────────────────────────────────────
DASH.write_text(h, encoding='utf-8')
shutil.copy(DASH, VER / f'Dashboard_Farma_Sul_{ts}_FixDnGrupos.html')
shutil.copy(DASH, DL  / f'Dashboard_FarmaSul_Giovano_{ts}.html')
print(f'\nSalvo:     Dashboard_Farma_Sul_20260512_2220.html')
print(f'Versao:    Dashboard_Farma_Sul_{ts}_FixDnGrupos.html')
print(f'Downloads: Dashboard_FarmaSul_Giovano_{ts}.html')
print('DONE.')
