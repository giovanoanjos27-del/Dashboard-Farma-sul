"""Share do One Page (24/11/2026): botão IQVIA | Nielsen no card 'Share no cliente'.
Nielsen não mede rede: a visão Nielsen mostra o share da SCJ (OFF! + Exposis), OFF! e Exposis no mercado da região do cliente,
mês a mês Jan/25–Out/26, da base Nielsen do dashboard (NQ_PR, % valor). YTD Jan–Out pelo valor (v).
Mercados: São João e Panvel = Farma Sul · Nissei = INFC PR · Clamed = INFC SC · Araujo = INFC MG (o do slide).
Uso: python share_nielsen.py <base.html>"""
import sys, re, json
H = sys.argv[1]; h = open(H, encoding="utf-8", newline="").read()


def rep(a, b, n=1):
    global h
    if h.count(a) != n and h.count(a.replace("\n", "\r\n")) == n: a, b = a.replace("\n", "\r\n"), b.replace("\n", "\r\n")
    assert h.count(a) == n, (h.count(a), a[:90]); h = h.replace(a, b)


assert "SHARE_NQ" not in h, "já aplicado"
m = re.search(r"var NQ_PR\s*=\s*", h); NQ = json.JSONDecoder().raw_decode(h[m.end():])[0]; MES = NQ["meses"]
i0, i1 = MES.index("Jan/25"), MES.index("Out/26")
MK = {"saojoao": "Farma Sul", "nissei": "INFC PR", "panvel": "Farma Sul", "clamed": "INFC SC", "araujo": "INFC MG"}
NOME = {"saojoao": "São João", "nissei": "Nissei", "panvel": "Panvel", "clamed": "Clamed", "araujo": "Araujo"}
y26 = [MES.index("Jan/26") + q for q in range(10)]; y25 = [MES.index("Jan/25") + q for q in range(10)]
S = {}
for cli, mk in MK.items():
    d = NQ["mk"][mk]; T, O, E = d["TOTAL MERCADO"], d["OFF!"], d["EXPOSIS"]
    r1 = lambda x: None if x is None else round(x, 1)
    tot = [r1((O["s"][p] or 0) + (E["s"][p] or 0)) for p in range(i0, i1 + 1)]
    sv = lambda b, P: sum(b["v"][p] or 0 for p in P)
    ytd = {"tot": [round((sv(O, y26) + sv(E, y26)) / sv(T, y26) * 100, 1), round((sv(O, y25) + sv(E, y25)) / sv(T, y25) * 100, 1)],
           "off": [round(sv(O, y26) / sv(T, y26) * 100, 1), round(sv(O, y25) / sv(T, y25) * 100, 1)],
           "exp": [round(sv(E, y26) / sv(T, y26) * 100, 1), round(sv(E, y25) / sv(T, y25) * 100, 1)]}
    S[cli] = {"nome": NOME[cli], "mkt": mk, "onde": "no mercado Nielsen " + mk, "tot": tot, "off": [r1(x) for x in O["s"][i0:i1 + 1]], "exp": [r1(x) for x in E["s"][i0:i1 + 1]],
              "ytd": ytd, "gScj": round(((sv(O, y26) + sv(E, y26)) / (sv(O, y25) + sv(E, y25)) - 1) * 100, 1), "gCat": round((sv(T, y26) / sv(T, y25) - 1) * 100, 1),
              "fonteSerie": "Nielsen " + mk + " (% valor) mês a mês; Total SCJ = OFF! + Exposis. Nielsen não mede rede: é o mercado da região do cliente"}
    print(f"{cli:8s} {mk:10s} YTD Total {ytd['tot']} OFF! {ytd['off']} Exposis {ytd['exp']} · SCJ {S[cli]['gScj']}% · categoria {S[cli]['gCat']}%")
# card com botão IQVIA | Nielsen
a = h.index("function iqShareHtml(cli){"); b = h.index("function iqShareRender(cli){", a)
h = h[:a] + r"""var SHARE_NQ = __NQ__;
var iqShareFonte = {};
function iqShareSet(cli, f){ iqShareFonte[cli] = f; iqShareRender(cli); }
function iqShareHtml(cli){
  var bt = function(f, t){ return '<button class="tgl" id="iqshare-b-'+f+'-'+cli+'" onclick="iqShareSet(\''+cli+'\',\''+f+'\')" style="font-size:11px;font-weight:700;padding:5px 14px;">'+t+'</button>'; };
  return '<div class="card full" id="iqshare-card-'+cli+'" style="margin-bottom:14px;">'
    +'<div class="card-header" style="display:flex;justify-content:space-between;align-items:flex-start;gap:12px;flex-wrap:wrap;"><div><div id="iqshare-tag-'+cli+'" style="font-size:10px;font-weight:700;letter-spacing:0.1em;color:#7C3AED;margin-bottom:4px;">IQVIA · MARKET SHARE NO CLIENTE</div>'
    +'<div class="card-title" id="iqshare-t-'+cli+'" style="font-size:17px;color:#2E2A6B;"></div>'
    +'<div class="card-sub" id="iqshare-s-'+cli+'"></div></div>'
    +'<div class="toggle-group" style="display:flex;gap:4px;">'+bt('iq','IQVIA')+bt('nq','Nielsen')+'</div></div>'
    +'<div style="position:relative;height:330px;"><canvas id="iqshare-c-'+cli+'"></canvas></div>'
    +'<div id="iqshare-k-'+cli+'" style="display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-top:12px;"></div>'
    +'<div id="iqshare-r-'+cli+'" style="margin-top:12px;background:rgba(124,58,237,0.05);border:1px solid rgba(124,58,237,0.18);border-radius:10px;padding:10px 14px;font-size:12px;color:#334155;"></div></div>';
}
""".replace("__NQ__", json.dumps(S, ensure_ascii=False, separators=(",", ":"))) + h[b:]
rep("  var D = SHARE_IQ[cli], cv = document.getElementById('iqshare-c-'+cli); if(!D || !cv || typeof Chart==='undefined') return;",
    """  var FN = iqShareFonte[cli] || 'iq', D = (FN==='nq' ? SHARE_NQ : SHARE_IQ)[cli], cv = document.getElementById('iqshare-c-'+cli); if(!D || !cv || typeof Chart==='undefined') return;
  ['iq','nq'].forEach(function(f){ var b=document.getElementById('iqshare-b-'+f+'-'+cli); if(b){ b.classList.toggle('active', f===FN); b.classList.toggle('blue', f===FN); } });
  var _t=document.getElementById('iqshare-t-'+cli), _s=document.getElementById('iqshare-s-'+cli), _g=document.getElementById('iqshare-tag-'+cli);
  if(_g) _g.textContent = FN==='nq' ? 'NIELSEN · MARKET SHARE NO MERCADO DA REGIÃO' : 'IQVIA · MARKET SHARE NO CLIENTE';
  if(_t) _t.textContent = FN==='nq' ? 'Share no mercado '+D.mkt+' – evolução mensal, Jan/25 a Out/26 (Nielsen) · referência para a '+D.nome : 'Share na '+D.nome+' – evolução mensal, Jan/25 a Out/26 (IQVIA)';
  if(_s) _s.textContent = FN==='nq' ? 'Share em valor na categoria Repelentes, mercado Nielsen '+D.mkt+' (o Nielsen não mede rede) · YTD Jan–Out/26 vs Jan–Out/25'
                                    : 'Share em R$ (CPP) na categoria Repelentes · YTD Jan–Out/26 vs Jan–Out/25'+(D.fonteSerie?'':' · OFF! e Exposis só Jul–Out (a edição IQVIA 202610 não traz os outros meses por marca)');""")
rep("em R$ na '+D.nome+', categoria '", "em R$ '+(D.onde||('na '+D.nome))+', categoria '")
rep("op1Sec('Share no cliente – IQVIA')", "op1Sec('Share no cliente – IQVIA · Nielsen')")
open(H, "w", encoding="utf-8", newline="").write(h); print("ok")
