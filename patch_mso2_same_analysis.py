"""
patch_mso2_same_analysis.py
Aplica ao MSO2 (Jan-Mar) a mesma analise do MSO3:
  1. HTML: adicionar div mso2-hb-total + ajustar flex 28% -> 22%
  2. KPI chips val/un: adicionar SCJ COMBINED como 1o chip (5 chips)
  3. JS: grafico HB OFF!+EXPOSIS entre Total Mercado e tabela de marcas
  4. renderMSO2Insight val/un: enriquecer com 3 blocos (Mercado Total,
     SCJ vs Mercado, Por Marca com share%)
"""
import shutil
from datetime import datetime

SRC      = r"C:\Users\valqu\OneDrive\Documentos\Claude\Projects\projeto Dashboard_farma_sul\Dashboard_farma_sul\Dashboard_Farma_Sul_20260512_2220.html"
VERS_DIR = r"C:\Users\valqu\OneDrive\Documentos\Claude\Projects\projeto Dashboard_farma_sul\Dashboard_farma_sul\versoes"
DL_DIR   = r"C:\Users\valqu\Downloads"

ts   = datetime.now().strftime('%Y%m%d_%H%M')
VERS = fr"{VERS_DIR}\Dashboard_Farma_Sul_{ts}_MSO2SameAnalysis.html"
DL   = fr"{DL_DIR}\Dashboard_FarmaSul_Giovano_{ts}.html"

with open(SRC, 'r', encoding='utf-8') as f:
    html = f.read()

ok = []

# ─── 1. HTML: adicionar mso2-hb-total div + ajustar flex ─────────────────────
OLD_HTML = (
    '      <div id="mso2-mkt-total" style="flex:0 0 28%;min-width:0;"></div>\n'
    '      <div style="flex:1;min-width:0;">\n'
    '        <div id="mso2-table-title" style="display:none;"></div>\n'
    '        <div id="mso2-table"></div>'
)
NEW_HTML = (
    '      <div id="mso2-mkt-total" style="flex:0 0 22%;min-width:0;"></div>\n'
    '      <div id="mso2-hb-total" style="flex:0 0 22%;min-width:0;"></div>\n'
    '      <div style="flex:1;min-width:0;">\n'
    '        <div id="mso2-table-title" style="display:none;"></div>\n'
    '        <div id="mso2-table"></div>'
)
if OLD_HTML in html:
    html = html.replace(OLD_HTML, NEW_HTML, 1)
    ok.append('HTML: mso2-hb-total adicionado (flex 28% -> 22%)')
else:
    ok.append('MISS HTML flex container mso2')

# ─── 2. KPI chips val/un: adicionar SCJ COMBINED como 1o chip ────────────────
OLD_KPI = (
    "      hdEl.innerHTML = '<div style=\"display:grid;grid-template-columns:repeat(4,1fr);gap:1px;background:rgba(255,255,255,0.06);\">'\n"
    "        +kpiChip(totDk.up?'#34d399':'#ef4444','TOTAL ACUM',fmtV(totV26k),'color:#f1f5f9',totDk.str+' vs /25','color:'+(totDk.up?'#34d399':'#ef4444'))\n"
    "        +kpiChip(colors[topBk.b]||'#e2e8f0','MAIOR VOLUME',fmtV(topBk.val26),'color:'+(colors[topBk.b]||'#e2e8f0'),topBk.b,'color:#94A3B8')\n"
    "        +kpiChip(topGk.delta.raw>=0?'#34d399':'#f59e0b',topGk.delta.raw>=0?'MAIOR CRESCIM.':'MENOR QUEDA',topGk.delta.str,'color:'+(topGk.delta.raw>=0?'#34d399':'#f59e0b'),topGk.b,'color:#94A3B8')\n"
    "        +kpiChip('#ef4444','MAIOR QUEDA',topLk.delta.str,'color:#ef4444',topLk.b,'color:#94A3B8')\n"
    "        +'</div>';\n"
    "    }\n"
    "  }"
)
NEW_KPI = (
    "      /* SCJ COMBINED share no mercado total (Jan-Mar) */\n"
    "      var fytMktH2=(typeof FYTD_MARKET_TOTAL!=='undefined')?FYTD_MARKET_TOTAL[mkt]:null;\n"
    "      var mktTot26k=fytMktH2?(isVal?fytMktH2.janmar26_val:fytMktH2.janmar26_un):0;\n"
    "      var mktTot25k=fytMktH2?(isVal?fytMktH2.janmar25_val:fytMktH2.janmar25_un):0;\n"
    "      var scjShr2k=mktTot26k>0?Math.round(totV26k/mktTot26k*1000)/10:0;\n"
    "      var scjShr1k=mktTot25k>0?Math.round(totV25k/mktTot25k*1000)/10:0;\n"
    "      var scjShrDtk=Math.round((scjShr2k-scjShr1k)*10)/10;\n"
    "      var scjShrCork=scjShrDtk>=0?'#34d399':'#ef4444';\n"
    "      var scjShrSubk=(scjShrDtk>=0?'+':'')+scjShrDtk.toFixed(1)+'pp vs /25';\n"
    "      hdEl.innerHTML = '<div style=\"display:grid;grid-template-columns:repeat(5,1fr);gap:1px;background:rgba(255,255,255,0.06);\">'\n"
    "        +kpiChip('#fbbf24','SCJ COMBINED',scjShr2k.toFixed(1)+'%','color:#fbbf24',scjShrSubk,'color:'+scjShrCork)\n"
    "        +kpiChip(totDk.up?'#34d399':'#ef4444','TOTAL ACUM',fmtV(totV26k),'color:#f1f5f9',totDk.str+' vs /25','color:'+(totDk.up?'#34d399':'#ef4444'))\n"
    "        +kpiChip(colors[topBk.b]||'#e2e8f0','MAIOR VOLUME',fmtV(topBk.val26),'color:'+(colors[topBk.b]||'#e2e8f0'),topBk.b,'color:#94A3B8')\n"
    "        +kpiChip(topGk.delta.raw>=0?'#34d399':'#f59e0b',topGk.delta.raw>=0?'MAIOR CRESCIM.':'MENOR QUEDA',topGk.delta.str,'color:'+(topGk.delta.raw>=0?'#34d399':'#f59e0b'),topGk.b,'color:#94A3B8')\n"
    "        +kpiChip('#ef4444','MAIOR QUEDA',topLk.delta.str,'color:#ef4444',topLk.b,'color:#94A3B8')\n"
    "        +'</div>';\n"
    "    }\n"
    "  }"
)
if OLD_KPI in html:
    html = html.replace(OLD_KPI, NEW_KPI, 1)
    ok.append('KPI chips: SCJ COMBINED adicionado (5 chips)')
else:
    ok.append('MISS KPI chips val/un mso2')

# ─── 3. JS: bloco grafico HB OFF!+EXPOSIS para MSO2 ─────────────────────────
HB_BLOCK_MSO2 = """
  /* HB MSO2: OFF! + EXPOSIS — 2 barras Jan-Mar/25 vs Jan-Mar/26 */
  var hbTotalEl2=document.getElementById('mso2-hb-total');
  if(hbTotalEl2&&!isShare){
    var hb25k=((d25['OFF!']?d25['OFF!'].acum:0)+(d25['EXPOSIS']?d25['EXPOSIS'].acum:0));
    var hb26k=((d26['OFF!']?d26['OFF!'].acum:0)+(d26['EXPOSIS']?d26['EXPOSIS'].acum:0));
    hb25k=Math.round(hb25k*100)/100; hb26k=Math.round(hb26k*100)/100;
    var hbDpk=hb25k>0?Math.round((hb26k-hb25k)/hb25k*1000)/10:0;
    var hbDstrk=(hbDpk>=0?'+':'')+hbDpk.toFixed(1)+'%';
    var hbCork=hbDpk>=0?'#34d399':'#ef4444';
    hbTotalEl2.innerHTML=
      '<div style="font-size:8px;font-weight:700;letter-spacing:.11em;color:#64748b;text-transform:uppercase;margin-bottom:10px;">OFF! + EXPOSIS (HB) &middot; JAN&ndash;MAR &middot; '+(isVal?'R$ MM':'Unidades')+'</div>'
      +'<div style="position:relative;height:210px;"><canvas id="mso2-hb-canvas"></canvas></div>';
    var prevHb2=Chart.getChart('mso2-hb-canvas'); if(prevHb2) prevHb2.destroy();
    var cvHb2=document.getElementById('mso2-hb-canvas');
    cvHb2.removeAttribute('width');cvHb2.removeAttribute('height');cvHb2.style.width='';cvHb2.style.height='';
    new Chart(cvHb2,{
      type:'bar',
      data:{labels:['Jan-Mar / 25','Jan-Mar / 26'],datasets:[{data:[hb25k,hb26k],
        backgroundColor:['rgba(100,116,139,0.45)','rgba(59,130,246,0.55)'],
        borderColor:['rgba(100,116,139,0.75)','#3b82f6'],
        borderWidth:1,borderRadius:5,barPercentage:0.55}]},
      options:{responsive:true,maintainAspectRatio:false,
        layout:{padding:{top:28,right:16,bottom:4,left:16}},
        plugins:{legend:{display:false},
          tooltip:{callbacks:{label:function(ctx){return '  OFF!+EXPOSIS: '+fmtV(ctx.raw);}}}},
        scales:{
          x:{ticks:{color:'#94A3B8',font:{size:10,weight:'700'}},grid:{display:false},border:{color:'rgba(255,255,255,0.08)'}},
          y:{ticks:{color:'#64748b',font:{size:10},callback:function(v){return fmtV(v);}},grid:{color:'rgba(255,255,255,0.05)'},border:{color:'rgba(255,255,255,0.08)'}}}},
      plugins:[{id:'mso2hbdelta',afterDatasetsDraw:function(chart){
        var ctx5=chart.ctx,meta=chart.getDatasetMeta(0);
        meta.data.forEach(function(bar,i){
          var val=i===0?hb25k:hb26k;
          ctx5.save();ctx5.fillStyle='#94A3B8';ctx5.font='700 10px system-ui,sans-serif';
          ctx5.textAlign='center';ctx5.fillText(fmtV(val),bar.x,bar.y-8);ctx5.restore();
        });
        var bar26k=meta.data[1];
        if(bar26k){
          var cYk=(bar26k.y+bar26k.base)/2+5;
          ctx5.save();ctx5.shadowColor='rgba(0,0,0,0.7)';ctx5.shadowBlur=4;
          ctx5.fillStyle=hbCork;ctx5.font='900 13px system-ui,sans-serif';
          ctx5.textAlign='center';ctx5.fillText(hbDstrk,bar26k.x,cYk);ctx5.restore();
        }
      }}]
    });
  } else if(hbTotalEl2&&isShare){
    hbTotalEl2.innerHTML='';
  }

"""

INSERT_BEFORE_MSO2 = '  /* TABLE / LINE CHART */'
if INSERT_BEFORE_MSO2 in html:
    html = html.replace(INSERT_BEFORE_MSO2, HB_BLOCK_MSO2 + INSERT_BEFORE_MSO2, 1)
    ok.append('JS: bloco HB OFF!+EXPOSIS MSO2 adicionado')
else:
    ok.append('MISS JS insert point TABLE/LINE CHART mso2')

# ─── 4. renderMSO2Insight val/un: enriquecer com 3 blocos ────────────────────
OLD_INSIGHT = (
    "  /* R$ MM / UNIDADES MODE */\n"
    "  var nbvI = (typeof NIELSEN_BRAND_VAL !== 'undefined') ? NIELSEN_BRAND_VAL[mkt] : null;\n"
    "  if(!nbvI) return;\n"
    "  var isValI = mso2Mode === 'val';\n"
    "  function fmtNI(v){ if(isValI) return v>=1?'R$'+v.toFixed(2)+'MM':'R$'+(v*1000).toFixed(0)+'K'; return Math.round(v).toLocaleString('pt-BR')+'K'; }\n"
    "  function pctI(v26,v25){ return v25>0?Math.round((v26-v25)/v25*1000)/10:0; }\n"
    "  var lines2 = MSO_BRANDS.map(function(b){\n"
    "    var bd=nbvI[b]; if(!bd) return null;\n"
    "    var cor=MSO_COLORS[b]||'#e2e8f0';\n"
    "    var f25=isValI?bd.fytd25_val:bd.fytd25_un, f26=isValI?bd.fytd26_val:bd.fytd26_un;\n"
    "    var j26=isValI?bd.jan_val:bd.jan_un, fv26=isValI?bd.fev_val:bd.fev_un, m26=isValI?bd.mar_val:bd.mar_un;\n"
    "    var p=pctI(f26,f25);\n"
    "    var cc=p>=0?'#34d399':'#ef4444';\n"
    "    var trend=p>2?'↗ ':(p<-2?'↘ ':'→ ');\n"
    "    return '<span style=\"color:'+cc+';font-weight:700;font-size:10px;\">'+trend+'</span>'\n"
    "      +'<strong style=\"color:'+cor+';\">'+b+'</strong>'\n"
    "      +' Jan: <strong style=\"color:'+cor+';\">'+fmtNI(j26)+'</strong>'\n"
    "      +' \xb7 Fev: <strong style=\"color:'+cor+';\">'+fmtNI(fv26)+'</strong>'\n"
    "      +' \xb7 Mar: <strong style=\"color:'+cor+';\">'+fmtNI(m26)+'</strong>'\n"
    "      +' <span style=\"color:'+cc+';font-weight:700;\">'+(p>=0?'▲ +':'▼ ')+Math.abs(p).toFixed(1)+'%</span>';\n"
    "  }).filter(Boolean);\n"
    "  el.innerHTML='<div style=\"background:#161B22;border-radius:10px;border-left:3px solid rgba(251,191,36,0.6);padding:14px 16px;\">'\n"
    "    +'<div style=\"font-size:9px;font-weight:700;letter-spacing:.14em;color:#fbbf24;text-transform:uppercase;margin-bottom:9px;\">\U0001f4ca DIAGN\xd3STICO \xb7 '+mkt+' \xb7 '+(isValI?'R$ MM':'Unidades')+' Jan–Mar/26</div>'\n"
    "    +'<div style=\"font-size:11px;color:#D1D5DB;line-height:1.9;\">'\n"
    "    +lines2.join('<br>')\n"
    "    +'</div></div>';\n"
    "}"
)
NEW_INSIGHT = (
    "  /* R$ MM / UNIDADES MODE — DIAGNOSTICO ENRIQUECIDO */\n"
    "  var nbvI = (typeof NIELSEN_BRAND_VAL !== 'undefined') ? NIELSEN_BRAND_VAL[mkt] : null;\n"
    "  if(!nbvI) return;\n"
    "  var isValI = mso2Mode === 'val';\n"
    "  function fmtNI(v){ if(isValI) return v>=1?'R$'+v.toFixed(2)+'MM':'R$'+(v*1000).toFixed(0)+'K'; return Math.round(v).toLocaleString('pt-BR')+'K'; }\n"
    "  function pctI(v26,v25){ return v25>0?Math.round((v26-v25)/v25*1000)/10:0; }\n"
    "  /* Mercado total Jan-Mar */\n"
    "  var fytMktI=(typeof FYTD_MARKET_TOTAL!=='undefined')?FYTD_MARKET_TOTAL[mkt]:null;\n"
    "  var mtI26=fytMktI?(isValI?fytMktI.janmar26_val:fytMktI.janmar26_un):0;\n"
    "  var mtI25=fytMktI?(isValI?fytMktI.janmar25_val:fytMktI.janmar25_un):0;\n"
    "  mtI26=Math.round(mtI26*100)/100; mtI25=Math.round(mtI25*100)/100;\n"
    "  var mtIDelta=mtI25>0?Math.round((mtI26-mtI25)/mtI25*1000)/10:0;\n"
    "  var mtICor=mtIDelta>=0?'#34d399':'#ef4444';\n"
    "  /* SCJ total Jan-Mar (soma das marcas) */\n"
    "  var scjI26=0, scjI25=0;\n"
    "  MSO_BRANDS.forEach(function(b){\n"
    "    var bd=nbvI[b]; if(!bd) return;\n"
    "    var j26=isValI?(bd.jan_val||0):(bd.jan_un||0);\n"
    "    var f26=isValI?(bd.fev_val||0):(bd.fev_un||0);\n"
    "    var m26=isValI?(bd.mar_val||0):(bd.mar_un||0);\n"
    "    scjI26 += j26+f26+m26;\n"
    "    var hasEx=isValI?(bd.jan25_val!==undefined):(bd.jan25_un!==undefined);\n"
    "    if(hasEx){\n"
    "      scjI25 += (isValI?(bd.jan25_val||0):(bd.jan25_un||0))\n"
    "               +(isValI?(bd.fev25_val||0):(bd.fev25_un||0))\n"
    "               +(isValI?(bd.mar25_val||0):(bd.mar25_un||0));\n"
    "    } else {\n"
    "      var fyt25=isValI?bd.fytd25_val:bd.fytd25_un, fyt26=isValI?bd.fytd26_val:bd.fytd26_un;\n"
    "      var ratio=fyt26>0?(j26+f26+m26)/fyt26:1/3;\n"
    "      scjI25 += fyt25*ratio;\n"
    "    }\n"
    "  });\n"
    "  scjI26=Math.round(scjI26*100)/100; scjI25=Math.round(scjI25*100)/100;\n"
    "  var scjIDelta=scjI25>0?Math.round((scjI26-scjI25)/scjI25*1000)/10:0;\n"
    "  var scjICor=scjIDelta>=0?'#34d399':'#ef4444';\n"
    "  /* Share SCJ no mercado */\n"
    "  var shrI26=mtI26>0?Math.round(scjI26/mtI26*1000)/10:0;\n"
    "  var shrI25=mtI25>0?Math.round(scjI25/mtI25*1000)/10:0;\n"
    "  var shrIDelta=Math.round((shrI26-shrI25)*10)/10;\n"
    "  var shrICor=shrIDelta>=0?'#34d399':'#ef4444';\n"
    "  var vsMarketI=Math.round((scjIDelta-mtIDelta)*10)/10;\n"
    "  var vsCorkI=vsMarketI>=0?'#34d399':'#ef4444';\n"
    "  var vsLabelI=vsMarketI>0.5?'SCJ superou o mercado':vsMarketI<-0.5?'SCJ ficou abaixo do mercado':'SCJ acompanhou o mercado';\n"
    "  /* Por marca */\n"
    "  var lines2 = MSO_BRANDS.map(function(b){\n"
    "    var bd=nbvI[b]; if(!bd) return null;\n"
    "    var cor=MSO_COLORS[b]||'#e2e8f0';\n"
    "    var j26=isValI?(bd.jan_val||0):(bd.jan_un||0);\n"
    "    var fv26=isValI?(bd.fev_val||0):(bd.fev_un||0);\n"
    "    var m26=isValI?(bd.mar_val||0):(bd.mar_un||0);\n"
    "    var v26b=Math.round((j26+fv26+m26)*100)/100;\n"
    "    var fyt25=isValI?bd.fytd25_val:bd.fytd25_un, fyt26=isValI?bd.fytd26_val:bd.fytd26_un;\n"
    "    var hasEx=isValI?(bd.jan25_val!==undefined):(bd.jan25_un!==undefined);\n"
    "    var v25b;\n"
    "    if(hasEx){\n"
    "      v25b=Math.round(((isValI?(bd.jan25_val||0):(bd.jan25_un||0))\n"
    "                      +(isValI?(bd.fev25_val||0):(bd.fev25_un||0))\n"
    "                      +(isValI?(bd.mar25_val||0):(bd.mar25_un||0)))*100)/100;\n"
    "    } else {\n"
    "      var ratio2=fyt26>0?v26b/fyt26:1/3;\n"
    "      v25b=Math.round(fyt25*ratio2*100)/100;\n"
    "    }\n"
    "    var pct=pctI(v26b,v25b);\n"
    "    var cc=pct>=0?'#34d399':'#ef4444';\n"
    "    var trend=pct>2?'↗':(pct<-2?'↘':'→');\n"
    "    var shrB=mtI26>0?Math.round(v26b/mtI26*1000)/10:0;\n"
    "    return '<div style=\"display:flex;align-items:center;gap:5px;padding:3px 0;border-bottom:0.5px solid rgba(255,255,255,0.04);\">'\n"
    "      +'<span style=\"width:5px;height:5px;border-radius:50%;background:'+cor+';flex-shrink:0;\"></span>'\n"
    "      +'<span style=\"color:'+cor+';font-weight:700;min-width:95px;font-size:11px;\">'+b+'</span>'\n"
    "      +'<span style=\"color:#e2e8f0;font-size:11px;\">Jan-Mar/26: <strong>'+fmtNI(v26b)+'</strong></span>'\n"
    "      +'<span style=\"color:#475569;margin:0 3px;\">\xb7</span>'\n"
    "      +'<span style=\"color:#64748b;font-size:11px;\">Jan-Mar/25: '+fmtNI(v25b)+'</span>'\n"
    "      +'<span style=\"color:'+cc+';font-weight:700;font-size:11px;margin-left:5px;\">'\n"
    "        +'<span style=\"font-size:10px;\">'+trend+'</span> '+(pct>=0?'+':'')+pct.toFixed(1)+'%'\n"
    "      +'</span>'\n"
    "      +'<span style=\"color:#334155;font-size:10px;margin-left:auto;background:rgba(255,255,255,0.04);padding:1px 5px;border-radius:3px;\">shr '+shrB.toFixed(1)+'%</span>'\n"
    "      +'</div>';\n"
    "  }).filter(Boolean);\n"
    "  el.innerHTML=\n"
    "    '<div style=\"background:#161B22;border-radius:10px;border-left:3px solid rgba(251,191,36,0.6);padding:14px 16px;\">'\n"
    "    +'<div style=\"font-size:9px;font-weight:700;letter-spacing:.14em;color:#fbbf24;text-transform:uppercase;margin-bottom:12px;\">\U0001f4ca DIAGN\xd3STICO \xb7 '+mkt+' \xb7 '+(isValI?'R$ MM':'Unidades')+' JAN–MAR/26</div>'\n"
    "    /* Bloco 1: Mercado Total */\n"
    "    +'<div style=\"margin-bottom:10px;padding-bottom:9px;border-bottom:0.5px solid rgba(255,255,255,0.06);\">'\n"
    "      +'<div style=\"font-size:9px;font-weight:700;letter-spacing:.1em;color:#475569;text-transform:uppercase;margin-bottom:5px;\">\U0001f30e Mercado Total (todas as marcas)</div>'\n"
    "      +'<div style=\"display:flex;align-items:center;gap:8px;flex-wrap:wrap;\">'\n"
    "        +'<span style=\"font-size:11px;color:#94a3b8;\">Jan-Mar/25: <strong style=\"color:#e2e8f0;\">'+fmtNI(mtI25)+'</strong></span>'\n"
    "        +'<span style=\"color:#334155;\">→</span>'\n"
    "        +'<span style=\"font-size:11px;color:#94a3b8;\">Jan-Mar/26: <strong style=\"color:#e2e8f0;\">'+fmtNI(mtI26)+'</strong></span>'\n"
    "        +'<span style=\"background:'+mtICor+'1a;color:'+mtICor+';font-weight:700;font-size:11px;padding:2px 8px;border-radius:4px;border:0.5px solid '+mtICor+'44;\">'\n"
    "          +(mtIDelta>=0?'▲ +':'▼ ')+Math.abs(mtIDelta).toFixed(1)+'%'\n"
    "        +'</span>'\n"
    "      +'</div>'\n"
    "    +'</div>'\n"
    "    /* Bloco 2: SCJ vs Mercado */\n"
    "    +'<div style=\"margin-bottom:10px;padding-bottom:9px;border-bottom:0.5px solid rgba(255,255,255,0.06);\">'\n"
    "      +'<div style=\"font-size:9px;font-weight:700;letter-spacing:.1em;color:#475569;text-transform:uppercase;margin-bottom:5px;\">\U0001f381 SCJ Portfolio vs Mercado</div>'\n"
    "      +'<div style=\"display:flex;align-items:center;gap:8px;flex-wrap:wrap;margin-bottom:6px;\">'\n"
    "        +'<span style=\"font-size:11px;color:#94a3b8;\">SCJ Jan-Mar/25: <strong style=\"color:#fbbf24;\">'+fmtNI(scjI25)+'</strong></span>'\n"
    "        +'<span style=\"color:#334155;\">→</span>'\n"
    "        +'<span style=\"font-size:11px;color:#94a3b8;\">Jan-Mar/26: <strong style=\"color:#fbbf24;\">'+fmtNI(scjI26)+'</strong></span>'\n"
    "        +'<span style=\"background:'+scjICor+'1a;color:'+scjICor+';font-weight:700;font-size:11px;padding:2px 8px;border-radius:4px;border:0.5px solid '+scjICor+'44;\">'\n"
    "          +(scjIDelta>=0?'▲ +':'▼ ')+Math.abs(scjIDelta).toFixed(1)+'%'\n"
    "        +'</span>'\n"
    "      +'</div>'\n"
    "      +'<div style=\"display:flex;gap:14px;align-items:center;flex-wrap:wrap;margin-bottom:5px;\">'\n"
    "        +'<span style=\"font-size:11px;color:#64748b;\">Share Jan-Mar/25: <strong style=\"color:#cbd5e1;\">'+shrI25.toFixed(1)+'%</strong></span>'\n"
    "        +'<span style=\"color:#1e293b;\">|</span>'\n"
    "        +'<span style=\"font-size:11px;color:#64748b;\">Share Jan-Mar/26: <strong style=\"color:#fbbf24;\">'+shrI26.toFixed(1)+'%</strong></span>'\n"
    "        +'<span style=\"color:'+shrICor+';font-weight:700;font-size:11px;\">'\n"
    "          +(shrIDelta>=0?'▲ +':'▼ ')+Math.abs(shrIDelta).toFixed(1)+'pp'\n"
    "        +'</span>'\n"
    "      +'</div>'\n"
    "      +'<div style=\"font-size:10px;color:'+vsCorkI+';padding:4px 8px;background:'+vsCorkI+'0d;border-radius:5px;display:inline-block;\">'\n"
    "        +'\U0001f50d '+vsLabelI+' — SCJ '+(scjIDelta>=0?'+':'')+scjIDelta.toFixed(1)+'% vs Mercado '+(mtIDelta>=0?'+':'')+mtIDelta.toFixed(1)+'%'\n"
    "        +(vsMarketI!==0?' &nbsp;(Δ '+(vsMarketI>=0?'+':'')+vsMarketI.toFixed(1)+'pp)':'')\n"
    "      +'</div>'\n"
    "    +'</div>'\n"
    "    /* Bloco 3: Por Marca */\n"
    "    +'<div>'\n"
    "      +'<div style=\"font-size:9px;font-weight:700;letter-spacing:.1em;color:#475569;text-transform:uppercase;margin-bottom:6px;\">\U0001f4c8 Por Marca \xb7 participacao no mercado total</div>'\n"
    "      +'<div style=\"font-size:11px;color:#D1D5DB;\">'+lines2.join('')+'</div>'\n"
    "    +'</div>'\n"
    "    +'</div>';\n"
    "}"
)

if OLD_INSIGHT in html:
    html = html.replace(OLD_INSIGHT, NEW_INSIGHT, 1)
    ok.append('renderMSO2Insight: diagnostico enriquecido (3 blocos)')
else:
    ok.append('MISS renderMSO2Insight val/un block')

with open(SRC, 'w', encoding='utf-8') as f:
    f.write(html)
shutil.copy2(SRC, VERS)
shutil.copy2(SRC, DL)

print()
print('=' * 60)
for c in ok: print(f'  {"OK" if not c.startswith("MISS") else "!!"} {c}')
print(f'\n  Versao: {VERS.split(chr(92))[-1]}')
print(f'  DL:     {DL.split(chr(92))[-1]}')
print('=' * 60)
