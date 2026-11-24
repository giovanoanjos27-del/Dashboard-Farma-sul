"""One Page › Sell-out por marca: valor escrito na ponta de cada barra (YTD, Diferença YTD e Diferença do mês) — 24/11/2026, todos os clientes.
Uso: python op1_valores_barras.py <base.html>"""
import sys
H = sys.argv[1]; h = open(H, encoding="utf-8", newline="").read()
a = """      op1Chart(id,{type:'bar', data:{labels:L, datasets:[{data:data, backgroundColor:colors, borderRadius:3, barPercentage:0.8, categoryPercentage:0.85}]},
        options:{indexAxis:'y', responsive:true, maintainAspectRatio:false, animation:false,"""
b = """      var fmtV = function(v){ return signed ? op1K(mk,v) : (mk==='val'?'R$ '+op1Num(v,1)+'k':op1Num(v)+' un'); };
      var valPl = {id:'op1val', afterDatasetsDraw:function(ch){ var c=ch.ctx, m=ch.getDatasetMeta(0); c.save(); c.font='700 9.5px system-ui,sans-serif'; c.textBaseline='middle';
        m.data.forEach(function(bar,i){ var v=data[i]; if(v==null) return; var neg=v<0; c.fillStyle=neg?'#DC2626':(signed?'#059669':'#1E293B'); c.textAlign=neg?'right':'left'; c.fillText(fmtV(v), bar.x+(neg?-4:4), bar.y); }); c.restore(); }};
      op1Chart(id,{type:'bar', data:{labels:L, datasets:[{data:data, backgroundColor:colors, borderRadius:3, barPercentage:0.8, categoryPercentage:0.85}]},
        plugins:[valPl],
        options:{indexAxis:'y', responsive:true, maintainAspectRatio:false, animation:false, layout:{padding:{right:6, left:4}},"""
assert "id:'op1val'" not in h, "já aplicado"
if h.count(a) != 1: a, b = a.replace("\n", "\r\n"), b.replace("\n", "\r\n")
assert h.count(a) == 1, h.count(a); h = h.replace(a, b)
a2 = "          scales:{x:{grid:{color:OP1_C.grid}, ticks:{font:{size:9}, color:'#64748B'}}, y:{grid:{display:false}, ticks:{autoSkip:false,"
assert h.count(a2) == 1, h.count(a2)
h = h.replace(a2, "          scales:{x:{grace:'18%', grid:{color:OP1_C.grid}, ticks:{font:{size:9}, color:'#64748B'}}, y:{grid:{display:false}, ticks:{autoSkip:false,")
open(H, "w", encoding="utf-8", newline="").write(h); print("ok")
