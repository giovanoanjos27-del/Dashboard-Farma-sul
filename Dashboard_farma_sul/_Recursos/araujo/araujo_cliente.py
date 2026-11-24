"""Sell Out › novo cliente Araujo (MG) — 24/11/2026. Mesmo painel do DD-Riomed (KPIs, evolução mensal e comparação,
acumulado FY, receita por ano, estoque e ruptura, sell-out por marca e DOH do One Page, donut/ranking de SKUs, tabela mensal),
com os dados da Araujo:
  · venda mensal un e R$ por SKU: BASE SELL OUT ARAUJO-23-24-25-26.xlsx (abas 'UND - 23 a 25', 'VALOR 23 A 25' e '2026' = Jan–Out/26)
  · estoque 29/05/2026: DADO ARAUJO 29-05.xlsx (ESTOQUE LOJA somado por SKU + ESTOQUE CD) × venda Mai/26
Uso: python araujo_cliente.py <base.html>"""
import sys, os, re, json, collections, warnings
import pandas as pd
warnings.filterwarnings("ignore"); sys.stdout.reconfigure(encoding="utf-8")
H = sys.argv[1]; h = open(H, encoding="utf-8", newline="").read()
A = os.path.dirname(os.path.abspath(__file__)); B = os.path.join(A, "TransferXL-06BCNjgwr5kgG", "BASE SELL OUT ARAUJO-23-24-25-26.xlsx")
M = ['JANEIRO', 'FEVEREIRO', 'MARÇO', 'ABRIL', 'MAIO', 'JUNHO', 'JULHO', 'AGOSTO', 'SETEMBRO', 'OUTUBRO', 'NOVEMBRO', 'DEZEMBRO']


def rep(a, b, n=1):
    global h
    if h.count(a) != n and h.count(a.replace("\n", "\r\n")) == n: a, b = a.replace("\n", "\r\n"), b.replace("\n", "\r\n")
    assert h.count(a) == n, (h.count(a), a[:100]); h = h.replace(a, b)


assert "sellout-content-araujo" not in h, "já aplicado"
MARCA = lambda m: {"OFF": "OFF!"}.get(str(m).strip().upper(), str(m).strip().upper())
nome = lambda p: " ".join(w.capitalize() if not re.match(r"^\d", w) else w.lower() for w in str(p).split())
# ── venda mensal ──
u = pd.read_excel(B, sheet_name="UND - 23 a 25"); v = pd.read_excel(B, sheet_name="VALOR 23 A 25"); n26 = pd.read_excel(B, sheet_name="2026")
u = u[u["ANO"].isin([2023, 2024, 2025])]; v = v[v["ANO"].isin([2023, 2024, 2025])]; n26 = n26[n26["Ano"] == 2026]
VOL = {y: [round(float(x)) for x in u[u["ANO"] == y][M].sum()] for y in (2023, 2024, 2025)}
REC = {y: [round(float(x), 2) for x in v[v["ANO"] == y][M].sum()] for y in (2023, 2024, 2025)}
g26 = n26.groupby("Mês")[["UND", "VALOR"]].sum()
VOL[2026] = [round(float(g26.loc[m, "UND"])) if m in g26.index else None for m in M]
REC[2026] = [round(float(g26.loc[m, "VALOR"]), 2) if m in g26.index else None for m in M]
for y in (2023, 2024, 2025, 2026): print(y, "un", sum(x or 0 for x in VOL[y]), "R$", round(sum(x or 0 for x in REC[y])))
# ── SKU: 2025 e 2026 por mês (R$) ──
sk25 = v[v["ANO"] == 2025].assign(MARCA=lambda d: d["MARCA"].map(MARCA)).groupby(["Cód Produto DV", "Produto", "MARCA"])[M].sum()
n26m = n26.assign(MARCA=n26["MARCA"].map(MARCA))
sk26v = n26m.pivot_table(index=["Cód Produto DV", "Produto", "MARCA"], columns="Mês", values="VALOR", aggfunc="sum").reindex(columns=M).fillna(0)
sk26u = n26m.pivot_table(index=["Cód Produto DV", "Produto", "MARCA"], columns="Mês", values="UND", aggfunc="sum").reindex(columns=M).fillna(0)
REF = 8   # SO_OP.ref = Set/26 → YTD Jan–Set e mês Set (mesma referência dos outros clientes)
assert "\"ref\":\"Set/26\"" in h.replace(" ", ""), "SO_OP.ref mudou — revisar REF"
brands = collections.defaultdict(list)
for k in set(sk25.index) | set(sk26v.index):
    a25 = float(sk25.loc[k, M[:REF + 1]].sum()) if k in sk25.index else 0; a26 = float(sk26v.loc[k, M[:REF + 1]].sum()) if k in sk26v.index else 0
    m25 = float(sk25.loc[k, M[REF]]) if k in sk25.index else 0; m26 = float(sk26v.loc[k, M[REF]]) if k in sk26v.index else 0
    if a25 or a26: brands[k[2]].append({"n": nome(k[1]), "a26": round(a26 / 1e3, 1), "a25": round(a25 / 1e3, 1), "m26": round(m26 / 1e3, 1), "m25": round(m25 / 1e3, 1)})
ORD = ["OFF!", "EXPOSIS", "RAID", "BAYGON", "LYSOFORM", "GLADE", "PATO", "BRAVO", "ZIPLOC"]
BR = [{"marca": b, "skus": sorted(brands[b], key=lambda s: -s["a26"])} for b in ORD if b in brands and sum(s["a26"] for s in brands[b]) > 0]
# ── ranking de SKUs 2026 (R$ Jan–Out) ──
COR = ['#3b82f6', '#60a5fa', '#818cf8', '#2dd4bf', '#34d399', '#fb923c', '#f472b6', '#facc15', '#a78bfa', '#22d3ee']
tot26 = sk26u.sum(axis=1).sort_values(ascending=False)   # ranking em unidades (o card mostra "un")
RANK = [[nome(k[1])[:34], round(float(val)), COR[i % len(COR)]] for i, (k, val) in enumerate(tot26.head(10).items())]
# ── estoque 29/05/2026 ──
D = os.path.join(A, "DADO ARAUJO 29-05.xlsx")
el = pd.read_excel(D, sheet_name="ESTOQUE LOJA"); cd = pd.read_excel(D, sheet_name="ESTOQUE CD", header=1)
proc = pd.read_excel(D, sheet_name="BASE PROCV").drop_duplicates("Cód Produto DV").set_index("Cód Produto DV")
stL = el.groupby("Cód Produto DV")["Loja"].sum(); nLj = el[el["Loja"] > 0].groupby("Cód Produto DV")["Loja - Fiscal"].nunique()
stC = cd.groupby("Cód Produto DV")["CD M. ANTONIO ARAUJO"].sum()
vMai = sk26u[M[4]]; vMai.index = [k[0] for k in vMai.index]; v3 = sk26u[M[2:5]].mean(axis=1); v3.index = vMai.index
nomes = {k[0]: (k[1], k[2]) for k in sk26u.index}
for c in proc.index:
    if c not in nomes: nomes[c] = (proc.loc[c, "Produto"], MARCA(proc.loc[c, "MARCA"]))
EST, EST_OP = [], []
totLj = el["Loja - Fiscal"].nunique()
for c in sorted(set(stL.index) | set(stC.index)):
    lj, cdv = int(stL.get(c, 0) or 0), int(stC.get(c, 0) or 0); e = lj + cdv; q = int(vMai.get(c, 0) or 0); q3 = round(float(v3.get(c, 0) or 0))
    if not e and not q: continue
    if str(c).strip().lower().startswith("total"): continue
    nm, mc = nomes.get(c, (c, ""));
    cob = round(e / q * 30) if q else (999 if e else 0)
    risco = "critico" if (q and cob < 15) or (not e and q) else ("atencao" if q and cob < 30 else "ok")
    EST.append({"sku": nome(nm), "marca": mc, "ean": "", "estoque": e, "venda": q, "venda_abr": q, "dem": q, "giro": q, "vendaSet": q, "vendaOut": q,
                "vendaNov": q, "vendaMar": q, "vendaAbr": q, "cob": cob, "dias": cob, "risco": risco, "lojas": lj, "cdRS": cdv, "cdPR": 0, "pend": 0,
                "lojasCount": int(nLj.get(c, 0) or 0), "totalLojas": totLj})
    if q: EST_OP.append({"n": nome(nm)[:38], "marca": mc, "est": e, "q": q, "q3": q3, "doh": cob})
EST_OP.sort(key=lambda x: -x["doh"])
print("estoque 29/05: SKUs", len(EST), "· un", sum(x["estoque"] for x in EST), "(lojas", sum(x["lojas"] for x in EST), "· CD", sum(x["cdRS"] for x in EST), ") · lojas", totLj)
js = lambda o: json.dumps(o, ensure_ascii=False, separators=(",", ":"))
arr = lambda a: "[" + ",".join("null" if x is None else (str(int(x)) if float(x).is_integer() else repr(round(x, 2))) for x in a) + "]"
DADOS = ("\n/* ═ ARAUJO (MG) — SELL-OUT (VOL + RECEITA + RANK) · fonte: BASE SELL OUT ARAUJO 23–26 (Jan/23–Out/26) ═ */\n"
         + "".join(f"const ARAUJO_REC_{y} = {arr(REC[y])};\nconst ARAUJO_VOL_{y} = {arr(VOL[y])};\n" for y in (2023, 2024, 2025, 2026))
         + "const ARAUJO_RANK = " + js(RANK) + ";\n"
         + "/* estoque Araujo 29/05/2026 (lojas + CD M. Antônio Araujo) × venda Mai/26 */\nconst ARA_ESTOQUE = " + js(EST) + ";\n"
         + "var araMetaMode = 'rec';\n")
rep("/* ═ DD-RIOMED — SELL-OUT (VOL + RECEITA + RANK) ═ */", DADOS + "/* ═ DD-RIOMED — SELL-OUT (VOL + RECEITA + RANK) ═ */")
# ── HTML do painel: cópia do DD-Riomed ──
a = h.index("<!-- ═══════════ DD-RIOMED ═══════════ -->"); b = h.index("</div><!-- fim panel-sellout -->", a); P = h[a:b]
i0 = P.index("<!-- INTOCAVEIS-ddriomed-INI -->"); i1 = P.index("<!-- INTOCAVEIS-ddriomed-FIM -->") + len("<!-- INTOCAVEIS-ddriomed-FIM -->"); P = P[:i0] + P[i1:]
for x, y in (("ddriomed", "araujo"), ("DD-RIOMED", "ARAUJO"), ("DD-Riomed", "Araujo"), ("RIOMED", "ARAUJO"), ("Riomed", "Araujo"),
             ("setRIO", "setARA"), ("setRio", "setAra"), ("renderRIO", "renderARA"), ("renderRio", "renderAra"), ("RIO_ESTOQUE", "ARA_ESTOQUE")):
    P = P.replace(x, y)
P = re.sub(r"(['\"#( ])rio-", r"\1ara-", P); P = P.replace("'rio'", "'ara'").replace('"rio"', '"ara"')
assert "rio" not in re.sub(r"[A-Za-zÀ-ú]*rio[A-Za-zÀ-ú]*", lambda m: "" if m.group(0) != "rio" else "rio", P).split("rio-")[0] or True
h = h[:b] + P + h[b:]
# CSS do painel (#panel-ddriomed-inner → também #panel-araujo-inner)
c1 = h.index("<script")
css = re.sub(r"#panel-ddriomed-inner([^,{]*)", r"#panel-ddriomed-inner\1, #panel-araujo-inner\1", h[:c1]); h = css + h[c1:]
# ── JS: cópia das funções do DD-Riomed ──
a = h.index("var rioEstoqueView  = 'barras';"); b = h.index("  renderRioMeta();\n}", a) + len("  renderRioMeta();\n}") if "  renderRioMeta();\n}" in h[a:] else h.index("  renderRioMeta();\r\n}", a) + len("  renderRioMeta();\r\n}")
J = h[a:b]
for x, y in (("RIO_ESTOQUE", "ARA_ESTOQUE"), ("rioEstoqueView", "araEstoqueView"), ("renderRIOEstoqueBarras", "renderARAEstoqueBarras"), ("setRioEstoqueView", "setAraEstoqueView"),
             ("rioLineMode", "araLineMode"), ("rioBarMode", "araBarMode"), ("renderRIOMesBars", "renderARAMesBars"), ("RIOMED_VOL_", "ARAUJO_VOL_"), ("RIOMED_REC_", "ARAUJO_REC_"),
             ("renderRioAnoBars", "renderAraAnoBars"), ("initRiomed", "initAraujo"), ("RIOMED_RANK", "ARAUJO_RANK"), ("renderRIOLine", "renderARALine"), ("renderRioMeta", "renderAraMeta"),
             ("getKpisForClient('rio')", "getKpisForClient('ara')"), ("'rio'", "'ara'"), ("DD-RIOMED", "ARAUJO"), ("Dias de estoque RIO", "Dias de estoque Araujo"), ("nov: ", "mai: "), ("'CD RS'", "'CD Araujo'")):
    J = J.replace(x, y)
J = re.sub(r"(['\"])rio-", r"\1ara-", J)
assert "RIO" not in J and "rio-" not in J, [m.start() for m in re.finditer("RIO|rio-", J)][:5]
h = h[:b] + "\n\n/* ═══════════ ARAUJO (MG) — cópia do painel DD-Riomed ═══════════ */\n" + J + "\n" + h[b:]
# ── cadastros ──
rep("""  rio: { vol: function(y){ return y==='2024'?RIOMED_VOL_2024:(y==='2025'?RIOMED_VOL_2025:RIOMED_VOL_2026); },
         rec: function(y){ return y==='2024'?RIOMED_REC_2024:(y==='2025'?RIOMED_REC_2025:RIOMED_REC_2026); } },""",
    """  rio: { vol: function(y){ return y==='2024'?RIOMED_VOL_2024:(y==='2025'?RIOMED_VOL_2025:RIOMED_VOL_2026); },
         rec: function(y){ return y==='2024'?RIOMED_REC_2024:(y==='2025'?RIOMED_REC_2025:RIOMED_REC_2026); } },
  ara: { vol: function(y){ return {'2024':ARAUJO_VOL_2024,'2025':ARAUJO_VOL_2025,'2026':ARAUJO_VOL_2026}[y]; },
         rec: function(y){ return {'2024':ARAUJO_REC_2024,'2025':ARAUJO_REC_2025,'2026':ARAUJO_REC_2026}[y]; } },""")
rep("""            'ddriomed': function(){delete initialized['sellout_ddriomed'];if(typeof initRiomed==='function')initRiomed();}""",
    """            'ddriomed': function(){delete initialized['sellout_ddriomed'];if(typeof initRiomed==='function')initRiomed();},
            'araujo': function(){delete initialized['sellout_araujo'];if(typeof initAraujo==='function')initAraujo();}""")
rep("""      <option value="ddriomed">DD-Riomed</option>
    </select>""", """      <option value="ddriomed">DD-Riomed</option>
      <option value="araujo">Araujo (MG)</option>
    </select>""")
rep("panvel:'Panvel', ddgam:'DD-GAM', ddgaucha:'DD-Gaúcha', ddriomed:'DD-Riomed'\n  };", "panvel:'Panvel', ddgam:'DD-GAM', ddgaucha:'DD-Gaúcha', ddriomed:'DD-Riomed', araujo:'Araujo'\n  };")
rep("""        _add(_fy(RIOMED_VOL_2024,RIOMED_VOL_2025,RIOMED_VOL_2026),v25,v26);
      }
    }""", """        _add(_fy(RIOMED_VOL_2024,RIOMED_VOL_2025,RIOMED_VOL_2026),v25,v26);
      }
    } else if(cl==='araujo'){
      if(typeof ARAUJO_REC_2024!=='undefined'){
        _add(_fy(ARAUJO_REC_2024,ARAUJO_REC_2025,ARAUJO_REC_2026),r25,r26);
        _add(_fy(ARAUJO_VOL_2024,ARAUJO_VOL_2025,ARAUJO_VOL_2026),v25,v26);
      }
    }""")
rep("""    rio: {
      rec: (typeof RIOMED_REC_2024 !== 'undefined') ? {'2024':RIOMED_REC_2024,'2025':RIOMED_REC_2025,'2026':RIOMED_REC_2026} : null,
      vol: (typeof RIOMED_VOL_2024 !== 'undefined') ? {'2024':RIOMED_VOL_2024,'2025':RIOMED_VOL_2025,'2026':RIOMED_VOL_2026} : null
    }""", """    rio: {
      rec: (typeof RIOMED_REC_2024 !== 'undefined') ? {'2024':RIOMED_REC_2024,'2025':RIOMED_REC_2025,'2026':RIOMED_REC_2026} : null,
      vol: (typeof RIOMED_VOL_2024 !== 'undefined') ? {'2024':RIOMED_VOL_2024,'2025':RIOMED_VOL_2025,'2026':RIOMED_VOL_2026} : null
    },
    ara: {
      rec: (typeof ARAUJO_REC_2024 !== 'undefined') ? {'2024':ARAUJO_REC_2024,'2025':ARAUJO_REC_2025,'2026':ARAUJO_REC_2026} : null,
      vol: (typeof ARAUJO_VOL_2024 !== 'undefined') ? {'2024':ARAUJO_VOL_2024,'2025':ARAUJO_VOL_2025,'2026':ARAUJO_VOL_2026} : null
    }""")
rep("var KPIS_CONFIG = {\n  rio: [", "var KPIS_CONFIG = {\n  ara: [],\n  rio: [")
rep("""        else if(clientId === 'ddriomed') initRiomed();""", """        else if(clientId === 'ddriomed') initRiomed();
        else if(clientId === 'araujo')   initAraujo();""")
rep("""      else if(id==='ddriomed') initRiomed();""", """      else if(id==='ddriomed') initRiomed();
      else if(id==='araujo') initAraujo();""")
rep("""            else if(_sub==='ddriomed') initRiomed();""", """            else if(_sub==='ddriomed') initRiomed();
            else if(_sub==='araujo') initAraujo();""")
rep("""  setRIOLineMode:[function(v){rioLineMode=v;}, function(){renderRIOLine();}],""", """  setRIOLineMode:[function(v){rioLineMode=v;}, function(){renderRIOLine();}],
  setARALineMode:[function(v){araLineMode=v;}, function(){renderARALine();}],
  setARABarMode:[function(v){araBarMode=v;}, function(){renderARAMesBars();}],
  setAraMetaMode:[function(v){araMetaMode=v;}, function(){renderAraMeta();}, 'todos'],""")
rep("""        vol:function(y){return {'2024':RIOMED_VOL_2024,'2025':RIOMED_VOL_2025,'2026':RIOMED_VOL_2026}[y];}, rec:function(y){return {'2024':RIOMED_REC_2024,'2025':RIOMED_REC_2025,'2026':RIOMED_REC_2026}[y];}}
};""", """        vol:function(y){return {'2024':RIOMED_VOL_2024,'2025':RIOMED_VOL_2025,'2026':RIOMED_VOL_2026}[y];}, rec:function(y){return {'2024':RIOMED_REC_2024,'2025':RIOMED_REC_2025,'2026':RIOMED_REC_2026}[y];}},
  Ara: {pre:'ara', barra:function(){return araBarMode;}, linha:function(){return araLineMode;}, meta:function(){return araMetaMode;}, parcial:true, nomeLinha:'ARA',
        vol:function(y){return {'2024':ARAUJO_VOL_2024,'2025':ARAUJO_VOL_2025,'2026':ARAUJO_VOL_2026}[y];}, rec:function(y){return {'2024':ARAUJO_REC_2024,'2025':ARAUJO_REC_2025,'2026':ARAUJO_REC_2026}[y];}}
};""")
rep("""    'rio-kpis':{vol:yd(g('RIOMED_VOL_2024'),g('RIOMED_VOL_2025'),g('RIOMED_VOL_2026')),rec:yd(g('RIOMED_REC_2024'),g('RIOMED_REC_2025'),g('RIOMED_REC_2026'))}
  };""", """    'rio-kpis':{vol:yd(g('RIOMED_VOL_2024'),g('RIOMED_VOL_2025'),g('RIOMED_VOL_2026')),rec:yd(g('RIOMED_REC_2024'),g('RIOMED_REC_2025'),g('RIOMED_REC_2026'))},
    'ara-kpis':{vol:yd(g('ARAUJO_VOL_2024'),g('ARAUJO_VOL_2025'),g('ARAUJO_VOL_2026')),rec:yd(g('ARAUJO_REC_2024'),g('ARAUJO_REC_2025'),g('ARAUJO_REC_2026'))}
  };""")
rep("ddgaucha:'DD-Gaúcha', ddriomed:'DD-Riomed'};\n\nfunction op1G", "ddgaucha:'DD-Gaúcha', ddriomed:'DD-Riomed', araujo:'Araujo'};\n\nfunction op1G")
rep("ddgaucha:'gch-kpis', ddriomed:'rio-kpis'};", "ddgaucha:'gch-kpis', ddriomed:'rio-kpis', araujo:'ara-kpis'};")
rep("  var LBL = {saojoao:'São João', nissei:'Nissei', clamed:'Clamed', panvel:'Panvel', ddgam:'DD-GAM', ddgaucha:'DD-Gaúcha', ddriomed:'DD-Riomed'};",
    "  var LBL = {saojoao:'São João', nissei:'Nissei', clamed:'Clamed', panvel:'Panvel', ddgam:'DD-GAM', ddgaucha:'DD-Gaúcha', ddriomed:'DD-Riomed', araujo:'Araujo'};")
rep("""    else if(cl==='ddriomed'){ R=[g('RIOMED_REC_2025'),g('RIOMED_REC_2026'),g('RIOMED_REC_2027')]; V=[g('RIOMED_VOL_2025'),g('RIOMED_VOL_2026'),g('RIOMED_VOL_2027')]; }""",
    """    else if(cl==='ddriomed'){ R=[g('RIOMED_REC_2025'),g('RIOMED_REC_2026'),g('RIOMED_REC_2027')]; V=[g('RIOMED_VOL_2025'),g('RIOMED_VOL_2026'),g('RIOMED_VOL_2027')]; }
    else if(cl==='araujo'){ R=[g('ARAUJO_REC_2025'),g('ARAUJO_REC_2026'),g('ARAUJO_REC_2027')]; V=[g('ARAUJO_VOL_2025'),g('ARAUJO_VOL_2026'),g('ARAUJO_VOL_2027')]; }""")
# SO_OP (One Page: marca e DOH)
a = h.index("var SO_OP = ") + len("var SO_OP = "); so, n = json.JSONDecoder().raw_decode(h[a:])
so["clientes"]["araujo"] = {"metric": "val", "brands": BR, "est": EST_OP, "estRef": "Mai/26 (estoque de 29/05/26)"}
h = h[:a] + js(so) + h[a + n:]
# estoque com data própria (estRef) no card DOH do detalhado e do One Page
rep("  var E=D.est, ref=SO_OP.ref;", "  var E=D.est, ref=D.estRef||SO_OP.ref;")
i = h.index("  h += op1Sec('DOH e Ruptura – posição '+mesRef);"); j = h.index("DOH = estoque ÷ venda média diária do mês de referência.');", i)
seg = h[i:j].replace("mesRef", "mesRefE"); h = h[:i] + "  var mesRefE = X.estRef || mesRef;" + chr(10) + seg + h[j:]
open(H, "w", encoding="utf-8", newline="").write(h); print("ok · marcas", [b["marca"] for b in BR], "· rank", RANK[:3])
