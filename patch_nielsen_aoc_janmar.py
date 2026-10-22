"""
patch_nielsen_aoc_janmar.py
Fix completo — Card 2 (Jan-Mar): ALL OTHERS CAMP + Export Excel.

FIX 1+2: chartBrandsBar2 — adiciona ALL OTHERS CAMP no gráfico de barras
  R$/Unidades. Share continua sem AOC. Carrega d25/d26 de AOC antes do chart.

FIX 3: Tooltip (title+label) no gráfico de barras usa chartBrandsBar2
  em vez de brands (que não tem AOC).

FIX 4: Diagnóstico renderMSO2Insight — lines2 inclui AOC quando
  mso2Mode != 'share'; exclui quando share (sem alterar cálculos SCJ).

FIX 5: getState() captura mso2Mode para card 2 (análogo ao mso3Mode).

FIX 6a: sheetJanMar — título e subtítulo dinâmicos conforme st.mode.

FIX 6b: sheetJanMar seção ② Valor R$M — adiciona linha AOC após marcas SCJ
  (somente quando st.mode != 'share').

FIX 6c: sheetJanMar — adiciona seção ③ Unidades (antes da Nota),
  com AOC quando st.mode != 'share'.

FIX 7: buildExcel card 2 — filename reflete modo ativo:
  Nielsen_Share_JanMar_*.xlsx / Nielsen_RMM_JanMar_*.xlsx /
  Nielsen_Unidades_JanMar_*.xlsx.

NÃO ALTERA:
  - brands (filtro SCJ, sem AOC) em cálculos de KPI, share e linhas
  - Cards 1 e 3
  - Sell Out, Sell In, Cobertura, OLs, Acumulado FY, outros gráficos
"""
import sys
from pathlib import Path
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

BASE = Path(r'C:\Users\valqu\OneDrive\Documentos\Claude\Projects\projeto Dashboard_farma_sul\Dashboard_farma_sul')
SRC  = BASE / 'Dashboard_Farma_Sul_20260512_2220.html'
VER  = BASE / 'versoes' / f'Dashboard_Farma_Sul_{datetime.now().strftime("%Y%m%d_%H%M")}_AocJanMar.html'

print('Lendo dashboard…')
h = SRC.read_text(encoding='utf-8')
orig_len = len(h)

# ─────────────────────────────────────────────────────────────────────────────
# FIX 1+2: chartBrandsBar2 + carregamento AOC + usar no gráfico de barras val/un
# ─────────────────────────────────────────────────────────────────────────────
OLD_BAR2 = """      var barLabels2 = brands.map(function(b){ return b==='SUPER REPELEX'?'S.REPELEX':b; });
      var bVals25=[],bVals26=[],bColors2=[],bDeltas2=[],bDeltaStrs2=[];
      brands.forEach(function(b){
        var p25=d25[b],p26=d26[b];"""

NEW_BAR2 = """      /* chartBrandsBar2: R$/Unidades inclui ALL OTHERS CAMP; Share usa brands (sem AOC) */
      var chartBrandsBar2 = MSO_BRANDS;
      /* Carregar d25/d26 de ALL OTHERS CAMP a partir de nbvS */
      if(nbvS && nbvS['ALL OTHERS CAMP']){
        var _aoc=nbvS['ALL OTHERS CAMP'];
        var _aocJ26=isVal?_aoc.jan_val:_aoc.jan_un, _aocF26=isVal?_aoc.fev_val:_aoc.fev_un, _aocM26=isVal?_aoc.mar_val:_aoc.mar_un;
        var _aocA26=Math.round((_aocJ26+_aocF26+_aocM26)*100)/100;
        var _aocHasEx=isVal?(_aoc.jan25_val!==undefined):(_aoc.jan25_un!==undefined);
        var _aocA25;
        if(_aocHasEx){
          _aocA25=Math.round(((isVal?_aoc.jan25_val:_aoc.jan25_un)+(isVal?_aoc.fev25_val:_aoc.fev25_un)+(isVal?_aoc.mar25_val:_aoc.mar25_un))*100)/100;
        } else {
          var _aocFyt25=isVal?_aoc.fytd25_val:_aoc.fytd25_un, _aocFyt26=isVal?_aoc.fytd26_val:_aoc.fytd26_un;
          _aocA25=Math.round(_aocFyt25*(_aocFyt26>0?_aocA26/_aocFyt26:1/3)*100)/100;
        }
        d25['ALL OTHERS CAMP']={jan:null,fev:null,mar:null,acum:_aocA25};
        d26['ALL OTHERS CAMP']={jan:_aocJ26,fev:_aocF26,mar:_aocM26,acum:_aocA26};
      }
      var barLabels2 = chartBrandsBar2.map(function(b){ return b==='SUPER REPELEX'?'S.REPELEX':b; });
      var bVals25=[],bVals26=[],bColors2=[],bDeltas2=[],bDeltaStrs2=[];
      chartBrandsBar2.forEach(function(b){
        var p25=d25[b],p26=d26[b];"""

assert h.count(OLD_BAR2) == 1, f'❌ âncora barLabels2: {h.count(OLD_BAR2)}×'
h = h.replace(OLD_BAR2, NEW_BAR2)
print('✅ FIX 1+2: chartBrandsBar2 + carregamento AOC + barLabels2/forEach')

# ─────────────────────────────────────────────────────────────────────────────
# FIX 3: Tooltip title/label no gráfico de barras val/un → chartBrandsBar2
# ─────────────────────────────────────────────────────────────────────────────
OLD_TIP2 = """                title:function(items){ return brands[items[0].dataIndex]; },
                label:function(ctx){
                  var b=brands[ctx.dataIndex];"""

NEW_TIP2 = """                title:function(items){ return chartBrandsBar2[items[0].dataIndex]; },
                label:function(ctx){
                  var b=chartBrandsBar2[ctx.dataIndex];"""

assert h.count(OLD_TIP2) == 1, f'❌ âncora tooltip brands: {h.count(OLD_TIP2)}×'
h = h.replace(OLD_TIP2, NEW_TIP2)
print('✅ FIX 3: tooltip title/label → chartBrandsBar2')

# ─────────────────────────────────────────────────────────────────────────────
# FIX 4: Diagnóstico renderMSO2Insight — lines2 condicional (AOC em val/un)
# ─────────────────────────────────────────────────────────────────────────────
OLD_LINES2 = "  var lines2 = MSO_BRANDS.filter(function(b){return b!=='ALL OTHERS CAMP';}).map(function(b){"

NEW_LINES2 = "  /* lines2: inclui ALL OTHERS CAMP em val/un; exclui em share (cálculos SCJ intactos) */\n  var lines2 = (mso2Mode!=='share' ? MSO_BRANDS : MSO_BRANDS.filter(function(b){return b!=='ALL OTHERS CAMP';})).map(function(b){"

assert h.count(OLD_LINES2) == 1, f'❌ âncora lines2: {h.count(OLD_LINES2)}×'
h = h.replace(OLD_LINES2, NEW_LINES2)
print('✅ FIX 4: lines2 diagnóstico condicional (AOC em val/un)')

# ─────────────────────────────────────────────────────────────────────────────
# FIX 5: getState() — capturar mso2Mode para card 2
# ─────────────────────────────────────────────────────────────────────────────
OLD_GETSTATE = "  if(selId === 'mso3MarketSel' && typeof mso3Mode !== 'undefined') mode = mso3Mode;"

NEW_GETSTATE = """  if(selId === 'mso3MarketSel' && typeof mso3Mode !== 'undefined') mode = mso3Mode;
  if(selId === 'mso2MarketSel' && typeof mso2Mode !== 'undefined') mode = mso2Mode;"""

assert h.count(OLD_GETSTATE) == 1, f'❌ âncora getState mso3: {h.count(OLD_GETSTATE)}×'
h = h.replace(OLD_GETSTATE, NEW_GETSTATE)
print('✅ FIX 5: getState() captura mso2Mode')

# ─────────────────────────────────────────────────────────────────────────────
# FIX 6a: sheetJanMar — título dinâmico por modo
# ─────────────────────────────────────────────────────────────────────────────
OLD_TITLE_JM = "  t.value='MARKET SHARE — JAN · FEV · MAR — 2025 vs 2026 · '+st.market;"

NEW_TITLE_JM = """  var _jmLbl=st.mode==='share'?'MARKET SHARE %':(st.mode==='un'?'UNIDADES':'R$ MILHÕES');
  t.value='NIELSEN PERFORMANCE — JAN · FEV · MAR — '+_jmLbl+' — 2025 vs 2026 · '+st.market.toUpperCase();"""

assert h.count(OLD_TITLE_JM) == 1, f'❌ âncora title JanMar: {h.count(OLD_TITLE_JM)}×'
h = h.replace(OLD_TITLE_JM, NEW_TITLE_JM)
print('✅ FIX 6a: título sheetJanMar dinâmico por modo')

OLD_SUB_JM = "  s2.value='Acumulado Jan–Mar \xb7 Share% por Marca \xb7 NielsenIQ Retail Measurement \xb7 Exportado '+new Date().toLocaleDateString('pt-BR');"

NEW_SUB_JM = "  s2.value='Acumulado Jan–Mar \xb7 '+_jmLbl+' por Marca \xb7 NielsenIQ Retail Measurement \xb7 Exportado '+new Date().toLocaleDateString('pt-BR');"

assert h.count(OLD_SUB_JM) == 1, f'❌ âncora subtitle JanMar: {h.count(OLD_SUB_JM)}×'
h = h.replace(OLD_SUB_JM, NEW_SUB_JM)
print('✅ FIX 6a: subtítulo sheetJanMar dinâmico por modo')

# ─────────────────────────────────────────────────────────────────────────────
# FIX 6b: sheetJanMar seção ② — adicionar linha AOC antes do Total Mercado
# ─────────────────────────────────────────────────────────────────────────────
OLD_TOTMKT = """  /* Total mercado */
  if(st.totD){
    var tot25m=st.totD.janmar25_val||0; var tot26m=st.totD.janmar26_val||0;"""

NEW_TOTMKT = """  /* ALL OTHERS CAMP — seção ② Valor R$M (somente quando modo != share) */
  if(st.mode!=='share' && st.valD && st.valD['ALL OTHERS CAMP']){
    var _aocV=st.valD['ALL OTHERS CAMP'];
    var _aocJ25v=_aocV.jan25_val||0, _aocF25v=_aocV.fev25_val||0, _aocM25v=_aocV.mar25_val||0;
    var _aocJ26v=_aocV.jan_val||0,   _aocF26v=_aocV.fev_val||0,   _aocM26v=_aocV.mar_val||0;
    var _aocTot25v=_aocJ25v+_aocF25v+_aocM25v, _aocTot26v=_aocJ26v+_aocF26v+_aocM26v;
    var _aocDv=_aocTot25v>0?(_aocTot26v-_aocTot25v)/_aocTot25v*100:null;
    ws.getRow(dataR).height=18;
    cell(ws,dataR,1,'',{bord:true});
    cell(ws,dataR,2,'ALL OTHERS CAMP',{fg:C.gray,bold:true,bord:true});
    cell(ws,dataR,3,_aocJ25v.toFixed(3),{fg:C.gray,align:'right',bord:true});
    cell(ws,dataR,4,_aocF25v.toFixed(3),{fg:C.gray,align:'right',bord:true});
    cell(ws,dataR,5,_aocM25v.toFixed(3),{fg:C.gray,align:'right',bord:true});
    cell(ws,dataR,6,_aocTot25v.toFixed(3),{fg:C.gray,bold:true,align:'right',bord:true,bg:'EEF2FF'});
    cell(ws,dataR,7,_aocJ26v.toFixed(3),{fg:C.gray,align:'right',bord:true});
    cell(ws,dataR,8,_aocF26v.toFixed(3),{fg:C.gray,align:'right',bord:true});
    cell(ws,dataR,9,_aocM26v.toFixed(3),{fg:C.gray,align:'right',bord:true});
    cell(ws,dataR,10,_aocTot26v.toFixed(3),{fg:C.gray,bold:true,align:'right',bord:true,bg:'EEF2FF'});
    cell(ws,dataR,11,_aocDv!=null?fmtPct(_aocDv,1):'—',{fg:_aocDv!=null?deltaColor(_aocDv):C.gray,bold:true,align:'center',bord:true});
    cell(ws,dataR,12,'',{bord:true});
    dataR++;
  }
  /* Total mercado */
  if(st.totD){
    var tot25m=st.totD.janmar25_val||0; var tot26m=st.totD.janmar26_val||0;"""

assert h.count(OLD_TOTMKT) == 1, f'❌ âncora Total mercado: {h.count(OLD_TOTMKT)}×'
h = h.replace(OLD_TOTMKT, NEW_TOTMKT)
print('✅ FIX 6b: seção ② recebe linha ALL OTHERS CAMP (val/un)')

# ─────────────────────────────────────────────────────────────────────────────
# FIX 6c: sheetJanMar — adicionar seção ③ Unidades antes da Nota
# ─────────────────────────────────────────────────────────────────────────────
OLD_NOTA = """  /* Nota */
  ws.mergeCells(dataR,2,dataR,lastC-1);
  var fn=ws.getCell(dataR,2);
  fn.value='Fonte: NielsenIQ Retail Measurement \xb7 Acum Jan\xb7Fev\xb7Mar \xb7 Share% = ΣValMarca(JanMar) \xf7 ΣMercado(JanMar) \xd7 100 \xb7 Exportado '+new Date().toLocaleString('pt-BR');"""

NEW_NOTA = """  /* ── Seção 3: Unidades ── */
  ws.getRow(dataR).height=18;
  ws.mergeCells(dataR,2,dataR,lastC-1);
  var sc3=ws.getCell(dataR,2);
  sc3.value='③ UNIDADES — Jan\xb7Fev\xb7Mar';
  sc3.fill={type:'pattern',pattern:'solid',fgColor:{argb:'FF166534'}};
  sc3.font={name:'Calibri',size:10,bold:true,color:{argb:'FFFFFFFF'}};
  sc3.alignment={vertical:'middle',horizontal:'left'};
  cell(ws,dataR,1,'',{bg:'166534'}); cell(ws,dataR,lastC,'',{bg:'166534'});
  dataR++;
  var uhdrs=['','Marca','Jan/25','Fev/25','Mar/25','JanMar25 K Un','Jan/26','Fev/26','Mar/26','JanMar26 K Un','Δ Un%',''];
  uhdrs.forEach(function(v,i){ hdr(ws,dataR,i+1,v,'D9E1F2','1E293B'); });
  ws.getRow(dataR).height=18;
  dataR++;
  st.brands.forEach(function(b){
    var ud=st.valD?st.valD[b]:null; if(!ud) return;
    var bc=BRAND_COL[b]||C.white;
    var j25u=ud.jan25_un||0; var f25u=ud.fev25_un||0; var m25u=ud.mar25_un||0;
    var j26u=ud.jan_un||0;   var f26u=ud.fev_un||0;   var m26u=ud.mar_un||0;
    var tot25u=j25u+f25u+m25u; var tot26u=j26u+f26u+m26u;
    var du=tot25u>0?(tot26u-tot25u)/tot25u*100:null;
    ws.getRow(dataR).height=18;
    cell(ws,dataR,1,'',{bord:true});
    cell(ws,dataR,2,b,{fg:bc,bold:true,bord:true});
    cell(ws,dataR,3,Math.round(j25u).toString(),{fg:C.gray,align:'right',bord:true});
    cell(ws,dataR,4,Math.round(f25u).toString(),{fg:C.gray,align:'right',bord:true});
    cell(ws,dataR,5,Math.round(m25u).toString(),{fg:C.gray,align:'right',bord:true});
    cell(ws,dataR,6,Math.round(tot25u).toString(),{fg:C.gray,bold:true,align:'right',bord:true,bg:'EEF2FF'});
    cell(ws,dataR,7,Math.round(j26u).toString(),{fg:bc,align:'right',bord:true});
    cell(ws,dataR,8,Math.round(f26u).toString(),{fg:bc,align:'right',bord:true});
    cell(ws,dataR,9,Math.round(m26u).toString(),{fg:bc,align:'right',bord:true});
    cell(ws,dataR,10,Math.round(tot26u).toString(),{fg:bc,bold:true,align:'right',bord:true,bg:'EEF2FF'});
    cell(ws,dataR,11,du!=null?fmtPct(du,1):'—',{fg:du!=null?deltaColor(du):C.gray,bold:true,align:'center',bord:true});
    cell(ws,dataR,12,'',{bord:true});
    dataR++;
  });
  /* ALL OTHERS CAMP — seção ③ Unidades (somente quando modo != share) */
  if(st.mode!=='share' && st.valD && st.valD['ALL OTHERS CAMP']){
    var _aocU=st.valD['ALL OTHERS CAMP'];
    var _aocJ25u=_aocU.jan25_un||0, _aocF25u=_aocU.fev25_un||0, _aocM25u=_aocU.mar25_un||0;
    var _aocJ26u=_aocU.jan_un||0,   _aocF26u=_aocU.fev_un||0,   _aocM26u=_aocU.mar_un||0;
    var _aocTot25u=_aocJ25u+_aocF25u+_aocM25u, _aocTot26u=_aocJ26u+_aocF26u+_aocM26u;
    var _aocDu=_aocTot25u>0?(_aocTot26u-_aocTot25u)/_aocTot25u*100:null;
    ws.getRow(dataR).height=18;
    cell(ws,dataR,1,'',{bord:true});
    cell(ws,dataR,2,'ALL OTHERS CAMP',{fg:C.gray,bold:true,bord:true});
    cell(ws,dataR,3,Math.round(_aocJ25u).toString(),{fg:C.gray,align:'right',bord:true});
    cell(ws,dataR,4,Math.round(_aocF25u).toString(),{fg:C.gray,align:'right',bord:true});
    cell(ws,dataR,5,Math.round(_aocM25u).toString(),{fg:C.gray,align:'right',bord:true});
    cell(ws,dataR,6,Math.round(_aocTot25u).toString(),{fg:C.gray,bold:true,align:'right',bord:true,bg:'EEF2FF'});
    cell(ws,dataR,7,Math.round(_aocJ26u).toString(),{fg:C.gray,align:'right',bord:true});
    cell(ws,dataR,8,Math.round(_aocF26u).toString(),{fg:C.gray,align:'right',bord:true});
    cell(ws,dataR,9,Math.round(_aocM26u).toString(),{fg:C.gray,align:'right',bord:true});
    cell(ws,dataR,10,Math.round(_aocTot26u).toString(),{fg:C.gray,bold:true,align:'right',bord:true,bg:'EEF2FF'});
    cell(ws,dataR,11,_aocDu!=null?fmtPct(_aocDu,1):'—',{fg:_aocDu!=null?deltaColor(_aocDu):C.gray,bold:true,align:'center',bord:true});
    cell(ws,dataR,12,'',{bord:true});
    dataR++;
  }
  /* Total mercado — Unidades */
  if(st.totD){
    var tot25mu=st.totD.janmar25_un||0; var tot26mu=st.totD.janmar26_un||0;
    var dtotu=tot25mu>0?(tot26mu-tot25mu)/tot25mu*100:null;
    ws.getRow(dataR).height=18;
    cell(ws,dataR,1,'',{bg:'EEF2FF',bord:true});
    cell(ws,dataR,2,'= TOTAL MERCADO',{bg:'EEF2FF',fg:C.green,bold:true,bord:true});
    cell(ws,dataR,3,Math.round(st.totD.jan25_un||0).toString(),{bg:'EEF2FF',fg:C.gray,align:'right',bord:true});
    cell(ws,dataR,4,Math.round(st.totD.fev25_un||0).toString(),{bg:'EEF2FF',fg:C.gray,align:'right',bord:true});
    cell(ws,dataR,5,Math.round(st.totD.mar25_un||0).toString(),{bg:'EEF2FF',fg:C.gray,align:'right',bord:true});
    cell(ws,dataR,6,Math.round(tot25mu).toString(),{bg:'EEF2FF',fg:C.gray,bold:true,align:'right',bord:true});
    cell(ws,dataR,7,Math.round(st.totD.jan26_un||0).toString(),{bg:'EEF2FF',fg:C.green,align:'right',bord:true});
    cell(ws,dataR,8,Math.round(st.totD.fev26_un||0).toString(),{bg:'EEF2FF',fg:C.green,align:'right',bord:true});
    cell(ws,dataR,9,Math.round(st.totD.mar26_un||0).toString(),{bg:'EEF2FF',fg:C.green,align:'right',bord:true});
    cell(ws,dataR,10,Math.round(tot26mu).toString(),{bg:'EEF2FF',fg:C.green,bold:true,align:'right',bord:true});
    cell(ws,dataR,11,dtotu!=null?fmtPct(dtotu,1):'—',{bg:'EEF2FF',fg:dtotu!=null?deltaColor(dtotu):C.gray,bold:true,align:'center',bord:true});
    cell(ws,dataR,12,'',{bg:'EEF2FF',bord:true});
    dataR++;
  }
  dataR++;

  /* Nota */
  ws.mergeCells(dataR,2,dataR,lastC-1);
  var fn=ws.getCell(dataR,2);
  fn.value='Fonte: NielsenIQ Retail Measurement \xb7 Acum Jan\xb7Fev\xb7Mar \xb7 Share% = ΣValMarca(JanMar) \xf7 ΣMercado(JanMar) \xd7 100 \xb7 Exportado '+new Date().toLocaleString('pt-BR');"""

assert h.count(OLD_NOTA) == 1, f'❌ âncora Nota JanMar: {h.count(OLD_NOTA)}×'
h = h.replace(OLD_NOTA, NEW_NOTA)
print('✅ FIX 6c: seção ③ Unidades adicionada em sheetJanMar')

# ─────────────────────────────────────────────────────────────────────────────
# FIX 7: buildExcel card 2 — filename reflete modo ativo
# ─────────────────────────────────────────────────────────────────────────────
OLD_FNAME2 = "      fname      = 'Nielsen_Share_JanMar_'+mktSlug+'.xlsx';"

NEW_FNAME2 = "      fname      = 'Nielsen_'+(state.mode==='share'?'Share':(state.mode==='un'?'Unidades':'RMM'))+'_JanMar_'+mktSlug+'.xlsx';"

assert h.count(OLD_FNAME2) == 1, f'❌ âncora fname card 2: {h.count(OLD_FNAME2)}×'
h = h.replace(OLD_FNAME2, NEW_FNAME2)
print('✅ FIX 7: filename card 2 dinâmico por modo')

# ─────────────────────────────────────────────────────────────────────────────
# Verificações finais
# ─────────────────────────────────────────────────────────────────────────────
assert 'var chartBrandsBar2 = MSO_BRANDS;' in h,                '❌ chartBrandsBar2 não encontrado'
assert "d25['ALL OTHERS CAMP']={jan:null" in h,                  '❌ d25 AOC JanMar não encontrado'
assert "d26['ALL OTHERS CAMP']={jan:_aocJ26" in h,               '❌ d26 AOC JanMar não encontrado'
assert 'chartBrandsBar2.forEach(function(b)' in h,               '❌ forEach chartBrandsBar2 não encontrado'
assert 'return chartBrandsBar2[items[0].dataIndex]' in h,         '❌ tooltip title chartBrandsBar2 não encontrado'
assert 'var b=chartBrandsBar2[ctx.dataIndex]' in h,              '❌ tooltip label chartBrandsBar2 não encontrado'
assert "mso2Mode!=='share' ? MSO_BRANDS" in h,                   '❌ lines2 condicional não encontrado'
assert "selId === 'mso2MarketSel' && typeof mso2Mode" in h,      '❌ getState mso2Mode não encontrado'
assert "var _jmLbl=st.mode==='share'" in h,                      '❌ _jmLbl JanMar não encontrado'
assert "st.mode!=='share' && st.valD && st.valD['ALL OTHERS CAMP']" in h, '❌ AOC seção ② não encontrado'
assert '③ UNIDADES' in h,                                    '❌ seção ③ header não encontrado'
assert "state.mode==='un'?'Unidades':'RMM'" in h,                '❌ filename modo não encontrado'
# Verificar que brands (SCJ) não foi alterado
assert "MSO_BRANDS.filter(function(b){ return b!=='ALL OTHERS CAMP'; })" in h, '❌ brands filter removido!'
print('✅ Todas as verificações OK')

print(f'\nTamanho original: {orig_len:,} | Novo: {len(h):,} | Δ: {len(h)-orig_len:+,}')

VER.parent.mkdir(parents=True, exist_ok=True)
VER.write_text(h, encoding='utf-8')
print(f'✅ Versão salva: {VER.name}')
SRC.write_text(h, encoding='utf-8')
print(f'✅ Base ativa atualizada: {SRC.name}')
print('DONE.')
