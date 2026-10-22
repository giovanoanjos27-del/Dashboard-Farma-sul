"""
patch_acumulado_fy_resize.py
Corrige gráficos em branco no card Acumulado FY.

Causa: Chart.js renderizava com o container em display:none (ao carregar a página),
criando charts com dimensões 0×0. Depois que o usuário clica em Sell Out, o resize
automático não disparava.

Fixes:
  1. Verificação de visibilidade (offsetWidth/offsetHeight) no início de renderAcumuladoFY;
     se canvas ainda invisível → reagendar até 20 vezes (2s total)
  2. chart.resize() forçado 80ms após criação dos charts
  3. Aumentar delay do acumMoveToClient init de 80ms → 160ms
"""
import sys
from pathlib import Path
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

BASE = Path(r'C:\Users\valqu\OneDrive\Documentos\Claude\Projects\projeto Dashboard_farma_sul\Dashboard_farma_sul')
SRC  = BASE / 'Dashboard_Farma_Sul_20260512_2220.html'
VER  = BASE / 'versoes' / f'Dashboard_Farma_Sul_{datetime.now().strftime("%Y%m%d_%H%M")}_AcumResize.html'

print('Lendo dashboard…')
h = SRC.read_text(encoding='utf-8')
orig_len = len(h)

# ─────────────────────────────────────────────────────────────────────────────
# FIX 1: Verificação de visibilidade + retry no início de renderAcumuladoFY
# ─────────────────────────────────────────────────────────────────────────────
OLD_RENDER_START = """    window.renderAcumuladoFY = function(clientId){
      if(typeof Chart==='undefined') return;
      if(!clientId) clientId = (typeof activeSelloutClient!=='undefined') ? activeSelloutClient : 'saojoao';
      _acumCurClient = clientId;"""

NEW_RENDER_START = """    var _acumRenderRetries = 0;
    window.renderAcumuladoFY = function(clientId){
      if(typeof Chart==='undefined') return;
      if(!clientId) clientId = (typeof activeSelloutClient!=='undefined') ? activeSelloutClient : 'saojoao';
      // Verificar visibilidade do canvas — se display:none, reagendar
      var _cv = document.getElementById('acum-rec-canvas');
      if(_cv && _cv.offsetWidth === 0){
        _acumRenderRetries++;
        if(_acumRenderRetries <= 20){
          setTimeout(function(){ window.renderAcumuladoFY(clientId); }, 100);
          return;
        }
      }
      _acumRenderRetries = 0;
      _acumCurClient = clientId;"""

assert h.count(OLD_RENDER_START) == 1, f'❌ âncora renderStart: {h.count(OLD_RENDER_START)}×'
h = h.replace(OLD_RENDER_START, NEW_RENDER_START)
print('✅ Verificação de visibilidade + retry adicionada')

# ─────────────────────────────────────────────────────────────────────────────
# FIX 2: chart.resize() 80ms após criação
# ─────────────────────────────────────────────────────────────────────────────
OLD_CHART_CREATE = """      _acumChartR = _mkChart('acum-rec-canvas',cR25,cR26,cR26P,_acumChartR,true);
      _acumChartV = _mkChart('acum-vol-canvas',cV25,cV26,cV26P,_acumChartV,false);"""

NEW_CHART_CREATE = """      _acumChartR = _mkChart('acum-rec-canvas',cR25,cR26,cR26P,_acumChartR,true);
      _acumChartV = _mkChart('acum-vol-canvas',cV25,cV26,cV26P,_acumChartV,false);
      // Forçar resize após inserção no DOM (container pode ter acabado de se tornar visível)
      setTimeout(function(){
        if(_acumChartR) try{ _acumChartR.resize(); }catch(e){}
        if(_acumChartV) try{ _acumChartV.resize(); }catch(e){}
      }, 80);"""

assert h.count(OLD_CHART_CREATE) == 1, f'❌ âncora chartCreate: {h.count(OLD_CHART_CREATE)}×'
h = h.replace(OLD_CHART_CREATE, NEW_CHART_CREATE)
print('✅ chart.resize() após criação adicionado')

# ─────────────────────────────────────────────────────────────────────────────
# FIX 3: Aumentar delay do renderAcumuladoFY dentro de acumMoveToClient
#         de 80ms → 200ms (garantir que o container já está visível)
# ─────────────────────────────────────────────────────────────────────────────
OLD_MOVE_DELAY = """      if(typeof window.renderAcumuladoFY === 'function')
        setTimeout(function(){ window.renderAcumuladoFY(clientId); }, 80);"""

NEW_MOVE_DELAY = """      if(typeof window.renderAcumuladoFY === 'function')
        setTimeout(function(){ window.renderAcumuladoFY(clientId); }, 200);"""

assert h.count(OLD_MOVE_DELAY) == 1, f'❌ âncora moveDelay: {h.count(OLD_MOVE_DELAY)}×'
h = h.replace(OLD_MOVE_DELAY, NEW_MOVE_DELAY)
print('✅ Delay de renderização aumentado: 80ms → 200ms')

# ─────────────────────────────────────────────────────────────────────────────
# Verificações
# ─────────────────────────────────────────────────────────────────────────────
assert '_acumRenderRetries' in h,          '❌ retry counter não encontrado'
assert 'offsetWidth === 0' in h,           '❌ verificação de visibilidade não encontrada'
assert '_acumChartR.resize()' in h,        '❌ chart.resize não encontrado'
assert '}, 200);' in h,                    '❌ delay 200ms não encontrado'
print('✅ Verificações OK')

print(f'\nTamanho original: {orig_len:,} | Novo: {len(h):,} | Δ: {len(h)-orig_len:+,}')

VER.parent.mkdir(parents=True, exist_ok=True)
VER.write_text(h, encoding='utf-8')
print(f'✅ Versão salva: {VER.name}')
SRC.write_text(h, encoding='utf-8')
print(f'✅ Base ativa atualizada: {SRC.name}')
print('DONE.')
