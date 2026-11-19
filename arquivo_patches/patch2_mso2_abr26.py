"""
patch2_mso2_abr26.py
Corrige as 3 pendências do patch1 + bug x.ab26 no insight
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

print("=== PATCH 2: Correcoes MSO2 Abr/26 ===\n")

# 1. HB chart titulo: MAR → ABR (linha 14210)
patch(
    "JAN&ndash;MAR &middot; '+hbUnitLbl+'</div>'",
    "JAN&ndash;ABR &middot; '+hbUnitLbl+'</div>'",
    "HB chart titulo — JAN-MAR → JAN-ABR"
)

# 2. Share bar chart: ACUM JAN–MAR → JAN–ABR (linha 14260)
patch(
    "ACUM JAN–MAR &middot; 2025 vs 2026</div>'",
    "ACUM JAN–ABR &middot; 2025 vs 2026</div>'",
    "Share bar ACUM JAN-MAR → JAN-ABR"
)

# 3. Insight header share mode: Jan–Mar/26 → Jan–Abr/26 (linha 19445)
patch(
    "DIAGNÓSTICO · '+mkt+' · Jan–Mar/26</div>'",
    "DIAGNÓSTICO · '+mkt+' · Jan–Abr/26</div>'",
    "Insight header share — Jan-Mar/26 → Jan-Abr/26"
)

# 4. Insight header val/un mode: JAN–MAR/26 → JAN–ABR/26 (linha 19564)
patch(
    "DIAGNÓSTICO · '+mkt+' · '+(isValI?'R$ MM':'Unidades')+' JAN–MAR/26</div>'",
    "DIAGNÓSTICO · '+mkt+' · '+(isValI?'R$ MM':'Unidades')+' JAN–ABR/26</div>'",
    "Insight header val/un — JAN-MAR/26 → JAN-ABR/26"
)

# 5. Bug no insight linha brand: x.m26 → x.ab26 no campo Abr (linha 19437)
patch(
    "+' · Abr: <strong style=\"color:'+x.cor+';\">'"+"+x.m26+'%</strong>';",
    "+' · Abr: <strong style=\"color:'+x.cor+';\">'"+"+x.ab26+'%</strong>';",
    "Insight Abr brand fix: x.m26 → x.ab26"
)

# 6. Insight brand rows: Jan-Mar/26 e Jan-Mar/25 → Jan-Abr (com fmtNI(v26b)/fmtNI(v25b))
patch(
    "Jan-Mar/26: <strong>'+fmtNI(v26b)+'</strong></span>'",
    "Jan-Abr/26: <strong>'+fmtNI(v26b)+'</strong></span>'",
    "Insight brand row Jan-Mar/26 → Jan-Abr/26"
)
patch(
    "Jan-Mar/25: '+fmtNI(v25b)+'</span>'",
    "Jan-Abr/25: '+fmtNI(v25b)+'</span>'",
    "Insight brand row Jan-Mar/25 → Jan-Abr/25"
)

# 7. Insight mercado total: Jan-Mar/25 e Jan-Mar/26 (com fmtNI(mtI25)/fmtNI(mtI26))
patch(
    "Jan-Mar/25: <strong style=\"color:#e2e8f0;\">'+fmtNI(mtI25)+'</strong></span>'",
    "Jan-Abr/25: <strong style=\"color:#e2e8f0;\">'+fmtNI(mtI25)+'</strong></span>'",
    "Insight mercado Jan-Mar/25 → Jan-Abr/25"
)
patch(
    "Jan-Mar/26: <strong style=\"color:#e2e8f0;\">'+fmtNI(mtI26)+'</strong></span>'",
    "Jan-Abr/26: <strong style=\"color:#e2e8f0;\">'+fmtNI(mtI26)+'</strong></span>'",
    "Insight mercado Jan-Mar/26 → Jan-Abr/26"
)

# 8. Insight HB bloco titulo: JAN-MAR → JAN-ABR (linha 19579)
patch(
    "JAN&ndash;MAR &middot; '+(isValI?'R$ MM':'Unidades')+'</div>'",
    "JAN&ndash;ABR &middot; '+(isValI?'R$ MM':'Unidades')+'</div>'",
    "Insight HB bloco titulo — JAN-MAR → JAN-ABR"
)

# 9. Insight HB valores: Jan-Mar/25 e Jan-Mar/26 (com fmtNI(hbI25)/fmtNI(hbI26))
patch(
    "Jan-Mar/25: <strong style=\"color:#3b82f6;\">'+fmtNI(hbI25)+'</strong></span>'",
    "Jan-Abr/25: <strong style=\"color:#3b82f6;\">'+fmtNI(hbI25)+'</strong></span>'",
    "Insight HB Jan-Mar/25 → Jan-Abr/25"
)
patch(
    "Jan-Mar/26: <strong style=\"color:#3b82f6;\">'+fmtNI(hbI26)+'</strong></span>'",
    "Jan-Abr/26: <strong style=\"color:#3b82f6;\">'+fmtNI(hbI26)+'</strong></span>'",
    "Insight HB Jan-Mar/26 → Jan-Abr/26"
)

# 10. Insight HB share: Share Jan-Mar → Share Jan-Abr
patch(
    "Share Jan-Mar/25: <strong style=\"color:#cbd5e1;\">'+shrHbI25.toFixed(1)+'%</strong></span>'",
    "Share Jan-Abr/25: <strong style=\"color:#cbd5e1;\">'+shrHbI25.toFixed(1)+'%</strong></span>'",
    "Insight HB Share Jan-Mar/25 → Jan-Abr/25"
)
patch(
    "Share Jan-Mar/26: <strong style=\"color:#3b82f6;\">'+shrHbI26.toFixed(1)+'%</strong></span>'",
    "Share Jan-Abr/26: <strong style=\"color:#3b82f6;\">'+shrHbI26.toFixed(1)+'%</strong></span>'",
    "Insight HB Share Jan-Mar/26 → Jan-Abr/26"
)

# 11. Comentario JAN-MAR no topo da funcao renderMSO2Insight (linha 19396)
patch(
    "// ── MSO2: Diagnóstico automático JAN-MAR YoY ──",
    "// ── MSO2: Diagnóstico automático JAN-ABR YoY ──",
    "Comentario funcao insight — JAN-MAR → JAN-ABR"
)

print(f"\n=== RESUMO ===")
print(f"Patches aplicados: {patches_applied}")
print(f"Tamanho original: {original_len:,} chars")
print(f"Tamanho final:    {len(html):,} chars")
print(f"Diferença:        {len(html)-original_len:+,} chars")

with open(SRC, 'w', encoding='utf-8') as f:
    f.write(html)
print(f"\nSalvo em: {SRC}")

VER = os.path.join(BASE, "versoes", f"Dashboard_Farma_Sul_{datetime.datetime.now().strftime('%Y%m%d_%H%M')}_MSO2Abr26_final2.html")
import shutil
shutil.copy2(SRC, VER)
print(f"Versao final: {VER}")
