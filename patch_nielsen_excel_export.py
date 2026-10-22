"""
patch_nielsen_excel_export.py
Adiciona botão "📥 Exportar Nielsen Excel" na aba Nielsen.
Exporta arquivo .xlsx executivo com 5 abas formatadas (dark premium).
ExcelJS carregado via CDN apenas ao clicar (zero impacto no carregamento).
"""
import sys
from pathlib import Path
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

BASE = Path(r'C:\Users\valqu\OneDrive\Documentos\Claude\Projects\projeto Dashboard_farma_sul\Dashboard_farma_sul')
SRC  = BASE / 'Dashboard_Farma_Sul_20260512_2220.html'
VER  = BASE / 'versoes' / f'Dashboard_Farma_Sul_{datetime.now().strftime("%Y%m%d_%H%M")}_NielsenExport.html'

print('Lendo dashboard…')
h = SRC.read_text(encoding='utf-8')
orig_len = len(h)

# ─────────────────────────────────────────────────────────────────────────────
# NOVO BLOCO — inserir antes de </body></html>
# ─────────────────────────────────────────────────────────────────────────────
EXPORT_SCRIPT = r"""
<script>
/* ═══════════ NIELSEN EXCEL EXPORT ═══════════ */
(function(){
'use strict';

/* ── 1. Injetar botão no header do card MSO ── */
function injectBtn(){
  var sel = document.getElementById('msoMarketSel');
  if(!sel) return;
  var wrap = sel.parentNode;
  if(document.getElementById('btn-nielsen-xls')) return;
  var btn = document.createElement('button');
  btn.id = 'btn-nielsen-xls';
  btn.innerHTML = '&#128229; Exportar Nielsen Excel';
  btn.title = 'Exporta relatório executivo .xlsx com 5 abas analíticas';
  btn.style.cssText = 'display:inline-flex;align-items:center;gap:5px;font-size:11px;font-weight:700;'
    +'background:rgba(251,191,36,0.1);border:1px solid rgba(251,191,36,0.35);color:#fbbf24;'
    +'border-radius:6px;padding:6px 14px;cursor:pointer;font-family:inherit;transition:background 0.2s;';
  btn.onmouseover = function(){ this.style.background='rgba(251,191,36,0.22)'; };
  btn.onmouseout  = function(){ this.style.background='rgba(251,191,36,0.1)'; };
  btn.onclick = triggerExport;
  wrap.appendChild(btn);
}

/* ── 2. Toast de notificação ── */
function showToast(msg, type){
  var el = document.getElementById('_nxlsToast');
  if(!el){
    el = document.createElement('div');
    el.id = '_nxlsToast';
    el.style.cssText = 'position:fixed;bottom:28px;right:28px;z-index:99999;padding:11px 20px;'
      +'border-radius:9px;font-size:12px;font-weight:600;font-family:inherit;max-width:340px;'
      +'transition:opacity 0.4s;pointer-events:none;box-shadow:0 4px 24px rgba(0,0,0,0.5);';
    document.body.appendChild(el);
  }
  var styles = {
    info   : ['rgba(21,28,43,0.98)','rgba(251,191,36,0.4)' ,'#fbbf24'],
    success: ['rgba(10,32,22,0.98)','rgba(52,211,153,0.45)','#34d399'],
    error  : ['rgba(32,10,10,0.98)','rgba(239,68,68,0.45)' ,'#f87171']
  };
  var s = styles[type||'info'];
  el.style.background = s[0]; el.style.border = '1px solid '+s[1]; el.style.color = s[2];
  el.style.opacity = '1'; el.textContent = msg;
  clearTimeout(el._t);
  if(type==='success'||type==='error') el._t = setTimeout(function(){ el.style.opacity='0'; }, 4000);
}

/* ── 3. Carregar ExcelJS do CDN (lazy, só ao clicar) ── */
function loadExcelJS(cb){
  if(window.ExcelJS){ cb(); return; }
  showToast('⏳ Carregando biblioteca Excel…', 'info');
  var s = document.createElement('script');
  s.src = 'https://cdn.jsdelivr.net/npm/exceljs@4.4.0/dist/exceljs.min.js';
  s.onload = function(){ cb(); };
  s.onerror = function(){ showToast('❌ Erro ao carregar ExcelJS. Verifique a conexão com a internet.', 'error'); };
  document.head.appendChild(s);
}

/* ── 4. Capturar estado atual ── */
function getState(){
  var sel = document.getElementById('msoMarketSel');
  var market = sel ? sel.value : 'T.BR Farma';
  var msoD = (typeof MKTSHARE_OVERVIEW!=='undefined') ? MKTSHARE_OVERVIEW[market] : null;
  var valD = (typeof NIELSEN_BRAND_VAL!=='undefined')  ? NIELSEN_BRAND_VAL[market]  : null;
  var totD = (typeof FYTD_MARKET_TOTAL!=='undefined')  ? FYTD_MARKET_TOTAL[market]  : null;
  var brands = (typeof MSO_BRANDS!=='undefined')
    ? MSO_BRANDS.filter(function(b){ return b!=='ALL OTHERS CAMP'; })
    : ['OFF!','EXPOSIS','XO INSETO','SUPER REPELEX','SBP'];
  var months = (typeof MSO_MONTHS!=='undefined') ? MSO_MONTHS
    : ['Jul/25','Ago/25','Set/25','Out/25','Nov/25','Dez/25','Jan/26','Fev/26','Mar/26'];
  if(!msoD){ showToast('❌ Nenhum dado disponível para exportação.', 'error'); return null; }
  return { market:market, msoD:msoD, valD:valD, totD:totD, brands:brands, months:months };
}

/* ── 5. Trigger principal ── */
function triggerExport(){
  var state = getState();
  if(!state) return;
  var btn = document.getElementById('btn-nielsen-xls');
  if(btn){ btn.disabled=true; btn.textContent='⏳ Gerando…'; }
  loadExcelJS(function(){
    showToast('⏳ Gerando relatório Nielsen…', 'info');
    setTimeout(function(){ buildExcel(state, btn); }, 80);
  });
}

/* ── 6. Helpers de estilo ── */
var C = { dark:'0D1117', hdr:'161B22', card:'1A2332',
          gold:'FBBF24', white:'E2E8F0', gray:'94A3B8', dim:'64748B',
          teal:'22D3EE', green:'34D399', red:'EF4444', amber:'F59E0B',
          blue:'60A5FA', orange:'F97316' };
var BRAND_COL = {'OFF!':'FBBF24','EXPOSIS':'3B82F6','XO INSETO':'EF4444',
                 'SUPER REPELEX':'F97316','SBP':'06B6D4'};

function cell(ws, r, c, val, o){
  o = o||{};
  var cl = ws.getCell(r,c);
  cl.value = val;
  cl.fill  = { type:'pattern', pattern:'solid', fgColor:{ argb:'FF'+(o.bg||C.dark) } };
  cl.font  = { name:'Calibri', size:o.sz||10, bold:!!o.bold,
               color:{ argb:'FF'+(o.fg||C.white) } };
  cl.alignment = { vertical:'middle', horizontal:o.align||'left', wrapText:!!o.wrap };
  if(o.bord){
    var br={style:'thin',color:{argb:'FF2D3748'}};
    cl.border = {top:br,left:br,bottom:br,right:br};
  }
  return cl;
}
function hdr(ws, r, c, val, bg, fg){
  return cell(ws,r,c,val,{bg:bg||C.hdr,fg:fg||C.gold,bold:true,sz:11,align:'center',bord:true});
}
function fillBg(ws, rows, cols){
  for(var r=1;r<=rows;r++) for(var c=1;c<=cols;c++){
    var cc=ws.getCell(r,c);
    if(!cc.fill||!cc.fill.fgColor) cc.fill={type:'pattern',pattern:'solid',fgColor:{argb:'FF'+C.dark}};
  }
}
function colLetter(n){
  var s=''; while(n>0){ var r=(n-1)%26; s=String.fromCharCode(65+r)+s; n=Math.floor((n-1)/26); } return s;
}
function deltaColor(d){ return d>=0.5?C.green:d<=-0.5?C.red:C.amber; }
function fmtPct(v,d){ return (v==null?'—':(v>=0?'+':'')+v.toFixed(d||2)+'%'); }
function fmtPp(v) { return (v==null?'—':(v>=0?'+':'')+v.toFixed(2)+'pp'); }

/* ── 7. SHEET 1 — CAPA ── */
function sheetCapa(wb, st){
  var ws = wb.addWorksheet('📋 Capa');
  ws.views = [{showGridLines:false}];
  ws.getRow(1).height=52; ws.getRow(2).height=28; ws.getRow(3).height=16; ws.getRow(4).height=4;
  ws.getColumn(1).width=2; ws.getColumn(2).width=24; ws.getColumn(3).width=14;
  ws.getColumn(4).width=14; ws.getColumn(5).width=12; ws.getColumn(6).width=18;
  ws.getColumn(7).width=14; ws.getColumn(8).width=14; ws.getColumn(9).width=6;

  /* Título */
  ws.mergeCells('B1:H1');
  var t=ws.getCell('B1');
  t.value='NIELSEN PERFORMANCE REPORT — FARMA SUL';
  t.fill={type:'pattern',pattern:'solid',fgColor:{argb:'FF0D1117'}};
  t.font={name:'Calibri',size:22,bold:true,color:{argb:'FFFBBF24'}};
  t.alignment={vertical:'middle',horizontal:'center'};

  ws.mergeCells('B2:H2');
  var s2=ws.getCell('B2');
  s2.value='FY26 · Jul/2025–Mar/2026 · Market: '+st.market+' · SC Johnson | NielsenIQ Retail Measurement';
  s2.fill={type:'pattern',pattern:'solid',fgColor:{argb:'FF0D1117'}};
  s2.font={name:'Calibri',size:12,color:{argb:'FF94A3B8'}};
  s2.alignment={vertical:'middle',horizontal:'center'};

  ws.mergeCells('B3:H3');
  var s3=ws.getCell('B3');
  s3.value='Extraído em: '+new Date().toLocaleString('pt-BR');
  s3.fill={type:'pattern',pattern:'solid',fgColor:{argb:'FF0D1117'}};
  s3.font={name:'Calibri',size:10,color:{argb:'FF64748B'}};
  s3.alignment={vertical:'middle',horizontal:'center'};

  /* Barra dourada */
  for(var c=1;c<=9;c++){
    var bc=ws.getCell(4,c);
    bc.fill={type:'pattern',pattern:'solid',fgColor:{argb:'FFFBBF24'}};
  }

  /* Header KPIs */
  ['','Marca','Share FY25','Share FY26','Δ pp','Status','Valor FY26 R$M','Vol FY26 Kun',''].forEach(function(v,i){
    hdr(ws,5,i+1,v,C.hdr,C.gold);
  });
  ws.getRow(5).height=22;

  /* Dados por marca */
  st.brands.forEach(function(b,i){
    var rd=st.msoD[b]; var vd=st.valD?st.valD[b]:null; if(!rd) return;
    var r=6+i; ws.getRow(r).height=20;
    var d=rd.delta||0; var dc=deltaColor(d); var bc=BRAND_COL[b]||C.white;
    var statusTxt=d>=0.5?'▲ CRESCENDO':d<=-0.5?'▼ RECUANDO':'≈ ESTÁVEL';
    cell(ws,r,1,'',{bord:true});
    cell(ws,r,2,b,{bg:C.card,fg:bc,bold:true,sz:11,bord:true});
    cell(ws,r,3,(rd.fytd25||0).toFixed(2)+'%',{fg:C.gray,align:'center',bord:true});
    cell(ws,r,4,(rd.fytd26||0).toFixed(2)+'%',{fg:bc,bold:true,align:'center',bord:true});
    cell(ws,r,5,fmtPp(d),{fg:dc,bold:true,align:'center',bord:true});
    cell(ws,r,6,statusTxt,{fg:dc,bold:true,align:'center',bord:true});
    cell(ws,r,7,vd?(vd.fytd26_val||0).toFixed(2):'—',{align:'right',bord:true});
    cell(ws,r,8,vd?((vd.fytd26_un||0)/1000).toFixed(1):'—',{align:'right',bord:true});
    cell(ws,r,9,'',{bord:true});
  });

  /* Total mercado */
  var tr=6+st.brands.length+1; ws.getRow(tr).height=22;
  if(st.totD){
    ws.mergeCells(tr,2,tr,5);
    cell(ws,tr,2,'TOTAL MERCADO — '+st.market,{bg:C.card,fg:C.teal,bold:true,sz:11,bord:true});
    cell(ws,tr,6,'',{bg:C.card,bord:true});
    cell(ws,tr,7,(st.totD.fytd26_val||0).toFixed(2)+' R$M',{bg:C.card,fg:C.teal,bold:true,align:'right',bord:true});
    cell(ws,tr,8,st.totD.fytd26_un?((st.totD.fytd26_un||0)/1000).toFixed(1)+' Kun':'—',{bg:C.card,align:'right',bord:true});
    cell(ws,tr,9,'',{bg:C.card,bord:true});
  }

  /* Nota de rodapé */
  var nr=tr+2;
  ws.mergeCells(nr,2,nr,8);
  var fn=ws.getCell(nr,2);
  fn.value='Fonte: NielsenIQ Retail Measurement · PS · GBL · SC JOHNSON · BR · PEST CONTROL';
  fn.fill={type:'pattern',pattern:'solid',fgColor:{argb:'FF0D1117'}};
  fn.font={name:'Calibri',size:9,italic:true,color:{argb:'FF64748B'}};
  fn.alignment={horizontal:'center'};

  fillBg(ws,50,10);
}

/* ── 8. SHEET 2 — BASE ANALÍTICA ── */
function sheetBase(wb, st){
  var ws=wb.addWorksheet('📊 Base Analítica');
  ws.views=[{state:'frozen',xSplit:1,ySplit:3,showGridLines:false}];
  var widths=[2,22,13,13,10,14,14,11,14,14,11,12,12,12];
  widths.forEach(function(w,i){ ws.getColumn(i+1).width=w; });

  /* Título */
  ws.mergeCells('B1:N1');
  var t=ws.getCell('B1');
  t.value='BASE ANALÍTICA NIELSEN — '+st.market+' — FY26 vs FY25';
  t.fill={type:'pattern',pattern:'solid',fgColor:{argb:'FF0D1117'}};
  t.font={name:'Calibri',size:14,bold:true,color:{argb:'FFFBBF24'}};
  t.alignment={vertical:'middle',horizontal:'center'};
  ws.getRow(1).height=28;

  ws.mergeCells('B2:N2');
  var s2=ws.getCell('B2');
  s2.value='Jul/2025–Mar/2026 · Market: '+st.market+' · Exportado: '+new Date().toLocaleDateString('pt-BR');
  s2.fill={type:'pattern',pattern:'solid',fgColor:{argb:'FF0D1117'}};
  s2.font={name:'Calibri',size:10,color:{argb:'FF64748B'}};
  s2.alignment={vertical:'middle',horizontal:'center'};
  ws.getRow(2).height=18;

  /* Headers */
  var hdrs=['','Marca','Share FY25%','Share FY26%','Δ pp','Val FY25 R$M','Val FY26 R$M','Δ Val%',
            'Vol FY25 Kun','Vol FY26 Kun','Δ Vol%','Jan/26 R$M','Fev/26 R$M','Mar/26 R$M'];
  hdrs.forEach(function(v,i){ hdr(ws,3,i+1,v,C.hdr,C.gold); });
  ws.getRow(3).height=22;

  st.brands.forEach(function(b,i){
    var rd=st.msoD[b]; var vd=st.valD?st.valD[b]:null; if(!rd) return;
    var r=4+i; ws.getRow(r).height=18;
    var d=rd.delta||0; var bc=BRAND_COL[b]||C.white; var dc=deltaColor(d);
    var dv=vd&&vd.fytd25_val>0?(vd.fytd26_val-vd.fytd25_val)/vd.fytd25_val*100:null;
    var du=vd&&vd.fytd25_un >0?(vd.fytd26_un -vd.fytd25_un )/vd.fytd25_un *100:null;
    cell(ws,r,1,'',{bord:true});
    cell(ws,r,2,b,{fg:bc,bold:true,bord:true});
    cell(ws,r,3,(rd.fytd25||0).toFixed(2)+'%',{fg:C.gray,align:'center',bord:true});
    cell(ws,r,4,(rd.fytd26||0).toFixed(2)+'%',{fg:bc,bold:true,align:'center',bord:true});
    cell(ws,r,5,fmtPp(d),{fg:dc,bold:true,align:'center',bord:true});
    cell(ws,r,6,vd?(vd.fytd25_val||0).toFixed(3):'—',{fg:C.gray,align:'right',bord:true});
    cell(ws,r,7,vd?(vd.fytd26_val||0).toFixed(3):'—',{fg:bc,align:'right',bord:true});
    cell(ws,r,8,dv!=null?fmtPct(dv,1):'—',{fg:dv!=null?(dv>=0?C.green:C.red):C.gray,align:'center',bord:true});
    cell(ws,r,9, vd?((vd.fytd25_un||0)/1000).toFixed(1):'—',{fg:C.gray,align:'right',bord:true});
    cell(ws,r,10,vd?((vd.fytd26_un||0)/1000).toFixed(1):'—',{fg:bc,align:'right',bord:true});
    cell(ws,r,11,du!=null?fmtPct(du,1):'—',{fg:du!=null?(du>=0?C.green:C.red):C.gray,align:'center',bord:true});
    cell(ws,r,12,vd?(vd.jan_val||0).toFixed(3):'—',{align:'right',bord:true});
    cell(ws,r,13,vd?(vd.fev_val||0).toFixed(3):'—',{align:'right',bord:true});
    cell(ws,r,14,vd?(vd.mar_val||0).toFixed(3):'—',{align:'right',bord:true});
  });

  ws.autoFilter={from:{row:3,column:2},to:{row:3+st.brands.length,column:14}};
  fillBg(ws,20,15);
}

/* ── 9. SHEET 3 — EVOLUÇÃO MENSAL ── */
function sheetEvolucao(wb, st){
  var ws=wb.addWorksheet('📈 Evolução Mensal');
  ws.views=[{state:'frozen',xSplit:1,ySplit:3,showGridLines:false}];
  ws.getColumn(1).width=2; ws.getColumn(2).width=22;
  st.months.forEach(function(_,i){ ws.getColumn(3+i).width=10; });
  ws.getColumn(3+st.months.length).width=11;
  ws.getColumn(4+st.months.length).width=11;

  var endCol=colLetter(4+st.months.length);
  ws.mergeCells('B1:'+endCol+'1');
  var t=ws.getCell('B1');
  t.value='EVOLUÇÃO MENSAL — SHARE % · '+st.market+' · Jul/25 a Mar/26';
  t.fill={type:'pattern',pattern:'solid',fgColor:{argb:'FF0D1117'}};
  t.font={name:'Calibri',size:14,bold:true,color:{argb:'FF22D3EE'}};
  t.alignment={vertical:'middle',horizontal:'center'};
  ws.getRow(1).height=28;

  ws.mergeCells('B2:'+endCol+'2');
  var s2=ws.getCell('B2');
  s2.value='Série mensal Jul/25–Mar/26 · Share de mercado por marca (%) · Fonte: NielsenIQ Retail Measurement';
  s2.fill={type:'pattern',pattern:'solid',fgColor:{argb:'FF0D1117'}};
  s2.font={name:'Calibri',size:10,color:{argb:'FF64748B'}};
  s2.alignment={vertical:'middle',horizontal:'center'};
  ws.getRow(2).height=16;

  /* Header */
  var hdrs=['','Marca'].concat(st.months).concat(['FYTD25','FYTD26']);
  hdrs.forEach(function(v,i){ hdr(ws,3,i+1,v,C.hdr,C.teal); });
  ws.getRow(3).height=22;

  st.brands.forEach(function(b,i){
    var rd=st.msoD[b]; if(!rd) return;
    var r=4+i; ws.getRow(r).height=18;
    var bc=BRAND_COL[b]||C.white; var monthly=rd.monthly||[];
    cell(ws,r,1,'',{bord:true});
    cell(ws,r,2,b,{fg:bc,bold:true,bord:true});
    st.months.forEach(function(_,mi){
      var v=monthly[mi]; var prev=mi>0?monthly[mi-1]:null;
      var fg=v!=null&&prev!=null?(v>prev?C.green:v<prev?C.red:C.white):C.white;
      cell(ws,r,3+mi,v!=null?v.toFixed(2)+'%':'—',{align:'center',bord:true,fg:fg});
    });
    cell(ws,r,3+st.months.length,  (rd.fytd25||0).toFixed(2)+'%',{fg:C.gray,align:'center',bord:true});
    cell(ws,r,4+st.months.length,(rd.fytd26||0).toFixed(2)+'%',{fg:bc,bold:true,align:'center',bord:true});
  });

  fillBg(ws,20,5+st.months.length);
}

/* ── 10. SHEET 4 — COMPARATIVO FYTD ── */
function sheetFYTD(wb, st){
  var ws=wb.addWorksheet('⚖️ Comparativo FYTD');
  ws.views=[{state:'frozen',xSplit:1,ySplit:4,showGridLines:false}];
  [2,22,12,12,10,13,13,10,13,13,10,10].forEach(function(w,i){ ws.getColumn(i+1).width=w; });

  ws.mergeCells('B1:L1');
  var t=ws.getCell('B1');
  t.value='COMPARATIVO FYTD25 vs FYTD26 — '+st.market;
  t.fill={type:'pattern',pattern:'solid',fgColor:{argb:'FF0D1117'}};
  t.font={name:'Calibri',size:14,bold:true,color:{argb:'FF34D399'}};
  t.alignment={vertical:'middle',horizontal:'center'};
  ws.getRow(1).height=28;

  /* Sub-grupos */
  var grpBg=C.card;
  [[3,3,5,'─── SHARE % ───',C.green],[6,3,8,'─── VALOR R$M ───',C.blue],[9,3,11,'─── VOL Kun ───',C.amber]].forEach(function(g){
    ws.mergeCells(2,g[0],2,g[4]===C.amber?11:g[2]);
    /* fix: indices wrong, do individually */
  });
  /* Simpler: just write group labels */
  for(var c=1;c<=12;c++) cell(ws,2,c,'',{bg:C.card});
  ws.mergeCells('C2:E2');
  var gA=ws.getCell('C2'); gA.value='─── SHARE % ───';
  gA.fill={type:'pattern',pattern:'solid',fgColor:{argb:'FF'+C.card}};
  gA.font={name:'Calibri',size:9,bold:true,color:{argb:'FF'+C.green}};
  gA.alignment={horizontal:'center'};
  ws.mergeCells('F2:H2');
  var gB=ws.getCell('F2'); gB.value='─── VALOR R$M ───';
  gB.fill={type:'pattern',pattern:'solid',fgColor:{argb:'FF'+C.card}};
  gB.font={name:'Calibri',size:9,bold:true,color:{argb:'FF'+C.blue}};
  gB.alignment={horizontal:'center'};
  ws.mergeCells('I2:K2');
  var gC=ws.getCell('I2'); gC.value='─── VOL Kun ───';
  gC.fill={type:'pattern',pattern:'solid',fgColor:{argb:'FF'+C.card}};
  gC.font={name:'Calibri',size:9,bold:true,color:{argb:'FF'+C.amber}};
  gC.alignment={horizontal:'center'};
  ws.getRow(2).height=14;

  /* Header linha 3 */
  ['','Marca','FY25%','FY26%','Δ pp','FY25 R$M','FY26 R$M','Δ Val%','FY25 Kun','FY26 Kun','Δ Vol%','Rank'].forEach(function(v,i){
    hdr(ws,3,i+1,v,C.hdr,C.green);
  });
  ws.getRow(3).height=22;

  /* Dados ordenados por FYTD26 desc */
  var ranked=st.brands.filter(function(b){ return !!st.msoD[b]; })
    .sort(function(a,b){ return (st.msoD[b].fytd26||0)-(st.msoD[a].fytd26||0); });

  ranked.forEach(function(b,i){
    var rd=st.msoD[b]; var vd=st.valD?st.valD[b]:null;
    var r=4+i; ws.getRow(r).height=20;
    var d=rd.delta||0; var bc=BRAND_COL[b]||C.white; var dc=deltaColor(d);
    var dv=vd&&vd.fytd25_val>0?(vd.fytd26_val-vd.fytd25_val)/vd.fytd25_val*100:null;
    var du=vd&&vd.fytd25_un >0?(vd.fytd26_un -vd.fytd25_un )/vd.fytd25_un *100:null;
    var rankLbl=i===0?'🥇':i===1?'🥈':i===2?'🥉':(i+1)+'º';
    cell(ws,r,1,'',{bord:true});
    cell(ws,r,2,b,{fg:bc,bold:true,bord:true});
    cell(ws,r,3,(rd.fytd25||0).toFixed(2)+'%',{fg:C.gray,align:'center',bord:true});
    cell(ws,r,4,(rd.fytd26||0).toFixed(2)+'%',{fg:bc,bold:true,align:'center',bord:true});
    cell(ws,r,5,fmtPp(d),{fg:dc,bold:true,align:'center',bord:true});
    cell(ws,r,6,vd?(vd.fytd25_val||0).toFixed(3):'—',{fg:C.gray,align:'right',bord:true});
    cell(ws,r,7,vd?(vd.fytd26_val||0).toFixed(3):'—',{fg:bc,align:'right',bord:true});
    cell(ws,r,8,dv!=null?fmtPct(dv,1):'—',{fg:dv!=null?(dv>=0?C.green:C.red):C.gray,align:'center',bord:true});
    cell(ws,r,9, vd?((vd.fytd25_un||0)/1000).toFixed(1):'—',{fg:C.gray,align:'right',bord:true});
    cell(ws,r,10,vd?((vd.fytd26_un||0)/1000).toFixed(1):'—',{fg:bc,align:'right',bord:true});
    cell(ws,r,11,du!=null?fmtPct(du,1):'—',{fg:du!=null?(du>=0?C.green:C.red):C.gray,align:'center',bord:true});
    cell(ws,r,12,rankLbl,{align:'center',bold:true,bord:true});
  });

  fillBg(ws,20,13);
}

/* ── 11. SHEET 5 — DIAGNÓSTICO ── */
function sheetDiagnostico(wb, st){
  var ws=wb.addWorksheet('🔍 Diagnóstico');
  ws.views=[{showGridLines:false}];
  ws.getColumn(1).width=3; ws.getColumn(2).width=4; ws.getColumn(3).width=70; ws.getColumn(4).width=5;

  ws.mergeCells('B1:D1');
  var t=ws.getCell('B1');
  t.value='DIAGNÓSTICO AUTOMÁTICO — NIELSEN FARMA SUL';
  t.fill={type:'pattern',pattern:'solid',fgColor:{argb:'FF0D1117'}};
  t.font={name:'Calibri',size:16,bold:true,color:{argb:'FFF59E0B'}};
  t.alignment={vertical:'middle',horizontal:'center'};
  ws.getRow(1).height=34;

  ws.mergeCells('B2:D2');
  var s2=ws.getCell('B2');
  s2.value='Market: '+st.market+' · FY26 (Jul/25–Mar/26) · NielsenIQ Retail Measurement';
  s2.fill={type:'pattern',pattern:'solid',fgColor:{argb:'FF0D1117'}};
  s2.font={name:'Calibri',size:11,color:{argb:'FF64748B'}};
  s2.alignment={horizontal:'center'};
  ws.getRow(2).height=20;

  var lines=[];

  /* SCJ Combined */
  var scj26=0,scj25=0;
  ['OFF!','EXPOSIS'].forEach(function(b){ var rd=st.msoD[b]; if(rd){scj26+=rd.fytd26||0;scj25+=rd.fytd25||0;} });
  var scjD=scj26-scj25;
  lines.push({icon:'▶',text:'DIAGNÓSTICO EXECUTIVO — '+st.market+' — FY26',fg:C.gold,bold:true,sz:13,h:24});
  lines.push({icon:'',text:'',fg:C.dark,h:6});

  lines.push({icon:scjD>=0?'▲':'▼',
    text:'SCJ Combined (OFF!+EXPOSIS): '+scj26.toFixed(1)+'% FYTD26 — '+(scjD>=0?'+':'')+scjD.toFixed(2)+'pp vs FYTD25 '+(scjD>=0?'| posição consolidada':'| requer atenção'),
    fg:scjD>=0?C.green:C.red,bold:true,sz:12,h:22});

  lines.push({icon:'',text:'',fg:C.dark,h:8});

  /* Por marca */
  st.brands.forEach(function(b){
    var rd=st.msoD[b]; if(!rd) return;
    var d=rd.delta||0; var bc=BRAND_COL[b]||C.white;
    var monthly=rd.monthly||[]; var last=monthly[monthly.length-1]; var first=monthly[0];
    var trend=last!=null&&first!=null?last-first:0;
    var icon=d>=1?'▲▲':d>=0.3?'▲':d<=-1?'▼▼':d<=-0.3?'▼':'≈';
    var msg='';
    if(d>=1)       msg=b+' — GANHANDO '+fmtPp(d)+' de share FYTD26 vs FY25. Posição de liderança reforçada.';
    else if(d>=0.3) msg=b+' — Avançando '+fmtPp(d)+' vs FY25. Tendência positiva.';
    else if(d<=-1)  msg=b+' — RECUANDO '+fmtPp(d)+' vs FY25. Atenção: perda de participação relevante.';
    else if(d<=-0.3)msg=b+' — Cedendo '+fmtPp(d)+' vs FY25. Monitorar evolução nos próximos meses.';
    else            msg=b+' — Estável, variação de '+fmtPp(d)+' vs FY25.';
    if(trend>=2)      msg+=' Tendência mensal ascendente (+'+trend.toFixed(1)+'pp Jul→Mar).';
    else if(trend<=-2)msg+=' Tendência mensal de queda ('+trend.toFixed(1)+'pp Jul→Mar).';
    msg+=' Share atual: '+rd.fytd26.toFixed(2)+'%';
    lines.push({icon:icon,text:msg,fg:bc,bold:Math.abs(d)>=1,sz:11,h:22});
  });

  lines.push({icon:'',text:'',fg:C.dark,h:10});

  /* Total mercado */
  if(st.totD){
    var totD=st.totD.fytd26_val&&st.totD.fytd25_val
      ?(st.totD.fytd26_val-st.totD.fytd25_val)/st.totD.fytd25_val*100:0;
    lines.push({icon:'📊',
      text:'MERCADO TOTAL '+st.market+': R$'+(st.totD.fytd26_val||0).toFixed(2)+'M FYTD26 | '+(totD>=0?'+':'')+totD.toFixed(1)+'% vs FY25',
      fg:C.teal,bold:true,sz:12,h:22});
  }

  lines.push({icon:'',text:'',fg:C.dark,h:8});
  lines.push({icon:'ℹ️',
    text:'Fonte: NielsenIQ Retail Measurement · PS · GBL · SC JOHNSON · BR · PEST CONTROL · Exportado em '+new Date().toLocaleString('pt-BR'),
    fg:C.dim,sz:9,h:16});

  /* Renderizar */
  lines.forEach(function(ln,i){
    var r=3+i; ws.getRow(r).height=ln.h||18;
    cell(ws,r,1,'');
    ws.mergeCells(r,2,r,4);
    var cc=ws.getCell(r,2);
    cc.value=(ln.icon?ln.icon+' ':'')+ln.text;
    cc.fill={type:'pattern',pattern:'solid',fgColor:{argb:'FF0D1117'}};
    cc.font={name:'Calibri',size:ln.sz||11,bold:!!ln.bold,color:{argb:'FF'+(ln.fg||C.white)}};
    cc.alignment={vertical:'middle',horizontal:'left',wrapText:true};
  });

  fillBg(ws,3+lines.length+5,5);
}

/* ── 12. Orquestrar a geração ── */
function buildExcel(state, btn){
  try{
    var wb=new ExcelJS.Workbook();
    wb.creator='Dashboard Farma Sul — Giovano Anjos';
    wb.created=new Date(); wb.modified=new Date();

    sheetCapa(wb,state);
    sheetBase(wb,state);
    sheetEvolucao(wb,state);
    sheetFYTD(wb,state);
    sheetDiagnostico(wb,state);

    wb.xlsx.writeBuffer().then(function(buf){
      var blob=new Blob([buf],{type:'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'});
      var a=document.createElement('a');
      a.href=URL.createObjectURL(blob);
      a.download='Nielsen_FarmaSul_FY26_Export.xlsx';
      a.click();
      URL.revokeObjectURL(a.href);
      showToast('✓ Exportação concluída com sucesso.', 'success');
      if(btn){ btn.disabled=false; btn.innerHTML='&#128229; Exportar Nielsen Excel'; }
    }).catch(function(e){
      showToast('❌ Erro na geração do arquivo: '+e.message,'error');
      if(btn){ btn.disabled=false; btn.innerHTML='&#128229; Exportar Nielsen Excel'; }
    });
  } catch(e){
    showToast('❌ Erro: '+e.message,'error');
    console.error('NielsenExport error:',e);
    if(btn){ btn.disabled=false; btn.innerHTML='&#128229; Exportar Nielsen Excel'; }
  }
}

/* ── 13. Init ── */
if(document.readyState==='loading'){
  document.addEventListener('DOMContentLoaded', injectBtn);
} else {
  injectBtn();
}

})();
</script>
"""

# ── Inserir antes do ÚLTIMO </body></html> ──
OLD_END = '</body></html>'
count = h.count(OLD_END)
assert count >= 1, f'Esperava pelo menos 1 ocorrência de </body></html>, encontrei {count}'

# Substitui apenas a última ocorrência
last_idx = h.rfind(OLD_END)
h = h[:last_idx] + EXPORT_SCRIPT + '\n' + OLD_END
print('✅ Bloco de exportação inserido antes de </body></html>')

# ── Verificações ──
assert 'btn-nielsen-xls' in h,   '❌ botão não encontrado'
assert 'ExcelJS' in h,            '❌ ExcelJS não encontrado'
assert 'sheetCapa' in h,          '❌ sheetCapa não encontrado'
assert 'sheetDiagnostico' in h,   '❌ sheetDiagnostico não encontrado'
assert 'Nielsen_FarmaSul_FY26' in h, '❌ nome do arquivo não encontrado'
print('✅ Verificações OK')

print(f'\nTamanho original: {orig_len:,} | Novo: {len(h):,} | Δ: {len(h)-orig_len:+,}')

VER.parent.mkdir(parents=True, exist_ok=True)
VER.write_text(h, encoding='utf-8')
print(f'✅ Versão salva: {VER.name}')

SRC.write_text(h, encoding='utf-8')
print(f'✅ Base ativa atualizada: {SRC.name}')
print('DONE.')
