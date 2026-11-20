"""Distribuição dos intocáveis acompanha o OL como a tabela de cima: OL regional / Base (_cpt2PorBan) → linhas por cliente do OL
(bandeira), mesmo com o botão 'Grupo econômico'; executivos e sem OL → grupo econômico. Uso: python cpt_intoc_ol.py <base.html>"""
import sys
H = sys.argv[1]; h = open(H, encoding="utf-8", newline="").read()
def rep(a, b, n=1):
    global h
    assert h.count(a) == n, (h.count(a), a[:90]); h = h.replace(a, b)
rep("var dim = _cpt2IntDim, g = {}, T = {c:0, s:0, v:[0,0,0,0,0,0]};",
    "var dim = (_cpt2IntDim==='grp' && typeof _cpt2PorBan==='function' && _cpt2PorBan()) ? 'ban' : _cpt2IntDim, g = {}, T = {c:0, s:0, v:[0,0,0,0,0,0]};   /* OL regional: clientes do OL = bandeiras */")
rep("var btn = function(d,t){ return '<button", "var btn = function(d,t){ var dimB = _cpt2IntDim; return '<button")
rep("'+(dim===d?'#1D6FA8':'rgba(148,163,184,0.45)')+';background:'+(dim===d?'#1D6FA81A':'#FFFFFF')+';color:'+(dim===d?'#1D6FA8':'#475569')+'",
    "'+(dimB===d?'#1D6FA8':'rgba(148,163,184,0.45)')+';background:'+(dimB===d?'#1D6FA81A':'#FFFFFF')+';color:'+(dimB===d?'#1D6FA8':'#475569')+'")
rep("btn('grp','Grupo econômico')", "btn('grp',(typeof _cpt2PorBan==='function' && _cpt2PorBan())?'Cliente do OL':'Grupo econômico')")
rep("th(dim==='uf'?'UF':(dim==='ban'?'Bandeira':'Grupo econômico'),'left')",
    "th(dim==='uf'?'UF':(dim==='ban'?((_cpt2IntDim==='grp')?'Cliente (bandeira)':'Bandeira'):'Grupo econômico'),'left')")
open(H, "w", encoding="utf-8", newline="").write(h); print("ok")
