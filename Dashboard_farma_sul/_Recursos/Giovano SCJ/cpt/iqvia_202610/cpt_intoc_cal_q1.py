"""CPT Clientes › Distribuição dos intocáveis por período (24/11/2026):
  · 2026 (YTD26) → Jan–Out/26: 7 exports IQVIA Análise Bandeira, Período = YTD (intocaveis/ytd_cal/*.xlsx) → CPT2_INTOC_CAL;
    lojas c/ categoria e c/ SCJ pelo export sem filtro de Apresentação (TOTAL.xlsx: Qtds. Lojas Total / Qtds. lojas Fabricante) → CPT2_LOJAS_CAL
  · Q1 → colunas de lojas Jul–Set/26 pela Matriz de Lojas loja a loja (preco/SCJ_RS_c*.xlsx, 202607–202609) → CPT2_LOJAS_Q1;
    % dos SKUs seguem Jul–Out/26 (Q1 por SKU não existe na edição 202610), com aviso amarelo
  · FY26 → Jul–Out/26 com aviso amarelo (não existe na edição)
Uso: python cpt_intoc_cal_q1.py <base.html>"""
import sys, os, re, json, collections, warnings
import pandas as pd
warnings.filterwarnings("ignore"); sys.stdout.reconfigure(encoding="utf-8")
H = sys.argv[1]; B = os.path.dirname(os.path.abspath(__file__)); D = os.path.join(B, "intocaveis", "ytd_cal"); PD = os.path.join(B, "preco")
h = open(H, encoding="utf-8", newline="").read()


def rep(a, b, n=1):
    global h
    if h.count(a) != n and h.count(a.replace("\n", "\r\n")) == n: a, b = a.replace("\n", "\r\n"), b.replace("\n", "\r\n")
    assert h.count(a) == n, (h.count(a), a[:90]); h = h.replace(a, b)


assert "CPT2_INTOC_CAL=" not in h, "já aplicado"
key = lambda r: "|".join((str(r[2]), str(r[3]), str(r[5]), str(r[4])))
V = collections.defaultdict(dict)
for nm in ("LOCAO200", "KIDS200", "SPRAY170", "ALGUM3", "PAR_LOCAO_KIDS", "PAR_LOCAO_SPRAY", "PAR_KIDS_SPRAY"):
    p = os.path.join(D, nm + ".xlsx"); f = str(pd.read_excel(p, header=None, nrows=1).iloc[0, 0])
    assert "Tipo de Período é YTD" in f and "YTD Fiscal" not in f, (nm, f)
    x = pd.read_excel(p, header=2); x = x[x["Categoria"] == "Repelentes"].fillna(0)
    for r in x.itertuples(index=False):
        k = key(r); V[k][nm] = V[k].get(nm, 0) + int(r[14] or 0)
I = {}; aj = 0
for k, v in V.items():
    a, b, c, u = v.get("LOCAO200", 0), v.get("KIDS200", 0), v.get("SPRAY170", 0), v.get("ALGUM3", 0)
    ab = a + b - v.get("PAR_LOCAO_KIDS", 0); ac = a + c - v.get("PAR_LOCAO_SPRAY", 0); bc = b + c - v.get("PAR_KIDS_SPRAY", 0)
    t = u - a - b - c + ab + ac + bc; d2 = ab + ac + bc - 2 * t
    if min(ab, ac, bc, t) < 0 or t > min(ab, ac, bc):
        aj += 1; ab, ac, bc = max(ab, 0), max(ac, 0), max(bc, 0); t = max(0, min(t, ab, ac, bc)); d2 = max(0, ab + ac + bc - 2 * t)
    if u: I[k] = [a, b, c, u, d2, t]
x = pd.read_excel(os.path.join(D, "TOTAL.xlsx"), header=2); x = x[x["Categoria"] == "Repelentes"].fillna(0)
LC = collections.defaultdict(lambda: [0, 0])
for r in x.itertuples(index=False):
    k = key(r); LC[k][0] += int(r[15] or 0); LC[k][1] += int(r[14] or 0)
LC = dict(LC)
for k in I:   # lojas nunca abaixo das lojas com algum intocável
    l = LC.setdefault(k, [0, 0]); l[0] = max(l[0], I[k][3]); l[1] = max(l[1], I[k][3])
print("Jan–Out/26 Brasil [Loção, Kids, Spray, ≥1, ≥2, os 3] =", [sum(v[j] for v in I.values()) for j in range(6)],
      "· lojas c/ cat", sum(v[0] for v in LC.values()), "c/ SCJ", sum(v[1] for v in LC.values()), "· células ajustadas", aj)
RX = re.compile(r"- ([^|]*)/([A-Z]{2})\s*$"); U = collections.defaultdict(set); S2 = collections.defaultdict(set)
for n in (1, 2, 3):
    x = pd.read_excel(os.path.join(PD, f"SCJ_RS_c{n}.xlsx"), header=2)
    for r in x.itertuples(index=False):
        pdv, mes = r[4], r[12]
        if not isinstance(pdv, str) or pd.isna(mes) or not 202607 <= int(mes) <= 202609: continue
        m = RX.search(pdv)
        if not m: continue
        k = "|".join((m.group(2), str(r[0]), str(r[2]), str(r[1]) if isinstance(r[1], str) else "N/I"))
        if not pd.isna(r[7]) and r[7] > 0: U[k].add(pdv)
        if not pd.isna(r[8]) and r[8] > 0: S2[k].add(pdv)
LQ = {k: [len(U[k]), len(S2[k])] for k in sorted(U)}
print("Jul–Set/26 lojas c/ cat", sum(v[0] for v in LQ.values()), "· c/ SCJ", sum(v[1] for v in LQ.values()))
a = h.index("var CPT2_INTOC_YTD=")
h = h[:a] + ("/* intocáveis Jan–Out/26 (IQVIA YTD calendário) e lojas [c/ categoria, c/ SCJ] Jan–Out/26; lojas Jul–Set/26 (Matriz de Lojas) para o Q1 */\n"
             "var CPT2_INTOC_CAL=" + json.dumps(I, ensure_ascii=False, separators=(",", ":")) + ";\n"
             "var CPT2_LOJAS_CAL=" + json.dumps(LC, ensure_ascii=False, separators=(",", ":")) + ";\n"
             "var CPT2_LOJAS_Q1=" + json.dumps(LQ, ensure_ascii=False, separators=(",", ":")) + ";\n") + h[a:]
rep("""  var mes = (typeof CPT2_FY!=='undefined' && CPT2_FY==='Q2') || typeof CPT2_INTOC_YTD==='undefined';   /* Q2 = Out/26; demais = Jul–Out/26 */
  var IN = mes ? CPT2_INTOC : CPT2_INTOC_YTD, LJ = mes ? CPT2_LOJAS : CPT2_LOJAS_YTD, PER = mes ? 'OUT/26' : 'JUL–OUT/26', PERt = mes ? 'Out/26' : 'Jul–Out/26';
  var NOTA = mes ? 'lojas com venda no mês' : 'lojas com venda em algum mês de Jul a Out'+((typeof CPT2_FY!=='undefined' && CPT2_FY!=='FY27') ? ' — este período não existe na edição; mostrando Jul–Out' : '');""",
    """  var FYc = (typeof CPT2_FY!=='undefined') ? CPT2_FY : 'FY27';
  var mes = FYc==='Q2' || typeof CPT2_INTOC_YTD==='undefined', cal = FYc==='YTD26' && typeof CPT2_INTOC_CAL!=='undefined', q1 = FYc==='Q1' && typeof CPT2_LOJAS_Q1!=='undefined';   /* Q2 = Out/26 · 2026 = Jan–Out/26 · demais = Jul–Out/26 */
  var IN = mes ? CPT2_INTOC : (cal ? CPT2_INTOC_CAL : CPT2_INTOC_YTD), LJ = mes ? CPT2_LOJAS : (cal ? CPT2_LOJAS_CAL : CPT2_LOJAS_YTD), LJD = q1 ? CPT2_LOJAS_Q1 : LJ;
  var PER = mes ? 'OUT/26' : (cal ? 'JAN–OUT/26' : 'JUL–OUT/26'), PERt = mes ? 'Out/26' : (cal ? 'Jan–Out/26' : 'Jul–Out/26'), PERl = q1 ? 'Jul–Set/26' : PERt;
  var NOTA = mes ? 'lojas com venda no mês' : (cal ? 'lojas com venda em algum mês de Jan a Out' : 'lojas com venda em algum mês de Jul a Out');
  var AVISO = q1 ? '⚠ O Q1 (Jul–Set/26) não existe na IQVIA por SKU (a edição 202610 só tem Out/26, Jul–Out/26 e Jan–Out/26). As colunas de lojas são <b>Jul–Set/26</b>; o % e as lojas de cada SKU são <b>Jul–Out/26</b>, sobre as lojas com venda de Jul–Out.'
    : (FYc==='FY26' ? '⚠ O FY26 (Jul/25–Jun/26) não existe na edição IQVIA 202610 para os intocáveis: o card mostra <b>Jul–Out/26</b>.' : '');""")
rep("    var k = all[key], lj = LJ[key] || [0,0], it = IN[key] || [0,0,0,0,0,0];",
    "    var k = all[key], lj = LJ[key] || [0,0], ljd = LJD[key] || [0,0], it = IN[key] || [0,0,0,0,0,0];")
rep("    if(!lj[0] && !it[3]) return;", "    if(!lj[0] && !it[3] && !ljd[0]) return;")
rep("var o = g[nm] || (g[nm] = {k:nm, c:0, s:0, cad:0, v:[0,0,0,0,0,0], uf:{}});",
    "var o = g[nm] || (g[nm] = {k:nm, c:0, s:0, dc:0, ds:0, cad:0, v:[0,0,0,0,0,0], uf:{}});")
rep("o.c += lj[0]; o.s += lj[1];", "o.c += lj[0]; o.s += lj[1]; o.dc += ljd[0]; o.ds += ljd[1]; T.dc = (T.dc||0) + ljd[0]; T.ds = (T.ds||0) + ljd[1];")
rep("td(o.c.toLocaleString('pt-BR'))+td(o.s.toLocaleString('pt-BR'))", "td(o.dc.toLocaleString('pt-BR'))+td(o.ds.toLocaleString('pt-BR'))")
rep("td(T.c.toLocaleString('pt-BR'),'right',true)+td(T.s.toLocaleString('pt-BR'),'right',true)",
    "td((T.dc||0).toLocaleString('pt-BR'),'right',true)+td((T.ds||0).toLocaleString('pt-BR'),'right',true)")
rep("""th('Lojas c/ venda cat.<br><span style="font-weight:500;text-transform:none;">'+PERt+'</span>')+th('Lojas c/ SCJ<br><span style="font-weight:500;text-transform:none;">'+PERt+'</span>')""",
    """th('Lojas c/ venda cat.<br><span style="font-weight:500;text-transform:none;">'+PERl+'</span>')+th('Lojas c/ SCJ<br><span style="font-weight:500;text-transform:none;">'+PERl+'</span>')""")
rep("""📅 Período filtrado: <b>'+PERt+'</b> — as colunas""", """📅 Período filtrado: <b>'+(q1?'Jul–Set/26 (lojas) · Jul–Out/26 (SKUs)':PERt)+'</b> — as colunas""")
rep("""🏆 DISTRIBUIÇÃO DOS INTOCÁVEIS · DADOS DE '+PER+' (PERÍODO FILTRADO)</div>'""",
    """🏆 DISTRIBUIÇÃO DOS INTOCÁVEIS · DADOS DE '+(q1?'JUL–SET/26 (LOJAS) · JUL–OUT/26 (SKUS)':PER)+' (PERÍODO FILTRADO)</div>'
      +(AVISO?'<div style="margin-top:5px;padding:5px 10px;border-radius:6px;background:#FEF3C7;border:1px solid #F59E0B;font-size:11px;font-weight:600;color:#92400E;">'+AVISO+'</div>':'')""")
rep("' lojas c/ venda'+(mes?'':' Jul–Out')", "' lojas c/ venda'+(mes?'':(cal?' Jan–Out':' Jul–Out'))")
open(H, "w", encoding="utf-8", newline="").write(h); print("ok")
