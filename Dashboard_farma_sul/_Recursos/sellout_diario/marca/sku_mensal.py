"""Venda mensal por SKU × cliente (2026 e 2025) para o hover "Top SKUs" da aba 3D.
Fontes (só o que existe por SKU; mês sem fonte fica null e o 3D estima pelo mix do mês real mais próximo):
  - planilha de sell out por SKU (gerar_so_onepage.py): São João e Panvel Jan/25–Set/26, Clamed Jan/25–Set/26 (sem Ago/26) — R$ e un (Clamed só un)
  - Nissei: portal (tsv do dia, colunas tot_2026MM) Ago–Nov/26 em un, sem Povidine e sem Lysoform
  - Panvel Nov/26: Venda por Loja (xlsx do dia), R$ e un por item
  - DD-GAM Nov/26: portal (tsv de estoque, coluna venda)
  - Riomed Set–Nov/26: relatório Target (tsv, colunas set/out/nov)
  - São João: mix dos últimos 30 dias (Giro 30 do Qlik) para estimar Out/Nov
SKUs de fontes diferentes são unidos por uma chave (marca + medidas + tipo), pois cada portal escreve o nome de um jeito.
Uso: python sku_mensal.py <saida.json> <data AAAAMMDD>"""
import sys, os, re, json, csv, io
OUT, DT = sys.argv[1], sys.argv[2]
B = os.path.dirname(os.path.abspath(__file__)); R = os.path.join(B, "..", ".."); DAD = os.path.join(R, "sellout_diario", "dados")
OP = os.path.join(R, "OnePage")
src = open(os.path.join(OP, "gerar_so_onepage.py"), encoding="utf-8").read().split("# mês de referência")[0]
argv0 = sys.argv; sys.argv = ["x", os.path.join(OP, "Panvel", "dados", "PLANILHA DE SELL OUT CLIENTES FARMA.xlsx"), os.devnull]
g = {}; exec(src, g); RAW = g["raw"]; sys.argv = argv0
import openpyxl

MARCAS = ["PATO BLOCK", "MR MUSCULO", "LYSOFORM", "EXPOSIS", "GLADE", "RAID", "PATO", "OFF"]
def marca(nm, dflt=None):
    u = nm.upper()
    if "PATO" in u and "BLOCK" in u: return "PATO BLOCK"
    if "MUSCULO" in u: return "MR MUSCULO"
    for m in ["LYSOFORM", "EXPOSIS", "GLADE", "RAID", "PATO"]:
        if m in u: return m
    if re.search(r"\bOFF\b", u): return "OFF!"
    return dflt
TIPOS = [("LOCAO", r"LOCAO|LOC\b|\bLC\b|LOTION"), ("SPRAY", r"SPRAY|SPR\b"), ("AERO", r"AERO|AEROSOL|AER\b"), ("GEL", r"\bGEL\b"),
         ("KIDS", r"KIDS|INFANTIL|INF\b"), ("BABY", r"BABY|BEBE"), ("ELET", r"ELET|ELETR"), ("REFIL", r"REFIL|\bREF\b"), ("KIT", r"\bKIT\b"),
         ("FAMILY", r"FAMILY|FAM\b"), ("EXTREME", r"EXTREME|EXT\b"), ("ICARIDINA", r"ICARIDINA|ICAR"), ("TOQUE", r"TOQUE"),
         ("MULTI", r"MULTI"), ("BASE", r"BASE AGUA|BASE\b"), ("LIQ", r"LIQ|LIQUIDO"), ("ORIGINAL", r"ORIGINAL|ORIG\b"), ("LAVANDA", r"LAVANDA|LAV\b"),
         ("CITRUS", r"CITRUS"), ("DIFUSOR", r"DIFUSOR"), ("ACTIVE", r"ACTIVE"), ("DURACAO", r"DURACAO")]
import unicodedata
def chave(nm, mc):
    u = unicodedata.normalize("NFKD", nm.upper()).encode("ascii", "ignore").decode().replace(",", ".")
    med = sorted(set(re.findall(r"(\d+(?:\.\d+)?)\s*(ML|G|UN|N)\b", u)))
    med = [a + b for a, b in med]
    tp = [t for t, rx in TIPOS if re.search(rx, u)]
    return (mc or "") + "|" + "+".join(med) + "|" + "+".join(tp)

C = {}  # cli -> key -> {"b","nm","u26":[12],"r26":[12],"u25":[12]}
COV = {}  # cli -> {"u":[12 bool], "r":[12 bool]}
def put(cli, nm, mc, ano, mi, u, r=None, nome_pref=False):
    if not mc: return
    k = chave(nm, mc); d = C.setdefault(cli, {}).setdefault(k, {"b": mc, "nm": nm, "u26": [0.0] * 12, "r26": [0.0] * 12, "u25": [0.0] * 12})
    if nome_pref: d["nm"] = nm
    if ano == 2026: d["u26"][mi] += u or 0; d["r26"][mi] += r or 0
    else: d["u25"][mi] += u or 0
def cov(cli, mi, r=False):
    c = COV.setdefault(cli, {"u": [False] * 12, "r": [False] * 12, "u25": [False] * 12}); c["u"][mi] = True
    if r: c["r"][mi] = True

# 1) planilha (SJ, PV, CL) — Nissei da planilha não tem nome de SKU (vem só o código)
MAP = {"saojoao": "SJ", "panvel": "PV", "clamed": "CL"}
for key, cli in MAP.items():
    meses = {}
    for x in RAW[key]:
        mc = "PATO BLOCK" if ("BLOCK" in x["sku"].upper() and "PATO" in x["sku"].upper()) else marca(x["sku"], x["marca"])
        for (y, m), (val, un) in x["m"].items():
            if y not in (2025, 2026) or not (val or un): continue
            if cli == "CL": val = 0.0
            put(cli, x["sku"], mc, y, m - 1, un, val); meses.setdefault(y, set()).add(m - 1)
    for mi in meses.get(2026, ()): cov(cli, mi, r=cli != "CL")
    for mi in meses.get(2025, ()): COV.setdefault(cli, {"u": [False] * 12, "r": [False] * 12, "u25": [False] * 12})["u25"][mi] = True

# 1b) NISSEI e CLAMED: nessas abas o nome do SKU fica na coluna C (o leitor do OnePage lê a D = fator caixa) e os dados começam na linha 3
import datetime as _dt
wbp = openpyxl.load_workbook(os.path.join(OP, "Panvel", "dados", "PLANILHA DE SELL OUT CLIENTES FARMA.xlsx"), read_only=True, data_only=True)
C.pop("CL", None); COV.pop("CL", None)
for tab, cli in (("CLAMED", "CL"), ("NISSEI", "NS")):
    rows = list(wbp[tab].iter_rows(values_only=True)); h0, h1 = rows[0], rows[1]; cols = {}
    for j, c in enumerate(h0):
        if isinstance(c, _dt.datetime):
            q = next((k for k in range(j + 1, j + 3) if k < len(h1) and h1[k] == "QUANT. VENDIDA"), None); cols[(c.year, c.month)] = (j, q)
    meses = {}
    for r_ in rows[2:]:
        if not r_ or not r_[2] or not isinstance(r_[2], str): continue
        nm = r_[2].strip(); u = nm.upper()
        if cli == "NS" and ("POVIDINE" in u or "LYSOFORM" in u): continue
        mc = marca(nm, str(r_[1] or "").strip().upper() or None)
        for (y, m), (j, q) in cols.items():
            if y not in (2025, 2026): continue
            val = r_[j] if isinstance(r_[j], (int, float)) else 0; un = r_[q] if q is not None and isinstance(r_[q], (int, float)) else 0
            if not (val or un): continue
            put(cli, nm, mc, y, m - 1, un, 0 if cli == "CL" else val); meses.setdefault(y, set()).add(m - 1)
    for mi in meses.get(2026, ()): cov(cli, mi, r=cli != "CL")
    for mi in meses.get(2025, ()): COV.setdefault(cli, {"u": [False] * 12, "r": [False] * 12, "u25": [False] * 12})["u25"][mi] = True

# 2) Nissei: tsv do portal (tot_2026MM), sem Povidine/Lysoform
p = os.path.join(DAD, "nissei_%s.tsv" % DT)
rows = list(csv.DictReader(io.open(p, encoding="utf-8"), delimiter="\t"))
cols = [c for c in rows[0] if re.match(r"tot_2026\d\d$", c)]
for r_ in rows:
    nm = r_["produto"]; u = nm.upper()
    if "POVIDINE" in u or "LYSOFORM" in u: continue
    for c in cols: put("NS", nm, marca(nm), 2026, int(c[-2:]) - 1, float(r_[c] or 0), nome_pref=True)
for c in cols: cov("NS", int(c[-2:]) - 1)

# 3) Panvel Nov: Venda por Loja (R$ e un por item)
wb = openpyxl.load_workbook(os.path.join(DAD, "panvel_venda_202611_%s.xlsx" % DT), read_only=True); ws = wb.active
it = ws.iter_rows(values_only=True); hd = list(next(it))
iA, iM, iD, iV, iQ, iB = 0, 1, 3, hd.index(next(h for h in hd if h and "Valor Total" in h)), hd.index(next(h for h in hd if h and "Quantidade" in h)), hd.index(next(h for h in hd if h and "Descri" in h and "Marca" in h))
pvm = set()
for r_ in it:
    if not r_[iD]: continue
    t = str(r_[iV]).replace("R$", "").replace(".", "").replace(",", ".").replace(" ", "").strip()
    try: v = float(t)
    except ValueError: v = 0.0
    try: q = float(r_[iQ] or 0)
    except (TypeError, ValueError): q = 0.0
    mi = int(r_[iM]) - 1; pvm.add(mi)
    mc = marca(r_[iD], (r_[iB] or "").upper().replace("OFF", "OFF!") or None)
    put("PV", r_[iD], mc, int(r_[iA]), mi, q, v, nome_pref=True)
for mi in pvm: cov("PV", mi, r=True)

# 4) GAM Nov (venda do mês corrente no portal)
p = os.path.join(DAD, "gam_estoque_%s.tsv" % DT)
for r_ in csv.DictReader(io.open(p, encoding="utf-8"), delimiter="\t"):
    put("GAM", r_["produto"], marca(r_["produto"]), 2026, 10, float(r_["venda"] or 0), nome_pref=True)
cov("GAM", 10)

# 5) Riomed Set/Out/Nov
p = os.path.join(DAD, "riomed_%s.tsv" % DT)
for r_ in csv.DictReader(io.open(p, encoding="utf-8"), delimiter="\t"):
    for c, mi in (("set", 8), ("out", 9), ("nov", 10)): put("RM", r_["produto"], marca(r_["produto"]), 2026, mi, float(r_[c] or 0), nome_pref=True)
for mi in (8, 9, 10): cov("RM", mi)

# 6) São João: mix dos últimos 30 dias (Giro 30) — usado no 3D para estimar Out/Nov
wb = openpyxl.load_workbook(os.path.join(DAD, "sj_estoque", "sj_estoque_%s.xlsx" % DT), read_only=True); ws = wb.active
it = ws.iter_rows(values_only=True); next(it); sjmix = {}
for r_ in it:
    if not r_[0] or not r_[3]: continue
    k = chave(r_[0], marca(r_[0]))
    if k in C.get("SJ", {}): sjmix[k] = sjmix.get(k, 0) + float(r_[3])
    else: put("SJ", r_[0], marca(r_[0]), 2026, 0, 0); sjmix[k] = float(r_[3])

out = {"fonte": "sku_mensal.py %s" % DT, "c": {}}
for cli, d in C.items():
    ks = [k for k in d if sum(d[k]["u26"]) + sum(d[k]["u25"]) + (sjmix.get(k, 0) if cli == "SJ" else 0) > 0]
    cv = COV.get(cli, {"u": [False] * 12, "r": [False] * 12, "u25": [False] * 12})
    out["c"][cli] = {
        "s": [[d[k]["b"], d[k]["nm"]] for k in ks],
        "u": [[round(d[k]["u26"][mi]) for k in ks] if cv["u"][mi] else None for mi in range(12)],
        "r": [[round(d[k]["r26"][mi], 2) for k in ks] if cv["r"][mi] else None for mi in range(12)],
        "u25": [[round(d[k]["u25"][mi]) for k in ks] if cv["u25"][mi] else None for mi in range(12)],
        "mix": [round(sjmix.get(k, 0)) for k in ks] if cli == "SJ" else None}
json.dump(out, io.open(OUT, "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
for cli, v in out["c"].items():
    print(cli, len(v["s"]), "SKUs · meses 2026 reais:", [i + 1 for i, x in enumerate(v["u"]) if x], "· R$:", [i + 1 for i, x in enumerate(v["r"]) if x], "· 2025:", [i + 1 for i, x in enumerate(v["u25"]) if x])
