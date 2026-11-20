"""CPT Clientes: cadastro de lojas de cada grupo econômico na base da IQVIA (com ou sem venda), lido do filtro
"Grupo Econômico" do CPT IQVIA edição 202610 (número ao lado de cada grupo), em CPT2_CAD_GRUPO.
O cadastro só existe por grupo (Brasil); aparece na tabela de grupos, no total e no card de lojas quando não há
filtro de região/UF/cidade/canal/OL/bandeira (com esses filtros fica a contagem de lojas com venda no mês).
Uso: python cpt_cadastro_grupo.py <dashboard.html> <cadastro_grupos.tsv>"""
import sys, json
H, T = sys.argv[1:3]; h = open(H, encoding="utf-8", newline="").read()


def rep(a, b, n=1):
    global h
    if h.count(a) != n and h.count(a.replace("\n", "\r\n")) == n: a, b = a.replace("\n", "\r\n"), b.replace("\n", "\r\n")
    assert h.count(a) == n, (h.count(a), a[:90]); h = h.replace(a, b)


G = json.JSONDecoder().raw_decode(h[h.index("var CPT2_ALL_GRUPOS=") + 20:])[0]
rows = [l.rstrip("\n").split("\t") for l in open(T, encoding="utf-8") if l.strip()]
FIX = {"FRANCHISING FARMACIA ACESSO POPULAR": 35, "FRANCHISING FARMACIA BRASIL POUPA LAR": 230,
       "FRANCHISING FARMACIA FARMA OFERTA": 17, "FRANCHISING FARMACIA FARMAE": 13, "DROG. SETE IRMAOS": 5}
cad, sem = {}, []
for g in G:
    if g in FIX: cad[g] = FIX[g]; continue
    ex = [int(c) for n, c in rows if n == g]
    if ex: cad[g] = ex[0]; continue
    pre = sorted(((n, int(c)) for n, c in rows if "?" not in n and len(n) >= 8 and g.startswith(n)), key=lambda x: -len(x[0]))
    if pre: cad[g] = pre[0][1]
    else: sem.append(g)
print("grupos com cadastro:", len(cad), "de", len(G), "· sem (sem lojas em Out/26):", len(sem))

a = h.index("var CPT2_LOJAS="); b = h.index("\n", a)
h = h[:b + 1] + ("/* lojas no cadastro IQVIA por grupo econômico (com ou sem venda; filtro Grupo Econômico do CPT IQVIA 202610) — só Brasil */\n"
                 "var CPT2_CAD_GRUPO=" + json.dumps(cad, ensure_ascii=False, separators=(",", ":")) + ";\n"
                 "function _cpt2CadOk(){ var M=(typeof CPT2_MS!=='undefined')?CPT2_MS:null; return !!M && !M.can.length && !M.ol.length && !M.ban.length && !M.reg.length && !M.uf.length && !M.cid.length; }\n"
                 "function _cpt2CadSoma(idx){ var g={}, t=0; idx.forEach(function(i){ g[CPT2_KEYS[i][4]]=1; }); Object.keys(g).forEach(function(k){ t+=CPT2_CAD_GRUPO[k]||0; }); return t; }\n") + h[b + 1:]

# linha da tabela (grupo): cadastro · c/ venda · c/ SCJ
rep("""  var ljTd = function(o){ var x=lj(o); if(!x[0]) return td('—','right','#94A3B8');
    return td(""", """  var ljTd = function(o){ var x=lj(o), cd=(dimI===2 && _cpt2CadOk()) ? CPT2_CAD_GRUPO[o.k] : null;
    if(cd) return td('<b>'+cd.toLocaleString('pt-BR')+'</b> <span style="color:#64748B;font-size:10px;">cadastro · '+x[0].toLocaleString('pt-BR')+' c/ venda · '+x[1].toLocaleString('pt-BR')+' c/ SCJ</span>','right','#0D1B2E');
    if(!x[0]) return td('—','right','#94A3B8');
    return td(""")
# total da tabela
rep("""      +(comLj?c(lt?('<b>'+lt[0].toLocaleString('pt-BR')+'</b>""",
    """      +(comLj?c((lt && dimI===2 && _cpt2CadOk()) ? ('<b>'+_cpt2CadSoma(idx).toLocaleString('pt-BR')+'</b> <span style="color:#64748B;font-size:10px;font-weight:600;">cadastro · '+lt[0].toLocaleString('pt-BR')+' c/ venda · '+lt[1].toLocaleString('pt-BR')+' c/ SCJ</span>') : lt?('<b>'+lt[0].toLocaleString('pt-BR')+'</b>""")
# card de lojas
rep("""            return t ? chip('CNPJs no filtro', t.toLocaleString('pt-BR'), '#3b82f6', s.toLocaleString('pt-BR')+' c/ venda SCJ ('+Math.round(s/t*100)+'%)') : ''; })()""",
    """            if(t && _cpt2CadOk()) return chip('Lojas no cadastro IQVIA', _cpt2CadSoma(idx).toLocaleString('pt-BR'), '#3b82f6', t.toLocaleString('pt-BR')+' c/ venda no mês · '+s.toLocaleString('pt-BR')+' c/ SCJ');
            return t ? chip('CNPJs no filtro', t.toLocaleString('pt-BR'), '#3b82f6', s.toLocaleString('pt-BR')+' c/ venda SCJ ('+Math.round(s/t*100)+'%)') : ''; })()""")
rep("· CNPJs = lojas IQVIA Out/26 (com venda da categoria · com venda SCJ no mês)</div>",
    "· lojas: cadastro IQVIA do grupo (com ou sem venda, Brasil) · c/ venda = lojas com venda da categoria em Out/26 · c/ SCJ = com venda SCJ</div>")
rep("(comLj?th('CNPJs (lojas)'):'')", "(comLj?th('Lojas'):'')")
open(H, "w", encoding="utf-8", newline="").write(h)
print("ok · cadastro total (grupos da base):", sum(cad.values()))
