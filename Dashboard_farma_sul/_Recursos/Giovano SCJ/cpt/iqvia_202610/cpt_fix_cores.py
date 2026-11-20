"""(1) Botões Grupo econômico / Bandeira / UF da distribuição dos intocáveis no mesmo estilo dos botões Todos/Em queda
(texto colorido sobre fundo claro; o branco sobre azul sumia com o tema Nielsen). (2) Fim da linha clara entre o
cabeçalho e as abas (cabeçalho com altura fracionada deixava 1 px do fundo aparecer). Uso: python cpt_fix_cores.py <base.html>"""
import sys
H = sys.argv[1]; h = open(H, encoding="utf-8", newline="").read()
a = """style="padding:4px 10px;border-radius:999px;font-size:10px;font-weight:700;cursor:pointer;border:1px solid rgba(29,111,168,0.45);'+(dim===d?'background:#1D6FA8;color:#FFFFFF;':'background:#FFFFFF;color:#1D6FA8;')+'">'"""
b = """style="border:1px solid '+(dim===d?'#1D6FA8':'rgba(148,163,184,0.45)')+';background:'+(dim===d?'#1D6FA81A':'#FFFFFF')+';color:'+(dim===d?'#1D6FA8':'#475569')+';border-radius:14px;padding:3px 11px;font-size:10px;font-weight:700;cursor:pointer;">'"""
assert h.count(a) == 1, h.count(a); h = h.replace(a, b)
css = ("<style>/* sem fresta entre cabeçalho e abas (altura fracionada do cabeçalho): faixa de 2 px da cor das abas logo abaixo */ "
       ":root:root:root:root body div.header{box-shadow:0 2px 0 0 #153B63 !important;}</style>\n")
i = h.rfind("</body>"); h = h[:i] + css + h[i:]
open(H, "w", encoding="utf-8", newline="").write(h); print("ok")
