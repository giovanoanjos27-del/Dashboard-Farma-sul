"""
fix_canvas_zero.py
Remove os atributos height=0 / width=0 / style inline de 0px
dos 33 canvas salvos com dimensao zero no HTML.
Causa: Chart.js salva o canvas com height:0 quando renderizado dentro de div oculta.
"""
import os, re, shutil
from datetime import datetime

BASE     = r"C:\Users\valqu\OneDrive\Documentos\Claude\Projects\projeto Dashboard_farma_sul"
HTML_DIR = os.path.join(BASE, "Dashboard_farma_sul")
SRC_HTML = os.path.join(HTML_DIR, "Dashboard_Farma_Sul_20260512_2220.html")
VER_DIR  = os.path.join(HTML_DIR, "versoes")

# Backup
ts = datetime.now().strftime("%Y%m%d_%H%M")
os.makedirs(VER_DIR, exist_ok=True)
BKP = os.path.join(VER_DIR, f"Dashboard_Farma_Sul_{ts}_PreCanvasFix.html")
shutil.copy2(SRC_HTML, BKP)
print(f"Backup: {BKP}")

with open(SRC_HTML, "r", encoding="utf-8") as f:
    content = f.read()

before = len(re.findall(r'<canvas[^>]+height:\s*0px[^>]*>', content))
print(f"Canvases com height:0px antes: {before}")

def clean_canvas_tag(m):
    tag = m.group(0)
    # Remover height="0"
    tag = re.sub(r'\s+height="0"', '', tag)
    # Remover width="0"
    tag = re.sub(r'\s+width="0"', '', tag)
    # Remover style que contem height:0px/width:0px (Chart.js style inline)
    # O estilo tem: display: block; box-sizing: border-box; height: 0px; width: 0px;
    tag = re.sub(r'\s+style="[^"]*height:\s*0px[^"]*"', '', tag)
    # Tambem remover style com width:0px (pode aparecer sozinho)
    tag = re.sub(r'\s+style="[^"]*width:\s*0px[^"]*"', '', tag)
    return tag

# Aplicar a todos os canvas tags
new_content = re.sub(r'<canvas\b[^>]*>', clean_canvas_tag, content)

after = len(re.findall(r'<canvas[^>]+height:\s*0px[^>]*>', new_content))
print(f"Canvases com height:0px depois: {after}")

# Verificar sj-line especificamente
m_sj = re.search(r'<canvas id="sj-line"[^>]*>', new_content)
if m_sj:
    print(f"\nsj-line: {m_sj.group(0)}")
m_ano = re.search(r'<canvas id="sj-ano-chart"[^>]*>', new_content)
if m_ano:
    print(f"sj-ano-chart: {m_ano.group(0)}")

changed = before - after
print(f"\nCanvases corrigidos: {changed}")

# Gravar
with open(SRC_HTML, "w", encoding="utf-8") as f:
    f.write(new_content)

# Versao final
ts2 = datetime.now().strftime("%Y%m%d_%H%M")
VER = os.path.join(VER_DIR, f"Dashboard_Farma_Sul_{ts2}_CanvasFix.html")
shutil.copy2(SRC_HTML, VER)
print(f"Versao: {VER}")
