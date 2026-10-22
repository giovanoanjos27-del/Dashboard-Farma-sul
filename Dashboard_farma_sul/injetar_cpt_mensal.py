#!/usr/bin/env python3
"""
Injeta dados mensais CPT (FY25 + FY26) no dashboard OLs tab.
- Adiciona mensal25/mensal26 ao GC_DATA.SCJ
- Insere card "Venda Mês a Mês no Calendário Fiscal da SCJ" após o card Grupo Cadeia
"""
import sys, os, shutil, pandas as pd
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

DASH = r'C:\Users\valqu\OneDrive\Documentos\Claude\Projects\projeto Dashboard_farma_sul\Dashboard_farma_sul\Dashboard_Farma_Sul_20260512_2220.html'
VER_DIR = r'C:\Users\valqu\OneDrive\Documentos\Claude\Projects\projeto Dashboard_farma_sul\Dashboard_farma_sul\versoes'
DOWNLOADS = os.path.join(os.path.expanduser('~'), 'Downloads')
XL = r'C:\Users\valqu\OneDrive\Documentos\Claude\Projects\projeto Dashboard_farma_sul\Dashboard_farma_sul\_Recursos\Giovano SCJ\cpt\fechamento fy25 x fy26 repelentes CPT .xlsx'

# ── Ler dashboard ──────────────────────────────────────────────────
with open(DASH, encoding='utf-8') as f:
    html = f.read()

# ── Verificar se override já existe ─────────────────────────────────
if '// === GC MONTHLY CPT ===' in html:
    print('Override GC MONTHLY CPT já existe — removendo antes de reinjetar...')
    start = html.index('// === GC MONTHLY CPT ===')
    end   = html.index('// === end GC MONTHLY CPT ===') + len('// === end GC MONTHLY CPT ===')
    html  = html[:start] + html[end:]

if 'id="ol-cpt-mensal-card"' in html:
    print('Card CPT mensal já existe — removendo antes de reinjetar...')
    START_TAG = '<!-- ══ CARD VENDA MÊS A MÊS CALENDÁRIO FISCAL SCJ ══ -->'
    END_TAG   = '<!-- ══ end CARD VENDA MÊS A MÊS ══ -->'
    if START_TAG in html and END_TAG in html:
        s = html.index(START_TAG)
        e = html.index(END_TAG) + len(END_TAG)
        html = html[:s] + html[e:]

# ── Calcular dados mensais ───────────────────────────────────────────
df = pd.read_excel(XL, sheet_name='Base', header=1)
scj = df[df['Grupo de Produtos'] == 'SCJ'].copy()

FY25 = [202407,202408,202409,202410,202411,202412,202501,202502,202503,202504,202505,202506]
FY26 = [202507,202508,202509,202510,202511,202512,202601,202602,202603,202604,202605,202606]

mapping = {
    'ARAUJO':      'GRUPO DROGARIA ARAUJO',
    'CLAMED':      'GRUPO CLAMED',
    'DPSP':        'GRUPO DPSP',
    'DROGAL':      'GRUPO DROGAL',
    'FARMA CONDE': 'FARMA CONDE REDE',
    'GLOBO':       None,
    'INDIANA':     'GRUPO INDIANA',
    'NISSEI':      'GRUPO NISSEI SA',
    'PAGUE MENOS': 'GRUPO PAGUE MENOS',
    'PANVEL':      'GRUPO PANVEL',
    'PROFARMA':    None,
    'RD':          'GRUPO RAIA DROGASIL',
    'REDEPHARMA':  'GRUPO REDEPHARMA',
    'SÃO JOÃO':    'GRUPO SAO JOAO',
    'VENÂNCIO':    'GRUPO VENANCIO',
}
val_col = 'Métrica Período Laboratório Analitico Bandeira'

def get_monthly(excel_nome):
    if excel_nome is None:
        return [0]*12, [0]*12
    sub = scj[scj['Grupo Econômico'] == excel_nome]
    m25 = [round(sub[sub['Mês']==m][val_col].sum()/1000, 1) for m in FY25]
    m26 = [round(sub[sub['Mês']==m][val_col].sum()/1000, 1) for m in FY26]
    return m25, m26

grupo_data = {}
for dash_nome, excel_nome in mapping.items():
    m25, m26 = get_monthly(excel_nome)
    grupo_data[dash_nome] = {'mensal25': m25, 'mensal26': m26}

# ── Gerar JS override ────────────────────────────────────────────────
js_lines = ['// === GC MONTHLY CPT ===']
for dash_nome, data in grupo_data.items():
    m25_str = '[' + ','.join(str(v) for v in data['mensal25']) + ']'
    m26_str = '[' + ','.join(str(v) for v in data['mensal26']) + ']'
    nome_escaped = dash_nome.replace("'", "\\'")
    js_lines.append(
        f"(function(){{ var g=GC_DATA.SCJ.grupos.find(function(x){{return x.nome==='{nome_escaped}';}});"
        f"if(g){{g.mensal25={m25_str};g.mensal26={m26_str};}} }})();"
    )
js_lines.append('// === end GC MONTHLY CPT ===')
js_override = '\n'.join(js_lines)

# ── Gerar HTML do novo card ──────────────────────────────────────────
# Cores por grupo
COLORS = [
    '#34d399','#f59e0b','#60a5fa','#f472b6','#a78bfa',
    '#fb923c','#2dd4bf','#fbbf24','#4ade80','#c084fc',
    '#38bdf8','#f87171','#e879f9','#86efac','#fdba74'
]
grupos_js_list = list(mapping.keys())
# Excluir grupos sem dados CPT do gráfico (mas manter na tabela como 0)

card_html = '''
<!-- ══ CARD VENDA MÊS A MÊS CALENDÁRIO FISCAL SCJ ══ -->
<div class="card full" id="ol-cpt-mensal-card" style="padding:20px;margin-bottom:14px;border:1px solid rgba(245,225,164,0.25);background:linear-gradient(135deg,#0D1117 0%,#111827 100%);">
  <div class="card-header" style="margin-bottom:18px;">
    <div>
      <div style="font-size:10px;font-weight:700;letter-spacing:0.1em;color:#F5E1A4;margin-bottom:4px;">CPT · VENDA MÊS A MÊS · CALENDÁRIO FISCAL</div>
      <div class="card-title">Venda Mês a Mês no Calendário Fiscal da SCJ</div>
      <div class="card-sub">FY25 Jul/24–Jun/25 · FY26 Jul/25–Jun/26 · Valor R$K · Fonte: CPT SCJ · Grupo Econômico</div>
    </div>
    <div style="display:flex;align-items:center;gap:10px;flex-shrink:0;">
      <div style="display:flex;align-items:center;gap:8px;">
        <span style="font-size:9px;font-weight:700;letter-spacing:0.1em;color:#F5E1A4;text-transform:uppercase;white-space:nowrap;">Grupo</span>
        <select id="ol-cpt-sel-grupo" onchange="renderCPTMensal()"
          style="font-size:11px;font-weight:600;padding:6px 24px 6px 10px;border-radius:7px;
                 border:1px solid rgba(245,225,164,0.4);background:#161B22;color:#F5E1A4;
                 cursor:pointer;appearance:none;-webkit-appearance:none;min-width:140px;
                 background-image:url(\\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='10' height='6'%3E%3Cpath d='M0 0l5 6 5-6z' fill='%23F5E1A4'/%3E%3C/svg%3E\\");
                 background-repeat:no-repeat;background-position:right 8px center;">
          <option value="TODOS">Todos os Grupos</option>
          <option value="ARAUJO">ARAÚJO</option>
          <option value="CLAMED">CLAMED</option>
          <option value="DPSP">DPSP</option>
          <option value="DROGAL">DROGAL</option>
          <option value="FARMA CONDE">FARMA CONDE</option>
          <option value="INDIANA">INDIANA</option>
          <option value="NISSEI">NISSEI</option>
          <option value="PAGUE MENOS">PAGUE MENOS</option>
          <option value="PANVEL">PANVEL</option>
          <option value="RD">RD (Raia Drogasil)</option>
          <option value="REDEPHARMA">REDEPHARMA</option>
          <option value="SÃO JOÃO">SÃO JOÃO</option>
          <option value="VENÂNCIO">VENÂNCIO</option>
        </select>
      </div>
      <div class="toggle-group" id="ol-cpt-view-toggle">
        <button class="tgl on" id="ol-cpt-btn-chart" onclick="setCPTView('chart',this)">📊 Gráfico</button>
        <button class="tgl" id="ol-cpt-btn-table" onclick="setCPTView('table',this)">📋 Tabela</button>
      </div>
    </div>
  </div>
  <!-- KPIs -->
  <div id="ol-cpt-kpis" style="display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin-bottom:18px;"></div>
  <!-- Chart view -->
  <div id="ol-cpt-chart-view">
    <div style="position:relative;height:320px;"><canvas id="ol-cpt-canvas"></canvas></div>
    <div id="ol-cpt-insight" style="margin-top:12px;padding:10px 14px;background:rgba(245,225,164,0.04);border:0.5px solid rgba(245,225,164,0.15);border-radius:8px;font-size:11px;color:#94A3B8;line-height:1.7;"></div>
  </div>
  <!-- Table view -->
  <div id="ol-cpt-table-view" style="display:none;overflow-x:auto;">
    <table id="ol-cpt-table" style="width:100%;border-collapse:collapse;font-size:11px;">
      <thead id="ol-cpt-thead"></thead>
      <tbody id="ol-cpt-tbody"></tbody>
    </table>
  </div>
</div>
<!-- ══ end CARD VENDA MÊS A MÊS ══ -->
'''

# ── JS para renderização do card ─────────────────────────────────────
js_render = '''
<script>
/* ── CPT MENSAL render ─────────────────────────────────────────── */
var _cptChart = null;
var _cptView  = 'chart';
var _CPT_COLORS = [
  '#34d399','#f59e0b','#60a5fa','#f472b6','#a78bfa',
  '#fb923c','#2dd4bf','#fbbf24','#4ade80','#c084fc',
  '#38bdf8','#f87171','#e879f9','#86efac','#fdba74'
];
var _FY_LABELS = ['Jul','Ago','Set','Out','Nov','Dez','Jan','Fev','Mar','Abr','Mai','Jun'];

function setCPTView(v, btn){
  _cptView = v;
  document.querySelectorAll('#ol-cpt-view-toggle .tgl').forEach(function(b){ b.classList.remove('on'); });
  if(btn) btn.classList.add('on');
  document.getElementById('ol-cpt-chart-view').style.display = (v==='chart') ? '' : 'none';
  document.getElementById('ol-cpt-table-view').style.display = (v==='table') ? '' : 'none';
  renderCPTMensal();
}

function renderCPTMensal(){
  var sel   = document.getElementById('ol-cpt-sel-grupo');
  var grupo = sel ? sel.value : 'TODOS';
  var kpisEl = document.getElementById('ol-cpt-kpis');
  var insEl  = document.getElementById('ol-cpt-insight');

  /* Grupos a exibir */
  var gruposLista = GC_DATA.SCJ.grupos.filter(function(g){
    return g.mensal25 && g.mensal26;
  });
  if(grupo !== 'TODOS'){
    gruposLista = gruposLista.filter(function(g){ return g.nome === grupo; });
  }

  /* Totais por mês */
  var tot25 = new Array(12).fill(0);
  var tot26 = new Array(12).fill(0);
  gruposLista.forEach(function(g){
    for(var i=0;i<12;i++){
      tot25[i] = Math.round((tot25[i] + (g.mensal25[i]||0))*10)/10;
      tot26[i] = Math.round((tot26[i] + (g.mensal26[i]||0))*10)/10;
    }
  });

  var sum25 = Math.round(tot25.reduce(function(a,b){return a+b;},0));
  var sum26 = Math.round(tot26.reduce(function(a,b){return a+b;},0));
  var varTot = sum25>0 ? ((sum26-sum25)/sum25*100) : 0;

  /* Melhor e pior mês FY26 vs FY25 */
  var bestI = -1, bestG = -Infinity, worstI = -1, worstG = Infinity;
  for(var i=0;i<12;i++){
    if(tot25[i]>0){
      var g=(tot26[i]-tot25[i])/tot25[i]*100;
      if(g>bestG){bestG=g;bestI=i;}
      if(g<worstG){worstG=g;worstI=i;}
    }
  }

  function fK(v){ return v>=1000?'R$'+(v/1000).toFixed(1)+'M':'R$'+Math.round(v)+'K'; }
  function fPct(v){ return (v>=0?'+':'')+v.toFixed(1)+'%'; }
  function col(v){ return v>=0?'#34d399':'#ef4444'; }

  /* KPIs */
  var kd = [
    { tag:'FY26 TOTAL',    val:fK(sum26),          sub:'FY25: '+fK(sum25),           dlt:fPct(varTot), c:col(varTot) },
    { tag:'GRUPOS',        val:gruposLista.length,  sub:'com dados CPT',              dlt:'',           c:'#F5E1A4'   },
    { tag:'MELHOR MÊS',    val:bestI>=0?_FY_LABELS[bestI]:'—', sub:'FY26 vs FY25',   dlt:bestI>=0?fPct(bestG):'—', c:'#34d399' },
    { tag:'QUEDA MAIOR',   val:worstI>=0?_FY_LABELS[worstI]:'—', sub:'FY26 vs FY25', dlt:worstI>=0?fPct(worstG):'—', c:'#ef4444' }
  ];
  kpisEl.innerHTML = kd.map(function(k){
    return '<div style="background:#161B22;border-top:3px solid '+k.c+';border-radius:10px;padding:14px 16px;">'
      +'<div style="font-size:9px;font-weight:700;letter-spacing:0.1em;color:#475569;text-transform:uppercase;margin-bottom:6px;">'+k.tag+'</div>'
      +'<div style="font-size:20px;font-weight:700;color:'+k.c+';">'+k.val+'</div>'
      +'<div style="font-size:10px;color:#64748B;margin-top:3px;">'+k.sub+'</div>'
      +(k.dlt?'<div style="font-size:10px;font-weight:600;color:'+k.c+';margin-top:2px;">'+k.dlt+'</div>':'')
      +'</div>';
  }).join('');

  if(_cptView === 'chart'){
    /* Destruir chart anterior */
    if(_cptChart){ _cptChart.destroy(); _cptChart=null; }
    var ctx = document.getElementById('ol-cpt-canvas');
    if(!ctx) return;

    var datasets = [];
    if(grupo === 'TODOS'){
      /* Linha total FY25 e FY26 */
      datasets.push({label:'FY26 Total',data:tot26,borderColor:'#34d399',backgroundColor:'rgba(52,211,153,0.12)',pointBackgroundColor:'#34d399',borderWidth:2.5,tension:0.4,fill:true,pointRadius:3,pointHoverRadius:6});
      datasets.push({label:'FY25 Total',data:tot25,borderColor:'#3b82f6',backgroundColor:'rgba(59,130,246,0.08)',pointBackgroundColor:'#3b82f6',borderWidth:2,tension:0.4,fill:true,pointRadius:3,pointHoverRadius:5,borderDash:[4,3]});
    } else {
      /* Linha única por grupo */
      gruposLista.forEach(function(g, idx){
        var c = _CPT_COLORS[idx % _CPT_COLORS.length];
        datasets.push({label:g.nome+' FY26',data:g.mensal26,borderColor:c,backgroundColor:c.replace(')',',0.12)').replace('rgb','rgba'),pointBackgroundColor:c,borderWidth:2.5,tension:0.4,fill:true,pointRadius:3,pointHoverRadius:6});
        datasets.push({label:g.nome+' FY25',data:g.mensal25,borderColor:c,backgroundColor:'transparent',pointBackgroundColor:c,borderWidth:1.5,tension:0.4,fill:false,pointRadius:2,pointHoverRadius:4,borderDash:[4,3]});
      });
    }

    _cptChart = new Chart(ctx, {
      type:'line',
      data:{ labels:_FY_LABELS, datasets:datasets },
      options:{
        responsive:true, maintainAspectRatio:false,
        interaction:{ mode:'index', intersect:false },
        plugins:{
          legend:{ position:'top', labels:{color:'#94A3B8',font:{size:11},boxWidth:14,padding:12} },
          tooltip:{
            backgroundColor:'#1E293B',borderColor:'rgba(94,153,208,0.4)',borderWidth:1,
            titleColor:'#F5E1A4',bodyColor:'#D1D5DB',padding:10,
            callbacks:{ label:function(ctx){ return ctx.dataset.label+': R$'+(ctx.parsed.y).toFixed(1)+'K'; } }
          }
        },
        scales:{
          x:{ grid:{color:'rgba(255,255,255,0.05)'}, ticks:{color:'#64748B',font:{size:10}} },
          y:{ grid:{color:'rgba(255,255,255,0.05)'}, ticks:{color:'#64748B',font:{size:10},callback:function(v){ return 'R$'+(v>=1000?(v/1000).toFixed(0)+'M':v+'K'); } } }
        }
      }
    });

    /* Insight */
    var insGrupoLabel = grupo==='TODOS'?'todos os grupos ('+gruposLista.length+')':grupo;
    insEl.innerHTML = '<strong style="color:#F5E1A4;font-size:10px;letter-spacing:.08em;">📊 DIAGNÓSTICO CPT — '+insGrupoLabel.toUpperCase()+'</strong><br>'
      +'💰 <strong>FY26 Total</strong>: <strong style="color:'+col(varTot)+';">'+fK(sum26)+'</strong>'
      +' vs FY25 <strong style="color:#94A3B8;">'+fK(sum25)+'</strong>'
      +' <span style="color:'+col(varTot)+';">('+fPct(varTot)+')</span><br>'
      +(bestI>=0?'📈 <strong>Melhor mês FY26</strong>: <strong style="color:#34d399;">'+_FY_LABELS[bestI]+'</strong> com <span style="color:#34d399;">'+fPct(bestG)+'</span> vs FY25<br>':'')
      +(worstI>=0?'📉 <strong>Pior mês FY26</strong>: <strong style="color:#ef4444;">'+_FY_LABELS[worstI]+'</strong> com <span style="color:#ef4444;">'+fPct(worstG)+'</span> vs FY25<br>':'')
      +'<span style="font-size:9px;color:#475569;">Fonte: CPT SCJ · Valores em R$K · FY25: Jul/24–Jun/25 · FY26: Jul/25–Jun/26</span>';

  } else {
    /* Tabela */
    var thead = document.getElementById('ol-cpt-thead');
    var tbody = document.getElementById('ol-cpt-tbody');
    var hdrStyle = 'style="padding:7px 8px;text-align:right;color:#475569;font-weight:700;border-bottom:1px solid rgba(94,153,208,0.3);font-size:10px;"';
    thead.innerHTML = '<tr><th style="padding:7px 10px;text-align:left;color:#1D6FA8;font-weight:700;border-bottom:1px solid rgba(94,153,208,0.3);">Grupo</th>'
      +'<th '+hdrStyle+'>FY (Total)</th>'
      + _FY_LABELS.map(function(l){ return '<th '+hdrStyle+'>'+l+'</th>'; }).join('')
      +'</tr>';

    var rows = '';
    // Add FY25 and FY26 rows per grupo
    var cols25 = gruposLista.map(function(g){ return { nome:g.nome, data:g.mensal25, fy:25 }; });
    var cols26 = gruposLista.map(function(g){ return { nome:g.nome, data:g.mensal26, fy:26 }; });

    // Total rows
    function totRow(label, totArr, fyColor){
      var total = Math.round(totArr.reduce(function(a,b){return a+b;},0));
      return '<tr style="border-bottom:1px solid rgba(94,153,208,0.25);background:rgba(245,225,164,0.04);">'
        +'<td style="padding:7px 10px;font-weight:700;color:'+fyColor+';">'+label+'</td>'
        +'<td style="padding:7px 8px;text-align:right;font-weight:700;color:'+fyColor+';">'+fK(total)+'</td>'
        + totArr.map(function(v){ return '<td style="padding:7px 8px;text-align:right;color:'+fyColor+';font-weight:600;">'+fK(v)+'</td>'; }).join('')
        +'</tr>';
    }
    rows += totRow('TOTAL FY25', tot25, '#3b82f6');
    rows += totRow('TOTAL FY26', tot26, '#34d399');

    // Var row
    var varRow = '<tr style="border-bottom:2px solid rgba(94,153,208,0.3);background:rgba(52,211,153,0.04);">'
      +'<td style="padding:7px 10px;font-weight:700;color:#94A3B8;">VAR FY26 vs FY25</td>'
      +'<td style="padding:7px 8px;text-align:right;font-weight:700;color:'+col(varTot)+';">'+fPct(varTot)+'</td>'
      + tot25.map(function(v25,i){
          var v26=tot26[i]; var vv=v25>0?((v26-v25)/v25*100):0;
          return '<td style="padding:7px 8px;text-align:right;font-weight:600;color:'+col(vv)+';">'+fPct(vv)+'</td>';
        }).join('')
      +'</tr>';
    rows += varRow;

    // Detail rows per grupo
    if(grupo==='TODOS'){
      gruposLista.forEach(function(g, idx){
        var c = _CPT_COLORS[idx % _CPT_COLORS.length];
        var tot25g = Math.round(g.mensal25.reduce(function(a,b){return a+b;},0));
        var tot26g = Math.round(g.mensal26.reduce(function(a,b){return a+b;},0));
        var varG = tot25g>0?((tot26g-tot25g)/tot25g*100):0;
        rows += '<tr style="border-bottom:0.5px solid rgba(255,255,255,0.05);">'
          +'<td style="padding:6px 10px;font-weight:600;color:'+c+';">'+g.nome+'</td>'
          +'<td style="padding:6px 8px;text-align:right;color:#64748B;font-size:10px;">'+fK(tot25g)+' → '+fK(tot26g)+' <span style="color:'+col(varG)+';">'+fPct(varG)+'</span></td>'
          + g.mensal26.map(function(v,i){
              var v25=g.mensal25[i]; var vv=v25>0?((v-v25)/v25*100):0;
              return '<td style="padding:6px 8px;text-align:right;color:#94A3B8;font-size:10px;">'+fK(v)+'</td>';
            }).join('')
          +'</tr>';
      });
    }

    tbody.innerHTML = rows;
  }
}

/* Auto-render — patcha initOLTabs que é chamado toda vez que a aba OLs abre */
(function(){
  var _origInitOL = window.initOLTabs;
  window.initOLTabs = function(){
    if(_origInitOL) _origInitOL();
    setTimeout(function(){ if(typeof renderCPTMensal==='function') renderCPTMensal(); }, 200);
  };
  /* Também patcha switchClient por segurança */
  var _origSwitch = window.switchClient;
  window.switchClient = function(c, btn){
    if(_origSwitch) _origSwitch(c, btn);
    if(c === 'ol'){
      setTimeout(function(){ if(typeof renderCPTMensal==='function') renderCPTMensal(); }, 400);
    }
  };
  /* Fallback: se panel-ol já está visível ao carregar */
  window.addEventListener('load', function(){
    var p = document.getElementById('panel-ol');
    if(p && p.style.display !== 'none' && p.offsetParent !== null){
      setTimeout(renderCPTMensal, 600);
    }
  });
})();
</script>
'''

# ── Injetar override JS antes do ÚLTIMO </body> ──────────────────────
INSERT_JS_MARKER = '</body>'
last_body_pos = html.rfind(INSERT_JS_MARKER)
if last_body_pos == -1:
    print('ERRO: marcador </body> não encontrado!')
    sys.exit(1)

html = html[:last_body_pos] + f'\n<script>\n{js_override}\n</script>\n' + html[last_body_pos:]

# ── Injetar card HTML após o card ol-grupo-cadeia-card ──────────────
# Inserir após a div que fecha o card Grupo Cadeia (id=ol-grupo-cadeia-card)
# The card ends with </div> after ol-gc-insights div
INSERT_AFTER = '<!-- ══ OL ACOMPANHAMENTO 4-Tabs ══ -->'
if INSERT_AFTER not in html:
    print(f'ERRO: marcador "{INSERT_AFTER}" não encontrado!')
    sys.exit(1)

html = html.replace(INSERT_AFTER, card_html + '\n  ' + INSERT_AFTER, 1)

# ── Injetar script de render antes do ÚLTIMO </body> ─────────────────
last_body_pos2 = html.rfind('</body>')
html = html[:last_body_pos2] + js_render + '\n' + html[last_body_pos2:]

# ── Versão + saves ───────────────────────────────────────────────────
ts = datetime.now().strftime('%Y%m%d_%H%M')
ver_path = os.path.join(VER_DIR, f'Dashboard_Farma_Sul_{ts}.html')
dl_path  = os.path.join(DOWNLOADS, f'Dashboard_FarmaSul_Giovano_{ts}.html')

with open(DASH, 'w', encoding='utf-8') as f:
    f.write(html)
shutil.copy(DASH, ver_path)
shutil.copy(DASH, dl_path)

print(f'✅ Dashboard atualizado!')
print(f'   Versão: {ver_path}')
print(f'   Downloads: {dl_path}')
print(f'   Timestamp: {ts}')
