"""
patch_chip_total_mercado_mso2.py
Substitui o chip "SCJ COMBINED" no card MARKET SHARE — JAN·FEV·MAR (renderMSO2)
pelo chip "TOTAL MERCADO" mostrando o valor acumulado Jan-Mar/26 em R$ MM e % de variação vs /25.
"""
import sys, shutil
sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path
from datetime import datetime

DASH = Path(r'C:\Users\valqu\OneDrive\Documentos\Claude\Projects\projeto Dashboard_farma_sul\Dashboard_farma_sul\Dashboard_Farma_Sul_20260512_2220.html')
VER  = DASH.parent / 'versoes'
DL   = Path.home() / 'Downloads'
ts   = datetime.now().strftime('%Y%m%d_%H%M')
shutil.copy(DASH, VER / f'Dashboard_Farma_Sul_{ts}_PreChipMktTotal2.html')
print(f'Backup: Dashboard_Farma_Sul_{ts}_PreChipMktTotal2.html')

h = DASH.read_text(encoding='utf-8')

# ── 1. Adicionar cálculo do total de mercado Jan-Mar antes do bloco HB ────────
OLD_CALC = (
    "      var scjShrSubk=(scjShrDtk>=0?'+':'')+scjShrDtk.toFixed(1)+'pp vs /25';\n"
    "      /* HB OFF!+EXPOSIS para chip Jan-Mar */"
)

NEW_CALC = (
    "      var scjShrSubk=(scjShrDtk>=0?'+':'')+scjShrDtk.toFixed(1)+'pp vs /25';\n"
    "      /* TOTAL MERCADO para chip Jan-Mar — sempre R$ MM */\n"
    "      var mktTot26kV=fytMktH2?fytMktH2.janmar26_val:0;\n"
    "      var mktTot25kV=fytMktH2?fytMktH2.janmar25_val:0;\n"
    "      var mktDeltaK=mktTot25kV>0?Math.round((mktTot26kV-mktTot25kV)/mktTot25kV*1000)/10:0;\n"
    "      var mktDeltaStrK=(mktDeltaK>=0?'+':'')+mktDeltaK.toFixed(1)+'% vs /25';\n"
    "      var mktDeltaCorK=mktDeltaK>=0?'#34d399':'#ef4444';\n"
    "      var mktValStrK=mktTot26kV>0?'R$'+mktTot26kV.toFixed(2)+'MM':'—';\n"
    "      /* HB OFF!+EXPOSIS para chip Jan-Mar */"
)

assert OLD_CALC in h, 'ERRO: bloco scjShrSubk (MSO2) não encontrado'
h = h.replace(OLD_CALC, NEW_CALC, 1)
print('OK: cálculo mktDeltaK adicionado')

# ── 2. Substituir chip SCJ COMBINED pelo chip TOTAL MERCADO ──────────────────
OLD_CHIP = (
    "        +kpiChip('#fbbf24','SCJ COMBINED',scjShr2k.toFixed(1)+'%',"
    "'color:#fbbf24',scjShrSubk,'color:'+scjShrCork)"
)

NEW_CHIP = (
    "        +kpiChip('#fbbf24','TOTAL MERCADO',mktValStrK,"
    "'color:#fbbf24',mktDeltaStrK,'color:'+mktDeltaCorK)"
)

assert OLD_CHIP in h, 'ERRO: chip SCJ COMBINED (MSO2) não encontrado'
h = h.replace(OLD_CHIP, NEW_CHIP, 1)
print('OK: chip TOTAL MERCADO substituído')

# ── 3. Salvar ─────────────────────────────────────────────────────────────────
DASH.write_text(h, encoding='utf-8')
shutil.copy(DASH, VER / f'Dashboard_Farma_Sul_{ts}_ChipMktTotal2.html')
shutil.copy(DASH, DL  / f'Dashboard_FarmaSul_Giovano_{ts}.html')
print(f'\nVersao:    Dashboard_Farma_Sul_{ts}_ChipMktTotal2.html')
print(f'Downloads: Dashboard_FarmaSul_Giovano_{ts}.html')
print('DONE.')
