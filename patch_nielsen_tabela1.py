"""
patch_nielsen_tabela1.py
Dois fixes no Exportar Nielsen Excel:

1. "Filtrado" — getState lê window.mso3Mode (val/un) do card 3;
   triggerExport passa modo; filename/título refletem modo ativo.

2. Nova aba "1-Tabela-1" — formato idêntico ao Base Giovano 26-04,
   com TODOS os mercados de NIELSEN_BRAND_VAL, todas as marcas, 11 períodos
   (FYTD25, FYTD26 + 9 meses Jul/25–Mar/26).
   Colunas: Markets | CATEGORY | BRAND | Products | Data |
            $ | Wghtd Dist Reach | Avg (UNID) Price | $ Shr - Product |
            TDP Wghtd Dist Reach Shr | (UNID) | ROS $ (C)
"""
import sys
from pathlib import Path
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

BASE = Path(r'C:\Users\valqu\OneDrive\Documentos\Claude\Projects\projeto Dashboard_farma_sul\Dashboard_farma_sul')
SRC  = BASE / 'Dashboard_Farma_Sul_20260512_2220.html'
VER  = BASE / 'versoes' / f'Dashboard_Farma_Sul_{datetime.now().strftime("%Y%m%d_%H%M")}_Tabela1.html'

print('Lendo dashboard…')
h = SRC.read_text(encoding='utf-8')
orig_len = len(h)

# ─────────────────────────────────────────────────────────────────────────────
# 1. getState — adicionar leitura de mso3Mode
# ─────────────────────────────────────────────────────────────────────────────
OLD_GETSTATE = """/* ── 4. Capturar estado atual ── */
function getState(selId){
  var sel = document.getElementById(selId || 'msoMarketSel');
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
}"""

NEW_GETSTATE = """/* ── 4. Capturar estado atual ── */
function getState(selId){
  var sel = document.getElementById(selId || 'msoMarketSel');
  var market = sel ? sel.value : 'T.BR Farma';
  /* Ler modo R$/Un do card 3 */
  var mode = 'val';
  if(selId === 'mso3MarketSel' && typeof mso3Mode !== 'undefined') mode = mso3Mode;
  var msoD = (typeof MKTSHARE_OVERVIEW!=='undefined') ? MKTSHARE_OVERVIEW[market] : null;
  var valD = (typeof NIELSEN_BRAND_VAL!=='undefined')  ? NIELSEN_BRAND_VAL[market]  : null;
  var totD = (typeof FYTD_MARKET_TOTAL!=='undefined')  ? FYTD_MARKET_TOTAL[market]  : null;
  /* Base completa (todos os mercados) para 1-Tabela-1 */
  var allNBV = (typeof NIELSEN_BRAND_VAL!=='undefined') ? NIELSEN_BRAND_VAL : null;
  var allMSO = (typeof MKTSHARE_OVERVIEW!=='undefined') ? MKTSHARE_OVERVIEW : null;
  var brands = (typeof MSO_BRANDS!=='undefined')
    ? MSO_BRANDS.filter(function(b){ return b!=='ALL OTHERS CAMP'; })
    : ['OFF!','EXPOSIS','XO INSETO','SUPER REPELEX','SBP'];
  var allBrands = (typeof MSO_BRANDS!=='undefined') ? MSO_BRANDS : brands;
  var months = (typeof MSO_MONTHS!=='undefined') ? MSO_MONTHS
    : ['Jul/25','Ago/25','Set/25','Out/25','Nov/25','Dez/25','Jan/26','Fev/26','Mar/26'];
  if(!msoD){ showToast('❌ Nenhum dado disponível para exportação.', 'error'); return null; }
  return { market:market, mode:mode, msoD:msoD, valD:valD, totD:totD,
           brands:brands, allBrands:allBrands, months:months,
           allNBV:allNBV, allMSO:allMSO };
}"""

c1 = h.count(OLD_GETSTATE)
assert c1 == 1, f'getState: {c1} ocorrências'
h = h.replace(OLD_GETSTATE, NEW_GETSTATE)
print('✅ getState atualizado com mso3Mode e allNBV/allMSO')

# ─────────────────────────────────────────────────────────────────────────────
# 2. buildExcel — título respeita modo + adiciona sheetTabela1
# ─────────────────────────────────────────────────────────────────────────────
OLD_BUILD = """    wb.creator='Dashboard Farma Sul — Giovano Anjos';
    wb.created=new Date(); wb.modified=new Date();

    sheetCapa(wb,state);
    sheetBase(wb,state);
    sheetEvolucao(wb,state);
    sheetFYTD(wb,state);
    sheetMemCalculo(wb,state);

    wb.xlsx.writeBuffer().then(function(buf){
      var blob=new Blob([buf],{type:'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'});
      var a=document.createElement('a');
      a.href=URL.createObjectURL(blob);
      a.download='Nielsen_FarmaSul_FY26_Export.xlsx';"""

NEW_BUILD = """    wb.creator='Dashboard Farma Sul — Giovano Anjos';
    wb.created=new Date(); wb.modified=new Date();

    sheetCapa(wb,state);
    sheetBase(wb,state);
    sheetEvolucao(wb,state);
    sheetFYTD(wb,state);
    sheetMemCalculo(wb,state);
    sheetTabela1(wb,state);

    var modeSuffix = (state.mode==='un') ? '_Unidades' : '_Valor';
    var mktSlug = state.market.replace(/[^a-zA-Z0-9]/g,'_').replace(/_+/g,'_');
    var fname = 'Nielsen_FarmaSul_FY26_'+mktSlug+modeSuffix+'.xlsx';

    wb.xlsx.writeBuffer().then(function(buf){
      var blob=new Blob([buf],{type:'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'});
      var a=document.createElement('a');
      a.href=URL.createObjectURL(blob);
      a.download=fname;"""

c2 = h.count(OLD_BUILD)
assert c2 == 1, f'buildExcel call: {c2} ocorrências'
h = h.replace(OLD_BUILD, NEW_BUILD)
print('✅ buildExcel atualizado: sheetTabela1 + filename com mercado e modo')

# ─────────────────────────────────────────────────────────────────────────────
# 3. sheetTabela1 — inserir ANTES do bloco buildExcel
# ─────────────────────────────────────────────────────────────────────────────
ANCHOR = "/* ── 12. Orquestrar a geração ── */"
assert h.count(ANCHOR) == 1, 'Âncora buildExcel não encontrada'

NEW_TABELA1 = r"""/* ── 11b. SHEET 6 — 1-TABELA-1 (Base Completa Nielsen) ── */
function sheetTabela1(wb, st){
  var ws = wb.addWorksheet('1-Tabela-1');

  /* Meses → datas de medição Nielsen (mesmo formato do arquivo original) */
  var MONTH_DATES = [
    '2025-07-23','2025-08-23','2025-09-22','2025-10-23','2025-11-22','2025-12-23',
    '2026-01-23','2026-02-20','2026-03-23'
  ];
  var CAT = 'PERSONAL REPELLENT';

  /* Larguras de colunas */
  var COL_W = [22,22,14,12,20,16,16,16,16,22,16,14];
  COL_W.forEach(function(w,i){ ws.getColumn(i+1).width = w; });

  /* ── Metadados do arquivo original (linhas 1-8) ── */
  var META_FONT = {name:'Calibri',size:9,color:{argb:'FF666666'}};
  var META_FILL = {type:'pattern',pattern:'solid',fgColor:{argb:'FFFFFFFF'}};
  function metaCell(r,txt){
    var c=ws.getCell(r,1); c.value=txt; c.font=META_FONT; c.fill=META_FILL;
  }
  metaCell(4,'Tabela-1');
  metaCell(5,'Voltar ao relatório');
  metaCell(6,'Dataset: NielsenIQ Retail Measurement | PS - GBL - SC JOHNSON - BR - PEST CONTROL  | PS - GBL - SC JOHNSON - BR - PEST CONTROL  | Currency: Brazilian real');
  metaCell(7,'7 Facts de 30 Products em...');
  metaCell(8,'Exportado via Dashboard Farma Sul · '+new Date().toLocaleDateString('pt-BR')+' · Mercado filtrado: '+st.market+' · Modo: '+(st.mode==='un'?'Unidades':'Valor R$M'));
  for(var r2=1;r2<=8;r2++){
    for(var c2=1;c2<=12;c2++){
      var mc=ws.getCell(r2,c2);
      if(!mc.fill||!mc.fill.fgColor) mc.fill=META_FILL;
    }
  }

  /* ── Linha de header (linha 9 — igual ao arquivo original) ── */
  var HDRS=['Markets','CATEGORY','BRAND','Products','Data','$',
            'Wghtd Dist Reach','Avg (UNID) Price','$ Shr - Product',
            'TDP Wghtd Dist Reach Shr ','(UNID)','ROS $ (C)'];
  var HDR_FILL = {type:'pattern',pattern:'solid',fgColor:{argb:'FFD9E1F2'}};
  var HDR_FONT = {name:'Calibri',size:10,bold:true,color:{argb:'FF1F3864'}};
  HDRS.forEach(function(h2,i){
    var hc=ws.getCell(9,i+1);
    hc.value=h2; hc.font=HDR_FONT; hc.fill=HDR_FILL;
    hc.alignment={horizontal:'center',vertical:'middle',wrapText:false};
    hc.border={bottom:{style:'medium',color:{argb:'FF1F3864'}}};
  });
  ws.getRow(9).height=20;
  ws.views=[{state:'frozen',xSplit:0,ySplit:9,showGridLines:true}];

  /* ── Dados: todos os mercados × marcas × períodos ── */
  var dataRow = 10;
  var allNBV  = st.allNBV || {};
  var allMSO  = st.allMSO || {};
  var allBrands = st.allBrands || st.brands;

  /* Ordenar mercados alfabeticamente */
  var markets = Object.keys(allNBV).sort();

  /* Estilos alternados por mercado */
  var ROW_FILL_A = {type:'pattern',pattern:'solid',fgColor:{argb:'FFFFFFFF'}};
  var ROW_FILL_B = {type:'pattern',pattern:'solid',fgColor:{argb:'FFF2F2F2'}};
  var BASE_FONT  = {name:'Calibri',size:9,color:{argb:'FF000000'}};
  var NUM_FONT   = {name:'Calibri',size:9,color:{argb:'FF1F3864'}};
  var FYTD_FONT  = {name:'Calibri',size:9,bold:true,color:{argb:'FF1F3864'}};

  markets.forEach(function(mkt, mktIdx){
    var nbvMkt = allNBV[mkt]; if(!nbvMkt) return;
    var msoMkt = allMSO[mkt] || {};
    var rowFill = (mktIdx%2===0) ? ROW_FILL_A : ROW_FILL_B;

    allBrands.forEach(function(brand){
      var vd = nbvMkt[brand]; if(!vd) return;
      var rd = msoMkt[brand] || {};
      var monthly_val = vd.monthly_val || [];
      var monthly_un  = vd.monthly_un  || [];
      var monthly_shr = rd.monthly     || [];

      /* Períodos: FYTD25, FYTD26, depois 9 meses */
      var periods = [
        {label:'FYTD25', val:(vd.fytd25_val||0)*1000000, un:(vd.fytd25_un||0)*1000, shr:(rd.fytd25||null), isFytd:true},
        {label:'FYTD26', val:(vd.fytd26_val||0)*1000000, un:(vd.fytd26_un||0)*1000, shr:(rd.fytd26||null), isFytd:true}
      ];
      for(var mi=0;mi<9;mi++){
        var mv = monthly_val[mi]; var mu = monthly_un[mi]; var ms = monthly_shr[mi];
        periods.push({
          label: MONTH_DATES[mi],
          val:   mv!=null ? mv*1000000 : null,
          un:    mu!=null ? mu*1000    : null,
          shr:   ms!=null ? ms         : null,
          isFytd:false
        });
      }

      periods.forEach(function(p){
        var avgPrice = (p.un && p.un>0 && p.val!=null) ? p.val/p.un : null;
        var fnt = p.isFytd ? FYTD_FONT : BASE_FONT;
        var row = ws.getRow(dataRow);
        /* Setar valores diretamente (mais rápido que getCell por getCell) */
        row.values = [
          mkt,
          CAT,
          brand,
          null,
          p.label,
          p.val    != null ? +p.val.toFixed(4)    : null,
          null, /* Wghtd Dist Reach — não disponível */
          avgPrice != null ? +avgPrice.toFixed(6)  : null,
          p.shr    != null ? +p.shr.toFixed(4)     : null,
          null, /* TDP — não disponível */
          p.un     != null ? +p.un.toFixed(4)      : null,
          null  /* ROS — não disponível */
        ];
        /* Aplicar formatação mínima nas colunas importantes */
        row.getCell(1).font = fnt;
        row.getCell(3).font = fnt;
        row.getCell(5).font = BASE_FONT;
        row.getCell(6).font = NUM_FONT;
        row.getCell(9).font = NUM_FONT;
        row.getCell(11).font = NUM_FONT;
        row.eachCell(function(c3){ c3.fill = rowFill; });
        dataRow++;
      });
    });
  });

  /* AutoFilter e nota de rodapé */
  ws.autoFilter = {from:{row:9,column:1}, to:{row:dataRow-1,column:12}};
  var footRow = dataRow+1;
  var fc = ws.getCell(footRow,1);
  fc.value = 'Fonte: NielsenIQ Retail Measurement · PS · GBL · SC JOHNSON · BR · PEST CONTROL'
           + ' · Gerado via Dashboard Farma Sul · '+new Date().toLocaleString('pt-BR');
  fc.font = {name:'Calibri',size:8,italic:true,color:{argb:'FF888888'}};
}

"""

h = h[:h.find(ANCHOR)] + NEW_TABELA1 + h[h.find(ANCHOR):]
print('✅ sheetTabela1 inserida')

# ─────────────────────────────────────────────────────────────────────────────
# Verificações
# ─────────────────────────────────────────────────────────────────────────────
assert 'sheetTabela1' in h,              '❌ sheetTabela1 não encontrada'
assert '1-Tabela-1' in h,               '❌ nome da aba não encontrado'
assert 'allNBV' in h,                   '❌ allNBV não encontrado'
assert 'mso3Mode' in h,                 '❌ mso3Mode não encontrado'
assert 'modeSuffix' in h,               '❌ modeSuffix não encontrado'
assert 'MONTH_DATES' in h,              '❌ MONTH_DATES não encontrado'
assert 'Wghtd Dist Reach' in h,         '❌ header Wghtd não encontrado'
assert h.count('sheetTabela1(wb,state)') == 1, '❌ chamada sheetTabela1 duplicada'
print('✅ Verificações OK')

print(f'\nTamanho original: {orig_len:,} | Novo: {len(h):,} | Δ: {len(h)-orig_len:+,}')

VER.parent.mkdir(parents=True, exist_ok=True)
VER.write_text(h, encoding='utf-8')
print(f'✅ Versão salva: {VER.name}')
SRC.write_text(h, encoding='utf-8')
print(f'✅ Base ativa atualizada: {SRC.name}')
print('DONE.')
