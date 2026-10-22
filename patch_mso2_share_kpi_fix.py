"""
patch_mso2_share_kpi_fix.py
Corrige divergencia nos chips do modo Share no MSO2:
  - ANTES: chips usavam acum=(Jan+Fev+Mar)/3 (media), tooltip mostrava Mar/26
  - DEPOIS: chips usam Mar/26 (mes mais recente), consistente com o grafico
  - SCJ COMBINED, LIDER DE SHARE, MAIOR GANHO, MAIOR QUEDA -> todos Mar/26
"""
import shutil
from datetime import datetime

SRC      = r"C:\Users\valqu\OneDrive\Documentos\Claude\Projects\projeto Dashboard_farma_sul\Dashboard_farma_sul\Dashboard_Farma_Sul_20260512_2220.html"
VERS_DIR = r"C:\Users\valqu\OneDrive\Documentos\Claude\Projects\projeto Dashboard_farma_sul\Dashboard_farma_sul\versoes"
DL_DIR   = r"C:\Users\valqu\Downloads"

ts   = datetime.now().strftime('%Y%m%d_%H%M')
VERS = fr"{VERS_DIR}\Dashboard_Farma_Sul_{ts}_MSO2ShareKpiFix.html"
DL   = fr"{DL_DIR}\Dashboard_FarmaSul_Giovano_{ts}.html"

with open(SRC, 'r', encoding='utf-8') as f:
    html = f.read()

# Substituir: acum -> mar para todos os calculos dos chips Share
# SCJ COMBINED: off26a/exp26a/off25a/exp25a usam .acum -> .mar
# leaderB: d26[b].acum -> d26[b].mar
# deltasKpi: acum-acum -> mar-mar
# chip LIDER: d26[leaderB].acum -> d26[leaderB].mar

OLD = (
    "var off26a = d26['OFF!']?d26['OFF!'].acum:0, exp26a = d26['EXPOSIS']?d26['EXPOSIS'].acum:0;\n"
    "      var off25a = d25['OFF!']?d25['OFF!'].acum:0, exp25a = d25['EXPOSIS']?d25['EXPOSIS'].acum:0;\n"
    "      var scj26h = Math.round((off26a+exp26a)*10)/10, scj25h = Math.round((off25a+exp25a)*10)/10;\n"
    "      var scjDh = Math.round((scj26h-scj25h)*10)/10;\n"
    "      var leaderB = brands.reduce(function(best,b){ return (d26[b]&&(!d26[best]||d26[b].acum>d26[best].acum))?b:best; }, brands[0]);\n"
    "      var deltasKpi = brands.map(function(b){ return {b:b,raw:d26[b]&&d25[b]?Math.round((d26[b].acum-d25[b].acum)*100)/100:0}; });\n"
    "      deltasKpi.sort(function(a,b){return b.raw-a.raw;});\n"
    "      var topG = deltasKpi[0], topL = deltasKpi[deltasKpi.length-1];\n"
    "      hdEl.innerHTML = '<div style=\"display:grid;grid-template-columns:repeat(4,1fr);gap:1px;background:rgba(255,255,255,0.06);\">'\n"
    "        +kpiChip('#fbbf24','SCJ COMBINED',scj26h+'%','color:#fbbf24',(scjDh>=0?'↑ +':'↓ ')+Math.abs(scjDh).toFixed(1)+'pp vs /25','color:'+(scjDh>=0?'#34d399':'#ef4444'))\n"
    "        +kpiChip(colors[leaderB]||'#e2e8f0','LÍDER DE SHARE',d26[leaderB]?d26[leaderB].acum.toFixed(2)+'%':'—','color:'+(colors[leaderB]||'#e2e8f0'),leaderB,'color:#94A3B8')"
)

NEW = (
    "/* Chips Share: usa Mar/26 (mes mais recente) — consistente com tooltip do grafico */\n"
    "      var off26a = d26['OFF!']?d26['OFF!'].mar:0, exp26a = d26['EXPOSIS']?d26['EXPOSIS'].mar:0;\n"
    "      var off25a = d25['OFF!']?d25['OFF!'].mar:0, exp25a = d25['EXPOSIS']?d25['EXPOSIS'].mar:0;\n"
    "      var scj26h = Math.round((off26a+exp26a)*10)/10, scj25h = Math.round((off25a+exp25a)*10)/10;\n"
    "      var scjDh = Math.round((scj26h-scj25h)*10)/10;\n"
    "      var leaderB = brands.reduce(function(best,b){ return (d26[b]&&(!d26[best]||d26[b].mar>d26[best].mar))?b:best; }, brands[0]);\n"
    "      var deltasKpi = brands.map(function(b){ return {b:b,raw:d26[b]&&d25[b]?Math.round((d26[b].mar-d25[b].mar)*100)/100:0}; });\n"
    "      deltasKpi.sort(function(a,b){return b.raw-a.raw;});\n"
    "      var topG = deltasKpi[0], topL = deltasKpi[deltasKpi.length-1];\n"
    "      hdEl.innerHTML = '<div style=\"display:grid;grid-template-columns:repeat(4,1fr);gap:1px;background:rgba(255,255,255,0.06);\">'\n"
    "        +kpiChip('#fbbf24','SCJ COMBINED',scj26h.toFixed(1)+'%','color:#fbbf24',(scjDh>=0?'↑ +':'↓ ')+Math.abs(scjDh).toFixed(1)+'pp vs Mar/25','color:'+(scjDh>=0?'#34d399':'#ef4444'))\n"
    "        +kpiChip(colors[leaderB]||'#e2e8f0','LÍDER DE SHARE',d26[leaderB]?d26[leaderB].mar.toFixed(2)+'%':'—','color:'+(colors[leaderB]||'#e2e8f0'),leaderB+' · Mar/26','color:#94A3B8')"
)

if OLD in html:
    html = html.replace(OLD, NEW, 1)
    print('OK  MSO2 Share KPI chips: acum -> Mar/26 (LIDER, MAIOR GANHO, MAIOR QUEDA, SCJ COMBINED)')
else:
    print('MISS  bloco nao encontrado')

with open(SRC, 'w', encoding='utf-8') as f:
    f.write(html)
shutil.copy2(SRC, VERS)
shutil.copy2(SRC, DL)

print(f'\n  Versao: {VERS.split(chr(92))[-1]}')
print(f'  DL:     {DL.split(chr(92))[-1]}')
