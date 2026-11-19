"""
Versão 2 do card YoY — adiciona:
1. Filtro de provedor interno ao card (input autocomplete)
2. Quando provedor selecionado: análise completa (gráfico mensal, CIMED+RB, UF breakdown)
3. Quando sem seleção: ranking geral (já existente)
"""

import shutil, re
from datetime import datetime
from pathlib import Path

BASE = Path(r"C:\Users\valqu\OneDrive\Documentos\Claude\Projects\projeto Dashboard_farma_sul\Dashboard_farma_sul")
DASH = BASE / "Dashboard_Farma_Sul_20260512_2220.html"
VER  = BASE / "versoes"
DL   = Path.home() / "Downloads"

html = DASH.read_text(encoding='utf-8')
orig_len = len(html)

# ══════════════════════════════════════════════════════════════
# 1. Substituir TODO o bloco JS antigo por versão nova + completa
# ══════════════════════════════════════════════════════════════

OLD_JS_START = "/* ═══ EVOLUCAO YoY POR PROVEDOR ═══ */"
OLD_JS_END   = "\nfunction initSellin(){"

if OLD_JS_START not in html:
    print("ERRO: bloco JS antigo nao encontrado!")
    exit(1)

idx_start = html.index(OLD_JS_START)
idx_end   = html.index(OLD_JS_END, idx_start)
html = html[:idx_start] + html[idx_end:]
print("Bloco JS antigo removido")

NEW_JS = r"""
/* ═══ EVOLUCAO YoY POR PROVEDOR v2 ═══ */
var _yoySortKey  = 'delta';
var _yoyShowAll  = false;
var _yoyTotal    = 0;
var _yoySelProv  = null;   // provedor selecionado no filtro interno
var _yoyChart    = null;   // instância Chart.js

function _yoyFiltInput(){ return document.getElementById('yoy-filt-input'); }
function _yoyFiltList(){ return document.getElementById('yoy-filt-list'); }

function yoyFiltKey(e){
  var q = (e.target.value||'').toLowerCase().trim();
  var list = _yoyFiltList();
  if(!list) return;
  if(!q){ list.style.display='none'; return; }
  var matches = (PROV_DATA||[]).filter(function(p){ return p.name.toLowerCase().indexOf(q)>=0; }).slice(0,10);
  if(!matches.length){ list.style.display='none'; return; }
  list.innerHTML = matches.map(function(p){
    var fy26=0; (p.monthly||[]).slice(15,24).forEach(function(v){fy26+=v;});
    return '<div onclick="yoySelectProv(\''+p.name.replace(/'/g,"\\'")+'\')" style="padding:8px 12px;cursor:pointer;border-bottom:0.5px solid rgba(255,255,255,0.05);font-size:11px;color:#D1D5DB;display:flex;justify-content:space-between;align-items:center;" onmouseover="this.style.background=\'rgba(34,197,94,0.08)\'" onmouseout="this.style.background=\'\'"><span>'+p.name+'</span><span style="font-size:9px;color:#475569;">'+p.scj.toLocaleString('pt-BR')+' SCJ · '+Math.round(p.pct)+'%</span></div>';
  }).join('');
  list.style.display='block';
}

function yoySelectProv(name){
  _yoySelProv = name;
  var inp = _yoyFiltInput();
  if(inp) inp.value = name;
  var list = _yoyFiltList();
  if(list) list.style.display='none';
  renderProvYoYCard();
}

function yoyClearProv(){
  _yoySelProv = null;
  var inp = _yoyFiltInput();
  if(inp) inp.value = '';
  renderProvYoYCard();
}

function setYoYSort(k, btn){
  _yoySortKey = k;
  document.querySelectorAll('#prov-yoy-card .yoy-sort-btn').forEach(function(b){
    b.style.background='transparent'; b.style.color='#64748b'; b.style.borderColor='rgba(255,255,255,0.07)';
  });
  btn.style.background='rgba(251,191,36,0.15)'; btn.style.color='#fbbf24'; btn.style.borderColor='rgba(251,191,36,0.3)';
  if(!_yoySelProv) renderProvYoYCard();
}

function toggleYoYAll(btn){
  _yoyShowAll = !_yoyShowAll;
  btn.textContent = _yoyShowAll ? 'Ver Top 20' : 'Ver todos ('+_yoyTotal+')';
  renderProvYoYCard();
}

/* ── Análise completa de um provedor selecionado ── */
function _yoyRenderDetail(p, bodyEl){
  var M   = p.monthly || [];
  var lbl = ['Jul','Ago','Set','Out','Nov','Dez','Jan','Fev','Mar'];
  // FY25: M[3]-M[11] | FY26: M[15]-M[23]
  var fy25arr=[],fy26arr=[];
  for(var i=3;i<=11;i++)  fy25arr.push(M[i]||0);
  for(var i=15;i<=23;i++) fy26arr.push(M[i]||0);
  var fy25=fy25arr.reduce(function(a,b){return a+b;},0);
  var fy26=fy26arr.reduce(function(a,b){return a+b;},0);
  var q1_25=(M[9]||0)+(M[10]||0)+(M[11]||0);
  var q1_26=(M[21]||0)+(M[22]||0)+(M[23]||0);
  var delta=fy25>0?(fy26-fy25)/fy25*100:null;
  var q1d  =q1_25>0?(q1_26-q1_25)/q1_25*100:null;
  var opp  =p.opp_total||0;
  var reconq=p.reconquista||0;
  var atend=(opp+reconq)>0?Math.round(reconq/(opp+reconq)*100):0;
  var dSign=function(v){return v===null?'—':(v>=0?'+':'')+v.toFixed(1)+'%';};
  var dCol =function(v){return v===null?'#64748b':v>=0?'#34d399':'#ef4444';};

  /* ── KPI strip ── */
  var kpi='<div style="display:grid;grid-template-columns:repeat(6,1fr);gap:1px;background:rgba(255,255,255,0.04);border-radius:10px;overflow:hidden;margin-bottom:16px;">'
    +_yoyKpi('FY25 Jul→Mar', fy25.toLocaleString('pt-BR'), 'PDV·meses','#3b82f6')
    +_yoyKpi('FY26 Jul→Mar', fy26.toLocaleString('pt-BR'), 'PDV·meses','#22c55e')
    +_yoyKpi('Δ YoY', dSign(delta), 'vs mesmo período','',dCol(delta))
    +_yoyKpi('Q1 FY25 (Jan-Mar)', q1_25.toLocaleString('pt-BR'), 'Jan+Fev+Mar/25','#3b82f6')
    +_yoyKpi('Q1 FY26 (Jan-Mar)', q1_26.toLocaleString('pt-BR'), 'Jan+Fev+Mar/26','#22c55e')
    +_yoyKpi('Δ Q1', dSign(q1d), 'pico temporada','',dCol(q1d))
    +'</div>';

  /* ── CIMED + RB strip ── */
  var cimedRb='<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin-bottom:16px;">'
    +'<div style="background:#161B22;border-radius:8px;padding:12px;border-left:3px solid #a78bfa;">'
      +'<div style="font-size:8px;font-weight:700;color:#475569;margin-bottom:4px;text-transform:uppercase;letter-spacing:0.06em;">CIMED sem SCJ</div>'
      +'<div style="font-size:22px;font-weight:800;color:#a78bfa;line-height:1;">'+(p.opp_ci||0).toLocaleString('pt-BR')+'</div>'
      +'<div style="font-size:9px;color:#334155;margin-top:3px;">PDVs com CIMED, sem SCJ</div></div>'
    +'<div style="background:#161B22;border-radius:8px;padding:12px;border-left:3px solid #60a5fa;">'
      +'<div style="font-size:8px;font-weight:700;color:#475569;margin-bottom:4px;text-transform:uppercase;letter-spacing:0.06em;">RB sem SCJ</div>'
      +'<div style="font-size:22px;font-weight:800;color:#60a5fa;line-height:1;">'+(p.opp_rb||0).toLocaleString('pt-BR')+'</div>'
      +'<div style="font-size:9px;color:#334155;margin-top:3px;">PDVs com RB, sem SCJ</div></div>'
    +'<div style="background:#161B22;border-radius:8px;padding:12px;border-left:3px solid #f97316;">'
      +'<div style="font-size:8px;font-weight:700;color:#475569;margin-bottom:4px;text-transform:uppercase;letter-spacing:0.06em;">CIMED+RB Consolidado</div>'
      +'<div style="font-size:22px;font-weight:800;color:#f97316;line-height:1;">'+opp.toLocaleString('pt-BR')+'</div>'
      +'<div style="font-size:9px;color:#334155;margin-top:3px;">Deduplicado nacional</div></div>'
    +'<div style="background:#161B22;border-radius:8px;padding:12px;border-left:3px solid #34d399;">'
      +'<div style="font-size:8px;font-weight:700;color:#475569;margin-bottom:4px;text-transform:uppercase;letter-spacing:0.06em;">Reconquistados</div>'
      +'<div style="font-size:22px;font-weight:800;color:#34d399;line-height:1;">'+reconq.toLocaleString('pt-BR')+'</div>'
      +'<div style="font-size:9px;color:'+(atend>=50?'#34d399':atend>=25?'#fbbf24':'#ef4444')+';margin-top:3px;font-weight:600;">'+atend+'% taxa conversão</div></div>'
    +'</div>';

  /* ── Canvas gráfico mensal ── */
  var canvas='<div style="background:#0d1117;border-radius:10px;padding:16px;margin-bottom:16px;">'
    +'<div style="font-size:9px;font-weight:700;color:#475569;letter-spacing:0.08em;margin-bottom:10px;text-transform:uppercase;">PDV·meses por mês — FY25 vs FY26 (Jul→Mar)</div>'
    +'<div style="position:relative;height:200px;"><canvas id="yoy-detail-chart"></canvas></div>'
    +'</div>';

  /* ── UF Breakdown ── */
  var ufHtml='';
  if(p.by_uf && p.by_uf.length){
    var sorted=[].concat(p.by_uf).sort(function(a,b){return b[2]-a[2];}).slice(0,10);
    var maxScj=sorted[0][2]||1;
    ufHtml='<div style="background:#0d1117;border-radius:10px;padding:16px;">'
      +'<div style="font-size:9px;font-weight:700;color:#475569;letter-spacing:0.08em;margin-bottom:12px;text-transform:uppercase;">Cobertura por Estado (Top 10)</div>'
      +'<div style="display:grid;grid-template-columns:repeat(2,1fr);gap:8px;">';
    sorted.forEach(function(u){
      var pct=u[1]>0?Math.round(u[2]/u[1]*100):0;
      var col=pct>=70?'#34d399':pct>=40?'#fbbf24':pct>=20?'#f97316':'#ef4444';
      var bw=u[1]>0?Math.round(u[2]/maxScj*100):0;
      ufHtml+='<div style="display:flex;align-items:center;gap:8px;">'
        +'<span style="font-size:10px;font-weight:700;color:#94a3b8;min-width:22px;">'+u[0]+'</span>'
        +'<div style="flex:1;background:rgba(255,255,255,0.04);border-radius:3px;height:8px;overflow:hidden;">'
          +'<div style="height:100%;background:'+col+';border-radius:3px;width:'+bw+'%;"></div></div>'
        +'<span style="font-size:10px;font-weight:700;color:'+col+';min-width:32px;text-align:right;">'+pct+'%</span>'
        +'<span style="font-size:9px;color:#334155;min-width:60px;">'+u[2].toLocaleString('pt-BR')+'/'+u[1].toLocaleString('pt-BR')+'</span>'
        +'</div>';
    });
    ufHtml+='</div></div>';
  }

  bodyEl.innerHTML = kpi + cimedRb + canvas + ufHtml;

  /* ── Renderizar gráfico após DOM estar pronto ── */
  setTimeout(function(){
    var ctx=document.getElementById('yoy-detail-chart');
    if(!ctx) return;
    if(_yoyChart){ _yoyChart.destroy(); _yoyChart=null; }
    _yoyChart=new Chart(ctx,{
      type:'bar',
      data:{
        labels:lbl,
        datasets:[
          {label:'FY25 (Jul/24-Mar/25)', data:fy25arr,
           backgroundColor:'rgba(59,130,246,0.5)', borderColor:'#3b82f6',
           borderWidth:1.5, borderRadius:4, barPercentage:0.4, categoryPercentage:0.8},
          {label:'FY26 (Jul/25-Mar/26)', data:fy26arr,
           backgroundColor:'rgba(34,197,94,0.6)', borderColor:'#22c55e',
           borderWidth:1.5, borderRadius:4, barPercentage:0.4, categoryPercentage:0.8}
        ]
      },
      options:{
        responsive:true, maintainAspectRatio:false,
        plugins:{legend:{labels:{color:'#94a3b8',font:{size:10}}},
          tooltip:{callbacks:{label:function(c){return c.dataset.label+': '+c.raw.toLocaleString('pt-BR')+' PDV·meses';}}}},
        scales:{
          x:{ticks:{color:'#64748b',font:{size:10}}, grid:{color:'rgba(255,255,255,0.04)'}},
          y:{ticks:{color:'#64748b',font:{size:9},callback:function(v){return v>=1000?(v/1000).toFixed(0)+'K':v;}},
             grid:{color:'rgba(255,255,255,0.05)'}, beginAtZero:true}
        }
      }
    });
  },80);
}

function _yoyKpi(lbl,val,sub,col,dynCol){
  var c=dynCol||col||'#94a3b8';
  return '<div style="background:#0d1117;padding:12px 16px;">'
    +'<div style="font-size:8px;font-weight:700;letter-spacing:0.08em;color:#475569;margin-bottom:4px;text-transform:uppercase;">'+lbl+'</div>'
    +'<div style="font-size:18px;font-weight:800;color:'+c+';line-height:1;">'+val+'</div>'
    +'<div style="font-size:8px;color:#334155;margin-top:3px;">'+sub+'</div>'
    +'</div>';
}

/* ── Ranking geral (todos os provedores) ── */
function _yoyRenderRanking(bodyEl){
  var rows=[];
  (PROV_DATA||[]).forEach(function(p){
    var M=p.monthly||[];
    var fy25=0,fy26=0;
    for(var i=3;i<=11;i++) fy25+=(M[i]||0);
    for(var i=15;i<=23;i++) fy26+=(M[i]||0);
    var q1_25=(M[9]||0)+(M[10]||0)+(M[11]||0);
    var q1_26=(M[21]||0)+(M[22]||0)+(M[23]||0);
    var delta=fy25>0?(fy26-fy25)/fy25*100:null;
    var q1d  =q1_25>0?(q1_26-q1_25)/q1_25*100:null;
    var opp=p.opp_total||0,reconq=p.reconquista||0;
    var atend=(opp+reconq)>0?Math.round(reconq/(opp+reconq)*100):0;
    if(fy25>=100||fy26>=100) rows.push({name:p.name,fy25:fy25,fy26:fy26,delta:delta,
      q1_25:q1_25,q1_26:q1_26,q1d:q1d,opp_ci:p.opp_ci||0,opp_rb:p.opp_rb||0,
      opp:opp,reconq:reconq,atend:atend,monthly:M});
  });
  _yoyTotal=rows.length;

  rows.sort(function(a,b){
    if(_yoySortKey==='opp')    return b.opp-a.opp;
    if(_yoySortKey==='reconq') return b.atend-a.atend;
    if(a.delta===null&&b.delta===null)return 0;
    if(a.delta===null)return 1; if(b.delta===null)return -1;
    return b.delta-a.delta;
  });

  var totFy25=0,totFy26=0,totOpp=0,totReconq=0,totQ1_25=0,totQ1_26=0;
  rows.forEach(function(r){totFy25+=r.fy25;totFy26+=r.fy26;totOpp+=r.opp;totReconq+=r.reconq;totQ1_25+=r.q1_25;totQ1_26+=r.q1_26;});
  var totDelta=totFy25>0?(totFy26-totFy25)/totFy25*100:0;
  var totQ1D  =totQ1_25>0?(totQ1_26-totQ1_25)/totQ1_25*100:0;
  var totAtend=(totOpp+totReconq)>0?Math.round(totReconq/(totOpp+totReconq)*100):0;
  var dSign=function(v){return v===null?'—':(v>=0?'+':'')+v.toFixed(1)+'%';};
  var dCol =function(v){return v===null?'#64748b':v>=0?'#34d399':'#ef4444';};

  /* KPI strip */
  var kpi='<div style="display:grid;grid-template-columns:repeat(5,1fr);gap:1px;background:rgba(255,255,255,0.04);border-radius:10px;overflow:hidden;margin-bottom:16px;">'
    +_yoyKpi('PROVEDORES ATIVOS',rows.length+' mapeados','min. 100 PDV·meses','#94a3b8')
    +_yoyKpi('FY25 Jul→Mar',totFy25.toLocaleString('pt-BR'),'PDV·meses consolid.','#3b82f6')
    +_yoyKpi('FY26 Jul→Mar',totFy26.toLocaleString('pt-BR'),'PDV·meses Jul/25→Mar/26','#22c55e')
    +_yoyKpi('Δ YoY TOTAL',dSign(totDelta),'FY26 vs FY25','',dCol(totDelta))
    +_yoyKpi('CIMED+RB · Conv.',totOpp.toLocaleString('pt-BR')+' · '+totAtend+'%','Oport.+Reconq: '+totReconq.toLocaleString('pt-BR'),'#f97316')
    +'</div>';

  var visible=_yoyShowAll?rows:rows.slice(0,20);

  var table='<div style="overflow-x:auto;">'
    +'<table style="width:100%;border-collapse:collapse;font-size:10px;">'
    +'<thead><tr style="border-bottom:1px solid rgba(255,255,255,0.06);">'
    +'<th style="padding:8px 6px;text-align:left;color:#475569;font-size:8px;font-weight:700;letter-spacing:0.06em;">#</th>'
    +'<th style="padding:8px 6px;text-align:left;color:#475569;font-size:8px;font-weight:700;">PROVEDOR</th>'
    +'<th style="padding:8px 6px;text-align:right;color:#3b82f6;font-size:8px;font-weight:700;white-space:nowrap;">FY25<br>Jul→Mar</th>'
    +'<th style="padding:8px 6px;text-align:right;color:#22c55e;font-size:8px;font-weight:700;white-space:nowrap;">FY26<br>Jul→Mar</th>'
    +'<th style="padding:8px 6px;text-align:right;color:#fbbf24;font-size:8px;font-weight:700;white-space:nowrap;">Δ YoY</th>'
    +'<th style="padding:8px 6px;text-align:right;color:#94a3b8;font-size:8px;font-weight:700;white-space:nowrap;">Q1/25</th>'
    +'<th style="padding:8px 6px;text-align:right;color:#94a3b8;font-size:8px;font-weight:700;white-space:nowrap;">Q1/26</th>'
    +'<th style="padding:8px 6px;text-align:right;color:#94a3b8;font-size:8px;font-weight:700;white-space:nowrap;">Δ Q1</th>'
    +'<th style="padding:8px 6px;text-align:right;color:#a78bfa;font-size:8px;font-weight:700;white-space:nowrap;">CIMED<br>sem SCJ</th>'
    +'<th style="padding:8px 6px;text-align:right;color:#60a5fa;font-size:8px;font-weight:700;white-space:nowrap;">RB<br>sem SCJ</th>'
    +'<th style="padding:8px 6px;text-align:right;color:#f97316;font-size:8px;font-weight:700;white-space:nowrap;">CIMED+RB<br>Consol.</th>'
    +'<th style="padding:8px 6px;text-align:right;color:#34d399;font-size:8px;font-weight:700;white-space:nowrap;">Reconq.</th>'
    +'<th style="padding:8px 6px;text-align:right;color:#f97316;font-size:8px;font-weight:700;white-space:nowrap;">Conv.%</th>'
    +'<th style="padding:8px 6px;color:#94a3b8;font-size:8px;font-weight:700;white-space:nowrap;">Trend FY26</th>'
    +'</tr></thead><tbody>';

  visible.forEach(function(r,idx){
    var rank=idx+1;
    var icon=rank===1?'🥇':rank===2?'🥈':rank===3?'🥉':rank;
    var dc=dCol(r.delta), qdc=dCol(r.q1d);
    var isTop=rank<=3&&_yoySortKey==='delta'&&r.delta>0;
    var isBad=r.delta!==null&&r.delta<-20;
    var bg=isTop?'background:rgba(52,211,153,0.04);':isBad?'background:rgba(239,68,68,0.03);':'';
    var aco=r.atend>=50?'#34d399':r.atend>=25?'#fbbf24':'#ef4444';
    // spark
    var sv=[]; for(var i=15;i<=23;i++) sv.push(r.monthly[i]||0);
    var smx=Math.max.apply(null,sv)||1;
    var spark='<div style="display:flex;align-items:flex-end;gap:1px;height:20px;width:80px;">';
    sv.forEach(function(v){
      var h=Math.max(1,Math.round(v/smx*18));
      var c=v>smx*0.7?'#34d399':v>smx*0.4?'#fbbf24':'#94a3b8';
      spark+='<div style="flex:1;height:'+h+'px;background:'+c+';border-radius:1px;opacity:0.8;"></div>';
    });
    spark+='</div>';

    table+='<tr style="border-bottom:0.5px solid rgba(255,255,255,0.04);'+bg+'" '
      +'onmouseover="this.style.background=\'rgba(34,197,94,0.05)\'" onmouseout="this.style.background=\''+bg.replace('background:','').replace(';','')+'\'">'
      +'<td style="padding:7px 6px;color:#475569;font-size:9px;font-weight:700;text-align:center;">'+icon+'</td>'
      +'<td style="padding:7px 6px;font-size:10px;font-weight:600;color:#D1D5DB;max-width:150px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">'
        +'<span onclick="yoySelectProv(\''+r.name.replace(/'/g,"\\'")+'\');" style="cursor:pointer;text-decoration:underline;text-decoration-color:#334155;text-underline-offset:3px;" onmouseover="this.style.color=\'#22c55e\'" onmouseout="this.style.color=\'#D1D5DB\'">'+r.name+'</span>'
      +'</td>'
      +'<td style="padding:7px 6px;text-align:right;color:#3b82f6;font-size:10px;">'+r.fy25.toLocaleString('pt-BR')+'</td>'
      +'<td style="padding:7px 6px;text-align:right;color:#22c55e;font-size:10px;font-weight:600;">'+r.fy26.toLocaleString('pt-BR')+'</td>'
      +'<td style="padding:7px 6px;text-align:right;font-size:11px;font-weight:800;color:'+dc+';">'+dSign(r.delta)+'</td>'
      +'<td style="padding:7px 6px;text-align:right;color:#64748b;font-size:9px;">'+r.q1_25.toLocaleString('pt-BR')+'</td>'
      +'<td style="padding:7px 6px;text-align:right;color:#94a3b8;font-size:9px;font-weight:600;">'+r.q1_26.toLocaleString('pt-BR')+'</td>'
      +'<td style="padding:7px 6px;text-align:right;font-size:10px;font-weight:700;color:'+qdc+';">'+dSign(r.q1d)+'</td>'
      +'<td style="padding:7px 6px;text-align:right;color:#a78bfa;font-size:10px;">'+(r.opp_ci>0?r.opp_ci.toLocaleString('pt-BR'):'<span style="color:#1e293b">—</span>')+'</td>'
      +'<td style="padding:7px 6px;text-align:right;color:#60a5fa;font-size:10px;">'+(r.opp_rb>0?r.opp_rb.toLocaleString('pt-BR'):'<span style="color:#1e293b">—</span>')+'</td>'
      +'<td style="padding:7px 6px;text-align:right;color:#f97316;font-size:10px;font-weight:600;">'+(r.opp>0?r.opp.toLocaleString('pt-BR'):'<span style="color:#1e293b">—</span>')+'</td>'
      +'<td style="padding:7px 6px;text-align:right;color:#34d399;font-size:10px;">'+(r.reconq>0?r.reconq.toLocaleString('pt-BR'):'<span style="color:#1e293b">—</span>')+'</td>'
      +'<td style="padding:7px 6px;text-align:right;font-size:10px;font-weight:700;color:'+aco+';">'+(r.opp>0?r.atend+'%':'<span style="color:#1e293b">—</span>')+'</td>'
      +'<td style="padding:7px 6px;">'+spark+'</td>'
      +'</tr>';
  });

  /* Linha total */
  table+='<tr style="border-top:1px solid rgba(251,191,36,0.2);background:rgba(251,191,36,0.03);">'
    +'<td></td>'
    +'<td style="padding:8px 6px;font-size:10px;font-weight:800;color:#fbbf24;">TOTAL GERAL</td>'
    +'<td style="padding:8px 6px;text-align:right;color:#3b82f6;font-weight:700;">'+totFy25.toLocaleString('pt-BR')+'</td>'
    +'<td style="padding:8px 6px;text-align:right;color:#22c55e;font-weight:700;">'+totFy26.toLocaleString('pt-BR')+'</td>'
    +'<td style="padding:8px 6px;text-align:right;font-size:11px;font-weight:800;color:'+dCol(totDelta)+';">'+dSign(totDelta)+'</td>'
    +'<td style="padding:8px 6px;text-align:right;color:#64748b;font-size:9px;">'+totQ1_25.toLocaleString('pt-BR')+'</td>'
    +'<td style="padding:8px 6px;text-align:right;color:#94a3b8;font-size:9px;font-weight:700;">'+totQ1_26.toLocaleString('pt-BR')+'</td>'
    +'<td style="padding:8px 6px;text-align:right;font-size:10px;font-weight:800;color:'+dCol(totQ1D)+';">'+dSign(totQ1D)+'</td>'
    +'<td colspan="2"></td>'
    +'<td style="padding:8px 6px;text-align:right;color:#f97316;font-weight:700;">'+totOpp.toLocaleString('pt-BR')+'</td>'
    +'<td style="padding:8px 6px;text-align:right;color:#34d399;font-weight:700;">'+totReconq.toLocaleString('pt-BR')+'</td>'
    +'<td style="padding:8px 6px;text-align:right;font-size:10px;font-weight:800;color:#f97316;">'+totAtend+'%</td>'
    +'<td></td>'
    +'</tr>';
  table+='</tbody></table></div>';

  var btnAll='<div style="text-align:center;margin-top:10px;">'
    +'<button onclick="toggleYoYAll(this)" style="font-size:10px;padding:6px 18px;border-radius:8px;border:0.5px solid rgba(255,255,255,0.1);background:transparent;color:#64748b;cursor:pointer;">'
    +(_yoyShowAll?'Ver Top 20':'Ver todos ('+rows.length+')')
    +'</button></div>';

  bodyEl.innerHTML=kpi+table+btnAll;
}

/* ── Entry point ── */
function renderProvYoYCard(){
  var bodyEl=document.getElementById('prov-yoy-body');
  if(!bodyEl||typeof PROV_DATA==='undefined') return;

  if(_yoySelProv){
    var p=null;
    for(var i=0;i<PROV_DATA.length;i++){if(PROV_DATA[i].name===_yoySelProv){p=PROV_DATA[i];break;}}
    if(p){ _yoyRenderDetail(p,bodyEl); return; }
  }
  _yoyRenderRanking(bodyEl);
}

"""

ANCHOR_JS = '\nfunction initSellin(){'
if ANCHOR_JS not in html:
    print("ERRO: anchor JS nao encontrado!")
    exit(1)
html = html.replace(ANCHOR_JS, NEW_JS + ANCHOR_JS, 1)
print("JS v2 inserido")

# ══════════════════════════════════════════════════════════════
# 2. Substituir HTML do card (manter a div mas trocar o conteúdo interno)
# ══════════════════════════════════════════════════════════════

OLD_CARD = """
    <!-- EVOLUÇÃO YoY POR PROVEDOR -->
    <div id="prov-yoy-card" class="card full" style="margin-bottom:18px;">
      <div class="card-header" style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:12px;margin-bottom:16px;">
        <div>
          <div style="font-size:10px;font-weight:700;letter-spacing:0.1em;color:#22c55e;margin-bottom:4px;">📈 EVOLUÇÃO ANUAL — TODOS OS PROVEDORES</div>
          <div class="card-title">Positivação FY25 vs FY26 por Provedor · Jul→Mar (9 meses)</div>
          <div class="card-sub">PDV·meses acumulados Jul/24→Mar/25 vs Jul/25→Mar/26 · CIMED + RB consolidado · ordenável</div>
        </div>
        <div style="display:flex;gap:6px;flex-wrap:wrap;align-items:center;">
          <span style="font-size:9px;color:#475569;font-weight:700;text-transform:uppercase;letter-spacing:0.06em;">Ordenar por:</span>
          <button class="yoy-sort-btn" onclick="setYoYSort('delta',this)"
            style="font-size:10px;font-weight:700;padding:4px 12px;border-radius:6px;border:0.5px solid rgba(251,191,36,0.3);cursor:pointer;background:rgba(251,191,36,0.15);color:#fbbf24;">
            Δ% Positivação
          </button>
          <button class="yoy-sort-btn" onclick="setYoYSort('opp',this)"
            style="font-size:10px;font-weight:700;padding:4px 12px;border-radius:6px;border:0.5px solid rgba(255,255,255,0.07);cursor:pointer;background:transparent;color:#64748b;">
            Oportunidades
          </button>
          <button class="yoy-sort-btn" onclick="setYoYSort('reconq',this)"
            style="font-size:10px;font-weight:700;padding:4px 12px;border-radius:6px;border:0.5px solid rgba(255,255,255,0.07);cursor:pointer;background:transparent;color:#64748b;">
            % Reconquista
          </button>
        </div>
      </div>
      <div id="prov-yoy-body">
        <div style="text-align:center;padding:40px;color:#334155;font-size:12px;">Carregando...</div>
      </div>
    </div>

"""

NEW_CARD = """
    <!-- EVOLUÇÃO YoY POR PROVEDOR v2 -->
    <div id="prov-yoy-card" class="card full" style="margin-bottom:18px;">
      <div class="card-header" style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:12px;margin-bottom:14px;">
        <div>
          <div style="font-size:10px;font-weight:700;letter-spacing:0.1em;color:#22c55e;margin-bottom:4px;">📈 EVOLUÇÃO ANUAL — TODOS OS PROVEDORES</div>
          <div class="card-title">Positivação FY25 vs FY26 por Provedor · Jul→Mar (9 meses)</div>
          <div class="card-sub">PDV·meses Jul/24→Mar/25 vs Jul/25→Mar/26 · CIMED + RB separados e consolidados · Clique no nome para análise completa</div>
        </div>
        <div style="display:flex;gap:6px;flex-wrap:wrap;align-items:center;">
          <span style="font-size:9px;color:#475569;font-weight:700;text-transform:uppercase;letter-spacing:0.06em;">Ordenar por:</span>
          <button class="yoy-sort-btn" onclick="setYoYSort('delta',this)"
            style="font-size:10px;font-weight:700;padding:4px 12px;border-radius:6px;border:0.5px solid rgba(251,191,36,0.3);cursor:pointer;background:rgba(251,191,36,0.15);color:#fbbf24;">
            Δ% Positivação
          </button>
          <button class="yoy-sort-btn" onclick="setYoYSort('opp',this)"
            style="font-size:10px;font-weight:700;padding:4px 12px;border-radius:6px;border:0.5px solid rgba(255,255,255,0.07);cursor:pointer;background:transparent;color:#64748b;">
            Oportunidades
          </button>
          <button class="yoy-sort-btn" onclick="setYoYSort('reconq',this)"
            style="font-size:10px;font-weight:700;padding:4px 12px;border-radius:6px;border:0.5px solid rgba(255,255,255,0.07);cursor:pointer;background:transparent;color:#64748b;">
            % Reconquista
          </button>
        </div>
      </div>

      <!-- Barra de busca de provedor -->
      <div style="position:relative;margin-bottom:14px;">
        <div style="display:flex;gap:8px;align-items:center;">
          <div style="position:relative;flex:1;">
            <input id="yoy-filt-input" type="text" placeholder="🔍  Buscar provedor para análise detalhada..."
              oninput="yoyFiltKey(event)"
              style="width:100%;box-sizing:border-box;background:#0d1117;border:1px solid rgba(34,197,94,0.25);border-radius:8px;padding:10px 14px;color:#D1D5DB;font-size:12px;outline:none;"
              onfocus="this.style.borderColor='rgba(34,197,94,0.5)'" onblur="setTimeout(function(){var l=document.getElementById('yoy-filt-list');if(l)l.style.display='none';},200)"/>
            <div id="yoy-filt-list" style="display:none;position:absolute;left:0;right:0;top:100%;z-index:99;background:#161B22;border:1px solid rgba(34,197,94,0.2);border-radius:0 0 8px 8px;max-height:280px;overflow-y:auto;box-shadow:0 8px 24px rgba(0,0,0,0.5);"></div>
          </div>
          <button onclick="yoyClearProv()" style="padding:10px 16px;font-size:11px;font-weight:700;color:#94a3b8;background:transparent;border:0.5px solid rgba(255,255,255,0.1);border-radius:8px;cursor:pointer;white-space:nowrap;">✕ Limpar</button>
        </div>
      </div>

      <div id="prov-yoy-body">
        <div style="text-align:center;padding:40px;color:#334155;font-size:12px;">Carregando...</div>
      </div>
    </div>

"""

if OLD_CARD not in html:
    print("ERRO: HTML antigo do card nao encontrado!")
    exit(1)
html = html.replace(OLD_CARD, NEW_CARD, 1)
print("HTML do card atualizado com filtro de provedor")

# ══════════════════════════════════════════════════════════════
# 3. SALVAR
# ══════════════════════════════════════════════════════════════
ts = datetime.now().strftime('%Y%m%d_%H%M')
versao = VER / f"Dashboard_Farma_Sul_{ts}_ProvYoYv2.html"
shutil.copy(DASH, versao)
print(f"\nVersao salva: {versao.name}")

DASH.write_text(html, encoding='utf-8')
print(f"Dashboard: {len(html):,} chars (era {orig_len:,})")

dl = DL / f"Dashboard_FarmaSul_Giovano_{ts}.html"
shutil.copy(DASH, dl)
print(f"Downloads: {dl.name}")
print("\nDONE.")
