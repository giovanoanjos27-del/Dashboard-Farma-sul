"""
PATCH 17 — Market Share Overview: seção expansível "Análise Curto Prazo"
Opção 3: botão ▸/▾ que expande tabela com Abr vs Mar (MoM) e Abr+Mar vs Fev+Jan (2M)
"""

import datetime, re

SRC = r'Dashboard_farma_sul\Dashboard_Farma_Sul_20260512_2220.html'

html = open(SRC, encoding='utf-8').read()
original_len = len(html)
patches = 0

# ─── 1. HTML: adicionar container após mso-insight ───────────────────────────
ST_HTML = '''<div id="shr-st-wrap" style="margin-top:14px;padding-top:10px;border-top:1px solid rgba(255,255,255,0.06);display:none;">
  <button id="shr-st-btn" onclick="toggleShrST()" style="background:none;border:1px solid rgba(255,255,255,0.12);color:#94a3b8;font-size:11px;padding:5px 14px;border-radius:6px;cursor:pointer;font-family:inherit;letter-spacing:.04em;transition:color .15s;">&#9658; Análise Curto Prazo</button>
  <div id="shr-st-table" style="display:none;margin-top:10px;overflow-x:auto;"></div>
</div>'''

OLD_HTML = '<div id="mso-insight" style="margin-top:14px;padding:12px 16px;background:rgba(255,255,255,0.03);border-radius:8px;border-left:3px solid rgba(255,255,255,0.1);font-size:11px;color:#D1D5DB;line-height:1.7;"></div>'
NEW_HTML = OLD_HTML + '\n  ' + ST_HTML

if OLD_HTML in html:
    html = html.replace(OLD_HTML, NEW_HTML, 1)
    patches += 1
    print('[OK] HTML: container shr-st-wrap inserido após mso-insight')
else:
    print('[MISS] HTML: mso-insight não encontrado')

# ─── 2. JS: chamar renderShrShortTerm no final de renderShrTrend ──────────────
OLD_RT_END = '''      +(scjOk?'<div style="margin-top:8px;padding-top:8px;border-top:1px solid rgba(255,255,255,0.08);font-size:11px;">'\
        +'<span style="font-weight:700;color:#fbbf24;">SCJ Portfolio</span>'\
        +' <span style="color:#94A3B8;">(OFF! + EXPOSIS)</span>'\
        +' <span style="color:#e2e8f0;font-weight:700;margin:0 10px;">'+scj26.toFixed(2)+'%</span>'\
        +'<span style="font-weight:800;color:'+scjCol+';">'+scjStr+'</span>'\
        +'</div>':'');
  }
}'''

NEW_RT_END = OLD_RT_END.rstrip('}') + '''
  // ── Curto Prazo ──
  renderShrShortTerm(mkt);
}'''

if OLD_RT_END in html:
    html = html.replace(OLD_RT_END, NEW_RT_END, 1)
    patches += 1
    print('[OK] JS: renderShrShortTerm chamada no final de renderShrTrend')
else:
    # fallback: buscar pelo fechamento da função
    old2 = "      +(scjOk?'<div style=\"margin-top:8px;padding-top:8px;border-top:1px solid rgba(255,255,255,0.08);font-size:11px;\">'"
    pos = html.find(old2, 14070000)
    if pos != -1:
        end_if = html.find('\n  }\n}', pos)
        if end_if != -1:
            old3 = html[end_if:end_if+6]
            html = html[:end_if] + '\n  // ── Curto Prazo ──\n  renderShrShortTerm(mkt);\n  }\n}' + html[end_if+6:]
            patches += 1
            print('[OK] JS: renderShrShortTerm via fallback')
    else:
        print('[MISS] JS: ponto de inserção não encontrado')

# ─── 3. JS: adicionar funções renderShrShortTerm + toggleShrST ───────────────
NEW_FUNCS = r"""
/* ═══════════ CURTO PRAZO — Market Share ═══════════ */
function renderShrShortTerm(mkt){
  var wrap=document.getElementById('shr-st-wrap');
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
  var tEl=document.getElementById('shr-st-table');
  if(tEl)tEl.innerHTML=h;
}
function toggleShrST(){
  var t=document.getElementById('shr-st-table');
  var btn=document.getElementById('shr-st-btn');
  if(!t||!btn)return;
  var open=t.style.display!=='none';
  t.style.display=open?'none':'block';
  btn.innerHTML=open?'&#9658; Análise Curto Prazo':'&#9660; Análise Curto Prazo';
}
"""

# Inserir antes do bloco ANÁLISE POR MARCA
OLD_ANCHOR = '\n/* ═══════════ ANÁLISE POR MARCA ═══════════ */'
if OLD_ANCHOR in html:
    html = html.replace(OLD_ANCHOR, NEW_FUNCS + OLD_ANCHOR, 1)
    patches += 1
    print('[OK] JS: funções renderShrShortTerm + toggleShrST inseridas')
else:
    print('[MISS] JS: âncora ANÁLISE POR MARCA não encontrada')

# ─── 4. Salvar ────────────────────────────────────────────────────────────────
print(f'\nPatches: {patches}/3')
print(f'Diff   : {len(html) - original_len:+,} bytes')

ts = datetime.datetime.now().strftime('%Y%m%d_%H%M')
ver = f'Dashboard_farma_sul/versoes/Dashboard_Farma_Sul_{ts}_CurtoPrazo.html'
open(SRC, 'w', encoding='utf-8').write(html)
open(ver, 'w', encoding='utf-8').write(html)
print(f'\nSalvo : {SRC}')
print(f'Versao: {ver}')
