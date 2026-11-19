"""Nissei · R$ REAL por comprador a partir do portal PIN (Evolução mensal - Vendas, um filtro de marca por vez).
Regra: André = OFF + EXPOSIS · Edmar = RAID + LYSOFORM (desde 18/11/2026) · POVIDINE fica fora (não é SCJ).
LYSOFORM é opcional no JSON (se faltar, Edmar = só RAID e o resultado avisa).
Entrada: JSON salvo pela rotina com as linhas da tabela "Evolução mensal - Vendas" de cada marca, ex.:
  {"atualizado":"05:02 (12/11/2026)", "OFF":["Novembro de 2026\tR$ 40.166,91", ...], "EXPOSIS":[...], "RAID":[...]}
(cada lista = o resultado do regex de "<Mês> de <ano> R$ <valor>" no document.body.innerText com a marca filtrada).
Saída: JSON no stdout com rec de André e Edmar para cada mês pedido (mes 0=Jan…11=Dez, ano 2026 por padrão).
Uso: python nissei_marca_ler.py <entrada.json> <mes> [<mes> ...]"""
import sys, json, re
J = sys.argv[1]; MESES = [int(x) for x in sys.argv[2:]]
NM = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
D = json.load(open(J, encoding="utf-8"))


def serie(linhas):
    out = {}
    for l in linhas:
        m = re.match(r"\s*(\w+) de (\d{4})\s+R\$\s*([\d.,]+)", l)
        if m and m.group(1) in NM: out[(int(m.group(2)), NM.index(m.group(1)))] = float(m.group(3).replace(".", "").replace(",", "."))
    return out


S = {b: serie(D.get(b, [])) for b in ("OFF", "EXPOSIS", "RAID")}
falta = [b for b, s in S.items() if not s]
assert not falta, "sem dados da(s) marca(s): %s" % falta
L = serie(D.get("LYSOFORM", []))
res = {"fonte": "Nissei PIN (evolução por marca, R$ real; sem Povidine; Lysoform no Edmar)", "atualizado": D.get("atualizado", ""), "meses": {}}
for mes in MESES:
    k = (2026, mes)
    off, exp, raid = S["OFF"].get(k), S["EXPOSIS"].get(k), S["RAID"].get(k)
    if None in (off, exp, raid): res["meses"][mes] = {"erro": "mês %s ausente em alguma marca" % NM[mes]}; continue
    lys = L.get(k, 0.0)
    res["meses"][mes] = {"andre_rec": round(off + exp, 2), "edmar_rec": round(raid + lys, 2), "off": off, "exposis": exp, "raid": raid, "lysoform": lys}
    if not L: res["meses"][mes]["aviso"] = "LYSOFORM não lido: Edmar só com RAID"
print(json.dumps(res, ensure_ascii=False))
