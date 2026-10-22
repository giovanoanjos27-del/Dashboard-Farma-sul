"""
patch_mso3_hb_chart.py
Adiciona grafico OFF! + EXPOSIS (HB) entre Total Mercado e Marcas no MSO3.
Layout flex: Total Mkt 22% | HB 22% | Marcas flex:1
"""
import shutil
from datetime import datetime

SRC      = r"C:\Users\valqu\OneDrive\Documentos\Claude\Projects\projeto Dashboard_farma_sul\Dashboard_farma_sul\Dashboard_Farma_Sul_20260512_2220.html"
VERS_DIR = r"C:\Users\valqu\OneDrive\Documentos\Claude\Projects\projeto Dashboard_farma_sul\Dashboard_farma_sul\versoes"
DL_DIR   = r"C:\Users\valqu\Downloads"

ts   = datetime.now().strftime('%Y%m%d_%H%M')
VERS = fr"{VERS_DIR}\Dashboard_Farma_Sul_{ts}_MSO3HbChart.html"
DL   = fr"{DL_DIR}\Dashboard_FarmaSul_Giovano_{ts}.html"

with open(SRC, 'r', encoding='utf-8') as f:
    html = f.read()

ok = []

# ─── 1. HTML: adicionar div mso3-hb-total + ajustar flex ─────────────────────
OLD_HTML = (
    '      <div id="mso3-mkt-total" style="flex:0 0 28%;min-width:0;"></div>\n'
    '      <div style="flex:1;min-width:0;">\n'
    '        <div id="mso3-table"></div>\n'
    '      </div>'
)
NEW_HTML = (
    '      <div id="mso3-mkt-total" style="flex:0 0 22%;min-width:0;"></div>\n'
    '      <div id="mso3-hb-total" style="flex:0 0 22%;min-width:0;"></div>\n'
    '      <div style="flex:1;min-width:0;">\n'
    '        <div id="mso3-table"></div>\n'
    '      </div>'
)
if OLD_HTML in html:
    html = html.replace(OLD_HTML, NEW_HTML, 1)
    ok.append('HTML: mso3-hb-total adicionado')
else:
    ok.append('MISS HTML flex container')

# ─── 2. JS: bloco do grafico HB (OFF! + EXPOSIS) ─────────────────────────────
# Inserir APOS o bloco do Total Mercado e ANTES do Brand Grouped Bar
HB_BLOCK = """
  /* HB: OFF! + EXPOSIS — 2 barras FYTD/25 vs FYTD/26 */
  var hbTotalEl=document.getElementById('mso3-hb-total');
  if(hbTotalEl){
    var hb25=((d25['OFF!']||0)+(d25['EXPOSIS']||0));
    var hb26=((d26['OFF!']||0)+(d26['EXPOSIS']||0));
    hb25=Math.round(hb25*100)/100; hb26=Math.round(hb26*100)/100;
    var hbDp=hb25>0?Math.round((hb26-hb25)/hb25*1000)/10:0;
    var hbDstr=(hbDp>=0?'+':'')+hbDp.toFixed(1)+'%';
    var hbCor=hbDp>=0?'#34d399':'#ef4444';
    function fmtHb(v){return isVal?'R$'+v.toFixed(2)+'MM':(v>=1000?(Math.round(v/1000*10)/10)+'M un':Math.round(v)+'K un');}
    hbTotalEl.innerHTML=
      '<div style="font-size:8px;font-weight:700;letter-spacing:.11em;color:#64748b;text-transform:uppercase;margin-bottom:10px;">OFF! + EXPOSIS (HB) &middot; FYTD JUL&ndash;MAR &middot; '+(isVal?'R$ MM':'Unidades')+'</div>'
      +'<div style="position:relative;height:210px;"><canvas id="mso3-hb-canvas"></canvas></div>';
    var prevHb=Chart.getChart('mso3-hb-canvas'); if(prevHb) prevHb.destroy();
    var cvHb=document.getElementById('mso3-hb-canvas');
    cvHb.removeAttribute('width');cvHb.removeAttribute('height');cvHb.style.width='';cvHb.style.height='';
    new Chart(cvHb,{
      type:'bar',
      data:{labels:['FYTD / 25','FYTD / 26'],datasets:[{data:[hb25,hb26],
        backgroundColor:['rgba(100,116,139,0.45)','rgba(59,130,246,0.55)'],
        borderColor:['rgba(100,116,139,0.75)','#3b82f6'],
        borderWidth:1,borderRadius:5,barPercentage:0.55}]},
      options:{responsive:true,maintainAspectRatio:false,
        layout:{padding:{top:28,right:16,bottom:4,left:16}},
        plugins:{legend:{display:false},
          tooltip:{callbacks:{label:function(ctx){return '  OFF!+EXPOSIS: '+fmtHb(ctx.raw);}}}},
        scales:{
          x:{ticks:{color:'#94A3B8',font:{size:11,weight:'700'}},grid:{display:false},border:{color:'rgba(255,255,255,0.08)'}},
          y:{ticks:{color:'#64748b',font:{size:10},callback:function(v){return fmtHb(v);}},grid:{color:'rgba(255,255,255,0.05)'},border:{color:'rgba(255,255,255,0.08)'}}}},
      plugins:[{id:'mso3hbdelta',afterDatasetsDraw:function(chart){
        var ctx4=chart.ctx,meta=chart.getDatasetMeta(0);
        meta.data.forEach(function(bar,i){
          var val=i===0?hb25:hb26;
          ctx4.save();ctx4.fillStyle='#94A3B8';ctx4.font='700 11px system-ui,sans-serif';
          ctx4.textAlign='center';ctx4.fillText(fmtHb(val),bar.x,bar.y-8);ctx4.restore();
        });
        var bar26=meta.data[1];
        if(bar26){
          var cY=(bar26.y+bar26.base)/2+5;
          ctx4.save();ctx4.shadowColor='rgba(0,0,0,0.7)';ctx4.shadowBlur=4;
          ctx4.fillStyle=hbCor;ctx4.font='900 14px system-ui,sans-serif';
          ctx4.textAlign='center';ctx4.fillText(hbDstr,bar26.x,cY);ctx4.restore();
        }
      }}]
    });
  }

"""

INSERT_BEFORE = '  /* BRAND GROUPED BAR CHART */'
if INSERT_BEFORE in html:
    html = html.replace(INSERT_BEFORE, HB_BLOCK + INSERT_BEFORE, 1)
    ok.append('JS: bloco HB OFF!+EXPOSIS adicionado')
else:
    ok.append('MISS JS insert point')

with open(SRC, 'w', encoding='utf-8') as f:
    f.write(html)
shutil.copy2(SRC, VERS)
shutil.copy2(SRC, DL)

print()
print('=' * 55)
for c in ok: print(f'  {"OK" if not c.startswith("MISS") else "!!"} {c}')
print(f'\n  Versao: {VERS.split(chr(92))[-1]}')
print(f'  DL:     {DL.split(chr(92))[-1]}')
print('=' * 55)
