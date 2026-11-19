"""São João · aplica Isadora e Caroline do Qlik (saída do sj_qlik_marca.py) em 2025 (Jan–Dez) e 2026 (Jan→mês atual).
2026: monta o JSON do aplicar_sellout.py (planilha mestre linhas 7/8 + arrays SJ_REC/SJ_UNID['2026'], SJC_REC_26/SJC_VOL_26, selo e SO_PARCIAL).
2025: planilha mestre linhas 5/6 de SO_SJoao_Isadora e SO_SJoao_Caroline + arrays SJ_REC/SJ_UNID['2025'], SJC_REC, SJC_VOL.
Uso: python sj_qlik_aplicar.py <sj_marca.json> <dd/mm de ontem> [--simular]"""
import sys, os, json, subprocess
J, ATE = sys.argv[1:3]; SIM = "--simular" in sys.argv
B = os.path.dirname(os.path.abspath(__file__)); BASE = os.path.dirname(os.path.dirname(B))
sys.path.insert(0, BASE); import dashboard_dados as dd
TS = dd.carimbo()
D = json.load(open(J, encoding="utf-8")); M = D["meses"]
idx = lambda y, m: M.index("%d-%02d" % (y, m + 1)) if "%d-%02d" % (y, m + 1) in M else None
I, C = D["isadora"], D["caroline"]
# ── 2026 via aplicar_sellout.py ──
last = max(m for m in range(12) if idx(2026, m) is not None)
lanc = []
for m in range(last + 1):
    k = idx(2026, m)
    lanc += [{"mes": m, "cliente": "SJ_ISA", "rec": I["rec"][k], "vol": I["vol"][k]}, {"mes": m, "cliente": "SJ_CAR", "rec": C["rec"][k], "vol": C["vol"][k]}]
jv = os.path.join(B, "dados", "sj_qlik", "valores_sj_qlik_%s.json" % TS[:8])
json.dump({"rotulo": "SJqlik%s" % TS[:8], "parcial": {"mes": last, "ate": ATE}, "lancamentos": lanc}, open(jv, "w", encoding="utf-8"), ensure_ascii=False)
r = subprocess.run([sys.executable, os.path.join(B, "aplicar_sellout.py"), jv] + (["--simular"] if SIM else []), capture_output=True, text=True, encoding="utf-8")
print(r.stdout[-2500:], r.stderr[-1500:]); assert r.returncode == 0, "aplicar_sellout falhou"
# ── 2025 ──
d = dd.Dashboard()
i25 = [I["rec"][idx(2025, m)] for m in range(12)]; c25 = [C["rec"][idx(2025, m)] for m in range(12)]
ui25 = [I["vol"][idx(2025, m)] for m in range(12)]; uc25 = [C["vol"][idx(2025, m)] for m in range(12)]
d.gravar("const SJ_REC", "2025", [round(i25[m] + c25[m], 2) for m in range(12)]); d.gravar("const SJ_UNID", "2025", [ui25[m] + uc25[m] for m in range(12)])
d.gravar("const SJC_REC =", None, c25); d.gravar("const SJC_VOL =", None, uc25)
print("\n".join(d.log))
cel = []
for m in range(12):
    c = chr(ord("C") + m)
    cel += [("SO_SJoao_Isadora", 5, c, i25[m]), ("SO_SJoao_Isadora", 6, c, ui25[m]), ("SO_SJoao_Caroline", 5, c, c25[m]), ("SO_SJoao_Caroline", 6, c, uc25[m])]
if SIM: print("[--simular] 2025 não gravado"); sys.exit(0)
dd.gravar_planilha(cel, "SJqlik2025", TS)
print(json.dumps(d.salvar("SJqlik", TS, versao_antes=False), ensure_ascii=False))
