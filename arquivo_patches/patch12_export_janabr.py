"""
patch12_export_janabr.py
Atualiza sheetJanMar (export Excel do card Jan·Fev·Mar) para incluir coluna Abril.
Estrutura: 12 cols -> 14 cols (adiciona Abr/25 e Abr/26)
"""
import os, shutil, datetime, sys
sys.stdout.reconfigure(encoding='utf-8')

BASE = r"C:\Users\valqu\OneDrive\Documentos\Claude\Projects\projeto Dashboard_farma_sul\Dashboard_farma_sul"
SRC  = os.path.join(BASE, "Dashboard_Farma_Sul_20260512_2220.html")

with open(SRC, 'r', encoding='utf-8') as f:
    html = f.read()

original_len = len(html)

# ── Localizar função exata ──────────────────────────────────────────────────
pos = html.find('function sheetJanMar')
end = html.find('\nfunction ', pos + 10)
OLD = html[pos:end]
print(f'sheetJanMar encontrada @ {pos}, len={len(OLD)}')

# ── Nova função com Abril ───────────────────────────────────────────────────
NEW = r"""function sheetJanMar(wb, st){
  var ws = wb.addWorksheet('📅 Jan\xb7Fev\xb7Mar\xb7Abr Comparativo');
  ws.views = [{state:'frozen',xSplit:1,ySplit:4,showGridLines:false}];

  /* Colunas: margem | marca | 4\xd725 | Acum25 | 4\xd726 | Acum26 | Δpp | margem */
  var widths=[2,22,10,10,10,10,13,10,10,10,10,13,10,2];
  widths.forEach(function(w,i){ ws.getColumn(i+1).width=w; });
  var lastC=14;

  /* T\xedtulo */
  ws.getRow(1).height=26;
  ws.mergeCells('B1:M1');
  var t=ws.getCell('B1');
  var _jmLbl=st.mode==='share'?'MARKET SHARE %':(st.mode==='un'?'UNIDADES':'R$ MILH\xd5ES');
  t.value='NIELSEN PERFORMANCE — JAN \xb7 FEV \xb7 MAR \xb7 ABR — '+_jmLbl+' — 2025 vs 2026 \xb7 '+st.market.toUpperCase();
  t.fill={type:'pattern',pattern:'solid',fgColor:{argb:'FFD9E1F2'}};
  t.font={name:'Calibri',size:13,bold:true,color:{argb:'FF1D4ED8'}};
  t.alignment={vertical:'middle',horizontal:'center'};

  ws.getRow(2).height=14;
  ws.mergeCells('B2:M2');
  var s2=ws.getCell('B2');
  s2.value='Acumulado Jan–Abr \xb7 '+_jmLbl+' por Marca \xb7 NielsenIQ Retail Measurement \xb7 Exportado '+new Date().toLocaleDateString('pt-BR');
  s2.fill={type:'pattern',pattern:'solid',fgColor:{argb:'FFFFFFFF'}};
  s2.font={name:'Calibri',size:9,italic:true,color:{argb:'FF94A3B8'}};
  s2.alignment={horizontal:'center'};

  /* Sub-header grupos */
  ws.getRow(3).height=14;
  for(var c=1;c<=lastC;c++) cell(ws,3,c,'',{bg:'D9E1F2'});
  ws.mergeCells('C3:G3');
  var g25=ws.getCell('C3'); g25.value='── 2025 ──';
  g25.fill={type:'pattern',pattern:'solid',fgColor:{argb:'FFD9E1F2'}};
  g25.font={name:'Calibri',size:9,bold:true,color:{argb:'FF64748B'}};
  g25.alignment={horizontal:'center'};
  ws.mergeCells('H3:L3');
  var g26=ws.getCell('H3'); g26.value='── 2026 ──';
  g26.fill={type:'pattern',pattern:'solid',fgColor:{argb:'FFD9E1F2'}};
  g26.font={name:'Calibri',size:9,bold:true,color:{argb:'FF1D4ED8'}};
  g26.alignment={horizontal:'center'};

  /* Header linha 4 */
  var hdrs=['','Marca','Jan/25','Fev/25','Mar/25','Abr/25','JanAbr25%','Jan/26','Fev/26','Mar/26','Abr/26','JanAbr26%','Δ pp',''];
  hdrs.forEach(function(v,i){ hdr(ws,4,i+1,v,'D9E1F2','1E293B'); });
  ws.getRow(4).height=20;

  /* ── Se\xe7\xe3o 1: Share % ── */
  var secR=5; ws.getRow(secR).height=18;
  ws.mergeCells(secR,2,secR,lastC-1);
  var sc1=ws.getCell(secR,2);
  sc1.value='① SHARE % — Jan\xb7Fev\xb7Mar\xb7Abr';
  sc1.fill={type:'pattern',pattern:'solid',fgColor:{argb:'FF1D4ED8'}};
  sc1.font={name:'Calibri',size:10,bold:true,color:{argb:'FFFFFFFF'}};
  sc1.alignment={vertical:'middle',horizontal:'left'};
  cell(ws,secR,1,'',{bg:'1D4ED8'}); cell(ws,secR,lastC,'',{bg:'1D4ED8'});

  var dataR=secR+1;
  st.brands.forEach(function(b){
    var rd=st.msoD[b]; if(!rd) return;
    var bc=BRAND_COL[b]||C.white;
    var j25=rd.jan25||0; var f25=rd.feb25||0; var m25=rd.mar25||0; var a25=rd.apr25||0;
    var monthly=rd.monthly||[];
    var j26=monthly[6]||0; var f26=monthly[7]||0; var m26=monthly[8]||0; var a26=monthly[9]||0;
    /* Share acumulado Jan-Abr: ponderado por valor de mercado */
    var janabr25_mkt = (st.totD?(st.totD.janmar25_val||0)+(st.totD.abr25_val||0):0);
    var janabr26_mkt = (st.totD?(st.totD.janmar26_val||0)+(st.totD.abr26_val||0):0);
    var janabr25_shr, janabr26_shr;
    if(janabr25_mkt>0 && st.valD && st.valD[b]){
      var vb=st.valD[b];
      janabr25_shr=((vb.jan25_val||0)+(vb.fev25_val||0)+(vb.mar25_val||0)+(vb.abr25_val||0))/janabr25_mkt*100;
    } else {
      janabr25_shr=(j25+f25+m25+a25)/4;
    }
    if(janabr26_mkt>0 && st.valD && st.valD[b]){
      var vb=st.valD[b];
      janabr26_shr=((vb.jan_val||0)+(vb.fev_val||0)+(vb.mar_val||0)+(vb.abr_val||0))/janabr26_mkt*100;
    } else {
      janabr26_shr=(j26+f26+m26+a26)/4;
    }
    var djanmar=janabr26_shr-janabr25_shr;
    ws.getRow(dataR).height=18;
    cell(ws,dataR,1,'',{bord:true});
    cell(ws,dataR,2,b,{fg:bc,bold:true,bord:true});
    cell(ws,dataR,3,j25.toFixed(2)+'%',{fg:C.gray,align:'center',bord:true});
    cell(ws,dataR,4,f25.toFixed(2)+'%',{fg:C.gray,align:'center',bord:true});
    cell(ws,dataR,5,m25.toFixed(2)+'%',{fg:C.gray,align:'center',bord:true});
    cell(ws,dataR,6,a25.toFixed(2)+'%',{fg:C.gray,align:'center',bord:true});
    cell(ws,dataR,7,janabr25_shr.toFixed(2)+'%',{fg:C.gray,bold:true,align:'center',bord:true,bg:'EEF2FF'});
    cell(ws,dataR,8,j26.toFixed(2)+'%',{fg:bc,align:'center',bord:true});
    cell(ws,dataR,9,f26.toFixed(2)+'%',{fg:bc,align:'center',bord:true});
    cell(ws,dataR,10,m26.toFixed(2)+'%',{fg:bc,align:'center',bord:true});
    cell(ws,dataR,11,a26.toFixed(2)+'%',{fg:bc,align:'center',bord:true});
    cell(ws,dataR,12,janabr26_shr.toFixed(2)+'%',{fg:bc,bold:true,align:'center',bord:true,bg:'EEF2FF'});
    cell(ws,dataR,13,fmtPp(djanmar),{fg:deltaColor(djanmar),bold:true,align:'center',bord:true});
    cell(ws,dataR,14,'',{bord:true});
    dataR++;
  });
  dataR++;

  /* ── Se\xe7\xe3o 2: Valor R$M ── */
  ws.getRow(dataR).height=18;
  ws.mergeCells(dataR,2,dataR,lastC-1);
  var sc2=ws.getCell(dataR,2);
  sc2.value='② VALOR R$M — Jan\xb7Fev\xb7Mar\xb7Abr';
  sc2.fill={type:'pattern',pattern:'solid',fgColor:{argb:'FF0E7490'}};
  sc2.font={name:'Calibri',size:10,bold:true,color:{argb:'FFFFFFFF'}};
  sc2.alignment={vertical:'middle',horizontal:'left'};
  cell(ws,dataR,1,'',{bg:'0E7490'}); cell(ws,dataR,lastC,'',{bg:'0E7490'});
  dataR++;

  var vhdrs=['','Marca','Jan/25','Fev/25','Mar/25','Abr/25','JanAbr25 R$M','Jan/26','Fev/26','Mar/26','Abr/26','JanAbr26 R$M','Δ Val%',''];
  vhdrs.forEach(function(v,i){ hdr(ws,dataR,i+1,v,'D9E1F2','1E293B'); });
  ws.getRow(dataR).height=18;
  dataR++;

  st.brands.forEach(function(b){
    var vd=st.valD?st.valD[b]:null; if(!vd) return;
    var bc=BRAND_COL[b]||C.white;
    var j25v=vd.jan25_val||0; var f25v=vd.fev25_val||0; var m25v=vd.mar25_val||0; var a25v=vd.abr25_val||0;
    var j26v=vd.jan_val||0;   var f26v=vd.fev_val||0;   var m26v=vd.mar_val||0;   var a26v=vd.abr_val||0;
    var tot25=j25v+f25v+m25v+a25v; var tot26=j26v+f26v+m26v+a26v;
    var dv=tot25>0?(tot26-tot25)/tot25*100:null;
    ws.getRow(dataR).height=18;
    cell(ws,dataR,1,'',{bord:true});
    cell(ws,dataR,2,b,{fg:bc,bold:true,bord:true});
    cell(ws,dataR,3,j25v.toFixed(3),{fg:C.gray,align:'right',bord:true});
    cell(ws,dataR,4,f25v.toFixed(3),{fg:C.gray,align:'right',bord:true});
    cell(ws,dataR,5,m25v.toFixed(3),{fg:C.gray,align:'right',bord:true});
    cell(ws,dataR,6,a25v.toFixed(3),{fg:C.gray,align:'right',bord:true});
    cell(ws,dataR,7,tot25.toFixed(3),{fg:C.gray,bold:true,align:'right',bord:true,bg:'EEF2FF'});
    cell(ws,dataR,8,j26v.toFixed(3),{fg:bc,align:'right',bord:true});
    cell(ws,dataR,9,f26v.toFixed(3),{fg:bc,align:'right',bord:true});
    cell(ws,dataR,10,m26v.toFixed(3),{fg:bc,align:'right',bord:true});
    cell(ws,dataR,11,a26v.toFixed(3),{fg:bc,align:'right',bord:true});
    cell(ws,dataR,12,tot26.toFixed(3),{fg:bc,bold:true,align:'right',bord:true,bg:'EEF2FF'});
    cell(ws,dataR,13,dv!=null?fmtPct(dv,1):'—',{fg:dv!=null?deltaColor(dv):C.gray,bold:true,align:'center',bord:true});
    cell(ws,dataR,14,'',{bord:true});
    dataR++;
  });

  /* ALL OTHERS CAMP — se\xe7\xe3o ② Valor R$M */
  if(st.mode!=='share' && st.valD && st.valD['ALL OTHERS CAMP']){
    var _aocV=st.valD['ALL OTHERS CAMP'];
    var _aocJ25v=_aocV.jan25_val||0,_aocF25v=_aocV.fev25_val||0,_aocM25v=_aocV.mar25_val||0,_aocA25v=_aocV.abr25_val||0;
    var _aocJ26v=_aocV.jan_val||0,  _aocF26v=_aocV.fev_val||0,  _aocM26v=_aocV.mar_val||0,  _aocA26v=_aocV.abr_val||0;
    var _aocTot25v=_aocJ25v+_aocF25v+_aocM25v+_aocA25v, _aocTot26v=_aocJ26v+_aocF26v+_aocM26v+_aocA26v;
    var _aocDv=_aocTot25v>0?(_aocTot26v-_aocTot25v)/_aocTot25v*100:null;
    ws.getRow(dataR).height=18;
    cell(ws,dataR,1,'',{bord:true});
    cell(ws,dataR,2,'ALL OTHERS CAMP',{fg:C.gray,bold:true,bord:true});
    cell(ws,dataR,3,_aocJ25v.toFixed(3),{fg:C.gray,align:'right',bord:true});
    cell(ws,dataR,4,_aocF25v.toFixed(3),{fg:C.gray,align:'right',bord:true});
    cell(ws,dataR,5,_aocM25v.toFixed(3),{fg:C.gray,align:'right',bord:true});
    cell(ws,dataR,6,_aocA25v.toFixed(3),{fg:C.gray,align:'right',bord:true});
    cell(ws,dataR,7,_aocTot25v.toFixed(3),{fg:C.gray,bold:true,align:'right',bord:true,bg:'EEF2FF'});
    cell(ws,dataR,8,_aocJ26v.toFixed(3),{fg:C.gray,align:'right',bord:true});
    cell(ws,dataR,9,_aocF26v.toFixed(3),{fg:C.gray,align:'right',bord:true});
    cell(ws,dataR,10,_aocM26v.toFixed(3),{fg:C.gray,align:'right',bord:true});
    cell(ws,dataR,11,_aocA26v.toFixed(3),{fg:C.gray,align:'right',bord:true});
    cell(ws,dataR,12,_aocTot26v.toFixed(3),{fg:C.gray,bold:true,align:'right',bord:true,bg:'EEF2FF'});
    cell(ws,dataR,13,_aocDv!=null?fmtPct(_aocDv,1):'—',{fg:_aocDv!=null?deltaColor(_aocDv):C.gray,bold:true,align:'center',bord:true});
    cell(ws,dataR,14,'',{bord:true});
    dataR++;
  }
  /* Total mercado — Valor */
  if(st.totD){
    var _tot25j=st.totD.jan25_val||0,_tot25f=st.totD.fev25_val||0,_tot25m=st.totD.mar25_val||0,_tot25a=st.totD.abr25_val||0;
    var _tot26j=st.totD.jan26_val||0,_tot26f=st.totD.fev26_val||0,_tot26m=st.totD.mar26_val||0,_tot26a=st.totD.abr26_val||0;
    var tot25m=_tot25j+_tot25f+_tot25m+_tot25a; var tot26m=_tot26j+_tot26f+_tot26m+_tot26a;
    var dtot=tot25m>0?(tot26m-tot25m)/tot25m*100:null;
    ws.getRow(dataR).height=18;
    cell(ws,dataR,1,'',{bg:'EEF2FF',bord:true});
    cell(ws,dataR,2,'= TOTAL MERCADO',{bg:'EEF2FF',fg:C.teal,bold:true,bord:true});
    cell(ws,dataR,3,_tot25j.toFixed(3),{bg:'EEF2FF',fg:C.gray,align:'right',bord:true});
    cell(ws,dataR,4,_tot25f.toFixed(3),{bg:'EEF2FF',fg:C.gray,align:'right',bord:true});
    cell(ws,dataR,5,_tot25m.toFixed(3),{bg:'EEF2FF',fg:C.gray,align:'right',bord:true});
    cell(ws,dataR,6,_tot25a.toFixed(3),{bg:'EEF2FF',fg:C.gray,align:'right',bord:true});
    cell(ws,dataR,7,tot25m.toFixed(3),{bg:'EEF2FF',fg:C.gray,bold:true,align:'right',bord:true});
    cell(ws,dataR,8,_tot26j.toFixed(3),{bg:'EEF2FF',fg:C.teal,align:'right',bord:true});
    cell(ws,dataR,9,_tot26f.toFixed(3),{bg:'EEF2FF',fg:C.teal,align:'right',bord:true});
    cell(ws,dataR,10,_tot26m.toFixed(3),{bg:'EEF2FF',fg:C.teal,align:'right',bord:true});
    cell(ws,dataR,11,_tot26a.toFixed(3),{bg:'EEF2FF',fg:C.teal,align:'right',bord:true});
    cell(ws,dataR,12,tot26m.toFixed(3),{bg:'EEF2FF',fg:C.teal,bold:true,align:'right',bord:true});
    cell(ws,dataR,13,dtot!=null?fmtPct(dtot,1):'—',{bg:'EEF2FF',fg:dtot!=null?deltaColor(dtot):C.gray,bold:true,align:'center',bord:true});
    cell(ws,dataR,14,'',{bg:'EEF2FF',bord:true});
    dataR++;
  }
  dataR++;

  /* ── Se\xe7\xe3o 3: Unidades ── */
  ws.getRow(dataR).height=18;
  ws.mergeCells(dataR,2,dataR,lastC-1);
  var sc3=ws.getCell(dataR,2);
  sc3.value='③ UNIDADES — Jan\xb7Fev\xb7Mar\xb7Abr';
  sc3.fill={type:'pattern',pattern:'solid',fgColor:{argb:'FF166534'}};
  sc3.font={name:'Calibri',size:10,bold:true,color:{argb:'FFFFFFFF'}};
  sc3.alignment={vertical:'middle',horizontal:'left'};
  cell(ws,dataR,1,'',{bg:'166534'}); cell(ws,dataR,lastC,'',{bg:'166534'});
  dataR++;
  var uhdrs=['','Marca','Jan/25','Fev/25','Mar/25','Abr/25','JanAbr25 K Un','Jan/26','Fev/26','Mar/26','Abr/26*','JanAbr26 K Un','Δ Un%',''];
  uhdrs.forEach(function(v,i){ hdr(ws,dataR,i+1,v,'D9E1F2','1E293B'); });
  ws.getRow(dataR).height=18;
  dataR++;
  st.brands.forEach(function(b){
    var ud=st.valD?st.valD[b]:null; if(!ud) return;
    var bc=BRAND_COL[b]||C.white;
    var j25u=ud.jan25_un||0; var f25u=ud.fev25_un||0; var m25u=ud.mar25_un||0; var a25u=ud.abr25_un||0;
    var j26u=ud.jan_un||0;   var f26u=ud.fev_un||0;   var m26u=ud.mar_un||0;   var a26u=ud.monthly_un?ud.monthly_un[9]||0:0;
    var tot25u=j25u+f25u+m25u+a25u; var tot26u=j26u+f26u+m26u+a26u;
    var du=tot25u>0?(tot26u-tot25u)/tot25u*100:null;
    ws.getRow(dataR).height=18;
    cell(ws,dataR,1,'',{bord:true});
    cell(ws,dataR,2,b,{fg:bc,bold:true,bord:true});
    cell(ws,dataR,3,Math.round(j25u).toString(),{fg:C.gray,align:'right',bord:true});
    cell(ws,dataR,4,Math.round(f25u).toString(),{fg:C.gray,align:'right',bord:true});
    cell(ws,dataR,5,Math.round(m25u).toString(),{fg:C.gray,align:'right',bord:true});
    cell(ws,dataR,6,Math.round(a25u).toString(),{fg:C.gray,align:'right',bord:true});
    cell(ws,dataR,7,Math.round(tot25u).toString(),{fg:C.gray,bold:true,align:'right',bord:true,bg:'EEF2FF'});
    cell(ws,dataR,8,Math.round(j26u).toString(),{fg:bc,align:'right',bord:true});
    cell(ws,dataR,9,Math.round(f26u).toString(),{fg:bc,align:'right',bord:true});
    cell(ws,dataR,10,Math.round(m26u).toString(),{fg:bc,align:'right',bord:true});
    cell(ws,dataR,11,a26u>0?Math.round(a26u).toString():'—',{fg:bc,align:'right',bord:true});
    cell(ws,dataR,12,Math.round(tot26u).toString(),{fg:bc,bold:true,align:'right',bord:true,bg:'EEF2FF'});
    cell(ws,dataR,13,du!=null?fmtPct(du,1):'—',{fg:du!=null?deltaColor(du):C.gray,bold:true,align:'center',bord:true});
    cell(ws,dataR,14,'',{bord:true});
    dataR++;
  });
  /* ALL OTHERS CAMP — se\xe7\xe3o ③ Unidades */
  if(st.mode!=='share' && st.valD && st.valD['ALL OTHERS CAMP']){
    var _aocU=st.valD['ALL OTHERS CAMP'];
    var _aocJ25u=_aocU.jan25_un||0,_aocF25u=_aocU.fev25_un||0,_aocM25u=_aocU.mar25_un||0,_aocA25u=_aocU.abr25_un||0;
    var _aocJ26u=_aocU.jan_un||0,  _aocF26u=_aocU.fev_un||0,  _aocM26u=_aocU.mar_un||0;
    var _aocA26u=_aocU.monthly_un?_aocU.monthly_un[9]||0:0;
    var _aocTot25u=_aocJ25u+_aocF25u+_aocM25u+_aocA25u, _aocTot26u=_aocJ26u+_aocF26u+_aocM26u+_aocA26u;
    var _aocDu=_aocTot25u>0?(_aocTot26u-_aocTot25u)/_aocTot25u*100:null;
    ws.getRow(dataR).height=18;
    cell(ws,dataR,1,'',{bord:true});
    cell(ws,dataR,2,'ALL OTHERS CAMP',{fg:C.gray,bold:true,bord:true});
    cell(ws,dataR,3,Math.round(_aocJ25u).toString(),{fg:C.gray,align:'right',bord:true});
    cell(ws,dataR,4,Math.round(_aocF25u).toString(),{fg:C.gray,align:'right',bord:true});
    cell(ws,dataR,5,Math.round(_aocM25u).toString(),{fg:C.gray,align:'right',bord:true});
    cell(ws,dataR,6,Math.round(_aocA25u).toString(),{fg:C.gray,align:'right',bord:true});
    cell(ws,dataR,7,Math.round(_aocTot25u).toString(),{fg:C.gray,bold:true,align:'right',bord:true,bg:'EEF2FF'});
    cell(ws,dataR,8,Math.round(_aocJ26u).toString(),{fg:C.gray,align:'right',bord:true});
    cell(ws,dataR,9,Math.round(_aocF26u).toString(),{fg:C.gray,align:'right',bord:true});
    cell(ws,dataR,10,Math.round(_aocM26u).toString(),{fg:C.gray,align:'right',bord:true});
    cell(ws,dataR,11,_aocA26u>0?Math.round(_aocA26u).toString():'—',{fg:C.gray,align:'right',bord:true});
    cell(ws,dataR,12,Math.round(_aocTot26u).toString(),{fg:C.gray,bold:true,align:'right',bord:true,bg:'EEF2FF'});
    cell(ws,dataR,13,_aocDu!=null?fmtPct(_aocDu,1):'—',{fg:_aocDu!=null?deltaColor(_aocDu):C.gray,bold:true,align:'center',bord:true});
    cell(ws,dataR,14,'',{bord:true});
    dataR++;
  }
  /* Total mercado — Unidades */
  if(st.totD){
    var _tu25j=st.totD.jan25_un||0,_tu25f=st.totD.fev25_un||0,_tu25m=st.totD.mar25_un||0;
    var _tu26j=st.totD.jan26_un||0,_tu26f=st.totD.fev26_un||0,_tu26m=st.totD.mar26_un||0;
    var tot25mu=_tu25j+_tu25f+_tu25m; var tot26mu=_tu26j+_tu26f+_tu26m;
    var dtotu=tot25mu>0?(tot26mu-tot25mu)/tot25mu*100:null;
    ws.getRow(dataR).height=18;
    cell(ws,dataR,1,'',{bg:'EEF2FF',bord:true});
    cell(ws,dataR,2,'= TOTAL MERCADO',{bg:'EEF2FF',fg:C.green,bold:true,bord:true});
    cell(ws,dataR,3,Math.round(_tu25j).toString(),{bg:'EEF2FF',fg:C.gray,align:'right',bord:true});
    cell(ws,dataR,4,Math.round(_tu25f).toString(),{bg:'EEF2FF',fg:C.gray,align:'right',bord:true});
    cell(ws,dataR,5,Math.round(_tu25m).toString(),{bg:'EEF2FF',fg:C.gray,align:'right',bord:true});
    cell(ws,dataR,6,'—',{bg:'EEF2FF',fg:C.gray,align:'right',bord:true});
    cell(ws,dataR,7,Math.round(tot25mu).toString(),{bg:'EEF2FF',fg:C.gray,bold:true,align:'right',bord:true});
    cell(ws,dataR,8,Math.round(_tu26j).toString(),{bg:'EEF2FF',fg:C.green,align:'right',bord:true});
    cell(ws,dataR,9,Math.round(_tu26f).toString(),{bg:'EEF2FF',fg:C.green,align:'right',bord:true});
    cell(ws,dataR,10,Math.round(_tu26m).toString(),{bg:'EEF2FF',fg:C.green,align:'right',bord:true});
    cell(ws,dataR,11,'—',{bg:'EEF2FF',fg:C.green,align:'right',bord:true});
    cell(ws,dataR,12,Math.round(tot26mu).toString(),{bg:'EEF2FF',fg:C.green,bold:true,align:'right',bord:true});
    cell(ws,dataR,13,dtotu!=null?fmtPct(dtotu,1):'—',{bg:'EEF2FF',fg:dtotu!=null?deltaColor(dtotu):C.gray,bold:true,align:'center',bord:true});
    cell(ws,dataR,14,'',{bg:'EEF2FF',bord:true});
    dataR++;
  }
  dataR++;

  /* Nota */
  ws.mergeCells(dataR,2,dataR,lastC-1);
  var fn=ws.getCell(dataR,2);
  fn.value='Fonte: NielsenIQ Retail Measurement \xb7 Acum Jan\xb7Fev\xb7Mar\xb7Abr \xb7 Share% = ΣValMarca(JanAbr) \xf7 ΣMercado(JanAbr) \xd7 100 \xb7 *Abr/26 Unidades: n\xe3o dispon\xedvel por SKU \xb7 Exportado '+new Date().toLocaleString('pt-BR');
  fn.fill={type:'pattern',pattern:'solid',fgColor:{argb:'FFFFFFFF'}};
  fn.font={name:'Calibri',size:8,italic:true,color:{argb:'FF94A3B8'}};
  fn.alignment={horizontal:'center'};

  fillBg(ws,dataR+3,lastC+1);
}
"""

# ── Aplicar substituição ────────────────────────────────────────────────────
if OLD not in html:
    print('ERRO: OLD function nao encontrada!')
else:
    html2 = html.replace(OLD, NEW, 1)
    diff = len(html2) - len(html)
    print(f'Substituicao OK. Diff: {diff:+,} bytes')

    with open(SRC, 'w', encoding='utf-8') as f:
        f.write(html2)
    print(f'Salvo: {SRC}')

    ts = datetime.datetime.now().strftime('%Y%m%d_%H%M')
    VER = os.path.join(BASE, 'versoes', f'Dashboard_Farma_Sul_{ts}_ExportJanAbr.html')
    shutil.copy2(SRC, VER)
    print(f'Versao: {VER}')
