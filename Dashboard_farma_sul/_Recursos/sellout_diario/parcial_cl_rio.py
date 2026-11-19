"""Clamed e Riomed: barras 'por Ano' calculadas dos arrays mensais (antes eram números fixos defasados) com rótulo
'2026 (Jan–Nov parcial até dd/mm)', e barras mensais com o mês de SO_PARCIAL rotulado 'Nov/26 parcial'. Uso: python parcial_cl_rio.py <html>"""
import sys
p = sys.argv[1]; h = open(p, encoding="utf-8", newline="").read()
def ano(fn, mode, canvas, pre):
    return ("function %s(){\r\n  var isVol = %s==='vol';\r\n"
            "  var s = function(a){ return (a||[]).reduce(function(t,v){ return t+(v||0); },0); };\r\n"
            "  var a26 = isVol?%sVOL_2026:%sREC_2026, l=-1; a26.forEach(function(v,i){ if(v) l=i; });\r\n"
            "  var M=['Jan','Fev','Mar','Abr','Mai','Jun','Jul','Ago','Set','Out','Nov','Dez'];\r\n"
            "  var parc = (typeof SO_PARCIAL!=='undefined' && SO_PARCIAL && l===SO_PARCIAL.mes);\r\n"
            "  var anos = ['2024','2025','2026 (Jan–'+M[l]+(parc?' parcial até '+SO_PARCIAL.ate:'')+')'];\r\n"
            "  var vals = [s(isVol?%sVOL_2024:%sREC_2024), s(isVol?%sVOL_2025:%sREC_2025), s(a26)];\r\n"
            "  renderAnoChart('%s', anos, vals, isVol);\r\n}") % (fn, mode, pre, pre, pre, pre, pre, pre, canvas)
for fn, mode, canvas, pre, old in (
    ("renderCLAnoBars", "clBarMode", "cl-ano-chart", "CL_", "  var vals = isVol ? [90534,95951,59987] : [3137722,3058207.54,2149873.0100000002];\r\n  renderAnoChart('cl-ano-chart', anos, vals, isVol);\r\n}"),
    ("renderRioAnoBars", "rioBarMode", "rio-ano-chart", "RIOMED_", "  var vals = isVol ? [92290,63489,26841] : [3111298,1742145,549396.3400000001];\r\n  renderAnoChart('rio-ano-chart', anos, vals, isVol);\r\n}")):
    i = h.index("function " + fn + "(){"); j = h.index(old, i) + len(old)
    assert j - i < 400, fn; h = h[:i] + ano(fn, mode, canvas, pre) + h[j:]
lab_old = "        items.push({nome:mLabels[i]+'/'+a.label.slice(2), val:v, color:a.color});"
lab_new = "        items.push({nome:mLabels[i]+'/'+a.label.slice(2)+((a.label==='2026' && typeof SO_PARCIAL!=='undefined' && SO_PARCIAL && i===SO_PARCIAL.mes)?' parcial até '+SO_PARCIAL.ate:''), val:v, color:a.color});"
for fn in ("function renderCLMesBars", "function renderRIOMesBars"):
    i = h.index(fn); k = h.index(lab_old, i); assert k - i < 1200, fn
    h = h[:k] + lab_new + h[k + len(lab_old):]
open(p, "w", encoding="utf-8", newline="").write(h); print("ok")
