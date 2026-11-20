"""CPT Clientes: cadastro IQVIA do grupo aparece também com filtro de região/UF/cidade/canal/OL/bandeira.
O cadastro só existe por grupo (Brasil); com filtro ele é estimado (≈) pela parte das lojas com venda do grupo que
está no filtro: cadastro × lojas c/ venda no filtro ÷ lojas c/ venda do grupo no Brasil.
Uso: python cpt_cadastro_filtro.py <dashboard.html>"""
import sys
H = sys.argv[1]; h = open(H, encoding="utf-8", newline="").read()


def rep(a, b, n=1):
    global h
    if h.count(a) != n and h.count(a.replace("\n", "\r\n")) == n: a, b = a.replace("\n", "\r\n"), b.replace("\n", "\r\n")
    assert h.count(a) == n, (h.count(a), a[:90]); h = h.replace(a, b)


rep("function _cpt2CadSoma(idx){ var g={}, t=0; idx.forEach(function(i){ g[CPT2_KEYS[i][4]]=1; }); Object.keys(g).forEach(function(k){ t+=CPT2_CAD_GRUPO[k]||0; }); return t; }",
    "function _cpt2LjGrp(){ if(_cpt2LjGrp._t) return _cpt2LjGrp._t; var t={}; Object.keys(CPT2_LOJAS).forEach(function(k){ var g=k.split('|')[3]; t[g]=(t[g]||0)+CPT2_LOJAS[k][0]; }); return (_cpt2LjGrp._t=t); }\n"
    "/* cadastro do grupo no filtro: exato sem filtro geográfico/canal/OL/bandeira; com filtro ≈ cadastro × lojas c/ venda no filtro ÷ lojas c/ venda do grupo */\n"
    "function _cpt2CadGrp(g, ljF){ var c=CPT2_CAD_GRUPO[g]; if(!c) return 0; if(_cpt2CadOk()) return c; var t=_cpt2LjGrp()[g]||0; return t ? Math.round(c*ljF/t) : 0; }\n"
    "function _cpt2CadSoma(idx){ var all={}, lg={}, s=0; idx.forEach(function(i){ var k=CPT2_KEYS[i]; all[k[0]+'|'+k[3]+'|'+k[2]+'|'+k[4]]=k[4]; });\n"
    "  Object.keys(all).forEach(function(k){ var x=CPT2_LOJAS[k]; if(x) lg[all[k]]=(lg[all[k]]||0)+x[0]; });\n"
    "  var g={}; idx.forEach(function(i){ g[CPT2_KEYS[i][4]]=1; }); Object.keys(g).forEach(function(k){ s+=_cpt2CadGrp(k, lg[k]||0); }); return s; }\n"
    "function _cpt2CadPre(){ return _cpt2CadOk() ? '' : '≈ '; }")
rep("var x=lj(o), cd=(dimI===2 && _cpt2CadOk()) ? CPT2_CAD_GRUPO[o.k] : null;\n    if(cd) return td('<b>'+cd.toLocaleString('pt-BR')+'</b>",
    "var x=lj(o), cd=(dimI===2) ? _cpt2CadGrp(o.k, x[0]) : null;\n    if(cd) return td('<b>'+_cpt2CadPre()+cd.toLocaleString('pt-BR')+'</b>")
rep("c((lt && dimI===2 && _cpt2CadOk()) ? ('<b>'+_cpt2CadSoma(idx).toLocaleString('pt-BR')+'</b>",
    "c((lt && dimI===2 && _cpt2CadSoma(idx)) ? ('<b>'+_cpt2CadPre()+_cpt2CadSoma(idx).toLocaleString('pt-BR')+'</b>")
rep("if(t && _cpt2CadOk()) return chip('Lojas no cadastro IQVIA', _cpt2CadSoma(idx).toLocaleString('pt-BR'),",
    "if(t && _cpt2CadSoma(idx)) return chip('Lojas no cadastro IQVIA', _cpt2CadPre()+_cpt2CadSoma(idx).toLocaleString('pt-BR'),")
rep("· lojas: cadastro IQVIA do grupo (com ou sem venda, Brasil) ·",
    "· lojas: cadastro IQVIA do grupo (com ou sem venda; ≈ = estimado no filtro pela parte das lojas com venda do grupo) ·")
open(H, "w", encoding="utf-8", newline="").write(h); print("ok")
