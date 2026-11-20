"""CPT Clientes › Distribuição dos intocáveis segue o Período:
  · Q2 (Out/26 vs Out/25) → Out/26 (Mês)  · FY27 Jul–Out e demais → Jul–Out/26 (IQVIA YTD Fiscal; Q1 Jul–Set não existe na edição 202610)
Jul–Out: exports intocaveis/ytd/*.xlsx (mesmos 7 recortes, Período = YTD Fiscal) → CPT2_INTOC_YTD [Loção, Kids, Spray, ≥1, ≥2, os 3]
por inclusão-exclusão; base = lojas com venda da categoria em algum mês de Jul–Out/26 (Matriz de Lojas loja a loja, preco/SCJ_RS_c*.xlsx)
→ CPT2_LOJAS_YTD [c/ categoria, c/ SCJ]. Uso: python cpt_intoc_periodo.py <base.html>"""
import sys, os, re, json, collections
import pandas as pd
H = sys.argv[1]; B = os.path.dirname(os.path.abspath(__file__)); D = os.path.join(B, "intocaveis", "ytd"); PD = os.path.join(B, "preco")
h = open(H, encoding="utf-8", newline="").read()


def rep(a, b, n=1):
    global h
    if h.count(a) != n and h.count(a.replace("\n", "\r\n")) == n: a, b = a.replace("\n", "\r\n"), b.replace("\n", "\r\n")
    assert h.count(a) == n, (h.count(a), a[:90]); h = h.replace(a, b)


assert "CPT2_INTOC_YTD=" not in h, "já aplicado"
V = collections.defaultdict(dict)
for nm in ("LOCAO200", "KIDS200", "SPRAY170", "ALGUM3", "PAR_LOCAO_KIDS", "PAR_LOCAO_SPRAY", "PAR_KIDS_SPRAY"):
    p = os.path.join(D, nm + ".xlsx"); f = str(pd.read_excel(p, header=None, nrows=1).iloc[0, 0]); assert "YTD Fiscal" in f, (nm, f)
    x = pd.read_excel(p, header=2); x = x[x["Categoria"] == "Repelentes"].fillna(0)
    for r in x.itertuples(index=False):
        k = "|".join((r[2], r[3], r[5], r[4])); V[k][nm] = V[k].get(nm, 0) + int(r[14] or 0)
I = {}
for k, v in V.items():
    a, b, c, u = v.get("LOCAO200", 0), v.get("KIDS200", 0), v.get("SPRAY170", 0), v.get("ALGUM3", 0)
    ab = a + b - v.get("PAR_LOCAO_KIDS", 0); ac = a + c - v.get("PAR_LOCAO_SPRAY", 0); bc = b + c - v.get("PAR_KIDS_SPRAY", 0)
    t = u - a - b - c + ab + ac + bc; d2 = ab + ac + bc - 2 * t
    assert min(ab, ac, bc, t) >= 0 and t <= min(ab, ac, bc), (k, v)
    if u: I[k] = [a, b, c, u, d2, t]
print("Jul–Out intocáveis Brasil [Loção, Kids, Spray, ≥1, ≥2, os 3] =", [sum(x[j] for x in I.values()) for j in range(6)])

RX = re.compile(r"- ([^|]*)/([A-Z]{2})\s*$")
U = collections.defaultdict(set); S2 = collections.defaultdict(set)
for n in (1, 2, 3):
    x = pd.read_excel(os.path.join(PD, f"SCJ_RS_c{n}.xlsx"), header=2)
    for r in x.itertuples(index=False):
        pdv, mes = r[4], r[12]
        if not isinstance(pdv, str) or pd.isna(mes) or int(mes) < 202607: continue
        m = RX.search(pdv)
        if not m: continue
        k = "|".join((m.group(2), str(r[0]), str(r[2]), str(r[1]) if isinstance(r[1], str) else "N/I"))
        if not pd.isna(r[7]) and r[7] > 0: U[k].add(pdv)
        if not pd.isna(r[8]) and r[8] > 0: S2[k].add(pdv)
LY = {k: [len(U[k]), len(S2[k])] for k in sorted(U)}
print("lojas Jul–Out: c/ categoria", sum(v[0] for v in LY.values()), "· c/ SCJ", sum(v[1] for v in LY.values()))
over = [(k, I[k][3], LY.get(k, [0, 0])[1]) for k in I if I[k][3] > LY.get(k, [0, 0])[1]]
print("células com ≥1 intocável > lojas c/ SCJ:", len(over), over[:5])

a = h.index("var CPT2_INTOC=")
h = h[:a] + ("/* intocáveis Jul–Out/26 (IQVIA YTD Fiscal; mesma ordem do CPT2_INTOC) e lojas com venda em algum mês de Jul–Out/26 [c/ categoria, c/ SCJ] */\n"
             "var CPT2_INTOC_YTD=" + json.dumps(I, ensure_ascii=False, separators=(",", ":")) + ";\n"
             "var CPT2_LOJAS_YTD=" + json.dumps(LY, ensure_ascii=False, separators=(",", ":")) + ";\n") + h[a:]
rep("  if(!idx || !idx.length || typeof CPT2_INTOC==='undefined'){ box.innerHTML=''; return; }",
    "  if(!idx || !idx.length || typeof CPT2_INTOC==='undefined'){ box.innerHTML=''; return; }\n"
    "  var mes = (typeof CPT2_FY!=='undefined' && CPT2_FY==='Q2') || typeof CPT2_INTOC_YTD==='undefined';   /* Q2 = Out/26; demais = Jul–Out/26 */\n"
    "  var IN = mes ? CPT2_INTOC : CPT2_INTOC_YTD, LJ = mes ? CPT2_LOJAS : CPT2_LOJAS_YTD, PER = mes ? 'OUT/26' : 'JUL–OUT/26';\n"
    "  var NOTA = mes ? 'lojas com venda no mês' : 'lojas com venda em algum mês de Jul a Out'+((typeof CPT2_FY!=='undefined' && CPT2_FY!=='FY27') ? ' — este período não existe na edição; mostrando Jul–Out' : '');")
rep("var k = all[key], lj = CPT2_LOJAS[key] || [0,0], it = CPT2_INTOC[key] || [0,0,0,0,0,0];",
    "var k = all[key], lj = LJ[key] || [0,0], it = IN[key] || [0,0,0,0,0,0];")
rep("🏆 DISTRIBUIÇÃO DOS INTOCÁVEIS · OUT/26</div>", "🏆 DISTRIBUIÇÃO DOS INTOCÁVEIS · '+PER+'</div>")
rep("DN = lojas com o SKU ÷ lojas com venda da categoria no mês (IQVIA CPT 202610)",
    "DN = lojas com o SKU ÷ '+NOTA+' (IQVIA CPT 202610)")
rep("+T.v[j].toLocaleString('pt-BR')+' de '+T.c.toLocaleString('pt-BR')+' lojas c/ venda</div></div>'; }).join('');",
    "+T.v[j].toLocaleString('pt-BR')+' de '+T.c.toLocaleString('pt-BR')+' lojas c/ venda'+(mes?'':' Jul–Out')+'</div></div>'; }).join('');")
open(H, "w", encoding="utf-8", newline="").write(h); print("ok")
