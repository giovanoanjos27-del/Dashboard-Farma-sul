"""Estoque São João pelo Qlik do Portal SJ (Indicadores Estoque › Detalhes Estoque, dimensão só Produto, Baixar › Dados) → SJ_ESTOQUE / SJC_ESTOQUE.
Não mexe na cobertura de lojas (SJ_COBERTURA). estoque = soma do produto; dias = estoque ÷ (venda ref do card ÷ 30);
risco crítico < 15 d, atenção < 30 d. Nome do card casado com o produto do portal (igual ou prefixo, só se único). Preserva CRLF.
Uso: python estoque_sj_qlik.py <html> <export.xlsx>"""
import sys, json, collections, warnings
import openpyxl
warnings.filterwarnings("ignore")
H, X = sys.argv[1:3]
h = open(H, encoding="utf-8", newline="").read()
nz = lambda s: " ".join(str(s).split()).upper()
rows = list(openpyxl.load_workbook(X, read_only=True, data_only=True).worksheets[0].iter_rows(values_only=True))
ix = {c: i for i, c in enumerate(rows[0])}
T = collections.Counter()
for r in rows[1:]:
    if r[ix["Produto"]]: T[nz(r[ix["Produto"]])] += r[ix["Qtde. Estoque"]] or 0


def pega(nome):
    tag = "const " + nome + " = "; a = h.index(tag) + len(tag); o, n = json.JSONDecoder().raw_decode(h[a:]); return o, a, a + n


usados = set()
for nome in ("SJ_ESTOQUE", "SJC_ESTOQUE"):
    arr, a, b = pega(nome); n = 0; tE = 0
    for x in arr:
        s = nz(x["sku"]); c = [p for p in T if p == s] or [p for p in T if p.startswith(s) or s.startswith(p)]
        if len(c) != 1: print("   SEM PAR ÚNICO NO PORTAL (mantido):", x["sku"], x["estoque"]); tE += x["estoque"]; continue
        usados.add(c[0]); e0, d0 = x["estoque"], x["dias"]; e = int(T[c[0]]); v = x.get("venda") or 0
        d = round(e / (v / 30)) if v else (999 if e else 0)
        x.update({"estoque": e, "lojas": e, "cob": d, "dias": d,
                  "risco": "critico" if (e == 0 or (v and d < 15)) else ("atencao" if (v and d < 30) else "ok")})
        n += 1; tE += e
    ind = "\r\n" if "\r\n" in h[a:b] else "\n"
    h = h[:a] + json.dumps(arr, ensure_ascii=False, indent=2).replace("\n", ind) + h[b:]
    print(nome, n, "de", len(arr), "SKUs atualizados · estoque", tE)
fora = {p: q for p, q in T.items() if p not in usados}
print("no portal sem SKU no card:", len(fora), "produtos ·", sum(fora.values()), "un", sorted(fora.items(), key=lambda t: -t[1])[:8])
open(H, "w", encoding="utf-8", newline="").write(h); print("ok")
