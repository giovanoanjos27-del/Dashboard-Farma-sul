"""Estoque DD-GAM pelo portal GAM (Central Relatórios › Estoque e Vendas, soma das filiais por produto) → GAM_ESTOQUE.
Entrada TSV: produto, estoque, venda (mês), pend. estoque = soma das filiais; dias = estoque ÷ (venda ref do card ÷ 30);
SKU sem venda ref usa a venda do mês do TSV. risco crítico < 15 d, atenção < 30 d. Preserva CRLF.
Uso: python estoque_gam_portal.py <html> <tsv>"""
import sys, json, csv, difflib
H, T = sys.argv[1:3]; h = open(H, encoding="utf-8", newline="").read()
nz = lambda s: " ".join(str(s).split()).upper()
E = {nz(r["produto"]): r for r in csv.DictReader(open(T, encoding="utf-8"), delimiter="\t")}
tag = "const GAM_ESTOQUE = "; a = h.index(tag) + len(tag); arr, n = json.JSONDecoder().raw_decode(h[a:]); b = a + n
def risco(e, v, d): return "critico" if (e == 0 or (v and d < 15)) else ("atencao" if (v and d < 30) else "ok")
tot = 0; sem = []
for x in arr:
    s = nz(x["sku"]); c = [p for p in E if p == s] or difflib.get_close_matches(s, list(E), n=1, cutoff=0.8)
    if not c: sem.append(x["sku"]); continue
    r = E[c[0]]; e = int(r["estoque"]); v = x.get("venda") or 0
    d = round(e / (v / 30)) if v else (999 if e else 0)
    print(f"   {x['sku'][:44]:44s} {x['estoque']:>6} -> {e:>6} un | {x['dias']} -> {d} d")
    x.update({"estoque": e, "lojas": e, "cob": d, "dias": d, "pend": int(r["pend"]), "risco": risco(e, v, d)}); tot += e
arr.sort(key=lambda x: -x["estoque"])
ind = "\r\n" if "\r\n" in h[a:b] else "\n"
h = h[:a] + json.dumps(arr, ensure_ascii=False, indent=2).replace("\n", ind) + h[b:]
open(H, "w", encoding="utf-8", newline="").write(h)
print("GAM_ESTOQUE", len(arr), "SKUs · estoque", tot, "· sem no portal:", sem)
