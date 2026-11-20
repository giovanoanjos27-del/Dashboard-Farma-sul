"""CPT Clientes › Distribuição dos intocáveis: lojas com 2 ou mais e com os 3 juntos (Out/26).
Exports IQVIA (Análise Bandeira › Apresentação) de cada SKU, dos 3 juntos (≥1) e dos pares (PAR_*), por UF × Canal × Grupo × Bandeira;
interseções por inclusão-exclusão em cada célula: A∩B = A + B − (A ou B); os 3 = (≥1) − A − B − C + A∩B + A∩C + B∩C; ≥2 = soma dos pares − 2 × os 3.
CPT2_INTOC passa a [Loção, Kids, Spray, ≥1, ≥2, os 3]. Painel ganha colunas, cartões e ordenação (lojas · % com os 3).
Uso: python cpt_intoc_os3.py <base.html>"""
import sys, os, json, collections
import pandas as pd
H = sys.argv[1]; D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "intocaveis")
h = open(H, encoding="utf-8", newline="").read()


def rep(a, b, n=1):
    global h
    if h.count(a) != n and h.count(a.replace("\n", "\r\n")) == n: a, b = a.replace("\n", "\r\n"), b.replace("\n", "\r\n")
    assert h.count(a) == n, (h.count(a), a[:90]); h = h.replace(a, b)


V = collections.defaultdict(dict)
for nm, txt in (("LOCAO200", "LOC FA 30%"), ("KIDS200", "L R K G83ML"), ("SPRAY170", "SP FAM OF ES 170"), ("ALGUM3", "LOC FA 30%"),
                ("PAR_LOCAO_KIDS", "G83ML"), ("PAR_LOCAO_SPRAY", "LOC FA 30%"), ("PAR_KIDS_SPRAY", "SP FAM OF ES 170")):
    p = os.path.join(D, nm + ".xlsx"); f = str(pd.read_excel(p, header=None, nrows=1).iloc[0, 0]); assert txt in f, (nm, f)
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
tot = [sum(x[j] for x in I.values()) for j in range(6)]
print("células", len(I), "· Brasil [Loção, Kids, Spray, ≥1, ≥2, os 3] =", tot)

a = h.index("var CPT2_INTOC="); b = a + 15 + json.JSONDecoder().raw_decode(h[a + 15:])[1]
h = h[:a] + "var CPT2_INTOC=" + json.dumps(I, ensure_ascii=False, separators=(",", ":")) + h[b:]
rep("com pelo menos 1] — IQVIA CPT 202610", "com pelo menos 1, com 2 ou mais, com os 3 juntos (inclusão-exclusão dos pares)] — IQVIA CPT 202610")
rep("var _cpt2IntDim = 'grp';", "var _cpt2IntDim = 'grp', _cpt2IntOrd = 'lojas';\nfunction _cpt2IntOrdSet(o){ _cpt2IntOrd = o; _cpt2IntSet(_cpt2IntDim); }")
rep("var dim = _cpt2IntDim, g = {}, T = {c:0, s:0, v:[0,0,0,0]};", "var dim = _cpt2IntDim, g = {}, T = {c:0, s:0, v:[0,0,0,0,0,0]};")
rep("it = CPT2_INTOC[key] || [0,0,0,0];", "it = CPT2_INTOC[key] || [0,0,0,0,0,0];")
rep("var o = g[nm] || (g[nm] = {k:nm, c:0, s:0, v:[0,0,0,0], uf:{}});", "var o = g[nm] || (g[nm] = {k:nm, c:0, s:0, v:[0,0,0,0,0,0], uf:{}});")
rep("for(var j=0;j<4;j++){ o.v[j] += it[j]; T.v[j] += it[j]; }", "for(var j=0;j<6;j++){ o.v[j] += it[j]||0; T.v[j] += it[j]||0; }")
rep("var L = Object.keys(g).map(function(x){ return g[x]; }).sort(function(a,b){ return b.c-a.c; });",
    "var p3 = function(o){ return o.c>0 ? o.v[5]/o.c : 0; };\n"
    "  var L = Object.keys(g).map(function(x){ return g[x]; }).sort(function(a,b){ return _cpt2IntOrd==='os3d' ? (p3(b)-p3(a))||(b.c-a.c) : (_cpt2IntOrd==='os3a' ? (p3(a)-p3(b))||(b.c-a.c) : b.c-a.c); });")
rep("var NOMES = ['Loção Family 30% 200ml','Loção Kids 200ml','Spray Family Oferta 170ml','Pelo menos 1 intocável'];",
    "var NOMES = ['Loção Family 30% 200ml','Loção Kids 200ml','Spray Family Oferta 170ml','Pelo menos 1 intocável','2 ou mais intocáveis','Os 3 intocáveis juntos'];")
rep("var chips = NOMES.map(function(n,j){", "var chips = NOMES.map(function(n,j){ if(j===4) return '';")
rep("+cel(o.v[0],o.c)+cel(o.v[1],o.c)+cel(o.v[2],o.c)+cel(o.v[3],o.c,true)+'</tr>'; }).join('');",
    "+cel(o.v[0],o.c)+cel(o.v[1],o.c)+cel(o.v[2],o.c)+cel(o.v[3],o.c)+cel(o.v[4],o.c)+cel(o.v[5],o.c,true)+'</tr>'; }).join('');")
rep("+th(NOMES[2])+th('≥ 1 intocável')+'</tr></thead>'", "+th(NOMES[2])+th('≥ 1 intocável')+th('≥ 2')+th('Os 3 juntos')+'</tr></thead>'")
rep("+cel(T.v[2],T.c,true)+cel(T.v[3],T.c,true)+'</tr></tbody></table></div>'", "+cel(T.v[2],T.c,true)+cel(T.v[3],T.c,true)+cel(T.v[4],T.c,true)+cel(T.v[5],T.c,true)+'</tr></tbody></table></div>'")
rep("+'<div style=\"display:flex;gap:6px;\">'+btn('grp','Grupo econômico')+btn('ban','Bandeira')+btn('uf','UF')+'</div></div>'",
    "+'<div style=\"display:flex;gap:6px;flex-wrap:wrap;align-items:center;\">'+btn('grp','Grupo econômico')+btn('ban','Bandeira')+btn('uf','UF')"
    "+'<span style=\"font-size:9px;font-weight:700;color:#94A3B8;text-transform:uppercase;margin-left:8px;\">Ordenar</span>'+obtn('lojas','Mais lojas')+obtn('os3d','▲ % com os 3')+obtn('os3a','▼ % com os 3')+'</div></div>'")
rep("var chips = NOMES.map(", "var obtn = function(o,t){ var on=_cpt2IntOrd===o; return '<button onclick=\"_cpt2IntOrdSet(\\''+o+'\\')\" style=\"border:1px solid '+(on?'#059669':'rgba(148,163,184,0.45)')+';background:'+(on?'#0596691A':'#FFFFFF')+';color:'+(on?'#059669':'#475569')+';border-radius:14px;padding:3px 11px;font-size:10px;font-weight:700;cursor:pointer;\">'+t+'</button>'; };\n  var chips = NOMES.map(")
rep("DN = lojas com o SKU ÷ lojas com venda da categoria no mês (IQVIA CPT 202610) · respeita os filtros acima",
    "DN = lojas com o SKU ÷ lojas com venda da categoria no mês (IQVIA CPT 202610) · ≥2 e os 3 juntos por interseção dos exports em pares · respeita os filtros acima")
open(H, "w", encoding="utf-8", newline="").write(h); print("ok")
