"""Atualiza os dados embutidos na aba 3D (apresentacao_3d.html) a partir do dashboard — é o que a aba usa quando o dashboard
é aberto como arquivo (file://), onde ela não consegue ler o dashboard ao vivo.
  - ESD (estoque por cliente e SKU, do card Estoque / ESTOQUE_DATA) para a visão Estoque
  - C (Sell Out FY27 Jul→Nov por cliente), CALD (ano-calendário Jan→Nov por cliente), SJIC (São João só Isadora)
  - BRMM (mensal por marca): se existir nissei_marca_*.json, a Nissei por marca passa a ser real (portal/planilha), sem Povidine/Lysoform.
  - --sj <sj_marca.json> (saída do sj_qlik_marca.py): São João por marca real (Qlik) em BRMM.
  - --sku <sku_mensal.json> (saída do sku_mensal.py): venda mensal por SKU (SKM) para o hover "Top SKUs".
Uso: python atualizar_snapshot_3d.py <dashboard.html> <apresentacao_3d.html> [marca_mensal.json] [nissei_marca.json] [--sj sj_marca.json] [--sku sku_mensal.json]"""
import sys, re, json
A = sys.argv[1:]; SJJ = None
if "--sj" in A: k = A.index("--sj"); SJJ = A[k + 1]; A = A[:k] + A[k + 2:]
SKJ = None
if "--sku" in A: k = A.index("--sku"); SKJ = A[k + 1]; A = A[:k] + A[k + 2:]
H, P = A[0:2]; MM = A[2] if len(A) > 2 else None; NJ = A[3] if len(A) > 3 else None
D = open(H, encoding="utf-8").read(); h = open(P, encoding="utf-8", newline="").read()


import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))); import dashboard_dados as dd
_d = dd.Dashboard(H)
arr = _d.ler   # arr(âncora, ano=None, de=0) → lista de 12 números


t = _d.pos("total:", _d.pos("const NS ="))
SRC = {"SJ": ("const SJ_REC", "const SJ_UNID", 0, 1), "GAM": ("const GAM_REC", "const GAM_VOL", 0, 1), "NS": ("rec:", "vol:", t, 1),
       "PV": ("const PV_REC", "const PV_VOL", 0, 1), "GA": ("const GAUCHA_REC", "const GAUCHA_VOL", 0, 1),
       "CL": ("const CL_REC_", "const CL_VOL_", 0, 0), "RM": ("const RIOMED_REC_", "const RIOMED_VOL_", 0, 0)}
full = {}
for k, (r, u, de, y) in SRC.items():
    if y: g = lambda a, ano, de=de: arr(a, ano, de)
    else: g = lambda a, ano: arr(a + ano + " =")
    full[k] = {"r25": g(r, "2025"), "r26": g(r, "2026"), "u25": g(u, "2025"), "u26": g(u, "2026")}
N = max(i + 1 for v in full.values() for i in range(12) if v["r26"][i] is not None or v["u26"][i] is not None)


def cut(v, a, b):
    return {kk: [(None if (x is None and kk.endswith("26")) else (0 if x is None else round(x, 2))) for x in v[kk][a:b]] for kk in v}


fmt = lambda a: "[" + ",".join("null" if v is None else (str(int(v)) if float(v).is_integer() else str(v)) for v in a) + "]"
cal = {k: cut(v, 0, N) for k, v in full.items()}
def dif(a, b, z):
    return [(0 if z else None) if x is None else round(x - (y or 0), 2) for x, y in zip(a, b)]


sjic = {"r25": dif(arr("const SJ_REC", "2025"), arr("const SJC_REC ="), 1), "r26": dif(arr("const SJ_REC", "2026"), arr("const SJC_REC_26 ="), 0),
        "u25": dif(arr("const SJ_UNID", "2025"), arr("const SJC_VOL ="), 1), "u26": dif(arr("const SJ_UNID", "2026"), arr("const SJC_VOL_26 ="), 0)}
h, n = re.subn(r"var SJIC=\{.*?\};\n", "var SJIC=" + json.dumps(sjic, separators=(",", ":")) + ";\n", h, count=1, flags=re.S); assert n == 1, "SJIC"
h, n = re.subn(r"var CALD=\{n:\d+,c:\{.*?\}\};", "var CALD={n:%d,c:%s};" % (N, json.dumps(cal, separators=(",", ":"))), h, count=1, flags=re.S); assert n == 1, "CALD"
for k, v in full.items():
    c = cut(v, 6, N)
    h, n = re.subn(r"(\{id:'%s',[^\n]*?r25:)\[[^\]]*\](, r26:)\[[^\]]*\](, u25:)\[[^\]]*\](, u26:)\[[^\]]*\]" % k,
                   lambda m: m.group(1) + fmt(c["r25"]) + m.group(2) + fmt(c["r26"]) + m.group(3) + fmt(c["u25"]) + m.group(4) + fmt(c["u26"]), h, count=1)
    assert n == 1, k
if MM:
    M = json.load(open(MM, encoding="utf-8"))
    if NJ:
        X = json.load(open(NJ, encoding="utf-8")); n26 = len(X["r26"]["OFF"])
        for b, key in (("OFF!", "OFF"), ("EXPOSIS", "EXPOSIS"), ("RAID", "RAID")):
            r26 = [round(v, 2) for v in X["r26"][key]] + [0.0] * (11 - n26); r25 = [round(v, 2) for v in X["r25"][key][:11]]
            M["B"].setdefault(b, {})["NS"] = {"r26": r26[:11], "r25": r25}
        # Nissei: Lysoform entra no Edmar desde 18/11/2026 (mantém o NS do Lysoform no BRMM)
        M["fonte"]["NS"] = "real"
    if SJJ:
        S = json.load(open(SJJ, encoding="utf-8")); ms = S["meses"]
        for b in list(M["B"]): M["B"][b].pop("SJ", None)
        for b, d in S["marca"].items():
            g2 = lambda y: [round(d["rec"][ms.index("%d-%02d" % (y, i + 1))], 2) if "%d-%02d" % (y, i + 1) in ms else 0.0 for i in range(11)]
            M["B"].setdefault(b, {})["SJ"] = {"r26": g2(2026), "r25": g2(2025)}
        M["fonte"]["SJ"] = "real"
    if NJ or SJJ:
        json.dump(M, open(MM, "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
    h, n = re.subn(r"var BRMM=\{.*?\};\n", "var BRMM=" + json.dumps({"meses": M["meses"], "B": M["B"], "fonte": M["fonte"]}, ensure_ascii=False, separators=(",", ":")) + ";\n", h, count=1, flags=re.S)
    assert n == 1, "BRMM"
# Estoque por cliente (card ESTOQUE_DATA do dashboard) → ESD da visão Estoque
MAPE = {"DD-GAM": "GAM", "São João": "SJ", "Nissei": "NS", "Clamed": "CL", "Panvel": "PV", "DD-Gaúcha": "GA", "DD-Riomed": "RM"}
ea = D.index("const ESTOQUE_DATA = ") + 21; EST, _ = json.JSONDecoder().raw_decode(D[ea:])
esd = {MAPE[k]: {"d": v["data_ref"], "s": [[x["marca"], x["sku"], int(x["est"] or 0), int(x["so"] or 0)] for x in v["skus"]]} for k, v in EST.items() if k in MAPE}
h, n = re.subn(r"var ESD=\{.*?\};(\r?\n)", lambda m: "var ESD=" + json.dumps(esd, ensure_ascii=False, separators=(",", ":")) + ";" + m.group(1), h, count=1, flags=re.S)
assert n == 1, "ESD"
# mês parcial do Sell Out (SO_PARCIAL) → PARC, base da tendência do mês na aba 3D
mp = re.search(r"var SO_PARCIAL = \{mes:(\d+), ate:'([^']+)'\};", D)
if mp:
    h, n = re.subn(r"var PARC=\{mes:\d+,ate:'[^']*'\};", "var PARC={mes:%s,ate:'%s'};" % (mp.group(1), mp.group(2)), h, count=1)
    assert n == 1, "PARC"
    mc = re.search(r"var SO_PARCIAL_CLI = (\{[^}]*\});", D); MP = {"saojoao": "SJ", "nissei": "NS", "clamed": "CL", "panvel": "PV", "ddgam": "GAM", "ddgaucha": "GA", "ddriomed": "RM"}
    par = re.findall(r"['\"]?(\w+)['\"]?\s*:\s*['\"]([^'\"]+)['\"]", mc.group(1)) if mc else []
    cli = {MP[k]: v for k, v in par if k in MP}
    h, n = re.subn(r"var PARCC=\{[^}]*\};", "var PARCC=" + json.dumps(cli, ensure_ascii=False) + ";", h, count=1)
    assert n == 1, "PARCC"
# data do snapshot no subtítulo (antes ficava fixo em 12/11/2026)
import datetime
h, n = re.subn(r"var FONTE='snapshot de [^']*';", "var FONTE='snapshot de %s';" % datetime.date.today().strftime("%d/%m/%Y"), h, count=1)
assert n == 1, "FONTE"
# Sell In FY27 por cliente (h = FY26 real, p = plano FY27, r = realizado) para o Acumulado da Tendência
_i = D.index("const SELLIN_DATA_FY27 = ["); _blk = D[_i:D.index("];", _i)]
_MP = {"São João": "SJ", "DD-Gaúcha": "GA", "Panvel": "PV", "DD-GAM": "GAM", "Nissei": "NS", "DD-Riomed": "RM", "Clamed": "CL"}
_sip = {_MP[m.group(1)]: {"h": float(m.group(2)), "p": float(m.group(3)), "r": float(m.group(4))}
        for m in re.finditer(r"nome:'([^']+)'.*?hist:([\d.]+), plan:([\d.]+), meta:[\d.]+, real:([\d.]+)", _blk) if m.group(1) in _MP}
h, n = re.subn(r"var SIP=\{[^;]*\};", lambda m: "var SIP=" + json.dumps(_sip, separators=(",", ":")) + ";", h, count=1)
if not n: print("aviso: var SIP não encontrada no 3D")
# Sell In mensal embutido (usado quando o 3D abre fora do dashboard): SI (FY, Jul→mês atual) e SICALD (ano-calendário Jan→mês atual)
def _siblk(nome_const):
    i = D.index(nome_const); blk = D[i:D.index("];", i)]; out = {}
    for m in re.finditer(r"nome:'([^']+)'(.*?)\}", blk, re.S):
        g = lambda k: [float(x) for x in re.search(k + r":\[([^\]]*)\]", m.group(2)).group(1).split(",")] if re.search(k + r":\[", m.group(2)) else [0.0] * 12
        out[m.group(1)] = {"hist_m": g("hist_m"), "real_m": g("real_m")}
    return out
_f27, _f26 = _siblk("const SELLIN_DATA_FY27 = ["), _siblk("const SELLIN_DATA_FY26 = [")
_ma = int(re.search(r"var SELLIN_MES_ATUAL\s*=\s*(\d+)", D).group(1)); _lbl = re.search(r"var SELLIN_MES_ATUAL_LBL\s*=\s*'([^']+)'", D).group(1)
_NM = ['Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez', 'Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun']; _n = _ma + 1
_IDS = {'São João': 'SJ', 'DD-GAM': 'GAM', 'Nissei': 'NS', 'Panvel': 'PV', 'DD-Gaúcha': 'GA', 'Clamed': 'CL', 'DD-Riomed': 'RM', 'Riomed': 'RM'}
_raw = {}; _e25 = [0.0] * _n; _e26 = [0.0] * _n; _ex = set()
for _lst, _k, _e in ((_f27, "u26", _e26), (_f26, "u25", _e25)):
    for _nome, _c in _lst.items():
        _id = _IDS.get(_nome)
        for _j in range(_n):
            _v = _c["real_m"][_j] if _j < len(_c["real_m"]) else 0.0
            if _id: _raw.setdefault(_id, {"u25": [0.0] * _n, "u26": [0.0] * _n})[_k][_j] += _v
            else: _e[_j] += _v; _ex.add(_nome) if _v else None
_si = "var SI=" + json.dumps({"MES": _NM[:_n], "parcial": _lbl[0] + _lbl[1:].lower(), "ext25": _e25, "ext26": _e26, "extNomes": ", ".join(sorted(_ex)), "raw": _raw}, ensure_ascii=False, separators=(",", ":")) + ";\n"
h, n = re.subn(r"var SI=\{MES:.*?\} \}\};\n|var SI=\{\"MES\".*?\};\n", lambda m: _si, h, count=1, flags=re.S)
if not n: print("aviso: var SI não encontrada no 3D")
_nc = 6 + _ma + 1; _rawc = {}; _c25 = [0.0] * _nc; _c26 = [0.0] * _nc; _exc = set()
for _nome, _c in _f26.items():
    _r27 = _f27.get(_nome, {}).get("real_m", [0.0] * 12)
    _y26 = _c["real_m"][6:12] + _r27[:_ma + 1]; _y25 = _c["hist_m"][6:12] + _c["real_m"][:_ma + 1]
    _id = _IDS.get(_nome)
    if _id:
        _r = _rawc.setdefault(_id, {"u25": [0.0] * _nc, "u26": [0.0] * _nc})
        for _j in range(_nc): _r["u25"][_j] += _y25[_j]; _r["u26"][_j] += _y26[_j]
    else:
        for _j in range(_nc): _c25[_j] += _y25[_j]; _c26[_j] += _y26[_j]
        if any(_y25 + _y26): _exc.add(_nome)
h, n = re.subn(r"var SICALD=\{.*?\};\n", lambda m: "var SICALD=" + json.dumps({"n": _nc, "raw": _rawc, "ext25": _c25, "ext26": _c26, "extNomes": ", ".join(sorted(_exc))}, ensure_ascii=False, separators=(",", ":")) + ";\n", h, count=1, flags=re.S)
if not n: print("aviso: var SICALD não encontrada no 3D")
if SKJ:
    sk = open(SKJ, encoding="utf-8").read().strip()
    h, n = re.subn(r"var SKM=\{.*?\};(\r?\n)", lambda m: "var SKM=" + sk + ";" + m.group(1), h, count=1, flags=re.S); assert n == 1, "SKM"
open(P, "w", encoding="utf-8", newline="").write(h)
print("ok · meses", N, "· NS Jul→ r26", cut(full["NS"], 6, N)["r26"])
