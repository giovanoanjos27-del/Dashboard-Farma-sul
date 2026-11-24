"""Araujo × slides SCJ de Out/26 (One_Page_Perfumaria_Outubro26_v24 e Deck_Conveniencia_YTD_Out26_v3) — 24/11/2026
  1) JBP Perfumaria calibrado no slide: YTD Out = venda + R$ 302 mil (93,5%); Out = venda − R$ 107 mil; ano = R$ 6,39 mi ÷ 101,6%;
     Jun–Set e Nov–Dez rateados pelo desenho anterior; projeção da Araujo pelo ritmo dos 2 últimos meses (set/out), como no slide
  2) JBP Conveniência = 2025 × 1,20 mês a mês (deck: 'Meta JBP Conveniência = +20% sobre 2025')
  3) Marcas da Araujo (Total, Perfumaria, Conveniência) com referência Out/26 (YTD Jan–Out e Out vs Out)
  4) One Page › Conveniência: Top 20 lojas, diagnóstico RAID (out vs out, preço × unidades por SKU, 20 maiores lojas de 2025) e Pato Block,
     pela base de lojas 25-26 (lojas físicas, sem e-commerce)
Uso: python araujo_slides_out26.py <base.html>"""
import sys, os, re, json, collections, warnings
import pandas as pd
warnings.filterwarnings("ignore"); sys.stdout.reconfigure(encoding="utf-8")
H = sys.argv[1]; h = open(H, encoding="utf-8", newline="").read(); A = os.path.dirname(os.path.abspath(__file__)); T = os.path.join(A, "TransferXL-06BCNjgwr5kgG")
M = ['JANEIRO', 'FEVEREIRO', 'MARÇO', 'ABRIL', 'MAIO', 'JUNHO', 'JULHO', 'AGOSTO', 'SETEMBRO', 'OUTUBRO', 'NOVEMBRO', 'DEZEMBRO']


def pega(n):
    m = re.search(r"var " + n + r"\s*=\s*", h); o, k = json.JSONDecoder().raw_decode(h[m.end():]); return o, m.end(), m.end() + k


def troca(n, v):
    global h
    _, a, b = pega(n); h = h[:a] + json.dumps(v, ensure_ascii=False, separators=(",", ":")) + h[b:]


def rep(a, b, n=1):
    global h
    if h.count(a) != n and h.count(a.replace("\n", "\r\n")) == n: a, b = a.replace("\n", "\r\n"), b.replace("\n", "\r\n")
    assert h.count(a) == n, (h.count(a), a[:100]); h = h.replace(a, b)


assert "ARA_CONV" not in h, "já aplicado"
SET, _, _ = pega("ARAUJO_SETOR")
# ── 1) JBP Perfumaria ──
p26 = SET["perfumaria"]["rec"]["2026"]; ytd = sum(p26[:10]); out = p26[9]
jY, jOut, jAno = ytd + 302000, out - 107000, 6390000 / 1.016
old = [1198681, 941113, 693452, 465603, 282878, 145000, 160000, 185000, 340000, 480000, 590000, 1080000]
base5 = sum(old[:5]); resto = jY - base5 - jOut; f4 = old[5:9]; jun_set = [round(resto * x / sum(f4)) for x in f4]
nd = jAno - jY; jbpP = old[:5] + jun_set + [round(jOut), round(nd * 590 / 1670), round(nd * 1080 / 1670)]
print("JBP Perfumaria", jbpP, "· YTD Out", sum(jbpP[:10]), f"({ytd / sum(jbpP[:10]) * 100:.1f}%) · Out", jbpP[9], "· ano", sum(jbpP))
c25 = SET["conveniencia"]["rec"]["2025"]; jbpC = [round(v * 1.2) for v in c25]
c26 = SET["conveniencia"]["rec"]["2026"]; print("JBP Conveniência YTD Out", sum(jbpC[:10]), f"({sum(c26[:10]) / sum(jbpC[:10]) * 100:.1f}%)")
JB = {"perfumaria": jbpP, "conveniencia": jbpC,
      "fonte": {"perfumaria": "calibrada no One Page Perfumaria Out/26 (YTD Out R$ " + format(round(sum(jbpP[:10])), ",").replace(",", ".") + "; ano R$ " + format(round(sum(jbpP)), ",").replace(",", ".") + "); meses intermediários rateados",
                "conveniencia": "JBP Conveniência = 2025 + 20% (deck Conveniência YTD Out/26)"}}
i = h.index("var ARAUJO_JBP = "); j = h.index("};", i) + 2
h = h[:i] + "var ARAUJO_JBP = " + json.dumps(JB, ensure_ascii=False, separators=(",", ":")) + ";" + h[j:]
rep("  var jbp = (cli==='araujo' && sub==='perfumaria' && metric==='val' && typeof ARAUJO_JBP!=='undefined') ? ARAUJO_JBP.perfumaria : null;",
    "  var jbp = (cli==='araujo' && (sub==='perfumaria'||sub==='conveniencia') && metric==='val' && typeof ARAUJO_JBP!=='undefined') ? ARAUJO_JBP[sub] : null;")
rep("'. <span style=\"color:#94A3B8;font-size:10px;\">Meta: '+ARAUJO_JBP.fonte+'.</span>';",
    "'. Projeção do ano = <b>'+op1Num(ano26/X.jbp.reduce(function(s,v){return s+(v||0);},0)*100,1)+'% do JBP</b> (meta '+op1Val('val',X.jbp.reduce(function(s,v){return s+(v||0);},0))+'). <span style=\"color:#94A3B8;font-size:10px;\">Meta: '+(ARAUJO_JBP.fonte[X.sub]||'')+'.</span>';")
rep("  var proj = a25.map(function(v,i){ return i<last ? null : i===last ? a26[i] : v*(1+(g||0)); });",
    "  var gP = (X.cli==='araujo' && last>=1 && (a25[last]+a25[last-1])>0) ? (a26[last]+a26[last-1])/(a25[last]+a25[last-1])-1 : g;   /* Araujo: ritmo dos 2 últimos meses, como nos slides SCJ */\n"
    "  var proj = a25.map(function(v,i){ return i<last ? null : i===last ? a26[i] : v*(1+(gP||0)); });")
rep("    + 'Mantido o ritmo do YTD, o ano fecha em <b>'",
    "    + (gP!==g ? 'Mantido o ritmo de '+OP1_MES[last-1].toLowerCase()+'/'+OP1_MES[last].toLowerCase()+' (<b>'+op1Pct(gP)+'</b>)' : 'Mantido o ritmo do YTD')+', o ano fecha em <b>'")
# ── 3) marcas com referência Out/26 ──
B = os.path.join(T, "BASE SELL OUT ARAUJO-23-24-25-26.xlsx")
v = pd.read_excel(B, sheet_name="VALOR 23 A 25"); v25 = v[v["ANO"] == 2025]; n = pd.read_excel(B, sheet_name="2026"); n = n[n["Ano"] == 2026]
MAR = lambda m: {"OFF": "OFF!"}.get(str(m).strip().upper(), str(m).strip().upper()); REF = 9
nome = lambda p: " ".join(w.capitalize() if not re.match(r"^\d", w) else w.lower() for w in str(p).split())
sub = lambda x: "KIT EXPOSIS" if str(x).startswith("KIT EXPOSIS") else str(x)
def agrega(d25, d26, chave):
    out = collections.defaultdict(lambda: collections.defaultdict(lambda: [0.0] * 4))
    for _, r in d25.iterrows():
        b = out[MAR(r["MARCA"])][chave(r)]; b[1] += float(r[M[:REF + 1]].fillna(0).sum()); b[3] += float(r[M[REF]] or 0) if pd.notna(r[M[REF]]) else 0
    for _, r in d26.iterrows():
        i = M.index(r["Mês"])
        if i <= REF:
            b = out[MAR(r["MARCA"])][chave(r)]; b[0] += float(r["VALOR"] or 0)
            if i == REF: b[2] += float(r["VALOR"] or 0)
    return out
def brands(o, ordem):
    R = []
    for mc in ordem + [m for m in o if m not in ordem]:
        if mc not in o: continue
        sk = [{"n": nome(k), "a26": round(x[0] / 1e3, 1), "a25": round(x[1] / 1e3, 1), "m26": round(x[2] / 1e3, 1), "m25": round(x[3] / 1e3, 1)} for k, x in o[mc].items() if x[0] or x[1]]
        if sum(s["a26"] for s in sk) > 0: R.append({"marca": mc, "skus": sorted(sk, key=lambda s: -s["a26"])})
    return R
ORD = ["OFF!", "EXPOSIS", "RAID", "BAYGON", "LYSOFORM", "GLADE", "PATO", "BRAVO"]
SO, a, b = pega("SO_OP")
SO["clientes"]["araujo"]["brands"] = brands(agrega(v25, n, lambda r: r["Produto"]), ORD)
SO["clientes"]["araujo_perf"]["brands"] = brands(agrega(v25[v25["SETOR"] == "PERFUMARIA"], n[n["SETOR"] == "PERFUMARIA"], lambda r: sub(r["SUB CATEGORIA"])), ["OFF!", "EXPOSIS"])
SO["clientes"]["araujo_conv"]["brands"] = brands(agrega(v25[v25["SETOR"] == "CONVENIÊNCIA"], n[n["SETOR"] == "CONVENIÊNCIA"], lambda r: r["Produto"]), ORD[2:])
for k in ("araujo", "araujo_perf", "araujo_conv"): SO["clientes"][k].update({"ref": "Out/26", "ytd": "Jan–Out", "mesExt": "Outubro"})
off = next(x for x in SO["clientes"]["araujo_perf"]["brands"] if x["marca"] == "OFF!"); t26 = sum(s["a26"] for s in off["skus"]); t25 = sum(s["a25"] for s in off["skus"])
print(f"OFF! YTD Out {t26:.0f}k vs {t25:.0f}k = {(t26 / t25 - 1) * 100:+.1f}% (slide +19,3%)")
troca("SO_OP", SO)
rep("  var met=D.metric, ref=SO_OP.ref, ytd=SO_OP.ytd, Y=SO_OP.ano;", "  var met=D.metric, ref=D.ref||SO_OP.ref, ytd=D.ytd||SO_OP.ytd, Y=SO_OP.ano;")
rep("  var txt='No YTD de '+(SO_OP.mesExt||ref.split('/')[0])", "  var txt='No YTD de '+(D.mesExt||SO_OP.mesExt||ref.split('/')[0])")
# ── 4) Conveniência por loja ──
L = pd.read_excel(os.path.join(T, "SELL OUT LOJA 2026 ARAUJO.xlsx"), sheet_name="BASE 25-26")
L = L[(L["SETOR"] == "CONVENIÊNCIA") & ~L["Loja - Fiscal"].astype(str).str.upper().str.contains("E-COMMERCE")].copy()
L["v"] = pd.to_numeric(L["Val Faturamento"], errors="coerce").fillna(0); L["u"] = pd.to_numeric(L["Qtd Vendida"], errors="coerce").fillna(0); L["m"] = L["MÊS"].map(M.index)
ytd_ = lambda d, y: d[(d["ANO"] == y) & (d["m"] <= 9)]; mes = lambda d, y, i: d[(d["ANO"] == y) & (d["m"] == i)]
g = lambda d: d.groupby("Loja - Fiscal")["v"].sum()
f25, y26, y25, o26, o25 = g(L[L["ANO"] == 2025]), g(ytd_(L, 2026)), g(ytd_(L, 2025)), g(mes(L, 2026, 9)), g(mes(L, 2025, 9))
top = f25.sort_values(ascending=False).head(20)
T20 = [[lj, round(f25[lj]), round(y26.get(lj, 0)), round(y25.get(lj, 0)), round(o26.get(lj, 0)), round(o25.get(lj, 0))] for lj in top.index]
res = {"f25": round(top.sum()), "pctFis": round(top.sum() / f25.sum() * 100, 1), "y26": round(sum(y26.get(l, 0) for l in top.index)), "y25": round(sum(y25.get(l, 0) for l in top.index)),
       "o26": round(sum(o26.get(l, 0) for l in top.index)), "o25": round(sum(o25.get(l, 0) for l in top.index)), "allY": round((y26.sum() / y25.sum() - 1) * 100, 1), "allO": round((o26.sum() / o25.sum() - 1) * 100, 1)}
R = L[L["MARCA"].astype(str).str.upper() == "RAID"]
ro26, ro25 = mes(R, 2026, 9), mes(R, 2025, 9)
rd = {"u25": int(ro25["u"].sum()), "u26": int(ro26["u"].sum()), "v25": round(ro25["v"].sum()), "v26": round(ro26["v"].sum()),
      "lj25": int((ro25.groupby("Loja - Fiscal")["v"].sum() > 0).sum()), "lj26": int((ro26.groupby("Loja - Fiscal")["v"].sum() > 0).sum())}
sk = []
for p, gg in R[R["m"] == 9].groupby("Produto"):
    a5, a6 = gg[gg["ANO"] == 2025], gg[gg["ANO"] == 2026]; u5, u6, v5, v6 = a5["u"].sum(), a6["u"].sum(), a5["v"].sum(), a6["v"].sum()
    if u5 + u6 > 0: sk.append([nome(p)[:34], round(v5 / u5, 2) if u5 else None, round(v6 / u6, 2) if u6 else None, int(u5), int(u6), round(v6 - v5)])
sk.sort(key=lambda r: -(r[3] * (r[1] or 0))); sk = sk[:12]
rf25 = g(R[R["ANO"] == 2025]).sort_values(ascending=False).head(20); ry26, ry25, rO26, rO25 = g(ytd_(R, 2026)), g(ytd_(R, 2025)), g(mes(R, 2026, 9)), g(mes(R, 2025, 9))
gu = lambda d: d.groupby("Loja - Fiscal")["u"].sum(); ru26, ru25 = gu(mes(R, 2026, 9)), gu(mes(R, 2025, 9))
RL = [[lj, round(rf25[lj]), round(ry26.get(lj, 0)), round(ry25.get(lj, 0)), round(rO25.get(lj, 0)), round(rO26.get(lj, 0)), int(ru25.get(lj, 0)), int(ru26.get(lj, 0))] for lj in rf25.index]
P = L[L["SUB CATEGORIA"].astype(str).str.upper().str.contains("BLOCK") & L["MARCA"].astype(str).str.upper().str.contains("PATO")]
py = ytd_(P, 2026); pv = lambda d: d.groupby("Loja - Fiscal")["u"].sum()
def mesP(i, filtro=None):
    d = mes(P, 2026, i); d = d if filtro is None else d[d["Produto"].astype(str).str.upper().str.contains(filtro)]
    lj = (pv(d) > 0).sum(); return {"v": round(d["v"].sum()), "u": int(d["u"].sum()), "lj": int(lj), "giro": round(d["u"].sum() / lj, 2) if lj else None}
PB = {"ytdV": round(py["v"].sum()), "ytdU": int(py["u"].sum()), "ytdLj": int((pv(py) > 0).sum()), "set": mesP(8), "out": mesP(9),
      "var": {k: {"ytd": round(py[py["Produto"].astype(str).str.upper().str.contains(k)]["v"].sum()), "set": mesP(8, k), "out": mesP(9, k)} for k in ("ALGOD", "LAVAND")}}
CONV = {"top": T20, "res": res, "raid": rd, "sku": sk, "rl": RL, "pato": PB}
print("Top20 2025", res, "· RAID out", rd, "· Pato", {k: PB[k] for k in ("ytdV", "ytdU", "ytdLj")}, PB["set"], PB["out"])
JS = r"""
/* Araujo › Conveniência por loja (base de lojas 25-26, lojas físicas): Top 20, diagnóstico RAID e Pato Block */
var ARA_CONV = __CONV__;
function araConvHtml(){
  var D=ARA_CONV, f=function(v){ return op1Val('val',v); }, p=function(a,b){ return b>0 ? a/b-1 : null; }, P=function(x,d){ return x==null?'—':op1Pct(x,d==null?0:d); }, C=function(x){ return op1Cor(x); };
  var th='padding:5px 8px;font-size:9.5px;font-weight:700;color:#64748B;text-transform:uppercase;border-bottom:1.5px solid rgba(94,153,208,0.35);text-align:right;', td='padding:4px 8px;font-size:11px;text-align:right;border-bottom:0.5px solid #E2E8F0;';
  var tb=function(cab, linhas){ return '<div style="overflow:auto;"><table style="width:100%;border-collapse:collapse;"><thead><tr>'+cab.map(function(c,i){ return '<th style="'+th+(i<2?'text-align:left;':'')+'">'+c+'</th>'; }).join('')+'</tr></thead><tbody>'+linhas.join('')+'</tbody></table></div>'; };
  var tile=function(l,v,c,s){ return '<div class="op1-mb"><div class="op1-ml">'+l+'</div><div class="op1-mv" style="color:'+c+'">'+v+'</div><div class="op1-ms">'+s+'</div></div>'; };
  var R=D.res, h='';
  h += op1Sec('Conveniência · Top 20 lojas – maiores faturamentos de 2025 e performance em 2026');
  h += '<div class="op1-row" style="grid-template-columns:repeat(4,1fr);">'+tile('Top 20 · Fat. 2025', f(R.f25), OP1_C.navy, op1Num(R.pctFis,0)+'% do sell-out das lojas físicas')+tile('Top 20 · YTD Out/26', P(p(R.y26,R.y25),1), C(p(R.y26,R.y25)), f(R.y26)+' vs '+f(R.y25))+tile('Top 20 · Out vs Out', P(p(R.o26,R.o25),1), C(p(R.o26,R.o25)), f(R.o26)+' vs '+f(R.o25))+tile('Todas as lojas físicas', P(R.allY/100,1), C(R.allY), 'YTD · out vs out '+P(R.allO/100,1))+'</div>';
  h += '<div class="card op1-card">'+tb(['#','Loja','Fat. 2025','YTD 2026','Var. YTD','Out vs Out'], D.top.map(function(r,i){ var a=p(r[2],r[3]), b=p(r[4],r[5]); return '<tr><td style="'+td+'text-align:left;">'+(i+1)+'</td><td style="'+td+'text-align:left;font-weight:600;">'+r[0]+'</td><td style="'+td+'">'+f(r[1])+'</td><td style="'+td+'">'+f(r[2])+'</td><td style="'+td+'color:'+C(a)+';font-weight:700;">'+P(a)+'</td><td style="'+td+'color:'+C(b)+';font-weight:700;">'+P(b)+'</td></tr>'; }))+'</div>';
  var Q=D.raid, pu25=Q.u25?Q.v25/Q.u25:0, pu26=Q.u26?Q.v26/Q.u26:0;
  h += op1Sec('Diagnóstico RAID – o que mudou em outubro (Out/26 vs Out/25)');
  h += '<div class="op1-row" style="grid-template-columns:repeat(4,1fr);">'+tile('Unidades', P(p(Q.u26,Q.u25),1), C(p(Q.u26,Q.u25)), op1Num(Q.u25)+' → '+op1Num(Q.u26))+tile('Preço médio', P(p(pu26,pu25),1), OP1_C.navy, 'R$ '+op1Num(pu25,1)+' → R$ '+op1Num(pu26,1))+tile('Lojas com RAID', Q.lj25+' → '+Q.lj26, OP1_C.navy, 'lojas físicas com venda')+tile('Unidades por loja', P(p(Q.u26/Q.lj26,Q.u25/Q.lj25),1), C(p(Q.u26/Q.lj26,Q.u25/Q.lj25)), op1Num(Q.u25/Q.lj25,1)+' → '+op1Num(Q.u26/Q.lj26,1))+'</div>';
  h += '<div class="card op1-card">'+tb(['SKU','','Preço out/25','Preço out/26','Var. preço','Unid. out/25','Unid. out/26','Var. unid.','Δ R$'], D.sku.map(function(r){ var vp=(r[1]&&r[2])?r[2]/r[1]-1:null, vu=p(r[4],r[3]); return '<tr><td style="'+td+'text-align:left;font-weight:600;" colspan="2">'+r[0]+'</td><td style="'+td+'">'+(r[1]==null?'—':'R$ '+op1Num(r[1],1))+'</td><td style="'+td+'">'+(r[2]==null?'—':'R$ '+op1Num(r[2],1))+'</td><td style="'+td+'">'+P(vp)+'</td><td style="'+td+'">'+op1Num(r[3])+'</td><td style="'+td+'">'+op1Num(r[4])+'</td><td style="'+td+'color:'+C(vu)+';font-weight:700;">'+P(vu)+'</td><td style="'+td+'color:'+C(r[5])+';font-weight:700;">'+f(r[5])+'</td></tr>'; }))+'</div>';
  h += op1Sec('Diagnóstico RAID – 20 maiores lojas de RAID em 2025 e 2026');
  h += '<div class="card op1-card">'+tb(['#','Loja','RAID 2025','Var. YTD','Out/25','Out/26','Out vs Out','Var. unid.'], D.rl.map(function(r,i){ var a=p(r[2],r[3]), b=p(r[5],r[4]), u=p(r[7],r[6]); return '<tr><td style="'+td+'text-align:left;">'+(i+1)+'</td><td style="'+td+'text-align:left;font-weight:600;">'+r[0]+'</td><td style="'+td+'">'+f(r[1])+'</td><td style="'+td+'color:'+C(a)+';font-weight:700;">'+P(a)+'</td><td style="'+td+'">'+f(r[4])+'</td><td style="'+td+'">'+f(r[5])+'</td><td style="'+td+'color:'+C(b)+';font-weight:700;">'+P(b)+'</td><td style="'+td+'color:'+C(u)+';">'+P(u)+'</td></tr>'; }))+'</div>';
  var B=D.pato, vo=function(k){ return B.var[k]; };
  h += op1Sec('Pato Block – sell-out, giro por loja e lojas com venda');
  h += '<div class="op1-row" style="grid-template-columns:repeat(4,1fr);">'+tile('Pato Block · YTD Out/26', f(B.ytdV), OP1_C.navy, op1Num(B.ytdU)+' un · '+B.ytdLj+' lojas no YTD')
     + tile('Algodão · YTD', f(vo('ALGOD').ytd), OP1_C.navy, 'Out vs Set '+P(p(vo('ALGOD').out.v,vo('ALGOD').set.v),1)+' · lojas '+vo('ALGOD').set.lj+' → '+vo('ALGOD').out.lj)
     + tile('Lavanda · YTD', f(vo('LAVAND').ytd), OP1_C.navy, 'Out vs Set '+P(p(vo('LAVAND').out.v,vo('LAVAND').set.v),1)+' · lojas '+vo('LAVAND').set.lj+' → '+vo('LAVAND').out.lj)
     + tile('Curto prazo · Out vs Set', P(p(B.out.v,B.set.v),1), C(p(B.out.v,B.set.v)), f(B.out.v)+' vs '+f(B.set.v)+' · lojas '+B.set.lj+' → '+B.out.lj+' · giro '+op1Num(B.set.giro,2)+' → '+op1Num(B.out.giro,2))+'</div>';
  h += '<div class="op1-fonte">Fonte: base de lojas 25-26 (sell-out Araujo), setor Conveniência, lojas físicas (sem e-commerce). Preço médio = valor ÷ unidades. Giro = unidades por loja com venda no mês.</div>';
  return h;
}
"""
rep("var araSetor = 'total';", JS.replace("__CONV__", json.dumps(CONV, ensure_ascii=False, separators=(",", ":"))).strip() + "\nvar araSetor = 'total';")
rep("  host.innerHTML = h;\n", "  if(X.cli==='araujo' && X.sub==='conveniencia' && typeof araConvHtml==='function'){ try{ h += araConvHtml(); }catch(e){ console.warn('[araConv]', e); } }\n  host.innerHTML = h;\n")
open(H, "w", encoding="utf-8", newline="").write(h); print("ok")
