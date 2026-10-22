"""
PATCH 27 — Fix filtro select + OB section header text
1. .fsel background-repeat:no-repeat !important (seta repetindo)
2. OB / section headers com cor clara (#34d399, #2dd4bf, #06b6d4, #f1f5f9) -> escuro
"""
import datetime

SRC = r'Dashboard_farma_sul\Dashboard_Farma_Sul_20260512_2220.html'
html = open(SRC, encoding='utf-8').read()
original_len = len(html)

ANCHOR = '* { text-shadow:none !important; }\n\n/* ═══ END UTILITY ═══ */'

EXTRA_CSS = '''* { text-shadow:none !important; }

/* ── PATCH 27 — fsel background-repeat fix ──────────────────── */
.fsel {
  background-repeat: no-repeat !important;
  background-position: right 8px center !important;
  background-size: 10px auto !important;
}
#sellout-client-selector {
  background-repeat: no-repeat !important;
  background-position: right 10px center !important;
  background-size: 10px auto !important;
}
select[class] {
  background-repeat: no-repeat !important;
}

/* ── PATCH 27 — OB section headers: cor clara -> escuro ──────── */
/* Cabeçalhos de seção com letter-spacing (labels de cards/paineis) */
[style*="letter-spacing"][style*="color:#34d399"] { color:#1E293B !important; }
[style*="letter-spacing"][style*="color:#2dd4bf"] { color:#1E293B !important; }
[style*="letter-spacing"][style*="color:#06b6d4"] { color:#1E293B !important; }
[style*="letter-spacing"][style*="color:#fbbf24"] { color:#1E293B !important; }
[style*="letter-spacing"][style*="color:#a3e635"] { color:#1E293B !important; }
/* Subtítulos quase brancos */
[style*="color:#f1f5f9"] { color:#1E293B !important; }
[style*="color:#f8fafc"] { color:#334155 !important; }

/* ═══ END UTILITY ═══ */'''

if ANCHOR in html:
    html = html.replace(ANCHOR, EXTRA_CSS)
    print('[OK] CSS patch27 injetado (fsel + OB headers)')
else:
    print('[MISS] ancora nao encontrada — verificar')

print('Diff: {:+,} bytes'.format(len(html) - original_len))

ts = datetime.datetime.now().strftime('%Y%m%d_%H%M')
ver = 'Dashboard_farma_sul/versoes/Dashboard_Farma_Sul_{}_FilterObFix.html'.format(ts)
open(SRC, 'w', encoding='utf-8').write(html)
open(ver, 'w', encoding='utf-8').write(html)
print('Salvo: ' + SRC)
print('Versao: ' + ver)
