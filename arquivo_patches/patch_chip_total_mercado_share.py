"""
patch_chip_total_mercado_share.py
Corrige o chip SCJ COMBINED no bloco isShare do renderMSO2
(modo Share ativo — que é o default do card Market Share Jan-Mar).
"""
import sys, shutil
sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path
from datetime import datetime

DASH = Path(r'C:\Users\valqu\OneDrive\Documentos\Claude\Projects\projeto Dashboard_farma_sul\Dashboard_farma_sul\Dashboard_Farma_Sul_20260512_2220.html')
VER  = DASH.parent / 'versoes'
DL   = Path.home() / 'Downloads'
ts   = datetime.now().strftime('%Y%m%d_%H%M')
shutil.copy(DASH, VER / f'Dashboard_Farma_Sul_{ts}_PreShareChip.html')
print(f'Backup: Dashboard_Farma_Sul_{ts}_PreShareChip.html')

h = DASH.read_text(encoding='utf-8')

# ── Substituir: adicionar cálculo de mercado + trocar chip no bloco isShare ───
OLD = (
    " topG = deltasKpi[0], topL = deltasKpi[deltasKpi.length-1];\n"
    "      hdEl.innerHTML = '<div style=\"display:grid;grid-template-columns:repeat(4,1fr);gap:1px;background:rgba(255,255,255,0.06);\">'\n"
    "        +kpiChip('#fbbf24','SCJ COMBINED',scj26h.toFixed(1)+'%','color:#fbbf24',(scjDh>=0?'↑ +':'↓ ')+Math.abs(scjDh).toFixed(1)+'pp vs Mar/25','color:'+(scjDh>=0?'#34d399':'#ef4444'))"
)

NEW = (
    " topG = deltasKpi[0], topL = deltasKpi[deltasKpi.length-1];\n"
    "      /* TOTAL MERCADO chip — Share mode */\n"
    "      var fytMktShare=(typeof FYTD_MARKET_TOTAL!=='undefined')?FYTD_MARKET_TOTAL[mkt]:null;\n"
    "      var mktS26=fytMktShare?fytMktShare.janmar26_val:0;\n"
    "      var mktS25=fytMktShare?fytMktShare.janmar25_val:0;\n"
    "      var mktDeltaS=mktS25>0?Math.round((mktS26-mktS25)/mktS25*1000)/10:0;\n"
    "      var mktDeltaStrS=(mktDeltaS>=0?'+':'')+mktDeltaS.toFixed(1)+'% vs /25';\n"
    "      var mktDeltaCorS=mktDeltaS>=0?'#34d399':'#ef4444';\n"
    "      var mktValStrS=mktS26>0?'R$'+mktS26.toFixed(2)+'MM':'—';\n"
    "      hdEl.innerHTML = '<div style=\"display:grid;grid-template-columns:repeat(4,1fr);gap:1px;background:rgba(255,255,255,0.06);\">'\n"
    "        +kpiChip('#fbbf24','TOTAL MERCADO',mktValStrS,'color:#fbbf24',mktDeltaStrS,'color:'+mktDeltaCorS)"
)

assert OLD in h, 'ERRO: bloco isShare SCJ COMBINED nao encontrado'
h = h.replace(OLD, NEW, 1)
print('OK: chip TOTAL MERCADO aplicado no bloco isShare')

DASH.write_text(h, encoding='utf-8')
shutil.copy(DASH, VER / f'Dashboard_Farma_Sul_{ts}_ShareChip.html')
shutil.copy(DASH, DL  / f'Dashboard_FarmaSul_Giovano_{ts}.html')
print(f'\nVersao:    Dashboard_Farma_Sul_{ts}_ShareChip.html')
print(f'Downloads: Dashboard_FarmaSul_Giovano_{ts}.html')
print('DONE.')
