"""Clamed: receita 2026 Ago–Nov estimada = volume × preço Abr/25 (Q5), igual Mai–Jul — fórmulas em SO_Clamed J5:M5.
Uso: python mestre_out26.py <Planilha_Mestre.xlsx>   (faz backup antes em versoes/backup_planilha/)"""
import sys, os, re, shutil, zipfile, datetime
X = sys.argv[1]
# (aba, linha, coluna, valor ou fórmula)
OUT = [
    ("SO_Clamed", 5, "J", "=J9*Q5"), ("SO_Clamed", 5, "K", "=K9*Q5"), ("SO_Clamed", 5, "L", "=L9*Q5"), ("SO_Clamed", 5, "M", "=M9*Q5"),
]
bk = os.path.join(os.path.dirname(X), "versoes", "backup_planilha", "Planilha_Mestre_FarmaSul_Giovano_%s_preClamedRecEst.xlsx" % datetime.datetime.now().strftime("%Y%m%d_%H%M"))
shutil.copy2(X, bk); print("backup:", bk)
z = zipfile.ZipFile(X); files = {n: z.read(n) for n in z.namelist()}; z.close()
wbx = files["xl/workbook.xml"].decode("utf-8"); rels = files["xl/_rels/workbook.xml.rels"].decode("utf-8")
def xml_da_aba(nome):
    m = re.search(r'<sheet [^>]*name="%s"[^>]*r:id="([^"]+)"' % re.escape(nome), wbx)
    rid = m.group(1); t = re.search(r'<Relationship [^>]*Id="%s"[^>]*Target="([^"]+)"' % rid, rels) or re.search(r'<Relationship [^>]*Target="([^"]+)"[^>]*Id="%s"' % rid, rels)
    alvo = t.group(1).lstrip("/"); return alvo if alvo.startswith("xl/") else "xl/" + alvo
col = lambda c: sum((ord(ch) - 64) * 26 ** i for i, ch in enumerate(reversed(c)))
for aba, lin, c, v in OUT:
    p = xml_da_aba(aba); s = files[p].decode("utf-8")
    m = re.search(r'<row [^>]*r="%d"[^>]*>(.*?)</row>' % lin, s, re.S); assert m, (aba, lin)
    row = m.group(0); ref = "%s%d" % (c, lin)
    k = re.search(r'<c r="K%d"([^>]*?)(/>|>.*?</c>)' % lin, row, re.S)
    estilo = re.search(r' s="(\d+)"', k.group(1)).group(1) if (k and ' s="' in k.group(1)) else None
    st = (' s="%s"' % estilo) if estilo else ""
    novo = ('<c r="%s"%s><f>%s</f></c>' % (ref, st, v[1:])) if isinstance(v, str) else ('<c r="%s"%s><v>%s</v></c>' % (ref, st, v))
    ex = re.search(r'<c r="%s"[^>]*?(/>|>.*?</c>)' % ref, row, re.S)
    if ex: row2 = row.replace(ex.group(0), novo)
    else:   # insere na ordem das colunas
        cells = list(re.finditer(r'<c r="([A-Z]+)%d"' % lin, row)); pos = None
        for cm in cells:
            if col(cm.group(1)) > col(c): pos = cm.start(); break
        row2 = (row[:pos] + novo + row[pos:]) if pos is not None else row.replace("</row>", novo + "</row>")
    s = s.replace(row, row2); files[p] = s.encode("utf-8"); print("ok", aba, ref, v)
# recalcular fórmulas ao abrir
wbx2 = re.sub(r'<calcPr([^>]*)/>', lambda m: '<calcPr' + (m.group(1) if 'fullCalcOnLoad' in m.group(1) else m.group(1) + ' fullCalcOnLoad="1"') + '/>', wbx)
files["xl/workbook.xml"] = wbx2.encode("utf-8")
files.pop("xl/calcChain.xml", None)
ct = files["[Content_Types].xml"].decode("utf-8"); files["[Content_Types].xml"] = re.sub(r'<Override PartName="/xl/calcChain.xml"[^>]*/>', '', ct).encode("utf-8")
r2 = files["xl/_rels/workbook.xml.rels"].decode("utf-8"); files["xl/_rels/workbook.xml.rels"] = re.sub(r'<Relationship [^>]*Target="[^"]*calcChain.xml"[^>]*/>', '', r2).encode("utf-8")
tmp = X + ".tmp"
with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zo:
    for n, b in files.items(): zo.writestr(n, b)
os.replace(tmp, X); print("gravado")
