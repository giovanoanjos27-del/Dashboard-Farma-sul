"""
patch_nielsen_per_card.py
Cada botão de export gera um Excel focado no SEU card:

  Card 1 ($ Share FYTD Jul–Mar)
    → Nielsen_Share_FYTD_[mkt].xlsx
    Abas: Capa | Evolução Mensal | Comparativo FYTD | Memória de Cálculo | 1-Tabela-1

  Card 2 ($ Share Jan·Fev·Mar 25 vs 26)
    → Nielsen_Share_JanMar_[mkt].xlsx
    Abas: Capa | Jan·Fev·Mar Comparativo | Memória de Cálculo | 1-Tabela-1

  Card 3 (Valor R$MM / Unidades FYTD)
    → Nielsen_Valor_[mkt].xlsx  ou  Nielsen_Unidades_[mkt].xlsx
    Abas: Capa | Base Analítica | Comparativo FYTD | Memória de Cálculo | 1-Tabela-1
"""
import sys
from pathlib import Path
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

BASE = Path(r'C:\Users\valqu\OneDrive\Documentos\Claude\Projects\projeto Dashboard_farma_sul\Dashboard_farma_sul')
SRC  = BASE / 'Dashboard_Farma_Sul_20260512_2220.html'
VER  = BASE / 'versoes' / f'Dashboard_Farma_Sul_{datetime.now().strftime("%Y%m%d_%H%M")}_PerCard.html'

print('Lendo dashboard…')
h = SRC.read_text(encoding='utf-8')
orig_len = len(h)

# ─────────────────────────────────────────────────────────────────────────────
# 1. injectBtn — passa cardNum ao triggerExport
# ─────────────────────────────────────────────────────────────────────────────
OLD_INJECT = """/* ── 1. Injetar botão em TODOS os 3 cards Nielsen ── */
function injectBtn(){
  var cards = [
    {selId:'msoMarketSel',  btnId:'btn-nielsen-xls-1'},
    {selId:'mso2MarketSel', btnId:'btn-nielsen-xls-2'},
    {selId:'mso3MarketSel', btnId:'btn-nielsen-xls-3'}
  ];
  var CSS = 'display:inline-flex;align-items:center;gap:5px;font-size:11px;font-weight:700;'
    +'background:rgba(251,191,36,0.1);border:1px solid rgba(251,191,36,0.35);color:#fbbf24;'
    +'border-radius:6px;padding:6px 14px;cursor:pointer;font-family:inherit;transition:background 0.2s;';
  cards.forEach(function(c){
    var sel = document.getElementById(c.selId);
    if(!sel || document.getElementById(c.btnId)) return;
    var btn = document.createElement('button');
    btn.id = c.btnId;
    btn.innerHTML = '&#128229; Exportar Nielsen Excel';
    btn.title = 'Exporta relatório executivo .xlsx com 5 abas analíticas';
    btn.style.cssText = CSS;
    btn.onmouseover = function(){ this.style.background='rgba(251,191,36,0.22)'; };
    btn.onmouseout  = function(){ this.style.background='rgba(251,191,36,0.1)'; };
    (function(sId, bId){ btn.onclick = function(){ triggerExport(sId, bId); }; })(c.selId, c.btnId);
    sel.parentNode.appendChild(btn);
  });
}"""

NEW_INJECT = """/* ── 1. Injetar botão em TODOS os 3 cards Nielsen ── */
function injectBtn(){
  var cards = [
    {selId:'msoMarketSel',  btnId:'btn-nielsen-xls-1', cardNum:1, label:'📥 Exportar Share FYTD'},
    {selId:'mso2MarketSel', btnId:'btn-nielsen-xls-2', cardNum:2, label:'📥 Exportar Jan·Fev·Mar'},
    {selId:'mso3MarketSel', btnId:'btn-nielsen-xls-3', cardNum:3, label:'📥 Exportar Valor/Un'}
  ];
  var CSS = 'display:inline-flex;align-items:center;gap:5px;font-size:11px;font-weight:700;'
    +'background:rgba(251,191,36,0.1);border:1px solid rgba(251,191,36,0.35);color:#fbbf24;'
    +'border-radius:6px;padding:6px 14px;cursor:pointer;font-family:inherit;transition:background 0.2s;';
  cards.forEach(function(c){
    var sel = document.getElementById(c.selId);
    if(!sel || document.getElementById(c.btnId)) return;
    var btn = document.createElement('button');
    btn.id = c.btnId;
    btn.innerHTML = c.label;
    btn.title = 'Exporta Excel com dados específicos deste card';
    btn.style.cssText = CSS;
    btn.onmouseover = function(){ this.style.background='rgba(251,191,36,0.22)'; };
    btn.onmouseout  = function(){ this.style.background='rgba(251,191,36,0.1)'; };
    (function(sId, bId, cN){ btn.onclick = function(){ triggerExport(sId, bId, cN); }; })(c.selId, c.btnId, c.cardNum);
    sel.parentNode.appendChild(btn);
  });
}"""

assert h.count(OLD_INJECT) == 1
h = h.replace(OLD_INJECT, NEW_INJECT)
print('✅ injectBtn → labels e cardNum por card')

# ─────────────────────────────────────────────────────────────────────────────
# 2. triggerExport — aceita cardNum
# ─────────────────────────────────────────────────────────────────────────────
OLD_TRIGGER = """/* ── 5. Trigger principal ── */
function triggerExport(selId, btnId){
  selId = selId || 'msoMarketSel';
  btnId = btnId || 'btn-nielsen-xls-1';
  var state = getState(selId);
  if(!state) return;
  var btn = document.getElementById(btnId);
  if(btn){ btn.disabled=true; btn.textContent='⏳ Gerando…'; }
  loadExcelJS(function(){
    showToast('⏳ Gerando relatório Nielsen…', 'info');
    setTimeout(function(){ buildExcel(state, btn); }, 80);
  });
}"""

NEW_TRIGGER = """/* ── 5. Trigger principal ── */
function triggerExport(selId, btnId, cardNum){
  selId   = selId   || 'msoMarketSel';
  btnId   = btnId   || 'btn-nielsen-xls-1';
  cardNum = cardNum || 1;
  var state = getState(selId, cardNum);
  if(!state) return;
  var btn = document.getElementById(btnId);
  if(btn){ btn.disabled=true; btn.textContent='⏳ Gerando…'; }
  loadExcelJS(function(){
    showToast('⏳ Gerando relatório…', 'info');
    setTimeout(function(){ buildExcel(state, btn); }, 80);
  });
}"""

assert h.count(OLD_TRIGGER) == 1
h = h.replace(OLD_TRIGGER, NEW_TRIGGER)
print('✅ triggerExport → recebe cardNum')

# ─────────────────────────────────────────────────────────────────────────────
# 3. getState — aceita cardNum
# ─────────────────────────────────────────────────────────────────────────────
OLD_GS_SIG = "function getState(selId){"
NEW_GS_SIG = "function getState(selId, cardNum){"
OLD_GS_RET = "  return { market:market, mode:mode, msoD:msoD, valD:valD, totD:totD,\n           brands:brands, allBrands:allBrands, months:months,\n           allNBV:allNBV, allMSO:allMSO };"
NEW_GS_RET = "  cardNum = cardNum || 1;\n  return { market:market, mode:mode, cardNum:cardNum, msoD:msoD, valD:valD, totD:totD,\n           brands:brands, allBrands:allBrands, months:months,\n           allNBV:allNBV, allMSO:allMSO };"

assert h.count(OLD_GS_SIG) == 1
h = h.replace(OLD_GS_SIG, NEW_GS_SIG)
assert h.count(OLD_GS_RET) == 1
h = h.replace(OLD_GS_RET, NEW_GS_RET)
print('✅ getState → inclui cardNum no estado')

# ─────────────────────────────────────────────────────────────────────────────
# 4. buildExcel — roteia sheets por card + filename por card
# ─────────────────────────────────────────────────────────────────────────────
OLD_BUILD_CORE = """    sheetCapa(wb,state);
    sheetBase(wb,state);
    sheetEvolucao(wb,state);
    sheetFYTD(wb,state);
    sheetMemCalculo(wb,state);
    sheetTabela1(wb,state);

    var modeSuffix = (state.mode==='un') ? '_Unidades' : '_Valor';
    var mktSlug = state.market.replace(/[^a-zA-Z0-9]/g,'_').replace(/_+/g,'_');
    var fname = 'Nielsen_FarmaSul_FY26_'+mktSlug+modeSuffix+'.xlsx';"""

NEW_BUILD_CORE = """    var mktSlug = state.market.replace(/[^a-zA-Z0-9]/g,'_').replace(/_+/g,'_');
    var fname, cardLabel;
    if(state.cardNum === 1){
      /* Card 1 — Share FYTD Jul–Mar */
      fname      = 'Nielsen_Share_FYTD_'+mktSlug+'.xlsx';
      cardLabel  = 'Share% FYTD · Jul/25–Mar/26 · '+state.market;
      sheetCapa(wb,state);
      sheetEvolucao(wb,state);
      sheetFYTD(wb,state);
      sheetMemCalculo(wb,state);
      sheetTabela1(wb,state);
    } else if(state.cardNum === 2){
      /* Card 2 — Share Jan·Fev·Mar 2025 vs 2026 */
      fname      = 'Nielsen_Share_JanMar_'+mktSlug+'.xlsx';
      cardLabel  = 'Share% Jan·Fev·Mar 2025 vs 2026 · '+state.market;
      sheetCapa(wb,state);
      sheetJanMar(wb,state);
      sheetMemCalculo(wb,state);
      sheetTabela1(wb,state);
    } else {
      /* Card 3 — Valor R$M ou Unidades FYTD */
      var modeSuffix = (state.mode==='un') ? '_Unidades' : '_Valor';
      fname      = 'Nielsen_'+((state.mode==='un')?'Unidades':'Valor')+'_FYTD_'+mktSlug+'.xlsx';
      cardLabel  = ((state.mode==='un')?'Unidades':'Valor R$M')+' FYTD · Jul/25–Mar/26 · '+state.market;
      sheetCapa(wb,state);
      sheetBase(wb,state);
      sheetFYTD(wb,state);
      sheetMemCalculo(wb,state);
      sheetTabela1(wb,state);
    }"""

assert h.count(OLD_BUILD_CORE) == 1
h = h.replace(OLD_BUILD_CORE, NEW_BUILD_CORE)
print('✅ buildExcel → roteamento por card')

# ─────────────────────────────────────────────────────────────────────────────
# 5. Nova função sheetJanMar — inserir ANTES de sheetTabela1
# ─────────────────────────────────────────────────────────────────────────────
ANCHOR_TABELA = "/* ── 11b. SHEET 6 — 1-TABELA-1 (Base Completa Nielsen) ── */"
assert h.count(ANCHOR_TABELA) == 1

SHEET_JAN_MAR = r"""/* ── 11c. SHEET — JAN·FEV·MAR COMPARATIVO (Card 2) ── */
function sheetJanMar(wb, st){
  var ws = wb.addWorksheet('📅 Jan·Fev·Mar Comparativo');
  ws.views = [{state:'frozen',xSplit:1,ySplit:4,showGridLines:false}];

  /* Colunas: margem | marca | 3×25 | Acum25 | 3×26 | Acum26 | Δpp/Δ% */
  var widths=[2,22,10,10,10,13,10,10,10,13,10,2];
  widths.forEach(function(w,i){ ws.getColumn(i+1).width=w; });
  var lastC=12;

  /* Título */
  ws.getRow(1).height=26;
  ws.mergeCells('B1:K1');
  var t=ws.getCell('B1');
  t.value='MARKET SHARE — JAN · FEV · MAR — 2025 vs 2026 · '+st.market;
  t.fill={type:'pattern',pattern:'solid',fgColor:{argb:'FFD9E1F2'}};
  t.font={name:'Calibri',size:13,bold:true,color:{argb:'FF1D4ED8'}};
  t.alignment={vertical:'middle',horizontal:'center'};

  ws.getRow(2).height=14;
  ws.mergeCells('B2:K2');
  var s2=ws.getCell('B2');
  s2.value='Acumulado Jan–Mar · Share% por Marca · NielsenIQ Retail Measurement · Exportado '+new Date().toLocaleDateString('pt-BR');
  s2.fill={type:'pattern',pattern:'solid',fgColor:{argb:'FFFFFFFF'}};
  s2.font={name:'Calibri',size:9,italic:true,color:{argb:'FF94A3B8'}};
  s2.alignment={horizontal:'center'};

  /* Sub-header grupos */
  ws.getRow(3).height=14;
  for(var c=1;c<=lastC;c++) cell(ws,3,c,'',{bg:'D9E1F2'});
  ws.mergeCells('C3:F3');
  var g25=ws.getCell('C3'); g25.value='── 2025 ──';
  g25.fill={type:'pattern',pattern:'solid',fgColor:{argb:'FFD9E1F2'}};
  g25.font={name:'Calibri',size:9,bold:true,color:{argb:'FF64748B'}};
  g25.alignment={horizontal:'center'};
  ws.mergeCells('G3:J3');
  var g26=ws.getCell('G3'); g26.value='── 2026 ──';
  g26.fill={type:'pattern',pattern:'solid',fgColor:{argb:'FFD9E1F2'}};
  g26.font={name:'Calibri',size:9,bold:true,color:{argb:'FF1D4ED8'}};
  g26.alignment={horizontal:'center'};
  ws.getRow(3).height=14;

  /* Header linha 4 */
  var hdrs=['','Marca','Jan/25','Fev/25','Mar/25','JanMar25%','Jan/26','Fev/26','Mar/26','JanMar26%','Δ pp',''];
  hdrs.forEach(function(v,i){ hdr(ws,4,i+1,v,'D9E1F2','1E293B'); });
  ws.getRow(4).height=20;

  /* ── Seção 1: Share % ── */
  var secR=5; ws.getRow(secR).height=18;
  ws.mergeCells(secR,2,secR,lastC-1);
  var sc1=ws.getCell(secR,2);
  sc1.value='① SHARE % — Jan·Fev·Mar';
  sc1.fill={type:'pattern',pattern:'solid',fgColor:{argb:'FF1D4ED8'}};
  sc1.font={name:'Calibri',size:10,bold:true,color:{argb:'FFFFFFFF'}};
  sc1.alignment={vertical:'middle',horizontal:'left'};
  cell(ws,secR,1,'',{bg:'1D4ED8'}); cell(ws,secR,lastC,'',{bg:'1D4ED8'});

  var dataR=secR+1;
  st.brands.forEach(function(b){
    var rd=st.msoD[b]; if(!rd) return;
    var bc=BRAND_COL[b]||C.white;
    var d=rd.delta||0; var dc=deltaColor(d);
    var j25=rd.jan25||0; var f25=rd.feb25||0; var m25=rd.mar25||0;
    /* Jan-Mar 26 from monthly[6,7,8] */
    var monthly=rd.monthly||[];
    var j26=monthly[6]||0; var f26=monthly[7]||0; var m26=monthly[8]||0;
    /* Acumulado: média ponderada aproximada (sem volumes mensais de mercado, usamos média) */
    /* FYTD share e JANMAR share: calcular do FYTD_MARKET_TOTAL se disponível */
    var janmar25_shr=st.totD&&st.totD.janmar25_val&&st.valD&&st.valD[b]
      ? (st.valD[b].fytd25_val>0
          ? ((st.valD[b].jan25_val||0)+(st.valD[b].fev25_val||0)+(st.valD[b].mar25_val||0))
            /st.totD.janmar25_val*100
          : (j25+f25+m25)/3)
      : (j25+f25+m25)/3;
    var janmar26_shr=st.totD&&st.totD.janmar26_val&&st.valD&&st.valD[b]
      ? ((st.valD[b].jan_val||0)+(st.valD[b].fev_val||0)+(st.valD[b].mar_val||0))
        /st.totD.janmar26_val*100
      : (j26+f26+m26)/3;
    var djanmar=janmar26_shr-janmar25_shr;
    ws.getRow(dataR).height=18;
    cell(ws,dataR,1,'',{bord:true});
    cell(ws,dataR,2,b,{fg:bc,bold:true,bord:true});
    cell(ws,dataR,3,j25.toFixed(2)+'%',{fg:C.gray,align:'center',bord:true});
    cell(ws,dataR,4,f25.toFixed(2)+'%',{fg:C.gray,align:'center',bord:true});
    cell(ws,dataR,5,m25.toFixed(2)+'%',{fg:C.gray,align:'center',bord:true});
    cell(ws,dataR,6,janmar25_shr.toFixed(2)+'%',{fg:C.gray,bold:true,align:'center',bord:true,bg:'EEF2FF'});
    cell(ws,dataR,7,j26.toFixed(2)+'%',{fg:bc,align:'center',bord:true});
    cell(ws,dataR,8,f26.toFixed(2)+'%',{fg:bc,align:'center',bord:true});
    cell(ws,dataR,9,m26.toFixed(2)+'%',{fg:bc,align:'center',bord:true});
    cell(ws,dataR,10,janmar26_shr.toFixed(2)+'%',{fg:bc,bold:true,align:'center',bord:true,bg:'EEF2FF'});
    cell(ws,dataR,11,fmtPp(djanmar),{fg:deltaColor(djanmar),bold:true,align:'center',bord:true});
    cell(ws,dataR,12,'',{bord:true});
    dataR++;
  });
  dataR++;

  /* ── Seção 2: Valor R$M ── */
  ws.getRow(dataR).height=18;
  ws.mergeCells(dataR,2,dataR,lastC-1);
  var sc2=ws.getCell(dataR,2);
  sc2.value='② VALOR R$M — Jan·Fev·Mar';
  sc2.fill={type:'pattern',pattern:'solid',fgColor:{argb:'FF0E7490'}};
  sc2.font={name:'Calibri',size:10,bold:true,color:{argb:'FFFFFFFF'}};
  sc2.alignment={vertical:'middle',horizontal:'left'};
  cell(ws,dataR,1,'',{bg:'0E7490'}); cell(ws,dataR,lastC,'',{bg:'0E7490'});
  dataR++;

  /* Sub-header valor */
  var vhdrs=['','Marca','Jan/25','Fev/25','Mar/25','JanMar25 R$M','Jan/26','Fev/26','Mar/26','JanMar26 R$M','Δ Val%',''];
  vhdrs.forEach(function(v,i){ hdr(ws,dataR,i+1,v,'D9E1F2','1E293B'); });
  ws.getRow(dataR).height=18;
  dataR++;

  st.brands.forEach(function(b){
    var vd=st.valD?st.valD[b]:null; if(!vd) return;
    var bc=BRAND_COL[b]||C.white;
    var j25v=vd.jan25_val||0; var f25v=vd.fev25_val||0; var m25v=vd.mar25_val||0;
    var j26v=vd.jan_val||0;   var f26v=vd.fev_val||0;   var m26v=vd.mar_val||0;
    var tot25=j25v+f25v+m25v; var tot26=j26v+f26v+m26v;
    var dv=tot25>0?(tot26-tot25)/tot25*100:null;
    ws.getRow(dataR).height=18;
    cell(ws,dataR,1,'',{bord:true});
    cell(ws,dataR,2,b,{fg:bc,bold:true,bord:true});
    cell(ws,dataR,3,j25v.toFixed(3),{fg:C.gray,align:'right',bord:true});
    cell(ws,dataR,4,f25v.toFixed(3),{fg:C.gray,align:'right',bord:true});
    cell(ws,dataR,5,m25v.toFixed(3),{fg:C.gray,align:'right',bord:true});
    cell(ws,dataR,6,tot25.toFixed(3),{fg:C.gray,bold:true,align:'right',bord:true,bg:'EEF2FF'});
    cell(ws,dataR,7,j26v.toFixed(3),{fg:bc,align:'right',bord:true});
    cell(ws,dataR,8,f26v.toFixed(3),{fg:bc,align:'right',bord:true});
    cell(ws,dataR,9,m26v.toFixed(3),{fg:bc,align:'right',bord:true});
    cell(ws,dataR,10,tot26.toFixed(3),{fg:bc,bold:true,align:'right',bord:true,bg:'EEF2FF'});
    cell(ws,dataR,11,dv!=null?fmtPct(dv,1):'—',{fg:dv!=null?deltaColor(dv):C.gray,bold:true,align:'center',bord:true});
    cell(ws,dataR,12,'',{bord:true});
    dataR++;
  });

  /* Total mercado */
  if(st.totD){
    var tot25m=st.totD.janmar25_val||0; var tot26m=st.totD.janmar26_val||0;
    var dtot=tot25m>0?(tot26m-tot25m)/tot25m*100:null;
    ws.getRow(dataR).height=18;
    cell(ws,dataR,1,'',{bg:'EEF2FF',bord:true});
    cell(ws,dataR,2,'= TOTAL MERCADO',{bg:'EEF2FF',fg:C.teal,bold:true,bord:true});
    cell(ws,dataR,3,(st.totD.jan25_val||0).toFixed(3),{bg:'EEF2FF',fg:C.gray,align:'right',bord:true});
    cell(ws,dataR,4,(st.totD.fev25_val||0).toFixed(3),{bg:'EEF2FF',fg:C.gray,align:'right',bord:true});
    cell(ws,dataR,5,(st.totD.mar25_val||0).toFixed(3),{bg:'EEF2FF',fg:C.gray,align:'right',bord:true});
    cell(ws,dataR,6,tot25m.toFixed(3),{bg:'EEF2FF',fg:C.gray,bold:true,align:'right',bord:true});
    cell(ws,dataR,7,(st.totD.jan26_val||0).toFixed(3),{bg:'EEF2FF',fg:C.teal,align:'right',bord:true});
    cell(ws,dataR,8,(st.totD.fev26_val||0).toFixed(3),{bg:'EEF2FF',fg:C.teal,align:'right',bord:true});
    cell(ws,dataR,9,(st.totD.mar26_val||0).toFixed(3),{bg:'EEF2FF',fg:C.teal,align:'right',bord:true});
    cell(ws,dataR,10,tot26m.toFixed(3),{bg:'EEF2FF',fg:C.teal,bold:true,align:'right',bord:true});
    cell(ws,dataR,11,dtot!=null?fmtPct(dtot,1):'—',{bg:'EEF2FF',fg:dtot!=null?deltaColor(dtot):C.gray,bold:true,align:'center',bord:true});
    cell(ws,dataR,12,'',{bg:'EEF2FF',bord:true});
    dataR++;
  }
  dataR++;

  /* Nota */
  ws.mergeCells(dataR,2,dataR,lastC-1);
  var fn=ws.getCell(dataR,2);
  fn.value='Fonte: NielsenIQ Retail Measurement · Acum Jan·Fev·Mar · Share% = ΣValMarca(JanMar) ÷ ΣMercado(JanMar) × 100 · Exportado '+new Date().toLocaleString('pt-BR');
  fn.fill={type:'pattern',pattern:'solid',fgColor:{argb:'FFFFFFFF'}};
  fn.font={name:'Calibri',size:8,italic:true,color:{argb:'FF94A3B8'}};
  fn.alignment={horizontal:'center'};

  fillBg(ws,dataR+3,lastC+1);
}

"""

h = h[:h.find(ANCHOR_TABELA)] + SHEET_JAN_MAR + h[h.find(ANCHOR_TABELA):]
print('✅ sheetJanMar inserida')

# ─────────────────────────────────────────────────────────────────────────────
# Verificações
# ─────────────────────────────────────────────────────────────────────────────
assert 'sheetJanMar' in h,                 '❌ sheetJanMar não encontrada'
assert 'cardNum:1' in h,                   '❌ cardNum 1 não encontrado'
assert 'cardNum:2' in h,                   '❌ cardNum 2 não encontrado'
assert 'cardNum:3' in h,                   '❌ cardNum 3 não encontrado'
assert 'Nielsen_Share_FYTD_' in h,         '❌ filename card 1 não encontrado'
assert 'Nielsen_Share_JanMar_' in h,       '❌ filename card 2 não encontrado'
assert 'Card 3 — Valor R$M ou Unidades FYTD' in h, '❌ branch card 3 não encontrado'
assert 'sheetJanMar(wb,state)' in h,       '❌ chamada sheetJanMar não encontrada'
assert h.count('sheetJanMar(wb,state)') == 1
print('✅ Verificações OK')

print(f'\nTamanho original: {orig_len:,} | Novo: {len(h):,} | Δ: {len(h)-orig_len:+,}')

VER.parent.mkdir(parents=True, exist_ok=True)
VER.write_text(h, encoding='utf-8')
print(f'✅ Versão salva: {VER.name}')
SRC.write_text(h, encoding='utf-8')
print(f'✅ Base ativa atualizada: {SRC.name}')
print('DONE.')
