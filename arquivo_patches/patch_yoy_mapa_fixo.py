"""
patch_yoy_mapa_fixo.py
======================
Move o mapa de cobertura por estado para um container fixo FORA do prov-yoy-body,
para que não seja substituído quando um provedor é filtrado.

Estrutura ANTES:
  prov-yoy-card
  └── prov-yoy-body  ← innerHTML substituído ao filtrar
      ├── KPI strip
      ├── [mapa + drill panel]   ← some ao filtrar provedor
      └── tabela / detalhe provedor

Estrutura DEPOIS:
  prov-yoy-card
  ├── [mapa + drill panel] id="yoy-map-fixed"  ← FIXO, nunca substituído
  └── prov-yoy-body  ← innerHTML substituído ao filtrar
      ├── KPI strip
      └── tabela / detalhe provedor
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

# ═══════════════════════════════════════════════════════════════════════════════
# 1) HTML estático: inserir div#yoy-map-fixed ANTES de prov-yoy-body
# ═══════════════════════════════════════════════════════════════════════════════
OLD_BODY_DIV = '      <div id="prov-yoy-body">'
assert h.count(OLD_BODY_DIV) == 1, f'prov-yoy-body não único: {h.count(OLD_BODY_DIV)}x'

NEW_BODY_DIV = (
    '      <!-- Mapa fixo: nunca substituído, inicializado uma vez -->\n'
    '      <div id="yoy-map-fixed" style="display:none;margin-bottom:14px;"></div>\n\n'
    '      <div id="prov-yoy-body">'
)
h = h.replace(OLD_BODY_DIV, NEW_BODY_DIV, 1)
print('✓ div#yoy-map-fixed inserido antes de prov-yoy-body')

# ═══════════════════════════════════════════════════════════════════════════════
# 2) JS: adicionar variáveis de controle do mapa fixo
# ═══════════════════════════════════════════════════════════════════════════════
OLD_MAP_VARS = 'var _yoyAggMap     = null;\nvar _yoyAggMapBrGeo= null;'
assert h.count(OLD_MAP_VARS) == 1, 'vars do mapa não encontradas'

NEW_MAP_VARS = (
    'var _yoyAggMap     = null;\n'
    'var _yoyAggMapBrGeo= null;\n'
    'var _yoyUfAgg      = null;  /* cache do ufAgg — computado uma vez */\n'
    'var _yoyMapInited  = false; /* flag: mapa fixo já renderizado */'
)
h = h.replace(OLD_MAP_VARS, NEW_MAP_VARS, 1)
print('✓ variáveis _yoyUfAgg e _yoyMapInited adicionadas')

# ═══════════════════════════════════════════════════════════════════════════════
# 3) Extrair ufAgg de _yoyRenderRanking para função separada _yoyBuildUfAgg()
#    e remover mapHtml do innerHTML de _yoyRenderRanking
# ═══════════════════════════════════════════════════════════════════════════════

# --- 3a) Substituir bloco de cálculo de ufAgg e mapHtml em _yoyRenderRanking ---
OLD_MAP_BLOCK = (
    '  /* ── Cobertura por Estado — dados reais CNPJ (UF_SCJ_DATA) + YoY PROV_DATA ── */\n'
    '  /* Fase 1: fy25/fy26 PDV-meses do PROV_DATA (prorate por share SCJ por estado) */\n'
    '  var _ufFy = {};\n'
    '  (PROV_DATA||[]).forEach(function(pv){\n'
    '    var _m = pv.monthly || [];\n'
    '    var _pFy25 = 0, _pFy26 = 0;\n'
    '    for(var _i=3;  _i<=11; _i++) _pFy25 += (_m[_i]||0);\n'
    '    for(var _i=15; _i<=23; _i++) _pFy26 += (_m[_i]||0);\n'
    '    var _pScjTot = 0;\n'
    '    (pv.by_uf||[]).forEach(function(u){ _pScjTot += u[2]||0; });\n'
    '    (pv.by_uf||[]).forEach(function(u){\n'
    '      var uf = u[0], scj = u[2]||0;\n'
    '      if(!_ufFy[uf]) _ufFy[uf] = {fy25:0, fy26:0};\n'
    '      var _share = _pScjTot > 0 ? scj / _pScjTot : 0;\n'
    '      _ufFy[uf].fy25 += _pFy25 * _share;\n'
    '      _ufFy[uf].fy26 += _pFy26 * _share;\n'
    '    });\n'
    '  });\n'
    '  /* Fase 2: ufAgg usa UF_SCJ_DATA (dados reais CNPJ-nível, Detalhe RB+CIMED) */\n'
    '  var _ufSCJ = (typeof UF_SCJ_DATA !== "undefined") ? UF_SCJ_DATA : {};\n'
    '  var ufAgg = {};\n'
    '  Object.keys(_ufSCJ).forEach(function(uf){\n'
    '    var r = _ufSCJ[uf];\n'
    '    if(!r.universe) return;\n'
    '    var fy = _ufFy[uf] || {fy25:0, fy26:0};\n'
    '    ufAgg[uf] = {\n'
    '      total:    r.universe,\n'
    '      scj:      r.scj_fy26,\n'
    '      scj_fy25: r.scj_fy25,\n'
    '      reconq:   r.reconq,\n'
    '      ws_puro:  r.ws_puro,\n'
    '      white_sp: r.white_sp,\n'
    '      fy25:     fy.fy25,\n'
    '      fy26:     fy.fy26\n'
    '    };\n'
    '  });\n'
    '  var _activeUFs = Object.keys(ufAgg).filter(function(uf){ return ufAgg[uf].scj > 0; });'
)

assert h.count(OLD_MAP_BLOCK) == 1, f'OLD_MAP_BLOCK não único: {h.count(OLD_MAP_BLOCK)}x'

NEW_MAP_BLOCK = (
    '  /* ── Usa ufAgg do cache (computado por _yoyEnsureMap) ── */\n'
    '  var ufAgg = _yoyUfAgg || {};\n'
    '  var _activeUFs = Object.keys(ufAgg).filter(function(uf){ return ufAgg[uf].scj > 0; });'
)
h = h.replace(OLD_MAP_BLOCK, NEW_MAP_BLOCK, 1)
print('✓ ufAgg em _yoyRenderRanking substituído por referência ao cache')

# --- 3b) Remover mapHtml e setTimeout do _yoyRenderRanking ---
OLD_MAP_HTML = (
    '  var _yoyLegendItems = [\n'
    '    {c:\'#34d399\',l:\'≥70%\'},{c:\'#fbbf24\',l:\'40–69%\'},\n'
    '    {c:\'#f97316\',l:\'20–39%\'},{c:\'#ef4444\',l:\'<20%\'},\n'
    '    {c:\'#334155\',l:\'Fora da área\',border:true}\n'
    '  ];\n'
    '  var _yoyLegendHtml = \'<div style="display:flex;gap:14px;margin-top:10px;flex-wrap:wrap;align-items:center;padding:0 2px;">\'\n'
    '    +_yoyLegendItems.map(function(it){\n'
    '      return \'<span style="display:flex;align-items:center;gap:4px;font-size:9px;color:#94A3B8;">\'\n'
    '        +\'<span style="display:inline-block;width:10px;height:10px;border-radius:2px;background:\'+it.c+\';\'+\(it.border?\'border:1px solid #4a5568;\':\'\'\)+\'">\\u00a0</span>\'+it.l+\'</span>\';\n'
    '    }).join(\'\')\n'
    '    +\'<span style="margin-left:auto;font-size:9px;color:#3d6b63;font-style:italic;">Clique em um estado para ver detalhes</span>\'\n'
    '    +\'</div>\';\n'
    '\n'
    '  var mapHtml = \'<div style="background:rgba(0,0,0,0.2);border-radius:8px;padding:12px 14px;margin-bottom:14px;">\'\n'
    '    +\'<div style="font-size:9px;font-weight:700;letter-spacing:0.1em;color:#94A3B8;margin-bottom:10px;">\'\n'
    '      +\'COBERTURA POR ESTADO — TODOS OS PROVEDORES\'\n'
    '      +\'<span style="color:#3d6b63;font-weight:400;"> · \'+_activeUFs.length+\' estados ativos</span>\'\n'
    '    +\'</div>\'\n'
    '    +\'<div style="display:grid;grid-template-columns:1.6fr 1fr;gap:12px;align-items:stretch;">\'\n'
    '      +\'<div id="yoy-agg-map" style="height:100%;min-height:360px;border-radius:8px;overflow:hidden;background:#0a1218;"></div>\'\n'
    '      +\'<div id="yoy-agg-drill" style="background:#161B22;border-radius:8px;padding:14px;border:0.5px solid rgba(103,232,249,0.12);display:flex;align-items:center;justify-content:center;min-height:360px;">\'\n'
    '        +\'<span style="font-size:11px;color:#334155;font-style:italic;text-align:center;">← Clique em um<br>estado para ver<br>os detalhes</span>\'\n'
    '      +\'</div>\'\n'
    '    +\'</div>\'\n'
    '    +_yoyLegendHtml\n'
    '    +\'</div>\';\n'
    '\n'
    '  bodyEl.innerHTML=kpi+mapHtml+table+btnAll;\n'
    '\n'
    '  /* Inicializar mapa após DOM estar pronto */\n'
    '  setTimeout(function(){ _yoyInitAggMap(ufAgg); }, 120);\n'
    '}'
)

assert h.count(OLD_MAP_HTML) == 1, f'OLD_MAP_HTML não único: {h.count(OLD_MAP_HTML)}x'

NEW_MAP_HTML = (
    '  bodyEl.innerHTML=kpi+table+btnAll;\n'
    '}'
)
h = h.replace(OLD_MAP_HTML, NEW_MAP_HTML, 1)
print('✓ mapHtml removido de _yoyRenderRanking (mapa será fixo em yoy-map-fixed)')

# ═══════════════════════════════════════════════════════════════════════════════
# 4) Adicionar função _yoyEnsureMap() e _yoyBuildUfAgg() antes do entry point
#    e atualizar renderProvYoYCard() para chamar _yoyEnsureMap()
# ═══════════════════════════════════════════════════════════════════════════════
OLD_ENTRY = (
    '/* ── Entry point ── */\n'
    'function renderProvYoYCard(){\n'
    '  var bodyEl=document.getElementById(\'prov-yoy-body\');\n'
    '  if(!bodyEl||typeof PROV_DATA===\'undefined\') return;\n'
    '\n'
    '  if(_yoySelProv){\n'
    '    var p=null;\n'
    '    for(var i=0;i<PROV_DATA.length;i++){if(PROV_DATA[i].name===_yoySelProv){p=PROV_DATA[i];break;}}\n'
    '    if(p){ _yoyRenderDetail(p,bodyEl); return; }\n'
    '  }\n'
    '  _yoyRenderRanking(bodyEl);\n'
    '}'
)
assert h.count(OLD_ENTRY) == 1, f'OLD_ENTRY não único: {h.count(OLD_ENTRY)}x'

NEW_ENTRY = r"""/* ── Computa ufAgg uma vez e mantém em cache ── */
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
        +'<span style="display:inline-block;width:10px;height:10px;border-radius:2px;background:'+it.c+';'+(it.border?'border:1px solid #4a5568;':'')+'">&nbsp;</span>'+it.l+'</span>';
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

  /* Garante mapa fixo — só executa na primeira vez */
  _yoyEnsureMap();

  if(_yoySelProv){
    var p=null;
    for(var i=0;i<PROV_DATA.length;i++){if(PROV_DATA[i].name===_yoySelProv){p=PROV_DATA[i];break;}}
    if(p){ _yoyRenderDetail(p,bodyEl); return; }
  }
  _yoyRenderRanking(bodyEl);
}"""

h = h.replace(OLD_ENTRY, NEW_ENTRY, 1)
print('✓ _yoyBuildUfAgg + _yoyEnsureMap + renderProvYoYCard atualizados')

# ═══════════════════════════════════════════════════════════════════════════════
# Verificações
# ═══════════════════════════════════════════════════════════════════════════════
assert 'id="yoy-map-fixed"'        in h,  'ERRO: div yoy-map-fixed não inserido'
assert '_yoyMapInited'              in h,  'ERRO: _yoyMapInited não declarado'
assert 'function _yoyBuildUfAgg'    in h,  'ERRO: _yoyBuildUfAgg não inserido'
assert 'function _yoyEnsureMap'     in h,  'ERRO: _yoyEnsureMap não inserido'
assert '_yoyEnsureMap()'            in h,  'ERRO: _yoyEnsureMap não chamada'
assert 'bodyEl.innerHTML=kpi+table+btnAll' in h, 'ERRO: _yoyRenderRanking sem mapa'
assert 'prov-yoy-body'              in h,  'ERRO: prov-yoy-body perdido'
assert h.count('function renderProvYoYCard') == 1, 'ERRO: renderProvYoYCard duplicada'
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
