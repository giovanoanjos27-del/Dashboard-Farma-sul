"""Card 'Estoque dos intocáveis nas lojas' sai do CPT Clientes e vai para o Sell Out de cada cliente (análise detalhada):
São João → panel-saojoao, Nissei → panel-nissei, Clamed → panel-clamed, Panvel → panel-panvel, logo abaixo do card de estoque
(depois do bloco <pre>-estoque-cobertura). Desenhado no carregamento, com todas as UFs. Uso: python so_intoc_estq_clientes.py <base.html>"""
import sys, re
H = sys.argv[1]; h = open(H, encoding="utf-8", newline="").read()
def rep(a, b, n=1):
    global h
    assert h.count(a) == n, (h.count(a), a[:90]); h = h.replace(a, b)

# 1) fora do CPT
rep("    +_cpt2SjEstqHtml(idx)\n", "")
# 2) função aceita idx nulo (todas as UFs)
rep("  var ufs = {}; idx.forEach(function(i){ if(CPT2_KEYS[i][4]===G) ufs[CPT2_KEYS[i][0]]=1; });\n  var E = CPT2_REDE_ESTQ[G],",
    "  var ufs = {}; if(idx) idx.forEach(function(i){ if(CPT2_KEYS[i][4]===G) ufs[CPT2_KEYS[i][0]]=1; }); else Object.keys(CPT2_REDE_ESTQ[G].uf).forEach(function(u){ ufs[u]=1; });\n  var E = CPT2_REDE_ESTQ[G],")
rep("Aqui conta quem <b>tem na prateleira</b>; o painel acima conta quem <b>vendeu</b> (IQVIA).",
    "Aqui conta quem <b>tem na prateleira</b>; a distribuição por venda (IQVIA) está no CPT Clientes.")
# 3) containers no Sell Out de cada cliente
ALVO = {"sj": "GRUPO SAO JOAO", "ns": "GRUPO NISSEI SA", "cl": "GRUPO CLAMED", "pv": "GRUPO PANVEL"}
for pre in ALVO:
    i = h.index(f'id="{pre}-estoque-cobertura"'); a = h.rfind("<div", 0, i); d = 0
    for m in re.finditer(r"<div\b|</div>", h[a:]):
        d += 1 if m.group() == "<div" else -1
        if d == 0: j = a + m.end(); break
    h = h[:j] + f'\n  <div id="{pre}-intoc-estq" class="so-intoc-estq"></div>' + h[j:]
JS = ("\n/* estoque dos intocáveis por loja no Sell Out de cada cliente (análise detalhada) */\n"
      "function _soIntocEstqRender(){ var A=" + str(ALVO).replace("'", '"') + "; Object.keys(A).forEach(function(p){ var e=document.getElementById(p+'-intoc-estq'); "
      "if(e && typeof CPT2_REDE_ESTQ!=='undefined' && CPT2_REDE_ESTQ[A[p]]) e.innerHTML=_cpt2RedeEstqHtml(null, A[p]); }); }\n"
      "window.addEventListener('load', function(){ try{ _soIntocEstqRender(); }catch(e){ console.warn('[dashboard]', e); } });\n")
rep("function _cpt2SjEstqHtml(idx){", JS.strip("\n") + "\nfunction _cpt2SjEstqHtml(idx){")
open(H, "w", encoding="utf-8", newline="").write(h); print("ok")
