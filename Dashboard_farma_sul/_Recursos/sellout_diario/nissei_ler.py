"""Nissei · portal PIN (Dashboard › Sell-out, mês atual) → venda do mês por comprador + estoque por produto.
Entrada: texto da página (get_page_text) salvo em arquivo. As linhas da tabela 'Estoque e Vendas por Produto' têm o formato
  EAN Código PRODUTO Ativo  lojasVendas lojasDemanda lojasEstoque estoque estoqueCD demandaLoja  tot_m0 tot_m1 tot_m2 tot_m3  omni×4
Regra: André = OFF!/EXPOSIS (tudo que não é RAID nem LYSOFORM), Edmar = RAID + LYSOFORM (decisão do Giovano 18/11/2026); fora: qualquer POVIDINE (tópico e o inseticida "POVIDINE ... RAID").
R$ = unidades × preço médio do mês de referência (padrão Set/26: André 49,951 · Edmar 28,385).
Saídas: <saida>.tsv (formato do estoque_nissei_*.py) e JSON no stdout.
Uso: python nissei_ler.py <pagina.txt> <saida_sem_ext> [pm_andre] [pm_edmar]"""
import sys, re, csv, json
T, OUT = sys.argv[1:3]
PM_A = float(sys.argv[3]) if len(sys.argv) > 3 else 198905 / 3982
PM_E = float(sys.argv[4]) if len(sys.argv) > 4 else 37043 / 1305
txt = open(T, encoding="utf-8").read()
m = re.search(r"Total\s+Omni\s+(\d{6})\s+(\d{6})\s+(\d{6})\s+(\d{6})", txt)
meses = list(m.groups()) if m else ["m0", "m1", "m2", "m3"]
atual = re.search(r"Sistema Atualizado às ([0-9:]+ \(\d\d/\d\d/\d{4}\))", txt)
rows = []
for l in txt.splitlines():
    r = re.match(r"(\d{13,14}) \d+ (.+?) Ativo ((?:\d+ ?){14})$", l.strip())
    if r:
        n = list(map(int, r.group(3).split())); rows.append([r.group(1), r.group(2)] + n[:10])
assert rows, "nenhuma linha de produto no texto"
H = ["ean", "produto", "lojas_vendas", "lojas_demanda", "lojas_estoque", "estoque", "estoque_cd", "demanda_loja"] + ["tot_" + x for x in meses]
with open(OUT + ".tsv", "w", encoding="utf-8", newline="") as f:
    w = csv.writer(f, delimiter="\t"); w.writerow(H); w.writerows(rows)
def grupo(p):
    if "POVIDINE" in p: return None   # qualquer Povidine (inclui "INSETICIDA POVIDINE ... RAID") não é SCJ
    return "EDMAR" if ("RAID" in p or "LYSOFORM" in p) else "ANDRE"   # Lysoform entra no Edmar (18/11/2026)
v = {"ANDRE": 0, "EDMAR": 0}; est = {"ANDRE": 0, "EDMAR": 0}
for r in rows:
    g = grupo(r[1])
    if g: v[g] += r[8]; est[g] += r[5] + r[6]
res = {"fonte": "Nissei PIN", "atualizado": atual.group(1) if atual else "", "mes": meses[0], "skus": len(rows),
       "andre": {"vol": v["ANDRE"], "rec": round(v["ANDRE"] * PM_A, 2), "estoque": est["ANDRE"]},
       "edmar": {"vol": v["EDMAR"], "rec": round(v["EDMAR"] * PM_E, 2), "estoque": est["EDMAR"]},
       "total_portal_un": sum(r[8] for r in rows)}
print(json.dumps(res, ensure_ascii=False))
