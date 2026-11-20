"""CPT Clientes › Distribuição dos intocáveis: card 'Estoque nas lojas · São João' (portal SJ › Qlik › Indicadores Estoque ›
Detalhes Estoque, por loja × produto). Aparece quando o filtro inclui o Grupo São João; respeita o filtro de UF.
Lojas ativas = sem CD/depósito, sem 'INATIVA'/'FECHADA'; 'trabalham SCJ' = com algum produto SCJ em estoque.
Uso: python cpt_sj_estoque_intoc.py <base.html> <sj_estoque_loja_produto.xlsx> <dd/mm/aaaa>"""
import sys, json
import pandas as pd
H, X, DT = sys.argv[1:4]; h = open(H, encoding="utf-8", newline="").read()
def rep(a, b, n=1):
    global h
    assert h.count(a) == n, (h.count(a), a[:90]); h = h.replace(a, b)

x = pd.read_excel(X); x = x[x["ID Loja"].notna()]
lj = x[~x["Nome Loja"].str.contains(r"\bCD\b|DEP |INATIV|FECHAD", regex=True, na=False) & x["Estado"].isin(["RS", "SC", "PR"])]
SK = ["REPELENTE OFF 200ML FAMILY LOCAO OFERTA ESPECIAL", "REPELENTE OFF KIDS LV200ML PG117ML", "REPELENTE OFF 170ML SPRAY FAMILY OFERTA ESPECIAL"]
tem = [set(lj[(lj["Produto"] == p) & (lj["Qtde. Estoque"] > 0)]["ID Loja"]) for p in SK]
scj = set(lj[lj["Qtde. Estoque"] > 0]["ID Loja"])
lojas = lj.drop_duplicates("ID Loja")[["ID Loja", "Nome Loja", "Estado"]]
UF = {}; FALTA = []
for r in lojas.itertuples(index=False):
    t = [int(r[0] in s) for s in tem]; n = sum(t)
    u = UF.setdefault(r[2], [0] * 9)          # ativas, scj, loc, kids, spr, os3, só2, só1, nenhum (entre as que trabalham SCJ)
    u[0] += 1
    if r[0] in scj:
        u[1] += 1; u[2] += t[0]; u[3] += t[1]; u[4] += t[2]; u[[8, 7, 6, 5][n]] += 1
    if n < 3: FALTA.append([str(r[1]), r[2], t[0], t[1], t[2], int(r[0] in scj)])
FALTA.sort(key=lambda f: (-f[5], sum(f[2:5]), f[1], f[0]))
tot = [sum(v[j] for v in UF.values()) for j in range(9)]
print("UF:", UF, "· total:", tot, "· lojas sem os 3:", len(FALTA))
DADOS = ("/* estoque dos intocáveis por loja · São João (portal SJ › Qlik Indicadores Estoque, " + DT + "): uf = [lojas ativas, c/ SCJ em estoque, "
         "Loção, Kids, Spray, os 3, só 2, só 1, nenhum]; falta = [loja, UF, tem Loção, Kids, Spray, trabalha SCJ] */\n"
         "var CPT2_SJ_ESTQ=" + json.dumps({"data": DT, "uf": UF, "falta": FALTA}, ensure_ascii=False, separators=(",", ":")) + ";\n")
JS = r"""
function _cpt2SjEstqHtml(idx){
  if(typeof CPT2_SJ_ESTQ==='undefined') return '';
  var temSJ = idx.some(function(i){ return CPT2_KEYS[i][4]==='GRUPO SAO JOAO'; }); if(!temSJ) return '';
  var ufs = {}; idx.forEach(function(i){ if(CPT2_KEYS[i][4]==='GRUPO SAO JOAO') ufs[CPT2_KEYS[i][0]]=1; });
  var E = CPT2_SJ_ESTQ, U = Object.keys(E.uf).filter(function(u){ return ufs[u]; }).sort(), T=[0,0,0,0,0,0,0,0,0];
  U.forEach(function(u){ for(var j=0;j<9;j++) T[j]+=E.uf[u][j]; });
  var pc = function(n,d){ return d>0 ? (n/d*100).toFixed(1).replace('.',',')+'%' : '—'; };
  var cor = function(n,d){ var p=d>0?n/d*100:0; return p>=90?'#059669':(p>=70?'#D97706':'#DC2626'); };
  var c = function(n,d){ return '<td style="padding:4px 9px;text-align:right;white-space:nowrap;border-bottom:0.5px solid rgba(94,153,208,0.18);"><b style="color:'+cor(n,d)+';">'+pc(n,d)+'</b> <span style="color:#64748B;font-size:10px;">'+n.toLocaleString('pt-BR')+' lj</span></td>'; };
  var t = function(s,al){ return '<td style="padding:4px 9px;text-align:'+(al||'right')+';white-space:nowrap;border-bottom:0.5px solid rgba(94,153,208,0.18);color:#0D1B2E;">'+s+'</td>'; };
  var th = function(s,al){ return '<th style="padding:5px 9px;text-align:'+(al||'right')+';font-size:9px;font-weight:700;letter-spacing:0.06em;color:#0F766E;text-transform:uppercase;border-bottom:1px solid rgba(15,118,110,0.35);white-space:nowrap;">'+s+'</th>'; };
  var linha = function(nm,v,b){ return '<tr'+(b?' style="background:rgba(15,118,110,0.07);font-weight:800;"':'')+'>'+t(nm,'left')+t(v[0].toLocaleString('pt-BR'))+t(v[1].toLocaleString('pt-BR'))+c(v[2],v[1])+c(v[3],v[1])+c(v[4],v[1])+c(v[5],v[1])+t(v[6]+' · '+v[7]+' · '+v[8])+'</tr>'; };
  var F = E.falta.filter(function(f){ return ufs[f[1]]; });
  var ok = function(x){ return x ? '<span style="color:#059669;">✓</span>' : '<b style="color:#DC2626;">falta</b>'; };
  var lista = F.map(function(f){ return '<tr>'+t(f[0],'left')+t(f[1],'left')+t(ok(f[2]),'center')+t(ok(f[3]),'center')+t(ok(f[4]),'center')+t(f[5]?'':'<span style="color:#94A3B8;">sem SCJ em estoque</span>','left')+'</tr>'; }).join('');
  return '<div style="margin-top:14px;border:1px solid rgba(15,118,110,0.30);border-radius:10px;padding:10px 12px;background:#FFFFFF;">'
    +'<div style="font-size:10px;font-weight:800;letter-spacing:0.1em;color:#0F766E;">📦 ESTOQUE DOS INTOCÁVEIS NAS LOJAS · SÃO JOÃO · '+E.data+'</div>'
    +'<div style="font-size:10px;color:#475569;margin:3px 0 8px;">Portal São João › Qlik › Indicadores Estoque, loja a loja (lojas ativas, sem CD). % sobre as lojas que trabalham SCJ (com algum produto SCJ em estoque). Aqui conta quem <b>tem na prateleira</b>; o painel acima conta quem <b>vendeu</b> (IQVIA).</div>'
    +'<div style="overflow-x:auto;"><table style="width:100%;border-collapse:collapse;font-size:11px;">'
    +'<thead><tr>'+th('UF','left')+th('Lojas ativas')+th('Trabalham SCJ')+th('Loção Family 200 OE')+th('Kids 200 (grátis 117)')+th('Spray Family 170 OE')+th('Os 3 em estoque')+th('Só 2 · só 1 · nenhum')+'</tr></thead><tbody>'
    +U.map(function(u){ return linha(u,E.uf[u]); }).join('')+(U.length>1?linha('Total',T,true):'')+'</tbody></table></div>'
    +(F.length ? '<details style="margin-top:8px;"><summary style="cursor:pointer;font-size:10px;font-weight:700;color:#0F766E;">'+F.length+' lojas sem os 3 em estoque — ver lista</summary>'
      +'<div style="overflow-x:auto;max-height:320px;overflow-y:auto;margin-top:6px;"><table style="width:100%;border-collapse:collapse;font-size:10.5px;"><thead><tr>'+th('Loja','left')+th('UF','left')+th('Loção','center')+th('Kids','center')+th('Spray','center')+th('','left')+'</tr></thead><tbody>'+lista+'</tbody></table></div></details>' : '')
    +'</div>';
}
"""
a = h.index("var CPT2_INTOC="); h = h[:a] + DADOS + h[a:]
rep("function _cpt2RenderIntoc(idx){", JS.strip("\n") + "\nfunction _cpt2RenderIntoc(idx){")
rep("    +(L.length>max ? '<button onclick=\"window._cpt2IntAll=!window._cpt2IntAll;_cpt2IntSet(_cpt2IntDim)\"",
    "    +_cpt2SjEstqHtml(idx)\n    +(L.length>max ? '<button onclick=\"window._cpt2IntAll=!window._cpt2IntAll;_cpt2IntSet(_cpt2IntDim)\"")
open(H, "w", encoding="utf-8", newline="").write(h); print("ok")
