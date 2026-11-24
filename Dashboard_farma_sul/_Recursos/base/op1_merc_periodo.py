"""One Page › Mercado Nielsen (24/11/2026): filtro de período na seção (Jan–Out/26 ano-calendário · FY27 Jul–Out/26 · Out/26 ·
últimos 12 meses · FY26 Jul/25–Jun/26), calculado na hora a partir da base Nielsen do dashboard (NQ_PR, % valor).
Uso: python op1_merc_periodo.py <base.html>"""
import sys
H = sys.argv[1]; h = open(H, encoding="utf-8", newline="").read()
assert "op1MercPer" not in h, "já aplicado"
a = h.index("function op1MercHtml(cli){"); b = h.index("\nvar SHARE_NQ = ", a)
NOVO = r"""var op1MercPer = 'cal';
var OP1_MERC_PER = {cal:{t:'Jan–Out/26 (ano-calendário)', c:'Jan–Out/26 vs Jan–Out/25', a:['Jan/26','Out/26'], p:['Jan/25','Out/25']},
  fy27:{t:'FY27 · Jul–Out/26', c:'Jul–Out/26 vs Jul–Out/25', a:['Jul/26','Out/26'], p:['Jul/25','Out/25']},
  mes:{t:'Out/26 (mês)', c:'Out/26 vs Out/25', a:['Out/26','Out/26'], p:['Out/25','Out/25']},
  mat:{t:'Últimos 12 meses (Nov/25–Out/26)', c:'Nov/25–Out/26 vs Nov/24–Out/25', a:['Nov/25','Out/26'], p:['Nov/24','Out/25']},
  fy26:{t:'FY26 · Jul/25–Jun/26', c:'Jul/25–Jun/26 vs Jul/24–Jun/25', a:['Jul/25','Jun/26'], p:['Jul/24','Jun/25']}};
function op1MercSet(v){ op1MercPer = v; if(typeof op1Render==='function') op1Render(); }
function op1MercTab(mk, per){
  var d = NQ_PR.mk[mk]; if(!d) return null; var M = NQ_PR.meses, P = OP1_MERC_PER[per] || OP1_MERC_PER.cal;
  var rg = function(x){ var i0=M.indexOf(x[0]), i1=M.indexOf(x[1]), r=[]; for(var i=i0;i<=i1 && i0>=0;i++) r.push(i); return r; }, A = rg(P.a), B = rg(P.p);
  var sv = function(b, I){ return I.reduce(function(s,i){ return s+((d[b]&&d[b].v[i])||0); },0); };
  var T6 = sv('TOTAL MERCADO',A), T5 = sv('TOTAL MERCADO',B);
  var LB = {'OFF!':'OFF','EXPOSIS':'EXPOSIS','XO INSETO':'XÔ INSETO','SUPER REPELEX':'REPELEX','SBP':'SBP','ALL OTHERS CAMP':'OUTRAS (inclui Moskitoff, Above, OAZ…)'};
  var rows = Object.keys(d).filter(function(b){ return b!=='TOTAL MERCADO'; }).map(function(b){ var x=sv(b,A), y=sv(b,B); return [LB[b]||b, x, y>0?(x/y-1)*100:null, T5>0?y/T5*100:0, T6>0?x/T6*100:0]; });
  rows.sort(function(r,s){ return (/^OUTRAS/.test(r[0])?1:0)-(/^OUTRAS/.test(s[0])?1:0) || s[1]-r[1]; });
  var s6 = sv('OFF!',A)+sv('EXPOSIS',A), s5 = sv('OFF!',B)+sv('EXPOSIS',B);
  return {mk:mk, cat:[T6,T5], scj:[s6,s5], part:[T6>0?s6/T6*100:0, T5>0?s5/T5*100:0], marcas:rows, per:P};
}
function op1MercHtml(cli){
  if(!NQ_MERC[cli] || typeof NQ_PR==='undefined') return '';
  var M = op1MercTab(NQ_MERC[cli].mk, op1MercPer), BR = op1MercTab('T.BR Farma', op1MercPer); if(!M) return '';
  var v = function(a){ return a[1]>0 ? (a[0]/a[1]-1)*100 : null; }, sg = function(x,dd){ return x==null?'—':(x>=0?'+':'−')+op1Num(Math.abs(x),dd==null?1:dd); };
  var cor = function(x){ return x==null?OP1_C.mut:(x>=0?OP1_C.pos:OP1_C.neg); };
  var card = function(tag, var_, val, sub, extra){ return '<div class="card op1-card" style="padding:12px 14px;"><div style="font-size:10px;font-weight:800;color:#2E2A6B;letter-spacing:.04em;">'+tag+'</div>'
    +'<div style="display:flex;justify-content:space-between;align-items:baseline;margin-top:6px;"><span style="font-size:24px;font-weight:800;color:'+cor(var_)+';">'+sg(var_)+'%</span><span style="font-size:13px;font-weight:700;color:#0D1B2E;">R$ '+op1Num(val,1)+' mi</span></div>'
    +'<div style="font-size:10.5px;color:#64748B;margin-top:4px;">'+sub+'</div>'+(extra?'<div style="font-size:10.5px;font-weight:700;color:#059669;margin-top:2px;">'+extra+'</div>':'')+'</div>'; };
  var dP = M.part[0]-M.part[1], P = M.per;
  var opts = Object.keys(OP1_MERC_PER).map(function(k){ return '<option value="'+k+'"'+(k===op1MercPer?' selected':'')+'>'+OP1_MERC_PER[k].t+'</option>'; }).join('');
  var h = op1Sec('Mercado Nielsen – '+M.mk+' ('+P.c+')');
  h += '<div style="display:flex;align-items:center;gap:8px;margin:-2px 0 10px;"><span style="font-size:10px;font-weight:800;color:#64748B;letter-spacing:.06em;">📅 PERÍODO</span>'
     + '<select onchange="op1MercSet(this.value)" style="font-size:12px;font-weight:600;padding:5px 10px;border-radius:6px;border:1px solid rgba(29,111,168,0.45);background:#fff;color:#0D1B2E;cursor:pointer;">'+opts+'</select>'
     + '<span style="font-size:10.5px;color:#64748B;">'+P.c+' · vale para os cards e a tabela de marcas desta seção</span></div>';
  h += '<div class="op1-row" style="grid-template-columns:repeat(3,1fr);">'
     + card('CATEGORIA REPELENTE · '+M.mk.toUpperCase(), v(M.cat), M.cat[0], 'vs R$ '+op1Num(M.cat[1],1)+' mi no ano anterior ('+sg(M.cat[0]-M.cat[1])+' mi)')
     + card('OFF + EXPOSIS · '+M.mk.toUpperCase(), v(M.scj), M.scj[0], 'vs R$ '+op1Num(M.scj[1],1)+' mi no ano anterior ('+sg(M.scj[0]-M.scj[1])+' mi)', 'Participação '+op1Num(M.part[0],1)+'% ('+sg(dP)+' p.p.)')
     + card('CATEGORIA REPELENTE · BR FARMA', v(BR.cat), BR.cat[0], 'vs R$ '+op1Num(BR.cat[1],1)+' mi no ano anterior ('+sg(BR.cat[0]-BR.cat[1])+' mi)') + '</div>';
  var mx = Math.max.apply(null, M.marcas.map(function(r){ return r[1]; }))||1, mp = Math.max.apply(null, M.marcas.map(function(r){ return Math.abs(r[4]-r[3]); }))||1;
  var th='padding:6px 8px;font-size:10px;font-weight:700;color:#64748B;border-bottom:1.5px solid rgba(94,153,208,0.35);text-align:left;', td='padding:6px 8px;font-size:11.5px;border-bottom:0.5px solid #E2E8F0;';
  h += '<div class="card op1-card"><div style="font-size:12px;font-weight:800;color:#2E2A6B;margin-bottom:6px;">Marcas em '+M.mk+' – faturamento, variação e share de mercado ('+P.c+')</div><div style="overflow:auto;"><table style="width:100%;border-collapse:collapse;"><thead><tr>'
     + '<th style="'+th+'">Marca</th><th style="'+th+'">Faturamento '+P.a[0]+(P.a[0]!==P.a[1]?'–'+P.a[1]:'')+' (R$ mi)</th><th style="'+th+'text-align:right;">Var. faturamento</th><th style="'+th+'text-align:center;">Share de mercado (ano ant. → atual)</th><th style="'+th+'">Var. share (p.p.)</th></tr></thead><tbody>'
     + M.marcas.map(function(r){ var scj = r[0]==='OFF'||r[0]==='EXPOSIS', dp = r[4]-r[3];
         return '<tr style="'+(scj?'background:rgba(46,42,107,0.06);':'')+'"><td style="'+td+'font-weight:'+(scj?'800':'600')+';color:#0D1B2E;">'+r[0]+'</td>'
           + '<td style="'+td+'"><div style="display:flex;align-items:center;gap:8px;"><span style="display:inline-block;height:12px;width:'+Math.max(2,Math.round(r[1]/mx*220))+'px;background:'+(r[0]==='OFF'?'#2E2A6B':r[0]==='EXPOSIS'?'#7C3AED':'#CBD5E1')+';border-radius:2px;"></span><b>R$ '+op1Num(r[1],1)+' mi</b></div></td>'
           + '<td style="'+td+'text-align:right;font-weight:700;color:'+cor(r[2])+';">'+sg(r[2])+'</td><td style="'+td+'text-align:center;">'+op1Num(r[3],1)+'% → '+op1Num(r[4],1)+'%</td>'
           + '<td style="'+td+'"><div style="display:flex;align-items:center;gap:6px;"><div style="width:120px;position:relative;height:12px;"><span style="position:absolute;left:60px;top:0;bottom:0;border-left:1px solid #94A3B8;"></span><span style="position:absolute;top:1px;height:10px;'+(dp>=0?'left:60px;':'right:60px;')+'width:'+Math.round(Math.abs(dp)/mp*58)+'px;background:'+(dp>=0?'#16A34A':'#DC2626')+';"></span></div><b style="color:'+cor(dp)+';">'+sg(dp)+'</b></div></td></tr>'; }).join('')
     + '</tbody></table></div></div>';
  var S = M.marcas.filter(function(r){ return !/^OUTRAS/.test(r[0]); }).map(function(r){ return [r[0], r[4]-r[3]]; }).sort(function(a,b){ return b[1]-a[1]; });
  var neg = S.filter(function(x){ return x[1]<0; }).slice(-2).reverse();
  h += op1Box('<b>'+S[0][0]+'</b> é quem mais ganha share em '+M.mk+' ('+sg(S[0][1])+' p.p., '+P.c+')'+(neg.length?'; '+neg.map(function(x){ return '<b>'+x[0]+'</b>'; }).join(' e ')+' '+(neg.length>1?'são quem mais perdem':'é quem mais perde')+'.':'.')
     + '<div style="font-size:10px;color:#94A3B8;margin-top:4px;">Fonte: Nielsen (base do dashboard), % valor. O Nielsen não mede rede: é o mercado da região do cliente. Moskitoff, Above e OAZ não vêm separadas nesta base (estão em Outras).</div>');
  return h;
}"""
h = h[:a] + NOVO + h[b:]
open(H, "w", encoding="utf-8", newline="").write(h); print("ok")
