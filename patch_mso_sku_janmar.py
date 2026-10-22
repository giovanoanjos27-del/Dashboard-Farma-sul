"""
patch_mso_sku_janmar.py
Muda o card MSO-SKU de FYTD para Jan-Mar/25 vs Jan-Mar/26:
1. Extrai shares por SKU de Jan/Fev/Mar 2025 e 2026 do Excel
2. Injeta const SKU_MKT_MONTHLY no dashboard
3. Substitui renderMSOSku() para usar SKU_MKT_MONTHLY + labels Jan-Mar
4. Atualiza textos HTML do card
"""
import sys, shutil, json, re
sys.stdout.reconfigure(encoding='utf-8')
import pandas as pd
import numpy as np
from datetime import datetime
from pathlib import Path

BASE  = Path(r"C:\Users\valqu\OneDrive\Documentos\Claude\Projects\projeto Dashboard_farma_sul\Dashboard_farma_sul")
DASH  = BASE / "Dashboard_Farma_Sul_20260512_2220.html"
XLS   = BASE / r"_Recursos\Giovano SCJ\Base Giovano 26-04.xlsx"
VER   = BASE / "versoes"
DL    = Path.home() / "Downloads"

ts = datetime.now().strftime('%Y%m%d_%H%M')
shutil.copy(DASH, VER / f"Dashboard_Farma_Sul_{ts}_PreJanMarSku.html")
print(f"Backup: Dashboard_Farma_Sul_{ts}_PreJanMarSku.html")

# ──────────────────────────────────────────────────────────────────────────────
# 1. LER EXCEL — 1-Tabela-1
# ──────────────────────────────────────────────────────────────────────────────
print("\n1. Lendo Excel...")
df = pd.read_excel(XLS, sheet_name='1-Tabela-1', header=8)
df.columns = ['markets','CATEGORY','BRAND','Products','Data','val','WDR','price','shr','TDP','unid','ROS']

def norm_date(v):
    if pd.isna(v): return ''
    s = str(v).strip()
    if 'FYTD' in s.upper(): return s.upper()
    try:
        dt = pd.to_datetime(v)
        return dt.strftime('%Y-%m-%d')
    except:
        return s

df['ds'] = df['Data'].apply(norm_date)

PERIODS = {
    'jan25': '2025-01-23',
    'fev25': '2025-02-20',
    'mar25': '2025-03-23',
    'jan26': '2026-01-23',
    'fev26': '2026-02-20',
    'mar26': '2026-03-23',
}
ALL_DATES = list(PERIODS.values())

# Filtrar apenas periodos de interesse
df_filt = df[df['ds'].isin(ALL_DATES) & df['val'].notna() & (df['val'] > 0)].copy()

# Linhas de CATEGORIA (market total): BRAND NaN e Products NaN
cat_rows = df_filt[df_filt['BRAND'].isna() & df_filt['Products'].isna()].copy()

# Linhas de SKU: Products nao NaN (BRAND NaN)
sku_rows = df_filt[df_filt['Products'].notna() & df_filt['BRAND'].isna()].copy()
# Deduplicar: cada SKU aparece 3x no export
sku_rows = sku_rows.drop_duplicates(['markets', 'Products', 'ds'])

print(f"   SKU rows (dedup): {len(sku_rows)}")
print(f"   Category rows: {len(cat_rows)}")

# ──────────────────────────────────────────────────────────────────────────────
# 2. CONSTRUIR MARKET TOTALS (val por mercado+periodo)
# ──────────────────────────────────────────────────────────────────────────────
# Para cada mercado, obter val da linha de categoria por periodo
# Deduplicar tambem
cat_rows = cat_rows.drop_duplicates(['markets', 'ds'])
mkt_totals = {}  # mkt_totals[market][period_key] = val
for _, row in cat_rows.iterrows():
    mkt = str(row['markets']).strip()
    for p_key, p_date in PERIODS.items():
        if row['ds'] == p_date:
            if mkt not in mkt_totals:
                mkt_totals[mkt] = {}
            mkt_totals[mkt][p_key] = float(row['val'])

print(f"   Mercados com totais de categoria: {len(mkt_totals)}")

# ──────────────────────────────────────────────────────────────────────────────
# 3. COMPUTAR SHARE JAN-MAR POR SKU POR MERCADO
# ──────────────────────────────────────────────────────────────────────────────
# share_janmar = (val_jan + val_fev + val_mar) / (mkt_jan + mkt_fev + mkt_mar) * 100
# Equivalent to weighted average of monthly shares

print("\n2. Computando shares Jan-Mar por SKU...")

def get_mkt_total(mkt, keys):
    t = 0.0
    if mkt not in mkt_totals:
        return None
    for k in keys:
        v = mkt_totals[mkt].get(k, 0.0)
        t += v
    return t if t > 0 else None

sku_data = {}  # sku_data[market] = {skus:[], janmar25:[], janmar26:[], var:[]}

all_markets = sku_rows['markets'].dropna().unique()

for mkt in all_markets:
    mkt_str = str(mkt).strip()
    sub = sku_rows[sku_rows['markets'] == mkt].copy()
    if sub.empty:
        continue

    # Market totals
    tot25 = get_mkt_total(mkt_str, ['jan25', 'fev25', 'mar25'])
    tot26 = get_mkt_total(mkt_str, ['jan26', 'fev26', 'mar26'])
    if not tot25 or not tot26:
        continue

    skus_in_mkt = sub['Products'].str.strip().unique()
    entries = []
    for sku in skus_in_mkt:
        sku_sub = sub[sub['Products'].str.strip() == sku]

        def get_val(period_date):
            row = sku_sub[sku_sub['ds'] == period_date]
            if len(row) > 0 and pd.notna(row.iloc[0]['val']):
                return float(row.iloc[0]['val'])
            return 0.0

        v_jan25 = get_val(PERIODS['jan25'])
        v_fev25 = get_val(PERIODS['fev25'])
        v_mar25 = get_val(PERIODS['mar25'])
        v_jan26 = get_val(PERIODS['jan26'])
        v_fev26 = get_val(PERIODS['fev26'])
        v_mar26 = get_val(PERIODS['mar26'])

        shr25 = round((v_jan25 + v_fev25 + v_mar25) / tot25 * 100, 4)
        shr26 = round((v_jan26 + v_fev26 + v_mar26) / tot26 * 100, 4)
        var   = round(shr26 - shr25, 4)

        entries.append({'sku': sku, 'janmar25': shr25, 'janmar26': shr26, 'var': var})

    # Ordenar por janmar26 decrescente, pegar top 10
    entries.sort(key=lambda x: x['janmar26'], reverse=True)
    top = entries[:10]

    if not top:
        continue

    sku_data[mkt_str] = {
        'skus':     [e['sku']      for e in top],
        'janmar25': [e['janmar25'] for e in top],
        'janmar26': [e['janmar26'] for e in top],
        'var':      [e['var']      for e in top],
    }

print(f"   Mercados extraidos: {len(sku_data)}")

# Validacao T.BR Farma
if 'T.BR Farma' in sku_data:
    d = sku_data['T.BR Farma']
    idx = d['skus'].index('OFF! Family') if 'OFF! Family' in d['skus'] else -1
    if idx >= 0:
        print(f"   VALIDACAO OFF! Family T.BR Farma:")
        print(f"     janmar25={d['janmar25'][idx]:.2f}%  janmar26={d['janmar26'][idx]:.2f}%  var={d['var'][idx]:+.2f}pp")
        print(f"     (esperado: ~14.46%, ~15.80%, ~+1.34pp)")

# ──────────────────────────────────────────────────────────────────────────────
# 4. GERAR JS CONST
# ──────────────────────────────────────────────────────────────────────────────
print("\n3. Gerando JS const SKU_MKT_MONTHLY...")

def js_arr_f(arr):
    return '[' + ','.join(str(round(v, 2)) for v in arr) + ']'

def js_arr_s(arr):
    return '[' + ','.join('"' + str(s).replace('"', '\\"') + '"' for s in arr) + ']'

lines = ['var SKU_MKT_MONTHLY = {']
items = list(sku_data.items())
for i, (mkt, d) in enumerate(items):
    comma = '' if i == len(items)-1 else ','
    mkt_esc = mkt.replace('"', '\\"')
    lines.append(f'  "{mkt_esc}": {{"skus":{js_arr_s(d["skus"])},"janmar25":{js_arr_f(d["janmar25"])},"janmar26":{js_arr_f(d["janmar26"])},"var":{js_arr_f(d["var"])}}}{comma}')
lines.append('};')
JS_CONST = '\n'.join(lines)
print(f"   JS const: {len(JS_CONST):,} chars, {len(sku_data)} mercados")

# ──────────────────────────────────────────────────────────────────────────────
# 5. LER DASHBOARD E INJETAR
# ──────────────────────────────────────────────────────────────────────────────
print("\n4. Lendo dashboard...")
html = DASH.read_text(encoding='utf-8')
orig = len(html)
print(f"   HTML: {orig:,} chars")

# ── 5a. Injetar SKU_MKT_MONTHLY antes de SKU_MKT_DATA ────────────────────────
SKU_ANCHOR = 'SKU_MKT_DATA ='
assert SKU_ANCHOR in html, "ERRO: SKU_MKT_DATA nao encontrado"
# Find the var/const declaration line
idx = html.rfind('\n', 0, html.find(SKU_ANCHOR))
inject_before = html[:idx+1] + JS_CONST + '\n' + html[idx+1:]
html = inject_before
print(f"   OK: SKU_MKT_MONTHLY injetado ({len(JS_CONST):,} chars)")

# ── 5b. Substituir renderMSOSku() ─────────────────────────────────────────────
OLD_FN_START = '\n/* ═══ MARKET SHARE POR SKU — mso-sku-card ═══ */'
NEW_FN_END   = '\nfunction fN(n){return Number(n).toLocaleString'

assert OLD_FN_START in html, "ERRO: inicio da funcao renderMSOSku nao encontrado"
assert NEW_FN_END in html,   "ERRO: ancora FN_END nao encontrada"

idx_s = html.index(OLD_FN_START)
idx_e = html.index(NEW_FN_END, idx_s)
old_fn = html[idx_s:idx_e]

NEW_FN = r"""
/* ═══ MARKET SHARE POR SKU — mso-sku-card (Jan-Mar) ═══ */
var _msoSkuChartL=null,_msoSkuChartR=null;
function initMSOSku(){
  var sel=document.getElementById('msoSkuMktSel');
  if(!sel||sel.options.length>0)return;
  var src=typeof SKU_MKT_MONTHLY!=='undefined'?SKU_MKT_MONTHLY:(typeof SKU_MKT_DATA!=='undefined'?SKU_MKT_DATA:null);
  var mks=src?Object.keys(src):['T.BR Farma'];
  mks.forEach(function(m){var o=document.createElement('option');o.value=m;o.textContent=m;if(m==='T.BR Farma')o.selected=true;sel.appendChild(o);});
}
function renderMSOSku(){
  initMSOSku();
  var sel=document.getElementById('msoSkuMktSel');
  var mkt=sel?sel.value:'T.BR Farma';
  var sub=document.getElementById('mso-sku-sub');
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
  var kEl=document.getElementById('mso-sku-kpis');
  if(kEl){
    var tI=d.janmar26.indexOf(Math.max.apply(null,d.janmar26));
    var gA=d.var.map(function(v,i){return{v:v,i:i};}).filter(function(x){return x.v>0;}).sort(function(a,b){return b.v-a.v;});
    var lA=d.var.map(function(v,i){return{v:v,i:i};}).filter(function(x){return x.v<0;}).sort(function(a,b){return a.v-b.v;});
    var scjT=0;
    d.skus.forEach(function(s,i){if(s.indexOf('OFF!')>=0||s.indexOf('Exposis')>=0||s.indexOf('Xô')>=0||s.indexOf('Xo')>=0)scjT+=d.janmar26[i];});
    var chips=[
      {l:'SKU LÍDER',v:d.skus[tI].trim().substring(0,22),s:d.janmar26[tI].toFixed(2)+'% Jan-Mar/26',c:'#fbbf24'},
      {l:'MAIOR GANHO Δpp',v:gA.length?'+'+gA[0].v.toFixed(2)+'pp':'—',s:gA.length?d.skus[gA[0].i].trim().substring(0,22):'',c:'#34d399'},
      {l:'MAIOR QUEDA Δpp',v:lA.length?lA[0].v.toFixed(2)+'pp':'—',s:lA.length?d.skus[lA[0].i].trim().substring(0,22):'',c:'#ef4444'},
      {l:'SCJ COMBINED',v:scjT.toFixed(2)+'%',s:'Share Jan-Mar/26 combinado',c:'#3b82f6'}
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
      {label:'Jan-Mar/25',data:sh25,backgroundColor:'rgba(156,163,175,0.18)',borderColor:'rgba(156,163,175,0.4)',borderWidth:1,borderRadius:2},
      {label:'Jan-Mar/26',data:sh26,backgroundColor:bgC,borderColor:bgC,borderWidth:0,borderRadius:3}
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
    var tI2=d.janmar26.indexOf(Math.max.apply(null,d.janmar26));
    var gD=[],lD=[];
    d.skus.forEach(function(s,i){
      var sc=s.indexOf('OFF!')>=0||s.indexOf('Exposis')>=0||s.indexOf('Xô')>=0||s.indexOf('Xo')>=0;
      if(sc){if(d.var[i]>0)gD.push('<strong style="color:#fbbf24">'+s.trim()+'</strong> <span style="color:#34d399">+'+d.var[i].toFixed(2)+'pp</span>');
             else if(d.var[i]<0)lD.push('<strong style="color:#fbbf24">'+s.trim()+'</strong> <span style="color:#ef4444">'+d.var[i].toFixed(2)+'pp</span>');}
    });
    var top3=d.janmar26.slice().sort(function(a,b){return b-a;}).slice(0,3).reduce(function(s,v){return s+v;},0);
    var dh='🔍 <span style="font-weight:800;color:#fbbf24;letter-spacing:.4px;">DIAGNÓSTICO SKU · '+mkt+'</span><br>';
    dh+='🏆 <strong style="color:#e2e8f0;">SKU Líder:</strong> <strong style="color:#fbbf24;">'+d.skus[tI2]+'</strong> — '+d.janmar26[tI2].toFixed(2)+'% Jan-Mar/26 <span style="color:'+(d.var[tI2]>=0?'#34d399':'#ef4444')+'">'+(d.var[tI2]>=0?'▲ +':'▼ ')+Math.abs(d.var[tI2]).toFixed(2)+'pp</span> vs Jan-Mar/25.<br>';
    dh+='📊 <strong style="color:#e2e8f0;">Top 3 SKUs</strong> representam <strong style="color:#67e8f9;">'+top3.toFixed(1)+'%</strong> do mercado.<br>';
    if(gD.length)dh+='✅ <strong style="color:#34d399;">Ganharam share:</strong> '+gD.join(' · ')+'.<br>';
    if(lD.length)dh+='⚠️ <strong style="color:#ef4444;">Perderam share:</strong> '+lD.join(' · ')+'.';
    dEl.innerHTML='<div style="font-size:11px;color:#D1D5DB;line-height:1.8;">'+dh+'</div>';
  }
}"""

html = html[:idx_s] + NEW_FN + html[idx_e:]
print("   OK: renderMSOSku() substituida (Jan-Mar)")

# ── 5c. Atualizar textos HTML do card ─────────────────────────────────────────
label_fixes = [
    ('MARKET SHARE POR SKU — FYTD26',       'MARKET SHARE POR SKU — JAN-MAR/26'),
    ('$ Share por SKU · FYTD26 vs FYTD25',  '$ Share por SKU · Jan-Mar/26 vs Jan-Mar/25'),
    ('MARKET SHARE SKU — FYTD26',            'MARKET SHARE SKU — Jan-Mar/26'),
    ('VAR MARKET SHARE SKU — FYTD26 vs FYTD25', 'VAR MARKET SHARE SKU — Jan-Mar/26 vs Jan-Mar/25'),
]
for old, new in label_fixes:
    if old in html:
        html = html.replace(old, new)
        print(f"   OK: label '{old[:35]}...' atualizado")
    else:
        print(f"   AVISO: label nao encontrado: '{old[:35]}...'")

# ──────────────────────────────────────────────────────────────────────────────
# 6. SALVAR
# ──────────────────────────────────────────────────────────────────────────────
DASH.write_text(html, encoding='utf-8')
versao = VER / f"Dashboard_Farma_Sul_{ts}_JanMarSku.html"
shutil.copy(DASH, versao)
dl = DL / f"Dashboard_FarmaSul_Giovano_{ts}.html"
shutil.copy(DASH, dl)

print(f"\nVersao:    {versao.name}")
print(f"Downloads: {dl.name}")
print(f"Dashboard: {len(html):,} chars (delta {len(html)-orig:+,})")
print("DONE.")
