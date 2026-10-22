"""
atualizar_nielsen.py — Atualiza a aba Nielsen do Dashboard Farma Sul a partir da base NielsenIQ nova.

Fonte aceita:
  • HTML PEGASUS  "Dashboard Nielsen - AC.PC.HC UXUI*.html"  (base "Base Padrão dash - SetXX" embutida)
  • xlsx "Base Padrão dash - XXXyy.xlsx"  (leitor por cabeçalho — ver load_xlsx; Odor Block vem de outro
    arquivo, então no modo xlsx o OB_DATA só é atualizado se --odor-block for passado)

O que faz (a cada execução):
  1. Detecta o último mês da base e o FYTD (ex.: Out/26 → FYTD27 = Jul–Out, rolling Nov/25–Out/26).
  2. Regenera os blocos de dados: MKTSHARE_OVERVIEW, SHR_TREND_DATA, NQ_PR, SKU_MKT_DATA, SKU_MKT_MONTHLY,
     SKU_SHR_MM, AVG_DATA, OB_DATA, ELET_MKT_DATA, AREA_DECOMP (mercados em NQ_BASE_ANTERIOR ficam intocados).
  3. Atualiza o período: NQ_ROLL_LABELS, OB_PERIODS_NEW, AVG_MESES_NEW, NQ_CUR_IDX/NQ_PREV_IDX e os índices
     do filtro FY (nqP), e reescreve por regra os rótulos do período antigo → novo ('Jul–Set/26' → 'Jul–Out/26',
     'Out/25–Set/26' → 'Nov/25–Out/26', '(base Set/26)', rodapés, opções do seletor FY, selo) — só dentro das
     regiões da aba Nielsen (função regioes); rótulos 'Jul–Jun' (ano fechado / base anterior) nunca são tocados.
     Virada de ano fiscal (Jul) não é automática: o script para e avisa.
  4. Mostra um resumo (Farma Sul: share OFF!/EXPOSIS/SCJ FYTD, mercado R$) e pede confirmação.
  5. Ao aplicar: backup pré em versoes/, grava o dashboard, versão pós em versoes/ e cópia em Downloads.

Uso:
  python atualizar_nielsen.py                       # procura o PEGASUS mais recente em ~/Downloads
  python atualizar_nielsen.py "C:\\...\\Dashboard Nielsen - AC.PC.HC UXUI.html"
  python atualizar_nielsen.py FONTE --simular       # só mostra o resumo, não grava
  python atualizar_nielsen.py FONTE --sim           # aplica sem perguntar
  python atualizar_nielsen.py FONTE --saida X.html  # grava em outro arquivo (teste, sem versões)
Rodar de novo com a mesma base não muda nada ("Nada a atualizar").
"""
import argparse, base64, datetime, glob, gzip, json, os, re, shutil, sys, unicodedata

sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.abspath(__file__))
DASH_DIR = os.path.join(ROOT, "Dashboard_farma_sul")
HTML_PADRAO = os.path.join(DASH_DIR, "Dashboard_Farma_Sul_20260512_2220.html")
VERSOES = os.path.join(DASH_DIR, "versoes")
DOWNLOADS = os.path.expanduser(r"~\Downloads")

MON_EN = ['Jul','Aug','Sep','Oct','Nov','Dec','Jan','Feb','Mar','Apr','May','Jun']
MON_PT = ['Jul','Ago','Set','Out','Nov','Dez','Jan','Fev','Mar','Abr','Mai','Jun']
MES_EXT = {'Jan':'Janeiro','Fev':'Fevereiro','Mar':'Março','Abr':'Abril','Mai':'Maio','Jun':'Junho',
           'Jul':'Julho','Ago':'Agosto','Set':'Setembro','Out':'Outubro','Nov':'Novembro','Dez':'Dezembro'}
MET = {'sales':4,'dist':5,'price':6,'share':7,'tdp':8,'units':9,'ros':10}
BRAND_ALIAS = {'ALL OTHERS CAMP':'ALL OTHERS'}
CATS = {'PR':'PERSONAL REPELLENT', 'LE':'LIQUIDO ELETRICO', 'PB':'HC PATO BLOCK'}


def norm(s):
    return unicodedata.normalize('NFKD', s).encode('ascii','ignore').decode().upper().strip()

def pt(lbl_en):
    """'Sep-26' -> 'Set/26'"""
    m, y = lbl_en.split('-'); return MON_PT[MON_EN.index(m)] + '/' + y


# ═══════════════════════════ leitura da base ═══════════════════════════
class Cat:
    def __init__(self, d):
        self.d = d
        self.M = {m:i for i,m in enumerate(d["markets"])}; self.B = {b:i for i,b in enumerate(d["brands"])}
        self.P = {p:i for i,p in enumerate(d["products"])}
        self.per = {p["label"]:i for i,p in enumerate(d["periods"])}
        self.idx = {(r[0],r[1],r[2],r[3]):r for r in d["rows"]}
        ms = sorted([p for p in d["periods"] if p["kind"]=="month"], key=lambda p:p["sort"])
        self.months = [p["label"] for p in ms]
    def has(self, m): return m in self.M
    def v(self, m, b, period, metric, prod=None):
        b = BRAND_ALIAS.get(b, b)
        if m not in self.M or b not in self.B: return None
        pi = -1 if prod is None else self.P.get(prod)
        if pi is None: return None
        k = self.per.get(period)
        if k is None: return None
        r = self.idx.get((self.M[m], self.B[b], pi, k))
        return None if r is None else r[MET[metric]]
    def fy_months(self, fy):  # fy=2026 -> Jul-25..Jun-26
        y0 = fy-1
        return [f"{MON_EN[i]}-{(y0 if i<6 else y0+1)%100:02d}" for i in range(12)]
    def series(self, m, b, fy, metric, prod=None):
        return [self.v(m,b,p,metric,prod) for p in self.fy_months(fy)]
    def fytd(self, m, b, fy, metric, prod=None):
        return self.v(m,b,f"FYTD{fy%100}",metric,prod)

def r2(x, k=2, mul=1):
    return None if x is None else round(x*mul, k)

def load_pegasus(path):
    h = open(path, encoding="utf-8", errors="replace").read()
    key = "const DASH_DATA_GZIP_BY_CATEGORY="
    s = h.find(key)
    if s < 0: sys.exit("ERRO: o HTML não tem DASH_DATA_GZIP_BY_CATEGORY (não é um PEGASUS).")
    obj, _ = json.JSONDecoder().raw_decode(h[s+len(key):])
    want = {norm(v):k for k,v in CATS.items()}
    out = {}
    for name, b64 in obj.items():
        k = want.get(norm(name))
        if k: out[k] = json.loads(gzip.decompress(base64.b64decode(b64)))
    return out

def load_xlsx(path, cat_filter=None):
    """Leitor da 'Base Padrão dash' em formato longo (uma linha por mercado × marca/produto × período).
    Cabeçalhos reconhecidos por palavra-chave (pt/en). Monta o mesmo JSON que o PEGASUS embute.
    NÃO testado com um arquivo real (só existia o PEGASUS em 20/10/2026): se os cabeçalhos não forem
    reconhecidos, o script para e lista as colunas encontradas."""
    import openpyxl
    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    COLS = {'cat':['CATEGORIA','CATEGORY'], 'market':['MERCADO','MARKET'], 'brand':['MARCA','BRAND','FABRICANTE'],
            'prod':['PRODUTO','PRODUCT','SKU','ITEM'], 'period':['PERIODO','PERIOD','MES','MONTH'],
            'sales':['VENDAS VALOR','SALES VALUE','VALOR','SALES'], 'dist':['DISTRIBUICAO','DISTRIBUTION','DN'],
            'price':['PRECO MEDIO','AVG PRICE','AVERAGE PRICE','PRECO'], 'share':['SHARE VALOR','VALUE SHARE','SHARE'],
            'tdp':['TDP'], 'units':['UNIDADES','UNITS','VOLUME'], 'ros':['ROS','RATE OF SALE']}
    data = {}
    for ws in wb.worksheets:
        rows = ws.iter_rows(values_only=True)
        hdr = None
        for _ in range(15):
            r = next(rows, None)
            if r is None: break
            cells = [norm(str(c)) if c is not None else '' for c in r]
            if any(c in ('MERCADO','MARKET','MARKETS','MERCADOS') for c in cells): hdr = cells; break
        if not hdr: continue
        col = {}
        for k, keys in COLS.items():
            for kk in keys:
                hit = [i for i,c in enumerate(hdr) if c == kk or c.startswith(kk)]
                if hit and k not in col and hit[0] not in col.values(): col[k] = hit[0]; break
        need = ['market','brand','period','sales','share','units']
        if any(k not in col for k in need):
            sys.exit(f"ERRO: aba '{ws.title}' sem colunas reconhecidas {[k for k in need if k not in col]}. Cabeçalho: {hdr}")
        for r in rows:
            if r is None or r[col['market']] in (None, ''): continue
            cname = norm(str(r[col['cat']])) if 'cat' in col and r[col['cat']] else norm(ws.title)
            k = next((kk for kk,v in CATS.items() if norm(v) in cname or cname in norm(v)), None)
            if not k or (cat_filter and k not in cat_filter): continue
            D = data.setdefault(k, {'markets':[], 'brands':[], 'products':[], 'productBrandIndex':[], 'periods':{}, 'rows':[], '_i':{}})
            per = r[col['period']]
            if isinstance(per, (int, float)) and per > 30000: per = datetime.date(1899,12,30) + datetime.timedelta(days=int(per))
            if isinstance(per, datetime.datetime): per = per.date()
            if isinstance(per, datetime.date):
                lab = f"{MON_EN[(per.month-7)%12]}-{per.year%100:02d}"
                pk = ('month', lab, per.year*10000+per.month*100+per.day, per.year+1 if per.month>=7 else per.year)
            else:
                mm = re.search(r"FYTD\W*(\d\d)", norm(str(per)))
                if not mm: continue
                pk = ('fytd', f"FYTD{mm.group(1)}", int(mm.group(1))*100, int(mm.group(1)))
            if pk[1] not in D['periods']:
                D['periods'][pk[1]] = {'kind':pk[0], 'label':pk[1], 'sort':pk[2], 'fy':pk[3]}
            def ix(lst, key, val):
                d = D['_i'].setdefault(key, {})
                if val not in d: d[val] = len(lst); lst.append(val)
                return d[val]
            mi = ix(D['markets'], 'm', str(r[col['market']]).strip()); bn = str(r[col['brand']]).strip(); bi = ix(D['brands'], 'b', bn)
            pr = str(r[col['prod']]).strip() if 'prod' in col and r[col['prod']] not in (None, '') else ''
            if not pr or norm(pr) in (norm(bn), 'TOTAL', 'TOTAL MARCA'): pi = -1
            else:
                pi = ix(D['products'], 'p', pr)
                if pi == len(D['productBrandIndex']): D['productBrandIndex'].append(bi)
            num = lambda k: (float(r[col[k]]) if k in col and isinstance(r[col[k]], (int, float)) else None)
            sh = num('share'); sh = sh/100 if sh is not None and sh > 1.0000001 else sh
            D['rows'].append([mi, bi, pi, pk[1], num('sales'), num('dist'), num('price'), sh, num('tdp'), num('units'), num('ros')])
    out = {}
    for k, D in data.items():
        plist = sorted(D['periods'].values(), key=lambda p:p['sort']); pidx = {p['label']:i for i,p in enumerate(plist)}
        for row in D['rows']: row[3] = pidx[row[3]]
        out[k] = {'markets':D['markets'], 'brands':D['brands'], 'products':D['products'], 'productBrandIndex':D['productBrandIndex'],
                  'periods':plist, 'rows':D['rows'], 'sourceFile':os.path.basename(path), 'meta':{'exportDate':''}}
    return out

def achar_fonte():
    c = glob.glob(os.path.join(DOWNLOADS, "**", "Dashboard Nielsen - AC.PC.HC UXUI*.html"), recursive=True)
    c += glob.glob(os.path.join(DOWNLOADS, "**", "Base Padr*dash*.xlsx"), recursive=True)
    if not c: sys.exit("ERRO: nenhuma fonte encontrada em Downloads. Passe o caminho do PEGASUS ou do xlsx.")
    return max(c, key=os.path.getmtime)


# ═══════════════════════════ período ═══════════════════════════
def periodo(pr, src_file, export_date):
    last = pr.months[-1]
    p = next(x for x in pr.d["periods"] if x["label"] == last)
    fy = p["fy"] if p["fy"] > 100 else 2000+p["fy"]
    n = MON_EN.index(last.split('-')[0]) + 1          # meses no FYTD
    cur = pr.fy_months(fy)[:n]; prev = pr.fy_months(fy-1)[:n]
    i_last = pr.months.index(last)
    roll = pr.months[max(0, i_last-11):i_last+1]
    if len(roll) < 12: sys.exit("ERRO: a base tem menos de 12 meses até o último mês.")
    ROLL = [pt(x) for x in roll]
    def per_lbl(ms):
        a, b = pt(ms[0]), pt(ms[-1])
        if len(ms) == 1: return a
        return f"Jul–{b}" if a[-2:] == b[-2:] else f"{a}–{b}"
    mL = pt(last).split('/')[0]
    per = 'Jul' if n == 1 else f"Jul–{mL}"
    fc, fpv = fy % 100, (fy-1) % 100
    meses = [pt(x) for x in pr.months]
    cur_idx = [meses.index(pt(x)) for x in cur]
    prev_idx = [meses.index(pt(x)) if pt(x) in meses else None for x in prev]
    if None in prev_idx: sys.exit("ERRO: a base não tem os meses do FYTD anterior.")
    exp = export_date or ''
    exp_txt = ''
    if re.match(r"\d\d/\d\d/\d{4}$", exp):
        d, m, y = exp.split('/'); exp_txt = f"{d} {['jan','fev','mar','abr','mai','jun','jul','ago','set','out','nov','dez'][int(m)-1]} {y}"
    src = re.sub(r"\.xlsx?$", "", src_file or '', flags=re.I)
    return {
        'last': pt(last), 'lastU': pt(last).upper(), 'mL': mL, 'mP': pt(roll[-2]).split('/')[0],
        'fyC': fc, 'fyP': fpv, 'c': f"FY{fc}", 'p': f"FY{fpv}", 'p2': f"FY{(fy-2)%100}",
        'fc': f"FYTD{fc}", 'fp': f"FYTD{fpv}", 'per': per, 'perU': per.upper(),
        'perC': per_lbl(cur), 'perP': per_lbl(prev), 'ms': [MON_PT[i] for i in range(n)], 'msC': [pt(x) for x in cur],
        'yC': f"{(fy-1)%100:02d}", 'yP': f"{(fy-2)%100:02d}",
        'serie': f"{ROLL[0]}–{ROLL[-1]}", 'serieA': f"{ROLL[0]} a {ROLL[-1]}", 'last6': ROLL[-6:],
        'iL': len(meses)-1, 'src': src, 'exp': exp,
        # só para o script:
        '_fy': fy, '_n': n, '_cur': cur, '_prev': prev, '_rollp': roll, '_roll': ROLL, '_meses': meses,
        '_cur_idx': cur_idx, '_prev_idx': prev_idx, '_exp_txt': exp_txt,
        '_first_full': f"{pt(pr.months[0]).split('/')[0]}/20{pt(pr.months[0]).split('/')[1]}",
        '_last_full': f"{mL}/20{pt(last).split('/')[1]}", '_mes_ext': f"{MES_EXT[mL]} 20{pt(last).split('/')[1]}",
    }

# ═══════════════════════════ utilitários de edição ═══════════════════════════
class Doc:
    def __init__(self, h): self.h = h; self.log = []
    def rep(self, a, b, cnt=1, tag=''):
        n = self.h.count(a)
        assert n == cnt, f"[{tag}] esperava {cnt} ocorrência(s), achei {n}: {a[:120]!r}"
        self.h = self.h.replace(a, b)
    def sub(self, pat, repl, cnt=1, tag='', flags=0):
        new, n = re.subn(pat, repl, self.h, flags=flags)
        assert n == cnt, f"[{tag}] regex esperava {cnt}, achei {n}: {pat[:120]!r}"
        self.h = new
    def span(self, start, end_pat, frm=0):
        a = self.h.index(start, frm); b = self.h.index(end_pat, a+len(start)); return a, b

def decl(h, name):
    """Início da declaração 'const|var|let NAME = ' (o filtro FY de 20/10/2026 trocou const por var)."""
    m = re.search(r"(?m)^(?:const|var|let) "+name+r" = ", h)
    if not m: sys.exit(f"ERRO: bloco {name} não encontrado no dashboard.")
    return m.start()

def reckitt(get):
    """RECKITT no Líquido Elétrico = SBP LE + REPELEX LE. (Não é 100 − SCJ: a NielsenIQ põe o EXPOSIS LE
    dentro de ALL OTHERS LE, e 'All Others' de verdade = ALL OTHERS LE − EXPOSIS LE — conferido em 21/10/2026.)"""
    v = [get("SBP LE"), get("REPELEX LE")]
    return None if all(x is None for x in v) else sum(x or 0 for x in v)

def tirar_overrides_elet(D, le):
    """Remove as linhas antigas 'if(ELET_MKT_DATA["X"]){…fytd26=[…]…}' (bloco ELET FYTD2) dos mercados que estão na
    base nova — elas rodavam no carregamento e sobrescreviam os shares novos com os da base anterior."""
    ls = D.h.split("\n"); n0 = len(ls)
    ls = [l for l in ls if not (l.startswith('if(ELET_MKT_DATA["') and le.has(re.match(r'if\(ELET_MKT_DATA\["([^"]+)"\]', l).group(1)))]
    D.h = "\n".join(ls); return n0 - len(ls)

def js(v): return 'null' if v is None else (str(int(v)) if float(v).is_integer() else repr(v))
def arr1(a): return '['+','.join(js(x) for x in a)+']'
def arr3(a): return '['+', '.join(js(x) for x in a)+']'
def ratio(a, b): return None if (a is None or not b) else a/b


# ═══════════════════════════ regeneração dos dados ═══════════════════════════
def regenerar(D, C, P):
    pr, le, pb = C.get('PR'), C.get('LE'), C.get('PB')
    BR = ['OFF!','EXPOSIS','XO INSETO','SUPER REPELEX','SBP','ALL OTHERS CAMP']
    fy = P['_fy']; ROLLP = P['_rollp']; ROLL = P['_roll']; n = P['_n']
    info = {}
    # ── MKTSHARE_OVERVIEW ──
    a = decl(D.h, "MKTSHARE_OVERVIEW"); b = D.h.index("\n};", a)+3
    spans = [(m.group(1), m.group(0)) for m in re.finditer(r"(?ms)^  '([^']+)': \{\n.*?^  \},?\n", D.h[a:b])]
    old = []; out = [D.h[a:D.h.index("{", a)+1]+"\n"]
    for mk, txt in spans:
        if not pr.has(mk):
            old.append(mk); out.append(txt if txt.endswith(",\n") else txt[:-1]+",\n"); continue
        L = [f"  '{mk}': {{\n"]
        for br in BR:
            f0 = r2(pr.fytd(mk,br,fy-1,'share'),2,100); f1 = r2(pr.fytd(mk,br,fy,'share'),2,100)
            dl = None if f0 is None or f1 is None else round(f1-f0,2)
            m0 = [r2(x,2,100) for x in pr.series(mk,br,fy-1,'share')]; m1 = [r2(x,2,100) for x in pr.series(mk,br,fy,'share')]
            rl = [r2(pr.v(mk,br,q,'share'),2,100) for q in ROLLP]
            cal = [r2(pr.v(mk,br,q,'share'),2,100) for q in ['Jan-25','Feb-25','Mar-25','Apr-25']]
            L.append(f"    '{br}':{{fytd25:{js(f0)}, fytd26:{js(f1)}, delta:{js(dl)}, monthly:{arr1(m0)}, monthly27:{arr1(m1)}, roll12:{arr1(rl)}, jan25:{js(cal[0])}, feb25:{js(cal[1])}, mar25:{js(cal[2])}, apr25:{js(cal[3])}}},\n")
        L.append("  },\n"); out.append("".join(L))
    out.append("};"); D.h = D.h[:a] + "".join(out) + D.h[b:]
    info['MKTSHARE_OVERVIEW'] = (len(spans)-len(old), len(old))
    ls = D.h.split("\n")
    ls = [l for l in ls if not l.startswith("if(MKTSHARE_OVERVIEW[") or re.match(r"if\(MKTSHARE_OVERVIEW\['([^']+)'\]", l).group(1) in old]
    D.h = "\n".join(ls)
    # ── SHR_TREND_DATA ──
    a = decl(D.h, "SHR_TREND_DATA"); b = D.h.index("\n};", a)+3
    spans = [(m.group(1), m.group(0)) for m in re.finditer(r"(?ms)^  '([^']+)': \{\n.*?^  \},?\n", D.h[a:b])]
    out = [D.h[a:D.h.index("{", a)+1]+"\n"]; old_tr = []
    for mk, txt in spans:
        if not pr.has(mk):
            old_tr.append(mk); out.append(txt if txt.endswith(",\n") else txt[:-1]+",\n"); continue
        L = [f"  '{mk}': {{\n"]
        for br in re.findall(r"(?m)^    '([^']+)':", txt):
            s = [[r2(x,2,100) for x in pr.series(mk,br,f,'share')] for f in (fy-2, fy-1, fy)]
            L.append(f"    '{br}':          {{fy24:{arr1(s[0])},fy25:{arr1(s[1])},fy26:{arr1(s[2])}}},\n")
        L.append("  },\n"); out.append("".join(L))
    out.append("};"); D.h = D.h[:a] + "".join(out) + D.h[b:]
    info['SHR_TREND_DATA'] = (len(spans)-len(old_tr), len(old_tr))
    allold = sorted(set(old) | set(old_tr))
    D.sub(r"var NQ_BASE_ANTERIOR = \{[^\n]*\};", lambda m: "var NQ_BASE_ANTERIOR = "+json.dumps({x:1 for x in allold}, ensure_ascii=False)+";", tag='NQ_BASE_ANTERIOR')
    info['_old'] = allold
    # ── NQ_PR ──
    pa = D.h.index('<div class="main active" id="panel-nielsen">'); pbnd = D.h.index('<div class="main', pa+50)
    mk = [m for m in sorted(set(re.findall(r'<option value="([^"]+)"', D.h[pa:pbnd]))) if pr.has(m)]
    BRP = ['TOTAL MERCADO'] + BR
    o = {"meses": P['_meses'], "mk": {}}
    for m in mk:
        e = {}
        for br in BRP:
            s = [r2(pr.v(m,br,q,'share'),2,100) for q in pr.months]
            v = [r2(pr.v(m,br,q,'sales'),4,1e-6) for q in pr.months]
            u = [r2(pr.v(m,br,q,'units'),2,1e-3) for q in pr.months]
            f = {}
            for y in (fy-2, fy-1, fy):
                k = str(y%100)
                f['s'+k] = r2(pr.fytd(m,br,y,'share'),2,100); f['v'+k] = r2(pr.fytd(m,br,y,'sales'),4,1e-6); f['u'+k] = r2(pr.fytd(m,br,y,'units'),2,1e-3)
            e[br] = {"s":s, "v":v, "u":u, **f}
        o["mk"][m] = e
    a = D.h.index("var NQ_PR = "); b = D.h.index(";\n", a)
    D.h = D.h[:a] + "var NQ_PR = " + json.dumps(o, ensure_ascii=False, separators=(',',':')) + D.h[b:]
    info['NQ_PR'] = (len(mk), 0)
    # ── ODOR BLOCK ──
    if pb is not None:
        a = D.h.index("=", decl(D.h, "OB_DATA"))+2; b = D.h.index(";\n", a)
        OB = json.loads(D.h[a:b]); oldOB = []
        PRODMAP = {"T. Odor Block":("TOTAL MERCADO",None),"Pato":("SCJ",None),"Pato Block Algodão":("SCJ","Pato Block Algodão"),
                   "Pato Block Lavanda":("SCJ","Pato Block Lavanda"),"Pato Block Eucalipto":("SCJ","Pato Block Eucalipto"),
                   "Freeco":("FREECO",None),"All Others":("ALL OTHERS",None)}
        if pb.months[-1] != pr.months[-1]:
            print(f"  ⚠ Odor Block vai até {pt(pb.months[-1])}, repelentes até {P['last']} — série do OB alinhada ao mês dos repelentes.")
        for m in list(OB.keys()):
            if not pb.has(m): oldOB.append(m); continue
            new = {}
            for p_, (br, prod) in PRODMAP.items():
                if p_ not in OB[m]: continue
                sh = [r2(pb.v(m,br,q,'share',prod),2,100) for q in ROLLP]
                vl = [r2(pb.v(m,br,q,'sales',prod),2) for q in ROLLP]
                un = [r2(pb.v(m,br,q,'units',prod),0) for q in ROLLP]
                new[p_] = {"share":sh, "preco":[r2(ratio(v,u),2) for v,u in zip(vl,un)], "valor":vl, "unid":un}
            OB[m] = new
        D.h = D.h[:a] + json.dumps(OB, ensure_ascii=False) + D.h[b:]
        D.sub(r"var OB_BASE_ANTERIOR = \{[^\n]*\};", lambda m_: "var OB_BASE_ANTERIOR = "+json.dumps({x:1 for x in oldOB}, ensure_ascii=False)+";", tag='OB_BASE_ANTERIOR')
        info['OB_DATA'] = (len(OB)-len(oldOB), len(oldOB))
    else:
        print("  ⚠ fonte sem HC PATO BLOCK — OB_DATA mantido como está.")
    D.sub(r"var OB_PERIODS_NEW = \[[^\]]*\];", lambda m_: "var OB_PERIODS_NEW = "+json.dumps(ROLL, ensure_ascii=False)+";", tag='OB_PERIODS_NEW')
    # ── PREÇO MÉDIO ──
    a = decl(D.h, "AVG_DATA"); b = D.h.index("\n};", a)+3; body = D.h[a:b]
    optmap = {v:t for v,t in re.findall(r'<option value="([a-z_]+)">([^<]+)</option>', D.h)}; optmap['tbr_farma'] = 'T.BR Farma'
    SEL = ['OFF! Family Loção 200ml PR','OFF! Family Spray 170ml PR','Xô Loção 200ml','Xô Spray 200ml']
    out = [D.h[a:D.h.index("{", a)+1]+"\n"]; oldAVG = []; spans = list(re.finditer(r"(?ms)^  ([a-z_]+): \{\n.*?^  \},?\n", body))
    for mm in spans:
        code = mm.group(1); name = optmap.get(code,'').replace(' · base anterior','')
        if not pr.has(name):
            oldAVG.append(code); out.append(mm.group(0) if mm.group(0).endswith(",\n") else mm.group(0)[:-1]+",\n"); continue
        L = [f"  {code}: {{\n"]
        for p_ in SEL:
            pi = pr.P.get(p_)
            if pi is None: sys.exit(f"ERRO: SKU '{p_}' não existe mais na base (preço médio).")
            br = pr.d["brands"][pr.d["productBrandIndex"][pi]]
            L.append(f"    '{p_}':  {arr3([r2(ratio(pr.v(name,br,q,'sales',p_),pr.v(name,br,q,'units',p_)),2) for q in ROLLP])},\n")
        L.append("  },\n"); out.append("".join(L))
    out.append("};"); D.h = D.h[:a] + "".join(out) + D.h[b:]
    D.sub(r"var AVG_MESES_NEW = \[[^\]]*\];", lambda m_: "var AVG_MESES_NEW = "+json.dumps([x.upper() for x in ROLL])+";", tag='AVG_MESES_NEW')
    D.sub(r"var AVG_BASE_ANTERIOR = \{[^\n]*\};", lambda m_: "var AVG_BASE_ANTERIOR = "+json.dumps({c:1 for c in oldAVG})+";", tag='AVG_BASE_ANTERIOR')
    info['AVG_DATA'] = (len(spans)-len(oldAVG), len(oldAVG))
    # ── ELÉTRICOS ──
    if le is not None:
        a = decl(D.h, "ELET_MKT_DATA"); b = D.h.index("\n};", a)+3
        LEB = {"SCJ":"SCJ","EXPOSIS":"EXPOSIS LE","RAID":"RAID LE","SBP":"SBP LE"}
        def leshare(m, b_, q):
            if b_ == "RECKITT": return reckitt(lambda b2: le.v(m,b2,q,'share'))
            return le.v(m,LEB[b_],q,'share')
        def lefy(m, b_, y):
            if b_ == "RECKITT": return reckitt(lambda b2: le.fytd(m,b2,y,'share'))
            return le.fytd(m,LEB[b_],y,'share')
        cnt = [0]
        sub_txt = f"% share dentro do mercado Elétrico · {P['fc']} = {P['perC']} vs {P['fp']} = {P['perP']} · série {P['serie']} · NielsenIQ (base {P['last']}) · "
        def fix_block(mm):
            txt = mm.group(0); m = mm.group(1)
            if not le.has(m): return txt
            cnt[0] += 1
            brands = json.loads(re.search(r"brands:(\[[^\]]*\])", txt).group(1))
            f0 = [r2(lefy(m,b_,fy-1),2,100) for b_ in brands]; f1 = [r2(lefy(m,b_,fy),2,100) for b_ in brands]
            mon = [[r2(leshare(m,b_,q),2,100) for q in ROLLP] for b_ in brands]
            k0 = r2(le.fytd(m,"TOTAL MERCADO",fy-1,'sales'),3,1e-6); k1 = r2(le.fytd(m,"TOTAL MERCADO",fy,'sales'),3,1e-6)
            mkm = [r2(le.v(m,"TOTAL MERCADO",q,'sales'),3,1e-6) for q in ROLLP]
            txt = re.sub(r'sub:"[^"]*"', lambda _: 'sub:"'+sub_txt+m+'"', txt)
            txt = re.sub(r"fytd25:\[[^\]]*\]", lambda _: "fytd25:"+arr3(f0), txt); txt = re.sub(r"fytd26:\[[^\]]*\]", lambda _: "fytd26:"+arr3(f1), txt)
            txt = re.sub(r"monthly:\[\[.*?\]\]", lambda _: "monthly:["+", ".join(arr3(x) for x in mon)+"]", txt, flags=re.S)
            txt = re.sub(r"mkt_fy25:[\d.]+", lambda _: "mkt_fy25:"+js(k0), txt); txt = re.sub(r"mkt_fy26:[\d.]+", lambda _: "mkt_fy26:"+js(k1), txt)
            txt = re.sub(r"mkt_monthly:\[[^\]]*\]", lambda _: "mkt_monthly:"+arr3(mkm), txt)
            return txt
        body = re.sub(r'(?ms)^  "([^"]+)":\{\n.*?^  \}', fix_block, D.h[a:b])
        D.h = D.h[:a] + body + D.h[b:]
        info['ELET_MKT_DATA'] = (cnt[0], 0)
        n_ov = tirar_overrides_elet(D, le)
        if n_ov: print(f"  Elétricos: {n_ov} overrides antigos de share removidos (sobrescreviam a base nova).")
    else:
        print("  ⚠ fonte sem LÍQUIDO ELÉTRICO — ELET_MKT_DATA mantido como está.")
    # ── SKU ──
    SKUP = list(pr.d["products"])
    def pbrand(p_): return pr.d["brands"][pr.d["productBrandIndex"][pr.P[p_]]]
    def sku_top(m):
        rows = [(p_, pr.fytd(m,pbrand(p_),fy,'share',p_)) for p_ in SKUP]
        rows = [x for x in rows if x[1] is not None]; rows.sort(key=lambda x:-x[1]); return [p_ for p_,_ in rows[:10]]
    a = D.h.index("=", decl(D.h, "SKU_MKT_DATA"))+2; b = D.h.index(";\n", a); SD = json.loads(D.h[a:b]); c_ = 0
    for m in SD:
        if not pr.has(m): continue
        sk = sku_top(m); c_ += 1
        f0 = [r2(pr.fytd(m,pbrand(p_),fy-1,'share',p_),2,100) or 0 for p_ in sk]; f1 = [r2(pr.fytd(m,pbrand(p_),fy,'share',p_),2,100) for p_ in sk]
        SD[m] = {"skus":sk, "fytd25":f0, "fytd26":f1, "var":[round((x or 0)-y,2) for x,y in zip(f1,f0)]}
    D.h = D.h[:a] + json.dumps(SD, ensure_ascii=False) + D.h[b:]
    info['SKU_MKT_DATA'] = (c_, len(SD)-c_)
    a = decl(D.h, "SKU_MKT_MONTHLY"); b = D.h.index("\n};", a)+3
    def mfix(mm):
        m = mm.group(1)
        if not pr.has(m): return mm.group(0)
        sk = sku_top(m)
        def avg(p_, pers):
            v = [pr.v(m,pbrand(p_),q,'share',p_) for q in pers]; v = [x for x in v if x is not None]
            return round(sum(v)/len(v)*100,2) if v else 0
        j0 = [avg(p_, P['_prev']) for p_ in sk]; j1 = [avg(p_, P['_cur']) for p_ in sk]
        end = ",\n" if mm.group(0).endswith(",\n") else "\n"
        return f'  "{m}": {{"skus":{json.dumps(sk,ensure_ascii=False)},"janmar25":{json.dumps(j0)},"janmar26":{json.dumps(j1)},"var":{json.dumps([round(x-y,2) for x,y in zip(j1,j0)])}}}'+end
    D.h = D.h[:a] + re.sub(r'(?m)^  "([^"]+)": \{"skus".*\n', mfix, D.h[a:b]) + D.h[b:]
    a = decl(D.h, "SKU_SHR_MM"); b = D.h.index("\n};", a)+3
    LAST6 = ROLLP[-6:]
    def sfix(mm):
        m = mm.group(1)
        if not pr.has(m): return mm.group(0)
        sk = sku_top(m)
        obj = {k:[r2(pr.v(m,pbrand(p_),q,'share',p_),2,100) or 0 for p_ in sk] for k,q in zip(['jan','fev','mar','abr','mai','jun'], LAST6)}
        end = ",\n" if mm.group(0).endswith(",\n") else "\n"
        return f'  "{m}":'+json.dumps(obj, ensure_ascii=False, separators=(',',':'))+end
    D.h = D.h[:a] + re.sub(r'(?m)^  "([^"]+)":\{"jan".*\n', sfix, D.h[a:b]) + D.h[b:]
    cols = {'OFF!':'#F59E0B','EXPOSIS':'#8B5CF6','XO INSETO':'#0EA5E9','SUPER REPELEX':'#64748B','ALL OTHERS':'#475569'}
    extra = {p_:cols.get(pbrand(p_),'#374151') for p_ in SKUP}
    D.sub(r"(\(function\(x\)\{for\(var k in x\)\{ if\(!_skuShrBrandColors\[k\]\) _skuShrBrandColors\[k\]=x\[k\]; \}\}\)\()\{[^\n]*?\}(\);)",
          lambda m_: m_.group(1)+json.dumps(extra, ensure_ascii=False)+m_.group(2), tag='SKU cores')
    # ── AREA_DECOMP ──
    a = decl(D.h, "AREA_DECOMP"); b = D.h.index("\n};", a)+3
    GRP = {"Farma Moderno":lambda ar:"Farma Moderno "+ar, "Farma Indep":lambda ar:"Farma Indep "+ar,
           "Farma Total":lambda ar:"Farma "+ar, "T.BR Farma (Canais)":lambda ar:"T.BR "+ar}
    newg = []; oldg = []
    def gfix(mm):
        g = mm.group(1); txt = mm.group(0)
        if g not in GRP: oldg.append(g); return txt
        obj = json.loads("{"+txt.strip().rstrip(",")+"}")[g]
        areas = obj["areas"]; mks = [GRP[g](x) for x in areas]
        if not all(pr.has(m) for m in mks): oldg.append(g); return txt
        T0 = sum(pr.fytd(m,"TOTAL MERCADO",fy-1,'sales') or 0 for m in mks); T1 = sum(pr.fytd(m,"TOTAL MERCADO",fy,'sales') or 0 for m in mks)
        o_ = {"areas":areas}
        for br in [k for k in obj if k != "areas"]:
            v0 = [pr.fytd(m,br,fy-1,'sales') or 0 for m in mks]; v1 = [pr.fytd(m,br,fy,'sales') or 0 for m in mks]
            s0 = [pr.fytd(m,br,fy-1,'share') for m in mks]; s1 = [pr.fytd(m,br,fy,'share') for m in mks]
            o_[br] = {"val26":[round(x/1e6,2) for x in v1],
                      "var":[round((y-x)*100,2) if x is not None and y is not None else 0 for x,y in zip(s0,s1)],
                      "contrib":[round((y/T1-x/T0)*100,3) for x,y in zip(v0,v1)]}
        newg.append(g)
        end = ",\n" if txt.endswith(",\n") else "\n"
        return f'  "{g}":'+json.dumps(o_, ensure_ascii=False)+end
    D.h = D.h[:a] + re.sub(r'(?m)^  "([^"]+)":\{"areas".*\n', gfix, D.h[a:b]) + D.h[b:]
    D.sub(r"var AD_BASE_ANTERIOR = \{[^\n]*\};", lambda m_: "var AD_BASE_ANTERIOR = "+json.dumps({g:1 for g in oldg}, ensure_ascii=False)+";", tag='AD_BASE_ANTERIOR')
    info['AREA_DECOMP'] = (len(newg), len(oldg))
    info['L12M (12 meses)'] = (gerar_l12(D, C, P), 0)
    return info


L12_INI = "/* ═══ NQ_L12 · Últimos 12 meses (gerado por atualizar_nielsen.py) ═══ */"
L12_FIM = "/* ═══ fim NQ_L12 ═══ */"

def gerar_l12(D, C, P):
    """Dados das visões de período do filtro global (além de FY27/FY26):
      • L12 = 'Últimos 12 meses' (últimos 12 × os 12 anteriores)
      • CAL = ano-calendário (Jan–último mês × mesmos meses do ano anterior), ex.: Jan–Set/26 × Jan–Set/25
    Share do período = Σ R$ marca / Σ R$ total. As séries mensais (Elétricos) ficam sempre nos últimos 12 meses
    (eixo NQ_ROLL_LABELS). OB e Preço médio já são séries de 12 meses (usam os dados FY atuais)."""
    pr, le = C['PR'], C.get('LE')
    roll, rollP = pr.months[-12:], pr.months[-24:-12]
    if len(rollP) < 12: sys.exit("ERRO: a base precisa de 24 meses para a visão 'Últimos 12 meses'.")
    yy = int(pr.months[-1].split('-')[1])
    calC = [q for q in pr.months if int(q.split('-')[1]) == yy]          # Jan-26 … Sep-26 (ordem cronológica)
    calP = [f"{q.split('-')[0]}-{yy-1:02d}" for q in calC]
    def lbl(ms): return pt(ms[0]) if len(ms) == 1 else (f"Jan–{pt(ms[-1])}" if ms[0].startswith('Jan') else f"{pt(ms[0])}–{pt(ms[-1])}")
    VIS = [('L12', roll, rollP, 'Últ. 12M', '12M ant.', f"{pt(roll[0])}–{pt(roll[-1])}", f"{pt(rollP[0])}–{pt(rollP[-1])}"),
           ('CAL', calC, calP, lbl(calC), lbl(calP), lbl(calC), lbl(calP))]
    def ssum(c, m, b, pers, met='sales', prod=None):
        v = [c.v(m,b,q,met,prod) for q in pers]; v = [x for x in v if x is not None]; return sum(v) if v else None
    def psh(c, m, b, pers, prod=None):
        t = ssum(c,m,"TOTAL MERCADO",pers); s = ssum(c,m,b,pers,'sales',prod)
        return None if (t is None or s is None or not t) else s/t
    def pbrand(p_): return pr.d["brands"][pr.d["productBrandIndex"][pr.P[p_]]]
    def avg(m, p_, pers):
        v = [pr.v(m,pbrand(p_),q,'share',p_) for q in pers]; v = [x for x in v if x is not None]
        return round(sum(v)/len(v)*100,2) if v else 0
    out = []
    a = D.h.index("=", decl(D.h, "SKU_MKT_DATA"))+2; b = D.h.index(";\n", a)
    mk = [m for m in json.loads(D.h[a:b]) if pr.has(m)]
    n_sku = 0
    for tag, cur, prev, nC, nP, perC, perP in VIS:
        # SKU (share do período) e, no L12, média mensal
        SKD = {}; SKM = {}
        for m in mk:
            rows = [(p_, psh(pr,m,pbrand(p_),cur,p_)) for p_ in pr.d["products"]]
            sk = [p_ for p_,s in sorted([x for x in rows if x[1] is not None], key=lambda x:-x[1])[:10]]
            f0 = [r2(psh(pr,m,pbrand(p_),prev,p_),2,100) or 0 for p_ in sk]; f1 = [r2(psh(pr,m,pbrand(p_),cur,p_),2,100) or 0 for p_ in sk]
            SKD[m] = {"skus":sk, "fytd25":f0, "fytd26":f1, "var":[round(y-x,2) for x,y in zip(f0,f1)]}
            if tag == 'L12':
                j0 = [avg(m,p_,prev) for p_ in sk]; j1 = [avg(m,p_,cur) for p_ in sk]
                SKM[m] = {"skus":sk, "janmar25":j0, "janmar26":j1, "var":[round(y-x,2) for x,y in zip(j0,j1)]}
        n_sku = max(n_sku, len(SKD))
        out.append(f"var SKU_MKT_DATA_{tag} = "+json.dumps(SKD, ensure_ascii=False)+";")
        if tag == 'L12':
            out.append("var SKU_MKT_MONTHLY_L12 = "+json.dumps(SKM, ensure_ascii=False)+";")
        else:
            # card 'Market Share por SKU — média' (sempre ano-calendário): média mensal dos SKUs
            CAL = {}
            for m in mk:
                rows = [(p_, avg(m, p_, cur)) for p_ in pr.d["products"]]
                sk = [p_ for p_,s in sorted([x for x in rows if x[1]], key=lambda x:-x[1])[:10]]
                j0 = [avg(m,p_,prev) for p_ in sk]; j1 = [avg(m,p_,cur) for p_ in sk]
                CAL[m] = {"skus":sk, "janmar25":j0, "janmar26":j1, "var":[round(y-x,2) for x,y in zip(j0,j1)]}
            out.append("var SKU_MKT_CAL = "+json.dumps(CAL, ensure_ascii=False)+";")
        # Elétricos
        EL = {}
        if le is not None:
            LEB = {"SCJ":"SCJ","EXPOSIS":"EXPOSIS LE","RAID":"RAID LE","SBP":"SBP LE"}
            a = decl(D.h, "ELET_MKT_DATA"); b = D.h.index("\n};", a)
            for mm in re.finditer(r'(?ms)^  "([^"]+)":\{\n(.*?)^  \}', D.h[a:b]):
                m = mm.group(1); txt = mm.group(2)
                if not le.has(m): continue
                brands = json.loads(re.search(r"brands:(\[[^\]]*\])", txt).group(1)); colors = json.loads(re.search(r"colors:(\[[^\]]*\])", txt).group(1))
                def lsh(b_, pers):
                    if b_ == "RECKITT": return reckitt(lambda b2: psh(le,m,b2,pers))
                    return psh(le,m,LEB[b_],pers)
                def msh(b_, q):
                    if b_ == "RECKITT": return reckitt(lambda b2: le.v(m,b2,q,'share'))
                    return le.v(m,LEB[b_],q,'share')
                EL[m] = {"label":re.search(r'label:"([^"]*)"', txt).group(1),
                         "sub":f"% share dentro do mercado Elétrico · {nC} = {perC} vs {nP} = {perP} · NielsenIQ (base {P['last']}) · {m}",
                         "brands":brands, "colors":colors,
                         "fytd25":[r2(lsh(b_,prev),2,100) for b_ in brands], "fytd26":[r2(lsh(b_,cur),2,100) for b_ in brands],
                         "monthly":[[r2(msh(b_,q),2,100) for q in roll] for b_ in brands],
                         "mkt_fy25":r2(ssum(le,m,"TOTAL MERCADO",prev),3,1e-6), "mkt_fy26":r2(ssum(le,m,"TOTAL MERCADO",cur),3,1e-6),
                         "mkt_monthly":[r2(le.v(m,"TOTAL MERCADO",q,'sales'),3,1e-6) for q in roll]}
        out.append(f"var ELET_MKT_DATA_{tag} = "+json.dumps(EL, ensure_ascii=False)+";")
        # Contribuição por área
        a = decl(D.h, "AREA_DECOMP"); b = D.h.index("\n};", a)
        GRP = {"Farma Moderno":lambda ar:"Farma Moderno "+ar, "Farma Indep":lambda ar:"Farma Indep "+ar,
               "Farma Total":lambda ar:"Farma "+ar, "T.BR Farma (Canais)":lambda ar:"T.BR "+ar}
        AD = {}
        for mm in re.finditer(r'(?m)^  "([^"]+)":(\{"areas".*?\}),?$', D.h[a:b]):
            g = mm.group(1)
            if g not in GRP: continue
            obj = json.loads(mm.group(2)); areas = obj["areas"]; mks = [GRP[g](x) for x in areas]
            if not all(pr.has(x) for x in mks): continue
            T0 = sum(ssum(pr,x,"TOTAL MERCADO",prev) or 0 for x in mks); T1 = sum(ssum(pr,x,"TOTAL MERCADO",cur) or 0 for x in mks)
            o_ = {"areas":areas}
            for br in [k for k in obj if k != "areas"]:
                v0 = [ssum(pr,x,br,prev) or 0 for x in mks]; v1 = [ssum(pr,x,br,cur) or 0 for x in mks]
                s0 = [psh(pr,x,br,prev) for x in mks]; s1 = [psh(pr,x,br,cur) for x in mks]
                o_[br] = {"val26":[round(x/1e6,2) for x in v1],
                          "var":[round((y-x)*100,2) if x is not None and y is not None else 0 for x,y in zip(s0,s1)],
                          "contrib":[round((y/T1-x/T0)*100,3) for x,y in zip(v0,v1)]}
            AD[g] = o_
        out.append(f"var AREA_DECOMP_{tag} = "+json.dumps(AD, ensure_ascii=False)+";")
    bloco = L12_INI + "\n" + "\n".join(out) + "\n" + L12_FIM
    if L12_INI in D.h:
        a = D.h.index(L12_INI); b = D.h.index(L12_FIM, a)+len(L12_FIM)
        D.h = D.h[:a] + bloco + D.h[b:]
    else:
        ancora = "/* ═══ Filtro de ano fiscal (aba Nielsen) ═══ */"
        assert D.h.count(ancora) == 1, "âncora do filtro FY não encontrada"
        D.h = D.h.replace(ancora, bloco + "\n" + ancora)
    return n_sku


# ═══════════════════════════ rótulos de período ═══════════════════════════
MESES_RE = 'Jan|Fev|Mar|Abr|Mai|Jun|Jul|Ago|Set|Out|Nov|Dez'
FIM_FYTD = 'Jan|Fev|Mar|Abr|Mai|Ago|Set|Out|Nov|Dez'   # 'Jul–Jun' = ano fechado/base anterior → nunca mexe

def estado_antigo(h):
    """Período em que o dashboard está hoje (lido do próprio HTML)."""
    roll = json.loads(re.search(r"var NQ_ROLL_LABELS = (\[[^\]]*\]);", h).group(1))
    m = re.search(r"/\* ═══ NIELSEN · base nova \([^)\n]*\) — FY(\d\d) × FY(\d\d) ═══", h)
    return {'roll': roll, 'last': roll[-1], 'fyC': int(m.group(2)), 'fyP': int(m.group(1))}

def regioes(h):
    """Trechos da aba Nielsen onde os rótulos de período podem ser reescritos (nunca o resto do dashboard)."""
    R = []
    a = h.index('<div class="main active" id="panel-nielsen">'); R.append((a, h.index('<div class="main', a+50)))
    i = h.find('ANO FISCAL · NIELSEN')
    if i >= 0: R.append((h.rfind('<div', 0, i), h.index('</div>', h.index('id="nq-fy-info"', i))))
    a = h.index("/* ═══ NIELSEN · base nova ("); R.append((a, h.index("\nvar mso2Mode = ", a)))
    for fn in ['renderEletricosCard', 'renderAreaDecomp', 'renderMSOSkuJanMar', 'renderShrSTSKU', 'renderSkuShrCard',
               'renderShrTrend', 'renderShrShortTerm', 'renderShrShortTerm2', 'renderAvgPriceChart', 'renderAvgInsight',
               'renderOBShare', 'renderOBPreco', 'renderOBVendas', 'renderOBMercado']:
        for m in re.finditer(r"\nfunction "+fn+r"\(", h):
            e = h.find("\nfunction ", m.start()+10); R.append((m.start(), e if e > 0 else len(h)))
    for anchor in ["var _adOld=", "_l25=_o?"]:     # funções sem nome fixo conhecido
        i = h.find(anchor)
        if i >= 0: R.append((h.rfind("\nfunction ", 0, i), h.find("\nfunction ", i)))
    R.sort(); out = []
    for s, e in R:                                   # junta sobreposições
        if out and s <= out[-1][1]: out[-1] = (out[-1][0], max(out[-1][1], e))
        else: out.append((s, e))
    return out

def regras(P, O):
    """Lista de (regex, função) que levam qualquer rótulo do período antigo O para o novo P."""
    oC, oP = f"{O['fyC']-1:02d}", f"{O['fyP']-1:02d}"         # ano de início do FYTD atual/anterior (ex.: 26 / 25)
    def fytd(m):
        sep = m.group('sep'); up = m.group(0)[:3] == 'JUL'
        y = m.group('y1') or m.group('y2')
        if y is None: new = P['per']
        elif y == oC: new = P['perC']
        elif y == oP: new = P['perP']
        else: return m.group(0)
        new = new.replace('–', sep)
        return new.upper() if up else new
    R = [
        (r"Jul(?:/(?P<y1>\d\d))?(?P<sep>–|&ndash;)(?:"+FIM_FYTD+r")(?:/(?P<y2>\d\d))?(?![\w/])", fytd),
        (r"JUL(?:/(?P<y1>\d\d))?(?P<sep>–|&ndash;)(?:"+FIM_FYTD.upper()+r")(?:/(?P<y2>\d\d))?(?![\w/])", fytd),
        (re.escape(f"{O['roll'][0]}–{O['roll'][-1]}"), lambda m: P['serie']),
        (re.escape(f"{O['roll'][0]} a {O['roll'][-1]}"), lambda m: P['serieA']),
        (re.escape(f"{O['roll'][0]}&ndash;{O['roll'][-1]}"), lambda m: P['serie'].replace('–','&ndash;')),
        (re.escape("['"+"','".join(O['roll'][-6:])+"']"), lambda m: "['"+"','".join(P['last6'])+"']"),
        (r"JUL(?: · (?:AGO|SET|OUT|NOV|DEZ|JAN|FEV|MAR|ABR|MAI))+", lambda m: ' · '.join(P['ms']).upper()),
        (r"\(base (?:"+MESES_RE+r")/\d\d\)", lambda m: f"(base {P['last']})"),
        (r"dados até (?:"+MESES_RE+r")/\d\d", lambda m: f"dados até {P['last']}"),
        (r"Base Padrão dash - [A-Za-zç]{3}\d\d", lambda m: P['src']),
        (r"Exportado: \d\d [a-z]{3} \d{4}(?= · dados até)", lambda m: f"Exportado: {P['_exp_txt']}"),
        (r"export \d\d/\d\d/\d{4}", lambda m: f"export {P['exp']}"),
        (r"Jul/20\d\d–(?:"+MESES_RE+r")/20\d\d(?= · FY)", lambda m: f"{P['_first_full']}–{P['_last_full']}"),
        (r"<p>(?:"+'|'.join(MES_EXT.values())+r") 20\d\d</p></div>", lambda m: f"<p>{P['_mes_ext']}</p></div>"),
        # índices do FYTD corrente (renderizadores e filtro FY)
        (r"var NQ_CUR_IDX = \[[\d,]*\], NQ_PREV_IDX = \[[\d,]*\];",
         lambda m: f"var NQ_CUR_IDX = [{','.join(map(str,P['_cur_idx']))}], NQ_PREV_IDX = [{','.join(map(str,P['_prev_idx']))}];"),
        (r"\{cur:\[[\d,]*\],prev:\[[\d,]*\](?=,fyC:'FYTD)",
         lambda m: f"{{cur:[{','.join(map(str,P['_cur_idx']))}],prev:[{','.join(map(str,P['_prev_idx']))}]"),
        (r"line:nqRange\(\d+,\d+\),roll:nqRange\(\d+,\d+\)(?=,acc:'JUL)",
         lambda m: f"line:nqRange({P['_prev_idx'][0]},{P['iL']}),roll:nqRange({P['iL']-11},{P['iL']})"),
    ]
    return [(re.compile(p), f) for p, f in R if f is not None]

def rotulos(D, P, O, novo_mes):
    D.sub(r"var NQ_ROLL_LABELS = \[[^\]]*\];", lambda m: "var NQ_ROLL_LABELS = "+json.dumps(P['_roll'], ensure_ascii=False)+";", tag='NQ_ROLL_LABELS')
    D.sub(r"/\* ═══ NIELSEN · base nova \([^)\n]*\) — FY\d\d × FY\d\d ═══",
          lambda m: f"/* ═══ NIELSEN · base nova ({P['src']}, export {P['exp']}) — {P['p']} × {P['c']} ═══", tag='cabeçalho')
    RG = regras(P, O); n = 0
    for s, e in reversed(regioes(D.h)):
        t = D.h[s:e]
        for rx, f in RG:
            t, k = rx.subn(f, t); n += k
        D.h = D.h[:s] + t + D.h[e:]
    if novo_mes:
        hoje = datetime.date.today().strftime('%d/%m/%Y')
        D.sub(r'(id="dash-update-badge"[^>]*>✓ Atualizado )\d\d/\d\d/\d{4}', lambda m: m.group(1)+hoje, tag='selo')
    return n

def sobras(h, O, P):
    """Rótulos do período antigo que ficaram para trás (fora das regiões conhecidas)."""
    if O['last'] == P['last']: return []
    mL = O['last'].split('/')[0]
    pats = [f"Jul–{mL}", f"JUL–{mL.upper()}", f"(base {O['last']})", f"{O['roll'][0]}–{O['roll'][-1]}"]
    achados = []
    for p in pats:
        for m in re.finditer(re.escape(p), h):
            achados.append(h[max(0, m.start()-60):m.end()+30].replace('\n', ' '))
    return achados


# ═══════════════════════════ resumo ═══════════════════════════
def resumo(C, P, mes_antes, info):
    pr = C['PR']; fy = P['_fy']; m = 'Farma Sul'
    print("\n" + "═"*72)
    print(f"  NIELSEN · {P['src'] or 'base'} (export {P['exp'] or '?'})")
    print(f"  Último mês: {P['last']}  ·  {P['fc']} = {P['perC']}  vs  {P['fp']} = {P['perP']}")
    print(f"  Série rolling: {P['serie']}   (dashboard estava em {mes_antes})")
    print("═"*72)
    if pr.has(m):
        print(f"  {m:<14} {P['fp']:>10} {P['fc']:>10} {'Δ':>9}")
        for br, lab in [('OFF!','OFF! share'),('EXPOSIS','EXPOSIS share'),('SCJ','SCJ share')]:
            a = r2(pr.fytd(m,br,fy-1,'share'),2,100); b = r2(pr.fytd(m,br,fy,'share'),2,100)
            d = '' if a is None or b is None else f"{b-a:+.2f}pp"
            print(f"  {lab:<14} {('%.2f%%'%a) if a is not None else '—':>10} {('%.2f%%'%b) if b is not None else '—':>10} {d:>9}")
        a = pr.fytd(m,'TOTAL MERCADO',fy-1,'sales'); b = pr.fytd(m,'TOTAL MERCADO',fy,'sales')
        if a and b: print(f"  {'Mercado R$':<14} {a/1e6:>9.2f}M {b/1e6:>9.2f}M {(b/a-1)*100:>+8.1f}%")
        mo = pt(pr.months[-1]).split('/')[0]
        v = pr.v(m,'OFF!',pr.months[-1],'share')
        if v is not None: print(f"  OFF! share em {P['last']}: {v*100:.2f}%")
    print("-"*72)
    for k, v in info.items():
        if k.startswith('_'): continue
        nv, od = v
        print(f"  {k:<18} {nv:>3} mercados/grupos atualizados" + (f" · {od} mantidos (base anterior)" if od else ""))
    print("═"*72)


# ═══════════════════════════ main ═══════════════════════════
def main():
    ap = argparse.ArgumentParser(description="Atualiza a aba Nielsen do Dashboard Farma Sul.")
    ap.add_argument("fonte", nargs="?", help="HTML PEGASUS ou xlsx 'Base Padrão dash' (padrão: mais recente em Downloads)")
    ap.add_argument("--html", default=HTML_PADRAO, help="dashboard alvo")
    ap.add_argument("--saida", help="grava o resultado neste arquivo (teste; não cria versões)")
    ap.add_argument("--odor-block", help="(modo xlsx) xlsx do Odor Block")
    ap.add_argument("--simular", action="store_true", help="só mostra o resumo")
    ap.add_argument("--sim", action="store_true", help="aplica sem perguntar")
    a = ap.parse_args()
    fonte = a.fonte or achar_fonte()
    print(f"Fonte: {fonte}")
    if fonte.lower().endswith(".html"):
        C = load_pegasus(fonte)
    else:
        C = load_xlsx(fonte)
        if a.odor_block: C.update(load_xlsx(a.odor_block, cat_filter={'PB'}))
    if 'PR' not in C: sys.exit("ERRO: a fonte não tem a categoria PERSONAL REPELLENT.")
    C = {k:Cat(v) for k,v in C.items()}
    pr = C['PR']
    P = periodo(pr, pr.d.get('sourceFile'), pr.d.get('meta',{}).get('exportDate'))
    if 'LE' in C and C['LE'].months[-1] != pr.months[-1]:
        sys.exit(f"ERRO: Líquido Elétrico vai até {pt(C['LE'].months[-1])} e repelentes até {P['last']} — bases desalinhadas.")

    orig = open(a.html, encoding="utf-8").read()
    D = Doc(orig)
    O = estado_antigo(orig); mes_antes = O['last']
    if P['fyC'] != O['fyC']:
        sys.exit(f"ERRO: virada de ano fiscal (dashboard em FY{O['fyC']}, base em {P['c']}). O script cobre os meses dentro do ano; "
                 "a virada exige ajuste estrutural (FY anterior vira 'ano fechado', conjuntos *_FY26, nqP/renderMSO, nqSeriesLabels).")
    info = regenerar(D, C, P)
    nreg = rotulos(D, P, O, novo_mes=(mes_antes != P['last']))
    resumo(C, P, mes_antes, info)
    print(f"  Rótulos de período reescritos: {nreg}")
    for s in sobras(D.h, O, P):
        print(f"  ⚠ rótulo antigo fora das regiões Nielsen conhecidas (conferir): …{s}…")
    old0 = json.loads(re.search(r"var NQ_BASE_ANTERIOR = (\{[^\n]*\});", orig).group(1))
    if set(old0) != set(info['_old']):
        print(f"  ⚠ mercados 'base anterior' mudaram: saíram {sorted(set(old0)-set(info['_old']))} · entraram {sorted(set(info['_old'])-set(old0))}"
              " — revisar rótulos '· base anterior' nos filtros.")
    if D.h == orig:
        print("\nNada a atualizar: o dashboard já está com esta base.")
        return
    if a.simular:
        print("\n[--simular] nada foi gravado."); return
    if a.saida:
        open(a.saida, "w", encoding="utf-8", newline="\r\n").write(D.h)
        print(f"\nGravado (teste): {a.saida}"); return
    if not a.sim:
        r = input("\nAplicar no dashboard? (s/N) ").strip().lower()
        if r not in ("s", "sim", "y"): print("Cancelado — nada foi gravado."); return
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M")
    tag = "Nielsen" + P['last'].replace('/', '')
    os.makedirs(VERSOES, exist_ok=True)
    pre = os.path.join(VERSOES, f"Dashboard_Farma_Sul_{ts}_pre{tag}.html"); shutil.copy2(a.html, pre)
    open(a.html, "w", encoding="utf-8", newline="\r\n").write(D.h)
    ver = os.path.join(VERSOES, f"Dashboard_Farma_Sul_{ts}_{tag}.html"); shutil.copy2(a.html, ver)
    dl = os.path.join(DOWNLOADS, f"Dashboard_FarmaSul_Giovano_{ts}.html")
    try: shutil.copy2(a.html, dl)
    except OSError as e: dl = f"(falhou: {e})"
    print(f"\n✓ Dashboard atualizado: {a.html}\n  Backup pré: {pre}\n  Versão:     {ver}\n  Downloads:  {dl}")
    print("  Lembrete: registrar em memory/status.md e na nota diária.")

if __name__ == "__main__":
    main()
