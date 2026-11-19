"""Sell Out mensal por marca × cliente, Jan–Nov de 2026 e de 2025, para a aba 3D (filtro de marca com meses acumuláveis).
Jan–Set:
  - real (planilha de sell out por SKU, mesma leitura do gerar_so_onepage.py) quando o Jan–Set da planilha bate com o card
    Sell-out por Marca (SO_OP) do cliente, com diferença menor que 3% (hoje: São João, Panvel e Clamed);
  - senão (Nissei, GAM, Gaúcha e Riomed não estão completos na cópia local da planilha), estimado: acumulado Jan–Set da marca
    no SO_OP distribuído pelos meses na proporção da venda mensal total do cliente no dashboard. O acumulado fica igual ao do card.
Out–Nov: marca_outnov_<data>.json (total do cliente no dashboard quebrado por marca; ver marca_outnov.py).
Saída JSON {meses, B:{marca:{cliente:{r26:[11], r25:[11]}}}, fonte:{cliente:'real'|'estimado'}} em R$ (Clamed em unidades).
null = mês sem dado (ex.: Clamed Nov/26).
Uso: python marca_mensal.py <dashboard.html> <marca_outnov.json> <saida.json>"""
import sys, os, json, re
H, J, OUT = sys.argv[1:4]
h = open(H, encoding="utf-8").read()
B = os.path.dirname(os.path.abspath(__file__)); OP = os.path.join(B, "..", "..", "OnePage")
src = open(os.path.join(OP, "gerar_so_onepage.py"), encoding="utf-8").read().split("# mês de referência")[0]
sys.argv = ["x", os.path.join(OP, "Panvel", "dados", "PLANILHA DE SELL OUT CLIENTES FARMA.xlsx"), os.devnull]
g = {}; exec(src, g); RAW = g["raw"]
MAP = {"saojoao": "SJ", "nissei": "NS", "clamed": "CL", "panvel": "PV", "ddgam": "GAM", "ddgaucha": "GA", "ddriomed": "RM"}
ON = json.load(open(J, encoding="utf-8"))["B"]
a = h.index("var SO_OP = ") + 12; SO_OP, _ = json.JSONDecoder().raw_decode(h[a:])


def arr(anchor, ano=None, de=0):
    i = h.index(anchor, de); m = (re.compile(r"'%s'\s*:\s*(\[[^\[\]]*\])" % ano) if ano else re.compile(r"(\[[^\[\]]*\])")).search(h, i)
    return [0.0 if x.strip() in ("null", "") else float(x) for x in m.group(1)[1:-1].split(",")]


t = h.index("total:", h.index("const NS ="))
TOT = {"NS": (arr("rec:", "2026", t), arr("rec:", "2025", t)), "GAM": (arr("const GAM_REC", "2026"), arr("const GAM_REC", "2025")),
       "GA": (arr("const GAUCHA_REC", "2026"), arr("const GAUCHA_REC", "2025")), "RM": (arr("const RIOMED_REC_2026 ="), arr("const RIOMED_REC_2025 =")),
       "PV": (arr("const PV_REC", "2026"), arr("const PV_REC", "2025")), "CL": (arr("const CL_VOL_2026 ="), arr("const CL_VOL_2025 ="))}
sj26, sj25 = arr("const SJ_REC", "2026"), arr("const SJ_REC", "2025")
TOT["SJ"] = (sj26, sj25)


def norm(m, sku):
    return "PATO BLOCK" if ("BLOCK" in sku.upper() and "PATO" in sku.upper()) else m


# acumulado Jan–Set por marca no SO_OP (R$; Clamed un)
acum = {}
for key, c in SO_OP["clientes"].items():
    cli = MAP.get(key) or ("SJ" if key == "caroline" else None)
    k = 1 if c["metric"] != "val" else 1000
    for b in c["brands"]:
        r = acum.setdefault(b["marca"], {}).setdefault(cli, [0.0, 0.0])
        r[0] += sum(s["a26"] for s in b["skus"]) * k; r[1] += sum(s["a25"] for s in b["skus"]) * k
# planilha mensal
sheet = {}
for key, skus in RAW.items():
    cli = MAP.get(key)
    if not cli: continue
    idx = 1 if cli == "CL" else 0
    for x in skus:
        r = sheet.setdefault(norm(x["marca"], x["sku"]), {}).setdefault(cli, {"r26": [0.0] * 9, "r25": [0.0] * 9})
        for k in range(9):
            r["r26"][k] += x["m"].get((2026, k + 1), (0, 0))[idx]; r["r25"][k] += x["m"].get((2025, k + 1), (0, 0))[idx]
# qual cliente tem a planilha completa (Jan–Set 2026 e 2025 batendo com o SO_OP)
fonte = {}
for cli in set(MAP.values()):
    s26 = sum(sum(d[cli]["r26"]) for d in sheet.values() if cli in d); s25 = sum(sum(d[cli]["r25"]) for d in sheet.values() if cli in d)
    o26 = sum(d[cli][0] for d in acum.values() if cli in d); o25 = sum(d[cli][1] for d in acum.values() if cli in d)
    ok = o26 and o25 and abs(s26 / o26 - 1) < .03 and abs(s25 / o25 - 1) < .03
    fonte[cli] = "real" if ok else "estimado"
res = {}
for m in set(acum) | set(sheet):
    for cli in set(MAP.values()):
        if fonte[cli] == "real":
            if cli not in sheet.get(m, {}): continue
            v = sheet[m][cli]; r26, r25 = v["r26"][:], v["r25"][:]
        else:
            if cli not in acum.get(m, {}): continue
            A26, A25 = acum[m][cli]; t26, t25 = TOT[cli][0][:9], TOT[cli][1][:9]
            r26 = [A26 * x / sum(t26) if sum(t26) else 0 for x in t26]; r25 = [A25 * x / sum(t25) if sum(t25) else 0 for x in t25]
        res.setdefault(m, {})[cli] = {"r26": r26 + [0.0, 0.0], "r25": r25 + [0.0, 0.0]}
for m, d in ON.items():
    for cli, v in d.items():
        k = 1 if cli == "CL" else 1000
        r = res.setdefault(m, {}).setdefault(cli, {"r26": [0.0] * 11, "r25": [0.0] * 11})
        r["r26"][9], r["r26"][10], r["r25"][9], r["r25"][10] = v[0] * k, (v[1] * k if v[1] else 0.0), v[2] * k, v[3] * k
for m, d in res.items():                 # Clamed sem Nov/26 → null (pendente; Nov/25 sai da comparação)
    if "CL" in d and not any((dd.get("CL") or {"r26": [0] * 11})["r26"][10] for dd in res.values()): d["CL"]["r26"][10] = None
out = {m: {c: {k: [None if v is None else round(v, 2) for v in a] for k, a in d2.items()} for c, d2 in d.items()
           if any((d2["r26"][i] or 0) or d2["r25"][i] for i in range(11))} for m, d in res.items()}
out = {m: d for m, d in out.items() if d}
json.dump({"meses": ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov"], "B": out, "fonte": fonte},
          open(OUT, "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
print("fonte Jan–Set:", fonte)
for m in ("OFF!", "EXPOSIS", "RAID", "GLADE", "LYSOFORM", "PATO", "PATO BLOCK"):
    d = out.get(m, {}); f = lambda k: sum(sum(v for v in c[k] if v) for cl, c in d.items() if cl != "CL")
    print(f"{m:10s} Jan–Nov 2026 R$ {f('r26')/1e6:6.2f} mi · 2025 R$ {f('r25')/1e6:6.2f} mi (sem Clamed)")
