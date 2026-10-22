"""
patch_mapa_labels.py
====================
Corrige dois problemas visuais do mapa COBERTURA POR ESTADO:

1. Mapa não renderiza completamente (parte inferior preta)
   → Troca height:100% por altura fixa 460px no container do mapa
   → Adiciona terceiro pass de invalidateSize/fitBounds (1200ms)

2. Labels UF + % muito pequenas e sem cor por cobertura
   → UF: 8px → 12px, font-weight 800→900, branca com sombra forte
   → %: 7px → 10px, cor dinâmica igual à do estado (verde/âmbar/laranja/vermelho)
   → iconSize [30,22] → [50,30], iconAnchor [15,11] → [25,15]
"""
import sys, shutil
sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path
from datetime import datetime

DASH = Path(r'C:\Users\valqu\OneDrive\Documentos\Claude\Projects\projeto Dashboard_farma_sul\Dashboard_farma_sul\Dashboard_Farma_Sul_20260512_2220.html')
VER  = DASH.parent / 'versoes'
DL   = Path.home() / 'Downloads'
ts   = datetime.now().strftime('%Y%m%d_%H%M')

shutil.copy(DASH, VER / f'Dashboard_Farma_Sul_{ts}_PreMapaLabels.html')
h = DASH.read_text(encoding='utf-8')
print(f'Backup: ...PreMapaLabels.html  |  {len(h):,} chars')

def replace_once(html, old, new, label):
    cnt = html.count(old)
    assert cnt == 1, f'ERRO [{label}]: {cnt}x encontrado'
    print(f'✓ {label}')
    return html.replace(old, new, 1)

# ═══════════════════════════════════════════════════════════════════════════════
# 1. Corrigir altura do container do mapa: height:100% → 460px (fixo)
#    Isso garante que o Leaflet sempre saiba o tamanho exato ao inicializar
# ═══════════════════════════════════════════════════════════════════════════════
OLD1 = (
    "+'<div id=\"yoy-agg-map\" style=\"height:100%;min-height:360px;"
    "border-radius:8px;overflow:hidden;background:#0a1218;\"></div>'"
)
NEW1 = (
    "+'<div id=\"yoy-agg-map\" style=\"height:460px;"
    "border-radius:8px;overflow:hidden;background:#0a1218;\"></div>'"
)
h = replace_once(h, OLD1, NEW1, 'Altura mapa fixada em 460px')

# ═══════════════════════════════════════════════════════════════════════════════
# 2. Labels UF + % — mais visíveis com cor dinâmica por cobertura
# ═══════════════════════════════════════════════════════════════════════════════
OLD2 = (
    '  /* Labels UF + % */\n'
    '  var lblLyr = L.layerGroup();\n'
    '  _yoyAggMapBrGeo.eachLayer(function(lyr){\n'
    '    var uf  = _edmIbge[String(lyr.feature.properties.codarea)];\n'
    '    if(!uf) return;\n'
    '    var d   = ufAgg[uf];\n'
    '    var pct = d && d.total > 0 ? Math.round(d.scj / d.total * 100) : null;\n'
    '    var center = lyr.getBounds().getCenter();\n'
    '    L.marker(center, {\n'
    '      icon: L.divIcon({\n'
    "        className: '',\n"
    "        html: '<div style=\"color:#fff;font-size:8px;font-weight:800;letter-spacing:.04em;'\n"
    "          +'text-shadow:0 0 4px #000,0 0 5px #000;'\n"
    "          +'white-space:nowrap;pointer-events:none;text-align:center;'\n"
    "          +'transform:translate(-50%,-50%);line-height:1.4\">'\n"
    "          +uf+(pct!==null?'<br><span style=\"font-size:7px;opacity:0.92\">'+pct+'%</span>':'')\n"
    "          +'</div>',\n"
    '        iconSize:[30,22], iconAnchor:[15,11]\n'
    '      }),\n'
    '      interactive:false, keyboard:false\n'
    '    }).addTo(lblLyr);\n'
    '  });\n'
    '  lblLyr.addTo(_yoyAggMap);'
)

NEW2 = (
    '  /* Labels UF + % — tamanho maior e cor por cobertura */\n'
    '  var lblLyr = L.layerGroup();\n'
    '  _yoyAggMapBrGeo.eachLayer(function(lyr){\n'
    '    var uf  = _edmIbge[String(lyr.feature.properties.codarea)];\n'
    '    if(!uf) return;\n'
    '    var d   = ufAgg[uf];\n'
    '    var pct = d && d.total > 0 ? Math.round(d.scj / d.total * 100) : null;\n'
    "    var pctCol = pct!=null ? (pct>=70?'#34d399':pct>=40?'#fbbf24':pct>=20?'#f97316':'#ef4444') : '#94a3b8';\n"
    '    var center = lyr.getBounds().getCenter();\n'
    '    L.marker(center, {\n'
    '      icon: L.divIcon({\n'
    "        className: '',\n"
    "        html: '<div style=\"color:#fff;font-size:12px;font-weight:900;letter-spacing:.03em;'\n"
    "          +'text-shadow:0 1px 4px #000,0 0 10px rgba(0,0,0,0.95),1px 1px 0 rgba(0,0,0,0.8);'\n"
    "          +'white-space:nowrap;pointer-events:none;text-align:center;'\n"
    "          +'transform:translate(-50%,-50%);line-height:1.25;\">'\n"
    "          +uf\n"
    "          +(pct!==null\n"
    "            ? '<br><span style=\"font-size:10px;font-weight:800;color:'+pctCol+';'\n"
    "                +'text-shadow:0 1px 3px #000,0 0 6px rgba(0,0,0,0.9);\">'+pct+'%</span>'\n"
    "            : '')\n"
    "          +'</div>',\n"
    '        iconSize:[50,30], iconAnchor:[25,15]\n'
    '      }),\n'
    '      interactive:false, keyboard:false\n'
    '    }).addTo(lblLyr);\n'
    '  });\n'
    '  lblLyr.addTo(_yoyAggMap);'
)
h = replace_once(h, OLD2, NEW2, 'Labels UF+% maiores com cor dinâmica')

# ═══════════════════════════════════════════════════════════════════════════════
# 3. Terceiro pass de invalidateSize + fitBounds para garantir render completo
# ═══════════════════════════════════════════════════════════════════════════════
OLD3 = (
    '  /* Fit bounds — duplo pass para resolver 0-size no primeiro frame */\n'
    '  setTimeout(function(){\n'
    '    if(!_yoyAggMap) return;\n'
    '    _yoyAggMap.invalidateSize(true);\n'
    "    if(_yoyAggMapBrGeo) _yoyAggMap.fitBounds(_yoyAggMapBrGeo.getBounds(), {padding:[15,15]});\n"
    '    setTimeout(function(){\n'
    '      if(!_yoyAggMap) return;\n'
    '      _yoyAggMap.invalidateSize(true);\n'
    "      if(_yoyAggMapBrGeo) _yoyAggMap.fitBounds(_yoyAggMapBrGeo.getBounds(), {padding:[15,15]});\n"
    '    }, 400);\n'
    '  }, 500);'
)
NEW3 = (
    '  /* Fit bounds — triplo pass para garantir render completo */\n'
    '  setTimeout(function(){\n'
    '    if(!_yoyAggMap) return;\n'
    '    _yoyAggMap.invalidateSize(true);\n'
    "    if(_yoyAggMapBrGeo) _yoyAggMap.fitBounds(_yoyAggMapBrGeo.getBounds(), {padding:[8,8]});\n"
    '    setTimeout(function(){\n'
    '      if(!_yoyAggMap) return;\n'
    '      _yoyAggMap.invalidateSize(true);\n'
    "      if(_yoyAggMapBrGeo) _yoyAggMap.fitBounds(_yoyAggMapBrGeo.getBounds(), {padding:[8,8]});\n"
    '      setTimeout(function(){\n'
    '        if(!_yoyAggMap) return;\n'
    '        _yoyAggMap.invalidateSize(true);\n'
    "        if(_yoyAggMapBrGeo) _yoyAggMap.fitBounds(_yoyAggMapBrGeo.getBounds(), {padding:[8,8]});\n"
    '      }, 600);\n'
    '    }, 400);\n'
    '  }, 300);'
)
h = replace_once(h, OLD3, NEW3, 'Triplo pass invalidateSize/fitBounds')

# ═══════════════════════════════════════════════════════════════════════════════
# Verificações
# ═══════════════════════════════════════════════════════════════════════════════
assert 'height:460px' in h,        'ERRO: altura 460px não inserida'
assert 'font-size:12px' in h,      'ERRO: label UF 12px não inserida'
assert 'font-size:10px' in h,      'ERRO: label % 10px não inserida'
assert 'iconSize:[50,30]' in h,    'ERRO: iconSize não atualizado'
assert 'pctCol' in h,              'ERRO: pctCol não inserido nos labels'
assert h.count('triplo pass') == 1,'ERRO: triplo pass não inserido'
print('Verificações: OK')
print(f'Tamanho final: {len(h):,} chars')

# ═══════════════════════════════════════════════════════════════════════════════
# Salvar
# ═══════════════════════════════════════════════════════════════════════════════
DASH.write_text(h, encoding='utf-8')
shutil.copy(DASH, VER / f'Dashboard_Farma_Sul_{ts}_MapaLabels.html')
shutil.copy(DASH, DL  / f'Dashboard_FarmaSul_Giovano_{ts}.html')
print(f'Versao:    Dashboard_Farma_Sul_{ts}_MapaLabels.html')
print(f'Downloads: Dashboard_FarmaSul_Giovano_{ts}.html')
print('DONE.')
