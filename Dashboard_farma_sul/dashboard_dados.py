"""Leitura e gravação dos dados do dashboard Farma Sul — o único lugar que sabe mexer no HTML e na Planilha Mestre.

Usado por _Recursos/sellout_diario/*.py (aplicar_sellout, sj_qlik_aplicar, nissei_marca_aplicar, marca/atualizar_snapshot_3d).

  import dashboard_dados as dd
  d = dd.Dashboard()                                   # lê o HTML principal
  d.ler("const SJ_REC", "2026")                        # → lista de 12 números (None = vazio)
  d.trocar_mes("const PV_REC", "2026", 10, 510503)     # troca um mês
  d.gravar("const SJC_REC =", None, valores)           # troca o array inteiro
  d.gravar("rec:", "2026", valores, de=d.pos("andre:", d.pos("const NS =")), parcial=True)   # só os primeiros meses
  d.salvar("SOdiario20261119")                         # versão antes, grava, versão depois, exporta a cópia do Giovano
  dd.gravar_planilha([("SO_Panvel", 5, "M", 510503)], "SOdiario20261119")

Linha de comando (célula avulsa na planilha, com backup):
  python dashboard_dados.py planilha "SO_Clamed!M9=3351" "SO_Clamed!J5==J9*Q5" --rotulo ClamedNov26
  (valor começando com "=" vira fórmula)
"""
import os, re, sys, shutil, zipfile, datetime

PASTA = os.path.dirname(os.path.abspath(__file__))                 # .../Dashboard_farma_sul
HTML = os.path.join(PASTA, "_Recursos/base/Dashboard_base.html")
XLSX = os.path.join(PASTA, "Planilha_Mestre_FarmaSul_Giovano.xlsx")
VERS = os.path.join(PASTA, "versoes")


def carimbo():
    return datetime.datetime.now().strftime("%Y%m%d_%H%M")


def num(v):
    """Número no formato dos arrays do dashboard: inteiro sem casas, senão até 2 casas."""
    return str(int(v)) if float(v).is_integer() else str(round(v, 2))


class Dashboard:
    """Texto do HTML em memória + registro do que mudou. Nada vai para o disco até salvar()."""

    def __init__(self, caminho=HTML):
        self.caminho = caminho
        self.h = open(caminho, encoding="utf-8", newline="").read()
        self.log = []

    def pos(self, ancora, de=0):
        """Posição de um texto no HTML (para começar a busca dentro de um bloco, ex. NS → andre:)."""
        return self.h.index(ancora, de)

    def _array(self, ancora, ano=None, de=0):
        """Trecho [a, b) do array que vem depois da âncora: o do ano ('2026': [...]) ou o primeiro [...]"""
        i = self.h.index(ancora, de) + len(ancora)
        rx = re.compile(r"'%s'\s*:\s*(\[[^\[\]]*\])" % ano) if ano else re.compile(r"(\[[^\[\]]*\])")
        m = rx.search(self.h, i)
        return m.start(1), m.end(1)

    def ler(self, ancora, ano=None, de=0):
        a, b = self._array(ancora, ano, de)
        return [None if x.strip() in ("null", "") else float(x) for x in self.h[a + 1:b - 1].split(",")]

    def trocar_mes(self, ancora, ano, mes, valor, de=0):
        """Troca um mês (0–11) de um array de 12 posições; o valor entra como veio (str(valor))."""
        a, b = self._array(ancora, ano, de)
        it = self.h[a + 1:b - 1].split(","); assert len(it) == 12, ancora
        antes = it[mes].strip(); it[mes] = str(valor)
        self.h = self.h[:a] + "[" + ",".join(it) + "]" + self.h[b:]
        self.log.append(f"{ancora.strip()[:24]:24s} {ano or '':4s} [{mes}] {antes:>10s} → {valor}")

    def gravar(self, ancora, ano, valores, de=0, parcial=False):
        """Troca o array inteiro, ou com parcial=True só as primeiras posições (o resto fica como está)."""
        a, b = self._array(ancora, ano, de); antigo = self.h[a:b]
        if parcial:
            it = [x.strip() for x in antigo[1:-1].split(",")]
            for i, v in enumerate(valores): it[i] = num(v)
        else:
            it = [num(v) for v in valores]
        novo = "[" + ",".join(it) + "]"
        self.log.append(f"{ancora.strip()[:20]:20s} {ano or '':4s} {antigo[:50]}… → {novo[:50]}…")
        self.h = self.h[:a] + novo + self.h[b:]

    def substituir(self, padrao, novo, flags=0, obrigatorio=True):
        """re.sub de uma ocorrência; acusa erro se o padrão sumiu do HTML (obrigatorio=True)."""
        self.h, n = re.subn(padrao, novo, self.h, count=1, flags=flags)
        assert n or not obrigatorio, "não achei no HTML: " + padrao
        return n

    def salvar(self, rotulo, ts=None, versao_antes=True, planilha=None):
        """versoes/…_pre<rotulo>.html → [planilha] → grava o HTML → versoes/…_<rotulo>.html → cópia do Giovano.
        planilha = lista de células para gravar_planilha (gravada entre a versão-antes e o HTML)."""
        ts = ts or carimbo(); r = {}
        if versao_antes:
            r["backup_html"] = os.path.join(VERS, f"Dashboard_Farma_Sul_{ts}_pre{rotulo}.html"); shutil.copy2(self.caminho, r["backup_html"])
        if planilha:
            r["backup_mestre"] = gravar_planilha(planilha, rotulo, ts)
        open(self.caminho, "w", encoding="utf-8", newline="").write(self.h)
        r["versao"] = os.path.join(VERS, f"Dashboard_Farma_Sul_{ts}_{rotulo}.html"); shutil.copy2(self.caminho, r["versao"])
        r["downloads"] = exportar_copia(self.caminho)
        return r


def exportar_copia(caminho=HTML):
    """Cópia única do Giovano (com o 3D embutido) — exportar_giovano.py da mesma pasta."""
    if PASTA not in sys.path: sys.path.insert(0, PASTA)
    import exportar_giovano
    return exportar_giovano.exportar(caminho)


def gravar_planilha(celulas, rotulo, ts=None, xlsx=XLSX):
    """Grava células na Planilha Mestre editando o XML direto (preserva a formatação). Backup antes em
    versoes/backup_planilha/. celulas = [(aba, linha, coluna, valor)] — valor str começando com '=' vira fórmula.
    O Excel recalcula ao abrir (fullCalcOnLoad; calcChain removido)."""
    ts = ts or carimbo()
    bk = os.path.join(os.path.dirname(xlsx), "versoes", "backup_planilha", f"Planilha_Mestre_FarmaSul_Giovano_{ts}_pre{rotulo}.xlsx"); shutil.copy2(xlsx, bk)
    z = zipfile.ZipFile(xlsx); files = {n: z.read(n) for n in z.namelist()}; z.close()
    wbx = files["xl/workbook.xml"].decode("utf-8"); rels = files["xl/_rels/workbook.xml.rels"].decode("utf-8")

    def xml_da_aba(nome):
        rid = re.search(r'<sheet [^>]*name="%s"[^>]*r:id="([^"]+)"' % re.escape(nome), wbx).group(1)
        t = re.search(r'<Relationship [^>]*Id="%s"[^>]*Target="([^"]+)"' % rid, rels) or re.search(r'<Relationship [^>]*Target="([^"]+)"[^>]*Id="%s"' % rid, rels)
        a = t.group(1).lstrip("/"); return a if a.startswith("xl/") else "xl/" + a
    col = lambda c: sum((ord(ch) - 64) * 26 ** i for i, ch in enumerate(reversed(c)))
    # formato de número de cada estilo (cellXfs) — para herdar o formato de um mês vizinho, não o do rótulo da linha
    sty = files["xl/styles.xml"].decode("utf-8"); xfs = re.search(r"<cellXfs[^>]*>(.*?)</cellXfs>", sty, re.S).group(1)
    nf = [int((re.search(r'numFmtId="(\d+)"', x) or re.search("()", "")).group(1) or 0) for x in re.findall(r"<xf\b[^>]*>", xfs)]

    def estilo(row, lin, c):
        """Estilo da célula mais próxima nas colunas de mês (C–N) que tenha formato de número; senão o da própria
        célula; senão o da primeira célula da linha."""
        cand = []
        for cm in re.finditer(r'<c r="([A-Z]+)%d"([^>]*?)(?:/>|>)' % lin, row):
            k = col(cm.group(1)); s_ = re.search(r' s="(\d+)"', cm.group(2))
            if s_ and 3 <= k <= 14 and cm.group(1) != c and int(s_.group(1)) < len(nf) and nf[int(s_.group(1))]:
                cand.append((abs(k - col(c)), k > col(c), s_.group(1)))
        if cand: return ' s="%s"' % min(cand)[2]
        for alvo in (r'<c r="%s%d"([^>]*?)(/>|>.*?</c>)' % (c, lin), r'<c r="[A-Z]+%d"([^>]*?)(/>|>.*?</c>)' % lin):
            m = re.search(alvo, row, re.S); s_ = re.search(r' s="(\d+)"', m.group(1)) if m else None
            if s_: return ' s="%s"' % s_.group(1)
        return ""
    for aba, lin, c, v in celulas:
        p = xml_da_aba(aba); s = files[p].decode("utf-8")
        row = re.search(r'<row [^>]*r="%d"[^>]*>(.*?)</row>' % lin, s, re.S).group(0); ref = "%s%d" % (c, lin)
        st = estilo(row, lin, c)
        novo = ('<c r="%s"%s><f>%s</f></c>' % (ref, st, v[1:])) if isinstance(v, str) else ('<c r="%s"%s><v>%s</v></c>' % (ref, st, v))
        ex = re.search(r'<c r="%s"[^>]*?(/>|>.*?</c>)' % ref, row, re.S)
        if ex: row2 = row.replace(ex.group(0), novo)
        else:
            pos = next((cm.start() for cm in re.finditer(r'<c r="([A-Z]+)%d"' % lin, row) if col(cm.group(1)) > col(c)), None)
            row2 = (row[:pos] + novo + row[pos:]) if pos is not None else row.replace("</row>", novo + "</row>")
        files[p] = s.replace(row, row2).encode("utf-8")
    wbx2 = re.sub(r'<calcPr([^>]*)/>', lambda m: '<calcPr' + (m.group(1) if 'fullCalcOnLoad' in m.group(1) else m.group(1) + ' fullCalcOnLoad="1"') + '/>', wbx)
    files["xl/workbook.xml"] = wbx2.encode("utf-8"); files.pop("xl/calcChain.xml", None)
    ct = files["[Content_Types].xml"].decode("utf-8"); files["[Content_Types].xml"] = re.sub(r'<Override PartName="/xl/calcChain.xml"[^>]*/>', '', ct).encode("utf-8")
    r2 = files["xl/_rels/workbook.xml.rels"].decode("utf-8"); files["xl/_rels/workbook.xml.rels"] = re.sub(r'<Relationship [^>]*Target="[^"]*calcChain.xml"[^>]*/>', '', r2).encode("utf-8")
    tmp = xlsx + ".tmp"
    with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zo:
        for n, b in files.items(): zo.writestr(n, b)
    os.replace(tmp, xlsx); return bk


if __name__ == "__main__":
    a = sys.argv[1:]
    if not a or a[0] != "planilha" or "--rotulo" not in a:
        sys.exit(__doc__)
    k = a.index("--rotulo"); rot = a[k + 1]; cel = []
    for x in a[1:k] + a[k + 2:]:
        m = re.fullmatch(r"(.+)!([A-Z]+)(\d+)=(.+)", x); assert m, "formato: Aba!M9=valor  (ou Aba!J5==J9*Q5 para fórmula)"
        v = m.group(4); v = v if v.startswith("=") else (float(v) if "." in v else int(v))
        cel.append((m.group(1), int(m.group(3)), m.group(2), v))
    print("backup:", gravar_planilha(cel, rot)); print("gravado:", cel)
