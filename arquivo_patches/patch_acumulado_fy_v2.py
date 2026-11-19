"""
patch_acumulado_fy_v2.py
Remove card ACUMULADO FY global (v1) e recria-o dentro de cada seção de cliente.

Mudanças vs v1:
  • Card fica DENTRO da seção do cliente selecionado, abaixo de Evolução Mensal
  • Dados filtrados pelo cliente ativo (não mais soma de todos)
  • switchSellOutClient() move o card para o slot correto e chama renderAcumuladoFY(clientId)
  • Subtítulo e diagnóstico mencionam o cliente selecionado
"""
import sys, re
from pathlib import Path
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

BASE = Path(r'C:\Users\valqu\OneDrive\Documentos\Claude\Projects\projeto Dashboard_farma_sul\Dashboard_farma_sul')
SRC  = BASE / 'Dashboard_Farma_Sul_20260512_2220.html'
VER  = BASE / 'versoes' / f'Dashboard_Farma_Sul_{datetime.now().strftime("%Y%m%d_%H%M")}_AcumuladoFY_v2.html'

print('Lendo dashboard…')
h = SRC.read_text(encoding='utf-8')
orig_len = len(h)

# ─────────────────────────────────────────────────────────────────────────────
# PASSO 1: Remover card v1 (global, antes de sellout-content-saojoao)
# ─────────────────────────────────────────────────────────────────────────────
V1_START = '  <!-- ════════════ CARD EVOLUÇÃO ACUMULADA FY25 vs FY26 ════════════ -->'
V1_END   = '  <!-- Conteúdos dinâmicos por cliente -->'

assert V1_START in h, '❌ Card v1 não encontrado'
assert V1_END   in h, '❌ Âncora clientes não encontrada'

pos_start = h.find(V1_START)
pos_end   = h.find(V1_END, pos_start)
h = h[:pos_start] + h[pos_end:]
print('✅ Card v1 removido')

# ─────────────────────────────────────────────────────────────────────────────
# PASSO 2: Inserir slots em cada seção de cliente (abaixo de Evolução Mensal)
#   Âncora: texto único logo antes do primeiro <div class="cards-row">
#   que segue o compare-wrap de cada cliente.
# ─────────────────────────────────────────────────────────────────────────────
SLOT_TEMPLATE = '\n  <div id="acum-slot-{client}" class="acum-slot" style="margin-bottom:0;"></div>\n  '

# Mapeamento: clientId -> texto único (final do compare-wrap -> antes de cards-row)
SLOT_ANCHORS = {
    'saojoao':  ('argin-top:6px;flex-wrap:wrap;"></div>\n        </div>\n      </div>\n    </div>\n\n  <div class="cards-row">',
                 'argin-top:6px;flex-wrap:wrap;"></div>\n        </div>\n      </div>\n    </div>\n\n  '),
    'nissei':   (';margin-top:6px;flex-wrap:wrap;"></div>\n        </div>\n      </div>\n  </div>\n\n  <div class="cards-row"',
                 None),   # unique=False: need offset approach
    'clamed':   None,   # same pattern as nissei
    'panvel':   None,
    'ddgam':    ('x;margin-top:6px;flex-wrap:wrap;"></div>\n        </div>\n      </div>\n  </div>\n  <div class="cards-row"',
                 None),
    'ddgaucha': None,
    'ddriomed': None,
}

# Para os clientes com padrão duplicado, usar offset baseado no compare-wrap ID
COMPARE_WRAP_IDS = {
    'saojoao':  'sj-compare-wrap',
    'nissei':   'ns-compare-wrap',
    'clamed':   'cl-compare-wrap',
    'panvel':   'pv-compare-wrap',
    'ddgam':    'gam-compare-wrap',
    'ddgaucha': 'gch-compare-wrap',
    'ddriomed': 'rio-compare-wrap',
}

insertions = []   # lista de (offset, texto_a_inserir)

for client, cwrap_id in COMPARE_WRAP_IDS.items():
    cwrap_pos = h.find(f'<div id="{cwrap_id}"')
    assert cwrap_pos >= 0, f'❌ {cwrap_id} não encontrado'

    # Encontrar o primeiro <div class="cards-row"> APÓS o compare-wrap
    seg = h[cwrap_pos:cwrap_pos+2000]
    cr_idx = seg.find('<div class="cards-row"')
    assert cr_idx >= 0, f'❌ cards-row não encontrado após {cwrap_id}'

    insert_pos = cwrap_pos + cr_idx
    slot_html  = SLOT_TEMPLATE.format(client=client)
    insertions.append((insert_pos, slot_html))
    print(f'  slot acum-slot-{client} @ offset {insert_pos}')

# Aplicar em ordem reversa para não invalidar offsets
for pos, txt in sorted(insertions, reverse=True):
    h = h[:pos] + txt + h[pos:]

print('✅ Slots inseridos em todos os clientes')

# ─────────────────────────────────────────────────────────────────────────────
# PASSO 3: Inserir card HTML + Script no slot do São João (default)
#   O card começa em saojoao; JS o move para o cliente ativo.
# ─────────────────────────────────────────────────────────────────────────────
CARD_HTML = r"""  <!-- ════════════ CARD EVOLUÇÃO ACUMULADA FY25 vs FY26 (v2) ════════════ -->
  <div id="card-acumulado-fy" class="card full" style="margin-bottom:16px;">
    <div class="card-header">
      <div>
        <div class="card-title">📈 EVOLUÇÃO ACUMULADA FY25 vs FY26</div>
        <div class="card-sub" id="acum-sub">Faturamento Acumulado · Jul/24–Jun/25 vs Jul/25–Jun/26</div>
      </div>
      <div style="display:flex;align-items:center;gap:14px;">
        <div class="toggle-group">
          <button class="tgl active blue" id="acum-btn-rec" onclick="setAcumMode('rec',this)">R$</button>
          <button class="tgl" id="acum-btn-vol" onclick="setAcumMode('vol',this)">Un.</button>
        </div>
        <div style="display:flex;gap:14px;align-items:center;">
          <span style="display:flex;align-items:center;gap:5px;font-size:11px;font-weight:700;color:#60a5fa;">
            <span style="width:18px;height:2.5px;background:#3b82f6;display:inline-block;border-radius:2px;"></span>FY25
          </span>
          <span style="display:flex;align-items:center;gap:5px;font-size:11px;font-weight:700;color:#34d399;">
            <span style="width:18px;height:2.5px;background:#34d399;display:inline-block;border-radius:2px;"></span>FY26
          </span>
          <span style="display:flex;align-items:center;gap:5px;font-size:10px;color:#64748B;">
            <span style="width:20px;height:2.5px;display:inline-block;border-radius:2px;background:repeating-linear-gradient(90deg,#64748B 0,#64748B 4px,transparent 4px,transparent 8px);"></span>Projetado
          </span>
        </div>
      </div>
    </div>

    <!-- KPI chips -->
    <div id="acum-kpi-strip" style="display:grid;grid-template-columns:repeat(3,1fr);gap:10px;padding:14px 0 16px;"></div>

    <!-- Gráficos -->
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;">
      <div>
        <div style="font-size:9px;font-weight:700;letter-spacing:.12em;color:#3d6b63;text-transform:uppercase;margin-bottom:8px;">💰 Faturamento Acumulado (R$)</div>
        <div style="position:relative;height:240px;"><canvas id="acum-rec-canvas"></canvas></div>
      </div>
      <div>
        <div style="font-size:9px;font-weight:700;letter-spacing:.12em;color:#3d6b63;text-transform:uppercase;margin-bottom:8px;">📦 Unidades Acumuladas</div>
        <div style="position:relative;height:240px;"><canvas id="acum-vol-canvas"></canvas></div>
      </div>
    </div>

    <!-- Diagnóstico -->
    <div id="acum-diag" style="margin-top:14px;padding:12px 16px;background:rgba(255,255,255,0.03);border-radius:8px;border-left:3px solid rgba(59,130,246,0.4);font-size:11px;color:#D1D5DB;line-height:1.7;"></div>
  </div>

  <script>
  (function(){
    var _acumMode   = 'rec';
    var _acumChartR = null;
    var _acumChartV = null;
    var _acumCurClient = 'saojoao';

    /* ── Nomes de exibição ─────────────────────────────────────────────── */
    var _CLIENT_LBL = {
      saojoao:'São João', nissei:'Nissei', clamed:'Clamed',
      panvel:'Panvel', ddgam:'DD-GAM', ddgaucha:'DD-Gaúcha', ddriomed:'DD-Riomed'
    };

    /* ── Toggle R$ / Un. ──────────────────────────────────────────────── */
    window.setAcumMode = function(mode, btn){
      _acumMode = mode;
      ['acum-btn-rec','acum-btn-vol'].forEach(function(id){
        var b = document.getElementById(id);
        if(!b) return;
        var on = (id === 'acum-btn-'+mode);
        b.classList.toggle('active', on);
        b.style.color      = on ? '#fbbf24' : '#D1D5DB';
        b.style.background = on ? 'rgba(251,191,36,0.12)' : '#161B22';
        b.style.fontWeight = on ? '700' : '600';
      });
      var sub = document.getElementById('acum-sub');
      var lbl = _CLIENT_LBL[_acumCurClient] || _acumCurClient;
      if(sub) sub.textContent = (mode==='rec'
        ? 'Faturamento Acumulado · Jul/24–Jun/25 vs Jul/25–Jun/26 · '
        : 'Unidades Acumuladas · Jul/24–Jun/25 vs Jul/25–Jun/26 · ') + lbl;
    };

    /* ── Formatar ─────────────────────────────────────────────────────── */
    function _fmtR(v){ if(!v) return 'R$ 0'; if(v>=1e6) return 'R$ '+(v/1e6).toFixed(1)+'M'; if(v>=1e3) return 'R$ '+(v/1e3).toFixed(0)+'K'; return 'R$ '+v.toFixed(0); }
    function _fmtU(v){ if(!v) return '0'; if(v>=1e6) return (v/1e6).toFixed(1)+'M'; if(v>=1e3) return (v/1e3).toFixed(0)+'K'; return v.toFixed(0); }
    function _fmtAxis(v,isR){ if(isR){ if(v>=1e6) return 'R$'+(v/1e6).toFixed(0)+'M'; if(v>=1e3) return 'R$'+(v/1e3).toFixed(0)+'K'; return 'R$'+v; } else { if(v>=1e6) return (v/1e6).toFixed(1)+'M'; if(v>=1e3) return (v/1e3).toFixed(0)+'K'; return v+''; } }
    function _pct(a,b){ return a>0?((b-a)/a*100).toFixed(1):'—'; }

    /* ── FY series: arr[Jan..Dez] → FY[Jul..Jun] ─────────────────────── */
    function _fy(a24, a25, a26){
      var f25=[],f26=[];
      for(var i=6;i<12;i++) f25.push((a24&&a24[i]!=null)?+a24[i]:0);
      for(var i=0;i<6;i++)  f25.push((a25&&a25[i]!=null)?+a25[i]:0);
      for(var i=6;i<12;i++) f26.push((a25&&a25[i]!=null)?+a25[i]:0);
      for(var i=0;i<6;i++)  f26.push((a26&&a26[i]!=null)?+a26[i]:null);
      return {fy25:f25,fy26:f26};
    }

    /* ── Dados por cliente ────────────────────────────────────────────── */
    function _getClientData(clientId){
      var r25=new Array(12).fill(0), r26=new Array(12).fill(null);
      var v25=new Array(12).fill(0), v26=new Array(12).fill(null);
      function _add(ser,t25,t26){ for(var i=0;i<12;i++){ if(ser.fy25[i]!=null) t25[i]=(t25[i]||0)+ser.fy25[i]; if(ser.fy26[i]!=null) t26[i]=(t26[i]||0)+ser.fy26[i]; } }
      if(clientId==='saojoao'){
        if(typeof SJ_REC!=='undefined')  _add(_fy(SJ_REC['2024'],SJ_REC['2025'],SJ_REC['2026']),  r25,r26);
        if(typeof SJ_UNID!=='undefined') _add(_fy(SJ_UNID['2024'],SJ_UNID['2025'],SJ_UNID['2026']),v25,v26);
      } else if(clientId==='nissei'){
        if(typeof NS!=='undefined'&&NS.total){
          _add(_fy(NS.total.rec['2024'],NS.total.rec['2025'],NS.total.rec['2026']),r25,r26);
          _add(_fy(NS.total.vol['2024'],NS.total.vol['2025'],NS.total.vol['2026']),v25,v26);
        }
      } else if(clientId==='clamed'){
        if(typeof CL_REC_2024!=='undefined'){
          _add(_fy(CL_REC_2024,CL_REC_2025,CL_REC_2026),r25,r26);
          _add(_fy(CL_VOL_2024,CL_VOL_2025,CL_VOL_2026),v25,v26);
        }
      } else if(clientId==='panvel'){
        if(typeof PV_REC!=='undefined'){
          _add(_fy(PV_REC['2024'],PV_REC['2025'],PV_REC['2026']),r25,r26);
          _add(_fy(PV_VOL['2024'],PV_VOL['2025'],PV_VOL['2026']),v25,v26);
        }
      } else if(clientId==='ddgam'){
        if(typeof GAM_REC!=='undefined'){
          _add(_fy(GAM_REC['2024'],GAM_REC['2025'],GAM_REC['2026']),r25,r26);
          _add(_fy(GAM_VOL['2024'],GAM_VOL['2025'],GAM_VOL['2026']),v25,v26);
        }
      } else if(clientId==='ddgaucha'){
        if(typeof GAUCHA_REC!=='undefined'){
          _add(_fy(GAUCHA_REC['2024'],GAUCHA_REC['2025'],GAUCHA_REC['2026']),r25,r26);
          _add(_fy(GAUCHA_VOL['2024'],GAUCHA_VOL['2025'],GAUCHA_VOL['2026']),v25,v26);
        }
      } else if(clientId==='ddriomed'){
        if(typeof RIOMED_REC_2024!=='undefined'){
          _add(_fy(RIOMED_REC_2024,RIOMED_REC_2025,RIOMED_REC_2026),r25,r26);
          _add(_fy(RIOMED_VOL_2024,RIOMED_VOL_2025,RIOMED_VOL_2026),v25,v26);
        }
      }
      return {rec25:r25,rec26:r26,vol25:v25,vol26:v26};
    }

    /* ── Cumulativo ───────────────────────────────────────────────────── */
    function _cum(arr){ var res=[],s=0; for(var i=0;i<arr.length;i++){ if(arr[i]!=null&&arr[i]>0){s+=arr[i];res.push(s);}else if(arr[i]===null){res.push(null);}else{res.push(s||null);} } return res; }
    function _cumP(arr){ var res=[],s=0; for(var i=0;i<arr.length;i++){ if(arr[i]!=null&&arr[i]>0) s+=arr[i]; res.push(s>0?s:null); } return res; }

    /* ── Gradiente ────────────────────────────────────────────────────── */
    function _grad(ctx,ca,col){ if(!ca) return col+'44'; try{ var g=ctx.createLinearGradient(0,ca.top,0,ca.bottom); g.addColorStop(0,col+'66'); g.addColorStop(1,col+'08'); return g; }catch(e){ return col+'44'; } }

    /* ── Render principal ────────────────────────────────────────────── */
    window.renderAcumuladoFY = function(clientId){
      if(typeof Chart==='undefined') return;
      if(!clientId) clientId = (typeof activeSelloutClient!=='undefined') ? activeSelloutClient : 'saojoao';
      _acumCurClient = clientId;

      var lbl = _CLIENT_LBL[clientId] || clientId;
      var FY_LBL = ['Jul','Ago','Set','Out','Nov','Dez','Jan','Fev','Mar','Abr','Mai','Jun'];
      var GC = 'rgba(255,255,255,0.07)';
      var TC = '#4a6b65';

      /* Dados */
      var tot = _getClientData(clientId);
      var cR25=_cum(tot.rec25), cR26=_cum(tot.rec26), cR26P=_cumP(tot.rec26);
      var cV25=_cum(tot.vol25), cV26=_cum(tot.vol26), cV26P=_cumP(tot.vol26);

      /* Totais */
      var sR25=tot.rec25.reduce(function(s,v){return s+(v||0);},0);
      var sR26=tot.rec26.reduce(function(s,v){return s+(v||0);},0);
      var sV25=tot.vol25.reduce(function(s,v){return s+(v||0);},0);
      var sV26=tot.vol26.reduce(function(s,v){return s+(v||0);},0);
      var dR=_pct(sR25,sR26), dV=_pct(sV25,sV26);

      /* Subtítulo */
      var sub = document.getElementById('acum-sub');
      if(sub) sub.textContent = (_acumMode==='rec'?'Faturamento Acumulado':'Unidades Acumuladas')
        +' · Jul/24–Jun/25 vs Jul/25–Jun/26 · '+lbl;

      /* ── KPI strip ──────────────────────────────────────────────────── */
      var kpiEl = document.getElementById('acum-kpi-strip');
      if(kpiEl){
        function _dStr(num){
          var n=parseFloat(num);
          if(isNaN(n)) return '<span style="color:#64748B;">—</span>';
          var col=n>=0?'#34d399':'#ef4444';
          return '<span style="color:'+col+';font-weight:700;">'+(n>=0?'▲ +':'▼ ')+Math.abs(n).toFixed(1)+'%</span>';
        }
        kpiEl.innerHTML=[
          {lbl:'💰 Faturamento FY25',v25:_fmtR(sR25),v26:'—',d:'—',ac:'#3b82f6'},
          {lbl:'💰 Faturamento FY26 YTD',v25:_fmtR(sR25),v26:_fmtR(sR26),d:dR,ac:'#34d399'},
          {lbl:'📦 Unidades FY26 YTD',v25:_fmtU(sV25),v26:_fmtU(sV26),d:dV,ac:'#2dd4bf'},
        ].map(function(k){
          return '<div style="background:#161B22;border-radius:10px;padding:12px 14px;border-top:2px solid '+k.ac+';">'
            +'<div style="font-size:8px;font-weight:700;letter-spacing:.1em;color:#3d6b63;margin-bottom:6px;text-transform:uppercase;">'+k.lbl+'</div>'
            +(k.v25!=='—'?'<div style="font-size:9px;color:#475569;margin-bottom:2px;">FY25: <span style="color:#64748B;font-weight:600;">'+k.v25+'</span></div>':'')
            +'<div style="display:flex;align-items:baseline;gap:8px;">'
              +'<span style="font-size:18px;font-weight:800;color:'+k.ac+';line-height:1;">'+(k.v26!=='—'?k.v26:k.v25)+'</span>'
              +_dStr(k.d)
            +'</div></div>';
        }).join('');
      }

      /* ── Gráficos ───────────────────────────────────────────────────── */
      function _mkChart(canvasId,c25,c26,c26P,old,isR){
        var canvas=document.getElementById(canvasId);
        if(!canvas) return old;
        if(old){ try{ old.destroy(); }catch(e){} }
        var cb={
          title:function(items){ return FY_LBL[items[0].dataIndex]+(isR?' (Acum.)':''); },
          label:function(item){ var v=item.raw; if(v==null) return item.dataset.label+': —'; return item.dataset.label+': '+(isR?_fmtR(v):_fmtU(v)); },
          afterBody:function(items){
            var idx=items[0]?items[0].dataIndex:-1; if(idx<0) return [];
            var a=c25[idx],b=c26P[idx];
            if(a&&b&&a>0){ var diff=b-a,pct=(diff/a*100).toFixed(1),sym=diff>=0?'+':'';
              return ['─────────────────','Δ vs FY25: '+sym+pct+'%  ('+sym+(isR?_fmtR(Math.abs(diff)):_fmtU(Math.abs(diff)))+')'];
            }
            return [];
          }
        };
        return new Chart(canvas.getContext('2d'),{type:'line',
          data:{labels:FY_LBL,datasets:[
            {label:'FY25',data:c25,borderColor:'#3b82f6',backgroundColor:function(ctx){return _grad(ctx.chart.ctx,ctx.chart.chartArea,'#3b82f6');},pointBackgroundColor:'#3b82f6',pointBorderColor:'#0D1117',pointBorderWidth:1.5,pointRadius:3,pointHoverRadius:6,borderWidth:2.5,tension:0.4,fill:true,spanGaps:false},
            {label:'FY26',data:c26,borderColor:'#34d399',backgroundColor:function(ctx){return _grad(ctx.chart.ctx,ctx.chart.chartArea,'#34d399');},pointBackgroundColor:'#34d399',pointBorderColor:'#0D1117',pointBorderWidth:1.5,pointRadius:3,pointHoverRadius:6,borderWidth:2.5,tension:0.4,fill:true,spanGaps:false},
            {label:'FY26 (proj.)',data:c26P,borderColor:'#34d39966',borderDash:[5,4],backgroundColor:'transparent',pointBackgroundColor:'#34d39966',pointBorderColor:'transparent',pointRadius:2,pointHoverRadius:4,borderWidth:1.5,tension:0.4,fill:false,spanGaps:true}
          ]},
          options:{responsive:true,maintainAspectRatio:false,interaction:{mode:'index',intersect:false},
            plugins:{legend:{display:false},tooltip:{backgroundColor:'#0a1a18',titleColor:'#e2e8f0',bodyColor:'#D1D5DB',borderColor:'rgba(255,255,255,0.13)',borderWidth:1,padding:10,callbacks:cb}},
            scales:{x:{grid:{color:GC},ticks:{color:TC,font:{size:9}}},y:{grid:{color:GC},ticks:{color:TC,font:{size:9},callback:function(v){return _fmtAxis(v,isR);}},min:0}}
          }
        });
      }
      _acumChartR = _mkChart('acum-rec-canvas',cR25,cR26,cR26P,_acumChartR,true);
      _acumChartV = _mkChart('acum-vol-canvas',cV25,cV26,cV26P,_acumChartV,false);

      /* ── Diagnóstico ────────────────────────────────────────────────── */
      var diagEl = document.getElementById('acum-diag');
      if(diagEl){
        var dRN=parseFloat(dR), dVN=parseFloat(dV);
        var dRC=isNaN(dRN)?'#94A3B8':(dRN>=0?'#34d399':'#ef4444');
        var dVC=isNaN(dVN)?'#94A3B8':(dVN>=0?'#34d399':'#ef4444');
        var bestM='—', bestG=-Infinity;
        for(var i=0;i<12;i++){
          if(tot.rec25[i]>0&&tot.rec26[i]!=null){
            var g=(tot.rec26[i]-tot.rec25[i])/tot.rec25[i]*100;
            if(g>bestG){bestG=g;bestM=FY_LBL[i];}
          }
        }
        var mFY26=tot.rec26.filter(function(v){return v!=null&&v>0;}).length;
        diagEl.innerHTML='<strong style="color:#fbbf24;font-size:10px;letter-spacing:.08em;">📊 DIAGNÓSTICO ACUMULADO FY25 vs FY26 — '+lbl.toUpperCase()+'</strong><br>'
          +'💰 <strong>Faturamento FY26 YTD</strong> ('+mFY26+' meses): <strong style="color:'+dRC+';">'+_fmtR(sR26)+'</strong>'
          +' vs FY25 <strong style="color:#94A3B8;">'+_fmtR(sR25)+'</strong>'
          +' — <span style="color:'+dRC+';font-weight:700;">'+(dRN>=0?'▲ +':'▼ ')+Math.abs(dRN).toFixed(1)+'%</span><br>'
          +'📦 <strong>Unidades FY26 YTD</strong>: <strong style="color:'+dVC+';">'+_fmtU(sV26)+'</strong>'
          +' vs FY25 <strong style="color:#94A3B8;">'+_fmtU(sV25)+'</strong>'
          +' — <span style="color:'+dVC+';font-weight:700;">'+(dVN>=0?'▲ +':'▼ ')+Math.abs(dVN).toFixed(1)+'%</span><br>'
          +(bestM!=='—'?'📈 <strong>Melhor mês FY26</strong>: <strong style="color:'+( bestG>=0?'#34d399':'#ef4444')+';">'+bestM+'</strong> com <span style="color:'+(bestG>=0?'#34d399':'#ef4444')+';">'+(bestG>=0?'+':'')+bestG.toFixed(1)+'%</span> vs FY25<br>':'')
          +'<span style="font-size:9px;color:#475569;">FY25: Jul/24–Jun/25 · FY26 YTD: Jul/25–Abr/26 (tracejado=projetado) · Fonte: '+lbl+'</span>';
      }
    };

    /* ── Mover card para o slot do cliente e re-renderizar ─────────────── */
    window.acumMoveToClient = function(clientId){
      var card = document.getElementById('card-acumulado-fy');
      var slot = document.getElementById('acum-slot-'+clientId);
      if(card && slot) slot.appendChild(card);
      if(typeof window.renderAcumuladoFY === 'function')
        setTimeout(function(){ window.renderAcumuladoFY(clientId); }, 80);
    };

    /* ── Init: aguardar Chart.js + dados ─────────────────────────────── */
    var _attempts = 0;
    function _init(){
      _attempts++;
      if(_attempts > 60) return;
      if(typeof Chart==='undefined'||typeof SJ_REC==='undefined'){
        setTimeout(_init, 100); return;
      }
      var initClient = (typeof activeSelloutClient!=='undefined') ? activeSelloutClient : 'saojoao';
      window.acumMoveToClient(initClient);
    }
    setTimeout(_init, 250);
  })();
  </script>

"""

# Inserir o card dentro do slot de saojoao (default)
SLOT_SJ_ANCHOR = '<div id="acum-slot-saojoao" class="acum-slot" style="margin-bottom:0;"></div>'
assert h.count(SLOT_SJ_ANCHOR) == 1, f'❌ slot saojoao: {h.count(SLOT_SJ_ANCHOR)}×'

# Substituir o slot vazio pelo slot com o card dentro
h = h.replace(SLOT_SJ_ANCHOR,
    '<div id="acum-slot-saojoao" class="acum-slot" style="margin-bottom:0;">\n'
    + CARD_HTML
    + '</div>\n', 1)
print('✅ Card HTML + script inserido no slot saojoao')

# ─────────────────────────────────────────────────────────────────────────────
# PASSO 4: Injetar chamada em switchSellOutClient()
#   Adicionar window.acumMoveToClient(clientId) ao final da função
# ─────────────────────────────────────────────────────────────────────────────
OLD_SWITCH_END = """  } catch(e){ console.error('[switchSellOutClient] Erro init', clientId, e); }
    }, 60);
  }
}

/* ═══════════ COBERTURA TAB ═══════════ */"""

NEW_SWITCH_END = """  } catch(e){ console.error('[switchSellOutClient] Erro init', clientId, e); }
    }, 60);
  }
  // Mover card Acumulado FY para o slot do cliente ativo
  if(typeof window.acumMoveToClient === 'function')
    setTimeout(function(){ window.acumMoveToClient(clientId); }, 120);
}

/* ═══════════ COBERTURA TAB ═══════════ */"""

assert h.count(OLD_SWITCH_END) == 1, f'❌ âncora switchSellOutClient end: {h.count(OLD_SWITCH_END)}×'
h = h.replace(OLD_SWITCH_END, NEW_SWITCH_END)
print('✅ switchSellOutClient() → acumMoveToClient injetado')

# ─────────────────────────────────────────────────────────────────────────────
# Verificações
# ─────────────────────────────────────────────────────────────────────────────
assert 'card-acumulado-fy' in h,        '❌ card id não encontrado'
assert 'renderAcumuladoFY' in h,        '❌ renderAcumuladoFY não encontrado'
assert 'acumMoveToClient' in h,         '❌ acumMoveToClient não encontrado'
assert 'acum-slot-saojoao' in h,        '❌ slot saojoao não encontrado'
assert 'acum-slot-nissei' in h,         '❌ slot nissei não encontrado'
assert 'acum-slot-clamed' in h,         '❌ slot clamed não encontrado'
assert 'acum-slot-panvel' in h,         '❌ slot panvel não encontrado'
assert 'acum-slot-ddgam' in h,          '❌ slot ddgam não encontrado'
assert 'acum-slot-ddgaucha' in h,       '❌ slot ddgaucha não encontrado'
assert 'acum-slot-ddriomed' in h,       '❌ slot ddriomed não encontrado'
assert h.count('card-acumulado-fy') >= 2, '❌ card deve aparecer no slot + referências'
# Card v1 deve ter sido removido (não deve haver CARD v1 comment)
assert '(v2)' in h,                     '❌ marcação v2 não encontrada'
print('✅ Verificações OK')

print(f'\nTamanho original: {orig_len:,} | Novo: {len(h):,} | Δ: {len(h)-orig_len:+,}')

VER.parent.mkdir(parents=True, exist_ok=True)
VER.write_text(h, encoding='utf-8')
print(f'✅ Versão salva: {VER.name}')
SRC.write_text(h, encoding='utf-8')
print(f'✅ Base ativa atualizada: {SRC.name}')
print('DONE.')
