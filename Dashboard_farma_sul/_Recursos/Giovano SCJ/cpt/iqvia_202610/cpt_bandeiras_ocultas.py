"""CPT Clientes: lista de bandeiras embaixo do grupo fica oculta (<details>); aparece ao passar o mouse (dica) ou ao clicar em 'N bandeiras'.
Uso: python cpt_bandeiras_ocultas.py <base.html>"""
import sys
H = sys.argv[1]; h = open(H, encoding="utf-8", newline="").read()
a = """'<div style="font-size:9.5px;font-weight:500;color:#64748B;margin-top:2px;" title="Bandeiras do grupo no filtro">'+Object.keys(o.bn).sort().join(' · ')+'</div>'"""
b = ("""(function(){ var L=Object.keys(o.bn).sort(), t=L.join(' · '); """
     """return '<details style="margin-top:2px;"><summary title="'+t.replace(/"/g,'&quot;')+'" style="cursor:pointer;font-size:9.5px;font-weight:600;color:#1D6FA8;">'+L.length+' bandeira'+(L.length>1?'s':'')+'</summary>"""
     """<div style="font-size:9.5px;font-weight:500;color:#64748B;margin-top:2px;">'+t+'</div></details>'; })()""")
assert h.count(a) == 1, h.count(a); h = h.replace(a, b)
open(H, "w", encoding="utf-8", newline="").write(h); print("ok")
