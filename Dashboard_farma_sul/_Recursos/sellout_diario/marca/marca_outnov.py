"""Sell Out por marca Out/Nov (2026 e 2025) por cliente, para a aba 3D (filtro de marca até Nov).
Total do cliente no mês = arrays do dashboard (mesma base dos cards); a quebra por marca usa a melhor fonte disponível:
  2026 real: Panvel (Dimed por SKU, R$), Nissei (PIN por SKU, un; R$ = André/Edmar do dashboard), Riomed (e-mail SKU, un), GAM Nov (portal, un),
             São João (Isadora x Caroline exato; dentro de cada uma, mix Set/26 do SO_OP).
  2026 Clamed Out: CSVs do portal (un, real, inclui Pato Block).  Clamed Nov: sem dado.
  2026 estimado: GAM Out e Gaúcha = mix Set/26 do SO_OP.
  2025: Planilha SKU (SJ, Nissei, Panvel, Clamed) real; GAM, Gaúcha e Riomed = mix Set/25 do SO_OP.
Unidades -> R$: peso pelo preço médio da marca na Panvel (Out+Nov/26).
Saída JSON: {marca: {cliente: [out26, nov26, out25, nov25]}} em R$ mil (Clamed em unidades) + fontes.
Uso: python marca_outnov.py <dashboard.html> <saida.json>"""
import sys, re, json, csv, warnings, os
import openpyxl
warnings.filterwarnings("ignore")
H, OUT = sys.argv[1:3]; h = open(H, encoding="utf-8").read()
B = os.path.dirname(os.path.abspath(__file__)); D = os.path.join(B, "..", "dados"); DL = os.path.join(os.path.expanduser("~"), "Downloads")
OP_DIR = os.path.join(B, "..", "..", "OnePage")


def arr(anchor, ano=None, de=0):
    i = h.index(anchor, de)
    m = (re.compile(r"'%s'\s*:\s*(\[[^\[\]]*\])" % ano) if ano else re.compile(r"(\[[^\[\]]*\])")).search(h, i)
    return [None if x.strip() in ("null", "") else float(x) for x in m.group(1)[1:-1].split(",")]


def obj(n):
    a = h.index(n + " = ") + len(n + " = ")
    return json.JSONDecoder().raw_decode(h[a:])[0]


def marca(p):
    p = str(p).upper()
    if "BLOQUEADOR" in p and "PATO" in p: return "PATO BLOCK"   # Clamed: 'BLOQUEADOR DE ODORES SANITARIOS PATO'
    for k, m in (("PATO BLOCK", "PATO BLOCK"), ("EXPOS", "EXPOSIS"), ("RAID", "RAID"), ("OFF", "OFF!"), ("LYSOFORM", "LYSOFORM"),
                 ("GLADE", "GLADE"), ("PATO", "PATO"), ("MUSCULO", "MR MUSCULO")):
        if k in p: return m
    return None


def num(x):
    if isinstance(x, (int, float)): return float(x)
    s = str(x or "").replace("R$", "").strip()
    if not s or s in ("-", "—"): return 0.0
    return float(s.replace(".", "").replace(",", "."))


def share(d):
    t = sum(d.values())
    return {k: v / t for k, v in d.items() if v} if t else {}


O = obj("SO_OP"); ns = h.index("const NS =")
an = h.index("andre:", ns); ed = h.index("edmar:", ns); tt = h.index("total:", ns)


def q(a26, a25): return [a26[9], a26[10], a25[9], a25[10]]


sj26, sj25 = arr("const SJ_REC", "2026"), arr("const SJ_REC", "2025")
sjc26, sjc25 = arr("const SJC_REC_26 ="), arr("const SJC_REC =")
T = {"SJI": [sj26[9] - sjc26[9], sj26[10] - sjc26[10], sj25[9] - sjc25[9], sj25[10] - sjc25[10]],
     "SJC": [sjc26[9], sjc26[10], sjc25[9], sjc25[10]],
     "PV": q(arr("const PV_REC", "2026"), arr("const PV_REC", "2025")),
     "GAM": q(arr("const GAM_REC", "2026"), arr("const GAM_REC", "2025")),
     "GA": q(arr("const GAUCHA_REC", "2026"), arr("const GAUCHA_REC", "2025")),
     "RM": q(arr("const RIOMED_REC_2026 ="), arr("const RIOMED_REC_2025 =")),
     "CL": q(arr("const CL_VOL_2026 ="), arr("const CL_VOL_2025 =")),
     "NSA": q(arr("rec:", "2026", an), arr("rec:", "2025", an)),
     "NSE": q(arr("rec:", "2026", ed), arr("rec:", "2025", ed)),
     "NST": q(arr("rec:", "2026", tt), arr("rec:", "2025", tt))}


def opmix(cli, k, brands=None):  # mix do SO_OP: k = 'm26' (Set/26) ou 'm25' (Set/25)
    d = {}
    for b in O["clientes"][cli]["brands"]:
        if brands and b["marca"] not in brands: continue
        d[b["marca"]] = sum(s[k] for s in b["skus"])
    return share(d)


def pv_file(f, cv, cq, cd):
    ws = openpyxl.load_workbook(f, read_only=True, data_only=True).worksheets[0]
    rows = list(ws.iter_rows(values_only=True)); ix = {c: i for i, c in enumerate(rows[0])}
    c = lambda s: next(k for k in ix if k and s in str(k))
    d = {}
    for r in rows[1:]:
        if not r: continue
        m = marca(r[ix[c(cd)]])
        if not m: continue
        x = d.setdefault(m, [0, 0]); x[0] += num(r[ix[c(cv)]]); x[1] += num(r[ix[c(cq)]])
    return d


pvO = pv_file(os.path.join(DL, "RelatorioVendaGeral_outubro2026_20261110114345.xlsx"), "Venda Efetiva (R$)", "Qtd. Venda", "Descri")
pvN = pv_file(os.path.join(D, "panvel_venda_202611_20261112.xlsx"), "Valor Total", "Quantidade", "Descri")
PR = {m: (pvO.get(m, [0, 0])[0] + pvN.get(m, [0, 0])[0]) / max(1, pvO.get(m, [0, 0])[1] + pvN.get(m, [0, 0])[1]) for m in set(pvO) | set(pvN)}
for k, v in (("LYSOFORM", 20), ("PATO", 15), ("GLADE", 30), ("PATO BLOCK", 15)): PR.setdefault(k, v)


def unR(d): return share({m: u * PR.get(m, 30) for m, u in d.items() if m})


res = {}; FONTE = {}


def put(cli, i, mix, total, fonte):
    if total is None: return
    for m, s in mix.items(): res.setdefault(m, {}).setdefault(cli, [0, 0, 0, 0])[i] += total * s
    FONTE.setdefault(cli, {})[["Out26", "Nov26", "Out25", "Nov25"][i]] = fonte


# planilha SKU (2025 real) — mesma leitura do gerar_so_onepage.py
src = open(os.path.join(OP_DIR, "gerar_so_onepage.py"), encoding="utf-8").read().split("# mês de referência")[0]
sys.argv = ["x", os.path.join(OP_DIR, "Panvel", "dados", "PLANILHA DE SELL OUT CLIENTES FARMA.xlsx"), os.devnull]
g = {}; exec(src, g); RAW = g["raw"]


def pl(key, ym, idx, brands=None):
    d = {}
    for x in RAW[key]:
        if brands and x["marca"] not in brands: continue
        d[x["marca"]] = d.get(x["marca"], 0) + x["m"].get(ym, (0, 0))[idx]
    return share(d)


HB, CV = {"OFF!", "EXPOSIS", "RAID"}, {"LYSOFORM", "GLADE", "PATO"}
# São João
for i in (0, 1):
    put("SJ", i, opmix("saojoao", "m26"), T["SJI"][i], "Isadora/Caroline exato; marca = mix Set/26 (est.)")
    put("SJ", i, opmix("caroline", "m26"), T["SJC"][i], "idem")
for i, ym in ((2, (2025, 10)), (3, (2025, 11))):
    put("SJ", i, pl("saojoao", ym, 0, HB), T["SJI"][i], "planilha SKU")
    put("SJ", i, pl("saojoao", ym, 0, CV), T["SJC"][i], "planilha SKU")
# Nissei: André = OFF+EXPOSIS (split por un do PIN x preço), Edmar = RAID
nsu = {"tot_202610": {}, "tot_202611": {}}
for r in csv.DictReader(open(os.path.join(D, "nissei_20261112.tsv"), encoding="utf-8"), delimiter="\t"):
    m = marca(r["produto"])
    if m in ("OFF!", "EXPOSIS") and "POVIDINE" not in r["produto"].upper():
        for k in nsu: nsu[k][m] = nsu[k].get(m, 0) + int(r[k])
for i, k in ((0, "tot_202610"), (1, "tot_202611")):
    put("NS", i, unR(nsu[k]), T["NSA"][i], "PIN SKU (un->R$)")
    put("NS", i, {"RAID": 1}, T["NSE"][i], "PIN SKU")
for i, ym in ((2, (2025, 10)), (3, (2025, 11))): put("NS", i, pl("nissei", ym, 0, HB), T["NST"][i], "planilha SKU")
# Panvel
for i, d in ((0, pvO), (1, pvN)): put("PV", i, share({m: v[0] for m, v in d.items()}), T["PV"][i], "Dimed SKU R$")
for i, ym in ((2, (2025, 10)), (3, (2025, 11))): put("PV", i, pl("panvel", ym, 0), T["PV"][i], "planilha SKU")
# GAM
gn = {}
for r in csv.DictReader(open(os.path.join(D, "gam_estoque_20261112.tsv"), encoding="utf-8"), delimiter="\t"):
    m = marca(r["produto"]); gn[m] = gn.get(m, 0) + int(r["venda"])
put("GAM", 0, opmix("ddgam", "m26"), T["GAM"][0], "mix Set/26 (est.)")
put("GAM", 1, unR(gn), T["GAM"][1], "portal SKU (un->R$)")
for i in (2, 3): put("GAM", i, opmix("ddgam", "m25"), T["GAM"][i], "mix Set/25 (est.)")
# Gaúcha
for i in (0, 1): put("GA", i, opmix("ddgaucha", "m26"), T["GA"][i], "mix Set/26 (est.)")
for i in (2, 3): put("GA", i, opmix("ddgaucha", "m25"), T["GA"][i], "mix Set/25 (est.)")
# Riomed
rm = {"out": {}, "nov": {}}
for r in csv.DictReader(open(os.path.join(D, "riomed_20261112.tsv"), encoding="utf-8"), delimiter="\t"):
    m = marca(r["produto"])
    for k in rm: rm[k][m] = rm[k].get(m, 0) + int(r[k])
put("RM", 0, unR(rm["out"]), T["RM"][0], "e-mail SKU (un->R$)")
put("RM", 1, unR(rm["nov"]), T["RM"][1], "e-mail SKU (un->R$)")
for i in (2, 3): put("RM", i, opmix("ddriomed", "m25"), T["RM"][i], "mix Set/25 (est.)")
# Clamed (unidades): Out/26 real pelos CSVs do portal (pastas '*_202610 ULTIMO*', arquivos duplicados ignorados).
# OFF+EXPOSIS = total do dashboard (CL_VOL); Pato Block entra por fora (não faz parte do total HB da Clamed).
import glob, hashlib
cl, vistos = {}, set()
for f in sorted(glob.glob(os.path.join(B, "..", "..", "Giovano SCJ", "clamed", "*_202610 ULTIMO*", "Vendas_*.csv"))):
    bts = open(f, "rb").read(); hs = hashlib.md5(bts).hexdigest()
    if hs in vistos: continue
    vistos.add(hs)
    for r in csv.DictReader(bts.decode("latin-1").splitlines(), delimiter=";"):
        m = marca(r["de_produto"])
        if m: cl[m] = cl.get(m, 0) + float(r["qt_vendida"].replace(",", "."))
if cl:
    for m, u in cl.items(): res.setdefault(m, {}).setdefault("CL", [0, 0, 0, 0])[0] += u
    FONTE.setdefault("CL", {})["Out26"] = "CSV portal Clamed (un)"
else:
    put("CL", 0, opmix("clamed", "m26"), T["CL"][0], "mix Set/26 (est.)")
for i, ym in ((2, (2025, 10)), (3, (2025, 11))): put("CL", i, pl("clamed", ym, 1), T["CL"][i], "planilha SKU")

out = {m: {c: [round(v / (1 if c == "CL" else 1000), 1) for v in vs] for c, vs in d.items()} for m, d in res.items()}
json.dump({"meses": ["Out", "Nov"], "parcial": "Nov/26 até 11/11", "B": out, "fonte": FONTE, "preco_pv": {k: round(v, 2) for k, v in PR.items()}},
          open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
for m in ("OFF!", "EXPOSIS", "RAID", "GLADE", "LYSOFORM", "PATO", "PATO BLOCK", "MR MUSCULO"):
    d = out.get(m, {}); f = lambda i: sum(v[i] for c, v in d.items() if c != "CL")
    print(f"{m:10s} Out/26 {f(0):8.1f} | Nov/26 {f(1):8.1f} | Out/25 {f(2):8.1f} | Nov/25 {f(3):8.1f}  (R$ mil, sem Clamed) | Clamed un {d.get('CL', '-')}")
print("preço Panvel R$/un:", {k: round(v, 2) for k, v in PR.items()})
