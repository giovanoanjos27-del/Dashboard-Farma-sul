"""Ressincroniza UM cliente do ESTOQUE_DATA (card Estoque & DOH) a partir dos arrays da Gestão de Estoque; os outros ficam intactos.
Uso: python estoque_data_cliente.py <html> <cliente> <data_ref> <ARR1[,ARR2]>   ex.: DD-Riomed 17/11/2026 RIO_ESTOQUE · "São João" 17/11/2026 SJ_ESTOQUE,SJC_ESTOQUE"""
import sys, json
H, CLI, REF, ARRS = sys.argv[1:5]; h = open(H, encoding="utf-8", newline="").read()
def arr(n):
    a = h.index("const " + n + " = ") + len("const " + n + " = "); x, _ = json.JSONDecoder().raw_decode(h[a:]); return x
def st(doh, so, est):
    if est == 0 or (so and doh < 30): return "🔴 CRÍTICO"
    if so and doh <= 90: return "⚠ ATENÇÃO"
    return "✅ OK"
skus = []
for x in [y for n in ARRS.split(",") for y in arr(n)]:
    e = int(x.get("estoque") or 0); so = int(round(x.get("venda") or 0)); doh = round(e / (so / 30)) if so else (999 if e else 0)
    skus.append({"marca": x.get("marca") or "OUTROS", "sku": x["sku"], "est": e, "so": so, "doh": doh, "status": st(doh, so, e)})
skus.sort(key=lambda s: -s["est"]); et, sm = sum(s["est"] for s in skus), sum(s["so"] for s in skus)
a = h.index("ESTOQUE_DATA = ") + len("ESTOQUE_DATA = "); D, n = json.JSONDecoder().raw_decode(h[a:])
D[CLI] = {"data_ref": REF, "est_total": et, "so_mes": sm, "doh": round(et / (sm / 30)) if sm else 999,
    "critico": sum(s["status"].startswith("🔴") for s in skus), "atencao": sum(s["status"].startswith("⚠") for s in skus),
    "ok": sum(s["status"].startswith("✅") for s in skus), "skus": skus}
nl = "\r\n" if "\r\n" in h[a:a + n] else "\n"
h = h[:a] + json.dumps(D, ensure_ascii=False, indent=2).replace("\n", nl) + h[a + n:]
open(H, "w", encoding="utf-8", newline="").write(h)
r = D[CLI]; print(CLI, REF, et, "un · SO ref", sm, "· DOH", r["doh"], "· 🔴", r["critico"], "⚠", r["atencao"], "✅", r["ok"])
