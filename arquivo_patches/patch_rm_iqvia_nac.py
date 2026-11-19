"""
Remove o card ESTUDO ED NACIONAL / COMPOSIÇÃO DO UNIVERSE NACIONAL
- bloco HTML (card + script associado)
- função JS renderIqviaNacional() + _iqviaNacCharts
- chamada renderIqviaNacional() no initCobertura
"""
import shutil
from datetime import datetime
from pathlib import Path

BASE = Path(r"C:\Users\valqu\OneDrive\Documentos\Claude\Projects\projeto Dashboard_farma_sul\Dashboard_farma_sul")
DASH = BASE / "Dashboard_Farma_Sul_20260512_2220.html"
VER  = BASE / "versoes"
DL   = Path.home() / "Downloads"

html = DASH.read_text(encoding='utf-8')
orig = len(html)
removed = []

# ── 1. HTML: card ⑧ até o próximo card ② ────────────────────
S1 = '\n    <!-- ⑨ ESTUDO ED NACIONAL — UNIVERSE IQVIA \xd7 SCJ BRASIL -->'
E1 = '\n    <!-- ② TOP CIDADES NÃO POSITIVADOS FY25 -->'
if S1 in html and E1 in html:
    i, j = html.index(S1), html.index(E1, html.index(S1))
    html = html[:i] + '\n' + html[j:]
    removed.append("Card HTML (ESTUDO ED NACIONAL)")
else:
    print("AVISO: card HTML nao encontrado — tentando fallback ASCII")
    S1b = '<!-- ⑨ ESTUDO ED NACIONAL'
    E1b = '<!-- ② TOP CIDADES'
    if S1b in html and E1b in html:
        i = html.rindex('\n', 0, html.index(S1b))
        j = html.index(E1b, i)
        html = html[:i] + '\n    ' + html[j:]
        removed.append("Card HTML (ESTUDO ED NACIONAL) via fallback")

# ── 2. JS: var _iqviaNacCharts + function renderIqviaNacional ─
S2 = '\nvar _iqviaNacCharts = {};'
E2 = '\nfunction renderConsCrossover(){'
if S2 in html and E2 in html:
    i, j = html.index(S2), html.index(E2, html.index(S2))
    html = html[:i] + html[j:]
    removed.append("JS renderIqviaNacional() + _iqviaNacCharts")
else:
    print("AVISO: JS renderIqviaNacional nao encontrado")

# ── 3. Chamada renderIqviaNacional() no initCobertura ─────────
OLD_CALL = '    renderIqviaNacional();\n  }, 80);\n}'
NEW_CALL = '  }, 80);\n}'
if OLD_CALL in html:
    html = html.replace(OLD_CALL, NEW_CALL, 1)
    removed.append("Chamada renderIqviaNacional() em initCobertura")
else:
    # fallback sem indentacao
    OLD2 = 'renderIqviaNacional();\n'
    if OLD2 in html:
        html = html.replace(OLD2, '', 1)
        removed.append("Chamada renderIqviaNacional() (fallback)")
    else:
        print("AVISO: chamada renderIqviaNacional nao encontrada")

# ── Relatorio ─────────────────────────────────────────────────
for r in removed:
    print("OK:", r)

if 'COMPOSICAO DO UNIVERSE NACIONAL' not in html.replace('Ç','C').replace('Ã','A'):
    print("Verificacao: card nao encontrado no HTML (OK)")

# ── Salvar ────────────────────────────────────────────────────
ts = datetime.now().strftime('%Y%m%d_%H%M')
versao = VER / f"Dashboard_Farma_Sul_{ts}_RmIqviaNac.html"
shutil.copy(DASH, versao)
print(f"Versao: {versao.name}")

DASH.write_text(html, encoding='utf-8')
print(f"Dashboard: {len(html):,} chars (removidos {orig-len(html):,})")

dl = DL / f"Dashboard_FarmaSul_Giovano_{ts}.html"
shutil.copy(DASH, dl)
print(f"Downloads: {dl.name}")
print("DONE.")
