"""Sell Out › card 'Share na <cliente> — evolução mensal (IQVIA)' em São João, Nissei, Panvel, Clamed e Araujo (24/11/2026).
Fonte IQVIA CPT 202610 (R$ CPP, só Repelentes):
  · Total SCJ mês a mês Jan/25–Out/26 = Demanda Fabricante ÷ Demanda Categoria da base CPT2 (CPT2_FAB_ALL / CPT2_CAT_ALL), pela bandeira
  · OFF! e Exposis mês a mês só Jul–Out/25 e Jul–Out/26 (CPT2_MARCA); demais meses sem dado na edição (fica sem ponto)
  · YTD Jan–Out/26 vs Jan–Out/25: Total pela base; OFF!/Exposis pelos exports Análise Bandeira (Marca, YTD, Ano Anterior) em share_marca_ytd/
Clamed = DROGARIA CATARINENSE + PRECO POPULAR.  Uso: python share_cliente_iqvia.py <base.html>"""
import sys, os, json, warnings
import pandas as pd
warnings.filterwarnings("ignore"); sys.stdout.reconfigure(encoding="utf-8")
H = sys.argv[1]; h = open(H, encoding="utf-8", newline="").read(); D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "share_marca_ytd")


def pega(n):
    import re
    m = re.search(r"var " + n + r"\s*=\s*", h); return json.JSONDecoder().raw_decode(h[m.end():])[0]


def rep(a, b, n=1):
    global h
    if h.count(a) != n and h.count(a.replace("\n", "\r\n")) == n: a, b = a.replace("\n", "\r\n"), b.replace("\n", "\r\n")
    assert h.count(a) == n, (h.count(a), a[:100]); h = h.replace(a, b)


assert "SHARE_IQ" not in h, "já aplicado"
K, F, C, MA, MES = pega("CPT2_KEYS"), pega("CPT2_FAB_ALL"), pega("CPT2_CAT_ALL"), pega("CPT2_MARCA"), pega("CPT2_MES_ALL")
CLI = {"saojoao": ["SAO JOAO FARMACIAS"], "nissei": ["NISSEI"], "panvel": ["PANVEL"], "clamed": ["DROGARIA CATARINENSE", "PRECO POPULAR"], "araujo": ["ARAUJO"]}
NOME = {"saojoao": "São João", "nissei": "Nissei", "panvel": "Panvel", "clamed": "Clamed", "araujo": "Araujo"}
i0, i1 = MES.index("Jan/25"), MES.index("Out/26")
POS_MA = [MES.index(m) for m in ("Jul/25", "Ago/25", "Set/25", "Out/25", "Jul/26", "Ago/26", "Set/26", "Out/26")]
yt = {}
for nm, mk in (("off", "OFF_YTD_AnoAnt"), ("exp", "EXP_YTD_AnoAnt")):
    x = pd.read_excel(os.path.join(D, mk + ".xlsx"), header=2); x = x[x["Categoria"] == "Repelentes"].fillna(0)
    x["cat25"] = x["Demanda Categoria"] / (1 + x["Cresc. Categoria"]); x["fab25"] = x.apply(lambda r: r["Demanda Fabricante"] / (1 + r["Cresc. Fabricante"]) if r["Cresc. Fabricante"] > -1 else 0, axis=1)
    yt[nm] = x
S = {}
for cli, bans in CLI.items():
    ix = [i for i, k in enumerate(K) if k[2] in bans]
    cat = [sum(C[i][p] for i in ix) for p in range(len(MES))]; fab = [sum(F[i][p] for i in ix) for p in range(len(MES))]
    tot = [round(fab[p] / cat[p] * 100, 1) if cat[p] else None for p in range(i0, i1 + 1)]
    mar = {}
    for nm, mk in (("off", "OFF"), ("exp", "EXP")):
        s = [None] * (i1 - i0 + 1)
        for j, p in enumerate(POS_MA):
            v = sum((MA[mk].get(str(i)) or [0] * 8)[j] for i in ix)
            if cat[p]: s[p - i0] = round(v / cat[p] * 100, 1)
        mar[nm] = s
    y26 = [MES.index("Jan/26") + q for q in range(10)]; y25 = [MES.index("Jan/25") + q for q in range(10)]
    ytd = {"tot": [round(sum(fab[p] for p in y26) / sum(cat[p] for p in y26) * 100, 1), round(sum(fab[p] for p in y25) / sum(cat[p] for p in y25) * 100, 1)]}
    for nm in ("off", "exp"):
        x = yt[nm][yt[nm]["Bandeira"].isin(bans)]
        ytd[nm] = [round(x["Demanda Fabricante"].sum() / x["Demanda Categoria"].sum() * 100, 1), round(x["fab25"].sum() / x["cat25"].sum() * 100, 1)] if len(x) else [None, None]
    S[cli] = {"nome": NOME[cli], "tot": tot, "off": mar["off"], "exp": mar["exp"], "ytd": ytd}
    print(f"{cli:8s} YTD Jan–Out/26 vs 25 · Total {ytd['tot']} · OFF! {ytd['off']} · Exposis {ytd['exp']} · Out/26 total {tot[-1]}")
JS = """
/* ═══ Share do cliente na IQVIA (Total SCJ · OFF! · Exposis) — evolução mensal Jan/25–Out/26 + YTD ═══ */
var SHARE_IQ = __DADOS__;
var SHARE_IQ_MES = __MESES__;
function iqShareHtml(cli){
  return '<div class="card full" id="iqshare-card-'+cli+'" style="margin-bottom:14px;">'
    +'<div class="card-header"><div><div style="font-size:10px;font-weight:700;letter-spacing:0.1em;color:#7C3AED;margin-bottom:4px;">IQVIA · MARKET SHARE NO CLIENTE</div>'
    +'<div class="card-title">Share na '+SHARE_IQ[cli].nome+' – evolução mensal, Jan/25 a Out/26 (IQVIA)</div>'
    +'<div class="card-sub">Share em R$ (CPP) na categoria Repelentes · Total SCJ mês a mês; OFF! e Exposis mês a mês só Jul–Out (a edição IQVIA 202610 não traz os outros meses por marca) · YTD Jan–Out/26 vs Jan–Out/25</div></div></div>'
    +'<div style="position:relative;height:300px;"><canvas id="iqshare-c-'+cli+'"></canvas></div>'
    +'<div id="iqshare-k-'+cli+'" style="display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-top:12px;"></div>'
    +'<div id="iqshare-r-'+cli+'" style="margin-top:12px;background:rgba(124,58,237,0.05);border:1px solid rgba(124,58,237,0.18);border-radius:10px;padding:10px 14px;font-size:12px;color:#334155;"></div></div>';
}
function iqShareRender(cli){
  var D = SHARE_IQ[cli], cv = document.getElementById('iqshare-c-'+cli); if(!D || !cv || typeof Chart==='undefined') return;
  var old = Chart.getChart ? Chart.getChart(cv) : null; if(old) old.destroy();
  var lbl = {id:'iqlbl', afterDatasetsDraw:function(ch){ var c=ch.ctx; c.save(); c.font='600 9px system-ui,sans-serif'; c.textAlign='center';
    ch.data.datasets.forEach(function(ds,di){ var m=ch.getDatasetMeta(di); if(m.hidden) return; m.data.forEach(function(p,i){ var v=ds.data[i]; if(v==null) return; c.fillStyle=ds.borderColor; c.fillText(v.toLocaleString('pt-BR',{minimumFractionDigits:1,maximumFractionDigits:1}), p.x, p.y+(di===0?-8:14)); }); }); c.restore(); }};
  new Chart(cv, {type:'line', data:{labels:SHARE_IQ_MES, datasets:[
      {label:'Total SCJ', data:D.tot, borderColor:'#2E2A6B', backgroundColor:'#2E2A6B', borderWidth:3, pointRadius:3, tension:0.35, spanGaps:true},
      {label:'OFF!', data:D.off, borderColor:'#F59E0B', backgroundColor:'#F59E0B', borderWidth:2.5, pointRadius:4, tension:0.3, spanGaps:false},
      {label:'Exposis', data:D.exp, borderColor:'#7C3AED', backgroundColor:'#7C3AED', borderWidth:2.5, pointRadius:4, tension:0.3, spanGaps:false}]},
    options:{responsive:true, maintainAspectRatio:false, animation:false, plugins:{legend:{position:'bottom', labels:{boxWidth:18, font:{size:10}}},
      tooltip:{callbacks:{label:function(c){ return c.dataset.label+': '+(c.raw==null?'sem dado':c.raw.toLocaleString('pt-BR')+'%'); }}}},
      scales:{x:{grid:{display:false}, ticks:{font:{size:9}}}, y:{suggestedMin:0, suggestedMax:80, ticks:{font:{size:9}, callback:function(v){ return v+'%'; }}}}},
    plugins:[lbl]});
  var f = function(v){ return v==null ? 'n/d' : v.toLocaleString('pt-BR',{minimumFractionDigits:1,maximumFractionDigits:1})+'%'; };
  var pp = function(a){ if(a[0]==null||a[1]==null) return ''; var d=a[0]-a[1]; return '<b style="color:'+(d>=0?'#059669':'#DC2626')+'">'+(d>=0?'+':'−')+Math.abs(d).toLocaleString('pt-BR',{minimumFractionDigits:1,maximumFractionDigits:1})+' p.p.</b>'; };
  var tile = function(t, cor, a){ return '<div style="border:1px solid #E2E8F0;border-radius:10px;padding:10px 12px;"><div style="display:inline-block;background:'+cor+';color:#fff;font-size:10px;font-weight:800;border-radius:6px;padding:3px 10px;">'+t+' · YTD OUT/26</div>'
    +'<div style="display:flex;align-items:baseline;gap:12px;margin-top:6px;"><span style="font-size:24px;font-weight:800;color:'+cor+';">'+f(a[0])+'</span><span style="font-size:11px;color:#64748B;">vs '+f(a[1])+' em Out/25<br>'+pp(a)+'</span></div></div>'; };
  var k = document.getElementById('iqshare-k-'+cli); if(k) k.innerHTML = tile('TOTAL SCJ','#2E2A6B',D.ytd.tot) + tile('OFF!','#F59E0B',D.ytd.off) + tile('EXPOSIS','#7C3AED',D.ytd.exp);
  var d = function(a){ return (a[0]!=null&&a[1]!=null) ? a[0]-a[1] : null; }, M = [['OFF!',d(D.ytd.off)],['Exposis',d(D.ytd.exp)]].filter(function(x){ return x[1]!=null; }).sort(function(a,b){ return b[1]-a[1]; });
  var r = document.getElementById('iqshare-r-'+cli);
  if(r) r.innerHTML = 'No YTD Jan–Out/26, a SC Johnson tem <b>'+f(D.ytd.tot[0])+'</b> de share em Repelentes na '+D.nome+' (vs '+f(D.ytd.tot[1])+' em Jan–Out/25, '+pp(D.ytd.tot)+'). '
    + (M.length ? '<b>'+M[0][0]+'</b> é a marca que '+(M[0][1]>=0?'mais ganha':'menos perde')+' share ('+pp(M[0][0]==='OFF!'?D.ytd.off:D.ytd.exp)+')'+(M[1]?'; '+M[1][0]+' '+pp(M[1][0]==='OFF!'?D.ytd.off:D.ytd.exp)+'.':'.') : '');
}
function iqShareMontar(){
  var A = {saojoao:'ed-atrib-slot-sj', nissei:'ed-atrib-slot-nissei', clamed:'ed-atrib-slot-clamed', panvel:'ed-atrib-slot-panvel', araujo:'acum-slot-araujo'};
  Object.keys(A).forEach(function(cli){ var s=document.getElementById(A[cli]); if(!s || document.getElementById('iqshare-card-'+cli)) return;
    var w=document.createElement('div'); w.innerHTML=iqShareHtml(cli); s.parentNode.insertBefore(w.firstChild, s); });
}
(function(){ function ini(){ try{ iqShareMontar(); }catch(e){ console.warn('[iqshare]', e); } } if(document.readyState==='loading') document.addEventListener('DOMContentLoaded', ini); else ini(); })();
"""
JS = JS.replace("__DADOS__", json.dumps(S, ensure_ascii=False, separators=(",", ":"))).replace("__MESES__", json.dumps(MES[i0:i1 + 1], ensure_ascii=False))
rep("var OP1_COB_CLIS = ", JS.strip() + "\nvar OP1_COB_CLIS = ")
rep("""  /* Acumulado FY: renderizar card do cliente ativo */""", """  /* share IQVIA do cliente (Total SCJ · OFF! · Exposis) */
  if(typeof iqShareRender==='function') setTimeout(function(){ try{ iqShareMontar(); iqShareRender(clientId); }catch(e){ console.warn('[iqshare]', e); } }, 700);
  /* Acumulado FY: renderizar card do cliente ativo */""")
open(H, "w", encoding="utf-8", newline="").write(h); print("ok")
