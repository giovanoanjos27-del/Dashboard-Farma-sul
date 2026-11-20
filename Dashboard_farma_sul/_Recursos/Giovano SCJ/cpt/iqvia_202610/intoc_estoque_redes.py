"""Estoque dos 3 intocáveis por loja — Nissei, Panvel e Clamed (últimos estoques por loja recebidos), mesmo critério da São João.
Intocáveis por EAN: Loção Family 200 OE 7894650940006 · Kids 200 (grátis) 7894650005712 · Spray Family 170 OE 7894650009567.
Saída: JSON {rede: {data, uf:{UF:[lojas, c/ SCJ, loc, kids, spr, os3, só2, só1, nenhum]}, falta:[[loja, UF, l, k, s, scj]]}}
Uso: python intoc_estoque_redes.py <pasta _Recursos> <saida.json>"""
import sys, os, glob, json, re
import pandas as pd
R, OUT = sys.argv[1:3]
E = ["7894650940006", "7894650005712", "7894650009567"]
ean = lambda s: s.astype(str).str.replace(r"\.0$", "", regex=True).str.strip()


def resumo(df, loja, uf, cod, qtd, data):
    df = df.copy(); df[cod] = ean(df[cod]); df[qtd] = pd.to_numeric(df[qtd], errors="coerce").fillna(0)
    lojas = df.drop_duplicates(loja)[[loja, uf]]
    scj = set(df[df[qtd] > 0][loja]); tem = [set(df[(df[cod] == e) & (df[qtd] > 0)][loja]) for e in E]
    UF, F = {}, []
    for l, u in lojas.itertuples(index=False):
        t = [int(l in s) for s in tem]; n = sum(t); v = UF.setdefault(str(u), [0] * 9); v[0] += 1
        if l in scj: v[1] += 1; v[2] += t[0]; v[3] += t[1]; v[4] += t[2]; v[[8, 7, 6, 5][n]] += 1
        if n < 3: F.append([str(l), str(u), t[0], t[1], t[2], int(l in scj)])
    F.sort(key=lambda f: (-f[5], sum(f[2:5]), f[1], f[0]))
    tot = [sum(x[j] for x in UF.values()) for j in range(9)]
    print(f"{data}: lojas {tot[0]} · c/ SCJ {tot[1]} · Loção {tot[2]} · Kids {tot[3]} · Spray {tot[4]} · os 3 {tot[5]} ({tot[5]/tot[1]:.1%}) · só2 {tot[6]} só1 {tot[7]} nenhum {tot[8]}")
    return {"data": data, "uf": UF, "falta": F}


out = {}
# Nissei — portal PIN, aba ProdutosLoja (sem CD)
n = pd.read_excel(os.path.join(R, "Giovano SCJ/nissei/FECHAMENTO OUT-26.xlsx"), sheet_name="ProdutosLoja")
n = n[~n["Filial"].astype(str).str.contains(" - CD - ")]
out["GRUPO NISSEI SA"] = resumo(n, "Filial", "UF", "EAN", "Estoque loja", "03/11/2026"); out["GRUPO NISSEI SA"]["fonte"] = "Portal PIN Nissei › ProdutosLoja (Estoque loja)"
# Panvel — Dimed › Estoque CD/Loja (Qtd Est Loja)
p = pd.read_excel(os.path.join(R, "sellout_diario/dados/panvel_estoque_20261119.xlsx"))
p["loja"] = p["Filial - Codigo"].astype(str) + " · " + p["Filial - Cidade"].astype(str)
out["GRUPO PANVEL"] = resumo(p, "loja", "Filial - Uf", "EAN", "Qtd Est Loja", "17/11/2026"); out["GRUPO PANVEL"]["fonte"] = "Portal Dimed › Estoque CD/Loja (Qtd Est Loja)"
# Clamed — portal (4 códigos de fornecedor), Estoque Nov/26
c = pd.concat([pd.read_csv(f, sep=None, engine="python", encoding="latin-1") for f in glob.glob(os.path.join(R, "Giovano SCJ/clamed/*_202611/Estoque_*.csv"))])
c["loja"] = c["cd_filial"].astype(str) + " · " + c["nm_fantasia"].astype(str)
c["uf"] = "Todas"   # o arquivo da Clamed não traz a UF da loja
out["GRUPO CLAMED"] = resumo(c, "loja", "uf", "de_codigo_barras", "qt_saldo_final", "16/11/2026"); out["GRUPO CLAMED"]["fonte"] = "Portal Clamed › Estoque Nov/26 (qt_saldo_final)"
json.dump(out, open(OUT, "w", encoding="utf-8"), ensure_ascii=False)
