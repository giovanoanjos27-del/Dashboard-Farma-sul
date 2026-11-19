"""Aplica valores de Sell Out (2026) na Planilha Mestre (XML direto, preserva formatação) e no dashboard, com backup e versão.
Entrada: JSON
  {"parcial": {"mes": 10, "ate": "11/11", "cli": {"ddgaucha": "10/11"}} | null,   # mês parcial (0=Jan … 10=Nov) ou null quando o mês fechou; "cli" opcional = data por cliente quando difere (sem "cli" mantém a do dashboard)
   "lancamentos": [ {"mes": 10, "cliente": "SJ_ISA", "rec": 696869, "vol": 31332}, ... ],
   "rotulo": "SOdiario20261112"}
  clientes: SJ_ISA, SJ_CAR (os dois juntos → SJ total), NS_AND, NS_EDM (juntos → Nissei total), PV, GCH, GAM, RIO, CL (só vol)
Mestre: aba/linhas por cliente (rec, vol); coluna do mês = C + mes (Jul=I, Out=L, Nov=M).
Dashboard: SJ_REC/SJ_UNID['2026'], SJC_REC_26/SJC_VOL_26, NS.total/andre/edmar, PV_*, GAUCHA_*, GAM_* ['2026'], RIOMED_*_2026, CL_VOL_2026.
Uso: python aplicar_sellout.py <valores.json> [--simular]"""
import sys, os, re, json, datetime
J = sys.argv[1]; SIM = "--simular" in sys.argv
BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))      # .../Dashboard_farma_sul
sys.path.insert(0, BASE); import dashboard_dados as dd
TS = dd.carimbo()
D = json.load(open(J, encoding="utf-8")); ROT = D.get("rotulo", "SOdiario")
L = {}
for x in D["lancamentos"]: L.setdefault(x["mes"], {})[x["cliente"]] = x
for mes, c in L.items():
    assert ("SJ_ISA" in c) == ("SJ_CAR" in c), "SJ_ISA e SJ_CAR precisam vir juntos"
    assert ("NS_AND" in c) == ("NS_EDM" in c), "NS_AND e NS_EDM precisam vir juntos"
MESTRE = {"SJ_ISA": ("SO_SJoao_Isadora", 7, 8), "SJ_CAR": ("SO_SJoao_Caroline", 7, 8), "NS_AND": ("SO_Nissei_willian", 7, 8),
          "NS_EDM": ("SO_Nissei_Edmar", 7, 8), "PV": ("SO_Panvel", 5, 9), "GCH": ("SO_DDGaúcha", 5, 9), "GAM": ("SO_DDGAM", 5, 9),
          "RIO": ("SO_DDRiomed", 5, 9), "CL": ("SO_Clamed", None, 9)}

# ── planilha mestre (células; gravadas por dd.gravar_planilha no salvar) ──
cel = []
for mes, c in L.items():
    cc = chr(ord("C") + mes)
    for k, x in c.items():
        aba, lr, lv = MESTRE[k]
        if lr and x.get("rec") is not None: cel.append((aba, lr, cc, x["rec"]))
        if x.get("vol") is not None: cel.append((aba, lv, cc, x["vol"]))
    if "NS_AND" in c: cel += [("SO_Nissei", 5, cc, f"=SUM(SO_Nissei_willian!{cc}7+SO_Nissei_Edmar!{cc}7)"), ("SO_Nissei", 9, cc, f"=SUM(SO_Nissei_willian!{cc}8+SO_Nissei_Edmar!{cc}8)")]

# ── dashboard ──
d = dd.Dashboard(); troca = d.trocar_mes
for M, c in L.items():
    if "SJ_ISA" in c:
        I, C = c["SJ_ISA"], c["SJ_CAR"]
        troca("const SJ_REC", "2026", M, round(I["rec"] + C["rec"], 2)); troca("const SJ_UNID", "2026", M, I["vol"] + C["vol"])
        troca("const SJC_REC_26 =", None, M, C["rec"]); troca("const SJC_VOL_26 =", None, M, C["vol"])
    if "NS_AND" in c:
        A, E = c["NS_AND"], c["NS_EDM"]; ns = d.pos("const NS =")
        for sub, (r, v) in (("total:", (round(A["rec"] + E["rec"], 2), A["vol"] + E["vol"])), ("andre:", (A["rec"], A["vol"])), ("edmar:", (E["rec"], E["vol"]))):
            s = d.pos(sub, ns); troca("vol:", "2026", M, v, de=s); troca("rec:", "2026", M, r, de=d.pos(sub, ns))
    for k, (ar, av) in {"PV": ("const PV_REC", "const PV_VOL"), "GCH": ("const GAUCHA_REC", "const GAUCHA_VOL"), "GAM": ("const GAM_REC", "const GAM_VOL")}.items():
        if k in c: troca(ar, "2026", M, c[k]["rec"]); troca(av, "2026", M, c[k]["vol"])
    if "RIO" in c: troca("const RIOMED_REC_2026 =", None, M, c["RIO"]["rec"]); troca("const RIOMED_VOL_2026 =", None, M, c["RIO"]["vol"])
    if "CL" in c: troca("const CL_VOL_2026 =", None, M, c["CL"]["vol"])
P = D.get("parcial")
d.substituir(r"var SO_PARCIAL = [^;]*;", "var SO_PARCIAL = %s;" % ("{mes:%d, ate:'%s'}" % (P["mes"], P["ate"]) if P else "null"))
if P and "cli" in P:   # data do parcial por cliente (chave = valor do seletor do Sell Out, ex. {"ddgaucha":"14/11"}); sem "cli" mantém a atual
    d.substituir(r"var SO_PARCIAL_CLI = \{[^}]*\};", "var SO_PARCIAL_CLI = %s;" % json.dumps(P["cli"], ensure_ascii=False).replace('"', "'"))
hoje = datetime.date.today().strftime("%d/%m/%Y")
d.substituir(r"✓ Atualizado \d\d/\d\d/\d{4}", "✓ Atualizado " + hoje)
print("\n".join(d.log)); print("SO_PARCIAL =", P, "· selo", hoje); print("mestre:", len(cel), "células")
if SIM: print("[--simular] nada gravado"); sys.exit(0)
print(json.dumps(d.salvar(ROT, TS, planilha=cel), ensure_ascii=False))
