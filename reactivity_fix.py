# reactivity_fix.py — Corrige acumulado Jan-Mar 2025 para T.BR Farma em R$/Un
#
# Diagnóstico raiz:
#   NIELSEN_BRAND_VAL['T.BR Farma'] já tem jan_val/fev_val/mar_val por marca (2026 OK)
#   Mas fytd25_val/fytd26_val = totais FYTD Jul-Mar (9 meses) — não Jan-Mar
#   Resultado: proporção errada → OFF! mostra +10.1% em vez de -10.6%
#
# Fix anterior (excel_sync_fix.py) foi aplicado em VOL_MKT_DATA (objeto errado).
# Este script:
#   P1 — Reverte VOL_MKT_DATA['T.BR Farma'] ao formato flat original
#   P2 — Adiciona jan25_val/fev25_val/mar25_val/jan25_un/fev25_un/mar25_un
#        a cada marca em NIELSEN_BRAND_VAL['T.BR Farma']
#   P3 — Corrige tooltip: usa soma exata para fyt25v/fyt26v quando jan25_val existe
import shutil, sys, os
sys.stdout.reconfigure(encoding='utf-8')

BASE = r'C:\Users\valqu\OneDrive\Documentos\Claude\Projects\projeto Dashboard_farma_sul'
SRC  = BASE + r'\Dashboard_farma_sul\Dashboard_Farma_Sul_20260512_2220.html'
BKP  = BASE + r'\Dashboard_farma_sul\versoes\Dashboard_Farma_Sul_20260513_1430_PreReactFix.html'
OUT  = BASE + r'\Dashboard_farma_sul\versoes\Dashboard_Farma_Sul_20260513_1435_ReactFix.html'

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
# PATCH 1 — Reverte VOL_MKT_DATA T.BR Farma ao flat original
#   O excel_sync_fix.py anterior substituiu a entrada flat por per-brand
#   em VOL_MKT_DATA (objeto errado). VOL_MKT_DATA não é usado pelo MSO2.
# ══════════════════════════════════════════════════════════════════════════════
print('\n=== Patch 1: Reverte VOL_MKT_DATA T.BR Farma ===')

# Match: o bloco multi-linha que foi inserido erroneamente no VOL_MKT_DATA
OLD_VOLTBR = (
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
NEW_VOLTBR = "  'T.BR Farma': {fytd25_val:419.62,fytd26_val:350.32,fytd25_un:14946.3,fytd26_un:12958.3,monthly_val:[20.308,17.772,23.247,27.268,33.373,51.28,68.229,55.537,53.304],monthly_un:[732.5,631.2,818.2,957.9,1287.0,1906.6,2473.8,2149.9,2001.1]},"

rep("VOL_MKT_DATA T.BR Farma revert", OLD_VOLTBR, NEW_VOLTBR)

# ══════════════════════════════════════════════════════════════════════════════
# PATCH 2 — Adiciona jan25_val...mar25_un a cada marca em NIELSEN_BRAND_VAL
#   Fonte: Excel Base Giovano 26-04.xlsx — valores exatos Jan-Mar 2025
#   Os campos jan_val/fev_val/mar_val (2026) JÁ EXISTEM — apenas adicionar 2025
# ══════════════════════════════════════════════════════════════════════════════
print('\n=== Patch 2: NIELSEN_BRAND_VAL T.BR Farma — adicionar jan25 por marca ===')

# OFF! — monthly_un termina em [...942.6, 816.1, 798.6, 802.0]}
rep("OFF! jan25 fields",
    "816.1, 798.6, 802.0]},",
    "816.1, 798.6, 802.0],jan25_val:24.018375,fev25_val:24.081004,mar25_val:24.473164,jan25_un:985.886,fev25_un:985.679,mar25_un:1000.829},"
)

# EXPOSIS — monthly_un termina em [...182.7, 170.2, 172.1]}
rep("EXPOSIS jan25 fields",
    "182.7, 170.2, 172.1]},",
    "182.7, 170.2, 172.1],jan25_val:15.720065,fev25_val:16.289647,mar25_val:16.767564,jan25_un:246.974,fev25_un:264.298,mar25_un:265.875},"
)

# XO INSETO — monthly_un termina em [...921.2, 895.0, 812.0]}
rep("XO INSETO jan25 fields",
    "921.2, 895.0, 812.0]},",
    "921.2, 895.0, 812.0],jan25_val:22.966070,fev25_val:20.674780,mar25_val:20.761698,jan25_un:1011.303,fev25_un:903.656,mar25_un:892.960},"
)

# SUPER REPELEX — monthly_un termina em [...161.0, 134.0, 152.4]}
rep("SUPER REPELEX jan25 fields",
    "161.0, 134.0, 152.4]},",
    "161.0, 134.0, 152.4],jan25_val:5.810664,fev25_val:5.067868,mar25_val:5.231167,jan25_un:267.155,fev25_un:235.785,mar25_un:241.212},"
)

# SBP — monthly_un termina em [...68.9, 63.0, 62.7]}
rep("SBP jan25 fields",
    "68.9, 63.0, 62.7]},",
    "68.9, 63.0, 62.7],jan25_val:4.129428,fev25_val:4.297143,mar25_val:4.372951,jan25_un:119.649,fev25_un:123.909,mar25_un:129.622},"
)

# ══════════════════════════════════════════════════════════════════════════════
# PATCH 3 — Corrige fyt25v e fyt26v no tooltip R$/Un
#   Antes: fyt25v = bd.fytd25_val (FYTD Jul-Mar total, errado para Jan-Mar)
#          fyt26v = bd.fytd26_val (FYTD Jul-Mar total, errado para Jan-Mar)
#   Depois: quando jan25_val existe → soma exata Jan+Fev+Mar/25
#            fyt26v = p26.acum (soma exata Jan+Fev+Mar/26, sempre disponível)
# ══════════════════════════════════════════════════════════════════════════════
print('\n=== Patch 3: Tooltip fyt25v/fyt26v exatos ===')

OLD_FYTV = (
  "        var isExact25 = nbvTp&&nbvTp[b]&&(isVal?nbvTp[b].jan25_val!==undefined:nbvTp[b].jan25_un!==undefined);\n"
  "        var lbl25 = isExact25 ? 'Jan-Mar/25' : 'Jan-Mar/25 (est.)';\n"
  "        tipRows = "
)

NEW_FYTV = (
  "        var isExact25 = nbvTp&&nbvTp[b]&&(isVal?nbvTp[b].jan25_val!==undefined:nbvTp[b].jan25_un!==undefined);\n"
  "        var lbl25 = isExact25 ? 'Jan-Mar/25' : 'Jan-Mar/25 (est.)';\n"
  "        var fyt25v, fyt26v;\n"
  "        if(isExact25 && nbvTp&&nbvTp[b]){\n"
  "          fyt25v = isVal\n"
  "            ? Math.round((nbvTp[b].jan25_val+nbvTp[b].fev25_val+nbvTp[b].mar25_val)*100)/100\n"
  "            : Math.round((nbvTp[b].jan25_un+nbvTp[b].fev25_un+nbvTp[b].mar25_un)*100)/100;\n"
  "        } else {\n"
  "          fyt25v = nbvTp&&nbvTp[b] ? (isVal?nbvTp[b].fytd25_val:nbvTp[b].fytd25_un) : 0;\n"
  "        }\n"
  "        fyt26v = p26.acum;\n"
  "        var fytD = calcDelta(fyt25v, fyt26v);\n"
  "        tipRows = "
)

rep("tooltip fyt25v/fyt26v exatos", OLD_FYTV, NEW_FYTV)

# ══════════════════════════════════════════════════════════════════════════════
# PATCH 4 — Remove declarações duplicadas fyt25v/fyt26v/fytD (do bloco anterior)
#   O bloco de tooltip antes do tipRows = tinha: var fyt25v, fyt26v, fytD
#   Agora que adicionamos essas declarações acima, as antigas são redundantes
# ══════════════════════════════════════════════════════════════════════════════
print('\n=== Patch 4: Remove fyt25v/fyt26v/fytD duplicados ===')

# O bloco else do tooltip tem as declarações originais logo acima do tipRows
# (linhas 9645-9650 da versão original)
OLD_DUP = (
  "        var pJulMar = p25.fytd25>0 ? Math.round((p26.acum - (p25.fytd25*(p26.acum/p26.acum||1)))/1*100)/100 : 0;\n"
  "        var fytPct = p25.fytd25>0 ? Math.round((p25.fytd26||p26.acum*(p25.fytd25>0?1:1)-p25.fytd25)/p25.fytd25*1000)/10 : 0;\n"
  "        var nbvTp = (typeof NIELSEN_BRAND_VAL !== 'undefined') ? NIELSEN_BRAND_VAL[mkt] : null;\n"
  "        var fyt25v = nbvTp&&nbvTp[b] ? (isVal?nbvTp[b].fytd25_val:nbvTp[b].fytd25_un) : 0;\n"
  "        var fyt26v = nbvTp&&nbvTp[b] ? (isVal?nbvTp[b].fytd26_val:nbvTp[b].fytd26_un) : 0;\n"
  "        var fytD = calcDelta(fyt25v, fyt26v);\n"
  "        var isExact25 ="
)

NEW_DUP = (
  "        var nbvTp = (typeof NIELSEN_BRAND_VAL !== 'undefined') ? NIELSEN_BRAND_VAL[mkt] : null;\n"
  "        var isExact25 ="
)

rep("remove fytv duplicados", OLD_DUP, NEW_DUP)

# ── Write ──────────────────────────────────────────────────────────────────────
with open(OUT, 'w', encoding='utf-8') as f:
    f.write(c)
shutil.copy2(OUT, SRC)
print(f'\n  Copied to active: {os.path.basename(SRC)}')
print(f'Linhas: {orig_lines} → {len(c.splitlines())} ({len(c.splitlines())-orig_lines:+d})')
print(f'Patches OK: {ok}/4')
print(f'Versão: {os.path.basename(OUT)}')

# ── Verify ─────────────────────────────────────────────────────────────────────
print()
absent = [
    # VOL_MKT_DATA não deve ter per-brand
    "'OFF!':{jan_val:24.198111",
    # Tooltip não deve mais ter fytd25_val como fyt25v fixo
    "fyt25v = nbvTp&&nbvTp[b] ? (isVal?nbvTp[b].fytd25_val",
]
present = [
    # NIELSEN_BRAND_VAL T.BR Farma OFF! deve ter jan25_val
    "802.0],jan25_val:24.018375",
    # EXPOSIS jan25
    "172.1],jan25_val:15.720065",
    # XO INSETO jan25
    "812.0],jan25_val:22.966070",
    # SUPER REPELEX jan25
    "152.4],jan25_val:5.810664",
    # SBP jan25
    "62.7],jan25_val:4.129428",
    # VOL_MKT_DATA flat restaurado
    "'T.BR Farma': {fytd25_val:419.62",
    # Tooltip com soma exata
    "fyt25v = isVal\n            ? Math.round((nbvTp[b].jan25_val",
    "fyt26v = p26.acum;",
    # renderMSO2 hasExact25 logic (do fix anterior)
    "hasExact25 = isVal",
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
