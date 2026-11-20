"""Painel dos intocáveis: (1) tira da tabela IQVIA as colunas '≥ 1 intocável', 'Os 3 juntos' e 'Lojas por nº de intocáveis'
(pedido do Giovano; os cartões do topo continuam); (2) card de estoque por loja vale para São João, Nissei, Panvel e Clamed
(CPT2_REDE_ESTQ por grupo econômico: data, fonte, uf, falta), um card por rede presente no filtro.
Uso: python cpt_intoc_redes_card.py <base.html> <intoc_estoque_redes.json>"""
import sys, json
H, J = sys.argv[1:3]; h = open(H, encoding="utf-8", newline="").read()
def rep(a, b, n=1):
    global h
    assert h.count(a) == n, (h.count(a), a[:90]); h = h.replace(a, b)

# (1) colunas fora
rep("+med(o.v,d)+cel(o.v[3],d)+cel(o.v[5],d,true)+mix(o.v,d)+'</tr>'; }).join('');", "+med(o.v,d)+'</tr>'; }).join('');")
rep("+th('Média dos 3 SKUs')+th('≥ 1 intocável')+th('Os 3 juntos')+th('Lojas por nº de intocáveis','left')+'</tr></thead>'", "+th('Média dos 3 SKUs')+'</tr></thead>'")
rep("+med(T.v,den(T),true)+cel(T.v[3],den(T),true)+cel(T.v[5],den(T),true)+mix(T.v,den(T),true)+'</tr></tbody></table></div>'", "+med(T.v,den(T),true)+'</tr></tbody></table></div>'")
a = h.index("+'<div style=\"font-size:10px;color:#475569;margin-top:6px;\">📌 <b>Média dos 3 SKUs</b>"); b = h.index("</div>'", a) + len("</div>'")
h = h[:a] + "+'<div style=\"font-size:10px;color:#475569;margin-top:6px;\">📌 <b>Média dos 3 SKUs</b> = presença média de cada intocável. Pelo menos 1 e os 3 juntos estão nos cartões acima.</div>'" + h[b:]

# (2) dados das 4 redes
a = h.index("var CPT2_SJ_ESTQ="); sj, n = json.JSONDecoder().raw_decode(h[a + 17:]); b = a + 17 + n
sj["fonte"] = "Portal São João › Qlik › Indicadores Estoque (Qtde. Estoque)"
R = {"GRUPO SAO JOAO": sj}; R.update(json.load(open(J, encoding="utf-8")))
h = h[:a] + "var CPT2_REDE_ESTQ=" + json.dumps(R, ensure_ascii=False, separators=(",", ":")) + h[b:]
rep("/* estoque dos intocáveis por loja · São João (portal SJ › Qlik Indicadores Estoque, ", "/* estoque dos intocáveis por loja por rede (último estoque por loja recebido de cada portal; São João Qlik ")
NOMES = {"GRUPO SAO JOAO": "SÃO JOÃO", "GRUPO NISSEI SA": "NISSEI", "GRUPO PANVEL": "PANVEL", "GRUPO CLAMED": "CLAMED"}
rep("function _cpt2SjEstqHtml(idx){\n  if(typeof CPT2_SJ_ESTQ==='undefined') return '';\n  var temSJ = idx.some(function(i){ return CPT2_KEYS[i][4]==='GRUPO SAO JOAO'; }); if(!temSJ) return '';\n  var ufs = {}; idx.forEach(function(i){ if(CPT2_KEYS[i][4]==='GRUPO SAO JOAO') ufs[CPT2_KEYS[i][0]]=1; });\n  var E = CPT2_SJ_ESTQ,",
    "var _CPT2_REDE_NOME = " + json.dumps(NOMES, ensure_ascii=False) + ";\n"
    "function _cpt2SjEstqHtml(idx){\n  if(typeof CPT2_REDE_ESTQ==='undefined') return '';\n"
    "  var gs = {}; idx.forEach(function(i){ var g=CPT2_KEYS[i][4]; if(CPT2_REDE_ESTQ[g]) gs[g]=1; });\n"
    "  return Object.keys(CPT2_REDE_ESTQ).filter(function(g){ return gs[g]; }).map(function(g){ return _cpt2RedeEstqHtml(idx, g); }).join('');\n}\n"
    "function _cpt2RedeEstqHtml(idx, G){\n"
    "  var ufs = {}; idx.forEach(function(i){ if(CPT2_KEYS[i][4]===G) ufs[CPT2_KEYS[i][0]]=1; });\n"
    "  var E = CPT2_REDE_ESTQ[G],")
rep("ESTOQUE DOS INTOCÁVEIS NAS LOJAS · SÃO JOÃO · '+E.data+'", "ESTOQUE DOS INTOCÁVEIS NAS LOJAS · '+(_CPT2_REDE_NOME[G]||G)+' · '+E.data+'")
rep("Portal São João › Qlik › Indicadores Estoque, loja a loja (lojas ativas, sem CD). % sobre as lojas que trabalham SCJ",
    "'+(E.fonte||'')+', loja a loja (sem CD). % sobre as lojas que trabalham SCJ")
rep("U = Object.keys(E.uf).filter(function(u){ return ufs[u]; }).sort()", "U = Object.keys(E.uf).filter(function(u){ return ufs[u] || u==='Todas'; }).sort()")
rep("var F = E.falta.filter(function(f){ return ufs[f[1]]; });", "var F = E.falta.filter(function(f){ return ufs[f[1]] || f[1]==='Todas'; });")
open(H, "w", encoding="utf-8", newline="").write(h); print("ok")
