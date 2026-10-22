"""
patch_acumulado_fy_v3.py
Substitui abordagem v2 (DOM move) por 7 cards independentes por cliente.

Problema do v2: mover canvas com Chart.js via DOM causa gráficos em branco/incorretos.
Solução v3:
  • 1 card HTML por cliente, com canvas IDs únicos (acum-r-saojoao, acum-v-nissei, ...)
  • JS compartilhado único (renderAcumuladoFYClient)
  • Cada card só renderiza quando seu container fica visível (polling offsetWidth)
  • Sem DOM move, sem acumMoveToClient, sem risco de stale canvas
"""
import sys
from pathlib import Path
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

BASE = Path(r'C:\Users\valqu\OneDrive\Documentos\Claude\Projects\projeto Dashboard_farma_sul\Dashboard_farma_sul')
SRC  = BASE / 'Dashboard_Farma_Sul_20260512_2220.html'
VER  = BASE / 'versoes' / f'Dashboard_Farma_Sul_{datetime.now().strftime("%Y%m%d_%H%M")}_AcumuladoFY_v3.html'

print('Lendo dashboard…')
h = SRC.read_text(encoding='utf-8')
orig_len = len(h)

# ─────────────────────────────────────────────────────────────────────────────
# Clientes e labels
# ─────────────────────────────────────────────────────────────────────────────
CLIENTS = [
    ('saojoao',  'São João'),
    ('nissei',   'Nissei'),
    ('clamed',   'Clamed'),
    ('panvel',   'Panvel'),
    ('ddgam',    'DD-GAM'),
    ('ddgaucha', 'DD-Gaúcha'),
    ('ddriomed', 'DD-Riomed'),
]

# ─────────────────────────────────────────────────────────────────────────────
# PASSO 1: Remover injeção acumMoveToClient de switchSellOutClient
# ─────────────────────────────────────────────────────────────────────────────
OLD_SWITCH_INJECT = """  // Mover card Acumulado FY para o slot do cliente ativo
  if(typeof window.acumMoveToClient === 'function')
    setTimeout(function(){ window.acumMoveToClient(clientId); }, 120);
}"""

NEW_SWITCH_INJECT = """}"""

assert h.count(OLD_SWITCH_INJECT) == 1, f'❌ injeção switchSellOutClient: {h.count(OLD_SWITCH_INJECT)}×'
h = h.replace(OLD_SWITCH_INJECT, NEW_SWITCH_INJECT)
print('✅ Injeção acumMoveToClient removida de switchSellOutClient')

# ─────────────────────────────────────────────────────────────────────────────
# PASSO 2: Remover slot saojoao (que contém o card v2 completo)
#   Substituir por: [JS compartilhado] + [card saojoao v3] + [init script saojoao]
# ─────────────────────────────────────────────────────────────────────────────

# Encontrar início e fim do slot saojoao
slot_sj_start = h.find('<div id="acum-slot-saojoao"')
assert slot_sj_start >= 0, '❌ slot saojoao não encontrado'

seg = h[slot_sj_start:]
depth, pos = 0, 0
while pos < len(seg):
    if seg[pos:pos+4] == '<div':
        depth += 1; pos += 4
    elif seg[pos:pos+6] == '</div>':
        depth -= 1
        if depth == 0:
            slot_sj_end = slot_sj_start + pos + 6
            break
        pos += 6
    else:
        pos += 1

print(f'✅ Slot saojoao localizado: {slot_sj_start}–{slot_sj_end} ({slot_sj_end-slot_sj_start} bytes)')

# ─────────────────────────────────────────────────────────────────────────────
# JS COMPARTILHADO (inserido uma vez, junto com o primeiro slot)
# ─────────────────────────────────────────────────────────────────────────────
SHARED_JS = r"""<script>
/* ════ ACUMULADO FY — JS COMPARTILHADO (v3) ════ */
(function(){
  var _charts = {};   // { clientId: { r: chartR, v: chartV } }
  var _rendered = {}; // { clientId: bool }

  var _LBL = {
    saojoao:'São João', nissei:'Nissei', clamed:'Clamed',
    panvel:'Panvel', ddgam:'DD-GAM', ddgaucha:'DD-Gaúcha', ddriomed:'DD-Riomed'
  };

  /* ── Formatar ──────────────────────────────────────────────────── */
  function _fmtR(v){ if(!v) return 'R$ 0'; if(v>=1e6) return 'R$ '+(v/1e6).toFixed(1)+'M'; if(v>=1e3) return 'R$ '+(v/1e3).toFixed(0)+'K'; return 'R$ '+v.toFixed(0); }
  function _fmtU(v){ if(!v) return '0'; if(v>=1e6) return (v/1e6).toFixed(1)+'M'; if(v>=1e3) return (v/1e3).toFixed(0)+'K'; return v.toFixed(0); }
  function _fmtAx(v,isR){ if(isR){ if(v>=1e6) return 'R$'+(v/1e6).toFixed(0)+'M'; if(v>=1e3) return 'R$'+(v/1e3).toFixed(0)+'K'; return 'R$'+v; } if(v>=1e6) return (v/1e6).toFixed(1)+'M'; if(v>=1e3) return (v/1e3).toFixed(0)+'K'; return v+''; }
  function _pct(a,b){ return a>0?((b-a)/a*100).toFixed(1):'—'; }

  /* ── FY series ─────────────────────────────────────────────────── */
  function _fy(a24,a25,a26){
    var f25=[],f26=[];
    for(var i=6;i<12;i++) f25.push((a24&&a24[i]!=null)?+a24[i]:0);
    for(var i=0;i<6;i++)  f25.push((a25&&a25[i]!=null)?+a25[i]:0);
    for(var i=6;i<12;i++) f26.push((a25&&a25[i]!=null)?+a25[i]:0);
    for(var i=0;i<6;i++)  f26.push((a26&&a26[i]!=null)?+a26[i]:null);
    return {fy25:f25,fy26:f26};
  }

  /* ── Dados por cliente ─────────────────────────────────────────── */
  function _data(cl){
    var r25=new Array(12).fill(0), r26=new Array(12).fill(null);
    var v25=new Array(12).fill(0), v26=new Array(12).fill(null);
    function _add(ser,t25,t26){ for(var i=0;i<12;i++){ if(ser.fy25[i]!=null) t25[i]=(t25[i]||0)+ser.fy25[i]; if(ser.fy26[i]!=null) t26[i]=(t26[i]||0)+ser.fy26[i]; } }
    if(cl==='saojoao'){
      if(typeof SJ_REC!=='undefined')  _add(_fy(SJ_REC['2024'],SJ_REC['2025'],SJ_REC['2026']),  r25,r26);
      if(typeof SJ_UNID!=='undefined') _add(_fy(SJ_UNID['2024'],SJ_UNID['2025'],SJ_UNID['2026']),v25,v26);
    } else if(cl==='nissei'){
      if(typeof NS!=='undefined'&&NS.total){
        _add(_fy(NS.total.rec['2024'],NS.total.rec['2025'],NS.total.rec['2026']),r25,r26);
        _add(_fy(NS.total.vol['2024'],NS.total.vol['2025'],NS.total.vol['2026']),v25,v26);
      }
    } else if(cl==='clamed'){
      if(typeof CL_REC_2024!=='undefined'){
        _add(_fy(CL_REC_2024,CL_REC_2025,CL_REC_2026),r25,r26);
        _add(_fy(CL_VOL_2024,CL_VOL_2025,CL_VOL_2026),v25,v26);
      }
    } else if(cl==='panvel'){
      if(typeof PV_REC!=='undefined'){
        _add(_fy(PV_REC['2024'],PV_REC['2025'],PV_REC['2026']),r25,r26);
        _add(_fy(PV_VOL['2024'],PV_VOL['2025'],PV_VOL['2026']),v25,v26);
      }
    } else if(cl==='ddgam'){
      if(typeof GAM_REC!=='undefined'){
        _add(_fy(GAM_REC['2024'],GAM_REC['2025'],GAM_REC['2026']),r25,r26);
        _add(_fy(GAM_VOL['2024'],GAM_VOL['2025'],GAM_VOL['2026']),v25,v26);
      }
    } else if(cl==='ddgaucha'){
      if(typeof GAUCHA_REC!=='undefined'){
        _add(_fy(GAUCHA_REC['2024'],GAUCHA_REC['2025'],GAUCHA_REC['2026']),r25,r26);
        _add(_fy(GAUCHA_VOL['2024'],GAUCHA_VOL['2025'],GAUCHA_VOL['2026']),v25,v26);
      }
    } else if(cl==='ddriomed'){
      if(typeof RIOMED_REC_2024!=='undefined'){
        _add(_fy(RIOMED_REC_2024,RIOMED_REC_2025,RIOMED_REC_2026),r25,r26);
        _add(_fy(RIOMED_VOL_2024,RIOMED_VOL_2025,RIOMED_VOL_2026),v25,v26);
      }
    }
    return {r25:r25,r26:r26,v25:v25,v26:v26};
  }

  /* ── Cumulativo ─────────────────────────────────────────────────── */
  function _cum(a){ var r=[],s=0; for(var i=0;i<a.length;i++){ if(a[i]!=null&&a[i]>0){s+=a[i];r.push(s);}else if(a[i]===null){r.push(null);}else{r.push(s>0?s:null);} } return r; }
  function _cumP(a){ var r=[],s=0; for(var i=0;i<a.length;i++){ if(a[i]!=null&&a[i]>0) s+=a[i]; r.push(s>0?s:null); } return r; }

  /* ── Gradiente ──────────────────────────────────────────────────── */
  function _grad(ctx,ca,col){ if(!ca) return col+'44'; try{ var g=ctx.createLinearGradient(0,ca.top,0,ca.bottom); g.addColorStop(0,col+'66'); g.addColorStop(1,col+'08'); return g; }catch(e){ return col+'44'; } }

  /* ── Criar chart ────────────────────────────────────────────────── */
  function _mkChart(id,c25,c26,c26P,old,isR){
    var cv=document.getElementById(id);
    if(!cv) return old;
    if(old){ try{ old.destroy(); }catch(e){} }
    var FY=['Jul','Ago','Set','Out','Nov','Dez','Jan','Fev','Mar','Abr','Mai','Jun'];
    var GC='rgba(255,255,255,0.07)',TC='#4a6b65';
    var cb={
      title:function(its){ return FY[its[0].dataIndex]+(isR?' (Acum.)':''); },
      label:function(it){ var v=it.raw; if(v==null) return it.dataset.label+': —'; return it.dataset.label+': '+(isR?_fmtR(v):_fmtU(v)); },
      afterBody:function(its){
        var idx=its[0]?its[0].dataIndex:-1; if(idx<0) return [];
        var a=c25[idx],b=c26P[idx];
        if(a&&b&&a>0){ var d=b-a,p=(d/a*100).toFixed(1),s=d>=0?'+':'';
          return ['─────────────','Δ vs FY25: '+s+p+'%  ('+s+(isR?_fmtR(Math.abs(d)):_fmtU(Math.abs(d)))+')'];
        } return [];
      }
    };
    var chart=new Chart(cv.getContext('2d'),{type:'line',
      data:{labels:FY,datasets:[
        {label:'FY25',data:c25,borderColor:'#3b82f6',backgroundColor:function(ctx){return _grad(ctx.chart.ctx,ctx.chart.chartArea,'#3b82f6');},pointBackgroundColor:'#3b82f6',pointBorderColor:'#0D1117',pointBorderWidth:1.5,pointRadius:3,pointHoverRadius:6,borderWidth:2.5,tension:0.4,fill:true,spanGaps:false},
        {label:'FY26',data:c26,borderColor:'#34d399',backgroundColor:function(ctx){return _grad(ctx.chart.ctx,ctx.chart.chartArea,'#34d399');},pointBackgroundColor:'#34d399',pointBorderColor:'#0D1117',pointBorderWidth:1.5,pointRadius:3,pointHoverRadius:6,borderWidth:2.5,tension:0.4,fill:true,spanGaps:false},
        {label:'FY26 proj.',data:c26P,borderColor:'#34d39966',borderDash:[5,4],backgroundColor:'transparent',pointBackgroundColor:'#34d39966',pointBorderColor:'transparent',pointRadius:2,pointHoverRadius:4,borderWidth:1.5,tension:0.4,fill:false,spanGaps:true}
      ]},
      options:{responsive:true,maintainAspectRatio:false,interaction:{mode:'index',intersect:false},
        plugins:{legend:{display:false},tooltip:{backgroundColor:'#0a1a18',titleColor:'#e2e8f0',bodyColor:'#D1D5DB',borderColor:'rgba(255,255,255,0.13)',borderWidth:1,padding:10,callbacks:cb}},
        scales:{x:{grid:{color:GC},ticks:{color:TC,font:{size:9}}},y:{grid:{color:GC},ticks:{color:TC,font:{size:9},callback:function(v){return _fmtAx(v,isR);}},min:0}}
      }
    });
    setTimeout(function(){ try{ chart.resize(); }catch(e){} },80);
    return chart;
  }

  /* ── Render principal ────────────────────────────────────────────── */
  window.renderAcumuladoFYClient = function(cl){
    if(typeof Chart==='undefined') return;
    var lbl=_LBL[cl]||cl;
    var tot=_data(cl);
    var cR25=_cum(tot.r25), cR26=_cum(tot.r26), cR26P=_cumP(tot.r26);
    var cV25=_cum(tot.v25), cV26=_cum(tot.v26), cV26P=_cumP(tot.v26);
    var sR25=tot.r25.reduce(function(s,v){return s+(v||0);},0);
    var sR26=tot.r26.reduce(function(s,v){return s+(v||0);},0);
    var sV25=tot.v25.reduce(function(s,v){return s+(v||0);},0);
    var sV26=tot.v26.reduce(function(s,v){return s+(v||0);},0);
    var dR=_pct(sR25,sR26), dV=_pct(sV25,sV26);
    /* KPI */
    var kpi=document.getElementById('acum-kpi-'+cl);
    if(kpi){
      function _dS(n){ var x=parseFloat(n); if(isNaN(x)) return '<span style="color:#64748B;">—</span>'; var c=x>=0?'#34d399':'#ef4444'; return '<span style="color:'+c+';font-weight:700;">'+(x>=0?'▲ +':'▼ ')+Math.abs(x).toFixed(1)+'%</span>'; }
      kpi.innerHTML=[
        {l:'💰 Faturamento FY25',v25:_fmtR(sR25),v26:'—',d:'—',ac:'#3b82f6'},
        {l:'💰 Fat. FY26 YTD',v25:_fmtR(sR25),v26:_fmtR(sR26),d:dR,ac:'#34d399'},
        {l:'📦 Un. FY26 YTD',v25:_fmtU(sV25),v26:_fmtU(sV26),d:dV,ac:'#2dd4bf'},
      ].map(function(k){
        return '<div style="background:#161B22;border-radius:10px;padding:12px 14px;border-top:2px solid '+k.ac+';">'
          +'<div style="font-size:8px;font-weight:700;letter-spacing:.1em;color:#3d6b63;margin-bottom:6px;text-transform:uppercase;">'+k.l+'</div>'
          +(k.v25!=='—'?'<div style="font-size:9px;color:#475569;margin-bottom:2px;">FY25: <span style="color:#64748B;font-weight:600;">'+k.v25+'</span></div>':'')
          +'<div style="display:flex;align-items:baseline;gap:8px;">'
          +'<span style="font-size:18px;font-weight:800;color:'+k.ac+';line-height:1;">'+(k.v26!=='—'?k.v26:k.v25)+'</span>'
          +_dS(k.d)+'</div></div>';
      }).join('');
    }
    /* Charts */
    if(!_charts[cl]) _charts[cl]={r:null,v:null};
    _charts[cl].r=_mkChart('acum-r-'+cl,cR25,cR26,cR26P,_charts[cl].r,true);
    _charts[cl].v=_mkChart('acum-v-'+cl,cV25,cV26,cV26P,_charts[cl].v,false);
    /* Diag */
    var diag=document.getElementById('acum-diag-'+cl);
    if(diag){
      var dRN=parseFloat(dR),dVN=parseFloat(dV);
      var dRC=isNaN(dRN)?'#94A3B8':(dRN>=0?'#34d399':'#ef4444');
      var dVC=isNaN(dVN)?'#94A3B8':(dVN>=0?'#34d399':'#ef4444');
      var FY=['Jul','Ago','Set','Out','Nov','Dez','Jan','Fev','Mar','Abr','Mai','Jun'];
      var bM='—',bG=-Infinity;
      for(var i=0;i<12;i++){ if(tot.r25[i]>0&&tot.r26[i]!=null){ var g=(tot.r26[i]-tot.r25[i])/tot.r25[i]*100; if(g>bG){bG=g;bM=FY[i];} } }
      var mFY26=tot.r26.filter(function(v){return v!=null&&v>0;}).length;
      diag.innerHTML='<strong style="color:#fbbf24;font-size:10px;letter-spacing:.08em;">📊 DIAGNÓSTICO ACUMULADO FY25 vs FY26 — '+lbl.toUpperCase()+'</strong><br>'
        +'💰 <strong>Fat. FY26 YTD</strong> ('+mFY26+' meses): <strong style="color:'+dRC+';">'+_fmtR(sR26)+'</strong>'
        +' vs FY25 <strong style="color:#94A3B8;">'+_fmtR(sR25)+'</strong>'
        +' — <span style="color:'+dRC+';font-weight:700;">'+(dRN>=0?'▲ +':'▼ ')+Math.abs(dRN).toFixed(1)+'%</span><br>'
        +'📦 <strong>Un. FY26 YTD</strong>: <strong style="color:'+dVC+';">'+_fmtU(sV26)+'</strong>'
        +' vs FY25 <strong style="color:#94A3B8;">'+_fmtU(sV25)+'</strong>'
        +' — <span style="color:'+dVC+';font-weight:700;">'+(dVN>=0?'▲ +':'▼ ')+Math.abs(dVN).toFixed(1)+'%</span><br>'
        +(bM!=='—'?'📈 <strong>Melhor mês FY26</strong>: <strong style="color:'+(bG>=0?'#34d399':'#ef4444')+';">'+bM+'</strong>'
          +' com <span style="color:'+(bG>=0?'#34d399':'#ef4444')+';">'+(bG>=0?'+':'')+bG.toFixed(1)+'%</span> vs FY25<br>':'')
        +'<span style="font-size:9px;color:#475569;">FY25: Jul/24–Jun/25 · FY26 YTD: Jul/25–Abr/26 (tracejado=projetado) · '+lbl+'</span>';
    }
    _rendered[cl]=true;
  };

  /* ── Init por cliente: polling até visível + dados prontos ────── */
  window._acumTryRender = function(cl, attempts){
    if(!attempts) attempts=0;
    if(attempts>60) return;
    if(typeof Chart==='undefined'||typeof SJ_REC==='undefined'){
      setTimeout(function(){ window._acumTryRender(cl,attempts+1); },100); return;
    }
    var cv=document.getElementById('acum-r-'+cl);
    if(!cv||cv.offsetWidth===0){
      setTimeout(function(){ window._acumTryRender(cl,attempts+1); },150); return;
    }
    window.renderAcumuladoFYClient(cl);
  };

  /* toggle modo R$/Un. — reservado para uso futuro */
  window.acumSetMode = function(cl,mode,btn){
    var card=document.getElementById('card-acum-'+cl);
    if(!card) return;
    card.querySelectorAll('[data-acummode]').forEach(function(b){
      var on=b.getAttribute('data-acummode')===mode;
      b.classList.toggle('active',on);
      b.style.color=on?'#fbbf24':'#D1D5DB';
      b.style.background=on?'rgba(251,191,36,0.12)':'#161B22';
      b.style.fontWeight=on?'700':'600';
    });
  };
})();
</script>
"""

# ─────────────────────────────────────────────────────────────────────────────
# Card HTML template por cliente
# ─────────────────────────────────────────────────────────────────────────────
def card_html(cl, lbl):
    init_script = (
        f'<script>setTimeout(function(){{'
        f'if(typeof window._acumTryRender==="function") window._acumTryRender("{cl}",0);'
        f'else{{ var _t=0,_iv=setInterval(function(){{'
        f'if(typeof window._acumTryRender==="function"){{clearInterval(_iv);window._acumTryRender("{cl}",0);}}'
        f'else if(++_t>40)clearInterval(_iv);}},100); }}'
        f'}},250);</script>'
    )
    return f"""  <!-- ═══ CARD EVOLUÇÃO ACUMULADA FY25 vs FY26 · {lbl.upper()} ═══ -->
  <div id="card-acum-{cl}" class="card full" style="margin-bottom:16px;">
    <div class="card-header">
      <div>
        <div class="card-title">📈 EVOLUÇÃO ACUMULADA FY25 vs FY26</div>
        <div class="card-sub" id="acum-sub-{cl}">Faturamento Acumulado · Jul/24–Jun/25 vs Jul/25–Jun/26 · {lbl}</div>
      </div>
      <div style="display:flex;align-items:center;gap:14px;">
        <div class="toggle-group">
          <button class="tgl active blue" data-acummode="rec" onclick="acumSetMode('{cl}','rec',this)">R$</button>
          <button class="tgl" data-acummode="vol" onclick="acumSetMode('{cl}','vol',this)">Un.</button>
        </div>
        <div style="display:flex;gap:14px;align-items:center;">
          <span style="display:flex;align-items:center;gap:5px;font-size:11px;font-weight:700;color:#60a5fa;"><span style="width:18px;height:2.5px;background:#3b82f6;display:inline-block;border-radius:2px;"></span>FY25</span>
          <span style="display:flex;align-items:center;gap:5px;font-size:11px;font-weight:700;color:#34d399;"><span style="width:18px;height:2.5px;background:#34d399;display:inline-block;border-radius:2px;"></span>FY26</span>
          <span style="display:flex;align-items:center;gap:5px;font-size:10px;color:#64748B;"><span style="width:20px;height:2.5px;display:inline-block;border-radius:2px;background:repeating-linear-gradient(90deg,#64748B 0,#64748B 4px,transparent 4px,transparent 8px);"></span>Projetado</span>
        </div>
      </div>
    </div>
    <div id="acum-kpi-{cl}" style="display:grid;grid-template-columns:repeat(3,1fr);gap:10px;padding:14px 0 16px;"></div>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;">
      <div>
        <div style="font-size:9px;font-weight:700;letter-spacing:.12em;color:#3d6b63;text-transform:uppercase;margin-bottom:8px;">💰 Faturamento Acumulado (R$)</div>
        <div style="position:relative;height:240px;"><canvas id="acum-r-{cl}"></canvas></div>
      </div>
      <div>
        <div style="font-size:9px;font-weight:700;letter-spacing:.12em;color:#3d6b63;text-transform:uppercase;margin-bottom:8px;">📦 Unidades Acumuladas</div>
        <div style="position:relative;height:240px;"><canvas id="acum-v-{cl}"></canvas></div>
      </div>
    </div>
    <div id="acum-diag-{cl}" style="margin-top:14px;padding:12px 16px;background:rgba(255,255,255,0.03);border-radius:8px;border-left:3px solid rgba(59,130,246,0.4);font-size:11px;color:#D1D5DB;line-height:1.7;"></div>
  </div>
  {init_script}
"""

# ─────────────────────────────────────────────────────────────────────────────
# PASSO 3: Substituir slot saojoao pelo JS compartilhado + card saojoao
# ─────────────────────────────────────────────────────────────────────────────
SJ_SLOT_TEXT = h[slot_sj_start:slot_sj_end]
NEW_SJ_BLOCK = (
    '<div id="acum-slot-saojoao" class="acum-slot" style="margin-bottom:0;">\n'
    + SHARED_JS
    + card_html('saojoao', 'São João')
    + '</div>'
)
h = h[:slot_sj_start] + NEW_SJ_BLOCK + h[slot_sj_end:]
print('✅ Slot saojoao substituído por JS compartilhado + card saojoao v3')

# ─────────────────────────────────────────────────────────────────────────────
# PASSO 4: Substituir slots vazios dos demais clientes
# ─────────────────────────────────────────────────────────────────────────────
EMPTY_SLOT_TPL = '<div id="acum-slot-{cl}" class="acum-slot" style="margin-bottom:0;"></div>'

for cl, lbl in CLIENTS[1:]:  # skip saojoao
    empty = EMPTY_SLOT_TPL.format(cl=cl)
    count = h.count(empty)
    assert count == 1, f'❌ slot vazio {cl}: {count}×'
    new_slot = (
        f'<div id="acum-slot-{cl}" class="acum-slot" style="margin-bottom:0;">\n'
        + card_html(cl, lbl)
        + '</div>'
    )
    h = h.replace(empty, new_slot, 1)
    print(f'✅ Slot {cl} substituído por card v3')

# ─────────────────────────────────────────────────────────────────────────────
# Verificações
# ─────────────────────────────────────────────────────────────────────────────
assert 'renderAcumuladoFYClient' in h,   '❌ renderAcumuladoFYClient não encontrado'
assert '_acumTryRender' in h,            '❌ _acumTryRender não encontrado'
for cl, lbl in CLIENTS:
    assert f'acum-r-{cl}' in h,          f'❌ canvas R$ {cl} não encontrado'
    assert f'acum-v-{cl}' in h,          f'❌ canvas Vol {cl} não encontrado'
    assert f'acum-kpi-{cl}' in h,        f'❌ KPI strip {cl} não encontrado'
    assert f'acum-diag-{cl}' in h,       f'❌ diag {cl} não encontrado'
    assert f'card-acum-{cl}' in h,       f'❌ card {cl} não encontrado'
# Garantir que o acumMoveToClient foi removido
assert 'acumMoveToClient' not in h,     '❌ acumMoveToClient ainda presente!'
# v3 marker
assert 'ACUMULADO FY — JS COMPARTILHADO (v3)' in h, '❌ marcação v3 não encontrada'
print('✅ Todas as verificações OK')

print(f'\nTamanho original: {orig_len:,} | Novo: {len(h):,} | Δ: {len(h)-orig_len:+,}')

VER.parent.mkdir(parents=True, exist_ok=True)
VER.write_text(h, encoding='utf-8')
print(f'✅ Versão salva: {VER.name}')
SRC.write_text(h, encoding='utf-8')
print(f'✅ Base ativa atualizada: {SRC.name}')
print('DONE.')
