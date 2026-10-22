"""
patch_cobertura_v2.py
=====================
Atualiza o card "COBERTURA POR ESTADO — TODOS OS PROVEDORES" com:

1. Injeta UF_COB_DATA + CITY_COB_DATA (extraídos de positivação 2024x2025x2026.xlsx)
2. Atualiza _yoyBuildUfAgg() → usa UF_COB_DATA (todos os provedores)
3. Atualiza _yoyAggUfClick() → 8 KPIs + tabela top cidades
4. Atualiza tooltip → 8 métricas

Fonte obrigatória: positivação ano 2024x2025x2026.xlsx (QUERY)
FY25 = Jul/24–Abr/25  |  FY26 = Jul/25–Abr/26
"""
import sys, shutil, json, time
sys.stdout.reconfigure(encoding='utf-8')
import pandas as pd
from pathlib import Path
from datetime import datetime

DASH = Path(r'C:\Users\valqu\OneDrive\Documentos\Claude\Projects\projeto Dashboard_farma_sul\Dashboard_farma_sul\Dashboard_Farma_Sul_20260512_2220.html')
VER  = DASH.parent / 'versoes'
DL   = Path.home() / 'Downloads'
BASE = DASH.parent / '_Recursos' / 'Giovano SCJ'
ts   = datetime.now().strftime('%Y%m%d_%H%M')

shutil.copy(DASH, VER / f'Dashboard_Farma_Sul_{ts}_PreCobV2.html')
h = DASH.read_text(encoding='utf-8')
print(f'Backup: ...PreCobV2.html  |  {len(h):,} chars')

def replace_once(html, old, new, label):
    cnt = html.count(old)
    assert cnt == 1, f'ERRO [{label}]: {cnt}x encontrado (esperado 1x)'
    print(f'✓ {label}')
    return html.replace(old, new, 1)

# ═══════════════════════════════════════════════════════════════════════════════
# 1. Extrair dados de positivação
# ═══════════════════════════════════════════════════════════════════════════════
t0 = time.time()
fp = BASE / 'positivação ano 2024x2025x2026.xlsx'
print(f'\nExtraindo dados de {fp.name}...')

cols_idx = [0, 3, 4] + list(range(10, 20)) + list(range(22, 32))
df = pd.read_excel(fp, sheet_name='QUERY', header=0, usecols=cols_idx, dtype={0: str})
fy25_cols = [f'f25_{i}' for i in range(10)]
fy26_cols = [f'f26_{i}' for i in range(10)]
df.columns = ['CNPJ', 'UF', 'Cidade'] + fy25_cols + fy26_cols

df['CNPJ']   = df['CNPJ'].str.strip().str.zfill(14)
df['UF']     = df['UF'].str.strip().str.upper()
df['Cidade'] = df['Cidade'].fillna('').str.strip()
df['is_fy25'] = df[fy25_cols].fillna(0).gt(0).any(axis=1)
df['is_fy26'] = df[fy26_cols].fillna(0).gt(0).any(axis=1)

cnpj_df = df.groupby('CNPJ').agg(
    UF=('UF','first'), Cidade=('Cidade','first'),
    is_fy25=('is_fy25','any'), is_fy26=('is_fy26','any')
).reset_index()
print(f'  {len(cnpj_df):,} CNPJs únicos | {time.time()-t0:.1f}s')

# Métricas por UF
def uf_metrics(g):
    tot = len(g); fy26 = int(g.is_fy26.sum())
    return pd.Series({
        'universe': tot, 'fy25': int(g.is_fy25.sum()), 'fy26': fy26,
        'reconq':   int((g.is_fy25 & ~g.is_fy26).sum()),
        'ws_puro':  int((~g.is_fy25 & ~g.is_fy26).sum()),
        'white_sp': tot - fy26
    })
uf_data = cnpj_df.groupby('UF').apply(uf_metrics).reset_index()

# Métricas por cidade (top 20/UF)
def clean_city(c):
    c = str(c).strip()
    if ' - ' in c: c = c.rsplit(' - ', 1)[0]
    return c.title()

cnpj_df['CityClean'] = cnpj_df['Cidade'].apply(clean_city)
city_raw = cnpj_df.groupby(['UF','CityClean']).apply(lambda g: pd.Series({
    'u': len(g), 'f25': int(g.is_fy25.sum()), 'f26': int(g.is_fy26.sum()),
    'rq': int((g.is_fy25 & ~g.is_fy26).sum()),
    'ws': int((~g.is_fy25 & ~g.is_fy26).sum()),
    'wsp': len(g) - int(g.is_fy26.sum())
})).reset_index()
city_top20 = (city_raw.sort_values('u', ascending=False)
              .groupby('UF', group_keys=False).head(20))

print(f'  {len(uf_data)} estados | {len(city_top20)} cidades top-20')

# ─────────────────────────────────────────────────────────────────────────────
# Gerar JS constants
# ─────────────────────────────────────────────────────────────────────────────
uf_lines = []
for _, r in uf_data.iterrows():
    pct = round(r.fy26/r.universe*100) if r.universe else 0
    uf_lines.append(
        f'  "{r.UF}":{{'
        f'universe:{int(r.universe)},fy25:{int(r.fy25)},fy26:{int(r.fy26)},'
        f'reconq:{int(r.reconq)},ws_puro:{int(r.ws_puro)},white_sp:{int(r.white_sp)},pct:{pct}}}'
    )
UF_COB_JS = 'const UF_COB_DATA = {\n' + ',\n'.join(uf_lines) + '\n};'

city_dict = {}
for uf, grp in city_top20.groupby('UF'):
    city_dict[uf] = []
    for _, r in grp.sort_values('u', ascending=False).iterrows():
        p = round(r.f26/r.u*100) if r.u else 0
        city_dict[uf].append({
            'n': r.CityClean, 'u': int(r.u), 'f25': int(r.f25), 'f26': int(r.f26),
            'rq': int(r.rq), 'ws': int(r.ws), 'wsp': int(r.wsp), 'p': p
        })
CITY_COB_JS = 'const CITY_COB_DATA = ' + json.dumps(city_dict, ensure_ascii=False, separators=(',',':')) + ';'

total_js_size = len(UF_COB_JS) + len(CITY_COB_JS)
print(f'  JS gerado: {total_js_size:,} chars ({total_js_size//1024}KB)')

# ═══════════════════════════════════════════════════════════════════════════════
# 2. Injetar UF_COB_DATA + CITY_COB_DATA antes de UF_SCJ_DATA
# ═══════════════════════════════════════════════════════════════════════════════
OLD_SCJ_ANCHOR = 'const UF_SCJ_DATA = {'
NEW_SCJ_ANCHOR = UF_COB_JS + '\n\n' + CITY_COB_JS + '\n\nconst UF_SCJ_DATA = {'

h = replace_once(h, OLD_SCJ_ANCHOR, NEW_SCJ_ANCHOR, 'UF_COB_DATA + CITY_COB_DATA injetados')

# ═══════════════════════════════════════════════════════════════════════════════
# 3. Atualizar _yoyBuildUfAgg() → usa UF_COB_DATA
# ═══════════════════════════════════════════════════════════════════════════════
OLD_BUILD = (
    'function _yoyBuildUfAgg(){\n'
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
    "      if(!_ufFy[uf]) _ufFy[uf] = {fy25:0, fy26:0};\n"
    '      var _share = _pScjTot > 0 ? scj / _pScjTot : 0;\n'
    '      _ufFy[uf].fy25 += _pFy25 * _share;\n'
    '      _ufFy[uf].fy26 += _pFy26 * _share;\n'
    '    });\n'
    '  });\n'
    "  var _ufSCJ = (typeof UF_SCJ_DATA !== 'undefined') ? UF_SCJ_DATA : {};\n"
    '  var agg = {};\n'
    '  Object.keys(_ufSCJ).forEach(function(uf){\n'
    '    var r = _ufSCJ[uf];\n'
    '    if(!r.universe) return;\n'
    "    var fy = _ufFy[uf] || {fy25:0, fy26:0};\n"
    '    agg[uf] = {\n'
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
    '  return agg;\n'
    '}'
)

NEW_BUILD = r"""function _yoyBuildUfAgg(){
  /* Usa UF_COB_DATA — fonte: positivação ano 2024x2025x2026.xlsx
     FY25 = Jul/24–Abr/25  |  FY26 = Jul/25–Abr/26
     CNPJs únicos deduplicados por provedor (todos os provedores SCJ) */
  var _cobData = (typeof UF_COB_DATA !== 'undefined') ? UF_COB_DATA : {};
  var agg = {};
  Object.keys(_cobData).forEach(function(uf){
    var r = _cobData[uf];
    if(!r.universe) return;
    var yoyD = r.fy25 > 0 ? Math.round((r.fy26 - r.fy25) / r.fy25 * 100) : 0;
    agg[uf] = {
      total:    r.universe,   /* universo IQVIA ativo */
      scj:      r.fy26,       /* positivados FY26 */
      scj_fy25: r.fy25,       /* positivados FY25 */
      reconq:   r.reconq,     /* FY25 ativo, sem FY26 — alta prioridade */
      ws_puro:  r.ws_puro,    /* nunca comprou — white space puro */
      white_sp: r.white_sp,   /* disponíveis p/ atendimento (= univ - FY26) */
      yoy_gap:  yoyD           /* Δ% FY25→FY26 */
    };
  });
  return agg;
}"""

h = replace_once(h, OLD_BUILD, NEW_BUILD, '_yoyBuildUfAgg atualizado → UF_COB_DATA')

# ═══════════════════════════════════════════════════════════════════════════════
# 4. Atualizar tooltip → 8 métricas (compacto)
# ═══════════════════════════════════════════════════════════════════════════════
OLD_TTIP = (
    '      /* Tooltip — compacto, estado sempre visível no topo */\n'
    "      var ttip = '<div style=\"min-width:170px;font-family:inherit;padding:2px;\">';\n"
    '      /* Header: estado + % lado a lado — sempre visível mesmo se tooltip for cortado */\n'
    '      ttip += \'<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px;padding-bottom:5px;border-bottom:0.5px solid rgba(255,255,255,0.1);">\'\n'
    "        +'<span style=\"font-weight:800;font-size:13px;color:#67e8f9;\">'+uf+'</span>'\n"
    "        +(pct!==null?'<span style=\"font-size:16px;font-weight:900;color:'+pctCol+';\">'+pct+'%</span>':'')\n"
    "        +'</div>';\n"
    '      if(d && d.total > 0){\n'
    "        ttip += '<div style=\"display:grid;grid-template-columns:1fr 1fr;gap:4px;\">'\n"
    '          +\'<div style="background:rgba(255,255,255,0.04);border-radius:4px;padding:4px 6px;">\'\n'
    "            +'<div style=\"font-size:8px;color:#64748b;\">Universo</div>'\n"
    "            +'<div style=\"font-size:12px;font-weight:700;color:#D1D5DB;\">'+d.total.toLocaleString('pt-BR')+'</div>'\n"
    '          +\'</div>\'\n'
    '          +\'<div style="background:rgba(52,211,153,0.08);border-radius:4px;padding:4px 6px;">\''
)

NEW_TTIP = (
    '      /* Tooltip — compacto, estado sempre visível no topo */\n'
    "      var ttip = '<div style=\"min-width:185px;font-family:inherit;padding:2px;\">';\n"
    '      /* Header: estado + % sempre visível */\n'
    '      ttip += \'<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px;padding-bottom:4px;border-bottom:0.5px solid rgba(255,255,255,0.1);">\'\n'
    "        +'<span style=\"font-weight:800;font-size:13px;color:#67e8f9;\">'+uf+'</span>'\n"
    "        +(pct!==null?'<span style=\"font-size:15px;font-weight:900;color:'+pctCol+';\">'+pct+'%</span>':'')\n"
    "        +'</div>';\n"
    '      if(d && d.total > 0){\n'
    '        var _yoyTip = d.scj_fy25>0 ? Math.round((d.scj-d.scj_fy25)/d.scj_fy25*100) : null;\n'
    '        var _yoyC = _yoyTip===null?\'#64748b\':_yoyTip>5?\'#34d399\':_yoyTip>=-5?\'#fbbf24\':\'#ef4444\';\n'
    "        ttip += '<div style=\"display:grid;grid-template-columns:1fr 1fr;gap:3px;\">'\n"
    '          +\'<div style="background:rgba(255,255,255,0.04);border-radius:3px;padding:3px 5px;">\'\n'
    "            +'<div style=\"font-size:7.5px;color:#64748b;\">🏪 Universo IQVIA</div>'\n"
    "            +'<div style=\"font-size:11px;font-weight:700;color:#D1D5DB;\">'+d.total.toLocaleString('pt-BR')+'</div>'\n"
    '          +\'</div>\'\n'
    '          +\'<div style="background:rgba(52,211,153,0.08);border-radius:3px;padding:3px 5px;">\''
)

h = replace_once(h, OLD_TTIP, NEW_TTIP, 'Tooltip header + universo atualizados')

# Continuação do tooltip — substituir os 3 cells restantes
OLD_TTIP2 = (
    "            +'<div style=\"font-size:8px;color:#64748b;\">SCJ FY26</div>'\n"
    "            +'<div style=\"font-size:12px;font-weight:700;color:#34d399;\">'+d.scj.toLocaleString('pt-BR')+'</div>'\n"
    '          +\'</div>\'\n'
    '          +\'<div style="background:rgba(239,68,68,0.06);border-radius:4px;padding:4px 6px;">\'\n'
    "            +'<div style=\"font-size:8px;color:#64748b;\">White Space</div>'\n"
    "            +'<div style=\"font-size:12px;font-weight:700;color:#ef4444;\">'+(d.white_sp||d.total-d.scj).toLocaleString('pt-BR')+'</div>'\n"
    '          +\'</div>\'\n'
    '          +\'<div style="background:rgba(251,191,36,0.06);border-radius:4px;padding:4px 6px;">\'\n'
    "            +'<div style=\"font-size:8px;color:#64748b;\">Alta Prior.</div>'\n"
    "            +'<div style=\"font-size:12px;font-weight:700;color:#fbbf24;\">'+(d.reconq||0).toLocaleString('pt-BR')+'</div>'\n"
    "          +'</div>'\n"
    "          +'</div>';\n"
    "        if(active) ttip += '<div style=\"margin-top:5px;font-size:8px;color:#3d6b63;text-align:center;\">▶ Clique para ver todos os detalhes</div>';"
)

NEW_TTIP2 = (
    "            +'<div style=\"font-size:7.5px;color:#64748b;\">✅ Positiv. FY26</div>'\n"
    "            +'<div style=\"font-size:11px;font-weight:700;color:#34d399;\">'+d.scj.toLocaleString('pt-BR')+'</div>'\n"
    '          +\'</div>\'\n'
    '          +\'<div style="background:rgba(59,130,246,0.08);border-radius:3px;padding:3px 5px;">\'\n'
    "            +'<div style=\"font-size:7.5px;color:#64748b;\">✅ Positiv. FY25</div>'\n"
    "            +'<div style=\"font-size:11px;font-weight:700;color:#93c5fd;\">'+d.scj_fy25.toLocaleString('pt-BR')+'</div>'\n"
    '          +\'</div>\'\n'
    '          +\'<div style="background:rgba(239,68,68,0.06);border-radius:3px;padding:3px 5px;">\'\n'
    "            +'<div style=\"font-size:7.5px;color:#64748b;\">⬜ Disponíveis</div>'\n"
    "            +'<div style=\"font-size:11px;font-weight:700;color:#ef4444;\">'+(d.white_sp||0).toLocaleString('pt-BR')+'</div>'\n"
    '          +\'</div>\'\n'
    '          +\'<div style="background:rgba(251,191,36,0.06);border-radius:3px;padding:3px 5px;">\'\n'
    "            +'<div style=\"font-size:7.5px;color:#64748b;\">🔄 Não Comp. FY26</div>'\n"
    "            +'<div style=\"font-size:11px;font-weight:700;color:#fbbf24;\">'+(d.reconq||0).toLocaleString('pt-BR')+'</div>'\n"
    '          +\'</div>\'\n'
    '          +\'<div style="background:rgba(148,163,184,0.06);border-radius:3px;padding:3px 5px;">\'\n'
    "            +'<div style=\"font-size:7.5px;color:#64748b;\">📭 Nunca Comprou</div>'\n"
    "            +'<div style=\"font-size:11px;font-weight:700;color:#94a3b8;\">'+(d.ws_puro||0).toLocaleString('pt-BR')+'</div>'\n"
    '          +\'</div>\'\n'
    '          +\'<div style="background:rgba(100,116,139,0.06);border-radius:3px;padding:3px 5px;border-left:2px solid \'+_yoyC+\';">\'\n'
    "            +'<div style=\"font-size:7.5px;color:#64748b;\">📈 GAP FY25→FY26</div>'\n"
    "            +'<div style=\"font-size:11px;font-weight:700;color:\'+_yoyC+\';\">'+(_yoyTip===null?'—':(_yoyTip>=0?\'+\':\'\')+_yoyTip+'%')+'</div>'\n"
    "          +'</div>'\n"
    "          +'</div>';\n"
    "        if(active) ttip += '<div style=\"margin-top:4px;font-size:7.5px;color:#3d6b63;text-align:center;\">▶ Clique para ver detalhes e cidades</div>';"
)

h = replace_once(h, OLD_TTIP2, NEW_TTIP2, 'Tooltip 8 métricas completo')

# ═══════════════════════════════════════════════════════════════════════════════
# 5. Atualizar _yoyAggUfClick() → 8 KPIs + tabela cidades
# ═══════════════════════════════════════════════════════════════════════════════
OLD_CLICK = (
    'function _yoyAggUfClick(uf, d){\n'
    '  var drill = document.getElementById(\'yoy-agg-drill\');\n'
    '  if(!drill) return;\n'
    '\n'
    '  var pct    = d.total > 0 ? Math.round(d.scj / d.total * 100) : 0;\n'
    '  var pctCol = pct>=70?\'#34d399\':pct>=40?\'#fbbf24\':pct>=20?\'#f97316\':\'#ef4444\';\n'
    '  var wsPct  = d.total > 0 ? Math.round(d.white_sp / d.total * 100) : 0;\n'
    '\n'
    '  /* Provedores ativos neste estado */\n'
    '  var provsInUF = (PROV_DATA||[]).filter(function(pv){\n'
    '    return (pv.by_uf||[]).some(function(u){ return u[0]===uf && u[2]>0; });\n'
    '  });\n'
    '\n'
    '  /* YoY real: CNPJs SCJ FY25 vs FY26 (dados reais Detalhe RB+CIMED) */\n'
    '  var scj25  = d.scj_fy25 || 0;\n'
    '  var scj26  = d.scj       || 0;\n'
    '  var yoyD   = scj25 > 0 ? Math.round((scj26 - scj25) / scj25 * 100) : null;\n'
    '  var yoyCol = yoyD===null?\'#64748b\':yoyD>5?\'#34d399\':yoyD>=-5?\'#fbbf24\':\'#ef4444\';\n'
)

NEW_CLICK = r"""function _yoyAggUfClick(uf, d){
  var drill = document.getElementById('yoy-agg-drill');
  if(!drill) return;

  var pct    = d.total > 0 ? Math.round(d.scj / d.total * 100) : 0;
  var pct25  = d.total > 0 ? Math.round(d.scj_fy25 / d.total * 100) : 0;
  var pctCol = pct>=70?'#34d399':pct>=40?'#fbbf24':pct>=20?'#f97316':'#ef4444';
  var wsPct  = d.total > 0 ? Math.round(d.white_sp / d.total * 100) : 0;
  var rqPct  = d.total > 0 ? Math.round(d.reconq / d.total * 100) : 0;

  /* YoY real — positivação ano 2024x2025x2026 */
  var scj25  = d.scj_fy25 || 0;
  var scj26  = d.scj       || 0;
  var yoyD   = scj25 > 0 ? Math.round((scj26 - scj25) / scj25 * 100) : null;
  var yoyCol = yoyD===null?'#64748b':yoyD>5?'#34d399':yoyD>=-5?'#fbbf24':'#ef4444';

  /* Cidades top-20 deste estado */
  var _cityCob = (typeof CITY_COB_DATA !== 'undefined') ? (CITY_COB_DATA[uf]||[]) : [];

"""

h = replace_once(h, OLD_CLICK, NEW_CLICK, '_yoyAggUfClick — cabeçalho + variáveis cidades')

# Substituir o conteúdo HTML da função (o html var até o fim da função)
OLD_CLICK_HTML = (
    "  var html = '<div style=\"width:100%;padding:4px;\">'\n"
    '    /* Header UF + % */\n'
    "    +'<div style=\"display:flex;justify-content:space-between;align-items:center;margin-bottom:10px;\">'\n"
    "      +'<div style=\"font-size:24px;font-weight:800;color:#67e8f9;\">'+uf+'</div>'\n"
    "      +'<div style=\"text-align:right;\">'\n"
    "        +'<div style=\"font-size:26px;font-weight:900;color:'+pctCol+';\">'+pct+'%</div>'\n"
    "        +'<div style=\"font-size:8px;color:#94A3B8;\">cobertura SCJ FY26</div>'\n"
    "      +'</div>'\n"
    "    +'</div>'\n"
    '\n'
    '    /* Barra de cobertura */\n'
    "    +'<div style=\"display:flex;height:14px;border-radius:4px;overflow:hidden;gap:1px;margin-bottom:4px;\">'\n"
    "      +'<div style=\"width:'+pct+'%;background:'+pctCol+';\"></div>'\n"
    "      +'<div style=\"flex:1;background:#1e3a4a;\"></div>'\n"
    "    +'</div>'\n"
    "    +'<div style=\"display:flex;gap:10px;margin-bottom:12px;\">'\n"
    "      +'<span style=\"font-size:8px;color:'+pctCol+';\">■ SCJ FY26 '+pct+'%</span>'\n"
    "      +'<span style=\"font-size:8px;color:#4a5568;\">■ White Space '+wsPct+'%</span>'\n"
    "    +'</div>'\n"
    '\n'
    '    /* 2×2 metric grid */\n'
    "    +'<div style=\"display:grid;grid-template-columns:1fr 1fr;gap:6px;margin-bottom:10px;\">'\n"
    '\n'
    '      /* Universo IQVIA */\n'
    "      +'<div style=\"background:rgba(103,232,249,0.06);border-radius:6px;padding:8px 10px;\">'\n"
    "        +'<div style=\"font-size:7.5px;color:#94A3B8;margin-bottom:2px;text-transform:uppercase;letter-spacing:.06em;\">🏪 Universo IQVIA</div>'\n"
    "        +'<div style=\"font-size:19px;font-weight:800;color:#67e8f9;\">'+d.total.toLocaleString('pt-BR')+'</div>'\n"
    "        +'<div style=\"font-size:7px;color:#334155;\">CNPJs únicos rastreados</div>'\n"
    "      +'</div>'\n"
    '\n'
    '      /* White Space */\n'
    "      +'<div style=\"background:rgba(239,68,68,0.06);border-radius:6px;padding:8px 10px;\">'\n"
    "        +'<div style=\"font-size:7.5px;color:#94A3B8;margin-bottom:2px;text-transform:uppercase;letter-spacing:.06em;\">⬜ White Space</div>'\n"
    "        +'<div style=\"font-size:19px;font-weight:800;color:#ef4444;\">'+(d.white_sp||0).toLocaleString('pt-BR')+'</div>'\n"
    "        +'<div style=\"font-size:7px;color:#334155;\">sem SCJ no universo</div>'\n"
    "      +'</div>'\n"
    '\n'
    '      /* Alta Prioridade */\n'
    "      +'<div style=\"background:rgba(251,191,36,0.06);border-radius:6px;padding:8px 10px;\">'\n"
    "        +'<div style=\"font-size:7.5px;color:#94A3B8;margin-bottom:2px;text-transform:uppercase;letter-spacing:.06em;\">🔄 Alta Prioridade</div>'\n"
    "        +'<div style=\"font-size:19px;font-weight:800;color:#fbbf24;\">'+(d.reconq||0).toLocaleString('pt-BR')+'</div>'\n"
    "        +'<div style=\"font-size:7px;color:#334155;\">FY25 ativo · perdemos FY26</div>'\n"
    "      +'</div>'\n"
    '\n'
    '      /* Provedores */\n'
    "      +'<div style=\"background:rgba(167,139,250,0.06);border-radius:6px;padding:8px 10px;\">'\n"
    "        +'<div style=\"font-size:7.5px;color:#94A3B8;margin-bottom:2px;text-transform:uppercase;letter-spacing:.06em;\">🏬 Provedores</div>'\n"
    "        +'<div style=\"font-size:19px;font-weight:800;color:#a78bfa;\">'+provsInUF.length+'</div>'\n"
    "        +'<div style=\"font-size:7px;color:#334155;\">ativos neste estado</div>'\n"
    "      +'</div>'\n"
    '\n'
    "    +'</div>'\n"
    '\n'
    '    /* SCJ Ativos — FY25 vs FY26 (dados reais CNPJs) */\n'
    "    +'<div style=\"background:rgba(34,197,94,0.04);border-radius:7px;padding:9px 12px;border:0.5px solid rgba(34,197,94,0.18);margin-bottom:0;\">'\n"
    "      +'<div style=\"font-size:7.5px;font-weight:800;letter-spacing:.1em;color:#22c55e;text-transform:uppercase;margin-bottom:8px;\">📊 SCJ ATIVOS — FY25 vs FY26 · CNPJs REAIS</div>'\n"
    "      +'<div style=\"display:grid;grid-template-columns:1fr 1fr 1fr;gap:5px;\">'\n"
    '\n'
    '        /* FY25 */\n'
    "        +'<div style=\"background:#0D1117;border-radius:6px;padding:8px 10px;\">'\n"
    "          +'<div style=\"font-size:7px;color:#3b82f6;font-weight:800;text-transform:uppercase;letter-spacing:.06em;margin-bottom:3px;\">FY25</div>'\n"
    "          +'<div style=\"font-size:18px;font-weight:900;color:#93c5fd;\">'+scj25.toLocaleString('pt-BR')+'</div>'\n"
    "          +'<div style=\"font-size:7px;color:#334155;margin-top:2px;\">Jul/24–Mar/25</div>'\n"
    "          +'<div style=\"font-size:7px;color:#60a5fa;margin-top:1px;\">'+(d.total>0?Math.round(scj25/d.total*100)+'% cobertura':'—')+'</div>'\n"
    "        +'</div>'\n"
    '\n'
    '        /* FY26 */\n'
    "        +'<div style=\"background:#0D1117;border-radius:6px;padding:8px 10px;\">'\n"
    "          +'<div style=\"font-size:7px;color:#22c55e;font-weight:800;text-transform:uppercase;letter-spacing:.06em;margin-bottom:3px;\">FY26</div>'\n"
    "          +'<div style=\"font-size:18px;font-weight:900;color:#34d399;\">'+scj26.toLocaleString('pt-BR')+'</div>'\n"
    "          +'<div style=\"font-size:7px;color:#334155;margin-top:2px;\">Jul/25–Mar/26</div>'\n"
    "          +'<div style=\"font-size:7px;color:#22c55e;margin-top:1px;\">'+(d.total>0?Math.round(scj26/d.total*100)+'% cobertura':'—')+'</div>'\n"
    "        +'</div>'\n"
    '\n'
    '        /* Δ% YoY */\n'
    "        +'<div style=\"background:#0D1117;border-radius:6px;padding:8px 10px;border-left:2px solid '+yoyCol+';\">'\n"
    "          +'<div style=\"font-size:7px;color:#94a3b8;font-weight:800;text-transform:uppercase;letter-spacing:.06em;margin-bottom:3px;\">Δ% YoY</div>'\n"
    "          +'<div style=\"font-size:20px;font-weight:900;color:'+yoyCol+';line-height:1;\">'+(yoyD===null?'—':(yoyD>=0?'+':'')+yoyD+'%')+'</div>'\n"
    "          +'<div style=\"font-size:7px;color:#334155;margin-top:4px;\">FY25 → FY26</div>'\n"
    "          +(yoyD!==null?'<div style=\"font-size:7px;margin-top:2px;color:'+yoyCol+';\">'+(yoyD>5?'▲ Crescimento':yoyD>=-5?'→ Estável':'▼ Queda')+'</div>':'')\n"
    "        +'</div>'\n"
    '\n'
    "      +'</div>'\n"
    "      +'<div style=\"font-size:7px;color:#1e3a4a;margin-top:6px;font-style:italic;\">Fonte: Detalhe RB + Detalhe CIMED · CNPJs únicos deduplicados · Jan–Mar de cada período</div>'\n"
    "    +'</div>'\n"
    '\n'
    "    +'</div>';\n"
    '\n'
    "  drill.style.cssText = 'background:#161B22;border-radius:8px;padding:14px;'\n"
    "    +'border:0.5px solid rgba(103,232,249,0.12);min-height:360px;overflow-y:auto;';\n"
    '  drill.innerHTML = html;\n'
    '}'
)

NEW_CLICK_HTML = r"""  var _kpiStyle = 'border-radius:6px;padding:8px 10px;';

  /* ── Tabela cidades ── */
  var _cityRows = '';
  if(_cityCob.length > 0){
    _cityRows = '<table style="width:100%;border-collapse:collapse;font-size:9px;">'
      +'<thead><tr style="border-bottom:0.5px solid rgba(255,255,255,0.08);">'
      +'<th style="text-align:left;padding:3px 4px;color:#64748b;font-weight:600;">Cidade</th>'
      +'<th style="text-align:right;padding:3px 4px;color:#64748b;font-weight:600;">Univ</th>'
      +'<th style="text-align:right;padding:3px 4px;color:#22c55e;font-weight:600;">FY26</th>'
      +'<th style="text-align:right;padding:3px 4px;color:#93c5fd;font-weight:600;">FY25</th>'
      +'<th style="text-align:right;padding:3px 4px;color:#64748b;font-weight:600;">Cob%</th>'
      +'<th style="text-align:right;padding:3px 4px;color:#fbbf24;font-weight:600;">Reconv</th>'
      +'</tr></thead><tbody>';
    _cityCob.forEach(function(c){
      var cPctCol = c.p>=70?'#34d399':c.p>=40?'#fbbf24':c.p>=20?'#f97316':'#ef4444';
      _cityRows += '<tr style="border-bottom:0.5px solid rgba(255,255,255,0.04);">'
        +'<td style="padding:3px 4px;color:#cbd5e1;font-size:8.5px;">'+c.n+'</td>'
        +'<td style="text-align:right;padding:3px 4px;color:#94a3b8;">'+c.u.toLocaleString('pt-BR')+'</td>'
        +'<td style="text-align:right;padding:3px 4px;color:#34d399;font-weight:700;">'+c.f26.toLocaleString('pt-BR')+'</td>'
        +'<td style="text-align:right;padding:3px 4px;color:#93c5fd;">'+c.f25.toLocaleString('pt-BR')+'</td>'
        +'<td style="text-align:right;padding:3px 4px;font-weight:700;color:'+cPctCol+';">'+c.p+'%</td>'
        +'<td style="text-align:right;padding:3px 4px;color:#fbbf24;">'+c.rq.toLocaleString('pt-BR')+'</td>'
        +'</tr>';
    });
    _cityRows += '</tbody></table>';
  }

  var html = '<div style="width:100%;padding:4px;">'

    /* ── Header ── */
    +'<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px;">'
      +'<div style="font-size:22px;font-weight:800;color:#67e8f9;">'+uf+'</div>'
      +'<div style="text-align:right;">'
        +'<div style="font-size:24px;font-weight:900;color:'+pctCol+';">'+pct+'%</div>'
        +'<div style="font-size:7.5px;color:#94A3B8;">cobertura FY26</div>'
      +'</div>'
    +'</div>'

    /* ── Barra cobertura ── */
    +'<div style="display:flex;height:10px;border-radius:3px;overflow:hidden;gap:1px;margin-bottom:3px;">'
      +'<div style="width:'+pct+'%;background:'+pctCol+';"></div>'
      +'<div style="flex:1;background:#1e3a4a;"></div>'
    +'</div>'
    +'<div style="display:flex;gap:12px;margin-bottom:10px;">'
      +'<span style="font-size:7.5px;color:'+pctCol+';">■ FY26 '+pct+'%</span>'
      +'<span style="font-size:7.5px;color:#93c5fd;">■ FY25 '+pct25+'%</span>'
      +'<span style="font-size:7.5px;color:#4a5568;">■ Disponível '+wsPct+'%</span>'
    +'</div>'

    /* ── 8 KPI cards em grid 2×4 ── */
    +'<div style="display:grid;grid-template-columns:1fr 1fr;gap:5px;margin-bottom:10px;">'

      /* 1. Universo IQVIA */
      +'<div style="'+_kpiStyle+'background:rgba(103,232,249,0.07);">'
        +'<div style="font-size:7px;color:#94A3B8;text-transform:uppercase;letter-spacing:.06em;margin-bottom:2px;">🏪 Universo IQVIA Ativo</div>'
        +'<div style="font-size:18px;font-weight:800;color:#67e8f9;">'+d.total.toLocaleString('pt-BR')+'</div>'
        +'<div style="font-size:7px;color:#334155;">CNPJs únicos IQVIA</div>'
      +'</div>'

      /* 2. Positivados FY26 */
      +'<div style="'+_kpiStyle+'background:rgba(34,197,94,0.07);">'
        +'<div style="font-size:7px;color:#94A3B8;text-transform:uppercase;letter-spacing:.06em;margin-bottom:2px;">✅ Positivados FY26</div>'
        +'<div style="font-size:18px;font-weight:800;color:#34d399;">'+scj26.toLocaleString('pt-BR')+'</div>'
        +'<div style="font-size:7px;color:#334155;">'+pct+'% · Jul/25–Abr/26</div>'
      +'</div>'

      /* 3. Positivados FY25 */
      +'<div style="'+_kpiStyle+'background:rgba(59,130,246,0.07);">'
        +'<div style="font-size:7px;color:#94A3B8;text-transform:uppercase;letter-spacing:.06em;margin-bottom:2px;">✅ Positivados FY25</div>'
        +'<div style="font-size:18px;font-weight:800;color:#93c5fd;">'+scj25.toLocaleString('pt-BR')+'</div>'
        +'<div style="font-size:7px;color:#334155;">'+pct25+'% · Jul/24–Abr/25</div>'
      +'</div>'

      /* 4. Disponíveis p/ Atendimento */
      +'<div style="'+_kpiStyle+'background:rgba(239,68,68,0.07);">'
        +'<div style="font-size:7px;color:#94A3B8;text-transform:uppercase;letter-spacing:.06em;margin-bottom:2px;">⬜ Disponíveis p/ Atend.</div>'
        +'<div style="font-size:18px;font-weight:800;color:#ef4444;">'+(d.white_sp||0).toLocaleString('pt-BR')+'</div>'
        +'<div style="font-size:7px;color:#334155;">'+wsPct+'% · universo − FY26</div>'
      +'</div>'

      /* 5. Não Compraram FY26 */
      +'<div style="'+_kpiStyle+'background:rgba(251,191,36,0.07);">'
        +'<div style="font-size:7px;color:#94A3B8;text-transform:uppercase;letter-spacing:.06em;margin-bottom:2px;">🔄 Não Compraram FY26</div>'
        +'<div style="font-size:18px;font-weight:800;color:#fbbf24;">'+(d.reconq||0).toLocaleString('pt-BR')+'</div>'
        +'<div style="font-size:7px;color:#334155;">'+rqPct+'% · FY25 sim · FY26 não</div>'
      +'</div>'

      /* 6. Nunca Comprou */
      +'<div style="'+_kpiStyle+'background:rgba(148,163,184,0.07);">'
        +'<div style="font-size:7px;color:#94A3B8;text-transform:uppercase;letter-spacing:.06em;margin-bottom:2px;">📭 Nunca Comprou SCJ</div>'
        +'<div style="font-size:18px;font-weight:800;color:#94a3b8;">'+(d.ws_puro||0).toLocaleString('pt-BR')+'</div>'
        +'<div style="font-size:7px;color:#334155;">Sem FY25 e sem FY26</div>'
      +'</div>'

      /* 7. % Cobertura FY26 */
      +'<div style="'+_kpiStyle+'background:rgba('+( pct>=70?'52,211,153':pct>=40?'251,191,36':pct>=20?'249,115,22':'239,68,68' )+',0.07);">'
        +'<div style="font-size:7px;color:#94A3B8;text-transform:uppercase;letter-spacing:.06em;margin-bottom:2px;">📊 % Cobertura FY26</div>'
        +'<div style="font-size:22px;font-weight:900;color:'+pctCol+';">'+pct+'%</div>'
        +'<div style="font-size:7px;color:#334155;">do universo IQVIA ativo</div>'
      +'</div>'

      /* 8. GAP FY25→FY26 */
      +'<div style="'+_kpiStyle+'border-left:2px solid '+yoyCol+';background:rgba(100,116,139,0.06);">'
        +'<div style="font-size:7px;color:#94A3B8;text-transform:uppercase;letter-spacing:.06em;margin-bottom:2px;">📈 GAP FY25→FY26</div>'
        +'<div style="font-size:22px;font-weight:900;color:'+yoyCol+';line-height:1;">'+(yoyD===null?'—':(yoyD>=0?'+':'')+yoyD+'%')+'</div>'
        +'<div style="font-size:7px;color:#334155;margin-top:2px;">'+(yoyD!==null?(yoyD>5?'▲ Crescimento':yoyD>=-5?'→ Estável':'▼ Queda em positivação'):'Sem dado FY25')+'</div>'
      +'</div>'

    +'</div>'

    /* ── Top Cidades ── */
    +(_cityCob.length > 0
      ? '<div style="margin-top:2px;">'
          +'<div style="font-size:7.5px;font-weight:700;color:#64748b;letter-spacing:.08em;text-transform:uppercase;margin-bottom:6px;">'
            +'📍 TOP CIDADES — '+uf
          +'</div>'
          +_cityRows
          +'<div style="font-size:7px;color:#1e3a4a;margin-top:5px;font-style:italic;">'
            +'Fonte: positivação 2024x2025x2026 · top 20 cidades por universo'
          +'</div>'
        +'</div>'
      : '')

  +'</div>';

  drill.style.cssText = 'background:#161B22;border-radius:8px;padding:14px;'
    +'border:0.5px solid rgba(103,232,249,0.12);min-height:360px;overflow-y:auto;';
  drill.innerHTML = html;
}"""

h = replace_once(h, OLD_CLICK_HTML, NEW_CLICK_HTML, '_yoyAggUfClick — 8 KPIs + tabela cidades')

# ═══════════════════════════════════════════════════════════════════════════════
# Verificações
# ═══════════════════════════════════════════════════════════════════════════════
assert 'const UF_COB_DATA'                    in h, 'ERRO: UF_COB_DATA não injetado'
assert 'const CITY_COB_DATA'                  in h, 'ERRO: CITY_COB_DATA não injetado'
assert "typeof UF_COB_DATA !== 'undefined'"   in h, 'ERRO: _yoyBuildUfAgg não atualizado'
assert 'CITY_COB_DATA[uf]'                    in h, 'ERRO: cidade lookup não inserido'
assert '✅ Positivados FY26'                   in h, 'ERRO: KPI FY26 não inserido'
assert '✅ Positivados FY25'                   in h, 'ERRO: KPI FY25 não inserido'
assert '⬜ Disponíveis p/ Atend.'              in h, 'ERRO: KPI disponíveis não inserido'
assert '🔄 Não Compraram FY26'                 in h, 'ERRO: KPI reconq não inserido'
assert '📭 Nunca Comprou SCJ'                  in h, 'ERRO: KPI ws_puro não inserido'
assert '📊 % Cobertura FY26'                   in h, 'ERRO: KPI cobertura% não inserido'
assert '📈 GAP FY25→FY26'                      in h, 'ERRO: KPI GAP não inserido'
assert '📍 TOP CIDADES'                        in h, 'ERRO: tabela cidades não inserida'
assert 'prov-yoy-body'                         in h, 'ERRO: prov-yoy-body perdido'
assert h.count('function renderProvYoYCard') == 1, 'ERRO: renderProvYoYCard duplicada'
print('Verificações: OK')
print(f'Tamanho final: {len(h):,} chars')

# ═══════════════════════════════════════════════════════════════════════════════
# Salvar
# ═══════════════════════════════════════════════════════════════════════════════
DASH.write_text(h, encoding='utf-8')
shutil.copy(DASH, VER / f'Dashboard_Farma_Sul_{ts}_CobV2.html')
shutil.copy(DASH, DL  / f'Dashboard_FarmaSul_Giovano_{ts}.html')
print(f'Versao:    Dashboard_Farma_Sul_{ts}_CobV2.html')
print(f'Downloads: Dashboard_FarmaSul_Giovano_{ts}.html')
print('DONE.')
