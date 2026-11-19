"""Estoque DD-Riomed pelo e-mail diário 'RIOMED || ESTOQUE E DEMANDA - SC JOHNSON' (Target Sistemas) → RIO_ESTOQUE.
Entrada TSV: ean, produto, estoque, custo, nov (venda atual), out (mês passado), set (mês retrasado).
Reconstrói a lista: venda ref = Set/26 (mesma referência do card), dias = estoque ÷ (venda ÷ 30); fevereiro/março antigos saem.
Uso: python estoque_riomed_email.py <html> <tsv>"""
import sys, json, csv
H, T = sys.argv[1:3]; h = open(H, encoding="utf-8", newline="").read()
def marca(p):
    for k, m in (("EXPOSIS", "EXPOSIS"), ("RAID", "RAID"), ("OFF", "OFF!"), ("GLADE", "GLADE"), ("PATO", "PATO"), ("LYSOFORM", "LYSOFORM")):
        if k in p: return m
    return "OUTROS"
def risco(e, v, d): return "critico" if (e == 0 or (v and d < 15)) else ("atencao" if (v and d < 30) else "ok")
arr = []
for r in csv.DictReader(open(T, encoding="utf-8"), delimiter="\t"):
    e, v, vo, vn = int(r["estoque"]), int(r["set"]), int(r["out"]), int(r["nov"])
    d = round(e / (v / 30)) if v else (999 if e else 0)
    arr.append({"sku": r["produto"], "marca": marca(r["produto"]), "ean": r["ean"], "estoque": e, "venda": v, "venda_abr": v, "dem": v, "giro": v,
                "vendaSet": v, "vendaOut": vo, "vendaNov": vn, "vendaMar": vo, "vendaAbr": vn,   # vendaMar/vendaAbr = nomes que renderRIOEstoqueBarras lê (mês passado / mês atual)
                "cob": d, "dias": d, "risco": risco(e, v, d), "lojas": e,
                "cdRS": 0, "cdPR": 0, "pend": 0, "lojasCount": 0, "totalLojas": 0})
arr.sort(key=lambda x: -x["estoque"])
tag = "const RIO_ESTOQUE = "; a = h.index(tag) + len(tag); old, n = json.JSONDecoder().raw_decode(h[a:]); b = a + n
ind = "\r\n" if "\r\n" in h[a:b] else "\n"
h = h[:a] + json.dumps(arr, ensure_ascii=False, indent=2).replace("\n", ind) + h[b:]
open(H, "w", encoding="utf-8", newline="").write(h)
print("RIO_ESTOQUE", len(old), "->", len(arr), "SKUs · estoque", sum(x["estoque"] for x in old), "->", sum(x["estoque"] for x in arr))
