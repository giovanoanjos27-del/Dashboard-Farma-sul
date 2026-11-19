"""
patch_ob_pato_total.py
Adiciona chip + linha tracejada "Pato Block Total" (soma das 3 variantes)
no card Market Share Odor Block:
  - 1o chip do grid (posicao de destaque, cor amarela #fbbf24)
  - Linha tracejada no grafico (destacada sobre as 3 variantes)
  - Diagnóstico mostra share total no periodo
Grid ja e repeat(6,1fr) — o 6o slot estava vazio.
"""
import shutil
from datetime import datetime

SRC      = r"C:\Users\valqu\OneDrive\Documentos\Claude\Projects\projeto Dashboard_farma_sul\Dashboard_farma_sul\Dashboard_Farma_Sul_20260512_2220.html"
VERS_DIR = r"C:\Users\valqu\OneDrive\Documentos\Claude\Projects\projeto Dashboard_farma_sul\Dashboard_farma_sul\versoes"
DL_DIR   = r"C:\Users\valqu\Downloads"

ts   = datetime.now().strftime('%Y%m%d_%H%M')
VERS = fr"{VERS_DIR}\Dashboard_Farma_Sul_{ts}_OBPatoTotal.html"
DL   = fr"{DL_DIR}\Dashboard_FarmaSul_Giovano_{ts}.html"

with open(SRC, 'r', encoding='utf-8') as f:
    html = f.read()

ok = []

# ── Substituir o inicio de renderOBShare para incluir Pato Total ──────────────
OLD = (
    "function renderOBShare(){\n"
    "  var d = OB_DATA[obMarket1]; if(!d) return;\n"
    "  var prods = ['Pato Block Algodão','Pato Block Lavanda','Pato Block Eucalipto','Freeco','All Others'];\n"
    "  var latest = OB_PERIODS.length-1;\n"
    "\n"
    "  /* KPIs */\n"
    "  var kpiEl = document.getElementById('ob-share-kpis'); if(!kpiEl) return;\n"
    "  kpiEl.innerHTML = prods.map(function(p){\n"
    "    var dd = d[p]; if(!dd) return '';\n"
    "    var cur = dd.share[latest], prev = dd.share[latest-1];\n"
    "    var delta = (cur!=null&&prev!=null) ? (cur-prev).toFixed(2) : null;\n"
    "    var cor = OB_COLORS[p]||'#D1D5DB';\n"
    "    return '<div style=\"background:rgba(0,0,0,0.2"
)

NEW = (
    "function renderOBShare(){\n"
    "  var d = OB_DATA[obMarket1]; if(!d) return;\n"
    "  var prods = ['Pato Block Algodão','Pato Block Lavanda','Pato Block Eucalipto','Freeco','All Others'];\n"
    "  var patoVariants = ['Pato Block Algodão','Pato Block Lavanda','Pato Block Eucalipto'];\n"
    "  var latest = OB_PERIODS.length-1;\n"
    "\n"
    "  /* Calcular Pato Block Total (soma das 3 variantes) por periodo */\n"
    "  var patoTotalSeries = OB_PERIODS.map(function(_,i){\n"
    "    var s = patoVariants.reduce(function(acc,p){\n"
    "      var dd=d[p]; return acc+(dd&&dd.share[i]!=null?dd.share[i]:0);\n"
    "    },0);\n"
    "    return Math.round(s*100)/100;\n"
    "  });\n"
    "  var patoTotCur  = patoTotalSeries[latest];\n"
    "  var patoTotPrev = patoTotalSeries[latest-1];\n"
    "  var patoTotDelta = patoTotCur-patoTotPrev;\n"
    "  var patoTotCor  = '#fbbf24';\n"
    "\n"
    "  /* KPIs — Pato Total primeiro, depois os 5 originais */\n"
    "  var kpiEl = document.getElementById('ob-share-kpis'); if(!kpiEl) return;\n"
    "  var patoTotChip =\n"
    "    '<div style=\"background:rgba(251,191,36,0.08);border-radius:8px;padding:10px 12px;border-top:2px solid #fbbf24;border:1px solid rgba(251,191,36,0.3);\">'\n"
    "    +'<div style=\"font-size:9px;font-weight:700;letter-spacing:0.08em;color:#fbbf24;margin-bottom:3px;\">PATO TOTAL</div>'\n"
    "    +'<div style=\"font-size:18px;font-weight:800;color:#fbbf24;line-height:1;\">'+patoTotCur.toFixed(1)+'%</div>'\n"
    "    +'<div style=\"font-size:9px;color:#94A3B8;margin-top:2px;\">'+(patoTotDelta>=0?'▲+':'▼')+Math.abs(patoTotDelta).toFixed(2)+'pp vs mês ant.</div>'\n"
    "    +'</div>';\n"
    "  kpiEl.innerHTML = patoTotChip + prods.map(function(p){\n"
    "    var dd = d[p]; if(!dd) return '';\n"
    "    var cur = dd.share[latest], prev = dd.share[latest-1];\n"
    "    var delta = (cur!=null&&prev!=null) ? (cur-prev).toFixed(2) : null;\n"
    "    var cor = OB_COLORS[p]||'#D1D5DB';\n"
    "    return '<div style=\"background:rgba(0,0,0,0.2"
)

if OLD in html:
    html = html.replace(OLD, NEW, 1)
    ok.append('KPI chips: Pato Total adicionado como 1o chip')
else:
    ok.append('MISS inicio de renderOBShare')

# ── Adicionar dataset Pato Total no grafico (linha tracejada) ─────────────────
OLD_DATASETS = (
    "  var datasets = prods.map(function(p){\n"
    "    var dd=d[p], cor=OB_COLORS[p]||'#D1D5DB';\n"
    "    return {label:p,data:dd?dd.share:[], borderColor:cor,\n"
    "      backgroundColor:function(ctx){var ca=ctx.chart.chartArea;return makeAreaGradient(ctx.chart.ctx,ca,cor);},\n"
    "      fill:true, tension:0.42, borderWidth:2.5,\n"
    "      pointBackgroundColor:cor, pointBorderColor:'#101828', pointBorderWidth:2,\n"
    "      pointRadius: dd&&dd.share?dd.share.map(function(v,i){\n"
    "        if(v==null) return 0;\n"
    "        var valid=dd.share.filter(function(x){return x!=null;});\n"
    "        var peak=Math.max.apply(null,valid);\n"
    "        return v===peak?8:4;\n"
    "      }):4,\n"
    "      pointHoverRadius:8};\n"
    "  });\n"
    "  obShareChart = new Chart(ctx,"
)

NEW_DATASETS = (
    "  var datasets = prods.map(function(p){\n"
    "    var dd=d[p], cor=OB_COLORS[p]||'#D1D5DB';\n"
    "    return {label:p,data:dd?dd.share:[], borderColor:cor,\n"
    "      backgroundColor:function(ctx){var ca=ctx.chart.chartArea;return makeAreaGradient(ctx.chart.ctx,ca,cor);},\n"
    "      fill:true, tension:0.42, borderWidth:2.5,\n"
    "      pointBackgroundColor:cor, pointBorderColor:'#101828', pointBorderWidth:2,\n"
    "      pointRadius: dd&&dd.share?dd.share.map(function(v,i){\n"
    "        if(v==null) return 0;\n"
    "        var valid=dd.share.filter(function(x){return x!=null;});\n"
    "        var peak=Math.max.apply(null,valid);\n"
    "        return v===peak?8:4;\n"
    "      }):4,\n"
    "      pointHoverRadius:8};\n"
    "  });\n"
    "  /* Adicionar Pato Block Total como linha tracejada no topo */\n"
    "  datasets.unshift({\n"
    "    label:'Pato Block Total',\n"
    "    data:patoTotalSeries,\n"
    "    borderColor:'#fbbf24',\n"
    "    backgroundColor:'rgba(251,191,36,0.0)',\n"
    "    fill:false,\n"
    "    tension:0.42,\n"
    "    borderWidth:2,\n"
    "    borderDash:[6,4],\n"
    "    pointBackgroundColor:'#fbbf24',\n"
    "    pointBorderColor:'#101828',\n"
    "    pointBorderWidth:2,\n"
    "    pointRadius:patoTotalSeries.map(function(v,i){\n"
    "      var peak=Math.max.apply(null,patoTotalSeries);\n"
    "      return v===peak?8:4;\n"
    "    }),\n"
    "    pointHoverRadius:8,\n"
    "    order:0\n"
    "  });\n"
    "  obShareChart = new Chart(ctx,"
)

if OLD_DATASETS in html:
    html = html.replace(OLD_DATASETS, NEW_DATASETS, 1)
    ok.append('Grafico: linha tracejada Pato Block Total adicionada')
else:
    ok.append('MISS datasets block em renderOBShare')

with open(SRC, 'w', encoding='utf-8') as f:
    f.write(html)
shutil.copy2(SRC, VERS)
shutil.copy2(SRC, DL)

print()
print('=' * 58)
for c in ok: print(f'  {"OK" if not c.startswith("MISS") else "!!"} {c}')
print(f'\n  Versao: {VERS.split(chr(92))[-1]}')
print(f'  DL:     {DL.split(chr(92))[-1]}')
print('=' * 58)
