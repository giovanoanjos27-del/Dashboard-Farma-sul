"""
patch_label_branco.py
=====================
Labels do mapa: UF + % totalmente branco com badge escuro por trás.
Antes: % usava pctCol (vermelho em baixa cobertura → some no fundo vermelho).
Agora: tudo branco + fundo rgba(0,0,0,0.52) com borda colorida sutil pelo pctCol.
Resultado: legível em QUALQUER cor de estado (verde, laranja, vermelho).
"""
import sys, shutil
sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path
from datetime import datetime

DASH = Path(r'C:\Users\valqu\OneDrive\Documentos\Claude\Projects\projeto Dashboard_farma_sul\Dashboard_farma_sul\Dashboard_Farma_Sul_20260512_2220.html')
VER  = DASH.parent / 'versoes'
DL   = Path.home() / 'Downloads'
ts   = datetime.now().strftime('%Y%m%d_%H%M')

shutil.copy(DASH, VER / f'Dashboard_Farma_Sul_{ts}_PreLabelBranco.html')
h = DASH.read_text(encoding='utf-8')
print(f'Backup: ...PreLabelBranco.html  |  {len(h):,} chars')

def replace_once(html, old, new, label):
    cnt = html.count(old)
    assert cnt == 1, f'ERRO [{label}]: {cnt}x encontrado'
    print(f'✓ {label}')
    return html.replace(old, new, 1)

# ─────────────────────────────────────────────────────────────────────────────
OLD = (
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

# Badge escuro por trás: UF branco bold + % branco bold
# Borda inferior colorida com pctCol para dar dica visual da cobertura
NEW = (
    '  /* Labels UF + % — branco com badge escuro, legível em qualquer fundo */\n'
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
    # Badge escuro com borda colorida no rodapé
    "        html: '<div style=\"pointer-events:none;text-align:center;transform:translate(-50%,-50%);white-space:nowrap;\">'\n"
    "          +'<div style=\"display:inline-block;background:rgba(0,0,0,0.55);'\n"
    "            +'border-radius:5px;padding:2px 6px 3px 6px;'\n"
    "            +'border-bottom:2px solid '+pctCol+';'\n"
    "            +'box-shadow:0 2px 6px rgba(0,0,0,0.7);\">'\n"
    "            +'<div style=\"font-size:11px;font-weight:900;color:#fff;line-height:1.2;letter-spacing:.04em;\">'+uf+'</div>'\n"
    "            +(pct!==null\n"
    "              ? '<div style=\"font-size:10px;font-weight:800;color:#fff;line-height:1.1;\">'+pct+'%</div>'\n"
    "              : '')\n"
    "          +'</div>'\n"
    "          +'</div>',\n"
    '        iconSize:[52,34], iconAnchor:[26,17]\n'
    '      }),\n'
    '      interactive:false, keyboard:false\n'
    '    }).addTo(lblLyr);\n'
    '  });\n'
    '  lblLyr.addTo(_yoyAggMap);'
)

h = replace_once(h, OLD, NEW, 'Labels brancos com badge escuro + borda pctCol')

# Verificações
assert 'badge escuro' in h,             'ERRO: novo label não inserido'
assert 'border-bottom:2px solid' in h,  'ERRO: borda colorida ausente'
assert 'rgba(0,0,0,0.55)' in h,         'ERRO: fundo badge ausente'
print('Verificações: OK')
print(f'Tamanho final: {len(h):,} chars')

DASH.write_text(h, encoding='utf-8')
shutil.copy(DASH, VER / f'Dashboard_Farma_Sul_{ts}_LabelBranco.html')
shutil.copy(DASH, DL  / f'Dashboard_FarmaSul_Giovano_{ts}.html')
print(f'Versao:    Dashboard_Farma_Sul_{ts}_LabelBranco.html')
print(f'Downloads: Dashboard_FarmaSul_Giovano_{ts}.html')
print('DONE.')
