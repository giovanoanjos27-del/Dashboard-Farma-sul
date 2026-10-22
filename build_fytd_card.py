#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_fytd_card.py
Inserts the new "VISAO FISCAL FYTD" card (MSO3) into the dashboard HTML.
Steps:
  1. Backup current dashboard
  2. Read fytd_data.json -> generate NIELSEN_FYTD_VAL JS object
  3. Insert HTML card after MSO2 card closing </div>
  4. Insert JS (data + functions) after renderMSO2Insight()
  5. Add renderMSO3() call inside renderMSO() after renderMSO2()
  6. Save updated dashboard
"""
import json, shutil, re
from pathlib import Path
from datetime import datetime

BASE = Path(r"C:\Users\valqu\OneDrive\Documentos\Claude\Projects\projeto Dashboard_farma_sul")
DASH_DIR = BASE / "Dashboard_farma_sul"
MAIN_FILE = DASH_DIR / "Dashboard_Farma_Sul_20260512_2220.html"
VERS_DIR  = DASH_DIR / "versoes"
FYTD_JSON = BASE / "fytd_data.json"

# ── 1. Backup ────────────────────────────────────────────────────────────────
ts = datetime.now().strftime("%Y%m%d_%H%M")
backup_name = f"Dashboard_Farma_Sul_{ts}_PreFYTDCard.html"
backup_path = VERS_DIR / backup_name
shutil.copy2(str(MAIN_FILE), str(backup_path))
print(f"Backup criado: {backup_name}")

# ── 2. Read fytd_data.json ──────────────────────────────────────────────────
with open(str(FYTD_JSON), encoding="utf-8") as f:
    fytd_data = json.load(f)

markets = list(fytd_data.keys())
print(f"Markets no JSON: {len(markets)}")

# ── 3. Generate NIELSEN_FYTD_VAL JS object ───────────────────────────────────
lines_js = ["const NIELSEN_FYTD_VAL = {"]
for mkt, brands in fytd_data.items():
    lines_js.append(f"  '{mkt}': {{")
    brand_entries = []
    for brand, periods in brands.items():
        f25v  = periods.get("FYTD25", {}).get("val",  0)
        f26v  = periods.get("FYTD26", {}).get("val",  0)
        f25un = periods.get("FYTD25", {}).get("un",   0)
        f26un = periods.get("FYTD26", {}).get("un",   0)
        brand_entries.append(
            f"    '{brand}': {{fytd25_val:{round(f25v,6)},fytd26_val:{round(f26v,6)},"
            f"fytd25_un:{round(f25un,3)},fytd26_un:{round(f26un,3)}}}"
        )
    lines_js.append(",\n".join(brand_entries))
    lines_js.append("  },")
lines_js.append("};")
NIELSEN_FYTD_VAL_JS = "\n".join(lines_js)

# ── 4. Build the HTML card string ────────────────────────────────────────────
# (Uses the same .mso2-* CSS classes — no new CSS needed)
DROPDOWN_OPTIONS = """          <option value="Farma Sul">Farma Sul</option>
          <optgroup label="─ Farma Regional ─">
          <option value="Farma CO">Farma CO</option>
          <option value="Farma Gde RJ">Farma Gde RJ</option>
          <option value="Farma Gde SP">Farma Gde SP</option>
          <option value="Farma Int SP">Farma Int SP</option>
          <option value="Farma MG+ES+Int RJ">Farma MG+ES+Int RJ</option>
          <option value="Farma NE">Farma NE</option>
          </optgroup>
          <optgroup label="─ Farma Independente ─">
          <option value="Farma Indep Sul">Farma Indep Sul</option>
          <option value="Farma Indep CO">Farma Indep CO</option>
          <option value="Farma Indep Gde RJ">Farma Indep Gde RJ</option>
          <option value="Farma Indep Gde SP">Farma Indep Gde SP</option>
          <option value="Farma Indep Int SP">Farma Indep Int SP</option>
          <option value="Farma Indep MG+ES+Int RJ">Farma Indep MG+ES+Int RJ</option>
          <option value="Farma Indep NE">Farma Indep NE</option>
          </optgroup>
          <optgroup label="─ Farma Moderno ─">
          <option value="Farma Moderno Sul">Farma Moderno Sul</option>
          <option value="Farma Moderno CO">Farma Moderno CO</option>
          <option value="Farma Moderno Gde RJ">Farma Moderno Gde RJ</option>
          <option value="Farma Moderno Gde SP">Farma Moderno Gde SP</option>
          <option value="Farma Moderno Int SP">Farma Moderno Int SP</option>
          <option value="Farma Moderno MG+ES+Int RJ">Farma Moderno MG+ES+Int RJ</option>
          <option value="Farma Moderno NE">Farma Moderno NE</option>
          </optgroup>
          <optgroup label="─ T.BR Farma ─">
          <option value="T.BR Farma" selected>T.BR Farma</option>
          <option value="T.BR Farma Indep">T.BR Farma Indep</option>
          <option value="T.BR Farma Moderno">T.BR Farma Moderno</option>
          </optgroup>
          <optgroup label="─ INFC Sul ─">
          <option value="INFC RS">INFC RS</option>
          <option value="INFC SC">INFC SC</option>
          <option value="INFC PR">INFC PR</option>
          <option value="INFC Curitiba">INFC Curitiba</option>
          <option value="INFC Porto Alegre">INFC Porto Alegre</option>
          <option value="INFC Sul">INFC Sul</option>
          <option value="INFC Int PR">INFC Int PR</option>
          <option value="INFC Int RS">INFC Int RS</option>
          <option value="INFC Cidade Gde Sul">INFC Cidade Gde Sul</option>
          <option value="INFC Cidade Peq+Med Sul">INFC Cidade Peq+Med Sul</option>
          </optgroup>
          <optgroup label="─ INFC Nacional ─">
          <option value="INFC MG">INFC MG</option>
          <option value="INFC CO">INFC CO</option>
          <option value="INFC BA">INFC BA</option>
          <option value="INFC Belo Horizonte">INFC Belo Horizonte</option>
          <option value="INFC CE">INFC CE</option>
          <option value="INFC Cidade Gde Gde RJ">INFC Cidade Gde Gde RJ</option>
          <option value="INFC Cidade Gde CO">INFC Cidade Gde CO</option>
          <option value="INFC Cidade Gde Gde SP">INFC Cidade Gde Gde SP</option>
          <option value="INFC Cidade Gde Int SP">INFC Cidade Gde Int SP</option>
          <option value="INFC Cidade Gde MG+ES+Int RJ">INFC Cidade Gde MG+ES+Int RJ</option>
          <option value="INFC Cidade Gde NE">INFC Cidade Gde NE</option>
          <option value="INFC Cidade Peq+Med CO">INFC Cidade Peq+Med CO</option>
          <option value="INFC Cidade Peq+Med Int SP">INFC Cidade Peq+Med Int SP</option>
          <option value="INFC Cidade Peq+Med MG+ES+Int RJ">INFC Cidade Peq+Med MG+ES+Int RJ</option>
          <option value="INFC Cidade Peq+Med NE">INFC Cidade Peq+Med NE</option>
          <option value="INFC DF">INFC DF</option>
          <option value="INFC Fortaleza">INFC Fortaleza</option>
          <option value="INFC GO">INFC GO</option>
          <option value="INFC Gde RJ">INFC Gde RJ</option>
          <option value="INFC Gde SP">INFC Gde SP</option>
          <option value="INFC Int BA">INFC Int BA</option>
          <option value="INFC Int CE">INFC Int CE</option>
          <option value="INFC Int MG">INFC Int MG</option>
          <option value="INFC Int PE">INFC Int PE</option>
          <option value="INFC Int SP">INFC Int SP</option>
          <option value="INFC MA+PI">INFC MA+PI</option>
          <option value="INFC MG+ES+Int RJ">INFC MG+ES+Int RJ</option>
          <option value="INFC Man+Bel+Ana">INFC Man+Bel+Ana</option>
          <option value="INFC Manaus">INFC Manaus</option>
          <option value="INFC NE">INFC NE</option>
          <option value="INFC PE">INFC PE</option>
          <option value="INFC Recife">INFC Recife</option>
          <option value="INFC SP">INFC SP</option>
          <option value="INFC Salvador">INFC Salvador</option>
          </optgroup>
          <optgroup label="─ T.BR INFC ─">
          <option value="T.BR INFC">T.BR INFC</option>
          </optgroup>"""

SELECT_STYLE = "font-size:11px;padding:6px 28px 6px 10px;border-radius:7px;border:0.5px solid rgba(251,191,36,0.3);background:#161B22;color:#e2e8f0;cursor:pointer;font-family:inherit;appearance:none;background-image:url(&quot;data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='10' height='6'%3E%3Cpath d='M0 0l5 6 5-6z' fill='%23fbbf24'/%3E%3C/svg%3E&quot;);background-repeat:no-repeat;background-position:right 10px center;"

MSO3_HTML = f"""
  <!-- CARD VISAO FISCAL FYTD — JUL-MAR 2025 vs 2026 -->

  <div class="card full" style="margin-bottom:14px;">
    <div class="card-header">
      <div>
        <div style="font-size:10px;font-weight:700;letter-spacing:0.1em;color:#fbbf24;margin-bottom:4px;" id="mso3-card-title">VISAO FISCAL FYTD &middot; JUL&ndash;MAR</div>
        <div style="margin-top:5px;margin-bottom:2px;"><span style="display:inline-flex;align-items:center;gap:5px;font-size:10px;font-weight:700;letter-spacing:0.06em;color:#22c55e;background:rgba(34,197,94,0.10);border:0.5px solid rgba(34,197,94,0.35);border-radius:5px;padding:3px 10px;text-transform:uppercase;">&#x1F4CA; FYTD &middot; Ano Fiscal HB (Jul&ndash;Mar)</span></div>
        <div class="card-title" id="mso3-card-h2">$ Share por Marca &mdash; FYTD 2025 vs 2026</div>
        <div class="card-sub" id="mso3-card-sub">Jul-Mar/25 vs Jul-Mar/26 &middot; OFF! &middot; EXPOSIS &middot; XO INSETO &middot; SUPER REPELEX &middot; SBP &middot; <span id="mso3-mkt-lbl">T.BR Farma</span></div>
      </div>
      <div style="display:flex;align-items:center;gap:8px;flex-wrap:wrap;">
        <select id="mso3MarketSel" onchange="renderMSO3()" style="{SELECT_STYLE}">
{DROPDOWN_OPTIONS}
        </select>
        <div class="toggle-group" style="display:flex;gap:0;border-radius:7px;overflow:hidden;border:0.5px solid rgba(251,191,36,0.3);">
          <button class="tgl active blue" id="mso3-mode-share" onclick="setMSO3Mode('share',this)" style="font-size:11px;padding:5px 12px;border:none;background:rgba(251,191,36,0.12);color:#fbbf24;cursor:pointer;font-family:inherit;font-weight:700;">Share</button>
          <button class="tgl" id="mso3-mode-val" onclick="setMSO3Mode('val',this)" style="font-size:11px;padding:5px 12px;border:none;border-left:0.5px solid rgba(251,191,36,0.2);background:#161B22;color:#D1D5DB;cursor:pointer;font-family:inherit;font-weight:600;">R$ MM</button>
          <button class="tgl" id="mso3-mode-un" onclick="setMSO3Mode('un',this)" style="font-size:11px;padding:5px 12px;border:none;border-left:0.5px solid rgba(251,191,36,0.2);background:#161B22;color:#D1D5DB;cursor:pointer;font-family:inherit;font-weight:600;">Unidades</button>
        </div>
      </div>
    </div>
    <!-- Headline diagnostico -->
    <div id="mso3-headline" style="font-size:12px;color:#D1D5DB;margin-bottom:16px;line-height:1.8;padding:10px 16px;background:rgba(34,197,94,0.05);border-radius:8px;border-left:3px solid #22c55e;"></div>

    <!-- Barras horizontais comparativas FYTD -->
    <div id="mso3-bars" style="display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:18px;"></div>

    <!-- Tabela FYTD YoY -->
    <div style="background:rgba(255,255,255,0.02);border-radius:10px;padding:14px 16px;margin-bottom:16px;border:0.5px solid rgba(255,255,255,0.06);">
      <div style="font-size:9px;font-weight:700;letter-spacing:0.1em;color:#64748b;margin-bottom:10px;" id="mso3-table-title">VARIACAO FYTD YoY &mdash; JUL&ndash;MAR</div>
      <div id="mso3-table"></div>
    </div>

    <!-- Diagnostico automatico -->
    <div id="mso3-insight" style="padding:12px 16px;background:rgba(255,255,255,0.03);border-radius:8px;border-left:3px solid rgba(34,197,94,0.35);font-size:11px;color:#D1D5DB;line-height:1.7;"></div>
    <div style="font-size:9px;color:#3d4451;margin-top:12px;padding-top:8px;border-top:0.5px solid rgba(255,255,255,0.04);">
      Fonte: NielsenIQ Retail Measurement &middot; PS - GBL - SC JOHNSON - BR - PEST CONTROL &middot; Exportado: 23 mar 2026
    </div>
  </div>

"""

# ── 5. Build the JS functions ─────────────────────────────────────────────────
MSO3_JS = r"""
/* ═══════════ MSO3 — VISAO FISCAL FYTD Jul-Mar ═══════════ */
var mso3Mode = 'share'; // 'share' | 'val' | 'un'

function setMSO3Mode(mode, btn){
  mso3Mode = mode;
  ['mso3-mode-share','mso3-mode-val','mso3-mode-un'].forEach(function(id){
    var b = document.getElementById(id);
    if(!b) return;
    var active = (id === 'mso3-mode-'+mode);
    b.style.color = active ? '#fbbf24' : '#D1D5DB';
    b.style.background = active ? 'rgba(251,191,36,0.12)' : '#1F2937';
  });
  renderMSO3();
}

function renderMSO3(){
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

  /* ── HELPERS ── */
  function fmtV3(v){
    if(v===null||v===undefined) return '—';
    if(isShare) return v.toFixed(2)+'%';
    if(isVal) return v>=1?'R$'+v.toFixed(2)+'MM':'R$'+(v*1000).toFixed(0)+'K';
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

  /* ── HEADLINE ── */
  var hdEl3 = document.getElementById('mso3-headline');
  if(hdEl3){
    function pctHl3(v26, v25){
      var p = v25>0 ? Math.round((v26-v25)/v25*1000)/10 : 0;
      return (p>=0?'<span style="color:#34d399;">▲ +':'<span style="color:#ef4444;">▼ ')
        + Math.abs(p).toFixed(1)+'%</span>';
    }
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
      + bPartsH3.join('  ·  ');
  }

  /* ── MAX VALUE FOR BAR SCALING ── */
  var allV3 = [];
  brands.forEach(function(b){ if(d25[b]!=null) allV3.push(d25[b]); if(d26[b]!=null) allV3.push(d26[b]); });
  var maxV3 = Math.max.apply(null, allV3) || 1;

  /* ── HORIZONTAL BARS ── */
  var barsEl3 = document.getElementById('mso3-bars');
  if(barsEl3){
    barsEl3.innerHTML = brands.map(function(b){
      var v25 = d25[b], v26 = d26[b];
      if(v25==null||v26==null) return '';
      var cor = colors[b]||'#e2e8f0';
      var delta3 = calcDelta3(v25, v26);
      var w25 = Math.max(2, Math.round(v25/maxV3*80));
      var w26 = Math.max(2, Math.round(v26/maxV3*80));
      var arrow3 = delta3.up ? '↑' : '↓';

      var tipRows3 = ''
        +'<div class="mso2-tip-row"><span class="mso2-tip-lbl">FYTD25 (Jul-Mar/25)</span><span class="mso2-tip-val">'+fmtV3(v25)+'</span></div>'
        +'<div class="mso2-tip-row"><span class="mso2-tip-lbl">FYTD26 (Jul-Mar/26)</span><span style="color:'+cor+';font-weight:700;">'+fmtV3(v26)+'</span></div>'
        +'<div style="height:1px;background:rgba(255,255,255,0.07);margin:5px 0;"></div>'
        +'<div class="mso2-tip-row"><span class="mso2-tip-lbl">Δ FYTD YoY</span><span style="font-weight:700;color:'+delta3.col+';">'+arrow3+' '+delta3.str+'</span></div>';

      return '<div class="mso2-br">'
        +'<div class="mso2-br-head">'
        +'<span style="display:inline-block;width:9px;height:9px;border-radius:50%;background:'+cor+';box-shadow:0 0 7px '+cor+'99;flex-shrink:0;"></span>'
        +'<span style="font-size:12px;font-weight:700;color:#e2e8f0;letter-spacing:0.03em;">'+b+'</span>'
        +'<span class="mso2-delta-badge" style="color:'+delta3.col+';background:'+delta3.col+'14;border-color:'+delta3.col+'40;">'
        +arrow3+' '+delta3.str+'</span>'
        +'</div>'
        +'<div class="mso2-bar-row">'
        +'<span class="mso2-bar-yr">FY25</span>'
        +'<div class="mso2-bar-track"><div class="mso2-bar-fill mso2-fill25" style="width:'+w25+'%"></div></div>'
        +'<span class="mso2-bar-val">'+fmtV3(v25)+'</span>'
        +'</div>'
        +'<div class="mso2-bar-row">'
        +'<span class="mso2-bar-yr mso2-yr26">FY26</span>'
        +'<div class="mso2-bar-track"><div class="mso2-bar-fill" style="width:'+w26+'%;background:'+cor+'cc;box-shadow:0 0 8px '+cor+'44;border-right:2px solid '+cor+';"></div></div>'
        +'<span class="mso2-bar-val mso2-bval26" style="color:'+cor+';">'+fmtV3(v26)+'</span>'
        +'</div>'
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
        +'<td class="mso2-tc">'+fmtV3(v25)+'</td>'
        +'<td class="mso2-tc" style="color:'+cor+';font-weight:700;">'+fmtV3(v26)+'</td>'
        +'<td class="mso2-tc" style="color:'+delta3.col+';font-weight:700;">'+arrow3+' '+delta3.str+'</td>'
        +'</tr>';
    }).join('');

    tableEl3.innerHTML = '<table class="mso2-tbl"><thead><tr>'
      + hds3.map(function(h,i){ return '<th class="mso2-th"' + (i===0?' style="text-align:left;"':'') + '>'+h+'</th>'; }).join('')
      + '</tr></thead><tbody>'+rows3+'</tbody></table>';
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
        diagLine3 += ' <span style="color:#64748b;">·</span> <strong style="color:'+laggard3.cor+';">'+laggard3.b+'</strong> maior retracão ('+laggard3.delta3.str+').';
      insEl3.innerHTML = '<strong style="color:#22c55e;font-size:10px;letter-spacing:0.08em;">📊 DIAGNÓSTICO FYTD &mdash; '+mkt+'  &middot;  '+metricLbl3.toUpperCase()+'</strong><br>'
        + lines3.join('<br>') + '<br>' + diagLine3;
    }
  }
}
/* ═══════════ END MSO3 ═══════════ */
"""

# ── 6. Read dashboard HTML ───────────────────────────────────────────────────
print("Lendo dashboard...")
with open(str(MAIN_FILE), encoding="utf-8") as f:
    html = f.read()

original_len = len(html)

# ── 7. Insert HTML card after MSO2 card closing </div> ───────────────────────
# Anchor: the comment "<!-- MARKET SHARE POR SKU -->"
ANCHOR_HTML = "<!-- MARKET SHARE POR SKU -->"
assert ANCHOR_HTML in html, "Anchor HTML not found!"
html = html.replace(ANCHOR_HTML, MSO3_HTML + ANCHOR_HTML, 1)
print("Card HTML inserido.")

# ── 8. Insert JS after renderMSO2Insight() end ──────────────────────────────
# Anchor: the comment "// ── Avg Price: pricing trend insight ──"
ANCHOR_JS = "// ── Avg Price: pricing trend insight ──"
assert ANCHOR_JS in html, "Anchor JS not found!"

# Insert NIELSEN_FYTD_VAL + MSO3 JS functions before the anchor
JS_INSERT = NIELSEN_FYTD_VAL_JS + "\n\n" + MSO3_JS + "\n"
html = html.replace(ANCHOR_JS, JS_INSERT + ANCHOR_JS, 1)
print("JS insertado (data + funcoes).")

# ── 9. Add renderMSO3() call after renderMSO2() in renderMSO() ──────────────
ANCHOR_CALL = "  renderMSO2();\n}"
assert ANCHOR_CALL in html, "Anchor call not found!"
html = html.replace(ANCHOR_CALL, "  renderMSO2();\n  renderMSO3();\n}", 1)
print("renderMSO3() call adicionado.")

# ── 10. Write updated dashboard ──────────────────────────────────────────────
with open(str(MAIN_FILE), "w", encoding="utf-8") as f:
    f.write(html)

new_len = len(html)
print(f"Dashboard salvo. Tamanho: {original_len:,} -> {new_len:,} chars ({new_len-original_len:+,})")

# ── 11. Save versioned copy ───────────────────────────────────────────────────
ts2 = datetime.now().strftime("%Y%m%d_%H%M")
ver_name = f"Dashboard_Farma_Sul_{ts2}_FYTDCard.html"
ver_path = VERS_DIR / ver_name
shutil.copy2(str(MAIN_FILE), str(ver_path))
print(f"Versao salva: {ver_name}")
print("DONE!")
