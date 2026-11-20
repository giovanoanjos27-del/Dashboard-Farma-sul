"""CPT Clientes: análise "Distribuição dos intocáveis" (Out/26) por grupo econômico, bandeira ou UF, respeitando os filtros do CPT.
Fonte: IQVIA CPT 202610 › Análise Bandeira, Período Mês, filtro Apresentação (intocaveis/*.xlsx):
  LOCAO200 = OFF REPELENTE LOC FA 30% D 200.0 ML · KIDS200 = OFF REPELENTE L R K G83ML 200.0 ML ·
  SPRAY170 = OFF REPELENTE SP FAM OF ES 170.0 ML · ALGUM3 = os 3 juntos (lojas com pelo menos 1).
'Qtds. lojas Fabricante' por UF × Canal × Grupo × Bandeira. DN = lojas com o SKU ÷ lojas com venda da categoria (CPT2_LOJAS).
Uso: python cpt_intocaveis.py <base.html>"""
import sys, os, json, collections
import pandas as pd
H = sys.argv[1]; D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "intocaveis")
h = open(H, encoding="utf-8", newline="").read()


def rep(a, b, n=1):
    global h
    if h.count(a) != n and h.count(a.replace("\n", "\r\n")) == n: a, b = a.replace("\n", "\r\n"), b.replace("\n", "\r\n")
    assert h.count(a) == n, (h.count(a), a[:90]); h = h.replace(a, b)


assert "CPT2_INTOC=" not in h, "já aplicado"
L = json.JSONDecoder().raw_decode(h[h.index("var CPT2_LOJAS=") + 15:])[0]
I = collections.defaultdict(lambda: [0, 0, 0, 0])
for j, (fn, txt) in enumerate((("LOCAO200", "LOC FA 30%"), ("KIDS200", "L R K G83ML"), ("SPRAY170", "SP FAM OF ES 170"), ("ALGUM3", " ou "))):
    p = os.path.join(D, fn + ".xlsx"); f = str(pd.read_excel(p, header=None, nrows=1).iloc[0, 0]); assert txt in f, (fn, f)
    x = pd.read_excel(p, header=2); x = x[x["Categoria"] == "Repelentes"].fillna(0)
    for r in x.itertuples(index=False):
        n = int(r[14] or 0)
        if n: I["|".join((r[2], r[3], r[5], r[4]))][j] += n
sem = [k for k in I if k not in L]
tot = [sum(v[j] for v in I.values()) for j in range(4)]
print("células", len(I), "· sem par em CPT2_LOJAS:", len(sem), sum(I[k][3] for k in sem), "lojas · totais", tot)

DADOS = ("/* intocáveis por 'UF|Canal|Bandeira|Grupo' = [lojas com Loção Family 30% 200ml, Loção Kids 200ml, Spray Family Oferta 170ml, "
         "com pelo menos 1] — IQVIA CPT 202610 (Out/26), Análise Bandeira › Apresentação */\nvar CPT2_INTOC=" + json.dumps(I, ensure_ascii=False, separators=(",", ":")) + ";\n")
JS = r"""
var _cpt2IntDim = 'grp';
function _cpt2IntSet(d){ _cpt2IntDim = d; try{ _cpt2RenderIntoc(_cpt2GetIndices()); }catch(e){ console.warn('cpt2 intocáveis', e); } }
function _cpt2RenderIntoc(idx){
  var box = document.getElementById('cpt2-intoc'); if(!box) return;
  if(!idx || !idx.length || typeof CPT2_INTOC==='undefined'){ box.innerHTML=''; return; }
  var all = {}; idx.forEach(function(i){ var k=CPT2_KEYS[i]; all[k[0]+'|'+k[3]+'|'+k[2]+'|'+k[4]] = k; });
  var dim = _cpt2IntDim, g = {}, T = {c:0, s:0, v:[0,0,0,0]};
  Object.keys(all).forEach(function(key){
    var k = all[key], lj = CPT2_LOJAS[key] || [0,0], it = CPT2_INTOC[key] || [0,0,0,0];
    if(!lj[0] && !it[3]) return;
    var nm = dim==='uf' ? k[0] : (dim==='ban' ? k[2] : k[4]);
    var o = g[nm] || (g[nm] = {k:nm, c:0, s:0, v:[0,0,0,0], uf:{}});
    o.c += lj[0]; o.s += lj[1]; for(var j=0;j<4;j++){ o.v[j] += it[j]; T.v[j] += it[j]; } T.c += lj[0]; T.s += lj[1];
    if(dim!=='uf') o.uf[k[0]] = 1;
  });
  var L = Object.keys(g).map(function(x){ return g[x]; }).sort(function(a,b){ return b.c-a.c; });
  var pct = function(n,d){ return d>0 ? n/d*100 : null; };
  var cor = function(p){ return p==null ? '#94A3B8' : (p>=70 ? '#059669' : (p>=40 ? '#D97706' : '#DC2626')); };
  var cel = function(n,d,b){ var p=pct(n,d); return '<td style="padding:5px 10px;text-align:right;white-space:nowrap;border-bottom:0.5px solid rgba(94,153,208,0.18);'+(b?'font-weight:800;':'')+'"><b style="color:'+cor(p)+';">'+(p==null?'—':p.toFixed(1).replace('.',',')+'%')+'</b> <span style="color:#64748B;font-size:10px;">'+n.toLocaleString('pt-BR')+' lj</span></td>'; };
  var td = function(t,al,b){ return '<td style="padding:5px 10px;text-align:'+(al||'right')+';white-space:nowrap;border-bottom:0.5px solid rgba(94,153,208,0.18);color:#0D1B2E;'+(b?'font-weight:800;':'')+'">'+t+'</td>'; };
  var th = function(t,al){ return '<th style="padding:6px 10px;text-align:'+(al||'right')+';font-size:9px;font-weight:700;letter-spacing:0.06em;color:#1D6FA8;text-transform:uppercase;border-bottom:1px solid rgba(94,153,208,0.4);white-space:nowrap;">'+t+'</th>'; };
  var NOMES = ['Loção Family 30% 200ml','Loção Kids 200ml','Spray Family Oferta 170ml','Pelo menos 1 intocável'];
  var btn = function(d,t){ return '<button onclick="_cpt2IntSet(\''+d+'\')" style="padding:4px 10px;border-radius:999px;font-size:10px;font-weight:700;cursor:pointer;border:1px solid rgba(29,111,168,0.45);'+(dim===d?'background:#1D6FA8;color:#FFFFFF;':'background:#FFFFFF;color:#1D6FA8;')+'">'+t+'</button>'; };
  var chips = NOMES.map(function(n,j){ var p=pct(T.v[j],T.c); return '<div style="flex:1 1 150px;background:#FFFFFF;border:1px solid rgba(94,153,208,0.30);border-radius:10px;padding:8px 12px;">'
      +'<div style="font-size:9px;font-weight:700;letter-spacing:0.06em;color:#475569;text-transform:uppercase;">'+n+'</div>'
      +'<div style="font-size:19px;font-weight:800;color:'+cor(p)+';">'+(p==null?'—':p.toFixed(1).replace('.',',')+'%')+'</div>'
      +'<div style="font-size:10px;color:#64748B;">'+T.v[j].toLocaleString('pt-BR')+' de '+T.c.toLocaleString('pt-BR')+' lojas c/ venda</div></div>'; }).join('');
  var max = 60, mostra = window._cpt2IntAll ? L : L.slice(0, max);
  var rows = mostra.map(function(o){
    var ufs = Object.keys(o.uf).sort(); var nm = o.k + (ufs.length ? ' <span style="color:#64748B;font-size:10px;font-weight:500;">'+(ufs.length>4 ? ufs.length+' UFs' : ufs.join(' · '))+'</span>' : '');
    return '<tr>'+td(nm,'left')+td(o.c.toLocaleString('pt-BR'))+td(o.s.toLocaleString('pt-BR'))+cel(o.v[0],o.c)+cel(o.v[1],o.c)+cel(o.v[2],o.c)+cel(o.v[3],o.c,true)+'</tr>'; }).join('');
  box.innerHTML = '<div style="border-top:1px solid rgba(94,153,208,0.30);padding-top:12px;margin-top:14px;">'
    +'<div style="display:flex;justify-content:space-between;align-items:center;gap:10px;flex-wrap:wrap;margin-bottom:8px;">'
      +'<div><div style="font-size:10px;font-weight:800;letter-spacing:0.1em;color:#1D6FA8;">🏆 DISTRIBUIÇÃO DOS INTOCÁVEIS · OUT/26</div>'
      +'<div style="font-size:10px;color:#475569;margin-top:3px;">DN = lojas com o SKU ÷ lojas com venda da categoria no mês (IQVIA CPT 202610) · respeita os filtros acima</div></div>'
      +'<div style="display:flex;gap:6px;">'+btn('grp','Grupo econômico')+btn('ban','Bandeira')+btn('uf','UF')+'</div></div>'
    +'<div style="display:flex;gap:8px;flex-wrap:wrap;margin-bottom:10px;">'+chips+'</div>'
    +'<div style="overflow-x:auto;"><table style="width:100%;border-collapse:collapse;font-size:11px;background:#FFFFFF;">'
      +'<thead><tr>'+th(dim==='uf'?'UF':(dim==='ban'?'Bandeira':'Grupo econômico'),'left')+th('Lojas c/ venda cat.')+th('Lojas c/ SCJ')+th(NOMES[0])+th(NOMES[1])+th(NOMES[2])+th('≥ 1 intocável')+'</tr></thead>'
      +'<tbody>'+rows+'<tr style="background:rgba(29,111,168,0.08);">'+td('Total do filtro ('+L.length+')','left',true)+td(T.c.toLocaleString('pt-BR'),'right',true)+td(T.s.toLocaleString('pt-BR'),'right',true)+cel(T.v[0],T.c,true)+cel(T.v[1],T.c,true)+cel(T.v[2],T.c,true)+cel(T.v[3],T.c,true)+'</tr></tbody></table></div>'
    +(L.length>max ? '<button onclick="window._cpt2IntAll=!window._cpt2IntAll;_cpt2IntSet(_cpt2IntDim)" style="margin-top:6px;padding:4px 10px;border-radius:6px;border:1px solid rgba(29,111,168,0.45);background:#FFFFFF;color:#1D6FA8;font-size:9.5px;font-weight:700;cursor:pointer;">'+(window._cpt2IntAll?'▲ Mostrar só os '+max+' maiores':'▼ Ver todos os '+L.length)+'</button>' : '')
    +'</div>';
}
"""
a = h.index("var CPT2_LOJAS="); h = h[:a] + DADOS + h[a:]
rep("function _cpt2Render(){", JS.strip("\n") + "\nfunction _cpt2Render(){")
rep("  try{ _cpt2RenderDiag(idx); }catch(e){ console.warn('cpt2 diag', e); }\n}",
    "  try{ _cpt2RenderDiag(idx); }catch(e){ console.warn('cpt2 diag', e); }\n  try{ _cpt2RenderIntoc(idx); }catch(e){ console.warn('cpt2 intocáveis', e); }\n}")
rep("    var _dg=document.getElementById('cpt2-diag'); if(_dg) _dg.innerHTML='';",
    "    var _dg=document.getElementById('cpt2-diag'); if(_dg) _dg.innerHTML=''; var _di=document.getElementById('cpt2-intoc'); if(_di) _di.innerHTML='';")
rep('    <div id="cpt2-diag" style="margin-top:14px;"></div>', '    <div id="cpt2-diag" style="margin-top:14px;"></div>\n    <div id="cpt2-intoc"></div>')
open(H, "w", encoding="utf-8", newline="").write(h); print("ok")
