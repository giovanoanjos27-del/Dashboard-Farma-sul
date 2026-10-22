#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
upgrade_mso3_v4.py — MSO3 Compactação Total + Barras Diagonais
Mudancas vs v3:
  1. Grid 2 colunas (repeat(2,1fr)) — altura total cai pela metade
  2. Header compacto: título + Mercado Total em uma faixa única horizontal
  3. Barras diagonais 45° (repeating-linear-gradient) no FY26 — identidade fiscal
  4. FY25 = apenas linha fina / contorno cinza
  5. Altura das barras: 8px
  6. Sub-label FY25 removido (ganho vertical)
  7. Nome da marca: 65px (mais compacto)
  8. Tabela: font 11px, apenas ▲/▼ + valores, rodapé NielsenIQ discreto
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
bk = VERS_DIR / f"Dashboard_Farma_Sul_{ts}_PreMSO3v4.html"
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
  var sel = document.getElementById('mso3MarketSel');
  var mkt = sel ? sel.value : 'T.BR Farma';
  var isShare = mso3Mode === 'share';
  var isVal   = mso3Mode === 'val';
  var isUn    = mso3Mode === 'un';

  var brands = MSO_BRANDS;
  var colors = MSO_COLORS;

  // ── Labels de topo ──
  var titleEl = document.getElementById('mso3-card-title');
  if(titleEl) titleEl.textContent = isShare ? 'VISAO FISCAL FYTD · JUL–MAR'
    : (isVal ? 'VENDA VALOR FYTD · JUL–MAR' : 'UNIDADES FYTD · JUL–MAR');
  var h2El = document.getElementById('mso3-card-h2');
  if(h2El) h2El.textContent = '';  // suprimido — fundido no header compacto
  var subEl = document.getElementById('mso3-card-sub');
  if(subEl) subEl.innerHTML =
    (isShare ? 'FYTD $ Share Jul-Mar/25 vs /26'
             : (isVal ? 'R$ MM · FYTD Jul-Mar' : 'Unidades · FYTD Jul-Mar'))
    + ' · <span id="mso3-mkt-lbl">' + mkt + '</span>';
  var tblTitleEl = document.getElementById('mso3-table-title');
  if(tblTitleEl) tblTitleEl.textContent = isShare
    ? 'VARIACAO FYTD YoY (pp) — JUL–MAR'
    : 'PERFORMANCE FYTD — JUL–MAR';

  // ── Helpers ──
  function fmtV4(v, compact){
    if(v===null||v===undefined) return '—';
    if(isShare) return v.toFixed(2)+'%';
    if(isVal){
      if(compact){
        if(v>=100) return 'R$'+Math.round(v)+'mm';
        if(v>=10)  return 'R$'+v.toFixed(1)+'mm';
        if(v>=1)   return 'R$'+v.toFixed(2)+'mm';
        return 'R$'+(v*1000).toFixed(0)+'k';
      }
      if(v>=100) return 'R$'+v.toFixed(1)+'MM';
      if(v>=1)   return 'R$'+v.toFixed(2)+'MM';
      return 'R$'+(v*1000).toFixed(0)+'K';
    }
    if(compact){
      if(v>=10000) return Math.round(v/1000)+'mMun';
      if(v>=1000)  return (v/1000).toFixed(1)+'mMun';
      return Math.round(v)+'k';
    }
    return v>=1000?(Math.round(v/1000*10)/10)+'MM un':Math.round(v)+'K un';
  }
  function calcDelta4(v25, v26){
    if(isShare){
      var d = Math.round((v26-v25)*100)/100;
      return {str:(d>=0?'+':'')+d.toFixed(2)+'pp', col:d>=0?'#34d399':'#ef4444', up:d>=0, raw:d};
    } else {
      var p = v25>0 ? Math.round((v26-v25)/v25*1000)/10 : 0;
      return {str:(p>=0?'+':'')+p.toFixed(1)+'%', col:p>=0?'#34d399':'#ef4444', up:p>=0, raw:p};
    }
  }

  // ── HEADER COMPACTO — funde título + Mercado Total em 1 faixa ──
  var mktTotalEl = document.getElementById('mso3-market-total');
  if(mktTotalEl){
    var mt = (typeof FYTD_MARKET_TOTAL !== 'undefined') ? FYTD_MARKET_TOTAL[mkt] : null;
    if(mt){
      var mtV25 = isUn ? mt.fytd25_un : mt.fytd25_val;
      var mtV26 = isUn ? mt.fytd26_un : mt.fytd26_val;
      var mtCres = mtV25>0 ? Math.round((mtV26/mtV25-1)*1000)/10 : 0;
      var mtCol = mtCres>=0?'#34d399':'#ef4444';
      var mtArr = mtCres>=0?'▲ +':'▼ ';
      // Mini-barra 70px × 6px
      var mtMax = Math.max(mtV25, mtV26);
      var w25m = Math.max(2, Math.round(mtV25/mtMax*100));
      var w26m = Math.max(2, Math.round(mtV26/mtMax*100));
      mktTotalEl.style.display = '';
      mktTotalEl.style.padding = '5px 14px';
      mktTotalEl.style.borderRadius = '6px';
      mktTotalEl.style.marginBottom = '6px';
      mktTotalEl.style.display = 'flex';
      mktTotalEl.style.alignItems = 'center';
      mktTotalEl.style.gap = '10px';
      mktTotalEl.style.background = 'rgba(34,197,94,0.06)';
      mktTotalEl.style.border = '0.5px solid rgba(34,197,94,0.22)';
      mktTotalEl.innerHTML =
        // Separador vertical
        '<span style="color:rgba(34,197,94,0.4);font-size:14px;line-height:1;">|</span>'
        // Label curto
        + '<span style="font-size:9px;font-weight:800;letter-spacing:0.09em;color:#22c55e;white-space:nowrap;">🌎 TOTAL MERCADO</span>'
        // Mini-barra
        + '<span style="display:inline-block;vertical-align:middle;width:70px;height:6px;'
        +   'border-radius:3px;background:rgba(255,255,255,0.05);position:relative;flex-shrink:0;">'
        +   '<span style="position:absolute;left:0;top:0;bottom:0;width:'+w25m+'%;'
        +     'background:rgba(100,116,139,0.30);border-radius:3px;"></span>'
        +   '<span style="position:absolute;left:0;top:1px;bottom:1px;width:'+w26m+'%;'
        +     'background:linear-gradient(90deg,#22c55e55,#22c55ecc);border-radius:2px;"></span>'
        + '</span>'
        // FYTD25 apagado
        + '<span style="color:#374151;font-size:10px;white-space:nowrap;">'
        +   fmtV4(mtV25,true)+'</span>'
        // seta
        + '<span style="color:#4b5563;font-size:10px;">→</span>'
        // FYTD26 destaque
        + '<span style="color:#e2e8f0;font-size:10px;font-weight:700;white-space:nowrap;">'
        +   fmtV4(mtV26,true)+'</span>'
        // Delta colorido grande
        + '<span style="color:'+mtCol+';font-size:12px;font-weight:800;white-space:nowrap;">'
        +   mtArr+Math.abs(mtCres).toFixed(1)+'%</span>'
        // Fonte discreta
        + '<span style="color:#1f2937;font-size:9px;margin-left:auto;white-space:nowrap;">NielsenIQ</span>';
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

  // ── HEADLINE compacto ──
  var hdEl4 = document.getElementById('mso3-headline');
  if(hdEl4){
    var parts4 = brands.map(function(b){
      var v25h=d25[b], v26h=d26[b]; if(v25h===undefined) return '';
      var dt=calcDelta4(v25h,v26h);
      return '<span style="color:'+colors[b]+';font-weight:700;font-size:10px;">'+b+'</span>'
        +' <span style="color:'+dt.col+';font-size:10px;">'+(dt.up?'▲':'▼')+' '+dt.str+'</span>';
    }).filter(Boolean);
    hdEl4.innerHTML =
      '<span style="color:#94A3B8;font-size:10px;font-weight:700;letter-spacing:0.04em;">'+mkt+'</span>'
      +'<span style="color:#374151;font-size:10px;margin:0 6px;">·</span>'
      + parts4.join('<span style="color:#2d3748;margin:0 5px;">·</span>');
    hdEl4.style.padding = '4px 14px 6px';
    hdEl4.style.lineHeight = '1.6';
  }

  // ── MAX VALUE FOR SCALING ──
  var allV4=[]; brands.forEach(function(b){ if(d25[b]!=null) allV4.push(d25[b]); if(d26[b]!=null) allV4.push(d26[b]); });
  var maxV4 = Math.max.apply(null,allV4)||1;

  // ── BARRAS DIAGONAIS 2 COLUNAS ──
  var barsEl4 = document.getElementById('mso3-bars');
  if(barsEl4){
    barsEl4.style.gridTemplateColumns = 'repeat(2, 1fr)';
    barsEl4.style.gap = '4px 8px';
    barsEl4.innerHTML = brands.map(function(b){
      var v25=d25[b], v26=d26[b]; if(v25==null||v26==null) return '';
      var cor = colors[b]||'#e2e8f0';
      var dt4 = calcDelta4(v25,v26);
      // Escala 0-88% da largura da célula
      var w25 = Math.max(2, Math.round(v25/maxV4*88));
      var w26 = Math.max(2, Math.round(v26/maxV4*88));
      var arr = dt4.up?'▲':'▼';

      // Tooltip
      var tip = '<div class="mso2-tip-row">'
        +'<span class="mso2-tip-lbl">FYTD25</span>'
        +'<span class="mso2-tip-val">'+fmtV4(v25)+'</span></div>'
        +'<div class="mso2-tip-row">'
        +'<span class="mso2-tip-lbl">FYTD26</span>'
        +'<span style="color:'+cor+';font-weight:700;">'+fmtV4(v26)+'</span></div>'
        +'<div style="height:1px;background:rgba(255,255,255,0.07);margin:4px 0;"></div>'
        +'<div class="mso2-tip-row">'
        +'<span class="mso2-tip-lbl">Δ YoY</span>'
        +'<span style="color:'+dt4.col+';font-weight:800;">'+arr+' '+dt4.str+'</span></div>';

      // Barra diagonal FY26: repeating-linear-gradient 45deg
      // FY25: linha fina cinza (outline) — mostra onde FY25 ficava
      var diagBg =
        'repeating-linear-gradient(45deg,'
        + cor+'44 0px,'+cor+'44 3px,'
        + 'transparent 3px,transparent 7px)';

      return '<div class="mso2-br" style="padding:5px 10px 5px;">'
        // Linha unica: dot + nome + track + delta + valor
        +'<div style="display:flex;align-items:center;gap:6px;">'
        // Dot
        +'<span style="display:inline-block;width:6px;height:6px;border-radius:50%;'
        +  'background:'+cor+';box-shadow:0 0 5px '+cor+'88;flex-shrink:0;"></span>'
        // Nome
        +'<span style="font-size:10px;font-weight:700;color:#cbd5e1;'
        +  'min-width:65px;max-width:65px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">'
        +  b+'</span>'
        // Track (position:relative, 8px)
        +'<div style="flex:1;position:relative;height:8px;border-radius:4px;'
        +  'background:rgba(255,255,255,0.04);">'
        //   FY25 — contorno cinza fino (muito suave)
        +'<div style="position:absolute;left:0;top:1px;bottom:1px;width:'+w25+'%;'
        +  'background:rgba(100,116,139,0.14);'
        +  'border-right:1.5px solid rgba(100,116,139,0.40);border-radius:4px;"></div>'
        //   FY26 — diagonal colorida
        +'<div style="position:absolute;left:0;top:0;bottom:0;width:'+w26+'%;'
        +  'background:'+diagBg+';'
        +  'border-right:2px solid '+cor+';'
        +  'border-radius:4px;box-shadow:0 0 6px '+cor+'44;"></div>'
        +'</div>'
        // Delta
        +'<span style="font-size:9px;font-weight:800;color:'+dt4.col+';'
        +  'min-width:46px;text-align:right;white-space:nowrap;">'+arr+' '+dt4.str+'</span>'
        // Valor FY26
        +'<span style="font-size:10px;font-weight:700;color:'+cor+';'
        +  'min-width:58px;text-align:right;white-space:nowrap;">'+fmtV4(v26,true)+'</span>'
        +'</div>'
        // Tooltip
        +'<div class="mso2-tooltip">'
        +'<div style="font-size:10px;font-weight:700;color:'+cor+';margin-bottom:5px;'
        +  'border-bottom:0.5px solid rgba(255,255,255,0.08);padding-bottom:4px;letter-spacing:0.05em;">'+b+'</div>'
        +tip
        +'</div>'
        +'</div>';
    }).join('');
  }

  // ── TABELA compacta (11px, ▲/▼ apenas) ──
  var tableEl4 = document.getElementById('mso3-table');
  if(tableEl4){
    var hds4 = isShare
      ? ['MARCA','FY25 (%)','FY26 (%)','Δ YoY']
      : ['MARCA','FY25','FY26','Δ YoY'];
    var rows4 = brands.map(function(b){
      var v25=d25[b], v26=d26[b]; if(v25==null||v26==null) return '';
      var cor=colors[b]||'#e2e8f0';
      var dt4=calcDelta4(v25,v26);
      var arr=dt4.up?'▲':'▼';
      return '<tr>'
        +'<td class="mso2-tc" style="font-size:11px;">'
        +'<span style="display:inline-flex;align-items:center;gap:5px;">'
        +'<span style="width:6px;height:6px;border-radius:50%;background:'+cor+';display:inline-block;"></span>'
        +'<span style="color:'+cor+';font-weight:700;">'+b+'</span></span></td>'
        +'<td class="mso2-tc" style="font-size:11px;color:#374151;">'+fmtV4(v25)+'</td>'
        +'<td class="mso2-tc" style="font-size:11px;color:'+cor+';font-weight:700;">'+fmtV4(v26)+'</td>'
        +'<td class="mso2-tc" style="font-size:11px;color:'+dt4.col+';font-weight:700;">'+arr+' '+dt4.str+'</td>'
        +'</tr>';
    }).join('');
    // Linha TOTAL PR
    var mt4=(typeof FYTD_MARKET_TOTAL!=='undefined')?FYTD_MARKET_TOTAL[mkt]:null;
    var totalRow4='';
    if(mt4&&!isShare){
      var mtV25t=isUn?mt4.fytd25_un:mt4.fytd25_val;
      var mtV26t=isUn?mt4.fytd26_un:mt4.fytd26_val;
      var mtDt4=calcDelta4(mtV25t,mtV26t); var mtArr4=mtDt4.up?'▲':'▼';
      totalRow4='<tr style="border-top:1px solid rgba(34,197,94,0.18);background:rgba(34,197,94,0.03);">'
        +'<td class="mso2-tc" style="font-size:11px;"><span style="color:#22c55e;font-weight:700;">🌎 TOTAL PR</span></td>'
        +'<td class="mso2-tc" style="font-size:11px;color:#374151;">'+fmtV4(mtV25t)+'</td>'
        +'<td class="mso2-tc" style="font-size:11px;color:#22c55e;font-weight:700;">'+fmtV4(mtV26t)+'</td>'
        +'<td class="mso2-tc" style="font-size:11px;color:'+mtDt4.col+';font-weight:700;">'+mtArr4+' '+mtDt4.str+'</td>'
        +'</tr>';
    }
    tableEl4.innerHTML='<table class="mso2-tbl"><thead><tr>'
      +hds4.map(function(h,i){ return '<th class="mso2-th" style="font-size:10px;"'+(i===0?' style="text-align:left;"':'')+'>'+h+'</th>'; }).join('')
      +'</tr></thead><tbody>'+rows4+totalRow4+'</tbody></table>'
      +'<div style="text-align:right;font-size:9px;color:#1e293b;margin-top:4px;letter-spacing:0.03em;">'
      +'fonte: NielsenIQ · 1-Tabela-1 · FYTD = Jul–Mar</div>';
  }

  // ── INSIGHT compacto ──
  var insEl4=document.getElementById('mso3-insight');
  if(insEl4){
    var ents4=brands.map(function(b){
      var v25=d25[b],v26=d26[b]; if(v25==null||v26==null) return null;
      return {b:b, dt:calcDelta4(v25,v26), cor:colors[b]||'#e2e8f0', v26:v26};
    }).filter(Boolean);
    if(ents4.length){
      var srt4=ents4.slice().sort(function(a,b){ return b.dt.raw-a.dt.raw; });
      var ldr4=srt4[0], lag4=srt4[srt4.length-1];
      var mLbl4=isShare?'share':(isVal?'receita':'volume');
      var lines4=ents4.map(function(e){
        return '• <strong style="color:'+e.cor+';font-size:10px;">'+e.b+'</strong>'
          +' <span style="font-size:10px;color:#94A3B8;">FYTD26:</span>'
          +' <strong style="color:#e2e8f0;font-size:10px;">'+fmtV4(e.v26)+'</strong>'
          +' <span style="color:'+e.dt.col+';font-size:10px;">'+(e.dt.up?'▲':'▼')+' '+e.dt.str+'</span>';
      });
      var diag4=ldr4.dt.up
        ?'🚀 <strong style="color:'+ldr4.cor+';">'+ldr4.b+'</strong> lidera crescimento FYTD · '+mkt+'.'
        :'⚠️ Todas as marcas recuam no FYTD · '+mkt+'.';
      if(!lag4.dt.up && lag4.b!==ldr4.b)
        diag4+=' <span style="color:#475569;">·</span> <strong style="color:'+lag4.cor+';">'+lag4.b+'</strong> maior retração ('+lag4.dt.str+').';
      insEl4.innerHTML=
        '<strong style="color:#22c55e;font-size:10px;letter-spacing:0.07em;">📊 DIAGNÓSTICO FYTD · '+mkt+'</strong><br>'
        +lines4.join('<br>')+'<br>'+diag4;
    }
  }
}
/* ═══════════ END MSO3 ═══════════ */"""

assert OLD_BLOCK in html, "OLD_BLOCK nao encontrado no HTML"
html = html.replace(OLD_BLOCK, NEW_FUNC, 1)
print("renderMSO3() v4 substituida.")

with open(str(MAIN_FILE), "w", encoding="utf-8") as f:
    f.write(html)
print(f"Salvo ({len(html):,} chars).")

ts2 = datetime.now().strftime("%Y%m%d_%H%M")
ver = VERS_DIR / f"Dashboard_Farma_Sul_{ts2}_MSO3v4.html"
shutil.copy2(str(MAIN_FILE), str(ver))
print(f"Versao: {ver.name}")
print("DONE!")
