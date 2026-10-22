"""
patch_mso3_scj_combined.py
Adiciona chip SCJ COMBINED (share % SCJ no mercado total) como 1o chip do MSO3.
Grid muda de repeat(4,1fr) para repeat(5,1fr).
"""
import shutil
from datetime import datetime

SRC      = r"C:\Users\valqu\OneDrive\Documentos\Claude\Projects\projeto Dashboard_farma_sul\Dashboard_farma_sul\Dashboard_Farma_Sul_20260512_2220.html"
VERS_DIR = r"C:\Users\valqu\OneDrive\Documentos\Claude\Projects\projeto Dashboard_farma_sul\Dashboard_farma_sul\versoes"
DL_DIR   = r"C:\Users\valqu\Downloads"

ts   = datetime.now().strftime('%Y%m%d_%H%M')
VERS = fr"{VERS_DIR}\Dashboard_Farma_Sul_{ts}_MSO3ScjCombined.html"
DL   = fr"{DL_DIR}\Dashboard_FarmaSul_Giovano_{ts}.html"

with open(SRC, 'r', encoding='utf-8') as f:
    html = f.read()

# ─── Substituição dos KPI chips do MSO3 ──────────────────────────────────────
OLD = """  if(hdEl){
    hdEl.innerHTML='<div style="display:grid;grid-template-columns:repeat(4,1fr);border-bottom:0.5px solid rgba(255,255,255,0.06);">'
      +kpiChip3('#22c55e','TOTAL ACUM',fmtV3(totV26),'color:#f1f5f9',totalDt.str+' vs /25','color:'+totalDt.col)
      +kpiChip3(colors[topB]||'#e2e8f0','MAIOR VOLUME',fmtV3(d26[topB]||0),'color:'+(colors[topB]||'#e2e8f0'),topB,'color:#94A3B8')
      +(topG3?kpiChip3(topG3.d.raw>=0?'#34d399':'#f59e0b',topG3.d.raw>=0?'MAIOR CRESCIM.':'MENOR QUEDA',topG3.d.str,'color:'+(topG3.d.raw>=0?'#34d399':'#f59e0b'),topG3.b,'color:#94A3B8'):'')
      +(topL3?kpiChip3('#ef4444','MAIOR QUEDA',topL3.d.str,'color:#ef4444',topL3.b,'color:#94A3B8'):'')
      +'</div>';
  }"""

NEW = """  /* SCJ COMBINED share no mercado total */
  var mt26h = mt ? (isVal ? mt.fytd26_val : mt.fytd26_un) : 0;
  var mt25h = mt ? (isVal ? mt.fytd25_val : mt.fytd25_un) : 0;
  var scjShr26 = mt26h > 0 ? Math.round(totV26 / mt26h * 1000) / 10 : 0;
  var scjShr25 = mt25h > 0 ? Math.round(totV25 / mt25h * 1000) / 10 : 0;
  var scjShrDt = Math.round((scjShr26 - scjShr25) * 10) / 10;
  var scjShrCor = scjShrDt >= 0 ? '#34d399' : '#ef4444';
  var scjShrSub = (scjShrDt >= 0 ? '+' : '') + scjShrDt.toFixed(1) + 'pp vs /25';

  if(hdEl){
    hdEl.innerHTML='<div style="display:grid;grid-template-columns:repeat(5,1fr);border-bottom:0.5px solid rgba(255,255,255,0.06);">'
      +kpiChip3('#fbbf24','SCJ COMBINED',scjShr26.toFixed(1)+'%','color:#fbbf24',scjShrSub,'color:'+scjShrCor)
      +kpiChip3('#22c55e','TOTAL ACUM',fmtV3(totV26),'color:#f1f5f9',totalDt.str+' vs /25','color:'+totalDt.col)
      +kpiChip3(colors[topB]||'#e2e8f0','MAIOR VOLUME',fmtV3(d26[topB]||0),'color:'+(colors[topB]||'#e2e8f0'),topB,'color:#94A3B8')
      +(topG3?kpiChip3(topG3.d.raw>=0?'#34d399':'#f59e0b',topG3.d.raw>=0?'MAIOR CRESCIM.':'MENOR QUEDA',topG3.d.str,'color:'+(topG3.d.raw>=0?'#34d399':'#f59e0b'),topG3.b,'color:#94A3B8'):'')
      +(topL3?kpiChip3('#ef4444','MAIOR QUEDA',topL3.d.str,'color:#ef4444',topL3.b,'color:#94A3B8'):'')
      +'</div>';
  }"""

if OLD in html:
    html = html.replace(OLD, NEW, 1)
    print("OK  SCJ COMBINED adicionado ao MSO3")
else:
    print("MISS  bloco nao encontrado")

with open(SRC, 'w', encoding='utf-8') as f:
    f.write(html)
shutil.copy2(SRC, VERS)
shutil.copy2(SRC, DL)

print(f"\n  Versao: {VERS.split(chr(92))[-1]}")
print(f"  DL:     {DL.split(chr(92))[-1]}")
