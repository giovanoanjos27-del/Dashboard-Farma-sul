"""CPT Clientes: share por marca (OFF/EXPOSIS) comparado só em Jul–Set (meses em que há dado por marca) e
listas dos filtros completadas com as bandeiras/cidades que estão na base mas faltavam nas listas.
Uso: python cpt_marca_julset.py <dashboard.html>"""
import sys, json
H = sys.argv[1]; h = open(H, encoding="utf-8", newline="").read()


def rep(a, b):
    global h
    if h.count(a) != 1 and h.count(a.replace("\n", "\r\n")) == 1: a, b = a.replace("\n", "\r\n"), b.replace("\n", "\r\n")
    assert h.count(a) == 1, (h.count(a), a[:90]); h = h.replace(a, b)


def pega(nome):
    tag = "var " + nome + "="; a = h.index(tag) + len(tag)
    o, n = json.JSONDecoder().raw_decode(h[a:]); return o, a, a + n


def troca(nome, valor):
    global h
    _, a, b = pega(nome); h = h[:a] + json.dumps(valor, ensure_ascii=False, separators=(",", ":")) + h[b:]


# 1) filtro de marca OFF/EXPOSIS/PATO: a janela FY27 fica só nos meses com dado por marca (Jul–Set)
rep("""  var n = cfg.n, p0 = cfg.p0, c0 = cfg.c0;
  var M = cfg.cal""", """  var n = cfg.n, p0 = cfg.p0, c0 = cfg.c0;
  if(CPT2_MARCA_SEL && CPT2_MARCA_SEL !== 'CONC' && CPT2_FY === 'FY27') n = Math.min(n, CPT2_MARCA_POS.length / 2);   /* por marca só há Jul–Set */
  var M = cfg.cal""")

# 2) diagnóstico sem filtro: share de OFF/EXPOSIS sobre a categoria dos mesmos meses (Jul–Set), com rótulo
rep("""    var s = function(x,c){ return c>0 ? x/c*100 : null; };
    var oP=s(o[0],T.cp), oC=s(o[1],T.cc), eP=s(e[0],T.cp), eC=s(e[1],T.cc);
    L.push('🏆 <b>OFF!</b> '""", """    var s = function(x,c){ return c>0 ? x/c*100 : null; }, P = CPT2_MARCA_POS, k = P.length / 2, cm = [0,0];
    idx.forEach(function(i){ var c = CPT2_CAT_ALL[i]; for(var j=0;j<k;j++){ cm[0] += c[P[j]]||0; cm[1] += c[P[k+j]]||0; } });
    var oP=s(o[0],cm[0]), oC=s(o[1],cm[1]), eP=s(e[0],cm[0]), eC=s(e[1],cm[1]);
    L.push('🏆 <span style="color:#64748B;">(Jul–Set)</span> <b>OFF!</b> '""")

# 3) listas dos filtros: bandeiras e cidades que existem na base mas não estavam nas listas
K, _, _ = pega("CPT2_KEYS")
ufc, _, _ = pega("CPT2_UF_CIDADES"); bu, _, _ = pega("CPT2_BAN_UFS"); cb, _, _ = pega("CPT2_CANAL_BANS"); cu, _, _ = pega("CPT2_CANAL_UFS"); ab, _, _ = pega("CPT2_ALL_BAN")
nb, nc = set(), 0
for uf, cid, ban, can in K:
    for d, ch, v in ((ufc, uf, cid), (bu, ban, uf), (cb, can, ban), (cu, can, uf)):
        l = d.setdefault(ch, [])
        if v not in l:
            l.append(v); l.sort()
            if d is ufc: nc += 1
    if ban not in ab: ab.append(ban); nb.add(ban)
ab.sort()
troca("CPT2_UF_CIDADES", ufc); troca("CPT2_BAN_UFS", bu); troca("CPT2_CANAL_BANS", cb); troca("CPT2_CANAL_UFS", cu); troca("CPT2_ALL_BAN", ab)
open(H, "w", encoding="utf-8", newline="").write(h)
print("ok · bandeiras incluídas no filtro:", len(nb), sorted(nb), "· cidades incluídas:", nc)
