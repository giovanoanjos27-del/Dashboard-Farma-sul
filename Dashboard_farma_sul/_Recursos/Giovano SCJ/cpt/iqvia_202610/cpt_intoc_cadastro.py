"""Distribuição dos intocáveis: base da DN escolhível — 'Total de lojas (cadastro IQVIA)' (padrão) ou 'Lojas c/ venda'.
Cadastro por célula UF|Canal|Bandeira|Grupo ≈ cadastro do grupo × lojas c/ venda da célula em Out/26 ÷ lojas c/ venda do grupo em Out/26
(nunca menor que as lojas c/ venda da célula no período). Nova coluna 'Total de lojas'. Uso: python cpt_intoc_cadastro.py <base.html>"""
import sys
H = sys.argv[1]; h = open(H, encoding="utf-8", newline="").read()
def rep(a, b, n=1):
    global h
    assert h.count(a) == n, (h.count(a), a[:90]); h = h.replace(a, b)

rep("var _cpt2IntDim = 'grp', _cpt2IntOrd = 'lojas';",
    "var _cpt2IntDim = 'grp', _cpt2IntOrd = 'lojas', _cpt2IntBase = 'cad';\nfunction _cpt2IntBaseSet(b){ _cpt2IntBase = b; _cpt2IntSet(_cpt2IntDim); }")
rep("g = {}, T = {c:0, s:0, v:[0,0,0,0,0,0]};", "g = {}, T = {c:0, s:0, cad:0, v:[0,0,0,0,0,0]};")
rep("    var o = g[nm] || (g[nm] = {k:nm, c:0, s:0, v:[0,0,0,0,0,0], uf:{}});",
    "    var o = g[nm] || (g[nm] = {k:nm, c:0, s:0, cad:0, v:[0,0,0,0,0,0], uf:{}});\n"
    "    var cg = (typeof CPT2_CAD_GRUPO!=='undefined') ? CPT2_CAD_GRUPO[k[4]] : 0, lt = (typeof _cpt2LjGrp==='function') ? (_cpt2LjGrp()[k[4]]||0) : 0, lo = (CPT2_LOJAS[key]||[0])[0];\n"
    "    var cad = Math.max(lj[0], (cg && lt) ? cg*lo/lt : lj[0]); o.cad += cad; T.cad += cad;   /* cadastro estimado da célula */")
rep("  var p3 = function(o){ return o.c>0 ? o.v[5]/o.c : 0; };",
    "  var CAD = _cpt2IntBase==='cad'; L0 = null;\n  var den = function(o){ return CAD ? Math.round(o.cad) : o.c; };\n  var p3 = function(o){ return den(o)>0 ? o.v[5]/den(o) : 0; };")
rep("var chips = NOMES.map(function(n,j){ if(j===4) return ''; var p=pct(T.v[j],T.c);",
    "var bbtn = function(b,t){ var on=_cpt2IntBase===b; return '<button onclick=\"_cpt2IntBaseSet(\\''+b+'\\')\" style=\"border:1px solid '+(on?'#7C3AED':'rgba(148,163,184,0.45)')+';background:'+(on?'#7C3AED1A':'#FFFFFF')+';color:'+(on?'#7C3AED':'#475569')+';border-radius:14px;padding:3px 11px;font-size:10px;font-weight:700;cursor:pointer;\">'+t+'</button>'; };\n"
    "  var chips = NOMES.map(function(n,j){ if(j===4) return ''; var p=pct(T.v[j],den(T));")
rep("+T.v[j].toLocaleString('pt-BR')+' de '+T.c.toLocaleString('pt-BR')+' lojas c/ venda'+(mes?'':' Jul–Out')+'</div></div>'; }).join('');",
    "+T.v[j].toLocaleString('pt-BR')+' de '+den(T).toLocaleString('pt-BR')+(CAD?' lojas (cadastro IQVIA)':' lojas c/ venda'+(mes?'':' Jul–Out'))+'</div></div>'; }).join('');")
rep("return '<tr>'+td(nm,'left')+td(o.c.toLocaleString('pt-BR'))+td(o.s.toLocaleString('pt-BR'))+cel(o.v[0],o.c)+cel(o.v[1],o.c)+cel(o.v[2],o.c)+cel(o.v[3],o.c)+cel(o.v[4],o.c)+cel(o.v[5],o.c,true)+'</tr>'; }).join('');",
    "var d = den(o); return '<tr>'+td(nm,'left')+td(Math.round(o.cad).toLocaleString('pt-BR'))+td(o.c.toLocaleString('pt-BR'))+td(o.s.toLocaleString('pt-BR'))+cel(o.v[0],d)+cel(o.v[1],d)+cel(o.v[2],d)+cel(o.v[3],d)+cel(o.v[4],d)+cel(o.v[5],d,true)+'</tr>'; }).join('');")
rep("+th('Lojas c/ venda cat.')+th('Lojas c/ SCJ')+", "+th('Total de lojas (cadastro)')+th('Lojas c/ venda cat.')+th('Lojas c/ SCJ')+")
rep("+td(T.c.toLocaleString('pt-BR'),'right',true)+td(T.s.toLocaleString('pt-BR'),'right',true)+cel(T.v[0],T.c,true)+cel(T.v[1],T.c,true)+cel(T.v[2],T.c,true)+cel(T.v[3],T.c,true)+cel(T.v[4],T.c,true)+cel(T.v[5],T.c,true)+'</tr></tbody></table></div>'",
    "+td(Math.round(T.cad).toLocaleString('pt-BR'),'right',true)+td(T.c.toLocaleString('pt-BR'),'right',true)+td(T.s.toLocaleString('pt-BR'),'right',true)+cel(T.v[0],den(T),true)+cel(T.v[1],den(T),true)+cel(T.v[2],den(T),true)+cel(T.v[3],den(T),true)+cel(T.v[4],den(T),true)+cel(T.v[5],den(T),true)+'</tr></tbody></table></div>'")
rep("DN = lojas com o SKU ÷ '+NOTA+' (IQVIA CPT 202610)",
    "DN = lojas com o SKU ÷ '+(CAD?'total de lojas do cadastro IQVIA (com ou sem venda; por bandeira/UF estimado pela parte das lojas do grupo)':NOTA)+' (IQVIA CPT 202610)")
rep("+'<span style=\"font-size:9px;font-weight:700;color:#94A3B8;text-transform:uppercase;margin-left:8px;\">Ordenar</span>'",
    "+'<span style=\"font-size:9px;font-weight:700;color:#94A3B8;text-transform:uppercase;margin-left:8px;\">Base</span>'+bbtn('cad','Total de lojas')+bbtn('venda','Lojas c/ venda')"
    "+'<span style=\"font-size:9px;font-weight:700;color:#94A3B8;text-transform:uppercase;margin-left:8px;\">Ordenar</span>'")
h = h.replace("var CAD = _cpt2IntBase==='cad'; L0 = null;", "var CAD = _cpt2IntBase==='cad';")
open(H, "w", encoding="utf-8", newline="").write(h); print("ok")
