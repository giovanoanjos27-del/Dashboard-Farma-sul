"""Estoque Nissei pelo portal PIN (Dashboard › Sell-out, tabela de produtos: estoque loja + estoque CD) → NS_ESTOQUE_HB (André) e NS_ESTOQUE_ED (Edmar).
Entrada TSV: produto, estoque. Casa pelo nome (espaços normalizados). dias = estoque ÷ (venda ref do card ÷ 30);
risco crítico se zerado ou < 15 d, atenção < 30 d. SKU do card ausente no portal fica como está. Povidine nunca entra. Preserva CRLF.
Uso: python estoque_nissei_pin.py <html> <tsv>"""
import sys, json, csv
H, T = sys.argv[1:3]; h = open(H, encoding="utf-8", newline="").read()
nz = lambda s: " ".join(str(s).split()).upper()
E = {nz(r["produto"]): int(r["estoque"]) for r in csv.DictReader(open(T, encoding="utf-8"), delimiter="\t")}
def risco(e, v, d): return "critico" if (e == 0 or (v and d < 15)) else ("atencao" if (v and d < 30) else "ok")
for n in ("NS_ESTOQUE_HB", "NS_ESTOQUE_ED"):
    tag = "const " + n + " = "; a = h.index(tag) + len(tag); arr, k = json.JSONDecoder().raw_decode(h[a:]); b = a + k
    tot = 0; sem = []
    for x in arr:
        if "POVID" in nz(x["sku"]): continue
        s = nz(x["sku"])
        if s not in E: sem.append(x["sku"]); tot += x["estoque"]; continue
        e = E[s]; v = x.get("venda") or 0; d = round(e / (v / 30)) if v else (999 if e else 0)
        print(f"   {x['sku'][:50]:50s} {x['estoque']:>6} -> {e:>6} | {x.get('dias')} -> {d} d")
        x.update({"estoque": e, "lojas": e, "cob": d, "dias": d, "risco": risco(e, v, d)}); tot += e
    arr.sort(key=lambda x: -x["estoque"])
    ind = "\r\n" if "\r\n" in h[a:b] else "\n"
    h = h[:a] + json.dumps(arr, ensure_ascii=False, indent=2).replace("\n", ind) + h[b:]
    print(n, len(arr), "SKUs · estoque", tot, "· sem no portal (mantidos):", sem)
open(H, "w", encoding="utf-8", newline="").write(h)
