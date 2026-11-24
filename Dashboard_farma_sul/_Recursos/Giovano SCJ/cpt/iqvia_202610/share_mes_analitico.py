"""Share IQVIA do One Page (24/11/2026, 5º ajuste): OFF! mês a mês por rede pela visão IQVIA 'Análise Bandeira › Analítico Bandeira'
(filtros Marca = OFF REPELENTE, Categoria = Repelentes, Métrica = R$ CPP; meses Nov/24–Out/26) → share_marca_mes/OFF_MES_REP.xlsx.
Exposis = Total SCJ − OFF! (em Repelentes a SCJ é OFF! + Exposis). Conferido com o slide da Araujo: OFF! idêntico mês a mês e Total − OFF! = Exposis do slide.
Substitui os blocos tracejados (Jan–Abr / Mai–Jun) e os meses vazios (Nov–Dez/25) de São João, Nissei, Panvel e Clamed; Araujo fica com a mesma fonte.
Clamed = DROGARIA CATARINENSE + PRECO POPULAR (ponderado pela categoria de cada bandeira = Demanda Fabricante ÷ Share).
Uso: python share_mes_analitico.py <base.html>"""
import sys, os, re, json, warnings
import pandas as pd
warnings.filterwarnings("ignore"); sys.stdout.reconfigure(encoding="utf-8")
H = sys.argv[1]; h = open(H, encoding="utf-8", newline="").read()
x = pd.read_excel(os.path.join(os.path.dirname(os.path.abspath(__file__)), "share_marca_mes", "OFF_MES_REP.xlsx"), header=2)
m = re.search(r"var SHARE_IQ\s*=\s*", h); S, k = json.JSONDecoder().raw_decode(h[m.end():]); a, b = m.end(), m.end() + k
assert not any(v.get("fonteSerie", "").startswith("IQVIA Analítico") for v in S.values()), "já aplicado"
BAN = {"saojoao": ["SAO JOAO FARMACIAS"], "nissei": ["NISSEI"], "panvel": ["PANVEL"], "clamed": ["DROGARIA CATARINENSE", "PRECO POPULAR"], "araujo": ["ARAUJO"]}
MESES = [202501 + i for i in range(12)] + [202601 + i for i in range(10)]
for cli, bans in BAN.items():
    s = x[x["Bandeira"].isin(bans)].copy(); s["cat"] = s["Demanda Fabricante"] / s["Share"]
    g = s.groupby("Mês")[["Demanda Fabricante", "cat"]].sum()
    off = [round(float(g.loc[mm, "Demanda Fabricante"] / g.loc[mm, "cat"] * 100), 1) if mm in g.index and g.loc[mm, "cat"] else None for mm in MESES]
    D = S[cli]; tot = D["tot"]
    D["off"] = off; D["exp"] = [round(t - o, 1) if (t is not None and o is not None) else None for t, o in zip(tot, off)]
    D.pop("blocos", None)
    D["fonteSerie"] = "IQVIA Analítico Bandeira mês a mês (OFF!: Marca OFF, Repelentes, R$ CPP); Exposis = Total SCJ − OFF!"
    print(cli, "OFF!", off[:6], "…", off[-4:], "· Exposis", D["exp"][:6], "…", D["exp"][-4:])
h = h[:a] + json.dumps(S, ensure_ascii=False, separators=(",", ":")) + h[b:]
open(H, "w", encoding="utf-8", newline="").write(h); print("ok")
