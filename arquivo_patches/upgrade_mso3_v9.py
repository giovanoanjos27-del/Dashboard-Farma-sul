#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
upgrade_mso3_v9.py
Auditoria global + padronização visual MSO3
  PATCH 1: FYTD_MARKET_TOTAL  → valores corretos = aba MERCADO do Excel
           (soma TODOS os tipos de linha: shr=100 + brands + products)
           Farma Sul F26 = 339.815MM ✓  |  T.BR Farma F26 = 1362.380MM ✓
  PATCH 2: renderMSO3 v9 com:
           • Δ YoY: 14px bold (maior destaque visual)
           • FYTD25 sidebar: cor amarela neon (#fbbf24) — alta visibilidade
           • FY25 sub-label nas barras: #cbd5e1 (claro, legível)
           • All Others: bloqueado permanentemente
           • Modo Share: bloqueado permanentemente (só val/un)
"""

import json, shutil
from pathlib import Path
from datetime import datetime

BASE      = Path(r"C:\Users\valqu\OneDrive\Documentos\Claude\Projects\projeto Dashboard_farma_sul")
DASH_DIR  = BASE / "Dashboard_farma_sul"
DASH_FILE = DASH_DIR / "Dashboard_Farma_Sul_20260512_2220.html"
VERS_DIR  = DASH_DIR / "versoes"
JSON_FILE = BASE / "fytd_market_total_v3.json"

ts = datetime.now().strftime("%Y%m%d_%H%M")

# ── Backup ────────────────────────────────────────────────────────────────
pre = VERS_DIR / f"Dashboard_Farma_Sul_{ts}_PreMSO3v9.html"
shutil.copy2(str(DASH_FILE), str(pre))
print(f"Backup: {pre.name}")

html = DASH_FILE.read_text(encoding="utf-8")

# ════════════════════════════════════════════════════════════════════════════
# PATCH 1 — FYTD_MARKET_TOTAL com valores corretos (aba MERCADO)
# ════════════════════════════════════════════════════════════════════════════
with open(str(JSON_FILE), "r", encoding="utf-8") as f:
    data = json.load(f)

lines = ["const FYTD_MARKET_TOTAL = {"]
for mkt, d in data.items():
    lines.append(
        f"  '{mkt}': {{fytd25_val:{d['fytd25_val']},fytd26_val:{d['fytd26_val']},"
        f"fytd25_un:{d['fytd25_un']},fytd26_un:{d['fytd26_un']}}},"
    )
lines.append("};")
new_block = "\n".join(lines)

START_MKT = "const FYTD_MARKET_TOTAL = {"
END_MKT   = "};\n\nconst NIELSEN_FYTD_VAL"
idx_s = html.find(START_MKT)
idx_e = html.find(END_MKT)
if idx_s == -1 or idx_e == -1:
    raise RuntimeError("FYTD_MARKET_TOTAL nao encontrado")
old_mkt_block = html[idx_s : idx_e + 2]
html = html[:idx_s] + new_block + html[idx_e + 2:]
print(f"PATCH 1 OK — {len(data)} mercados atualizados (Farma Sul F26={data['Farma Sul']['fytd26_val']:.3f}MM)")

# ════════════════════════════════════════════════════════════════════════════
# PATCH 2 — renderMSO3 v9 completo (substitui âncora function→END)
# ════════════════════════════════════════════════════════════════════════════
START_MSO3 = "function renderMSO3(){"
END_MSO3   = "/* ═══════════ END MSO3 ═══════════ */"
idx_start  = html.find(START_MSO3)
idx_end    = html.find(END_MSO3)
if idx_start == -1 or idx_end == -1:
    raise RuntimeError("Bloco renderMSO3 nao encontrado")

NEW_RENDER = r'''function renderMSO3(){
  var sel=document.getElementById('mso3MarketSel');
  var mkt=sel?sel.value:'T.BR Farma';
  if(mso3Mode==='share') mso3Mode='val';
  var isVal=mso3Mode==='val', isUn=mso3Mode==='un';
  var brands=MSO_BRANDS, colors=MSO_COLORS;

  // ── Labels estáticos ──
  var titleEl=document.getElementById('mso3-card-title');
  if(titleEl) titleEl.textContent=isVal?'VENDA VALOR FYTD · JUL–MAR':'UNIDADES FYTD · JUL–MAR';
  var h2El=document.getElementById('mso3-card-h2');
  if(h2El) h2El.textContent='Visão consolidada por Marca em '+(isVal?'Valor (R$ MM)':'Unidades');
  var subEl=document.getElementById('mso3-card-sub');
  if(subEl) subEl.textContent='NielsenIQ · '+(isVal?'R$ e Unidades':'Unidades')+' · Jul/25–Mar/26 · '+mkt;
  ['mso3-table-title','mso3-table'].forEach(function(id){
    var el=document.getElementById(id); if(el) el.style.display='none';
  });
  var hdEl=document.getElementById('mso3-headline');
  if(hdEl) hdEl.style.display='none';

  // ── Helpers ──
  function fmtV9(v,compact){
    if(v===null||v===undefined||isNaN(v)) return '—';
    if(isVal){
      if(compact){
        if(v>=1000) return 'R$'+Math.round(v/1000)+'B';
        if(v>=100)  return 'R$'+Math.round(v)+'MM';
        if(v>=10)   return 'R$'+v.toFixed(1)+'MM';
        if(v>=1)    return 'R$'+v.toFixed(2)+'MM';
        return 'R$'+(v*1000).toFixed(0)+'K';
      }
      if(v>=1000) return 'R$ '+(v/1000).toFixed(2)+' B';
      if(v>=100) return 'R$ '+v.toFixed(1)+' MM';
      if(v>=1)   return 'R$ '+v.toFixed(2)+' MM';
      return 'R$ '+(v*1000).toFixed(0)+' K';
    }
    if(compact){
      if(v>=10000) return (v/1000).toFixed(1)+'M';
      if(v>=1000)  return Math.round(v/1000)+'M';
      return Math.round(v)+'K';
    }
    if(v>=1000) return (v/1000).toFixed(1)+' M un';
    return Math.round(v)+' K un';
  }
  function calcDelta9(v25,v26){
    var p=v25>0?Math.round((v26/v25-1)*10000)/100:0;
    return {str:(p>=0?'+':'')+p.toFixed(1)+'%',col:p>=0?'#4ade80':'#f87171',up:p>=0,raw:p};
  }

  // ── Dados ──
  var mt=(typeof FYTD_MARKET_TOTAL!=='undefined')?FYTD_MARKET_TOTAL[mkt]:null;
  var nfv=(typeof NIELSEN_FYTD_VAL!=='undefined')?NIELSEN_FYTD_VAL[mkt]:null;
  var dS=(typeof MKTSHARE_OVERVIEW!=='undefined')?MKTSHARE_OVERVIEW[mkt]:null;
  var d25={}, d26={};
  brands.forEach(function(b){
    var bd=nfv&&nfv[b];
    if(bd){d25[b]=isVal?bd.fytd25_val:bd.fytd25_un; d26[b]=isVal?bd.fytd26_val:bd.fytd26_un;}
  });
  var mtV25=mt?(isVal?mt.fytd25_val:mt.fytd25_un):0;
  var mtV26=mt?(isVal?mt.fytd26_val:mt.fytd26_un):0;
  var mtDt=calcDelta9(mtV25,mtV26);
  var scaleRef=mtV26>0?mtV26:1;

  // ── SCORECARDS 3 cards ──
  var scList=[
    {lbl:'MERCADO TOTAL',col:'#22c55e',v25:mtV25,v26:mtV26,sub:'Total canal HB'},
    {lbl:'OFF!',col:colors['OFF!']||'#f59e0b',v25:d25['OFF!']||0,v26:d26['OFF!']||0,
     sub:dS&&dS['OFF!']?(dS['OFF!'].fytd26||0).toFixed(1)+'% share':'Rep. líder SCJ'},
    {lbl:'EXPOSIS',col:colors['EXPOSIS']||'#818cf8',v25:d25['EXPOSIS']||0,v26:d26['EXPOSIS']||0,
     sub:dS&&dS['EXPOSIS']?(dS['EXPOSIS'].fytd26||0).toFixed(1)+'% share':'2ª marca SCJ'},
  ];
  var mktTotalEl=document.getElementById('mso3-market-total');
  if(mktTotalEl){
    mktTotalEl.style.cssText='display:flex;gap:1px;border-radius:8px;overflow:hidden;'
      +'margin-bottom:14px;border:none;background:none;padding:0;';
    mktTotalEl.innerHTML=scList.map(function(sc){
      var dt=calcDelta9(sc.v25,sc.v26);
      return '<div style="flex:1;min-width:0;padding:12px 16px 10px;'
        +'background:rgba(15,23,42,0.80);border-top:2px solid '+sc.col+';'
        +'border-right:0.5px solid rgba(255,255,255,0.04);">'
        +'<div style="font-size:9px;font-weight:800;letter-spacing:0.08em;color:#94A3B8;'
          +'text-transform:uppercase;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">'
          +sc.lbl+'</div>'
        +'<div style="font-size:20px;font-weight:800;color:#f1f5f9;line-height:1.15;margin-top:5px;">'
          +fmtV9(sc.v26)+'</div>'
        +'<div style="font-size:10px;color:#94A3B8;margin-top:2px;white-space:nowrap;'
          +'overflow:hidden;text-overflow:ellipsis;">'+sc.sub+'</div>'
        +'<div style="font-size:14px;font-weight:900;color:'+dt.col+';margin-top:5px;">'
          +(dt.up?'▲':'▼')+' '+dt.str
          +'<span style="font-size:9px;color:#64748b;font-weight:400;margin-left:5px;">vs FYTD25</span>'
        +'</div>'
        +'</div>';
    }).join('');
  }

  // ── Gerador de linha de barra ──
  function makeBarRow9(label,labelCol,v25,v26,cor,isTotalRow){
    var dt=calcDelta9(v25,v26);
    var w26=scaleRef>0?Math.max(isTotalRow?100:1,Math.round(v26/scaleRef*100)):0;
    var w25=scaleRef>0?Math.max(0,Math.round(v25/scaleRef*100)):0;
    if(isTotalRow){w26=100;w25=Math.round(v25/scaleRef*100);}
    var valInside=w26>18;
    var valStyle=valInside
      ?'position:absolute;right:8px;top:50%;transform:translateY(-50%);'
        +'font-size:10px;font-weight:800;color:rgba(0,0,0,0.75);white-space:nowrap;'
      :'position:absolute;left:'+(w26+1)+'%;top:50%;transform:translateY(-50%);'
        +'font-size:10px;font-weight:700;color:'+cor+';white-space:nowrap;padding-left:3px;';
    var trackBg=isTotalRow
      ?'background:rgba(34,197,94,0.08);border:0.5px solid rgba(34,197,94,0.22);'
      :'background:rgba(255,255,255,0.04);';
    var barBg=isTotalRow
      ?'background:rgba(34,197,94,0.35);border-right:2px solid #22c55e;'
      :'background:'+cor+';opacity:0.85;box-shadow:0 0 10px '+cor+'33;';
    return '<div style="flex:1;display:flex;align-items:center;gap:0;padding:2px 0;min-height:36px;">'
      +'<div style="width:108px;flex-shrink:0;text-align:right;padding-right:10px;">'
        +'<span style="font-size:10px;font-weight:700;color:'+labelCol+';white-space:nowrap;">'
          +label+'</span>'
      +'</div>'
      +'<div style="flex:1;display:flex;flex-direction:column;justify-content:center;gap:3px;">'
        +'<div style="position:relative;height:26px;border-radius:4px;'+trackBg+'">'
          +'<div style="position:absolute;left:0;top:6px;bottom:6px;width:'+w25+'%;'
            +'background:rgba(100,116,139,0.15);border-right:1.5px solid rgba(100,116,139,0.25);'
            +'border-radius:2px;"></div>'
          +'<div style="position:absolute;left:0;top:0;bottom:0;width:'+w26+'%;'
            +'border-radius:4px;'+barBg+'"></div>'
          +(w26>0?'<span style="'+valStyle+'">'+fmtV9(v26,true)+'</span>':'')
        +'</div>'
        +'<div style="font-size:9px;color:#cbd5e1;padding-left:2px;white-space:nowrap;">'
          +'FY25: '+fmtV9(v25,true)
        +'</div>'
      +'</div>'
      +'<span style="width:72px;flex-shrink:0;text-align:right;font-size:12px;font-weight:900;'
        +'color:'+dt.col+';padding-left:8px;white-space:nowrap;">'
        +(dt.up?'▲':'▼')+' '+dt.str+'</span>'
      +'</div>';
  }

  // ── AREA PRINCIPAL ──
  var barsEl=document.getElementById('mso3-bars');
  if(!barsEl) return;
  barsEl.style.cssText='display:flex;gap:0;align-items:stretch;margin-bottom:14px;';

  // X-axis
  var tickVals=[0,0.25,0.5,0.75,1].map(function(f){return f*mtV26;});
  var xAxisHtml='<div style="display:flex;align-items:flex-start;padding-top:4px;'
    +'border-top:0.5px solid rgba(255,255,255,0.05);margin-top:2px;">'
    +'<div style="width:108px;flex-shrink:0;"></div>'
    +'<div style="flex:1;display:flex;justify-content:space-between;">'
    +tickVals.map(function(t,i){
      var txt=(t===0)?'0':fmtV9(t,true);
      var a=i===0?'left':i===tickVals.length-1?'right':'center';
      return '<span style="font-size:9px;color:#64748b;text-align:'+a+';flex:1;">'+txt+'</span>';
    }).join('')
    +'</div>'
    +'<div style="width:72px;flex-shrink:0;"></div>'
    +'</div>';

  var chartCol=
    '<div style="flex:1;min-width:0;padding-right:4px;display:flex;flex-direction:column;min-height:300px;">'
    +makeBarRow9('TOTAL MKT','#22c55e',mtV25,mtV26,'#22c55e',true)
    +brands.map(function(b){
      return makeBarRow9(b,colors[b]||'#94A3B8',d25[b]||0,d26[b]||0,colors[b]||'#64748b',false);
    }).join('')
    +xAxisHtml
    +'</div>';

  // ── Sidebar 4 colunas: BRAND | FYTD25 | FYTD26 | Δ ──
  var sideRows9=
    '<tr style="background:rgba(34,197,94,0.08);border-bottom:0.5px solid rgba(34,197,94,0.2);">'
    +'<td style="padding:6px 7px;font-size:10px;">'
      +'<span style="display:inline-flex;align-items:center;gap:4px;">'
      +'<span style="width:7px;height:7px;border-radius:2px;background:#22c55e;display:inline-block;flex-shrink:0;"></span>'
      +'<span style="color:#22c55e;font-weight:700;">TOTAL</span>'
      +'</span></td>'
    +'<td style="padding:6px 7px;font-size:10px;text-align:right;color:#fbbf24;font-weight:700;white-space:nowrap;">'
      +fmtV9(mtV25,true)+'</td>'
    +'<td style="padding:6px 7px;font-size:10px;text-align:right;font-weight:700;color:#f1f5f9;white-space:nowrap;">'
      +fmtV9(mtV26,true)+'</td>'
    +'<td style="padding:6px 7px;font-size:14px;text-align:right;font-weight:900;color:'
      +mtDt.col+';white-space:nowrap;">'
      +(mtDt.up?'▲':'▼')+' '+mtDt.str+'</td>'
    +'</tr>';

  brands.forEach(function(b){
    var v25=d25[b]||0,v26=d26[b]||0;
    var cor=colors[b]||'#64748b';
    var dt=calcDelta9(v25,v26);
    sideRows9+='<tr style="border-bottom:0.5px solid rgba(255,255,255,0.04);">'
      +'<td style="padding:5px 7px;font-size:10px;">'
        +'<span style="display:inline-flex;align-items:center;gap:4px;">'
        +'<span style="width:6px;height:6px;border-radius:1px;background:'+cor+';display:inline-block;flex-shrink:0;"></span>'
        +'<span style="color:'+cor+';font-weight:600;white-space:nowrap;overflow:hidden;'
          +'text-overflow:ellipsis;max-width:70px;display:inline-block;vertical-align:middle;">'+b+'</span>'
        +'</span></td>'
      +'<td style="padding:5px 7px;font-size:10px;text-align:right;color:#fbbf24;font-weight:700;white-space:nowrap;">'
        +fmtV9(v25,true)+'</td>'
      +'<td style="padding:5px 7px;font-size:10px;text-align:right;font-weight:700;color:#e2e8f0;white-space:nowrap;">'
        +fmtV9(v26,true)+'</td>'
      +'<td style="padding:5px 7px;font-size:14px;text-align:right;font-weight:900;color:'+dt.col+';white-space:nowrap;">'
        +(dt.up?'▲':'▼')+' '+dt.str+'</td>'
      +'</tr>';
  });

  var sideTable=
    '<div style="width:290px;flex-shrink:0;margin-left:10px;background:rgba(255,255,255,0.02);'
      +'border-radius:6px;overflow:hidden;border:0.5px solid rgba(255,255,255,0.07);'
      +'display:flex;flex-direction:column;">'
    +'<table style="width:100%;border-collapse:collapse;flex:1;">'
    +'<thead><tr style="border-bottom:1px solid rgba(255,255,255,0.08);">'
    +'<th style="padding:5px 7px;font-size:9px;font-weight:700;letter-spacing:0.07em;color:#94A3B8;text-align:left;">BRAND</th>'
    +'<th style="padding:5px 7px;font-size:9px;font-weight:700;letter-spacing:0.07em;color:#fbbf24;text-align:right;">FYTD25</th>'
    +'<th style="padding:5px 7px;font-size:9px;font-weight:700;letter-spacing:0.07em;color:#f1f5f9;text-align:right;">FYTD26</th>'
    +'<th style="padding:5px 7px;font-size:9px;font-weight:700;letter-spacing:0.07em;color:#94A3B8;text-align:right;">Δ YoY</th>'
    +'</tr></thead>'
    +'<tbody>'+sideRows9+'</tbody>'
    +'</table>'
    +'<div style="padding:5px 8px;font-size:9px;color:#64748b;border-top:0.5px solid rgba(255,255,255,0.04);">'
      +'NielsenIQ · 1-Tabela-1 · FYTD = Jul–Mar</div>'
    +'</div>';

  barsEl.innerHTML=chartCol+sideTable;

  // ── INSIGHT rodé (neon bullet) ──
  var insEl=document.getElementById('mso3-insight');
  if(insEl){
    insEl.style.cssText='padding:10px 16px;background:rgba(255,255,255,0.02);'
      +'border-radius:8px;border-left:3px solid rgba(34,197,94,0.35);'
      +'font-size:10px;color:#D1D5DB;line-height:1.8;margin-top:2px;';
    var ents9=brands.map(function(b){
      var v25=d25[b],v26=d26[b]; if(v25==null||v26==null) return null;
      var dt=calcDelta9(v25,v26);
      return {b:b,dt:dt,cor:colors[b]||'#e2e8f0',v26:v26};
    }).filter(Boolean);
    if(!ents9.length){insEl.innerHTML='';return;}
    var srt9=ents9.slice().sort(function(a,b){return b.dt.raw-a.dt.raw;});
    var ldr9=srt9[0],lag9=srt9[srt9.length-1];
    var mDt=calcDelta9(mtV25,mtV26);
    var mLbl9=isVal?'Tamanho do Mercado · Valor':'Tamanho do Mercado · Unidades';
    var totLine=mt
      ?'Total mercado: <strong style="color:#f1f5f9;">'+fmtV9(mtV26)+'</strong>'
        +' <span style="color:'+mDt.col+';font-weight:700;">'+(mDt.up?'▲':'▼')+' '+mDt.str
        +' vs FYTD25</span><br>':'';
    var ldrTxt=ldr9.dt.up
      ?'<strong style="color:'+ldr9.cor+';">'+ldr9.b+'</strong>'
        +' lidera <span style="color:#4ade80;font-weight:700;">▲ '+ldr9.dt.str+'</span> vs FYTD25'
      :'Todas as marcas recuam vs FYTD25';
    var lagTxt=(!lag9.dt.up&&lag9.b!==ldr9.b)
      ?' · <strong style="color:'+lag9.cor+';">'+lag9.b+'</strong>'
        +' maior retração <span style="color:#f87171;font-weight:700;">'+lag9.dt.str+'</span>':'';
    insEl.innerHTML=
      '<span style="display:inline-block;width:7px;height:7px;border-radius:50%;'
        +'background:#22c55e;box-shadow:0 0 6px #22c55e88;margin-right:7px;vertical-align:middle;"></span>'
      +'<strong style="color:#22c55e;letter-spacing:0.06em;">Diagnóstico · '+mLbl9+'</strong>'
      +'<br>'+totLine+ldrTxt+lagTxt+'.'
      +'<br><span style="font-size:9px;color:#64748b;">Período: FYTD (Jul–Mar) · NielsenIQ · '+mkt+'</span>';
  }
}
/* ═══════════ END MSO3 ═══════════ */'''

html = html[:idx_start] + NEW_RENDER + html[idx_end + len(END_MSO3):]
print("PATCH 2 OK — renderMSO3 v9 aplicado")

# ── Salva ────────────────────────────────────────────────────────────────
DASH_FILE.write_text(html, encoding="utf-8")
final = VERS_DIR / f"Dashboard_Farma_Sul_{ts}_MSO3v9.html"
shutil.copy2(str(DASH_FILE), str(final))
print(f"\nSalvo: {DASH_FILE.name} ({len(html):,} chars)")
print(f"Versao: {final.name}")

# ── Verificacao ───────────────────────────────────────────────────────────
print("\n--- Verificacao ---")
for mkt in ["Farma Sul", "T.BR Farma", "Farma Indep Sul", "Farma Moderno Sul"]:
    d = data.get(mkt, {})
    cres = (d.get("fytd26_val",0)/d.get("fytd25_val",1)-1)*100 if d.get("fytd25_val",0)>0 else 0
    print(f"  {mkt:<25} F25={d.get('fytd25_val',0):.3f}MM  F26={d.get('fytd26_val',0):.3f}MM  Cres={cres:+.2f}%")

# Confirma END_MSO3 presente
if END_MSO3 not in html:
    # Tenta com unicode
    if "END MSO3" in html:
        print("  END MSO3 OK (unicode)")
    else:
        print("  ATENCAO: END MSO3 nao encontrado!")
else:
    print("\n  Ancora END MSO3 OK")
print("Done. v9 aplicado.")
