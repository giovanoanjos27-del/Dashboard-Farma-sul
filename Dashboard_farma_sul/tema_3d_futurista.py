"""Tema "Obsidiana Holográfica" para a aba 3D — troca SÓ cores/acabamento (nada de estrutura, dados ou lógica).
Uso:  python tema_3d_futurista.py [origem.html] [saida.html]
Padrão: gera o ESBOÇO esboco_3d_futurista.html a partir de apresentacao_3d.html (o original não muda)."""
import os, sys, io, re

PASTA = os.path.dirname(os.path.abspath(__file__))
ORIGEM = os.path.join(PASTA, "apresentacao_3d.html")
SAIDA = os.path.join(PASTA, "esboco_3d_futurista.html")

# three.js (0x......) — dourado -> ciano/gelo, chão e grade -> obsidiana/ciano escuro
HEX3 = {
    "0x06060a": "0x03050a",  # névoa
    "0xfff1cc": "0xcfe8ff",  # luz ambiente
    "0xffe2a0": "0xbfe3ff",  # luz direcional
    "0xf5c542": "0x22d3ee",  # GOLD (luz pontual / emissivo)
    "0x14100a": "0x050a14",  # piso
    "0x3a2f14": "0x0e4a5c",  # grade principal
    "0x1a1508": "0x07202b",  # grade secundária
    "0xcfc6b0": "0xaab8cc",  # ano anterior (vidro prateado)
    "0xf3ead2": "0xe6f1ff",  # aresta ano anterior
    "0xc9961f": "0x0891b2",  # corpo da barra
    "0xffe9a8": "0xa5f3fc",  # arestas
    "0xffd666": "0x67e8f9",  # bloco tendência
}
# CSS / textos HTML
HEXC = {
    "#06060a": "#03050a", "#f5c542": "#22d3ee", "#ffdf7a": "#67e8f9", "#ffe9a8": "#a5f3fc",
    "#f3ead2": "#e6f1ff", "#9a8f74": "#7d8ba3", "#d8cfb8": "#b8c4d6", "#c9961f": "#0891b2",
    "#b8891c": "#0e7490", "#fff8e6": "#ecfeff", "#fff1b8": "#cffafe",
}
RGBA = {
    "rgba(245,197,66": "rgba(34,211,238", "rgba(255,214,102": "rgba(103,232,249",
    "rgba(255,233,168": "rgba(165,243,252", "rgba(14,11,6": "rgba(5,8,16",
    "rgba(20,16,8": "rgba(6,12,24", "rgba(12,10,6": "rgba(4,8,16",
    "rgba(207,198,176": "rgba(184,196,214",
}
# acabamento extra (só visual): névoa azul-violeta no fundo, linhas de varredura sutis, brilho holográfico
EXTRA = """
<style id="tema-obsidiana">
html,body{background:radial-gradient(1200px 700px at 50% 38%,#0a1a33 0%,#050913 55%,#03050a 100%) !important}
body:after{content:"";position:fixed;inset:0;pointer-events:none;z-index:1;
  background:repeating-linear-gradient(0deg,rgba(103,232,249,.025) 0 1px,transparent 1px 3px),
             radial-gradient(900px 500px at 85% 0%,rgba(139,92,246,.10),transparent 60%)}
#cv{background:transparent}
.tt h1{letter-spacing:.04em;text-shadow:0 0 18px rgba(34,211,238,.25)}
.tt h1 b{background:linear-gradient(90deg,#22d3ee,#a5f3fc 55%,#a78bfa);-webkit-background-clip:text;background-clip:text;color:transparent}
.k,#det,.seg{box-shadow:0 0 0 1px rgba(34,211,238,.06) inset,0 10px 30px rgba(0,0,0,.45)}
.k:after{content:"";position:absolute;right:-1px;bottom:-1px;width:10px;height:10px;border-right:2px solid rgba(167,139,250,.8);border-bottom:2px solid rgba(167,139,250,.8)}
.seg button.on{box-shadow:inset 0 -2px 0 #22d3ee,0 0 14px rgba(34,211,238,.25)}
</style>
"""


def aplicar(src=ORIGEM, saida=SAIDA):
    h = io.open(src, encoding="utf-8", newline="").read()
    for a, b in HEX3.items():
        h = re.sub(re.escape(a), b, h, flags=re.I)
    for a, b in HEXC.items():
        h = re.sub(re.escape(a) + r"\b", b, h, flags=re.I)
    for a, b in RGBA.items():
        h = h.replace(a, b)
    i = h.find("</head>")
    h = (h[:i] + EXTRA + h[i:]) if i >= 0 else (EXTRA + h)
    io.open(saida, "w", encoding="utf-8", newline="").write(h)
    return saida


if __name__ == "__main__":
    a = sys.argv[1:]
    print("gerado:", aplicar(*(a[:2] if a else [])))
