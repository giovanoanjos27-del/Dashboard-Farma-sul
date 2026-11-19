#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
upgrade_mso3.py
Melhora o card MSO3 (VISÃO FISCAL FYTD) com:
  1. Headline de mercado total Personal Repellent (por mercado)
  2. Barras aprimoradas: delta % inline + gradiente FY26 vs FY25 suave
  3. Dados FYTD_MARKET_TOTAL injetados
"""
import json, shutil
from pathlib import Path
from datetime import datetime

BASE      = Path(r"C:\Users\valqu\OneDrive\Documentos\Claude\Projects\projeto Dashboard_farma_sul")
DASH_DIR  = BASE / "Dashboard_farma_sul"
MAIN_FILE = DASH_DIR / "Dashboard_Farma_Sul_20260512_2220.html"
VERS_DIR  = DASH_DIR / "versoes"
TOTAL_JSON = BASE / "fytd_market_total.json"

# ── 1. Backup ─────────────────────────────────────────────────────────────────
ts = datetime.now().strftime("%Y%m%d_%H%M")
bk = VERS_DIR / f"Dashboard_Farma_Sul_{ts}_PreMSO3v2.html"
shutil.copy2(str(MAIN_FILE), str(bk))
print(f"Backup: {bk.name}")

# ── 2. Gera FYTD_MARKET_TOTAL JS ──────────────────────────────────────────────
with open(str(TOTAL_JSON), encoding="utf-8") as f:
    total_data = json.load(f)

js_lines = ["const FYTD_MARKET_TOTAL = {"]
for mkt, periods in total_data.items():
    f25v = periods.get("FYTD25", {}).get("val", 0)
    f26v = periods.get("FYTD26", {}).get("val", 0)
    f25u = periods.get("FYTD25", {}).get("un",  0)
    f26u = periods.get("FYTD26", {}).get("un",  0)
    js_lines.append(
        f"  '{mkt}': {{fytd25_val:{round(f25v,6)},fytd26_val:{round(f26v,6)},"
        f"fytd25_un:{round(f25u,3)},fytd26_un:{round(f26u,3)}}},"
    )
js_lines.append("};")
FYTD_MARKET_TOTAL_JS = "\n".join(js_lines)

# ── 3. Lê o dashboard ─────────────────────────────────────────────────────────
print("Lendo dashboard...")
with open(str(MAIN_FILE), encoding="utf-8") as f:
    html = f.read()

# ── 4. Insere div mso3-market-total no HTML card ──────────────────────────────
# Inserir ANTES do div mso3-headline
OLD_HEADLINE_DIV = '    <!-- Headline diagnostico -->\n    <div id="mso3-headline"'
NEW_HEADLINE_DIV = (
    '    <!-- Mercado Total Personal Repellent -->\n'
    '    <div id="mso3-market-total" style="font-size:11px;color:#D1D5DB;margin-bottom:8px;'
    'line-height:1.6;padding:8px 14px;background:rgba(34,197,94,0.04);border-radius:7px;'
    'border:0.5px solid rgba(34,197,94,0.2);"></div>\n\n'
    '    <!-- Headline diagnostico -->\n'
    '    <div id="mso3-headline"'
)
assert OLD_HEADLINE_DIV in html, "Ancora HTML mso3-headline nao encontrada!"
html = html.replace(OLD_HEADLINE_DIV, NEW_HEADLINE_DIV, 1)
print("Div mso3-market-total inserido.")

# ── 5. Injeta FYTD_MARKET_TOTAL antes de NIELSEN_FYTD_VAL ──────────────────────
ANCHOR_DATA = "const NIELSEN_FYTD_VAL = {"
assert ANCHOR_DATA in html, "Ancora NIELSEN_FYTD_VAL nao encontrada!"
html = html.replace(ANCHOR_DATA, FYTD_MARKET_TOTAL_JS + "\n\n" + ANCHOR_DATA, 1)
print("FYTD_MARKET_TOTAL injetado.")

# ── 6. Substitui renderMSO3() pela versão aprimorada ─────────────────────────
OLD_FUNC_START = "function renderMSO3(){"
OLD_FUNC_END   = "/* ═══════════ END MSO3 ═══════════ */"
assert OLD_FUNC_START in html, "Ancora renderMSO3 nao encontrada!"
assert OLD_FUNC_END in html, "Ancora END MSO3 nao encontrada!"

# Find the entire block to replace (from function start to END comment)
start_idx = html.index(OLD_FUNC_START)
end_idx   = html.index(OLD_FUNC_END) + len(OLD_FUNC_END)
OLD_BLOCK = html[start_idx:end_idx]

NEW_FUNC = r"""function renderMSO3(){
  var sel = document.getElementById('mso3MarketSel');
  var mkt = sel ? sel.value : 'T.BR Farma';
  var isShare = mso3Mode === 'share';
  var isVal   = mso3Mode === 'val';
  var isUn    = mso3Mode === 'un';

  var brands = MSO_BRANDS;
  var colors = MSO_COLORS;

  // Update labels
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

  /* ── HELPERS ── */
  function fmtV3(v){
    if(v===null||v===undefined) return '—';
    if(isShare) return v.toFixed(2)+'%';
    if(isVal){
      if(v>=100) return 'R$'+v.toFixed(1)+'MM';
      if(v>=1)   return 'R$'+v.toFixed(2)+'MM';
      return 'R$'+(v*1000).toFixed(0)+'K';
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

  /* ── MARKET TOTAL HEADLINE ── */
  var mktTotalEl = document.getElementById('mso3-market-total');
  if(mktTotalEl){
    var mt = (typeof FYTD_MARKET_TOTAL !== 'undefined') ? FYTD_MARKET_TOTAL[mkt] : null;
    if(mt && (isVal || isUn)){
      var mtV25 = isVal ? mt.fytd25_val : mt.fytd25_un;
      var mtV26 = isVal ? mt.fytd26_val : mt.fytd26_un;
      var mtCres = mtV25>0 ? Math.round((mtV26/mtV25-1)*1000)/10 : 0;
      var mtCol = mtCres>=0?'#34d399':'#ef4444';
      var mtArr = mtCres>=0?'▲ +':'▼ ';
      var mtUnit = isVal ? 'R$ MM' : 'K un';
      mktTotalEl.style.display = '';
      mktTotalEl.innerHTML =
        '🌎 <strong style="color:#94A3B8;font-size:10px;letter-spacing:0.06em;">PERSONAL REPELLENT · MERCADO TOTAL</strong>'
        + '&nbsp;&nbsp;FYTD25: <span style="color:#64748b;">'+fmtV3(mtV25)+'</span>'
        + '&nbsp;&nbsp;FYTD26: <strong style="color:#e2e8f0;">'+fmtV3(mtV26)+'</strong>'
        + '&nbsp;&nbsp;<span style="color:'+mtCol+';font-weight:700;font-size:12px;">'+mtArr+Math.abs(mtCres).toFixed(1)+'%</span>'
        + '<span style="color:#3d4451;font-size:9px;margin-left:8px;">vs FYTD25 (NielsenIQ)</span>';
    } else if(mt && isShare){
      // For share mode: show market context as total value reference
      var mt25v = mt.fytd25_val, mt26v = mt.fytd26_val;
      var mtCresS = mt25v>0?Math.round((mt26v/mt25v-1)*1000)/10:0;
      var mtColS = mtCresS>=0?'#34d399':'#ef4444';
      mktTotalEl.style.display = '';
      mktTotalEl.innerHTML =
        '🌎 <strong style="color:#94A3B8;font-size:10px;letter-spacing:0.06em;">PERSONAL REPELLENT · MERCADO TOTAL</strong>'
        + '&nbsp;&nbsp;FYTD25: <span style="color:#64748b;">R$'+(mt25v>=100?mt25v.toFixed(1):mt25v.toFixed(2))+'MM</span>'
        + '&nbsp;&nbsp;FYTD26: <strong style="color:#e2e8f0;">R$'+(mt26v>=100?mt26v.toFixed(1):mt26v.toFixed(2))+'MM</strong>'
        + '&nbsp;&nbsp;<span style="color:'+mtColS+';font-weight:700;font-size:12px;">'+(mtCresS>=0?'▲ +':'▼ ')+Math.abs(mtCresS).toFixed(1)+'%</span>'
        + '<span style="color:#3d4451;font-size:9px;margin-left:8px;">vs FYTD25 (NielsenIQ)</span>';
    } else {
      mktTotalEl.style.display = 'none';
    }
  }

  /* ── BUILD VALUE SETS ── */
  var d25 = {}, d26 = {};

  if(isShare){
    var dS = (typeof MKTSHARE_OVERVIEW !== 'undefined') ? MKTSHARE_OVERVIEW[mkt] : null;
    if(!dS){
      var hdEl3 = document.getElementById('mso3-headline');
      if(hdEl3) hdEl3.innerHTML = '<span style="color:#64748b;">Dados de share não disponíveis para este mercado.</span>';
      return;
    }
    brands.forEach(function(b){
      var bd = dS[b]; if(!bd) return;
      d25[b] = bd.fytd25 != null ? bd.fytd25 : 0;
      d26[b] = bd.fytd26 != null ? bd.fytd26 : 0;
    });
  } else {
    var nfv = (typeof NIELSEN_FYTD_VAL !== 'undefined') ? NIELSEN_FYTD_VAL[mkt] : null;
    if(!nfv){
      var hdEl3 = document.getElementById('mso3-headline');
      if(hdEl3) hdEl3.innerHTML = '<span style="color:#64748b;">Dados FYTD não disponíveis para este mercado.</span>';
      return;
    }
    brands.forEach(function(b){
      var bd = nfv[b]; if(!bd) return;
      d25[b] = isVal ? bd.fytd25_val : bd.fytd25_un;
      d26[b] = isVal ? bd.fytd26_val : bd.fytd26_un;
    });
  }

  /* ── BRAND HEADLINE ── */
  var hdEl3 = document.getElementById('mso3-headline');
  if(hdEl3){
    var bPartsH3 = brands.map(function(b){
      var v25h = d25[b], v26h = d26[b];
      if(v25h===undefined||v26h===undefined) return '';
      var delta3 = calcDelta3(v25h, v26h);
      return '<span style="color:'+colors[b]+';font-weight:700;">'+b+'</span>'
        +' <span style="color:'+delta3.col+';font-weight:700;">'+(delta3.up?'▲ ':'▼ ')+delta3.str+'</span>';
    }).filter(Boolean);
    var unitLbl3 = isShare ? 'Share FYTD YoY' : (isVal ? 'R$ MM FYTD YoY' : 'Unidades FYTD YoY');
    hdEl3.innerHTML = '<strong style="color:#e2e8f0;">'+mkt+'</strong>'
      + ' · <span style="font-size:11px;color:#94A3B8;">'+unitLbl3+': </span>'
      + bPartsH3.join('&nbsp;&nbsp;·&nbsp;&nbsp;');
  }

  /* ── MAX VALUE FOR BAR SCALING ── */
  var allV3 = [];
  brands.forEach(function(b){ if(d25[b]!=null) allV3.push(d25[b]); if(d26[b]!=null) allV3.push(d26[b]); });
  var maxV3 = Math.max.apply(null, allV3) || 1;

  /* ── ENHANCED HORIZONTAL BARS ── */
  var barsEl3 = document.getElementById('mso3-bars');
  if(barsEl3){
    barsEl3.innerHTML = brands.map(function(b){
      var v25 = d25[b], v26 = d26[b];
      if(v25==null||v26==null) return '';
      var cor = colors[b]||'#e2e8f0';
      var delta3 = calcDelta3(v25, v26);
      var w25 = Math.max(2, Math.round(v25/maxV3*78));
      var w26 = Math.max(2, Math.round(v26/maxV3*78));
      var arrow3 = delta3.up ? '↑' : '↓';

      var tipRows3 = ''
        +'<div class="mso2-tip-row"><span class="mso2-tip-lbl">FYTD25 (Jul-Mar/25)</span><span class="mso2-tip-val">'+fmtV3(v25)+'</span></div>'
        +'<div class="mso2-tip-row"><span class="mso2-tip-lbl">FYTD26 (Jul-Mar/26)</span><span style="color:'+cor+';font-weight:700;">'+fmtV3(v26)+'</span></div>'
        +'<div style="height:1px;background:rgba(255,255,255,0.07);margin:5px 0;"></div>'
        +'<div class="mso2-tip-row"><span class="mso2-tip-lbl">Δ FYTD YoY</span><span style="font-weight:700;color:'+delta3.col+';">'+arrow3+' '+delta3.str+'</span></div>';

      return '<div class="mso2-br">'
        // Header: brand name only (delta badge inline with bar now)
        +'<div class="mso2-br-head" style="margin-bottom:5px;">'
        +'<span style="display:inline-block;width:9px;height:9px;border-radius:50%;background:'+cor+';box-shadow:0 0 7px '+cor+'99;flex-shrink:0;"></span>'
        +'<span style="font-size:12px;font-weight:700;color:#e2e8f0;letter-spacing:0.03em;">'+b+'</span>'
        +'</div>'
        // FY25 bar — suave/muted como referência de fundo
        +'<div class="mso2-bar-row" style="margin-bottom:4px;">'
        +'<span class="mso2-bar-yr" style="color:#374151;">FY25</span>'
        +'<div class="mso2-bar-track">'
        +'<div style="height:100%;border-radius:3px;width:'+w25+'%;background:rgba(100,116,139,0.18);border:0.5px solid rgba(100,116,139,0.22);"></div>'
        +'</div>'
        +'<span class="mso2-bar-val" style="color:#4a5568;">'+fmtV3(v25)+'</span>'
        +'</div>'
        // FY26 bar — gradiente neon + delta inline
        +'<div class="mso2-bar-row">'
        +'<span class="mso2-bar-yr mso2-yr26">FY26</span>'
        +'<div class="mso2-bar-track">'
        +'<div style="height:100%;border-radius:3px;width:'+w26+'%;'
        +'background:linear-gradient(90deg,'+cor+'44,'+cor+'cc);'
        +'box-shadow:0 0 8px '+cor+'33;border-right:2px solid '+cor+';"></div>'
        +'</div>'
        // Delta inline ao fim da barra
        +'<span style="font-size:10px;font-weight:800;color:'+delta3.col+';white-space:nowrap;min-width:48px;text-align:left;padding-left:4px;">'+arrow3+' '+delta3.str+'</span>'
        +'<span class="mso2-bar-val mso2-bval26" style="color:'+cor+';">'+fmtV3(v26)+'</span>'
        +'</div>'
        // Tooltip
        +'<div class="mso2-tooltip">'
        +'<div style="font-size:10px;font-weight:700;color:'+cor+';margin-bottom:6px;letter-spacing:0.05em;border-bottom:0.5px solid rgba(255,255,255,0.08);padding-bottom:5px;">'+b+'</div>'
        +tipRows3
        +'</div>'
        +'</div>';
    }).join('');
  }

  /* ── TABLE ── */
  var tableEl3 = document.getElementById('mso3-table');
  if(tableEl3){
    var hds3 = isShare
      ? ['MARCA','FYTD25 (%)','FYTD26 (%)','&#916; FYTD YoY (pp)']
      : ['MARCA','FYTD25','FYTD26','&#916; FYTD YoY'];

    var rows3 = brands.map(function(b){
      var v25 = d25[b], v26 = d26[b];
      if(v25==null||v26==null) return '';
      var cor = colors[b]||'#e2e8f0';
      var delta3 = calcDelta3(v25, v26);
      var arrow3 = delta3.up ? '↑' : '↓';
      return '<tr>'
        +'<td class="mso2-tc"><span style="color:'+cor+';font-weight:700;font-size:10px;letter-spacing:0.03em;">'+b+'</span></td>'
        +'<td class="mso2-tc" style="color:#64748b;">'+fmtV3(v25)+'</td>'
        +'<td class="mso2-tc" style="color:'+cor+';font-weight:700;">'+fmtV3(v26)+'</td>'
        +'<td class="mso2-tc" style="color:'+delta3.col+';font-weight:700;">'+arrow3+' '+delta3.str+'</td>'
        +'</tr>';
    }).join('');

    // Market total row separator
    var mt3 = (typeof FYTD_MARKET_TOTAL !== 'undefined') ? FYTD_MARKET_TOTAL[mkt] : null;
    var totalRow3 = '';
    if(mt3 && !isShare){
      var mtV25t = isVal ? mt3.fytd25_val : mt3.fytd25_un;
      var mtV26t = isVal ? mt3.fytd26_val : mt3.fytd26_un;
      var mtDt = calcDelta3(mtV25t, mtV26t);
      var mtArrt = mtDt.up ? '↑' : '↓';
      totalRow3 = '<tr style="border-top:1px solid rgba(34,197,94,0.2);">'
        +'<td class="mso2-tc"><span style="color:#22c55e;font-weight:700;font-size:10px;letter-spacing:0.03em;">🌎 TOTAL PR</span></td>'
        +'<td class="mso2-tc" style="color:#64748b;">'+fmtV3(mtV25t)+'</td>'
        +'<td class="mso2-tc" style="color:#22c55e;font-weight:700;">'+fmtV3(mtV26t)+'</td>'
        +'<td class="mso2-tc" style="color:'+mtDt.col+';font-weight:700;">'+mtArrt+' '+mtDt.str+'</td>'
        +'</tr>';
    }

    tableEl3.innerHTML = '<table class="mso2-tbl"><thead><tr>'
      + hds3.map(function(h,i){ return '<th class="mso2-th"' + (i===0?' style="text-align:left;"':'') + '>'+h+'</th>'; }).join('')
      + '</tr></thead><tbody>'+rows3+totalRow3+'</tbody></table>';
  }

  /* ── INSIGHT ── */
  var insEl3 = document.getElementById('mso3-insight');
  if(insEl3){
    var entries3 = brands.map(function(b){
      var v25 = d25[b], v26 = d26[b];
      if(v25==null||v26==null) return null;
      var delta3 = calcDelta3(v25, v26);
      return {b:b, delta3:delta3, cor:colors[b]||'#e2e8f0'};
    }).filter(Boolean);

    if(entries3.length){
      var sorted3 = entries3.slice().sort(function(a,b3){
        var va = parseFloat(a.delta3.str), vb3 = parseFloat(b3.delta3.str); return vb3-va;
      });
      var leader3 = sorted3[0], laggard3 = sorted3[sorted3.length-1];
      var metricLbl3 = isShare ? 'share' : (isVal ? 'receita' : 'volume');
      var lines3 = entries3.map(function(e){
        var arr3 = e.delta3.up ? '▲ ' : '▼ ';
        return '• <strong style="color:'+e.cor+';">'+e.b+'</strong>: FYTD26 = <strong style="color:#e2e8f0;">'+fmtV3(d26[e.b])+'</strong>'
          +' <span style="color:'+e.delta3.col+';">('+arr3+e.delta3.str+' vs FYTD25)</span>';
      });
      var diagLine3 = leader3.delta3.up
        ? '🚀 <strong style="color:'+leader3.cor+';">'+leader3.b+'</strong> lidera crescimento FYTD em <strong style="color:#e2e8f0;">'+mkt+'</strong>.'
        : '⚠️ Todas as marcas recuam no FYTD '+mkt+'.';
      if(laggard3.delta3.up === false && laggard3.b !== leader3.b)
        diagLine3 += ' <span style="color:#64748b;">·</span> <strong style="color:'+laggard3.cor+';">'+laggard3.b+'</strong> maior retração ('+laggard3.delta3.str+').';
      insEl3.innerHTML = '<strong style="color:#22c55e;font-size:10px;letter-spacing:0.08em;">📊 DIAGNÓSTICO FYTD &mdash; '+mkt+'&nbsp;&nbsp;·&nbsp;&nbsp;'+metricLbl3.toUpperCase()+'</strong><br>'
        + lines3.join('<br>') + '<br>' + diagLine3;
    }
  }
}
/* ═══════════ END MSO3 ═══════════ */"""

# Replace the old block
assert OLD_BLOCK in html, "Bloco renderMSO3 nao encontrado no HTML!"
html = html.replace(OLD_BLOCK, NEW_FUNC, 1)
print("renderMSO3() substituida pela versao aprimorada.")

# ── 7. Salva ──────────────────────────────────────────────────────────────────
with open(str(MAIN_FILE), "w", encoding="utf-8") as f:
    f.write(html)
print(f"Dashboard salvo ({len(html):,} chars).")

ts2 = datetime.now().strftime("%Y%m%d_%H%M")
ver = VERS_DIR / f"Dashboard_Farma_Sul_{ts2}_MSO3v2.html"
shutil.copy2(str(MAIN_FILE), str(ver))
print(f"Versao: {ver.name}")
print("DONE!")
