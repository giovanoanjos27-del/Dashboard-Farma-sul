"""CPT Clientes: (1) OFF/EXPOSIS ganham Out/26 e Out/25 (IQVIA CPT 202610 › Análise Bandeira, Marca = OFF REPELENTE /
EXPOSIS, Mercado Repelentes, Mês × Ano Anterior, R$ CPP; marca/{OFF,EXPOSIS}_Mes_AnoAnt.xlsx) → CPT2_MARCA com 8 meses
[Jul25,Ago25,Set25,Out25,Jul26,Ago26,Set26,Out26]; cada célula UF × Canal × Grupo × Bandeira vai para as chaves pelo peso
do SCJ no mês (sem chave do grupo: UF × Canal × Bandeira).
(2) Filtro Período: FY27 Jul–Out acumulado, Q1 (Jul–Set/26 vs Jul–Set/25) e Q2 (Out/26 vs Out/25, cresce até Dez).
Uso: python cpt_marca_out_q1q2.py <base.html>"""
import sys, os, json, collections, warnings
import openpyxl
warnings.filterwarnings("ignore"); sys.stdout.reconfigure(encoding="utf-8")
H = sys.argv[1]; D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "marca")
h = open(H, encoding="utf-8", newline="").read()


def pega(nome):
    tag = "var " + nome + "="; a = h.index(tag) + len(tag)
    o, n = json.JSONDecoder().raw_decode(h[a:]); return o, a, a + n


def rep(a, b, n=1):
    global h
    if h.count(a) != n and h.count(a.replace("\n", "\r\n")) == n: a, b = a.replace("\n", "\r\n"), b.replace("\n", "\r\n")
    assert h.count(a) == n, (h.count(a), a[:90]); h = h.replace(a, b)


K, _, _ = pega("CPT2_KEYS"); F, _, _ = pega("CPT2_FAB_ALL"); C, _, _ = pega("CPT2_CAT_ALL"); MA, a0, b0 = pega("CPT2_MARCA")
assert all(len(v) == 6 for v in MA["OFF"].values()), "CPT2_MARCA já tem Out"
g4 = collections.defaultdict(list); g3 = collections.defaultdict(list)
for i, k in enumerate(K): g4[(k[0], k[3], k[2], k[4])].append(i); g3[(k[0], k[3], k[2])].append(i)


def ler(fn, marca):
    ws = openpyxl.load_workbook(os.path.join(D, fn), data_only=True).active
    f = ws.cell(1, 1).value; assert marca in f and "Ano Anterior" in f and "R$ CPP" in f and "Repelentes" in f and "Mês" in f, (fn, f)
    out = {}
    for r in ws.iter_rows(min_row=4, values_only=True):
        if r[0] != "Repelentes" or not r[5]: continue
        fab = float(r[8] or 0); cf = float(r[12]) if r[12] not in (None, "") else None
        out[(r[2], r[3], r[5], r[4])] = (fab, fab / (1 + cf) if cf is not None and cf > -1 else 0.0)
    return out


def peso(idx, p):
    for S in (F, C):
        w = [S[i][p] for i in idx]; t = sum(w)
        if t > 0: return [x / t for x in w]
    return [1.0 / len(idx)] * len(idx)


novo = {}
for cod, arq, nome in (("OFF", "OFF", "OFF REPELENTE"), ("EXP", "EXPOSIS", "EXPOSIS")):
    X = ler(f"{arq}_Mes_AnoAnt.xlsx", nome)
    res = {i: v[:3] + [0.0] + v[3:] + [0.0] for i, v in ((int(k), v) for k, v in MA[cod].items())}
    sem = 0.0; tot = [0.0, 0.0]
    for (uf, can, ban, grp), (o26, o25) in X.items():
        tot[0] += o26; tot[1] += o25
        idx = g4.get((uf, can, ban, grp)) or g3.get((uf, can, ban))
        if not idx: sem += o26; continue
        for p, v, j in ((27, o26, 7), (15, o25, 3)):
            for i, w in zip(idx, peso(idx, p)):
                if v * w: res.setdefault(i, [0.0] * 8)[j] += v * w
    novo[cod] = {str(i): [round(x, 2) for x in v] for i, v in sorted(res.items()) if any(v)}
    t = [sum(v[j] for v in novo[cod].values()) for j in range(8)]
    print(f"{cod}: Out/25 {t[3]/1e6:.2f} MM → Out/26 {t[7]/1e6:.2f} MM ({t[7]/t[3]-1:+.1%}) · IQVIA {tot[1]/1e6:.2f} → {tot[0]/1e6:.2f} · sem chave R$ {sem:,.0f}"
          f" · Jul–Out/25 {sum(t[:4])/1e6:.2f} → Jul–Out/26 {sum(t[4:])/1e6:.2f} MM")
h = h[:a0] + json.dumps(novo, separators=(",", ":")) + h[b0:]
rep("CPT2_MARCA_POS = [12,13,14,24,25,26]", "CPT2_MARCA_POS = [12,13,14,15,24,25,26,27]")

# ---- período: Q1 / Q2 ----
rep('cursor:pointer;"><option value="FY27" selected>FY27 · Jul–Out/26 vs Jul–Out/25</option>',
    'cursor:pointer;"><option value="FY27" selected>FY27 · Jul–Out/26 vs Jul–Out/25 (acumulado)</option><option value="Q1">FY27 · Jul–Set/26 vs Jul–Set/25 (Q1)</option><option value="Q2">FY27 · Out/26 vs Out/25 (Q2)</option>')
rep("""  else                        cfg = {p:'FY26', c:'FY27', p0:12, c0:24, n:N-24, ini:'Jul', yP:25, cal:false};
  var n = cfg.n, p0 = cfg.p0, c0 = cfg.c0;""", """  else if(CPT2_FY === 'Q1')   cfg = {p:'Q1 FY26', c:'Q1 FY27', p0:12, c0:24, n:Math.min(3, N-24), ini:'Jul', yP:25, cal:false, mi:0};
  else if(CPT2_FY === 'Q2')   cfg = {p:'Q2 FY26', c:'Q2 FY27', p0:15, c0:27, n:Math.max(0, Math.min(3, N-27)), ini:'Out', yP:25, cal:false, mi:3};
  else                        cfg = {p:'FY26', c:'FY27', p0:12, c0:24, n:N-24, ini:'Jul', yP:25, cal:false};
  var n = cfg.n, p0 = cfg.p0, c0 = cfg.c0;""")
rep("  if(CPT2_MARCA_SEL && CPT2_MARCA_SEL !== 'CONC' && CPT2_FY === 'FY27') n = Math.min(n, CPT2_MARCA_POS.length / 2);   /* por marca só há Jul–Set */",
    "  if(CPT2_MARCA_SEL && CPT2_MARCA_SEL !== 'CONC' && CPT2_FY === 'FY27') n = Math.min(n, CPT2_MARCA_POS.length / 2);   /* por marca: Jul–Out */")
rep("""  var M = cfg.cal ? ['Jan','Fev','Mar','Abr','Mai','Jun','Jul','Ago','Set','Out','Nov','Dez'] : ['Jul','Ago','Set','Out','Nov','Dez','Jan','Fev','Mar','Abr','Mai','Jun'];
  _C2 = {p:cfg.p, c:cfg.c, n:n, per:(n<12 ? M[0]+'–'+M[n-1] : '')};""", """  var M = cfg.cal ? ['Jan','Fev','Mar','Abr','Mai','Jun','Jul','Ago','Set','Out','Nov','Dez'] : ['Jul','Ago','Set','Out','Nov','Dez','Jan','Fev','Mar','Abr','Mai','Jun'];
  if(cfg.mi) M = M.slice(cfg.mi).concat(M.slice(0, cfg.mi));
  _C2 = {p:cfg.p, c:cfg.c, n:n, p0:p0, c0:c0, per:(n<12 ? (n>1 ? M[0]+'–'+M[n-1] : M[0]) : '')};""")
rep("  CPT2_MES_FY25 = M.map(function(x,i){ return x+'/'+(cfg.cal ? y0 : y0+(i>=6?1:0)); });\n  CPT2_MES_FY26 = M.map(function(x,i){ return x+'/'+(cfg.cal ? y0+1 : y0+1+(i>=6?1:0)); });",
    "  var vira = cfg.mi ? 6 - cfg.mi : 6;   /* posição do Jan na lista de meses */\n  CPT2_MES_FY25 = M.map(function(x,i){ return x+'/'+(cfg.cal ? y0 : y0+(i>=vira?1:0)); });\n  CPT2_MES_FY26 = M.map(function(x,i){ return x+'/'+(cfg.cal ? y0+1 : y0+1+(i>=vira?1:0)); });")
rep("  if(typeof CPT2_MARCA_SEL !== 'undefined' && CPT2_MARCA_SEL && CPT2_MARCA_SEL !== 'CONC') v = 'FY27';   /* OFF/EXPOSIS/PATO só têm Jul–Set */\n  CPT2_FY = (v === 'FY26' || v === 'YTD26') ? v : 'FY27'; cpt2BuildView();",
    "  if(typeof CPT2_MARCA_SEL !== 'undefined' && CPT2_MARCA_SEL && CPT2_MARCA_SEL !== 'CONC' && ['FY27','Q1','Q2'].indexOf(v) < 0) v = 'FY27';   /* OFF/EXPOSIS/PATO: só FY27 (Jul–Out, Q1, Q2) */\n  CPT2_FY = ['FY26','YTD26','Q1','Q2'].indexOf(v) >= 0 ? v : 'FY27'; cpt2BuildView();")
rep("  if(s) [].forEach.call(s.options, function(o){ o.disabled = so && o.value !== 'FY27'; });",
    "  if(s) [].forEach.call(s.options, function(o){ o.disabled = so && ['FY27','Q1','Q2'].indexOf(o.value) < 0; });")
rep("  if(n) n.textContent = so ? 'por marca: só FY27 (Jul–Set)' :", "  if(n) n.textContent = so ? 'por marca: só FY27 (Jul–Out)' :")
rep("  cpt2SetFY(so ? 'FY27' : CPT2_FY);", "  cpt2SetFY(so && ['FY27','Q1','Q2'].indexOf(CPT2_FY) < 0 ? 'FY27' : CPT2_FY);")
# estimativa Jul/Ago só no início do FY
rep("&& (m===0 || m===1); }", "&& (m===0 || m===1) && (typeof _C2==='undefined' || _C2.p0===12); }")
# diagnóstico por marca: meses do período escolhido
rep("""  if(!sel && CPT2_FY === 'FY27' && typeof CPT2_MARCA !== 'undefined'){
    var o=[0,0], e=[0,0];
    idx.forEach(function(i){ var a=CPT2_MARCA.OFF[i], b=CPT2_MARCA.EXP[i];
      if(a){ o[0]+=a[0]+a[1]+a[2]; o[1]+=a[3]+a[4]+a[5]; } if(b){ e[0]+=b[0]+b[1]+b[2]; e[1]+=b[3]+b[4]+b[5]; } });
    var s = function(x,c){ return c>0 ? x/c*100 : null; }, P = CPT2_MARCA_POS, k = P.length / 2, cm = [0,0];
    idx.forEach(function(i){ var c = CPT2_CAT_ALL[i]; for(var j=0;j<k;j++){ cm[0] += c[P[j]]||0; cm[1] += c[P[k+j]]||0; } });""",
    """  if(!sel && ['FY27','Q1','Q2'].indexOf(CPT2_FY) >= 0 && typeof CPT2_MARCA !== 'undefined' && _C2.n > 0){
    var o=[0,0], e=[0,0], P = CPT2_MARCA_POS, J = [[],[]], cm = [0,0];
    for(var z=0; z<_C2.n; z++){ J[0].push(P.indexOf(_C2.p0+z)); J[1].push(P.indexOf(_C2.c0+z)); }
    idx.forEach(function(i){ var a=CPT2_MARCA.OFF[i], b=CPT2_MARCA.EXP[i], c=CPT2_CAT_ALL[i];
      for(var t=0;t<2;t++) J[t].forEach(function(j, z){ if(j<0) return; if(a) o[t]+=a[j]||0; if(b) e[t]+=b[j]||0; cm[t] += c[(t?_C2.c0:_C2.p0)+z]||0; }); });
    var s = function(x,c){ return c>0 ? x/c*100 : null; };""")
rep("L.push('🏆 <span style=\"color:#64748B;\">(Jul–Set)</span> <b>OFF!</b> '", "L.push('🏆 <span style=\"color:#64748B;\">('+_C2.per+')</span> <b>OFF!</b> '")
open(H, "w", encoding="utf-8", newline="").write(h); print("ok")
