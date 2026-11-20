"""Distribuição dos intocáveis mais clara: coluna 'Média dos 3 SKUs' (média das DNs de Loção, Kids e Spray) e coluna
'Lojas por nº de intocáveis' (barra empilhada nenhum · só 1 · só 2 · os 3, soma 100% da base), no lugar de '≥ 2'.
Só 1 = ≥1 − ≥2 · só 2 = ≥2 − os 3 · nenhum = base − ≥1. Uso: python cpt_intoc_mix.py <base.html>"""
import sys
H = sys.argv[1]; h = open(H, encoding="utf-8", newline="").read()
def rep(a, b, n=1):
    global h
    assert h.count(a) == n, (h.count(a), a[:90]); h = h.replace(a, b)

MIX = r"""  var mix = function(v,d,b){ var n0=Math.max(0,d-v[3]), n1=v[3]-v[4], n2=v[4]-v[5], n3=v[5], P=function(x){ return d>0 ? x/d*100 : 0; };
    var seg = function(x,c,t){ var p=P(x); return p>0 ? '<span title="'+t+': '+x.toLocaleString('pt-BR')+' lojas ('+p.toFixed(1).replace('.',',')+'%)" style="display:inline-block;height:100%;width:'+p+'%;background:'+c+';"></span>' : ''; };
    var lab = function(x){ return P(x).toFixed(0)+'%'; };
    return '<td style="padding:5px 10px;border-bottom:0.5px solid rgba(94,153,208,0.18);min-width:190px;'+(b?'font-weight:800;':'')+'">'
      +'<div style="display:flex;height:9px;border-radius:5px;overflow:hidden;background:#E2E8F0;">'+seg(n0,'#CBD5E1','Nenhum')+seg(n1,'#FCA5A5','Só 1')+seg(n2,'#FCD34D','Só 2')+seg(n3,'#34D399','Os 3')+'</div>'
      +'<div style="font-size:9.5px;color:#64748B;margin-top:2px;white-space:nowrap;">0: '+lab(n0)+' · 1: '+lab(n1)+' · 2: '+lab(n2)+' · <b style="color:#059669;">3: '+lab(n3)+'</b></div></td>'; };
  var med = function(v,d,b){ return cel(Math.round((v[0]+v[1]+v[2])/3), d, b); };
"""
rep("  var td = function(t,al,b){", MIX + "  var td = function(t,al,b){")
rep("+cel(o.v[0],d)+cel(o.v[1],d)+cel(o.v[2],d)+cel(o.v[3],d)+cel(o.v[4],d)+cel(o.v[5],d,true)+'</tr>'; }).join('');",
    "+cel(o.v[0],d)+cel(o.v[1],d)+cel(o.v[2],d)+med(o.v,d)+cel(o.v[3],d)+cel(o.v[5],d,true)+mix(o.v,d)+'</tr>'; }).join('');")
rep("+th(NOMES[2])+th('≥ 1 intocável')+th('≥ 2')+th('Os 3 juntos')+'</tr></thead>'",
    "+th(NOMES[2])+th('Média dos 3 SKUs')+th('≥ 1 intocável')+th('Os 3 juntos')+th('Lojas por nº de intocáveis','left')+'</tr></thead>'")
rep("+cel(T.v[0],den(T),true)+cel(T.v[1],den(T),true)+cel(T.v[2],den(T),true)+cel(T.v[3],den(T),true)+cel(T.v[4],den(T),true)+cel(T.v[5],den(T),true)+'</tr></tbody></table></div>'",
    "+cel(T.v[0],den(T),true)+cel(T.v[1],den(T),true)+cel(T.v[2],den(T),true)+med(T.v,den(T),true)+cel(T.v[3],den(T),true)+cel(T.v[5],den(T),true)+mix(T.v,den(T),true)+'</tr></tbody></table></div>'"
    "+'<div style=\"font-size:10px;color:#475569;margin-top:6px;\">📌 <b>Média dos 3 SKUs</b> = presença média de cada intocável. <b>Os 3 juntos</b> = lojas que têm os três ao mesmo tempo (interseção), por isso é sempre menor ou igual ao menor SKU. "
    "A barra mostra como as lojas se dividem: <span style=\"color:#94A3B8;\">■</span> nenhum · <span style=\"color:#F87171;\">■</span> só 1 · <span style=\"color:#F59E0B;\">■</span> só 2 · <span style=\"color:#10B981;\">■</span> os 3 (soma 100%).</div>'")
open(H, "w", encoding="utf-8", newline="").write(h); print("ok")
