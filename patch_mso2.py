#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
patch_mso2.py
Replaces renderMSO2() and renderMSO2Insight() in the dashboard HTML file.
"""

import re
import shutil
import os
from datetime import datetime

HTML_PATH = r'C:\Users\valqu\OneDrive\Documentos\Claude\Projects\projeto Dashboard_farma_sul\Dashboard_farma_sul\Dashboard_Farma_Sul_20260512_2220.html'
VERSOES_DIR = r'C:\Users\valqu\OneDrive\Documentos\Claude\Projects\projeto Dashboard_farma_sul\Dashboard_farma_sul\versoes'

# ── NEW renderMSO2 ────────────────────────────────────────────────────────────
NEW_RENDERMSO2 = r"""function renderMSO2(){
  var sel = document.getElementById('mso2MarketSel') || document.getElementById('msoMarketSel');
  var mkt = sel ? sel.value : 'Farma Sul';
  var isShare = mso2Mode === 'share';
  var isVal   = mso2Mode === 'val';
  var isUn    = mso2Mode === 'un';

  // Destroy legacy charts
  if(mso2BarChart){ try{mso2BarChart.destroy();}catch(e){} mso2BarChart = null; }
  if(mso2LineChart){ try{mso2LineChart.destroy();}catch(e){} mso2LineChart = null; }

  // Update card labels
  var lbl = document.getElementById('mso2-mkt-lbl');
  if(lbl) lbl.textContent = mkt;
  var titleEl = document.getElementById('mso2-card-title');
  if(titleEl) titleEl.textContent = isShare ? 'MARKET SHARE — JAN · FEV · MAR'
    : (isVal ? 'VENDA VALOR — JAN · FEV · MAR' : 'UNIDADES — JAN · FEV · MAR');
  var subEl = document.getElementById('mso2-card-sub');
  if(subEl) subEl.innerHTML = (isShare ? 'Acum Jan–Mar/25 vs Jan–Mar/26'
    : (isVal ? 'R$ MM · Jan–Mar/26' : 'Unidades · Jan–Mar/26'))
    + ' · NielsenIQ · <span id="mso2-mkt-lbl">' + mkt + '</span>';
  var h2El = document.getElementById('mso2-card-h2');
  if(h2El) h2El.textContent = isShare ? '$ Share por Marca — 2025 vs 2026'
    : (isVal ? 'Venda R$ MM por Marca — 2025 vs 2026' : 'Volume Unidades por Marca — 2025 vs 2026');

  var brands = MSO_BRANDS;
  var colors = MSO_COLORS;

  /* BUILD VALUE SETS */
  var d25 = {}, d26 = {};
  var GrowthMode = false;

  if(isShare){
    var dS = MKTSHARE_OVERVIEW[mkt]; if(!dS) return;
    brands.forEach(function(b){
      var bd = dS[b]; if(!bd) return;
      var j25 = bd.jan25!=null?bd.jan25:bd.fytd25, f25 = bd.feb25!=null?bd.feb25:bd.fytd25, m25 = bd.mar25!=null?bd.mar25:bd.fytd25;
      var j26 = bd.monthly[6], f26 = bd.monthly[7], m26 = bd.monthly[8];
      d25[b] = {jan:j25, fev:f25, mar:m25, acum:Math.round((j25+f25+m25)/3*100)/100};
      d26[b] = {jan:j26, fev:f26, mar:m26, acum:Math.round((j26+f26+m26)/3*100)/100};
    });
  } else {
    var nbvS = (typeof NIELSEN_BRAND_VAL !== 'undefined') ? NIELSEN_BRAND_VAL[mkt] : null;
    if(!nbvS){ console.warn('No NIELSEN_BRAND_VAL for', mkt); return; }
    brands.forEach(function(b){
      var bd = nbvS[b]; if(!bd) return;
      var j26 = isVal?bd.jan_val:bd.jan_un, f26 = isVal?bd.fev_val:bd.fev_un, m26 = isVal?bd.mar_val:bd.mar_un;
      var fyt25 = isVal?bd.fytd25_val:bd.fytd25_un, fyt26 = isVal?bd.fytd26_val:bd.fytd26_un;
      var a26 = Math.round((j26+f26+m26)*100)/100;
      var hasExact25 = isVal ? (bd.jan25_val!==undefined) : (bd.jan25_un!==undefined);
      var j25, f25, m25, a25;
      if(hasExact25){
        j25 = isVal?bd.jan25_val:bd.jan25_un;
        f25 = isVal?bd.fev25_val:bd.fev25_un;
        m25 = isVal?bd.mar25_val:bd.mar25_un;
        a25 = Math.round((j25+f25+m25)*100)/100;
      } else {
        j25 = null; f25 = null; m25 = null;
        var ratio = fyt26>0 ? a26/fyt26 : 1/3;
        a25 = Math.round(fyt25*ratio*100)/100;
        GrowthMode = true;
      }
      d25[b] = {jan:j25, fev:f25, mar:m25, acum:a25, fytd25:fyt25, fytd26:fyt26, hasExact:hasExact25};
      d26[b] = {jan:j26, fev:f26, mar:m26, acum:a26};
    });
  }

  /* HELPERS */
  function fmtV(v){
    if(v===null||v===undefined) return '—';
    if(isShare) return v.toFixed(2)+'%';
    if(isVal) return v>=1?'R$'+v.toFixed(2)+'MM':'R$'+(v*1000).toFixed(0)+'K';
    return v>=1000?(Math.round(v/1000*10)/10)+'MM un':Math.round(v)+'K un';
  }
  function calcDelta(v25, v26){
    if(isShare){
      var dv = Math.round((v26-v25)*100)/100;
      return {str:(dv>=0?'+':'')+dv.toFixed(2)+'pp', col:dv>=0?'#34d399':'#ef4444', up:dv>=0, raw:dv};
    } else {
      var p = v25>0 ? Math.round((v26-v25)/v25*1000)/10 : 0;
      return {str:(p>=0?'+':'')+p.toFixed(1)+'%', col:p>=0?'#34d399':'#ef4444', up:p>=0, raw:p};
    }
  }

  /* MAX VALUE FOR BAR SCALING */
  var allV = [];
  brands.forEach(function(b){ if(d25[b]) allV.push(d25[b].acum); if(d26[b]) allV.push(d26[b].acum); });
  var maxV = Math.max.apply(null, allV) || 1;

  /* KPI CHIPS (mso2-headline) */
  var hdEl = document.getElementById('mso2-headline');
  if(hdEl){
    function kpiChip(borderColor, label, value, valueCss, sub, subCss){
      return '<div style="padding:14px 18px;background:#0D1117;border-top:3px solid '+borderColor+';">'
        +'<div style="font-size:9px;color:#64748b;font-weight:700;letter-spacing:.12em;text-transform:uppercase;margin-bottom:6px;">'+label+'</div>'
        +'<div style="font-size:24px;font-weight:900;'+valueCss+';line-height:1;">'+value+'</div>'
        +'<div style="font-size:10px;'+subCss+';margin-top:5px;">'+sub+'</div>'
        +'</div>';
    }
    if(isShare){
      var off26a = d26['OFF!']?d26['OFF!'].acum:0, exp26a = d26['EXPOSIS']?d26['EXPOSIS'].acum:0;
      var off25a = d25['OFF!']?d25['OFF!'].acum:0, exp25a = d25['EXPOSIS']?d25['EXPOSIS'].acum:0;
      var scj26h = Math.round((off26a+exp26a)*10)/10, scj25h = Math.round((off25a+exp25a)*10)/10;
      var scjDh = Math.round((scj26h-scj25h)*10)/10;
      var leaderB = brands.reduce(function(best,b){ return (d26[b]&&(!d26[best]||d26[b].acum>d26[best].acum))?b:best; }, brands[0]);
      var deltasKpi = brands.map(function(b){ return {b:b,raw:d26[b]&&d25[b]?Math.round((d26[b].acum-d25[b].acum)*100)/100:0}; });
      deltasKpi.sort(function(a,b){return b.raw-a.raw;});
      var topG = deltasKpi[0], topL = deltasKpi[deltasKpi.length-1];
      hdEl.innerHTML = '<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:1px;background:rgba(255,255,255,0.06);">'
        +kpiChip('#fbbf24','SCJ COMBINED',scj26h+'%','color:#fbbf24',(scjDh>=0?'↑ +':'↓ ')+Math.abs(scjDh).toFixed(1)+'pp vs /25','color:'+(scjDh>=0?'#34d399':'#ef4444'))
        +kpiChip(colors[leaderB]||'#e2e8f0','LÍDER DE SHARE',d26[leaderB]?d26[leaderB].acum.toFixed(2)+'%':'—','color:'+(colors[leaderB]||'#e2e8f0'),leaderB,'color:#94A3B8')
        +kpiChip('#34d399','MAIOR GANHO',(topG.raw>=0?'+':'')+topG.raw.toFixed(2)+'pp','color:#34d399',topG.b,'color:#94A3B8')
        +kpiChip('#ef4444','MAIOR QUEDA',topL.raw.toFixed(2)+'pp','color:#ef4444',topL.b,'color:#94A3B8')
        +'</div>';
    } else {
      var allDkpi = brands.map(function(b){
        var p25=d25[b],p26=d26[b]; if(!p25||!p26) return null;
        var delta=calcDelta(p25.acum,p26.acum);
        return {b:b,val26:p26.acum,val25:p25.acum,delta:delta};
      }).filter(Boolean);
      var totV26k=allDkpi.reduce(function(s,x){return s+x.val26;},0);
      var totV25k=allDkpi.reduce(function(s,x){return s+x.val25;},0);
      var totDk=calcDelta(totV25k,totV26k);
      allDkpi.sort(function(a,b){return b.val26-a.val26;});
      var topBk=allDkpi[0];
      var byDeltaKpi=allDkpi.slice().sort(function(a,b){return b.delta.raw-a.delta.raw;});
      var topGk=byDeltaKpi[0], topLk=byDeltaKpi[byDeltaKpi.length-1];
      hdEl.innerHTML = '<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:1px;background:rgba(255,255,255,0.06);">'
        +kpiChip(totDk.up?'#34d399':'#ef4444','TOTAL ACUM',fmtV(totV26k),'color:#f1f5f9',totDk.str+' vs /25','color:'+(totDk.up?'#34d399':'#ef4444'))
        +kpiChip(colors[topBk.b]||'#e2e8f0','MAIOR VOLUME',fmtV(topBk.val26),'color:'+(colors[topBk.b]||'#e2e8f0'),topBk.b,'color:#94A3B8')
        +kpiChip('#34d399','MAIOR CRESCIM.',topGk.delta.str,'color:#34d399',topGk.b,'color:#94A3B8')
        +kpiChip('#ef4444','MAIOR QUEDA',topLk.delta.str,'color:#ef4444',topLk.b,'color:#94A3B8')
        +'</div>';
    }
  }

  /* HORIZONTAL BARS + SHARE MOVERS */
  var barsEl = document.getElementById('mso2-bars');
  if(barsEl){
    var moversData = brands.map(function(b){
      var p25=d25[b],p26=d26[b]; if(!p25||!p26) return null;
      var delta=calcDelta(p25.acum,p26.acum);
      return {b:b,delta:delta,cor:colors[b]||'#e2e8f0'};
    }).filter(Boolean);
    var gainers=moversData.filter(function(x){return x.delta.raw>0;}).sort(function(a,b){return b.delta.raw-a.delta.raw;});
    var losers=moversData.filter(function(x){return x.delta.raw<0;}).sort(function(a,b){return a.delta.raw-b.delta.raw;});
    function moverRows(arr,clr){
      if(!arr.length) return '<div style="font-size:10px;color:#3d4451;padding:4px 0;">—</div>';
      return arr.map(function(x){
        return '<div style="display:flex;justify-content:space-between;align-items:center;padding:4px 0;border-bottom:0.5px solid rgba(255,255,255,0.04);">'
          +'<span style="font-size:10px;color:'+x.cor+';font-weight:700;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;max-width:108px;">'+x.b+'</span>'
          +'<span style="font-size:11px;font-weight:900;color:'+clr+';">'+x.delta.str+'</span>'
          +'</div>';
      }).join('');
    }
    var moversHTML = '<div style="width:190px;flex-shrink:0;background:#161B22;border-radius:10px;padding:12px 14px;align-self:flex-start;">'
      +'<div style="font-size:9px;font-weight:700;letter-spacing:.12em;color:#64748b;text-transform:uppercase;margin-bottom:10px;">SHARE MOVERS</div>'
      +(isShare
        ? '<div style="margin-bottom:10px;"><div style="font-size:9px;color:#34d399;font-weight:700;letter-spacing:.08em;margin-bottom:5px;">🟢 GANHOS</div>'+moverRows(gainers,'#34d399')+'</div>'
          +'<div><div style="font-size:9px;color:#ef4444;font-weight:700;letter-spacing:.08em;margin-bottom:5px;">🔴 PERDAS</div>'+moverRows(losers,'#ef4444')+'</div>'
        : '<div style="font-size:10px;color:#64748b;font-style:italic;line-height:1.5;">Disponível no<br>modo Share</div>')
      +'</div>';
    var barRows = brands.map(function(b){
      var p25=d25[b],p26=d26[b]; if(!p25||!p26) return '';
      var cor=colors[b]||'#e2e8f0';
      var delta=calcDelta(p25.acum,p26.acum);
      var w25=Math.max(2,Math.round(p25.acum/maxV*100));
      var w26=Math.max(2,Math.round(p26.acum/maxV*100));
      return '<div style="display:flex;align-items:center;margin-bottom:12px;">'
        +'<div style="width:150px;flex-shrink:0;padding-right:14px;">'
          +'<div style="display:flex;align-items:center;gap:6px;margin-bottom:4px;">'
            +'<span style="width:8px;height:8px;border-radius:50%;background:'+cor+';box-shadow:0 0 6px '+cor+'88;flex-shrink:0;"></span>'
            +'<span style="font-size:11px;font-weight:700;color:#e2e8f0;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">'+b+'</span>'
          +'</div>'
          +'<div style="font-size:10px;color:#475569;">2025 <span style="color:#64748b;">'+fmtV(p25.acum)+'</span></div>'
          +'<div style="font-size:10px;color:'+cor+';font-weight:700;">2026 '+fmtV(p26.acum)+'</div>'
        +'</div>'
        +'<div style="flex:1;min-width:0;">'
          +'<div style="margin-bottom:5px;">'
            +'<div style="height:10px;background:rgba(255,255,255,0.05);border-radius:5px;overflow:hidden;">'
              +'<div style="height:100%;width:'+w25+'%;background:#374151;border-radius:5px;transition:width .4s ease;"></div>'
            +'</div>'
          +'</div>'
          +'<div>'
            +'<div style="height:24px;background:rgba(255,255,255,0.04);border-radius:6px;overflow:hidden;">'
              +'<div style="height:100%;width:'+w26+'%;background:linear-gradient(90deg,'+cor+'bb,'+cor+');border-radius:6px;box-shadow:0 0 12px '+cor+'44;transition:width .4s ease;"></div>'
            +'</div>'
          +'</div>'
        +'</div>'
        +'<div style="width:86px;flex-shrink:0;text-align:right;padding-left:12px;">'
          +'<div style="font-size:15px;font-weight:900;color:'+delta.col+';line-height:1.1;">'+delta.str+'</div>'
          +'<div style="font-size:9px;color:#475569;margin-top:2px;">vs /25</div>'
        +'</div>'
        +'</div>';
    }).join('');
    barsEl.innerHTML = '<div style="display:flex;gap:16px;align-items:flex-start;">'
      +'<div style="flex:1;min-width:0;">'+barRows+'</div>'
      +moversHTML
      +'</div>';
  }

  /* HEATMAP TABLE */
  var tableEl = document.getElementById('mso2-table');
  var tblTitleEl = document.getElementById('mso2-table-title');
  if(tblTitleEl) tblTitleEl.style.display='none';
  if(tableEl){
    function heatCell(dpp){
      var abs=Math.abs(dpp);
      var alpha=isShare?Math.min(0.65,abs/4):Math.min(0.65,Math.abs(dpp)/30);
      var bg=dpp>=0?'rgba(52,211,153,'+alpha+')':'rgba(239,68,68,'+alpha+')';
      var txt=dpp>=0?'#6ee7b7':'#fca5a5';
      if(abs<(isShare?0.05:0.2)){bg='transparent';txt='#64748b';}
      var label=isShare?((dpp>=0?'+':'')+dpp.toFixed(2)+'pp'):((dpp>=0?'+':'')+dpp.toFixed(1)+'%');
      return '<td style="padding:8px 12px;text-align:center;font-size:11px;font-weight:700;color:'+txt+';background:'+bg+';border:0.5px solid rgba(255,255,255,0.04);">'+label+'</td>';
    }
    var months=[{k:'jan'},{k:'fev'},{k:'mar'}];
    var rows2=brands.map(function(b){
      var p25=d25[b],p26=d26[b]; if(!p25||!p26) return '';
      var cor=colors[b]||'#e2e8f0';
      var mCells=months.map(function(m){
        var v25=p25[m.k],v26=p26[m.k];
        if(v25===null||v25===undefined||v26===null||v26===undefined)
          return '<td style="padding:8px 12px;text-align:center;font-size:11px;color:#3d4451;border:0.5px solid rgba(255,255,255,0.04);">—</td>';
        var dv=isShare?Math.round((v26-v25)*100)/100:(v25>0?Math.round((v26-v25)/v25*1000)/10:0);
        return heatCell(dv);
      }).join('');
      var acumD=calcDelta(p25.acum,p26.acum);
      return '<tr>'
        +'<td style="padding:8px 12px;border:0.5px solid rgba(255,255,255,0.04);">'
          +'<span style="display:inline-block;width:7px;height:7px;border-radius:50%;background:'+cor+';margin-right:6px;vertical-align:middle;"></span>'
          +'<span style="font-size:10px;font-weight:700;color:'+cor+';">'+b+'</span>'
        +'</td>'
        +mCells
        +heatCell(acumD.raw)
        +'</tr>';
    }).join('');
    var thStyle='padding:8px 12px;font-size:9px;font-weight:700;letter-spacing:.1em;color:#64748b;text-transform:uppercase;background:#0D1117;border:0.5px solid rgba(255,255,255,0.04);';
    tableEl.innerHTML='<div style="background:#161B22;border-radius:10px;overflow:hidden;border:0.5px solid rgba(255,255,255,0.06);">'
      +'<table style="width:100%;border-collapse:collapse;">'
      +'<thead><tr>'
      +'<th style="'+thStyle+'text-align:left;">MARCA</th>'
      +'<th style="'+thStyle+'text-align:center;">JAN</th>'
      +'<th style="'+thStyle+'text-align:center;">FEV</th>'
      +'<th style="'+thStyle+'text-align:center;">MAR</th>'
      +'<th style="'+thStyle+'text-align:center;">ACUM</th>'
      +'</tr></thead><tbody>'+rows2+'</tbody></table>'
      +(GrowthMode?'<div style="padding:5px 12px;font-size:9px;color:#3d4451;">★ Acum Jan-Mar/25 estimado proporcionalmente.</div>':'')
      +'</div>';
  }

  renderMSO2Insight();
}"""

# ── NEW renderMSO2Insight ─────────────────────────────────────────────────────
NEW_RENDERMSO2INSIGHT = r"""function renderMSO2Insight(){
  var el = document.getElementById('mso2-insight');
  if(!el) return;
  var sel = document.getElementById('mso2MarketSel') || document.getElementById('msoMarketSel');
  var mkt = sel ? sel.value : 'Farma Sul';

  function col(v){ return v>=0?'#34d399':'#ef4444'; }
  function sig(v){ return v>=0?'+':''; }
  function arrowTrend(v){ return v>0.1?'↗ ':(v<-0.1?'↘ ':'→ '); }

  if(typeof mso2Mode === 'undefined' || mso2Mode === 'share'){
    var d = MKTSHARE_OVERVIEW[mkt]; if(!d) return;
    var off = d['OFF!'], exp = d['EXPOSIS'];
    if(!off||!exp) return;
    var oj25=off.jan25!=null?off.jan25:off.fytd25, of25=off.feb25!=null?off.feb25:off.fytd25, om25=off.mar25!=null?off.mar25:off.fytd25;
    var ej25=exp.jan25!=null?exp.jan25:exp.fytd25, ef25=exp.feb25!=null?exp.feb25:exp.fytd25, em25=exp.mar25!=null?exp.mar25:exp.fytd25;
    var oj26=off.monthly[6], of26=off.monthly[7], om26=off.monthly[8];
    var ej26=exp.monthly[6], ef26=exp.monthly[7], em26=exp.monthly[8];
    var offAcum25=Math.round((oj25+of25+om25)/3*100)/100, offAcum26=Math.round((oj26+of26+om26)/3*100)/100;
    var expAcum25=Math.round((ej25+ef25+em25)/3*100)/100, expAcum26=Math.round((ej26+ef26+em26)/3*100)/100;
    var scjA25=Math.round((offAcum25+expAcum25)*10)/10, scjA26=Math.round((offAcum26+expAcum26)*10)/10;
    var scjDA=Math.round((scjA26-scjA25)*10)/10;
    var allDeltas2 = MSO_BRANDS.map(function(b){
      var bd=d[b]; if(!bd) return null;
      var bj25=bd.jan25!=null?bd.jan25:bd.fytd25, bf25=bd.feb25!=null?bd.feb25:bd.fytd25, bm25=bd.mar25!=null?bd.mar25:bd.fytd25;
      var bj26=bd.monthly[6], bf26=bd.monthly[7], bm26=bd.monthly[8];
      var ba25=Math.round((bj25+bf25+bm25)/3*100)/100, ba26=Math.round((bj26+bf26+bm26)/3*100)/100;
      var da=Math.round((ba26-ba25)*100)/100;
      return {b:b,a25:ba25,a26:ba26,da:da,j26:bj26,f26:bf26,m26:bm26,cor:MSO_COLORS[b]||'#e2e8f0'};
    }).filter(Boolean);
    var lines=[];
    lines.push('<span style="color:#fbbf24;font-weight:700;font-size:10px;">★</span> '
      +'<strong style="color:#fbbf24;">SCJ Combined</strong> (OFF!+EXPOSIS): '
      +'Acum Jan-Mar/26 <strong style="color:#fbbf24;">'+scjA26+'%</strong> '
      +'<span style="color:'+col(scjDA)+';font-weight:700;">'+(scjDA>=0?'↑ +':'↓ ')+Math.abs(scjDA).toFixed(1)+'pp vs /25</span>');
    allDeltas2.forEach(function(x){
      var trend=arrowTrend(x.da);
      var monthStr='Jan: <strong style="color:'+x.cor+';">'+x.j26+'%</strong>'
        +' · Fev: <strong style="color:'+x.cor+';">'+x.f26+'%</strong>'
        +' · Mar: <strong style="color:'+x.cor+';">'+x.m26+'%</strong>';
      lines.push('<span style="color:'+col(x.da)+';font-weight:700;font-size:10px;">'+trend+'</span>'
        +'<strong style="color:'+x.cor+';">'+x.b+'</strong>'
        +' Acum/26 <strong style="color:'+x.cor+';">'+x.a26.toFixed(2)+'%</strong>'
        +' <span style="color:'+col(x.da)+';"> ('+sig(x.da)+x.da.toFixed(2)+'pp)</span>'
        +' · '+monthStr);
    });
    el.innerHTML='<div style="background:#161B22;border-radius:10px;border-left:3px solid rgba(251,191,36,0.6);padding:14px 16px;">'
      +'<div style="font-size:9px;font-weight:700;letter-spacing:.14em;color:#fbbf24;text-transform:uppercase;margin-bottom:9px;">📊 DIAGNÓSTICO · '+mkt+' · Jan–Mar/26</div>'
      +'<div style="font-size:11px;color:#D1D5DB;line-height:1.9;">'
      +lines.join('<br>')
      +'</div></div>';
    return;
  }

  /* R$ MM / UNIDADES MODE */
  var nbvI = (typeof NIELSEN_BRAND_VAL !== 'undefined') ? NIELSEN_BRAND_VAL[mkt] : null;
  if(!nbvI) return;
  var isValI = mso2Mode === 'val';
  function fmtNI(v){ if(isValI) return v>=1?'R$'+v.toFixed(2)+'MM':'R$'+(v*1000).toFixed(0)+'K'; return Math.round(v).toLocaleString('pt-BR')+'K'; }
  function pctI(v26,v25){ return v25>0?Math.round((v26-v25)/v25*1000)/10:0; }
  var lines2 = MSO_BRANDS.map(function(b){
    var bd=nbvI[b]; if(!bd) return '';
    var cor=MSO_COLORS[b]||'#e2e8f0';
    var f25=isValI?bd.fytd25_val:bd.fytd25_un, f26=isValI?bd.fytd26_val:bd.fytd26_un;
    var j26=isValI?bd.jan_val:bd.jan_un, fv26=isValI?bd.fev_val:bd.fev_un, m26=isValI?bd.mar_val:bd.mar_un;
    var p=pctI(f26,f25);
    var cc=p>=0?'#34d399':'#ef4444';
    var trend=p>2?'↗ ':(p<-2?'↘ ':'→ ');
    return '<span style="color:'+cc+';font-weight:700;font-size:10px;">'+trend+'</span>'
      +'<strong style="color:'+cor+';">'+b+'</strong>'
      +' Jan: <strong style="color:'+cor+';">'+fmtNI(j26)+'</strong>'
      +' · Fev: <strong style="color:'+cor+';">'+fmtNI(fv26)+'</strong>'
      +' · Mar: <strong style="color:'+cor+';">'+fmtNI(m26)+'</strong>'
      +' <span style="color:'+cc+';font-weight:700;">'+(p>=0?'▲ +':'▼ ')+Math.abs(p).toFixed(1)+'%</span>';
  }).filter(Boolean);
  el.innerHTML='<div style="background:#161B22;border-radius:10px;border-left:3px solid rgba(251,191,36,0.6);padding:14px 16px;">'
    +'<div style="font-size:9px;font-weight:700;letter-spacing:.14em;color:#fbbf24;text-transform:uppercase;margin-bottom:9px;">📊 DIAGNÓSTICO · '+mkt+' · '+(isValI?'R$ MM':'Unidades')+' Jan–Mar/26</div>'
    +'<div style="font-size:11px;color:#D1D5DB;line-height:1.9;">'
    +lines2.join('<br>')
    +'</div></div>';
}"""


def main():
    print("Reading file...")
    with open(HTML_PATH, 'r', encoding='utf-8') as f:
        content = f.read()
    original_size = len(content)
    print(f"File size: {original_size:,} bytes")

    # ── BACKUP ────────────────────────────────────────────────────────────────
    ts = datetime.now().strftime('%Y%m%d_%H%M')
    backup_name = f'Dashboard_Farma_Sul_{ts}.html'
    backup_path = os.path.join(VERSOES_DIR, backup_name)
    os.makedirs(VERSOES_DIR, exist_ok=True)
    shutil.copy2(HTML_PATH, backup_path)
    print(f"Backup created: {backup_path}")

    # ── REPLACE renderMSO2 ────────────────────────────────────────────────────
    ANCHOR1 = '\n\n/* ═══════════ MSO ÁREA ═══════════ */'
    pat1 = re.compile(r'function renderMSO2\(\)\{.*?(?=\n\n/\* ═{11} MSO ÁREA ═{11} \*/)', re.DOTALL)
    match1 = pat1.search(content)
    if not match1:
        print("ERROR: Could not find renderMSO2 block!")
        return False
    print(f"renderMSO2 found at pos {match1.start()} to {match1.end()}")
    content = pat1.sub(NEW_RENDERMSO2, content, count=1)

    # ── REPLACE renderMSO2Insight ─────────────────────────────────────────────
    pat2 = re.compile(r'function renderMSO2Insight\(\)\{.*?(?=\n\nconst FYTD_MARKET_TOTAL)', re.DOTALL)
    match2 = pat2.search(content)
    if not match2:
        print("ERROR: Could not find renderMSO2Insight block!")
        return False
    print(f"renderMSO2Insight found at pos {match2.start()} to {match2.end()}")
    content = pat2.sub(NEW_RENDERMSO2INSIGHT, content, count=1)

    # ── WRITE BACK ────────────────────────────────────────────────────────────
    with open(HTML_PATH, 'w', encoding='utf-8') as f:
        f.write(content)
    new_size = len(content)
    print(f"File written: {new_size:,} bytes (delta: {new_size - original_size:+,})")

    # ── EXPORT TO DOWNLOADS ───────────────────────────────────────────────────
    downloads_path = os.path.expanduser(fr'~\Downloads\Dashboard_FarmaSul_Giovano_{ts}.html')
    shutil.copy2(HTML_PATH, downloads_path)
    print(f"Copy exported to: {downloads_path}")

    return True


if __name__ == '__main__':
    ok = main()
    print("DONE - SUCCESS" if ok else "DONE - FAILED")
