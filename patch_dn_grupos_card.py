"""
patch_dn_grupos_card.py
=======================
Adiciona card "INTOCÁVEIS × GRUPO PROVEDOR" no dashboard:
  - Filtro dropdown com todos os 81 grupos (≥10 PDVs visíveis)
  - Toggle de período: FYTD25 | FYTD26 | Por Mês
  - Seletor de mês individual (Jul/24–Mar/26)
  - Barras de DN% por SKU com comparativo FYTD25 vs FYTD26
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

shutil.copy(DASH, VER / f'Dashboard_Farma_Sul_{ts}_PreDnGrupos.html')
print(f'Backup: Dashboard_Farma_Sul_{ts}_PreDnGrupos.html')

h   = DASH.read_text(encoding='utf-8')
js  = JS_SRC.read_text(encoding='utf-8')

# ── Montar o bloco a injetar ───────────────────────────────────────────────────
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

# Opções do seletor de mês
mes_options = ''
mes_options += '<optgroup label="── FYTD25 (Jul/24–Mar/25) ──">'
for m in FYTD25_MESES:
    mes_options += f'<option value="{m}">{MESES_LABEL[m]}</option>'
mes_options += '</optgroup>'
mes_options += '<optgroup label="── FYTD26 (Jul/25–Mar/26) ──">'
for m in FYTD26_MESES:
    sel = ' selected' if m == '202603' else ''
    mes_options += f'<option value="{m}"{sel}>{MESES_LABEL[m]}</option>'
mes_options += '</optgroup>'

NEW_BLOCK = f"""
<!-- INTOCÁVEIS × GRUPO PROVEDOR — SELL OUT -->
<script>
{js}
</script>

<div id="intoc-grupos-card" class="card full" style="margin-bottom:14px;">
  <div class="card-header" style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:12px;margin-bottom:16px;">
    <div>
      <div style="font-size:10px;font-weight:700;letter-spacing:0.1em;color:#fbbf24;margin-bottom:4px;">🏆 INTOCÁVEIS × GRUPO PROVEDOR — SELL OUT</div>
      <div class="card-title">Distribuição Numérica dos 3 SKUs Intocáveis</div>
      <div class="card-sub" id="intoc-g-sub">OFF Loção 200ml · OFF Spray 170ml · OFF Kids 200ml · Fonte: vendas por EAN</div>
    </div>
    <!-- Toggle período -->
    <div style="display:flex;gap:8px;align-items:center;flex-wrap:wrap;">
      <div class="toggle-group">
        <button class="tgl" onclick="setIntocGPeriodo('fytd25',this)">FYTD25</button>
        <button class="tgl active blue" onclick="setIntocGPeriodo('fytd26',this)">FYTD26</button>
        <button class="tgl" onclick="setIntocGPeriodo('mes',this)">Por Mês</button>
      </div>
      <!-- Seletor de mês (visível só quando modo=mes) -->
      <select id="intoc-g-mes-sel" onchange="renderIntocGruposCard()"
        style="display:none;font-size:11px;padding:5px 22px 5px 8px;border-radius:7px;
               border:0.5px solid rgba(251,191,36,0.3);background:#161B22;color:#e2e8f0;
               cursor:pointer;font-family:inherit;appearance:none;
               background-image:url('data:image/svg+xml,%3Csvg xmlns=\\'http://www.w3.org/2000/svg\\' width=\\'10\\' height=\\'6\\'%3E%3Cpath d=\\'M0 0l5 6 5-6z\\' fill=\\'%23fbbf24\\'/%3E%3C/svg%3E');
               background-repeat:no-repeat;background-position:right 8px center;">
        {mes_options}
      </select>
    </div>
  </div>

  <!-- Filtro Grupo -->
  <div style="display:flex;align-items:center;gap:10px;margin-bottom:14px;flex-wrap:wrap;">
    <span style="font-size:9px;font-weight:700;color:#475569;text-transform:uppercase;letter-spacing:0.06em;white-space:nowrap;">GRUPO:</span>
    <select id="intoc-g-grupo-sel" onchange="renderIntocGruposCard()"
      style="font-size:11px;padding:5px 28px 5px 10px;border-radius:7px;
             border:0.5px solid rgba(251,191,36,0.3);background:#161B22;color:#e2e8f0;
             cursor:pointer;font-family:inherit;appearance:none;min-width:220px;
             background-image:url('data:image/svg+xml,%3Csvg xmlns=\\'http://www.w3.org/2000/svg\\' width=\\'10\\' height=\\'6\\'%3E%3Cpath d=\\'M0 0l5 6 5-6z\\' fill=\\'%23fbbf24\\'/%3E%3C/svg%3E');
             background-repeat:no-repeat;background-position:right 10px center;">
    </select>
    <span id="intoc-g-badge" style="font-size:10px;font-weight:700;padding:3px 10px;border-radius:6px;background:rgba(251,191,36,0.1);color:#fbbf24;border:0.5px solid rgba(251,191,36,0.3);"></span>
  </div>

  <!-- Sub-tabs SKU -->
  <div id="intoc-g-tabs" style="display:flex;gap:6px;margin-bottom:14px;flex-wrap:wrap;"></div>

  <!-- Corpo: barras DN -->
  <div id="intoc-g-body"></div>
</div>

<script>
(function(){{
  var _igPeriodo = 'fytd26';
  var _igSku     = 'soma';
  var _igGrupo   = null;

  var SKU_NOMES = {{
    soma:     'Somatório (qualquer Intocável)',
    kids200:  'OFF Kids Loção 200ML',
    spray170: 'OFF Spray Family 170ML',
    locao200: 'OFF Loção 200ML 30% desc',
  }};

  var MESES_LABEL = {{}};
  var FYTD25 = {FYTD25_MESES};
  var FYTD26 = {FYTD26_MESES};
  {'; '.join([f'MESES_LABEL["{m}"] = "{MESES_LABEL[m]}"' for m in FYTD25_MESES + FYTD26_MESES])};

  // Preencher dropdown de grupos (só grupos com ≥10 PDVs em FYTD26)
  function populateGrupos(){{
    var sel = document.getElementById('intoc-g-grupo-sel');
    if(!sel || sel.options.length > 1) return;
    var grupos = Object.keys(DN_INTOC_GRUPOS).sort();
    // grupos com >=10 PDVs FYTD26 primeiro, depois resto
    var big = [], small = [];
    grupos.forEach(function(g){{
      var d = DN_INTOC_GRUPOS[g];
      var tot = d.fytd26 ? d.fytd26.kids200.total : 0;
      if(tot >= 10) big.push(g); else small.push(g);
    }});
    big.sort(function(a,b){{
      return (DN_INTOC_GRUPOS[b].fytd26.kids200.total) - (DN_INTOC_GRUPOS[a].fytd26.kids200.total);
    }});
    var html = '<optgroup label="── Grupos representativos (≥10 PDVs) ──">';
    big.forEach(function(g){{
      var tot = DN_INTOC_GRUPOS[g].fytd26.kids200.total;
      html += '<option value="'+g+'">'+g+' ('+tot.toLocaleString('pt-BR')+' PDVs)</option>';
    }});
    html += '</optgroup>';
    if(small.length){{
      html += '<optgroup label="── Grupos menores ──">';
      small.forEach(function(g){{ html += '<option value="'+g+'">'+g+'</option>'; }});
      html += '</optgroup>';
    }}
    sel.innerHTML = html;
    _igGrupo = big[0] || grupos[0];
    sel.value = _igGrupo;
  }}

  window.setIntocGPeriodo = function(p, btn){{
    _igPeriodo = p;
    document.querySelectorAll('.toggle-group button').forEach(function(b){{
      if(b.getAttribute('onclick') && b.getAttribute('onclick').indexOf('setIntocGPeriodo') >= 0)
        b.classList.remove('active','blue');
    }});
    if(btn){{ btn.classList.add('active','blue'); }}
    var mesSel = document.getElementById('intoc-g-mes-sel');
    if(mesSel) mesSel.style.display = p === 'mes' ? 'block' : 'none';
    renderIntocGruposCard();
  }};

  function getDados(grupo, periodo, skuKey){{
    var d = DN_INTOC_GRUPOS[grupo];
    if(!d) return null;
    if(periodo === 'fytd25') return d.fytd25 ? d.fytd25[skuKey] : null;
    if(periodo === 'fytd26') return d.fytd26 ? d.fytd26[skuKey] : null;
    // mes
    var m = document.getElementById('intoc-g-mes-sel');
    var mes = m ? m.value : '202603';
    return d.meses && d.meses[mes] ? d.meses[mes][skuKey] : null;
  }}

  function getDadosSoma(grupo, periodo){{
    var d = DN_INTOC_GRUPOS[grupo];
    if(!d) return null;
    if(periodo === 'fytd25') return d.fytd25 ? d.fytd25.soma : null;
    if(periodo === 'fytd26') return d.fytd26 ? d.fytd26.soma : null;
    var m = document.getElementById('intoc-g-mes-sel');
    var mes = m ? m.value : '202603';
    if(d.meses && d.meses[mes]){{
      var md = d.meses[mes];
      return {{total:md.total, algum:0, dnAlgum:md.soma_dn, dois:0, dnDois:0, todos:0, dnTodos:0}};
    }}
    return null;
  }}

  window.renderIntocGruposCard = function(){{
    populateGrupos();
    var sel = document.getElementById('intoc-g-grupo-sel');
    if(sel) _igGrupo = sel.value;
    if(!_igGrupo || !DN_INTOC_GRUPOS[_igGrupo]) return;

    var d = DN_INTOC_GRUPOS[_igGrupo];

    // Badge total
    var badge = document.getElementById('intoc-g-badge');
    var tot26 = d.fytd26 && d.fytd26.kids200 ? d.fytd26.kids200.total : 0;
    if(badge) badge.textContent = tot26.toLocaleString('pt-BR') + ' PDVs (FYTD26)';

    // Sub-tabs SKU
    var tabsEl = document.getElementById('intoc-g-tabs');
    if(tabsEl){{
      var tabHtml = '';
      ['soma','kids200','spray170','locao200'].forEach(function(k){{
        var isAct = k === _igSku;
        var icon = k === 'soma' ? '∑' : '🏆';
        var nome = {{soma:'Somatório', kids200:'Kids 200ML', spray170:'Spray 170ML', locao200:'Loção 200ML'}}[k];
        tabHtml += '<button onclick="window._igSkuSet(\\''+k+'\\',this)" style="font-size:10px;font-weight:700;'
          +'padding:4px 12px;border-radius:6px;cursor:pointer;font-family:inherit;'
          +'border:0.5px solid '+(isAct?'rgba(251,191,36,0.4)':'rgba(255,255,255,0.07)')+';'
          +'background:'+(isAct?'rgba(251,191,36,0.15)':'transparent')+';'
          +'color:'+(isAct?'#fbbf24':'#64748b')+';">'
          +icon+' '+nome+'</button>';
      }});
      tabsEl.innerHTML = tabHtml;
    }}

    // Barras
    var bodyEl = document.getElementById('intoc-g-body');
    if(!bodyEl) return;

    var periodoLabel = _igPeriodo === 'fytd25' ? 'FYTD25 Jul/24–Mar/25'
                     : _igPeriodo === 'fytd26' ? 'FYTD26 Jul/25–Mar/26'
                     : (function(){{ var m = document.getElementById('intoc-g-mes-sel'); return m ? MESES_LABEL[m.value]||m.value : ''; }})();

    var html = '';

    if(_igSku === 'soma'){{
      // Modo somatório: mostrar os 3 SKUs lado a lado com comparativo
      var skus = ['kids200','spray170','locao200'];
      var nomes = {{kids200:'Kids 200ML',spray170:'Spray 170ML',locao200:'Loção 200ML'}};
      var cores  = {{kids200:'#fbbf24', spray170:'#34d399', locao200:'#60a5fa'}};

      html += '<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-bottom:16px;">';
      skus.forEach(function(sk){{
        var cur  = getDados(_igGrupo, _igPeriodo, sk);
        var comp = _igPeriodo === 'fytd26' ? getDados(_igGrupo,'fytd25',sk) :
                   _igPeriodo === 'fytd25' ? getDados(_igGrupo,'fytd26',sk) : null;
        var dn   = cur ? cur.dn  : 0;
        var dnC  = comp ? comp.dn : null;
        var pdvs = cur ? cur.pdvs : 0;
        var tot  = cur ? cur.total : 0;
        var cor  = cores[sk];
        var delta = (dnC !== null) ? (dn - dnC) : null;
        var deltaStr = delta !== null ? (delta >= 0 ? '+' : '') + delta.toFixed(1) + 'pp vs '
                       + (_igPeriodo === 'fytd26' ? 'FYTD25' : 'FYTD26') : '';
        var deltaCor = delta !== null ? (delta >= 0 ? '#34d399' : '#ef4444') : '#94a3b8';
        var dnCor = dn >= 50 ? '#34d399' : dn >= 30 ? '#fbbf24' : '#ef4444';

        html += '<div style="background:#161B22;border-radius:10px;padding:14px;border-top:2px solid '+cor+';">';
        html += '<div style="font-size:9px;font-weight:700;color:#475569;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:8px;">'+nomes[sk]+'</div>';
        html += '<div style="font-size:28px;font-weight:800;color:'+dnCor+';line-height:1;">'+dn.toFixed(1)+'%</div>';
        html += '<div style="font-size:10px;color:#94a3b8;margin-top:4px;">'+pdvs.toLocaleString('pt-BR')+' positivados / '+tot.toLocaleString('pt-BR')+' PDVs</div>';
        if(delta !== null) html += '<div style="font-size:10px;font-weight:700;color:'+deltaCor+';margin-top:6px;">'+deltaStr+'</div>';

        // Mini barra
        var pct = Math.min(dn, 100);
        html += '<div style="margin-top:10px;height:4px;background:rgba(255,255,255,0.06);border-radius:2px;">';
        html += '<div style="width:'+pct+'%;height:4px;background:'+cor+';border-radius:2px;"></div>';
        html += '</div></div>';
      }});
      html += '</div>';

      // Tabela de meses (histórico)
      html += '<div style="margin-top:4px;">';
      html += '<div style="font-size:9px;font-weight:700;color:#475569;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:8px;">EVOLUÇÃO MENSAL</div>';
      html += '<div style="display:grid;grid-template-columns:80px repeat(18,1fr);gap:2px;font-size:9px;">';
      // Header meses
      html += '<div></div>';
      var todosMs = {FYTD25_MESES + FYTD26_MESES};
      todosMs.forEach(function(m){{
        var isFY26 = {FYTD26_MESES}.indexOf(m) >= 0;
        html += '<div style="text-align:center;color:'+(isFY26?'#60a5fa':'#94a3b8')+';font-weight:700;white-space:nowrap;padding-bottom:2px;">'+(MESES_LABEL[m]||m)+'</div>';
      }});
      // Linhas por SKU
      skus.forEach(function(sk){{
        html += '<div style="color:'+cores[sk]+';font-weight:700;padding:4px 0;">'+nomes[sk]+'</div>';
        todosMs.forEach(function(m){{
          var md = d.meses && d.meses[m] ? d.meses[m][sk] : null;
          var dn_m = md ? md.dn : null;
          var bg = dn_m === null ? 'transparent' : dn_m >= 50 ? 'rgba(52,211,153,0.15)' : dn_m >= 30 ? 'rgba(251,191,36,0.1)' : 'rgba(239,68,68,0.1)';
          var tc = dn_m === null ? '#475569' : dn_m >= 50 ? '#34d399' : dn_m >= 30 ? '#fbbf24' : '#ef4444';
          html += '<div style="text-align:center;background:'+bg+';border-radius:3px;padding:3px 1px;color:'+tc+';font-weight:600;">'+(dn_m !== null ? dn_m.toFixed(0)+'%' : '—')+'</div>';
        }});
      }});
      html += '</div></div>';

    }} else {{
      // Modo SKU único: barra grande + histórico
      var cur  = getDados(_igGrupo, _igPeriodo, _igSku);
      var dn   = cur ? cur.dn   : 0;
      var pdvs = cur ? cur.pdvs : 0;
      var tot  = cur ? cur.total : 0;
      var gap  = tot - pdvs;
      var dnCor = dn >= 50 ? '#34d399' : dn >= 30 ? '#fbbf24' : '#ef4444';

      html += '<div style="display:flex;align-items:center;gap:20px;margin-bottom:16px;flex-wrap:wrap;">';
      html += '<div style="font-size:48px;font-weight:800;color:'+dnCor+';line-height:1;">'+dn.toFixed(1)+'%</div>';
      html += '<div>';
      html += '<div style="font-size:12px;color:#94a3b8;">'+pdvs.toLocaleString('pt-BR')+' PDVs positivaram o SKU</div>';
      html += '<div style="font-size:12px;color:#94a3b8;">'+tot.toLocaleString('pt-BR')+' PDVs total no grupo</div>';
      html += '<div style="font-size:12px;color:#ef4444;font-weight:700;">'+gap.toLocaleString('pt-BR')+' PDVs SEM o SKU — oportunidade</div>';
      html += '</div></div>';

      // Barra visual
      html += '<div style="background:rgba(255,255,255,0.05);border-radius:8px;height:12px;margin-bottom:16px;">';
      html += '<div style="width:'+Math.min(dn,100).toFixed(1)+'%;height:12px;background:'+dnCor+';border-radius:8px;transition:width 0.4s;"></div>';
      html += '</div>';

      // Tabela mensal
      html += '<div style="font-size:9px;font-weight:700;color:#475569;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:8px;">EVOLUÇÃO MENSAL — '+SKU_NOMES[_igSku]+'</div>';
      html += '<div style="display:grid;grid-template-columns:repeat(9,1fr);gap:6px;">';
      [{{'meses': FYTD25_MESES, 'label': 'FYTD25', 'cor': '#94a3b8'}},
       {{'meses': FYTD26_MESES, 'label': 'FYTD26', 'cor': '#60a5fa'}}].forEach(function(grp){{
        grp.meses.forEach(function(m){{
          var md = d.meses && d.meses[m] ? d.meses[m][_igSku] : null;
          var dn_m = md ? md.dn : null;
          var bg = dn_m === null ? 'rgba(255,255,255,0.03)' : dn_m >= 50 ? 'rgba(52,211,153,0.12)' : dn_m >= 30 ? 'rgba(251,191,36,0.1)' : 'rgba(239,68,68,0.1)';
          var tc = dn_m === null ? '#475569' : dn_m >= 50 ? '#34d399' : dn_m >= 30 ? '#fbbf24' : '#ef4444';
          html += '<div style="background:'+bg+';border-radius:6px;padding:8px 4px;text-align:center;">';
          html += '<div style="font-size:8px;color:'+grp.cor+';font-weight:700;margin-bottom:4px;">'+MESES_LABEL[m]+'</div>';
          html += '<div style="font-size:14px;font-weight:800;color:'+tc+';line-height:1;">'+(dn_m !== null ? dn_m.toFixed(0)+'%' : '—')+'</div>';
          if(md) html += '<div style="font-size:8px;color:#475569;margin-top:2px;">'+md.pdvs+'/'+md.total+'</div>';
          html += '</div>';
        }});
      }});
      html += '</div>';
    }}

    bodyEl.innerHTML = html;
  }};

  window._igSkuSet = function(k, btn){{
    _igSku = k;
    renderIntocGruposCard();
  }};

  // Init
  document.addEventListener('DOMContentLoaded', function(){{
    if(typeof DN_INTOC_GRUPOS !== 'undefined') renderIntocGruposCard();
  }});
  if(typeof DN_INTOC_GRUPOS !== 'undefined' && document.readyState !== 'loading') renderIntocGruposCard();
}})();
</script>
"""

# ── Injetar antes do card de Verbas ──────────────────────────────────────────
ANCHOR = '\n  <!-- VERBAS -->'
assert ANCHOR in h, 'ERRO: âncora <!-- VERBAS --> não encontrada'
h = h.replace(ANCHOR, NEW_BLOCK + ANCHOR, 1)
print('OK: card INTOCÁVEIS × GRUPO PROVEDOR injetado')

# ── Salvar ────────────────────────────────────────────────────────────────────
DASH.write_text(h, encoding='utf-8')
shutil.copy(DASH, VER / f'Dashboard_Farma_Sul_{ts}_DnGrupos.html')
shutil.copy(DASH, DL  / f'Dashboard_FarmaSul_Giovano_{ts}.html')
print(f'\nVersao:    Dashboard_Farma_Sul_{ts}_DnGrupos.html')
print(f'Downloads: Dashboard_FarmaSul_Giovano_{ts}.html')
print('DONE.')
