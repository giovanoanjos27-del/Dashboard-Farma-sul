"""
Aplica correções ao HTML:
1. Substitui DN_INTOC_GRUPOS com dados corrigidos (30 grupos)
2. Adiciona _DISTRIBUIDORES array e atualiza _populateGrupo
"""
import re, shutil
from datetime import datetime

HTML_FILE = 'Dashboard_Farma_Sul_20260512_2220.html'
JS_FILE   = '_temp_intoc_grupos.js'

with open(HTML_FILE, encoding='utf-8') as f:
    html = f.read()

with open(JS_FILE, encoding='utf-8') as f:
    new_block = f.read().strip()

# ---- 1. Replace DN_INTOC_GRUPOS block ----
m = re.search(r'const DN_INTOC_GRUPOS = \{.*?\n\};', html, re.DOTALL)
if not m:
    print("ERROR: DN_INTOC_GRUPOS block not found!")
    exit(1)

old_block = m.group(0)
print(f"Old block: {len(old_block):,} chars")
print(f"New block: {len(new_block):,} chars")
html = html[:m.start()] + new_block + html[m.end():]
print("DN_INTOC_GRUPOS replaced OK")

# ---- 2. Add _DISTRIBUIDORES array after _OL ----
old_ol_arr = "var _OL = ['OL MG','OL NE','OL PR/SC','OL RJ','OL RS','OL SPC','OL SPI'];"
new_ol_arr = (
    "var _OL = ['OL MG','OL NE','OL PR/SC','OL RJ','OL RS','OL SPC','OL SPI'];\n"
    "  var _DISTRIBUIDORES = ['GAM','GAUCHA FARMA'];"
)
if old_ol_arr in html:
    html = html.replace(old_ol_arr, new_ol_arr, 1)
    print("_DISTRIBUIDORES array added OK")
else:
    print("WARNING: _OL array not found for replacement")

# ---- 3. Update _populateGrupo to include DISTRIBUIDORES ----
old_pop = """function _populateGrupo(){
    var sel = document.getElementById('intoc-g-grupo-sel');
    if(!sel || sel.options.length>0) return;
    var g1 = document.createElement('optgroup');
    g1.label = '🏪 DIRETO';
    _DIRETO.forEach(function(g){
      var o = document.createElement('option');
      o.value=g; o.textContent=g;
      if(g==='SAO JOAO FARMACIAS') o.selected=true;
      g1.appendChild(o);
    });
    sel.appendChild(g1);
    var g2 = document.createElement('optgroup');
    g2.label = '📦 OL (Operadores Logísticos)';
    _OL.forEach(function(g){
      var o = document.createElement('option');
      o.value=g; o.textContent=g;
      g2.appendChild(o);
    });
    sel.appendChild(g2);
  }"""

new_pop = """function _populateGrupo(){
    var sel = document.getElementById('intoc-g-grupo-sel');
    if(!sel || sel.options.length>0) return;
    var g1 = document.createElement('optgroup');
    g1.label = '🏪 DIRETO';
    _DIRETO.forEach(function(g){
      var o = document.createElement('option');
      o.value=g; o.textContent=g;
      if(g==='SAO JOAO FARMACIAS') o.selected=true;
      g1.appendChild(o);
    });
    sel.appendChild(g1);
    var g2 = document.createElement('optgroup');
    g2.label = '📦 OL (Operadores Logísticos)';
    _OL.forEach(function(g){
      var o = document.createElement('option');
      o.value=g; o.textContent=g;
      g2.appendChild(o);
    });
    sel.appendChild(g2);
    var g3 = document.createElement('optgroup');
    g3.label = '🚚 DISTRIBUIDORES';
    _DISTRIBUIDORES.forEach(function(g){
      var o = document.createElement('option');
      o.value=g; o.textContent=g;
      g3.appendChild(o);
    });
    sel.appendChild(g3);
  }"""

if old_pop in html:
    html = html.replace(old_pop, new_pop, 1)
    print("_populateGrupo updated OK")
else:
    print("WARNING: _populateGrupo old text not found — trying partial match")
    # Try to find and print the actual function
    idx = html.find('function _populateGrupo')
    print("Found at:", idx)
    print(repr(html[idx:idx+800]))

# ---- 4. Create backup and save ----
ts = datetime.now().strftime('%Y%m%d_%H%M')
backup = f'versoes/Dashboard_Farma_Sul_{ts}.html'
shutil.copy(HTML_FILE, backup)
print(f"Backup: {backup}")

with open(HTML_FILE, 'w', encoding='utf-8') as f:
    f.write(html)
print(f"Saved {HTML_FILE} ({len(html):,} chars)")

# ---- 5. Also copy to Downloads ----
import os
downloads = os.path.expanduser(r'~\Downloads')
dl_file = os.path.join(downloads, f'Dashboard_FarmaSul_Giovano_{ts}.html')
shutil.copy(HTML_FILE, dl_file)
print(f"Downloads copy: {dl_file}")
