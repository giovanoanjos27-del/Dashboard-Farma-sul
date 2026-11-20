"""Atualiza a base CPT2 da aba CPT Clientes com a edição IQVIA CPT 202610 (só Repelentes):
  1) FY27 (Jul–Out/26, posições 24–27): Out/26 novo + Jul–Set/26 refeitos pela Matriz de Lojas › Analítico – 6 Meses
     (preco/preco_medio_202610.json; meses Mai..Out/26 nas posições 0..5 do JSON).
     · chave que já existe → valor direto · cidade nova em UF × Bandeira × Canal existente → rateio pelo peso no FY26
     · combinação nova → chave nova com histórico zerado.
     Corrige Jul–Set/26: a edição 202609 alinhada (AlinhaCPT202609) somava Bloqueadores na categoria.
  2) Jul–Out/25 (posições 12–15) alinhados ao IQVIA › Análise Bandeira, Ano Anterior, só Repelentes, por UF × Canal × Bandeira:
     Out/25 = Mês (Ano Anterior) ÷ (1 + cresc.) · Jul+Ago+Set/25 = YTD Fiscal/25 − Out/25, divididos pela proporção que já estava na base.
     Dentro de UF × Canal × Bandeira, a cidade segue o peso no próprio mês (fallback: FY26; senão igual).
  3) CPT2_LOJAS → Out/26 (lojas com venda da categoria / com venda SCJ), meses e rótulos Jul–Out.
Uso: python gerar_cpt2_202610.py <dashboard.html> [saida.html]"""
import sys, os, re, json, collections, warnings
import openpyxl, pandas as pd
warnings.filterwarnings("ignore"); sys.stdout.reconfigure(encoding="utf-8")
H = sys.argv[1]; OUT = sys.argv[2] if len(sys.argv) > 2 else H
D = os.path.dirname(os.path.abspath(__file__)); PD = os.path.join(D, "preco")
h = open(H, encoding="utf-8", newline="").read()


def pega(nome):
    tag = "var " + nome + "="; a = h.index(tag) + len(tag)
    o, n = json.JSONDecoder().raw_decode(h[a:]); return o, a, a + n


def troca(nome, valor):
    global h
    _, a, b = pega(nome); h = h[:a] + json.dumps(valor, ensure_ascii=False, separators=(",", ":")) + h[b:]


def rep(a, b):
    global h; assert h.count(a) == 1, (h.count(a), a[:90]); h = h.replace(a, b)


r2 = lambda v: round(v, 2)

K, _, _ = pega("CPT2_KEYS"); F, _, _ = pega("CPT2_FAB_ALL"); C, _, _ = pega("CPT2_CAT_ALL")
assert len(F[0]) == 27, "base esperada com 27 meses (Jul/24–Set/26)"
antes = {n: (sum(sum(s[a:b]) for s in C), sum(sum(s[a:b]) for s in F)) for n, a, b in (("Jul–Set/25", 12, 15), ("Out/25", 15, 16), ("Jul–Set/26", 24, 27))}

# ---------- 1) Jul–Out/26 pela Matriz de Lojas ----------
P = json.load(open(os.path.join(PD, "preco_medio_202610.json"), encoding="utf-8"))
JP = [2, 3, 4, 5]                      # Jul, Ago, Set, Out/26 no JSON (Mai..Out)
pos = {tuple(k): i for i, k in enumerate(K)}
grp = collections.defaultdict(list)
for i, k in enumerate(K): grp[(k[0], k[2], k[3])].append(i)


def peso_fy26(idx, serie):
    w = [sum(serie[i][12:24]) for i in idx]; t = sum(w)
    return [x / t for x in w] if t > 0 else [1.0 / len(idx)] * len(idx)


nF = [[0.0] * 4 for _ in K]; nC = [[0.0] * 4 for _ in K]; novos = []; cont = collections.Counter()
for j, k in enumerate(P["keys"]):
    k = tuple(k); f = [P["d"]["SCJ"]["rs"][j][m] for m in JP]; c = [P["d"]["CAT"]["rs"][j][m] for m in JP]
    if k in pos:
        i = pos[k]
        for m in range(4): nF[i][m] += f[m]; nC[i][m] += c[m]
        cont["direto"] += sum(c)
    elif (k[0], k[2], k[3]) in grp:
        idx = grp[(k[0], k[2], k[3])]; wf = peso_fy26(idx, F); wc = peso_fy26(idx, C)
        for i, a, b in zip(idx, wf, wc):
            for m in range(4): nF[i][m] += f[m] * a; nC[i][m] += c[m] * b
        cont["rateio"] += sum(c)
    else:
        novos.append((k, f, c)); cont["novo"] += sum(c)
for i in range(len(K)):
    F[i] = F[i][:24] + [r2(x) for x in nF[i]]; C[i] = C[i][:24] + [r2(x) for x in nC[i]]
for k, f, c in sorted(novos):
    K.append(list(k)); F.append([0.0] * 24 + [r2(x) for x in f]); C.append([0.0] * 24 + [r2(x) for x in c])


# ---------- 2) Jul–Out/25 alinhados ao Ano Anterior (só Repelentes) ----------
def ler(fn, tipo):
    ws = openpyxl.load_workbook(os.path.join(D, fn), data_only=True).active
    filtro = ws.cell(1, 1).value
    assert "R$ CPP" in filtro and tipo in filtro and "SCJ" in filtro and "Ano Anterior" in filtro, (fn, filtro)
    g = collections.defaultdict(lambda: [0.0, 0.0])                 # cat_ant, fab_ant
    for r in ws.iter_rows(min_row=4, values_only=True):
        if not r[5] or r[0] != "Repelentes": continue
        cat, fab = float(r[6] or 0), float(r[8] or 0)
        cc = float(r[11]) if r[11] not in (None, "") else None; cf = float(r[12]) if r[12] not in (None, "") else None
        x = g[(r[2], r[5], r[3])]
        x[0] += cat / (1 + cc) if cc is not None and cc > -1 else 0.0
        x[1] += fab / (1 + cf) if cf is not None and cf > -1 else 0.0
    return g


Y = ler("CPT_202610_YTDFiscal_AnoAnt_SCJ.xlsx", "YTD Fiscal"); M = ler("CPT_202610_Mes_AnoAnt_SCJ.xlsx", "odo é M")
grp = collections.defaultdict(list)
for i, k in enumerate(K): grp[(k[0], k[2], k[3])].append(i)
novos25 = []
for g in sorted((set(Y) | set(M)) - set(grp)):
    uf, ban, can = g; K.append([uf, "N/I", ban, can]); F.append([0.0] * 28); C.append([0.0] * 28); grp[g].append(len(K) - 1); novos25.append(g)


def peso(idx, serie, p):
    w = [serie[i][p] for i in idx]; t = sum(w)
    if t <= 0: w = [sum(serie[i][12:24]) for i in idx]; t = sum(w)
    return [x / t for x in w] if t > 0 else [1.0 / len(idx)] * len(idx)


for g, idx in grp.items():
    for s, S in ((0, C), (1, F)):
        y, m = Y.get(g, [0.0, 0.0])[s], M.get(g, [0.0, 0.0])[s]
        v = {15: m}; resto = max(0.0, y - m)
        base = [sum(S[i][p] for i in idx) for p in (12, 13, 14)]; tb = sum(base)
        for p, b in zip((12, 13, 14), base): v[p] = resto * (b / tb if tb > 0 else 1 / 3)
        for p in (12, 13, 14, 15):
            w = peso(idx, S, p)
            for i, x in zip(idx, w): S[i][p] = r2(x * v[p])
troca("CPT2_KEYS", K); troca("CPT2_FAB_ALL", F); troca("CPT2_CAT_ALL", C)

# listas dos filtros com as combinações novas
ufc, _, _ = pega("CPT2_UF_CIDADES"); bu, _, _ = pega("CPT2_BAN_UFS"); cb, _, _ = pega("CPT2_CANAL_BANS"); cu, _, _ = pega("CPT2_CANAL_UFS"); ab, _, _ = pega("CPT2_ALL_BAN")
for uf, cid, ban, can in [k for k, _, _ in novos] + [(g[0], "N/I", g[1], g[2]) for g in novos25]:
    for d, ch, v in ((ufc, uf, cid), (bu, ban, uf), (cb, can, ban), (cu, can, uf)):
        l = d.setdefault(ch, [])
        if v not in l: l.append(v); l.sort()
    if ban not in ab: ab.append(ban)
ab.sort()
troca("CPT2_UF_CIDADES", ufc); troca("CPT2_BAN_UFS", bu); troca("CPT2_CANAL_BANS", cb); troca("CPT2_CANAL_UFS", cu); troca("CPT2_ALL_BAN", ab)

# ---------- 3) CNPJs Out/26, meses e rótulos ----------
RX = re.compile(r"- ([^|]*)/([A-Z]{2})\s*$")
U = collections.defaultdict(set); S2 = collections.defaultdict(set)
for n in (1, 2, 3):
    x = pd.read_excel(os.path.join(PD, f"SCJ_RS_c{n}.xlsx"), header=2)
    for r in x.itertuples(index=False):
        pdv = r[4]
        if not isinstance(pdv, str) or pd.isna(r[12]) or int(r[12]) != 202610: continue
        mm = RX.search(pdv)
        if not mm: continue
        k = mm.group(2) + "|" + str(r[0]) + "|" + str(r[2])
        if not pd.isna(r[7]) and r[7] > 0: U[k].add(pdv)
        if not pd.isna(r[8]) and r[8] > 0: S2[k].add(pdv)
troca("CPT2_LOJAS", {k: [len(U[k]), len(S2[k])] for k in sorted(U)})
rep('"Jun/26","Jul/26","Ago/26","Set/26"];', '"Jun/26","Jul/26","Ago/26","Set/26","Out/26"];')
a = h.index("/* CPT2 — séries completas Jul/24…Set/26"); b = h.index("\n", a)
h = h[:a] + "/* CPT2 — séries completas Jul/24…Out/26 (28 meses; Jul–Out/26 = IQVIA CPT edição 202610, Matriz de Lojas por loja, só Repelentes; Jul–Out/25 alinhados ao Ano Anterior da edição 202610 › Análise Bandeira, só Repelentes; Nov/25–Jun/26 = edições anteriores)." + h[b:]
rep("— IQVIA CPT edição 202609 (Set/26) */", "— IQVIA CPT edição 202610 (Out/26) */")
rep("CNPJs = lojas IQVIA Set/26 (", "CNPJs = lojas IQVIA Out/26 (")
rep('<option value="FY27" selected>FY27 · Jul–Set/26 vs Jul–Set/25</option>', '<option value="FY27" selected>FY27 · Jul–Out/26 vs Jul–Out/25</option>')
rep('<option value="YTD26">2026 · Jan–Set/26 vs Jan–Set/25</option>', '<option value="YTD26">2026 · Jan–Out/26 vs Jan–Out/25</option>')
rep('id="cpt2-sub-fab">FY26 vs FY27 (Jul–Set)<', 'id="cpt2-sub-fab">FY26 vs FY27 (Jul–Out)<')
rep('id="cpt2-sub-shr">FY26 vs FY27 (Jul–Set) ·', 'id="cpt2-sub-shr">FY26 vs FY27 (Jul–Out) ·')
open(OUT, "w", encoding="utf-8", newline="").write(h)

tot = sum(cont.values())
print("chaves", len(K), f"(+{len(novos)} novas pela Matriz, +{len(novos25)} N/I pelo alinhamento) ·", ", ".join(f"{a} {v/tot*100:.1f}%" for a, v in cont.items()))
for nome, a, b in (("Jul–Set/25", 12, 15), ("Out/25", 15, 16), ("Jul–Set/26", 24, 27)):
    c, f = sum(sum(s[a:b]) for s in C), sum(sum(s[a:b]) for s in F)
    print(f"  {nome}: categoria {antes[nome][0]/1e6:6.2f} -> {c/1e6:6.2f} MM · SCJ {antes[nome][1]/1e6:6.2f} -> {f/1e6:6.2f} MM · share {f/c*100:5.2f}%")
for nome, p in (("Jul/25", 12), ("Ago/25", 13), ("Set/25", 14), ("Out/25", 15), ("Jul/26", 24), ("Ago/26", 25), ("Set/26", 26), ("Out/26", 27)):
    c, f = sum(s[p] for s in C), sum(s[p] for s in F); print(f"  {nome}: categoria {c/1e6:6.2f} MM · SCJ {f/1e6:6.2f} MM · share {f/c*100:5.2f}%")
c26, f26 = sum(sum(s[24:28]) for s in C), sum(sum(s[24:28]) for s in F); c25, f25 = sum(sum(s[12:16]) for s in C), sum(sum(s[12:16]) for s in F)
print(f"  Brasil Jul–Out: categoria {c25/1e6:.2f} -> {c26/1e6:.2f} MM ({c26/c25-1:+.1%}) · SCJ {f25/1e6:.2f} -> {f26/1e6:.2f} MM ({f26/f25-1:+.1%}) · share {f25/c25*100:.2f}% -> {f26/c26*100:.2f}% ({(f26/c26-f25/c25)*100:+.2f} p.p.)")
G = {"GRUPO SAO JOAO": ["SAO JOAO FARMACIAS"], "GRUPO NISSEI SA": ["NISSEI"], "GRUPO PANVEL": ["PANVEL"], "GRUPO CLAMED": ["PRECO POPULAR", "DROGARIA CATARINENSE"]}
for gname, bans in G.items():
    ix = [i for i, k in enumerate(K) if k[2] in bans]
    c26, f26 = sum(sum(C[i][24:28]) for i in ix), sum(sum(F[i][24:28]) for i in ix); c25, f25 = sum(sum(C[i][12:16]) for i in ix), sum(sum(F[i][12:16]) for i in ix)
    print(f"  {gname:16s} Jul–Out cat {c26:>13,.0f} ({c26/c25-1:+.1%}) · SCJ {f26:>12,.0f} ({f26/f25-1:+.1%}) · share {f26/c26*100:5.2f}% ({(f26/c26-f25/c25)*100:+.2f} p.p.)")
print("  CNPJs Out/26:", sum(len(v) for v in U.values()), "lojas c/ categoria ·", sum(len(v) for v in S2.values()), "c/ SCJ")
