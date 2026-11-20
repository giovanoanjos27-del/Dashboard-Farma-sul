"""Gera o ÚNICO arquivo do Giovano: Dashboard_farma_sul/Dashboard_FarmaSul_Giovano.html (nome fixo, sempre sobrescrito)
e o index.html do site (cópia idêntica, na pasta acima). Desde 20/11/2026 não existe mais a cópia _NIELSEN separada.
  base editável (os scripts gravam aqui): _Recursos/base/Dashboard_base.html  — não é para abrir
  → aba 3D (apresentacao_3d.html) EMBUTIDA (iframe srcdoc) → visual Nielsen (aplicar_tema_nielsen) → Giovano → index.html
Uso como script:  python exportar_giovano.py [base.html]
Uso em outro script:  import exportar_giovano; exportar_giovano.exportar(caminho_da_base)"""
import os, sys, io, shutil

PASTA = os.path.dirname(os.path.abspath(__file__))
MAIN = os.path.join(PASTA, "_Recursos/base/Dashboard_base.html")
TRES_D = os.path.join(PASTA, "apresentacao_3d.html")
SAIDA = os.path.join(PASTA, "Dashboard_FarmaSul_Giovano.html")
INDEX = os.path.join(os.path.dirname(PASTA), "index.html")
ANCORA = "var _f3d=document.getElementById('frame-3d'); if(_f3d){"


def exportar(src=MAIN, saida=SAIDA, index=True):
    h = io.open(src, encoding="utf-8", newline="").read()
    d3 = io.open(TRES_D, encoding="utf-8", newline="").read()
    if ANCORA not in h:
        raise SystemExit("exportar_giovano: âncora do iframe 3D não encontrada no dashboard")
    # 3D como texto dentro de <script type="text/plain">: "</script" escapado para não fechar o bloco
    bloco = '<script type="text/plain" id="h3d-embed">' + d3.replace("</script", "<\\/script") + "</script>\n"
    h = h.replace(ANCORA, "var _f3d=document.getElementById('frame-3d'); if(_f3d&&!_f3d.srcdoc){ var _e3d=document.getElementById('h3d-embed'); "
                  "if(_e3d){ _f3d.removeAttribute('src'); _f3d.srcdoc=_e3d.textContent.replace(/<\\\\\\/script/g,'</'+'script'); } } if(_f3d&&!_f3d.srcdoc){", 1)
    i = h.rfind("</body>")
    h = (h[:i] + bloco + h[i:]) if i >= 0 else (h + bloco)
    io.open(saida, "w", encoding="utf-8", newline="").write(h)
    # visual Nielsen no próprio arquivo do Giovano (sem cópia separada)
    if PASTA not in sys.path: sys.path.insert(0, PASTA)
    import aplicar_tema_nielsen
    aplicar_tema_nielsen.aplicar(saida, saida)
    if index and saida == SAIDA:
        shutil.copyfile(saida, INDEX)   # site = o mesmo arquivo do Giovano
    return saida


if __name__ == "__main__":
    print("exportado:", exportar(sys.argv[1] if len(sys.argv) > 1 else MAIN), "+ index.html")
