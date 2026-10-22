"""
Adiciona janabr25 (Jan-Abr/25) e janabr26 (Jan-Abr/26) ao DN_INTOC_GRUPOS
e insere botões de filtro no card Intocáveis × Grupo Provedor.

janabr25 = acumulado 10 meses FY25 até Abril/25 (Jul/24–Abr/25)
           → DIRETO/OL sheet, col 44 (D=locao/kids), col 47 (A=spray proxy)

janabr26 = acumulado 10 meses FY26 até Abril/26 (Jul/25–Abr/26)
           → DIRETO/OL sheet, col 44 FY26 section + BASE tab para spray170 correto
           → GAM: CERAS JOHNSON jan-abr/26 agregado
           → Gaúcha: positivação file meses 20-23 (Jan-Abr/26)
"""
import pandas as pd, json, re, shutil
from datetime import datetime

EXP_PATH  = r'_Recursos\Giovano SCJ\Expandindo Distribuição Farma - Abril (FY26)\Expandindo Distribuição Farma - Abril (FY26).xlsx'
GAM_HIST  = r'_Recursos\Giovano SCJ\gam\vendas gam ano\RELATÓRIO GIOVANO 2024x2025.xlsx'
GAM_2026  = r'_Recursos\Giovano SCJ\gam\vendas gam ano\CERAS JOHNSON jan-fev-mar-abri-2026.xlsx'
GAUCHA_P  = r'_Recursos\Giovano SCJ\GAUCHA\positivação gaucha.xlsx'
HTML_FILE = 'Dashboard_Farma_Sul_20260512_2220.html'

EAN_LOCAO = 7894650005712
EAN_SPRAY = 7894650009567
EAN_KIDS  = 7894650940006

DIRETO_CLIENTS = [
    'ARAUJO','DROGAL','DROGARIA CATARINENSE','DROGARIA GLOBO',
    'DROGARIA ROSARIO','DROGARIA TAMOIO','DROGARIA VENANCIO','DROGASIL',
    'DROGASMIL','DSP','EXTRAFARMA','FARMA CONDE','INDIANA','NISSEI',
    'PACHECO','PAGUE MENOS','PANVEL','PRECO POPULAR','RAIA','REDEPHARMA',
    'SAO JOAO FARMACIAS'
]
OL_CLIENTS = ['OL MG','OL NE','OL PR/SC','OL RJ','OL RS','OL SPC','OL SPI']

def safe_dn(pdvs, total):
    return round(pdvs / total * 100, 1) if total > 0 else 0.0

def to_int(v):
    try:
        return int(v) if pd.notna(v) else 0
    except:
        return 0

def mk_period_obj(total, locao, spray, kids):
    algum = max(locao, spray, kids)
    todos = min(locao, spray, kids)
    return {
        'soma': {
            'total': total, 'algum': algum, 'dnAlgum': safe_dn(algum, total),
            'dois': algum,  'dnDois': safe_dn(algum, total),
            'todos': todos, 'dnTodos': safe_dn(todos, total)
        },
        'kids200':  {'total': total, 'pdvs': kids,  'dn': safe_dn(kids,  total)},
        'spray170': {'total': total, 'pdvs': spray, 'dn': safe_dn(spray, total)},
        'locao200': {'total': total, 'pdvs': locao, 'dn': safe_dn(locao, total)},
    }

# ─── 1. DIRETO/OL — FY25 monthly (col 44 = Apr/25 cumulative) ───────────────
print("Reading DIRETO/OL FY25 April data...")
xl = pd.ExcelFile(EXP_PATH)
df_d  = xl.parse('DIRETO', header=None)
df_ol = xl.parse('OL',     header=None)

# FY25 rows: DIRETO 6-26, OL 5-11  |  FY26 rows: DIRETO 109-129, OL 53-59
# Col 44 = D Apr (locao/kids cumulative),  Col 47 = A Apr (spray proxy)

janabr = {}  # janabr[group] = {janabr25: {...}, janabr26: {...}}

for i, cl in enumerate(DIRETO_CLIENTS):
    row25 = df_d.iloc[6 + i]
    row26 = df_d.iloc[109 + i]
    univ = to_int(row25.iloc[2])

    # janabr25: FY25 col 44 (D) and 47 (A)
    d25_locao = to_int(row25.iloc[44]); d25_spray = to_int(row25.iloc[47])
    # janabr26: FY26 col 44 (D) only — spray comes from BASE tab below
    d26_locao = to_int(row26.iloc[44]); d26_univ  = to_int(row26.iloc[2])
    if d26_univ == 0: d26_univ = univ

    janabr[cl] = {
        'janabr25': (univ,   d25_locao, d25_spray, d25_locao),
        'janabr26': (d26_univ, d26_locao, None, d26_locao)  # spray26 filled below
    }

for i, ol in enumerate(OL_CLIENTS):
    row25 = df_ol.iloc[5 + i]
    row26 = df_ol.iloc[53 + i]
    univ = to_int(row25.iloc[2])

    d25_locao = to_int(row25.iloc[44]); d25_spray = to_int(row25.iloc[47])
    d26_locao = to_int(row26.iloc[44]); d26_univ  = to_int(row26.iloc[2])
    if d26_univ == 0: d26_univ = univ

    janabr[ol] = {
        'janabr25': (univ,   d25_locao, d25_spray, d25_locao),
        'janabr26': (d26_univ, d26_locao, None, d26_locao)
    }

# ─── 2. Fill spray170 janabr26 from BASE tab (correct EAN 7894650009567) ────
print("Reading BASE tab for spray170 janabr26...")
df_base = pd.read_excel(EXP_PATH, sheet_name='Base', header=4)
col_spray = 'Ean 007894650009567 PDVS'
df_base[col_spray] = pd.to_numeric(df_base[col_spray], errors='coerce').fillna(0)
df_base['Bandeira_up'] = df_base['Bandeira'].astype(str).str.upper().str.strip()

# OL mapping
df_ol_tab = pd.read_excel(EXP_PATH, sheet_name='Base OL', header=None)
header_row = next(i for i,r in df_ol_tab.iterrows() if any('cnpj' in str(v).lower() for v in r))
df_ol_map = pd.read_excel(EXP_PATH, sheet_name='Base OL', header=header_row)
ol_col  = [c for c in df_ol_map.columns if 'OL' in str(c).upper() or c == 'OL'][-1]
cnpj_col = [c for c in df_ol_map.columns if 'CNPJ' in str(c).upper()][0]
df_ol_map['CNPJ_str'] = df_ol_map[cnpj_col].astype(str).str.replace(r'\.0$','',regex=True)
df_base['CNPJ_str'] = df_base['CNPJ'].astype(str).str.replace(r'\.0$','',regex=True)
df_merged = df_base.merge(df_ol_map[['CNPJ_str', ol_col]], on='CNPJ_str', how='left')

for cl in DIRETO_CLIENTS:
    sub = df_base[df_base['Bandeira_up'] == cl.upper()]
    spray_pdvs = int((sub[col_spray] > 0).sum())
    t, lo, _, ki = janabr[cl]['janabr26']
    janabr[cl]['janabr26'] = (t, lo, spray_pdvs, ki)

for ol in OL_CLIENTS:
    sub = df_merged[df_merged[ol_col].astype(str).str.upper().str.strip() == ol.upper()]
    if len(sub) == 0:
        sub = df_merged[df_merged[ol_col].astype(str).str.upper().str.contains(ol.replace('OL ','').upper(), na=False)]
    spray_pdvs = int((sub[col_spray] > 0).sum())
    t, lo, _, ki = janabr[ol]['janabr26']
    janabr[ol]['janabr26'] = (t, lo, spray_pdvs, ki)

# ─── 3. GAM — Jan-Abr 2025 and 2026 ─────────────────────────────────────────
print("Computing GAM Jan-Abr...")
df_hist = pd.read_excel(GAM_HIST)
df_2026 = pd.read_excel(GAM_2026)

def clean_ean(v):
    try: return int(round(float(v)))
    except: return None

def gam_janabr(dfs, ean_col='CD EAN MERCADORIA', cnpj_col='CNPJ CLIENTE'):
    df = pd.concat(dfs, ignore_index=True)
    df['EAN_int'] = df[ean_col].apply(clean_ean)
    df['CNPJ_s'] = df[cnpj_col].astype(str).str.replace(r'\.0$','',regex=True)
    total = len(df['CNPJ_s'].unique())
    def pdvs(ean):
        m = (df['EAN_int'] == ean) & (df.get('QUANTIDADES TOTAIS', pd.Series(1, index=df.index)) > 0)
        return len(df.loc[m, 'CNPJ_s'].unique())
    return total, pdvs(EAN_LOCAO), pdvs(EAN_SPRAY), pdvs(EAN_KIDS)

gam_ja25 = gam_janabr([df_hist[(df_hist['ANO']==2025) & (df_hist['MES'].isin(['jan','fev','mar','abr']))]])
gam_ja26 = gam_janabr([df_2026[(df_2026['ANO']==2026) & (df_2026['MES'].isin(['jan','fev','mar','abr']))]])
janabr['GAM'] = {'janabr25': gam_ja25, 'janabr26': gam_ja26}
print(f"  GAM janabr25: total={gam_ja25[0]}, spray={safe_dn(gam_ja25[2],gam_ja25[0])}%")
print(f"  GAM janabr26: total={gam_ja26[0]}, spray={safe_dn(gam_ja26[2],gam_ja26[0])}%")

# ─── 4. Gaúcha — Jan-Abr 2025 (idx 8-11) and 2026 (idx 20-23) ──────────────
print("Computing Gaúcha Jan-Abr...")
df_g = pd.read_excel(GAUCHA_P, header=None)
ROW_TOTAL = 2; ROW_SPRAY = 3; ROW_KIDS = 14; ROW_LOCAO = 15

def gaucha_pdvs_col(idx): return 9 + (idx * 3)

def gaucha_period(idx_list):
    vals = {r: [int(df_g.iloc[r, gaucha_pdvs_col(i)] or 0) if pd.notna(df_g.iloc[r, gaucha_pdvs_col(i)]) else 0
                for i in idx_list] for r in [ROW_TOTAL, ROW_SPRAY, ROW_KIDS, ROW_LOCAO]}
    total = max(vals[ROW_TOTAL]) if vals[ROW_TOTAL] else 0
    locao = max(vals[ROW_LOCAO]); spray = max(vals[ROW_SPRAY]); kids = max(vals[ROW_KIDS])
    return total, locao, spray, kids

gaucha_ja25 = gaucha_period(range(8, 12))   # 2025/JAN-ABR = indices 8,9,10,11
gaucha_ja26 = gaucha_period(range(20, 24))  # 2026/JAN-ABR = indices 20,21,22,23
janabr['GAUCHA FARMA'] = {'janabr25': gaucha_ja25, 'janabr26': gaucha_ja26}
print(f"  Gaúcha janabr25: total={gaucha_ja25[0]}, spray={safe_dn(gaucha_ja25[2],gaucha_ja25[0])}%")
print(f"  Gaúcha janabr26: total={gaucha_ja26[0]}, spray={safe_dn(gaucha_ja26[2],gaucha_ja26[0])}%")

# ─── 5. Patch HTML ───────────────────────────────────────────────────────────
print("\nPatching HTML...")
with open(HTML_FILE, encoding='utf-8') as f:
    html = f.read()

# 5a. Add janabr25/janabr26 to each group in DN_INTOC_GRUPOS
# Find block and parse existing JSON-like structure, then add fields
# Strategy: use regex to find each group and append janabr25/janabr26 before closing }

def build_janabr_js(t, l, s, k):
    obj = mk_period_obj(t, l, s, k)
    return json.dumps(obj, separators=(', ', ': '))

# Find DN_INTOC_GRUPOS block
m = re.search(r'(const DN_INTOC_GRUPOS = \{.*?\n\};)', html, re.DOTALL)
if not m:
    print("ERROR: DN_INTOC_GRUPOS not found"); exit(1)

old_block = m.group(1)
new_block = old_block

ALL_GROUPS = DIRETO_CLIENTS + OL_CLIENTS + ['GAM', 'GAUCHA FARMA']
for grp in ALL_GROUPS:
    if grp not in janabr:
        print(f"  WARNING: {grp} not in janabr, skipping"); continue
    t25, l25, s25, k25 = janabr[grp]['janabr25']
    t26, l26, s26, k26 = janabr[grp]['janabr26']
    ja25_js = build_janabr_js(t25, l25, s25, k25)
    ja26_js = build_janabr_js(t26, l26, s26, k26)

    insert_snippet = f',\n    "janabr25": {ja25_js},\n    "janabr26": {ja26_js}\n  }}'

    # Find closing of this group: look for "meses": {...} ... }  }  (end of group)
    # Each group ends with:  \n  },\n  "NEXT_GROUP"  OR  \n  },\n};
    gname_esc = re.escape(json.dumps(grp))
    # Match the group block and replace closing
    pat = re.compile(
        r'(' + gname_esc + r':\s*\{.*?)(^\s*\},?)',
        re.DOTALL | re.MULTILINE
    )
    # Better: find the group and its last line before }, then insert janabr lines
    # Find the specific group's "meses" key end
    grp_pos = new_block.find(f'"{grp}": {{')
    if grp_pos == -1:
        print(f"  WARNING: {grp} not found in block"); continue

    # Find end of "meses" object for this group
    # After "meses": { ... } we have \n  },  (end of group)
    # Since each group is nested 2 levels:
    # Search for the pattern:  \n    },\n  },  which closes meses then group
    search_from = grp_pos
    # Find the meses block end for this group
    meses_key = new_block.find('"meses":', search_from)
    if meses_key == -1:
        print(f"  WARNING: meses not found for {grp}"); continue

    # Count braces from meses position to find its closing }
    pos = meses_key + len('"meses":')
    depth = 0; found_open = False
    for ci, ch in enumerate(new_block[pos:]):
        if ch == '{': depth += 1; found_open = True
        elif ch == '}':
            depth -= 1
            if found_open and depth == 0:
                meses_end = pos + ci  # position of closing } of meses
                break

    # After meses closing }, there's \n  } (group closing)
    # We need to insert janabr25/janabr26 BEFORE the group closing
    # Find the group closing: first occurrence of \n  } after meses_end
    after_meses = new_block[meses_end+1:meses_end+20]
    # Insert before the group's closing }
    group_close_search = new_block.find('\n  }', meses_end)
    if group_close_search == -1:
        print(f"  WARNING: group close not found for {grp}"); continue

    # Insert janabr keys
    ja_insert = f',\n    "janabr25": {ja25_js},\n    "janabr26": {ja26_js}'
    new_block = new_block[:meses_end+1] + ja_insert + new_block[meses_end+1:]

html = html.replace(old_block, new_block, 1)
print(f"  Added janabr to {len(ALL_GROUPS)} groups")

# 5b. Update _igSetPeriodo to handle 'janabr25' and 'janabr26'
old_setperiodo = """window._igSetPeriodo = function(p){
    _periodo = p;
    var mesSel = document.getElementById('intoc-g-mes-sel');
    if(mesSel) mesSel.style.display = (p==='mes') ? '' : 'none';
    ['fytd25','fytd26','mes'].forEach(function(id){
      var btn = document.getElementById('ig-btn-'+id);
      if(!btn) return;
      btn.className = 'tgl' + (id===p ? ' active blue' : '');
    });
    window._igRender"""

new_setperiodo = """window._igSetPeriodo = function(p){
    _periodo = p;
    var mesSel = document.getElementById('intoc-g-mes-sel');
    if(mesSel) mesSel.style.display = (p==='mes') ? '' : 'none';
    ['fytd25','fytd26','janabr25','janabr26','mes'].forEach(function(id){
      var btn = document.getElementById('ig-btn-'+id);
      if(!btn) return;
      btn.className = 'tgl' + (id===p ? ' active blue' : '');
    });
    window._igRender"""

if old_setperiodo in html:
    html = html.replace(old_setperiodo, new_setperiodo, 1)
    print("  _igSetPeriodo updated")
else:
    print("  WARNING: _igSetPeriodo old text not found")

# 5c. Update _igRender to handle 'janabr25' and 'janabr26'
old_render_period = """    if(_periodo === 'fytd25'){
      periodoData = data.fytd25;
      periodoLabel = 'FYTD25 (Jul/24–Mar/25)';
    } else if(_periodo === 'fytd26'){
      periodoData = data.fytd26;
      periodoLabel = 'FYTD26 (Jul/25–Abr/26)';
    } else {"""

new_render_period = """    if(_periodo === 'fytd25'){
      periodoData = data.fytd25;
      periodoLabel = 'FYTD25 (Jul/24–Jun/25)';
    } else if(_periodo === 'fytd26'){
      periodoData = data.fytd26;
      periodoLabel = 'FYTD26 (Jul/25–Abr/26)';
    } else if(_periodo === 'janabr25'){
      periodoData = data.janabr25;
      periodoLabel = 'Jan–Abr/25';
    } else if(_periodo === 'janabr26'){
      periodoData = data.janabr26;
      periodoLabel = 'Jan–Abr/26';
    } else {"""

if old_render_period in html:
    html = html.replace(old_render_period, new_render_period, 1)
    print("  _igRender period handling updated")
else:
    print("  WARNING: old render period text not found, trying search...")
    idx = html.find("periodoLabel = 'FYTD25")
    print(f"  FYTD25 label found at {idx}")
    print(repr(html[idx-60:idx+200]))

# 5d. Update badge to include DISTRIBUIDOR type
old_badge = """      var isOL = _OL.indexOf(grupo) !== -1;
      badge.textContent = isOL ? 'OL' : 'DIRETO';
      badge.style.background = isOL ? 'rgba(96,165,250,0.12)' : 'rgba(251,191,36,0.12)';
      badge.style.color = isOL ? '#60a5fa' : '#fbbf24';
      badge.style.borderColor = isOL ? 'rgba(96,165,250,0.35)' : 'rgba(251,191,36,0.35)';"""

new_badge = """      var isOL = _OL.indexOf(grupo) !== -1;
      var isDist = _DISTRIBUIDORES.indexOf(grupo) !== -1;
      badge.textContent = isDist ? 'DISTRIB' : isOL ? 'OL' : 'DIRETO';
      badge.style.background = isDist ? 'rgba(52,211,153,0.12)' : isOL ? 'rgba(96,165,250,0.12)' : 'rgba(251,191,36,0.12)';
      badge.style.color = isDist ? '#34d399' : isOL ? '#60a5fa' : '#fbbf24';
      badge.style.borderColor = isDist ? 'rgba(52,211,153,0.35)' : isOL ? 'rgba(96,165,250,0.35)' : 'rgba(251,191,36,0.35)';"""

if old_badge in html:
    html = html.replace(old_badge, new_badge, 1)
    print("  Badge updated for DISTRIBUIDOR")

# 5e. Add buttons Jan-Abr/25 and Jan-Abr/26 next to FYTD buttons
old_buttons = '''<button id="ig-btn-fytd25" class="tgl" onclick="window._igSetPeriodo('fytd25')">FYTD25</button>
        <button id="ig-btn-fytd26" class="tgl active blue" onclick="window._igSetPeriodo('fytd26')">FYTD26</button>
        <button id="ig-btn-mes"    class="tgl"             onclick="window._igSetPeriodo('mes')">Por M&#234;s</button>'''

new_buttons = '''<button id="ig-btn-fytd25"   class="tgl" onclick="window._igSetPeriodo('fytd25')">FYTD25</button>
        <button id="ig-btn-fytd26"   class="tgl active blue" onclick="window._igSetPeriodo('fytd26')">FYTD26</button>
        <button id="ig-btn-janabr25" class="tgl" onclick="window._igSetPeriodo('janabr25')" style="font-size:10px">Jan&#8211;Abr/25</button>
        <button id="ig-btn-janabr26" class="tgl" onclick="window._igSetPeriodo('janabr26')" style="font-size:10px">Jan&#8211;Abr/26</button>
        <button id="ig-btn-mes"      class="tgl" onclick="window._igSetPeriodo('mes')">Por M&#234;s</button>'''

if old_buttons in html:
    html = html.replace(old_buttons, new_buttons, 1)
    print("  Buttons Jan-Abr/25 and Jan-Abr/26 added")
else:
    print("  WARNING: old buttons text not found")
    idx = html.find('ig-btn-fytd25')
    print(f"  Found at {idx}")
    print(repr(html[idx-10:idx+250]))

# ─── 6. Save ──────────────────────────────────────────────────────────────────
ts = datetime.now().strftime('%Y%m%d_%H%M')
backup = f'versoes/Dashboard_Farma_Sul_{ts}.html'
shutil.copy(HTML_FILE, backup)
print(f"\nBackup: {backup}")

with open(HTML_FILE, 'w', encoding='utf-8') as f:
    f.write(html)
print(f"Saved {HTML_FILE} ({len(html):,} chars)")

import os, shutil as sh
dl = os.path.join(os.path.expanduser('~'), 'Downloads', f'Dashboard_FarmaSul_Giovano_{ts}.html')
sh.copy(HTML_FILE, dl)
print(f"Downloads: {dl}")
