"""
PATCH 18 — Card 2 ($ Share por Marca — Jan·Fev·Mar·Abr): seção expansível "Análise Curto Prazo"
Espelha patch17, mas usando ids: shr-st-wrap2 / shr-st-table2 / shr-st-btn2
Hook: ao final de renderMSO2() após renderMSO2Insight()
"""

import datetime

SRC = r'Dashboard_farma_sul\Dashboard_Farma_Sul_20260512_2220.html'

html = open(SRC, encoding='utf-8').read()
original_len = len(html)
patches = 0

# ─── 1. HTML: adicionar container após mso2-insight ──────────────────────────
ST2_HTML = '''<div id="shr-st-wrap2" style="margin:0 24px 14px;padding-top:10px;border-top:1px solid rgba(255,255,255,0.06);display:none;">
  <button id="shr-st-btn2" onclick="toggleShrST2()" style="background:none;border:1px solid rgba(255,255,255,0.12);color:#94a3b8;font-size:11px;padding:5px 14px;border-radius:6px;cursor:pointer;font-family:inherit;letter-spacing:.04em;transition:color .15s;">&#9658; Análise Curto Prazo</button>
  <div id="shr-st-table2" style="display:none;margin-top:10px;overflow-x:auto;"></div>
</div>'''

OLD_HTML2 = '<div style="padding:0 24px 16px;"><div id="mso2-insight"></div></div>'
NEW_HTML2 = OLD_HTML2 + '\n    ' + ST2_HTML

if OLD_HTML2 in html:
    html = html.replace(OLD_HTML2, NEW_HTML2, 1)
    patches += 1
    print('[OK] HTML: container shr-st-wrap2 inserido após mso2-insight')
else:
    print('[MISS] HTML: mso2-insight container não encontrado')

# ─── 2. JS: chamar renderShrShortTerm2 ao final de renderMSO2() ──────────────
OLD_MSO2_END = '''  renderMSO2Insight();
}

/* ═══════════ MSO ÁREA ═══════════ */'''

NEW_MSO2_END = '''  renderMSO2Insight();
  if(typeof renderShrShortTerm2==='function') renderShrShortTerm2(mkt);
}

/* ═══════════ MSO ÁREA ═══════════ */'''

if OLD_MSO2_END in html:
    html = html.replace(OLD_MSO2_END, NEW_MSO2_END, 1)
    patches += 1
    print('[OK] JS: renderShrShortTerm2 chamada no final de renderMSO2()')
else:
    print('[MISS] JS: fim de renderMSO2() não encontrado')

# ─── 3. JS: adicionar funções renderShrShortTerm2 + toggleShrST2 ─────────────
NEW_FUNCS2 = r"""
/* ═══════════ CURTO PRAZO — Card 2 (Jan·Fev·Mar·Abr) ═══════════ */
function renderShrShortTerm2(mkt){
  var wrap=document.getElementById('shr-st-wrap2');
  if(!wrap)return;
  var d=SHR_TREND_DATA[mkt];
  if(!d){wrap.style.display='none';return;}
  wrap.style.display='block';
  var brands=['OFF!','EXPOSIS','XO INSETO','SUPER REPELEX','SBP'];
  function gv(br,idx){var bd=d[br];if(!bd||!bd.fy26)return null;return bd.fy26[idx]!=null?bd.fy26[idx]:null;}
  var ABR=9,MAR=8,FEV=7,JAN=6;
  function dc(v){return v==null?'#6b7280':(v>0?'#34d399':v<0?'#fb7185':'#94a3b8');}
  function fp(v){return v!=null?v.toFixed(2)+'%':'—';}
  function fd(v){if(v==null)return'—';return(v>=0?'+':'')+v.toFixed(2)+'pp';}
  var rows=brands.map(function(br){
    var a=gv(br,ABR),m=gv(br,MAR),f=gv(br,FEV),j=gv(br,JAN);
    var mom=(a!=null&&m!=null)?a-m:null;
    var bi26=(a!=null&&m!=null)?(a+m)/2:null;
    var bi25=(f!=null&&j!=null)?(f+j)/2:null;
    var d2m=(bi26!=null&&bi25!=null)?bi26-bi25:null;
    return{br:br,a:a,m:m,mom:mom,bi26:bi26,bi25:bi25,d2m:d2m};
  });
  // SCJ = OFF! + EXPOSIS
  var scja=0,scjm=0,scjf=0,scjj=0,ok=true;
  ['OFF!','EXPOSIS'].forEach(function(br){
    var a=gv(br,ABR),m=gv(br,MAR),f=gv(br,FEV),j=gv(br,JAN);
    if(a==null||m==null||f==null||j==null){ok=false;return;}
    scja+=a;scjm+=m;scjf+=f;scjj+=j;
  });
  if(ok){
    var smom=scja-scjm,sbi26=(scja+scjm)/2,sbi25=(scjf+scjj)/2,sd2m=sbi26-sbi25;
    rows.push({br:'SCJ (OFF!+EXPOSIS)',a:scja,m:scjm,mom:smom,bi26:sbi26,bi25:sbi25,d2m:sd2m,isSCJ:true});
  }
  var h='<table style="width:100%;border-collapse:collapse;font-size:11px;">';
  h+='<thead><tr style="border-bottom:1px solid rgba(255,255,255,0.1);">';
  h+='<th style="padding:5px 8px;text-align:left;color:#64748b;font-size:9px;font-weight:700;letter-spacing:.08em;">MARCA</th>';
  h+='<th style="padding:5px 8px;text-align:right;color:#fbbf24;font-size:9px;font-weight:700;">ABR/26</th>';
  h+='<th style="padding:5px 8px;text-align:right;color:#64748b;font-size:9px;font-weight:700;">MAR/26</th>';
  h+='<th style="padding:5px 8px;text-align:right;color:#e2e8f0;font-size:9px;font-weight:700;">Δ MoM</th>';
  h+='<th style="padding:5px 8px;text-align:right;color:#fbbf24;font-size:9px;font-weight:700;border-left:1px solid rgba(255,255,255,0.07);">Abr+Mar</th>';
  h+='<th style="padding:5px 8px;text-align:right;color:#64748b;font-size:9px;font-weight:700;">Fev+Jan</th>';
  h+='<th style="padding:5px 8px;text-align:right;color:#e2e8f0;font-size:9px;font-weight:700;">Δ 2M</th>';
  h+='</tr></thead><tbody>';
  rows.forEach(function(r){
    var scjStyle=r.isSCJ?'border-top:1px solid rgba(255,255,255,0.1);background:rgba(251,191,36,0.04);':'';
    var brc=r.isSCJ?'#fbbf24':(_shrBrandColors[r.br]||'#e2e8f0');
    h+='<tr style="'+scjStyle+'">';
    h+='<td style="padding:4px 8px;font-weight:700;color:'+brc+';font-size:11px;">'+r.br+'</td>';
    h+='<td style="padding:4px 8px;text-align:right;color:#e2e8f0;font-weight:700;">'+fp(r.a)+'</td>';
    h+='<td style="padding:4px 8px;text-align:right;color:#94a3b8;">'+fp(r.m)+'</td>';
    h+='<td style="padding:4px 8px;text-align:right;font-weight:800;color:'+dc(r.mom)+';">'+fd(r.mom)+'</td>';
    h+='<td style="padding:4px 8px;text-align:right;color:#e2e8f0;font-weight:700;border-left:1px solid rgba(255,255,255,0.07);">'+fp(r.bi26)+'</td>';
    h+='<td style="padding:4px 8px;text-align:right;color:#94a3b8;">'+fp(r.bi25)+'</td>';
    h+='<td style="padding:4px 8px;text-align:right;font-weight:800;color:'+dc(r.d2m)+';">'+fd(r.d2m)+'</td>';
    h+='</tr>';
  });
  h+='</tbody></table>';
  h+='<div style="font-size:9px;color:#475569;margin-top:6px;">Δ MoM = Abr/26 − Mar/26 &nbsp;|&nbsp; Δ 2M = média (Abr+Mar)/26 − média (Fev+Jan)/26</div>';
  var tEl=document.getElementById('shr-st-table2');
  if(tEl)tEl.innerHTML=h;
}
function toggleShrST2(){
  var t=document.getElementById('shr-st-table2');
  var btn=document.getElementById('shr-st-btn2');
  if(!t||!btn)return;
  var open=t.style.display!=='none';
  t.style.display=open?'none':'block';
  btn.innerHTML=open?'&#9658; Análise Curto Prazo':'&#9660; Análise Curto Prazo';
}
"""

# Inserir antes do bloco FYTD_MARKET_TOTAL
OLD_ANCHOR2 = '\nconst FYTD_MARKET_TOTAL = {'
if OLD_ANCHOR2 in html:
    html = html.replace(OLD_ANCHOR2, NEW_FUNCS2 + OLD_ANCHOR2, 1)
    patches += 1
    print('[OK] JS: funções renderShrShortTerm2 + toggleShrST2 inseridas')
else:
    print('[MISS] JS: âncora FYTD_MARKET_TOTAL não encontrada')

# ─── 4. Salvar ────────────────────────────────────────────────────────────────
print(f'\nPatches: {patches}/3')
print(f'Diff   : {len(html) - original_len:+,} bytes')

ts = datetime.datetime.now().strftime('%Y%m%d_%H%M')
ver = f'Dashboard_farma_sul/versoes/Dashboard_Farma_Sul_{ts}_Card2CurtoPrazo.html'
open(SRC, 'w', encoding='utf-8').write(html)
open(ver, 'w', encoding='utf-8').write(html)
print(f'\nSalvo : {SRC}')
print(f'Versao: {ver}')
