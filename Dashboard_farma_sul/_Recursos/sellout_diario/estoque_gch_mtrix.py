"""Estoque DD-Gaúcha pelo Mtrix (SSE - Ceras Johnson › Days On Hand › Detalhes em Und, Agente = GAUCHAFARMA, dimensão Descrição, Send to Excel).
Dois exports: <total.xlsx> sem período (posição do estoque atual) e <venda.xlsx> com o mês de referência marcado (S.Out do mês).
Reconstrói GCH_ESTOQUE (nomes do Mtrix): só produtos com estoque ou venda; dias = estoque ÷ (venda ÷ 30); crítico < 15 d, atenção < 30 d.
Uso: python estoque_gch_mtrix.py <html> <total.xlsx> <venda.xlsx>"""
import sys, json, re, warnings
import openpyxl
warnings.filterwarnings("ignore")
H, XT, XV = sys.argv[1:4]
h = open(H, encoding="utf-8", newline="").read()


def num(v):
    if v is None: return 0
    if isinstance(v, (int, float)): return v
    return float(str(v).replace(".", "").replace(",", "."))


def ler(x):
    r = list(openpyxl.load_workbook(x, read_only=True, data_only=True).worksheets[0].iter_rows(values_only=True))
    out = {}
    for t in r[1:]:
        if not t[2]: continue
        out[" ".join(str(t[2]).split())] = {"marca": t[1], "so": num(t[4]), "est": num(t[9]), "dt": t[10]}
    return out


T, V = ler(XT), ler(XV)
MB = {"OFF": "OFF!", "MR. MUSCULO": "MR MUSCULO", "MR MUSCULO": "MR MUSCULO"}
dt = max(x["dt"] for x in T.values() if x["dt"])
arr = []
for d, x in T.items():
    e = int(max(0, x["est"])); v = int(max(0, (V.get(d) or {}).get("so", 0)))
    if not e and not v: continue
    dias = round(e / (v / 30)) if v else (999 if e else 0)
    risco = "critico" if (e == 0 or (v and dias < 15)) else ("atencao" if (v and dias < 30) else "ok")
    m = MB.get(str(x["marca"]).upper(), str(x["marca"]).upper())
    arr.append({"sku": re.sub(r"^PR\s+", "", d), "marca": m, "estoque": e, "venda": v, "venda_abr": v, "dem": v, "giro": v,
                "vendaMar": 0, "vendaAbr": 0, "vendaJun": v, "fev26": 0, "mar26": 0, "cob": dias, "dias": dias, "risco": risco,
                "lojas": e, "cdRS": 0, "cdPR": 0, "pend": 0, "lojasCount": 0, "totalLojas": 0})
arr.sort(key=lambda x: (x["risco"] != "critico", -x["estoque"]))
tag = "const GCH_ESTOQUE = "; a = h.index(tag) + len(tag); old, n = json.JSONDecoder().raw_decode(h[a:]); b = a + n
NL = "\r\n" if "\r\n" in h[a:b] else "\n"
h = h[:a] + "[" + NL + ("," + NL).join("  " + json.dumps(x, ensure_ascii=False) for x in arr) + NL + "]" + h[b:]
open(H, "w", encoding="utf-8", newline="").write(h)
print("posição", dt.strftime("%d/%m/%Y"), "· GCH_ESTOQUE", len(old), "->", len(arr), "SKUs · estoque", sum(x["estoque"] for x in old), "->", sum(x["estoque"] for x in arr),
      "· venda ref", sum(x["venda"] for x in arr), "· críticos", sum(x["risco"] == "critico" for x in arr))
