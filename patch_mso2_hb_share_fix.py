"""
patch_mso2_hb_share_fix.py
Grafico HB OFF!+EXPOSIS no MSO2 agora mostra R$MM em TODOS os modos
(Share, R$MM e Unidades). Antes ficava vazio no modo Share.
Em modo Share usa NIELSEN_BRAND_VAL para obter valores R$MM direto.
"""
import shutil
from datetime import datetime

SRC      = r"C:\Users\valqu\OneDrive\Documentos\Claude\Projects\projeto Dashboard_farma_sul\Dashboard_farma_sul\Dashboard_Farma_Sul_20260512_2220.html"
VERS_DIR = r"C:\Users\valqu\OneDrive\Documentos\Claude\Projects\projeto Dashboard_farma_sul\Dashboard_farma_sul\versoes"
DL_DIR   = r"C:\Users\valqu\Downloads"

ts   = datetime.now().strftime('%Y%m%d_%H%M')
VERS = fr"{VERS_DIR}\Dashboard_Farma_Sul_{ts}_MSO2HbShareFix.html"
DL   = fr"{DL_DIR}\Dashboard_FarmaSul_Giovano_{ts}.html"

with open(SRC, 'r', encoding='utf-8') as f:
    html = f.read()

OLD = (
    "/* HB MSO2: OFF! + EXPOSIS — 2 barras Jan-Mar/25 vs Jan-Mar/26 */\n"
    "  var hbTotalEl2=document.getElementById('mso2-hb-total');\n"
    "  if(hbTotalEl2&&!isShare){\n"
    "    var hb25k=((d25['OFF!']?d25['OFF!'].acum:0)+(d25['EXPOSIS']?d25['EXPOSIS'].acum:0));\n"
    "    var hb26k=((d26['OFF!']?d26['OFF!'].acum:0)+(d26['EXPOSIS']?d26['EXPOSIS'].acum:0));\n"
    "    hb25k=Math.round(hb25k*100)/100; hb26k=Math.round(hb26k*100)/100;\n"
    "    var hbDpk=hb25k>0?Math.round((hb26k-hb25k)/hb25k*1000)/10:0;\n"
    "    var hbDstrk=(hbDpk>=0?'+':'')+hbDpk.toFixed(1)+'%';\n"
    "    var hbCork=hbDpk>=0?'#34d399':'#ef4444';\n"
    "    hbTotalEl2.innerHTML=\n"
    "      '<div style=\"font-size:8px;font-weight:700;letter-spacing:.11em;color:#64748b;text-transform:uppercase;margin-bottom:10px;\">OFF! + EXPOSIS (HB) &middot; JAN&ndash;MAR &middot; '+(isVal?'R$ MM':'Unidades')+'</div>'\n"
    "      +'<div style=\"position:relative;height:210px;\"><canvas id=\"mso2-hb-canvas\"></canvas></div>';\n"
    "    var prevHb2=Chart.getChart('mso2-hb-canvas'); if(prevHb2) prevHb2.destroy();\n"
    "    var cvHb2=document.getElementById('mso2-hb-canvas');\n"
    "    cvHb2.removeAttribute('width');cvHb2.removeAttribute('height');cvHb2.style.width='';cvHb2.style.height='';\n"
    "    new Chart(cvHb2,{\n"
    "      type:'bar',\n"
    "      data:{labels:['Jan-Mar / 25','Jan-Mar / 26'],datasets:[{data:[hb25k,hb26k],\n"
    "        backgroundColor:['rgba(100,116,139,0.45)','rgba(59,130,246,0.55)'],\n"
    "        borderColor:['rgba(100,116,139,0.75)','#3b82f6'],\n"
    "        borderWidth:1,borderRadius:5,barPercentage:0.55}]},\n"
    "      options:{responsive:true,maintainAspectRatio:false,\n"
    "        layout:{padding:{top:28,right:16,bottom:4,left:16}},\n"
    "        plugins:{legend:{display:false},\n"
    "          tooltip:{callbacks:{label:function(ctx){return '  OFF!+EXPOSIS: '+fmtV(ctx.raw);}}}},\n"
    "        scales:{\n"
    "          x:{ticks:{color:'#94A3B8',font:{size:10,weight:'700'}},grid:{display:false},border:{color:'rgba(255,255,255,0.08)'}},\n"
    "          y:{ticks:{color:'#64748b',font:{size:10},callback:function(v){return fmtV(v);}},grid:{color:'rgba(255,255,255,0.05)'},border:{color:'rgba(255,255,255,0.08)'}}}},\n"
    "      plugins:[{id:'mso2hbdelta',afterDatasetsDraw:function(chart){\n"
    "        var ctx5=chart.ctx,meta=chart.getDatasetMeta(0);\n"
    "        meta.data.forEach(function(bar,i){\n"
    "          var val=i===0?hb25k:hb26k;\n"
    "          ctx5.save();ctx5.fillStyle='#94A3B8';ctx5.font='700 10px system-ui,sans-serif';\n"
    "          ctx5.textAlign='center';ctx5.fillText(fmtV(val),bar.x,bar.y-8);ctx5.restore();\n"
    "        });\n"
    "        var bar26k=meta.data[1];\n"
    "        if(bar26k){\n"
    "          var cYk=(bar26k.y+bar26k.base)/2+5;\n"
    "          ctx5.save();ctx5.shadowColor='rgba(0,0,0,0.7)';ctx5.shadowBlur=4;\n"
    "          ctx5.fillStyle=hbCork;ctx5.font='900 13px system-ui,sans-serif';\n"
    "          ctx5.textAlign='center';ctx5.fillText(hbDstrk,bar26k.x,cYk);ctx5.restore();\n"
    "        }\n"
    "      }}]\n"
    "    });\n"
    "  } else if(hbTotalEl2&&isShare){\n"
    "    hbTotalEl2.innerHTML='';\n"
    "  }"
)

NEW = (
    "/* HB MSO2: OFF! + EXPOSIS — sempre R$MM independente do modo */\n"
    "  var hbTotalEl2=document.getElementById('mso2-hb-total');\n"
    "  if(hbTotalEl2){\n"
    "    /* Valores R$MM: em Share busca direto do NIELSEN_BRAND_VAL; em Val usa d25/d26 acum */\n"
    "    var hb25k,hb26k;\n"
    "    function fmtHbVal(v){ return v>=1?'R$'+v.toFixed(2)+'MM':'R$'+(v*1000).toFixed(0)+'K'; }\n"
    "    if(isShare){\n"
    "      var nbvHb=(typeof NIELSEN_BRAND_VAL!=='undefined')?NIELSEN_BRAND_VAL[mkt]:null;\n"
    "      if(nbvHb){\n"
    "        var offHb=nbvHb['OFF!']||{}, expHb=nbvHb['EXPOSIS']||{};\n"
    "        hb26k=Math.round(((offHb.jan_val||0)+(offHb.fev_val||0)+(offHb.mar_val||0)\n"
    "                         +(expHb.jan_val||0)+(expHb.fev_val||0)+(expHb.mar_val||0))*100)/100;\n"
    "        hb25k=Math.round(((offHb.jan25_val||0)+(offHb.fev25_val||0)+(offHb.mar25_val||0)\n"
    "                         +(expHb.jan25_val||0)+(expHb.fev25_val||0)+(expHb.mar25_val||0))*100)/100;\n"
    "      } else { hb25k=0; hb26k=0; }\n"
    "    } else if(isVal){\n"
    "      hb25k=Math.round(((d25['OFF!']?d25['OFF!'].acum:0)+(d25['EXPOSIS']?d25['EXPOSIS'].acum:0))*100)/100;\n"
    "      hb26k=Math.round(((d26['OFF!']?d26['OFF!'].acum:0)+(d26['EXPOSIS']?d26['EXPOSIS'].acum:0))*100)/100;\n"
    "    } else {\n"
    "      /* Unidades: usa d25/d26 acum mas formata como units nao R$ */\n"
    "      hb25k=Math.round(((d25['OFF!']?d25['OFF!'].acum:0)+(d25['EXPOSIS']?d25['EXPOSIS'].acum:0))*100)/100;\n"
    "      hb26k=Math.round(((d26['OFF!']?d26['OFF!'].acum:0)+(d26['EXPOSIS']?d26['EXPOSIS'].acum:0))*100)/100;\n"
    "      fmtHbVal=function(v){ return v>=1000?(Math.round(v/1000*10)/10)+'M un':Math.round(v)+'K un'; };\n"
    "    }\n"
    "    var hbDpk=hb25k>0?Math.round((hb26k-hb25k)/hb25k*1000)/10:0;\n"
    "    var hbDstrk=(hbDpk>=0?'+':'')+hbDpk.toFixed(1)+'%';\n"
    "    var hbCork=hbDpk>=0?'#34d399':'#ef4444';\n"
    "    var hbUnitLbl=(!isShare&&!isVal)?'Unidades':'R$ MM';\n"
    "    hbTotalEl2.innerHTML=\n"
    "      '<div style=\"font-size:8px;font-weight:700;letter-spacing:.11em;color:#64748b;text-transform:uppercase;margin-bottom:10px;\">OFF! + EXPOSIS (HB) &middot; JAN&ndash;MAR &middot; '+hbUnitLbl+'</div>'\n"
    "      +'<div style=\"position:relative;height:210px;\"><canvas id=\"mso2-hb-canvas\"></canvas></div>';\n"
    "    var prevHb2=Chart.getChart('mso2-hb-canvas'); if(prevHb2) prevHb2.destroy();\n"
    "    var cvHb2=document.getElementById('mso2-hb-canvas');\n"
    "    cvHb2.removeAttribute('width');cvHb2.removeAttribute('height');cvHb2.style.width='';cvHb2.style.height='';\n"
    "    new Chart(cvHb2,{\n"
    "      type:'bar',\n"
    "      data:{labels:['Jan-Mar / 25','Jan-Mar / 26'],datasets:[{data:[hb25k,hb26k],\n"
    "        backgroundColor:['rgba(100,116,139,0.45)','rgba(59,130,246,0.55)'],\n"
    "        borderColor:['rgba(100,116,139,0.75)','#3b82f6'],\n"
    "        borderWidth:1,borderRadius:5,barPercentage:0.55}]},\n"
    "      options:{responsive:true,maintainAspectRatio:false,\n"
    "        layout:{padding:{top:28,right:16,bottom:4,left:16}},\n"
    "        plugins:{legend:{display:false},\n"
    "          tooltip:{callbacks:{label:function(ctx){return '  OFF!+EXPOSIS: '+fmtHbVal(ctx.raw);}}}},\n"
    "        scales:{\n"
    "          x:{ticks:{color:'#94A3B8',font:{size:10,weight:'700'}},grid:{display:false},border:{color:'rgba(255,255,255,0.08)'}},\n"
    "          y:{ticks:{color:'#64748b',font:{size:10},callback:function(v){return fmtHbVal(v);}},grid:{color:'rgba(255,255,255,0.05)'},border:{color:'rgba(255,255,255,0.08)'}}}},\n"
    "      plugins:[{id:'mso2hbdelta',afterDatasetsDraw:function(chart){\n"
    "        var ctx5=chart.ctx,meta=chart.getDatasetMeta(0);\n"
    "        meta.data.forEach(function(bar,i){\n"
    "          var val=i===0?hb25k:hb26k;\n"
    "          ctx5.save();ctx5.fillStyle='#94A3B8';ctx5.font='700 10px system-ui,sans-serif';\n"
    "          ctx5.textAlign='center';ctx5.fillText(fmtHbVal(val),bar.x,bar.y-8);ctx5.restore();\n"
    "        });\n"
    "        var bar26k=meta.data[1];\n"
    "        if(bar26k){\n"
    "          var cYk=(bar26k.y+bar26k.base)/2+5;\n"
    "          ctx5.save();ctx5.shadowColor='rgba(0,0,0,0.7)';ctx5.shadowBlur=4;\n"
    "          ctx5.fillStyle=hbCork;ctx5.font='900 13px system-ui,sans-serif';\n"
    "          ctx5.textAlign='center';ctx5.fillText(hbDstrk,bar26k.x,cYk);ctx5.restore();\n"
    "        }\n"
    "      }}]\n"
    "    });\n"
    "  }"
)

if OLD in html:
    html = html.replace(OLD, NEW, 1)
    print('OK  HB MSO2: sempre visivel (R$MM em Share mode)')
else:
    print('MISS  bloco HB MSO2 nao encontrado')

with open(SRC, 'w', encoding='utf-8') as f:
    f.write(html)
shutil.copy2(SRC, VERS)
shutil.copy2(SRC, DL)

print(f'\n  Versao: {VERS.split(chr(92))[-1]}')
print(f'  DL:     {DL.split(chr(92))[-1]}')
