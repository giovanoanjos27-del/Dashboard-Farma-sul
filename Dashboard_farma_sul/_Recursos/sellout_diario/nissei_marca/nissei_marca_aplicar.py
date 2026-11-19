"""Nissei por marca, sem Povidine/Lysoform: André = OFF + EXPOSIS, Edmar = RAID, total = André + Edmar.
2025 (R$ e unidades, Jan–Dez): planilha 2025 x 2024 da Nissei (aba Marca). 2026 (R$, Jan→mês atual): portal PIN, evolução mensal por marca.
Grava na Planilha Mestre (SO_Nissei, SO_Nissei_willian, SO_Nissei_Edmar) e nos arrays NS do dashboard, com backup e versão.
Uso: python nissei_marca_aplicar.py <nissei_marca.json> [--simular]"""
import sys, os, json
J = sys.argv[1]; SIM = "--simular" in sys.argv
BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, BASE); import dashboard_dados as dd
TS = dd.carimbo(); ROT = "NisseiMarca"
D = json.load(open(J, encoding="utf-8"))
r26, r25, u25 = D["r26"], D["r25"], D["u25"]
n26 = len(r26["OFF"])
A26 = [round(r26["OFF"][i] + r26["EXPOSIS"][i], 2) for i in range(n26)]; E26 = [round(r26["RAID"][i], 2) for i in range(n26)]
A25 = [round(r25["OFF"][i] + r25["EXPOSIS"][i], 2) for i in range(12)]; E25 = [round(r25["RAID"][i], 2) for i in range(12)]
UA25 = [u25["OFF"][i] + u25["EXPOSIS"][i] for i in range(12)]; UE25 = u25["RAID"]

# ── planilha mestre (células; gravadas por dd.gravar_planilha no salvar) ──
col = lambda m: chr(ord("C") + m)
cel = []
for m in range(12):
    c = col(m)
    cel += [("SO_Nissei_willian", 5, c, A25[m]), ("SO_Nissei_willian", 6, c, UA25[m]), ("SO_Nissei_Edmar", 5, c, E25[m]), ("SO_Nissei_Edmar", 6, c, UE25[m]),
            ("SO_Nissei", 4, c, round(A25[m] + E25[m], 2)), ("SO_Nissei", 8, c, UA25[m] + UE25[m])]
for m in range(n26):
    c = col(m)
    cel += [("SO_Nissei_willian", 7, c, A26[m]), ("SO_Nissei_Edmar", 7, c, E26[m]),
            ("SO_Nissei", 5, c, f"=SUM(SO_Nissei_willian!{c}7+SO_Nissei_Edmar!{c}7)")]

# ── dashboard: arrays NS (total / andre / edmar) ──
d = dd.Dashboard(); ns = d.pos("const NS =")


def put(sub, key, ano, vals):
    d.gravar(key, ano, vals, de=d.pos(sub, ns), parcial=True)


put("total:", "rec:", "2025", [A25[i] + E25[i] for i in range(12)]); put("total:", "vol:", "2025", [UA25[i] + UE25[i] for i in range(12)])
put("andre:", "rec:", "2025", A25); put("andre:", "vol:", "2025", UA25)
put("edmar:", "rec:", "2025", E25); put("edmar:", "vol:", "2025", UE25)
put("total:", "rec:", "2026", [A26[i] + E26[i] for i in range(n26)]); put("andre:", "rec:", "2026", A26); put("edmar:", "rec:", "2026", E26)
print("\n".join(d.log)); print("mestre:", len(cel), "células")
if SIM: print("[--simular] nada gravado"); sys.exit(0)
print(json.dumps(d.salvar(ROT, TS, planilha=cel), ensure_ascii=False))
