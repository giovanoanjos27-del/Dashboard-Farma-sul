"""
patch11_sku_fytd_avg_diag.py

Fix 1: SKU_MKT_DATA fytd26 atualizado para incluir Abril (Jul-Abr/26)
  — T.BR Farma e Farma Sul recalculados pelo método weighted $
  — Outros mercados: fytd26 permanece como Jul-Mar (sem dados de Abril disponíveis)

Fix 2: renderAvgInsight — Diagnóstico Preço Médio
  — Adiciona rótulo de período: "Jul/25: R$X → Abr/26: R$Y"
  — Adiciona tendência recente (últimos 3 meses vs 3 anteriores)
  — Classifica como "em queda" apenas se tendência RECENTE for negativa (>5%)
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

print("=== PATCH 11: SKU FYTD + Avg Diag ===\n")

# ──────────────────────────────────────────────────────────────────────────────
# 1. SKU_MKT_DATA — T.BR Farma fytd26 → Jul-Abr/26
# ──────────────────────────────────────────────────────────────────────────────
# Metodologia: fytd26_new_$ = fytd26_old_$ + abr26_sku_$
#   abr26_sku_$ calculado back-computing de janabr26 e janmar26_old
# T.BR Farma: fy9=431.73MM, abr26=59.05MM, fy10=490.77MM
# OLD fytd26: [15.56,13.7,9.83,7.82,7.22,6.39,5.79,4.61,3.81,3.76]
# NEW fytd26: [15.61,13.74,9.93,7.94,7.30,6.42,5.70,4.66,3.82,3.76]
# OLD var:    [1.73,-1.54,0.34,-0.62,0.80,-0.04,-1.88,1.12,1.23,0.33]
# NEW var:    [1.77,-1.50,0.43,-0.50,0.89,-0.02,-1.97,1.17,1.24,0.33]

print("--- SKU_MKT_DATA T.BR Farma fytd26 ---")
patch(
    '"T.BR Farma": {"skus": ["OFF! Family", "Exposis Infantil", "X\xf4 Spray 200ml", "X\xf4 Lo\xe7\xe3o 200ml", "OFF! Family Lo\xe7\xe3o 200ml PR", "OFF! Kids ", "All Others Lo\xe7\xe3o", "OFF! Baby", "OFF! Family Spray 170ml PR", "All Others Aero"], '
    '"fytd25": [13.84, 15.24, 9.5, 8.44, 6.41, 6.44, 7.67, 3.49, 2.58, 3.43], '
    '"fytd26": [15.56, 13.7, 9.83, 7.82, 7.22, 6.39, 5.79, 4.61, 3.81, 3.76], '
    '"var": [1.73, -1.54, 0.34, -0.62, 0.8, -0.04, -1.88, 1.12, 1.23, 0.33]}',
    '"T.BR Farma": {"skus": ["OFF! Family", "Exposis Infantil", "X\xf4 Spray 200ml", "X\xf4 Lo\xe7\xe3o 200ml", "OFF! Family Lo\xe7\xe3o 200ml PR", "OFF! Kids ", "All Others Lo\xe7\xe3o", "OFF! Baby", "OFF! Family Spray 170ml PR", "All Others Aero"], '
    '"fytd25": [13.84, 15.24, 9.5, 8.44, 6.41, 6.44, 7.67, 3.49, 2.58, 3.43], '
    '"fytd26": [15.61, 13.74, 9.93, 7.94, 7.3, 6.42, 5.7, 4.66, 3.82, 3.76], '
    '"var": [1.77, -1.5, 0.43, -0.5, 0.89, -0.02, -1.97, 1.17, 1.24, 0.33]}',
    "T.BR Farma fytd26 Jul-Abr (inclui Abril)"
)

# ──────────────────────────────────────────────────────────────────────────────
# 2. SKU_MKT_DATA — Farma Sul fytd26 → Jul-Abr/26
# ──────────────────────────────────────────────────────────────────────────────
# Farma Sul: fy9=107.10MM, abr26=11.32MM, fy10=118.42MM
# OLD fytd26: [14.93,12.97,11.71,8.96,8.31,5.42,5.32,5.24,5.02,3.33]
# NEW fytd26: [14.94,12.65,11.68,8.84,8.48,5.46,5.31,5.21,5.02,3.33]
# OLD var:    [1.62, 1.05, 0.85,-2.45,-1.90,-0.34,0.19,1.65,-0.67,0.13]
# NEW var:    [1.62, 0.73, 0.82,-2.57,-1.73,-0.30,0.18,1.62,-0.67,0.13]

print("\n--- SKU_MKT_DATA Farma Sul fytd26 ---")
patch(
    '"Farma Sul": {"skus": ["OFF! Family", "All Others Aero", "X\xf4 Spray 200ml", "All Others Lo\xe7\xe3o", "Exposis Infantil", "X\xf4 Lo\xe7\xe3o 200ml", "OFF! Family Lo\xe7\xe3o 200ml PR", "OFF! Family Spray 170ml PR", "OFF! Kids ", "OFF! Baby"], '
    '"fytd25": [13.32, 11.92, 10.86, 11.41, 10.21, 5.76, 5.13, 3.59, 5.69, 3.2], '
    '"fytd26": [14.93, 12.97, 11.71, 8.96, 8.31, 5.42, 5.32, 5.24, 5.02, 3.33], '
    '"var": [1.62, 1.05, 0.85, -2.45, -1.9, -0.34, 0.19, 1.65, -0.67, 0.14]}',
    '"Farma Sul": {"skus": ["OFF! Family", "All Others Aero", "X\xf4 Spray 200ml", "All Others Lo\xe7\xe3o", "Exposis Infantil", "X\xf4 Lo\xe7\xe3o 200ml", "OFF! Family Lo\xe7\xe3o 200ml PR", "OFF! Family Spray 170ml PR", "OFF! Kids ", "OFF! Baby"], '
    '"fytd25": [13.32, 11.92, 10.86, 11.41, 10.21, 5.76, 5.13, 3.59, 5.69, 3.2], '
    '"fytd26": [14.94, 12.65, 11.68, 8.84, 8.48, 5.46, 5.31, 5.21, 5.02, 3.33], '
    '"var": [1.62, 0.73, 0.82, -2.57, -1.73, -0.3, 0.18, 1.62, -0.67, 0.13]}',
    "Farma Sul fytd26 Jul-Abr (inclui Abril)"
)

# ──────────────────────────────────────────────────────────────────────────────
# 3. renderAvgInsight — Diagnóstico com período e tendência recente
# ──────────────────────────────────────────────────────────────────────────────
print("\n--- renderAvgInsight: adicionar rótulo de período + tendência recente ---")

old_insight = (
    "function renderAvgInsight(){\n"
    "  var el = document.getElementById('avg-insight');\n"
    "  if(!el) return;\n"
    "  var _avgSel = document.getElementById('avgMarketSel');\n"
    "  var mktLabel = (_avgSel && _avgSel.selectedIndex >= 0) ? _avgSel.options[_avgSel.selectedIndex].text : avgMarket;\n"
    "  var d = AVG_DATA[avgMarket] || AVG_DATA['farmasul'];\n"
    "  if(!d) return;\n"
    "  var diagLabel = mktLabel;\n"
    "  var produtos = Object.keys(d);\n"
    "  var lines = [];\n"
    "  produtos.forEach(function(p){\n"
    "    var vals = d[p].filter(Boolean);\n"
    "    if(!vals.length) return;\n"
    "    var first = vals[0], last = vals[vals.length-1];\n"
    "    var trend = Math.round((last-first)/first*100);\n"
    "    var col = trend>=0?'#34d399':'#ef4444';\n"
    "    lines.push('\\u2022 <strong style=\"color:#e2e8f0;\">'+p+'</strong>: R$'+first.toFixed(2)+' \\u2192 <strong style=\"color:'+col+';\">R$'+last.toFixed(2)+'</strong> <span style=\"color:'+col+';\">'"
    "+(trend>=0?'+':'')+trend+'%</span>');\n"
    "  });\n"
    "  var falling = produtos.filter(function(p){\n"
    "    var v=d[p].filter(Boolean); return v.length>1&&v[v.length-1]<v[0]*0.9;\n"
    "  }).length;\n"
    "  var summary = falling>1\n"
    "    ? '\\u26a0\\ufe0f <strong style=\"color:#06b6d4;\">'+falling+' produtos com pre\\xe7o em queda &gt;10%</strong> \\u2014 press\\xe3o promocional em <strong style=\"color:#e2e8f0;\">'+diagLabel+'</strong>.'\n"
    "    : '\\u2705 Pre\\xe7os m\\xe9dios relativamente est\\xe1veis em <strong style=\"color:#e2e8f0;\">'+diagLabel+'</strong>.';\n"
    "  el.innerHTML = '<strong style=\"color:#34d399;font-size:10px;letter-spacing:0.08em;\">\\ud83d\\udcca DIAGN\\u00d3STICO PRE\\u00c7O M\\u00c9DIO \\u00b7 '+diagLabel+'</strong><br>'+summary+'<br>'+lines.join('<br>');\n"
    "}"
)

new_insight = (
    "function renderAvgInsight(){\n"
    "  var el = document.getElementById('avg-insight');\n"
    "  if(!el) return;\n"
    "  var _avgSel = document.getElementById('avgMarketSel');\n"
    "  var mktLabel = (_avgSel && _avgSel.selectedIndex >= 0) ? _avgSel.options[_avgSel.selectedIndex].text : avgMarket;\n"
    "  var d = AVG_DATA[avgMarket] || AVG_DATA['farmasul'];\n"
    "  if(!d) return;\n"
    "  var diagLabel = mktLabel;\n"
    "  var meses = AVG_MESES || [];\n"
    "  var produtos = Object.keys(d);\n"
    "  var lines = [];\n"
    "  var recentFalling = 0;\n"
    "  produtos.forEach(function(p){\n"
    "    var vals = d[p].filter(Boolean);\n"
    "    if(!vals.length) return;\n"
    "    var first = vals[0], last = vals[vals.length-1];\n"
    "    var lblFirst = meses[0] || 'Jul/25';\n"
    "    var lblLast  = meses[vals.length-1] || 'Abr/26';\n"
    "    var trend = Math.round((last-first)/first*100);\n"
    "    /* Tendencia recente: ultimos 3 meses vs 3 anteriores */\n"
    "    var rLen = Math.min(3, Math.floor(vals.length/2));\n"
    "    var recAvg = vals.slice(-rLen).reduce(function(a,b){return a+b;},0)/rLen;\n"
    "    var priAvg = vals.slice(-rLen*2,-rLen).reduce(function(a,b){return a+b;},0)/rLen;\n"
    "    var recTrend = priAvg>0?Math.round((recAvg-priAvg)/priAvg*100):0;\n"
    "    if(recTrend<-5) recentFalling++;\n"
    "    var col  = trend>=0?'#34d399':'#ef4444';\n"
    "    var rCol = recTrend>0?'#34d399':recTrend<-5?'#ef4444':'#fbbf24';\n"
    "    var rArrow = recTrend>0?'\\u2191':recTrend<0?'\\u2193':'\\u2192';\n"
    "    lines.push('\\u2022 <strong style=\"color:#e2e8f0;\">'+p+'</strong>'"
    "+'<span style=\"color:#64748b;\"> '+lblFirst+':</span> R$'+first.toFixed(2)"
    "+' \\u2192 <span style=\"color:#64748b;\">'+lblLast+':</span> <strong style=\"color:'+col+';\">R$'+last.toFixed(2)+'</strong> <span style=\"color:'+col+';\">'"
    "+(trend>=0?'+':'')+trend+'%</span>'"
    "+'  <span style=\"color:'+rCol+';font-size:9px;\">recente: '+rArrow+(recTrend>=0?'+':'')+recTrend+'%</span>');\n"
    "  });\n"
    "  var summary = recentFalling>1\n"
    "    ? '\\u26a0\\ufe0f <strong style=\"color:#fbbf24;\">'+recentFalling+' produtos com tend\\u00eancia recente de queda</strong> em <strong style=\"color:#e2e8f0;\">'+diagLabel+'</strong>.'\n"
    "    : recentFalling===1\n"
    "    ? '\\u26a0\\ufe0f <strong style=\"color:#fbbf24;\">1 produto com tend\\u00eancia recente de queda</strong> em <strong style=\"color:#e2e8f0;\">'+diagLabel+'</strong>.'\n"
    "    : '\\u2705 Tend\\u00eancia recente est\\u00e1vel/alta em <strong style=\"color:#e2e8f0;\">'+diagLabel+'</strong>.';\n"
    "  el.innerHTML = '<strong style=\"color:#34d399;font-size:10px;letter-spacing:0.08em;\">\\ud83d\\udcca DIAGN\\u00d3STICO PRE\\u00c7O M\\u00c9DIO \\u00b7 '+diagLabel+'</strong>'"
    "+'<br><span style=\"color:#64748b;font-size:9px;\">Compara\\u00e7\\u00e3o: '+lblFirst+' (in\\u00edcio FY) \\u2192 '+lblLast+' (atual) | Recente = \\u00falt 3 meses vs 3 ant.</span>'"
    "+'<br>'+summary+'<br>'+lines.join('<br>');\n"
    "}"
)

patch(old_insight, new_insight, "renderAvgInsight: rótulo de período + tendência recente")

# ──────────────────────────────────────────────────────────────────────────────
# RESUMO
# ──────────────────────────────────────────────────────────────────────────────
print(f"\n=== RESUMO ===")
print(f"Patches: {patches}")
print(f"Original: {original_len:,} | Final: {len(html):,} | Diff: {len(html)-original_len:+,}")

with open(SRC, 'w', encoding='utf-8') as f:
    f.write(html)
print(f"\nSalvo: {SRC}")

ts = datetime.datetime.now().strftime('%Y%m%d_%H%M')
VER = os.path.join(BASE, "versoes", f"Dashboard_Farma_Sul_{ts}_SKUFytdAvgDiag.html")
shutil.copy2(SRC, VER)
print(f"Versao: {VER}")
