"""
patch_hide_allothers_charts.py
Remove ALL OTHERS CAMP dos gráficos de share (bar+line),
mantendo os KPI cards intactos.

Alterações:
  renderMSO():
    - Bar chart FYTD25 vs FYTD26 → usa chartBrands (sem ALL OTHERS)
    - Line chart Evolução Mensal → usa chartBrands (sem ALL OTHERS)
    - KPI cards mso-kpis → MSO_BRANDS inalterado (ALL OTHERS permanece)
  renderMSO2() [isShare block]:
    - Bar chart ACUM JAN-MAR → usa chartBrands2 (sem ALL OTHERS)
    - Line chart EVOLUÇÃO MENSAL ΔPP → usa chartBrands2 (sem ALL OTHERS)
"""
import sys, re, shutil
from pathlib import Path
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

BASE = Path(r'C:\Users\valqu\OneDrive\Documentos\Claude\Projects\projeto Dashboard_farma_sul\Dashboard_farma_sul')
SRC  = BASE / 'Dashboard_Farma_Sul_20260512_2220.html'
VER  = BASE / 'versoes' / f'Dashboard_Farma_Sul_{datetime.now().strftime("%Y%m%d_%H%M")}_HideAOCCharts.html'

print('Lendo dashboard…')
h = SRC.read_text(encoding='utf-8')
orig_len = len(h)

# ─────────────────────────────────────────────────────────
# PATCH 1 — renderMSO(): injetar chartBrands antes do bar chart FYTD
# ─────────────────────────────────────────────────────────
OLD1 = '''  // ── Bar chart FYTD ──
  if(msoBarChart) msoBarChart.destroy();'''

NEW1 = '''  // ── Bar chart FYTD ──
  var chartBrands = MSO_BRANDS.filter(function(b){return b!=='ALL OTHERS CAMP';});
  if(msoBarChart) msoBarChart.destroy();'''

assert h.count(OLD1) == 1, f'PATCH1: encontrei {h.count(OLD1)} ocorrências (esperava 1)'
h = h.replace(OLD1, NEW1)
print('✅ PATCH 1: chartBrands definido antes do bar chart FYTD')

# ─────────────────────────────────────────────────────────
# PATCH 2 — renderMSO(): bar chart usa chartBrands
# ─────────────────────────────────────────────────────────
OLD2 = '''        labels: MSO_BRANDS,
        datasets:[
          {label:'FYTD25', data:MSO_BRANDS.map(function(b){return d[b].fytd25;}),
           backgroundColor:'rgba(255,255,255,0.12)', borderColor:'rgba(255,255,255,0.25)', borderWidth:1.5, borderRadius:8, borderDash:[4,3]},
          {label:'FYTD26', data:MSO_BRANDS.map(function(b){return d[b].fytd26;}),
           backgroundColor:MSO_BRANDS.map(function(b){return MSO_COLORS[b]+'bb';}),
           borderColor:MSO_BRANDS.map(function(b){return MSO_COLORS[b];}), borderWidth:1.5, borderRadius:8},'''

NEW2 = '''        labels: chartBrands,
        datasets:[
          {label:'FYTD25', data:chartBrands.map(function(b){return d[b].fytd25;}),
           backgroundColor:'rgba(255,255,255,0.12)', borderColor:'rgba(255,255,255,0.25)', borderWidth:1.5, borderRadius:8, borderDash:[4,3]},
          {label:'FYTD26', data:chartBrands.map(function(b){return d[b].fytd26;}),
           backgroundColor:chartBrands.map(function(b){return MSO_COLORS[b]+'bb';}),
           borderColor:chartBrands.map(function(b){return MSO_COLORS[b];}), borderWidth:1.5, borderRadius:8},'''

assert h.count(OLD2) == 1, f'PATCH2: encontrei {h.count(OLD2)} ocorrências (esperava 1)'
h = h.replace(OLD2, NEW2)
print('✅ PATCH 2: bar chart FYTD usa chartBrands')

# ─────────────────────────────────────────────────────────
# PATCH 3 — renderMSO(): line chart datasets usa chartBrands
# ─────────────────────────────────────────────────────────
OLD3 = '    var datasets = MSO_BRANDS.map(function(b,i){'
NEW3 = '    var datasets = chartBrands.map(function(b,i){'

assert h.count(OLD3) == 1, f'PATCH3: encontrei {h.count(OLD3)} ocorrências (esperava 1)'
h = h.replace(OLD3, NEW3)
print('✅ PATCH 3: line chart datasets usa chartBrands')

# ─────────────────────────────────────────────────────────
# PATCH 4 — renderMSO(): legenda do line chart usa chartBrands
# ─────────────────────────────────────────────────────────
OLD4 = '    if(leg) leg.innerHTML = MSO_BRANDS.map(function(b){'
NEW4 = '    if(leg) leg.innerHTML = chartBrands.map(function(b){'

assert h.count(OLD4) == 1, f'PATCH4: encontrei {h.count(OLD4)} ocorrências (esperava 1)'
h = h.replace(OLD4, NEW4)
print('✅ PATCH 4: legenda do line chart usa chartBrands')

# ─────────────────────────────────────────────────────────
# PATCH 5 — renderMSO2() isShare: injetar chartBrands2 antes do bar chart ACUM
# ─────────────────────────────────────────────────────────
OLD5 = '''        /* ── BAR CHART ── */
        var prevBC = Chart.getChart('mso2-bar-canvas');
        if(prevBC) prevBC.destroy();
        var cvBar = document.getElementById('mso2-bar-canvas');
        cvBar.removeAttribute('width'); cvBar.removeAttribute('height');
        cvBar.style.width=''; cvBar.style.height='';
        var barLabels = brands.map(function(b){ return b==='SUPER REPELEX'?'S.REP':b==='XO INSETO'?'XO INS':b; });
        var bVals25=[],bVals26=[],bBarColors=[],bBarDeltas=[];
        brands.forEach(function(b){'''

NEW5 = '''        /* ── BAR CHART ── */
        var prevBC = Chart.getChart('mso2-bar-canvas');
        if(prevBC) prevBC.destroy();
        var cvBar = document.getElementById('mso2-bar-canvas');
        cvBar.removeAttribute('width'); cvBar.removeAttribute('height');
        cvBar.style.width=''; cvBar.style.height='';
        var chartBrands2 = brands.filter(function(b){return b!=='ALL OTHERS CAMP';});
        var barLabels = chartBrands2.map(function(b){ return b==='SUPER REPELEX'?'S.REP':b==='XO INSETO'?'XO INS':b; });
        var bVals25=[],bVals26=[],bBarColors=[],bBarDeltas=[];
        chartBrands2.forEach(function(b){'''

assert h.count(OLD5) == 1, f'PATCH5: encontrei {h.count(OLD5)} ocorrências (esperava 1)'
h = h.replace(OLD5, NEW5)
print('✅ PATCH 5: bar chart ACUM JAN-MAR usa chartBrands2')

# ─────────────────────────────────────────────────────────
# PATCH 6 — renderMSO2() isShare: bar chart labels/data usa chartBrands2 (tooltip)
# ─────────────────────────────────────────────────────────
# O tooltip do bar chart usa brands[items[0].dataIndex] — trocar por chartBrands2
OLD6 = '''                  title:function(items){return brands[items[0].dataIndex];},'''
NEW6 = '''                  title:function(items){return chartBrands2[items[0].dataIndex];},'''

assert h.count(OLD6) == 1, f'PATCH6: encontrei {h.count(OLD6)} ocorrências (esperava 1)'
h = h.replace(OLD6, NEW6)
print('✅ PATCH 6: tooltip do bar chart usa chartBrands2')

# ─────────────────────────────────────────────────────────
# PATCH 7 — renderMSO2() isShare: lineDeltasPP usa chartBrands2
# ─────────────────────────────────────────────────────────
OLD7 = '''        var lineDeltasPP={};
        brands.forEach(function(b){'''
NEW7 = '''        var lineDeltasPP={};
        chartBrands2.forEach(function(b){'''

assert h.count(OLD7) == 1, f'PATCH7: encontrei {h.count(OLD7)} ocorrências (esperava 1)'
h = h.replace(OLD7, NEW7)
print('✅ PATCH 7: lineDeltasPP usa chartBrands2')

# ─────────────────────────────────────────────────────────
# PATCH 8 — renderMSO2() isShare: lineDatasets usa chartBrands2
# ─────────────────────────────────────────────────────────
OLD8 = '''        var lineDatasets=brands.map(function(b){'''
NEW8 = '''        var lineDatasets=chartBrands2.map(function(b){'''

assert h.count(OLD8) == 1, f'PATCH8: encontrei {h.count(OLD8)} ocorrências (esperava 1)'
h = h.replace(OLD8, NEW8)
print('✅ PATCH 8: lineDatasets usa chartBrands2')

# ─────────────────────────────────────────────────────────
# PATCH 9 — renderMSO2() isShare: tooltip do line chart usa chartBrands2
# ─────────────────────────────────────────────────────────
OLD9 = '''                    var b=brands[ctx.datasetIndex];'''
NEW9 = '''                    var b=chartBrands2[ctx.datasetIndex];'''

assert h.count(OLD9) == 1, f'PATCH9: encontrei {h.count(OLD9)} ocorrências (esperava 1)'
h = h.replace(OLD9, NEW9)
print('✅ PATCH 9: tooltip do line chart usa chartBrands2')

# ─────────────────────────────────────────────────────────
# Salvar
# ─────────────────────────────────────────────────────────
print(f'\nTamanho original: {orig_len:,} | Novo: {len(h):,} | Δ: +{len(h)-orig_len:,}')

VER.parent.mkdir(parents=True, exist_ok=True)
VER.write_text(h, encoding='utf-8')
print(f'✅ Versão salva: {VER.name}')

SRC.write_text(h, encoding='utf-8')
print(f'✅ Base ativa atualizada: {SRC.name}')

# Verificação final
assert 'var chartBrands = MSO_BRANDS.filter' in h, 'chartBrands não foi injetado em renderMSO'
assert 'var chartBrands2 = brands.filter' in h, 'chartBrands2 não foi injetado em renderMSO2'
assert h.count('labels: chartBrands,') == 1, 'bar chart FYTD ainda usa labels errados'
print('\n✅ Verificações finais OK')
print('DONE.')
