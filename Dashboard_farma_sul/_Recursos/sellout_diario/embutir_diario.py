"""Card 'Venda diária' na Visão detalhada do Sell Out: gráfico de linhas, uma linha por mês, dias 1 a 31 (R$ ou un; diário ou acumulado).
Fontes (o melhor que existe por cliente):
  • São João — Qlik 'mês × produto × data' (dados/sj_qlik/sj_mes_produto_data_*.xlsx, o mais recente): venda real dia a dia desde Jan/25;
    os dias depois do fim do arquivo vêm das fotos diárias do acumulado.
  • DD-Gaúcha — planilhas da distribuidora 'Venda SCJ - <mês>.xlsx' (PERIODO de cada nota): dia a dia real.
  • Nissei, Panvel, DD-GAM, DD-Riomed — fotos diárias do acumulado do mês que a rotina SOdiario grava (dados/valores_*.json):
    venda do dia = acumulado do dia − acumulado da foto anterior; quando a foto pula dias, a diferença é dividida igualmente
    entre eles e o ponto fica marcado como média (estimado).
Uso: python embutir_diario.py [--teste]   (rodar de novo depois de cada SOdiario para o card acompanhar)"""
import collections, datetime as dt, glob, json, os, re, sys
import openpyxl

MAIN = r"C:\Users\valqu\OneDrive\Documentos\Claude\Projects\projeto Dashboard_farma_sul\Dashboard_farma_sul"
sys.path.insert(0, MAIN)
import dashboard_dados as dd

SD = os.path.join(MAIN, "_Recursos", "sellout_diario", "dados")
GCH = os.path.join(MAIN, "_Recursos", "Giovano SCJ", "GAUCHA")
ANO = 2026
NOME = {"saojoao:isadora": "São João · Isadora", "saojoao:caroline": "São João · Caroline", "nissei:andre": "Nissei · Jhonatam", "nissei:edmar": "Nissei · Edmar", "saojoao": "São João", "nissei": "Nissei", "panvel": "Panvel", "ddgam": "DD-GAM", "ddgaucha": "DD-Gaúcha",
        "ddriomed": "DD-Riomed", "clamed": "Clamed", "araujo": "Araujo"}
CHAVES = {"saojoao:isadora": ("SJ_ISA",), "saojoao:caroline": ("SJ_CAR",), "nissei:andre": ("NS_AND",), "nissei:edmar": ("NS_EDM",), "saojoao": ("SJ_ISA", "SJ_CAR"), "nissei": ("NS_AND", "NS_EDM"), "panvel": ("PV",), "ddgam": ("GAM",),
          "ddgaucha": ("GCH",), "ddriomed": ("RIO",)}
D = {}                                           # cli -> {fonte, meses: {'AAAA-MM': {rec:[31], vol:[31], est:[31]}}}


def mes_vazio(): return {"rec": [None] * 31, "vol": [None] * 31, "est": [0] * 31}


def soma_dia(cli, data, rec, vol):
    m = D.setdefault(cli, {"meses": {}})["meses"].setdefault(data.strftime("%Y-%m"), mes_vazio()); i = data.day - 1
    m["rec"][i] = round((m["rec"][i] or 0) + rec, 2); m["vol"][i] = round((m["vol"][i] or 0) + vol, 2)


# ---------------- São João: Qlik por data
sj = sorted(glob.glob(os.path.join(SD, "sj_qlik", "sj_mes_produto_data_*.xlsx")))[-1]
ws = openpyxl.load_workbook(sj, read_only=True, data_only=True).active
rows = list(ws.iter_rows(values_only=True)); H = [str(c) for c in rows[0]]
idt, irs, iq = H.index("Data Venda"), H.index("Valor Venda"), H.index("Quantidade Venda")
fim_sj = None
_h = open(dd.BASE if hasattr(dd, "BASE") else os.path.join(MAIN, "_Recursos", "base", "Dashboard_base.html"), encoding="utf-8").read()
_a = _h.index("const SJC_ESTOQUE = ") + len("const SJC_ESTOQUE = ")
CAROL = {" ".join(x["sku"].upper().split()) for x in json.JSONDecoder().raw_decode(_h[_a:])[0]}     # SKUs da Caroline (conveniência)
for r in rows[1:]:
    if not r or not isinstance(r[idt], dt.datetime): continue
    soma_dia("saojoao", r[idt], float(r[irs] or 0), float(r[iq] or 0)); fim_sj = max(fim_sj or r[idt], r[idt])
    sub = "saojoao:caroline" if " ".join(str(r[H.index("Produto")]).upper().split()) in CAROL else "saojoao:isadora"
    soma_dia(sub, r[idt], float(r[irs] or 0), float(r[iq] or 0))
for k_ in ("saojoao", "saojoao:isadora", "saojoao:caroline"):
    D[k_]["fonte"] = f"Qlik São João (venda por data) até {fim_sj:%d/%m}; depois, fotos diárias do acumulado"
print("SJ Qlik até", fim_sj.date(), os.path.basename(sj))

# ---------------- Gaúcha: notas da distribuidora (mais recente por mês)
por_mes = {}
for f in glob.glob(os.path.join(GCH, "Venda SCJ - *.xlsx")):
    k = os.path.basename(f).lower()
    if k not in por_mes or os.path.getmtime(f) > os.path.getmtime(por_mes[k]): por_mes[k] = f
fim_gch = None
for f in por_mes.values():
    for w in openpyxl.load_workbook(f, read_only=True, data_only=True).worksheets:
        rr = list(w.iter_rows(values_only=True))
        hs = [i for i, x in enumerate(rr[:30]) if x and "PERIODO" in [str(c).strip() for c in x]]
        if not hs: continue
        HH = [str(c).strip() for c in rr[hs[0]]]
        ip, iq2 = HH.index("PERIODO"), HH.index("QTVENDIDA"); iv = HH.index("VENDA R$") if "VENDA R$" in HH else HH.index("VENDA")
        for x in rr[hs[0] + 1:]:
            if not x or not isinstance(x[ip], dt.datetime): continue
            soma_dia("ddgaucha", x[ip], float(x[iv] or 0), float(x[iq2] or 0)); fim_gch = max(fim_gch or x[ip], x[ip])
if fim_gch: D["ddgaucha"]["fonte"] = f"Notas da distribuidora (Venda SCJ) até {fim_gch:%d/%m}"
print("Gaúcha notas até", fim_gch and fim_gch.date(), list(por_mes))

# ---------------- fotos diárias do acumulado (valores_*.json)
fotos = collections.defaultdict(dict)          # (cli, mes) -> {dia: (rec, vol)}
for f in sorted(glob.glob(os.path.join(SD, "valores_*.json"))):
    try: v = json.load(open(f, encoding="utf-8"))
    except Exception: continue
    p = v.get("parcial") or {}
    if not p.get("ate"): continue
    cli_dt = p.get("cli") or {}
    lanc = collections.defaultdict(dict)
    for l in v.get("lancamentos", []): lanc[l["mes"]][l["cliente"]] = l
    for mes, L in lanc.items():
        if mes != p.get("mes"): continue                  # revisões de meses anteriores não são foto do dia
        for cli, ks in CHAVES.items():
            if not all(k in L for k in ks): continue
            dd_, mm_ = map(int, (cli_dt.get(cli.split(":")[0]) or p["ate"]).split("/"))
            if mm_ != mes + 1: continue
            fotos[(cli, mes)][dd_] = (sum(L[k].get("rec") or 0 for k in ks), sum(L[k].get("vol") or 0 for k in ks))

# Isadora × Caroline: o nome do produto não separa 100% como o filtro de comprador do Qlik → a Caroline de cada mês de 2026 é
# ajustada ao total oficial (SJC_REC_26/SJC_VOL_26; no mês corrente, à foto do último dia do arquivo) e a Isadora = total − Caroline.
def _arr(nome):
    a_ = _h.index("const " + nome + " = ") + len("const " + nome + " = "); return json.JSONDecoder().raw_decode(_h[a_:])[0]
OF = {"rec": _arr("SJC_REC_26"), "vol": _arr("SJC_VOL_26")}
for chave, mc in D["saojoao:caroline"]["meses"].items():
    y, mm = map(int, chave.split("-"))
    if y != ANO: continue
    mt, mi = D["saojoao"]["meses"][chave], D["saojoao:isadora"]["meses"][chave]
    lim = 31
    if fim_sj.year == y and fim_sj.month == mm:
        ft = fotos.get(("saojoao:caroline", mm - 1), {}).get(fim_sj.day)
        alvo = {"rec": ft[0], "vol": ft[1]} if ft else None; lim = fim_sj.day
    else:
        alvo = {k: OF[k][mm - 1] for k in OF} if OF["rec"][mm - 1] else None
    if not alvo: continue
    for k in ("rec", "vol"):
        tot = sum(x or 0 for x in mc[k][:lim])
        if not tot or not alvo[k]: continue
        fat = alvo[k] / tot
        for i in range(lim):
            if mc[k][i] is None: continue
            mc[k][i] = round(mc[k][i] * fat, 2); mi[k][i] = round((mt[k][i] or 0) - mc[k][i], 2)

for (cli, mes), F in fotos.items():
    chave = f"{ANO}-{mes + 1:02d}"
    if cli == "ddgaucha" and chave in D.get("ddgaucha", {}).get("meses", {}): continue     # já tem o dia a dia real
    base_dia, base = 0, (0.0, 0.0)
    if cli.startswith("saojoao"):
        if chave in D[cli]["meses"] and fim_sj.month == mes + 1:
            base_dia = fim_sj.day
            if base_dia in F: base = F[base_dia]                      # parte da foto do mesmo dia (mesma régua das fotos)
            else:
                m = D[cli]["meses"][chave]; base = (sum(x or 0 for x in m["rec"]), sum(x or 0 for x in m["vol"]))
        F = {d: x for d, x in F.items() if d > base_dia}
    m = D.setdefault(cli, {"meses": {}})["meses"].setdefault(chave, mes_vazio())
    for d in sorted(F):
        r, v_ = F[d]
        if r < base[0] - 1: continue                                  # acumulado não pode cair (correções de fonte)
        n = d - base_dia
        for i in range(base_dia, d):
            m["rec"][i] = round((r - base[0]) / n, 2); m["vol"][i] = round((v_ - base[1]) / n, 2); m["est"][i] = 1 if n > 1 else 0
        base_dia, base = d, (r, v_)
    if not cli.startswith("saojoao"):
        D[cli]["fonte"] = "Fotos diárias do acumulado (rotina SOdiario); dias sem foto = média do intervalo"
    print(cli, chave, "fotos em", sorted(F))

for cli, fim in (("saojoao", fim_sj), ("saojoao:isadora", fim_sj), ("saojoao:caroline", fim_sj), ("ddgaucha", fim_gch)):          # fonte com data real: dia sem venda/nota = 0 (fim de semana)
    for chave, m in D.get(cli, {}).get("meses", {}).items():
        y, mm = map(int, chave.split("-")); ult = max([i for i, x in enumerate(m["rec"]) if x is not None] or [-1])
        nd = (dt.date(y + mm // 12, mm % 12 + 1, 1) - dt.timedelta(days=1)).day
        lim = ult if (fim and fim.year == y and fim.month == mm) else nd - 1
        for i in range(lim + 1):
            if m["rec"][i] is None: m["rec"][i] = 0; m["vol"][i] = 0
for cli in D:
    D[cli]["nome"] = NOME.get(cli, cli)
    D[cli]["meses"] = dict(sorted(D[cli]["meses"].items()))
SO_DIARIO = json.dumps(D, ensure_ascii=False, separators=(",", ":"))
print("clientes:", {c: len(x["meses"]) for c, x in D.items()}, f"{len(SO_DIARIO) / 1024:.0f} KB")

INI, FIM = "<!-- DIARIO-INI -->", "<!-- DIARIO-FIM -->"
bloco = INI + r"""
<style>
#so-diario{background:#fff;border:1px solid #E2E8F0;border-radius:14px;padding:16px 18px;margin:0 0 18px;box-shadow:0 1px 3px rgba(15,23,42,.06);}
#panel-sellout.op1-on #so-diario{display:none !important;}
#so-diario .sd-top{display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:10px;margin-bottom:10px;}
#so-diario h3{margin:0;font:800 15px Inter,Arial;color:#0D1B2E;}
#so-diario .sd-sub{font:500 11.5px Inter,Arial;color:#64748B;margin-top:2px;}
#so-diario .sd-tg{display:flex;gap:4px;flex-wrap:wrap;}
#so-diario .sd-tg button,#so-diario .sd-mes button{border:1px solid #CBD5E1;background:#fff;border-radius:999px;padding:4px 11px;font:600 11.5px Inter,Arial;color:#334155;cursor:pointer;}
#so-diario .sd-tg button.on{background:#0D1B2E;color:#fff;border-color:#0D1B2E;}
#so-diario .sd-mes{display:flex;gap:5px;flex-wrap:wrap;margin:4px 0 10px;}
#so-diario .sd-mes button.on{color:#fff;border-color:transparent;}
#so-diario .sd-kpis{display:flex;gap:10px;flex-wrap:wrap;margin-bottom:8px;}
#so-diario .sd-kpi{background:#F8FAFC;border:1px solid #E2E8F0;border-radius:10px;padding:7px 12px;min-width:130px;}
#so-diario .sd-kpi b{display:block;font:800 16px Inter,Arial;color:#0D1B2E;}
#so-diario .sd-kpi span{font:600 10.5px Inter,Arial;color:#64748B;text-transform:uppercase;letter-spacing:.03em;}
#so-diario .sd-graf{position:relative;height:300px;}
#so-diario .sd-nota{font:500 10.5px Inter,Arial;color:#94A3B8;margin-top:6px;}
#so-diario .sd-vazio{padding:28px;text-align:center;color:#64748B;font:italic 500 12.5px Inter,Arial;}
</style>
<script>
/* Venda diária (linha do tempo dia 1–31 por mês) — gerado por _Recursos/sellout_diario/embutir_diario.py */
var SO_DIARIO = __DADOS__;
var SDV = {met:'rec', modo:'dia', sel:{}, chart:null};
var SD_CORES = ['#1D4ED8','#F59E0B','#10B981','#DC2626','#7C3AED','#0891B2','#DB2777','#65A30D','#475569','#EA580C','#0F766E','#9333EA'];
var SD_MES = ['Jan','Fev','Mar','Abr','Mai','Jun','Jul','Ago','Set','Out','Nov','Dez'];
function sdNomeMes(k){ var p=k.split('-'); return SD_MES[+p[1]-1]+'/'+p[0].slice(2); }
function sdCli(){ var s=document.getElementById('sellout-client-selector'), c=s ? s.value : '', sub='total';
  if(c==='saojoao' && typeof sjModo!=='undefined') sub=sjModo; else if(c==='nissei' && typeof nsComprador!=='undefined') sub=nsComprador;
  return (sub && sub!=='total' && SO_DIARIO[c+':'+sub]) ? c+':'+sub : c; }
function sdFmt(v, curto){ if(v==null) return '—'; if(SDV.met==='vol') return Math.round(v).toLocaleString('pt-BR')+' un';
  if(curto && Math.abs(v)>=1e6) return 'R$ '+(v/1e6).toLocaleString('pt-BR',{maximumFractionDigits:2})+' mi';
  if(curto && Math.abs(v)>=1e3) return 'R$ '+(v/1e3).toLocaleString('pt-BR',{maximumFractionDigits:1})+' mil';
  return 'R$ '+v.toLocaleString('pt-BR',{maximumFractionDigits:0}); }
function sdPadrao(meses){ var ks=Object.keys(meses).sort(), u=ks[ks.length-1], s={}; if(!u) return s; s[u]=1;
  var p=u.split('-'), y=+p[0], m=+p[1], ant=(m===1?(y-1)+'-12':y+'-'+('0'+(m-1)).slice(-2)), aa=(y-1)+'-'+p[1];
  if(meses[ant]) s[ant]=1; if(meses[aa]) s[aa]=1; return s; }
function sdSerie(arr){ if(SDV.modo==='dia') return arr.slice(); var a=0, out=[], ult=-1; arr.forEach(function(v,i){ if(v!=null) ult=i; });
  return arr.map(function(v,i){ if(i>ult) return null; a+=(v||0); return Math.round(a*100)/100; }); }
function sdRender(){
  var box=document.getElementById('so-diario'); if(!box) return;
  var cli=sdCli(), C=SO_DIARIO[cli];
  box.hidden = (cli==='araujo');   /* Araujo: sem card de venda diária (pedido 27/11) */
  if(box.hidden){ if(SDV.chart){ SDV.chart.destroy(); SDV.chart=null; } box.innerHTML=''; return; }
  if(!C){ box.innerHTML='<div class="sd-top"><div><h3>Venda diária · linha do tempo</h3><div class="sd-sub">'+((document.querySelector('#sellout-client-selector option:checked')||{}).textContent||'')+'</div></div></div><div class="sd-vazio">Ainda não há venda diária deste cliente (sem portal com data nem fotos diárias do acumulado).</div>'; if(SDV.chart){ SDV.chart.destroy(); SDV.chart=null; } return; }
  if(!SDV.sel[cli]) SDV.sel[cli]=sdPadrao(C.meses);
  var ks=Object.keys(C.meses).sort().reverse(), sel=SDV.sel[cli];
  var ordem=ks.filter(function(k){ return sel[k]; }), cor=function(k){ return SD_CORES[ordem.indexOf(k)%SD_CORES.length]; };   /* cor pela posição entre os meses escolhidos (o mais recente é azul) */
  var h='<div class="sd-top"><div><h3>Venda diária · linha do tempo — '+C.nome+'</h3><div class="sd-sub">Dia 1 a 31, uma linha por mês · escolha os meses abaixo</div></div>'
    +'<div class="sd-tg"><button data-k="met" data-v="rec" class="'+(SDV.met==='rec'?'on':'')+'">R$</button><button data-k="met" data-v="vol" class="'+(SDV.met==='vol'?'on':'')+'">Unidades</button>'
    +'<span style="width:8px"></span><button data-k="modo" data-v="dia" class="'+(SDV.modo==='dia'?'on':'')+'">Diário</button><button data-k="modo" data-v="acum" class="'+(SDV.modo==='acum'?'on':'')+'">Acumulado</button></div></div>';
  h+='<div class="sd-mes">'+ks.map(function(k){ var on=sel[k]; return '<button data-m="'+k+'" class="'+(on?'on':'')+'" style="'+(on?'background:'+cor(k):'')+'">'+sdNomeMes(k)+'</button>'; }).join('')+'</div>';
  var u=ks[0], M=C.meses[u][SDV.met], dias=M.map(function(v,i){ return v==null?null:i; }).filter(function(x){ return x!=null; });
  var tot=M.reduce(function(a,v){ return a+(v||0); },0), nd=dias.length, best=-1; M.forEach(function(v,i){ if(v!=null && C.meses[u].est[i]===0 && (best<0 || v>M[best])) best=i; });
  h+='<div class="sd-kpis"><div class="sd-kpi"><span>'+sdNomeMes(u)+' até dia '+(nd?dias[nd-1]+1:'—')+'</span><b>'+sdFmt(tot,true)+'</b></div>'
    +'<div class="sd-kpi"><span>Média por dia</span><b>'+sdFmt(nd?tot/nd:null,true)+'</b></div>'
    +'<div class="sd-kpi"><span>Melhor dia (real)</span><b>'+(best<0?'—':(best+1)+' · '+sdFmt(M[best],true))+'</b></div></div>';
  h+='<div class="sd-graf"><canvas id="sd-cv"></canvas></div><div class="sd-nota">Fonte: '+C.fonte+'. Ponto vazado = média de dias sem foto diária (estimado).</div>';
  box.innerHTML=h;
  box.querySelectorAll('.sd-tg button').forEach(function(b){ b.onclick=function(){ SDV[b.getAttribute('data-k')]=b.getAttribute('data-v'); sdRender(); }; });
  box.querySelectorAll('.sd-mes button').forEach(function(b){ b.onclick=function(){ var k=b.getAttribute('data-m'); if(sel[k]) delete sel[k]; else sel[k]=1; sdRender(); }; });
  var todos=Object.keys(C.meses).sort();
  var ds=todos.filter(function(k){ return sel[k]; }).map(function(k){ var cr=cor(k), E=C.meses[k].est;
    return {label:sdNomeMes(k), data:sdSerie(C.meses[k][SDV.met]), borderColor:cr, backgroundColor:cr, borderWidth:k===u?3:2, tension:0.25, spanGaps:false,
      pointRadius:function(c){ return E[c.dataIndex] ? 3 : 2.5; }, pointBackgroundColor:function(c){ return E[c.dataIndex] ? '#fff' : cr; }, pointBorderColor:cr,
      segment:{borderDash:function(c){ return (SDV.modo==='dia' && (E[c.p0DataIndex]||E[c.p1DataIndex])) ? [4,3] : undefined; }}, _est:E};
  });
  if(SDV.chart){ try{ SDV.chart.destroy(); }catch(e){} }
  if(typeof Chart==='undefined') return;
  SDV.chart = new Chart(document.getElementById('sd-cv'), {type:'line', data:{labels:Array.from({length:31},function(_,i){ return i+1; }), datasets:ds},
    options:{responsive:true, maintainAspectRatio:false, animation:false, interaction:{mode:'index', intersect:false},
      plugins:{legend:{position:'top', labels:{boxWidth:12, font:{size:11}}},
        tooltip:{callbacks:{title:function(it){ return 'Dia '+it[0].label; }, label:function(c){ return c.dataset.label+': '+sdFmt(c.raw)+(c.dataset._est[c.dataIndex]&&SDV.modo==='dia'?' (média)':''); }}}},
      scales:{x:{title:{display:true, text:'dia do mês', font:{size:10}}, grid:{display:false}, ticks:{font:{size:10}}},
        y:{beginAtZero:true, grid:{color:'rgba(148,163,184,.18)'}, ticks:{font:{size:10}, callback:function(v){ return sdFmt(v,true); }}}}}});
}
function sdInit(){
  var f=document.querySelector('#panel-sellout > .filters'); if(!f || typeof switchSellOutClient!=='function'){ setTimeout(sdInit,500); return; }
  if(!document.getElementById('so-diario')){ var d=document.createElement('div'); d.id='so-diario'; f.parentNode.insertBefore(d, f.nextSibling); }
  var fn=window.switchSellOutClient;
  if(!fn._sd){ var w=function(){ var r=fn.apply(this, arguments); setTimeout(sdRender,60); return r; }; w._sd=true; w._op1=fn._op1; w._revppt=fn._revppt; w._opppt=fn._opppt; w._jbp=fn._jbp; window.switchSellOutClient=w; }
  document.querySelectorAll('#sj-compradora-row button, #ns-compradora-row button').forEach(function(b){ b.addEventListener('click', function(){ setTimeout(sdRender, 120); }); });
  sdRender();
}
if(document.readyState==='loading') document.addEventListener('DOMContentLoaded', function(){ setTimeout(sdInit, 2800); }); else setTimeout(sdInit, 2800);
</script>
""".replace("__DADOS__", SO_DIARIO) + FIM

d = dd.Dashboard()
if INI in d.h:
    a = d.h.index(INI); b = d.h.index(FIM) + len(FIM); d.h = d.h[:a] + bloco + d.h[b:]; print("bloco DIARIO trocado")
else:
    k = d.h.rindex("</body>"); d.h = d.h[:k] + bloco + "\n" + d.h[k:]; print("bloco DIARIO inserido antes de </body>")
if "--teste" in sys.argv:
    out = os.path.join(dd.VERS, f"Dashboard_Farma_Sul_{dd.carimbo()}_testeDiario.html")
    open(out, "w", encoding="utf-8", newline="").write(d.h); print("teste:", out)
else:
    print(d.salvar("Diario"))
