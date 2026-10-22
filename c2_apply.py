import re, shutil, sys, os
sys.stdout.reconfigure(encoding='utf-8')

BASE = r'C:\Users\valqu\OneDrive\Documentos\Claude\Projects\projeto Dashboard_farma_sul'
SRC  = BASE + r'\Dashboard_farma_sul\Dashboard_Farma_Sul_20260512_2220.html'
BKP  = BASE + r'\Dashboard_farma_sul\versoes\Dashboard_Farma_Sul_20260513_1200_PreC2.html'
OUT  = BASE + r'\Dashboard_farma_sul\versoes\Dashboard_Farma_Sul_20260513_1205_C2.html'

shutil.copy2(SRC, BKP)
print(f'Backup: {os.path.basename(BKP)}')

with open(SRC, encoding='utf-8') as f:
    content = f.read()

orig_lines = len(content.splitlines())
c = content
ok_count = 0

def patch(label, old, new, src):
    if old not in src:
        print(f'  MISS  {label}')
        return src, False
    n = src.replace(old, new, 1)
    print(f'  OK    {label}')
    return n, True

# ════════════════════════════════════════════════════════════════════════════
# 1. CSS — add .cmp-row and .cmp-col after .u-bar-bg
# ════════════════════════════════════════════════════════════════════════════
print('\n=== CSS ===')
CSS_ANCHOR = '.u-bar-bg{background:rgba(245,225,164,0.08);border-radius:2px;height:4px;width:52px;margin-top:3px;overflow:hidden;}'
CSS_ADD    = (
    '.u-bar-bg{background:rgba(245,225,164,0.08);border-radius:2px;height:4px;width:52px;margin-top:3px;overflow:hidden;}\n'
    '.cmp-row{display:flex;gap:10px;padding:0 0 10px;}\n'
    '.cmp-col{flex:1;min-width:0;}'
)
c, ok = patch('add .cmp-row + .cmp-col', CSS_ANCHOR, CSS_ADD, c)
if not ok: sys.exit(1)
ok_count += 1

# ════════════════════════════════════════════════════════════════════════════
# 2. HTML — ⊞ toggle buttons (insert before each legend div)
# ════════════════════════════════════════════════════════════════════════════
print('\n=== Botões ⊞ ===')

clients = ['sjc', 'sj', 'ns', 'cl', 'pv', 'gam', 'gch', 'rio']
# sjc/sj are nested deeper (10 spaces); others use 8 spaces
indent_map = {'sjc': '          ', 'sj': '          ',
              'ns': '        ', 'cl': '        ', 'pv': '        ',
              'gam': '        ', 'gch': '        ', 'rio': '        '}

for pfx in clients:
    ind    = indent_map[pfx]
    anchor = f'{ind}<div id="{pfx}-line-legend"'
    btn    = (
        f'{ind}<button class="tgl" id="{pfx}-cmp-btn" '
        f'onclick="toggleCmp(\'{pfx}\',this)" '
        f'title="Comparar Vol × R$">⊞</button>\n'
        f'{ind}<div id="{pfx}-line-legend"'
    )
    c, ok = patch(f'{pfx}: insert ⊞ button', anchor, btn, c)
    if not ok: sys.exit(1)
    ok_count += 1

# ════════════════════════════════════════════════════════════════════════════
# 3. HTML — compare-wrap divs (insert after each line-wrap canvas div)
# ════════════════════════════════════════════════════════════════════════════
print('\n=== compare-wrap divs ===')

def cmp_html(pfx):
    return (
        f'\n      <div id="{pfx}-compare-wrap" class="cmp-row" style="display:none;">\n'
        f'        <div class="cmp-col">\n'
        f'          <div class="u-kpi-lbl" style="margin-bottom:4px;">\U0001f4e6 VOLUME</div>\n'
        f'          <div class="line-wrap"><canvas id="{pfx}-cmp-vol"></canvas></div>\n'
        f'          <div id="{pfx}-cmp-vol-legend" style="display:flex;gap:8px;margin-top:6px;flex-wrap:wrap;"></div>\n'
        f'        </div>\n'
        f'        <div class="cmp-col">\n'
        f'          <div class="u-kpi-lbl" style="margin-bottom:4px;">\U0001f4b0 RECEITA</div>\n'
        f'          <div class="line-wrap"><canvas id="{pfx}-cmp-rec"></canvas></div>\n'
        f'          <div id="{pfx}-cmp-rec-legend" style="display:flex;gap:8px;margin-top:6px;flex-wrap:wrap;"></div>\n'
        f'        </div>\n'
        f'      </div>'
    )

for pfx in clients:
    pattern = r'(<div class="line-wrap"><canvas id="' + re.escape(pfx) + r'-line"[^>]*></canvas></div>)'
    m = re.search(pattern, c)
    if not m:
        print(f'  MISS  {pfx}: line-wrap canvas not found')
        sys.exit(1)
    c = c[:m.end()] + cmp_html(pfx) + c[m.end():]
    print(f'  OK    {pfx}: compare-wrap inserted')
    ok_count += 1

# ════════════════════════════════════════════════════════════════════════════
# 4. JS — C2 logic block (insert before </script>)
# ════════════════════════════════════════════════════════════════════════════
print('\n=== JS C2 block ===')

JS_BLOCK = """
// ══════════════════════════════════════════════════════════
// C2 — Modo Comparativo VOL × R$ (side-by-side)
// ══════════════════════════════════════════════════════════
var _cmpActive = {};

var _cmpData = {
  sj:  { vol: function(y){ return sjGetVol(y); },
         rec: function(y){ return sjGetRec(y); } },
  sjc: { vol: function(y){ return y==='2024'?SJC_VOL_24:(y==='2025'?SJC_VOL:SJC_VOL_26); },
         rec: function(y){ return y==='2024'?SJC_REC_24:(y==='2025'?SJC_REC:SJC_REC_26); } },
  ns:  { vol: function(y){ return nsData().vol[y]; },
         rec: function(y){ return nsData().rec[y]; } },
  cl:  { vol: function(y){ return y==='2024'?CL_VOL_2024:(y==='2025'?CL_VOL_2025:CL_VOL_2026); },
         rec: function(y){ return y==='2024'?CL_REC_2024:(y==='2025'?CL_REC_2025:CL_REC_2026); } },
  pv:  { vol: function(y){ return PV_VOL[y]; },
         rec: function(y){ return PV_REC[y]; } },
  gam: { vol: function(y){ return GAM_VOL[y]; },
         rec: function(y){ return GAM_REC[y]; } },
  gch: { vol: function(y){ return GAUCHA_VOL[y]; },
         rec: function(y){ return GAUCHA_REC[y]; } },
  rio: { vol: function(y){ return y==='2024'?RIOMED_VOL_2024:(y==='2025'?RIOMED_VOL_2025:RIOMED_VOL_2026); },
         rec: function(y){ return y==='2024'?RIOMED_REC_2024:(y==='2025'?RIOMED_REC_2025:RIOMED_REC_2026); } },
};

function _cmpRender(pfx) {
  var d = _cmpData[pfx];
  if (!d) return;
  var yrs = ['2024', '2025', '2026'];
  var volDs = yrs.map(function(y){ return { label: y, data: d.vol(y) }; });
  var recDs = yrs.map(function(y){ return { label: y, data: d.rec(y) }; });
  renderLineChart(pfx + '-cmp-vol', volDs, pfx + '-cmp-vol-legend', true);
  renderLineChart(pfx + '-cmp-rec', recDs, pfx + '-cmp-rec-legend', false);
}

function toggleCmp(pfx, btn) {
  var wrap = document.getElementById(pfx + '-compare-wrap');
  if (!wrap) return;
  var active = _cmpActive[pfx];
  if (active) {
    wrap.style.display = 'none';
    btn.classList.remove('active', 'blue');
    _cmpActive[pfx] = false;
  } else {
    wrap.style.display = 'flex';
    btn.classList.add('active', 'blue');
    _cmpActive[pfx] = true;
    _cmpRender(pfx);
  }
}
"""

c, ok = patch('C2 JS block before </script>', '</script>', JS_BLOCK + '</script>', c)
if not ok: sys.exit(1)
ok_count += 1

# ── Write ─────────────────────────────────────────────────────────────────
with open(OUT, 'w', encoding='utf-8') as f:
    f.write(c)

shutil.copy2(OUT, SRC)
print(f'\n  Copied to active: {os.path.basename(SRC)}')

new_lines = len(c.splitlines())
delta = new_lines - orig_lines
print(f'\nLinhas: {orig_lines} → {new_lines} ({delta:+d})')
print(f'Patches OK: {ok_count}')
print(f'Versão: {os.path.basename(OUT)}')

# ── Quick verify ──────────────────────────────────────────────────────────
print()
checks = [
    ('CSS .cmp-row',          '.cmp-row{display:flex;gap:10px;'),
    ('CSS .cmp-col',          '.cmp-col{flex:1;min-width:0;}'),
    ('sjc ⊞ btn',            'id="sjc-cmp-btn"'),
    ('sj ⊞ btn',             'id="sj-cmp-btn"'),
    ('ns ⊞ btn',             'id="ns-cmp-btn"'),
    ('cl ⊞ btn',             'id="cl-cmp-btn"'),
    ('pv ⊞ btn',             'id="pv-cmp-btn"'),
    ('gam ⊞ btn',            'id="gam-cmp-btn"'),
    ('gch ⊞ btn',            'id="gch-cmp-btn"'),
    ('rio ⊞ btn',            'id="rio-cmp-btn"'),
    ('sjc compare-wrap',      'id="sjc-compare-wrap"'),
    ('sj compare-wrap',       'id="sj-compare-wrap"'),
    ('ns cmp-vol canvas',     'id="ns-cmp-vol"'),
    ('rio cmp-rec canvas',    'id="rio-cmp-rec"'),
    ('JS toggleCmp fn',       'function toggleCmp(pfx, btn)'),
    ('JS _cmpData',           'var _cmpData = {'),
    ('JS _cmpRender fn',      'function _cmpRender(pfx)'),
]
for label, needle in checks:
    found = needle in c
    print(f"  {'OK  ' if found else 'FAIL'}  {label}")
