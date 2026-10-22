"""
patch_universo_estado.py
========================
Corrige o que "Universo IQVIA Ativo" representa quando um provedor está filtrado.

ANTES (errado):
  total = pv.by_uf[total_iqvia]  ← universo do TERRITÓRIO daquele provedor
  Ex: GAM no MS = 359  (apenas o território coberto pelo GAM)

DEPOIS (correto):
  total = UF_COB_DATA[uf].universe ← TODOS os CNPJs distintos do estado
  Inclui: CNPJs com venda SCJ + CNPJs com venda CIMED/RB (sem SCJ) + etc.
  Fonte: positivação ano 2024x2025x2026.xlsx — todos os players, deduplicado por CNPJ

Impacto visual:
  • Universo agora mostra o mercado total do estado, não o território do provedor
  • % Cobertura = SCJ deste provedor / universo TOTAL estado (mais honesto)
  • Disponíveis = universo estado − SCJ provedor
  • Mapa: cor reflete cobertura real do provedor sobre o mercado total do estado
"""
import sys, shutil
sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path
from datetime import datetime

DASH = Path(r'C:\Users\valqu\OneDrive\Documentos\Claude\Projects\projeto Dashboard_farma_sul\Dashboard_farma_sul\Dashboard_Farma_Sul_20260512_2220.html')
VER  = DASH.parent / 'versoes'
DL   = Path.home() / 'Downloads'
ts   = datetime.now().strftime('%Y%m%d_%H%M')

shutil.copy(DASH, VER / f'Dashboard_Farma_Sul_{ts}_PreUniverso.html')
h = DASH.read_text(encoding='utf-8')
print(f'Backup: ...PreUniverso.html  |  {len(h):,} chars')

def replace_once(html, old, new, label):
    cnt = html.count(old)
    assert cnt == 1, f'ERRO [{label}]: {cnt}x encontrado'
    print(f'✓ {label}')
    return html.replace(old, new, 1)

# ═══════════════════════════════════════════════════════════════════════════════
# 1. Corrigir _yoyBuildUfAgg: universo no modo provedor = estado total, não território
# ═══════════════════════════════════════════════════════════════════════════════
OLD1 = (
    '    if(pv && pv.by_uf){\n'
    '      (pv.by_uf).forEach(function(u){\n'
    '        var uf = u[0], tot = u[1]||0, scj = u[2]||0;\n'
    '        if(!tot) return;\n'
    '        agg[uf] = {\n'
    '          total:    tot,       /* universo deste provedor neste estado */\n'
    '          scj:      scj,       /* CNPJs SCJ ativos neste provedor */\n'
    '          scj_fy25: 0,         /* não disponível por provedor */\n'
    '          reconq:   0,\n'
    '          ws_puro:  0,\n'
    '          white_sp: tot - scj, /* disponíveis = universo provedor − SCJ */\n'
    '          yoy_gap:  null,\n'
    '          _prov_mode: true\n'
    '        };\n'
    '      });\n'
    '    }\n'
    '    return agg;\n'
    '  }'
)

NEW1 = (
    '    /* Universo por estado — todos os CNPJs distintos (UF_COB_DATA) */\n'
    "    var _cobDataPv = (typeof UF_COB_DATA !== 'undefined') ? UF_COB_DATA : {};\n"
    '    if(pv && pv.by_uf){\n'
    '      (pv.by_uf).forEach(function(u){\n'
    '        var uf = u[0], provTot = u[1]||0, scj = u[2]||0;\n'
    '        if(!provTot) return;\n'
    '        /* Universo = TODOS os CNPJs distintos do estado (positivação 2024x2025x2026)\n'
    '           Inclui: SCJ + CIMED + RB + qualquer player — deduplicado por CNPJ\n'
    '           Fallback para provTot se o estado não estiver em UF_COB_DATA */\n'
    '        var univTotal = (_cobDataPv[uf] && _cobDataPv[uf].universe) ? _cobDataPv[uf].universe : provTot;\n'
    '        agg[uf] = {\n'
    '          total:    univTotal,         /* universo TOTAL estado — todos CNPJs distintos IQVIA */\n'
    '          scj:      scj,              /* CNPJs SCJ ativos via este provedor */\n'
    '          scj_fy25: 0,\n'
    '          reconq:   0,\n'
    '          ws_puro:  0,\n'
    '          white_sp: univTotal - scj,  /* disponíveis = universo estado − SCJ deste provedor */\n'
    '          yoy_gap:  null,\n'
    '          _prov_mode: true\n'
    '        };\n'
    '      });\n'
    '    }\n'
    '    return agg;\n'
    '  }'
)
h = replace_once(h, OLD1, NEW1, 'Universo = estado total (todos CNPJs distintos), não território provedor')

# ═══════════════════════════════════════════════════════════════════════════════
# 2. Atualizar legenda "universo − FY26" no KPI Disponíveis p/ Atend.
#    para mostrar mensagem correta no modo provedor
# ═══════════════════════════════════════════════════════════════════════════════
OLD2 = (
    "        +'<div style=\"font-size:7px;color:#334155;\">'+wsPct+'% · universo − FY26</div>'"
)
NEW2 = (
    "        +'<div style=\"font-size:7px;color:#334155;\">'+wsPct+'% · '+(d._prov_mode?'estado − SCJ provedor':'universo − FY26')+'</div>'"
)
h = replace_once(h, OLD2, NEW2, 'Legenda KPI Disponíveis adaptada para modo provedor')

# ═══════════════════════════════════════════════════════════════════════════════
# Verificações
# ═══════════════════════════════════════════════════════════════════════════════
assert 'univTotal' in h,          'ERRO: univTotal não inserido'
assert '_cobDataPv' in h,         'ERRO: _cobDataPv não inserido'
assert 'universo TOTAL estado' in h, 'ERRO: comentário universo total ausente'
assert 'estado − SCJ provedor' in h, 'ERRO: legenda prov_mode ausente'
print('Verificações: OK')
print(f'Tamanho final: {len(h):,} chars')

# ═══════════════════════════════════════════════════════════════════════════════
# Salvar
# ═══════════════════════════════════════════════════════════════════════════════
DASH.write_text(h, encoding='utf-8')
shutil.copy(DASH, VER / f'Dashboard_Farma_Sul_{ts}_UniversoEstado.html')
shutil.copy(DASH, DL  / f'Dashboard_FarmaSul_Giovano_{ts}.html')
print(f'Versao:    Dashboard_Farma_Sul_{ts}_UniversoEstado.html')
print(f'Downloads: Dashboard_FarmaSul_Giovano_{ts}.html')
print('DONE.')
