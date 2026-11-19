"""Nissei: tira qualquer SKU POVIDINE (não é SCJ) de NS_ESTOQUE_HB, NS_ESTOQUE_ED e NS_COBERTURA. Uso: python nissei_tira_povidine.py <html>"""
import sys, json
H = sys.argv[1]; h = open(H, encoding="utf-8", newline="").read()
for n in ("NS_ESTOQUE_HB", "NS_ESTOQUE_ED", "NS_COBERTURA"):
    tag = "const " + n + " = "
    if tag not in h: print(n, "não existe"); continue
    a = h.index(tag) + len(tag); x, k = json.JSONDecoder().raw_decode(h[a:])
    if not isinstance(x, list): print(n, "não é lista"); continue
    y = [s for s in x if "POVID" not in json.dumps(s, ensure_ascii=False).upper()]
    nl = "\r\n" if "\r\n" in h[a:a + k] else "\n"
    h = h[:a] + json.dumps(y, ensure_ascii=False, indent=2).replace("\n", nl) + h[a + k:]
    print(n, len(x), "->", len(y))
open(H, "w", encoding="utf-8", newline="").write(h)
