"""Share IQVIA no One Page (24/11/2026, 4º ajuste): OFF! e Exposis ganham os blocos Jan–Abr e Mai–Jun de 2025 e 2026
(a edição 202610 não tem mês a mês por marca e bandeira antes de Jul), por diferença de acumulados da IQVIA:
  marca Jan–Abr = YTD (Jan–Out) − Semestre Móvel (Mai–Out)   ·   marca Mai–Jun = Semestre Móvel − Jul–Out (CPT2_MARCA)
  categoria do bloco = soma mensal da base CPT2; ano anterior pelo 'Cresc.' dos exports (Comparação = Ano Anterior)
Cada mês do bloco recebe o share médio do bloco (linha tracejada, rótulo só no 1º mês). Araujo fica com os valores mês a mês do slide.
Exports: share_marca_ytd/{OFF,EXP}_{YTD,SEM}_AnoAnt.xlsx.  Uso: python share_blocos.py <base.html>"""
import sys, os, re, json, warnings
import pandas as pd
warnings.filterwarnings("ignore"); sys.stdout.reconfigure(encoding="utf-8")
H = sys.argv[1]; h = open(H, encoding="utf-8", newline="").read(); D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "share_marca_ytd")


def pega(n):
    m = re.search(r"var " + n + r"\s*=\s*", h); o, k = json.JSONDecoder().raw_decode(h[m.end():]); return o, m.end(), m.end() + k


def rep(a, b, n=1):
    global h
    if h.count(a) != n and h.count(a.replace("\n", "\r\n")) == n: a, b = a.replace("\n", "\r\n"), b.replace("\n", "\r\n")
    assert h.count(a) == n, (h.count(a), a[:90]); h = h.replace(a, b)


S, a0, b0 = pega("SHARE_IQ"); assert not any("blocos" in v for v in S.values()), "já aplicado"
K, _, _ = pega("CPT2_KEYS"); C, _, _ = pega("CPT2_CAT_ALL"); MA, _, _ = pega("CPT2_MARCA"); MES, _, _ = pega("CPT2_MES_ALL")
BAN = {"saojoao": ["SAO JOAO FARMACIAS"], "nissei": ["NISSEI"], "panvel": ["PANVEL"], "clamed": ["DROGARIA CATARINENSE", "PRECO POPULAR"], "araujo": ["ARAUJO"]}
def ex(nm):
    x = pd.read_excel(os.path.join(D, nm + ".xlsx"), header=2); x = x[x["Categoria"] == "Repelentes"].fillna(0)
    x["f25"] = x.apply(lambda r: r["Demanda Fabricante"] / (1 + r["Cresc. Fabricante"]) if r["Cresc. Fabricante"] > -1 else 0, axis=1); return x
E = {(m, p): ex(f"{m}_{p}_AnoAnt") for m in ("OFF", "EXP") for p in ("YTD", "SEM")}
mi = lambda s: MES.index(s)
for cli, bans in BAN.items():
    if cli == "araujo": continue
    ix = [i for i, k in enumerate(K) if k[2] in bans]
    cat = lambda ms: sum(C[i][mi(m)] for i in ix for m in ms)
    blocos = []
    for nm, mk in (("off", "OFF"), ("exp", "EXP")):
        s = S[cli][nm]
        for ano, col, jo in (("26", "Demanda Fabricante", [4, 5, 6, 7]), ("25", "f25", [0, 1, 2, 3])):
            fy = E[(mk, "YTD")]; fs = E[(mk, "SEM")]
            ytd = fy[fy["Bandeira"].isin(bans)][col].sum(); sem = fs[fs["Bandeira"].isin(bans)][col].sum()
            julout = sum((MA[mk].get(str(i)) or [0] * 8)[j] for i in ix for j in jo)
            ja, mj = ytd - sem, sem - julout
            mJA = [f"{m}/{ano}" for m in ("Jan", "Fev", "Mar", "Abr")]; mMJ = [f"{m}/{ano}" for m in ("Mai", "Jun")]
            sJA = round(ja / cat(mJA) * 100, 1) if cat(mJA) and ja > 0 else None; sMJ = round(mj / cat(mMJ) * 100, 1) if cat(mMJ) and mj > 0 else None
            o = 0 if ano == "25" else 12
            for q in range(4): s[o + q] = sJA
            for q in range(4, 6): s[o + q] = sMJ
            print(f"{cli:8s} {nm} 20{ano}: Jan–Abr {sJA} · Mai–Jun {sMJ} · Jul–Out {s[o + 6:o + 10]}")
    S[cli]["blocos"] = [0, 1, 2, 3, 4, 5, 12, 13, 14, 15, 16, 17]
    S[cli]["fonteSerie"] = "OFF! e Exposis: Jan–Abr e Mai–Jun = share médio do bloco (IQVIA: YTD − Semestre Móvel e Semestre Móvel − Jul–Out, linha tracejada); Jul–Out mês a mês"
# conferência com a Araujo (valores do slide): blocos calculados vs média do slide
ix = [i for i, k in enumerate(K) if k[2] == "ARAUJO"]
for mk, nm in (("OFF", "off"), ("EXP", "exp")):
    fy = E[(mk, "YTD")]; fs = E[(mk, "SEM")]; ytd = fy[fy["Bandeira"] == "ARAUJO"]["Demanda Fabricante"].sum(); sem = fs[fs["Bandeira"] == "ARAUJO"]["Demanda Fabricante"].sum()
    c = sum(C[i][mi(m)] for i in ix for m in ("Jan/26", "Fev/26", "Mar/26", "Abr/26"))
    print(f"Araujo {nm} Jan–Abr/26 calculado {(ytd - sem) / c * 100:.1f} · slide (média ponderada aprox.) {sum(S['araujo'][nm][12:16]) / 4:.1f}")
h = h[:a0] + json.dumps(S, ensure_ascii=False, separators=(",", ":")) + h[b0:]
rep("      {label:'OFF!', data:D.off, borderColor:'#F59E0B', backgroundColor:'#fff', borderWidth:3, pointRadius:3.5, pointBorderWidth:2, tension:0.4, spanGaps:false},\n      {label:'Exposis', data:D.exp, borderColor:'#7C3AED', backgroundColor:'#fff', borderWidth:3, pointRadius:3.5, pointBorderWidth:2, tension:0.4, spanGaps:false}]},",
    "      {label:'OFF!', data:D.off, borderColor:'#F59E0B', backgroundColor:'#fff', borderWidth:3, pointRadius:function(c){ return BL(c.dataIndex)&&!IN(c.dataIndex)?0:3.5; }, pointBorderWidth:2, tension:0.4, spanGaps:false, segment:{borderDash:function(c){ return (BL(c.p0DataIndex)&&BL(c.p1DataIndex))?[6,5]:undefined; }}},\n"
    "      {label:'Exposis', data:D.exp, borderColor:'#7C3AED', backgroundColor:'#fff', borderWidth:3, pointRadius:function(c){ return BL(c.dataIndex)&&!IN(c.dataIndex)?0:3.5; }, pointBorderWidth:2, tension:0.4, spanGaps:false, segment:{borderDash:function(c){ return (BL(c.p0DataIndex)&&BL(c.p1DataIndex))?[6,5]:undefined; }}}]},")
rep("  var nf = function(v){ return v.toLocaleString('pt-BR',{minimumFractionDigits:1,maximumFractionDigits:1}); };",
    "  var nf = function(v){ return v.toLocaleString('pt-BR',{minimumFractionDigits:1,maximumFractionDigits:1}); };\n"
    "  var BLs = D.blocos || [], BL = function(i){ return BLs.indexOf(i)>=0; }, IN = function(i){ return i===0||i===4||i===12||i===16; };   /* blocos Jan–Abr e Mai–Jun: rótulo só no 1º mês */")
rep("      m.data.forEach(function(p,i){ var v=ds.data[i]; if(v==null) return; last=p; c.fillStyle=ds.borderColor; c.fillText(nf(v), p.x, p.y+(di===0?-9:(di===1?15:-9))); });",
    "      m.data.forEach(function(p,i){ var v=ds.data[i]; if(v==null) return; last=p; if(di>0 && BL(i) && !IN(i)) return; c.fillStyle=ds.borderColor; c.fillText(nf(v), p.x, p.y+(di===0?-9:(di===1?15:-9))); });")
rep("tooltip:{callbacks:{label:function(c){ return c.dataset.label+': '+(c.raw==null?'sem dado':nf(c.raw)+'%'); }}}},\n      scales:{x:{grid:{display:false}, ticks:{font:{size:10}, color:'#64748B',",
    "tooltip:{callbacks:{label:function(c){ return c.dataset.label+': '+(c.raw==null?'sem dado':nf(c.raw)+'%'+((c.datasetIndex>0&&BL(c.dataIndex))?' (média '+((c.dataIndex%12)<4?'Jan–Abr':'Mai–Jun')+')':'')); }}}},\n      scales:{x:{grid:{display:false}, ticks:{font:{size:10}, color:'#64748B',")
open(H, "w", encoding="utf-8", newline="").write(h); print("ok")
