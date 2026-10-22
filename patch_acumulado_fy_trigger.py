"""
patch_acumulado_fy_trigger.py
Correção cirúrgica do card EVOLUÇÃO ACUMULADA FY25 vs FY26.

Diagnóstico:
  O polling de offsetWidth nas init scripts para quando a seção ainda está oculta
  (display:none). Quando o usuário abre a aba Sell Out, nenhum gatilho dispara
  a renderização — o card fica em branco.

Correção (3 mudanças):
  1. Injetar chamada em switchSellOutClient → _acumTryRender(clientId, 0)
     Garante render imediato quando o usuário troca de cliente (seção já visível).
  2. Forçar re-render no _mkChart com chart.update() após resize()
  3. Aumentar delay inicial dos init scripts: 250ms → 600ms (mais tempo pra DOM)

NÃO ALTERA: outros gráficos, filtros, Nielsen, Sell In, Cobertura, Diagnóstico,
Plano Negócios, OLs, medidas existentes, layout do dashboard.
"""
import sys
from pathlib import Path
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

BASE = Path(r'C:\Users\valqu\OneDrive\Documentos\Claude\Projects\projeto Dashboard_farma_sul\Dashboard_farma_sul')
SRC  = BASE / 'Dashboard_Farma_Sul_20260512_2220.html'
VER  = BASE / 'versoes' / f'Dashboard_Farma_Sul_{datetime.now().strftime("%Y%m%d_%H%M")}_AcumTrigger.html'

print('Lendo dashboard…')
h = SRC.read_text(encoding='utf-8')
orig_len = len(h)

# ─────────────────────────────────────────────────────────────────────────────
# FIX 1: Injetar _acumTryRender em switchSellOutClient
# Gatilho direto quando usuário troca de cliente — seção já está visível
# ─────────────────────────────────────────────────────────────────────────────
OLD_SWITCH_END = """  } catch(e){ console.error('[switchSellOutClient] Erro init', clientId, e); }
    }, 60);
  }
}

/* ═══════════ COBERTURA TAB ═══════════ */"""

NEW_SWITCH_END = """  } catch(e){ console.error('[switchSellOutClient] Erro init', clientId, e); }
    }, 60);
  }
  /* Acumulado FY: renderizar card do cliente ativo */
  if(typeof window._acumTryRender === 'function')
    setTimeout(function(){ window._acumTryRender(clientId, 0); }, 350);
}

/* ═══════════ COBERTURA TAB ═══════════ */"""

assert h.count(OLD_SWITCH_END) == 1, f'❌ âncora switchSellOutClient: {h.count(OLD_SWITCH_END)}×'
h = h.replace(OLD_SWITCH_END, NEW_SWITCH_END)
print('✅ switchSellOutClient → _acumTryRender(clientId, 0) injetado')

# ─────────────────────────────────────────────────────────────────────────────
# FIX 2: Adicionar chart.update() após resize() no _mkChart
# Força Chart.js a redesenhar após o container se tornar visível
# ─────────────────────────────────────────────────────────────────────────────
OLD_RESIZE = """    setTimeout(function(){ try{ chart.resize(); }catch(e){} },80);
    return chart;"""

NEW_RESIZE = """    setTimeout(function(){
      try{ chart.resize(); }catch(e){}
      setTimeout(function(){ try{ chart.update(); }catch(e){} },60);
    },80);
    return chart;"""

assert h.count(OLD_RESIZE) == 1, f'❌ âncora resize: {h.count(OLD_RESIZE)}×'
h = h.replace(OLD_RESIZE, NEW_RESIZE)
print('✅ chart.update() após chart.resize() adicionado')

# ─────────────────────────────────────────────────────────────────────────────
# FIX 3: Aumentar delay dos init scripts 250ms → 600ms
# Garante que o DOM e Chart.js estão disponíveis antes do primeiro poll
# ─────────────────────────────────────────────────────────────────────────────
OLD_INIT_DELAY = '},250);'
NEW_INIT_DELAY = '},600);'

count = h.count(OLD_INIT_DELAY)
assert count == 7, f'❌ init scripts: {count} encontrados (esperado 7)'
h = h.replace(OLD_INIT_DELAY, NEW_INIT_DELAY)
print(f'✅ Delay dos init scripts: 250ms → 600ms ({count} scripts atualizados)')

# ─────────────────────────────────────────────────────────────────────────────
# FIX 4: Também disparar render na inicialização da aba Sell Out
# Procurar onde initSellOut ou o seletor inicial é configurado
# ─────────────────────────────────────────────────────────────────────────────
# Verificar se existe uma chamada inicial para switchSellOutClient no load
# Se não existir, adicionar dentro do bloco que inicializa o Sell Out

# Verificar se há initSellout ou similar
has_init_sellout = 'initSellout' in h or 'initSellOut' in h
has_switchsellout_init = h.count('switchSellOutClient(') > 1

print(f'\nStatus: initSellout={has_init_sellout}, switchSellOutClient calls={h.count("switchSellOutClient(")}')

# ─────────────────────────────────────────────────────────────────────────────
# FIX 5: Dentro do _acumTryRender, resetar attempt para 0 se não visível
#         mas clientId mudou (evitar stale retry de cliente anterior)
# Também: aumentar timeout de poll de 150ms → 100ms e limite de 60 → 80 tries
# ─────────────────────────────────────────────────────────────────────────────
OLD_TRY_RENDER = """  window._acumTryRender = function(cl, attempts){
    if(!attempts) attempts=0;
    if(attempts>60) return;
    if(typeof Chart==='undefined'||typeof SJ_REC==='undefined'){
      setTimeout(function(){ window._acumTryRender(cl,attempts+1); },100); return;
    }
    var cv=document.getElementById('acum-r-'+cl);
    if(!cv||cv.offsetWidth===0){
      setTimeout(function(){ window._acumTryRender(cl,attempts+1); },150); return;
    }
    window.renderAcumuladoFYClient(cl);
  };"""

NEW_TRY_RENDER = """  window._acumTryRender = function(cl, attempts){
    if(!attempts) attempts=0;
    if(attempts>80) return;
    if(typeof Chart==='undefined'||typeof SJ_REC==='undefined'){
      setTimeout(function(){ window._acumTryRender(cl,attempts+1); },100); return;
    }
    var cv=document.getElementById('acum-r-'+cl);
    if(!cv||cv.offsetWidth===0||cv.offsetHeight===0){
      setTimeout(function(){ window._acumTryRender(cl,attempts+1); },120); return;
    }
    window.renderAcumuladoFYClient(cl);
  };"""

assert h.count(OLD_TRY_RENDER) == 1, f'❌ âncora _acumTryRender: {h.count(OLD_TRY_RENDER)}×'
h = h.replace(OLD_TRY_RENDER, NEW_TRY_RENDER)
print('✅ _acumTryRender: limite 60→80 tries, 150ms→120ms, checa offsetHeight também')

# ─────────────────────────────────────────────────────────────────────────────
# Verificações
# ─────────────────────────────────────────────────────────────────────────────
assert '_acumTryRender(clientId, 0)' in h,    '❌ gatilho switchSellOutClient não encontrado'
assert 'chart.update()' in h,                  '❌ chart.update não encontrado'
assert '},600);' in h,                          '❌ delay 600ms não encontrado'
assert 'attempts>80' in h,                      '❌ limite 80 não encontrado'
assert 'offsetHeight===0' in h,                 '❌ offsetHeight check não encontrado'
for cl in ['saojoao','nissei','clamed','panvel','ddgam','ddgaucha','ddriomed']:
    assert f'acum-r-{cl}' in h, f'❌ canvas {cl} não encontrado'
print('✅ Todas as verificações OK')

print(f'\nTamanho original: {orig_len:,} | Novo: {len(h):,} | Δ: {len(h)-orig_len:+,}')

VER.parent.mkdir(parents=True, exist_ok=True)
VER.write_text(h, encoding='utf-8')
print(f'✅ Versão salva: {VER.name}')
SRC.write_text(h, encoding='utf-8')
print(f'✅ Base ativa atualizada: {SRC.name}')
print('DONE.')
