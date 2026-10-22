"""
Remove o card '📊 SCJ · POSITIVAÇÃO POR CNPJ — FY25 vs FY26'
e o bloco <script> associado (dados + funções buildPositivTables/Charts).
"""
import shutil
from datetime import datetime
from pathlib import Path

BASE = Path(r"C:\Users\valqu\OneDrive\Documentos\Claude\Projects\projeto Dashboard_farma_sul\Dashboard_farma_sul")
DASH = BASE / "Dashboard_Farma_Sul_20260512_2220.html"
VER  = BASE / "versoes"
DL   = Path.home() / "Downloads"

html = DASH.read_text(encoding='utf-8')
orig_len = len(html)

# ── âncora de início e fim do bloco ──────────────────────────
START = '\n    <!-- ⑦b SCJ POSITIVAÇÃO FY25 vs FY26 -->'
END   = '\n    <!-- ⑧ ESTUDO ED NACIONAL'

if START not in html:
    print("ERRO: âncora de início não encontrada!")
    exit(1)
if END not in html:
    print("ERRO: âncora de fim não encontrada!")
    exit(1)

idx_s = html.index(START)
idx_e = html.index(END, idx_s)

# Remove o bloco e preserva o ⑧ que começa logo após
html = html[:idx_s] + '\n' + html[idx_e:]

# sanity check
if 'POSITIVAÇÃO POR CNPJ — FY25 vs FY26' in html:
    print("AVISO: texto ainda encontrado (verificar manualmente)")
else:
    print("Card e script associado removidos com sucesso")

if 'ESTUDO ED NACIONAL' in html:
    print("Bloco ESTUDO ED NACIONAL preservado OK")

ts = datetime.now().strftime('%Y%m%d_%H%M')
versao = VER / f"Dashboard_Farma_Sul_{ts}_RmPositivFY.html"
shutil.copy(DASH, versao)
print(f"Versao salva: {versao.name}")

DASH.write_text(html, encoding='utf-8')
print(f"Dashboard: {len(html):,} chars (era {orig_len:,}, removidos {orig_len-len(html):,})")

dl = DL / f"Dashboard_FarmaSul_Giovano_{ts}.html"
shutil.copy(DASH, dl)
print(f"Downloads: {dl.name}")
print("DONE.")
