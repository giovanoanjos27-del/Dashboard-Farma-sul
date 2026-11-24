"""CPT Clientes › Diagnóstico do filtro: colunas de lojas (c/ venda, c/ SCJ) seguem o Período (24/11/2026):
FY27 Jul–Out/26 (CPT2_LOJAS_YTD) · Q1 Jul–Set/26 (CPT2_LOJAS_Q1) · Q2 Out/26 (CPT2_LOJAS) · 2026 Jan–Out/26 (CPT2_LOJAS_CAL)
· FY26 sem dado loja a loja → Out/26, dito no rótulo. O cadastro estimado (≈) continua calculado pela parte das lojas de Out/26.
Uso: python cpt_diag_lojas_periodo.py <base.html>"""
import sys
H = sys.argv[1]; h = open(H, encoding="utf-8", newline="").read()


def rep(a, b, n=1):
    global h
    if h.count(a) != n and h.count(a.replace("\n", "\r\n")) == n: a, b = a.replace("\n", "\r\n"), b.replace("\n", "\r\n")
    assert h.count(a) == n, (h.count(a), a[:90]); h = h.replace(a, b)


assert "function _cpt2LjPer" not in h, "já aplicado"
rep("function _cpt2RenderDiag(idx){",
    """/* lojas com venda do período escolhido: [mapa UF|Canal|Bandeira|Grupo → [c/ categoria, c/ SCJ], rótulo] */
function _cpt2LjPer(){ var f = (typeof CPT2_FY!=='undefined') ? CPT2_FY : 'FY27', u = function(n){ return typeof window[n]!=='undefined' ? window[n] : null; };
  if(f==='FY27' && u('CPT2_LOJAS_YTD')) return {L:CPT2_LOJAS_YTD, r:'Jul–Out/26'};
  if(f==='Q1' && u('CPT2_LOJAS_Q1')) return {L:CPT2_LOJAS_Q1, r:'Jul–Set/26'};
  if(f==='YTD26' && u('CPT2_LOJAS_CAL')) return {L:CPT2_LOJAS_CAL, r:'Jan–Out/26'};
  return {L:CPT2_LOJAS, r:'Out/26'+(f==='FY26'?' (FY26 sem dado de lojas)':'')}; }
function _cpt2RenderDiag(idx){""")
rep("""  var ljUF = function(o,u){ var t=0; if(typeof CPT2_LOJAS==='undefined') return 0; Object.keys(o.lk).forEach(function(k){ if(k.split('|')[0]===u){ var x=CPT2_LOJAS[k]; if(x) t+=x[0]; } }); return t; };""",
    """  var LJP = (typeof CPT2_LOJAS!=='undefined') ? _cpt2LjPer() : {L:{}, r:''};
  var ljUF = function(o,u){ var t=0; if(typeof CPT2_LOJAS==='undefined') return 0; Object.keys(o.lk).forEach(function(k){ if(k.split('|')[0]===u){ var x=LJP.L[k]; if(x) t+=x[0]; } }); return t; };""")
rep("""  var lj = function(o){ var t=0, s=0; Object.keys(o.lk).forEach(function(k){ var x=CPT2_LOJAS[k]; if(x){ t+=x[0]; s+=x[1]; } }); return [t,s]; };
  var ljTd = function(o){ var x=lj(o), cd=(dimI===2) ? (_cpt2PorBan() ? Math.min(CPT2_CAD_GRUPO[_cpt2BanGrp(o.k)]||0, _cpt2CadGrp(_cpt2BanGrp(o.k), x[0])) : _cpt2CadGrp(o.k, x[0])) : null;""",
    """  var lj = function(o,M){ var t=0, s=0; M=M||LJP.L; Object.keys(o.lk).forEach(function(k){ var x=M[k]; if(x){ t+=x[0]; s+=x[1]; } }); return [t,s]; };
  var ljTd = function(o){ var x=lj(o), xo=lj(o,CPT2_LOJAS), cd=(dimI===2) ? (_cpt2PorBan() ? Math.min(CPT2_CAD_GRUPO[_cpt2BanGrp(o.k)]||0, _cpt2CadGrp(_cpt2BanGrp(o.k), xo[0])) : _cpt2CadGrp(o.k, xo[0])) : null;""")
rep("""      var t=0,s=0; Object.keys(all).forEach(function(k){ var x=CPT2_LOJAS[k]; if(x){ t+=x[0]; s+=x[1]; } }); return t?[t,s]:null; })();""",
    """      var t=0,s=0; Object.keys(all).forEach(function(k){ var x=LJP.L[k]; if(x){ t+=x[0]; s+=x[1]; } }); return t?[t,s]:null; })();""")
rep("""            var t=0,s=0; Object.keys(all).forEach(function(k){ var x=CPT2_LOJAS[k]; if(x){ t+=x[0]; s+=x[1]; } });
            if(t && _cpt2CadSoma(idx)) return chip('Lojas no cadastro IQVIA', _cpt2CadPre()+_cpt2CadSoma(idx).toLocaleString('pt-BR'), '#3b82f6', t.toLocaleString('pt-BR')+' c/ venda no mês · '+s.toLocaleString('pt-BR')+' c/ SCJ');""",
    """            var t=0,s=0; Object.keys(all).forEach(function(k){ var x=LJP.L[k]; if(x){ t+=x[0]; s+=x[1]; } });
            if(t && _cpt2CadSoma(idx)) return chip('Lojas no cadastro IQVIA', _cpt2CadPre()+_cpt2CadSoma(idx).toLocaleString('pt-BR'), '#3b82f6', t.toLocaleString('pt-BR')+' c/ venda '+LJP.r+' · '+s.toLocaleString('pt-BR')+' c/ SCJ');""")
rep("c/ venda = lojas com venda da categoria em Out/26 · c/ SCJ = com venda SCJ", "c/ venda = lojas com venda da categoria em '+LJP.r+' · c/ SCJ = com venda SCJ no mesmo período")
rep("(comLj?th('Lojas'):'')", """(comLj?th('Lojas<br><span style="font-weight:500;text-transform:none;">c/ venda '+LJP.r+'</span>'):'')""")
open(H, "w", encoding="utf-8", newline="").write(h); print("ok")
