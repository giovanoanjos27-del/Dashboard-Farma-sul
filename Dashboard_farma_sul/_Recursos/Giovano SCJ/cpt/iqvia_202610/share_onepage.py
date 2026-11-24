"""Share IQVIA do cliente (24/11/2026, 2º ajuste): sai da visão detalhada (que volta à ordem padrão de cards de todos os clientes)
e entra só no One Page, logo depois do 'Sell-out Total'. Uso: python share_onepage.py <base.html>"""
import sys
H = sys.argv[1]; h = open(H, encoding="utf-8", newline="").read()
def rep(a, b, n=1):
    global h
    if h.count(a) != n and h.count(a.replace("\n", "\r\n")) == n: a, b = a.replace("\n", "\r\n"), b.replace("\n", "\r\n")
    assert h.count(a) == n, (h.count(a), a[:90]); h = h.replace(a, b)
assert "share só no One Page" not in h, "já aplicado"
i = h.index("  if(typeof iqShareRender==='function') setTimeout(function(){ try{ iqShareMontar(); iqShareRender(clientId);"); j = h.index("\n", i)
h = h[:i] + "  /* share IQVIA do cliente: só no One Page (op1Render) */" + h[j:]
i = h.index("(function(){ function ini(){ try{ iqShareMontar(); }"); j = h.index("\n", i)
h = h[:i] + "/* share só no One Page: iqShareMontar não é mais chamado na visão detalhada */" + h[j:]
rep("  h += op1Box(tTxt);\n", "  h += op1Box(tTxt);\n  if(typeof SHARE_IQ!=='undefined' && SHARE_IQ[X.cli]) h += op1Sec('Share no cliente – IQVIA') + iqShareHtml(X.cli);\n")
rep("  host.innerHTML = h;\n", "  host.innerHTML = h;\n  if(typeof SHARE_IQ!=='undefined' && SHARE_IQ[X.cli]) setTimeout(function(){ try{ iqShareRender(X.cli); }catch(e){ console.warn('[iqshare]', e); } }, 50);\n")
open(H, "w", encoding="utf-8", newline="").write(h); print("ok")
