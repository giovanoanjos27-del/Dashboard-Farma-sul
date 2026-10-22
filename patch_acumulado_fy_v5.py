"""
patch_acumulado_fy_v5.py
Correção cirúrgica — card FY25 vs FY26 com filtro de compradora interno.

FIX 1: _acumCompr — estado interno de compradora por card
  Substitui dependência de sjModo/nsComprador por estado próprio do card.
  Padrão: saojoao='total', nissei='total'.

FIX 2: window.acumSetCompradora(cl, comp, btn)
  Nova função que troca o compradora do card e re-renderiza.
  Substitui acumSetMode (R$/Un) que não tinha mais utilidade.

FIX 3: _data saojoao — usa _acumCompr ao invés de sjModo
  Remove dependência externa (sjModo) da função de dados.

FIX 4: _data nissei — suporte a andre/edmar via _acumCompr
  Usa NS[_acumCompr['nissei']] para acessar dados do comprador correto.

FIX 5: renderAcumuladoFYClient — lbl dinâmico para SJ e Nissei
  Usa _acumCompr[cl] para gerar label correto para ambos os clientes.

FIX 6: SJ card — substituir R$/Un por [Total SJ][Isadora][Caroline]
FIX 7: Nissei card — substituir R$/Un por [Total NS][André][Edmar]
FIX 8: Outros 5 cards — remover toggle-group R$/Un (gráficos sempre duplos)
FIX 9: Remover triggers switchSJCompradora (v4) — card agora autônomo

NÃO ALTERA: outros gráficos, Nielsen, Sell In, Cobertura, Diagnóstico,
Plano Negócios, OLs, outros clientes, layout, medidas existentes.
"""
import sys
from pathlib import Path
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

BASE = Path(r'C:\Users\valqu\OneDrive\Documentos\Claude\Projects\projeto Dashboard_farma_sul\Dashboard_farma_sul')
SRC  = BASE / 'Dashboard_Farma_Sul_20260512_2220.html'
VER  = BASE / 'versoes' / f'Dashboard_Farma_Sul_{datetime.now().strftime("%Y%m%d_%H%M")}_AcumV5.html'

print('Lendo dashboard…')
h = SRC.read_text(encoding='utf-8')
orig_len = len(h)

# ─────────────────────────────────────────────────────────────────────────────
# FIX 1 + 2: Injetar _acumCompr state + acumSetCompradora na IIFE compartilhada
# ─────────────────────────────────────────────────────────────────────────────
OLD_IIFE_VARS = "  var _charts = {};   // { clientId: { r: chartR, v: chartV } }"

NEW_IIFE_VARS = """  var _charts = {};   // { clientId: { r: chartR, v: chartV } }
  var _acumCompr = { saojoao:'total', nissei:'total' }; // compradora ativa por card"""

assert h.count(OLD_IIFE_VARS) == 1, f'❌ âncora _charts: {h.count(OLD_IIFE_VARS)}×'
h = h.replace(OLD_IIFE_VARS, NEW_IIFE_VARS)
print('✅ FIX 1: _acumCompr state adicionado')

# Injetar acumSetCompradora antes do fechamento da IIFE (após acumSetMode)
OLD_IIFE_END = """      b.style.fontWeight=on?'700':'600';
    });
  };
})();
</script>"""

NEW_IIFE_END = """      b.style.fontWeight=on?'700':'600';
    });
  };
  /* Filtro de compradora interno do card FY (SJ: total/isadora/caroline · Nissei: total/andre/edmar) */
  window.acumSetCompradora = function(cl, comp, btn){
    _acumCompr[cl] = comp;
    var card = document.getElementById('card-acum-'+cl);
    if(card) card.querySelectorAll('[data-acumcompr]').forEach(function(b){
      var on = b.getAttribute('data-acumcompr') === comp;
      b.classList.toggle('active', on);
      b.style.color     = on ? '#fbbf24' : '#D1D5DB';
      b.style.background= on ? 'rgba(251,191,36,0.12)' : '#161B22';
      b.style.fontWeight= on ? '700' : '600';
    });
    window.renderAcumuladoFYClient(cl);
  };
})();
</script>"""

assert h.count(OLD_IIFE_END) == 1, f'❌ âncora IIFE end: {h.count(OLD_IIFE_END)}×'
h = h.replace(OLD_IIFE_END, NEW_IIFE_END)
print('✅ FIX 2: window.acumSetCompradora adicionado à IIFE')

# ─────────────────────────────────────────────────────────────────────────────
# FIX 3: _data saojoao — usar _acumCompr em vez de sjModo (externo)
# ─────────────────────────────────────────────────────────────────────────────
OLD_SJ_MODE = "      var _sjm=(typeof sjModo!=='undefined')?sjModo:'total';"
NEW_SJ_MODE = "      var _sjm=_acumCompr['saojoao']||'total';"

assert h.count(OLD_SJ_MODE) == 1, f'❌ âncora _sjm: {h.count(OLD_SJ_MODE)}×'
h = h.replace(OLD_SJ_MODE, NEW_SJ_MODE)
print('✅ FIX 3: _data saojoao usa _acumCompr[\'saojoao\'] em vez de sjModo')

# ─────────────────────────────────────────────────────────────────────────────
# FIX 4: _data nissei — suporte a andre/edmar via _acumCompr
# ─────────────────────────────────────────────────────────────────────────────
OLD_NS_DATA = """  } else if(cl==='nissei'){
      if(typeof NS!=='undefined'&&NS.total){
        _add(_fy(NS.total.rec['2024'],NS.total.rec['2025'],NS.total.rec['2026']),r25,r26);
        _add(_fy(NS.total.vol['2024'],NS.total.vol['2025'],NS.total.vol['2026']),v25,v26);
      }
    }"""

NEW_NS_DATA = """  } else if(cl==='nissei'){
      var _nsm=_acumCompr['nissei']||'total';
      var _nsd=(typeof NS!=='undefined')?(NS[_nsm]||NS.total):null;
      if(_nsd){
        _add(_fy(_nsd.rec['2024'],_nsd.rec['2025'],_nsd.rec['2026']),r25,r26);
        _add(_fy(_nsd.vol['2024'],_nsd.vol['2025'],_nsd.vol['2026']),v25,v26);
      }
    }"""

assert h.count(OLD_NS_DATA) == 1, f'❌ âncora nissei _data: {h.count(OLD_NS_DATA)}×'
h = h.replace(OLD_NS_DATA, NEW_NS_DATA)
print('✅ FIX 4: _data nissei usa _acumCompr[\'nissei\'] → NS.total/andre/edmar')

# ─────────────────────────────────────────────────────────────────────────────
# FIX 5: renderAcumuladoFYClient — lbl dinâmico para SJ e Nissei
# ─────────────────────────────────────────────────────────────────────────────
OLD_LBL_V4 = """    /* Label dinâmico: para SJ, usa compradora ativa */
    var _cMode=(cl==='saojoao'&&typeof sjModo!=='undefined')?sjModo:'total';
    var lbl=cl==='saojoao'
      ?(_cMode==='isadora'?'Compradora Isadora':_cMode==='caroline'?'Compradora Caroline':'São João Total')
      :(_LBL[cl]||cl);
    /* Atualizar subtitle do card */
    var _subEl=document.getElementById('acum-sub-'+cl);
    if(_subEl) _subEl.textContent='Faturamento Acumulado · Jul/24–Jun/25 vs Jul/25–Jun/26 · '+lbl;"""

NEW_LBL_V5 = """    /* Label dinâmico: usa compradora interna do card (_acumCompr) */
    var _cMode=_acumCompr[cl]||'total';
    var lbl=cl==='saojoao'
      ?(_cMode==='isadora'?'Compradora Isadora':_cMode==='caroline'?'Compradora Caroline':'São João Total')
      :(cl==='nissei'
        ?(_cMode==='andre'?'Nissei · André':_cMode==='edmar'?'Nissei · Edmar':'Nissei Total')
        :(_LBL[cl]||cl));
    /* Atualizar subtitle do card */
    var _subEl=document.getElementById('acum-sub-'+cl);
    if(_subEl) _subEl.textContent='Faturamento Acumulado · Jul/24–Jun/25 vs Jul/25–Jun/26 · '+lbl;"""

assert h.count(OLD_LBL_V4) == 1, f'❌ âncora lbl v4: {h.count(OLD_LBL_V4)}×'
h = h.replace(OLD_LBL_V4, NEW_LBL_V5)
print('✅ FIX 5: lbl dinâmico para SJ e Nissei via _acumCompr')

# ─────────────────────────────────────────────────────────────────────────────
# FIX 6: SJ card — toggle R$/Un → filtro [Total SJ][Isadora][Caroline]
# ─────────────────────────────────────────────────────────────────────────────
OLD_SJ_TOGGLE = """<div class="toggle-group">
          <button class="tgl active blue" data-acummode="rec" onclick="acumSetMode('saojoao','rec',this)">R$</button>
          <button class="tgl" data-acummode="vol" onclick="acumSetMode('saojoao','vol',this)">Un.</button>
        </div>"""

NEW_SJ_TOGGLE = """<div class="toggle-group">
          <button class="tgl active blue" data-acumcompr="total" onclick="acumSetCompradora('saojoao','total',this)" style="font-size:10px;padding:4px 9px;">Total SJ</button>
          <button class="tgl" data-acumcompr="isadora" onclick="acumSetCompradora('saojoao','isadora',this)" style="font-size:10px;padding:4px 9px;">Isadora</button>
          <button class="tgl" data-acumcompr="caroline" onclick="acumSetCompradora('saojoao','caroline',this)" style="font-size:10px;padding:4px 9px;">Caroline</button>
        </div>"""

assert h.count(OLD_SJ_TOGGLE) == 1, f'❌ âncora SJ toggle: {h.count(OLD_SJ_TOGGLE)}×'
h = h.replace(OLD_SJ_TOGGLE, NEW_SJ_TOGGLE)
print('✅ FIX 6: SJ card → filtro [Total SJ][Isadora][Caroline]')

# ─────────────────────────────────────────────────────────────────────────────
# FIX 7: Nissei card — toggle R$/Un → filtro [Total NS][André][Edmar]
# ─────────────────────────────────────────────────────────────────────────────
OLD_NS_TOGGLE = """<div class="toggle-group">
          <button class="tgl active blue" data-acummode="rec" onclick="acumSetMode('nissei','rec',this)">R$</button>
          <button class="tgl" data-acummode="vol" onclick="acumSetMode('nissei','vol',this)">Un.</button>
        </div>"""

NEW_NS_TOGGLE = """<div class="toggle-group">
          <button class="tgl active blue" data-acumcompr="total" onclick="acumSetCompradora('nissei','total',this)" style="font-size:10px;padding:4px 9px;">Total NS</button>
          <button class="tgl" data-acumcompr="andre" onclick="acumSetCompradora('nissei','andre',this)" style="font-size:10px;padding:4px 9px;">André</button>
          <button class="tgl" data-acumcompr="edmar" onclick="acumSetCompradora('nissei','edmar',this)" style="font-size:10px;padding:4px 9px;">Edmar</button>
        </div>"""

assert h.count(OLD_NS_TOGGLE) == 1, f'❌ âncora Nissei toggle: {h.count(OLD_NS_TOGGLE)}×'
h = h.replace(OLD_NS_TOGGLE, NEW_NS_TOGGLE)
print('✅ FIX 7: Nissei card → filtro [Total NS][André][Edmar]')

# ─────────────────────────────────────────────────────────────────────────────
# FIX 8: Remover toggle R$/Un dos outros 5 clientes (gráficos sempre duplos)
# ─────────────────────────────────────────────────────────────────────────────
other_clients = ['clamed', 'panvel', 'ddgam', 'ddgaucha', 'ddriomed']
for cl in other_clients:
    old_tg = (f'<div class="toggle-group">\n'
              f'          <button class="tgl active blue" data-acummode="rec" onclick="acumSetMode(\'{cl}\',\'rec\',this)">R$</button>\n'
              f'          <button class="tgl" data-acummode="vol" onclick="acumSetMode(\'{cl}\',\'vol\',this)">Un.</button>\n'
              f'        </div>')
    assert h.count(old_tg) == 1, f'❌ âncora {cl} toggle: {h.count(old_tg)}×'
    h = h.replace(old_tg, '')
    print(f'✅ FIX 8: {cl} toggle-group removido')

# ─────────────────────────────────────────────────────────────────────────────
# FIX 9: Remover triggers switchSJCompradora adicionados no v4 (card autônomo)
# ─────────────────────────────────────────────────────────────────────────────
OLD_V4_TRIGGER_CAROLINE = (
    "      /* Acumulado FY: re-renderizar com dados da Caroline */\n"
    "      if(typeof window._acumTryRender==='function') window._acumTryRender('saojoao',0);"
)
OLD_V4_TRIGGER_TOTAL = (
    "      /* Acumulado FY: re-renderizar com dados corretos (total ou isadora) */\n"
    "      if(typeof window._acumTryRender==='function') window._acumTryRender('saojoao',0);"
)

assert h.count(OLD_V4_TRIGGER_CAROLINE) == 1, f'❌ âncora v4 caroline trigger: {h.count(OLD_V4_TRIGGER_CAROLINE)}×'
assert h.count(OLD_V4_TRIGGER_TOTAL)    == 1, f'❌ âncora v4 total trigger: {h.count(OLD_V4_TRIGGER_TOTAL)}×'
h = h.replace(OLD_V4_TRIGGER_CAROLINE, '')
h = h.replace(OLD_V4_TRIGGER_TOTAL,    '')
print('✅ FIX 9: Triggers switchSJCompradora v4 removidos (card autônomo)')

# ─────────────────────────────────────────────────────────────────────────────
# Verificações finais
# ─────────────────────────────────────────────────────────────────────────────
assert "_acumCompr = { saojoao:'total', nissei:'total' }" in h, '❌ _acumCompr não encontrado'
assert "window.acumSetCompradora = function(cl, comp, btn)" in h, '❌ acumSetCompradora não encontrado'
assert "_acumCompr['saojoao']||'total'" in h,               '❌ _data SJ _acumCompr não encontrado'
assert "_acumCompr['nissei']||'total'" in h,                '❌ _data NS _acumCompr não encontrado'
assert "NS[_nsm]||NS.total" in h,                           '❌ NS[_nsm] não encontrado'
assert "data-acumcompr=\"caroline\"" in h,                  '❌ botão caroline não encontrado'
assert "data-acumcompr=\"edmar\"" in h,                     '❌ botão edmar não encontrado'
assert h.count("acumSetMode('clamed'") == 0,                '❌ toggle clamed ainda existe'
assert h.count("acumSetMode('panvel'") == 0,                '❌ toggle panvel ainda existe'
assert 'Nissei · André' in h,                               '❌ label André não encontrado'
assert 'Nissei · Edmar' in h,                               '❌ label Edmar não encontrado'
print('✅ Todas as verificações OK')

print(f'\nTamanho original: {orig_len:,} | Novo: {len(h):,} | Δ: {len(h)-orig_len:+,}')

VER.parent.mkdir(parents=True, exist_ok=True)
VER.write_text(h, encoding='utf-8')
print(f'✅ Versão salva: {VER.name}')
SRC.write_text(h, encoding='utf-8')
print(f'✅ Base ativa atualizada: {SRC.name}')
print('DONE.')
