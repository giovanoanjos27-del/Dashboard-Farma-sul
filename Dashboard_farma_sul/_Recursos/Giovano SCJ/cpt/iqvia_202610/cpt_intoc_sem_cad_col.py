"""Distribuição dos intocáveis: tira a coluna 'Total de lojas (cadastro)' da tabela (pedido do Giovano 20/11).
A base 'Total de lojas' continua escolhível nos botões. Uso: python cpt_intoc_sem_cad_col.py <base.html>"""
import sys
H = sys.argv[1]; h = open(H, encoding="utf-8", newline="").read()
def rep(a, b, n=1):
    global h
    assert h.count(a) == n, (h.count(a), a[:90]); h = h.replace(a, b)
rep("+td(nm,'left')+td(Math.round(o.cad).toLocaleString('pt-BR'))+td(o.c.", "+td(nm,'left')+td(o.c.")
rep("'left')+th('Total de lojas (cadastro)')+th('Lojas c/ venda cat.')", "'left')+th('Lojas c/ venda cat.')")
rep("+td('Total do filtro ('+L.length+')','left',true)+td(Math.round(T.cad).toLocaleString('pt-BR'),'right',true)+", "+td('Total do filtro ('+L.length+')','left',true)+")
open(H, "w", encoding="utf-8", newline="").write(h); print("ok")
