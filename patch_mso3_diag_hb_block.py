"""
patch_mso3_diag_hb_block.py
No Diagnostico do MSO3 (FYTD JUL-MAR):
  - Remove bloco "SCJ Portfolio vs Mercado" (todas as 5 marcas)
  - Substitui por bloco "OFF! + EXPOSIS (HB)" com FYTD25/26, delta%,
    share HB no mercado e comparativo HB vs mercado
2 substituicoes:
  A) Injeta variaveis HB apos vsLabel (antes do lines3 loop)
  B) Substitui o bloco HTML concatenado pelo HB
"""
import shutil
from datetime import datetime

SRC      = r"C:\Users\valqu\OneDrive\Documentos\Claude\Projects\projeto Dashboard_farma_sul\Dashboard_farma_sul\Dashboard_Farma_Sul_20260512_2220.html"
VERS_DIR = r"C:\Users\valqu\OneDrive\Documentos\Claude\Projects\projeto Dashboard_farma_sul\Dashboard_farma_sul\versoes"
DL_DIR   = r"C:\Users\valqu\Downloads"

ts   = datetime.now().strftime('%Y%m%d_%H%M')
VERS = fr"{VERS_DIR}\Dashboard_Farma_Sul_{ts}_MSO3DiagHbBlock.html"
DL   = fr"{DL_DIR}\Dashboard_FarmaSul_Giovano_{ts}.html"

with open(SRC, 'r', encoding='utf-8') as f:
    html = f.read()

ok = []

# ── A) Injetar variaveis HB antes do lines3 ──────────────────────────────────
OLD_VARS = (
    "    var vsLabel=vsMarket>0.5?'SCJ superou o mercado':vsMarket<-0.5?'SCJ ficou abaixo do mercado':'SCJ acompanhou o mercado';\n"
    "    var unitLbl=isVal?'R$ MM':'Mil Un';\n"
    "    /* Linha por marca com share no mercado */"
)
NEW_VARS = (
    "    var vsLabel=vsMarket>0.5?'SCJ superou o mercado':vsMarket<-0.5?'SCJ ficou abaixo do mercado':'SCJ acompanhou o mercado';\n"
    "    var unitLbl=isVal?'R$ MM':'Mil Un';\n"
    "    /* HB OFF!+EXPOSIS — variaveis para bloco diagnostico */\n"
    "    var hb25d=Math.round(((d25['OFF!']||0)+(d25['EXPOSIS']||0))*100)/100;\n"
    "    var hb26d=Math.round(((d26['OFF!']||0)+(d26['EXPOSIS']||0))*100)/100;\n"
    "    var hbDeltaD=hb25d>0?Math.round((hb26d-hb25d)/hb25d*1000)/10:0;\n"
    "    var hbCorD=hbDeltaD>=0?'#34d399':'#ef4444';\n"
    "    var shrHb26=mt26d>0?Math.round(hb26d/mt26d*1000)/10:0;\n"
    "    var shrHb25=mt25d>0?Math.round(hb25d/mt25d*1000)/10:0;\n"
    "    var shrHbDelta=Math.round((shrHb26-shrHb25)*10)/10;\n"
    "    var shrHbCor=shrHbDelta>=0?'#34d399':'#ef4444';\n"
    "    var vsHb=Math.round((hbDeltaD-mtDelta)*10)/10;\n"
    "    var vsHbCor=vsHb>=0?'#34d399':'#ef4444';\n"
    "    var vsHbLabel=vsHb>0.5?'HB superou o mercado':vsHb<-0.5?'HB ficou abaixo do mercado':'HB acompanhou o mercado';\n"
    "    /* Linha por marca com share no mercado */"
)
if OLD_VARS in html:
    html = html.replace(OLD_VARS, NEW_VARS, 1)
    ok.append('Vars HB injetadas antes de lines3')
else:
    ok.append('MISS vars HB — anchor vsLabel nao encontrado')

# ── B) Substituir bloco HTML: SCJ Portfolio vs Mercado → OFF!+EXPOSIS (HB) ───
OLD_BLOCK = (
    "+'<div style=\"margin-bottom:10px;padding-bottom:9px;border-bottom:0.5px solid rgba(255,255,255,0.06);\">'\n"
    "        +'<div style=\"font-size:9px;font-weight:700;letter-spacing:.1em;color:#475569;text-transform:uppercase;margin-bottom:5px;\">&#127381; SCJ Portfolio vs Mercado</div>'\n"
    "        +'<div style=\"display:flex;align-items:center;gap:8px;flex-wrap:wrap;margin-bottom:6px;\">'\n"
    "          +'<span style=\"font-size:11px;color:#94a3b8;\">SCJ FYTD/25: <strong style=\"color:#fbbf24;\">'+fmtV3(scj25d)+'</strong></span>'\n"
    "          +'<span style=\"color:#334155;\">&#8594;</span>'\n"
    "          +'<span style=\"font-size:11px;color:#94a3b8;\">FYTD/26: <strong style=\"color:#fbbf24;\">'+fmtV3(scj26d)+'</strong></span>'\n"
    "          +'<span style=\"background:'+scjCor+'1a;color:'+scjCor+';font-weight:700;font-size:11px;padding:2px 8px;border-radius:4px;border:0.5px solid '+scjCor+'44;\">'\n"
    "            +(scjDelta>=0?'&#9650; +':'&#9660; ')+Math.abs(scjDelta).toFixed(1)+'%'\n"
    "          +'</span>'\n"
    "        +'</div>'\n"
    "        +'<div style=\"display:flex;gap:14px;align-items:center;flex-wrap:wrap;margin-bottom:5px;\">'\n"
    "          +'<span style=\"font-size:11px;color:#64748b;\">Share FYTD/25: <strong style=\"color:#cbd5e1;\">'+shr25d.toFixed(1)+'%</strong></span>'\n"
    "          +'<span style=\"color:#1e293b;\">|</span>'\n"
    "          +'<span style=\"font-size:11px;color:#64748b;\">Share FYTD/26: <strong style=\"color:#fbbf24;\">'+shr26d.toFixed(1)+'%</strong></span>'\n"
    "          +'<span style=\"color:'+shrCor+';font-weight:700;font-size:11px;\">'\n"
    "            +(shrDelta>=0?'&#9650; +':'&#9660; ')+Math.abs(shrDelta).toFixed(1)+'pp'\n"
    "          +'</span>'\n"
    "        +'</div>'\n"
    "        +'<div style=\"font-size:10px;color:'+vsCor+';padding:4px 8px;background:'+vsCor+'0d;border-radius:5px;display:inline-block;\">'\n"
    "          +'&#128269; '+vsLabel+' &mdash; SCJ '+(scjDelta>=0?'+':'')+scjDelta.toFixed(1)+'% vs Mercado '+(mtDelta>=0?'+':'')+mtDelta.toFixed(1)+'%'\n"
    "          +(vsMarket!==0?' &nbsp;(&#916; '+(vsMarket>=0?'+':'')+vsMarket.toFixed(1)+'pp)':'')\n"
    "        +'</div>'\n"
    "      +'</div>'\n"
    "      "
)
NEW_BLOCK = (
    "+'<div style=\"margin-bottom:10px;padding-bottom:9px;border-bottom:0.5px solid rgba(255,255,255,0.06);\">'\n"
    "        +'<div style=\"font-size:9px;font-weight:700;letter-spacing:.1em;color:#475569;text-transform:uppercase;margin-bottom:5px;\">&#128293; OFF! + EXPOSIS (HB) &middot; FYTD JUL&ndash;MAR &middot; '+unitLbl+'</div>'\n"
    "        +'<div style=\"display:flex;align-items:center;gap:8px;flex-wrap:wrap;margin-bottom:6px;\">'\n"
    "          +'<span style=\"font-size:11px;color:#94a3b8;\">FYTD/25: <strong style=\"color:#3b82f6;\">'+fmtV3(hb25d)+'</strong></span>'\n"
    "          +'<span style=\"color:#334155;\">&#8594;</span>'\n"
    "          +'<span style=\"font-size:11px;color:#94a3b8;\">FYTD/26: <strong style=\"color:#3b82f6;\">'+fmtV3(hb26d)+'</strong></span>'\n"
    "          +'<span style=\"background:'+hbCorD+'1a;color:'+hbCorD+';font-weight:700;font-size:11px;padding:2px 8px;border-radius:4px;border:0.5px solid '+hbCorD+'44;\">'\n"
    "            +(hbDeltaD>=0?'&#9650; +':'&#9660; ')+Math.abs(hbDeltaD).toFixed(1)+'%'\n"
    "          +'</span>'\n"
    "        +'</div>'\n"
    "        +'<div style=\"display:flex;gap:14px;align-items:center;flex-wrap:wrap;margin-bottom:5px;\">'\n"
    "          +'<span style=\"font-size:11px;color:#64748b;\">Share FYTD/25: <strong style=\"color:#cbd5e1;\">'+shrHb25.toFixed(1)+'%</strong></span>'\n"
    "          +'<span style=\"color:#1e293b;\">|</span>'\n"
    "          +'<span style=\"font-size:11px;color:#64748b;\">Share FYTD/26: <strong style=\"color:#3b82f6;\">'+shrHb26.toFixed(1)+'%</strong></span>'\n"
    "          +'<span style=\"color:'+shrHbCor+';font-weight:700;font-size:11px;\">'\n"
    "            +(shrHbDelta>=0?'&#9650; +':'&#9660; ')+Math.abs(shrHbDelta).toFixed(1)+'pp'\n"
    "          +'</span>'\n"
    "        +'</div>'\n"
    "        +'<div style=\"font-size:10px;color:'+vsHbCor+';padding:4px 8px;background:'+vsHbCor+'0d;border-radius:5px;display:inline-block;\">'\n"
    "          +'&#128269; '+vsHbLabel+' &mdash; HB '+(hbDeltaD>=0?'+':'')+hbDeltaD.toFixed(1)+'% vs Mercado '+(mtDelta>=0?'+':'')+mtDelta.toFixed(1)+'%'\n"
    "          +(vsHb!==0?' &nbsp;(&#916; '+(vsHb>=0?'+':'')+vsHb.toFixed(1)+'pp)':'')\n"
    "        +'</div>'\n"
    "      +'</div>'\n"
    "      "
)
if OLD_BLOCK in html:
    html = html.replace(OLD_BLOCK, NEW_BLOCK, 1)
    ok.append('Bloco HTML: OFF!+EXPOSIS (HB) substituiu SCJ Portfolio vs Mercado')
else:
    ok.append('MISS bloco HTML SCJ Portfolio')

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
