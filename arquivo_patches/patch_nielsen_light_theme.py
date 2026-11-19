"""
patch_nielsen_light_theme.py
Troca o tema do Excel de dark (fundo preto) para light (fundo branco).

Mudanças:
  • C.dark  0D1117 → FFFFFF  (fundo padrão: branco)
  • C.hdr   161B22 → D9E1F2  (cabeçalhos: azul-cinza claro)
  • C.card  1A2332 → F0F4FF  (linhas destaque: azul muito claro)
  • C.gold  FBBF24 → B45309  (dourado escuro — legível em branco)
  • C.white E2E8F0 → 1E293B  (texto padrão: quase-preto)
  • C.gray  94A3B8 → 64748B  (texto secundário)
  • C.dim   64748B → 94A3B8  (texto terciário)
  • C.teal  22D3EE → 0E7490  (teal escuro)
  • C.green 34D399 → 166534  (verde escuro)
  • C.red   EF4444 → B91C1C  (vermelho escuro)
  • C.amber F59E0B → B45309  (âmbar escuro)
  • C.blue  60A5FA → 1D4ED8  (azul escuro)
  • C.orange F97316→ C2410C  (laranja escuro)
  BRAND_COL — tons mais escuros para fundo claro
  Hard-coded FF0D1117 / FF161B22 / FF1A2332 → substituídos
"""
import sys
from pathlib import Path
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

BASE = Path(r'C:\Users\valqu\OneDrive\Documentos\Claude\Projects\projeto Dashboard_farma_sul\Dashboard_farma_sul')
SRC  = BASE / 'Dashboard_Farma_Sul_20260512_2220.html'
VER  = BASE / 'versoes' / f'Dashboard_Farma_Sul_{datetime.now().strftime("%Y%m%d_%H%M")}_NielsenLightTheme.html'

print('Lendo dashboard…')
h = SRC.read_text(encoding='utf-8')
orig_len = len(h)

# ── Delimitar o bloco do export para não tocar no resto do dashboard ──
BLOCK_START = '/* ═══════════ NIELSEN EXCEL EXPORT ═══════════ */'
BLOCK_END   = '})();\n</script>'

idx_s = h.find(BLOCK_START)
idx_e = h.find(BLOCK_END, idx_s) + len(BLOCK_END)
assert idx_s != -1, '❌ NIELSEN EXCEL EXPORT block não encontrado'
assert idx_e != -1, '❌ Fim do bloco não encontrado'

before = h[:idx_s]
block  = h[idx_s:idx_e]
after  = h[idx_e:]
print(f'Bloco de export: {len(block):,} bytes')

# ─────────────────────────────────────────────────────────────────────────────
# 1. Paleta de cores C
# ─────────────────────────────────────────────────────────────────────────────
OLD_C = """var C = { dark:'0D1117', hdr:'161B22', card:'1A2332',
          gold:'FBBF24', white:'E2E8F0', gray:'94A3B8', dim:'64748B',
          teal:'22D3EE', green:'34D399', red:'EF4444', amber:'F59E0B',
          blue:'60A5FA', orange:'F97316' };"""

NEW_C = """var C = { dark:'FFFFFF', hdr:'D9E1F2', card:'EEF2FF',
          gold:'B45309', white:'1E293B', gray:'64748B', dim:'94A3B8',
          teal:'0E7490', green:'166534', red:'B91C1C', amber:'B45309',
          blue:'1D4ED8', orange:'C2410C' };"""

assert block.count(OLD_C) == 1, f'C palette: {block.count(OLD_C)} ocorrências'
block = block.replace(OLD_C, NEW_C)
print('✅ Paleta C → light theme')

# ─────────────────────────────────────────────────────────────────────────────
# 2. BRAND_COL — tons escuros para fundo claro
# ─────────────────────────────────────────────────────────────────────────────
OLD_BC = """var BRAND_COL = {'OFF!':'FBBF24','EXPOSIS':'3B82F6','XO INSETO':'EF4444',
                 'SUPER REPELEX':'F97316','SBP':'06B6D4'};"""

NEW_BC = """var BRAND_COL = {'OFF!':'B45309','EXPOSIS':'1D4ED8','XO INSETO':'B91C1C',
                 'SUPER REPELEX':'C2410C','SBP':'0E7490'};"""

assert block.count(OLD_BC) == 1, f'BRAND_COL: {block.count(OLD_BC)} ocorrências'
block = block.replace(OLD_BC, NEW_BC)
print('✅ BRAND_COL → tons escuros')

# ─────────────────────────────────────────────────────────────────────────────
# 3. Hard-coded argb dark colors → light equivalents
# ─────────────────────────────────────────────────────────────────────────────
replacements = [
    # fundo preto → branco
    ("argb:'FF0D1117'",   "argb:'FFFFFFFF'"),
    # header escuro → azul-cinza claro
    ("argb:'FF161B22'",   "argb:'FFD9E1F2'"),
    # card escuro → azul muito claro
    ("argb:'FF1A2332'",   "argb:'FFEEF2FF'"),
    # dourado brilhante (font) → dourado escuro
    ("argb:'FFFBBF24'",   "argb:'FFB45309'"),
    # teal claro (font) → teal escuro
    ("argb:'FF22D3EE'",   "argb:'FF0E7490'"),
    # verde claro (font) → verde escuro
    ("argb:'FF34D399'",   "argb:'FF166534'"),
    # azul claro (font) → azul escuro
    ("argb:'FF60A5FA'",   "argb:'FF1D4ED8'"),
    # laranja claro (font) → laranja escuro
    ("argb:'FFF97316'",   "argb:'FFC2410C'"),
    # âmbar claro (font) → âmbar escuro
    ("argb:'FFF59E0B'",   "argb:'FFB45309'"),
    # vermelho claro (font) → vermelho escuro
    ("argb:'FFEF4444'",   "argb:'FFB91C1C'"),
    # texto claro E2E8F0 → texto escuro
    ("argb:'FFE2E8F0'",   "argb:'FF1E293B'"),
    # cinza médio 94A3B8 como texto → manter mas escurecer
    ("argb:'FF94A3B8'",   "argb:'FF64748B'"),
    # cinza escuro 64748B → cinza mais claro (ok em fundo branco)
    ("argb:'FF64748B'",   "argb:'FF94A3B8'"),
    # borda escura 2D3748 → cinza claro
    ("argb:'FF2D3748'",   "argb:'FFCBD5E1'"),
    # sheetTabela1: header fill azul escuro 1F3864 → manter (já é escuro, fica bem)
    # sheetTabela1: fonte azul escuro 1F3864 → manter
    # fundo branco já está correto na 1-Tabela-1
]

for old, new in replacements:
    cnt = block.count(old)
    if cnt > 0:
        block = block.replace(old, new)
        print(f'  {old} → {new}  ({cnt}×)')

print('✅ Hard-coded argb substituídos')

# ─────────────────────────────────────────────────────────────────────────────
# 4. Border color de 'thin' border → cinza claro
# ─────────────────────────────────────────────────────────────────────────────
OLD_BORDER = "var br={style:'thin',color:{argb:'FF2D3748'}};"
NEW_BORDER = "var br={style:'thin',color:{argb:'FFCBD5E1'}};"
# já foi substituído acima via argb replacements; mas garantir o objeto br:
if OLD_BORDER in block:
    block = block.replace(OLD_BORDER, NEW_BORDER)
    print('✅ Border color atualizado')

# ─────────────────────────────────────────────────────────────────────────────
# 5. Barra dourada na Capa (row 4) → cor de acento azul
#    Era: fgColor:{argb:'FFFBBF24'} — já tratado acima
#    Toast: background dark → light
# ─────────────────────────────────────────────────────────────────────────────
OLD_TOAST_INFO = "['rgba(21,28,43,0.98)','rgba(251,191,36,0.4)' ,'#fbbf24'],"
NEW_TOAST_INFO = "['rgba(255,251,235,0.98)','rgba(180,83,9,0.4)' ,'#B45309'],"
OLD_TOAST_OK   = "['rgba(10,32,22,0.98)','rgba(52,211,153,0.45)','#34d399'],"
NEW_TOAST_OK   = "['rgba(240,253,244,0.98)','rgba(22,101,52,0.45)','#166534'],"
OLD_TOAST_ERR  = "['rgba(32,10,10,0.98)','rgba(239,68,68,0.45)' ,'#f87171']"
NEW_TOAST_ERR  = "['rgba(255,241,242,0.98)','rgba(185,28,28,0.45)','#B91C1C']"

for old, new in [(OLD_TOAST_INFO,NEW_TOAST_INFO),(OLD_TOAST_OK,NEW_TOAST_OK),(OLD_TOAST_ERR,NEW_TOAST_ERR)]:
    if block.count(old) == 1:
        block = block.replace(old, new)
        print(f'✅ Toast style atualizado')

# ─────────────────────────────────────────────────────────────────────────────
# 6. Botão — borda e cor do botão manter dourado escuro
#    (já vive no browser, não no Excel — sem mudança necessária)
# ─────────────────────────────────────────────────────────────────────────────

# ─────────────────────────────────────────────────────────────────────────────
# Verificações
# ─────────────────────────────────────────────────────────────────────────────
assert "'FFFFFF'" in block,   '❌ C.dark branco não encontrado'
assert "'D9E1F2'" in block,   '❌ C.hdr claro não encontrado'
assert "'B45309'" in block,   '❌ C.gold escuro não encontrado'
assert "'1E293B'" in block,   '❌ C.white texto escuro não encontrado'
assert '0D1117' not in block, '❌ cor preta 0D1117 ainda presente'
assert '161B22' not in block, '❌ cor preta 161B22 ainda presente'
assert '1A2332' not in block, '❌ cor preta 1A2332 ainda presente'
print('✅ Verificações OK — sem cores pretas residuais')

h = before + block + after
print(f'\nTamanho original: {orig_len:,} | Novo: {len(h):,} | Δ: {len(h)-orig_len:+,}')

VER.parent.mkdir(parents=True, exist_ok=True)
VER.write_text(h, encoding='utf-8')
print(f'✅ Versão salva: {VER.name}')
SRC.write_text(h, encoding='utf-8')
print(f'✅ Base ativa atualizada: {SRC.name}')
print('DONE.')
