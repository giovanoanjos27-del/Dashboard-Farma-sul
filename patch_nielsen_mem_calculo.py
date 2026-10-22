"""
patch_nielsen_mem_calculo.py
Substitui a aba "Diagnóstico Automático" pela aba "Memória de Cálculo"
que mostra os dados brutos + fórmulas que geram todos os indicadores Nielsen.

4 seções:
  ① Valor R$M Mensal     — numerador do share (+ total mercado onde disponível)
  ② Share % Mensal       — ValorMarca ÷ TotalMercado × 100, todos os 9 meses
  ③ SCJ Combined         — OFF! + EXPOSIS breakdown mensal + FYTD
  ④ Volume Mensal (Un)   — base para Δ% de volume
"""
import sys
from pathlib import Path
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

BASE = Path(r'C:\Users\valqu\OneDrive\Documentos\Claude\Projects\projeto Dashboard_farma_sul\Dashboard_farma_sul')
SRC  = BASE / 'Dashboard_Farma_Sul_20260512_2220.html'
VER  = BASE / 'versoes' / f'Dashboard_Farma_Sul_{datetime.now().strftime("%Y%m%d_%H%M")}_NielsenMemCalculo.html'

print('Lendo dashboard…')
h = SRC.read_text(encoding='utf-8')
orig_len = len(h)

# ─────────────────────────────────────────────────────────────────────────────
# Ler bloco antigo de sheetDiagnostico para encontrar âncoras
# ─────────────────────────────────────────────────────────────────────────────
OLD_SHEET_START = "/* ── 11. SHEET 5 — DIAGNÓSTICO ── */"
OLD_SHEET_END   = "/* ── 12. Orquestrar a geração ── */"

idx_start = h.find(OLD_SHEET_START)
idx_end   = h.find(OLD_SHEET_END)
assert idx_start != -1, '❌ Não encontrou início de sheetDiagnostico'
assert idx_end   != -1, '❌ Não encontrou início de buildExcel'
assert idx_start < idx_end, '❌ Ordem incorreta'

OLD_DIAG_BLOCK = h[idx_start:idx_end]

NEW_DIAG_BLOCK = r"""/* ── 11. SHEET 5 — MEMÓRIA DE CÁLCULO ── */
function sheetMemCalculo(wb, st){
  var ws = wb.addWorksheet('📐 Memória de Cálculo');
  ws.views = [{showGridLines:false}];
  var nM = st.months.length; /* 9 meses Jul-Mar */

  /* Larguras: margem | marca | 9 meses | FYTD25 | FYTD26 | delta | margem */
  ws.getColumn(1).width = 2;
  ws.getColumn(2).width = 24;
  for(var mi=0;mi<nM;mi++) ws.getColumn(3+mi).width = 8;
  ws.getColumn(3+nM).width = 11;
  ws.getColumn(4+nM).width = 11;
  ws.getColumn(5+nM).width = 10;
  ws.getColumn(6+nM).width = 2;
  var lastC = 6+nM;

  /* ── helpers locais ── */
  function secTitle(r, txt, col){
    ws.getRow(r).height = 21;
    for(var c2=1;c2<=lastC;c2++) cell(ws,r,c2,'',{bg:C.hdr});
    ws.mergeCells(r,2,r,lastC-1);
    var sc = ws.getCell(r,2);
    sc.value = txt;
    sc.fill = {type:'pattern',pattern:'solid',fgColor:{argb:'FF'+C.hdr}};
    sc.font = {name:'Calibri',size:10,bold:true,color:{argb:'FF'+(col||C.gold)}};
    sc.alignment = {vertical:'middle',horizontal:'left'};
  }
  function note(r, txt){
    ws.getRow(r).height = 13;
    ws.mergeCells(r,2,r,lastC-1);
    var nc = ws.getCell(r,2);
    nc.value = txt;
    nc.fill = {type:'pattern',pattern:'solid',fgColor:{argb:'FF0D1117'}};
    nc.font = {name:'Calibri',size:8,italic:true,color:{argb:'FF64748B'}};
    nc.alignment = {horizontal:'left'};
  }
  function hdrRow(r, col1Label, colLabel, lastLbl1, lastLbl2, deltaLbl){
    ws.getRow(r).height = 20;
    hdr(ws,r,1,'',C.hdr,C.gold);
    hdr(ws,r,2,col1Label,C.hdr,colLabel||C.gold);
    st.months.forEach(function(m,i){ hdr(ws,r,3+i,m,C.hdr,C.gold); });
    hdr(ws,r,3+nM,lastLbl1||'FYTD25',C.hdr,C.gray);
    hdr(ws,r,4+nM,lastLbl2||'FYTD26',C.hdr,colLabel||C.teal);
    hdr(ws,r,5+nM,deltaLbl||'Δ',C.hdr,C.gold);
    hdr(ws,r,6+nM,'',C.hdr,C.gold);
  }

  var row = 1;

  /* ══ Título principal ══ */
  ws.getRow(row).height = 28;
  ws.mergeCells(row,2,row,lastC-1);
  var tit = ws.getCell(row,2);
  tit.value = 'MEMÓRIA DE CÁLCULO — ' + st.market + ' — FY26 (Jul/25–Mar/26)';
  tit.fill = {type:'pattern',pattern:'solid',fgColor:{argb:'FF0D1117'}};
  tit.font = {name:'Calibri',size:14,bold:true,color:{argb:'FFF59E0B'}};
  tit.alignment = {vertical:'middle',horizontal:'center'};
  row++;
  ws.getRow(row).height = 14;
  ws.mergeCells(row,2,row,lastC-1);
  var sub = ws.getCell(row,2);
  sub.value = 'Detalhamento dos cálculos que geram os indicadores do relatório Nielsen · NielsenIQ Retail Measurement · SC Johnson';
  sub.fill = {type:'pattern',pattern:'solid',fgColor:{argb:'FF0D1117'}};
  sub.font = {name:'Calibri',size:9,italic:true,color:{argb:'FF64748B'}};
  sub.alignment = {horizontal:'center'};
  row += 2;

  /* ══════════════════════════════════════════════
     SEÇÃO 1 — VALOR R$M MENSAL
  ══════════════════════════════════════════════ */
  secTitle(row, '① VALOR R$M MENSAL  —  numerador do cálculo de Share%', C.teal);
  row++;
  hdrRow(row, 'Marca / Fonte', C.teal, 'FYTD25 R$M', 'FYTD26 R$M', 'Δ Val%');
  row++;

  st.brands.forEach(function(b){
    var vd = st.valD ? st.valD[b] : null; if(!vd) return;
    var bc = BRAND_COL[b]||C.white;
    var mv = vd.monthly_val||[];
    var dv = vd.fytd25_val>0 ? (vd.fytd26_val-vd.fytd25_val)/vd.fytd25_val*100 : null;
    ws.getRow(row).height = 17;
    cell(ws,row,1,'',{bord:true});
    cell(ws,row,2,b,{fg:bc,bold:true,bord:true});
    for(var i=0;i<nM;i++){
      var v = mv[i];
      cell(ws,row,3+i, v!=null?+v.toFixed(4):0, {align:'right',bord:true});
    }
    cell(ws,row,3+nM, vd.fytd25_val!=null?+vd.fytd25_val.toFixed(4):0, {fg:C.gray,align:'right',bord:true});
    cell(ws,row,4+nM, vd.fytd26_val!=null?+vd.fytd26_val.toFixed(4):0, {fg:bc,bold:true,align:'right',bord:true});
    cell(ws,row,5+nM, dv!=null?fmtPct(dv,1):'—', {fg:dv!=null?(dv>=0?C.green:C.red):C.gray,align:'center',bord:true});
    cell(ws,row,6+nM,'',{bord:true});
    row++;
  });

  /* Linha total mercado */
  if(st.totD){
    var totMonths = [null,null,null,null,null,null,
      st.totD.jan26_val||null, st.totD.fev26_val||null, st.totD.mar26_val||null];
    var dtot = st.totD.fytd25_val>0
      ? (st.totD.fytd26_val-st.totD.fytd25_val)/st.totD.fytd25_val*100 : null;
    ws.getRow(row).height = 18;
    cell(ws,row,1,'',{bg:C.card,bord:true});
    cell(ws,row,2,'= TOTAL MERCADO (denominador)',{bg:C.card,fg:C.teal,bold:true,bord:true});
    for(var i=0;i<nM;i++){
      var tv = totMonths[i];
      cell(ws,row,3+i, tv!=null?+tv.toFixed(4):'—', {bg:C.card,fg:tv!=null?C.teal:C.dim,align:'right',bord:true});
    }
    cell(ws,row,3+nM, st.totD.fytd25_val!=null?+st.totD.fytd25_val.toFixed(4):0, {bg:C.card,fg:C.gray,align:'right',bord:true});
    cell(ws,row,4+nM, st.totD.fytd26_val!=null?+st.totD.fytd26_val.toFixed(4):0, {bg:C.card,fg:C.teal,bold:true,align:'right',bord:true});
    cell(ws,row,5+nM, dtot!=null?fmtPct(dtot,1):'—', {bg:C.card,fg:dtot!=null?(dtot>=0?C.green:C.red):C.gray,align:'center',bord:true});
    cell(ws,row,6+nM,'',{bg:C.card,bord:true});
    row++;
  }
  note(row,'  "—" = valor mensal do total de mercado não disponível por mês individual neste período (Jul–Dez). Disponível: Jan/Fev/Mar e FYTD total.');
  row += 2;

  /* ══════════════════════════════════════════════
     SEÇÃO 2 — SHARE % MENSAL
  ══════════════════════════════════════════════ */
  secTitle(row, '② SHARE % MENSAL  —  Fórmula: ValorMarca ÷ TotalMercado × 100', C.green);
  row++;
  hdrRow(row, 'Marca', C.green, 'FYTD25 %', 'FYTD26 %', 'Δ pp');
  row++;

  st.brands.forEach(function(b){
    var rd = st.msoD[b]; if(!rd) return;
    var bc = BRAND_COL[b]||C.white;
    var d = rd.delta||0; var dc = deltaColor(d);
    var monthly = rd.monthly||[];
    ws.getRow(row).height = 17;
    cell(ws,row,1,'',{bord:true});
    cell(ws,row,2,b,{fg:bc,bold:true,bord:true});
    for(var i=0;i<nM;i++){
      var v = monthly[i];
      cell(ws,row,3+i, v!=null?+v.toFixed(2)+'%':'—', {align:'center',bord:true});
    }
    cell(ws,row,3+nM, (rd.fytd25||0).toFixed(2)+'%', {fg:C.gray,align:'center',bord:true});
    cell(ws,row,4+nM, (rd.fytd26||0).toFixed(2)+'%', {fg:bc,bold:true,align:'center',bord:true});
    cell(ws,row,5+nM, fmtPp(d), {fg:dc,bold:true,align:'center',bord:true});
    cell(ws,row,6+nM,'',{bord:true});
    row++;
  });
  note(row,'  Share% mensal = ValorMarca(mês) ÷ TotalMercado(mês) × 100  |  FYTD% = Σ ValorMarca(Jul–Mar) ÷ Σ TotalMercado(FYTD) × 100  |  Δpp = FYTD26% − FYTD25%');

  /* verificação Jan/Fev/Mar onde temos totais mensais */
  if(st.totD && st.totD.jan26_val){
    row++;
    ws.getRow(row).height = 13;
    ws.mergeCells(row,2,row,lastC-1);
    var vn = ws.getCell(row,2);
    vn.value = '  Verificação Jan/26: OFF! '
      + (st.valD&&st.valD['OFF!']?(st.valD['OFF!'].jan_val||0).toFixed(4):'—')
      + ' ÷ ' + (st.totD.jan26_val||0).toFixed(4)
      + ' × 100 = '
      + (st.valD&&st.valD['OFF!']&&st.totD.jan26_val
          ? ((st.valD['OFF!'].jan_val||0)/st.totD.jan26_val*100).toFixed(2)+'%'
          : '—')
      + '  |  Fev/26: OFF! '
      + (st.valD&&st.valD['OFF!']?(st.valD['OFF!'].fev_val||0).toFixed(4):'—')
      + ' ÷ ' + (st.totD.fev26_val||0).toFixed(4)
      + ' × 100 = '
      + (st.valD&&st.valD['OFF!']&&st.totD.fev26_val
          ? ((st.valD['OFF!'].fev_val||0)/st.totD.fev26_val*100).toFixed(2)+'%'
          : '—');
    vn.fill = {type:'pattern',pattern:'solid',fgColor:{argb:'FF0D1117'}};
    vn.font = {name:'Calibri',size:8,italic:true,color:{argb:'FF64748B'}};
    vn.alignment = {horizontal:'left'};
  }
  row += 2;

  /* ══════════════════════════════════════════════
     SEÇÃO 3 — SCJ COMBINED
  ══════════════════════════════════════════════ */
  secTitle(row, '③ SCJ COMBINED  —  OFF! + EXPOSIS  |  Share% e Valor R$M', C.blue);
  row++;

  var offD = st.msoD['OFF!']||{};
  var expD = st.msoD['EXPOSIS']||{};
  var offV = st.valD?(st.valD['OFF!']||{}):{};
  var expV = st.valD?(st.valD['EXPOSIS']||{}):{};
  var offM = offD.monthly||[]; var expM = expD.monthly||[];
  var offV_m = offV.monthly_val||[]; var expV_m = expV.monthly_val||[];

  /* Header share */
  hdrRow(row, 'Componente (Share %)', C.blue, 'FYTD25 %', 'FYTD26 %', 'Δ pp');
  row++;

  var scjShare = [
    {label:'OFF! Share %', monthly:offM, fy25:(offD.fytd25||0).toFixed(2)+'%', fy26:(offD.fytd26||0).toFixed(2)+'%', d:offD.delta||0, fg:BRAND_COL['OFF!']||C.white, bold:false},
    {label:'EXPOSIS Share %', monthly:expM, fy25:(expD.fytd25||0).toFixed(2)+'%', fy26:(expD.fytd26||0).toFixed(2)+'%', d:expD.delta||0, fg:BRAND_COL['EXPOSIS']||C.white, bold:false},
    {label:'= SCJ Combined Share %',
      monthly: offM.map(function(v,i){ return (v!=null&&expM[i]!=null)?+(v+expM[i]).toFixed(2):null; }),
      fy25: ((offD.fytd25||0)+(expD.fytd25||0)).toFixed(2)+'%',
      fy26: ((offD.fytd26||0)+(expD.fytd26||0)).toFixed(2)+'%',
      d: ((offD.fytd26||0)+(expD.fytd26||0))-((offD.fytd25||0)+(expD.fytd25||0)),
      fg:C.teal, bold:true}
  ];
  scjShare.forEach(function(sr){
    ws.getRow(row).height = 17;
    var bg2 = sr.bold?C.card:C.dark;
    cell(ws,row,1,'',{bg:bg2,bord:true});
    cell(ws,row,2,sr.label,{bg:bg2,fg:sr.fg,bold:sr.bold,bord:true});
    for(var i=0;i<nM;i++){
      var v=sr.monthly[i];
      cell(ws,row,3+i, v!=null?v.toFixed(2)+'%':'—', {bg:bg2,align:'center',bord:true,fg:sr.bold?sr.fg:C.white});
    }
    cell(ws,row,3+nM,sr.fy25,{bg:bg2,fg:C.gray,align:'center',bord:true});
    cell(ws,row,4+nM,sr.fy26,{bg:bg2,fg:sr.fg,bold:sr.bold,align:'center',bord:true});
    cell(ws,row,5+nM,fmtPp(sr.d),{bg:bg2,fg:deltaColor(sr.d),bold:sr.bold,align:'center',bord:true});
    cell(ws,row,6+nM,'',{bg:bg2,bord:true});
    row++;
  });

  row++;
  /* Header valor */
  hdrRow(row, 'Componente (Valor R$M)', C.blue, 'FYTD25 R$M', 'FYTD26 R$M', 'Δ Val%');
  row++;

  var scjVal = [
    {label:'OFF! Valor R$M', monthly:offV_m, fy25:(offV.fytd25_val||0), fy26:(offV.fytd26_val||0), fg:BRAND_COL['OFF!']||C.white, bold:false},
    {label:'EXPOSIS Valor R$M', monthly:expV_m, fy25:(expV.fytd25_val||0), fy26:(expV.fytd26_val||0), fg:BRAND_COL['EXPOSIS']||C.white, bold:false},
    {label:'= Total SCJ Valor R$M',
      monthly: offV_m.map(function(v,i){ return (v!=null&&expV_m[i]!=null)?+(v+expV_m[i]).toFixed(4):null; }),
      fy25:(offV.fytd25_val||0)+(expV.fytd25_val||0),
      fy26:(offV.fytd26_val||0)+(expV.fytd26_val||0),
      fg:C.teal, bold:true}
  ];
  scjVal.forEach(function(sr){
    ws.getRow(row).height = 17;
    var bg2 = sr.bold?C.card:C.dark;
    var dv = sr.fy25>0?(sr.fy26-sr.fy25)/sr.fy25*100:null;
    cell(ws,row,1,'',{bg:bg2,bord:true});
    cell(ws,row,2,sr.label,{bg:bg2,fg:sr.fg,bold:sr.bold,bord:true});
    for(var i=0;i<nM;i++){
      var v=sr.monthly[i];
      cell(ws,row,3+i, v!=null?+v.toFixed(4):0, {bg:bg2,align:'right',bord:true,fg:sr.bold?sr.fg:C.white});
    }
    cell(ws,row,3+nM, +sr.fy25.toFixed(4), {bg:bg2,fg:C.gray,align:'right',bord:true});
    cell(ws,row,4+nM, +sr.fy26.toFixed(4), {bg:bg2,fg:sr.fg,bold:sr.bold,align:'right',bord:true});
    cell(ws,row,5+nM, dv!=null?fmtPct(dv,1):'—', {bg:bg2,fg:dv!=null?(dv>=0?C.green:C.red):C.gray,align:'center',bord:true});
    cell(ws,row,6+nM,'',{bg:bg2,bord:true});
    row++;
  });
  row += 2;

  /* ══════════════════════════════════════════════
     SEÇÃO 4 — VOLUME MENSAL
  ══════════════════════════════════════════════ */
  secTitle(row, '④ VOLUME MENSAL (Unidades)  —  base para cálculo de Δ% Volume', C.amber);
  row++;
  hdrRow(row, 'Marca', C.amber, 'FYTD25 Un', 'FYTD26 Un', 'Δ Vol%');
  row++;

  st.brands.forEach(function(b){
    var vd = st.valD?st.valD[b]:null; if(!vd) return;
    var bc = BRAND_COL[b]||C.white;
    var mu = vd.monthly_un||[];
    var du = vd.fytd25_un>0?(vd.fytd26_un-vd.fytd25_un)/vd.fytd25_un*100:null;
    ws.getRow(row).height = 17;
    cell(ws,row,1,'',{bord:true});
    cell(ws,row,2,b,{fg:bc,bold:true,bord:true});
    for(var i=0;i<nM;i++){
      var v=mu[i];
      cell(ws,row,3+i, v!=null?Math.round(v):0, {align:'right',bord:true});
    }
    cell(ws,row,3+nM, vd.fytd25_un!=null?Math.round(vd.fytd25_un):0, {fg:C.gray,align:'right',bord:true});
    cell(ws,row,4+nM, vd.fytd26_un!=null?Math.round(vd.fytd26_un):0, {fg:bc,bold:true,align:'right',bord:true});
    cell(ws,row,5+nM, du!=null?fmtPct(du,1):'—', {fg:du!=null?(du>=0?C.green:C.red):C.gray,align:'center',bord:true});
    cell(ws,row,6+nM,'',{bord:true});
    row++;
  });
  note(row,'  Δ% Volume = (FYTD26_Un − FYTD25_Un) ÷ FYTD25_Un × 100');
  row += 2;

  /* Nota de rodapé */
  ws.mergeCells(row,2,row,lastC-1);
  var fn = ws.getCell(row,2);
  fn.value = 'Fonte: NielsenIQ Retail Measurement · PS · GBL · SC JOHNSON · BR · PEST CONTROL · Exportado: '+new Date().toLocaleString('pt-BR');
  fn.fill = {type:'pattern',pattern:'solid',fgColor:{argb:'FF0D1117'}};
  fn.font = {name:'Calibri',size:8,italic:true,color:{argb:'FF64748B'}};
  fn.alignment = {horizontal:'center'};

  fillBg(ws, row+3, lastC+1);
}

"""

h = h[:idx_start] + NEW_DIAG_BLOCK + h[idx_end:]
print('✅ sheetDiagnostico substituído por sheetMemCalculo')

# ─────────────────────────────────────────────────────────────────────────────
# 2. Atualizar chamada em buildExcel
# ─────────────────────────────────────────────────────────────────────────────
OLD_CALL = '    sheetDiagnostico(wb,state);'
NEW_CALL = '    sheetMemCalculo(wb,state);'
assert h.count(OLD_CALL) == 1, f'sheetDiagnostico call: encontrei {h.count(OLD_CALL)} (esperava 1)'
h = h.replace(OLD_CALL, NEW_CALL)
print('✅ Chamada buildExcel atualizada')

# ─────────────────────────────────────────────────────────────────────────────
# Verificações
# ─────────────────────────────────────────────────────────────────────────────
assert 'sheetMemCalculo' in h,            '❌ sheetMemCalculo não encontrado'
assert 'Memória de Cálculo' in h,         '❌ nome da aba não encontrado'
assert 'sheetDiagnostico' not in h,       '❌ sheetDiagnostico ainda presente'
assert 'TOTAL MERCADO (denominador)' in h,'❌ seção 1 não encontrada'
assert 'ValorMarca' in h,                 '❌ fórmula seção 2 não encontrada'
assert 'SCJ COMBINED' in h,               '❌ seção 3 não encontrada'
assert 'VOLUME MENSAL' in h,              '❌ seção 4 não encontrada'
print('✅ Verificações OK')

print(f'\nTamanho original: {orig_len:,} | Novo: {len(h):,} | Δ: {len(h)-orig_len:+,}')

VER.parent.mkdir(parents=True, exist_ok=True)
VER.write_text(h, encoding='utf-8')
print(f'✅ Versão salva: {VER.name}')
SRC.write_text(h, encoding='utf-8')
print(f'✅ Base ativa atualizada: {SRC.name}')
print('DONE.')
