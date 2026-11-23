"""Estoque DD-Gaúcha pela planilha da distribuidora 'CERAS_JOHSON_-_ESTOQUE_DD.MM.AAAA.xlsx'
(colunas: Cod Prod, Cod Fabrica, EAN, Produto, Estoque, Demanda <mês atual>, Demanda <mês passado>, Demanda <mês retrasado>).
Reconstrói GCH_ESTOQUE com os nomes da planilha: só produtos com estoque ou demanda; estoque negativo conta 0;
venda de referência = demanda do mês passado (mês fechado); dias = estoque ÷ (venda ÷ 30); crítico < 15 d, atenção < 30 d. Preserva CRLF.
Uso: python estoque_gch_planilha.py <html> <planilha.xlsx>"""
import sys, json, warnings
import openpyxl
warnings.filterwarnings("ignore")
H, X = sys.argv[1:3]
h = open(H, encoding="utf-8", newline="").read()


def marca(p):
    for k, m in (("EXPOSIS", "EXPOSIS"), ("RAID", "RAID"), ("OFF", "OFF!"), ("GLADE", "GLADE"), ("PATO", "PATO"),
                 ("LYSOFORM", "LYSOFORM"), ("MUSCULO", "MR MUSCULO")):
        if k in p.upper(): return m
    return "OUTROS"


def risco(e, v, d): return "critico" if (e == 0 or (v and d < 15)) else ("atencao" if (v and d < 30) else "ok")


ws = openpyxl.load_workbook(X, data_only=True).active
arr = []
for r in ws.iter_rows(min_row=2, values_only=True):
    if not r[0] or not r[3]: continue
    e = max(int(r[4] or 0), 0); vn, vo, vs = int(r[5] or 0), int(r[6] or 0), int(r[7] or 0)
    if not (e or vn or vo or vs): continue
    v = vo; d = round(e / (v / 30)) if v else (999 if e else 0)
    arr.append({"sku": str(r[3]).strip(), "marca": marca(str(r[3])), "ean": str(r[2]), "estoque": e, "venda": v, "venda_abr": v,
                "dem": v, "giro": v, "vendaMar": vs, "vendaAbr": vn, "vendaJun": v, "fev26": 0, "mar26": 0,
                "cob": d, "dias": d, "risco": risco(e, v, d), "lojas": e, "cdRS": 0, "cdPR": 0, "pend": 0, "lojasCount": 0, "totalLojas": 0})
arr.sort(key=lambda x: -x["estoque"])
tag = "const GCH_ESTOQUE = "; a = h.index(tag) + len(tag); old, n = json.JSONDecoder().raw_decode(h[a:]); b = a + n
ind = "\r\n" if "\r\n" in h[a:b] else "\n"
h = h[:a] + json.dumps(arr, ensure_ascii=False, indent=2).replace("\n", ind) + h[b:]
open(H, "w", encoding="utf-8", newline="").write(h)
print("GCH_ESTOQUE", len(old), "->", len(arr), "SKUs · estoque", sum(x["estoque"] for x in old), "->", sum(x["estoque"] for x in arr),
      "· venda ref (mês passado)", sum(x["venda"] for x in arr))
