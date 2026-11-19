"""
patch_mso3_diagnostico.py
Enriquece o Diagnostico do MSO3 com 3 blocos:
  1. MERCADO TOTAL — FYTD/25 vs FYTD/26 + delta do mercado
  2. SCJ vs MERCADO — share SCJ, delta comparativo, se perdeu/ganhou share
  3. POR MARCA — cada marca com FYTD/26, FYTD/25, delta e share no mercado
"""

import shutil
from datetime import datetime

SRC      = r"C:\Users\valqu\OneDrive\Documentos\Claude\Projects\projeto Dashboard_farma_sul\Dashboard_farma_sul\Dashboard_Farma_Sul_20260512_2220.html"
VERS_DIR = r"C:\Users\valqu\OneDrive\Documentos\Claude\Projects\projeto Dashboard_farma_sul\Dashboard_farma_sul\versoes"
DL_DIR   = r"C:\Users\valqu\Downloads"

ts   = datetime.now().strftime('%Y%m%d_%H%M')
VERS = fr"{VERS_DIR}\Dashboard_Farma_Sul_{ts}_MSO3Diag.html"
DL   = fr"{DL_DIR}\Dashboard_FarmaSul_Giovano_{ts}.html"

with open(SRC, 'r', encoding='utf-8') as f:
    html = f.read()

OLD = """  /* DIAGNOSTICO */
  var insightEl=document.getElementById('mso3-insight');
  if(insightEl&&nbv){
    var lines3=brands.map(function(b){
      var bd=nbv[b]; if(!bd) return null;
      var cor=colors[b]||'#e2e8f0';
      var v25=isVal?bd.fytd25_val:bd.fytd25_un, v26=isVal?bd.fytd26_val:bd.fytd26_un;
      var p=v25>0?Math.round((v26-v25)/v25*1000)/10:0;
      var cc=p>=0?'#34d399':'#ef4444', trend=p>2?'&#8599; ':(p<-2?'&#8600; ':'&#8594; ');
      return '<span style="color:'+cc+';font-weight:700;font-size:10px;">'+trend+'</span>'
        +'<strong style="color:'+cor+';">'+b+'</strong>'
        +' FYTD/26: <strong style="color:'+cor+';">'+fmtV3(v26)+'</strong>'
        +' &middot; FYTD/25: '+fmtV3(v25)
        +' <span style="color:'+cc+';font-weight:700;">'+(p>=0?'&#9650; +':'&#9660; ')+Math.abs(p).toFixed(1)+'%</span>';
    }).filter(Boolean);
    insightEl.innerHTML='<div style="background:#161B22;border-radius:10px;border-left:3px solid rgba(251,191,36,0.6);padding:14px 16px;">'
      +'<div style="font-size:9px;font-weight:700;letter-spacing:.14em;color:#fbbf24;text-transform:uppercase;margin-bottom:9px;">&#128202; DIAGNOSTICO &middot; '+mkt+' &middot; '+(isVal?'R$ MM':'Unidades')+' FYTD JUL&ndash;MAR/26</div>'
      +'<div style="font-size:11px;color:#D1D5DB;line-height:1.9;">'+lines3.join('<br>')+'</div></div>';
  }
"""

NEW = """  /* DIAGNOSTICO ENRIQUECIDO */
  var insightEl=document.getElementById('mso3-insight');
  if(insightEl&&nbv){
    /* Totais do mercado real (todas as marcas) */
    var mt25d=mt?(isVal?mt.fytd25_val:mt.fytd25_un):totV25;
    var mt26d=mt?(isVal?mt.fytd26_val:mt.fytd26_un):totV26;
    mt25d=Math.round(mt25d*100)/100; mt26d=Math.round(mt26d*100)/100;
    var scj25d=Math.round(totV25*100)/100, scj26d=Math.round(totV26*100)/100;
    /* Deltas */
    var mtDelta=mt25d>0?Math.round((mt26d-mt25d)/mt25d*1000)/10:0;
    var scjDelta=scj25d>0?Math.round((scj26d-scj25d)/scj25d*1000)/10:0;
    var mtCor=mtDelta>=0?'#34d399':'#ef4444';
    var scjCor=scjDelta>=0?'#34d399':'#ef4444';
    /* Share SCJ no mercado total */
    var shr26d=mt26d>0?Math.round(scj26d/mt26d*1000)/10:0;
    var shr25d=mt25d>0?Math.round(scj25d/mt25d*1000)/10:0;
    var shrDelta=Math.round((shr26d-shr25d)*10)/10;
    var shrCor=shrDelta>=0?'#34d399':'#ef4444';
    /* Performance SCJ vs Mercado */
    var vsMarket=Math.round((scjDelta-mtDelta)*10)/10;
    var vsCor=vsMarket>=0?'#34d399':'#ef4444';
    var vsLabel=vsMarket>0.5?'SCJ superou o mercado':vsMarket<-0.5?'SCJ ficou abaixo do mercado':'SCJ acompanhou o mercado';
    var unitLbl=isVal?'R$ MM':'Mil Un';
    /* Linha por marca com share no mercado */
    var lines3=brands.map(function(b){
      var bd=nbv[b]; if(!bd) return null;
      var cor=colors[b]||'#e2e8f0';
      var v25=isVal?bd.fytd25_val:bd.fytd25_un, v26=isVal?bd.fytd26_val:bd.fytd26_un;
      var pct=v25>0?Math.round((v26-v25)/v25*1000)/10:0;
      var cc=pct>=0?'#34d399':'#ef4444';
      var trend=pct>2?'&#8599;':(pct<-2?'&#8600;':'&#8594;');
      var shrB=mt26d>0?Math.round(v26/mt26d*1000)/10:0;
      return '<div style="display:flex;align-items:center;gap:5px;padding:3px 0;border-bottom:0.5px solid rgba(255,255,255,0.04);">'
        +'<span style="width:5px;height:5px;border-radius:50%;background:'+cor+';flex-shrink:0;"></span>'
        +'<span style="color:'+cor+';font-weight:700;min-width:95px;font-size:11px;">'+b+'</span>'
        +'<span style="color:#e2e8f0;font-size:11px;">FYTD/26: <strong>'+fmtV3(v26)+'</strong></span>'
        +'<span style="color:#475569;margin:0 3px;">·</span>'
        +'<span style="color:#64748b;font-size:11px;">FYTD/25: '+fmtV3(v25)+'</span>'
        +'<span style="color:'+cc+';font-weight:700;font-size:11px;margin-left:5px;">'
          +'<span style="font-size:10px;">'+trend+'</span> '+(pct>=0?'+':'')+pct.toFixed(1)+'%'
        +'</span>'
        +'<span style="color:#334155;font-size:10px;margin-left:auto;background:rgba(255,255,255,0.04);padding:1px 5px;border-radius:3px;">shr '+shrB.toFixed(1)+'%</span>'
        +'</div>';
    }).filter(Boolean);
    insightEl.innerHTML=
      '<div style="background:#161B22;border-radius:10px;border-left:3px solid rgba(251,191,36,0.6);padding:14px 16px;">'
      /* Titulo */
      +'<div style="font-size:9px;font-weight:700;letter-spacing:.14em;color:#fbbf24;text-transform:uppercase;margin-bottom:12px;">&#128202; DIAGNOSTICO &middot; '+mkt+' &middot; '+unitLbl+' FYTD JUL&ndash;MAR/26</div>'
      /* Bloco 1: Mercado Total */
      +'<div style="margin-bottom:10px;padding-bottom:9px;border-bottom:0.5px solid rgba(255,255,255,0.06);">'
        +'<div style="font-size:9px;font-weight:700;letter-spacing:.1em;color:#475569;text-transform:uppercase;margin-bottom:5px;">&#127758; Mercado Total (todas as marcas)</div>'
        +'<div style="display:flex;align-items:center;gap:8px;flex-wrap:wrap;">'
          +'<span style="font-size:11px;color:#94a3b8;">FYTD/25: <strong style="color:#e2e8f0;">'+fmtV3(mt25d)+'</strong></span>'
          +'<span style="color:#334155;">&#8594;</span>'
          +'<span style="font-size:11px;color:#94a3b8;">FYTD/26: <strong style="color:#e2e8f0;">'+fmtV3(mt26d)+'</strong></span>'
          +'<span style="background:'+mtCor+'1a;color:'+mtCor+';font-weight:700;font-size:11px;padding:2px 8px;border-radius:4px;border:0.5px solid '+mtCor+'44;">'
            +(mtDelta>=0?'&#9650; +':'&#9660; ')+Math.abs(mtDelta).toFixed(1)+'%'
          +'</span>'
        +'</div>'
      +'</div>'
      /* Bloco 2: SCJ vs Mercado */
      +'<div style="margin-bottom:10px;padding-bottom:9px;border-bottom:0.5px solid rgba(255,255,255,0.06);">'
        +'<div style="font-size:9px;font-weight:700;letter-spacing:.1em;color:#475569;text-transform:uppercase;margin-bottom:5px;">&#127381; SCJ Portfolio vs Mercado</div>'
        +'<div style="display:flex;align-items:center;gap:8px;flex-wrap:wrap;margin-bottom:6px;">'
          +'<span style="font-size:11px;color:#94a3b8;">SCJ FYTD/25: <strong style="color:#fbbf24;">'+fmtV3(scj25d)+'</strong></span>'
          +'<span style="color:#334155;">&#8594;</span>'
          +'<span style="font-size:11px;color:#94a3b8;">FYTD/26: <strong style="color:#fbbf24;">'+fmtV3(scj26d)+'</strong></span>'
          +'<span style="background:'+scjCor+'1a;color:'+scjCor+';font-weight:700;font-size:11px;padding:2px 8px;border-radius:4px;border:0.5px solid '+scjCor+'44;">'
            +(scjDelta>=0?'&#9650; +':'&#9660; ')+Math.abs(scjDelta).toFixed(1)+'%'
          +'</span>'
        +'</div>'
        +'<div style="display:flex;gap:14px;align-items:center;flex-wrap:wrap;margin-bottom:5px;">'
          +'<span style="font-size:11px;color:#64748b;">Share FYTD/25: <strong style="color:#cbd5e1;">'+shr25d.toFixed(1)+'%</strong></span>'
          +'<span style="color:#1e293b;">|</span>'
          +'<span style="font-size:11px;color:#64748b;">Share FYTD/26: <strong style="color:#fbbf24;">'+shr26d.toFixed(1)+'%</strong></span>'
          +'<span style="color:'+shrCor+';font-weight:700;font-size:11px;">'
            +(shrDelta>=0?'&#9650; +':'&#9660; ')+Math.abs(shrDelta).toFixed(1)+'pp'
          +'</span>'
        +'</div>'
        +'<div style="font-size:10px;color:'+vsCor+';padding:4px 8px;background:'+vsCor+'0d;border-radius:5px;display:inline-block;">'
          +'&#128269; '+vsLabel+' &mdash; SCJ '+(scjDelta>=0?'+':'')+scjDelta.toFixed(1)+'% vs Mercado '+(mtDelta>=0?'+':'')+mtDelta.toFixed(1)+'%'
          +(vsMarket!==0?' &nbsp;(&#916; '+(vsMarket>=0?'+':'')+vsMarket.toFixed(1)+'pp)':'')
        +'</div>'
      +'</div>'
      /* Bloco 3: Por Marca */
      +'<div>'
        +'<div style="font-size:9px;font-weight:700;letter-spacing:.1em;color:#475569;text-transform:uppercase;margin-bottom:6px;">&#128200; Por Marca &middot; participacao no mercado total</div>'
        +'<div style="font-size:11px;color:#D1D5DB;">'+lines3.join('')+'</div>'
      +'</div>'
      +'</div>';
  }
"""

if OLD in html:
    html = html.replace(OLD, NEW, 1)
    print("OK  MSO3 Diagnostico enriquecido")
else:
    print("MISS  bloco nao encontrado — verificar")

with open(SRC, 'w', encoding='utf-8') as f:
    f.write(html)
shutil.copy2(SRC, VERS)
shutil.copy2(SRC, DL)

print()
print("=" * 55)
print(f"  Versao: {VERS.split(chr(92))[-1]}")
print(f"  DL:     {DL.split(chr(92))[-1]}")
print("=" * 55)
