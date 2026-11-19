#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
upgrade_mso3_v10.py
Ajuste de largura, contraste extremo e correção de corte:
  • Sidebar 310px com table-layout:fixed + larguras explícitas → sem corte
  • Δ YoY: 14px/900 no scorecard; 13px/900 na tabela e barras (evita overflow)
  • "vs FYTD25" → #cbd5e1 (visível no fundo escuro)
  • Billion format: toFixed(1) → "R$1.4B" em vez de "R$1B"
  • min-height:42px por linha de marca (mais espaço vertical)
  • Marcas: cores 100% opacidade nas barras (sem opacity:0.85)
  • Valores numéricos: font-weight:800 em tudo
"""

import shutil
from pathlib import Path
from datetime import datetime

BASE      = Path(r"C:\Users\valqu\OneDrive\Documentos\Claude\Projects\projeto Dashboard_farma_sul")
DASH_DIR  = BASE / "Dashboard_farma_sul"
DASH_FILE = DASH_DIR / "Dashboard_Farma_Sul_20260512_2220.html"
VERS_DIR  = DASH_DIR / "versoes"

ts = datetime.now().strftime("%Y%m%d_%H%M")

pre = VERS_DIR / f"Dashboard_Farma_Sul_{ts}_PreMSO3v10.html"
shutil.copy2(str(DASH_FILE), str(pre))
print(f"Backup: {pre.name}")

html = DASH_FILE.read_text(encoding="utf-8")

START_MSO3 = "function renderMSO3(){"
END_MSO3   = "/* ═══════════ END MSO3 ═══════════ */"
idx_start  = html.find(START_MSO3)
idx_end    = html.find(END_MSO3)
if idx_start == -1 or idx_end == -1:
    raise RuntimeError("Bloco renderMSO3 nao encontrado")

NEW_RENDER = r'''function renderMSO3(){
  var sel=document.getElementById('mso3MarketSel');
  var mkt=sel?sel.value:'T.BR Farma';
  if(mso3Mode==='share') mso3Mode='val';
  var isVal=mso3Mode==='val', isUn=mso3Mode==='un';
  var brands=MSO_BRANDS, colors=MSO_COLORS;

  var titleEl=document.getElementById('mso3-card-title');
  if(titleEl) titleEl.textContent=isVal?'VENDA VALOR FYTD · JUL–MAR':'UNIDADES FYTD · JUL–MAR';
  var h2El=document.getElementById('mso3-card-h2');
  if(h2El) h2El.textContent='Visão consolidada por Marca em '+(isVal?'Valor (R$ MM)':'Unidades');
  var subEl=document.getElementById('mso3-card-sub');
  if(subEl) subEl.textContent='NielsenIQ · '+(isVal?'R$ e Unidades':'Unidades')+' · Jul/25–Mar/26 · '+mkt;
  ['mso3-table-title','mso3-table'].forEach(function(id){
    var el=document.getElementById(id); if(el) el.style.display='none';
  });
  var hdEl=document.getElementById('mso3-headline');
  if(hdEl) hdEl.style.display='none';

  // ── fmtV10: formata valores ──────────────────────────────────────────────
  function fmtV10(v,compact){
    if(v===null||v===undefined||isNaN(v)) return '—';
    if(isVal){
      if(compact){
        if(v>=1000) return 'R$'+(v/1000).toFixed(1)+'B';   // R$1.4B
        if(v>=100)  return 'R$'+Math.round(v)+'MM';        // R$339MM
        if(v>=10)   return 'R$'+v.toFixed(1)+'MM';         // R$27.2MM
        if(v>=1)    return 'R$'+v.toFixed(2)+'MM';         // R$2.85MM
        return 'R$'+(v*1000).toFixed(0)+'K';
      }
      if(v>=1000) return 'R$ '+(v/1000).toFixed(2)+' B';
      if(v>=100) return 'R$ '+v.toFixed(1)+' MM';
      if(v>=1)   return 'R$ '+v.toFixed(2)+' MM';
      return 'R$ '+(v*1000).toFixed(0)+' K';
    }
    if(compact){
      if(v>=10000) return (v/1000).toFixed(1)+'M';
      if(v>=1000)  return (v/1000).toFixed(1)+'M';
      return Math.round(v)+'K';
    }
    if(v>=1000) return (v/1000).toFixed(1)+' M un';
    return Math.round(v)+' K un';
  }
  function calcDelta10(v25,v26){
    var p=v25>0?Math.round((v26/v25-1)*10000)/100:0;
    return {str:(p>=0?'+':'')+p.toFixed(1)+'%',col:p>=0?'#4ade80':'#f87171',up:p>=0,raw:p};
  }

  // ── Dados ────────────────────────────────────────────────────────────────
  var mt=(typeof FYTD_MARKET_TOTAL!=='undefined')?FYTD_MARKET_TOTAL[mkt]:null;
  var nfv=(typeof NIELSEN_FYTD_VAL!=='undefined')?NIELSEN_FYTD_VAL[mkt]:null;
  var dS=(typeof MKTSHARE_OVERVIEW!=='undefined')?MKTSHARE_OVERVIEW[mkt]:null;
  var d25={},d26={};
  brands.forEach(function(b){
    var bd=nfv&&nfv[b];
    if(bd){d25[b]=isVal?bd.fytd25_val:bd.fytd25_un; d26[b]=isVal?bd.fytd26_val:bd.fytd26_un;}
  });
  var mtV25=mt?(isVal?mt.fytd25_val:mt.fytd25_un):0;
  var mtV26=mt?(isVal?mt.fytd26_val:mt.fytd26_un):0;
  var mtDt=calcDelta10(mtV25,mtV26);
  var scaleRef=mtV26>0?mtV26:1;

  // ── SCORECARDS (3 cards, Δ 14px) ─────────────────────────────────────────
  var scList=[
    {lbl:'MERCADO TOTAL',col:'#22c55e',v25:mtV25,v26:mtV26,sub:'Total canal HB'},
    {lbl:'OFF!',col:colors['OFF!']||'#f59e0b',v25:d25['OFF!']||0,v26:d26['OFF!']||0,
     sub:dS&&dS['OFF!']?(dS['OFF!'].fytd26||0).toFixed(1)+'% share':'Rep. líder SCJ'},
    {lbl:'EXPOSIS',col:colors['EXPOSIS']||'#818cf8',v25:d25['EXPOSIS']||0,v26:d26['EXPOSIS']||0,
     sub:dS&&dS['EXPOSIS']?(dS['EXPOSIS'].fytd26||0).toFixed(1)+'% share':'2ª marca SCJ'},
  ];
  var mktTotalEl=document.getElementById('mso3-market-total');
  if(mktTotalEl){
    mktTotalEl.style.cssText='display:flex;gap:1px;border-radius:8px;overflow:hidden;margin-bottom:14px;border:none;background:none;padding:0;';
    mktTotalEl.innerHTML=scList.map(function(sc){
      var dt=calcDelta10(sc.v25,sc.v26);
      return '<div style="flex:1;min-width:0;padding:12px 16px 10px;background:rgba(15,23,42,0.80);'
        +'border-top:2px solid '+sc.col+';border-right:0.5px solid rgba(255,255,255,0.04);">'
        +'<div style="font-size:9px;font-weight:800;letter-spacing:0.08em;color:#94A3B8;'
          +'text-transform:uppercase;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">'
          +sc.lbl+'</div>'
        +'<div style="font-size:22px;font-weight:900;color:#ffffff;line-height:1.1;margin-top:6px;">'
          +fmtV10(sc.v26)+'</div>'
        +'<div style="font-size:10px;color:#94A3B8;margin-top:2px;white-space:nowrap;'
          +'overflow:hidden;text-overflow:ellipsis;">'+sc.sub+'</div>'
        +'<div style="font-size:14px;font-weight:900;color:'+dt.col+';margin-top:6px;">'
          +(dt.up?'▲':'▼')+' '+dt.str
          +'<span style="font-size:10px;color:#cbd5e1;font-weight:600;margin-left:6px;">vs FYTD25</span>'
        +'</div>'
        +'</div>';
    }).join('');
  }

  // ── Gerador de linha de barra ─────────────────────────────────────────────
  function makeBarRow10(label,labelCol,v25,v26,cor,isTotalRow){
    var dt=calcDelta10(v25,v26);
    var w26=scaleRef>0?Math.max(isTotalRow?100:1,Math.round(v26/scaleRef*100)):0;
    var w25=scaleRef>0?Math.max(0,Math.round(v25/scaleRef*100)):0;
    if(isTotalRow){w26=100;w25=Math.round(v25/scaleRef*100);}
    var valInside=w26>16;
    var valCol=valInside?'rgba(0,0,0,0.82)':cor;
    var valStyle=valInside
      ?'position:absolute;right:8px;top:50%;transform:translateY(-50%);'
        +'font-size:11px;font-weight:900;color:'+valCol+';white-space:nowrap;'
      :'position:absolute;left:'+(w26+1)+'%;top:50%;transform:translateY(-50%);'
        +'font-size:11px;font-weight:800;color:'+valCol+';white-space:nowrap;padding-left:4px;';
    var trackBg=isTotalRow
      ?'background:rgba(34,197,94,0.10);border:0.5px solid rgba(34,197,94,0.30);'
      :'background:rgba(255,255,255,0.05);';
    var barBg=isTotalRow
      ?'background:linear-gradient(90deg,rgba(34,197,94,0.50),rgba(34,197,94,0.35));border-right:2px solid #22c55e;'
      :'background:'+cor+';box-shadow:0 0 12px '+cor+'44;';
    return '<div style="flex:1;display:flex;align-items:center;gap:0;padding:3px 0;min-height:42px;">'
      +'<div style="width:100px;flex-shrink:0;text-align:right;padding-right:10px;">'
        +'<span style="font-size:10px;font-weight:800;color:'+labelCol+';white-space:nowrap;">'
          +label+'</span>'
      +'</div>'
      +'<div style="flex:1;display:flex;flex-direction:column;justify-content:center;gap:4px;">'
        +'<div style="position:relative;height:28px;border-radius:4px;'+trackBg+'">'
          +'<div style="position:absolute;left:0;top:7px;bottom:7px;width:'+w25+'%;'
            +'background:rgba(100,116,139,0.18);border-right:2px solid rgba(100,116,139,0.35);'
            +'border-radius:2px;"></div>'
          +'<div style="position:absolute;left:0;top:0;bottom:0;width:'+w26+'%;'
            +'border-radius:4px;'+barBg+'"></div>'
          +(w26>0?'<span style="'+valStyle+'">'+fmtV10(v26,true)+'</span>':'')
        +'</div>'
        +'<div style="font-size:9px;font-weight:700;color:#cbd5e1;padding-left:2px;white-space:nowrap;">'
          +'FY25: '+fmtV10(v25,true)
        +'</div>'
      +'</div>'
      +'<span style="width:70px;flex-shrink:0;text-align:right;font-size:13px;font-weight:900;'
        +'color:'+dt.col+';padding-left:6px;white-space:nowrap;">'
        +(dt.up?'▲':'▼')+' '+dt.str+'</span>'
      +'</div>';
  }

  // ── ÁREA PRINCIPAL ───────────────────────────────────────────────────────
  var barsEl=document.getElementById('mso3-bars');
  if(!barsEl) return;
  barsEl.style.cssText='display:flex;gap:0;align-items:stretch;margin-bottom:14px;';

  // Eixo X
  var tickVals=[0,0.25,0.5,0.75,1].map(function(f){return f*mtV26;});
  var xAxisHtml=
    '<div style="display:flex;align-items:flex-start;padding-top:4px;'
      +'border-top:0.5px solid rgba(255,255,255,0.06);margin-top:2px;">'
    +'<div style="width:100px;flex-shrink:0;"></div>'
    +'<div style="flex:1;display:flex;justify-content:space-between;">'
    +tickVals.map(function(t,i){
      var txt=(t===0)?'0':fmtV10(t,true);
      var al=i===0?'left':i===tickVals.length-1?'right':'center';
      return '<span style="font-size:9px;color:#64748b;text-align:'+al+';flex:1;font-weight:600;">'+txt+'</span>';
    }).join('')
    +'</div>'
    +'<div style="width:70px;flex-shrink:0;"></div>'
    +'</div>';

  var chartCol=
    '<div style="flex:1;min-width:0;padding-right:6px;display:flex;flex-direction:column;min-height:300px;">'
    +makeBarRow10('TOTAL MKT','#22c55e',mtV25,mtV26,'#22c55e',true)
    +brands.map(function(b){
      return makeBarRow10(b,colors[b]||'#94A3B8',d25[b]||0,d26[b]||0,colors[b]||'#64748b',false);
    }).join('')
    +xAxisHtml
    +'</div>';

  // ── Sidebar: table-layout:fixed → sem corte ──────────────────────────────
  // Larguras fixas: BRAND=80px | F25=62px | F26=68px | Δ=100px → total=310px
  var sideRows10=
    '<tr style="background:rgba(34,197,94,0.09);border-bottom:0.5px solid rgba(34,197,94,0.25);">'
    +'<td style="padding:5px 6px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">'
      +'<span style="display:inline-flex;align-items:center;gap:4px;">'
      +'<span style="width:7px;height:7px;border-radius:2px;background:#22c55e;flex-shrink:0;display:inline-block;"></span>'
      +'<span style="font-size:10px;font-weight:800;color:#22c55e;">TOTAL</span>'
      +'</span></td>'
    +'<td style="padding:5px 6px;text-align:right;overflow:hidden;white-space:nowrap;">'
      +'<span style="font-size:10px;font-weight:800;color:#fbbf24;">'+fmtV10(mtV25,true)+'</span></td>'
    +'<td style="padding:5px 6px;text-align:right;overflow:hidden;white-space:nowrap;">'
      +'<span style="font-size:10px;font-weight:800;color:#ffffff;">'+fmtV10(mtV26,true)+'</span></td>'
    +'<td style="padding:5px 6px;text-align:right;overflow:hidden;white-space:nowrap;">'
      +'<span style="font-size:13px;font-weight:900;color:'+mtDt.col+';">'
        +(mtDt.up?'▲':'▼')+' '+mtDt.str+'</span></td>'
    +'</tr>';

  brands.forEach(function(b){
    var v25=d25[b]||0,v26=d26[b]||0;
    var cor=colors[b]||'#64748b';
    var dt=calcDelta10(v25,v26);
    sideRows10+='<tr style="border-bottom:0.5px solid rgba(255,255,255,0.05);">'
      +'<td style="padding:4px 6px;overflow:hidden;">'
        +'<span style="display:inline-flex;align-items:center;gap:4px;max-width:100%;overflow:hidden;">'
        +'<span style="width:6px;height:6px;border-radius:1px;background:'+cor+';flex-shrink:0;display:inline-block;"></span>'
        +'<span style="font-size:10px;font-weight:700;color:'+cor+';white-space:nowrap;overflow:hidden;'
          +'text-overflow:ellipsis;display:inline-block;max-width:62px;vertical-align:middle;">'+b+'</span>'
        +'</span></td>'
      +'<td style="padding:4px 6px;text-align:right;overflow:hidden;white-space:nowrap;">'
        +'<span style="font-size:10px;font-weight:700;color:#fbbf24;">'+fmtV10(v25,true)+'</span></td>'
      +'<td style="padding:4px 6px;text-align:right;overflow:hidden;white-space:nowrap;">'
        +'<span style="font-size:10px;font-weight:700;color:#e2e8f0;">'+fmtV10(v26,true)+'</span></td>'
      +'<td style="padding:4px 6px;text-align:right;overflow:hidden;white-space:nowrap;">'
        +'<span style="font-size:13px;font-weight:900;color:'+dt.col+';">'
          +(dt.up?'▲':'▼')+' '+dt.str+'</span></td>'
      +'</tr>';
  });

  // Tabela com table-layout:fixed — sem overflow de colunas
  var sideTable=
    '<div style="width:310px;flex-shrink:0;margin-left:8px;background:rgba(255,255,255,0.025);'
      +'border-radius:6px;border:0.5px solid rgba(255,255,255,0.08);'
      +'display:flex;flex-direction:column;overflow:hidden;">'
    +'<table style="width:310px;border-collapse:collapse;table-layout:fixed;flex:1;">'
    // Larguras fixas das colunas
    +'<colgroup>'
      +'<col style="width:82px;">'   // BRAND
      +'<col style="width:64px;">'   // FYTD25
      +'<col style="width:68px;">'   // FYTD26
      +'<col style="width:96px;">'   // Δ YoY (maior para 13px bold "▼ -17.6%")
    +'</colgroup>'
    +'<thead><tr style="border-bottom:1px solid rgba(255,255,255,0.10);">'
    +'<th style="padding:5px 6px;font-size:9px;font-weight:700;letter-spacing:0.07em;'
      +'color:#94A3B8;text-align:left;overflow:hidden;">BRAND</th>'
    +'<th style="padding:5px 6px;font-size:9px;font-weight:700;letter-spacing:0.06em;'
      +'color:#fbbf24;text-align:right;overflow:hidden;">FY25</th>'
    +'<th style="padding:5px 6px;font-size:9px;font-weight:700;letter-spacing:0.06em;'
      +'color:#ffffff;text-align:right;overflow:hidden;">FY26</th>'
    +'<th style="padding:5px 6px;font-size:9px;font-weight:700;letter-spacing:0.06em;'
      +'color:#94A3B8;text-align:right;overflow:hidden;">Δ YoY</th>'
    +'</tr></thead>'
    +'<tbody>'+sideRows10+'</tbody>'
    +'</table>'
    +'<div style="padding:4px 8px;font-size:8px;font-weight:500;color:#64748b;'
      +'border-top:0.5px solid rgba(255,255,255,0.05);white-space:nowrap;overflow:hidden;'
      +'text-overflow:ellipsis;">'
      +'NielsenIQ · 1-Tabela-1 · FYTD Jul–Mar</div>'
    +'</div>';

  barsEl.innerHTML=chartCol+sideTable;

  // ── INSIGHT ──────────────────────────────────────────────────────────────
  var insEl=document.getElementById('mso3-insight');
  if(insEl){
    insEl.style.cssText='padding:10px 16px;background:rgba(255,255,255,0.02);'
      +'border-radius:8px;border-left:3px solid rgba(34,197,94,0.35);'
      +'font-size:10px;color:#D1D5DB;line-height:1.8;margin-top:2px;';
    var ents10=brands.map(function(b){
      var v25=d25[b],v26=d26[b]; if(v25==null||v26==null) return null;
      var dt=calcDelta10(v25,v26);
      return {b:b,dt:dt,cor:colors[b]||'#e2e8f0',v26:v26};
    }).filter(Boolean);
    if(!ents10.length){insEl.innerHTML='';return;}
    var srt=ents10.slice().sort(function(a,b){return b.dt.raw-a.dt.raw;});
    var ldr=srt[0], lag=srt[srt.length-1];
    var mDt=calcDelta10(mtV25,mtV26);
    var mLbl=isVal?'Tamanho do Mercado · Valor':'Tamanho do Mercado · Unidades';
    var totLine=mt
      ?'Total mercado: <strong style="color:#ffffff;">'+fmtV10(mtV26)+'</strong>'
        +' <span style="color:'+mDt.col+';font-weight:700;">'+(mDt.up?'▲':'▼')+' '+mDt.str
        +' vs FYTD25</span><br>':'';
    var ldrTxt=ldr.dt.up
      ?'<strong style="color:'+ldr.cor+';">'+ldr.b+'</strong>'
        +' lidera <span style="color:#4ade80;font-weight:700;">▲ '+ldr.dt.str+'</span> vs FYTD25'
      :'Todas as marcas recuam vs FYTD25';
    var lagTxt=(!lag.dt.up&&lag.b!==ldr.b)
      ?' · <strong style="color:'+lag.cor+';">'+lag.b+'</strong>'
        +' maior retração <span style="color:#f87171;font-weight:700;">'+lag.dt.str+'</span>':'';
    insEl.innerHTML=
      '<span style="display:inline-block;width:7px;height:7px;border-radius:50%;'
        +'background:#22c55e;box-shadow:0 0 6px #22c55e88;margin-right:7px;vertical-align:middle;"></span>'
      +'<strong style="color:#22c55e;letter-spacing:0.06em;">Diagnóstico · '+mLbl+'</strong>'
      +'<br>'+totLine+ldrTxt+lagTxt+'.'
      +'<br><span style="font-size:9px;color:#64748b;">Período: FYTD (Jul–Mar) · NielsenIQ · '+mkt+'</span>';
  }
}
/* ═══════════ END MSO3 ═══════════ */'''

html = html[:idx_start] + NEW_RENDER + html[idx_end + len(END_MSO3):]
print("PATCH OK — renderMSO3 v10 aplicado")

DASH_FILE.write_text(html, encoding="utf-8")
final = VERS_DIR / f"Dashboard_Farma_Sul_{ts}_MSO3v10.html"
shutil.copy2(str(DASH_FILE), str(final))
print(f"Salvo: {DASH_FILE.name}")
print(f"Versao: {final.name}")

# Verificacao rapida
if END_MSO3 in html and "table-layout:fixed" in html and "fmtV10" in html:
    print("\nVerificacao OK: END_MSO3 + table-layout:fixed + fmtV10 presentes")
else:
    print("\nATENCAO: algo faltou!")
print("Done. v10 aplicado.")
