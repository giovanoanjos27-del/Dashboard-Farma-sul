"""
patch_cobertura_filtro.py
=========================
Corrige dois problemas do card "COBERTURA POR ESTADO":

1. Filtro de provedor não atualizava o mapa
   → Adiciona _yoyCurProv para rastrear último provedor renderizado
   → Quando _yoySelProv muda, reseta _yoyMapInited e reconstrói o mapa
   → Com provedor filtrado: usa pv.by_uf (universo desse provedor)
   → Sem filtro: usa UF_COB_DATA (todos os provedores)

2. Universo por estado com filtro = universo DAQUELE provedor (pv.by_uf[total])
   Universo sem filtro = universo total todos provedores (UF_COB_DATA)
"""
import sys, shutil
sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path
from datetime import datetime

DASH = Path(r'C:\Users\valqu\OneDrive\Documentos\Claude\Projects\projeto Dashboard_farma_sul\Dashboard_farma_sul\Dashboard_Farma_Sul_20260512_2220.html')
VER  = DASH.parent / 'versoes'
DL   = Path.home() / 'Downloads'
ts   = datetime.now().strftime('%Y%m%d_%H%M')

shutil.copy(DASH, VER / f'Dashboard_Farma_Sul_{ts}_PreCobFiltro.html')
h = DASH.read_text(encoding='utf-8')
print(f'Backup: ...PreCobFiltro.html  |  {len(h):,} chars')

def replace_once(html, old, new, label):
    cnt = html.count(old)
    assert cnt == 1, f'ERRO [{label}]: {cnt}x encontrado'
    print(f'✓ {label}')
    return html.replace(old, new, 1)

# ═══════════════════════════════════════════════════════════════════════════════
# 1. Adicionar variável _yoyCurProv perto de _yoyMapInited
# ═══════════════════════════════════════════════════════════════════════════════
OLD1 = (
    'var _yoyUfAgg      = null;  /* cache do ufAgg — computado uma vez */\n'
    'var _yoyMapInited  = false; /* flag: mapa fixo já renderizado */'
)
NEW1 = (
    'var _yoyUfAgg      = null;  /* cache do ufAgg — computado uma vez */\n'
    'var _yoyMapInited  = false; /* flag: mapa fixo já renderizado */\n'
    "var _yoyCurProv    = '__ALL__'; /* provedor que o mapa exibe atualmente */"
)
h = replace_once(h, OLD1, NEW1, '_yoyCurProv adicionado')

# ═══════════════════════════════════════════════════════════════════════════════
# 2. Atualizar _yoyBuildUfAgg() para suportar filtro de provedor
# ═══════════════════════════════════════════════════════════════════════════════
OLD2 = (
    'function _yoyBuildUfAgg(){\n'
    '  /* Usa UF_COB_DATA — fonte: positivação ano 2024x2025x2026.xlsx\n'
    '     FY25 = Jul/24–Abr/25  |  FY26 = Jul/25–Abr/26\n'
    '     CNPJs únicos deduplicados por provedor (todos os provedores SCJ) */\n'
    "  var _cobData = (typeof UF_COB_DATA !== 'undefined') ? UF_COB_DATA : {};\n"
    '  var agg = {};\n'
    '  Object.keys(_cobData).forEach(function(uf){\n'
    '    var r = _cobData[uf];\n'
    '    if(!r.universe) return;\n'
    '    var yoyD = r.fy25 > 0 ? Math.round((r.fy26 - r.fy25) / r.fy25 * 100) : 0;\n'
    '    agg[uf] = {\n'
    '      total:    r.universe,   /* universo IQVIA ativo */\n'
    '      scj:      r.fy26,       /* positivados FY26 */\n'
    '      scj_fy25: r.fy25,       /* positivados FY25 */\n'
    '      reconq:   r.reconq,     /* FY25 ativo, sem FY26 — alta prioridade */\n'
    '      ws_puro:  r.ws_puro,    /* nunca comprou — white space puro */\n'
    '      white_sp: r.white_sp,   /* disponíveis p/ atendimento (= univ - FY26) */\n'
    '      yoy_gap:  yoyD           /* Δ% FY25→FY26 */\n'
    '    };\n'
    '  });\n'
    '  return agg;\n'
    '}'
)

NEW2 = r"""function _yoyBuildUfAgg(provName){
  /* Se provName fornecido: filtra para aquele provedor (usa pv.by_uf do PROV_DATA)
     Se não: usa UF_COB_DATA (todos os provedores, positivação 2024x2025x2026.xlsx) */
  var agg = {};

  if(provName){
    /* ── Modo provedor filtrado ── */
    var pv = null;
    for(var _i=0; _i<(PROV_DATA||[]).length; _i++){
      if(PROV_DATA[_i].name === provName){ pv = PROV_DATA[_i]; break; }
    }
    if(pv && pv.by_uf){
      (pv.by_uf).forEach(function(u){
        var uf = u[0], tot = u[1]||0, scj = u[2]||0;
        if(!tot) return;
        agg[uf] = {
          total:    tot,       /* universo deste provedor neste estado */
          scj:      scj,       /* CNPJs SCJ ativos neste provedor */
          scj_fy25: 0,         /* não disponível por provedor */
          reconq:   0,
          ws_puro:  0,
          white_sp: tot - scj, /* disponíveis = universo provedor − SCJ */
          yoy_gap:  null,
          _prov_mode: true
        };
      });
    }
    return agg;
  }

  /* ── Modo todos os provedores — UF_COB_DATA ── */
  var _cobData = (typeof UF_COB_DATA !== 'undefined') ? UF_COB_DATA : {};
  Object.keys(_cobData).forEach(function(uf){
    var r = _cobData[uf];
    if(!r.universe) return;
    var yoyD = r.fy25 > 0 ? Math.round((r.fy26 - r.fy25) / r.fy25 * 100) : 0;
    agg[uf] = {
      total:    r.universe,
      scj:      r.fy26,
      scj_fy25: r.fy25,
      reconq:   r.reconq,
      ws_puro:  r.ws_puro,
      white_sp: r.white_sp,
      yoy_gap:  yoyD,
      _prov_mode: false
    };
  });
  return agg;
}"""

h = replace_once(h, OLD2, NEW2, '_yoyBuildUfAgg com suporte a filtro de provedor')

# ═══════════════════════════════════════════════════════════════════════════════
# 3. Atualizar _yoyEnsureMap() para detectar mudança de provedor e reconstruir
# ═══════════════════════════════════════════════════════════════════════════════
OLD3 = (
    '/* ── Garante que o mapa fixo está renderizado (executa apenas uma vez) ── */\n'
    'function _yoyEnsureMap(){\n'
    '  if(_yoyMapInited) return;\n'
    "  if(typeof PROV_DATA === 'undefined') return;\n"
    '\n'
    '  _yoyUfAgg = _yoyBuildUfAgg();\n'
    '\n'
    "  var mapWrap = document.getElementById('yoy-map-fixed');\n"
    '  if(!mapWrap) return;\n'
    '\n'
    "  var _activeUFs = Object.keys(_yoyUfAgg).filter(function(uf){ return _yoyUfAgg[uf].scj > 0; });\n"
    '\n'
    '  var _yoyLegendItems = [\n'
    "    {c:'#34d399',l:'≥70%'},{c:'#fbbf24',l:'40–69%'},\n"
    "    {c:'#f97316',l:'20–39%'},{c:'#ef4444',l:'<20%'},\n"
    "    {c:'#334155',l:'Fora da área',border:true}\n"
    '  ];\n'
    "  var _yoyLegendHtml = '<div style=\"display:flex;gap:14px;margin-top:10px;flex-wrap:wrap;align-items:center;padding:0 2px;\">'\n"
    '    +_yoyLegendItems.map(function(it){\n'
    "      return '<span style=\"display:flex;align-items:center;gap:4px;font-size:9px;color:#94A3B8;\">'\n"
    "        +'<span style=\"display:inline-block;width:10px;height:10px;border-radius:2px;background:'+it.c+';'+(it.border?'border:1px solid #4a5568;':'')+';\"> </span>'+it.l+'</span>';\n"
    '    }).join(\'\')\n'
    "    +'<span style=\"margin-left:auto;font-size:9px;color:#3d6b63;font-style:italic;\">Clique em um estado para ver detalhes</span>'\n"
    "    +'</div>';\n"
    '\n'
    '  mapWrap.innerHTML =\n'
    "    '<div style=\"background:rgba(0,0,0,0.2);border-radius:8px;padding:12px 14px;\">'\n"
    "    +'<div style=\"font-size:9px;font-weight:700;letter-spacing:0.1em;color:#94A3B8;margin-bottom:10px;\">'\n"
    "      +'COBERTURA POR ESTADO — TODOS OS PROVEDORES'\n"
    "      +'<span style=\"color:#3d6b63;font-weight:400;\"> · '+_activeUFs.length+' estados ativos</span>'\n"
    "    +'</div>'\n"
    "    +'<div style=\"display:grid;grid-template-columns:1.6fr 1fr;gap:12px;align-items:stretch;\">'\n"
    "      +'<div id=\"yoy-agg-map\" style=\"height:100%;min-height:360px;border-radius:8px;overflow:hidden;background:#0a1218;\"></div>'\n"
    "      +'<div id=\"yoy-agg-drill\" style=\"background:#161B22;border-radius:8px;padding:14px;border:0.5px solid rgba(103,232,249,0.12);display:flex;align-items:center;justify-content:center;min-height:360px;\">'\n"
    "        +'<span style=\"font-size:11px;color:#334155;font-style:italic;text-align:center;\">← Clique em um<br>estado para ver<br>os detalhes</span>'\n"
    "      +'</div>'\n"
    "    +'</div>'\n"
    '    +_yoyLegendHtml\n'
    "    +'</div>';\n"
    '\n'
    '  mapWrap.style.display = \'block\';\n'
    '  _yoyMapInited = true;\n'
    '  setTimeout(function(){ _yoyInitAggMap(_yoyUfAgg); }, 120);\n'
    '}'
)

NEW3 = r"""/* ── Garante mapa fixo — reconstrói se o filtro de provedor mudou ── */
function _yoyEnsureMap(){
  var _reqProv = _yoySelProv || '__ALL__';
  /* Só recria se não inicializado ou se o provedor mudou */
  if(_yoyMapInited && _yoyCurProv === _reqProv) return;
  if(typeof PROV_DATA === 'undefined') return;

  /* Destruir instância Leaflet anterior se houver */
  if(_yoyAggMap){ try{_yoyAggMap.remove();}catch(e){} _yoyAggMap=null; _yoyAggMapBrGeo=null; }

  _yoyCurProv = _reqProv;
  _yoyUfAgg   = _yoyBuildUfAgg(_yoySelProv || null);

  var mapWrap = document.getElementById('yoy-map-fixed');
  if(!mapWrap) return;

  var _activeUFs = Object.keys(_yoyUfAgg).filter(function(uf){ return _yoyUfAgg[uf].scj > 0; });
  var _isProv = !!_yoySelProv;
  var _headerTitle = _isProv
    ? 'COBERTURA POR ESTADO — <span style="color:#67e8f9;">'+_yoySelProv+'</span>'
    : 'COBERTURA POR ESTADO — TODOS OS PROVEDORES';

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
      +_headerTitle
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
}"""

# Substituição por slice (evita problemas de escape em strings longas)
ANCHOR_S = '\n/* ── Garante que o mapa fixo'
ANCHOR_E = '\n/* ── Entry point ── */'
_s3 = h.find(ANCHOR_S); _e3 = h.find(ANCHOR_E, _s3)
assert _s3 != -1 and _e3 != -1, f'ERRO: anchors _yoyEnsureMap não encontrados s={_s3} e={_e3}'
h = h[:_s3] + '\n' + NEW3 + '\n' + h[_e3:]
print('✓ _yoyEnsureMap com detecção de mudança de provedor')

# ═══════════════════════════════════════════════════════════════════════════════
# 4. Atualizar _yoyAggUfClick() para mostrar versão reduzida no modo provedor
#    (sem FY25/reconq/cidades — dados não disponíveis por provedor)
# ═══════════════════════════════════════════════════════════════════════════════
OLD4 = (
    "        +'<div style=\"font-size:7px;color:#94A3B8;text-transform:uppercase;letter-spacing:.06em;margin-bottom:2px;\">✅ Positivados FY26</div>'\n"
    "        +'<div style=\"font-size:18px;font-weight:800;color:#34d399;\">'+scj26.toLocaleString('pt-BR')+'</div>'\n"
    "        +'<div style=\"font-size:7px;color:#334155;\">'+pct+'% · Jul/25–Abr/26</div>'\n"
    "      +'</div>'"
)
NEW4 = (
    "        +'<div style=\"font-size:7px;color:#94A3B8;text-transform:uppercase;letter-spacing:.06em;margin-bottom:2px;\">✅ '+(!d._prov_mode?'Positivados FY26':'SCJ Ativos')+'</div>'\n"
    "        +'<div style=\"font-size:18px;font-weight:800;color:#34d399;\">'+scj26.toLocaleString('pt-BR')+'</div>'\n"
    "        +'<div style=\"font-size:7px;color:#334155;\">'+pct+'% · '+(d._prov_mode?'deste provedor':'Jul/25–Abr/26')+'</div>'\n"
    "      +'</div>'"
)
h = replace_once(h, OLD4, NEW4, 'KPI FY26 adaptado para modo provedor')

# Ocultar KPIs de FY25/reconq/ws_puro/GAP quando em modo provedor (dados N/D)
OLD5 = (
    "      /* 3. Positivados FY25 */\n"
    "      +'<div style=\"'+_kpiStyle+'background:rgba(59,130,246,0.07);\">'\n"
    "        +'<div style=\"font-size:7px;color:#94A3B8;text-transform:uppercase;letter-spacing:.06em;margin-bottom:2px;\">✅ Positivados FY25</div>'\n"
    "        +'<div style=\"font-size:18px;font-weight:800;color:#93c5fd;\">'+scj25.toLocaleString('pt-BR')+'</div>'\n"
    "        +'<div style=\"font-size:7px;color:#334155;\">'+pct25+'% · Jul/24–Abr/25</div>'\n"
    "      +'</div>'"
)
NEW5 = (
    "      /* 3. Positivados FY25 — oculto no modo provedor */\n"
    "      +(!d._prov_mode\n"
    "        ? '<div style=\"'+_kpiStyle+'background:rgba(59,130,246,0.07);\">'\n"
    "            +'<div style=\"font-size:7px;color:#94A3B8;text-transform:uppercase;letter-spacing:.06em;margin-bottom:2px;\">✅ Positivados FY25</div>'\n"
    "            +'<div style=\"font-size:18px;font-weight:800;color:#93c5fd;\">'+scj25.toLocaleString('pt-BR')+'</div>'\n"
    "            +'<div style=\"font-size:7px;color:#334155;\">'+pct25+'% · Jul/24–Abr/25</div>'\n"
    "          +'</div>'\n"
    "        : '')"
)
h = replace_once(h, OLD5, NEW5, 'KPI FY25 condicionado ao modo all-provedores')

# Ocultar Não Compraram / Nunca Comprou / GAP quando modo provedor
OLD6 = (
    "      /* 5. Não Compraram FY26 */\n"
    "      +'<div style=\"'+_kpiStyle+'background:rgba(251,191,36,0.07);\">'\n"
    "        +'<div style=\"font-size:7px;color:#94A3B8;text-transform:uppercase;letter-spacing:.06em;margin-bottom:2px;\">🔄 Não Compraram FY26</div>'\n"
    "        +'<div style=\"font-size:18px;font-weight:800;color:#fbbf24;\">'+(d.reconq||0).toLocaleString('pt-BR')+'</div>'\n"
    "        +'<div style=\"font-size:7px;color:#334155;\">'+rqPct+'% · FY25 sim · FY26 não</div>'\n"
    "      +'</div>'\n"
    "\n"
    "      /* 6. Nunca Comprou */\n"
    "      +'<div style=\"'+_kpiStyle+'background:rgba(148,163,184,0.07);\">'\n"
    "        +'<div style=\"font-size:7px;color:#94A3B8;text-transform:uppercase;letter-spacing:.06em;margin-bottom:2px;\">📭 Nunca Comprou SCJ</div>'\n"
    "        +'<div style=\"font-size:18px;font-weight:800;color:#94a3b8;\">'+(d.ws_puro||0).toLocaleString('pt-BR')+'</div>'\n"
    "        +'<div style=\"font-size:7px;color:#334155;\">Sem FY25 e sem FY26</div>'\n"
    "      +'</div>'"
)
NEW6 = (
    "      /* 5. Não Compraram FY26 — só no modo todos provedores */\n"
    "      +(!d._prov_mode\n"
    "        ? '<div style=\"'+_kpiStyle+'background:rgba(251,191,36,0.07);\">'\n"
    "            +'<div style=\"font-size:7px;color:#94A3B8;text-transform:uppercase;letter-spacing:.06em;margin-bottom:2px;\">🔄 Não Compraram FY26</div>'\n"
    "            +'<div style=\"font-size:18px;font-weight:800;color:#fbbf24;\">'+(d.reconq||0).toLocaleString('pt-BR')+'</div>'\n"
    "            +'<div style=\"font-size:7px;color:#334155;\">'+rqPct+'% · FY25 sim · FY26 não</div>'\n"
    "          +'</div>'\n"
    "        : '')\n"
    "\n"
    "      /* 6. Nunca Comprou — só no modo todos provedores */\n"
    "      +(!d._prov_mode\n"
    "        ? '<div style=\"'+_kpiStyle+'background:rgba(148,163,184,0.07);\">'\n"
    "            +'<div style=\"font-size:7px;color:#94A3B8;text-transform:uppercase;letter-spacing:.06em;margin-bottom:2px;\">📭 Nunca Comprou SCJ</div>'\n"
    "            +'<div style=\"font-size:18px;font-weight:800;color:#94a3b8;\">'+(d.ws_puro||0).toLocaleString('pt-BR')+'</div>'\n"
    "            +'<div style=\"font-size:7px;color:#334155;\">Sem FY25 e sem FY26</div>'\n"
    "          +'</div>'\n"
    "        : '')"
)
h = replace_once(h, OLD6, NEW6, 'KPIs Reconq/WS condicionados ao modo all-provedores')

# GAP condicional
OLD7 = (
    "      /* 8. GAP FY25→FY26 */\n"
    "      +'<div style=\"'+_kpiStyle+'border-left:2px solid '+yoyCol+';background:rgba(100,116,139,0.06);\">'\n"
    "        +'<div style=\"font-size:7px;color:#94A3B8;text-transform:uppercase;letter-spacing:.06em;margin-bottom:2px;\">📈 GAP FY25→FY26</div>'\n"
    "        +'<div style=\"font-size:22px;font-weight:900;color:'+yoyCol+';line-height:1;\">'+(yoyD===null?'—':(yoyD>=0?'+':'')+yoyD+'%')+'</div>'\n"
    "        +'<div style=\"font-size:7px;color:#334155;margin-top:2px;\">'+(yoyD!==null?(yoyD>5?'▲ Crescimento':yoyD>=-5?'→ Estável':'▼ Queda em positivação'):'Sem dado FY25')+'</div>'\n"
    "      +'</div>'"
)
NEW7 = (
    "      /* 8. GAP FY25→FY26 — só no modo todos provedores */\n"
    "      +(!d._prov_mode\n"
    "        ? '<div style=\"'+_kpiStyle+'border-left:2px solid '+yoyCol+';background:rgba(100,116,139,0.06);\">'\n"
    "            +'<div style=\"font-size:7px;color:#94A3B8;text-transform:uppercase;letter-spacing:.06em;margin-bottom:2px;\">📈 GAP FY25→FY26</div>'\n"
    "            +'<div style=\"font-size:22px;font-weight:900;color:'+yoyCol+';line-height:1;\">'+(yoyD===null?'—':(yoyD>=0?'+':'')+yoyD+'%')+'</div>'\n"
    "            +'<div style=\"font-size:7px;color:#334155;margin-top:2px;\">'+(yoyD!==null?(yoyD>5?'▲ Crescimento':yoyD>=-5?'→ Estável':'▼ Queda em positivação'):'Sem dado FY25')+'</div>'\n"
    "          +'</div>'\n"
    "        : '')"
)
h = replace_once(h, OLD7, NEW7, 'KPI GAP condicionado ao modo all-provedores')

# Tabela cidades: ocultar no modo provedor
OLD8 = (
    "    /* ── Top Cidades ── */\n"
    "    +(_cityCob.length > 0\n"
    "      ? '<div style=\"margin-top:2px;\">'\n"
    "          +'<div style=\"font-size:7.5px;font-weight:700;color:#64748b;letter-spacing:.08em;text-transform:uppercase;margin-bottom:6px;\">'\n"
    "            +'📍 TOP CIDADES — '+uf\n"
    "          +'</div>'\n"
    "          +_cityRows\n"
    "          +'<div style=\"font-size:7px;color:#1e3a4a;margin-top:5px;font-style:italic;\">'\n"
    "            +'Fonte: positivação 2024x2025x2026 · top 20 cidades por universo'\n"
    "          +'</div>'\n"
    "        +'</div>'\n"
    "      : '')"
)
NEW8 = (
    "    /* ── Top Cidades — só no modo todos provedores ── */\n"
    "    +(!d._prov_mode && _cityCob.length > 0\n"
    "      ? '<div style=\"margin-top:2px;\">'\n"
    "          +'<div style=\"font-size:7.5px;font-weight:700;color:#64748b;letter-spacing:.08em;text-transform:uppercase;margin-bottom:6px;\">'\n"
    "            +'📍 TOP CIDADES — '+uf\n"
    "          +'</div>'\n"
    "          +_cityRows\n"
    "          +'<div style=\"font-size:7px;color:#1e3a4a;margin-top:5px;font-style:italic;\">'\n"
    "            +'Fonte: positivação 2024x2025x2026 · top 20 cidades por universo'\n"
    "          +'</div>'\n"
    "        +'</div>'\n"
    "      : '')"
)
h = replace_once(h, OLD8, NEW8, 'Tabela cidades condicionada ao modo all-provedores')

# ═══════════════════════════════════════════════════════════════════════════════
# Verificações
# ═══════════════════════════════════════════════════════════════════════════════
assert '_yoyCurProv'                       in h, 'ERRO: _yoyCurProv não declarado'
assert '_reqProv = _yoySelProv'            in h, 'ERRO: _reqProv não inserido'
assert '_yoyCurProv === _reqProv'          in h, 'ERRO: comparação _yoyCurProv ausente'
assert '_yoyBuildUfAgg(_yoySelProv'        in h, 'ERRO: chamada _yoyBuildUfAgg com filtro'
assert "provName"                          in h, 'ERRO: parâmetro provName ausente'
assert "d._prov_mode"                      in h, 'ERRO: _prov_mode não referenciado'
assert '_isProv'                           in h, 'ERRO: _isProv ausente'
assert 'prov-yoy-body'                     in h, 'ERRO: prov-yoy-body perdido'
assert h.count('function renderProvYoYCard') == 1, 'ERRO: renderProvYoYCard duplicada'
print('Verificações: OK')
print(f'Tamanho final: {len(h):,} chars')

# ═══════════════════════════════════════════════════════════════════════════════
# Salvar
# ═══════════════════════════════════════════════════════════════════════════════
DASH.write_text(h, encoding='utf-8')
shutil.copy(DASH, VER / f'Dashboard_Farma_Sul_{ts}_CobFiltro.html')
shutil.copy(DASH, DL  / f'Dashboard_FarmaSul_Giovano_{ts}.html')
print(f'Versao:    Dashboard_Farma_Sul_{ts}_CobFiltro.html')
print(f'Downloads: Dashboard_FarmaSul_Giovano_{ts}.html')
print('DONE.')
