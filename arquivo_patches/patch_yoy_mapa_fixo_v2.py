"""
patch_yoy_mapa_fixo_v2.py
=========================
Move o mapa de cobertura por estado para um container fixo FORA do prov-yoy-body,
para que não seja substituído quando um provedor é filtrado.

Estratégia: usa find()+slice para evitar problemas de escape em strings longas.
"""
import sys, shutil
sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path
from datetime import datetime

DASH = Path(r'C:\Users\valqu\OneDrive\Documentos\Claude\Projects\projeto Dashboard_farma_sul\Dashboard_farma_sul\Dashboard_Farma_Sul_20260512_2220.html')
VER  = DASH.parent / 'versoes'
DL   = Path.home() / 'Downloads'
ts   = datetime.now().strftime('%Y%m%d_%H%M')

shutil.copy(DASH, VER / f'Dashboard_Farma_Sul_{ts}_PreMapaFixo.html')
h = DASH.read_text(encoding='utf-8')
print(f'Backup: ...PreMapaFixo.html  |  {len(h):,} chars')

# ───────────────────────────────────────────────────────────────────────────────
# Helper: substituição com verificação de unicidade
# ───────────────────────────────────────────────────────────────────────────────
def replace_once(html, old, new, label):
    cnt = html.count(old)
    assert cnt == 1, f'ERRO [{label}]: {cnt}x encontrado (esperado 1x)'
    result = html.replace(old, new, 1)
    print(f'✓ {label}')
    return result

# ═══════════════════════════════════════════════════════════════════════════════
# 1) HTML estático: inserir div#yoy-map-fixed ANTES de prov-yoy-body
# ═══════════════════════════════════════════════════════════════════════════════
OLD1 = '      <div id="prov-yoy-body">'
NEW1 = (
    '      <!-- Mapa fixo: nunca substituído, inicializado uma vez -->\n'
    '      <div id="yoy-map-fixed" style="display:none;margin-bottom:14px;"></div>\n\n'
    '      <div id="prov-yoy-body">'
)
h = replace_once(h, OLD1, NEW1, 'div#yoy-map-fixed inserido')

# ═══════════════════════════════════════════════════════════════════════════════
# 2) JS: adicionar variáveis de controle do mapa fixo
# ═══════════════════════════════════════════════════════════════════════════════
OLD2 = 'var _yoyAggMap     = null;\nvar _yoyAggMapBrGeo= null;'
NEW2 = (
    'var _yoyAggMap     = null;\n'
    'var _yoyAggMapBrGeo= null;\n'
    'var _yoyUfAgg      = null;  /* cache do ufAgg — computado uma vez */\n'
    'var _yoyMapInited  = false; /* flag: mapa fixo já renderizado */'
)
h = replace_once(h, OLD2, NEW2, 'variáveis _yoyUfAgg/_yoyMapInited adicionadas')

# ═══════════════════════════════════════════════════════════════════════════════
# 3) Substituir ufAgg + mapHtml + setTimeout em _yoyRenderRanking
#    Âncora: do comentário até o } de fechamento da função
#    Usa find()+slice para evitar problemas com escapes
# ═══════════════════════════════════════════════════════════════════════════════
ANCHOR_START = '  /* ── Cobertura por Estado — dados reais CNPJ (UF_SCJ_DATA) + YoY PROV_DATA ── */'
ANCHOR_END   = '  setTimeout(function(){ _yoyInitAggMap(ufAgg); }, 120);\n}'

idx_s = h.find(ANCHOR_START)
assert idx_s != -1, 'ERRO: ANCHOR_START não encontrado'
idx_e = h.find(ANCHOR_END, idx_s)
assert idx_e != -1, 'ERRO: ANCHOR_END não encontrado'
idx_e += len(ANCHOR_END)  # incluir o } de fechamento

OLD3 = h[idx_s:idx_e]
# Verificar unicidade
assert h.count(OLD3) == 1, f'ERRO: bloco OLD3 não único ({h.count(OLD3)}x)'

NEW3 = (
    '  /* ── Usa ufAgg do cache (computado por _yoyEnsureMap) ── */\n'
    '  var ufAgg = _yoyUfAgg || {};\n'
    '  var _activeUFs = Object.keys(ufAgg).filter(function(uf){ return ufAgg[uf].scj > 0; });\n'
    '\n'
    '  bodyEl.innerHTML=kpi+table+btnAll;\n'
    '}'
)
h = h[:idx_s] + NEW3 + h[idx_e:]
print('✓ ufAgg + mapHtml + setTimeout removidos de _yoyRenderRanking')

# ═══════════════════════════════════════════════════════════════════════════════
# 4) Inserir _yoyBuildUfAgg + _yoyEnsureMap + renderProvYoYCard atualizado
#    (substitui o antigo entry point)
# ═══════════════════════════════════════════════════════════════════════════════
OLD4 = (
    '/* ── Entry point ── */\n'
    'function renderProvYoYCard(){\n'
    "  var bodyEl=document.getElementById('prov-yoy-body');\n"
    "  if(!bodyEl||typeof PROV_DATA==='undefined') return;\n"
    '\n'
    '  if(_yoySelProv){\n'
    '    var p=null;\n'
    "    for(var i=0;i<PROV_DATA.length;i++){if(PROV_DATA[i].name===_yoySelProv){p=PROV_DATA[i];break;}}\n"
    '    if(p){ _yoyRenderDetail(p,bodyEl); return; }\n'
    '  }\n'
    '  _yoyRenderRanking(bodyEl);\n'
    '}'
)

NEW4 = r"""/* ── Computa ufAgg uma vez e mantém em cache ── */
function _yoyBuildUfAgg(){
  var _ufFy = {};
  (PROV_DATA||[]).forEach(function(pv){
    var _m = pv.monthly || [];
    var _pFy25 = 0, _pFy26 = 0;
    for(var _i=3;  _i<=11; _i++) _pFy25 += (_m[_i]||0);
    for(var _i=15; _i<=23; _i++) _pFy26 += (_m[_i]||0);
    var _pScjTot = 0;
    (pv.by_uf||[]).forEach(function(u){ _pScjTot += u[2]||0; });
    (pv.by_uf||[]).forEach(function(u){
      var uf = u[0], scj = u[2]||0;
      if(!_ufFy[uf]) _ufFy[uf] = {fy25:0, fy26:0};
      var _share = _pScjTot > 0 ? scj / _pScjTot : 0;
      _ufFy[uf].fy25 += _pFy25 * _share;
      _ufFy[uf].fy26 += _pFy26 * _share;
    });
  });
  var _ufSCJ = (typeof UF_SCJ_DATA !== 'undefined') ? UF_SCJ_DATA : {};
  var agg = {};
  Object.keys(_ufSCJ).forEach(function(uf){
    var r = _ufSCJ[uf];
    if(!r.universe) return;
    var fy = _ufFy[uf] || {fy25:0, fy26:0};
    agg[uf] = {
      total:    r.universe,
      scj:      r.scj_fy26,
      scj_fy25: r.scj_fy25,
      reconq:   r.reconq,
      ws_puro:  r.ws_puro,
      white_sp: r.white_sp,
      fy25:     fy.fy25,
      fy26:     fy.fy26
    };
  });
  return agg;
}

/* ── Garante que o mapa fixo está renderizado (executa apenas uma vez) ── */
function _yoyEnsureMap(){
  if(_yoyMapInited) return;
  if(typeof PROV_DATA === 'undefined') return;

  _yoyUfAgg = _yoyBuildUfAgg();

  var mapWrap = document.getElementById('yoy-map-fixed');
  if(!mapWrap) return;

  var _activeUFs = Object.keys(_yoyUfAgg).filter(function(uf){ return _yoyUfAgg[uf].scj > 0; });

  var _yoyLegendItems = [
    {c:'#34d399',l:'≥70%'},{c:'#fbbf24',l:'40–69%'},
    {c:'#f97316',l:'20–39%'},{c:'#ef4444',l:'<20%'},
    {c:'#334155',l:'Fora da área',border:true}
  ];
  var _yoyLegendHtml = '<div style="display:flex;gap:14px;margin-top:10px;flex-wrap:wrap;align-items:center;padding:0 2px;">'
    +_yoyLegendItems.map(function(it){
      return '<span style="display:flex;align-items:center;gap:4px;font-size:9px;color:#94A3B8;">'
        +'<span style="display:inline-block;width:10px;height:10px;border-radius:2px;background:'+it.c+';'+(it.border?'border:1px solid #4a5568;':'')+'"> </span>'+it.l+'</span>';
    }).join('')
    +'<span style="margin-left:auto;font-size:9px;color:#3d6b63;font-style:italic;">Clique em um estado para ver detalhes</span>'
    +'</div>';

  mapWrap.innerHTML =
    '<div style="background:rgba(0,0,0,0.2);border-radius:8px;padding:12px 14px;">'
    +'<div style="font-size:9px;font-weight:700;letter-spacing:0.1em;color:#94A3B8;margin-bottom:10px;">'
      +'COBERTURA POR ESTADO — TODOS OS PROVEDORES'
      +'<span style="color:#3d6b63;font-weight:400;"> · '+_activeUFs.length+' estados ativos</span>'
    +'</div>'
    +'<div style="display:grid;grid-template-columns:1.6fr 1fr;gap:12px;align-items:stretch;">'
      +'<div id="yoy-agg-map" style="height:100%;min-height:360px;border-radius:8px;overflow:hidden;background:#0a1218;"></div>'
      +'<div id="yoy-agg-drill" style="background:#161B22;border-radius:8px;padding:14px;border:0.5px solid rgba(103,232,249,0.12);display:flex;align-items:center;justify-content:center;min-height:360px;">'
        +'<span style="font-size:11px;color:#334155;font-style:italic;text-align:center;">← Clique em um<br>estado para ver<br>os detalhes</span>'
      +'</div>'
    +'</div>'
    +_yoyLegendHtml
    +'</div>';

  mapWrap.style.display = 'block';
  _yoyMapInited = true;
  setTimeout(function(){ _yoyInitAggMap(_yoyUfAgg); }, 120);
}

/* ── Entry point ── */
function renderProvYoYCard(){
  var bodyEl=document.getElementById('prov-yoy-body');
  if(!bodyEl||typeof PROV_DATA==='undefined') return;

  /* Garante mapa fixo — só renderiza na primeira chamada */
  _yoyEnsureMap();

  if(_yoySelProv){
    var p=null;
    for(var i=0;i<PROV_DATA.length;i++){if(PROV_DATA[i].name===_yoySelProv){p=PROV_DATA[i];break;}}
    if(p){ _yoyRenderDetail(p,bodyEl); return; }
  }
  _yoyRenderRanking(bodyEl);
}"""

h = replace_once(h, OLD4, NEW4, '_yoyBuildUfAgg + _yoyEnsureMap + renderProvYoYCard atualizados')

# ═══════════════════════════════════════════════════════════════════════════════
# Verificações finais
# ═══════════════════════════════════════════════════════════════════════════════
assert 'id="yoy-map-fixed"'                          in h, 'ERRO: yoy-map-fixed não inserido'
assert '_yoyMapInited'                               in h, 'ERRO: _yoyMapInited ausente'
assert 'function _yoyBuildUfAgg'                     in h, 'ERRO: _yoyBuildUfAgg ausente'
assert 'function _yoyEnsureMap'                      in h, 'ERRO: _yoyEnsureMap ausente'
assert '_yoyEnsureMap();'                            in h, 'ERRO: _yoyEnsureMap não chamada'
assert 'bodyEl.innerHTML=kpi+table+btnAll;'          in h, 'ERRO: _yoyRenderRanking sem mapa'
assert 'bodyEl.innerHTML=kpi+mapHtml+table+btnAll;' not in h, 'ERRO: mapHtml ainda no ranking'
assert h.count('function renderProvYoYCard') == 1,         'ERRO: renderProvYoYCard duplicada'
assert 'prov-yoy-body'                               in h, 'ERRO: prov-yoy-body perdido'
assert 'scj25.toLocaleString'                        in h, 'ERRO: bloco YoY drill perdido'
print('Verificações: OK')
print(f'Tamanho final: {len(h):,} chars')

# ═══════════════════════════════════════════════════════════════════════════════
# Salvar
# ═══════════════════════════════════════════════════════════════════════════════
DASH.write_text(h, encoding='utf-8')
shutil.copy(DASH, VER / f'Dashboard_Farma_Sul_{ts}_MapaFixo.html')
shutil.copy(DASH, DL  / f'Dashboard_FarmaSul_Giovano_{ts}.html')
print(f'Versao:    Dashboard_Farma_Sul_{ts}_MapaFixo.html')
print(f'Downloads: Dashboard_FarmaSul_Giovano_{ts}.html')
print('DONE.')
