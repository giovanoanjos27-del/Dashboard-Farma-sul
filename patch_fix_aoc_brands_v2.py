"""
patch_fix_aoc_brands_v2.py
Corrige todos os lugares onde ALL OTHERS CAMP contamina cálculos e gráficos.

PROBLEMAS:
  1. renderMSO2() val/un mode: var brands = MSO_BRANDS → inclui ALL OTHERS
     no bar chart R$MM e nos KPI chips (MAIOR VOLUME, MAIOR QUEDA)
  2. renderMSO2() diagnóstico val/un: scjI26 soma ALL OTHERS → SCJ share ~100%
  3. renderMSO3(): var brands = MSO_BRANDS → totV26 inflado, bar chart com ALL OTHERS,
     KPI chips (MAIOR VOLUME, MAIOR QUEDA) podem apontar ALL OTHERS

REGRA: ALL OTHERS CAMP fica apenas nos KPI cards (mso-kpis em renderMSO),
       removido de TODOS os cálculos, gráficos e chips em renderMSO2 e renderMSO3.
"""
import sys
from pathlib import Path
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

BASE = Path(r'C:\Users\valqu\OneDrive\Documentos\Claude\Projects\projeto Dashboard_farma_sul\Dashboard_farma_sul')
SRC  = BASE / 'Dashboard_Farma_Sul_20260512_2220.html'
VER  = BASE / 'versoes' / f'Dashboard_Farma_Sul_{datetime.now().strftime("%Y%m%d_%H%M")}_FixAOCBrands.html'

print('Lendo dashboard…')
h = SRC.read_text(encoding='utf-8')
orig_len = len(h)

# ─────────────────────────────────────────────────────────
# PATCH A — renderMSO2(): filtrar ALL OTHERS de `brands`
# (afeta bar chart val/un E KPI chips share+val+un E d25/d26 builds)
# ─────────────────────────────────────────────────────────
OLD_A = '''  var brands = MSO_BRANDS;
  var colors = MSO_COLORS;

  /* BUILD VALUE SETS */'''

NEW_A = '''  var brands = MSO_BRANDS.filter(function(b){return b!=='ALL OTHERS CAMP';});
  var colors = MSO_COLORS;

  /* BUILD VALUE SETS */'''

count_a = h.count(OLD_A)
assert count_a == 1, f'PATCH A: encontrei {count_a} ocorrências (esperava 1)'
h = h.replace(OLD_A, NEW_A)
print('✅ PATCH A: renderMSO2 brands filtrado (sem ALL OTHERS CAMP)')

# ─────────────────────────────────────────────────────────
# PATCH B — renderMSO2() diagnóstico val/un: scjI26 excluir ALL OTHERS
# Sem esse fix: scjI26 ≈ total mercado → share SCJ ~100%
# ─────────────────────────────────────────────────────────
OLD_B = '''  var scjI26=0, scjI25=0;
  MSO_BRANDS.forEach(function(b){
    var bd=nbvI[b]; if(!bd) return;'''

NEW_B = '''  var scjI26=0, scjI25=0;
  MSO_BRANDS.forEach(function(b){
    if(b==='ALL OTHERS CAMP') return; /* excluir ALL OTHERS do total SCJ */
    var bd=nbvI[b]; if(!bd) return;'''

count_b = h.count(OLD_B)
assert count_b == 1, f'PATCH B: encontrei {count_b} ocorrências (esperava 1)'
h = h.replace(OLD_B, NEW_B)
print('✅ PATCH B: scjI26 diagnóstico exclui ALL OTHERS (share SCJ correto)')

# ─────────────────────────────────────────────────────────
# PATCH C — renderMSO2() diagnóstico val/un: lines2 excluir ALL OTHERS
# Bloco "Por Marca" do diagnóstico não deve mostrar ALL OTHERS CAMP
# ─────────────────────────────────────────────────────────
OLD_C = '''  var lines2 = MSO_BRANDS.map(function(b){
    var bd=nbvI[b]; if(!bd) return null;'''

NEW_C = '''  var lines2 = MSO_BRANDS.filter(function(b){return b!=='ALL OTHERS CAMP';}).map(function(b){
    var bd=nbvI[b]; if(!bd) return null;'''

count_c = h.count(OLD_C)
assert count_c == 1, f'PATCH C: encontrei {count_c} ocorrências (esperava 1)'
h = h.replace(OLD_C, NEW_C)
print('✅ PATCH C: diagnóstico "Por Marca" exclui ALL OTHERS CAMP')

# ─────────────────────────────────────────────────────────
# PATCH D — renderMSO3(): filtrar ALL OTHERS de `brands`
# Afeta: totV25/totV26, KPI chips, brand bar chart FYTD
# ─────────────────────────────────────────────────────────
OLD_D = '''  var brands = MSO_BRANDS;
  var colors = MSO_COLORS;

  /* Atualizar títulos */'''

NEW_D = '''  var brands = MSO_BRANDS.filter(function(b){return b!=='ALL OTHERS CAMP';});
  var colors = MSO_COLORS;

  /* Atualizar títulos */'''

count_d = h.count(OLD_D)
assert count_d == 1, f'PATCH D: encontrei {count_d} ocorrências (esperava 1)'
h = h.replace(OLD_D, NEW_D)
print('✅ PATCH D: renderMSO3 brands filtrado (sem ALL OTHERS CAMP)')

# ─────────────────────────────────────────────────────────
# PATCH E — renderMSO2() diagnóstico share: allDeltas2 exclui ALL OTHERS
# (linha 18798 usa MSO_BRANDS diretamente)
# ─────────────────────────────────────────────────────────
OLD_E = '''    var allDeltas2 = MSO_BRANDS.map(function(b){'''
NEW_E = '''    var allDeltas2 = MSO_BRANDS.filter(function(b){return b!=='ALL OTHERS CAMP';}).map(function(b){'''

count_e = h.count(OLD_E)
assert count_e == 1, f'PATCH E: encontrei {count_e} ocorrências (esperava 1)'
h = h.replace(OLD_E, NEW_E)
print('✅ PATCH E: allDeltas2 diagnóstico share exclui ALL OTHERS CAMP')

# ─────────────────────────────────────────────────────────
# Verificações finais
# ─────────────────────────────────────────────────────────
print(f'\nTamanho original: {orig_len:,} | Novo: {len(h):,} | Δ: +{len(h)-orig_len:,}')

# Verificar que os patches estão no arquivo
assert "MSO_BRANDS.filter(function(b){return b!=='ALL OTHERS CAMP';});" in h or \
       "MSO_BRANDS.filter(function(b){return b!=='ALL OTHERS CAMP';})" in h, 'Filtro não encontrado'
assert "if(b==='ALL OTHERS CAMP') return; /* excluir ALL OTHERS do total SCJ */" in h, 'PATCH B não aplicado'

# Contar ocorrências perigosas: var brands = MSO_BRANDS; (sem filtro) nas funções renderMSO2 e renderMSO3
remaining = h.count("var brands = MSO_BRANDS;")
print(f'\nOcorrências de "var brands = MSO_BRANDS;" restantes: {remaining}')
# Deve ser 0 (todas foram filtradas)
if remaining > 0:
    print('⚠️  ATENÇÃO: ainda existem brands = MSO_BRANDS sem filtro — verificar manualmente')
else:
    print('✅ Nenhuma ocorrência perigosa de "var brands = MSO_BRANDS;" restante')

# Salvar
VER.parent.mkdir(parents=True, exist_ok=True)
VER.write_text(h, encoding='utf-8')
print(f'\n✅ Versão salva: {VER.name}')

SRC.write_text(h, encoding='utf-8')
print(f'✅ Base ativa atualizada: {SRC.name}')
print('DONE.')
