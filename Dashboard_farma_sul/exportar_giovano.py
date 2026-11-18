"""Exporta a cópia única do Giovano: Dashboard_farma_sul/Dashboard_FarmaSul_Giovano.html (nome fixo, sempre sobrescrito).
A aba 3D (apresentacao_3d.html) vai EMBUTIDA dentro do arquivo (iframe srcdoc): abrir só esse arquivo já mostra o 3D
mais novo, sem depender do arquivo separado nem do cache do navegador.
Uso como script:  python exportar_giovano.py [dashboard.html]
Uso em outro script:  import exportar_giovano; exportar_giovano.exportar(caminho_do_dashboard)"""
import os, sys, io

PASTA = os.path.dirname(os.path.abspath(__file__))
MAIN = os.path.join(PASTA, "Dashboard_Farma_Sul_20260512_2220.html")
TRES_D = os.path.join(PASTA, "apresentacao_3d.html")
SAIDA = os.path.join(PASTA, "Dashboard_FarmaSul_Giovano.html")
ANCORA = "var _f3d=document.getElementById('frame-3d'); if(_f3d){"


def exportar(src=MAIN, saida=SAIDA):
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
    if saida == SAIDA:  # mantém a versão com visual Nielsen sempre junto da cópia do Giovano
        try:
            import aplicar_tema_nielsen
            aplicar_tema_nielsen.aplicar()
        except Exception as e:
            print("aviso: tema Nielsen não aplicado:", e)
    return saida


if __name__ == "__main__":
    print("exportado:", exportar(sys.argv[1] if len(sys.argv) > 1 else MAIN))
