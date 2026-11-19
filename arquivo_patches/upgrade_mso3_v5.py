#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
upgrade_mso3_v5.py — MSO3 "Odor Block" Style
Redesign completo do card FYTD para o padrao executivo do card Odor Block:
  1. Scorecards de topo (4 KPI cards horizontais com borda colorida)
  2. Bar chart horizontal simples + sidebar de tabela à direita
  3. Diagnóstico estilo neon bullet no rodapé
  4. Sem barras diagonais / sem grid 2 colunas — foco em legibilidade
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
bk = VERS_DIR / f"Dashboard_Farma_Sul_{ts}_PreMSO3v5.html"
shutil.copy2(str(MAIN_FILE), str(bk))
print(f"Backup: {bk.name}")

with open(str(MAIN_FILE), encoding="utf-8") as f:
    html = f.read()

# ── 2. Substitui renderMSO3 ───────────────────────────────────────────────────
OLD_START = "function renderMSO3(){"
OLD_END   = "/* ═══════════ END MSO3 ═══════════ */"
assert OLD_START in html, "ANCHOR START nao encontrado"
assert OLD_END   in html, "ANCHOR END nao encontrado"

start_idx = html.index(OLD_START)
end_idx   = html.index(OLD_END) + len(OLD_END)
OLD_BLOCK = html[start_idx:end_idx]

NEW_FUNC = r"""function renderMSO3(){
  var sel=document.getElementById('mso3MarketSel');
  var mkt=sel?sel.value:'T.BR Farma';
  var isShare=mso3Mode==='share', isVal=mso3Mode==='val', isUn=mso3Mode==='un';
  var brands=MSO_BRANDS, colors=MSO_COLORS;

  // ── Labels estáticos ──
  var titleEl=document.getElementById('mso3-card-title');
  if(titleEl) titleEl.textContent=isShare?'VISAO FISCAL FYTD · JUL–MAR':(isVal?'VENDA VALOR FYTD · JUL–MAR':'UNIDADES FYTD · JUL–MAR');
  var h2El=document.getElementById('mso3-card-h2');
  if(h2El) h2El.textContent='Visão consolidada por Marca em '+(isShare?'$ Share':(isVal?'Valor (R$)':'Unidades'));
  var subEl=document.getElementById('mso3-card-sub');
  if(subEl) subEl.textContent='NielsenIQ · '+(isUn?'Unidades':'R$ e Unidades')+' · Jul/25–Mar/26 · '+mkt;
  // Ocultar tabela legado
  var ttl5=document.getElementById('mso3-table-title');
  if(ttl5) ttl5.style.display='none';
  var tbl5=document.getElementById('mso3-table');
  if(tbl5) tbl5.style.display='none';
  // Ocultar headline legado
  var hdEl=document.getElementById('mso3-headline');
  if(hdEl) hdEl.style.display='none';

  // ── Helpers ──
  function fmtV5(v,compact){
    if(v===null||v===undefined||isNaN(v)) return '—';
    if(isShare) return v.toFixed(2)+'%';
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
    if(compact){
      if(v>=10000) return (v/1000).toFixed(1)+'M';
      if(v>=1000)  return Math.round(v/1000)+'M';
      if(v>=100)   return Math.round(v)+'K';
      return v.toFixed(1)+'K';
    }
    if(v>=1000) return (v/1000).toFixed(1)+' M un';
    return Math.round(v)+' K un';
  }
  function calcDelta5(v25,v26){
    if(isShare){
      var d=Math.round((v26-v25)*100)/100;
      return {str:(d>=0?'+':'')+d.toFixed(2)+'pp',col:d>=0?'#34d399':'#ef4444',up:d>=0,raw:d};
    }
    var p=v25>0?Math.round((v26/v25-1)*10000)/100:0;
    return {str:(p>=0?'+':'')+p.toFixed(1)+'%',col:p>=0?'#34d399':'#ef4444',up:p>=0,raw:p};
  }
  function niceMax5(m){
    if(!m||m<=0) return 1;
    var exp=Math.pow(10,Math.floor(Math.log10(m)));
    var r=[1,2,2.5,5,10];
    for(var i=0;i<r.length;i++){
      var c=Math.ceil(m/(exp*r[i]))*(exp*r[i]);
      if(c>=m) return c;
    }
    return Math.ceil(m/exp)*exp;
  }

  // ── Coleta de dados ──
  var mt=(typeof FYTD_MARKET_TOTAL!=='undefined')?FYTD_MARKET_TOTAL[mkt]:null;
  var nfv=(typeof NIELSEN_FYTD_VAL!=='undefined')?NIELSEN_FYTD_VAL[mkt]:null;
  var dS=(typeof MKTSHARE_OVERVIEW!=='undefined')?MKTSHARE_OVERVIEW[mkt]:null;
  var d25={}, d26={};
  brands.forEach(function(b){
    if(isShare){ var bd=dS&&dS[b]; if(bd){d25[b]=bd.fytd25||0; d26[b]=bd.fytd26||0;} }
    else { var bd=nfv&&nfv[b]; if(bd){d25[b]=isVal?bd.fytd25_val:bd.fytd25_un; d26[b]=isVal?bd.fytd26_val:bd.fytd26_un;} }
  });
  var mtV25=mt?(isUn?mt.fytd25_un:mt.fytd25_val):0;
  var mtV26=mt?(isUn?mt.fytd26_un:mt.fytd26_val):0;
  // All Others (KPI card) = SBP + XO INSETO + SUPER REPELEX
  var aoV25=(d25['SBP']||0)+(d25['XO INSETO']||0)+(d25['SUPER REPELEX']||0);
  var aoV26=(d26['SBP']||0)+(d26['XO INSETO']||0)+(d26['SUPER REPELEX']||0);
  // All Others não-SCJ (sidebar) = total mercado - soma 5 marcas SCJ
  var scjSum=brands.reduce(function(s,b){return s+(d26[b]||0);},0);
  var nonScjV26=mt&&!isShare?Math.max(0,mtV26-scjSum):null;

  // ── SCORECARDS DE TOPO ──
  var scList=[
    {lbl:'MERCADO TOTAL', sub:'Personal Repellent', col:'#22c55e',
     v25:mtV25, v26:mtV26, shareTxt:null},
    {lbl:'OFF!', sub:'Repelente líder SCJ', col:colors['OFF!']||'#f59e0b',
     v25:d25['OFF!']||0, v26:d26['OFF!']||0,
     shareTxt:isShare?null:(dS&&dS['OFF!']?(dS['OFF!'].fytd26||0).toFixed(2)+'% share':null)},
    {lbl:'EXPOSIS', sub:'2º marca SCJ', col:colors['EXPOSIS']||'#818cf8',
     v25:d25['EXPOSIS']||0, v26:d26['EXPOSIS']||0,
     shareTxt:isShare?null:(dS&&dS['EXPOSIS']?(dS['EXPOSIS'].fytd26||0).toFixed(2)+'% share':null)},
    {lbl:'ALL OTHERS', sub:'SBP · XO · Super Repelex', col:'#64748b',
     v25:aoV25, v26:aoV26, shareTxt:null},
  ];
  var mktTotalEl=document.getElementById('mso3-market-total');
  if(mktTotalEl){
    // Reset estilos legado
    mktTotalEl.style.cssText='display:flex;gap:1px;border-radius:8px;overflow:hidden;'
      +'margin-bottom:12px;border:none;background:none;padding:0;';
    mktTotalEl.innerHTML=scList.map(function(sc){
      var dt=calcDelta5(sc.v25,sc.v26);
      var arr=dt.up?'▲':'▼';
      var shareLine=sc.shareTxt?'<div style="font-size:10px;color:#64748b;margin-top:1px;">'+sc.shareTxt+'</div>':'';
      return '<div style="flex:1;min-width:0;padding:12px 14px 10px;'
        +'background:rgba(15,23,42,0.75);border-top:2px solid '+sc.col+';border-right:0.5px solid rgba(255,255,255,0.04);">'
        +'<div style="font-size:9px;font-weight:800;letter-spacing:0.09em;color:#475569;'
          +'text-transform:uppercase;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">'
          +sc.lbl+'</div>'
        +'<div style="font-size:17px;font-weight:800;color:#f1f5f9;letter-spacing:-0.01em;'
          +'line-height:1.15;margin-top:5px;white-space:nowrap;">'+fmtV5(sc.v26)+'</div>'
        +shareLine
        +'<div style="font-size:11px;font-weight:700;color:'+dt.col+';margin-top:4px;">'
          +arr+' '+dt.str
          +'<span style="font-size:9px;color:#1e293b;font-weight:400;margin-left:4px;">vs FYTD25</span>'
        +'</div>'
        +'</div>';
    }).join('');
  }

  // ── ÁREA PRINCIPAL: bar chart (flex:1) + sidebar (220px) ──
  var barsEl=document.getElementById('mso3-bars');
  if(!barsEl) return;
  barsEl.style.cssText='display:flex;gap:0;align-items:flex-start;margin-bottom:14px;';

  // Escala do gráfico
  var allV5=brands.map(function(b){return d26[b]||0;}).filter(function(v){return v>0;});
  var scaleMax=niceMax5(Math.max.apply(null,allV5)||1);
  var tickVals=[0,0.25,0.5,0.75,1].map(function(f){return f*scaleMax;});

  // Barras (FY26 sólido + FY25 contorno cinza)
  var barRows=brands.map(function(b){
    var v25=d25[b]||0, v26=d26[b]||0;
    var cor=colors[b]||'#64748b';
    var dt=calcDelta5(v25,v26);
    var w26=Math.max(0,Math.round(v26/scaleMax*100));
    var w25=Math.max(0,Math.round(v25/scaleMax*100));
    var tip='FYTD25: '+fmtV5(v25)+' | FYTD26: '+fmtV5(v26)+' | Δ: '+dt.str;
    return '<div title="'+tip+'" style="display:flex;align-items:center;gap:0;margin-bottom:8px;cursor:default;">'
      // Nome marca (coluna esquerda fixa)
      +'<div style="width:100px;flex-shrink:0;text-align:right;padding-right:10px;">'
        +'<span style="font-size:10px;font-weight:600;color:#94A3B8;white-space:nowrap;">'+b+'</span>'
      +'</div>'
      // Track
      +'<div style="flex:1;position:relative;height:22px;border-radius:3px;background:rgba(255,255,255,0.04);">'
        // FY25 cinza faint (referência de fundo)
        +'<div style="position:absolute;left:0;top:5px;bottom:5px;width:'+w25+'%;'
          +'background:rgba(100,116,139,0.16);border-right:1.5px solid rgba(100,116,139,0.30);border-radius:2px;"></div>'
        // FY26 sólido
        +'<div style="position:absolute;left:0;top:0;bottom:0;width:'+w26+'%;'
          +'background:'+cor+';border-radius:3px;opacity:0.82;'
          +'box-shadow:0 0 10px '+cor+'33;"></div>'
        // Valor dentro/fora da barra
        +'<span style="position:absolute;left:'+(w26>18?w26-1:w26+1)+'%;top:50%;transform:translate('+(w26>18?'-100%':'0')+',-50%);'
          +'font-size:9px;font-weight:700;color:'+(w26>18?'rgba(0,0,0,0.7)':'#'+cor.slice(1))+';white-space:nowrap;padding:0 4px;">'
          +fmtV5(v26,true)+'</span>'
      +'</div>'
      // Delta
      +'<span style="width:58px;flex-shrink:0;text-align:right;font-size:10px;font-weight:700;'
        +'color:'+dt.col+';padding-left:8px;white-space:nowrap;">'+(dt.up?'▲':'▼')+' '+dt.str+'</span>'
      +'</div>';
  }).join('');

  // Eixo X (ticks)
  var xAxis='<div style="display:flex;align-items:flex-start;margin-top:3px;">'
    +'<div style="width:100px;flex-shrink:0;"></div>'
    +'<div style="flex:1;display:flex;justify-content:space-between;">'
    +tickVals.map(function(t,i){
      var txt=t===0?'0':fmtV5(t,true);
      var align=i===0?'left':i===tickVals.length-1?'right':'center';
      return '<span style="font-size:9px;color:#1e293b;text-align:'+align+';flex:1;">'+txt+'</span>';
    }).join('')
    +'</div>'
    +'<div style="width:58px;flex-shrink:0;"></div>'
    +'</div>';

  // Sidebar — tabela Brand | Valor | Delta/Share%
  var sideColA=isShare?'Share':'Valor';
  var sideColB=isShare?'Δ pp':(!isShare&&mtV26>0?'Share%':'Δ');
  var sideRows5=
    // Linha TOTAL
    '<tr style="background:rgba(34,197,94,0.07);border-bottom:0.5px solid rgba(34,197,94,0.18);">'
    +'<td style="padding:7px 8px;font-size:10px;">'
      +'<span style="display:inline-flex;align-items:center;gap:5px;">'
      +'<span style="width:8px;height:8px;border-radius:2px;background:#22c55e;flex-shrink:0;display:inline-block;"></span>'
      +'<span style="color:#22c55e;font-weight:700;letter-spacing:0.02em;">TOTAL MERCADO</span>'
      +'</span></td>'
    +'<td style="padding:7px 8px;font-size:10px;text-align:right;font-weight:700;color:#f1f5f9;white-space:nowrap;">'
      +fmtV5(mtV26,true)+'</td>'
    +'<td style="padding:7px 8px;font-size:10px;text-align:right;color:#374151;">—</td>'
    +'</tr>';

  // Linhas por marca
  brands.forEach(function(b){
    var v25=d25[b]||0, v26=d26[b]||0;
    var cor=colors[b]||'#64748b';
    var dt=calcDelta5(v25,v26);
    var colA=fmtV5(v26,true);
    var colB=isShare?dt.str:(mtV26>0?(v26/mtV26*100).toFixed(1)+'%':'—');
    sideRows5+='<tr style="border-bottom:0.5px solid rgba(255,255,255,0.04);">'
      +'<td style="padding:5px 8px;font-size:10px;">'
        +'<span style="display:inline-flex;align-items:center;gap:5px;">'
        +'<span style="width:6px;height:6px;border-radius:1px;background:'+cor+';flex-shrink:0;display:inline-block;"></span>'
        +'<span style="color:'+cor+';font-weight:600;">'+b+'</span>'
        +'</span></td>'
      +'<td style="padding:5px 8px;font-size:10px;text-align:right;color:#e2e8f0;font-weight:700;white-space:nowrap;">'+colA+'</td>'
      +'<td style="padding:5px 8px;font-size:10px;text-align:right;color:'+dt.col+';font-weight:700;">'+(dt.up?'▲':'▼')+' '+colB+'</td>'
      +'</tr>';
  });
  // All Others não-SCJ
  if(nonScjV26!==null&&nonScjV26>1){
    var aoShare=mtV26>0?(nonScjV26/mtV26*100).toFixed(1)+'%':'—';
    sideRows5+='<tr style="border-top:0.5px solid rgba(255,255,255,0.05);">'
      +'<td style="padding:5px 8px;font-size:10px;color:#374151;">· All Others</td>'
      +'<td style="padding:5px 8px;font-size:10px;text-align:right;color:#374151;white-space:nowrap;">'+fmtV5(nonScjV26,true)+'</td>'
      +'<td style="padding:5px 8px;font-size:10px;text-align:right;color:#374151;">'+aoShare+'</td>'
      +'</tr>';
  }

  var sideTable=
    '<div style="width:228px;flex-shrink:0;margin-left:10px;background:rgba(255,255,255,0.02);'
      +'border-radius:6px;overflow:hidden;border:0.5px solid rgba(255,255,255,0.07);">'
    +'<table style="width:100%;border-collapse:collapse;">'
    +'<thead><tr style="border-bottom:1px solid rgba(255,255,255,0.08);">'
    +'<th style="padding:6px 8px;font-size:9px;font-weight:700;letter-spacing:0.07em;color:#374151;text-align:left;">BRAND</th>'
    +'<th style="padding:6px 8px;font-size:9px;font-weight:700;letter-spacing:0.07em;color:#374151;text-align:right;">'+sideColA+'</th>'
    +'<th style="padding:6px 8px;font-size:9px;font-weight:700;letter-spacing:0.07em;color:#374151;text-align:right;">'+sideColB+'</th>'
    +'</tr></thead>'
    +'<tbody>'+sideRows5+'</tbody>'
    +'</table>'
    +'<div style="padding:5px 8px;font-size:9px;color:#1e293b;border-top:0.5px solid rgba(255,255,255,0.04);">'
      +'NielsenIQ · 1-Tabela-1 · FYTD = Jul–Mar</div>'
    +'</div>';

  // Chart area (flex:1)
  var chartArea=
    '<div style="flex:1;min-width:0;padding-right:4px;">'
    +barRows
    +xAxis
    +'</div>';

  barsEl.innerHTML=chartArea+sideTable;

  // ── INSIGHT neon-bullet (rodapé esquerdo, estilo Odor Block) ──
  var insEl=document.getElementById('mso3-insight');
  if(insEl){
    insEl.style.cssText='padding:10px 16px;background:rgba(255,255,255,0.02);'
      +'border-radius:8px;border-left:3px solid rgba(34,197,94,0.35);'
      +'font-size:10px;color:#D1D5DB;line-height:1.8;margin-top:2px;';
    var ents5=brands.map(function(b){
      var v25=d25[b],v26=d26[b]; if(v25==null||v26==null) return null;
      return {b:b, dt:calcDelta5(v25,v26), cor:colors[b]||'#e2e8f0', v26:v26};
    }).filter(Boolean);
    if(!ents5.length){insEl.innerHTML=''; return;}
    var srt5=ents5.slice().sort(function(a,b){return b.dt.raw-a.dt.raw;});
    var ldr5=srt5[0], lag5=srt5[srt5.length-1];
    var mLbl5=isShare?'Tamanho do Mercado · $ Share':(isVal?'Tamanho do Mercado · Valor':'Tamanho do Mercado · Unidades');
    var mtDt=calcDelta5(mtV25,mtV26);
    var totalLine=mt
      ?'Total mercado: <strong style="color:#f1f5f9;">'+fmtV5(mtV26)+'</strong>'
        +' <span style="color:'+mtDt.col+';">'+(mtDt.up?'▲':'▼')+' '+mtDt.str+' vs FYTD25</span><br>':'';
    var ldrTxt=ldr5.dt.up
      ?'<strong style="color:'+ldr5.cor+';">'+ldr5.b+'</strong> lidera '
        +'<span style="color:#34d399;">▲ '+ldr5.dt.str+'</span> vs FYTD25'
      :'Todas as marcas recuam vs FYTD25';
    var lagTxt=(!lag5.dt.up&&lag5.b!==ldr5.b)
      ?' · <strong style="color:'+lag5.cor+';">'+lag5.b+'</strong> maior retração '
        +'<span style="color:#ef4444;">'+lag5.dt.str+'</span>':'';
    insEl.innerHTML=
      '<span style="display:inline-block;width:7px;height:7px;border-radius:50%;'
        +'background:#22c55e;box-shadow:0 0 6px #22c55e88;margin-right:7px;vertical-align:middle;"></span>'
      +'<strong style="font-size:10px;color:#22c55e;letter-spacing:0.06em;">Diagnóstico · '+mLbl5+'</strong>'
      +'<br>'
      +totalLine
      +ldrTxt+lagTxt+'.'
      +'<br><span style="font-size:9px;color:#1e293b;">Período: FYTD (Jul–Mar) · NielsenIQ · '+mkt+'</span>';
  }
}
/* ═══════════ END MSO3 ═══════════ */"""

assert OLD_BLOCK in html, "OLD_BLOCK nao encontrado no HTML"
html = html.replace(OLD_BLOCK, NEW_FUNC, 1)
print("renderMSO3() v5 substituida.")

with open(str(MAIN_FILE), "w", encoding="utf-8") as f:
    f.write(html)
print(f"Salvo ({len(html):,} chars).")

ts2 = datetime.now().strftime("%Y%m%d_%H%M")
ver = VERS_DIR / f"Dashboard_Farma_Sul_{ts2}_MSO3v5.html"
shutil.copy2(str(MAIN_FILE), str(ver))
print(f"Versao: {ver.name}")
print("DONE!")
