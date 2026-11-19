"""Estoque Panvel pelo portal Dimed › Relatório de Estoque CD e Loja (todos os fornecedores, D-2) → PV_ESTOQUE.
Por item: estoque = soma das lojas + CD EDS + CD PRN (o CD se repete em cada linha de filial: conta uma vez, máximo).
dias = estoque ÷ (venda ref do card ÷ 30); risco crítico < 15 d, atenção < 30 d. Não mexe em PV_COBERTURA. Preserva CRLF.
Uso: python estoque_pv_portal.py <html> <RelatorioEstoqueCDLoja.xlsx>"""
import sys, json, warnings
import openpyxl
warnings.filterwarnings("ignore")
H, X = sys.argv[1:3]
h = open(H, encoding="utf-8", newline="").read()
nz = lambda s: " ".join(str(s).split()).upper()
ALIAS = {"OFF KIDS LOCAO LV 200ML PG 117ML": "OFF KIDS LOCAO 200ML", "KIT REP EXPOSIS 100ML+ BEBE 117G": "KIT REP EXPOSIS 100ML+ REP BEBE 117G"}
rows = list(openpyxl.load_workbook(X, read_only=True, data_only=True).worksheets[0].iter_rows(values_only=True))
ix = {c: i for i, c in enumerate(rows[0])}
n = lambda v: int(float(v or 0))
I = {}
for r in rows[1:]:
    k = nz(r[ix["Item - Nomenclatura Varejo"]]); o = I.setdefault(k, {"loja": 0, "eds": 0, "prn": 0})
    o["loja"] += n(r[ix["Qtd Est Loja"]]); o["eds"] = max(o["eds"], n(r[ix["Qtd Est Cd EDS"]])); o["prn"] = max(o["prn"], n(r[ix["Qtd Est Cd PRN"]]))
print("posição", rows[1][ix["Periodo"]][:10], "·", len(I), "itens · total", sum(o["loja"] + o["eds"] + o["prn"] for o in I.values()))
tag = "const PV_ESTOQUE = "; a = h.index(tag) + len(tag); arr, m = json.JSONDecoder().raw_decode(h[a:]); b = a + m
usados = set(); tE = 0; k = 0
for x in arr:
    s = nz(ALIAS.get(x["sku"], x["sku"])); c = [p for p in I if p == s] or [p for p in I if p.startswith(s) or s.startswith(p)]
    if len(c) != 1: print("   SEM PAR ÚNICO (mantido):", x["sku"], x["estoque"], c[:3]); tE += x["estoque"]; continue
    usados.add(c[0]); o = I[c[0]]; e0, d0 = x["estoque"], x["dias"]; e = o["loja"] + o["eds"] + o["prn"]; v = x.get("venda") or 0
    d = round(e / (v / 30)) if v else (999 if e else 0)
    x.update({"estoque": e, "lojas": e, "cob": d, "dias": d, "risco": "critico" if (e == 0 or (v and d < 15)) else ("atencao" if (v and d < 30) else "ok")})
    print("   ", x["sku"][:42].ljust(42), e0, "->", e, "un |", d0, "->", d, "d"); tE += e; k += 1
fora = {p: I[p]["loja"] + I[p]["eds"] + I[p]["prn"] for p in I if p not in usados}
print("PV_ESTOQUE", k, "de", len(arr), "SKUs · estoque", tE, "· no portal sem SKU no card:", sorted(fora.items(), key=lambda t: -t[1])[:10])
ind = "\r\n" if "\r\n" in h[a:b] else "\n"
h = h[:a] + json.dumps(arr, ensure_ascii=False, indent=2).replace("\n", ind) + h[b:]
open(H, "w", encoding="utf-8", newline="").write(h); print("ok")
