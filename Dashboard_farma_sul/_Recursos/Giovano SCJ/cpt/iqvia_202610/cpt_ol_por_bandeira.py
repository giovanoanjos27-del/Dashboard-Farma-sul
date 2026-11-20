"""CPT Clientes: com filtro de OL (inclusive Base/Espelho), as linhas da tabela são os clientes do OL = bandeiras
(como na lista do Giovano), e não o grupo econômico da IQVIA (que separava a mesma bandeira em N/I, MAXCENTER,
REDE LOUREIRO etc.). Sem filtro de OL continua por grupo econômico. Cadastro da linha-bandeira = cadastro do grupo
principal da bandeira (o de mais lojas), proporcional às lojas da bandeira no filtro.
Uso: python cpt_ol_por_bandeira.py <base.html>"""
import sys
H = sys.argv[1]; h = open(H, encoding="utf-8", newline="").read()


def rep(a, b, n=1):
    global h
    if h.count(a) != n and h.count(a.replace("\n", "\r\n")) == n: a, b = a.replace("\n", "\r\n"), b.replace("\n", "\r\n")
    assert h.count(a) == n, (h.count(a), a[:90]); h = h.replace(a, b)


rep("(CPT2_KEYS[i][4]||_cpt2GrpDe(CPT2_KEYS[i][2]))", "_cpt2LinhaDe(i)", 2)
rep("function _cpt2CadPre(){", """/* com filtro de OL a linha da tabela é a bandeira (cliente do OL); sem OL, o grupo econômico */
function _cpt2PorBan(){ return (typeof CPT2_MS!=='undefined') && CPT2_MS.ol.length>0; }
function _cpt2LinhaDe(i){ var k=CPT2_KEYS[i]; return _cpt2PorBan() ? k[2] : (k[4]||_cpt2GrpDe(k[2])); }
function _cpt2BanGrp(b){ var m=_cpt2BanGrp._m; if(!m){ m=_cpt2BanGrp._m={}; var best={};
  Object.keys(CPT2_LOJAS).forEach(function(k){ var p=k.split('|'), g=p[3]; if(g==='N/I') return; var x=(best[p[2]]=best[p[2]]||{}); x[g]=(x[g]||0)+CPT2_LOJAS[k][0]; });
  Object.keys(best).forEach(function(bb){ var x=best[bb]; m[bb]=Object.keys(x).sort(function(a,c){ return x[c]-x[a]; })[0]; }); }
  return m[b] || b; }
function _cpt2CadPre(){""")
rep("var x=lj(o), cd=(dimI===2) ? _cpt2CadGrp(o.k, x[0]) : null;",
    "var x=lj(o), cd=(dimI===2) ? (_cpt2PorBan() ? Math.min(CPT2_CAD_GRUPO[_cpt2BanGrp(o.k)]||0, _cpt2CadGrp(_cpt2BanGrp(o.k), x[0])) : _cpt2CadGrp(o.k, x[0])) : null;")
rep("th(dimNome==='Cliente'?'Grupo econômico':dimNome,'left')", "th(dimNome==='Cliente'?(_cpt2PorBan()?'Cliente (bandeira)':'Grupo econômico'):dimNome,'left')")
rep("(dimNome==='Cliente'?'Grupos econômicos':dimNome==='UF'?'Estados':'Cidades')+' do filtro",
    "(dimNome==='Cliente'?(_cpt2PorBan()?'Clientes do OL (bandeiras)':'Grupos econômicos'):dimNome==='UF'?'Estados':'Cidades')+' do filtro")
open(H, "w", encoding="utf-8", newline="").write(h); print("ok")
