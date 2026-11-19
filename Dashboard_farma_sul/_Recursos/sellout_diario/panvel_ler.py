"""Panvel · portal Dimed › Relatório de Venda por Loja (fornecedores AM 2359192 + Cajamar 5279922, período 'Real' = mês atual).
Soma 'Valor Total de Venda' e 'Quantidade Vendida' do relatório exportado (RelatorioVendaPorLoja-AAAAMM-parte-1_*.xlsx).
Uso: python panvel_ler.py <relatorio.xlsx>   → JSON no stdout"""
import sys, json, warnings
import openpyxl
warnings.filterwarnings("ignore")
ws = openpyxl.load_workbook(sys.argv[1], read_only=True, data_only=True).worksheets[0]
rows = list(ws.iter_rows(values_only=True)); ix = {c: i for i, c in enumerate(rows[0])}
cv = next(c for c in ix if c and "Valor Total" in str(c)); cq = next(c for c in ix if c and "Quantidade" in str(c))
cm = next(c for c in ix if c and str(c).startswith("M"))
def num(x):
    if isinstance(x, (int, float)): return float(x)
    s = str(x or "").replace("R$", "").strip()
    if not s or s in ("-", "—"): return 0.0
    if "," in s: s = s.replace(".", "").replace(",", ".")
    return float(s)
rec = sum(num(r[ix[cv]]) for r in rows[1:] if r); vol = sum(num(r[ix[cq]]) for r in rows[1:] if r)
forn = sorted({str(r[ix["Cód. do Fornecedor"]]) for r in rows[1:] if r} if "Cód. do Fornecedor" in ix else [])
mes = sorted({r[ix[cm]] for r in rows[1:] if r})
print(json.dumps({"fonte": "Panvel Dimed", "linhas": len(rows) - 1, "mes": mes, "fornecedores": forn, "rec": round(rec, 2), "vol": int(vol)}, ensure_ascii=False))
