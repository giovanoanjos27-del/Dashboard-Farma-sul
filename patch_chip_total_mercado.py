"""
patch_chip_total_mercado.py
Substitui o chip "SCJ COMBINED" (share %) pelo chip "TOTAL MERCADO"
mostrando o valor absoluto FYTD/26 (R$ MM ou unidades) e % de crescimento/queda vs /25.
Afeta apenas o card VENDA VALOR FYTD · JUL-MAR (renderMSO3).
"""
import sys, shutil
sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path
from datetime import datetime

DASH = Path(r'C:\Users\valqu\OneDrive\Documentos\Claude\Projects\projeto Dashboard_farma_sul\Dashboard_farma_sul\Dashboard_Farma_Sul_20260512_2220.html')
VER  = DASH.parent / 'versoes'
DL   = Path.home() / 'Downloads'
ts   = datetime.now().strftime('%Y%m%d_%H%M')
shutil.copy(DASH, VER / f'Dashboard_Farma_Sul_{ts}_PreChipMktTotal.html')
print(f'Backup: Dashboard_Farma_Sul_{ts}_PreChipMktTotal.html')

h = DASH.read_text(encoding='utf-8')

# ── 1. Adicionar cálculo do delta de mercado antes do bloco HB ────────────────
OLD_CALC = (
    "  var scjShrDt = Math.round((scjShr26 - scjShr25) * 10) / 10;\n"
    "  var scjShrCor = scjShrDt >= 0 ? '#34d399' : '#ef4444';\n"
    "  var scjShrSub = (scjShrDt >= 0 ? '+' : '') + scjShrDt.toFixed(1) + 'pp vs /25';\n"
    "  /* HB OFF!+EXPOSIS para chip do cabecalho */"
)

NEW_CALC = (
    "  var scjShrDt = Math.round((scjShr26 - scjShr25) * 10) / 10;\n"
    "  var scjShrCor = scjShrDt >= 0 ? '#34d399' : '#ef4444';\n"
    "  var scjShrSub = (scjShrDt >= 0 ? '+' : '') + scjShrDt.toFixed(1) + 'pp vs /25';\n"
    "  /* TOTAL MERCADO para chip do cabecalho */\n"
    "  var mktDelta3 = mt25h > 0 ? Math.round((mt26h - mt25h) / mt25h * 1000) / 10 : 0;\n"
    "  var mktDeltaStr3 = (mktDelta3 >= 0 ? '+' : '') + mktDelta3.toFixed(1) + '% vs /25';\n"
    "  var mktDeltaCor3 = mktDelta3 >= 0 ? '#34d399' : '#ef4444';\n"
    "  var mktValStr3 = mt26h > 0 ? (isVal ? 'R$'+mt26h.toFixed(2)+'MM' : (mt26h>=1000?(Math.round(mt26h/10)/100)+'M un':Math.round(mt26h)+'K un')) : '—';\n"
    "  /* HB OFF!+EXPOSIS para chip do cabecalho */"
)

assert OLD_CALC in h, 'ERRO: bloco de cálculo scjShrDt não encontrado'
h = h.replace(OLD_CALC, NEW_CALC, 1)
print('OK: cálculo mktDelta3 adicionado')

# ── 2. Substituir o chip SCJ COMBINED pelo chip TOTAL MERCADO ─────────────────
OLD_CHIP = (
    "+kpiChip3('#fbbf24','SCJ COMBINED',scjShr26.toFixed(1)+'%',"
    "'color:#fbbf24',scjShrSub,'color:'+scjShrCor)"
)

NEW_CHIP = (
    "+kpiChip3('#fbbf24','TOTAL MERCADO',mktValStr3,"
    "'color:#fbbf24',mktDeltaStr3,'color:'+mktDeltaCor3)"
)

assert OLD_CHIP in h, 'ERRO: chip SCJ COMBINED não encontrado'
h = h.replace(OLD_CHIP, NEW_CHIP, 1)
print('OK: chip TOTAL MERCADO substituído')

# ── 3. Salvar ─────────────────────────────────────────────────────────────────
DASH.write_text(h, encoding='utf-8')
shutil.copy(DASH, VER / f'Dashboard_Farma_Sul_{ts}_ChipMktTotal.html')
shutil.copy(DASH, DL  / f'Dashboard_FarmaSul_Giovano_{ts}.html')
print(f'\nVersao:    Dashboard_Farma_Sul_{ts}_ChipMktTotal.html')
print(f'Downloads: Dashboard_FarmaSul_Giovano_{ts}.html')
print('DONE.')
