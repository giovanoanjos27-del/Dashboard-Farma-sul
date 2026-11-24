"""Araujo (24/11/2026, 2º ajuste):
  1) card 'Estoque por SKU — Araujo': textos e KPIs fixos herdados do DD-Riomed → calculados do ARA_ESTOQUE (29/05/26 × venda Mai/26);
     Ruptura passa a ter dados (ESTOQUE_DATA_MAP.ara); rodapé com a fonte da Araujo
  2) login MG vê tudo o que o SCJ vê (Nielsen, CPT Clientes, Visão Geral 3D no modo SCJ) + Sell Out › Araujo
Uso: python araujo_fix_estoque_mg.py <base.html>"""
import sys, re, json
H = sys.argv[1]; h = open(H, encoding="utf-8", newline="").read()


def rep(a, b, n=1):
    global h
    if h.count(a) != n and h.count(a.replace("\n", "\r\n")) == n: a, b = a.replace("\n", "\r\n"), b.replace("\n", "\r\n")
    assert h.count(a) == n, (h.count(a), a[:100]); h = h.replace(a, b)


assert "ara-kpi-est" not in h, "já aplicado"
p0 = h.index('id="sellout-content-araujo"'); p1 = h.index("</div><!-- fim panel-sellout -->", p0); P = h[p0:p1]


def rp(a, b):
    global P
    assert P.count(a) == 1, (P.count(a), a[:80]); P = P.replace(a, b)


rp("GESTÃO DE ESTOQUE · ATUALIZADO JUN/2026", "GESTÃO DE ESTOQUE · POSIÇÃO 29/05/2026")
rp("Estoque Jun/2026 vs Venda Jun/2025 · Cobertura real por SKU", "Estoque lojas + CD em 29/05/26 × venda Mai/26 · cobertura por SKU")
P = re.sub(r'<div class="u-kpi-lbl">ESTOQUE TOTAL</div><div style="([^"]*)">[^<]*</div><div style="([^"]*)">[^<]*</div>',
           r'<div class="u-kpi-lbl">ESTOQUE TOTAL</div><div id="ara-kpi-est" style="\1">—</div><div id="ara-kpi-est-s" style="\2">—</div>', P, count=1)
P = re.sub(r'<div class="u-kpi-lbl">SKUs CRÍTICOS</div><div style="([^"]*)">[^<]*</div><div style="([^"]*)">[^<]*</div>',
           r'<div class="u-kpi-lbl">SKUs CRÍTICOS</div><div id="ara-kpi-crit" style="\1">—</div><div id="ara-kpi-crit-s" style="\2">—</div>', P, count=1)
P = re.sub(r'<div class="u-kpi-lbl">VENDA JUN/2025</div><div style="([^"]*)">[^<]*</div><div style="([^"]*)">[^<]*</div>',
           r'<div class="u-kpi-lbl">VENDA MAI/2026</div><div id="ara-kpi-vnd" style="\1">—</div><div style="\2">referência da cobertura</div>', P, count=1)
assert P.count("ara-kpi-") >= 5, "KPIs do estoque não encontrados"
i = P.index('<div id="ara-estoque-bars" class="bar-list">') + len('<div id="ara-estoque-bars" class="bar-list">'); j = P.index('<div id="ara-estoque-linha"', i)
k = P.rindex("</div></div>", i, j)   # mantém o fechamento de ara-estoque-bars e ara-estoque-barras
P = P[:i] + P[k:]
P = re.sub(r'<div class="dash-footer"><p>Fonte: Araujo[^<]*</p><p>[^<]*</p></div>',
           '<div class="dash-footer"><p>Fonte: Araujo · Sell-Out Jan/2023–Out/2026 · estoque lojas + CD 29/05/2026</p><p>Novembro 2026</p></div>', P)
h = h[:p0] + P + h[p1:]
rep("  rio:  function(){ return typeof RIO_ESTOQUE  !== 'undefined' ? RIO_ESTOQUE  : []; },",
    "  rio:  function(){ return typeof RIO_ESTOQUE  !== 'undefined' ? RIO_ESTOQUE  : []; },\n  ara:  function(){ return typeof ARA_ESTOQUE  !== 'undefined' ? ARA_ESTOQUE  : []; },")
rep("""function initAraujo(){
  setTimeout(renderAraAnoBars, 100);""", """function initAraujo(){
  setTimeout(renderAraAnoBars, 100);
  /* KPIs do estoque Araujo (29/05/26 × venda Mai/26) */
  (function(){ var E=ARA_ESTOQUE, f=function(n){return n.toLocaleString('pt-BR');}, s=function(id,t){var e=document.getElementById(id); if(e) e.textContent=t;};
    var tE=E.reduce(function(a,d){return a+(d.estoque||0);},0), tL=E.reduce(function(a,d){return a+(d.lojas||0);},0), tV=E.reduce(function(a,d){return a+(d.vendaMar||0);},0);
    var cr=E.filter(function(d){return d.risco==='critico';}).length;
    s('ara-kpi-est', f(tE)); s('ara-kpi-est-s', E.length+' SKUs · lojas '+f(tL)+' + CD '+f(tE-tL)+' · 29/05/26');
    s('ara-kpi-crit', f(cr)); s('ara-kpi-crit-s', 'cobertura < 15 dias ou sem estoque com venda');
    s('ara-kpi-vnd', f(tV)+' un'); }());""")
# ── MG = tudo do SCJ + Sell Out › Araujo ──
rep("""    /* MG: só a aba Sell Out e só o cliente Araujo */
    document.querySelectorAll('.ctab').forEach(function(b){ if(!/'sellout'/.test(b.getAttribute('onclick')||'')) b.style.display='none'; });""",
    """    /* MG: o mesmo que o SCJ vê (Nielsen, CPT Clientes, Visão Geral 3D) + Sell Out só com o cliente Araujo */
    ['sellin','diagnostico','expd','cobertura','plano','ol','distribuicao'].forEach(function(t){ var b=document.querySelector('.ctab[onclick*="\\''+t+'\\'"]'); if(b) b.style.display='none'; });
    var _b3m=document.getElementById('btn-3d'); if(_b3m) _b3m.style.display='';
    var _bgM=document.getElementById('dash-header-badge'); if(_bgM) _bgM.style.display='none';
    ['cob-card-top-cidades','cob-card-evol-mensal','cob-card-posit-comp','cob-card-intocaveis','cob-card-white-space','cob-card-universe'].forEach(function(id){ var e=document.getElementById(id); if(e) e.style.display='none'; });""")
rep("""  /* MG: só Sell Out */
  if(_loginRole==='mg' && id!=='sellout'){ if(typeof showAccessDenied==='function') showAccessDenied(); return; }""",
    """  /* MG: o que o SCJ vê + Sell Out */
  if(_loginRole==='mg' && ['nielsen','cpt','3d','sellout'].indexOf(id)===-1){ if(typeof showAccessDenied==='function') showAccessDenied(); return; }""")
rep("    if(_loginUser!=='Giovano' && _loginRole!=='scj'){ return; }", "    if(_loginUser!=='Giovano' && _loginRole!=='scj' && _loginRole!=='mg'){ return; }")
rep("(_loginRole==='scj'?'?perfil=scj&':'?')", "((_loginRole==='scj'||_loginRole==='mg')?'?perfil=scj&':'?')")
rep("  'MG':      { s1:'12345', s2:'12345', role:'mg' }   /* MG: só Sell Out › Araujo */",
    "  'MG':      { s1:'12345', s2:'12345', role:'mg' }   /* MG: visão SCJ + Sell Out › Araujo */")

# linha 'Total Geral' da planilha de estoque não é SKU
a = h.index("const ARA_ESTOQUE = ") + len("const ARA_ESTOQUE = "); E, n = json.JSONDecoder().raw_decode(h[a:])
E = [e for e in E if not str(e.get("sku", "")).lower().startswith("total")]; h = h[:a] + json.dumps(E, ensure_ascii=False, separators=(",", ":")) + h[a + n:]
a = h.index("var SO_OP = ") + len("var SO_OP = "); so, n = json.JSONDecoder().raw_decode(h[a:])
so["clientes"]["araujo"]["est"] = [e for e in so["clientes"]["araujo"]["est"] if not str(e["n"]).lower().startswith("total")]
h = h[:a] + json.dumps(so, ensure_ascii=False, separators=(",", ":")) + h[a + n:]
# detalhes da barra de estoque: venda Mai/26 e lojas / CD (no lugar de Out/Nov herdados do DD-Riomed)
i = h.index("function renderARAEstoqueBarras"); j = h.index("function setAraEstoqueView", i); F = h[i:j]
F = F.replace("['Venda Out/26',estUn(d.vendaMar),'#D1D5DB'], ['Venda Nov/26 parcial',estUn(d.vendaAbr),'#fbbf24'],",
              "['Venda Mai/26',estUn(d.vendaMar),'#D1D5DB'], ['Lojas c/ estoque',(d.lojasCount||0)+' de '+(d.totalLojas||0),'#fbbf24'], ['Lojas / CD',estUn(d.lojas)+' / '+estUn(d.cdRS),'#D1D5DB'],")
F = F.replace("' (ref: Out/26)'", "' (ref: Mai/26)'")
assert "Venda Out/26" not in F and "ref: Out/26" not in F; h = h[:i] + F + h[j:]
open(H, "w", encoding="utf-8", newline="").write(h); print("ok")
