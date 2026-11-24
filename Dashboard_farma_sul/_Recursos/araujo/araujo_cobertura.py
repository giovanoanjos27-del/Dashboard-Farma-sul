"""Araujo › One Page: card 'Estoque e Cobertura por loja' (o mesmo da São João/Nissei/Panvel/Clamed) — 24/11/2026.
Fonte: DADO ARAUJO 29-05.xlsx · ESTOQUE LOJA (SKU × loja, 29/05/26) + ESTOQUE CD; giro = venda Mai/26 (aba 2026 da base de sell out).
ARA_COBERTURA = [{sku, marca, lojas (lojas com estoque > 0), total (lojas listadas para o SKU), estoque (lojas), estoqueCD, giro30}]
Uso: python araujo_cobertura.py <base.html>"""
import sys, os, re, json, warnings
import pandas as pd
warnings.filterwarnings("ignore"); sys.stdout.reconfigure(encoding="utf-8")
H = sys.argv[1]; h = open(H, encoding="utf-8", newline="").read()
A = os.path.dirname(os.path.abspath(__file__))


def rep(a, b, n=1):
    global h
    assert h.count(a) == n, (h.count(a), a[:100]); h = h.replace(a, b)


assert "ARA_COBERTURA" not in h, "já aplicado"
D = os.path.join(A, "DADO ARAUJO 29-05.xlsx")
el = pd.read_excel(D, sheet_name="ESTOQUE LOJA"); cd = pd.read_excel(D, sheet_name="ESTOQUE CD", header=1)
proc = pd.read_excel(D, sheet_name="BASE PROCV").drop_duplicates("Cód Produto DV").set_index("Cód Produto DV")
n26 = pd.read_excel(os.path.join(A, "TransferXL-06BCNjgwr5kgG", "BASE SELL OUT ARAUJO-23-24-25-26.xlsx"), sheet_name="2026")
mai = n26[(n26["Ano"] == 2026) & (n26["Mês"] == "MAIO")].groupby("Cód Produto DV")["UND"].sum()
stC = cd.groupby("Cód Produto DV")["CD M. ANTONIO ARAUJO"].sum()
el = el[el["Cód Produto DV"].astype(str).str.contains(r"\d")]
nome = lambda p: " ".join(w.capitalize() if not re.match(r"^\d", w) else w.lower() for w in str(p).split())
MARCA = lambda m: {"OFF": "OFF!", "LUSTRA MOVEIS": "BRAVO"}.get(str(m).strip().upper(), str(m).strip().upper())
C = []
for c, g in el.groupby("Cód Produto DV"):
    est = pd.to_numeric(g["Loja"], errors="coerce").fillna(0)
    mc = MARCA(proc.loc[c, "MARCA"]) if c in proc.index else ""
    C.append({"sku": nome(g["Produto"].iloc[0]), "marca": mc, "lojas": int((est > 0).sum()), "total": int(g["Loja - Fiscal"].nunique()),
              "estoque": int(est.sum()), "estoqueCD": int(stC.get(c, 0) or 0), "giro30": int(mai.get(c, 0) or 0)})
print("SKUs", len(C), "· lojas máx", max(x["total"] for x in C), "· estoque lojas", sum(x["estoque"] for x in C), "· CD", sum(x["estoqueCD"] for x in C),
      "· venda Mai", sum(x["giro30"] for x in C))
rep("var OP1_COB_CLIS = ['saojoao','nissei','panvel','clamed'];",
    "/* Araujo: estoque por loja 29/05/26 (DADO ARAUJO 29-05) × venda Mai/26 */\nvar ARA_COBERTURA = " + json.dumps(C, ensure_ascii=False, separators=(",", ":")) + ";\n"
    "var OP1_COB_CLIS = ['saojoao','nissei','panvel','clamed','araujo'];")
rep("clamed:{arr:['CL_COBERTURA'], ref:'Nov/26 até 15/11'}};", "clamed:{arr:['CL_COBERTURA'], ref:'Nov/26 até 15/11'}, araujo:{arr:['ARA_COBERTURA'], ref:'29/05/26 (venda Mai/26)'}};")
open(H, "w", encoding="utf-8", newline="").write(h); print("ok")
