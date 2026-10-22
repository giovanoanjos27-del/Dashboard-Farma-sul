# excel_sync_fix.py — Corrige dados T.BR Farma: flat → per-brand (valores exatos Jan-Mar 2025/2026)
import shutil, sys, os
sys.stdout.reconfigure(encoding='utf-8')

BASE = r'C:\Users\valqu\OneDrive\Documentos\Claude\Projects\projeto Dashboard_farma_sul'
SRC  = BASE + r'\Dashboard_farma_sul\Dashboard_Farma_Sul_20260512_2220.html'
BKP  = BASE + r'\Dashboard_farma_sul\versoes\Dashboard_Farma_Sul_20260513_1420_PreExcelSync.html'
OUT  = BASE + r'\Dashboard_farma_sul\versoes\Dashboard_Farma_Sul_20260513_1425_ExcelSync.html'

shutil.copy2(SRC, BKP)
print(f'Backup: {os.path.basename(BKP)}')

with open(SRC, encoding='utf-8') as f:
    c = f.read()

orig_lines = len(c.splitlines())
ok = 0

def rep(label, old, new):
    global c, ok
    n = c.count(old)
    if n == 0:
        print(f'  MISS  {label}')
        return False
    c = c.replace(old, new, 1)
    print(f'  OK ({n})  {label}')
    ok += 1
    return True

# ══════════════════════════════════════════════════════════════════════════════
# PATCH 1 — DATA: Substitui entrada flat T.BR Farma por estrutura per-brand
#   Fonte: Excel "Base Giovano 26-04.xlsx" — aba 1-Tabela-1 — Jan-Mar 2025/2026
#   Acumulados calculados: soma exata Jan+Fev+Mar
#   OFF!   2025: 24.018375+24.081004+24.473164 = 72.572543   2026: 64.904622
#   EXPOSIS 2025: 48.777276   2026: 35.760853
#   SBP     2025: 12.799522   2026:  7.931457
#   SREP    2025: 16.109699   2026: 11.807590
#   XO      2025: 64.402548   2026: 56.665614
# ══════════════════════════════════════════════════════════════════════════════
print('\n=== Patch 1: T.BR Farma per-brand data ===')

OLD_DATA = "  'T.BR Farma': {fytd25_val:419.62,fytd26_val:350.32,fytd25_un:14946.3,fytd26_un:12958.3,monthly_val:[20.308,17.772,23.247,27.268,33.373,51.28,68.229,55.537,53.304],monthly_un:[732.5,631.2,818.2,957.9,1287.0,1906.6,2473.8,2149.9,2001.1]},"

NEW_DATA = (
  "  'T.BR Farma': {\n"
  "    fytd25_val:419.62,fytd26_val:350.32,fytd25_un:14946.3,fytd26_un:12958.3,\n"
  "    monthly_val:[20.308,17.772,23.247,27.268,33.373,51.28,68.229,55.537,53.304],\n"
  "    monthly_un:[732.5,631.2,818.2,957.9,1287.0,1906.6,2473.8,2149.9,2001.1],\n"
  "    'OFF!':{jan_val:24.198111,fev_val:20.579864,mar_val:20.126647,"
       "jan_un:942.135,fev_un:816.119,mar_un:801.997,"
       "fytd25_val:72.572543,fytd26_val:64.904622,fytd25_un:2972.394,fytd26_un:2560.251,"
       "jan25_val:24.018375,fev25_val:24.081004,mar25_val:24.473164,"
       "jan25_un:985.886,fev25_un:985.679,mar25_un:1000.829},\n"
  "    'EXPOSIS':{jan_val:14.369583,fev_val:11.083412,mar_val:10.307858,"
       "jan_un:232.755,fev_un:182.683,mar_un:172.056,"
       "fytd25_val:48.777276,fytd26_val:35.760853,fytd25_un:777.147,fytd26_un:587.494,"
       "jan25_val:15.720065,fev25_val:16.289647,mar25_val:16.767564,"
       "jan25_un:246.974,fev25_un:264.298,mar25_un:265.875},\n"
  "    'SBP':{jan_val:3.255353,fev_val:2.448259,mar_val:2.227845,"
       "jan_un:88.329,fev_un:68.930,mar_un:62.683,"
       "fytd25_val:12.799522,fytd26_val:7.931457,fytd25_un:373.180,fytd26_un:219.942,"
       "jan25_val:4.129428,fev25_val:4.297143,mar25_val:4.372951,"
       "jan25_un:119.649,fev25_un:123.909,mar25_un:129.622},\n"
  "    'SUPER REPELEX':{jan_val:5.081680,fev_val:3.499159,mar_val:3.226751,"
       "jan_un:222.556,fev_un:161.015,mar_un:152.376,"
       "fytd25_val:16.109699,fytd26_val:11.807590,fytd25_un:744.152,fytd26_un:535.947,"
       "jan25_val:5.810664,fev25_val:5.067868,mar25_val:5.231167,"
       "jan25_un:267.155,fev25_un:235.785,mar25_un:241.212},\n"
  "    'XO INSETO':{jan_val:21.324345,fev_val:17.926568,mar_val:17.414701,"
       "jan_un:988.003,fev_un:921.170,mar_un:811.990,"
       "fytd25_val:64.402548,fytd26_val:56.665614,fytd25_un:2807.919,fytd26_un:2721.163,"
       "jan25_val:22.966070,fev25_val:20.674780,mar25_val:20.761698,"
       "jan25_un:1011.303,fev25_un:903.656,mar25_un:892.960}\n"
  "  },"
)

rep("T.BR Farma flat → per-brand", OLD_DATA, NEW_DATA)

# ══════════════════════════════════════════════════════════════════════════════
# PATCH 2 — CODE: renderMSO2 forEach R$/Un — usar jan25_val quando disponível
#   Antes: a25 sempre estimado proporcionalmente (fytd25 * ratio)
#   Depois: se bd.jan25_val existe → a25 = jan25+fev25+mar25 (exato)
#           se não existe → mantém estimativa proporcional + GrowthMode = true
# ══════════════════════════════════════════════════════════════════════════════
print('\n=== Patch 2: renderMSO2 forEach exact25 ===')

OLD_LOOP = (
  "    var nbvS = (typeof NIELSEN_BRAND_VAL !== 'undefined') ? NIELSEN_BRAND_VAL[mkt] : null;\n"
  "    if(!nbvS){ console.warn('No NIELSEN_BRAND_VAL for', mkt); return; }\n"
  "    GrowthMode = true;\n"
  "    brands.forEach(function(b){\n"
  "      var bd = nbvS[b]; if(!bd) return;\n"
  "      var j26 = isVal?bd.jan_val:bd.jan_un, f26 = isVal?bd.fev_val:bd.fev_un, m26 = isVal?bd.mar_val:bd.mar_un;\n"
  "      var fyt25 = isVal?bd.fytd25_val:bd.fytd25_un, fyt26 = isVal?bd.fytd26_val:bd.fytd26_un;\n"
  "      var a26 = Math.round((j26+f26+m26)*100)/100;\n"
  "      var ratio = fyt26>0 ? a26/fyt26 : 1/3;\n"
  "      var a25 = Math.round(fyt25*ratio*100)/100;\n"
  "      d25[b] = {jan:null, fev:null, mar:null, acum:a25, fytd25:fyt25, fytd26:fyt26};\n"
  "      d26[b] = {jan:j26, fev:f26, mar:m26, acum:a26};\n"
  "    });"
)

NEW_LOOP = (
  "    var nbvS = (typeof NIELSEN_BRAND_VAL !== 'undefined') ? NIELSEN_BRAND_VAL[mkt] : null;\n"
  "    if(!nbvS){ console.warn('No NIELSEN_BRAND_VAL for', mkt); return; }\n"
  "    GrowthMode = false;\n"
  "    brands.forEach(function(b){\n"
  "      var bd = nbvS[b]; if(!bd) return;\n"
  "      var j26 = isVal?bd.jan_val:bd.jan_un, f26 = isVal?bd.fev_val:bd.fev_un, m26 = isVal?bd.mar_val:bd.mar_un;\n"
  "      var fyt25 = isVal?bd.fytd25_val:bd.fytd25_un, fyt26 = isVal?bd.fytd26_val:bd.fytd26_un;\n"
  "      var a26 = Math.round((j26+f26+m26)*100)/100;\n"
  "      var hasExact25 = isVal ? (bd.jan25_val!==undefined) : (bd.jan25_un!==undefined);\n"
  "      var j25, f25, m25, a25;\n"
  "      if(hasExact25){\n"
  "        j25 = isVal?bd.jan25_val:bd.jan25_un;\n"
  "        f25 = isVal?bd.fev25_val:bd.fev25_un;\n"
  "        m25 = isVal?bd.mar25_val:bd.mar25_un;\n"
  "        a25 = Math.round((j25+f25+m25)*100)/100;\n"
  "      } else {\n"
  "        j25 = null; f25 = null; m25 = null;\n"
  "        var ratio = fyt26>0 ? a26/fyt26 : 1/3;\n"
  "        a25 = Math.round(fyt25*ratio*100)/100;\n"
  "        GrowthMode = true;\n"
  "      }\n"
  "      d25[b] = {jan:j25, fev:f25, mar:m25, acum:a25, fytd25:fyt25, fytd26:fyt26, hasExact:hasExact25};\n"
  "      d26[b] = {jan:j26, fev:f26, mar:m26, acum:a26};\n"
  "    });"
)

rep("renderMSO2 forEach exact25", OLD_LOOP, NEW_LOOP)

# ══════════════════════════════════════════════════════════════════════════════
# PATCH 3 — CODE: Tooltip R$/Un — mostrar meses exatos 2025 quando disponível
#   Remove "(est.)" quando dados são exatos; exibe Jan/25, Fev/25, Mar/25
# ══════════════════════════════════════════════════════════════════════════════
print('\n=== Patch 3: tooltip exact25 label + monthly 2025 ===')

OLD_TIP = (
  "        tipRows = '<div class=\"mso2-tip-row\"><span class=\"mso2-tip-lbl\">Jan/26</span>"
    "<span style=\"color:'+cor+';font-weight:700;\">'+fmtV(p26.jan||0)+'</span></div>'\n"
  "          +'<div class=\"mso2-tip-row\"><span class=\"mso2-tip-lbl\">Fev/26</span>"
    "<span style=\"color:'+cor+';font-weight:700;\">'+fmtV(p26.fev||0)+'</span></div>'\n"
  "          +'<div class=\"mso2-tip-row\"><span class=\"mso2-tip-lbl\">Mar/26</span>"
    "<span style=\"color:'+cor+';font-weight:700;\">'+fmtV(p26.mar||0)+'</span></div>'\n"
  "          +'<div style=\"height:1px;background:rgba(255,255,255,0.07);margin:5px 0;\"></div>'\n"
  "          +'<div class=\"mso2-tip-row\"><span class=\"mso2-tip-lbl\">Jan-Mar/25 (est.)</span>"
    "<span class=\"mso2-tip-val\">'+fmtV(fyt25v)+'</span></div>'\n"
  "          +'<div class=\"mso2-tip-row\"><span class=\"mso2-tip-lbl\">Jan-Mar/26</span>"
    "<span style=\"color:'+cor+';font-weight:700;\">'+fmtV(fyt26v)+'</span></div>'\n"
  "          +'<div class=\"mso2-tip-row\"><span class=\"mso2-tip-lbl\">Δ JAN-MAR (YoY)</span>"
    "<span style=\"font-weight:700;color:'+fytD.col+';\">\'+(fytD.up?\'\\u2191 \':\'\\u2193 \')+fytD.str+\'</span></div>\';"
)

# Verificar se a string de busca existe com esta representação
# — teste alternativo com a string literal do arquivo
OLD_TIP2 = (
  "        tipRows = '<div class=\"mso2-tip-row\"><span class=\"mso2-tip-lbl\">Jan/26</span><span style=\"color:'+cor+';font-weight:700;\">'+fmtV(p26.jan||0)+'</span></div>'\n"
  "          +'<div class=\"mso2-tip-row\"><span class=\"mso2-tip-lbl\">Fev/26</span><span style=\"color:'+cor+';font-weight:700;\">'+fmtV(p26.fev||0)+'</span></div>'\n"
  "          +'<div class=\"mso2-tip-row\"><span class=\"mso2-tip-lbl\">Mar/26</span><span style=\"color:'+cor+';font-weight:700;\">'+fmtV(p26.mar||0)+'</span></div>'\n"
  "          +'<div style=\"height:1px;background:rgba(255,255,255,0.07);margin:5px 0;\"></div>'\n"
  "          +'<div class=\"mso2-tip-row\"><span class=\"mso2-tip-lbl\">Jan-Mar/25 (est.)</span><span class=\"mso2-tip-val\">'+fmtV(fyt25v)+'</span></div>'\n"
  "          +'<div class=\"mso2-tip-row\"><span class=\"mso2-tip-lbl\">Jan-Mar/26</span><span style=\"color:'+cor+';font-weight:700;\">'+fmtV(fyt26v)+'</span></div>'\n"
  "          +'<div class=\"mso2-tip-row\"><span class=\"mso2-tip-lbl\">Δ JAN-MAR (YoY)</span><span style=\"font-weight:700;color:'+fytD.col+';\">'"
  "+(fytD.up?'↑ ':'↓ ')+fytD.str+'</span></div>';"
)

NEW_TIP2 = (
  "        var isExact25 = nbvTp&&nbvTp[b]&&(isVal?nbvTp[b].jan25_val!==undefined:nbvTp[b].jan25_un!==undefined);\n"
  "        var lbl25 = isExact25 ? 'Jan-Mar/25' : 'Jan-Mar/25 (est.)';\n"
  "        tipRows = '<div class=\"mso2-tip-row\"><span class=\"mso2-tip-lbl\">Jan/26</span><span style=\"color:'+cor+';font-weight:700;\">'+fmtV(p26.jan||0)+'</span></div>'\n"
  "          +'<div class=\"mso2-tip-row\"><span class=\"mso2-tip-lbl\">Fev/26</span><span style=\"color:'+cor+';font-weight:700;\">'+fmtV(p26.fev||0)+'</span></div>'\n"
  "          +'<div class=\"mso2-tip-row\"><span class=\"mso2-tip-lbl\">Mar/26</span><span style=\"color:'+cor+';font-weight:700;\">'+fmtV(p26.mar||0)+'</span></div>'\n"
  "          +'<div style=\"height:1px;background:rgba(255,255,255,0.07);margin:5px 0;\"></div>'\n"
  "          +(isExact25\n"
  "            ? '<div class=\"mso2-tip-row\"><span class=\"mso2-tip-lbl\">Jan/25</span><span class=\"mso2-tip-val\">'+(isVal?fmtV(nbvTp[b].jan25_val):fmtV(nbvTp[b].jan25_un))+'</span></div>'\n"
  "              +'<div class=\"mso2-tip-row\"><span class=\"mso2-tip-lbl\">Fev/25</span><span class=\"mso2-tip-val\">'+(isVal?fmtV(nbvTp[b].fev25_val):fmtV(nbvTp[b].fev25_un))+'</span></div>'\n"
  "              +'<div class=\"mso2-tip-row\"><span class=\"mso2-tip-lbl\">Mar/25</span><span class=\"mso2-tip-val\">'+(isVal?fmtV(nbvTp[b].mar25_val):fmtV(nbvTp[b].mar25_un))+'</span></div>'\n"
  "              +'<div style=\"height:1px;background:rgba(255,255,255,0.07);margin:4px 0;\"></div>'\n"
  "            : '')\n"
  "          +'<div class=\"mso2-tip-row\"><span class=\"mso2-tip-lbl\">'+lbl25+'</span><span class=\"mso2-tip-val\">'+fmtV(fyt25v)+'</span></div>'\n"
  "          +'<div class=\"mso2-tip-row\"><span class=\"mso2-tip-lbl\">Jan-Mar/26</span><span style=\"color:'+cor+';font-weight:700;\">'+fmtV(fyt26v)+'</span></div>'\n"
  "          +'<div class=\"mso2-tip-row\"><span class=\"mso2-tip-lbl\">Δ JAN-MAR (YoY)</span><span style=\"font-weight:700;color:'+fytD.col+';\">'"
  "+(fytD.up?'↑ ':'↓ ')+fytD.str+'</span></div>';"
)

rep("tooltip exact25 meses", OLD_TIP2, NEW_TIP2)

# ── Write ──────────────────────────────────────────────────────────────────────
with open(OUT, 'w', encoding='utf-8') as f:
    f.write(c)
shutil.copy2(OUT, SRC)
print(f'\n  Copied to active: {os.path.basename(SRC)}')
print(f'Linhas: {orig_lines} → {len(c.splitlines())} ({len(c.splitlines())-orig_lines:+d})')
print(f'Patches OK: {ok}/3')
print(f'Versão: {os.path.basename(OUT)}')

# ── Verify ─────────────────────────────────────────────────────────────────────
print()
absent = [
    "'T.BR Farma': {fytd25_val:419.62",   # flat entry deve sumir
    "GrowthMode = true;\n    brands.forEach",  # GrowthMode = true antes do loop deve sumir
    "Jan-Mar/25 (est.)</span><span class=\"mso2-tip-val\">'+fmtV(fyt25v)",  # label (est.) incondicional deve sumir
]
present = [
    "'OFF!':{jan_val:24.198111",            # per-brand OFF!
    "'EXPOSIS':{jan_val:14.369583",         # per-brand EXPOSIS
    "'SBP':{jan_val:3.255353",              # per-brand SBP
    "'SUPER REPELEX':{jan_val:5.081680",    # per-brand SUPER REPELEX
    "'XO INSETO':{jan_val:21.324345",       # per-brand XO INSETO
    "jan25_val:24.018375",                  # campo jan25_val OFF!
    "jan25_val:22.966070",                  # campo jan25_val XO INSETO
    "hasExact25 = isVal",                   # lógica exact25
    "GrowthMode = false;",                  # reset antes do loop
    "lbl25 = isExact25",                    # label dinâmico tooltip
]

print('--- AUSENTES (OK = não encontrado) ---')
for s in absent:
    found = s in c
    print(f"  {'FAIL ainda presente!':22s}" if found else f"  {'OK  ausente':22s}", s[:60])

print()
print('--- PRESENTES (OK = encontrado) ---')
for s in present:
    found = s in c
    print(f"  {'OK  ':22s}" if found else f"  {'FAIL não encontrado!':22s}", s[:60])
