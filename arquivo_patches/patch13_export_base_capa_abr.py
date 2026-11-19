"""
patch13_export_base_capa_abr.py
Corrige 2 sheets do export Excel para incluir Abril:

1. sheetCapa  — subtitle "Jul/2025–Mar/2026" → "Jul/2025–Abr/2026"
2. sheetBase  — mesmo subtitle + coluna Abr/26 adicionada (14→15 cols)
               + mergeCells B1:N1→B1:O1 e B2:N2→B2:O2
"""
import os, shutil, datetime, sys
sys.stdout.reconfigure(encoding='utf-8')

BASE = r"C:\Users\valqu\OneDrive\Documentos\Claude\Projects\projeto Dashboard_farma_sul\Dashboard_farma_sul"
SRC  = os.path.join(BASE, "Dashboard_Farma_Sul_20260512_2220.html")

with open(SRC, 'r', encoding='utf-8') as f:
    html = f.read()

original_len = len(html)
patches = 0

def patch(old, new, desc):
    global html, patches
    c = html.count(old)
    if c == 0:
        print(f"  [X] NAO ENCONTRADO: {desc}")
        return False
    if c > 1:
        print(f"  [!] {c}x (substituindo 1): {desc}")
    html = html.replace(old, new, 1)
    patches += 1
    print(f"  [OK] {desc}")
    return True

print("=== PATCH 13: sheetCapa + sheetBase Abr/26 ===\n")

# ─────────────────────────────────────────────────────────────────
# 1. sheetCapa — subtitle periodo
# ─────────────────────────────────────────────────────────────────
print("--- sheetCapa: subtitle ---")
patch(
    "'FY26 \\u00b7 Jul/2025\\u2013Mar/2026 \\u00b7 Market: '+st.market+' \\u00b7 SC Johnson | NielsenIQ Retail Measurement'",
    "'FY26 \\u00b7 Jul/2025\\u2013Abr/2026 \\u00b7 Market: '+st.market+' \\u00b7 SC Johnson | NielsenIQ Retail Measurement'",
    "sheetCapa subtitle Jul/2025-Mar/2026 -> Abr/2026"
)

# Fallback: texto literal sem unicode escapes
if patches == 0:
    patch(
        "FY26 · Jul/2025–Mar/2026 · Market: ",
        "FY26 · Jul/2025–Abr/2026 · Market: ",
        "sheetCapa subtitle (literal unicode)"
    )

# ─────────────────────────────────────────────────────────────────
# 2. sheetBase — função completa reescrita com coluna Abr/26
# ─────────────────────────────────────────────────────────────────
print("\n--- sheetBase: reescrever com coluna Abr/26 ---")

OLD_BASE = (
    "function sheetBase(wb, st){\n"
    "  var ws=wb.addWorksheet('\U0001f4ca Base Analítica');\n"
    "  ws.views=[{state:'frozen',xSplit:1,ySplit:3,showGridLines:false}];\n"
    "  var widths=[2,22,13,13,10,14,14,11,14,14,11,12,12,12];\n"
    "  widths.forEach(function(w,i){ ws.getColumn(i+1).width=w; });\n"
    "\n"
    "  /* Título */\n"
    "  ws.mergeCells('B1:N1');\n"
    "  var t=ws.getCell('B1');\n"
    "  var _bmLbl=st.mode==='un'?' · UNIDADES':st.mode==='val'?' · VALOR R$M':'';\n"
    "  t.value='BASE ANALÍTICA NIELSEN'+_bmLbl+' — '+st.market.toUpperCase()+' — FY26 vs FY25';\n"
    "  t.fill={type:'pattern',pattern:'solid',fgColor:{argb:'FFFFFFFF'}};\n"
    "  t.font={name:'Calibri',size:14,bold:true,color:{argb:'FFB45309'}};\n"
    "  t.alignment={vertical:'middle',horizontal:'center'};\n"
    "  ws.getRow(1).height=28;\n"
    "\n"
    "  ws.mergeCells('B2:N2');\n"
    "  var s2=ws.getCell('B2');\n"
    "  s2.value='Jul/2025–Mar/2026 · Market: '+st.market+' · Exportado: '+new Date().toLocaleDateString('pt-BR');\n"
    "  s2.fill={type:'pattern',pattern:'solid',fgColor:{argb:'FFFFFFFF'}};\n"
    "  s2.font={name:'Calibri',size:10,color:{argb:'FF94A3B8'}};\n"
    "  s2.alignment={vertical:'middle',horizontal:'center'};\n"
    "  ws.getRow(2).height=18;\n"
    "\n"
    "  /* Headers */\n"
    "  var _isUnMode=(st.mode==='un');\n"
    "  var hdrs=['','Marca','Share FY25%','Share FY26%','Δ pp','Val FY25 R$M','Val FY26 R$M','Δ Val%',\n"
    "            'Vol FY25 Kun','Vol FY26 Kun','Δ Vol%',\n"
    "            _isUnMode?'Jan/26 Kun':'Jan/26 R$M',\n"
    "            _isUnMode?'Fev/26 Kun':'Fev/26 R$M',\n"
    "            _isUnMode?'Mar/26 Kun':'Mar/26 R$M'];\n"
    "  hdrs.forEach(function(v,i){ hdr(ws,3,i+1,v,C.hdr,C.gold); });\n"
    "  ws.getRow(3).height=22;\n"
    "\n"
    "  st.brands.forEach(function(b,i){\n"
    "    var rd=st.msoD[b]; var vd=st.valD?st.valD[b]:null; if(!rd) return;\n"
    "    var r=4+i; ws.getRow(r).height=18;\n"
    "    var d=rd.delta||0; var bc=BRAND_COL[b]||C.white; var dc=deltaColor(d);\n"
    "    var dv=vd&&vd.fytd25_val>0?(vd.fytd26_val-vd.fytd25_val)/vd.fytd25_val*100:null;\n"
    "    var du=vd&&vd.fytd25_un >0?(vd.fytd26_un -vd.fytd25_un )/vd.fytd25_un *100:null;\n"
    "    cell(ws,r,1,'',{bord:true});\n"
    "    cell(ws,r,2,b,{fg:bc,bold:true,bord:true});\n"
    "    cell(ws,r,3,(rd.fytd25||0).toFixed(2)+'%',{fg:C.gray,align:'center',bord:true});\n"
    "    cell(ws,r,4,(rd.fytd26||0).toFixed(2)+'%',{fg:bc,bold:true,align:'center',bord:true});\n"
    "    cell(ws,r,5,fmtPp(d),{fg:dc,bold:true,align:'center',bord:true});\n"
    "    cell(ws,r,6,vd?(vd.fytd25_val||0).toFixed(3):'--',{fg:C.gray,align:'right',bord:true});\n"
    "    cell(ws,r,7,vd?(vd.fytd26_val||0).toFixed(3):'--',{fg:bc,align:'right',bord:true});\n"
    "    cell(ws,r,8,dv!=null?fmtPct(dv,1):'--',{fg:dv!=null?(dv>=0?C.green:C.red):C.gray,align:'center',bord:true});\n"
    "    cell(ws,r,9, vd?((vd.fytd25_un||0)/1000).toFixed(1):'--',{fg:C.gray,align:'right',bord:true});\n"
    "    cell(ws,r,10,vd?((vd.fytd26_un||0)/1000).toFixed(1):'--',{fg:bc,align:'right',bord:true});\n"
    "    cell(ws,r,11,du!=null?fmtPct(du,1):'--',{fg:du!=null?(du>=0?C.green:C.red):C.gray,align:'center',bord:true});\n"
    "    cell(ws,r,12,vd?(_isUnMode?Math.round(vd.jan_un||0).toString():(vd.jan_val||0).toFixed(3)):'--',{align:'right',bord:true});\n"
    "    cell(ws,r,13,vd?(_isUnMode?Math.round(vd.fev_un||0).toString():(vd.fev_val||0).toFixed(3)):'--',{align:'right',bord:true});\n"
    "    cell(ws,r,14,vd?(_isUnMode?Math.round(vd.mar_un||0).toString():(vd.mar_val||0).toFixed(3)):'--',{align:'right',bord:true});\n"
    "  });\n"
    "\n"
    "  ws.autoFilter={from:{row:3,column:2},to:{row:3+st.brands.length,column:14}};\n"
    "  fillBg(ws,20,15);\n"
    "}"
)

NEW_BASE = (
    "function sheetBase(wb, st){\n"
    "  var ws=wb.addWorksheet('\U0001f4ca Base Analítica');\n"
    "  ws.views=[{state:'frozen',xSplit:1,ySplit:3,showGridLines:false}];\n"
    "  var widths=[2,22,13,13,10,14,14,11,14,14,11,12,12,12,12];\n"
    "  widths.forEach(function(w,i){ ws.getColumn(i+1).width=w; });\n"
    "\n"
    "  /* Título */\n"
    "  ws.mergeCells('B1:O1');\n"
    "  var t=ws.getCell('B1');\n"
    "  var _bmLbl=st.mode==='un'?' · UNIDADES':st.mode==='val'?' · VALOR R$M':'';\n"
    "  t.value='BASE ANALÍTICA NIELSEN'+_bmLbl+' — '+st.market.toUpperCase()+' — FY26 vs FY25';\n"
    "  t.fill={type:'pattern',pattern:'solid',fgColor:{argb:'FFFFFFFF'}};\n"
    "  t.font={name:'Calibri',size:14,bold:true,color:{argb:'FFB45309'}};\n"
    "  t.alignment={vertical:'middle',horizontal:'center'};\n"
    "  ws.getRow(1).height=28;\n"
    "\n"
    "  ws.mergeCells('B2:O2');\n"
    "  var s2=ws.getCell('B2');\n"
    "  s2.value='Jul/2025–Abr/2026 · Market: '+st.market+' · Exportado: '+new Date().toLocaleDateString('pt-BR');\n"
    "  s2.fill={type:'pattern',pattern:'solid',fgColor:{argb:'FFFFFFFF'}};\n"
    "  s2.font={name:'Calibri',size:10,color:{argb:'FF94A3B8'}};\n"
    "  s2.alignment={vertical:'middle',horizontal:'center'};\n"
    "  ws.getRow(2).height=18;\n"
    "\n"
    "  /* Headers */\n"
    "  var _isUnMode=(st.mode==='un');\n"
    "  var hdrs=['','Marca','Share FY25%','Share FY26%','Δ pp','Val FY25 R$M','Val FY26 R$M','Δ Val%',\n"
    "            'Vol FY25 Kun','Vol FY26 Kun','Δ Vol%',\n"
    "            _isUnMode?'Jan/26 Kun':'Jan/26 R$M',\n"
    "            _isUnMode?'Fev/26 Kun':'Fev/26 R$M',\n"
    "            _isUnMode?'Mar/26 Kun':'Mar/26 R$M',\n"
    "            _isUnMode?'Abr/26 Kun':'Abr/26 R$M'];\n"
    "  hdrs.forEach(function(v,i){ hdr(ws,3,i+1,v,C.hdr,C.gold); });\n"
    "  ws.getRow(3).height=22;\n"
    "\n"
    "  st.brands.forEach(function(b,i){\n"
    "    var rd=st.msoD[b]; var vd=st.valD?st.valD[b]:null; if(!rd) return;\n"
    "    var r=4+i; ws.getRow(r).height=18;\n"
    "    var d=rd.delta||0; var bc=BRAND_COL[b]||C.white; var dc=deltaColor(d);\n"
    "    var dv=vd&&vd.fytd25_val>0?(vd.fytd26_val-vd.fytd25_val)/vd.fytd25_val*100:null;\n"
    "    var du=vd&&vd.fytd25_un >0?(vd.fytd26_un -vd.fytd25_un )/vd.fytd25_un *100:null;\n"
    "    var a26v=vd?(vd.abr_val||0):0;\n"
    "    var a26u=vd&&vd.monthly_un?(vd.monthly_un[9]||0):0;\n"
    "    cell(ws,r,1,'',{bord:true});\n"
    "    cell(ws,r,2,b,{fg:bc,bold:true,bord:true});\n"
    "    cell(ws,r,3,(rd.fytd25||0).toFixed(2)+'%',{fg:C.gray,align:'center',bord:true});\n"
    "    cell(ws,r,4,(rd.fytd26||0).toFixed(2)+'%',{fg:bc,bold:true,align:'center',bord:true});\n"
    "    cell(ws,r,5,fmtPp(d),{fg:dc,bold:true,align:'center',bord:true});\n"
    "    cell(ws,r,6,vd?(vd.fytd25_val||0).toFixed(3):'--',{fg:C.gray,align:'right',bord:true});\n"
    "    cell(ws,r,7,vd?(vd.fytd26_val||0).toFixed(3):'--',{fg:bc,align:'right',bord:true});\n"
    "    cell(ws,r,8,dv!=null?fmtPct(dv,1):'--',{fg:dv!=null?(dv>=0?C.green:C.red):C.gray,align:'center',bord:true});\n"
    "    cell(ws,r,9, vd?((vd.fytd25_un||0)/1000).toFixed(1):'--',{fg:C.gray,align:'right',bord:true});\n"
    "    cell(ws,r,10,vd?((vd.fytd26_un||0)/1000).toFixed(1):'--',{fg:bc,align:'right',bord:true});\n"
    "    cell(ws,r,11,du!=null?fmtPct(du,1):'--',{fg:du!=null?(du>=0?C.green:C.red):C.gray,align:'center',bord:true});\n"
    "    cell(ws,r,12,vd?(_isUnMode?Math.round(vd.jan_un||0).toString():(vd.jan_val||0).toFixed(3)):'--',{align:'right',bord:true});\n"
    "    cell(ws,r,13,vd?(_isUnMode?Math.round(vd.fev_un||0).toString():(vd.fev_val||0).toFixed(3)):'--',{align:'right',bord:true});\n"
    "    cell(ws,r,14,vd?(_isUnMode?Math.round(vd.mar_un||0).toString():(vd.mar_val||0).toFixed(3)):'--',{align:'right',bord:true});\n"
    "    cell(ws,r,15,_isUnMode?(a26u>0?Math.round(a26u).toString():'--'):a26v.toFixed(3),{fg:bc,align:'right',bord:true});\n"
    "  });\n"
    "\n"
    "  ws.autoFilter={from:{row:3,column:2},to:{row:3+st.brands.length,column:15}};\n"
    "  fillBg(ws,20,16);\n"
    "}"
)

# Tentar substituição direta
c = html.count(OLD_BASE)
if c == 1:
    html = html.replace(OLD_BASE, NEW_BASE, 1)
    patches += 1
    print("  [OK] sheetBase: reescrita com coluna Abr/26 + subtitle atualizado")
elif c == 0:
    # Tentar com dashes '—' em vez de '—' literal
    print("  [!] sheetBase OLD não encontrado como string — tentando extração por posição")
    p = html.find('function sheetBase')
    end = html.find('\nfunction ', p + 10)
    if p > 0:
        OLD_EXTRACTED = html[p:end]
        html = html.replace(OLD_EXTRACTED, NEW_BASE, 1)
        patches += 1
        print(f"  [OK] sheetBase substituído por posição (len_old={len(OLD_EXTRACTED)})")
    else:
        print("  [X] sheetBase não encontrada!")
else:
    print(f"  [!] {c} ocorrências — abortando para segurança")

# ─────────────────────────────────────────────────────────────────
# RESUMO
# ─────────────────────────────────────────────────────────────────
print(f"\n=== RESUMO ===")
print(f"Patches: {patches}")
print(f"Original: {original_len:,} | Final: {len(html):,} | Diff: {len(html)-original_len:+,}")

with open(SRC, 'w', encoding='utf-8') as f:
    f.write(html)
print(f"\nSalvo: {SRC}")

ts = datetime.datetime.now().strftime('%Y%m%d_%H%M')
VER = os.path.join(BASE, "versoes", f"Dashboard_Farma_Sul_{ts}_ExportBaseCapaAbr.html")
shutil.copy2(SRC, VER)
print(f"Versao: {VER}")
