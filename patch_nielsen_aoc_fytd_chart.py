"""
patch_nielsen_aoc_fytd_chart.py
Inclui "ALL OTHERS CAMP" no card FYTD JUL-MAR R$/Unidades (renderMSO3).

Diagnóstico:
  O gráfico de barras "FYTD JUL-MAR · 2025 vs 2026" usava `brands` (array
  filtrado sem ALL OTHERS CAMP). A marca estava nos dados mas invisível no
  gráfico, causando diferença entre soma das barras e total mercado.

Fixes (cirúrgicos — só em renderMSO3, sem tocar outros cards):
  1. Criar chartBrands3 = MSO_BRANDS (todas, incluindo AOC) para o gráfico
  2. Carregar d25/d26 de 'ALL OTHERS CAMP' antes de montar o chart
  3. Usar chartBrands3 no barLabels3 e no forEach do chart
  4. Corrigir referência `brands` → `chartBrands3` no callback do tooltip
  5. Incluir ALL OTHERS CAMP na seção "Por Marca" do diagnóstico (lines3)

NÃO ALTERA:
  - `brands` (usado nos cálculos SCJ — correto ficar sem AOC)
  - totV25 / totV26 (somas SCJ — sem AOC para não inflar share SCJ)
  - KPI chips de MAIOR VOLUME / MAIOR QUEDA (permanecem sem AOC)
  - Cards 1 (renderMSO) e 2 (renderMSO2)
  - Todos os outros gráficos, filtros, Sell Out, Sell In, Cobertura, OLs
"""
import sys
from pathlib import Path
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

BASE = Path(r'C:\Users\valqu\OneDrive\Documentos\Claude\Projects\projeto Dashboard_farma_sul\Dashboard_farma_sul')
SRC  = BASE / 'Dashboard_Farma_Sul_20260512_2220.html'
VER  = BASE / 'versoes' / f'Dashboard_Farma_Sul_{datetime.now().strftime("%Y%m%d_%H%M")}_AocFytdChart.html'

print('Lendo dashboard…')
h = SRC.read_text(encoding='utf-8')
orig_len = len(h)

# ─────────────────────────────────────────────────────────────────────────────
# FIX 1 + 2 + 3: chartBrands3 + carregamento AOC + usar no gráfico
# ─────────────────────────────────────────────────────────────────────────────
OLD_BAR_BRANDS = """    var barLabels3=brands.map(function(b){return b==='SUPER REPELEX'?'S.REPELEX':b;});
    var bV25=[],bV26=[],bCols=[],bDs=[],bDstrs=[];
    brands.forEach(function(b){
      var v25=d25[b]||0,v26=d26[b]||0,cor=colors[b]||'#e2e8f0',dt=calcDelta3(v25,v26);
      bV25.push(v25);bV26.push(v26);bCols.push(cor);bDs.push(dt.raw);bDstrs.push(dt.str);
    });"""

NEW_BAR_BRANDS = """    /* chartBrands3: inclui ALL OTHERS CAMP no gráfico de barras */
    var chartBrands3 = MSO_BRANDS; // todas as marcas, incluindo ALL OTHERS CAMP
    /* Carregar dados de ALL OTHERS CAMP para d25/d26 */
    if(nbv && nbv['ALL OTHERS CAMP']){
      d25['ALL OTHERS CAMP'] = isVal ? nbv['ALL OTHERS CAMP'].fytd25_val : nbv['ALL OTHERS CAMP'].fytd25_un;
      d26['ALL OTHERS CAMP'] = isVal ? nbv['ALL OTHERS CAMP'].fytd26_val : nbv['ALL OTHERS CAMP'].fytd26_un;
    }
    var barLabels3=chartBrands3.map(function(b){return b==='SUPER REPELEX'?'S.REPELEX':(b==='ALL OTHERS CAMP'?'OUTROS':b);});
    var bV25=[],bV26=[],bCols=[],bDs=[],bDstrs=[];
    chartBrands3.forEach(function(b){
      var v25=d25[b]||0,v26=d26[b]||0,cor=colors[b]||'#e2e8f0',dt=calcDelta3(v25,v26);
      bV25.push(v25);bV26.push(v26);bCols.push(cor);bDs.push(dt.raw);bDstrs.push(dt.str);
    });"""

assert h.count(OLD_BAR_BRANDS) == 1, f'❌ âncora barLabels3: {h.count(OLD_BAR_BRANDS)}×'
h = h.replace(OLD_BAR_BRANDS, NEW_BAR_BRANDS)
print('✅ FIX 1+2+3: chartBrands3 + carregamento AOC + barLabels usando chartBrands3')

# ─────────────────────────────────────────────────────────────────────────────
# FIX 4: Corrigir referência brands → chartBrands3 no callback tooltip
# ─────────────────────────────────────────────────────────────────────────────
OLD_TOOLTIP_BRANDS = """            var b=brands[ctx.dataIndex];
            if(ctx.datasetIndex===0) return '  FYTD/25: '+fmtV3(d25[b]||0);
            return '  FYTD/26: '+fmtV3(d26[b]||0)+'   ('+bDstrs[ctx.dataIndex]+' YoY)';"""

NEW_TOOLTIP_BRANDS = """            var b=chartBrands3[ctx.dataIndex];
            if(ctx.datasetIndex===0) return '  FYTD/25: '+fmtV3(d25[b]||0);
            return '  FYTD/26: '+fmtV3(d26[b]||0)+'   ('+bDstrs[ctx.dataIndex]+' YoY)';"""

assert h.count(OLD_TOOLTIP_BRANDS) == 1, f'❌ âncora tooltip brands: {h.count(OLD_TOOLTIP_BRANDS)}×'
h = h.replace(OLD_TOOLTIP_BRANDS, NEW_TOOLTIP_BRANDS)
print('✅ FIX 4: tooltip callback corrigido → chartBrands3[ctx.dataIndex]')

# ─────────────────────────────────────────────────────────────────────────────
# FIX 5: lines3 diagnóstico — incluir ALL OTHERS CAMP
# ─────────────────────────────────────────────────────────────────────────────
OLD_LINES3 = "    var lines3=brands.map(function(b){"
NEW_LINES3 = "    var lines3=MSO_BRANDS.map(function(b){"

assert h.count(OLD_LINES3) == 1, f'❌ âncora lines3: {h.count(OLD_LINES3)}×'
h = h.replace(OLD_LINES3, NEW_LINES3)
print('✅ FIX 5: lines3 diagnóstico usa MSO_BRANDS (inclui ALL OTHERS CAMP)')

# ─────────────────────────────────────────────────────────────────────────────
# Verificações finais
# ─────────────────────────────────────────────────────────────────────────────
assert 'var chartBrands3 = MSO_BRANDS;' in h,                 '❌ chartBrands3 não encontrado'
assert "d25['ALL OTHERS CAMP'] = isVal" in h,                  '❌ carregamento AOC d25 não encontrado'
assert "d26['ALL OTHERS CAMP'] = isVal" in h,                  '❌ carregamento AOC d26 não encontrado'
assert "b==='ALL OTHERS CAMP'?'OUTROS'" in h,                  '❌ label OUTROS não encontrado'
assert 'chartBrands3.forEach(function(b)' in h,                '❌ forEach chartBrands3 não encontrado'
assert 'var b=chartBrands3[ctx.dataIndex]' in h,               '❌ tooltip chartBrands3 não encontrado'
assert 'var lines3=MSO_BRANDS.map(function(b)' in h,           '❌ lines3 MSO_BRANDS não encontrado'
# Verificar que as partes de SCJ não foram alteradas
assert 'var brands = MSO_BRANDS.filter(function(b){return b' in h, '❌ brands filter removido!'
assert h.count("totV25+=d25[b]||0;totV26+=d26[b]||0;") == 1,  '❌ totV25/V26 alterado!'
print('✅ Todas as verificações OK')

print(f'\nTamanho original: {orig_len:,} | Novo: {len(h):,} | Δ: {len(h)-orig_len:+,}')

VER.parent.mkdir(parents=True, exist_ok=True)
VER.write_text(h, encoding='utf-8')
print(f'✅ Versão salva: {VER.name}')
SRC.write_text(h, encoding='utf-8')
print(f'✅ Base ativa atualizada: {SRC.name}')
print('DONE.')
