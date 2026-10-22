"""
patch_yoy_mapa_fixes.py
=======================
Duas correções no mapa YoY Aggregate (seleção "Ambos"):
1. Deduplicação universo IQVIA: Math.max(total) em vez de += total
2. YoY por estado: prorate FY25/FY26 pelo share SCJ + bloco Δ% no drill-down
"""
import sys, shutil
sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path
from datetime import datetime

DASH = Path(r'C:\Users\valqu\OneDrive\Documentos\Claude\Projects\projeto Dashboard_farma_sul\Dashboard_farma_sul\Dashboard_Farma_Sul_20260512_2220.html')
VER  = DASH.parent / 'versoes'
DL   = Path.home() / 'Downloads'
ts   = datetime.now().strftime('%Y%m%d_%H%M')

shutil.copy(DASH, VER / f'Dashboard_Farma_Sul_{ts}_PreMapaFixes.html')
h = DASH.read_text(encoding='utf-8')
print(f'Backup: ...PreMapaFixes.html  |  {len(h):,} chars')

# ═══════════════════════════════════════════════════════════════════════════════
# 1) Corrigir ufAgg: Math.max para total + adicionar fy25/fy26 por estado
# ═══════════════════════════════════════════════════════════════════════════════
OLD_AGG = (
    '  /* ── Cobertura por Estado — Mapa Leaflet agregado ── */\n'
    '  var ufAgg = {};\n'
    '  (PROV_DATA||[]).forEach(function(pv){\n'
    '    (pv.by_uf||[]).forEach(function(u){\n'
    '      var uf = u[0], tot = u[1]||0, scj = u[2]||0;\n'
    '      if(!ufAgg[uf]) ufAgg[uf] = {total:0, scj:0};\n'
    '      ufAgg[uf].total += tot;\n'
    '      ufAgg[uf].scj   += scj;\n'
    '    });\n'
    '  });'
)

assert h.count(OLD_AGG) == 1, f'OLD_AGG não-única: {h.count(OLD_AGG)}x'

NEW_AGG = (
    '  /* ── Cobertura por Estado — Mapa Leaflet agregado ── */\n'
    '  var ufAgg = {};\n'
    '  (PROV_DATA||[]).forEach(function(pv){\n'
    '    /* FY25 = M[3..11] (Jul/24–Mar/25)  ·  FY26 = M[15..23] (Jul/25–Mar/26) */\n'
    '    var _m = pv.monthly || [];\n'
    '    var _pFy25 = 0, _pFy26 = 0;\n'
    '    for(var _i=3;  _i<=11; _i++) _pFy25 += (_m[_i]||0);\n'
    '    for(var _i=15; _i<=23; _i++) _pFy26 += (_m[_i]||0);\n'
    '    /* Total SCJ deste provedor → denominador do share por estado */\n'
    '    var _pScjTot = 0;\n'
    '    (pv.by_uf||[]).forEach(function(u){ _pScjTot += u[2]||0; });\n'
    '    (pv.by_uf||[]).forEach(function(u){\n'
    '      var uf = u[0], tot = u[1]||0, scj = u[2]||0;\n'
    '      if(!ufAgg[uf]) ufAgg[uf] = {total:0, scj:0, fy25:0, fy26:0};\n'
    '      ufAgg[uf].total = Math.max(ufAgg[uf].total, tot); /* MAX: evita duplicar universo IQVIA */\n'
    '      ufAgg[uf].scj  += scj;\n'
    '      /* Prorate FY25/FY26 pelo share deste estado no SCJ deste provedor */\n'
    '      var _share = _pScjTot > 0 ? scj / _pScjTot : 0;\n'
    '      ufAgg[uf].fy25 += _pFy25 * _share;\n'
    '      ufAgg[uf].fy26 += _pFy26 * _share;\n'
    '    });\n'
    '  });'
)

h = h.replace(OLD_AGG, NEW_AGG, 1)
print('✓ ufAgg: Math.max(total) + fy25/fy26 por estado inseridos')

# ═══════════════════════════════════════════════════════════════════════════════
# 2) Atualizar _yoyAggUfClick: adicionar bloco YoY FY25/FY26/Δ% no drill-down
#    Usamos marcadores de início/fim para não depender de string longa exata
# ═══════════════════════════════════════════════════════════════════════════════
FN_START = 'function _yoyAggUfClick(uf, d){'
FN_END   = "  drill.style.cssText = 'background:#161B22;border-radius:8px;padding:14px;'\n    +'border:0.5px solid rgba(103,232,249,0.12);min-height:360px;overflow-y:auto;';\n  drill.innerHTML = html;\n}"

s = h.find(FN_START)
e = h.find(FN_END, s)
assert s != -1, 'ERRO: _yoyAggUfClick não encontrado'
assert e != -1, 'ERRO: fim de _yoyAggUfClick não encontrado'
e += len(FN_END)

old_fn = h[s:e]
print(f'Função _yoyAggUfClick encontrada: {len(old_fn):,} chars')

NEW_FN = r"""function _yoyAggUfClick(uf, d){
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

  /* YoY estimado: PDV-meses ponderados pelo share de SCJ por estado */
  var fy25r  = Math.round(d.fy25||0);
  var fy26r  = Math.round(d.fy26||0);
  var yoyD   = fy25r > 0 ? Math.round((fy26r - fy25r) / fy25r * 100) : null;
  var yoyCol = yoyD===null?'#64748b':yoyD>5?'#34d399':yoyD>=-5?'#fbbf24':'#ef4444';

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
        +'<div style="font-size:8px;color:#334155;margin-top:2px;">PDVs únicos (max)</div>'
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

    /* ── Evolução YoY por Estado ── */
    +'<div style="margin-top:10px;background:rgba(34,197,94,0.04);border-radius:7px;padding:10px 12px;border:0.5px solid rgba(34,197,94,0.12);">'
      +'<div style="font-size:7.5px;font-weight:800;letter-spacing:.1em;color:#22c55e;text-transform:uppercase;margin-bottom:8px;">📈 EVOLUÇÃO YoY — PDV-MESES ESTIMADOS</div>'
      +'<div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:6px;">'
        +'<div style="background:#0D1117;border-radius:5px;padding:7px 9px;">'
          +'<div style="font-size:7px;color:#3b82f6;font-weight:700;margin-bottom:2px;">FY25</div>'
          +'<div style="font-size:14px;font-weight:800;color:#e2e8f0;">'+fy25r.toLocaleString('pt-BR')+'</div>'
          +'<div style="font-size:7px;color:#334155;">Jul/24–Mar/25</div>'
        +'</div>'
        +'<div style="background:#0D1117;border-radius:5px;padding:7px 9px;">'
          +'<div style="font-size:7px;color:#22c55e;font-weight:700;margin-bottom:2px;">FY26</div>'
          +'<div style="font-size:14px;font-weight:800;color:#e2e8f0;">'+fy26r.toLocaleString('pt-BR')+'</div>'
          +'<div style="font-size:7px;color:#334155;">Jul/25–Mar/26</div>'
        +'</div>'
        +'<div style="background:#0D1117;border-radius:5px;padding:7px 9px;border-left:2px solid '+yoyCol+';">'
          +'<div style="font-size:7px;color:#94a3b8;font-weight:700;margin-bottom:2px;">Δ% YoY</div>'
          +'<div style="font-size:16px;font-weight:900;color:'+yoyCol+';">'+(yoyD===null?'—':(yoyD>=0?'+':'')+yoyD+'%')+'</div>'
          +'<div style="font-size:7px;color:#334155;">FY25→FY26</div>'
        +'</div>'
      +'</div>'
      +'<div style="font-size:7px;color:#1e3a4a;margin-top:6px;font-style:italic;">Estimativa proporcional ao share de SCJ ativos por estado</div>'
    +'</div>'

    +'</div>';

  drill.style.cssText = 'background:#161B22;border-radius:8px;padding:14px;'
    +'border:0.5px solid rgba(103,232,249,0.12);min-height:360px;overflow-y:auto;';
  drill.innerHTML = html;
}"""

h = h[:s] + NEW_FN + h[e:]
print('✓ _yoyAggUfClick: bloco YoY FY25/FY26/Δ% adicionado')

# ═══════════════════════════════════════════════════════════════════════════════
# Verificações
# ═══════════════════════════════════════════════════════════════════════════════
assert 'Math.max(ufAgg[uf].total, tot)' in h,    'ERRO: Math.max não inserido'
assert 'ufAgg[uf].fy25 +='              in h,    'ERRO: fy25 acumulação não inserida'
assert 'fy25r.toLocaleString'           in h,    'ERRO: YoY drill FY25 não inserido'
assert 'fy26r.toLocaleString'           in h,    'ERRO: YoY drill FY26 não inserido'
assert 'EVOLUÇÃO YoY'                   in h,    'ERRO: cabeçalho YoY drill não inserido'
assert 'prov-yoy-body'                  in h,    'ERRO: prov-yoy-body perdido'
assert h.count('function _yoyAggUfClick') == 1,  'ERRO: função _yoyAggUfClick duplicada'
print('Verificações: OK')
print(f'Tamanho final: {len(h):,} chars')

# ═══════════════════════════════════════════════════════════════════════════════
# Salvar
# ═══════════════════════════════════════════════════════════════════════════════
DASH.write_text(h, encoding='utf-8')
shutil.copy(DASH, VER / f'Dashboard_Farma_Sul_{ts}_MapaFixes.html')
shutil.copy(DASH, DL  / f'Dashboard_FarmaSul_Giovano_{ts}.html')
print(f'Versao:    Dashboard_Farma_Sul_{ts}_MapaFixes.html')
print(f'Downloads: Dashboard_FarmaSul_Giovano_{ts}.html')
print('DONE.')
