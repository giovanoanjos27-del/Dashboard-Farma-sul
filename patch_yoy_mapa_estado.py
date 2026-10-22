"""
patch_yoy_mapa_estado.py
========================
Substitui o bloco de barras TOP 10 do _yoyRenderRanking() pelo mapa
interativo Leaflet choropleth (igual ao COBERTURA POR ESTADO do GPF),
agregando dados de todos os 157 provedores de PROV_DATA.

O que faz:
  1. Remove o bloco de barras ufTop10Html anterior (patch_yoy_cob_estado)
  2. Insere mapa Leaflet com grid 1.6fr/1fr (mapa + painel drill)
  3. Adiciona funções: _yoyAggMap, _yoyInitAggMap(), _yoyAggUfClick()
  4. Clique no estado → painel direito com métricas do estado
     (Universo total, SCJ ativos, White Space, Provedores ativos)
"""
import sys, shutil
sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path
from datetime import datetime

DASH = Path(r'C:\Users\valqu\OneDrive\Documentos\Claude\Projects\projeto Dashboard_farma_sul\Dashboard_farma_sul\Dashboard_Farma_Sul_20260512_2220.html')
VER  = DASH.parent / 'versoes'
DL   = Path.home() / 'Downloads'
ts   = datetime.now().strftime('%Y%m%d_%H%M')

shutil.copy(DASH, VER / f'Dashboard_Farma_Sul_{ts}_PreYoyMapa.html')
h = DASH.read_text(encoding='utf-8')
print(f'Backup: ...PreYoyMapa.html  |  {len(h):,} chars')

# ── 1) Substituir bloco ufAgg/ufTop10Html pelo bloco de mapa ─────────────────
OLD_RANKING_END = (
  '  /* ── Cobertura por Estado — Agregado de todos os provedores ── */\n'
  '  var ufAgg = {};\n'
  '  (PROV_DATA||[]).forEach(function(p){\n'
  '    (p.by_uf||[]).forEach(function(u){\n'
  '      var uf = u[0], tot = u[1]||0, scj = u[2]||0;\n'
  '      if(!ufAgg[uf]) ufAgg[uf] = {total:0, scj:0};\n'
  '      ufAgg[uf].total += tot;\n'
  '      ufAgg[uf].scj   += scj;\n'
  '    });\n'
  '  });\n'
  '  var ufArr = Object.keys(ufAgg).map(function(uf){\n'
  '    var d = ufAgg[uf];\n'
  '    var pct = d.total > 0 ? Math.round(d.scj / d.total * 100) : 0;\n'
  '    return {uf:uf, total:d.total, scj:d.scj, pct:pct};\n'
  "  }).sort(function(a,b){ return b.total - a.total; }).slice(0,10);\n"
)

assert h.count(OLD_RANKING_END) == 1, f'Anchor início não-única: {h.count(OLD_RANKING_END)}x'

# Também localizamos o final (bodyEl.innerHTML)
OLD_BODY_LINE = '  bodyEl.innerHTML=kpi+ufTop10Html+table+btnAll;\n}'
assert h.count(OLD_BODY_LINE) == 1, f'Anchor fim não-única: {h.count(OLD_BODY_LINE)}x'

# Find start and end positions
start = h.find(OLD_RANKING_END)
# Find OLD_BODY_LINE after start
end   = h.find(OLD_BODY_LINE, start) + len(OLD_BODY_LINE)

NEW_RANKING_END = r"""  /* ── Cobertura por Estado — Mapa Leaflet agregado ── */
  var ufAgg = {};
  (PROV_DATA||[]).forEach(function(pv){
    (pv.by_uf||[]).forEach(function(u){
      var uf = u[0], tot = u[1]||0, scj = u[2]||0;
      if(!ufAgg[uf]) ufAgg[uf] = {total:0, scj:0};
      ufAgg[uf].total += tot;
      ufAgg[uf].scj   += scj;
    });
  });
  var _activeUFs = Object.keys(ufAgg).filter(function(uf){ return ufAgg[uf].scj > 0; });

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

  var mapHtml = '<div style="background:rgba(0,0,0,0.2);border-radius:8px;padding:12px 14px;margin-bottom:14px;">'
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

  bodyEl.innerHTML=kpi+mapHtml+table+btnAll;

  /* Inicializar mapa após DOM estar pronto */
  setTimeout(function(){ _yoyInitAggMap(ufAgg); }, 120);
}"""

h = h[:start] + NEW_RANKING_END + h[end:]
print('Bloco ufTop10Html → mapa Leaflet substituído em _yoyRenderRanking()')

# ── 2) Injetar funções _yoyInitAggMap e _yoyAggUfClick após _yoyRenderRanking ─
AFTER_ANCHOR = '\n/* ── Entry point ── */'
assert h.count(AFTER_ANCHOR) >= 1, f'Entry point não encontrado'

NEW_FUNCS = r"""
/* ═══════════════════════════════════════════════════════════════════════
   YoY Aggregate Map — Leaflet choropleth com dados de todos os provedores
   Instância separada de _gpfMap para evitar conflitos de container.
═══════════════════════════════════════════════════════════════════════ */
var _yoyAggMap     = null;
var _yoyAggMapBrGeo= null;

function _yoyInitAggMap(ufAgg){
  /* Destruir instância anterior */
  if(_yoyAggMap){ try{_yoyAggMap.remove();}catch(e){} _yoyAggMap=null; _yoyAggMapBrGeo=null; }

  /* Garantir GeoJSON EDM carregado */
  _gpfPreloadEDMData();

  if(typeof window.EDM_BR_GEO === 'undefined' || typeof window.EDM_IBGE === 'undefined'){
    setTimeout(function(){ _yoyInitAggMap(ufAgg); }, 600);
    return;
  }

  var el = document.getElementById('yoy-agg-map');
  if(!el || typeof L === 'undefined') return;

  function stateColor(uf){
    var d = ufAgg[uf];
    if(!d || d.total === 0) return '#1e3a4a';
    var pct = Math.round(d.scj / d.total * 100);
    return pct>=70?'#34d399':pct>=40?'#fbbf24':pct>=20?'#f97316':'#ef4444';
  }

  _yoyAggMap = L.map(el, {center:[-15,-52], zoom:4, zoomControl:false, attributionControl:false});
  L.control.zoom({position:'bottomright'}).addTo(_yoyAggMap);

  var _edmGeo  = window.EDM_BR_GEO;
  var _edmIbge = window.EDM_IBGE;

  _yoyAggMapBrGeo = L.geoJSON(_edmGeo, {
    style: function(f){
      var uf     = _edmIbge[String(f.properties.codarea)];
      var d      = uf && ufAgg[uf];
      var active = d && d.scj > 0;
      return {
        fillColor:   uf ? stateColor(uf) : '#1e3a4a',
        fillOpacity: active ? 0.85 : 0.25,
        color: 'rgba(255,255,255,0.18)',
        weight: 1
      };
    },
    onEachFeature: function(f, lyr){
      var uf  = _edmIbge[String(f.properties.codarea)];
      if(!uf) return;
      var d   = ufAgg[uf];
      var pct = d && d.total > 0 ? Math.round(d.scj / d.total * 100) : null;
      var pctCol = pct!=null ? (pct>=40?'#fbbf24':'#f97316') : '#334155';
      var active = !!(d && d.scj > 0);

      /* Tooltip */
      var ttip = '<div style="min-width:140px;font-family:inherit">'
        +'<div style="font-weight:800;font-size:12px;margin-bottom:5px;color:#D1D5DB;">'+uf+'</div>';
      if(d && d.total > 0){
        ttip += '<table style="font-size:10px;border-collapse:collapse;width:100%">'
          +'<tr><td style="color:#94A3B8;padding:1px 0">Total PDVs</td><td style="text-align:right;color:#D1D5DB;font-weight:700">'+d.total.toLocaleString('pt-BR')+'</td></tr>'
          +'<tr><td style="color:#94A3B8;padding:1px 0">SCJ Ativos</td><td style="text-align:right;color:#34d399;font-weight:700">'+d.scj.toLocaleString('pt-BR')+'</td></tr>'
          +'<tr><td style="color:#94A3B8;padding:1px 0">Cobertura</td><td style="text-align:right;font-weight:800;color:'+pctCol+'">'+(pct!==null?pct+'%':'—')+'</td></tr>'
          +'<tr><td style="color:#94A3B8;padding:1px 0">White Space</td><td style="text-align:right;color:#ef4444;font-weight:700">'+(d.total-d.scj).toLocaleString('pt-BR')+'</td></tr>'
          +'</table>';
        if(active) ttip += '<div style="margin-top:5px;font-size:9px;color:#4a6b65;">▶ Clique para detalhes</div>';
      } else {
        ttip += '<div style="font-size:10px;color:#334155;">Fora da área de cobertura</div>';
      }
      ttip += '</div>';

      lyr.bindTooltip(ttip, {sticky:true, opacity:1, className:'gpf-map-tip'});
      lyr.on({
        mouseover: function(e){
          if(active){ e.target.setStyle({fillOpacity:1, weight:2, color:'#06b6d4'}); e.target.bringToFront(); }
        },
        mouseout: function(e){ if(_yoyAggMapBrGeo) _yoyAggMapBrGeo.resetStyle(e.target); },
        click:    function(){ if(active) _yoyAggUfClick(uf, d); }
      });
    }
  }).addTo(_yoyAggMap);

  /* Labels UF + % */
  var lblLyr = L.layerGroup();
  _yoyAggMapBrGeo.eachLayer(function(lyr){
    var uf  = _edmIbge[String(lyr.feature.properties.codarea)];
    if(!uf) return;
    var d   = ufAgg[uf];
    var pct = d && d.total > 0 ? Math.round(d.scj / d.total * 100) : null;
    var center = lyr.getBounds().getCenter();
    L.marker(center, {
      icon: L.divIcon({
        className: '',
        html: '<div style="color:#fff;font-size:8px;font-weight:800;letter-spacing:.04em;'
          +'text-shadow:0 0 4px #000,0 0 5px #000;'
          +'white-space:nowrap;pointer-events:none;text-align:center;'
          +'transform:translate(-50%,-50%);line-height:1.4">'
          +uf+(pct!==null?'<br><span style="font-size:7px;opacity:0.92">'+pct+'%</span>':'')
          +'</div>',
        iconSize:[30,22], iconAnchor:[15,11]
      }),
      interactive:false, keyboard:false
    }).addTo(lblLyr);
  });
  lblLyr.addTo(_yoyAggMap);

  /* Fit bounds — duplo pass para resolver 0-size no primeiro frame */
  setTimeout(function(){
    if(!_yoyAggMap) return;
    _yoyAggMap.invalidateSize(true);
    if(_yoyAggMapBrGeo) _yoyAggMap.fitBounds(_yoyAggMapBrGeo.getBounds(), {padding:[15,15]});
    setTimeout(function(){
      if(!_yoyAggMap) return;
      _yoyAggMap.invalidateSize(true);
      if(_yoyAggMapBrGeo) _yoyAggMap.fitBounds(_yoyAggMapBrGeo.getBounds(), {padding:[15,15]});
    }, 400);
  }, 500);
}

function _yoyAggUfClick(uf, d){
  var drill = document.getElementById('yoy-agg-drill');
  if(!drill) return;

  var pct    = d.total > 0 ? Math.round(d.scj / d.total * 100) : 0;
  var pctCol = pct>=70?'#34d399':pct>=40?'#fbbf24':pct>=20?'#f97316':'#ef4444';
  var ws     = d.total - d.scj;
  var wsPct  = d.total > 0 ? Math.round(ws / d.total * 100) : 0;

  /* Provedores ativos neste estado */
  var provsInUF = (PROV_DATA||[]).filter(function(pv){
    return (pv.by_uf||[]).some(function(u){ return u[0]===uf && u[2]>0; });
  });

  var html = '<div style="width:100%;padding:4px;">'
    /* Header UF + % */
    +'<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px;">'
      +'<div style="font-size:24px;font-weight:800;color:#67e8f9;">'+uf+'</div>'
      +'<div style="text-align:right;">'
        +'<div style="font-size:26px;font-weight:900;color:'+pctCol+';">'+pct+'%</div>'
        +'<div style="font-size:8px;color:#94A3B8;">cobertura SCJ</div>'
      +'</div>'
    +'</div>'

    /* Barra de cobertura */
    +'<div style="display:flex;height:16px;border-radius:4px;overflow:hidden;gap:1px;margin-bottom:5px;">'
      +'<div style="width:'+pct+'%;background:'+pctCol+';"></div>'
      +'<div style="flex:1;background:#1e3a4a;"></div>'
    +'</div>'
    +'<div style="display:flex;gap:10px;margin-bottom:14px;">'
      +'<span style="font-size:8px;color:'+pctCol+';">■ SCJ '+pct+'%</span>'
      +'<span style="font-size:8px;color:#4a5568;">■ White Space '+wsPct+'%</span>'
    +'</div>'

    /* 2×2 metric cards */
    +'<div style="display:grid;grid-template-columns:1fr 1fr;gap:7px;">'
      +'<div style="background:rgba(103,232,249,0.06);border-radius:6px;padding:9px 10px;">'
        +'<div style="font-size:7.5px;color:#94A3B8;margin-bottom:3px;text-transform:uppercase;letter-spacing:.06em;">🏪 Universo Total</div>'
        +'<div style="font-size:20px;font-weight:800;color:#67e8f9;">'+d.total.toLocaleString('pt-BR')+'</div>'
        +'<div style="font-size:8px;color:#334155;margin-top:2px;">PDVs únicos</div>'
      +'</div>'
      +'<div style="background:rgba(34,197,94,0.06);border-radius:6px;padding:9px 10px;">'
        +'<div style="font-size:7.5px;color:#94A3B8;margin-bottom:3px;text-transform:uppercase;letter-spacing:.06em;">✅ SCJ Ativos</div>'
        +'<div style="font-size:20px;font-weight:800;color:#34d399;">'+d.scj.toLocaleString('pt-BR')+'</div>'
        +'<div style="font-size:8px;color:#334155;margin-top:2px;">comprando SCJ</div>'
      +'</div>'
      +'<div style="background:rgba(239,68,68,0.06);border-radius:6px;padding:9px 10px;">'
        +'<div style="font-size:7.5px;color:#94A3B8;margin-bottom:3px;text-transform:uppercase;letter-spacing:.06em;">⬜ White Space</div>'
        +'<div style="font-size:20px;font-weight:800;color:#ef4444;">'+ws.toLocaleString('pt-BR')+'</div>'
        +'<div style="font-size:8px;color:#334155;margin-top:2px;">PDVs sem SCJ</div>'
      +'</div>'
      +'<div style="background:rgba(251,191,36,0.06);border-radius:6px;padding:9px 10px;">'
        +'<div style="font-size:7.5px;color:#94A3B8;margin-bottom:3px;text-transform:uppercase;letter-spacing:.06em;">🏬 Provedores</div>'
        +'<div style="font-size:20px;font-weight:800;color:#fbbf24;">'+provsInUF.length+'</div>'
        +'<div style="font-size:8px;color:#334155;margin-top:2px;">ativos neste estado</div>'
      +'</div>'
    +'</div>'
    +'</div>';

  drill.style.cssText = 'background:#161B22;border-radius:8px;padding:14px;'
    +'border:0.5px solid rgba(103,232,249,0.12);min-height:360px;overflow-y:auto;';
  drill.innerHTML = html;
}

"""

# Inject before "/* ── Entry point ── */"
first_entry = h.find(AFTER_ANCHOR)
assert first_entry != -1, 'Entry point não encontrado'
h = h[:first_entry] + NEW_FUNCS + h[first_entry:]
print('Funções _yoyInitAggMap() e _yoyAggUfClick() injetadas')

# ── Verificações ──────────────────────────────────────────────────────────────
assert 'yoy-agg-map'      in h, 'ERRO: div yoy-agg-map não encontrado'
assert 'yoy-agg-drill'    in h, 'ERRO: div yoy-agg-drill não encontrado'
assert '_yoyInitAggMap'   in h, 'ERRO: função _yoyInitAggMap não inserida'
assert '_yoyAggUfClick'   in h, 'ERRO: função _yoyAggUfClick não inserida'
assert '_yoyAggMap'       in h, 'ERRO: variável _yoyAggMap não inserida'
assert 'ufTop10Html'  not in h, 'AVISO: ufTop10Html antigo ainda presente'
assert 'prov-yoy-body'    in h, 'ERRO: prov-yoy-body perdido'
print('Verificações: OK')
print(f'Tamanho final: {len(h):,} chars')

# ── Salvar ────────────────────────────────────────────────────────────────────
DASH.write_text(h, encoding='utf-8')
shutil.copy(DASH, VER / f'Dashboard_Farma_Sul_{ts}_YoyMapa.html')
shutil.copy(DASH, DL  / f'Dashboard_FarmaSul_Giovano_{ts}.html')
print(f'Versao:    Dashboard_Farma_Sul_{ts}_YoyMapa.html')
print(f'Downloads: Dashboard_FarmaSul_Giovano_{ts}.html')
print('DONE.')
