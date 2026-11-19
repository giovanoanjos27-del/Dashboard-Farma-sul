"""São João · Qlik (Portal SJ › Relatórios Qlik › Indicadores Venda › Detalhes Vendas, dimensões Ano Mês Venda + Produto, Baixar › Dados).
Agrupa por mês × marca (pelo nome do produto) e por compradora: Isadora = OFF + EXPOSIS + RAID · Caroline = LYSOFORM + GLADE + PATO + PATO BLOCK.
Usa "Valor Venda" (R$) e "Quantidade Venda" (un). Saída JSON: {"meses":["2025-01",...], "marca":{m:{"rec":[...],"vol":[...]}}, "isadora":{...}, "caroline":{...}}.
Uso: python sj_qlik_marca.py <export.xlsx> <saida.json> [--ate AAAA-MM-DD]
--ate: se o export tiver a coluna "Data Venda", ignora vendas depois dessa data (fecha o mês parcial no mesmo corte do dashboard)."""
import sys, json, warnings
import openpyxl
warnings.filterwarnings("ignore")
X, OUT = sys.argv[1:3]
ATE = sys.argv[sys.argv.index("--ate") + 1] if "--ate" in sys.argv else None
MES = {"Jan": 1, "Fev": 2, "Mar": 3, "Abr": 4, "Mai": 5, "Jun": 6, "Jul": 7, "Ago": 8, "Set": 9, "Out": 10, "Nov": 11, "Dez": 12}


def marca(p):
    p = p.upper()
    if "PATO" in p and ("BLOCK" in p or "BLOQUEADOR" in p): return "PATO BLOCK"
    for k, m in (("EXPOS", "EXPOSIS"), ("RAID", "RAID"), ("OFF", "OFF!"), ("LYSOFORM", "LYSOFORM"), ("GLADE", "GLADE"), ("PATO", "PATO")):
        if k in p: return m
    raise ValueError("produto sem marca: " + p)


rows = list(openpyxl.load_workbook(X, read_only=True, data_only=True).worksheets[0].iter_rows(values_only=True))
H = {c: i for i, c in enumerate(rows[0])}
agg = {}
for r in rows[1:]:
    if not r or not r[H["Ano Mês Venda"]]: continue
    if ATE and "Data Venda" in H and r[H["Data Venda"]] is not None and str(r[H["Data Venda"]])[:10] > ATE: continue
    mn, an = str(r[H["Ano Mês Venda"]]).split()
    k = "%s-%02d" % (an, MES[mn]); m = marca(str(r[H["Produto"]]))
    a = agg.setdefault(m, {}).setdefault(k, [0.0, 0])
    a[0] += float(r[H["Valor Venda"]] or 0); a[1] += int(r[H["Quantidade Venda"]] or 0)
meses = sorted({k for d in agg.values() for k in d})
out = {"meses": meses, "marca": {}}
for m, d in agg.items():
    out["marca"][m] = {"rec": [round(d.get(k, [0, 0])[0], 2) for k in meses], "vol": [d.get(k, [0, 0])[1] for k in meses]}
for nome, ms in (("isadora", ("OFF!", "EXPOSIS", "RAID")), ("caroline", ("LYSOFORM", "GLADE", "PATO", "PATO BLOCK"))):
    out[nome] = {"rec": [round(sum(out["marca"].get(m, {"rec": [0] * len(meses)})["rec"][i] for m in ms), 2) for i in range(len(meses))],
                 "vol": [sum(out["marca"].get(m, {"vol": [0] * len(meses)})["vol"][i] for m in ms) for i in range(len(meses))]}
json.dump(out, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("meses", meses[0], "→", meses[-1], "·", len(rows) - 1, "linhas · marcas", sorted(agg))
