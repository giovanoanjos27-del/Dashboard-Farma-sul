"""Araujo › One Page no modelo 'One Page SC Johnson & Araújo' (24/11/2026):
  · seletor Total · Perfumaria · Conveniência (abre em Perfumaria, como o One Page da SCJ/JBP)
  · Perfumaria: marcas OFF! e Exposis por SUB CATEGORIA (OFF Loção, OFF Spray…, Kit Exposis somado)
  · meta JBP Perfumaria na linha do Sell-out Total + 'vs Meta YTD' e frase no texto
    Jan–Abr = R$ 3.298.849 (slide One Page Abril/26) rateado pelo desenho do gráfico; Mai ≈ venda Mai/26 ÷ 1,61 (e-mail: +61% vs meta);
    Jun–Dez lidos do gráfico do slide (APROXIMADOS até chegar a planilha do JBP)
Uso: python araujo_setor_jbp.py <base.html>"""
import sys, os, json, collections, warnings
import pandas as pd
warnings.filterwarnings("ignore"); sys.stdout.reconfigure(encoding="utf-8")
H = sys.argv[1]; h = open(H, encoding="utf-8", newline="").read()
A = os.path.dirname(os.path.abspath(__file__)); B = os.path.join(A, "TransferXL-06BCNjgwr5kgG", "BASE SELL OUT ARAUJO-23-24-25-26.xlsx")
M = ['JANEIRO', 'FEVEREIRO', 'MARÇO', 'ABRIL', 'MAIO', 'JUNHO', 'JULHO', 'AGOSTO', 'SETEMBRO', 'OUTUBRO', 'NOVEMBRO', 'DEZEMBRO']


def rep(a, b, n=1):
    global h
    if h.count(a) != n and h.count(a.replace("\n", "\r\n")) == n: a, b = a.replace("\n", "\r\n"), b.replace("\n", "\r\n")
    assert h.count(a) == n, (h.count(a), a[:100]); h = h.replace(a, b)


assert "ARAUJO_SETOR" not in h, "já aplicado"
u = pd.read_excel(B, sheet_name="UND - 23 a 25"); v = pd.read_excel(B, sheet_name="VALOR 23 A 25"); n = pd.read_excel(B, sheet_name="2026"); n = n[n["Ano"] == 2026]
SET = {"perfumaria": "PERFUMARIA", "conveniencia": "CONVENIÊNCIA"}
r2 = lambda x: None if x is None else round(float(x), 2)
SETOR = {}
for k, s in SET.items():
    rec, vol = {}, {}
    for y in (2024, 2025):
        rec[str(y)] = [r2(x) for x in v[(v["ANO"] == y) & (v["SETOR"] == s)][M].sum()]
        vol[str(y)] = [round(float(x)) for x in u[(u["ANO"] == y) & (u["SETOR"] == s)][M].sum()]
    g = n[n["SETOR"] == s].groupby("Mês")[["UND", "VALOR"]].sum()
    rec["2026"] = [r2(g.loc[m, "VALOR"]) if m in g.index else None for m in M]
    vol["2026"] = [round(float(g.loc[m, "UND"])) if m in g.index else None for m in M]
    SETOR[k] = {"rec": rec, "vol": vol}
    print(k, "2025", round(sum(rec["2025"])), "· 2026 Jan–Abr", round(sum(rec["2026"][:4])), "vs", round(sum(rec["2025"][:4])))
# JBP Perfumaria
forma = [1210, 950, 700, 470]; ytd4 = 3298849.0
jbp = [round(ytd4 * f / sum(forma)) for f in forma]
jbp.append(round(SETOR["perfumaria"]["rec"]["2026"][4] / 1.61))
jbp += [145000, 160000, 185000, 340000, 480000, 590000, 1080000]
print("JBP", jbp, "· Jan–Abr", sum(jbp[:4]), "· Jan–Mai", sum(jbp[:5]))
# SO_OP: Perfumaria por sub categoria, Conveniência por SKU
REF = 8
assert '"ref":"Set/26"' in h.replace(" ", "")
v25 = v[v["ANO"] == 2025]; sub = lambda x: "KIT EXPOSIS" if str(x).startswith("KIT EXPOSIS") else str(x)
MAR = lambda m: {"OFF": "OFF!"}.get(str(m).strip().upper(), str(m).strip().upper())
def agrega(d25, d26, chave):
    out = collections.defaultdict(lambda: collections.defaultdict(lambda: [0.0] * 4))
    for _, r in d25.iterrows():
        b = out[MAR(r["MARCA"])][chave(r)]; b[1] += float(r[M[:REF + 1]].sum() or 0); b[3] += float(r[M[REF]] or 0)
    for _, r in d26.iterrows():
        i = M.index(r["Mês"])
        if i <= REF:
            b = out[MAR(r["MARCA"])][chave(r)]; b[0] += float(r["VALOR"] or 0)
            if i == REF: b[2] += float(r["VALOR"] or 0)
    return out
nome = lambda p: " ".join(w.capitalize() for w in str(p).split())
def brands(out, ordem):
    R = []
    for mc in ordem + [m for m in out if m not in ordem]:
        if mc not in out: continue
        sk = [{"n": nome(k), "a26": round(x[0] / 1e3, 1), "a25": round(x[1] / 1e3, 1), "m26": round(x[2] / 1e3, 1), "m25": round(x[3] / 1e3, 1)}
              for k, x in out[mc].items() if x[0] or x[1]]
        if sum(s["a26"] for s in sk) > 0: R.append({"marca": mc, "skus": sorted(sk, key=lambda s: -s["a26"])})
    return R
P = brands(agrega(v25[v25["SETOR"] == "PERFUMARIA"], n[n["SETOR"] == "PERFUMARIA"], lambda r: sub(r["SUB CATEGORIA"])), ["OFF!", "EXPOSIS"])
C = brands(agrega(v25[v25["SETOR"] == "CONVENIÊNCIA"], n[n["SETOR"] == "CONVENIÊNCIA"], lambda r: r["Produto"]), ["RAID", "BAYGON", "LYSOFORM", "GLADE", "PATO", "BRAVO"])
a = h.index("var SO_OP = ") + len("var SO_OP = "); so, k = json.JSONDecoder().raw_decode(h[a:])
est = so["clientes"]["araujo"]["est"]
so["clientes"]["araujo_perf"] = {"metric": "val", "brands": P, "est": [e for e in est if e["marca"] in ("OFF!", "EXPOSIS")], "estRef": so["clientes"]["araujo"].get("estRef")}
so["clientes"]["araujo_conv"] = {"metric": "val", "brands": C, "est": [e for e in est if e["marca"] not in ("OFF!", "EXPOSIS")], "estRef": so["clientes"]["araujo"].get("estRef")}
h = h[:a] + json.dumps(so, ensure_ascii=False, separators=(",", ":")) + h[a + k:]
# dados + estado do seletor
rep("/* Araujo: estoque por loja 29/05/26 (DADO ARAUJO 29-05) × venda Mai/26 */",
    "/* Araujo por setor (Perfumaria = repelentes OFF!/Exposis · Conveniência = Raid, Baygon, Lysoform, Glade, Pato, Bravo) e meta JBP Perfumaria */\n"
    "var ARAUJO_SETOR = " + json.dumps(SETOR, separators=(",", ":")) + ";\n"
    "var ARAUJO_JBP = {perfumaria:" + json.dumps(jbp) + ", fonte:'Jan–Abr R$ 3.298.849 (One Page Abril/26) · Mai pelo e-mail (+61% vs meta) · Jun–Dez aproximados do gráfico do JBP'};\n"
    "var araSetor = 'perfumaria';\n"
    "function setAraSetor(s, btn){ araSetor = s; var r=document.getElementById('ara-setor-row'); if(r) r.querySelectorAll('.stab').forEach(function(b){ b.classList.toggle('active', b===btn); }); if(typeof op1Render==='function') op1Render(); }\n"
    "/* Araujo: estoque por loja 29/05/26 (DADO ARAUJO 29-05) × venda Mai/26 */")
# seletor no topo do Sell Out
rep("    <!-- Filtro compradora SJ — inline com CLIENTE, visível só quando SJ ativo -->",
    """    <!-- Setor Araujo — visível só com Araujo (One Page) -->
    <div id="ara-setor-row" style="display:none;align-items:center;gap:4px;border-left:2px solid rgba(94,153,208,0.55);padding-left:12px;margin-left:4px;">
      <button class="stab" onclick="setAraSetor('total',this)">Araujo Total</button>
      <button class="stab active" onclick="setAraSetor('perfumaria',this)">Perfumaria</button>
      <button class="stab" onclick="setAraSetor('conveniencia',this)">Conveniência</button>
    </div>
    <!-- Filtro compradora SJ — inline com CLIENTE, visível só quando SJ ativo -->""")
rep("""  var _nsRow = document.getElementById('ns-compradora-row');""",
    """  var _araRow = document.getElementById('ara-setor-row'); if(_araRow) _araRow.style.display = clientId==='araujo' ? 'flex' : 'none';
  var _nsRow = document.getElementById('ns-compradora-row');""")
# One Page: contexto por setor + JBP
rep("""    var kmap = {clamed:'cl-kpis', panvel:'pv-kpis', ddgam:'gam-kpis', ddgaucha:'gch-kpis', ddriomed:'rio-kpis', araujo:'ara-kpis'};
    var s = S[kmap[cli]] || {}; rec = s.rec; vol = s.vol;
  }""", """    var kmap = {clamed:'cl-kpis', panvel:'pv-kpis', ddgam:'gam-kpis', ddgaucha:'gch-kpis', ddriomed:'rio-kpis', araujo:'ara-kpis'};
    var s = S[kmap[cli]] || {}; rec = s.rec; vol = s.vol;
    if(cli==='araujo' && typeof ARAUJO_SETOR!=='undefined'){
      sub = (typeof araSetor!=='undefined') ? araSetor : 'total';
      if(sub!=='total' && ARAUJO_SETOR[sub]){ rec = ARAUJO_SETOR[sub].rec; vol = ARAUJO_SETOR[sub].vol; opk = sub==='perfumaria' ? 'araujo_perf' : 'araujo_conv'; subNome = sub==='perfumaria' ? 'Perfumaria' : 'Conveniência'; }
      else subNome = 'Total';
    }
  }""")
rep("""  return {cli:cli, sub:sub, nome:OP1_NOME[cli]||cli, subNome:subNome, M:metric==='val'?rec:vol, metric:metric,""",
    """  var jbp = (cli==='araujo' && sub==='perfumaria' && metric==='val' && typeof ARAUJO_JBP!=='undefined') ? ARAUJO_JBP.perfumaria : null;
  return {cli:cli, sub:sub, nome:OP1_NOME[cli]||cli, subNome:subNome, M:metric==='val'?rec:vol, metric:metric, jbp:jbp,""")
rep("(X.cli==='saojoao'?'compradora ':'comprador ')+X.subNome", "(X.cli==='saojoao'?'compradora ':X.cli==='araujo'?'setor ':'comprador ')+X.subNome")
rep("""       + '<div class="op1-mb"><div class="op1-ml">Ano proj. vs 2025</div><div class="op1-mv" style="color:'+op1Cor(gAno)+'">'+op1Pct(gAno)+'</div><div class="op1-ms">ritmo do YTD</div></div></div></div>'""",
    """       + '<div class="op1-mb"><div class="op1-ml">Ano proj. vs 2025</div><div class="op1-mv" style="color:'+op1Cor(gAno)+'">'+op1Pct(gAno)+'</div><div class="op1-ms">ritmo do YTD</div></div>'
       + (X.jbp ? '<div class="op1-mb"><div class="op1-ml">vs Meta JBP YTD</div><div class="op1-mv" style="color:'+op1Cor(gJ)+'">'+op1Pct(gJ)+'</div><div class="op1-ms">meta '+op1Val('val',jY)+'</div></div>' : '')
       + '</div></div>'""")
rep("""  var titulo = 'One Page SC Johnson & '+X.nome""", """  var jY = 0; if(X.jbp){ for(var _j=0;_j<=last;_j++) jY += X.jbp[_j]||0; } var gJ = (X.jbp && jY>0) ? ytd26/jY-1 : null, gJm = (X.jbp && X.jbp[last]>0) ? a26[last]/X.jbp[last]-1 : null;
  var titulo = 'One Page SC Johnson & '+X.nome""")
rep("""  if(parc){ var _p25 = a25[parc.i]; tTxt +=""", """  if(X.jbp) tTxt += ' Frente ao <b>target JBP</b>, a variação no YTD é de <b style="color:'+op1Cor(gJ)+'">'+op1Pct(gJ)+'</b> ('+(ytd26-jY<0?'gap de ':'acima em ')+'<b>'+op1Val('val',ytd26-jY)+'</b>)'+(gJm!=null?'; em '+OP1_MESX[mRef]+', <b style="color:'+op1Cor(gJm)+'">'+op1Pct(gJm,0)+'</b> vs JBP':'')+'. <span style="color:#94A3B8;font-size:10px;">Meta: '+ARAUJO_JBP.fonte+'.</span>';
  if(parc){ var _p25 = a25[parc.i]; tTxt +=""")
rep("""      {label:'Projeção 2026', data:proj, borderColor:OP1_C.y26, borderDash:[6,5], borderWidth:2.5, pointRadius:function(c){return c.dataIndex>last?4:0;}, pointBackgroundColor:'#fff', pointBorderColor:OP1_C.y26, tension:0.35}
    ].concat(""", """      {label:'Projeção 2026', data:proj, borderColor:OP1_C.y26, borderDash:[6,5], borderWidth:2.5, pointRadius:function(c){return c.dataIndex>last?4:0;}, pointBackgroundColor:'#fff', pointBorderColor:OP1_C.y26, tension:0.35}
    ].concat(X.jbp ? [{label:'JBP', data:X.jbp, borderColor:'#F59E0B', backgroundColor:'#F59E0B', borderDash:[2,3], borderWidth:2.5, pointRadius:0, tension:0.35}] : []).concat(""")
# cobertura por loja segue o setor
rep("""  if(X.cli==='nissei' && X.sub && X.sub!=='total'){ var kp = X.sub==='andre'""",
    """  if(X.cli==='araujo' && X.sub && X.sub!=='total'){ it = it.filter(function(x){ var p = x.m==='OFF!' || x.m==='EXPOSIS'; return X.sub==='perfumaria' ? p : !p; }); }
  if(X.cli==='nissei' && X.sub && X.sub!=='total'){ var kp = X.sub==='andre'""")
open(H, "w", encoding="utf-8", newline="").write(h); print("ok · Perfumaria", [(b["marca"], [s["n"] for s in b["skus"]][:4]) for b in P])
