"""renderMetaTable (tabela mensal 2024/2025/2026 de cada cliente): mês de SO_PARCIAL vira 'parcial até dd/mm' e, em vez de ▲▼,
mostra '% do mês/25 inteiro' (comparação só quando o mês fechar). Uso: python meta_table_parcial.py <html>"""
import sys
p = sys.argv[1]; h = open(p, encoding="utf-8", newline="").read()
a = """    var noData = v26 == null;

    return '<tr class="u-row-hover">'

      // Month
      + '<td style="padding:9px 12px;font-size:11px;font-weight:600;color:#D1D5DB;white-space:nowrap;width:42px;">'
      + (MESES_ABR[i]||m) + '</td>'"""
b = """    var noData = v26 == null;
    var isParc = !noData && typeof SO_PARCIAL!=='undefined' && SO_PARCIAL && i===SO_PARCIAL.mes;   /* mês em andamento: sem ▲▼, mostra % do mês/25 inteiro */

    return '<tr class="u-row-hover"'+(isParc?' style="background:rgba(245,158,11,0.06);"':'')+'>'

      // Month
      + '<td style="padding:9px 12px;font-size:11px;font-weight:600;color:#D1D5DB;white-space:nowrap;width:42px;">'
      + (MESES_ABR[i]||m) + (isParc?'<div style="font-size:9px;font-weight:700;color:#F59E0B;">parcial até '+SO_PARCIAL.ate+'</div>':'') + '</td>'"""
a2 = """      + (vp26===null
        ? '<span style="color:#2d3748;font-size:10px;">—</span>'"""
b2 = """      + (isParc
        ? '<span style="font-size:10px;font-weight:700;color:#F59E0B;" title="Mês em andamento — comparação só quando fechar">'+(v25>0?Math.round(v26/v25*100)+'% de '+(MESES_ABR[i]||m)+'/25':'parcial')+'</span>'
        : vp26===null
        ? '<span style="color:#2d3748;font-size:10px;">—</span>'"""
for x, y in ((a, b), (a2, b2)):
    x, y = x.replace("\n", "\r\n"), y.replace("\n", "\r\n")
    assert h.count(x) == 1, x[:60]; h = h.replace(x, y)
open(p, "w", encoding="utf-8", newline="").write(h); print("ok")
