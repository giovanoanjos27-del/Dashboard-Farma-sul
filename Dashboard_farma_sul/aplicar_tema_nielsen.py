"""Gera Dashboard_FarmaSul_Giovano_NIELSEN.html: cópia exata do Dashboard_FarmaSul_Giovano.html
com a camada visual Nielsen inserida no final (antes do </body> real).
O arquivo de origem NÃO é alterado. Só CSS é adicionado; nenhum HTML/JS/ID/classe é modificado.

Camadas adicionadas (em <style id="tema-nielsen">):
  1. REMAPEAMENTO DE PALETA (gerado aqui): para cada regra CSS original que pinta o fundo com uma
     cor estrutural antiga (azul-claro), cria uma regra-espelho mais específica com a cor Nielsen.
     Também cobre estilos inline com essas cores. Tons semânticos (verde/vermelho/âmbar) não entram.
  2. tema_nielsen.css (manual): tokens, cabeçalho navy, abas, cards, KPIs, filtros, tabelas.
Uso:  python aplicar_tema_nielsen.py [origem.html] [saida.html]"""
import os, sys, io, re

PASTA = os.path.dirname(os.path.abspath(__file__))
ORIGEM = os.path.join(PASTA, "Dashboard_FarmaSul_Giovano.html")
SAIDA = os.path.join(PASTA, "Dashboard_FarmaSul_Giovano_NIELSEN.html")
CSS = os.path.join(PASTA, "tema_nielsen.css")
MARCA = '<style id="tema-nielsen">'
EMBED_3D = '<script type="text/plain" id="h3d-embed">'

# cor antiga (fundo estrutural) -> cor Nielsen
PALETA = {
    "eaeef4": "#ffffff",  # card antigo -> card branco
    "e4eaf2": "#ffffff",  # KPI antigo -> branco
    "dfecfb": "#f3f5f7",  # fundo da página azul -> cinza muito claro
    "e2e7ef": "#f7f8f9",  # card alternativo -> superfície secundária
    "f4f7fc": "#f7f8f9",
    "d6dce8": "#e8eef3",  # hover
    "dde3ed": "#eef3f7",
    "dce3ec": "#eef3f7",
    "c5d5ec": "#eef3f7",
}
# componentes tratados à mão em tema_nielsen.css — fora do remapeamento
EXCLUIR = re.compile(r"\.header|\.ctab|login-overlay|\.stab|\.sellin-fy-btn|\.filters|(^|[\s>+~,(])th\b", re.I)


def _rgb(hx):
    return "rgb(%d, %d, %d)" % tuple(int(hx[i:i + 2], 16) for i in (0, 2, 4))


def _dividir(sel):
    """Divide a lista de seletores nas vírgulas de topo (ignora vírgulas dentro de [], () e aspas)."""
    partes, atual, prof, aspas = [], [], 0, None
    for ch in sel:
        if aspas:
            if ch == aspas:
                aspas = None
        elif ch in "\"'":
            aspas = ch
        elif ch in "[(":
            prof += 1
        elif ch in "])":
            prof -= 1
        elif ch == "," and prof == 0:
            partes.append("".join(atual)); atual = []; continue
        atual.append(ch)
    partes.append("".join(atual))
    return partes


def _prefixar(parte):
    p = parte.strip()
    if p.lower().startswith("html"):
        return "html:root:root" + p[4:]
    if p.startswith(":root"):
        return ":root:root" + p
    return ":root:root " + p


def remapear(h):
    """Gera o CSS de remapeamento a partir dos <style> originais (sem o 3D embutido e sem strings JS)."""
    corte = h.find(EMBED_3D)
    base = h if corte < 0 else h[:corte]
    cores = "|".join(PALETA)
    decl = re.compile(r"background(?:-color)?\s*:\s*#(" + cores + r")\b", re.I)
    vistos, saida = set(), []
    for bloco in re.findall(r"<style[^>]*>(.*?)</style>", base, re.S | re.I):
        if "' +" in bloco or "'+" in bloco:  # <style> montado dentro de string JS
            continue
        bloco = re.sub(r"/\*.*?\*/", "", bloco, flags=re.S)
        for sel, corpo in re.findall(r"([^{}]+)\{([^{}]*)\}", bloco):
            m = decl.search(corpo)
            sel = sel.strip()
            if not m or sel.startswith("@") or not sel:
                continue
            partes = [p for p in _dividir(sel) if p.strip() and not EXCLUIR.search(p)]
            if not partes:
                continue
            novo = ", ".join(_prefixar(p) for p in partes)
            chave = (novo, m.group(1).lower())
            if chave in vistos:
                continue
            vistos.add(chave)
            saida.append("%s { background-color: %s !important; }" % (novo, PALETA[m.group(1).lower()]))
    # estilos inline (no HTML e os gerados por JS, que o navegador serializa como rgb())
    for hx, nova in PALETA.items():
        alvos = []
        for prop in ("background", "background-color"):
            for v in ("#" + hx, _rgb(hx)):
                for sep in (":", ": "):
                    alvos.append('[style*="%s%s%s" i]' % (prop, sep, v))
        sels = ", ".join(":root:root body " + a for a in alvos)
        saida.append("%s { background-color: %s !important; }" % (sels, nova))
    return "\n".join(saida)


def aplicar(src=ORIGEM, saida=SAIDA):
    h = io.open(src, encoding="utf-8", newline="").read()
    if MARCA in h:
        raise SystemExit("origem já contém o tema Nielsen")
    css = io.open(CSS, encoding="utf-8", newline="").read()
    remap = remapear(h)
    bloco = ("\n" + MARCA + "\n/* ── 0. REMAPEAMENTO DE PALETA (gerado por aplicar_tema_nielsen.py) ── */\n"
             + remap + "\n\n" + css + "\n</style>\n")
    # no <head> real (antes do <body> do dashboard): o tema vale desde o 1º desenho da página,
    # sem mostrar as cores antigas enquanto o navegador lê os 29 MB. Prefixos :root garantem
    # especificidade maior que as regras originais, então a posição não muda o resultado.
    m = re.search(r"\r?\n</head>\r?\n<body>", h)
    i = m.start() if m else -1
    if i < 0 or (h.find(EMBED_3D) >= 0 and i > h.find(EMBED_3D)):
        i = h.rfind("</body>")
    h = (h[:i] + bloco + h[i:]) if i >= 0 else (h + bloco)
    io.open(saida, "w", encoding="utf-8", newline="").write(h)
    return saida, remap.count("\n") + 1


if __name__ == "__main__":
    a = sys.argv[1:]
    s, n = aplicar(*(a[:2] if a else []))
    print("gerado:", s, "| regras de remapeamento:", n)
