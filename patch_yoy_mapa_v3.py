"""
patch_yoy_mapa_v3.py
====================
Substitui estimativa por dados reais de CNPJ por estado:

Fonte: Oportunidades_RB_Cimed_SCJ2026.xlsx (Detalhe RB + Detalhe CIMED)
       ED_UF_DATA (universo IQVIA por estado)

Campos calculados por estado (CNPJs únicos, sem duplicação):
  - universe  → ED_UF_DATA[uf].pdvs  (universo IQVIA total)
  - scj_fy26  → CNPJs com Posit. FY26 = 'SIM'  (SCJ ativos FY26)
  - scj_fy25  → CNPJs com Comprou FY25 = 'SIM' (SCJ ativos FY25)
  - reconq    → FY25=SIM mas FY26=NÃO  (alta prioridade reconquista)
  - ws_puro   → FY25=NÃO e FY26=NÃO   (white space puro — nunca comprou)
  - white_sp  → universe - scj_fy26   (white space total vs universo)
"""
import sys, shutil, json, re
sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path
from datetime import datetime
from collections import defaultdict
import openpyxl

DASH = Path(r'C:\Users\valqu\OneDrive\Documentos\Claude\Projects\projeto Dashboard_farma_sul\Dashboard_farma_sul\Dashboard_Farma_Sul_20260512_2220.html')
XLS  = Path(r'C:\Users\valqu\OneDrive\Documentos\Claude\Projects\projeto Dashboard_farma_sul\Dashboard_farma_sul\Oportunidades_RB_Cimed_SCJ2026.xlsx')
VER  = DASH.parent / 'versoes'
DL   = Path.home() / 'Downloads'
ts   = datetime.now().strftime('%Y%m%d_%H%M')

shutil.copy(DASH, VER / f'Dashboard_Farma_Sul_{ts}_PreMapaV3.html')
h = DASH.read_text(encoding='utf-8')
print(f'Backup: ...PreMapaV3.html  |  {len(h):,} chars')

# ═══════════════════════════════════════════════════════════════════════════════
# 1) Extrair dados reais por estado da planilha CNPJ-nível
# ═══════════════════════════════════════════════════════════════════════════════
wb = openpyxl.load_workbook(str(XLS), read_only=True, data_only=True)

scj_fy26 = defaultdict(set)
scj_fy25 = defaultdict(set)
reconq   = defaultdict(set)
ws_puro  = defaultdict(set)

for sheet_name in ['Detalhe RB', 'Detalhe CIMED']:
    ws_sheet = wb[sheet_name]
    for i, r in enumerate(ws_sheet.iter_rows(values_only=True)):
        if i < 2: continue
        if not r[2]: continue
        uf   = r[1]
        cnpj = str(r[2]).strip()
        f25  = str(r[5]).strip().upper() if r[5] else 'NAO'
        f26  = str(r[9]).strip().upper() if r[9] else 'NAO'
        if not uf: continue

        if f26 == 'SIM':
            scj_fy26[uf].add(cnpj)
        if f25 == 'SIM':
            scj_fy25[uf].add(cnpj)
        if f25 == 'SIM' and f26 != 'SIM':
            reconq[uf].add(cnpj)
        if f25 != 'SIM' and f26 != 'SIM':
            ws_puro[uf].add(cnpj)

print(f'CNPJs processados — SCJ FY26: {sum(len(v) for v in scj_fy26.values()):,}')

# ═══════════════════════════════════════════════════════════════════════════════
# 2) Carregar ED_UF_DATA do HTML para universo IQVIA por estado
# ═══════════════════════════════════════════════════════════════════════════════
idx_ed = h.find('var ED_UF_DATA=')
end_ed = h.find(';', idx_ed)
ed = json.loads(h[idx_ed + len('var ED_UF_DATA='):end_ed])

# ═══════════════════════════════════════════════════════════════════════════════
# 3) Montar UF_SCJ_DATA — constante JavaScript com dados reais
# ═══════════════════════════════════════════════════════════════════════════════
all_ufs = sorted(set(list(scj_fy26.keys()) + list(ed.keys())))
uf_scj = {}
for uf in all_ufs:
    universe = ed.get(uf, {}).get('pdvs', 0)
    s26      = len(scj_fy26.get(uf, set()))
    s25      = len(scj_fy25.get(uf, set()))
    rec      = len(reconq.get(uf, set()))
    wsp      = len(ws_puro.get(uf, set()))
    ws_total = max(universe - s26, 0)
    uf_scj[uf] = {
        'universe': universe,
        'scj_fy26': s26,
        'scj_fy25': s25,
        'reconq':   rec,
        'ws_puro':  wsp,
        'white_sp': ws_total
    }

# Gera JS
lines = []
for uf, d in sorted(uf_scj.items()):
    lines.append(
        f'  "{uf}":{{universe:{d["universe"]},scj_fy26:{d["scj_fy26"]},'
        f'scj_fy25:{d["scj_fy25"]},reconq:{d["reconq"]},'
        f'ws_puro:{d["ws_puro"]},white_sp:{d["white_sp"]}}}'
    )
UF_SCJ_JS = 'const UF_SCJ_DATA = {\n' + ',\n'.join(lines) + '\n};'
print(f'UF_SCJ_DATA: {len(uf_scj)} estados')

# Injeta antes de ED_UF_DATA
assert h.count('var ED_UF_DATA=') == 1, 'ED_UF_DATA não encontrado'
OLD_ED_MARKER = 'var ED_UF_DATA='
h = h.replace(OLD_ED_MARKER, UF_SCJ_JS + '\n' + OLD_ED_MARKER, 1)
print('✓ UF_SCJ_DATA injetado antes de ED_UF_DATA')

# ═══════════════════════════════════════════════════════════════════════════════
# 4) Atualizar ufAgg — usar UF_SCJ_DATA para total/scj, manter fy25/fy26 do PROV_DATA
# ═══════════════════════════════════════════════════════════════════════════════
OLD_AGG = (
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

assert h.count(OLD_AGG) == 1, f'OLD_AGG não-única: {h.count(OLD_AGG)}x'

NEW_AGG = (
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
    '  });'
)

h = h.replace(OLD_AGG, NEW_AGG, 1)
print('✓ ufAgg: dados reais UF_SCJ_DATA + YoY de PROV_DATA')

# ═══════════════════════════════════════════════════════════════════════════════
# 5) Atualizar _yoyAggUfClick: mostrar reconquista e white space puro no drill
# ═══════════════════════════════════════════════════════════════════════════════
FN_START = 'function _yoyAggUfClick(uf, d){'
FN_END   = "  drill.style.cssText = 'background:#161B22;border-radius:8px;padding:14px;'\n    +'border:0.5px solid rgba(103,232,249,0.12);min-height:360px;overflow-y:auto;';\n  drill.innerHTML = html;\n}"

s = h.find(FN_START)
e = h.find(FN_END, s)
assert s != -1, 'ERRO: _yoyAggUfClick não encontrado'
assert e != -1, 'ERRO: fim de _yoyAggUfClick não encontrado'
e += len(FN_END)
print(f'Função _yoyAggUfClick: {e-s:,} chars')

NEW_FN = r"""function _yoyAggUfClick(uf, d){
  var drill = document.getElementById('yoy-agg-drill');
  if(!drill) return;

  var pct    = d.total > 0 ? Math.round(d.scj / d.total * 100) : 0;
  var pctCol = pct>=70?'#34d399':pct>=40?'#fbbf24':pct>=20?'#f97316':'#ef4444';
  var wsPct  = d.total > 0 ? Math.round(d.white_sp / d.total * 100) : 0;

  /* Provedores ativos neste estado */
  var provsInUF = (PROV_DATA||[]).filter(function(pv){
    return (pv.by_uf||[]).some(function(u){ return u[0]===uf && u[2]>0; });
  });

  /* YoY estimado (PDV-meses ponderados pelo share de SCJ) */
  var fy25r  = Math.round(d.fy25||0);
  var fy26r  = Math.round(d.fy26||0);
  var yoyD   = fy25r > 0 ? Math.round((fy26r - fy25r) / fy25r * 100) : null;
  var yoyCol = yoyD===null?'#64748b':yoyD>5?'#34d399':yoyD>=-5?'#fbbf24':'#ef4444';

  var html = '<div style="width:100%;padding:4px;">'
    /* Header UF + % */
    +'<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px;">'
      +'<div style="font-size:24px;font-weight:800;color:#67e8f9;">'+uf+'</div>'
      +'<div style="text-align:right;">'
        +'<div style="font-size:26px;font-weight:900;color:'+pctCol+';">'+pct+'%</div>'
        +'<div style="font-size:8px;color:#94A3B8;">cobertura SCJ FY26</div>'
      +'</div>'
    +'</div>'

    /* Barra de cobertura */
    +'<div style="display:flex;height:14px;border-radius:4px;overflow:hidden;gap:1px;margin-bottom:4px;">'
      +'<div style="width:'+pct+'%;background:'+pctCol+';"></div>'
      +'<div style="flex:1;background:#1e3a4a;"></div>'
    +'</div>'
    +'<div style="display:flex;gap:10px;margin-bottom:12px;">'
      +'<span style="font-size:8px;color:'+pctCol+';">■ SCJ FY26 '+pct+'%</span>'
      +'<span style="font-size:8px;color:#4a5568;">■ White Space '+wsPct+'%</span>'
    +'</div>'

    /* 3×2 metric grid */
    +'<div style="display:grid;grid-template-columns:1fr 1fr;gap:6px;margin-bottom:10px;">'

      /* Universo Total */
      +'<div style="background:rgba(103,232,249,0.06);border-radius:6px;padding:8px 10px;">'
        +'<div style="font-size:7.5px;color:#94A3B8;margin-bottom:2px;text-transform:uppercase;letter-spacing:.06em;">🏪 Universo IQVIA</div>'
        +'<div style="font-size:19px;font-weight:800;color:#67e8f9;">'+d.total.toLocaleString('pt-BR')+'</div>'
        +'<div style="font-size:7px;color:#334155;">CNPJs únicos rastreados</div>'
      +'</div>'

      /* SCJ Ativos FY26 */
      +'<div style="background:rgba(34,197,94,0.06);border-radius:6px;padding:8px 10px;">'
        +'<div style="font-size:7.5px;color:#94A3B8;margin-bottom:2px;text-transform:uppercase;letter-spacing:.06em;">✅ SCJ Ativos FY26</div>'
        +'<div style="font-size:19px;font-weight:800;color:#34d399;">'+d.scj.toLocaleString('pt-BR')+'</div>'
        +'<div style="font-size:7px;color:#334155;">compraram Jan–Mar/26</div>'
      +'</div>'

      /* White Space Total */
      +'<div style="background:rgba(239,68,68,0.06);border-radius:6px;padding:8px 10px;">'
        +'<div style="font-size:7.5px;color:#94A3B8;margin-bottom:2px;text-transform:uppercase;letter-spacing:.06em;">⬜ White Space</div>'
        +'<div style="font-size:19px;font-weight:800;color:#ef4444;">'+(d.white_sp||0).toLocaleString('pt-BR')+'</div>'
        +'<div style="font-size:7px;color:#334155;">sem SCJ no universo</div>'
      +'</div>'

      /* Alta Prioridade (reconquista) */
      +'<div style="background:rgba(251,191,36,0.06);border-radius:6px;padding:8px 10px;">'
        +'<div style="font-size:7.5px;color:#94A3B8;margin-bottom:2px;text-transform:uppercase;letter-spacing:.06em;">🔄 Alta Prioridade</div>'
        +'<div style="font-size:19px;font-weight:800;color:#fbbf24;">'+(d.reconq||0).toLocaleString('pt-BR')+'</div>'
        +'<div style="font-size:7px;color:#334155;">FY25 ativo · sem FY26</div>'
      +'</div>'

      /* SCJ Ativos FY25 */
      +'<div style="background:rgba(59,130,246,0.06);border-radius:6px;padding:8px 10px;">'
        +'<div style="font-size:7.5px;color:#94A3B8;margin-bottom:2px;text-transform:uppercase;letter-spacing:.06em;">📅 SCJ Ativos FY25</div>'
        +'<div style="font-size:19px;font-weight:800;color:#60a5fa;">'+(d.scj_fy25||0).toLocaleString('pt-BR')+'</div>'
        +'<div style="font-size:7px;color:#334155;">compraram FY25</div>'
      +'</div>'

      /* Provedores */
      +'<div style="background:rgba(167,139,250,0.06);border-radius:6px;padding:8px 10px;">'
        +'<div style="font-size:7.5px;color:#94A3B8;margin-bottom:2px;text-transform:uppercase;letter-spacing:.06em;">🏬 Provedores</div>'
        +'<div style="font-size:19px;font-weight:800;color:#a78bfa;">'+provsInUF.length+'</div>'
        +'<div style="font-size:7px;color:#334155;">ativos neste estado</div>'
      +'</div>'

    +'</div>'

    /* Evolução YoY */
    +'<div style="background:rgba(34,197,94,0.04);border-radius:7px;padding:9px 12px;border:0.5px solid rgba(34,197,94,0.12);">'
      +'<div style="font-size:7.5px;font-weight:800;letter-spacing:.1em;color:#22c55e;text-transform:uppercase;margin-bottom:7px;">📈 EVOLUÇÃO YoY — PDV-MESES ESTIMADOS</div>'
      +'<div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:5px;">'
        +'<div style="background:#0D1117;border-radius:5px;padding:6px 9px;">'
          +'<div style="font-size:7px;color:#3b82f6;font-weight:700;margin-bottom:2px;">FY25</div>'
          +'<div style="font-size:13px;font-weight:800;color:#e2e8f0;">'+fy25r.toLocaleString('pt-BR')+'</div>'
          +'<div style="font-size:7px;color:#334155;">Jul/24–Mar/25</div>'
        +'</div>'
        +'<div style="background:#0D1117;border-radius:5px;padding:6px 9px;">'
          +'<div style="font-size:7px;color:#22c55e;font-weight:700;margin-bottom:2px;">FY26</div>'
          +'<div style="font-size:13px;font-weight:800;color:#e2e8f0;">'+fy26r.toLocaleString('pt-BR')+'</div>'
          +'<div style="font-size:7px;color:#334155;">Jul/25–Mar/26</div>'
        +'</div>'
        +'<div style="background:#0D1117;border-radius:5px;padding:6px 9px;border-left:2px solid '+yoyCol+';">'
          +'<div style="font-size:7px;color:#94a3b8;font-weight:700;margin-bottom:2px;">Δ% YoY</div>'
          +'<div style="font-size:15px;font-weight:900;color:'+yoyCol+';">'+(yoyD===null?'—':(yoyD>=0?'+':'')+yoyD+'%')+'</div>'
          +'<div style="font-size:7px;color:#334155;">FY25→FY26</div>'
        +'</div>'
      +'</div>'
      +'<div style="font-size:7px;color:#1e3a4a;margin-top:5px;font-style:italic;">PDV-meses estimados via share SCJ por provedor · CNPJs: dados reais Detalhe RB+CIMED</div>'
    +'</div>'

    +'</div>';

  drill.style.cssText = 'background:#161B22;border-radius:8px;padding:14px;'
    +'border:0.5px solid rgba(103,232,249,0.12);min-height:360px;overflow-y:auto;';
  drill.innerHTML = html;
}"""

h = h[:s] + NEW_FN + h[e:]
print('✓ _yoyAggUfClick: 6 cards com dados reais + YoY')

# ═══════════════════════════════════════════════════════════════════════════════
# Verificações
# ═══════════════════════════════════════════════════════════════════════════════
assert 'const UF_SCJ_DATA'               in h,  'ERRO: UF_SCJ_DATA não inserido'
assert '_ufSCJ = (typeof UF_SCJ_DATA'    in h,  'ERRO: referência _ufSCJ não inserida'
assert 'scj_fy25: r.scj_fy25'            in h,  'ERRO: scj_fy25 não mapeado'
assert 'Alta Prioridade'                  in h,  'ERRO: card Alta Prioridade não inserido'
assert 'white_sp: r.white_sp'            in h,  'ERRO: white_sp não mapeado'
assert 'CNPJs únicos rastreados'          in h,  'ERRO: label universo não inserido'
assert 'prov-yoy-body'                   in h,  'ERRO: prov-yoy-body perdido'
assert h.count('function _yoyAggUfClick') == 1, 'ERRO: função duplicada'
print('Verificações: OK')
print(f'Tamanho final: {len(h):,} chars')

# ═══════════════════════════════════════════════════════════════════════════════
# Salvar
# ═══════════════════════════════════════════════════════════════════════════════
DASH.write_text(h, encoding='utf-8')
shutil.copy(DASH, VER / f'Dashboard_Farma_Sul_{ts}_MapaV3.html')
shutil.copy(DASH, DL  / f'Dashboard_FarmaSul_Giovano_{ts}.html')
print(f'Versao:    Dashboard_Farma_Sul_{ts}_MapaV3.html')
print(f'Downloads: Dashboard_FarmaSul_Giovano_{ts}.html')
print('DONE.')
