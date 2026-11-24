"""Share IQVIA no One Page (24/11/2026, 3º ajuste) — igual ao slide 'Share na Araujo – evolução mensal' (One_Page_Perfumaria_Outubro26_v24):
  · Araujo: Total SCJ, OFF! e Exposis de Jan/25 a Set/26 com os valores do slide (IQVIA mês a mês); Out/26 pela edição 202610
  · todos os clientes: faixas 2025 / 2026 no fundo, nome da linha no fim, eixo ajustado aos dados, frase 'SCJ x% em R$, categoria y%'
Uso: python share_visual_slide.py <base.html>"""
import sys, re, json
H = sys.argv[1]; h = open(H, encoding="utf-8", newline="").read()


def rep(a, b, n=1):
    global h
    if h.count(a) != n and h.count(a.replace("\n", "\r\n")) == n: a, b = a.replace("\n", "\r\n"), b.replace("\n", "\r\n")
    assert h.count(a) == n, (h.count(a), a[:90]); h = h.replace(a, b)


assert "fonteSerie" not in h, "já aplicado"
m = re.search(r"var SHARE_IQ\s*=\s*", h); S, k = json.JSONDecoder().raw_decode(h[m.end():]); a, b = m.end(), m.end() + k
TOT = [62.6, 53.5, 56.7, 55.2, 58.7, 60.7, 60.8, 61.8, 55.5, 55.9, 58.3, 62.7, 66.0, 62.1, 65.8, 62.2, 69.9, 66.3, 69.1, 63.7, 66.7]
OFF = [31.0, 24.5, 27.4, 27.2, 27.5, 26.7, 24.1, 26.7, 25.5, 23.6, 26.7, 30.0, 30.0, 31.7, 35.8, 32.8, 42.7, 31.5, 32.7, 31.6, 35.1]
EXP = [31.6, 29.0, 29.3, 28.1, 31.1, 34.0, 36.7, 35.1, 30.0, 32.3, 31.6, 32.7, 36.0, 30.3, 30.0, 29.4, 27.2, 34.8, 36.4, 32.2, 31.6]
A = S["araujo"]
A["tot"] = TOT + [A["tot"][21]]; A["off"] = OFF + [A["off"][21]]; A["exp"] = EXP + [A["exp"][21]]
A["fonteSerie"] = "Jan/25–Set/26: valores mês a mês do One Page Perfumaria Out/26 (IQVIA); Out/26: edição IQVIA 202610"
# SCJ e categoria em R$ no YTD Jan–Out (base CPT2) por cliente
mK = re.search(r"var CPT2_KEYS\s*=\s*", h); K = json.JSONDecoder().raw_decode(h[mK.end():])[0]
mF = re.search(r"var CPT2_FAB_ALL\s*=\s*", h); F = json.JSONDecoder().raw_decode(h[mF.end():])[0]
mC = re.search(r"var CPT2_CAT_ALL\s*=\s*", h); C = json.JSONDecoder().raw_decode(h[mC.end():])[0]
mM = re.search(r"var CPT2_MES_ALL\s*=\s*", h); MES = json.JSONDecoder().raw_decode(h[mM.end():])[0]
BAN = {"saojoao": ["SAO JOAO FARMACIAS"], "nissei": ["NISSEI"], "panvel": ["PANVEL"], "clamed": ["DROGARIA CATARINENSE", "PRECO POPULAR"], "araujo": ["ARAUJO"]}
y26 = [MES.index("Jan/26") + q for q in range(10)]; y25 = [MES.index("Jan/25") + q for q in range(10)]
for cli, bans in BAN.items():
    ix = [i for i, kk in enumerate(K) if kk[2] in bans]
    s = lambda A_, P: sum(A_[i][p] for i in ix for p in P)
    S[cli]["gScj"] = round((s(F, y26) / s(F, y25) - 1) * 100, 1); S[cli]["gCat"] = round((s(C, y26) / s(C, y25) - 1) * 100, 1)
    print(cli, "SCJ", S[cli]["gScj"], "% · categoria", S[cli]["gCat"], "%")
h = h[:a] + json.dumps(S, ensure_ascii=False, separators=(",", ":")) + h[b:]
i = h.index("function iqShareRender(cli){"); j = h.index("function iqShareMontar(){", i)
NOVO = r"""function iqShareRender(cli){
  var D = SHARE_IQ[cli], cv = document.getElementById('iqshare-c-'+cli); if(!D || !cv || typeof Chart==='undefined') return;
  var old = Chart.getChart ? Chart.getChart(cv) : null; if(old) old.destroy();
  var nf = function(v){ return v.toLocaleString('pt-BR',{minimumFractionDigits:1,maximumFractionDigits:1}); };
  var vals = [].concat(D.tot, D.off, D.exp).filter(function(v){ return v!=null; });
  var yMin = Math.max(0, Math.floor((Math.min.apply(null, vals)-6)/10)*10), yMax = Math.min(100, Math.ceil((Math.max.apply(null, vals)+6)/10)*10);
  var faixas = {id:'iqfaixa', beforeDatasetsDraw:function(ch){ var c=ch.ctx, x=ch.scales.x, a=ch.chartArea, w=(x.getPixelForValue(1)-x.getPixelForValue(0))/2; c.save();
    [[0,11,'2025','rgba(148,163,184,0.10)'],[12,SHARE_IQ_MES.length-1,'2026','rgba(99,102,241,0.10)']].forEach(function(f){ var x0=x.getPixelForValue(f[0])-w, x1=x.getPixelForValue(f[1])+w;
      c.fillStyle=f[3]; c.fillRect(x0, a.top, x1-x0, a.bottom-a.top); c.fillStyle='#94A3B8'; c.font='700 13px system-ui,sans-serif'; c.textAlign='center'; c.fillText(f[2], (x0+x1)/2, a.top+16); });
    c.strokeStyle='rgba(148,163,184,0.45)'; c.beginPath(); var xs=x.getPixelForValue(11)+w; c.moveTo(xs,a.top); c.lineTo(xs,a.bottom); c.stroke(); c.restore(); }};
  var rotulos = {id:'iqlbl', afterDatasetsDraw:function(ch){ var c=ch.ctx; c.save(); c.font='700 9.5px system-ui,sans-serif'; c.textAlign='center';
    ch.data.datasets.forEach(function(ds,di){ var m=ch.getDatasetMeta(di); if(m.hidden) return; var last=null;
      m.data.forEach(function(p,i){ var v=ds.data[i]; if(v==null) return; last=p; c.fillStyle=ds.borderColor; c.fillText(nf(v), p.x, p.y+(di===0?-9:(di===1?15:-9))); });
      if(last){ c.textAlign='left'; c.font='700 11px system-ui,sans-serif'; c.fillText(ds.label, last.x+12, last.y+4); c.textAlign='center'; c.font='700 9.5px system-ui,sans-serif'; } }); c.restore(); }};
  new Chart(cv, {type:'line', data:{labels:SHARE_IQ_MES, datasets:[
      {label:'Total SCJ', data:D.tot, borderColor:'#2E2A6B', backgroundColor:'#fff', borderWidth:3.5, pointRadius:3.5, pointBorderWidth:2, tension:0.4, spanGaps:true},
      {label:'OFF!', data:D.off, borderColor:'#F59E0B', backgroundColor:'#fff', borderWidth:3, pointRadius:3.5, pointBorderWidth:2, tension:0.4, spanGaps:false},
      {label:'Exposis', data:D.exp, borderColor:'#7C3AED', backgroundColor:'#fff', borderWidth:3, pointRadius:3.5, pointBorderWidth:2, tension:0.4, spanGaps:false}]},
    options:{responsive:true, maintainAspectRatio:false, animation:false, layout:{padding:{right:70, top:8}},
      plugins:{legend:{display:false}, tooltip:{callbacks:{label:function(c){ return c.dataset.label+': '+(c.raw==null?'sem dado':nf(c.raw)+'%'); }}}},
      scales:{x:{grid:{display:false}, ticks:{font:{size:10}, color:'#64748B', callback:function(v,i){ return SHARE_IQ_MES[i].split('/')[0]; }}},
              y:{min:yMin, max:yMax, ticks:{stepSize:10, font:{size:10}, color:'#64748B', callback:function(v){ return v+'%'; }}, grid:{color:'rgba(148,163,184,0.18)'}}}},
    plugins:[faixas, rotulos]});
  var f = function(v){ return v==null ? 'n/d' : nf(v)+'%'; };
  var pp = function(a){ if(a[0]==null||a[1]==null) return ''; var d=a[0]-a[1]; return '<b style="color:'+(d>=0?'#059669':'#DC2626')+'">'+(d>=0?'+':'−')+nf(Math.abs(d))+' p.p.</b>'; };
  var tile = function(t, cor, a){ return '<div style="border:1px solid #E2E8F0;border-radius:12px;padding:10px 14px;box-shadow:0 1px 4px rgba(15,23,42,0.06);"><div style="display:inline-block;background:'+cor+';color:#fff;font-size:10.5px;font-weight:800;border-radius:7px;padding:4px 16px;letter-spacing:.03em;">'+t+' · YTD OUT/26</div>'
    +'<div style="display:flex;align-items:center;justify-content:space-between;gap:12px;margin-top:8px;"><span style="font-size:26px;font-weight:800;color:'+cor+';">'+f(a[0])+'</span><span style="font-size:11px;color:#475569;text-align:left;">vs '+f(a[1])+' em Out/25<br>'+pp(a)+'</span></div></div>'; };
  var k = document.getElementById('iqshare-k-'+cli); if(k) k.innerHTML = tile('TOTAL SCJ','#2E2A6B',D.ytd.tot) + tile('OFF!','#F59E0B',D.ytd.off) + tile('EXPOSIS','#7C3AED',D.ytd.exp);
  var d = function(a){ return (a[0]!=null&&a[1]!=null) ? a[0]-a[1] : null; }, dO=d(D.ytd.off), dE=d(D.ytd.exp);
  var frase1 = (dO==null||dE==null) ? '' : (Math.abs(dO-dE)<0.5 ? 'OFF! ('+pp(D.ytd.off)+') e Exposis ('+pp(D.ytd.exp)+') andam juntos.' :
     (dO>dE ? 'OFF! '+(dO>=0?'puxa o ganho':'perde menos')+' ('+pp(D.ytd.off)+'); Exposis '+(Math.abs(dE)<1.5?'fica lateral':(dE>=0?'também ganha':'perde'))+' ('+pp(D.ytd.exp)+').'
            : 'Exposis '+(dE>=0?'puxa o ganho':'perde menos')+' ('+pp(D.ytd.exp)+'); OFF! '+(Math.abs(dO)<1.5?'fica lateral':(dO>=0?'também ganha':'perde'))+' ('+pp(D.ytd.off)+').'));
  var g = function(v){ return '<b style="color:'+(v>=0?'#059669':'#DC2626')+'">'+(v>=0?'+':'−')+nf(Math.abs(v))+'%</b>'; }, dT = d(D.ytd.tot);
  var frase2 = (D.gScj==null) ? '' : ((dT!=null&&dT>=0) ? 'O ganho vem dos concorrentes' : 'A perda vai para os concorrentes')+': SCJ '+g(D.gScj)+' em R$ na '+D.nome+', categoria '+g(D.gCat)+' (YTD Jan–Out).';
  var r = document.getElementById('iqshare-r-'+cli);
  if(r) r.innerHTML = frase1 + '<br>' + frase2 + (D.fonteSerie ? '<div style="font-size:10px;color:#94A3B8;margin-top:4px;">'+D.fonteSerie+'.</div>' : '');
}
"""
h = h[:i] + NOVO + h[j:]
rep("+'<div class=\"card-title\">Share na '+SHARE_IQ[cli].nome+' – evolução mensal, Jan/25 a Out/26 (IQVIA)</div>'",
    "+'<div class=\"card-title\" style=\"font-size:17px;color:#2E2A6B;\">Share na '+SHARE_IQ[cli].nome+' – evolução mensal, Jan/25 a Out/26 (IQVIA)</div>'")
rep("+'<div class=\"card-sub\">Share em R$ (CPP) na categoria Repelentes · Total SCJ mês a mês; OFF! e Exposis mês a mês só Jul–Out (a edição IQVIA 202610 não traz os outros meses por marca) · YTD Jan–Out/26 vs Jan–Out/25</div></div></div>'",
    "+'<div class=\"card-sub\">Share em R$ (CPP) na categoria Repelentes · YTD Jan–Out/26 vs Jan–Out/25'+(SHARE_IQ[cli].fonteSerie?'':' · OFF! e Exposis só Jul–Out (a edição IQVIA 202610 não traz os outros meses por marca)')+'</div></div></div>'")
rep("+'<div style=\"position:relative;height:300px;\"><canvas id=\"iqshare-c-'+cli+'\"></canvas></div>'", "+'<div style=\"position:relative;height:330px;\"><canvas id=\"iqshare-c-'+cli+'\"></canvas></div>'")
open(H, "w", encoding="utf-8", newline="").write(h); print("ok")
