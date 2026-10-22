"""
patch_acumulado_fy_v4.py
Correção cirúrgica — 4 fixes no card EVOLUÇÃO ACUMULADA FY25 vs FY26.

FIX 1: Gráficos em branco (backgroundColor gradient → rgba sólido)
  Causa: createLinearGradient(0,0,0,0) com container 0×0 produz gradiente
  zerado (transparente) em alguns ambientes. Substitui por rgba() fixo.

FIX 2: Dados errados ao selecionar Compradora Isadora ou Caroline
  Causa: _data('saojoao') sempre usava SJ_REC (total), sem checar sjModo.
  Fix: detecta sjModo → total=SJ_REC, isadora=SJ_REC−SJC, caroline=SJC.

FIX 3: Card não re-renderiza ao trocar Compradora (Isadora/Caroline)
  Causa: switchSJCompradora não chamava _acumTryRender.
  Fix: injetar _acumTryRender('saojoao',0) nos dois setTimeout() da função.

FIX 4: Título do card atualizado dinamicamente conforme compradora
  Subtitle e label do diagnóstico atualizam para refletir a compradora ativa.

NÃO ALTERA: outros gráficos, Nielsen, Sell In, Cobertura, Diagnóstico,
Plano Negócios, OLs, outros clientes, medidas existentes, layout.
"""
import sys
from pathlib import Path
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

BASE = Path(r'C:\Users\valqu\OneDrive\Documentos\Claude\Projects\projeto Dashboard_farma_sul\Dashboard_farma_sul')
SRC  = BASE / 'Dashboard_Farma_Sul_20260512_2220.html'
VER  = BASE / 'versoes' / f'Dashboard_Farma_Sul_{datetime.now().strftime("%Y%m%d_%H%M")}_AcumV4.html'

print('Lendo dashboard…')
h = SRC.read_text(encoding='utf-8')
orig_len = len(h)

# ─────────────────────────────────────────────────────────────────────────────
# FIX 1: Substituir backgroundColor com gradient por rgba() sólido em _mkChart
# O gradient com container 0×0 cria gradiente zerado (transparente)
# ─────────────────────────────────────────────────────────────────────────────
OLD_BG_FY25 = "backgroundColor:function(ctx){return _grad(ctx.chart.ctx,ctx.chart.chartArea,'#3b82f6');}"
NEW_BG_FY25 = "backgroundColor:'rgba(59,130,246,0.18)'"

OLD_BG_FY26 = "backgroundColor:function(ctx){return _grad(ctx.chart.ctx,ctx.chart.chartArea,'#34d399');}"
NEW_BG_FY26 = "backgroundColor:'rgba(52,211,153,0.18)'"

assert h.count(OLD_BG_FY25) == 1, f'❌ âncora FY25 backgroundColor: {h.count(OLD_BG_FY25)}×'
assert h.count(OLD_BG_FY26) == 1, f'❌ âncora FY26 backgroundColor: {h.count(OLD_BG_FY26)}×'
h = h.replace(OLD_BG_FY25, NEW_BG_FY25)
h = h.replace(OLD_BG_FY26, NEW_BG_FY26)
print('✅ FIX 1: backgroundColor gradient → rgba() sólido (FY25 + FY26)')

# ─────────────────────────────────────────────────────────────────────────────
# FIX 2: _data('saojoao') com suporte a sjModo (total / isadora / caroline)
# ─────────────────────────────────────────────────────────────────────────────
OLD_DATA_SJ = """    if(cl==='saojoao'){
      if(typeof SJ_REC!=='undefined')  _add(_fy(SJ_REC['2024'],SJ_REC['2025'],SJ_REC['2026']),  r25,r26);
      if(typeof SJ_UNID!=='undefined') _add(_fy(SJ_UNID['2024'],SJ_UNID['2025'],SJ_UNID['2026']),v25,v26);
    }"""

NEW_DATA_SJ = """    if(cl==='saojoao'){
      var _sjm=(typeof sjModo!=='undefined')?sjModo:'total';
      /* subtração elemento a elemento para Isadora = Total − Caroline */
      function _aS(a,b){return a.map(function(v,i){return(v!=null&&b&&b[i]!=null)?(v-b[i]):(v!=null?v:null);});}
      if(_sjm==='caroline'){
        /* Compradora Caroline — arrays SJC */
        if(typeof SJC_REC!=='undefined'){
          _add(_fy(SJC_REC_24,SJC_REC,SJC_REC_26),r25,r26);
          _add(_fy(SJC_VOL_24,SJC_VOL,SJC_VOL_26),v25,v26);
        }
      } else if(_sjm==='isadora'){
        /* Compradora Isadora = SJ Total − Caroline */
        if(typeof SJ_REC!=='undefined'&&typeof SJC_REC!=='undefined'){
          _add(_fy(_aS(SJ_REC['2024'],SJC_REC_24),_aS(SJ_REC['2025'],SJC_REC),_aS(SJ_REC['2026'],SJC_REC_26)),r25,r26);
          _add(_fy(_aS(SJ_UNID['2024'],SJC_VOL_24),_aS(SJ_UNID['2025'],SJC_VOL),_aS(SJ_UNID['2026'],SJC_VOL_26)),v25,v26);
        }
      } else {
        /* total (padrão) */
        if(typeof SJ_REC!=='undefined')  _add(_fy(SJ_REC['2024'],SJ_REC['2025'],SJ_REC['2026']),r25,r26);
        if(typeof SJ_UNID!=='undefined') _add(_fy(SJ_UNID['2024'],SJ_UNID['2025'],SJ_UNID['2026']),v25,v26);
      }
    }"""

assert h.count(OLD_DATA_SJ) == 1, f'❌ âncora _data saojoao: {h.count(OLD_DATA_SJ)}×'
h = h.replace(OLD_DATA_SJ, NEW_DATA_SJ)
print('✅ FIX 2: _data saojoao → suporte a sjModo (total / isadora / caroline)')

# ─────────────────────────────────────────────────────────────────────────────
# FIX 3: Injetar _acumTryRender nos dois branches de switchSJCompradora
# ─────────────────────────────────────────────────────────────────────────────
OLD_SWITCH_SJ = """  if(comp==='caroline'){
    setTimeout(function(){
      initCaroline();
      if(window.edAtribShow) window.edAtribShow('sj', null);
  if(window.edAtribSetRede) window.edAtribSetRede('sj');
    }, 30);
  } else {
    /* re-renderiza KPIs e gráficos com o modo correto (total / isadora) */
    setTimeout(function(){
      initSJ();
      if(window.edAtribShow) window.edAtribShow('sj', null);
    }, 30);
  }
}"""

NEW_SWITCH_SJ = """  if(comp==='caroline'){
    setTimeout(function(){
      initCaroline();
      if(window.edAtribShow) window.edAtribShow('sj', null);
  if(window.edAtribSetRede) window.edAtribSetRede('sj');
      /* Acumulado FY: re-renderizar com dados da Caroline */
      if(typeof window._acumTryRender==='function') window._acumTryRender('saojoao',0);
    }, 30);
  } else {
    /* re-renderiza KPIs e gráficos com o modo correto (total / isadora) */
    setTimeout(function(){
      initSJ();
      if(window.edAtribShow) window.edAtribShow('sj', null);
      /* Acumulado FY: re-renderizar com dados corretos (total ou isadora) */
      if(typeof window._acumTryRender==='function') window._acumTryRender('saojoao',0);
    }, 30);
  }
}"""

assert h.count(OLD_SWITCH_SJ) == 1, f'❌ âncora switchSJCompradora: {h.count(OLD_SWITCH_SJ)}×'
h = h.replace(OLD_SWITCH_SJ, NEW_SWITCH_SJ)
print('✅ FIX 3: switchSJCompradora → _acumTryRender injetado (caroline + total/isadora)')

# ─────────────────────────────────────────────────────────────────────────────
# FIX 4: lbl dinâmico em renderAcumuladoFYClient (reflete compradora ativa)
# ─────────────────────────────────────────────────────────────────────────────
OLD_LBL = "    var lbl=_LBL[cl]||cl;"

NEW_LBL = """    /* Label dinâmico: para SJ, usa compradora ativa */
    var _cMode=(cl==='saojoao'&&typeof sjModo!=='undefined')?sjModo:'total';
    var lbl=cl==='saojoao'
      ?(_cMode==='isadora'?'Compradora Isadora':_cMode==='caroline'?'Compradora Caroline':'São João Total')
      :(_LBL[cl]||cl);
    /* Atualizar subtitle do card */
    var _subEl=document.getElementById('acum-sub-'+cl);
    if(_subEl) _subEl.textContent='Faturamento Acumulado · Jul/24–Jun/25 vs Jul/25–Jun/26 · '+lbl;"""

assert h.count(OLD_LBL) == 1, f'❌ âncora lbl: {h.count(OLD_LBL)}×'
h = h.replace(OLD_LBL, NEW_LBL)
print('✅ FIX 4: lbl dinâmico → subtitle do card atualizado por compradora')

# ─────────────────────────────────────────────────────────────────────────────
# Verificações finais
# ─────────────────────────────────────────────────────────────────────────────
assert "backgroundColor:'rgba(59,130,246,0.18)'" in h,  '❌ rgba FY25 não encontrado'
assert "backgroundColor:'rgba(52,211,153,0.18)'" in h,  '❌ rgba FY26 não encontrado'
assert '_sjm===\'caroline\'' in h,                       '❌ modo caroline não encontrado'
assert '_sjm===\'isadora\'' in h,                        '❌ modo isadora não encontrado'
assert '_acumTryRender(\'saojoao\',0)' in h,             '❌ trigger saojoao não encontrado'
assert '_cMode===\'isadora\'' in h,                      '❌ lbl isadora não encontrado'
assert 'acum-sub-\'+cl' in h,                            '❌ subtitle update não encontrado'
print('✅ Todas as verificações OK')

print(f'\nTamanho original: {orig_len:,} | Novo: {len(h):,} | Δ: {len(h)-orig_len:+,}')

VER.parent.mkdir(parents=True, exist_ok=True)
VER.write_text(h, encoding='utf-8')
print(f'✅ Versão salva: {VER.name}')
SRC.write_text(h, encoding='utf-8')
print(f'✅ Base ativa atualizada: {SRC.name}')
print('DONE.')
