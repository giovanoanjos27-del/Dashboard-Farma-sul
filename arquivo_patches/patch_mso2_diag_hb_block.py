"""
patch_mso2_diag_hb_block.py
No Diagnostico do MSO2 (JAN-MAR):
  - Remove bloco "SCJ Portfolio vs Mercado"
  - Substitui por bloco "OFF! + EXPOSIS (HB) · JAN-MAR"
"""
import shutil
from datetime import datetime

SRC      = r"C:\Users\valqu\OneDrive\Documentos\Claude\Projects\projeto Dashboard_farma_sul\Dashboard_farma_sul\Dashboard_Farma_Sul_20260512_2220.html"
VERS_DIR = r"C:\Users\valqu\OneDrive\Documentos\Claude\Projects\projeto Dashboard_farma_sul\Dashboard_farma_sul\versoes"
DL_DIR   = r"C:\Users\valqu\Downloads"

ts   = datetime.now().strftime('%Y%m%d_%H%M')
VERS = fr"{VERS_DIR}\Dashboard_Farma_Sul_{ts}_MSO2DiagHbBlock.html"
DL   = fr"{DL_DIR}\Dashboard_FarmaSul_Giovano_{ts}.html"

with open(SRC, 'r', encoding='utf-8') as f:
    html = f.read()

ok = []

# ── A) Injetar variaveis HB apos vsLabelI (antes de lines2) ──────────────────
OLD_VARS = (
    "  var vsLabelI=vsMarketI>0.5?'SCJ superou o mercado':vsMarketI<-0.5?'SCJ ficou abaixo do mercado':'SCJ acompanhou o mercado';\n"
    "  /* Por marca */\n"
    "  "
)
NEW_VARS = (
    "  var vsLabelI=vsMarketI>0.5?'SCJ superou o mercado':vsMarketI<-0.5?'SCJ ficou abaixo do mercado':'SCJ acompanhou o mercado';\n"
    "  /* HB OFF!+EXPOSIS — variaveis para bloco diagnostico MSO2 */\n"
    "  var hbI25=0, hbI26=0;\n"
    "  MSO_BRANDS.forEach(function(b){\n"
    "    if(b!=='OFF!'&&b!=='EXPOSIS') return;\n"
    "    var bd=nbvI[b]; if(!bd) return;\n"
    "    var j26=isValI?(bd.jan_val||0):(bd.jan_un||0);\n"
    "    var f26=isValI?(bd.fev_val||0):(bd.fev_un||0);\n"
    "    var m26=isValI?(bd.mar_val||0):(bd.mar_un||0);\n"
    "    hbI26 += j26+f26+m26;\n"
    "    var hasEx=isValI?(bd.jan25_val!==undefined):(bd.jan25_un!==undefined);\n"
    "    if(hasEx){\n"
    "      hbI25 += (isValI?(bd.jan25_val||0):(bd.jan25_un||0))\n"
    "              +(isValI?(bd.fev25_val||0):(bd.fev25_un||0))\n"
    "              +(isValI?(bd.mar25_val||0):(bd.mar25_un||0));\n"
    "    } else {\n"
    "      var fyt25b=isValI?bd.fytd25_val:bd.fytd25_un, fyt26b=isValI?bd.fytd26_val:bd.fytd26_un;\n"
    "      var ratio=fyt26b>0?(j26+f26+m26)/fyt26b:1/3;\n"
    "      hbI25 += fyt25b*ratio;\n"
    "    }\n"
    "  });\n"
    "  hbI25=Math.round(hbI25*100)/100; hbI26=Math.round(hbI26*100)/100;\n"
    "  var hbIDelta=hbI25>0?Math.round((hbI26-hbI25)/hbI25*1000)/10:0;\n"
    "  var hbICorD=hbIDelta>=0?'#34d399':'#ef4444';\n"
    "  var shrHbI26=mtI26>0?Math.round(hbI26/mtI26*1000)/10:0;\n"
    "  var shrHbI25=mtI25>0?Math.round(hbI25/mtI25*1000)/10:0;\n"
    "  var shrHbIDelta=Math.round((shrHbI26-shrHbI25)*10)/10;\n"
    "  var shrHbICor=shrHbIDelta>=0?'#34d399':'#ef4444';\n"
    "  var vsHbI=Math.round((hbIDelta-mtIDelta)*10)/10;\n"
    "  var vsHbICor=vsHbI>=0?'#34d399':'#ef4444';\n"
    "  var vsHbILabel=vsHbI>0.5?'HB superou o mercado':vsHbI<-0.5?'HB ficou abaixo do mercado':'HB acompanhou o mercado';\n"
    "  /* Por marca */\n"
    "  "
)
if OLD_VARS in html:
    html = html.replace(OLD_VARS, NEW_VARS, 1)
    ok.append('Vars HB injetadas antes de lines2 (MSO2 insight)')
else:
    ok.append('MISS vars HB MSO2 — anchor vsLabelI nao encontrado')

# ── B) Substituir bloco HTML: SCJ Portfolio → HB ─────────────────────────────
OLD_BLOCK = (
    "+'<div style=\"margin-bottom:10px;padding-bottom:9px;border-bottom:0.5px solid rgba(255,255,255,0.06);\">'\n"
    "      +'<div style=\"font-size:9px;font-weight:700;letter-spacing:.1em;color:#475569;text-transform:uppercase;margin-bottom:5px;\">🎁 SCJ Portfolio vs Mercado</div>'\n"
    "      +'<div style=\"display:flex;align-items:center;gap:8px;flex-wrap:wrap;margin-bottom:6px;\">'\n"
    "        +'<span style=\"font-size:11px;color:#94a3b8;\">SCJ Jan-Mar/25: <strong style=\"color:#fbbf24;\">'+fmtNI(scjI25)+'</strong></span>'\n"
    "        +'<span style=\"color:#334155;\">→</span>'\n"
    "        +'<span style=\"font-size:11px;color:#94a3b8;\">Jan-Mar/26: <strong style=\"color:#fbbf24;\">'+fmtNI(scjI26)+'</strong></span>'\n"
    "        +'<span style=\"background:'+scjICor+'1a;color:'+scjICor+';font-weight:700;font-size:11px;padding:2px 8px;border-radius:4px;border:0.5px solid '+scjICor+'44;\">'\n"
    "          +(scjIDelta>=0?'▲ +':'▼ ')+Math.abs(scjIDelta).toFixed(1)+'%'\n"
    "        +'</span>'\n"
    "      +'</div>'\n"
    "      +'<div style=\"display:flex;gap:14px;align-items:center;flex-wrap:wrap;margin-bottom:5px;\">'\n"
    "        +'<span style=\"font-size:11px;color:#64748b;\">Share Jan-Mar/25: <strong style=\"color:#cbd5e1;\">'+shrI25.toFixed(1)+'%</strong></span>'\n"
    "        +'<span style=\"color:#1e293b;\">|</span>'\n"
    "        +'<span style=\"font-size:11px;color:#64748b;\">Share Jan-Mar/26: <strong style=\"color:#fbbf24;\">'+shrI26.toFixed(1)+'%</strong></span>'\n"
    "        +'<span style=\"color:'+shrICor+';font-weight:700;font-size:11px;\">'\n"
    "          +(shrIDelta>=0?'▲ +':'▼ ')+Math.abs(shrIDelta).toFixed(1)+'pp'\n"
    "        +'</span>'\n"
    "      +'</div>'\n"
    "      +'<div style=\"font-size:10px;color:'+vsCorkI+';padding:4px 8px;background:'+vsCorkI+'0d;border-radius:5px;display:inline-block;\">'\n"
    "        +'🔍 '+vsLabelI+' — SCJ '+(scjIDelta>=0?'+':'')+scjIDelta.toFixed(1)+'% vs Mercado '+(mtIDelta>=0?'+':'')+mtIDelta.toFixed(1)+'%'\n"
    "        +(vsMarketI!==0?' &nbsp;(Δ '+(vsMarketI>=0?'+':'')+vsMarketI.toFixed(1)+'pp)':'')\n"
    "      +'</div>'\n"
    "    +'</div>'\n"
    "    "
)
NEW_BLOCK = (
    "+'<div style=\"margin-bottom:10px;padding-bottom:9px;border-bottom:0.5px solid rgba(255,255,255,0.06);\">'\n"
    "      +'<div style=\"font-size:9px;font-weight:700;letter-spacing:.1em;color:#475569;text-transform:uppercase;margin-bottom:5px;\">&#128293; OFF! + EXPOSIS (HB) &middot; JAN&ndash;MAR &middot; '+(isValI?'R$ MM':'Unidades')+'</div>'\n"
    "      +'<div style=\"display:flex;align-items:center;gap:8px;flex-wrap:wrap;margin-bottom:6px;\">'\n"
    "        +'<span style=\"font-size:11px;color:#94a3b8;\">Jan-Mar/25: <strong style=\"color:#3b82f6;\">'+fmtNI(hbI25)+'</strong></span>'\n"
    "        +'<span style=\"color:#334155;\">→</span>'\n"
    "        +'<span style=\"font-size:11px;color:#94a3b8;\">Jan-Mar/26: <strong style=\"color:#3b82f6;\">'+fmtNI(hbI26)+'</strong></span>'\n"
    "        +'<span style=\"background:'+hbICorD+'1a;color:'+hbICorD+';font-weight:700;font-size:11px;padding:2px 8px;border-radius:4px;border:0.5px solid '+hbICorD+'44;\">'\n"
    "          +(hbIDelta>=0?'▲ +':'▼ ')+Math.abs(hbIDelta).toFixed(1)+'%'\n"
    "        +'</span>'\n"
    "      +'</div>'\n"
    "      +'<div style=\"display:flex;gap:14px;align-items:center;flex-wrap:wrap;margin-bottom:5px;\">'\n"
    "        +'<span style=\"font-size:11px;color:#64748b;\">Share Jan-Mar/25: <strong style=\"color:#cbd5e1;\">'+shrHbI25.toFixed(1)+'%</strong></span>'\n"
    "        +'<span style=\"color:#1e293b;\">|</span>'\n"
    "        +'<span style=\"font-size:11px;color:#64748b;\">Share Jan-Mar/26: <strong style=\"color:#3b82f6;\">'+shrHbI26.toFixed(1)+'%</strong></span>'\n"
    "        +'<span style=\"color:'+shrHbICor+';font-weight:700;font-size:11px;\">'\n"
    "          +(shrHbIDelta>=0?'▲ +':'▼ ')+Math.abs(shrHbIDelta).toFixed(1)+'pp'\n"
    "        +'</span>'\n"
    "      +'</div>'\n"
    "      +'<div style=\"font-size:10px;color:'+vsHbICor+';padding:4px 8px;background:'+vsHbICor+'0d;border-radius:5px;display:inline-block;\">'\n"
    "        +'&#128269; '+vsHbILabel+' &mdash; HB '+(hbIDelta>=0?'+':'')+hbIDelta.toFixed(1)+'% vs Mercado '+(mtIDelta>=0?'+':'')+mtIDelta.toFixed(1)+'%'\n"
    "        +(vsHbI!==0?' &nbsp;(&#916; '+(vsHbI>=0?'+':'')+vsHbI.toFixed(1)+'pp)':'')\n"
    "      +'</div>'\n"
    "    +'</div>'\n"
    "    "
)
if OLD_BLOCK in html:
    html = html.replace(OLD_BLOCK, NEW_BLOCK, 1)
    ok.append('Bloco HTML MSO2: OFF!+EXPOSIS (HB) substituiu SCJ Portfolio vs Mercado')
else:
    ok.append('MISS bloco HTML SCJ Portfolio MSO2')

with open(SRC, 'w', encoding='utf-8') as f:
    f.write(html)
shutil.copy2(SRC, VERS)
shutil.copy2(SRC, DL)

print()
print('=' * 58)
for c in ok: print(f'  {"OK" if not c.startswith("MISS") else "!!"} {c}')
print(f'\n  Versao: {VERS.split(chr(92))[-1]}')
print(f'  DL:     {DL.split(chr(92))[-1]}')
print('=' * 58)
