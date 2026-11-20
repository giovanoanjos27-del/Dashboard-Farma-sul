"""CPT Clientes: executivos (GIOVANO, GABI, JOÃO, FERNANDA, KAREN, VINICIUS) listam por grupo econômico;
só OLs regionais (OL ...) e Bases/Espelho listam por bandeira. Uso: python cpt_exec_grupo.py <base.html>"""
import sys
H = sys.argv[1]; h = open(H, encoding="utf-8", newline="").read()
a = "function _cpt2PorBan(){ return (typeof CPT2_MS!=='undefined') && CPT2_MS.ol.length>0; }"
b = ("function _cpt2PorBan(){ return (typeof CPT2_MS!=='undefined') && CPT2_MS.ol.length>0 && "
     "CPT2_MS.ol.every(function(o){ return /^(OL |Base\/)/.test(o); }); }   /* executivos: por grupo econômico */")
assert h.count(a) == 1; h = h.replace(a, b)
open(H, "w", encoding="utf-8", newline="").write(h); print("ok")
