"""One Page (24/11/2026) — pedidos do Giovano sobre o One Page da Araujo (slide SCJ YTD Out/26):
  1) Sell-out por marca: gráficos de diferença (YTD e mês) em % de variação no lugar de R$ (todos os clientes)
  2) Clientes com meta JBP: quadro ao lado do Sell-out Total com barras YTD 2025 · YTD 2026 · Meta YTD (valores escritos) e
     'vs Hist' / 'vs Meta'; rótulo da projeção mostra o ritmo usado (set/out na Araujo). JBP Perfumaria YTD Out = R$ 4.683.059 (slide)
  3) Seção 'Mercado Nielsen' por marca (mercado da região do cliente): categoria, OFF!+Exposis e categoria BR Farma (Jan–Out vs 2025)
     + tabela de marcas (faturamento, variação, share 2025→2026, var. p.p.), da base Nielsen do dashboard (NQ_PR, % valor).
     Moskitoff, Above e OAZ não vêm separadas no Nielsen do dashboard (ficam em 'All Others').
Uso: python op1_pct_meta_nielsen.py <base.html>"""
import sys, re, json
H = sys.argv[1]; h = open(H, encoding="utf-8", newline="").read()


def rep(a, b, n=1):
    global h
    if h.count(a) != n and h.count(a.replace("\n", "\r\n")) == n: a, b = a.replace("\n", "\r\n"), b.replace("\n", "\r\n")
    assert h.count(a) == n, (h.count(a), a[:90]); h = h.replace(a, b)


assert "NQ_MERC" not in h, "já aplicado"
# ── 1) diferenças em % ──
rep("    var hb = function(id,data,colors,signed){\n      var fmtV = function(v){ return signed ? op1K(mk,v)",
    "    var hb = function(id,data,colors,signed,pct){\n      var fmtV = function(v){ return pct ? (v==null?'novo':(v>=0?'+':'−')+op1Num(Math.abs(v),1)+'%') : signed ? op1K(mk,v)")
rep("tooltip:{callbacks:{label:function(c){ return signed ? op1K(mk,c.raw) : (mk==='val'?'R$ '+op1Num(c.raw,1)+'k':op1Num(c.raw)+' un'); }}}},",
    "tooltip:{callbacks:{label:function(c){ return pct ? fmtV(c.raw) : signed ? op1K(mk,c.raw) : (mk==='val'?'R$ '+op1Num(c.raw,1)+'k':op1Num(c.raw)+' un'); }}}},")
rep("    var d1 = [t26-t25].concat(sk.map(function(s){return s.a26-s.a25;})), d2 = [tm26-tm25].concat(sk.map(function(s){return s.m26-s.m25;}));",
    "    var vp = function(a,b){ return b>0 ? Math.round((a/b-1)*1000)/10 : null; };\n"
    "    var d1 = [vp(t26,t25)].concat(sk.map(function(s){return vp(s.a26,s.a25);})), d2 = [vp(tm26,tm25)].concat(sk.map(function(s){return vp(s.m26,s.m25);}));")
rep("    hb('op1-b'+bi+'-2', d1, d1.map(function(v,i){ return v<0?(i?OP1_C.negB:OP1_C.neg):(i?OP1_C.posB:OP1_C.pos); }), true);\n    hb('op1-b'+bi+'-3', d2, d2.map(function(v,i){ return v<0?(i?OP1_C.negB:OP1_C.neg):(i?OP1_C.posB:OP1_C.pos); }), true);",
    "    hb('op1-b'+bi+'-2', d1, d1.map(function(v,i){ return v<0?(i?OP1_C.negB:OP1_C.neg):(i?OP1_C.posB:OP1_C.pos); }), true, true);\n    hb('op1-b'+bi+'-3', d2, d2.map(function(v,i){ return v<0?(i?OP1_C.negB:OP1_C.neg):(i?OP1_C.posB:OP1_C.pos); }), true, true);")
rep("<div class=\"op1-ct\">Diferença – 2026 vs 2025 <span>(YTD)</span></div>", "<div class=\"op1-ct\">Variação % – 2026 vs 2025 <span>(YTD)</span></div>")
rep("<div class=\"op1-ct\">Diferença – '+mesRef+' vs '+OP1_MES[mRef]+'/25</div>", "<div class=\"op1-ct\">Variação % – '+mesRef+' vs '+OP1_MES[mRef]+'/25</div>")
# ── 2) quadro YTD 2025 · 2026 · Meta ──
rep("<div class=\"op1-ms\">ritmo do YTD</div></div>'", "<div class=\"op1-ms\">'+(gP!==g?'ritmo de '+OP1_MES[last-1].toLowerCase()+'/'+OP1_MES[last].toLowerCase():'ritmo do YTD')+'</div></div>'")
rep("  op1Chart('op1-ano', {type:'bar', data:{labels:['2025','2026 proj.'], datasets:[",
    """  if(X.jbp){ var _vl={id:'op1anoV', afterDatasetsDraw:function(ch){ var c=ch.ctx, m=ch.getDatasetMeta(0); c.save(); c.font='800 10px system-ui,sans-serif'; c.fillStyle='#fff'; c.textAlign='center';
      m.data.forEach(function(b,i){ var v=ch.data.datasets[0].data[i]; c.save(); c.translate(b.x, b.base-8); c.rotate(-Math.PI/2); c.textAlign='left'; c.textBaseline='middle'; c.fillText(Math.round(v).toLocaleString('pt-BR'), 0, 0); c.restore(); }); c.restore(); }};
    op1Chart('op1-ano', {type:'bar', data:{labels:['YTD 2025','YTD 2026','Meta YTD'], datasets:[{data:[ytd25, ytd26, jY], backgroundColor:['#2A9D7C','#2E2A6B','#F5A524'], borderRadius:3, barPercentage:0.75}]},
      plugins:[_vl], options:{responsive:true, maintainAspectRatio:false, animation:false, plugins:{legend:{display:false}, title:{display:true, text:ytdLbl+': 2025 · 2026 · meta JBP', color:'#0D1B2E', font:{size:11, weight:'700'}},
        tooltip:{callbacks:{label:function(c){ return op1Val('val',c.raw); }}}}, scales:{x:{grid:{display:false}, ticks:{font:{size:10}}}, y:{beginAtZero:true, grid:{color:OP1_C.grid}, ticks:{font:{size:9}, callback:fmtAx}}}}});
  } else
  op1Chart('op1-ano', {type:'bar', data:{labels:['2025','2026 proj.'], datasets:[""")
rep("       + (X.jbp ? '<div class=\"op1-mb\"><div class=\"op1-ml\">vs Meta JBP YTD</div>",
    "       + (X.jbp ? '<div class=\"op1-mb\"><div class=\"op1-ml\">Ano proj. vs JBP</div><div class=\"op1-mv\" style=\"color:'+op1Cor(jAnoP)+'\">'+op1Pct(jAnoP)+'</div><div class=\"op1-ms\">meta ano '+op1Val('val',jAno)+'</div></div>' : '')\n"
    "       + (X.jbp ? '<div class=\"op1-mb\"><div class=\"op1-ml\">vs Meta JBP YTD</div>")
rep("  var jY = 0; if(X.jbp){ for(var _j=0;_j<=last;_j++) jY += X.jbp[_j]||0; }",
    "  var jY = 0, jAno = 0; if(X.jbp){ for(var _j=0;_j<=last;_j++) jY += X.jbp[_j]||0; X.jbp.forEach(function(v){ jAno += v||0; }); }")
# jAnoP depende de ano26 (definido antes do HTML do quadro)
rep("  var titulo = 'One Page SC Johnson & '+X.nome", "  var jAnoP = (X.jbp && jAno>0) ? ano26/jAno-1 : null;\n  var titulo = 'One Page SC Johnson & '+X.nome")
# JBP Perfumaria YTD Out = R$ 4.683.059 (slide): diferença em Set
i = h.index("var ARAUJO_JBP = "); jb, k = json.JSONDecoder().raw_decode(h[i + len("var ARAUJO_JBP = "):])
dif = 4683059 - sum(jb["perfumaria"][:10]); jb["perfumaria"][8] += dif; print("JBP Perfumaria ajuste Set", dif, "→ YTD", sum(jb["perfumaria"][:10]))
h = h[:i] + "var ARAUJO_JBP = " + json.dumps(jb, ensure_ascii=False, separators=(",", ":")) + h[i + len("var ARAUJO_JBP = ") + k:]
# ── 3) Mercado Nielsen por marca ──
m = re.search(r"var NQ_PR\s*=\s*", h); NQ = json.JSONDecoder().raw_decode(h[m.end():])[0]; MES = NQ["meses"]
y26 = [MES.index("Jan/26") + q for q in range(10)]; y25 = [MES.index("Jan/25") + q for q in range(10)]
MK = {"saojoao": "Farma Sul", "nissei": "INFC PR", "panvel": "Farma Sul", "clamed": "INFC SC", "araujo": "INFC MG"}
LBL = {"OFF!": "OFF", "EXPOSIS": "EXPOSIS", "XO INSETO": "XÔ INSETO", "SUPER REPELEX": "REPELEX", "SBP": "SBP", "ALL OTHERS CAMP": "OUTRAS (inclui Moskitoff, Above, OAZ…)"}
def tab(mk):
    d = NQ["mk"][mk]; sv = lambda b, P: sum(d[b]["v"][p] or 0 for p in P); T6, T5 = sv("TOTAL MERCADO", y26), sv("TOTAL MERCADO", y25)
    B = [[LBL.get(b, b), round(sv(b, y26), 2), round((sv(b, y26) / sv(b, y25) - 1) * 100, 1), round(sv(b, y25) / T5 * 100, 1), round(sv(b, y26) / T6 * 100, 1)] for b in d if b != "TOTAL MERCADO"]
    B.sort(key=lambda r: -r[1] if not r[0].startswith("OUTRAS") else 1)
    scj6, scj5 = sv("OFF!", y26) + sv("EXPOSIS", y26), sv("OFF!", y25) + sv("EXPOSIS", y25)
    return {"mk": mk, "cat": [round(T6, 1), round(T5, 1)], "scj": [round(scj6, 1), round(scj5, 1)], "part": [round(scj6 / T6 * 100, 1), round(scj5 / T5 * 100, 1)], "marcas": B}
MERC = {cli: tab(mk) for cli, mk in MK.items()}; MERC["_br"] = tab("T.BR Farma")
print("Araujo", MERC["araujo"]["cat"], MERC["araujo"]["scj"], MERC["araujo"]["part"])
JS = r"""
/* Mercado Nielsen por marca no One Page (Jan–Out/26 vs Jan–Out/25, % valor, mercado da região do cliente) */
var NQ_MERC = __M__;
function op1MercHtml(cli){
  var M = NQ_MERC[cli], BR = NQ_MERC._br; if(!M) return '';
  var v = function(a){ return a[1]>0 ? (a[0]/a[1]-1)*100 : null; }, sg = function(x,d){ return x==null?'—':(x>=0?'+':'−')+op1Num(Math.abs(x),d==null?1:d); };
  var cor = function(x){ return x==null?OP1_C.mut:(x>=0?OP1_C.pos:OP1_C.neg); };
  var card = function(tag, var_, val, sub, extra){ return '<div class="card op1-card" style="padding:12px 14px;"><div style="font-size:10px;font-weight:800;color:#2E2A6B;letter-spacing:.04em;">'+tag+'</div>'
    +'<div style="display:flex;justify-content:space-between;align-items:baseline;margin-top:6px;"><span style="font-size:24px;font-weight:800;color:'+cor(var_)+';">'+sg(var_)+'%</span><span style="font-size:13px;font-weight:700;color:#0D1B2E;">R$ '+op1Num(val,1)+' mi</span></div>'
    +'<div style="font-size:10.5px;color:#64748B;margin-top:4px;">'+sub+'</div>'+(extra?'<div style="font-size:10.5px;font-weight:700;color:#059669;margin-top:2px;">'+extra+'</div>':'')+'</div>'; };
  var dP = M.part[0]-M.part[1];
  var h = op1Sec('Mercado Nielsen – '+M.mk+' (Jan–Out vs 2025)');
  h += '<div class="op1-row" style="grid-template-columns:repeat(3,1fr);">'
     + card('CATEGORIA REPELENTE · '+M.mk.toUpperCase(), v(M.cat), M.cat[0], 'vs R$ '+op1Num(M.cat[1],1)+' mi em 2025 ('+sg(M.cat[0]-M.cat[1])+' mi)')
     + card('OFF + EXPOSIS · '+M.mk.toUpperCase(), v(M.scj), M.scj[0], 'vs R$ '+op1Num(M.scj[1],1)+' mi em 2025 ('+sg(M.scj[0]-M.scj[1])+' mi)', 'Participação '+op1Num(M.part[0],1)+'% ('+sg(dP)+' p.p.)')
     + card('CATEGORIA REPELENTE · BR FARMA', v(BR.cat), BR.cat[0], 'vs R$ '+op1Num(BR.cat[1],1)+' mi em 2025 ('+sg(BR.cat[0]-BR.cat[1])+' mi)') + '</div>';
  var mx = Math.max.apply(null, M.marcas.map(function(r){ return r[1]; })), mp = Math.max.apply(null, M.marcas.map(function(r){ return Math.abs(r[4]-r[3]); }))||1;
  var th='padding:6px 8px;font-size:10px;font-weight:700;color:#64748B;border-bottom:1.5px solid rgba(94,153,208,0.35);text-align:left;', td='padding:6px 8px;font-size:11.5px;border-bottom:0.5px solid #E2E8F0;';
  h += '<div class="card op1-card"><div style="font-size:12px;font-weight:800;color:#2E2A6B;margin-bottom:6px;">Marcas em '+M.mk+' – faturamento, variação e share de mercado (Jan–Out/26 vs 2025)</div><div style="overflow:auto;"><table style="width:100%;border-collapse:collapse;"><thead><tr>'
     + '<th style="'+th+'">Marca</th><th style="'+th+'">Faturamento Jan–Out/26 (R$ mi)</th><th style="'+th+'text-align:right;">Var. faturamento</th><th style="'+th+'text-align:center;">Share de mercado (2025 → 2026)</th><th style="'+th+'">Var. share (p.p.)</th></tr></thead><tbody>'
     + M.marcas.map(function(r){ var scj = r[0]==='OFF'||r[0]==='EXPOSIS', dp = r[4]-r[3];
         return '<tr style="'+(scj?'background:rgba(46,42,107,0.06);':'')+'"><td style="'+td+'font-weight:'+(scj?'800':'600')+';color:#0D1B2E;">'+r[0]+'</td>'
           + '<td style="'+td+'"><div style="display:flex;align-items:center;gap:8px;"><span style="display:inline-block;height:12px;width:'+Math.max(2,Math.round(r[1]/mx*220))+'px;background:'+(r[0]==='OFF'?'#2E2A6B':r[0]==='EXPOSIS'?'#7C3AED':'#CBD5E1')+';border-radius:2px;"></span><b>R$ '+op1Num(r[1],1)+' mi</b></div></td>'
           + '<td style="'+td+'text-align:right;font-weight:700;color:'+cor(r[2])+';">'+sg(r[2])+'</td><td style="'+td+'text-align:center;">'+op1Num(r[3],1)+'% → '+op1Num(r[4],1)+'%</td>'
           + '<td style="'+td+'"><div style="display:flex;align-items:center;gap:6px;"><div style="width:120px;position:relative;height:12px;"><span style="position:absolute;left:60px;top:0;bottom:0;border-left:1px solid #94A3B8;"></span><span style="position:absolute;top:1px;height:10px;'+(dp>=0?'left:60px;':'right:60px;')+'width:'+Math.round(Math.abs(dp)/mp*58)+'px;background:'+(dp>=0?'#16A34A':'#DC2626')+';"></span></div><b style="color:'+cor(dp)+';">'+sg(dp)+'</b></div></td></tr>'; }).join('')
     + '</tbody></table></div></div>';
  var S = M.marcas.filter(function(r){ return !/^OUTRAS/.test(r[0]); }).map(function(r){ return [r[0], r[4]-r[3]]; }).sort(function(a,b){ return b[1]-a[1]; });
  var neg = S.filter(function(x){ return x[1]<0; }).slice(-2).reverse();
  h += op1Box('<b>'+S[0][0]+'</b> é quem mais ganha share em '+M.mk+' ('+sg(S[0][1])+' p.p.)'+(neg.length?'; '+neg.map(function(x){ return '<b>'+x[0]+'</b>'; }).join(' e ')+' '+(neg.length>1?'são quem mais perdem':'é quem mais perde')+'.':'.')
     + '<div style="font-size:10px;color:#94A3B8;margin-top:4px;">Fonte: Nielsen (base do dashboard), % valor, Jan–Out/26 vs Jan–Out/25. O Nielsen não mede rede: é o mercado da região do cliente. Moskitoff, Above e OAZ não vêm separadas nesta base (estão em Outras).</div>');
  return h;
}
"""
rep("var SHARE_NQ = ", JS.replace("__M__", json.dumps(MERC, ensure_ascii=False, separators=(",", ":"))).strip() + "\nvar SHARE_NQ = ")
rep("  if(typeof SHARE_IQ!=='undefined' && SHARE_IQ[X.cli] && !_semShare) h += op1Sec('Share no cliente – IQVIA · Nielsen') + iqShareHtml(X.cli);",
    "  if(typeof NQ_MERC!=='undefined' && NQ_MERC[X.cli] && !_semShare) h += op1MercHtml(X.cli);\n"
    "  if(typeof SHARE_IQ!=='undefined' && SHARE_IQ[X.cli] && !_semShare) h += op1Sec('Share no cliente – IQVIA · Nielsen') + iqShareHtml(X.cli);")
open(H, "w", encoding="utf-8", newline="").write(h); print("ok")
