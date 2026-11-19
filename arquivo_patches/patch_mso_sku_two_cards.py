"""
patch_mso_sku_two_cards.py
1. Reverte mso-sku-card de volta para FYTD25 vs FYTD26 (renderMSOSku original)
2. Cria NOVO card mso-sku-jm-card com Jan-Mar/25 vs Jan-Mar/26 (renderMSOSkuJanMar)
   inserido imediatamente abaixo do card existente
"""
import sys, shutil
sys.stdout.reconfigure(encoding='utf-8')
from datetime import datetime
from pathlib import Path

BASE = Path(r"C:\Users\valqu\OneDrive\Documentos\Claude\Projects\projeto Dashboard_farma_sul\Dashboard_farma_sul")
DASH = BASE / "Dashboard_Farma_Sul_20260512_2220.html"
VER  = BASE / "versoes"
DL   = Path.home() / "Downloads"

ts = datetime.now().strftime('%Y%m%d_%H%M')
shutil.copy(DASH, VER / f"Dashboard_Farma_Sul_{ts}_PreTwoCardsSku.html")
print(f"Backup: Dashboard_Farma_Sul_{ts}_PreTwoCardsSku.html")

html = DASH.read_text(encoding='utf-8')
orig = len(html)

# ══════════════════════════════════════════════════════════════════════════════
# 1. REVERTER labels do card existente (JAN-MAR → FYTD)
# ══════════════════════════════════════════════════════════════════════════════
label_reverts = [
    ('MARKET SHARE POR SKU — JAN-MAR/26',          'MARKET SHARE POR SKU — FYTD26'),
    ('$ Share por SKU · Jan-Mar/26 vs Jan-Mar/25',  '$ Share por SKU · FYTD26 vs FYTD25'),
    ('MARKET SHARE SKU — Jan-Mar/26',               'MARKET SHARE SKU — FYTD26'),
    ('VAR MARKET SHARE SKU — Jan-Mar/26 vs Jan-Mar/25', 'VAR MARKET SHARE SKU — FYTD26 vs FYTD25'),
    ('Share por SKU · Jan-Mar/26 vs Jan-Mar/25 · Personal Repellent',
     'Share por SKU · FYTD · Personal Repellent'),
]
for old, new in label_reverts:
    if old in html:
        html = html.replace(old, new)
        print(f"OK revert label: {old[:45]}")
    else:
        print(f"AVISO: nao encontrado para reverter: {old[:45]}")

# ══════════════════════════════════════════════════════════════════════════════
# 2. REVERTER renderMSOSku() para FYTD
# ══════════════════════════════════════════════════════════════════════════════
OLD_FN_MARKER = '\n/* ═══ MARKET SHARE POR SKU — mso-sku-card (Jan-Mar) ═══ */'
FN_END_MARKER = '\nfunction fN(n){return Number(n).toLocaleString'

assert OLD_FN_MARKER in html, "ERRO: marcador da funcao Jan-Mar nao encontrado"
idx_s = html.index(OLD_FN_MARKER)
idx_e = html.index(FN_END_MARKER, idx_s)

FYTD_FN = r"""
/* ═══ MARKET SHARE POR SKU — mso-sku-card ═══ */
var _msoSkuChartL=null,_msoSkuChartR=null;
function initMSOSku(){
  var sel=document.getElementById('msoSkuMktSel');
  if(!sel||sel.options.length>0)return;
  var mks=typeof SKU_MKT_DATA!=='undefined'?Object.keys(SKU_MKT_DATA):['T.BR Farma'];
  mks.forEach(function(m){var o=document.createElement('option');o.value=m;o.textContent=m;if(m==='T.BR Farma')o.selected=true;sel.appendChild(o);});
}
function renderMSOSku(){
  initMSOSku();
  var sel=document.getElementById('msoSkuMktSel');
  var mkt=sel?sel.value:'T.BR Farma';
  var sub=document.getElementById('mso-sku-sub');
  if(sub) sub.textContent='Share por SKU · FYTD26 vs FYTD25 · '+mkt+' · Personal Repellent';
  var d=typeof SKU_MKT_DATA!=='undefined'?SKU_MKT_DATA[mkt]:null;
  if(!d)return;
  var n=d.skus.length;
  var idx=Array.from({length:n},function(_,i){return i;}).sort(function(a,b){return d.fytd26[a]-d.fytd26[b];});
  var labels=idx.map(function(i){return d.skus[i];});
  var sh26=idx.map(function(i){return d.fytd26[i];});
  var sh25=idx.map(function(i){return d.fytd25[i];});
  var vars=idx.map(function(i){return d.var[i];});
  var bgC=labels.map(function(l){return(_skuShrBrandColors&&_skuShrBrandColors[l.trim()])||'#374151';});
  var vC=vars.map(function(v){return v>=0?'rgba(52,211,153,0.85)':'rgba(239,68,68,0.85)';});
  var vB=vars.map(function(v){return v>=0?'#34d399':'#ef4444';});
  /* KPIs */
  var kEl=document.getElementById('mso-sku-kpis');
  if(kEl){
    var tI=d.fytd26.indexOf(Math.max.apply(null,d.fytd26));
    var gA=d.var.map(function(v,i){return{v:v,i:i};}).filter(function(x){return x.v>0;}).sort(function(a,b){return b.v-a.v;});
    var lA=d.var.map(function(v,i){return{v:v,i:i};}).filter(function(x){return x.v<0;}).sort(function(a,b){return a.v-b.v;});
    var scjT=0;
    d.skus.forEach(function(s,i){if(s.indexOf('OFF!')>=0||s.indexOf('Exposis')>=0||s.indexOf('Xô')>=0||s.indexOf('Xo')>=0)scjT+=d.fytd26[i];});
    var chips=[
      {l:'SKU LÍDER',v:d.skus[tI].trim().substring(0,22),s:d.fytd26[tI].toFixed(2)+'% FYTD26',c:'#fbbf24'},
      {l:'MAIOR GANHO Δpp',v:gA.length?'+'+gA[0].v.toFixed(2)+'pp':'—',s:gA.length?d.skus[gA[0].i].trim().substring(0,22):'',c:'#34d399'},
      {l:'MAIOR QUEDA Δpp',v:lA.length?lA[0].v.toFixed(2)+'pp':'—',s:lA.length?d.skus[lA[0].i].trim().substring(0,22):'',c:'#ef4444'},
      {l:'SCJ COMBINED',v:scjT.toFixed(2)+'%',s:'Share FYTD26 combinado',c:'#3b82f6'}
    ];
    kEl.innerHTML='<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:8px;">'+chips.map(function(k){
      return '<div style="background:#161B22;border-radius:8px;padding:10px 12px;border-top:2px solid '+k.c+'">'
        +'<div style="font-size:8px;font-weight:700;letter-spacing:0.1em;color:#3d6b63;margin-bottom:4px;">'+k.l+'</div>'
        +'<div style="font-size:15px;font-weight:800;color:'+k.c+';line-height:1;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">'+k.v+'</div>'
        +'<div style="font-size:8.5px;color:#94A3B8;margin-top:3px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">'+k.s+'</div>'
        +'</div>';
    }).join('')+'</div>';
  }
  /* Left chart */
  var lC=document.getElementById('mso-sku-bar-l');
  if(lC){
    if(_msoSkuChartL){try{_msoSkuChartL.destroy();}catch(e){}_msoSkuChartL=null;}
    var mx=Math.max.apply(null,sh26.concat(sh25));
    _msoSkuChartL=new Chart(lC,{type:'bar',data:{labels:labels,datasets:[
      {label:'FYTD25',data:sh25,backgroundColor:'rgba(156,163,175,0.18)',borderColor:'rgba(156,163,175,0.4)',borderWidth:1,borderRadius:2},
      {label:'FYTD26',data:sh26,backgroundColor:bgC,borderColor:bgC,borderWidth:0,borderRadius:3}
    ]},options:{indexAxis:'y',responsive:true,maintainAspectRatio:false,
      plugins:{legend:{display:false},tooltip:{callbacks:{label:function(c){return c.dataset.label+': '+c.parsed.x.toFixed(2)+'%';}}}},
      scales:{x:{min:0,max:Math.ceil(mx)+2,ticks:{color:'#94A3B8',font:{size:9},callback:function(v){return v+'%';}},grid:{color:'rgba(245,225,164,0.05)'}},
              y:{ticks:{color:'#e2e8f0',font:{size:10,weight:'600'}},grid:{display:false}}}}});
  }
  /* Right chart */
  var rC=document.getElementById('mso-sku-bar-r');
  if(rC){
    if(_msoSkuChartR){try{_msoSkuChartR.destroy();}catch(e){}_msoSkuChartR=null;}
    var mv=Math.max.apply(null,vars.map(Math.abs)),lim=Math.ceil(mv*10)/10+0.3;
    _msoSkuChartR=new Chart(rC,{type:'bar',data:{labels:labels,datasets:[{label:'Var pp',data:vars,backgroundColor:vC,borderColor:vB,borderWidth:1,borderRadius:3}]},
      options:{indexAxis:'y',responsive:true,maintainAspectRatio:false,
        plugins:{legend:{display:false},tooltip:{callbacks:{label:function(c){var v=c.parsed.x;return 'Var: '+(v>=0?'+':'')+v.toFixed(2)+'pp';}}}},
        scales:{x:{min:-lim,max:lim,ticks:{color:'#94A3B8',font:{size:9},callback:function(v){return(v>=0?'+':'')+v.toFixed(1)+'pp';}},grid:{color:'rgba(245,225,164,0.05)'},border:{color:'rgba(255,255,255,0.15)'}},
                y:{ticks:{color:'#e2e8f0',font:{size:10,weight:'600'}},grid:{display:false}}}},
      plugins:[{id:'msoSkuZL',afterDraw:function(ch){var ct=ch.ctx,xa=ch.scales.x,ya=ch.scales.y,x0=xa.getPixelForValue(0);ct.save();ct.strokeStyle='rgba(255,255,255,0.25)';ct.lineWidth=1;ct.beginPath();ct.moveTo(x0,ya.top);ct.lineTo(x0,ya.bottom);ct.stroke();ct.restore();}}]});
  }
  /* Diagnostic */
  var dEl=document.getElementById('mso-sku-diag');
  if(dEl){
    var tI2=d.fytd26.indexOf(Math.max.apply(null,d.fytd26));
    var gD=[],lD=[];
    d.skus.forEach(function(s,i){
      var sc=s.indexOf('OFF!')>=0||s.indexOf('Exposis')>=0||s.indexOf('Xô')>=0||s.indexOf('Xo')>=0;
      if(sc){if(d.var[i]>0)gD.push('<strong style="color:#fbbf24">'+s.trim()+'</strong> <span style="color:#34d399">+'+d.var[i].toFixed(2)+'pp</span>');
             else if(d.var[i]<0)lD.push('<strong style="color:#fbbf24">'+s.trim()+'</strong> <span style="color:#ef4444">'+d.var[i].toFixed(2)+'pp</span>');}
    });
    var top3=d.fytd26.slice().sort(function(a,b){return b-a;}).slice(0,3).reduce(function(s,v){return s+v;},0);
    var dh='\u{1F50D} <span style="font-weight:800;color:#fbbf24;letter-spacing:.4px;">DIAGNÓSTICO SKU · '+mkt+'</span><br>';
    dh+='\u{1F3C6} <strong style="color:#e2e8f0;">SKU Líder:</strong> <strong style="color:#fbbf24;">'+d.skus[tI2]+'</strong> — '+d.fytd26[tI2].toFixed(2)+'% FYTD26 <span style="color:'+(d.var[tI2]>=0?'#34d399':'#ef4444')+'">'+(d.var[tI2]>=0?'▲ +':'▼ ')+Math.abs(d.var[tI2]).toFixed(2)+'pp</span> vs FYTD25.<br>';
    dh+='\u{1F4CA} <strong style="color:#e2e8f0;">Top 3 SKUs</strong> representam <strong style="color:#67e8f9;">'+top3.toFixed(1)+'%</strong> do mercado.<br>';
    if(gD.length)dh+='✅ <strong style="color:#34d399;">Ganharam share:</strong> '+gD.join(' · ')+'.<br>';
    if(lD.length)dh+='⚠️ <strong style="color:#ef4444;">Perderam share:</strong> '+lD.join(' · ')+'.';
    dEl.innerHTML='<div style="font-size:11px;color:#D1D5DB;line-height:1.8;">'+dh+'</div>';
  }
}"""

html = html[:idx_s] + FYTD_FN + html[idx_e:]
print("OK: renderMSOSku() revertida para FYTD")

# ══════════════════════════════════════════════════════════════════════════════
# 3. HTML DO NOVO CARD JAN-MAR
# ══════════════════════════════════════════════════════════════════════════════
JM_CARD_HTML = (
    "\n\n  <!-- CARD MARKET SHARE POR SKU — JAN-MAR -->"
    "\n  <div id=\"mso-sku-jm-card\" class=\"card full\" style=\"margin-bottom:18px;\">"
    "\n    <div class=\"card-header\" style=\"display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:12px;margin-bottom:14px;\">"
    "\n      <div>"
    "\n        <div style=\"font-size:10px;font-weight:700;letter-spacing:0.1em;color:#34d399;margin-bottom:4px;\">📦 MARKET SHARE POR SKU — JAN·FEV·MAR</div>"
    "\n        <div class=\"card-title\">$ Share por SKU · Jan-Mar/26 vs Jan-Mar/25</div>"
    "\n        <div id=\"mso-sku-jm-sub\" class=\"card-sub\">Share por SKU · Jan-Mar/26 vs Jan-Mar/25 · Personal Repellent</div>"
    "\n      </div>"
    "\n      <select id=\"msoSkuJMSel\" onchange=\"renderMSOSkuJanMar()\""
    "\n        style=\"background:#161B22;border:1px solid rgba(52,211,153,0.3);border-radius:8px;color:#e2e8f0;font-size:11px;padding:6px 12px;cursor:pointer;min-width:160px;\">"
    "\n      </select>"
    "\n    </div>"
    "\n    <div id=\"mso-sku-jm-kpis\" style=\"margin-bottom:14px;\"></div>"
    "\n    <div style=\"display:flex;gap:16px;align-items:stretch;\">"
    "\n      <div style=\"flex:1.6;min-width:0;\">"
    "\n        <div style=\"font-size:9px;font-weight:700;letter-spacing:0.1em;color:#94A3B8;margin-bottom:8px;\">MARKET SHARE SKU — Jan-Mar/26</div>"
    "\n        <div style=\"height:320px;position:relative;\"><canvas id=\"mso-sku-jm-bar-l\"></canvas></div>"
    "\n      </div>"
    "\n      <div style=\"flex:1;min-width:0;\">"
    "\n        <div style=\"font-size:9px;font-weight:700;letter-spacing:0.1em;color:#94A3B8;margin-bottom:8px;\">VAR MARKET SHARE SKU — Jan-Mar/26 vs Jan-Mar/25</div>"
    "\n        <div style=\"height:320px;position:relative;\"><canvas id=\"mso-sku-jm-bar-r\"></canvas></div>"
    "\n      </div>"
    "\n    </div>"
    "\n    <div style=\"display:flex;gap:14px;flex-wrap:wrap;margin-top:10px;padding-top:8px;border-top:0.5px solid rgba(255,255,255,0.06);\">"
    "\n      <span style=\"display:flex;align-items:center;gap:5px;font-size:9px;color:#94A3B8;\"><span style=\"width:10px;height:10px;border-radius:2px;background:#f97316;display:inline-block;\"></span>OFF!</span>"
    "\n      <span style=\"display:flex;align-items:center;gap:5px;font-size:9px;color:#94A3B8;\"><span style=\"width:10px;height:10px;border-radius:2px;background:#38bdf8;display:inline-block;\"></span>Xô Inset</span>"
    "\n      <span style=\"display:flex;align-items:center;gap:5px;font-size:9px;color:#94A3B8;\"><span style=\"width:10px;height:10px;border-radius:2px;background:#a78bfa;display:inline-block;\"></span>Exposis</span>"
    "\n      <span style=\"display:flex;align-items:center;gap:5px;font-size:9px;color:#94A3B8;\"><span style=\"width:10px;height:10px;border-radius:2px;background:#374151;display:inline-block;\"></span>All Others</span>"
    "\n      <span style=\"display:flex;align-items:center;gap:5px;font-size:9px;color:#94A3B8;\"><span style=\"width:10px;height:10px;border-radius:2px;background:#34d399;display:inline-block;\"></span>Var +</span>"
    "\n      <span style=\"display:flex;align-items:center;gap:5px;font-size:9px;color:#94A3B8;\"><span style=\"width:10px;height:10px;border-radius:2px;background:#ef4444;display:inline-block;\"></span>Var -</span>"
    "\n    </div>"
    "\n    <div id=\"mso-sku-jm-diag\" style=\"margin-top:12px;padding:12px 16px;background:rgba(52,211,153,0.04);border-radius:10px;border-left:3px solid #34d399;font-size:11px;color:#D1D5DB;line-height:1.8;\"></div>"
    "\n  </div>"
)

# Inserir APÓS o mso-sku-card (antes de <!-- CARD VISAO FISCAL FYTD)
JM_HTML_ANCHOR = "\n\n\n  <!-- CARD VISAO FISCAL FYTD"
assert JM_HTML_ANCHOR in html, "ERRO: ancora HTML p/ novo card nao encontrada"
html = html.replace(JM_HTML_ANCHOR, JM_CARD_HTML + JM_HTML_ANCHOR, 1)
print("OK: HTML do novo card Jan-Mar inserido")

# ══════════════════════════════════════════════════════════════════════════════
# 4. JS DA FUNÇÃO renderMSOSkuJanMar()
# ══════════════════════════════════════════════════════════════════════════════
JM_FN = r"""
/* ═══ MARKET SHARE POR SKU — Jan-Mar (mso-sku-jm-card) ═══ */
var _msoSkuJMChartL=null,_msoSkuJMChartR=null;
function initMSOSkuJM(){
  var sel=document.getElementById('msoSkuJMSel');
  if(!sel||sel.options.length>0)return;
  var mks=typeof SKU_MKT_MONTHLY!=='undefined'?Object.keys(SKU_MKT_MONTHLY):['T.BR Farma'];
  mks.forEach(function(m){var o=document.createElement('option');o.value=m;o.textContent=m;if(m==='T.BR Farma')o.selected=true;sel.appendChild(o);});
}
function renderMSOSkuJanMar(){
  initMSOSkuJM();
  var sel=document.getElementById('msoSkuJMSel');
  var mkt=sel?sel.value:'T.BR Farma';
  var sub=document.getElementById('mso-sku-jm-sub');
  if(sub) sub.textContent='Share por SKU · Jan-Mar/26 vs Jan-Mar/25 · '+mkt+' · Personal Repellent';
  var d=typeof SKU_MKT_MONTHLY!=='undefined'?SKU_MKT_MONTHLY[mkt]:null;
  if(!d)return;
  var n=d.skus.length;
  var idx=Array.from({length:n},function(_,i){return i;}).sort(function(a,b){return d.janmar26[a]-d.janmar26[b];});
  var labels=idx.map(function(i){return d.skus[i];});
  var sh26=idx.map(function(i){return d.janmar26[i];});
  var sh25=idx.map(function(i){return d.janmar25[i];});
  var vars=idx.map(function(i){return d.var[i];});
  var bgC=labels.map(function(l){return(_skuShrBrandColors&&_skuShrBrandColors[l.trim()])||'#374151';});
  var vC=vars.map(function(v){return v>=0?'rgba(52,211,153,0.85)':'rgba(239,68,68,0.85)';});
  var vB=vars.map(function(v){return v>=0?'#34d399':'#ef4444';});
  /* KPIs */
  var kEl=document.getElementById('mso-sku-jm-kpis');
  if(kEl){
    var tI=d.janmar26.indexOf(Math.max.apply(null,d.janmar26));
    var gA=d.var.map(function(v,i){return{v:v,i:i};}).filter(function(x){return x.v>0;}).sort(function(a,b){return b.v-a.v;});
    var lA=d.var.map(function(v,i){return{v:v,i:i};}).filter(function(x){return x.v<0;}).sort(function(a,b){return a.v-b.v;});
    var scjT=0;
    d.skus.forEach(function(s,i){if(s.indexOf('OFF!')>=0||s.indexOf('Exposis')>=0||s.indexOf('Xô')>=0||s.indexOf('Xo')>=0)scjT+=d.janmar26[i];});
    var chips=[
      {l:'SKU LÍDER',v:d.skus[tI].trim().substring(0,22),s:d.janmar26[tI].toFixed(2)+'% Jan-Mar/26',c:'#34d399'},
      {l:'MAIOR GANHO Δpp',v:gA.length?'+'+gA[0].v.toFixed(2)+'pp':'—',s:gA.length?d.skus[gA[0].i].trim().substring(0,22):'',c:'#3b82f6'},
      {l:'MAIOR QUEDA Δpp',v:lA.length?lA[0].v.toFixed(2)+'pp':'—',s:lA.length?d.skus[lA[0].i].trim().substring(0,22):'',c:'#ef4444'},
      {l:'SCJ COMBINED',v:scjT.toFixed(2)+'%',s:'Share Jan-Mar/26 combinado',c:'#fbbf24'}
    ];
    kEl.innerHTML='<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:8px;">'+chips.map(function(k){
      return '<div style="background:#161B22;border-radius:8px;padding:10px 12px;border-top:2px solid '+k.c+'">'
        +'<div style="font-size:8px;font-weight:700;letter-spacing:0.1em;color:#3d6b63;margin-bottom:4px;">'+k.l+'</div>'
        +'<div style="font-size:15px;font-weight:800;color:'+k.c+';line-height:1;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">'+k.v+'</div>'
        +'<div style="font-size:8.5px;color:#94A3B8;margin-top:3px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">'+k.s+'</div>'
        +'</div>';
    }).join('')+'</div>';
  }
  /* Left chart */
  var lC=document.getElementById('mso-sku-jm-bar-l');
  if(lC){
    if(_msoSkuJMChartL){try{_msoSkuJMChartL.destroy();}catch(e){}_msoSkuJMChartL=null;}
    var mx=Math.max.apply(null,sh26.concat(sh25));
    _msoSkuJMChartL=new Chart(lC,{type:'bar',data:{labels:labels,datasets:[
      {label:'Jan-Mar/25',data:sh25,backgroundColor:'rgba(156,163,175,0.18)',borderColor:'rgba(156,163,175,0.4)',borderWidth:1,borderRadius:2},
      {label:'Jan-Mar/26',data:sh26,backgroundColor:bgC,borderColor:bgC,borderWidth:0,borderRadius:3}
    ]},options:{indexAxis:'y',responsive:true,maintainAspectRatio:false,
      plugins:{legend:{display:false},tooltip:{callbacks:{label:function(c){return c.dataset.label+': '+c.parsed.x.toFixed(2)+'%';}}}},
      scales:{x:{min:0,max:Math.ceil(mx)+2,ticks:{color:'#94A3B8',font:{size:9},callback:function(v){return v+'%';}},grid:{color:'rgba(52,211,153,0.05)'}},
              y:{ticks:{color:'#e2e8f0',font:{size:10,weight:'600'}},grid:{display:false}}}}});
  }
  /* Right chart */
  var rC=document.getElementById('mso-sku-jm-bar-r');
  if(rC){
    if(_msoSkuJMChartR){try{_msoSkuJMChartR.destroy();}catch(e){}_msoSkuJMChartR=null;}
    var mv=Math.max.apply(null,vars.map(Math.abs)),lim=Math.ceil(mv*10)/10+0.3;
    _msoSkuJMChartR=new Chart(rC,{type:'bar',data:{labels:labels,datasets:[{label:'Var pp',data:vars,backgroundColor:vC,borderColor:vB,borderWidth:1,borderRadius:3}]},
      options:{indexAxis:'y',responsive:true,maintainAspectRatio:false,
        plugins:{legend:{display:false},tooltip:{callbacks:{label:function(c){var v=c.parsed.x;return 'Var: '+(v>=0?'+':'')+v.toFixed(2)+'pp';}}}},
        scales:{x:{min:-lim,max:lim,ticks:{color:'#94A3B8',font:{size:9},callback:function(v){return(v>=0?'+':'')+v.toFixed(1)+'pp';}},grid:{color:'rgba(52,211,153,0.05)'},border:{color:'rgba(255,255,255,0.15)'}},
                y:{ticks:{color:'#e2e8f0',font:{size:10,weight:'600'}},grid:{display:false}}}},
      plugins:[{id:'msoSkuJMZL',afterDraw:function(ch){var ct=ch.ctx,xa=ch.scales.x,ya=ch.scales.y,x0=xa.getPixelForValue(0);ct.save();ct.strokeStyle='rgba(255,255,255,0.25)';ct.lineWidth=1;ct.beginPath();ct.moveTo(x0,ya.top);ct.lineTo(x0,ya.bottom);ct.stroke();ct.restore();}}]});
  }
  /* Diagnostic */
  var dEl=document.getElementById('mso-sku-jm-diag');
  if(dEl){
    var tI2=d.janmar26.indexOf(Math.max.apply(null,d.janmar26));
    var gD=[],lD=[];
    d.skus.forEach(function(s,i){
      var sc=s.indexOf('OFF!')>=0||s.indexOf('Exposis')>=0||s.indexOf('Xô')>=0||s.indexOf('Xo')>=0;
      if(sc){if(d.var[i]>0)gD.push('<strong style="color:#fbbf24">'+s.trim()+'</strong> <span style="color:#34d399">+'+d.var[i].toFixed(2)+'pp</span>');
             else if(d.var[i]<0)lD.push('<strong style="color:#fbbf24">'+s.trim()+'</strong> <span style="color:#ef4444">'+d.var[i].toFixed(2)+'pp</span>');}
    });
    var top3=d.janmar26.slice().sort(function(a,b){return b-a;}).slice(0,3).reduce(function(s,v){return s+v;},0);
    var dh='🔍 <span style="font-weight:800;color:#34d399;letter-spacing:.4px;">DIAGNÓSTICO SKU JAN-MAR · '+mkt+'</span><br>';
    dh+='🏆 <strong style="color:#e2e8f0;">SKU Líder:</strong> <strong style="color:#34d399;">'+d.skus[tI2]+'</strong> — '+d.janmar26[tI2].toFixed(2)+'% Jan-Mar/26 <span style="color:'+(d.var[tI2]>=0?'#34d399':'#ef4444')+'">'+(d.var[tI2]>=0?'▲ +':'▼ ')+Math.abs(d.var[tI2]).toFixed(2)+'pp</span> vs Jan-Mar/25.<br>';
    dh+='📊 <strong style="color:#e2e8f0;">Top 3 SKUs</strong> representam <strong style="color:#67e8f9;">'+top3.toFixed(1)+'%</strong> do mercado.<br>';
    if(gD.length)dh+='✅ <strong style="color:#34d399;">Ganharam share:</strong> '+gD.join(' · ')+'.<br>';
    if(lD.length)dh+='⚠️ <strong style="color:#ef4444;">Perderam share:</strong> '+lD.join(' · ')+'.';
    dEl.innerHTML='<div style="font-size:11px;color:#D1D5DB;line-height:1.8;">'+dh+'</div>';
  }
}"""

# Inserir após renderMSOSku() (antes de fN)
FN_END_MARKER2 = '\nfunction fN(n){return Number(n).toLocaleString'
assert FN_END_MARKER2 in html, "ERRO: ancora fN nao encontrada"
html = html.replace(FN_END_MARKER2, JM_FN + FN_END_MARKER2, 1)
print("OK: renderMSOSkuJanMar() inserida")

# ══════════════════════════════════════════════════════════════════════════════
# 5. ADICIONAR CALL SITES para renderMSOSkuJanMar()
# ══════════════════════════════════════════════════════════════════════════════
JM_CALL = "if(typeof renderMSOSkuJanMar==='function') renderMSOSkuJanMar();\n"

# Pattern 1: tab-switch (10 spaces)
P1 = "if(typeof renderMSOSku==='function') renderMSOSku();\n          if(typeof renderSkuShrCard"
if P1 in html:
    html = html.replace(P1, "if(typeof renderMSOSku==='function') renderMSOSku();\n          " + JM_CALL + "          if(typeof renderSkuShrCard")
    print("OK: call site tab-switch adicionado")

# Pattern 2: deferred (6 spaces)
P2 = "if(typeof renderMSOSku==='function') renderMSOSku();\n      if(typeof renderSkuShrCard"
cnt2 = html.count(P2)
if cnt2 > 0:
    html = html.replace(P2, "if(typeof renderMSOSku==='function') renderMSOSku();\n      " + JM_CALL + "      if(typeof renderSkuShrCard")
    print(f"OK: call site deferred adicionado ({cnt2}x)")

# Pattern 3: sync try/catch
P3 = "try { if(typeof renderMSOSku==='function'){ renderMSOSku(); } } catch(e){ console.error('renderMSOSku err:',e); }"
if P3 in html:
    html = html.replace(P3, P3 + "\ntry { if(typeof renderMSOSkuJanMar==='function'){ renderMSOSkuJanMar(); } } catch(e){ console.error('renderMSOSkuJanMar err:',e); }", 1)
    print("OK: call site sync try/catch adicionado")

# Pattern 4: setTimeout fallback
P4 = "try { if(typeof renderMSOSku==='function'){ renderMSOSku(); } } catch(e){}"
if P4 in html:
    html = html.replace(P4, P4 + "\n  try { if(typeof renderMSOSkuJanMar==='function'){ renderMSOSkuJanMar(); } } catch(e){}", 1)
    print("OK: call site setTimeout fallback adicionado")

# ══════════════════════════════════════════════════════════════════════════════
# 6. SALVAR
# ══════════════════════════════════════════════════════════════════════════════
DASH.write_text(html, encoding='utf-8')
versao = VER / f"Dashboard_Farma_Sul_{ts}_TwoCardsSku.html"
shutil.copy(DASH, versao)
dl = DL / f"Dashboard_FarmaSul_Giovano_{ts}.html"
shutil.copy(DASH, dl)

print(f"\nVersao:    {versao.name}")
print(f"Downloads: {dl.name}")
print(f"Dashboard: {len(html):,} chars (delta {len(html)-orig:+,})")
print("DONE.")
