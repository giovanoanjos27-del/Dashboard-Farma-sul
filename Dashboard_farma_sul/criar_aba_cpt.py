#!/usr/bin/env python3
"""
Cria nova aba CPT Clientes no dashboard.
Tabela: Grupo Econômico × Mês (FY25+FY26) com SCJ / CIMED / RB / Total / Share.
"""
import sys, os, shutil, json, pandas as pd
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

DASH    = r'C:\Users\valqu\OneDrive\Documentos\Claude\Projects\projeto Dashboard_farma_sul\Dashboard_farma_sul\Dashboard_Farma_Sul_20260512_2220.html'
VER_DIR = r'C:\Users\valqu\OneDrive\Documentos\Claude\Projects\projeto Dashboard_farma_sul\Dashboard_farma_sul\versoes'
DOWNLOADS = os.path.join(os.path.expanduser('~'), 'Downloads')
XL = r'C:\Users\valqu\OneDrive\Documentos\Claude\Projects\projeto Dashboard_farma_sul\Dashboard_farma_sul\_Recursos\Giovano SCJ\cpt\fechamento fy25 x fy26 repelentes CPT .xlsx'

# ── Ler dashboard ──────────────────────────────────────────────────
with open(DASH, encoding='utf-8') as f:
    html = f.read()

# Verificar se já existe
if 'panel-cpt' in html:
    print('Aba CPT já existe — removendo para reinjetar...')
    # Remover botão
    import re
    html = re.sub(r"\s*<button[^>]*switchClient\('cpt'[^>]*>[^<]*</button>", '', html)
    # Remover painel
    if '<!-- ═══════════ CPT CLIENTES ═══════════ -->' in html:
        s = html.index('<!-- ═══════════ CPT CLIENTES ═══════════ -->')
        # Encontrar próximo painel
        e = html.find('<!-- ═══════════', s + 10)
        if e == -1:
            e = html.rfind('</body>')
        html = html[:s] + html[e:]
    # Remover script CPT
    if '// === CPT_CLI_DATA ===' in html:
        s = html.index('// === CPT_CLI_DATA ===')
        e = html.index('// === end CPT_CLI_DATA ===') + len('// === end CPT_CLI_DATA ===')
        html = html[:s] + html[e:]

# ── Ler e processar Excel ──────────────────────────────────────────
print('Lendo Excel...')
df = pd.read_excel(XL, sheet_name='Base', header=1)
print(f'  Linhas: {len(df)}')

FY25 = [202407,202408,202409,202410,202411,202412,202501,202502,202503,202504,202505,202506]
FY26 = [202507,202508,202509,202510,202511,202512,202601,202602,202603,202604,202605,202606]
ALL_MONTHS = FY25 + FY26

dem_col = 'Demanda Categoria'
grp_col = 'Grupo Econômico'
prod_col = 'Grupo de Produtos'
mes_col  = 'Mês'

# Agregar: soma Demanda Categoria por Grupo Econômico × Grupo de Produtos × Mês
agg = df[df[mes_col].isin(ALL_MONTHS)].groupby([grp_col, prod_col, mes_col])[dem_col].sum().reset_index()

# Pivotar: linhas=Grupo Econômico × Mês, colunas=Grupo de Produtos
piv = agg.pivot_table(index=[grp_col, mes_col], columns=prod_col, values=dem_col, fill_value=0).reset_index()
piv.columns.name = None
for col in ['SCJ', 'CIMED_OTHERS', 'RB_OTHERS']:
    if col not in piv.columns:
        piv[col] = 0

piv['TOTAL'] = piv['SCJ'] + piv['CIMED_OTHERS'] + piv['RB_OTHERS']

# Calcular SCJ FY26 por grupo para ordenação
fy26_scj = piv[piv[mes_col].isin(FY26)].groupby(grp_col)['SCJ'].sum().sort_values(ascending=False)
grupos_ordenados = fy26_scj.index.tolist()
print(f'  Grupos únicos: {len(grupos_ordenados)}')

# ── Construir JS data ──────────────────────────────────────────────
# Estrutura: CPT_CLI_DATA[grupo] = { fy25: [[cimed,scj,rb,tot]×12], fy26: [[cimed,scj,rb,tot]×12] }
def build_entry(grupo_df, months):
    result = []
    for m in months:
        row = grupo_df[grupo_df[mes_col] == m]
        if len(row) > 0:
            r = row.iloc[0]
            result.append([
                round(r['CIMED_OTHERS'], 2),
                round(r['SCJ'], 2),
                round(r['RB_OTHERS'], 2),
                round(r['TOTAL'], 2)
            ])
        else:
            result.append([0, 0, 0, 0])
    return result

print('Construindo JS data...')
js_entries = []
for grupo in grupos_ordenados:
    gdf = piv[piv[grp_col] == grupo]
    fy25_data = build_entry(gdf, FY25)
    fy26_data = build_entry(gdf, FY26)
    # Comprimir como array plano para economizar espaço
    # [c25,s25,r25,t25, c25,s25,...] × 12 meses FY25, depois × 12 FY26
    f25 = [[v for v in row] for row in fy25_data]
    f26 = [[v for v in row] for row in fy26_data]
    g_esc = grupo.replace('\\', '\\\\').replace("'", "\\'")
    js_entries.append(f"'{g_esc}':{{'f25':{json.dumps(f25)},'f26':{json.dumps(f26)}}}")

js_data = '// === CPT_CLI_DATA ===\nvar CPT_CLI_DATA = {\n  ' + ',\n  '.join(js_entries) + '\n};\n// === end CPT_CLI_DATA ==='
print(f'  JS data size: {len(js_data)/1024:.0f} KB')

# Lista de grupos para o select
grupos_lista_js = json.dumps(grupos_ordenados)

# ── HTML da nova aba ───────────────────────────────────────────────
MES_LABELS_FY25 = ['Jul/24','Ago/24','Set/24','Out/24','Nov/24','Dez/24','Jan/25','Fev/25','Mar/25','Abr/25','Mai/25','Jun/25']
MES_LABELS_FY26 = ['Jul/25','Ago/25','Set/25','Out/25','Nov/25','Dez/25','Jan/26','Fev/26','Mar/26','Abr/26','Mai/26','Jun/26']

panel_html = f'''
<!-- ═══════════ CPT CLIENTES ═══════════ -->

<div class="main" id="panel-cpt">

  <!-- Header card -->
  <div class="card full" style="padding:20px;margin-bottom:14px;border:1px solid rgba(245,225,164,0.3);background:linear-gradient(135deg,#0D1117 0%,#111827 100%);">
    <div class="card-header" style="margin-bottom:16px;">
      <div>
        <div style="font-size:10px;font-weight:700;letter-spacing:0.1em;color:#F5E1A4;margin-bottom:4px;">CPT · ANÁLISE POR GRUPO ECONÔMICO</div>
        <div class="card-title">CPT Clientes — SCJ × CIMED × RB</div>
        <div class="card-sub">FY25 Jul/24–Jun/25 · FY26 Jul/25–Jun/26 · Demanda Categoria R$ · Fonte: CPT SCJ</div>
      </div>
      <div style="display:flex;align-items:center;gap:12px;flex-shrink:0;">
        <div style="display:flex;align-items:center;gap:8px;">
          <span style="font-size:9px;font-weight:700;letter-spacing:0.1em;color:#F5E1A4;text-transform:uppercase;white-space:nowrap;">Grupo Econômico</span>
          <select id="cpt-sel-grupo"
            style="font-size:11px;font-weight:600;padding:6px 28px 6px 10px;border-radius:7px;
                   border:1px solid rgba(245,225,164,0.4);background:#161B22;color:#F5E1A4;
                   cursor:pointer;appearance:none;-webkit-appearance:none;min-width:200px;
                   background-image:url(\\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='10' height='6'%3E%3Cpath d='M0 0l5 6 5-6z' fill='%23F5E1A4'/%3E%3C/svg%3E\\");
                   background-repeat:no-repeat;background-position:right 8px center;">
            <option value="">— Selecione o Grupo —</option>
          </select>
        </div>
        <div class="toggle-group">
          <button class="tgl on" id="cpt-btn-val" onclick="setCPTMetric('val',this)">R$ Valor</button>
          <button class="tgl" id="cpt-btn-share" onclick="setCPTMetric('share',this)">Share %</button>
        </div>
      </div>
    </div>

    <!-- KPIs -->
    <div id="cpt-kpis" style="display:grid;grid-template-columns:repeat(6,1fr);gap:10px;margin-bottom:18px;">
      <div style="background:#161B22;border-radius:8px;padding:12px;text-align:center;color:#475569;font-size:10px;">Selecione um grupo</div>
    </div>

    <!-- Gráficos de linha -->
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-bottom:20px;">
      <div style="background:#0D1117;border-radius:10px;padding:16px;border:0.5px solid rgba(94,153,208,0.2);">
        <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:10px;">
          <div>
            <div style="font-size:9px;font-weight:700;letter-spacing:0.1em;color:#34d399;text-transform:uppercase;">EVOLUÇÃO MENSAL R$</div>
            <div style="font-size:11px;color:#D1D5DB;margin-top:2px;">SCJ FY25 vs FY26 · CIMED · RB · Total</div>
          </div>
          <div style="display:flex;gap:4px;">
            <button class="tgl on" id="cpt-c1-scj" onclick="setCPTChart1Mode(\'scj\',this)" style="font-size:9px;padding:3px 8px;">SCJ</button>
            <button class="tgl" id="cpt-c1-all" onclick="setCPTChart1Mode(\'all\',this)" style="font-size:9px;padding:3px 8px;">Todos</button>
          </div>
        </div>
        <div style="position:relative;height:220px;"><canvas id="cpt-canvas-val"></canvas></div>
      </div>
      <div style="background:#0D1117;border-radius:10px;padding:16px;border:0.5px solid rgba(94,153,208,0.2);">
        <div style="margin-bottom:10px;">
          <div style="font-size:9px;font-weight:700;letter-spacing:0.1em;color:#F5E1A4;text-transform:uppercase;">SHARE MENSAL SCJ (%)</div>
          <div style="font-size:11px;color:#D1D5DB;margin-top:2px;">FY25 (Jul/24–Jun/25) vs FY26 (Jul/25–Jun/26)</div>
        </div>
        <div style="position:relative;height:220px;"><canvas id="cpt-canvas-shr"></canvas></div>
      </div>
    </div>

    <!-- Tabela principal -->
    <div style="overflow-x:auto;border-radius:8px;border:0.5px solid rgba(94,153,208,0.2);">
      <table id="cpt-table" style="width:100%;border-collapse:collapse;font-size:10.5px;min-width:1400px;">
        <thead id="cpt-thead"></thead>
        <tbody id="cpt-tbody"></tbody>
      </table>
    </div>
    <div style="margin-top:8px;font-size:9px;color:#475569;">Fonte: CPT SCJ · Demanda Categoria = soma de vendas por Grupo de Produtos (SCJ + CIMED_OTHERS + RB_OTHERS) · Valores em R$</div>
  </div>

</div>

'''

# ── JS de renderização ─────────────────────────────────────────────
mes_labels_fy25_js = json.dumps(MES_LABELS_FY25)
mes_labels_fy26_js = json.dumps(MES_LABELS_FY26)
grupos_js = json.dumps(grupos_ordenados)

js_render = f'''
<script>
/* ══ CPT CLIENTES ══ */
var _cptMetric  = 'val';
var _cptC1Mode  = 'scj';
var _cptGrupos  = {grupos_js};
var _MES_FY25   = {mes_labels_fy25_js};
var _MES_FY26   = {mes_labels_fy26_js};
var _MES_FY_LBL = ['Jul','Ago','Set','Out','Nov','Dez','Jan','Fev','Mar','Abr','Mai','Jun'];
var _cptChartVal = null;
var _cptChartShr = null;

/* Popular select ao carregar */
(function(){{
  window.addEventListener('load', function(){{
    var sel = document.getElementById('cpt-sel-grupo');
    if(!sel) return;
    _cptGrupos.forEach(function(g){{
      var o = document.createElement('option');
      o.value = g; o.textContent = g;
      sel.appendChild(o);
    }});
    sel.addEventListener('change', renderCPTClientes);
  }});
}})();

function setCPTMetric(m, btn){{
  _cptMetric = m;
  document.querySelectorAll('#panel-cpt .toggle-group .tgl').forEach(function(b){{ b.classList.remove('on'); }});
  if(btn) btn.classList.add('on');
  renderCPTClientes();
}}

function setCPTChart1Mode(m, btn){{
  _cptC1Mode = m;
  ['cpt-c1-scj','cpt-c1-all'].forEach(function(id){{
    var el=document.getElementById(id); if(el) el.classList.remove('on');
  }});
  if(btn) btn.classList.add('on');
  var sel = document.getElementById('cpt-sel-grupo');
  var grupo = sel ? sel.value : '';
  if(grupo && CPT_CLI_DATA[grupo]) _renderCPTCharts(CPT_CLI_DATA[grupo]);
}}

function _renderCPTCharts(d){{
  var FY_LBL = _MES_FY_LBL;
  function fR(v){{ return v>=1e6?'R$'+(v/1e6).toFixed(2)+'MM':v>=1e3?'R$'+(v/1e3).toFixed(1)+'K':'R$'+Math.round(v); }}

  /* ── Gráfico 1: Evolução R$ ── */
  if(_cptChartVal){{ _cptChartVal.destroy(); _cptChartVal=null; }}
  var ctx1 = document.getElementById('cpt-canvas-val');
  if(ctx1){{
    var datasets1 = [];
    if(_cptC1Mode === 'scj'){{
      var scj25 = d.f25.map(function(r){{return r[1];}});
      var scj26 = d.f26.map(function(r){{return r[1];}});
      datasets1 = [
        {{label:'SCJ FY25',  data:scj25, borderColor:'#3b82f6', backgroundColor:'rgba(59,130,246,0.1)', borderWidth:2, borderDash:[5,4], pointRadius:3, pointHoverRadius:6, tension:0.4, fill:true}},
        {{label:'SCJ FY26',  data:scj26, borderColor:'#34d399', backgroundColor:'rgba(52,211,153,0.12)', borderWidth:2.5, pointRadius:3, pointHoverRadius:6, tension:0.4, fill:true}}
      ];
    }} else {{
      var c25=d.f25.map(function(r){{return r[0];}}), s25=d.f25.map(function(r){{return r[1];}}), r25=d.f25.map(function(r){{return r[2];}}), t25=d.f25.map(function(r){{return r[3];}});
      var c26=d.f26.map(function(r){{return r[0];}}), s26=d.f26.map(function(r){{return r[1];}}), r26=d.f26.map(function(r){{return r[2];}}), t26=d.f26.map(function(r){{return r[3];}});
      datasets1 = [
        {{label:'SCJ FY25',   data:s25, borderColor:'#3b82f6', borderDash:[4,3], borderWidth:1.5, pointRadius:2, tension:0.4, fill:false, backgroundColor:'transparent'}},
        {{label:'SCJ FY26',   data:s26, borderColor:'#34d399', borderWidth:2.5,  pointRadius:3,  tension:0.4, fill:false, backgroundColor:'transparent'}},
        {{label:'CIMED FY26', data:c26, borderColor:'#f59e0b', borderWidth:2,    pointRadius:2,  tension:0.4, fill:false, backgroundColor:'transparent'}},
        {{label:'RB FY26',    data:r26, borderColor:'#a78bfa', borderWidth:2,    pointRadius:2,  tension:0.4, fill:false, backgroundColor:'transparent'}},
        {{label:'Total FY26', data:t26, borderColor:'#60a5fa', borderWidth:1.5,  borderDash:[3,3],pointRadius:2,tension:0.4,fill:false,backgroundColor:'transparent'}}
      ];
    }}
    _cptChartVal = new Chart(ctx1, {{
      type:'line',
      data:{{labels:FY_LBL, datasets:datasets1}},
      options:{{
        responsive:true, maintainAspectRatio:false,
        interaction:{{mode:'index',intersect:false}},
        plugins:{{
          legend:{{position:'top',labels:{{color:'#94A3B8',font:{{size:10}},boxWidth:12,padding:8}}}},
          tooltip:{{backgroundColor:'#1E293B',borderColor:'rgba(94,153,208,0.3)',borderWidth:1,titleColor:'#F5E1A4',bodyColor:'#D1D5DB',padding:8,
            callbacks:{{label:function(c){{return c.dataset.label+': '+fR(c.parsed.y);}}}}
          }}
        }},
        scales:{{
          x:{{grid:{{color:'rgba(255,255,255,0.04)'}},ticks:{{color:'#64748B',font:{{size:9}}}}}},
          y:{{grid:{{color:'rgba(255,255,255,0.04)'}},ticks:{{color:'#64748B',font:{{size:9}},callback:function(v){{return v>=1e6?(v/1e6).toFixed(1)+'MM':v>=1e3?(v/1e3).toFixed(0)+'K':v;}}}}}}
        }}
      }}
    }});
  }}

  /* ── Gráfico 2: Share Mensal SCJ ── */
  if(_cptChartShr){{ _cptChartShr.destroy(); _cptChartShr=null; }}
  var ctx2 = document.getElementById('cpt-canvas-shr');
  if(ctx2){{
    var shr25 = d.f25.map(function(r){{ return r[3]>0?Math.round(r[1]/r[3]*10000)/100:0; }});
    var shr26 = d.f26.map(function(r){{ return r[3]>0?Math.round(r[1]/r[3]*10000)/100:0; }});
    _cptChartShr = new Chart(ctx2, {{
      type:'line',
      data:{{labels:FY_LBL, datasets:[
        {{label:'Share SCJ FY25', data:shr25, borderColor:'#3b82f6', backgroundColor:'rgba(59,130,246,0.1)', borderWidth:2, borderDash:[5,4], pointRadius:3, pointHoverRadius:6, tension:0.4, fill:true}},
        {{label:'Share SCJ FY26', data:shr26, borderColor:'#F5E1A4', backgroundColor:'rgba(245,225,164,0.08)', borderWidth:2.5, pointRadius:3, pointHoverRadius:6, tension:0.4, fill:true}}
      ]}},
      options:{{
        responsive:true, maintainAspectRatio:false,
        interaction:{{mode:'index',intersect:false}},
        plugins:{{
          legend:{{position:'top',labels:{{color:'#94A3B8',font:{{size:10}},boxWidth:12,padding:8}}}},
          tooltip:{{backgroundColor:'#1E293B',borderColor:'rgba(94,153,208,0.3)',borderWidth:1,titleColor:'#F5E1A4',bodyColor:'#D1D5DB',padding:8,
            callbacks:{{label:function(c){{return c.dataset.label+': '+c.parsed.y.toFixed(2)+'%';}}}}
          }}
        }},
        scales:{{
          x:{{grid:{{color:'rgba(255,255,255,0.04)'}},ticks:{{color:'#64748B',font:{{size:9}}}}}},
          y:{{grid:{{color:'rgba(255,255,255,0.04)'}},ticks:{{color:'#64748B',font:{{size:9}},callback:function(v){{return v.toFixed(0)+'%';}}}}}}
        }}
      }}
    }});
  }}
}}

function renderCPTClientes(){{
  var sel   = document.getElementById('cpt-sel-grupo');
  var grupo = sel ? sel.value : '';
  var kpisEl  = document.getElementById('cpt-kpis');
  var theadEl = document.getElementById('cpt-thead');
  var tbodyEl = document.getElementById('cpt-tbody');
  if(!kpisEl || !theadEl || !tbodyEl) return;

  if(!grupo || !CPT_CLI_DATA[grupo]){{
    kpisEl.innerHTML  = '<div style="grid-column:1/-1;text-align:center;color:#475569;font-size:11px;padding:10px;">Selecione um Grupo Econômico para exibir a análise.</div>';
    theadEl.innerHTML = '';
    tbodyEl.innerHTML = '';
    if(_cptChartVal){{_cptChartVal.destroy();_cptChartVal=null;}}
    if(_cptChartShr){{_cptChartShr.destroy();_cptChartShr=null;}}
    return;
  }}

  var d = CPT_CLI_DATA[grupo];
  var isShare = (_cptMetric === 'share');

  /* Renderizar gráficos */
  _renderCPTCharts(d);

  /* Totais anuais por linha */
  function sumLine(arrs, idx){{ return arrs.reduce(function(a,r){{return a+r[idx];}},0); }}
  var scj25=sumLine(d.f25,1), cim25=sumLine(d.f25,0), rb25=sumLine(d.f25,2), tot25=sumLine(d.f25,3);
  var scj26=sumLine(d.f26,1), cim26=sumLine(d.f26,0), rb26=sumLine(d.f26,2), tot26=sumLine(d.f26,3);

  var shr25 = tot25>0 ? scj25/tot25*100 : 0;
  var shr26 = tot26>0 ? scj26/tot26*100 : 0;
  var varShr = shr26 - shr25;
  var cresScj = scj25>0 ? (scj26-scj25)/scj25*100 : 0;
  var cresTot = tot25>0 ? (tot26-tot25)/tot25*100 : 0;

  function fR(v){{ return v>=1e6?'R$'+(v/1e6).toFixed(2)+'MM':v>=1e3?'R$'+(v/1e3).toFixed(1)+'K':'R$'+Math.round(v); }}
  function fPct(v){{ return (v>=0?'+':'')+v.toFixed(1)+'%'; }}
  function fPP(v){{  return (v>=0?'+':'')+v.toFixed(2)+'pp'; }}
  function col(v){{ return v>=0?'#34d399':'#ef4444'; }}
  function fShr(v){{ return v.toFixed(2)+'%'; }}

  /* KPIs */
  var kd = [
    {{tag:'SCJ FY25',   val:fR(scj25), sub:'Total anual',             dlt:'',              c:'#3b82f6'}},
    {{tag:'SCJ FY26',   val:fR(scj26), sub:'Total anual',             dlt:fPct(cresScj),   c:col(cresScj)}},
    {{tag:'DIF SCJ',    val:fR(scj26-scj25), sub:'FY26 vs FY25',      dlt:'',              c:col(scj26-scj25)}},
    {{tag:'SHARE FY25', val:fShr(shr25), sub:'SCJ/Total Mercado',     dlt:'',              c:'#3b82f6'}},
    {{tag:'SHARE FY26', val:fShr(shr26), sub:'SCJ/Total Mercado',     dlt:fPP(varShr),     c:col(varShr)}},
    {{tag:'TOTAL MERCADO FY26', val:fR(tot26), sub:'CIMED+SCJ+RB',    dlt:fPct(cresTot),   c:col(cresTot)}},
  ];
  kpisEl.innerHTML = kd.map(function(k){{
    return '<div style="background:#161B22;border-top:3px solid '+k.c+';border-radius:8px;padding:12px 14px;">'
      +'<div style="font-size:9px;font-weight:700;letter-spacing:0.1em;color:#475569;text-transform:uppercase;margin-bottom:5px;">'+k.tag+'</div>'
      +'<div style="font-size:18px;font-weight:700;color:'+k.c+';line-height:1.1;">'+k.val+'</div>'
      +'<div style="font-size:9px;color:#64748B;margin-top:3px;">'+k.sub+'</div>'
      +(k.dlt?'<div style="font-size:10px;font-weight:600;color:'+k.c+';margin-top:2px;">'+k.dlt+'</div>':'')
      +'</div>';
  }}).join('');

  /* Cabeçalho da tabela */
  var hS = 'style="padding:6px 8px;text-align:right;font-weight:700;font-size:9.5px;border-bottom:2px solid rgba(94,153,208,0.4);white-space:nowrap;"';
  var hSL = 'style="padding:6px 10px;text-align:left;font-weight:700;font-size:9.5px;border-bottom:2px solid rgba(94,153,208,0.4);white-space:nowrap;"';
  var hSC = function(c){{ return 'style="padding:6px 8px;text-align:right;font-weight:700;font-size:9.5px;border-bottom:2px solid rgba(94,153,208,0.4);white-space:nowrap;color:'+c+';"'; }};

  var head = '<tr style="background:rgba(29,111,168,0.12);">'
    +'<th '+hSL+'>Grupo de Produtos</th>';
  // FY25 months
  _MES_FY25.forEach(function(l){{ head += '<th '+hS+' style="color:#3b82f6;padding:6px 8px;text-align:right;font-weight:700;font-size:9.5px;border-bottom:2px solid rgba(94,153,208,0.4);white-space:nowrap;">'+l+'</th>'; }});
  head += '<th style="padding:6px 10px;text-align:right;font-weight:700;font-size:9.5px;border-bottom:2px solid rgba(94,153,208,0.4);white-space:nowrap;color:#3b82f6;background:rgba(59,130,246,0.1);border-left:2px solid rgba(59,130,246,0.3);">FY25</th>';
  // FY26 months
  _MES_FY26.forEach(function(l){{ head += '<th style="padding:6px 8px;text-align:right;font-weight:700;font-size:9.5px;border-bottom:2px solid rgba(94,153,208,0.4);white-space:nowrap;color:#34d399;">'+l+'</th>'; }});
  head += '<th style="padding:6px 10px;text-align:right;font-weight:700;font-size:9.5px;border-bottom:2px solid rgba(94,153,208,0.4);white-space:nowrap;color:#34d399;background:rgba(52,211,153,0.1);border-left:2px solid rgba(52,211,153,0.3);">FY26</th>';
  // Summary
  head += '<th style="padding:6px 8px;text-align:right;font-weight:700;font-size:9.5px;border-bottom:2px solid rgba(94,153,208,0.4);white-space:nowrap;color:#F5E1A4;border-left:2px solid rgba(245,225,164,0.3);">DIF</th>';
  head += '<th style="padding:6px 8px;text-align:right;font-weight:700;font-size:9.5px;border-bottom:2px solid rgba(94,153,208,0.4);white-space:nowrap;color:#F5E1A4;">CRES %</th>';
  head += '<th style="padding:6px 8px;text-align:right;font-weight:700;font-size:9.5px;border-bottom:2px solid rgba(94,153,208,0.4);white-space:nowrap;color:#F5E1A4;">SHARE FY25</th>';
  head += '<th style="padding:6px 8px;text-align:right;font-weight:700;font-size:9.5px;border-bottom:2px solid rgba(94,153,208,0.4);white-space:nowrap;color:#F5E1A4;">SHARE FY26</th>';
  head += '<th style="padding:6px 8px;text-align:right;font-weight:700;font-size:9.5px;border-bottom:2px solid rgba(94,153,208,0.4);white-space:nowrap;color:#F5E1A4;">VAR. SHARE</th>';
  head += '</tr>';
  theadEl.innerHTML = head;

  /* Linhas de dados */
  var rows_def = [
    {{ label:'CIMED_OTHERS', idx:0, color:'#94A3B8', bg:'' }},
    {{ label:'RB_OTHERS',    idx:2, color:'#94A3B8', bg:'' }},
    {{ label:'SCJ',          idx:1, color:'#F5E1A4', bg:'rgba(245,225,164,0.06)', bold:true }},
    {{ label:'TOTAL MERCADO',idx:3, color:'#60a5fa', bg:'rgba(59,130,246,0.06)', bold:true }},
  ];

  var body = '';

  rows_def.forEach(function(rd){{
    var bgStyle = rd.bg ? 'background:'+rd.bg+';' : '';
    var wStyle  = rd.bold ? 'font-weight:700;' : '';
    var anual25 = sumLine(d.f25, rd.idx);
    var anual26 = sumLine(d.f26, rd.idx);
    var dif     = anual26 - anual25;
    var cres    = anual25>0 ? dif/anual25*100 : 0;
    var shr25i  = tot25>0 ? anual25/tot25*100 : 0;
    var shr26i  = tot26>0 ? anual26/tot26*100 : 0;
    var varShri = shr26i - shr25i;

    var row = '<tr style="border-bottom:0.5px solid rgba(255,255,255,0.06);'+bgStyle+'">';
    row += '<td style="padding:7px 10px;color:'+rd.color+';'+wStyle+'white-space:nowrap;">'+rd.label+'</td>';

    if(isShare){{
      // Mostrar share mensal
      d.f25.forEach(function(r){{
        var tot_m = r[3]; var val_m = r[rd.idx];
        var shr_m = tot_m>0?val_m/tot_m*100:0;
        row += '<td style="padding:7px 8px;text-align:right;color:'+rd.color+';'+wStyle+'">'+fShr(shr_m)+'</td>';
      }});
      row += '<td style="padding:7px 10px;text-align:right;color:#3b82f6;'+wStyle+'background:rgba(59,130,246,0.07);border-left:2px solid rgba(59,130,246,0.2);">'+fShr(shr25i)+'</td>';
      d.f26.forEach(function(r){{
        var tot_m = r[3]; var val_m = r[rd.idx];
        var shr_m = tot_m>0?val_m/tot_m*100:0;
        row += '<td style="padding:7px 8px;text-align:right;color:'+rd.color+';'+wStyle+'">'+fShr(shr_m)+'</td>';
      }});
      row += '<td style="padding:7px 10px;text-align:right;color:#34d399;'+wStyle+'background:rgba(52,211,153,0.07);border-left:2px solid rgba(52,211,153,0.2);">'+fShr(shr26i)+'</td>';
      row += '<td style="padding:7px 8px;text-align:right;color:'+col(dif)+';border-left:2px solid rgba(245,225,164,0.2);">'+fPP(varShri)+'</td>';
      row += '<td style="padding:7px 8px;text-align:right;color:'+col(cres)+';">'+fPct(cres)+'</td>';
      row += '<td style="padding:7px 8px;text-align:right;color:#64748B;">'+fShr(shr25i)+'</td>';
      row += '<td style="padding:7px 8px;text-align:right;color:#64748B;">'+fShr(shr26i)+'</td>';
      row += '<td style="padding:7px 8px;text-align:right;color:'+col(varShri)+';">'+fPP(varShri)+'</td>';
    }} else {{
      // Mostrar valor R$
      d.f25.forEach(function(r){{
        row += '<td style="padding:7px 8px;text-align:right;color:'+rd.color+';'+wStyle+'">'+fR(r[rd.idx])+'</td>';
      }});
      row += '<td style="padding:7px 10px;text-align:right;color:#3b82f6;'+wStyle+'background:rgba(59,130,246,0.07);border-left:2px solid rgba(59,130,246,0.2);">'+fR(anual25)+'</td>';
      d.f26.forEach(function(r){{
        row += '<td style="padding:7px 8px;text-align:right;color:'+rd.color+';'+wStyle+'">'+fR(r[rd.idx])+'</td>';
      }});
      row += '<td style="padding:7px 10px;text-align:right;color:#34d399;'+wStyle+'background:rgba(52,211,153,0.07);border-left:2px solid rgba(52,211,153,0.2);">'+fR(anual26)+'</td>';
      row += '<td style="padding:7px 8px;text-align:right;color:'+col(dif)+';'+wStyle+'border-left:2px solid rgba(245,225,164,0.2);">'+fR(dif)+'</td>';
      row += '<td style="padding:7px 8px;text-align:right;color:'+col(cres)+';'+wStyle+'">'+fPct(cres)+'</td>';
      row += '<td style="padding:7px 8px;text-align:right;color:#64748B;">'+fShr(shr25i)+'</td>';
      row += '<td style="padding:7px 8px;text-align:right;color:#64748B;">'+fShr(shr26i)+'</td>';
      row += '<td style="padding:7px 8px;text-align:right;color:'+col(varShri)+';">'+fPP(varShri)+'</td>';
    }}
    row += '</tr>';
    body += row;
  }});

  /* Linha Share Mensal SCJ */
  var shrRow = '<tr style="border-top:2px solid rgba(94,153,208,0.3);background:rgba(59,130,246,0.04);">'
    +'<td style="padding:7px 10px;color:#3b82f6;font-weight:700;font-size:10px;">SHARE MENSAL SCJ</td>';
  d.f25.forEach(function(r){{
    var tot_m=r[3]; var scj_m=r[1];
    var s=tot_m>0?scj_m/tot_m*100:0;
    shrRow += '<td style="padding:7px 8px;text-align:right;color:#3b82f6;font-weight:600;">'+fShr(s)+'</td>';
  }});
  shrRow += '<td style="padding:7px 10px;text-align:right;color:#3b82f6;font-weight:700;background:rgba(59,130,246,0.1);border-left:2px solid rgba(59,130,246,0.2);">'+fShr(shr25)+'</td>';
  d.f26.forEach(function(r){{
    var tot_m=r[3]; var scj_m=r[1];
    var s=tot_m>0?scj_m/tot_m*100:0;
    shrRow += '<td style="padding:7px 8px;text-align:right;color:#34d399;font-weight:600;">'+fShr(s)+'</td>';
  }});
  shrRow += '<td style="padding:7px 10px;text-align:right;color:#34d399;font-weight:700;background:rgba(52,211,153,0.1);border-left:2px solid rgba(52,211,153,0.2);">'+fShr(shr26)+'</td>';
  shrRow += '<td style="padding:7px 8px;text-align:right;color:'+col(varShr)+';font-weight:700;border-left:2px solid rgba(245,225,164,0.2);">'+fPP(varShr)+'</td>';
  shrRow += '<td colspan="4" style="padding:7px 8px;color:#475569;font-size:9px;">Var. Share: '+fPP(varShr)+'</td>';
  shrRow += '</tr>';
  body += shrRow;

  tbodyEl.innerHTML = body;
}}
</script>
'''

# ── Injetar botão da aba ───────────────────────────────────────────
BTN_ANCHOR = "<button class=\"ctab\" onclick=\"switchClient('distribuicao',this)\">"
if BTN_ANCHOR not in html:
    print('ERRO: âncora do botão não encontrada!')
    import sys; sys.exit(1)

cpt_btn = '<button class="ctab" onclick="switchClient(\'cpt\',this)">CPT Clientes <span class="cdot cdot-empty"></span></button>\n  '
html = html.replace(BTN_ANCHOR, cpt_btn + BTN_ANCHOR, 1)

# ── Injetar painel após Sell Out ────────────────────────────────────
# Inserir antes do painel Sell Out (panel-sellout)
PANEL_ANCHOR = '<!-- ═══════════ SELL OUT (CONSOLIDADO) ═══════════ -->'
if PANEL_ANCHOR not in html:
    print('ERRO: âncora do painel não encontrada!')
    import sys; sys.exit(1)

html = html.replace(PANEL_ANCHOR, panel_html + '\n' + PANEL_ANCHOR, 1)

# ── Injetar dados e render JS antes do último </body> ──────────────
last_body = html.rfind('</body>')
inject_js = f'\n<script>\n{js_data}\n</script>\n{js_render}\n'
html = html[:last_body] + inject_js + html[last_body:]

# ── Salvar ─────────────────────────────────────────────────────────
with open(DASH, 'w', encoding='utf-8') as f:
    f.write(html)

ts = datetime.now().strftime('%Y%m%d_%H%M')
ver_path = os.path.join(VER_DIR, f'Dashboard_Farma_Sul_{ts}.html')
dl_path  = os.path.join(DOWNLOADS, f'Dashboard_FarmaSul_Giovano_{ts}.html')
shutil.copy(DASH, ver_path)
shutil.copy(DASH, dl_path)

print(f'\n✅ Aba CPT Clientes criada!')
print(f'   Versão: versoes/Dashboard_Farma_Sul_{ts}.html')
print(f'   Downloads: {dl_path}')
print(f'   Tamanho final: {len(html)/1024/1024:.1f} MB')
