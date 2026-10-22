"""
patch4_nielsen_abr26.py
Corrige 7 componentes Nielsen que ainda mostravam MAR/26 ou tinham fy26[9]=null:
 1. SHR_TREND_DATA Farma Sul     — fy26[9] para 5 marcas
 2. SHR_TREND_DATA T.BR Farma   — fy26[9] para 5 marcas
 3. renderShrTrend forEach       — indice dinamico _lIdx (remove corte i<9)
 4. renderShrTrend diagnostico   — indice dinamico _dLi
 5. renderMSO3                   — JUL-MAR → JUL-ABR (titulo + chart label)
 6. AVG_MESES                    — adiciona 'ABR/26'
 7. MESES_LBL                    — adiciona "202604":"Abr/26"
 8. renderMSOSkuJanMar           — subtitle Jan-Mar → Jan-Abr
"""
import os, shutil, datetime

BASE = r"C:\Users\valqu\OneDrive\Documentos\Claude\Projects\projeto Dashboard_farma_sul\Dashboard_farma_sul"
SRC  = os.path.join(BASE, "Dashboard_Farma_Sul_20260512_2220.html")

with open(SRC, 'r', encoding='utf-8') as f:
    html = f.read()

original_len = len(html)
patches_applied = 0

def patch(old, new, desc):
    global html, patches_applied
    count = html.count(old)
    if count == 0:
        print(f"  [X] NAO ENCONTRADO: {desc}")
        return False
    if count > 1:
        print(f"  [!] MULTIPLOS ({count}x): {desc} — aplicando todos")
    html = html.replace(old, new)
    patches_applied += count
    print(f"  [OK] ({count}x) {desc}")
    return True

print("=== PATCH 4: Nielsen Abr/26 — 7 componentes ===\n")

# ── 1. SHR_TREND_DATA — Farma Sul ──────────────────────────────────────────
print("--- SHR_TREND_DATA Farma Sul ---")
patch(
    "fy26:[23.86,24.06,23.6,25.62,26.29,25.44,24.67,25.46,26.51,null,null,null]}",
    "fy26:[23.86,24.06,23.6,25.62,26.29,25.44,24.67,25.46,26.51,26.06,null,null]}",
    "Farma Sul OFF! fy26[9]=26.06"
)
patch(
    "fy26:[13.26,12.7,11.78,11.11,9.72,9.79,9.53,11.16,10.87,null,null,null]}",
    "fy26:[13.26,12.7,11.78,11.11,9.72,9.79,9.53,11.16,10.87,12.95,null,null]}",
    "Farma Sul EXPOSIS fy26[9]=12.95"
)
patch(
    "fy26:[21.51,23.02,22.57,19.37,22.48,22.09,25.45,26.37,24.65,null,null,null]}",
    "fy26:[21.51,23.02,22.57,19.37,22.48,22.09,25.45,26.37,24.65,24.95,null,null]}",
    "Farma Sul XO INSETO fy26[9]=24.95"
)
patch(
    "fy26:[5.35,5.73,5.97,7.28,7.26,7.63,7.45,6.78,7.1,null,null,null]}",
    "fy26:[5.35,5.73,5.97,7.28,7.26,7.63,7.45,6.78,7.1,6.41,null,null]}",
    "Farma Sul SUPER REPELEX fy26[9]=6.41"
)
patch(
    "fy26:[2.72,2.58,3.36,2.95,2.55,2.85,2.47,2.49,2.52,null,null,null]}",
    "fy26:[2.72,2.58,3.36,2.95,2.55,2.85,2.47,2.49,2.52,2.27,null,null]}",
    "Farma Sul SBP fy26[9]=2.27"
)

# ── 2. SHR_TREND_DATA — T.BR Farma ─────────────────────────────────────────
print("--- SHR_TREND_DATA T.BR Farma ---")
patch(
    "fy26:[31.04,30.32,29.61,29.94,29.51,28.89,28.49,30.42,31.25,null,null,null]}",
    "fy26:[31.04,30.32,29.61,29.94,29.51,28.89,28.49,30.42,31.25,31.00,null,null]}",
    "T.BR Farma OFF! fy26[9]=31.00"
)
patch(
    "fy26:[18.99,18.52,18.94,18.74,16.83,16.42,16.92,16.38,16.0,null,null,null]}",
    "fy26:[18.99,18.52,18.94,18.74,16.83,16.42,16.92,16.38,16.0,17.50,null,null]}",
    "T.BR Farma EXPOSIS fy26[9]=17.50"
)
patch(
    "fy26:[23.75,23.97,22.65,21.71,24.17,24.21,25.11,26.49,27.04,null,null,null]}",
    "fy26:[23.75,23.97,22.65,21.71,24.17,24.21,25.11,26.49,27.04,26.87,null,null]}",
    "T.BR Farma XO INSETO fy26[9]=26.87"
)
patch(
    "fy26:[4.8,5.2,5.16,5.46,5.55,5.79,5.98,5.17,5.01,null,null,null]}",
    "fy26:[4.8,5.2,5.16,5.46,5.55,5.79,5.98,5.17,5.01,5.02,null,null]}",
    "T.BR Farma SUPER REPELEX fy26[9]=5.02"
)
patch(
    "fy26:[4.59,4.8,4.83,4.61,3.96,4.05,3.83,3.62,3.46,null,null,null]}",
    "fy26:[4.59,4.8,4.83,4.61,3.96,4.05,3.83,3.62,3.46,3.21,null,null]}",
    "T.BR Farma SBP fy26[9]=3.21"
)

# ── 3. renderShrTrend forEach — indice dinamico ─────────────────────────────
print("--- renderShrTrend forEach ---")

# 3a. delta: substituir [8] por _lIdx dinamico (insere _lIdx/_latLbl antes do delta)
patch(
    "var delta=bd.delta!=null?bd.delta:(bd.fy26[8]!=null&&bd.fy25[8]!=null?parseFloat((bd.fy26[8]-bd.fy25[8]).toFixed(2)):null);var sign=delta!=null&&delta>=0?'+':'';",
    "var _lIdx=bd.fy26.reduce(function(a,v,i){return v!=null?i:a;},8);var _latLbl=['Jul','Ago','Set','Out','Nov','Dez','Jan','Fev','Mar','Abr'][_lIdx]||'Mar';var delta=bd.delta!=null?bd.delta:(bd.fy26[_lIdx]!=null&&bd.fy25[_lIdx]!=null?parseFloat((bd.fy26[_lIdx]-bd.fy25[_lIdx]).toFixed(2)):null);var sign=delta!=null&&delta>=0?'+':'';",
    "renderShrTrend forEach: delta dinamico com _lIdx"
)

# 3b. label "vs Mar/25" → dinamico
patch(
    "+'pp':'\\u2014')+' vs Mar/25</span>'",
    "+'pp':'\\u2014')+' vs '+_latLbl+'/25</span>'",
    "renderShrTrend forEach: vs Mar/25 → vs _latLbl/25"
)

# 3c. label "Mar/26:" no single-brand detail → dinamico
patch(
    ">Mar/26: <b style=\"color:'+col+';\">'+latest.toFixed(2)+'%</b> share</div>';",
    ">'+_latLbl+'/26: <b style=\"color:'+col+';\">'+latest.toFixed(2)+'%</b> share</div>';",
    "renderShrTrend forEach: Mar/26 → _latLbl/26"
)

# 3d. corte fy26 i<9 → i<=_lIdx (exibe Abr quando disponivel)
patch(
    "var fy26f=bd.fy26.map(function(v,i){return i<9?v:null;});",
    "var fy26f=bd.fy26.map(function(v,i){return i<=_lIdx?v:null;});",
    "renderShrTrend forEach: corte i<9 → i<=_lIdx"
)

# ── 4. renderShrTrend diagnostico — indice dinamico ────────────────────────
print("--- renderShrTrend diagnostico ---")

# 4a. Insere _dLi/_dLbl antes de allBrandsD e ajusta s26/s25
patch(
    "var allBrandsD=['OFF!','EXPOSIS','XO INSETO','SUPER REPELEX','SBP'];\n    var rows = allBrandsD.map(function(br){\n      var bd2=d[br]; if(!bd2)return null;\n      var s26=bd2.fy26[8]; var s25=bd2.fy25[8];",
    "var allBrandsD=['OFF!','EXPOSIS','XO INSETO','SUPER REPELEX','SBP'];var _dRef=d['OFF!']||d['XO INSETO'];var _dLi=_dRef?_dRef.fy26.reduce(function(a,v,i){return v!=null?i:a;},8):8;var _dLbl=['Jul','Ago','Set','Out','Nov','Dez','Jan','Fev','Mar','Abr'][_dLi]||'Mar';\n    var rows = allBrandsD.map(function(br){\n      var bd2=d[br]; if(!bd2)return null;\n      var s26=bd2.fy26[_dLi]; var s25=bd2.fy25[_dLi];",
    "diagnostico: _dLi/_dLbl + s26/s25 dinamicos"
)

# 4b. SCJ portfolio: null-check e acumuladores com _dLi
patch(
    "      if(!bd2||bd2.fy26[8]==null||bd2.fy25[8]==null){scjOk=false;return;}\n      scj26+=bd2.fy26[8]; scj25+=bd2.fy25[8];",
    "      if(!bd2||bd2.fy26[_dLi]==null||bd2.fy25[_dLi]==null){scjOk=false;return;}\n      scj26+=bd2.fy26[_dLi]; scj25+=bd2.fy25[_dLi];",
    "diagnostico: SCJ null-check e acumuladores com _dLi"
)

# 4c. Header DIAGNOSTICO · MAR/26 → dinamico
patch(
    "margin-bottom:8px;\">DIAGNÓSTICO · MAR/26 · '+mkt+'</div>'",
    "margin-bottom:8px;\">DIAGNÓSTICO · '+_dLbl.toUpperCase()+'/26 · '+mkt+'</div>'",
    "diagnostico: header MAR/26 → _dLbl/26"
)

# 4d. Coluna MAR/26 no thead (estilo completo para garantir unicidade)
patch(
    "rgba(255,255,255,0.06);\">MAR/26</th>'",
    "rgba(255,255,255,0.06);\">'+_dLbl.toUpperCase()+'/26</th>'",
    "diagnostico: coluna MAR/26 → _dLbl/26"
)

# 4e. Coluna MAR/25 no thead (estilo completo para garantir unicidade)
patch(
    "rgba(255,255,255,0.06);\">MAR/25</th>'",
    "rgba(255,255,255,0.06);\">'+_dLbl.toUpperCase()+'/25</th>'",
    "diagnostico: coluna MAR/25 → _dLbl/25"
)

# ── 5. renderMSO3 — JUL-MAR → JUL-ABR ──────────────────────────────────────
print("--- renderMSO3 ---")
patch(
    "isVal ? 'VENDA VALOR FYTD · JUL–MAR' : 'UNIDADES FYTD · JUL–MAR'",
    "isVal ? 'VENDA VALOR FYTD · JUL–ABR' : 'UNIDADES FYTD · JUL–ABR'",
    "renderMSO3: titulo JUL-MAR → JUL-ABR"
)
patch(
    "FYTD JUL&ndash;MAR &middot; '+(isVal?'R$ MM':'Unidades')+'</div>'",
    "FYTD JUL&ndash;ABR &middot; '+(isVal?'R$ MM':'Unidades')+'</div>'",
    "renderMSO3: chart label FYTD JUL-MAR → JUL-ABR"
)

# ── 6. AVG_MESES — adiciona ABR/26 ──────────────────────────────────────────
print("--- AVG_MESES ---")
patch(
    "const AVG_MESES = ['JUL/25','AGO/25','SET/25','OUT/25','NOV/25','DEZ/25','JAN/26','FEV/26','MAR/26'];",
    "const AVG_MESES = ['JUL/25','AGO/25','SET/25','OUT/25','NOV/25','DEZ/25','JAN/26','FEV/26','MAR/26','ABR/26'];",
    "AVG_MESES: adiciona ABR/26 como 10o eixo"
)

# ── 7. MESES_LBL — adiciona 202604:Abr/26 ───────────────────────────────────
print("--- MESES_LBL ---")
patch(
    '"202603":"Mar/26"};',
    '"202603":"Mar/26","202604":"Abr/26"};',
    "MESES_LBL: adiciona 202604 → Abr/26"
)

# ── 8. renderMSOSkuJanMar — subtitle Jan-Mar → Jan-Abr ──────────────────────
print("--- renderMSOSkuJanMar ---")
patch(
    "sub.textContent='Share por SKU · Jan-Mar/26 vs Jan-Mar/25 · '+mkt+' · Personal Repellent';",
    "sub.textContent='Share por SKU · Jan-Abr/26 vs Jan-Abr/25 · '+mkt+' · Personal Repellent';",
    "renderMSOSkuJanMar: subtitle Jan-Mar → Jan-Abr"
)

# ── RESUMO ───────────────────────────────────────────────────────────────────
print(f"\n=== RESUMO ===")
print(f"Patches aplicados: {patches_applied}")
print(f"Tamanho original:  {original_len:,} chars")
print(f"Tamanho final:     {len(html):,} chars")
print(f"Diferenca:         {len(html)-original_len:+,} chars")

with open(SRC, 'w', encoding='utf-8') as f:
    f.write(html)
print(f"\nSalvo em: {SRC}")

VER = os.path.join(BASE, "versoes", f"Dashboard_Farma_Sul_{datetime.datetime.now().strftime('%Y%m%d_%H%M')}_NielsenAbr26_final.html")
shutil.copy2(SRC, VER)
print(f"Versao final: {VER}")
