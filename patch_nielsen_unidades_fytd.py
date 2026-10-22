"""
patch_nielsen_unidades_fytd.py
Fix "Export Unidades não vem consolidado" — Card 3 FYTD.

Diagnóstico:
  Ao exportar com Unidades selecionado, o Excel trazia Share% e R$MM em
  destaque. A aba "📊 Base Analítica" sempre mostrava Jan/26 R$M (não K Un).
  A aba "⚖️ Comparativo FYTD" ordenava por Share%, não por Unidades.
  Não existia aba dedicada de Unidades consolidada.

Fixes:
  FIX 1: sheetBase — últimas 3 colunas dinâmicas (Jan/26 R$M ou Jan/26 Kun
         conforme st.mode). Título menciona modo.
  FIX 2: sheetFYTD — título menciona modo (SHARE % / VALOR R$M / UNIDADES).
         Ordenação: por fytd26_un quando mode='un', fytd26_val quando mode='val'.
  FIX 3: Adiciona função sheetUnidadesFYTD — aba dedicada consolidada de
         Unidades FYTD. Inclui ALL OTHERS CAMP. Colunas FY25 Kun, FY26 Kun,
         Δ%, + 9 meses mensais. Linha SCJ Combined + Total Mercado.
  FIX 4: buildExcel Card 3 — quando mode='un', chama sheetUnidadesFYTD
         como primeira aba de dados (após Capa).

NÃO ALTERA:
  - Cards 1 e 2, Jan-Mar, Sell Out, Sell In, Cobertura, OLs
  - Cálculos de KPI, share, diagnósticos
  - sheetMemCalculo, sheetTabela1, sheetEvolucao
"""
import sys
from pathlib import Path
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

BASE = Path(r'C:\Users\valqu\OneDrive\Documentos\Claude\Projects\projeto Dashboard_farma_sul\Dashboard_farma_sul')
SRC  = BASE / 'Dashboard_Farma_Sul_20260512_2220.html'
VER  = BASE / 'versoes' / f'Dashboard_Farma_Sul_{datetime.now().strftime("%Y%m%d_%H%M")}_UnidadesFYTD.html'

print('Lendo dashboard…')
h = SRC.read_text(encoding='utf-8')
orig_len = len(h)

# ─────────────────────────────────────────────────────────────────────────────
# FIX 1: sheetBase — título modo-ciente + últimas 3 colunas dinâmicas
# ─────────────────────────────────────────────────────────────────────────────
OLD_BASE_TITLE = "  t.value='BASE ANALÍTICA NIELSEN — '+st.market+' — FY26 vs FY25';"

NEW_BASE_TITLE = "  var _bmLbl=st.mode==='un'?' · UNIDADES':st.mode==='val'?' · VALOR R$M':'';\n  t.value='BASE ANALÍTICA NIELSEN'+_bmLbl+' — '+st.market.toUpperCase()+' — FY26 vs FY25';"

assert h.count(OLD_BASE_TITLE) == 1, f'❌ âncora sheetBase title: {h.count(OLD_BASE_TITLE)}×'
h = h.replace(OLD_BASE_TITLE, NEW_BASE_TITLE)
print('✅ FIX 1a: sheetBase título modo-ciente')

OLD_BASE_HDRS = """  var hdrs=['','Marca','Share FY25%','Share FY26%','Δ pp','Val FY25 R$M','Val FY26 R$M','Δ Val%',
            'Vol FY25 Kun','Vol FY26 Kun','Δ Vol%','Jan/26 R$M','Fev/26 R$M','Mar/26 R$M'];"""

NEW_BASE_HDRS = """  var _isUnMode=(st.mode==='un');
  var hdrs=['','Marca','Share FY25%','Share FY26%','Δ pp','Val FY25 R$M','Val FY26 R$M','Δ Val%',
            'Vol FY25 Kun','Vol FY26 Kun','Δ Vol%',
            _isUnMode?'Jan/26 Kun':'Jan/26 R$M',
            _isUnMode?'Fev/26 Kun':'Fev/26 R$M',
            _isUnMode?'Mar/26 Kun':'Mar/26 R$M'];"""

assert h.count(OLD_BASE_HDRS) == 1, f'❌ âncora sheetBase hdrs: {h.count(OLD_BASE_HDRS)}×'
h = h.replace(OLD_BASE_HDRS, NEW_BASE_HDRS)
print('✅ FIX 1b: sheetBase headers últimas 3 colunas dinâmicas')

OLD_BASE_MONTHLY = """    cell(ws,r,12,vd?(vd.jan_val||0).toFixed(3):'—',{align:'right',bord:true});
    cell(ws,r,13,vd?(vd.fev_val||0).toFixed(3):'—',{align:'right',bord:true});
    cell(ws,r,14,vd?(vd.mar_val||0).toFixed(3):'—',{align:'right',bord:true});"""

NEW_BASE_MONTHLY = """    cell(ws,r,12,vd?(_isUnMode?Math.round(vd.jan_un||0).toString():(vd.jan_val||0).toFixed(3)):'—',{align:'right',bord:true});
    cell(ws,r,13,vd?(_isUnMode?Math.round(vd.fev_un||0).toString():(vd.fev_val||0).toFixed(3)):'—',{align:'right',bord:true});
    cell(ws,r,14,vd?(_isUnMode?Math.round(vd.mar_un||0).toString():(vd.mar_val||0).toFixed(3)):'—',{align:'right',bord:true});"""

assert h.count(OLD_BASE_MONTHLY) == 1, f'❌ âncora sheetBase monthly cells: {h.count(OLD_BASE_MONTHLY)}×'
h = h.replace(OLD_BASE_MONTHLY, NEW_BASE_MONTHLY)
print('✅ FIX 1c: sheetBase células mensais Jan/Fev/Mar → Kun quando mode=un')

# ─────────────────────────────────────────────────────────────────────────────
# FIX 2: sheetFYTD — título modo + ordenação dinâmica
# ─────────────────────────────────────────────────────────────────────────────
OLD_FYTD_TITLE = "  t.value='COMPARATIVO FYTD25 vs FYTD26 — '+st.market;"

NEW_FYTD_TITLE = """  var _ftLbl=st.mode==='un'?' · UNIDADES':st.mode==='val'?' · VALOR R$M':'';
  t.value='COMPARATIVO FYTD25 vs FYTD26'+_ftLbl+' — '+st.market.toUpperCase();"""

assert h.count(OLD_FYTD_TITLE) == 1, f'❌ âncora sheetFYTD title: {h.count(OLD_FYTD_TITLE)}×'
h = h.replace(OLD_FYTD_TITLE, NEW_FYTD_TITLE)
print('✅ FIX 2a: sheetFYTD título modo-ciente')

OLD_FYTD_SORT = """  var ranked=st.brands.filter(function(b){ return !!st.msoD[b]; })
    .sort(function(a,b){ return (st.msoD[b].fytd26||0)-(st.msoD[a].fytd26||0); });"""

NEW_FYTD_SORT = """  var ranked=st.brands.filter(function(b){ return !!st.msoD[b]; })
    .sort(function(a,b){
      if(st.mode==='un'){
        var _au=st.valD?((st.valD[a]&&st.valD[a].fytd26_un)||0):0;
        var _bu=st.valD?((st.valD[b]&&st.valD[b].fytd26_un)||0):0;
        return _bu-_au;
      }
      if(st.mode==='val'){
        var _av=st.valD?((st.valD[a]&&st.valD[a].fytd26_val)||0):0;
        var _bv=st.valD?((st.valD[b]&&st.valD[b].fytd26_val)||0):0;
        return _bv-_av;
      }
      return (st.msoD[b].fytd26||0)-(st.msoD[a].fytd26||0);
    });"""

assert h.count(OLD_FYTD_SORT) == 1, f'❌ âncora sheetFYTD sort: {h.count(OLD_FYTD_SORT)}×'
h = h.replace(OLD_FYTD_SORT, NEW_FYTD_SORT)
print('✅ FIX 2b: sheetFYTD ordenação por fytd26_un/val/share conforme modo')

# ─────────────────────────────────────────────────────────────────────────────
# FIX 3: Adicionar função sheetUnidadesFYTD antes de sheetJanMar
# ─────────────────────────────────────────────────────────────────────────────
SHEET_UNIDADES_FYTD = r"""
/* ── 11d. SHEET — UNIDADES FYTD JUL-MAR CONSOLIDADO ── */
function sheetUnidadesFYTD(wb, st){
  var ws = wb.addWorksheet('\u{1F4E6} Unidades FYTD');
  ws.views = [{state:'frozen',xSplit:1,ySplit:4,showGridLines:false}];
  var nM = st.months.length; /* 9 meses Jul-Mar */

  /* Colunas: margin | Marca | FY25 Kun | FY26 Kun | Δ Un% | 9 meses | margin */
  var widths=[2,22,11,11,9];
  for(var mi=0;mi<nM;mi++) widths.push(8);
  widths.push(2);
  widths.forEach(function(w,i){ ws.getColumn(i+1).width=w; });
  var lastC = widths.length;

  /* Título */
  ws.getRow(1).height=26;
  ws.mergeCells(1,2,1,lastC-1);
  var t=ws.getCell(1,2);
  t.value='UNIDADES FYTD JUL–MAR \xb7 FY25 vs FY26 \xb7 '+st.market.toUpperCase();
  t.fill={type:'pattern',pattern:'solid',fgColor:{argb:'FFFFFFFF'}};
  t.font={name:'Calibri',size:13,bold:true,color:{argb:'FF'+C.amber}};
  t.alignment={vertical:'middle',horizontal:'center'};
  ws.getRow(2).height=14;
  ws.mergeCells(2,2,2,lastC-1);
  var s2=ws.getCell(2,2);
  s2.value='Unidades (Mil) FYTD \xb7 Jul/2025–Mar/2026 \xb7 NielsenIQ Retail Measurement \xb7 Exportado: '+new Date().toLocaleDateString('pt-BR');
  s2.fill={type:'pattern',pattern:'solid',fgColor:{argb:'FFFFFFFF'}};
  s2.font={name:'Calibri',size:9,italic:true,color:{argb:'FF94A3B8'}};
  s2.alignment={horizontal:'center'};

  /* Sub-grupos linha 3 */
  ws.getRow(3).height=14;
  for(var c=1;c<=lastC;c++) cell(ws,3,c,'',{bg:C.hdr});
  ws.mergeCells(3,3,3,5);
  var gA=ws.getCell(3,3); gA.value='── FYTD ──';
  gA.fill={type:'pattern',pattern:'solid',fgColor:{argb:'FF'+C.hdr}};
  gA.font={name:'Calibri',size:9,bold:true,color:{argb:'FF'+C.amber}};
  gA.alignment={horizontal:'center'};
  if(nM>0){
    ws.mergeCells(3,6,3,5+nM);
    var gB=ws.getCell(3,6); gB.value='── Mensal (Mil Un) ──';
    gB.fill={type:'pattern',pattern:'solid',fgColor:{argb:'FF'+C.hdr}};
    gB.font={name:'Calibri',size:9,bold:true,color:{argb:'FF'+C.amber}};
    gB.alignment={horizontal:'center'};
  }

  /* Headers linha 4 */
  var hdrs=['','Marca','FY25 Kun','FY26 Kun','Δ Un%'];
  st.months.forEach(function(m){ hdrs.push(m); });
  hdrs.push('');
  hdrs.forEach(function(v,i){ hdr(ws,4,i+1,v,C.hdr,C.amber); });
  ws.getRow(4).height=20;

  /* Dados: allBrands (inclui ALL OTHERS CAMP) */
  var dataR=5;
  var scjFy25=0, scjFy26=0;
  var scjMonthly=Array(nM).fill(0);

  st.allBrands.forEach(function(b){
    var vd=st.valD?st.valD[b]:null; if(!vd) return;
    var bc=BRAND_COL[b]||C.gray;
    var fy25=vd.fytd25_un||0, fy26=vd.fytd26_un||0;
    var du=fy25>0?(fy26-fy25)/fy25*100:null;
    var mu=vd.monthly_un||[];
    ws.getRow(dataR).height=18;
    cell(ws,dataR,1,'',{bord:true});
    cell(ws,dataR,2,b,{fg:bc,bold:true,bord:true});
    cell(ws,dataR,3,(fy25/1000).toFixed(1),{fg:C.gray,align:'right',bord:true});
    cell(ws,dataR,4,(fy26/1000).toFixed(1),{fg:bc,bold:true,align:'right',bord:true});
    cell(ws,dataR,5,du!=null?fmtPct(du,1):'—',{fg:du!=null?(du>=0?C.green:C.red):C.gray,bold:true,align:'center',bord:true});
    for(var i=0;i<nM;i++){
      var v=mu[i]; cell(ws,dataR,6+i,v!=null?(v/1000).toFixed(1):'—',{align:'right',bord:true});
    }
    cell(ws,dataR,lastC,'',{bord:true});
    if(b!=='ALL OTHERS CAMP'){
      scjFy25+=fy25; scjFy26+=fy26;
      for(var j=0;j<nM;j++) scjMonthly[j]+=(mu[j]||0);
    }
    dataR++;
  });

  /* SCJ Combined (sem AOC) */
  var scjDu=scjFy25>0?(scjFy26-scjFy25)/scjFy25*100:null;
  ws.getRow(dataR).height=18;
  cell(ws,dataR,1,'',{bg:C.card,bord:true});
  cell(ws,dataR,2,'= SCJ COMBINED (OFF!+EXPOSIS+XO+S.REP+SBP)',{bg:C.card,fg:C.teal,bold:true,bord:true});
  cell(ws,dataR,3,(scjFy25/1000).toFixed(1),{bg:C.card,fg:C.gray,align:'right',bord:true});
  cell(ws,dataR,4,(scjFy26/1000).toFixed(1),{bg:C.card,fg:C.teal,bold:true,align:'right',bord:true});
  cell(ws,dataR,5,scjDu!=null?fmtPct(scjDu,1):'—',{bg:C.card,fg:scjDu!=null?(scjDu>=0?C.green:C.red):C.gray,bold:true,align:'center',bord:true});
  for(var i=0;i<nM;i++) cell(ws,dataR,6+i,(scjMonthly[i]/1000).toFixed(1),{bg:C.card,fg:C.teal,align:'right',bord:true});
  cell(ws,dataR,lastC,'',{bg:C.card,bord:true});
  dataR++;

  /* Total Mercado */
  if(st.totD){
    var mFy25=st.totD.fytd25_un||0, mFy26=st.totD.fytd26_un||0;
    var mDu=mFy25>0?(mFy26-mFy25)/mFy25*100:null;
    ws.getRow(dataR).height=18;
    cell(ws,dataR,1,'',{bg:C.card,bord:true});
    cell(ws,dataR,2,'= TOTAL MERCADO',{bg:C.card,fg:C.green,bold:true,bord:true});
    cell(ws,dataR,3,(mFy25/1000).toFixed(1),{bg:C.card,fg:C.gray,align:'right',bord:true});
    cell(ws,dataR,4,(mFy26/1000).toFixed(1),{bg:C.card,fg:C.green,bold:true,align:'right',bord:true});
    cell(ws,dataR,5,mDu!=null?fmtPct(mDu,1):'—',{bg:C.card,fg:mDu!=null?(mDu>=0?C.green:C.red):C.gray,bold:true,align:'center',bord:true});
    for(var i=0;i<nM;i++) cell(ws,dataR,6+i,'—',{bg:C.card,fg:C.dim,align:'right',bord:true});
    cell(ws,dataR,lastC,'',{bg:C.card,bord:true});
    dataR++;
  }

  /* Nota */
  ws.mergeCells(dataR,2,dataR,lastC-1);
  var fn=ws.getCell(dataR,2);
  fn.value='Fonte: NielsenIQ Retail Measurement \xb7 Unidades em Mil (Kun) \xb7 FYTD = Σ Jul/25–Mar/26 \xb7 SCJ Combined = todas as marcas exceto ALL OTHERS CAMP \xb7 Exportado: '+new Date().toLocaleString('pt-BR');
  fn.fill={type:'pattern',pattern:'solid',fgColor:{argb:'FFFFFFFF'}};
  fn.font={name:'Calibri',size:8,italic:true,color:{argb:'FF94A3B8'}};
  fn.alignment={horizontal:'center'};

  fillBg(ws,dataR+3,lastC+1);
}

"""

OLD_JANMAR_COMMENT = "/* ── 11c. SHEET — JAN·FEV·MAR COMPARATIVO (Card 2) ── */"
assert h.count(OLD_JANMAR_COMMENT) == 1, f'❌ âncora sheetJanMar comment: {h.count(OLD_JANMAR_COMMENT)}×'
h = h.replace(OLD_JANMAR_COMMENT, SHEET_UNIDADES_FYTD + OLD_JANMAR_COMMENT)
print('✅ FIX 3: sheetUnidadesFYTD adicionada')

# ─────────────────────────────────────────────────────────────────────────────
# FIX 4: buildExcel Card 3 — quando mode='un', chama sheetUnidadesFYTD primeiro
# ─────────────────────────────────────────────────────────────────────────────
OLD_CARD3_BUILD = """      sheetCapa(wb,state);
      sheetBase(wb,state);
      sheetFYTD(wb,state);
      sheetMemCalculo(wb,state);
      sheetTabela1(wb,state);"""

NEW_CARD3_BUILD = """      sheetCapa(wb,state);
      if(state.mode==='un') sheetUnidadesFYTD(wb,state);
      sheetBase(wb,state);
      sheetFYTD(wb,state);
      sheetMemCalculo(wb,state);
      sheetTabela1(wb,state);"""

assert h.count(OLD_CARD3_BUILD) == 1, f'❌ âncora buildExcel Card 3: {h.count(OLD_CARD3_BUILD)}×'
h = h.replace(OLD_CARD3_BUILD, NEW_CARD3_BUILD)
print('✅ FIX 4: buildExcel Card 3 → sheetUnidadesFYTD quando mode=un')

# ─────────────────────────────────────────────────────────────────────────────
# Verificações finais
# ─────────────────────────────────────────────────────────────────────────────
assert "var _bmLbl=st.mode==='un'" in h,                       '❌ _bmLbl sheetBase não encontrado'
assert "var _isUnMode=(st.mode==='un')" in h,                  '❌ _isUnMode não encontrado'
assert "_isUnMode?'Jan/26 Kun'" in h,                          '❌ header Jan/26 Kun não encontrado'
assert "_isUnMode?Math.round(vd.jan_un" in h,                  '❌ cell jan_un não encontrado'
assert "var _ftLbl=st.mode==='un'" in h,                       '❌ _ftLbl sheetFYTD não encontrado'
assert "st.mode==='un')" in h and "_bu-_au" in h,              '❌ sort por fytd26_un não encontrado'
assert "function sheetUnidadesFYTD(wb, st)" in h,              '❌ sheetUnidadesFYTD não encontrado'
assert "UNIDADES FYTD JUL" in h,                               '❌ título aba Unidades não encontrado'
assert "SCJ COMBINED (OFF!+EXPOSIS" in h,                      '❌ SCJ Combined row não encontrado'
assert "if(state.mode==='un') sheetUnidadesFYTD(wb,state)" in h,'❌ call sheetUnidadesFYTD não encontrado'
print('✅ Todas as verificações OK')

print(f'\nTamanho original: {orig_len:,} | Novo: {len(h):,} | Δ: {len(h)-orig_len:+,}')

VER.parent.mkdir(parents=True, exist_ok=True)
VER.write_text(h, encoding='utf-8')
print(f'✅ Versão salva: {VER.name}')
SRC.write_text(h, encoding='utf-8')
print(f'✅ Base ativa atualizada: {SRC.name}')
print('DONE.')
