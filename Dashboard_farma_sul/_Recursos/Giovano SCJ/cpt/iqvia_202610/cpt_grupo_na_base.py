"""CPT Clientes: grupo econômico passa a fazer parte da chave da base CPT2 → [UF, Cidade, Bandeira, Canal, Grupo].
Antes o grupo era deduzido pela bandeira, e bandeira compartilhada (INDEPENDENTES, MASTERFARMA…) entrava inteira em
todo grupo que a tinha (ex.: Grupo ADM Pharma = 14.405 lojas). Cada chave antiga é dividida entre os grupos que têm
lojas nela, pelos exports loja a loja da Matriz de Lojas (IQVIA CPT 202610, Mai–Out/26, preco/SCJ_RS_c{1,2,3}.xlsx):
  · Mai–Out/26 (posições 22–27): proporção de cada grupo naquele mês (categoria para a categoria, SCJ para o SCJ)
  · Jul–Out/25 (12–15): proporção do grupo no Ano Anterior da IQVIA (UF × Canal × Bandeira), só entre os grupos da chave
  · demais meses: proporção somada de Mai–Out/26 da chave (sem loja na cidade: UF × Bandeira × Canal; depois Análise
    Bandeira Out/26 da IQVIA; por fim o grupo único da bandeira ou a própria bandeira)
Também: CPT2_MARCA (OFF/EXPOSIS por chave) reindexado, CPT2_LOJAS por UF|Canal|Bandeira|Grupo, CPT2_GRP_BANS/ALL_GRUPOS
refeitos, e o JavaScript do filtro/tabela passa a usar o grupo da chave.
Uso: python cpt_grupo_na_base.py <dashboard.html>"""
import sys, os, re, json, collections, warnings
import pandas as pd
warnings.filterwarnings("ignore"); sys.stdout.reconfigure(encoding="utf-8")
H = sys.argv[1]; h = open(H, encoding="utf-8", newline="").read()
D = os.path.dirname(os.path.abspath(__file__)); PD = os.path.join(D, "preco")
dd = lambda: collections.defaultdict(float)


def pega(nome):
    tag = "var " + nome + "="; a = h.index(tag) + len(tag)
    o, n = json.JSONDecoder().raw_decode(h[a:]); return o, a, a + n


def troca(nome, valor):
    global h
    _, a, b = pega(nome); h = h[:a] + json.dumps(valor, ensure_ascii=False, separators=(",", ":")) + h[b:]


def rep(a, b, n=1):
    global h
    if h.count(a) != n and h.count(a.replace("\n", "\r\n")) == n: a, b = a.replace("\n", "\r\n"), b.replace("\n", "\r\n")
    assert h.count(a) == n, (h.count(a), a[:90]); h = h.replace(a, b)


K, _, _ = pega("CPT2_KEYS"); F, _, _ = pega("CPT2_FAB_ALL"); C, _, _ = pega("CPT2_CAT_ALL"); MA, _, _ = pega("CPT2_MARCA")
GB, _, _ = pega("CPT2_GRP_BANS"); MP = [12, 13, 14, 24, 25, 26]
assert all(len(k) == 4 for k in K), "base já tem grupo na chave"
NP = len(F[0]); assert NP == 28

# ---------- lojas da Matriz (Mai–Out/26) ----------
POS = {202605: 22, 202606: 23, 202607: 24, 202608: 25, 202609: 26, 202610: 27}
RX = re.compile(r"- ([^|]*)/([A-Z]{2})\s*$")
W = collections.defaultdict(lambda: collections.defaultdict(lambda: [dd(), dd()]))    # key4 -> pos -> [cat{g}, fab{g}]
W2 = collections.defaultdict(lambda: [dd(), dd()])                                      # (uf,ban,can) -> [cat{g}, fab{g}]
LU = collections.defaultdict(set); LS = collections.defaultdict(set)
for n in (1, 2, 3):
    x = pd.read_excel(os.path.join(PD, f"SCJ_RS_c{n}.xlsx"), header=2)
    for r in x.itertuples(index=False):
        can, grp, ban, pdv, cat, fab, mes = r[0], r[1], r[2], r[4], r[7], r[8], r[12]
        if not isinstance(pdv, str) or pd.isna(mes): continue
        m = RX.search(pdv)
        if not m: continue
        uf, cid = m.group(2), m.group(1).strip(); grp = str(grp) if isinstance(grp, str) else "N/I"
        cat = 0.0 if pd.isna(cat) else float(cat); fab = 0.0 if pd.isna(fab) else float(fab)
        p = POS[int(mes)]; w = W[(uf, cid, ban, can)][p]; w[0][grp] += cat; w[1][grp] += fab
        W2[(uf, ban, can)][0][grp] += cat; W2[(uf, ban, can)][1][grp] += fab
        if p == 27:
            if cat > 0: LU[(uf, can, ban, grp)].add(pdv)
            if fab > 0: LS[(uf, can, ban, grp)].add(pdv)


# ---------- IQVIA Análise Bandeira: Out/26 e Ano Anterior por grupo ----------
def bandeira(fn, ant):
    x = pd.read_excel(os.path.join(D, fn), header=2); out = collections.defaultdict(lambda: [dd(), dd()])
    for r in x.itertuples(index=False):
        if r[0] != "Repelentes" or not isinstance(r[5], str): continue
        cat, fab = float(r[6] or 0), float(r[8] or 0)
        if ant:
            cc = r[11] if not pd.isna(r[11]) else None; cf = r[12] if not pd.isna(r[12]) else None
            cat = cat / (1 + cc) if cc is not None and cc > -1 else 0.0; fab = fab / (1 + cf) if cf is not None and cf > -1 else 0.0
        o = out[(r[2], r[5], r[3])]; o[0][r[4]] += cat; o[1][r[4]] += fab
    return out


IQ = bandeira("CPT_202610_Mes_SCJ.xlsx", False)
AM = bandeira("CPT_202610_Mes_AnoAnt_SCJ.xlsx", True); AY = bandeira("CPT_202610_YTDFiscal_AnoAnt_SCJ.xlsx", True)
A25 = {}                                    # (uf,ban,can) -> {pos: [cat{g}, fab{g}]} : Out/25 = Mês, Jul–Set/25 = YTD − Mês
for k in set(AM) | set(AY):
    m, y = AM.get(k, [{}, {}]), AY.get(k, [{}, {}])
    rest = [{g: max(0.0, y[s].get(g, 0) - m[s].get(g, 0)) for g in set(y[s]) | set(m[s])} for s in (0, 1)]
    A25[k] = {15: [dict(m[0]), dict(m[1])], 12: rest, 13: rest, 14: rest}

inv = collections.defaultdict(list)
for g, bs in GB.items():
    for b in bs: inv[b].append(g)


def norm(d):
    t = sum(v for v in d.values() if v > 0)
    return {g: v / t for g, v in d.items() if v > 0} if t > 0 else None


def base(key):
    """proporção-base da chave por série (0 cat, 1 fab) e de onde veio"""
    uf, cid, ban, can = key
    if key in W:
        agg = [dd(), dd()]
        for p, w in W[key].items():
            for s in (0, 1):
                for g, v in w[s].items(): agg[s][g] += v
        b = [norm(agg[0]) or norm(agg[1]), norm(agg[1]) or norm(agg[0])]
        if b[0]: return b, "cidade"
    k3 = (uf, ban, can)
    if k3 in W2:
        b = [norm(W2[k3][0]) or norm(W2[k3][1]), norm(W2[k3][1]) or norm(W2[k3][0])]
        if b[0]: return b, "uf"
    for src, nm in ((IQ, "iqvia"), (AY, "iqvia")):
        if k3 in src:
            b = [norm(src[k3][0]) or norm(src[k3][1]), norm(src[k3][1]) or norm(src[k3][0])]
            if b[0]: return b, nm
    g = inv[ban][0] if len(inv[ban]) == 1 else ban
    return [{g: 1.0}, {g: 1.0}], "único"


nK, nF, nC, nM = [], [], [], {"OFF": {}, "EXP": {}}
cont = collections.Counter(); r2 = lambda v: round(v, 2)
for i, key in enumerate(K):
    key = tuple(key); b, de = base(key); cont[de] += sum(C[i]) + sum(F[i])
    sup = set(b[0]) | set(b[1])
    wp = []                                     # por posição: [pesos cat, pesos fab]
    for p in range(NP):
        ws = []
        for s in (0, 1):
            w = None
            if 22 <= p <= 27 and key in W and p in W[key]:
                w = norm(W[key][p][s]) or norm(W[key][p][1 - s])
            elif 12 <= p <= 15 and (key[0], key[2], key[3]) in A25:
                a = A25[(key[0], key[2], key[3])][p]
                w = norm({g: v for g, v in a[s].items() if g in sup}) or norm({g: v for g, v in a[1 - s].items() if g in sup})
            ws.append(w or b[s])
        wp.append(ws)
    gs = sorted({g for ws in wp for w in ws for g in w})
    mo, me = MA["OFF"].get(str(i)), MA["EXP"].get(str(i))
    for g in gs:
        c = [r2(C[i][p] * wp[p][0].get(g, 0)) for p in range(NP)]
        f = [r2(F[i][p] * wp[p][1].get(g, 0)) for p in range(NP)]
        if not any(c) and not any(f): continue
        j = len(nK); nK.append(list(key) + [g]); nC.append(c); nF.append(f)
        for nm, v in (("OFF", mo), ("EXP", me)):
            if v:
                x = [r2(v[t] * wp[MP[t]][1].get(g, 0)) for t in range(6)]
                if any(x): nM[nm][str(j)] = x

# ---------- conferência ----------
tot = lambda A, ps: sum(sum(a[p] for p in ps) for a in A)
for nome, ps in (("Jul–Out/25", range(12, 16)), ("Jul–Out/26", range(24, 28)), ("tudo", range(NP))):
    print(f"{nome}: categoria {tot(C, ps)/1e6:.3f} → {tot(nC, ps)/1e6:.3f} MM · SCJ {tot(F, ps)/1e6:.3f} → {tot(nF, ps)/1e6:.3f} MM")
print("chaves", len(K), "→", len(nK), "· origem da proporção:", {k: f"{v/sum(cont.values())*100:.1f}%" for k, v in cont.items()})
gq = collections.defaultdict(lambda: [0.0, 0.0, 0.0, 0.0])
for k, c, f in zip(nK, nC, nF): gq[k[4]][0] += c[27]; gq[k[4]][1] += f[27]
for (uf, ban, can), v in IQ.items():
    for g, x in v[0].items(): gq[g][2] += x
    for g, x in v[1].items(): gq[g][3] += x
err = [(g, *v) for g, v in gq.items() if abs(v[0] - v[2]) > max(1000, 0.02 * v[2])]
print("Out/26 por grupo vs IQVIA: grupos", len(gq), "· diferença > 2% (e > R$ 1 mil):", len(err))
for e in sorted(err, key=lambda e: -abs(e[1] - e[3]))[:8]: print("   ", e[0], f"dash {e[1]:,.0f} · IQVIA {e[3]:,.0f}")
for g in ("GRUPO ADM PHARMA", "REDE LUCREMAIS", "GRUPO FARMARCAS", "FARMACIAS ASSOCIADAS", "GRUPO SAO JOAO", "GRUPO CLAMED", "GRUPO NISSEI SA", "GRUPO PANVEL"):
    v = gq.get(g, [0, 0, 0, 0]); print(f"   {g:22s} Out/26 cat dash {v[0]:>12,.0f} · IQVIA {v[2]:>12,.0f} | SCJ dash {v[1]:>11,.0f} · IQVIA {v[3]:>11,.0f}")

# ---------- grava dados ----------
gb = collections.defaultdict(set)
for k in nK: gb[k[4]].add(k[2])
troca("CPT2_KEYS", nK); troca("CPT2_FAB_ALL", nF); troca("CPT2_CAT_ALL", nC); troca("CPT2_MARCA", nM)
troca("CPT2_GRP_BANS", {g: sorted(v) for g, v in sorted(gb.items())}); troca("CPT2_ALL_GRUPOS", sorted(gb))
troca("CPT2_LOJAS", {"|".join(k): [len(LU[k]), len(LS[k])] for k in sorted(LU)})

# ---------- JavaScript: filtro, tabela e lojas pelo grupo da chave ----------
rep("function _cpt2MSPassa(uf, cid, ban, can){", "function _cpt2MSPassa(uf, cid, ban, can, grp){")
rep("  if(M.grp.length && !_cpt2MSPassa._grp[ban]) return false;",
    "  if(M.grp.length && (grp !== undefined ? M.grp.indexOf(grp) < 0 : !_cpt2MSPassa._grp[ban])) return false;   /* grupo da chave; sem grupo (preço médio) → pela bandeira */")
rep("if(_cpt2MSPassa(k[0],k[1],k[2],k[3])) res.push(i); }\n  return res;", "if(_cpt2MSPassa(k[0],k[1],k[2],k[3],k[4])) res.push(i); }\n  return res;")
rep("_cpt2GrpDe(CPT2_KEYS[i][2])", "(CPT2_KEYS[i][4]||_cpt2GrpDe(CPT2_KEYS[i][2]))", 2)
rep("CPT2_KEYS[i][0]+'|'+CPT2_KEYS[i][3]+'|'+CPT2_KEYS[i][2]", "CPT2_KEYS[i][0]+'|'+CPT2_KEYS[i][3]+'|'+CPT2_KEYS[i][2]+'|'+CPT2_KEYS[i][4]", 3)
open(H, "w", encoding="utf-8", newline="").write(h)
print("CNPJs Out/26:", sum(len(v) for v in LU.values()), "c/ categoria ·", sum(len(v) for v in LS.values()), "c/ SCJ · grupos", len(gb))
