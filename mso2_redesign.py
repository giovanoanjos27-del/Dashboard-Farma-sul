# mso2_redesign.py — Redesign completo do card MARKET SHARE Calendário Gregoriano
# Substitui gráfico de linhas por barras horizontais executivas + tabela mensal YoY
import shutil, sys, os, re
sys.stdout.reconfigure(encoding='utf-8')

BASE = r'C:\Users\valqu\OneDrive\Documentos\Claude\Projects\projeto Dashboard_farma_sul'
SRC  = BASE + r'\Dashboard_farma_sul\Dashboard_Farma_Sul_20260512_2220.html'
BKP  = BASE + r'\Dashboard_farma_sul\versoes\Dashboard_Farma_Sul_20260513_1400_PreMSO2Redesign.html'
OUT  = BASE + r'\Dashboard_farma_sul\versoes\Dashboard_Farma_Sul_20260513_1405_MSO2Redesign.html'

shutil.copy2(SRC, BKP)
print(f'Backup: {os.path.basename(BKP)}')

with open(SRC, encoding='utf-8') as f:
    c = f.read()

orig_lines = len(c.splitlines())
ok_count = 0

def patch_str(label, old, new, src):
    n = src.count(old)
    if n == 0:
        print(f'  MISS  {label}')
        return src, False
    if n > 1:
        print(f'  WARN ({n})  {label}')
    r = src.replace(old, new, 1)
    print(f'  OK    {label}')
    return r, True

def patch_re(label, pattern, new, src):
    m = re.search(pattern, src, re.DOTALL)
    if not m:
        print(f'  MISS  {label}')
        return src, False
    r = src[:m.start()] + new + src[m.end():]
    print(f'  OK    {label}')
    return r, True

# ════════════════════════════════════════════════════════════════════════════
# 1. CSS — adicionar classes para barras horizontais, tooltip, tabela
# ════════════════════════════════════════════════════════════════════════════
print('\n=== 1. CSS ===')

CSS_NEW = """.mso2-br{position:relative;padding:10px 16px;background:rgba(255,255,255,0.025);border-radius:10px;border:0.5px solid rgba(255,255,255,0.06);transition:background 0.15s,border-color 0.15s;}
.mso2-br:hover{background:rgba(255,255,255,0.05);border-color:rgba(255,255,255,0.14);}
.mso2-br-head{display:flex;align-items:center;gap:8px;margin-bottom:7px;}
.mso2-delta-badge{margin-left:auto;font-size:10px;font-weight:700;padding:2px 9px;border-radius:20px;letter-spacing:0.04em;flex-shrink:0;}
.mso2-bar-row{display:flex;align-items:center;gap:10px;margin-bottom:3px;}
.mso2-bar-yr{font-size:9px;font-weight:700;letter-spacing:0.07em;color:#4a5568;width:30px;flex-shrink:0;}
.mso2-yr26{color:#fbbf24!important;}
.mso2-bar-track{flex:1;height:7px;background:rgba(255,255,255,0.06);border-radius:3px;overflow:hidden;}
.mso2-bar-fill{height:100%;border-radius:3px;transition:width 0.55s cubic-bezier(.4,0,.2,1);}
.mso2-fill25{background:rgba(148,163,184,0.18);border:1px solid rgba(148,163,184,0.28);}
.mso2-bar-val{font-size:11px;font-weight:600;color:#64748b;width:64px;text-align:right;flex-shrink:0;}
.mso2-bval26{color:#e2e8f0!important;font-weight:700!important;}
.mso2-tooltip{display:none;position:absolute;right:8px;top:4px;z-index:200;background:#0c1824;border:0.5px solid rgba(251,191,36,0.25);border-radius:10px;padding:10px 14px;min-width:195px;box-shadow:0 8px 32px rgba(0,0,0,0.65);}
.mso2-br:hover .mso2-tooltip{display:block;}
.mso2-tip-row{display:flex;justify-content:space-between;align-items:center;gap:12px;font-size:10px;padding:1px 0;}
.mso2-tip-lbl{color:#64748b;}
.mso2-tip-val{font-weight:600;color:#cbd5e1;}
.mso2-tbl{width:100%;border-collapse:collapse;font-size:11px;}
.mso2-th{padding:5px 10px;text-align:center;font-size:9px;font-weight:700;letter-spacing:0.08em;color:#64748b;border-bottom:0.5px solid rgba(255,255,255,0.07);white-space:nowrap;}
.mso2-th:first-child{text-align:left;padding-left:4px;}
.mso2-tc{padding:5px 10px;text-align:center;border-bottom:0.5px solid rgba(255,255,255,0.04);}
.mso2-tc:first-child{text-align:left;padding-left:4px;}"""

CSS_ANCHOR = '.cmp-col{flex:1;min-width:0;}'
c, ok = patch_str('CSS mso2 classes', CSS_ANCHOR, CSS_ANCHOR + '\n' + CSS_NEW, c)
if not ok: sys.exit(1)
ok_count += 1

# ════════════════════════════════════════════════════════════════════════════
# 2. HTML — substituir corpo do card (manter header/select, trocar conteúdo)
# ════════════════════════════════════════════════════════════════════════════
print('\n=== 2. HTML card body ===')

NEW_CARD_BODY = """    <!-- Headline diagnóstico -->
    <div id="mso2-headline" style="font-size:12px;color:#D1D5DB;margin-bottom:16px;line-height:1.8;padding:10px 16px;background:rgba(251,191,36,0.05);border-radius:8px;border-left:3px solid #fbbf24;"></div>

    <!-- Barras horizontais comparativas -->
    <div id="mso2-bars" style="display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:18px;"></div>

    <!-- Tabela mensal YoY -->
    <div style="background:rgba(255,255,255,0.02);border-radius:10px;padding:14px 16px;margin-bottom:16px;border:0.5px solid rgba(255,255,255,0.06);">
      <div style="font-size:9px;font-weight:700;letter-spacing:0.1em;color:#64748b;margin-bottom:10px;" id="mso2-table-title">VARIAÇÃO YoY — JAN · FEV · MAR</div>
      <div id="mso2-table"></div>
    </div>

    <!-- Diagnóstico automático -->
    <div id="mso2-insight" style="padding:12px 16px;background:rgba(255,255,255,0.03);border-radius:8px;border-left:3px solid rgba(251,191,36,0.35);font-size:11px;color:#D1D5DB;line-height:1.7;"></div>
    <div style="font-size:9px;color:#3d4451;margin-top:12px;padding-top:8px;border-top:0.5px solid rgba(255,255,255,0.04);">
      Fonte: NielsenIQ Retail Measurement · PS - GBL - SC JOHNSON - BR - PEST CONTROL · Exportado: 23 mar 2026
    </div>
  </div>"""

c, ok = patch_re(
    'HTML card inner content',
    r'    <!-- Headline diagnóstico -->.*?(?=\n\n<!-- MARKET SHARE POR SKU -->)',
    NEW_CARD_BODY,
    c
)
if not ok: sys.exit(1)
ok_count += 1

# ════════════════════════════════════════════════════════════════════════════
# 3. JS — substituir renderMSO2() completo
# ════════════════════════════════════════════════════════════════════════════
print('\n=== 3. JS renderMSO2 ===')

NEW_RENDER_MSO2 = """function renderMSO2(){
  var sel = document.getElementById('mso2MarketSel') || document.getElementById('msoMarketSel');
  var mkt = sel ? sel.value : 'Farma Sul';
  var isShare = mso2Mode === 'share';
  var isVal   = mso2Mode === 'val';
  var isUn    = mso2Mode === 'un';

  // Limpar Chart.js legados (T8)
  if(mso2BarChart){ try{mso2BarChart.destroy();}catch(e){} mso2BarChart = null; }
  if(mso2LineChart){ try{mso2LineChart.destroy();}catch(e){} mso2LineChart = null; }

  // Atualizar labels
  var lbl = document.getElementById('mso2-mkt-lbl');
  if(lbl) lbl.textContent = mkt;
  var titleEl = document.getElementById('mso2-card-title');
  if(titleEl) titleEl.textContent = isShare ? 'MARKET SHARE — JAN · FEV · MAR'
    : (isVal ? 'VENDA VALOR — JAN · FEV · MAR' : 'UNIDADES — JAN · FEV · MAR');
  var subEl = document.getElementById('mso2-card-sub');
  if(subEl) subEl.innerHTML = (isShare ? 'Acum Jan-Mar/25 vs Jan-Mar/26'
    : (isVal ? 'R$ MM · Jan-Mar/26' : 'Unidades · Jan-Mar/26'))
    + ' · OFF! · EXPOSIS · XO INSETO · SUPER REPELEX · SBP · <span id="mso2-mkt-lbl">' + mkt + '</span>';

  var brands = MSO_BRANDS;
  var colors = MSO_COLORS;

  /* ── HEADLINE ── */
  var hdEl = document.getElementById('mso2-headline');
  if(hdEl){
    if(isShare){
      var dH = MKTSHARE_OVERVIEW[mkt];
      if(!dH){ hdEl.innerHTML = ''; }
      else {
        var offH = dH['OFF!'], expH = dH['EXPOSIS'];
        var lbsCfg = [{lb:'Jan',p25:'jan25',i26:6},{lb:'Fev',p25:'feb25',i26:7},{lb:'Mar',p25:'mar25',i26:8}];
        var parts = ['<strong style="color:#e2e8f0;">' + mkt + '</strong>'];
        lbsCfg.forEach(function(ci){
          var o25 = offH[ci.p25]!=null?offH[ci.p25]:offH.fytd25, e25 = expH[ci.p25]!=null?expH[ci.p25]:expH.fytd25;
          var scj26 = Math.round((offH.monthly[ci.i26]+expH.monthly[ci.i26])*10)/10;
          var scj25 = Math.round((o25+e25)*10)/10;
          var ds = Math.round((scj26-scj25)*10)/10;
          parts.push('SCJ Combined ' + ci.lb + '/26: <span style="color:#fbbf24;font-weight:700;">' + scj26 + '%</span>'
            + ' <span style="color:' + (ds>=0?'#34d399':'#ef4444') + ';font-size:11px;">' + (ds>=0?'▲':'▼') + Math.abs(ds).toFixed(1) + 'pp vs ' + ci.lb + '/25</span>');
        });
        var bPartsH = brands.map(function(b){
          var bd = dH[b]; if(!bd) return '';
          var segs = lbsCfg.map(function(ci){
            var v25 = bd[ci.p25]!=null?bd[ci.p25]:bd.fytd25, v26 = bd.monthly[ci.i26];
            var dv = Math.round((v26-v25)*100)/100;
            return ci.lb + '<span style="color:' + (dv>=0?'#34d399':'#ef4444') + ';">' + (dv>=0?'+':'') + dv.toFixed(2) + 'pp</span>';
          });
          return '<span style="color:' + colors[b] + ';font-weight:700;">' + b + '</span> ' + segs.join(' ');
        }).filter(Boolean);
        hdEl.innerHTML = parts.join('  |  ')
          + '<br><span style="font-size:11px;color:#94A3B8;">YoY:  </span>' + bPartsH.join('  ·  ');
      }
    } else {
      var nbvH = (typeof NIELSEN_BRAND_VAL !== 'undefined') ? NIELSEN_BRAND_VAL[mkt] : null;
      if(!nbvH){ hdEl.innerHTML = '<span style="color:#64748b;">Dados não disponíveis para este mercado.</span>'; }
      else {
        function pctHlFmt(v26, v25){ var p = v25>0 ? Math.round((v26-v25)/v25*1000)/10 : 0; return (p>=0?'<span style="color:#34d399;">▲ +':'<span style="color:#ef4444;">▼ ') + Math.abs(p).toFixed(1) + '%</span>'; }
        var bPartsHV = brands.map(function(b){
          var bd = nbvH[b]; if(!bd) return '';
          var f25 = isVal?bd.fytd25_val:bd.fytd25_un, f26 = isVal?bd.fytd26_val:bd.fytd26_un;
          return '<span style="color:' + colors[b] + ';font-weight:700;">' + b + '</span> ' + pctHlFmt(f26, f25);
        }).filter(Boolean);
        hdEl.innerHTML = '<strong style="color:#e2e8f0;">' + mkt + '</strong>'
          + ' · <span style="font-size:11px;color:#94A3B8;">' + (isVal?'R$ MM':'Unidades') + ' Jul-Mar YoY: </span>'
          + bPartsHV.join('  ·  ');
      }
    }
  }

  /* ── BUILD VALUE SETS ── */
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
    GrowthMode = true;
    brands.forEach(function(b){
      var bd = nbvS[b]; if(!bd) return;
      var j26 = isVal?bd.jan_val:bd.jan_un, f26 = isVal?bd.fev_val:bd.fev_un, m26 = isVal?bd.mar_val:bd.mar_un;
      var fyt25 = isVal?bd.fytd25_val:bd.fytd25_un, fyt26 = isVal?bd.fytd26_val:bd.fytd26_un;
      var a26 = Math.round((j26+f26+m26)*100)/100;
      var ratio = fyt26>0 ? a26/fyt26 : 1/3;
      var a25 = Math.round(fyt25*ratio*100)/100;
      d25[b] = {jan:null, fev:null, mar:null, acum:a25, fytd25:fyt25, fytd26:fyt26};
      d26[b] = {jan:j26, fev:f26, mar:m26, acum:a26};
    });
  }

  /* ── HELPERS ── */
  function fmtV(v){
    if(v===null||v===undefined) return '—';
    if(isShare) return v.toFixed(2)+'%';
    if(isVal) return v>=1?'R$'+v.toFixed(2)+'MM':'R$'+(v*1000).toFixed(0)+'K';
    return v>=1000?(Math.round(v/1000*10)/10)+'MM un':Math.round(v)+'K un';
  }
  function calcDelta(v25, v26){
    if(isShare){
      var d = Math.round((v26-v25)*100)/100;
      return {str:(d>=0?'+':'')+d.toFixed(2)+'pp', col:d>=0?'#34d399':'#ef4444', up:d>=0, raw:d};
    } else {
      var p = v25>0 ? Math.round((v26-v25)/v25*1000)/10 : 0;
      return {str:(p>=0?'+':'')+p.toFixed(1)+'%', col:p>=0?'#34d399':'#ef4444', up:p>=0, raw:p};
    }
  }

  /* ── MAX VALUE FOR BAR SCALING ── */
  var allV = [];
  brands.forEach(function(b){ if(d25[b]) allV.push(d25[b].acum); if(d26[b]) allV.push(d26[b].acum); });
  var maxV = Math.max.apply(null, allV) || 1;

  /* ── HORIZONTAL BARS ── */
  var barsEl = document.getElementById('mso2-bars');
  if(barsEl){
    barsEl.innerHTML = brands.map(function(b){
      var p25 = d25[b], p26 = d26[b]; if(!p25||!p26) return '';
      var cor = colors[b]||'#e2e8f0';
      var delta = calcDelta(p25.acum, p26.acum);
      var w25 = Math.max(2, Math.round(p25.acum/maxV*80));
      var w26 = Math.max(2, Math.round(p26.acum/maxV*80));
      var arrow = delta.up ? '↑' : '↓';

      /* tooltip */
      var tipRows = '';
      if(isShare){
        tipRows = '<div class="mso2-tip-row"><span class="mso2-tip-lbl">2025 (média Acum)</span><span class="mso2-tip-val">'+fmtV(p25.acum)+'</span></div>'
          +'<div class="mso2-tip-row"><span class="mso2-tip-lbl">2026 (média Acum)</span><span style="font-weight:700;color:'+cor+';">'+fmtV(p26.acum)+'</span></div>'
          +'<div class="mso2-tip-row"><span class="mso2-tip-lbl">Delta Acum</span><span style="font-weight:700;color:'+delta.col+';">'+arrow+' '+delta.str+'</span></div>'
          +'<div style="height:1px;background:rgba(255,255,255,0.07);margin:5px 0;"></div>'
          +'<div class="mso2-tip-row"><span class="mso2-tip-lbl">Jan/25</span><span class="mso2-tip-val">'+fmtV(p25.jan)+'</span></div>'
          +'<div class="mso2-tip-row"><span class="mso2-tip-lbl">Jan/26</span><span style="color:'+cor+';font-weight:700;">'+fmtV(p26.jan)+'</span></div>'
          +'<div class="mso2-tip-row"><span class="mso2-tip-lbl">Fev/25</span><span class="mso2-tip-val">'+fmtV(p25.fev)+'</span></div>'
          +'<div class="mso2-tip-row"><span class="mso2-tip-lbl">Fev/26</span><span style="color:'+cor+';font-weight:700;">'+fmtV(p26.fev)+'</span></div>'
          +'<div class="mso2-tip-row"><span class="mso2-tip-lbl">Mar/25</span><span class="mso2-tip-val">'+fmtV(p25.mar)+'</span></div>'
          +'<div class="mso2-tip-row"><span class="mso2-tip-lbl">Mar/26</span><span style="color:'+cor+';font-weight:700;">'+fmtV(p26.mar)+'</span></div>';
      } else {
        var pJulMar = p25.fytd25>0 ? Math.round((p26.acum - (p25.fytd25*(p26.acum/p26.acum||1)))/1*100)/100 : 0;
        var fytPct = p25.fytd25>0 ? Math.round((p25.fytd26||p26.acum*(p25.fytd25>0?1:1)-p25.fytd25)/p25.fytd25*1000)/10 : 0;
        var nbvTp = (typeof NIELSEN_BRAND_VAL !== 'undefined') ? NIELSEN_BRAND_VAL[mkt] : null;
        var fyt25v = nbvTp&&nbvTp[b] ? (isVal?nbvTp[b].fytd25_val:nbvTp[b].fytd25_un) : 0;
        var fyt26v = nbvTp&&nbvTp[b] ? (isVal?nbvTp[b].fytd26_val:nbvTp[b].fytd26_un) : 0;
        var fytD = calcDelta(fyt25v, fyt26v);
        tipRows = '<div class="mso2-tip-row"><span class="mso2-tip-lbl">Jan/26</span><span style="color:'+cor+';font-weight:700;">'+fmtV(p26.jan||0)+'</span></div>'
          +'<div class="mso2-tip-row"><span class="mso2-tip-lbl">Fev/26</span><span style="color:'+cor+';font-weight:700;">'+fmtV(p26.fev||0)+'</span></div>'
          +'<div class="mso2-tip-row"><span class="mso2-tip-lbl">Mar/26</span><span style="color:'+cor+';font-weight:700;">'+fmtV(p26.mar||0)+'</span></div>'
          +'<div style="height:1px;background:rgba(255,255,255,0.07);margin:5px 0;"></div>'
          +'<div class="mso2-tip-row"><span class="mso2-tip-lbl">Jul-Mar/25</span><span class="mso2-tip-val">'+fmtV(fyt25v)+'</span></div>'
          +'<div class="mso2-tip-row"><span class="mso2-tip-lbl">Jul-Mar/26</span><span style="color:'+cor+';font-weight:700;">'+fmtV(fyt26v)+'</span></div>'
          +'<div class="mso2-tip-row"><span class="mso2-tip-lbl">Δ Jul-Mar</span><span style="font-weight:700;color:'+fytD.col+';">'+(fytD.up?'↑ ':'↓ ')+fytD.str+'</span></div>';
      }

      return '<div class="mso2-br">'
        +'<div class="mso2-br-head">'
        +'<span style="display:inline-block;width:9px;height:9px;border-radius:50%;background:'+cor+';box-shadow:0 0 7px '+cor+'99;flex-shrink:0;"></span>'
        +'<span style="font-size:12px;font-weight:700;color:#e2e8f0;letter-spacing:0.03em;">'+b+'</span>'
        +'<span class="mso2-delta-badge" style="color:'+delta.col+';background:'+delta.col+'14;border-color:'+delta.col+'40;">'
        +arrow+' '+delta.str+'</span>'
        +'</div>'
        +'<div class="mso2-bar-row">'
        +'<span class="mso2-bar-yr">2025</span>'
        +'<div class="mso2-bar-track"><div class="mso2-bar-fill mso2-fill25" style="width:'+w25+'%"></div></div>'
        +'<span class="mso2-bar-val">'+fmtV(p25.acum)+'</span>'
        +'</div>'
        +'<div class="mso2-bar-row">'
        +'<span class="mso2-bar-yr mso2-yr26">2026</span>'
        +'<div class="mso2-bar-track"><div class="mso2-bar-fill" style="width:'+w26+'%;background:'+cor+'cc;box-shadow:0 0 8px '+cor+'44;border-right:2px solid '+cor+';"></div></div>'
        +'<span class="mso2-bar-val mso2-bval26" style="color:'+cor+';">'+fmtV(p26.acum)+'</span>'
        +'</div>'
        +'<div class="mso2-tooltip">'
        +'<div style="font-size:10px;font-weight:700;color:'+cor+';margin-bottom:6px;letter-spacing:0.05em;border-bottom:0.5px solid rgba(255,255,255,0.08);padding-bottom:5px;">'+b+'</div>'
        +tipRows
        +'</div>'
        +'</div>';
    }).join('');
  }

  /* ── MONTHLY TABLE ── */
  var tableEl = document.getElementById('mso2-table');
  var tblTitleEl = document.getElementById('mso2-table-title');
  if(tblTitleEl) tblTitleEl.textContent = isShare
    ? 'VARIAÇÃO YoY (pp) — JAN · FEV · MAR'
    : 'PERFORMANCE MENSAL — JAN · FEV · MAR';

  if(tableEl){
    var hds = isShare
      ? ['MARCA','JAN (pp)','FEV (pp)','MAR (pp)','Δ ACUM']
      : ['MARCA','JAN/26','FEV/26','MAR/26','ACUM/26','Δ Jul-Mar'];

    function ppCell(v25, v26){
      var dv = Math.round((v26-v25)*100)/100;
      var cc = dv>=0?'#34d399':'#ef4444';
      return '<td class="mso2-tc" style="color:'+cc+';font-weight:700;">'+(dv>=0?'+':'')+dv.toFixed(2)+'pp</td>';
    }

    var rows = brands.map(function(b){
      var p25 = d25[b], p26 = d26[b]; if(!p25||!p26) return '';
      var cor = colors[b]||'#e2e8f0';
      var delta = calcDelta(p25.acum, p26.acum);
      var arrowT = delta.up ? '↑' : '↓';

      if(isShare){
        return '<tr>'
          +'<td class="mso2-tc"><span style="color:'+cor+';font-weight:700;font-size:10px;letter-spacing:0.03em;">'+b+'</span></td>'
          +ppCell(p25.jan, p26.jan)
          +ppCell(p25.fev, p26.fev)
          +ppCell(p25.mar, p26.mar)
          +'<td class="mso2-tc" style="color:'+delta.col+';font-weight:700;">'+arrowT+' '+delta.str+'</td>'
          +'</tr>';
      } else {
        return '<tr>'
          +'<td class="mso2-tc"><span style="color:'+cor+';font-weight:700;font-size:10px;letter-spacing:0.03em;">'+b+'</span></td>'
          +'<td class="mso2-tc" style="color:'+cor+';">'+fmtV(p26.jan||0)+'</td>'
          +'<td class="mso2-tc" style="color:'+cor+';">'+fmtV(p26.fev||0)+'</td>'
          +'<td class="mso2-tc" style="color:'+cor+';">'+fmtV(p26.mar||0)+'</td>'
          +'<td class="mso2-tc" style="color:'+cor+';font-weight:700;">'+fmtV(p26.acum)+'</td>'
          +'<td class="mso2-tc" style="color:'+delta.col+';font-weight:700;">'+arrowT+' '+delta.str+'</td>'
          +'</tr>';
      }
    }).join('');

    tableEl.innerHTML = '<table class="mso2-tbl"><thead><tr>'
      + hds.map(function(h,i){ return '<th class="mso2-th"' + (i===0?' style="text-align:left;"':'') + '>' + h + '</th>'; }).join('')
      + '</tr></thead><tbody>' + rows + '</tbody></table>'
      + (GrowthMode ? '<div style="font-size:9px;color:#3d4451;margin-top:5px;">★ Δ baseado em Jul-Mar (dados mensais 2025 R$/Un não disponíveis individualmente)</div>' : '');
  }

  renderMSO2Insight();
}"""

c, ok = patch_re(
    'JS renderMSO2()',
    r'function renderMSO2\(\)\{.*?renderMSO2Insight\(\);\n\}',
    NEW_RENDER_MSO2,
    c
)
if not ok: sys.exit(1)
ok_count += 1

# ════════════════════════════════════════════════════════════════════════════
# 4. JS — substituir renderMSO2Insight() atualizado
# ════════════════════════════════════════════════════════════════════════════
print('\n=== 4. JS renderMSO2Insight ===')

NEW_MSO2_INSIGHT = """// ── MSO2: Diagnóstico automático JAN-MAR YoY ──
function renderMSO2Insight(){
  var el = document.getElementById('mso2-insight');
  if(!el) return;
  var sel = document.getElementById('mso2MarketSel') || document.getElementById('msoMarketSel');
  var mkt = sel ? sel.value : 'Farma Sul';

  function col(v){ return v>=0?'#34d399':'#ef4444'; }
  function sig(v){ return v>=0?'+':''; }
  function arrow(v){ return v>=0?'▲ +':'▼ '; }

  if(typeof mso2Mode === 'undefined' || mso2Mode === 'share'){
    var d = MKTSHARE_OVERVIEW[mkt]; if(!d) return;
    var off = d['OFF!'], exp = d['EXPOSIS'], xo = d['XO INSETO'], sr = d['SUPER REPELEX'];
    if(!off||!exp||!xo||!sr) return;

    var oj25=off.jan25!=null?off.jan25:off.fytd25, of25=off.feb25!=null?off.feb25:off.fytd25, om25=off.mar25!=null?off.mar25:off.fytd25;
    var ej25=exp.jan25!=null?exp.jan25:exp.fytd25, ef25=exp.feb25!=null?exp.feb25:exp.fytd25, em25=exp.mar25!=null?exp.mar25:exp.fytd25;
    var xj25=xo.jan25!=null?xo.jan25:xo.fytd25,  xf25=xo.feb25!=null?xo.feb25:xo.fytd25,  xm25=xo.mar25!=null?xo.mar25:xo.fytd25;
    var sj25=sr.jan25!=null?sr.jan25:sr.fytd25,   sf25=sr.feb25!=null?sr.feb25:sr.fytd25,   sm25=sr.mar25!=null?sr.mar25:sr.fytd25;
    var oj26=off.monthly[6], of26=off.monthly[7], om26=off.monthly[8];
    var ej26=exp.monthly[6], ef26=exp.monthly[7], em26=exp.monthly[8];
    var xj26=xo.monthly[6],  xf26=xo.monthly[7],  xm26=xo.monthly[8];
    var sj26=sr.monthly[6],  sf26=sr.monthly[7],  sm26=sr.monthly[8];

    // Acumulado (média Jan-Mar)
    var offAcum25=Math.round((oj25+of25+om25)/3*100)/100, offAcum26=Math.round((oj26+of26+om26)/3*100)/100;
    var xoAcum25=Math.round((xj25+xf25+xm25)/3*100)/100,  xoAcum26=Math.round((xj26+xf26+xm26)/3*100)/100;
    var expAcum25=Math.round((ej25+ef25+em25)/3*100)/100,  expAcum26=Math.round((ej26+ef26+em26)/3*100)/100;
    var srAcum25=Math.round((sj25+sf25+sm25)/3*100)/100,   srAcum26=Math.round((sj26+sf26+sm26)/3*100)/100;
    var offDA=Math.round((offAcum26-offAcum25)*100)/100;
    var xoDA=Math.round((xoAcum26-xoAcum25)*100)/100;
    var expDA=Math.round((expAcum26-expAcum25)*100)/100;
    var srDA=Math.round((srAcum26-srAcum25)*100)/100;
    var scjA25=Math.round((offAcum25+expAcum25)*10)/10, scjA26=Math.round((offAcum26+expAcum26)*10)/10;
    var scjDA=Math.round((scjA26-scjA25)*10)/10;

    // Diagnóstico inteligente
    var allDeltas=[{b:'OFF!',d:offDA,c:'#fbbf24'},{b:'XO INSETO',d:xoDA,c:'#ef4444'},{b:'EXPOSIS',d:expDA,c:'#3b82f6'},{b:'SUPER REPELEX',d:srDA,c:'#f97316'}];
    allDeltas.sort(function(a,b){return b.d-a.d;});
    var leader=allDeltas[0], laggard=allDeltas[allDeltas.length-1];

    var lines=[
      '🏆 <strong style="color:#fbbf24;">SCJ Combined</strong> (OFF!+EXPOSIS): Acum Jan-Mar/26 <strong style="color:'+col(scjDA)+';">'
        +scjA26+'%</strong> <span style="color:'+col(scjDA)+';font-size:10px;">'+arrow(scjDA)+Math.abs(scjDA).toFixed(1)+'pp vs /25</span>'
        +' (Jan: '+col(Math.round((oj26+ej26)-(oj25+ej25)*10)/10)+')</span>',
      '📦 <strong style="color:#fbbf24;">OFF!</strong> Jan/26: <strong style="color:'+col(Math.round((oj26-oj25)*100)/100)+';">'+oj26+'%</strong> '
        +'Fev/26: <strong style="color:'+col(Math.round((of26-of25)*100)/100)+';">'+of26+'%</strong> '
        +'Mar/26: <strong style="color:'+col(Math.round((om26-om25)*100)/100)+';">'+om26+'%</strong>'
        +' — Acum: <strong style="color:'+col(offDA)+';">'+sig(offDA)+offDA.toFixed(2)+'pp</strong>.',
      '🔴 <strong style="color:#ef4444;">XO INSETO</strong> Jan/26: <strong style="color:'+col(Math.round((xj26-xj25)*100)/100)+';">'+xj26+'%</strong> '
        +'Fev/26: <strong style="color:'+col(Math.round((xf26-xf25)*100)/100)+';">'+xf26+'%</strong> '
        +'Mar/26: <strong style="color:'+col(Math.round((xm26-xm25)*100)/100)+';">'+xm26+'%</strong>'
        +((xoDA>0&&xoDA>0)?' — <strong style="color:#06b6d4;">concorrente em expansão.</strong>':' — cedendo espaço YoY.'),
    ];

    // Linha diagnóstico final
    var diagFinal = leader.d>0
      ? '🚀 <strong style="color:'+leader.c+';">'+leader.b+'</strong> lidera crescimento acumulado no período Jan-Mar/2026 em <strong style="color:#e2e8f0;">'+mkt+'</strong>.'
      : '⚠️ Todas as marcas monitoradas perdem share no acumulado Jan-Mar/2026.';
    if(laggard.d<0 && laggard.b!==leader.b)
      diagFinal += ' <span style="color:#64748b;">·</span> ⚠️ <strong style="color:'+laggard.c+';">'+laggard.b+'</strong> registra maior retração ('+(laggard.d.toFixed(2))+'pp).';
    lines.push(diagFinal);

    el.innerHTML = '<strong style="color:#fbbf24;font-size:10px;letter-spacing:0.08em;">📊 DIAGNÓSTICO — '+mkt+'  ·  Calendário Gregoriano Jan·Fev·Mar</strong><br>'
      + lines.join('<br>');
    return;
  }

  /* ── R$ MM / UNIDADES MODE ── */
  var nbvI = (typeof NIELSEN_BRAND_VAL !== 'undefined') ? NIELSEN_BRAND_VAL[mkt] : null;
  if(!nbvI) return;
  var isValI = mso2Mode === 'val';
  var unitLbl = isValI ? 'R$ MM' : 'Unidades';
  function fmtNI(v){ if(isValI) return v>=1?'R$'+v.toFixed(2)+'MM':'R$'+(v*1000).toFixed(0)+'K'; return Math.round(v).toLocaleString('pt-BR')+'K'; }
  function pctI(v26,v25){ return v25>0?Math.round((v26-v25)/v25*1000)/10:0; }

  var MSO_EMOJIS = {'OFF!':'📦','EXPOSIS':'🟡','XO INSETO':'🔴','SUPER REPELEX':'🔵','SBP':'🟠'};
  var lines2 = MSO_BRANDS.map(function(b){
    var bd=nbvI[b]; if(!bd) return '';
    var cor=MSO_COLORS[b]||'#e2e8f0';
    var f25=isValI?bd.fytd25_val:bd.fytd25_un, f26=isValI?bd.fytd26_val:bd.fytd26_un;
    var j26=isValI?bd.jan_val:bd.jan_un, fv26=isValI?bd.fev_val:bd.fev_un, m26=isValI?bd.mar_val:bd.mar_un;
    var p=pctI(f26,f25);
    var cc=p>=0?'#34d399':'#ef4444';
    return (MSO_EMOJIS[b]||'▪') + ' <strong style="color:'+cor+';">'+b+'</strong>'
      +' Jan: <strong style="color:'+cor+';">'+fmtNI(j26)+'</strong>'
      +' · Fev: <strong style="color:'+cor+';">'+fmtNI(fv26)+'</strong>'
      +' · Mar: <strong style="color:'+cor+';">'+fmtNI(m26)+'</strong>'
      +'  ·  Jul-Mar/25: '+fmtNI(f25)
      +' → Jul-Mar/26: <strong style="color:'+cor+';">'+fmtNI(f26)+'</strong>'
      +' <span style="color:'+cc+';font-weight:700;">'+(p>=0?'▲ +':'▼ ')+Math.abs(p).toFixed(1)+'%</span>';
  }).filter(Boolean);

  el.innerHTML = '<strong style="color:#fbbf24;font-size:10px;letter-spacing:0.08em;">📊 DIAGNÓSTICO — '+mkt+'  ·  '+unitLbl+' Jan·Fev·Mar/26</strong><br>'
    + lines2.join('<br>');
}"""

c, ok = patch_re(
    'JS renderMSO2Insight()',
    r'// ── MSO2: Jan/Fev YoY insight ──\nfunction renderMSO2Insight\(\)\{.*?\n\}(?=\n\n// ── Avg Price)',
    NEW_MSO2_INSIGHT,
    c
)
if not ok: sys.exit(1)
ok_count += 1

# ════════════════════════════════════════════════════════════════════════════
# Write
# ════════════════════════════════════════════════════════════════════════════
with open(OUT, 'w', encoding='utf-8') as f:
    f.write(c)
shutil.copy2(OUT, SRC)
print(f'\n  Copied to active: {os.path.basename(SRC)}')

new_lines = len(c.splitlines())
delta = new_lines - orig_lines
print(f'\nLinhas: {orig_lines} → {new_lines} ({delta:+d})')
print(f'Patches OK: {ok_count}/4')
print(f'Versão: {os.path.basename(OUT)}')

# ── Verify ──────────────────────────────────────────────────────────────────
print()
checks = [
    ('CSS .mso2-br',           '.mso2-br{position:relative'),
    ('CSS .mso2-tooltip',      '.mso2-tooltip{display:none'),
    ('CSS .mso2-tbl',          '.mso2-tbl{width:100%'),
    ('HTML mso2-bars',         'id="mso2-bars"'),
    ('HTML mso2-table',        'id="mso2-table"'),
    ('HTML mso2-table-title',  'id="mso2-table-title"'),
    ('HTML mso2-insight',      'id="mso2-insight"'),
    ('JS renderMSO2',          'function renderMSO2(){'),
    ('JS renderMSO2Insight',   'function renderMSO2Insight(){'),
    ('JS mso2-bars innerHTML', "document.getElementById('mso2-bars')"),
    ('JS mso2-table innerHTML',"document.getElementById('mso2-table')"),
    ('JS calcDelta',           'function calcDelta('),
    ('JS GrowthMode',          'var GrowthMode = false'),
    ('JS destroy legacy',      'mso2BarChart.destroy()'),
    ('NO mso2-bar canvas',     'id="mso2-bar"'),
    ('NO mso2-line canvas',    'id="mso2-line"'),
]
for label, needle in checks:
    if label.startswith('NO '):
        found = needle not in c
        print(f"  {'OK  ' if found else 'FAIL'} (absent) {label[3:]}")
    else:
        found = needle in c
        print(f"  {'OK  ' if found else 'FAIL'}  {label}")
