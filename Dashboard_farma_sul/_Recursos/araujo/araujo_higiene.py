"""Araujo › setor Higiene Pessoal no seletor do One Page (24/11/2026), a pedido do Giovano mesmo sem venda:
o setor existe só no cadastro (BASE PROCV: 8 SKUs Method); a base de sell out 2023–Out/2026 e a base de lojas não têm venda deles.
O One Page mostra a lista dos SKUs e o aviso; quando chegar a venda, o setor entra com os mesmos cards dos outros.
Uso: python araujo_higiene.py <base.html>"""
import sys, os, json, re, warnings
import pandas as pd
warnings.filterwarnings("ignore"); sys.stdout.reconfigure(encoding="utf-8")
H = sys.argv[1]; h = open(H, encoding="utf-8", newline="").read(); A = os.path.dirname(os.path.abspath(__file__))


def rep(a, b, n=1):
    global h
    if h.count(a) != n and h.count(a.replace("\n", "\r\n")) == n: a, b = a.replace("\n", "\r\n"), b.replace("\n", "\r\n")
    assert h.count(a) == n, (h.count(a), a[:90]); h = h.replace(a, b)


assert "ARA_HIGIENE" not in h, "já aplicado"
b = pd.read_excel(os.path.join(A, "BASE SELL OUT ARAUJO-23-24-25-26.xlsx"), sheet_name="BASE PROCV")
hp = b[b["SETOR"] == "HIGIENE PESSOAL"]
nome = lambda p: " ".join(w.capitalize() if not re.match(r"^\d", w) else w.lower() for w in str(p).split())
L = [[str(r["Cód Produto DV"]), nome(r["Produto"]), str(int(r["Cód Barra Venda"])), str(r["MARCA"]).title(), str(r["SUB CATEGORIA"]).title(), str(r["Situação Atual"])] for _, r in hp.iterrows()]
print(len(L), "SKUs:", [x[1] for x in L])
rep("""      <button class="stab" onclick="setAraSetor('conveniencia',this)">Conveniência</button>""",
    """      <button class="stab" onclick="setAraSetor('conveniencia',this)">Conveniência</button>
      <button class="stab" onclick="setAraSetor('higiene',this)">Higiene Pessoal</button>""")
rep("var araSetor = 'total';", "/* Araujo › Higiene Pessoal: só cadastro (BASE PROCV), sem venda na base */\nvar ARA_HIGIENE = " + json.dumps(L, ensure_ascii=False) + ";\nvar araSetor = 'total';")
rep("  var X = op1Ctx(), M = X.M;", """  var X = op1Ctx(), M = X.M;
  if(X.cli==='araujo' && typeof araSetor!=='undefined' && araSetor==='higiene' && typeof ARA_HIGIENE!=='undefined'){
    var _th='padding:6px 8px;font-size:9.5px;font-weight:700;color:#64748B;text-transform:uppercase;border-bottom:1.5px solid rgba(94,153,208,0.35);text-align:left;', _td='padding:5px 8px;font-size:11.5px;border-bottom:0.5px solid #E2E8F0;';
    host.innerHTML = '<div class="op1-hdr"><div class="op1-hdr-t">One Page SC Johnson &amp; Araujo – Higiene Pessoal</div><div class="op1-hdr-s">Setor do cadastro SCJ × Araujo (BASE PROCV) · '+ARA_HIGIENE.length+' SKUs</div></div><div class="op1-stripe"></div>'
      + op1Sec('Higiene Pessoal – SKUs cadastrados')
      + op1Box('<b>Ainda sem venda registrada.</b> Os '+ARA_HIGIENE.length+' SKUs de Higiene Pessoal (Method) estão no cadastro da Araujo, mas não aparecem na base de sell out (Jan/23–Out/26) nem na base de lojas. Assim que a venda vier na planilha, o setor ganha os mesmos cards dos outros (sell-out total, marca, estoque e cobertura).')
      + '<div class="card op1-card"><div style="overflow:auto;"><table style="width:100%;border-collapse:collapse;"><thead><tr><th style="'+_th+'">Cód. Araujo</th><th style="'+_th+'">SKU</th><th style="'+_th+'">EAN</th><th style="'+_th+'">Marca</th><th style="'+_th+'">Sub categoria</th><th style="'+_th+'">Situação</th></tr></thead><tbody>'
      + ARA_HIGIENE.map(function(r){ return '<tr>'+r.map(function(c,i){ return '<td style="'+_td+(i===1?'font-weight:600;':'')+'">'+c+'</td>'; }).join('')+'</tr>'; }).join('')
      + '</tbody></table></div></div><div class="op1-fonte">Fonte: BASE SELL OUT ARAUJO-23-24-25-26.xlsx › BASE PROCV (setor HIGIENE PESSOAL).</div>';
    return;
  }""")
open(H, "w", encoding="utf-8", newline="").write(h); print("ok")
