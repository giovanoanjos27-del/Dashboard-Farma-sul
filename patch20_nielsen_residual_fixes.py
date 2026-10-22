"""
PATCH 20 - Nielsen Tema Claro: fixes residuais
Corrige os problemas que os patches 19/19b/19c nao capturaram:
1. renderAvgPriceChart: GC 'rgba(255,255,255,0.09)' -> azul
2. renderMSOArea: GC branco + tooltip CO escuro -> tema claro
3. setShrBrand: botoes inativos com fundo escuro via JS -> tema claro
4. EXPOSIS button HTML: color:#ffffff -> #1d4ed8 (visivel no fundo claro)
5. ShrTrend diagnostico: borda/bg ambar -> azul
6. CSS: capturar bg RGB normalizado pelo browser (rgb(31,41,55) = #1f2937)
"""
import datetime, re

SRC = r'Dashboard_farma_sul\Dashboard_Farma_Sul_20260512_2220.html'
html = open(SRC, encoding='utf-8').read()
original_len = len(html)
patches = 0

def replace_in_fn(h, fn_name, old, new, count=1):
    start = h.find('function ' + fn_name + '(')
    if start == -1: return h, False
    end = h.find('\nfunction ', start + 10)
    if end == -1: end = start + 200000
    chunk = h[start:end]
    if old not in chunk: return h, False
    new_chunk = chunk.replace(old, new, count)
    return h[:start] + new_chunk + h[end:], True

# ------------------------------------------------------------------------------------
# 1. renderAvgPriceChart — GC branco → azul
# ------------------------------------------------------------------------------------
html, ok = replace_in_fn(html, 'renderAvgPriceChart',
    "var GC = 'rgba(255,255,255,0.09)', TC = '#4a6b65'",
    "var GC = 'rgba(59,130,246,0.10)', TC = '#64748b'")
if ok: patches += 1; print('[OK] renderAvgPriceChart: GC white -> blue, TC dark')
else:
    # Tentar variante sem espaços
    html, ok = replace_in_fn(html, 'renderAvgPriceChart',
        "var GC='rgba(255,255,255,0.09)',TC='#4a6b65'",
        "var GC='rgba(59,130,246,0.10)',TC='#64748b'")
    if ok: patches += 1; print('[OK] renderAvgPriceChart: GC white -> blue (v2)')
    else: print('[MISS] renderAvgPriceChart: GC anchor nao encontrado')

# ------------------------------------------------------------------------------------
# 2. renderMSOArea — GC branco + tooltip CO escuro → tema claro
# ------------------------------------------------------------------------------------
html, ok = replace_in_fn(html, 'renderMSOArea',
    "var GC='rgba(255,255,255,0.09)', TC='#4a6b65';",
    "var GC='rgba(59,130,246,0.10)', TC='#64748b';")
if ok: patches += 1; print('[OK] renderMSOArea: GC -> blue, TC -> #64748b')
else: print('[MISS] renderMSOArea: GC anchor nao encontrado')

html, ok = replace_in_fn(html, 'renderMSOArea',
    "var CO={backgroundColor:'#0a1a18',titleColor:'#e2e8f0',bodyColor:'#D1D5DB',borderColor:'rgba(255,255,255,0.13)',borderWidth:1,padding:10};",
    "var CO={backgroundColor:'#F0F4FA',titleColor:'#1e293b',bodyColor:'#475569',borderColor:'rgba(59,130,246,0.2)',borderWidth:1,padding:10};")
if ok: patches += 1; print('[OK] renderMSOArea: tooltip CO -> tema claro')
else: print('[MISS] renderMSOArea: tooltip CO anchor nao encontrado')

# ------------------------------------------------------------------------------------
# 3. setShrBrand — botões inativos no tema claro usam fundo claro
# ------------------------------------------------------------------------------------
OLD_SET_SHR = """function setShrBrand(brand, btn){
  _shrActiveBrand = brand;
  // Reset all buttons
  var _shrBtnOrigColors = {'shr-btn-all':'#fbbf24','OFF!':'#fbbf24','EXPOSIS':'#ffffff','XO INSETO':'#ef4444','SUPER REPELEX':'#f97316','SBP':'#06b6d4'};
  var allBtns = document.querySelectorAll('#shr-brand-filters button');
  allBtns.forEach(function(b){
    b.style.background = '#1f2937';
    if(b.id === 'shr-btn-all'){
      b.style.color = '#fbbf24';
      b.style.border = '1px solid #fbbf24';
    } else {
      var bText = b.textContent.trim();
      b.style.color = _shrBtnOrigColors[bText] || b.style.color;
    }
  });"""

NEW_SET_SHR = """function setShrBrand(brand, btn){
  _shrActiveBrand = brand;
  // Reset all buttons — aware of light theme
  var _isLight = document.body.classList.contains('nielsen-theme');
  var _shrBtnOrigColors = {'shr-btn-all':'#fbbf24','OFF!':'#fbbf24','EXPOSIS':'#1d4ed8','XO INSETO':'#b91c1c','SUPER REPELEX':'#7c3aed','SBP':'#0891b2'};
  var allBtns = document.querySelectorAll('#shr-brand-filters button');
  allBtns.forEach(function(b){
    if(_isLight){
      b.style.background = '#EDF2F9';
      b.style.border = '1px solid rgba(59,130,246,0.25)';
      if(b.id === 'shr-btn-all'){
        b.style.color = '#1e293b';
      } else {
        var bText = b.textContent.trim();
        b.style.color = _shrBtnOrigColors[bText] || '#475569';
      }
    } else {
      b.style.background = '#1f2937';
      if(b.id === 'shr-btn-all'){
        b.style.color = '#fbbf24';
        b.style.border = '1px solid #fbbf24';
      } else {
        var bText = b.textContent.trim();
        var _origDark = {'OFF!':'#fbbf24','EXPOSIS':'#ffffff','XO INSETO':'#ef4444','SUPER REPELEX':'#f97316','SBP':'#06b6d4'};
        b.style.color = _origDark[bText] || b.style.color;
      }
    }
  });"""

if OLD_SET_SHR in html:
    html = html.replace(OLD_SET_SHR, NEW_SET_SHR, 1)
    patches += 1
    print('[OK] setShrBrand: botoes inativos -> tema claro ou escuro')
else:
    print('[MISS] setShrBrand: bloco de reset nao encontrado')

# ------------------------------------------------------------------------------------
# 4. EXPOSIS button HTML — color:#ffffff → #1d4ed8
# ------------------------------------------------------------------------------------
OLD_EXPOSIS_BTN = 'style="background:#161B22;color:#ffffff;border:1px solid #3b82f6;border-radius:6px;padding:5px 12px;font-size:11px;font-weight:700;cursor:pointer;">EXPOSIS</button>'
NEW_EXPOSIS_BTN = 'style="background:#161B22;color:#1d4ed8;border:1px solid #3b82f6;border-radius:6px;padding:5px 12px;font-size:11px;font-weight:700;cursor:pointer;">EXPOSIS</button>'

if OLD_EXPOSIS_BTN in html:
    html = html.replace(OLD_EXPOSIS_BTN, NEW_EXPOSIS_BTN, 1)
    patches += 1
    print('[OK] EXPOSIS button: color:#ffffff -> #1d4ed8')
else:
    print('[MISS] EXPOSIS button: anchor nao encontrado')

# ------------------------------------------------------------------------------------
# 5. ShrTrend diagnostico — borda/bg âmbar → azul
# ------------------------------------------------------------------------------------
OLD_DIAG = 'id="shr-diagnostico" style="margin-top:14px;background:rgba(251,191,36,0.04);border:1px solid rgba(251,191,36,0.15);border-radius:10px;padding:14px 16px;"'
NEW_DIAG = 'id="shr-diagnostico" style="margin-top:14px;background:rgba(59,130,246,0.04);border:1px solid rgba(59,130,246,0.15);border-radius:10px;padding:14px 16px;"'

if OLD_DIAG in html:
    html = html.replace(OLD_DIAG, NEW_DIAG, 1)
    patches += 1
    print('[OK] ShrTrend diagnostico: ambar -> azul')
else:
    print('[MISS] ShrTrend diagnostico: anchor nao encontrado')

# ------------------------------------------------------------------------------------
# 6. CSS: capturar bg RGB normalizado pelo browser + reforço para botões
# ------------------------------------------------------------------------------------
OLD_CSS_ANCHOR = '.u-badge-cyan{font-size:9px;font-weight:700;background:#06b6d422;color:#06b6d4;border-radius:3px;padding:1px 5px;}'

NEW_CSS_EXTRA = '''
/* ================================================================
   PATCH 20 — Fixes residuais tema claro Nielsen
   ================================================================ */

/* Browser normaliza #1f2937 para rgb(31,41,55) ao setar via JS style.background */
#panel-nielsen [style*="background: rgb(31, 41, 55)"],
#panel-nielsen [style*="background:rgb(31, 41, 55)"],
#panel-nielsen [style*="background: rgb(22, 27, 34)"],
#panel-nielsen [style*="background:rgb(22, 27, 34)"],
#panel-nielsen [style*="background: rgb(10, 26, 24)"],
#panel-nielsen [style*="background:rgb(10, 26, 24)"] { background: #EDF2F9 !important; }

/* ShrTrend brand filter buttons - forcar fundo claro no tema nielsen */
body.nielsen-theme #shr-brand-filters button {
  background: #EDF2F9 !important;
  border: 1px solid rgba(59,130,246,0.25) !important;
  color: #475569 !important;
  transition: all 0.15s !important;
}
/* Botao ativo com cor de marca - preservar cor original */
body.nielsen-theme #shr-brand-filters button[style*="background:#fbbf24"],
body.nielsen-theme #shr-brand-filters button[style*="background: rgb(251, 191, 36)"] {
  background: #fbbf24 !important; color: #000 !important; border-color: #fbbf24 !important;
}
body.nielsen-theme #shr-brand-filters button[style*="background:#3b82f6"],
body.nielsen-theme #shr-brand-filters button[style*="background: rgb(59, 130, 246)"] {
  background: #3b82f6 !important; color: #fff !important; border-color: #3b82f6 !important;
}
body.nielsen-theme #shr-brand-filters button[style*="background:#ef4444"],
body.nielsen-theme #shr-brand-filters button[style*="background: rgb(239, 68, 68)"] {
  background: #ef4444 !important; color: #fff !important; border-color: #ef4444 !important;
}
body.nielsen-theme #shr-brand-filters button[style*="background:#f97316"],
body.nielsen-theme #shr-brand-filters button[style*="background: rgb(249, 115, 22)"] {
  background: #f97316 !important; color: #fff !important; border-color: #f97316 !important;
}
body.nielsen-theme #shr-brand-filters button[style*="background:#06b6d4"],
body.nielsen-theme #shr-brand-filters button[style*="background: rgb(6, 182, 212)"] {
  background: #06b6d4 !important; color: #000 !important; border-color: #06b6d4 !important;
}

/* ShrTrend legenda texto e linha separadora */
body.nielsen-theme #shr-trend > div[style*="margin-top:10px"] { color: #64748b !important; }
body.nielsen-theme #panel-nielsen > div[style*="border-top"] { border-top-color: rgba(59,130,246,0.15) !important; }

/* MSO Area KPI chips — forçar fundo claro */
#panel-nielsen #mso-area-kpis > div {
  background: #EDF2F9 !important;
  border-top-width: 2px !important;
}
#panel-nielsen #mso-area-kpis [style*="color:#3d6b63"] { color: #64748b !important; }
#panel-nielsen #mso-area-kpis [style*="color:#94A3B8"],
#panel-nielsen #mso-area-kpis [style*="color:#94a3b8"] { color: #64748b !important; }
'''

if OLD_CSS_ANCHOR in html:
    html = html.replace(OLD_CSS_ANCHOR, OLD_CSS_ANCHOR + NEW_CSS_EXTRA, 1)
    patches += 1
    print('[OK] CSS: RGB bg catch + button light theme + MSO Area KPI reforço')
else:
    print('[MISS] CSS: anchor u-badge-cyan nao encontrado')

# ------------------------------------------------------------------------------------
# 7. Salvar
# ------------------------------------------------------------------------------------
print(f'\nPatches: {patches}')
print(f'Diff   : {len(html) - original_len:+,} bytes')

ts = datetime.datetime.now().strftime('%Y%m%d_%H%M')
ver = f'Dashboard_farma_sul/versoes/Dashboard_Farma_Sul_{ts}_NielsenResidualFixes.html'
open(SRC, 'w', encoding='utf-8').write(html)
open(ver, 'w', encoding='utf-8').write(html)
print(f'\nSalvo : {SRC}')
print(f'Versao: {ver}')
