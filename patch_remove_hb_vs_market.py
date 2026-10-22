"""
patch_remove_hb_vs_market.py
Remove a linha "HB superou/ficou abaixo/acompanhou o mercado — HB X% vs Mercado Y%"
do bloco HB no Diagnostico de AMBOS os cards:
  - MSO2 (JAN-MAR): renderMSO2Insight
  - MSO3 (FYTD): renderMSO3 diagnostico
"""
import shutil
from datetime import datetime

SRC      = r"C:\Users\valqu\OneDrive\Documentos\Claude\Projects\projeto Dashboard_farma_sul\Dashboard_farma_sul\Dashboard_Farma_Sul_20260512_2220.html"
VERS_DIR = r"C:\Users\valqu\OneDrive\Documentos\Claude\Projects\projeto Dashboard_farma_sul\Dashboard_farma_sul\versoes"
DL_DIR   = r"C:\Users\valqu\Downloads"

ts   = datetime.now().strftime('%Y%m%d_%H%M')
VERS = fr"{VERS_DIR}\Dashboard_Farma_Sul_{ts}_RemoveHbVsMarket.html"
DL   = fr"{DL_DIR}\Dashboard_FarmaSul_Giovano_{ts}.html"

with open(SRC, 'r', encoding='utf-8') as f:
    html = f.read()

ok = []

# ── MSO2: remover linha HB vs Mercado ────────────────────────────────────────
OLD_MSO2 = (
    "+'<div style=\"font-size:10px;color:'+vsHbICor+';padding:4px 8px;background:'+vsHbICor+'0d;border-radius:5px;display:inline-block;\">'\n"
    "        +'&#128269; '+vsHbILabel+' &mdash; HB '+(hbIDelta>=0?'+':'')+hbIDelta.toFixed(1)+'% vs Mercado '+(mtIDelta>=0?'+':'')+mtIDelta.toFixed(1)+'%'\n"
    "        +(vsHbI!==0?' &nbsp;(&#916; '+(vsHbI>=0?'+':'')+vsHbI.toFixed(1)+'pp)':'')\n"
    "      +'</div>'\n"
    "    +'</div>'\n"
    "    "
)
NEW_MSO2 = (
    "    +'</div>'\n"
    "    "
)
if OLD_MSO2 in html:
    html = html.replace(OLD_MSO2, NEW_MSO2, 1)
    ok.append('MSO2: linha HB vs Mercado removida')
else:
    ok.append('MISS MSO2 HB vs Mercado line')

# ── MSO3: remover linha HB vs Mercado ────────────────────────────────────────
OLD_MSO3 = (
    "+'<div style=\"font-size:10px;color:'+vsHbCor+';padding:4px 8px;background:'+vsHbCor+'0d;border-radius:5px;display:inline-block;\">'\n"
    "          +'&#128269; '+vsHbLabel+' &mdash; HB '+(hbDeltaD>=0?'+':'')+hbDeltaD.toFixed(1)+'% vs Mercado '+(mtDelta>=0?'+':'')+mtDelta.toFixed(1)+'%'\n"
    "          +(vsHb!==0?' &nbsp;(&#916; '+(vsHb>=0?'+':'')+vsHb.toFixed(1)+'pp)':'')\n"
    "        +'</div>'\n"
    "      +'</div>'\n"
    "    "
)
NEW_MSO3 = (
    "      +'</div>'\n"
    "    "
)
if OLD_MSO3 in html:
    html = html.replace(OLD_MSO3, NEW_MSO3, 1)
    ok.append('MSO3: linha HB vs Mercado removida')
else:
    ok.append('MISS MSO3 HB vs Mercado line')

with open(SRC, 'w', encoding='utf-8') as f:
    f.write(html)
shutil.copy2(SRC, VERS)
shutil.copy2(SRC, DL)

print()
print('=' * 52)
for c in ok: print(f'  {"OK" if not c.startswith("MISS") else "!!"} {c}')
print(f'\n  Versao: {VERS.split(chr(92))[-1]}')
print(f'  DL:     {DL.split(chr(92))[-1]}')
print('=' * 52)
