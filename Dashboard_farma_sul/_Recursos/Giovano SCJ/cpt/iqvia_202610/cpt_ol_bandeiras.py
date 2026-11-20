"""CPT Clientes: bandeiras e estados dos OLs conforme lista do Giovano (20/11/2026).
OL PR/SC (só PR e SC): + LIDER FARMA, MAXIFARMA · STYLOFARMA → STYLOFARMA - GRUPO STYLO (nome IQVIA)
                       − FARMACIA SAO RAFAEL - FRANQ, FARMACIA SAO RAFAEL - LOJA PROPRIA, SESI (SC)
OL RJ (só RJ):         + MAIS BARATO, MUNDIAL · − INDEPENDENTES, REDE LUCREMAIS
OL SP (só SP):         DROGARIA TOTAL - GRUPO TOTAL → GRUPO TOTAL (nome IQVIA)
Uso: python cpt_ol_bandeiras.py <dashboard.html>"""
import sys, json
H = sys.argv[1]; h = open(H, encoding="utf-8", newline="").read()
TROCA = {"OL PR/SC": (["LIDER FARMA", "MAXIFARMA", "STYLOFARMA - GRUPO STYLO"],
                      ["FARMACIA SAO RAFAEL - FRANQ", "FARMACIA SAO RAFAEL - LOJA PROPRIA", "SESI (SC)", "STYLOFARMA"]),
         "OL RJ": (["MAIS BARATO", "MUNDIAL"], ["INDEPENDENTES", "REDE LUCREMAIS"]),
         "OL SP": (["GRUPO TOTAL"], ["DROGARIA TOTAL - GRUPO TOTAL"])}
UFS = {"OL PR/SC": ["PR", "SC"], "OL RJ": ["RJ"], "OL SP": ["SP"]}


def pega(nome):
    tag = "var " + nome + "="; a = h.index(tag) + len(tag)
    o, n = json.JSONDecoder().raw_decode(h[a:]); return o, a, a + n


def troca(nome, valor):
    global h
    _, a, b = pega(nome); h = h[:a] + json.dumps(valor, ensure_ascii=False, separators=(",", ":")) + h[b:]


K, _, _ = pega("CPT2_KEYS"); bans = {k[2] for k in K}
B, _, _ = pega("CPT2_OL_BANS"); U, _, _ = pega("CPT2_OL_UFS")
for ol, (mais, menos) in TROCA.items():
    l = B[ol]
    for x in mais:
        assert x in bans, ("bandeira não existe na base", x)
        if x not in l: l.append(x)
    for x in menos:
        assert x in l, (ol, x); l.remove(x)
    l.sort(); U[ol] = UFS[ol]; print(ol, len(l), "bandeiras ·", "/".join(UFS[ol]))
troca("CPT2_OL_BANS", B); troca("CPT2_OL_UFS", U)
open(H, "w", encoding="utf-8", newline="").write(h)
