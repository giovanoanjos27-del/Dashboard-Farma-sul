#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
upgrade_mso3_v6.py — MSO3 Foco Valor/Unid + Barra Total + Fill Vertical
Mudancas:
  1. Botão Share ocultado (display:none) — apenas R$ MM e Unidades
  2. mso3Mode default = 'val'
  3. Bar chart: barra TOTAL MERCADO no topo (100% largura) + 5 marcas
     escaladas proporcionalmente ao total
  4. Barras altas (36px) + espaçamento que preenche todo o card
  5. Sidebar: TOTAL + 5 marcas (sem All Others row)
"""
import shutil
from pathlib import Path
from datetime import datetime

BASE      = Path(r"C:\Users\valqu\OneDrive\Documentos\Claude\Projects\projeto Dashboard_farma_sul")
DASH_DIR  = BASE / "Dashboard_farma_sul"
MAIN_FILE = DASH_DIR / "Dashboard_Farma_Sul_20260512_2220.html"
VERS_DIR  = DASH_DIR / "versoes"

# ── 1. Backup ─────────────────────────────────────────────────────────────────
ts = datetime.now().strftime("%Y%m%d_%H%M")
bk = VERS_DIR / f"Dashboard_Farma_Sul_{ts}_PreMSO3v6.html"
shutil.copy2(str(MAIN_FILE), str(bk))
print(f"Backup: {bk.name}")

with open(str(MAIN_FILE), encoding="utf-8") as f:
    html = f.read()

# ── 2. Ocultar botão Share ────────────────────────────────────────────────────
OLD_SHARE_BTN = (
    '<button class="tgl active blue" id="mso3-mode-share" '
    "onclick=\"setMSO3Mode('share',this)\" "
    'style="font-size:11px;padding:5px 12px;border:none;'
    'background:rgba(251,191,36,0.12);color:#fbbf24;cursor:pointer;'
    'font-family:inherit;font-weight:700;">Share</button>'
)
NEW_SHARE_BTN = (
    '<button class="tgl" id="mso3-mode-share" '
    "onclick=\"setMSO3Mode('share',this)\" "
    'style="display:none;">Share</button>'
)
assert OLD_SHARE_BTN in html, "Botão Share não encontrado"
html = html.replace(OLD_SHARE_BTN, NEW_SHARE_BTN, 1)
print("Share button ocultado.")

# ── 3. Ativar R$ MM como botão default ───────────────────────────────────────
OLD_VAL_BTN = (
    '<button class="tgl" id="mso3-mode-val" '
    "onclick=\"setMSO3Mode('val',this)\" "
    'style="font-size:11px;padding:5px 12px;border:none;'
    'border-left:0.5px solid rgba(251,191,36,0.2);background:#161B22;'
    'color:#D1D5DB;cursor:pointer;font-family:inherit;font-weight:600;">R$ MM</button>'
)
NEW_VAL_BTN = (
    '<button class="tgl active" id="mso3-mode-val" '
    "onclick=\"setMSO3Mode('val',this)\" "
    'style="font-size:11px;padding:5px 12px;border:none;'
    'background:rgba(251,191,36,0.12);color:#fbbf24;cursor:pointer;'
    'font-family:inherit;font-weight:700;">R$ MM</button>'
)
assert OLD_VAL_BTN in html, "Botão R$ MM não encontrado"
html = html.replace(OLD_VAL_BTN, NEW_VAL_BTN, 1)
print("R$ MM button ativado como default.")

# ── 4. mso3Mode default → 'val' ──────────────────────────────────────────────
OLD_MODE = "var mso3Mode = 'share'; // 'share' | 'val' | 'un'"
NEW_MODE = "var mso3Mode = 'val'; // 'val' | 'un'"
assert OLD_MODE in html, "mso3Mode default não encontrado"
html = html.replace(OLD_MODE, NEW_MODE, 1)
print("mso3Mode default = 'val'.")

# ── 5. Nova renderMSO3 v6 ─────────────────────────────────────────────────────
OLD_START = "function renderMSO3(){"
OLD_END   = "/* ═══════════ END MSO3 ═══════════ */"
assert OLD_START in html and OLD_END in html
start_idx = html.index(OLD_START)
end_idx   = html.index(OLD_END) + len(OLD_END)
OLD_BLOCK = html[start_idx:end_idx]

NEW_FUNC = r"""function renderMSO3(){
  var sel=document.getElementById('mso3MarketSel');
  var mkt=sel?sel.value:'T.BR Farma';
  // Share desativado — apenas val e un
  if(mso3Mode==='share') mso3Mode='val';
  var isVal=mso3Mode==='val', isUn=mso3Mode==='un';
  var brands=MSO_BRANDS, colors=MSO_COLORS;

  // ── Labels estáticos ──
  var titleEl=document.getElementById('mso3-card-title');
  if(titleEl) titleEl.textContent=isVal?'VENDA VALOR FYTD · JUL–MAR':'UNIDADES FYTD · JUL–MAR';
  var h2El=document.getElementById('mso3-card-h2');
  if(h2El) h2El.textContent='Visão consolidada por Marca em '+(isVal?'Valor (R$ MM)':'Unidades');
  var subEl=document.getElementById('mso3-card-sub');
  if(subEl) subEl.textContent='NielsenIQ · '+(isVal?'R$ e Unidades':'Unidades')+' · Jul/25–Mar/26 · '+mkt;
  var ttl6=document.getElementById('mso3-table-title');
  if(ttl6) ttl6.style.display='none';
  var tbl6=document.getElementById('mso3-table');
  if(tbl6) tbl6.style.display='none';
  var hdEl=document.getElementById('mso3-headline');
  if(hdEl) hdEl.style.display='none';

  // ── Helpers ──
  function fmtV6(v,compact){
    if(v===null||v===undefined||isNaN(v)) return '—';
    if(isVal){
      if(compact){
        if(v>=100)  return 'R$'+Math.round(v)+'MM';
        if(v>=10)   return 'R$'+v.toFixed(1)+'MM';
        if(v>=1)    return 'R$'+v.toFixed(2)+'MM';
        return 'R$'+(v*1000).toFixed(0)+'K';
      }
      if(v>=100) return 'R$ '+v.toFixed(1)+' MM';
      if(v>=1)   return 'R$ '+v.toFixed(2)+' MM';
      return 'R$ '+(v*1000).toFixed(0)+' K';
    }
    // unidades
    if(compact){
      if(v>=10000) return (v/1000).toFixed(1)+'M';
      if(v>=1000)  return Math.round(v/1000)+'M';
      if(v>=100)   return Math.round(v)+'K';
      return v.toFixed(1)+'K';
    }
    if(v>=1000) return (v/1000).toFixed(1)+' M un';
    return Math.round(v)+' K un';
  }
  function calcDelta6(v25,v26){
    var p=v25>0?Math.round((v26/v25-1)*10000)/100:0;
    return {str:(p>=0?'+':'')+p.toFixed(1)+'%',col:p>=0?'#34d399':'#ef4444',up:p>=0,raw:p};
  }

  // ── Coleta de dados ──
  var mt=(typeof FYTD_MARKET_TOTAL!=='undefined')?FYTD_MARKET_TOTAL[mkt]:null;
  var nfv=(typeof NIELSEN_FYTD_VAL!=='undefined')?NIELSEN_FYTD_VAL[mkt]:null;
  var dS=(typeof MKTSHARE_OVERVIEW!=='undefined')?MKTSHARE_OVERVIEW[mkt]:null;
  var d25={}, d26={};
  brands.forEach(function(b){
    var bd=nfv&&nfv[b];
    if(bd){d25[b]=isVal?bd.fytd25_val:bd.fytd25_un; d26[b]=isVal?bd.fytd26_val:bd.fytd26_un;}
  });
  var mtV25=mt?(isVal?mt.fytd25_val:mt.fytd25_un):0;
  var mtV26=mt?(isVal?mt.fytd26_val:mt.fytd26_un):0;
  var mtDt=calcDelta6(mtV25,mtV26);
  // All Others scorecard = SBP + XO INSETO + SUPER REPELEX
  var aoV25=(d25['SBP']||0)+(d25['XO INSETO']||0)+(d25['SUPER REPELEX']||0);
  var aoV26=(d26['SBP']||0)+(d26['XO INSETO']||0)+(d26['SUPER REPELEX']||0);

  // ── SCORECARDS DE TOPO ──
  var scList=[
    {lbl:'MERCADO TOTAL', col:'#22c55e', v25:mtV25, v26:mtV26,
     sub:'Personal Repellent'},
    {lbl:'OFF!', col:colors['OFF!']||'#f59e0b', v25:d25['OFF!']||0, v26:d26['OFF!']||0,
     sub:dS&&dS['OFF!']?(dS['OFF!'].fytd26||0).toFixed(1)+'% share':'Repelente líder'},
    {lbl:'EXPOSIS', col:colors['EXPOSIS']||'#818cf8', v25:d25['EXPOSIS']||0, v26:d26['EXPOSIS']||0,
     sub:dS&&dS['EXPOSIS']?(dS['EXPOSIS'].fytd26||0).toFixed(1)+'% share':'2ª marca SCJ'},
    {lbl:'ALL OTHERS', col:'#64748b', v25:aoV25, v26:aoV26,
     sub:'SBP · XO · Super Repelex'},
  ];
  var mktTotalEl=document.getElementById('mso3-market-total');
  if(mktTotalEl){
    mktTotalEl.style.cssText='display:flex;gap:1px;border-radius:8px;overflow:hidden;'
      +'margin-bottom:14px;border:none;background:none;padding:0;';
    mktTotalEl.innerHTML=scList.map(function(sc){
      var dt=calcDelta6(sc.v25,sc.v26);
      return '<div style="flex:1;min-width:0;padding:12px 14px 10px;'
        +'background:rgba(15,23,42,0.80);border-top:2px solid '+sc.col+';'
        +'border-right:0.5px solid rgba(255,255,255,0.04);">'
        +'<div style="font-size:9px;font-weight:800;letter-spacing:0.08em;color:#374151;'
          +'text-transform:uppercase;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">'
          +sc.lbl+'</div>'
        +'<div style="font-size:18px;font-weight:800;color:#f1f5f9;line-height:1.15;margin-top:5px;">'
          +fmtV6(sc.v26)+'</div>'
        +'<div style="font-size:10px;color:#374151;margin-top:2px;white-space:nowrap;'
          +'overflow:hidden;text-overflow:ellipsis;">'+sc.sub+'</div>'
        +'<div style="font-size:11px;font-weight:700;color:'+dt.col+';margin-top:4px;">'
          +(dt.up?'▲':'▼')+' '+dt.str
          +'<span style="font-size:9px;color:#1e293b;font-weight:400;margin-left:4px;">vs FYTD25</span>'
        +'</div>'
        +'</div>';
    }).join('');
  }

  // ── ÁREA PRINCIPAL: barchart + sidebar ──
  var barsEl=document.getElementById('mso3-bars');
  if(!barsEl) return;
  barsEl.style.cssText='display:flex;gap:0;align-items:flex-start;margin-bottom:14px;';

  // Escala: TOTAL = 100% sempre; marcas proporcionais ao total
  var scaleRef=mtV26>0?mtV26:1;
  // Ticks x-axis: 0%, 25%, 50%, 75%, 100% do total
  var tickVals=[0,0.25,0.5,0.75,1].map(function(f){return f*scaleRef;});

  var BAR_H=36, GAP=13;  // px — 6 barras × (36+13) = 294px

  // ── Barra TOTAL MERCADO (100%) ──
  var totalBarHtml=
    '<div style="display:flex;align-items:center;gap:0;margin-bottom:'+GAP+'px;">'
    // Label
    +'<div style="width:102px;flex-shrink:0;text-align:right;padding-right:10px;">'
      +'<span style="font-size:10px;font-weight:700;color:#22c55e;white-space:nowrap;">TOTAL MKT</span>'
    +'</div>'
    // Track
    +'<div style="flex:1;position:relative;height:'+BAR_H+'px;border-radius:4px;'
      +'background:rgba(34,197,94,0.07);border:0.5px solid rgba(34,197,94,0.20);">'
      // Barra FY25 (faint, por baixo)
      +'<div style="position:absolute;left:0;top:8px;bottom:8px;width:100%;'
        +'background:rgba(100,116,139,0.12);border-radius:3px;"></div>'
      // Barra FY26 (total = 100%)
      +'<div style="position:absolute;left:0;top:0;bottom:0;width:100%;'
        +'background:rgba(34,197,94,0.30);border-radius:4px;'
        +'border-right:2px solid #22c55e;"></div>'
      // Valor (dentro, à direita)
      +'<span style="position:absolute;right:10px;top:50%;transform:translateY(-50%);'
        +'font-size:11px;font-weight:700;color:#22c55e;white-space:nowrap;">'
        +fmtV6(mtV26,true)+'</span>'
    +'</div>'
    // Delta
    +'<span style="width:60px;flex-shrink:0;text-align:right;font-size:10px;font-weight:700;'
      +'color:'+mtDt.col+';padding-left:8px;white-space:nowrap;">'
      +(mtDt.up?'▲':'▼')+' '+mtDt.str+'</span>'
    +'</div>';

  // ── Barras por marca ──
  var brandBarsHtml=brands.map(function(b){
    var v25=d25[b]||0, v26=d26[b]||0;
    var cor=colors[b]||'#64748b';
    var dt=calcDelta6(v25,v26);
    var w26=v26>0?Math.max(2,Math.round(v26/scaleRef*100)):0;
    var w25=v25>0?Math.max(0,Math.round(v25/scaleRef*100)):0;
    // Valor: inside se barra >22%, fora se pequena
    var valInside=w26>22;
    var valStyle=valInside
      ?'position:absolute;right:8px;top:50%;transform:translateY(-50%);'
        +'font-size:10px;font-weight:700;color:rgba(0,0,0,0.75);white-space:nowrap;'
      :'position:absolute;left:'+(w26+1)+'%;top:50%;transform:translateY(-50%);'
        +'font-size:10px;font-weight:700;color:'+cor+';white-space:nowrap;padding-left:4px;';
    return '<div style="display:flex;align-items:center;gap:0;margin-bottom:'+GAP+'px;">'
      // Label
      +'<div style="width:102px;flex-shrink:0;text-align:right;padding-right:10px;">'
        +'<span style="font-size:10px;font-weight:600;color:#94A3B8;white-space:nowrap;">'+b+'</span>'
      +'</div>'
      // Track
      +'<div style="flex:1;position:relative;height:'+BAR_H+'px;border-radius:4px;'
        +'background:rgba(255,255,255,0.04);">'
        // FY25 cinza faint
        +'<div style="position:absolute;left:0;top:8px;bottom:8px;width:'+w25+'%;'
          +'background:rgba(100,116,139,0.16);border-right:1.5px solid rgba(100,116,139,0.28);'
          +'border-radius:2px;"></div>'
        // FY26 sólido
        +'<div style="position:absolute;left:0;top:0;bottom:0;width:'+w26+'%;'
          +'background:'+cor+';opacity:0.85;border-radius:4px;'
          +'box-shadow:0 0 12px '+cor+'33;"></div>'
        // Valor
        +(w26>0?'<span style="'+valStyle+'">'+fmtV6(v26,true)+'</span>':'')
      +'</div>'
      // Delta
      +'<span style="width:60px;flex-shrink:0;text-align:right;font-size:10px;font-weight:700;'
        +'color:'+dt.col+';padding-left:8px;white-space:nowrap;">'
        +(dt.up?'▲':'▼')+' '+dt.str+'</span>'
      +'</div>';
  }).join('');

  // Eixo X
  var xAxisHtml='<div style="display:flex;align-items:flex-start;margin-top:2px;">'
    +'<div style="width:102px;flex-shrink:0;"></div>'
    +'<div style="flex:1;display:flex;justify-content:space-between;">'
    +tickVals.map(function(t,i){
      var txt=t===0?'0':fmtV6(t,true);
      var align=i===0?'left':i===tickVals.length-1?'right':'center';
      return '<span style="font-size:9px;color:#1e293b;text-align:'+align+';flex:1;">'+txt+'</span>';
    }).join('')
    +'</div>'
    +'<div style="width:60px;flex-shrink:0;"></div>'
    +'</div>';

  // Sidebar
  var sideColA=isVal?'FYTD26':'FYTD26';
  var sideRows6=
    '<tr style="background:rgba(34,197,94,0.08);border-bottom:0.5px solid rgba(34,197,94,0.2);">'
    +'<td style="padding:7px 8px;font-size:10px;">'
      +'<span style="display:inline-flex;align-items:center;gap:5px;">'
      +'<span style="width:8px;height:8px;border-radius:2px;background:#22c55e;flex-shrink:0;display:inline-block;"></span>'
      +'<span style="color:#22c55e;font-weight:700;font-size:10px;">TOTAL</span>'
      +'</span></td>'
    +'<td style="padding:7px 8px;font-size:10px;text-align:right;font-weight:700;color:#f1f5f9;white-space:nowrap;">'
      +fmtV6(mtV26,true)+'</td>'
    +'<td style="padding:7px 8px;font-size:10px;text-align:right;color:'+mtDt.col+';font-weight:700;">'
      +(mtDt.up?'▲':'▼')+' '+mtDt.str+'</td>'
    +'</tr>';
  brands.forEach(function(b){
    var v25=d25[b]||0, v26=d26[b]||0;
    var cor=colors[b]||'#64748b';
    var dt=calcDelta6(v25,v26);
    var shareStr=mtV26>0?(v26/mtV26*100).toFixed(1)+'%':'—';
    sideRows6+='<tr style="border-bottom:0.5px solid rgba(255,255,255,0.04);">'
      +'<td style="padding:5px 8px;font-size:10px;">'
        +'<span style="display:inline-flex;align-items:center;gap:5px;">'
        +'<span style="width:6px;height:6px;border-radius:1px;background:'+cor+';flex-shrink:0;display:inline-block;"></span>'
        +'<span style="color:'+cor+';font-weight:600;font-size:10px;">'+b+'</span>'
        +'</span></td>'
      +'<td style="padding:5px 8px;font-size:10px;text-align:right;font-weight:700;color:#e2e8f0;white-space:nowrap;">'
        +fmtV6(v26,true)+'</td>'
      +'<td style="padding:5px 8px;font-size:10px;text-align:right;color:'+dt.col+';font-weight:700;">'
        +(dt.up?'▲':'▼')+' '+dt.str+'</td>'
      +'</tr>';
  });

  var sideTable=
    '<div style="width:218px;flex-shrink:0;margin-left:10px;background:rgba(255,255,255,0.02);'
      +'border-radius:6px;overflow:hidden;border:0.5px solid rgba(255,255,255,0.07);">'
    +'<table style="width:100%;border-collapse:collapse;">'
    +'<thead><tr style="border-bottom:1px solid rgba(255,255,255,0.08);">'
    +'<th style="padding:6px 8px;font-size:9px;font-weight:700;letter-spacing:0.07em;color:#374151;text-align:left;">BRAND</th>'
    +'<th style="padding:6px 8px;font-size:9px;font-weight:700;letter-spacing:0.07em;color:#374151;text-align:right;">'+sideColA+'</th>'
    +'<th style="padding:6px 8px;font-size:9px;font-weight:700;letter-spacing:0.07em;color:#374151;text-align:right;">Δ YoY</th>'
    +'</tr></thead>'
    +'<tbody>'+sideRows6+'</tbody>'
    +'</table>'
    +'<div style="padding:5px 8px;font-size:9px;color:#1e293b;border-top:0.5px solid rgba(255,255,255,0.04);">'
      +'NielsenIQ · 1-Tabela-1 · FYTD = Jul–Mar</div>'
    +'</div>';

  // Chart area (flex:1)
  var chartArea=
    '<div style="flex:1;min-width:0;padding-right:4px;">'
    +totalBarHtml
    +brandBarsHtml
    +xAxisHtml
    +'</div>';

  barsEl.innerHTML=chartArea+sideTable;

  // ── INSIGHT rodapé ──
  var insEl=document.getElementById('mso3-insight');
  if(insEl){
    insEl.style.cssText='padding:10px 16px;background:rgba(255,255,255,0.02);'
      +'border-radius:8px;border-left:3px solid rgba(34,197,94,0.35);'
      +'font-size:10px;color:#D1D5DB;line-height:1.8;margin-top:2px;';
    var ents6=brands.map(function(b){
      var v25=d25[b],v26=d26[b];if(v25==null||v26==null)return null;
      var dt=calcDelta6(v25,v26);
      return {b:b,dt:dt,cor:colors[b]||'#e2e8f0',v26:v26};
    }).filter(Boolean);
    if(!ents6.length){insEl.innerHTML='';return;}
    var srt6=ents6.slice().sort(function(a,b){return b.dt.raw-a.dt.raw;});
    var ldr6=srt6[0],lag6=srt6[srt6.length-1];
    var mDt=calcDelta6(mtV25,mtV26);
    var mLbl6=isVal?'Tamanho do Mercado · Valor':'Tamanho do Mercado · Unidades';
    var totLine=mt
      ?'Total mercado: <strong style="color:#f1f5f9;">'+fmtV6(mtV26)+'</strong>'
        +' <span style="color:'+mDt.col+';">'+(mDt.up?'▲':'▼')+' '+mDt.str+' vs FYTD25</span><br>':'';
    var ldrTxt=ldr6.dt.up
      ?'<strong style="color:'+ldr6.cor+';">'+ldr6.b+'</strong> lidera '
        +'<span style="color:#34d399;">▲ '+ldr6.dt.str+'</span> vs FYTD25'
      :'Todas as marcas recuam vs FYTD25';
    var lagTxt=(!lag6.dt.up&&lag6.b!==ldr6.b)
      ?' · <strong style="color:'+lag6.cor+';">'+lag6.b+'</strong> maior retração '
        +'<span style="color:#ef4444;">'+lag6.dt.str+'</span>':'';
    insEl.innerHTML=
      '<span style="display:inline-block;width:7px;height:7px;border-radius:50%;'
        +'background:#22c55e;box-shadow:0 0 6px #22c55e88;margin-right:7px;vertical-align:middle;"></span>'
      +'<strong style="color:#22c55e;letter-spacing:0.06em;">Diagnóstico · '+mLbl6+'</strong>'
      +'<br>'+totLine+ldrTxt+lagTxt+'.'
      +'<br><span style="font-size:9px;color:#1e293b;">Período: FYTD (Jul–Mar) · NielsenIQ · '+mkt+'</span>';
  }
}
/* ═══════════ END MSO3 ═══════════ */"""

assert OLD_BLOCK in html, "OLD_BLOCK não encontrado"
html = html.replace(OLD_BLOCK, NEW_FUNC, 1)
print("renderMSO3() v6 substituida.")

# ── 6. Salvar ─────────────────────────────────────────────────────────────────
with open(str(MAIN_FILE), "w", encoding="utf-8") as f:
    f.write(html)
print(f"Salvo ({len(html):,} chars).")

ts2 = datetime.now().strftime("%Y%m%d_%H%M")
ver = VERS_DIR / f"Dashboard_Farma_Sul_{ts2}_MSO3v6.html"
shutil.copy2(str(MAIN_FILE), str(ver))
print(f"Versao: {ver.name}")
print("DONE!")
