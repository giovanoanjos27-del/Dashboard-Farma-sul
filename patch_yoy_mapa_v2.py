"""
patch_yoy_mapa_v2.py
====================
Corrige universo por estado no mapa YoY:

Problema anterior:
  - Math.max(total) = maior universo de 1 provedor (SP: 7.581)
  - scj SUM = todos os provedores (SP: 17.267) → 228% impossível

Solução:
  - Universe = ED_UF_DATA[uf].pdvs → universo IQVIA real por estado (SP: 9.296)
  - SCJ estimado = (Σscj_uf / Σtot_uf) × ed_pdvs → % ponderada × universo real
    SP: 17.267 / 39.071 = 44.2% × 9.296 = ~4.107 PDVs — valor realista
  - fy25/fy26: prorate continua por share de SCJ do provedor (sem mudança)
"""
import sys, shutil
sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path
from datetime import datetime

DASH = Path(r'C:\Users\valqu\OneDrive\Documentos\Claude\Projects\projeto Dashboard_farma_sul\Dashboard_farma_sul\Dashboard_Farma_Sul_20260512_2220.html')
VER  = DASH.parent / 'versoes'
DL   = Path.home() / 'Downloads'
ts   = datetime.now().strftime('%Y%m%d_%H%M')

shutil.copy(DASH, VER / f'Dashboard_Farma_Sul_{ts}_PreMapaV2.html')
h = DASH.read_text(encoding='utf-8')
print(f'Backup: ...PreMapaV2.html  |  {len(h):,} chars')

# ═══════════════════════════════════════════════════════════════════════════════
# 1) Substituir ufAgg: usar % ponderada + ED_UF_DATA como universo real
# ═══════════════════════════════════════════════════════════════════════════════
OLD_AGG = (
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

assert h.count(OLD_AGG) == 1, f'OLD_AGG não-única: {h.count(OLD_AGG)}x'

NEW_AGG = (
    '  /* ── Cobertura por Estado — Mapa Leaflet agregado ── */\n'
    '  /* Fase 1: acumular pesos (totW/scjW) e fy25/fy26 por estado */\n'
    '  var ufAgg = {};\n'
    '  (PROV_DATA||[]).forEach(function(pv){\n'
    '    /* FY25 = M[3..11] (Jul/24–Mar/25)  ·  FY26 = M[15..23] (Jul/25–Mar/26) */\n'
    '    var _m = pv.monthly || [];\n'
    '    var _pFy25 = 0, _pFy26 = 0;\n'
    '    for(var _i=3;  _i<=11; _i++) _pFy25 += (_m[_i]||0);\n'
    '    for(var _i=15; _i<=23; _i++) _pFy26 += (_m[_i]||0);\n'
    '    var _pScjTot = 0;\n'
    '    (pv.by_uf||[]).forEach(function(u){ _pScjTot += u[2]||0; });\n'
    '    (pv.by_uf||[]).forEach(function(u){\n'
    '      var uf = u[0], tot = u[1]||0, scj = u[2]||0;\n'
    '      if(!ufAgg[uf]) ufAgg[uf] = {totW:0, scjW:0, fy25:0, fy26:0};\n'
    '      ufAgg[uf].totW += tot;   /* soma pesos para % ponderada */\n'
    '      ufAgg[uf].scjW += scj;\n'
    '      /* Prorate FY25/FY26 pelo share deste estado no SCJ deste provedor */\n'
    '      var _share = _pScjTot > 0 ? scj / _pScjTot : 0;\n'
    '      ufAgg[uf].fy25 += _pFy25 * _share;\n'
    '      ufAgg[uf].fy26 += _pFy26 * _share;\n'
    '    });\n'
    '  });\n'
    '  /* Fase 2: converter para total/scj usando ED_UF_DATA como universo IQVIA real */\n'
    '  var _edUF = (typeof ED_UF_DATA !== "undefined") ? ED_UF_DATA : {};\n'
    '  Object.keys(ufAgg).forEach(function(uf){\n'
    '    var d = ufAgg[uf];\n'
    '    var iqviaTotal = (_edUF[uf] && _edUF[uf].pdvs) ? _edUF[uf].pdvs : d.totW;\n'
    '    var pctW = d.totW > 0 ? d.scjW / d.totW : 0;  /* % ponderada pelos provedores */\n'
    '    d.total = iqviaTotal;                           /* universo IQVIA real */\n'
    '    d.scj   = Math.min(Math.round(pctW * iqviaTotal), iqviaTotal); /* cap 100% */\n'
    '  });'
)

h = h.replace(OLD_AGG, NEW_AGG, 1)
print('✓ ufAgg: % ponderada + ED_UF_DATA como universo IQVIA real')

# ═══════════════════════════════════════════════════════════════════════════════
# Verificações
# ═══════════════════════════════════════════════════════════════════════════════
assert 'ufAgg[uf].totW +='        in h,  'ERRO: totW não inserido'
assert 'ufAgg[uf].scjW +='        in h,  'ERRO: scjW não inserido'
assert 'ED_UF_DATA'                in h,  'ERRO: ED_UF_DATA não referenciado'
assert 'pctW = d.totW > 0'         in h,  'ERRO: pctW não inserido'
assert 'd.total = iqviaTotal'      in h,  'ERRO: atribuição total não inserida'
assert 'Math.min(Math.round(pctW'  in h,  'ERRO: cap 100% não inserido'
assert 'prov-yoy-body'             in h,  'ERRO: prov-yoy-body perdido'
assert 'fy25r.toLocaleString'      in h,  'ERRO: bloco YoY drill perdido'
print('Verificações: OK')
print(f'Tamanho final: {len(h):,} chars')

# ═══════════════════════════════════════════════════════════════════════════════
# Salvar
# ═══════════════════════════════════════════════════════════════════════════════
DASH.write_text(h, encoding='utf-8')
shutil.copy(DASH, VER / f'Dashboard_Farma_Sul_{ts}_MapaV2.html')
shutil.copy(DASH, DL  / f'Dashboard_FarmaSul_Giovano_{ts}.html')
print(f'Versao:    Dashboard_Farma_Sul_{ts}_MapaV2.html')
print(f'Downloads: Dashboard_FarmaSul_Giovano_{ts}.html')
print('DONE.')
