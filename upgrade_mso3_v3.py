#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
upgrade_mso3_v3.py — MSO3 Visual Redesign
Mudancas:
  1. Mini-barra de progresso no header de Mercado Total
  2. Barras sobrepostas (FY25 cinza atras + FY26 colorida na frente, mesmo track)
  3. Layout horizontal: uma linha por marca (brand dot | nome | barra dupla | delta | valor)
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
bk = VERS_DIR / f"Dashboard_Farma_Sul_{ts}_PreMSO3v3.html"
shutil.copy2(str(MAIN_FILE), str(bk))
print(f"Backup: {bk.name}")

with open(str(MAIN_FILE), encoding="utf-8") as f:
    html = f.read()

# ── 2. Nova funcao renderMSO3 ──────────────────────────────────────────────────
OLD_START = "function renderMSO3(){"
OLD_END   = "/* ═══════════ END MSO3 ═══════════ */"
assert OLD_START in html and OLD_END in html

start_idx = html.index(OLD_START)
end_idx   = html.index(OLD_END) + len(OLD_END)
OLD_BLOCK = html[start_idx:end_idx]

NEW_FUNC = r"""function renderMSO3(){
  var sel = document.getElementById('mso3MarketSel');
  var mkt = sel ? sel.value : 'T.BR Farma';
  var isShare = mso3Mode === 'share';
  var isVal   = mso3Mode === 'val';
  var isUn    = mso3Mode === 'un';

  var brands = MSO_BRANDS;
  var colors = MSO_COLORS;

  // ── Labels ──
  var lblEl = document.getElementById('mso3-mkt-lbl');
  if(lblEl) lblEl.textContent = mkt;
  var titleEl = document.getElementById('mso3-card-title');
  if(titleEl) titleEl.textContent = isShare ? 'VISAO FISCAL FYTD · JUL–MAR'
    : (isVal ? 'VENDA VALOR FYTD · JUL–MAR' : 'UNIDADES FYTD · JUL–MAR');
  var h2El = document.getElementById('mso3-card-h2');
  if(h2El) h2El.textContent = isShare ? '$ Share por Marca — FYTD 2025 vs 2026'
    : (isVal ? 'Venda R$ MM por Marca — FYTD 2025 vs 2026' : 'Volume Unidades por Marca — FYTD 2025 vs 2026');
  var subEl = document.getElementById('mso3-card-sub');
  if(subEl) subEl.innerHTML = (isShare ? 'FYTD Share Jul-Mar/25 vs /26'
    : (isVal ? 'R$ MM · FYTD Jul-Mar/26' : 'Unidades · FYTD Jul-Mar/26'))
    + ' · OFF! · EXPOSIS · XO INSETO · SUPER REPELEX · SBP · <span id="mso3-mkt-lbl">' + mkt + '</span>';
  var tblTitleEl = document.getElementById('mso3-table-title');
  if(tblTitleEl) tblTitleEl.textContent = isShare
    ? 'VARIACAO FYTD YoY (pp) — JUL–MAR'
    : 'PERFORMANCE FYTD — JUL–MAR';

  // ── Helpers ──
  function fmtV3(v, compact){
    if(v===null||v===undefined) return '—';
    if(isShare) return v.toFixed(2)+'%';
    if(isVal){
      if(compact){
        if(v>=100) return 'R$'+Math.round(v)+'MM';
        if(v>=10)  return 'R$'+v.toFixed(1)+'MM';
        if(v>=1)   return 'R$'+v.toFixed(2)+'MM';
        return 'R$'+(v*1000).toFixed(0)+'K';
      }
      if(v>=100) return 'R$'+v.toFixed(1)+'MM';
      if(v>=1)   return 'R$'+v.toFixed(2)+'MM';
      return 'R$'+(v*1000).toFixed(0)+'K';
    }
    // unidades
    if(compact){
      if(v>=10000) return Math.round(v/1000)+'MMun';
      if(v>=1000)  return (v/1000).toFixed(1)+'MMun';
      return Math.round(v)+'K';
    }
    return v>=1000?(Math.round(v/1000*10)/10)+'MM un':Math.round(v)+'K un';
  }
  function calcDelta3(v25, v26){
    if(isShare){
      var d = Math.round((v26-v25)*100)/100;
      return {str:(d>=0?'+':'')+d.toFixed(2)+'pp', col:d>=0?'#34d399':'#ef4444', up:d>=0};
    } else {
      var p = v25>0 ? Math.round((v26-v25)/v25*1000)/10 : 0;
      return {str:(p>=0?'+':'')+p.toFixed(1)+'%', col:p>=0?'#34d399':'#ef4444', up:p>=0};
    }
  }

  // ── MERCADO TOTAL — header com mini-barra ──
  var mktTotalEl = document.getElementById('mso3-market-total');
  if(mktTotalEl){
    var mt = (typeof FYTD_MARKET_TOTAL !== 'undefined') ? FYTD_MARKET_TOTAL[mkt] : null;
    if(mt){
      var mtV25 = isVal ? mt.fytd25_val : (isUn ? mt.fytd25_un : mt.fytd25_val);
      var mtV26 = isVal ? mt.fytd26_val : (isUn ? mt.fytd26_un : mt.fytd26_val);
      var mtCres = mtV25>0 ? Math.round((mtV26/mtV25-1)*1000)/10 : 0;
      var mtCol = mtCres>=0?'#34d399':'#ef4444';
      var mtArr = mtCres>=0?'▲ +':'▼ ';
      // mini-barra: max = maior dos dois
      var mtMax = Math.max(mtV25, mtV26);
      var w25m = Math.max(2, Math.round(mtV25/mtMax*100));
      var w26m = Math.max(2, Math.round(mtV26/mtMax*100));
      mktTotalEl.style.display = '';
      mktTotalEl.innerHTML =
        // Label
        '<span style="font-size:9px;font-weight:700;letter-spacing:0.08em;color:#22c55e;">🌎 PERSONAL REPELLENT · MERCADO TOTAL</span>'
        + '&nbsp;&nbsp;&nbsp;'
        // Mini barra dupla
        + '<span style="display:inline-block;vertical-align:middle;width:90px;height:8px;border-radius:4px;background:rgba(255,255,255,0.06);position:relative;">'
        +   '<span style="position:absolute;left:0;top:0;bottom:0;width:'+w25m+'%;background:rgba(100,116,139,0.35);border-radius:4px;"></span>'
        +   '<span style="position:absolute;left:0;top:1px;bottom:1px;width:'+w26m+'%;background:linear-gradient(90deg,#22c55e44,#22c55ecc);border-radius:3px;"></span>'
        + '</span>'
        + '&nbsp;&nbsp;'
        // Valores
        + '<span style="color:#4a5568;font-size:10px;">FYTD25: '+fmtV3(mtV25)+'</span>'
        + '&nbsp;&nbsp;'
        + '<span style="color:#e2e8f0;font-size:10px;font-weight:700;">FYTD26: '+fmtV3(mtV26)+'</span>'
        + '&nbsp;&nbsp;'
        + '<span style="color:'+mtCol+';font-size:12px;font-weight:800;">'+mtArr+Math.abs(mtCres).toFixed(1)+'%</span>'
        + '<span style="color:#2d3748;font-size:9px;margin-left:8px;">vs FYTD25 (NielsenIQ)</span>';
    } else {
      mktTotalEl.style.display = 'none';
    }
  }

  // ── BUILD VALUE SETS ──
  var d25 = {}, d26 = {};
  if(isShare){
    var dS = (typeof MKTSHARE_OVERVIEW !== 'undefined') ? MKTSHARE_OVERVIEW[mkt] : null;
    if(!dS){ document.getElementById('mso3-headline').innerHTML='<span style="color:#64748b;">Dados não disponíveis.</span>'; return; }
    brands.forEach(function(b){ var bd=dS[b]; if(!bd) return; d25[b]=bd.fytd25||0; d26[b]=bd.fytd26||0; });
  } else {
    var nfv = (typeof NIELSEN_FYTD_VAL !== 'undefined') ? NIELSEN_FYTD_VAL[mkt] : null;
    if(!nfv){ document.getElementById('mso3-headline').innerHTML='<span style="color:#64748b;">Dados FYTD não disponíveis.</span>'; return; }
    brands.forEach(function(b){ var bd=nfv[b]; if(!bd) return; d25[b]=isVal?bd.fytd25_val:bd.fytd25_un; d26[b]=isVal?bd.fytd26_val:bd.fytd26_un; });
  }

  // ── HEADLINE ──
  var hdEl3 = document.getElementById('mso3-headline');
  if(hdEl3){
    var parts3 = brands.map(function(b){
      var v25h=d25[b], v26h=d26[b]; if(v25h===undefined) return '';
      var dt3=calcDelta3(v25h,v26h);
      return '<span style="color:'+colors[b]+';font-weight:700;">'+b+'</span>'
        +' <span style="color:'+dt3.col+';font-weight:700;">'+(dt3.up?'▲ ':'▼ ')+dt3.str+'</span>';
    }).filter(Boolean);
    var uLbl = isShare?'Share FYTD YoY':(isVal?'R$ MM FYTD YoY':'Unidades FYTD YoY');
    hdEl3.innerHTML = '<strong style="color:#e2e8f0;">'+mkt+'</strong>'
      +' · <span style="font-size:11px;color:#94A3B8;">'+uLbl+':</span> '
      +parts3.join('&nbsp;&nbsp;·&nbsp;&nbsp;');
  }

  // ── MAX VALUE FOR SCALING ──
  var allV3=[]; brands.forEach(function(b){ if(d25[b]!=null) allV3.push(d25[b]); if(d26[b]!=null) allV3.push(d26[b]); });
  var maxV3 = Math.max.apply(null,allV3)||1;

  // ── BARRAS SOBREPOSTAS (novo design) ──
  // Layout por marca: uma linha com barra dupla sobreposta + delta + valor
  var barsEl3 = document.getElementById('mso3-bars');
  if(barsEl3){
    // Mudar para 1 coluna para aproveitar largura total da barra
    barsEl3.style.gridTemplateColumns = '1fr';
    barsEl3.innerHTML = brands.map(function(b){
      var v25=d25[b], v26=d26[b]; if(v25==null||v26==null) return '';
      var cor=colors[b]||'#e2e8f0';
      var dt3=calcDelta3(v25,v26);
      var w25=Math.max(2, Math.round(v25/maxV3*82));
      var w26=Math.max(2, Math.round(v26/maxV3*82));
      var arrow3=dt3.up?'↑':'↓';

      var tipRows3=''
        +'<div class="mso2-tip-row"><span class="mso2-tip-lbl">FYTD25 (Jul-Mar/25)</span><span class="mso2-tip-val">'+fmtV3(v25)+'</span></div>'
        +'<div class="mso2-tip-row"><span class="mso2-tip-lbl">FYTD26 (Jul-Mar/26)</span><span style="color:'+cor+';font-weight:700;">'+fmtV3(v26)+'</span></div>'
        +'<div style="height:1px;background:rgba(255,255,255,0.07);margin:5px 0;"></div>'
        +'<div class="mso2-tip-row"><span class="mso2-tip-lbl">Δ FYTD YoY</span><span style="font-weight:700;color:'+dt3.col+';">'+arrow3+' '+dt3.str+'</span></div>';

      // Barra sobreposta: track unico com FY25 atras e FY26 na frente
      return '<div class="mso2-br" style="padding:9px 14px;">'
        // Linha principal: dot + nome + barra dupla + delta + valor
        +'<div style="display:flex;align-items:center;gap:8px;">'
        // Dot colorido
        +'<span style="display:inline-block;width:8px;height:8px;border-radius:50%;background:'+cor+';box-shadow:0 0 6px '+cor+'88;flex-shrink:0;"></span>'
        // Nome marca
        +'<span style="font-size:11px;font-weight:700;color:#e2e8f0;min-width:90px;letter-spacing:0.02em;">'+b+'</span>'
        // Container barra dupla sobreposta (flex:1)
        +'<div style="flex:1;position:relative;height:12px;border-radius:6px;background:rgba(255,255,255,0.05);">'
        //   FY25 — cinza atras (camada inferior)
        +'<div style="position:absolute;left:0;top:0;bottom:0;width:'+w25+'%;background:rgba(100,116,139,0.28);border-radius:6px;"></div>'
        //   FY26 — colorido na frente (camada superior, ligeiramente menor em altura)
        +'<div style="position:absolute;left:0;top:2px;bottom:2px;width:'+w26+'%;'
        +'background:linear-gradient(90deg,'+cor+'44,'+cor+'cc);'
        +'border-radius:4px;box-shadow:0 0 8px '+cor+'33;'
        +'border-right:2px solid '+cor+';"></div>'
        // Linha separadora FY25 (se FY26 > FY25, marca onde era o FY25)
        +(w26>w25?'<div style="position:absolute;left:'+w25+'%;top:0;bottom:0;width:1.5px;background:'+cor+'55;transform:translateX(-1px);border-radius:1px;"></div>':'')
        +'</div>'
        // Delta colorido
        +'<span style="font-size:10px;font-weight:800;color:'+dt3.col+';min-width:52px;text-align:right;white-space:nowrap;">'+arrow3+' '+dt3.str+'</span>'
        // Valor FY26
        +'<span style="font-size:11px;font-weight:700;color:'+cor+';min-width:68px;text-align:right;white-space:nowrap;">'+fmtV3(v26,true)+'</span>'
        +'</div>'
        // Sub-linha: FY25 valor (pequeno, muted)
        +'<div style="display:flex;align-items:center;padding-left:16px;margin-top:3px;gap:8px;">'
        +'<div style="min-width:90px;"></div>'
        +'<div style="flex:1;"></div>'
        +'<span style="font-size:9px;color:#374151;min-width:52px;text-align:right;"></span>'
        +'<span style="font-size:9px;color:#374151;min-width:68px;text-align:right;">FY25: '+fmtV3(v25,true)+'</span>'
        +'</div>'
        // Tooltip
        +'<div class="mso2-tooltip">'
        +'<div style="font-size:10px;font-weight:700;color:'+cor+';margin-bottom:6px;letter-spacing:0.05em;border-bottom:0.5px solid rgba(255,255,255,0.08);padding-bottom:5px;">'+b+'</div>'
        +tipRows3
        +'</div>'
        +'</div>';
    }).join('');
  }

  // ── TABELA ──
  var tableEl3=document.getElementById('mso3-table');
  if(tableEl3){
    var hds3=isShare
      ?['MARCA','FYTD25 (%)','FYTD26 (%)','&#916; FYTD YoY (pp)']
      :['MARCA','FYTD25','FYTD26','&#916; FYTD YoY'];
    var rows3=brands.map(function(b){
      var v25=d25[b],v26=d26[b]; if(v25==null||v26==null) return '';
      var cor=colors[b]||'#e2e8f0'; var dt3=calcDelta3(v25,v26); var arr3=dt3.up?'↑':'↓';
      return '<tr>'
        +'<td class="mso2-tc"><span style="display:inline-flex;align-items:center;gap:6px;">'
        +'<span style="width:7px;height:7px;border-radius:50%;background:'+cor+';display:inline-block;box-shadow:0 0 4px '+cor+'77;"></span>'
        +'<span style="color:'+cor+';font-weight:700;font-size:10px;">'+b+'</span></span></td>'
        +'<td class="mso2-tc" style="color:#4a5568;">'+fmtV3(v25)+'</td>'
        +'<td class="mso2-tc" style="color:'+cor+';font-weight:700;">'+fmtV3(v26)+'</td>'
        +'<td class="mso2-tc" style="color:'+dt3.col+';font-weight:700;">'+arr3+' '+dt3.str+'</td>'
        +'</tr>';
    }).join('');
    // Linha total mercado
    var mt3=(typeof FYTD_MARKET_TOTAL!=='undefined')?FYTD_MARKET_TOTAL[mkt]:null;
    var totalRow3='';
    if(mt3&&!isShare){
      var mtV25t=isVal?mt3.fytd25_val:mt3.fytd25_un, mtV26t=isVal?mt3.fytd26_val:mt3.fytd26_un;
      var mtDt=calcDelta3(mtV25t,mtV26t); var mtArr=mtDt.up?'↑':'↓';
      totalRow3='<tr style="border-top:1px solid rgba(34,197,94,0.2);background:rgba(34,197,94,0.03);">'
        +'<td class="mso2-tc"><span style="color:#22c55e;font-weight:700;font-size:10px;letter-spacing:0.02em;">🌎 TOTAL PR</span></td>'
        +'<td class="mso2-tc" style="color:#4a5568;">'+fmtV3(mtV25t)+'</td>'
        +'<td class="mso2-tc" style="color:#22c55e;font-weight:700;">'+fmtV3(mtV26t)+'</td>'
        +'<td class="mso2-tc" style="color:'+mtDt.col+';font-weight:700;">'+mtArr+' '+mtDt.str+'</td>'
        +'</tr>';
    }
    tableEl3.innerHTML='<table class="mso2-tbl"><thead><tr>'
      +hds3.map(function(h,i){ return '<th class="mso2-th"'+(i===0?' style="text-align:left;"':'')+'>'+h+'</th>'; }).join('')
      +'</tr></thead><tbody>'+rows3+totalRow3+'</tbody></table>';
  }

  // ── INSIGHT ──
  var insEl3=document.getElementById('mso3-insight');
  if(insEl3){
    var ents3=brands.map(function(b){
      var v25=d25[b],v26=d26[b]; if(v25==null||v26==null) return null;
      return {b:b, dt:calcDelta3(v25,v26), cor:colors[b]||'#e2e8f0', v26:v26};
    }).filter(Boolean);
    if(ents3.length){
      var srt3=ents3.slice().sort(function(a,b){ return parseFloat(b.dt.str)-parseFloat(a.dt.str); });
      var ldr3=srt3[0], lag3=srt3[srt3.length-1];
      var mLbl=isShare?'share':(isVal?'receita':'volume');
      var lines3=ents3.map(function(e){
        var arr=e.dt.up?'▲ ':'▼ ';
        return '• <strong style="color:'+e.cor+';">'+e.b+'</strong>: FYTD26 = <strong style="color:#e2e8f0;">'+fmtV3(e.v26)+'</strong>'
          +' <span style="color:'+e.dt.col+';">('+arr+e.dt.str+' vs FYTD25)</span>';
      });
      var diag3=ldr3.dt.up
        ?'🚀 <strong style="color:'+ldr3.cor+';">'+ldr3.b+'</strong> lidera crescimento FYTD em <strong style="color:#e2e8f0;">'+mkt+'</strong>.'
        :'⚠️ Todas as marcas recuam no FYTD em '+mkt+'.';
      if(!lag3.dt.up && lag3.b!==ldr3.b)
        diag3+=' <span style="color:#64748b;">·</span> <strong style="color:'+lag3.cor+';">'+lag3.b+'</strong> maior retração ('+lag3.dt.str+').';
      insEl3.innerHTML='<strong style="color:#22c55e;font-size:10px;letter-spacing:0.08em;">📊 DIAGNÓSTICO FYTD — '+mkt+'&nbsp;&nbsp;·&nbsp;&nbsp;'+mLbl.toUpperCase()+'</strong><br>'
        +lines3.join('<br>')+'<br>'+diag3;
    }
  }
}
/* ═══════════ END MSO3 ═══════════ */"""

assert OLD_BLOCK in html
html = html.replace(OLD_BLOCK, NEW_FUNC, 1)
print("renderMSO3() v3 substituida.")

with open(str(MAIN_FILE), "w", encoding="utf-8") as f:
    f.write(html)
print(f"Salvo ({len(html):,} chars).")

ts2 = datetime.now().strftime("%Y%m%d_%H%M")
ver = VERS_DIR / f"Dashboard_Farma_Sul_{ts2}_MSO3v3.html"
shutil.copy2(str(MAIN_FILE), str(ver))
print(f"Versao: {ver.name}")
print("DONE!")
