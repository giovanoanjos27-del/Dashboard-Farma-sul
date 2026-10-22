"""
patch_nielsen_delta_colors.py
Regra simples de cores nos deltas do Excel:
  > 0  → verde  (C.green)
  < 0  → vermelho (C.red)
  = 0  → cinza  (C.gray)
Antes: threshold ±0.5 (valores entre -0.5 e +0.5 ficavam âmbar).
"""
import sys
from pathlib import Path
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

BASE = Path(r'C:\Users\valqu\OneDrive\Documentos\Claude\Projects\projeto Dashboard_farma_sul\Dashboard_farma_sul')
SRC  = BASE / 'Dashboard_Farma_Sul_20260512_2220.html'
VER  = BASE / 'versoes' / f'Dashboard_Farma_Sul_{datetime.now().strftime("%Y%m%d_%H%M")}_DeltaColors.html'

print('Lendo dashboard…')
h = SRC.read_text(encoding='utf-8')
orig_len = len(h)

# ── deltaColor: threshold 0 em vez de ±0.5 ──
OLD_DELTA = "function deltaColor(d){ return d>=0.5?C.green:d<=-0.5?C.red:C.amber; }"
NEW_DELTA = "function deltaColor(d){ return d>0?C.green:d<0?C.red:C.gray; }"

assert h.count(OLD_DELTA) == 1, f'deltaColor: {h.count(OLD_DELTA)} ocorrências'
h = h.replace(OLD_DELTA, NEW_DELTA)
print('✅ deltaColor → d>0 verde / d<0 vermelho / d=0 cinza')

# Verificação
assert 'function deltaColor(d){ return d>0?C.green:d<0?C.red:C.gray; }' in h
print('✅ Verificação OK')

print(f'\nTamanho original: {orig_len:,} | Novo: {len(h):,} | Δ: {len(h)-orig_len:+,}')

VER.parent.mkdir(parents=True, exist_ok=True)
VER.write_text(h, encoding='utf-8')
print(f'✅ Versão salva: {VER.name}')
SRC.write_text(h, encoding='utf-8')
print(f'✅ Base ativa atualizada: {SRC.name}')
print('DONE.')
