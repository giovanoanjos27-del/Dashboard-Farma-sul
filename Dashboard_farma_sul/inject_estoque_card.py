#!/usr/bin/env python3
# inject_estoque_card.py
# Injects the Estoque & DOH por Cliente card into the dashboard HTML

import os
import shutil
from datetime import datetime

# ── Paths ──────────────────────────────────────────────────────────────────────
DASHBOARD_DIR = r"C:\Users\valqu\OneDrive\Documentos\Claude\Projects\projeto Dashboard_farma_sul\Dashboard_farma_sul"
VERSOES_DIR   = os.path.join(DASHBOARD_DIR, "versoes")
DOWNLOADS_DIR = r"C:\Users\valqu\Downloads"
SOURCE_FILE   = os.path.join(DASHBOARD_DIR, "Dashboard_Farma_Sul_20260512_2220.html")
ANCHOR        = "<!-- VERBAS -->"

now_str  = datetime.now().strftime("%Y%m%d_%H%M")
version_name   = f"Dashboard_Farma_Sul_{now_str}_EstoqueCard.html"
version_path   = os.path.join(VERSOES_DIR, version_name)
downloads_name = f"Dashboard_FarmaSul_Giovano_{now_str}.html"
downloads_path = os.path.join(DOWNLOADS_DIR, downloads_name)

# ── Card HTML+JS to inject ─────────────────────────────────────────────────────
CARD_HTML = r"""
<!-- ESTOQUE & DOH CARD -->
<script>
const ESTOQUE_DATA = {
  "DD-GAM": {
    data_ref:"Abr/2026", est_total:59594, so_mes:32246, doh:55.4,
    critico:13, atencao:5, ok:4,
    skus: [
      {marca:"LYSOFORM",sku:"LYSOFORM AERO ORIGINAL 250ML",est:438,so:227,doh:57.9,status:"❗ CRÍTICO"},
      {marca:"PATO",sku:"ODORIZADOR PATO BLOCK SPRAY ALGODAO 60ML",est:227,so:7,doh:972.9,status:"✓ OK"},
      {marca:"PATO",sku:"ODORIZADOR PATO BLOCK SPRAY EUCALIPTO 60ML",est:304,so:8,doh:1140.0,status:"✓ OK"},
      {marca:"PATO",sku:"ODORIZADOR PATO BLOCK SPRAY LAVANDA 60ML",est:176,so:13,doh:406.2,status:"✓ OK"},
      {marca:"EXPOSIS",sku:"REPELENTE EXPOSIS COM APARELHO CASA+REFIL 32.9ML",est:430,so:345,doh:37.4,status:"🔴 CRÍTICO"},
      {marca:"EXPOSIS",sku:"REPELENTE EXPOSIS GATILHO 150ML",est:203,so:162,doh:37.6,status:"🔴 CRÍTICO"},
      {marca:"EXPOSIS",sku:"REPELENTE EXPOSIS ICARIDINA BEBE GEL 117ML",est:1058,so:569,doh:55.8,status:"🔴 CRÍTICO"},
      {marca:"EXPOSIS",sku:"REPELENTE EXPOSIS ICARIDINA EXTREME SPRAY 100ML",est:1141,so:718,doh:47.7,status:"🔴 CRÍTICO"},
      {marca:"EXPOSIS",sku:"REPELENTE EXPOSIS ICARIDINA GEL 100ML",est:606,so:441,doh:41.2,status:"🔴 CRÍTICO"},
      {marca:"EXPOSIS",sku:"REPELENTE EXPOSIS ICARIDINA INFANTIL GEL 100ML",est:1343,so:820,doh:49.1,status:"🔴 CRÍTICO"},
      {marca:"EXPOSIS",sku:"REPELENTE EXPOSIS ICARIDINA INFANTIL SPRAY 100ML",est:1463,so:848,doh:51.8,status:"🔴 CRÍTICO"},
      {marca:"EXPOSIS",sku:"REPELENTE EXPOSIS REFIL 32.9ML",est:89,so:229,doh:11.7,status:"🔴 CRÍTICO"},
      {marca:"OFF!",sku:"REPELENTE OFF BABY LOCAO 117ML",est:8150,so:2918,doh:83.8,status:"⚠ ATENÇÃO"},
      {marca:"OFF!",sku:"REPELENTE OFF FAMILY GEL HIDRAT.TOQUE LEVE 100ML",est:991,so:359,doh:82.8,status:"⚠ ATENÇÃO"},
      {marca:"OFF!",sku:"REPELENTE OFF FAMILY OFERTA ESPECIAL LOCAO 200ML",est:6584,so:9968,doh:19.8,status:"🔴 CRÍTICO"},
      {marca:"OFF!",sku:"REPELENTE OFF FAMILY SPRAY 170ML",est:14916,so:6365,doh:70.3,status:"⚠ ATENÇÃO"},
      {marca:"OFF!",sku:"REPELENTE OFF FAMILY TOQUE LEVE SPRAY 100ML",est:788,so:133,doh:177.7,status:"✓ OK"},
      {marca:"OFF!",sku:"REPELENTE OFF KIDS LOCAO 200ML",est:16625,so:5774,doh:86.4,status:"⚠ ATENÇÃO"},
      {marca:"OFF!",sku:"REPELENTE OFF LONGA DURACAO LOCAO 100ML",est:1851,so:687,doh:80.8,status:"⚠ ATENÇÃO"},
      {marca:"RAID",sku:"REPELENTE RAID ELETRICO LIQ. 45N REFIL 32.9ML",est:613,so:473,doh:38.9,status:"🔴 CRÍTICO"},
      {marca:"RAID",sku:"REPELENTE RAID ELETRICO REFIL 2UN 32.9ML",est:800,so:419,doh:57.3,status:"🔴 CRÍTICO"},
      {marca:"RAID",sku:"REPELENTE RAID RAID LE FAMILY 45N AP 32.9ML",est:798,so:763,doh:31.4,status:"🔴 CRÍTICO"}
    ]
  },
  "São João": {
    data_ref:"Abr/2026", est_total:87278, so_mes:18774, doh:139.5,
    critico:8, atencao:15, ok:45,
    skus: [
      {marca:"EXPOSIS",sku:"KIT REPELENTE GEL EXPOSIS 100ML+REPELENTE GEL BEBE 117G S/PERFUME",est:1117,so:16,doh:2094.4,status:"✓ OK"},
      {marca:"EXPOSIS",sku:"KIT REPELENTE GEL EXPOSIS 100ML+REPELENTE INF 52ML S/PERFUME",est:793,so:47,doh:506.2,status:"✓ OK"},
      {marca:"EXPOSIS",sku:"KIT REPELENTE LIQ EXPOSIS 100ML+REPELENTE EXTREME 52ML S/PERFUME",est:880,so:49,doh:538.8,status:"✓ OK"},
      {marca:"EXPOSIS",sku:"KIT REPELENTE LIQ EXPOSIS CASA 32,9ML E",est:578,so:179,doh:96.9,status:"⚠ ATENÇÃO"},
      {marca:"RAID",sku:"RAID INSET 12UN REFIL PASTILHAS LV12 PG10",est:16,so:0,doh:null,status:"✓ OK"},
      {marca:"RAID",sku:"RAID INSET APAR ELET 12PAST 12HORAS 4NOITES",est:4,so:0,doh:null,status:"✓ OK"},
      {marca:"RAID",sku:"RAID INSET APAR ELET LIQ 45 NOITES + REFIL 32,9ML",est:94,so:76,doh:37.1,status:"🔴 CRÍTICO"},
      {marca:"RAID",sku:"RAID INSET APAR ELET LIQ 45 NOITES + REFIL 32,9ML FAMILY",est:165,so:184,doh:26.9,status:"🔴 CRÍTICO"},
      {marca:"RAID",sku:"RAID INSET LIQ 32,9ML RFL 45 NOITES FAMILY 50%DESC 2°UN",est:459,so:193,doh:71.3,status:"⚠ ATENÇÃO"},
      {marca:"RAID",sku:"RAID INSET LIQ REFIL 32,9ML 50%DESC 2°UN",est:291,so:117,doh:74.6,status:"⚠ ATENÇÃO"},
      {marca:"RAID",sku:"RAID MULTI AERO 420ML AQUA PROTECTION ECONOMICA",est:389,so:159,doh:73.4,status:"⚠ ATENÇÃO"},
      {marca:"OFF!",sku:"RAID MULTI AERO 420ML BASE AGUA LV+ PG-",est:190,so:101,doh:56.4,status:"🔴 CRÍTICO"},
      {marca:"EXPOSIS",sku:"RAID MULTI AERO 420ML EUCALIPTO LV+ PG-",est:1,so:0,doh:null,status:"✓ OK"},
      {marca:"EXPOSIS",sku:"RAID MULTI INSET AERO 420ML ESSENCIAL",est:55,so:16,doh:103.1,status:"⚠ ATENÇÃO"},
      {marca:"EXPOSIS",sku:"REPELENTE AEROSSOL OFF 100ML TOQUE LEVE S/PERFUME SPRAY",est:3769,so:616,doh:183.6,status:"✓ OK"},
      {marca:"EXPOSIS",sku:"REPELENTE EXPOSIS 100ML AERO EXTREME",est:2126,so:153,doh:416.9,status:"✓ OK"},
      {marca:"EXPOSIS",sku:"REPELENTE EXPOSIS GEL 100ML ICARIDINA",est:2048,so:182,doh:337.8,status:"✓ OK"},
      {marca:"EXPOSIS",sku:"REPELENTE EXPOSIS GEL BEBE 117G",est:1831,so:231,doh:237.8,status:"✓ OK"},
      {marca:"EXPOSIS",sku:"REPELENTE EXPOSIS GEL INFANTIL 100ML ICARIDINA",est:1694,so:193,doh:263.3,status:"✓ OK"},
      {marca:"EXPOSIS",sku:"REPELENTE EXPOSIS ICARIDINA EXTREME SPRAY 100ML",est:756,so:95,doh:238.7,status:"✓ OK"},
      {marca:"EXPOSIS",sku:"REPELENTE EXPOSIS KIT LIQU CASAS + REFIL",est:325,so:85,doh:114.7,status:"⚠ ATENÇÃO"},
      {marca:"EXPOSIS",sku:"REPELENTE EXPOSIS REFIL 32.9ML",est:96,so:87,doh:33.1,status:"🔴 CRÍTICO"},
      {marca:"EXPOSIS",sku:"REPELENTE EXPOSIS SPRAY EXTREME 100ML",est:1031,so:148,doh:209.3,status:"✓ OK"},
      {marca:"OFF!",sku:"REPELENTE OFF AEROSSOL INSETICIDE",est:1282,so:113,doh:340.4,status:"✓ OK"},
      {marca:"OFF!",sku:"REPELENTE OFF BABY GEL 117G",est:2453,so:462,doh:159.5,status:"✓ OK"},
      {marca:"OFF!",sku:"REPELENTE OFF FAMILY GEL HIDRAT.TOQUE LEVE 100ML",est:2043,so:351,doh:174.7,status:"✓ OK"},
      {marca:"OFF!",sku:"REPELENTE OFF FAMILY LOCAO 200ML",est:2668,so:1154,doh:69.4,status:"⚠ ATENÇÃO"},
      {marca:"OFF!",sku:"REPELENTE OFF FAMILY LOCAO 200ML LV+PG-",est:4116,so:1349,doh:91.5,status:"✓ OK"},
      {marca:"OFF!",sku:"REPELENTE OFF FAMILY SPRAY 170ML",est:7337,so:2296,doh:96.0,status:"✓ OK"},
      {marca:"OFF!",sku:"REPELENTE OFF FAMILY SPRAY 170ML LV+PG-",est:5313,so:2048,doh:77.8,status:"⚠ ATENÇÃO"},
      {marca:"OFF!",sku:"REPELENTE OFF FAMILY TOQUE LEVE SPRAY 100ML",est:1047,so:182,doh:172.7,status:"✓ OK"},
      {marca:"OFF!",sku:"REPELENTE OFF KIDS 200ML",est:2296,so:712,doh:96.9,status:"✓ OK"},
      {marca:"OFF!",sku:"REPELENTE OFF KIDS LOCAO 200ML",est:5826,so:1742,doh:100.4,status:"✓ OK"},
      {marca:"OFF!",sku:"REPELENTE OFF KIDS LOCAO 200ML LV+PG-",est:3944,so:1431,doh:82.7,status:"⚠ ATENÇÃO"},
      {marca:"OFF!",sku:"REPELENTE OFF LONGA DURACAO 100ML",est:1149,so:336,doh:102.6,status:"✓ OK"},
      {marca:"OFF!",sku:"REPELENTE OFF LONGA DURACAO GEL TOQUE LEVE 100ML",est:1026,so:172,doh:179.1,status:"✓ OK"},
      {marca:"OFF!",sku:"REPELENTE OFF LONGA DURACAO LOCAO 100ML",est:1065,so:288,doh:111.0,status:"⚠ ATENÇÃO"},
      {marca:"OFF!",sku:"REPELENTE OFF MILITARY LOCAO 100ML",est:1222,so:225,doh:163.0,status:"✓ OK"},
      {marca:"RAID",sku:"REPELENTE RAID ELETRICO LIQ. 45N REFIL 32.9ML",est:1046,so:506,doh:62.0,status:"⚠ ATENÇÃO"},
      {marca:"RAID",sku:"REPELENTE RAID ELETRICO REFIL 2UN 32.9ML",est:1264,so:444,doh:85.4,status:"⚠ ATENÇÃO"},
      {marca:"RAID",sku:"REPELENTE RAID RAID LE FAMILY 45N AP 32.9ML",est:953,so:603,doh:47.4,status:"🔴 CRÍTICO"},
      {marca:"RAID",sku:"REPELENTE RAID ELETRICO FAMILY + REFIL 32.9ML 45N",est:1020,so:379,doh:80.8,status:"⚠ ATENÇÃO"},
      {marca:"RAID",sku:"REPELENTE RAID ELETRICO FAMILY + REFIL 32.9ML 45N LV+PG-",est:965,so:302,doh:95.9,status:"✓ OK"},
      {marca:"RAID",sku:"REPELENTE RAID ELETRICO LIQ FAMILY 45N AP 32.9ML",est:982,so:247,doh:119.3,status:"⚠ ATENÇÃO"},
      {marca:"RAID",sku:"REPELENTE RAID ELETRICO LIQ FAMILY REFIL 32.9ML",est:974,so:221,doh:132.5,status:"✓ OK"},
      {marca:"RAID",sku:"REPELENTE RAID MULTI INSET AERO 420ML AQUA PROTECTION",est:1235,so:331,doh:112.0,status:"✓ OK"},
      {marca:"RAID",sku:"REPELENTE RAID MULTI INSET AERO 420ML ESSENCIAL",est:1182,so:218,doh:162.8,status:"✓ OK"},
      {marca:"RAID",sku:"REPELENTE RAID MULTI INSET AERO BASE AGUA 420ML",est:1054,so:182,doh:174.0,status:"✓ OK"},
      {marca:"RAID",sku:"REPELENTE RAID MULTI INSET AERO LAVANDA 420ML",est:1055,so:195,doh:162.3,status:"✓ OK"},
      {marca:"RAID",sku:"REPELENTE RAID ELETRICO LIQ REFIL 32.9ML MAX",est:934,so:148,doh:189.6,status:"✓ OK"},
      {marca:"RAID",sku:"REPELENTE RAID ELETRICO LIQ REFIL FAMILY 32.9ML MAX",est:872,so:133,doh:196.7,status:"✓ OK"},
      {marca:"RAID",sku:"REPELENTE RAID INSET AERO 300ML BASE AGUA",est:845,so:115,doh:220.9,status:"✓ OK"},
      {marca:"RAID",sku:"REPELENTE RAID ELETRICO LIQ APARELHO + REFIL 32.9ML MAX",est:769,so:103,doh:224.0,status:"✓ OK"}
    ]
  },
  "Nissei": {
    data_ref:"Abr/2026", est_total:40105, so_mes:9724, doh:123.7,
    critico:8, atencao:7, ok:24, skus:[]
  },
  "Clamed": {
    data_ref:"Abr/2026", est_total:42630, so_mes:9892, doh:129.3,
    critico:2, atencao:1, ok:13, skus:[]
  },
  "Panvel": {
    data_ref:"Abr/2026", est_total:68921, so_mes:12017, doh:172.1,
    critico:0, atencao:4, ok:22, skus:[]
  },
  "DD-Gaúcha": {
    data_ref:"Abr/2026", est_total:19558, so_mes:23649, doh:24.8,
    critico:28, atencao:10, ok:7, skus:[]
  },
  "DD-Riomed": {
    data_ref:"Abr/2026", est_total:29640, so_mes:6092, doh:146.0,
    critico:7, atencao:6, ok:19, skus:[]
  }
};

const ESTOQUE_CLIENT_COLORS = {
  "São João": "#60a5fa",
  "DD-Gaúcha":    "#f97316",
  "Panvel":      "#2dd4bf",
  "DD-GAM":      "#34d399",
  "Nissei":      "#a78bfa",
  "DD-Riomed":   "#fb923c",
  "Clamed":      "#f472b6"
};

function estoqueDohColor(doh) {
  if (doh === null || doh === undefined) return "#94a3b8";
  if (doh < 30)  return "#ef4444";
  if (doh < 60)  return "#f97316";
  if (doh < 90)  return "#fbbf24";
  return "#34d399";
}

function estoqueDohBar(doh, maxDoh) {
  const color = estoqueDohColor(doh);
  if (doh === null || doh === undefined) {
    return '<div style="height:8px;border-radius:4px;background:#1e293b;width:100%;"></div>';
  }
  const pct = Math.min(100, (doh / maxDoh) * 100);
  return `<div style="height:8px;border-radius:4px;background:#1e293b;width:100%;position:relative;">
    <div style="height:8px;border-radius:4px;background:${color};width:${pct.toFixed(1)}%;position:absolute;top:0;left:0;"></div>
  </div>`;
}

function renderEstoqueCard() {
  const clients = Object.keys(ESTOQUE_DATA);
  const maxDoh = Math.max(...clients.map(c => ESTOQUE_DATA[c].doh || 0));

  // ── Summary table ──────────────────────────────────────────────────────────
  let summaryRows = "";
  clients.forEach(name => {
    const d = ESTOQUE_DATA[name];
    const color = ESTOQUE_CLIENT_COLORS[name] || "#94a3b8";
    const dohColor = estoqueDohColor(d.doh);
    const dohLabel = d.doh !== null ? d.doh.toFixed(1) + "d" : "—";
    const totalSkus = d.critico + d.atencao + d.ok;
    let statusBadge = "";
    if (d.critico > 0) {
      statusBadge = `<span style="font-size:10px;padding:2px 7px;border-radius:4px;background:rgba(239,68,68,0.15);color:#ef4444;font-weight:700;">🔴 ${d.critico} crítico${d.critico > 1 ? "s" : ""}</span>`;
    } else if (d.atencao > 0) {
      statusBadge = `<span style="font-size:10px;padding:2px 7px;border-radius:4px;background:rgba(249,115,22,0.15);color:#f97316;font-weight:700;">⚠ Monitorar</span>`;
    } else {
      statusBadge = `<span style="font-size:10px;padding:2px 7px;border-radius:4px;background:rgba(52,211,153,0.15);color:#34d399;font-weight:700;">✓ Saudável</span>`;
    }

    summaryRows += `
    <tr style="border-bottom:1px solid rgba(255,255,255,0.04);">
      <td style="padding:10px 8px;font-size:12px;color:${color};font-weight:700;white-space:nowrap;">${name}</td>
      <td style="padding:10px 8px;font-size:12px;color:#e2e8f0;text-align:right;">${d.est_total.toLocaleString("pt-BR")}</td>
      <td style="padding:10px 8px;font-size:12px;color:#94a3b8;text-align:right;">${d.so_mes.toLocaleString("pt-BR")}</td>
      <td style="padding:10px 8px;min-width:120px;">
        <div style="display:flex;align-items:center;gap:8px;">
          <span style="font-size:12px;color:${dohColor};font-weight:700;min-width:40px;">${dohLabel}</span>
          ${estoqueDohBar(d.doh, maxDoh)}
        </div>
      </td>
      <td style="padding:10px 8px;text-align:center;font-size:12px;color:#ef4444;">${d.critico || "—"}</td>
      <td style="padding:10px 8px;text-align:center;font-size:12px;color:#f97316;">${d.atencao || "—"}</td>
      <td style="padding:10px 8px;text-align:center;font-size:12px;color:#34d399;">${d.ok || "—"}</td>
      <td style="padding:10px 8px;">${statusBadge}</td>
    </tr>`;
  });

  // ── Build HTML ─────────────────────────────────────────────────────────────
  const filterBtns = ['Todos', ...clients].map((name, i) => {
    const active = i === 0 ? ' active' : '';
    const key = name === 'Todos' ? 'todos' : name;
    return `<button class="tgl${active}" onclick="estoqueFiltrar('${key}',this)" style="margin:2px 3px;">${name}</button>`;
  }).join('');

  document.getElementById('estoque-card').innerHTML = `
    <!-- Card Header -->
    <div class="card-header" style="margin-bottom:16px;">
      <div>
        <div style="font-size:10px;font-weight:700;letter-spacing:0.1em;color:#34d399;margin-bottom:4px;">ESTOQUE &amp; DOH</div>
        <div class="card-title">📦 Estoque &amp; DOH — Por Cliente · Ref. Abr/2026</div>
        <div class="card-sub">Estoque em caixas · Último SO fechado · Days On Hand</div>
      </div>
    </div>

    <!-- Filter buttons -->
    <div style="margin-bottom:14px;display:flex;flex-wrap:wrap;gap:0;">
      ${filterBtns}
    </div>

    <!-- Summary table -->
    <div style="overflow-x:auto;margin-bottom:4px;">
      <table style="width:100%;border-collapse:collapse;">
        <thead>
          <tr style="border-bottom:1px solid rgba(255,255,255,0.08);">
            <th style="padding:6px 8px;font-size:9px;color:#475569;font-weight:700;text-transform:uppercase;text-align:left;">CLIENTE</th>
            <th style="padding:6px 8px;font-size:9px;color:#475569;font-weight:700;text-transform:uppercase;text-align:right;">ESTOQUE (cx)</th>
            <th style="padding:6px 8px;font-size:9px;color:#475569;font-weight:700;text-transform:uppercase;text-align:right;">SO REF/MÊS</th>
            <th style="padding:6px 8px;font-size:9px;color:#475569;font-weight:700;text-transform:uppercase;min-width:140px;">DOH</th>
            <th style="padding:6px 8px;font-size:9px;color:#ef4444;font-weight:700;text-align:center;">🔴 CRÍTICO</th>
            <th style="padding:6px 8px;font-size:9px;color:#f97316;font-weight:700;text-align:center;">⚠ ATENÇÃO</th>
            <th style="padding:6px 8px;font-size:9px;color:#34d399;font-weight:700;text-align:center;">✓ OK</th>
            <th style="padding:6px 8px;font-size:9px;color:#475569;font-weight:700;text-transform:uppercase;text-align:left;">STATUS</th>
          </tr>
        </thead>
        <tbody id="estoque-summary-tbody">
          ${summaryRows}
        </tbody>
      </table>
    </div>

    <!-- Detail panel -->
    <div id="estoque-detail-panel" style="display:none;margin-top:16px;padding:14px;background:rgba(255,255,255,0.02);border-radius:8px;border:0.5px solid rgba(255,255,255,0.06);">
      <div id="estoque-detail-title" style="font-size:11px;font-weight:700;color:#e2e8f0;margin-bottom:10px;"></div>
      <div style="overflow-x:auto;">
        <table style="width:100%;border-collapse:collapse;">
          <thead>
            <tr style="border-bottom:1px solid rgba(255,255,255,0.08);">
              <th style="padding:5px 8px;font-size:9px;color:#475569;font-weight:700;text-transform:uppercase;text-align:left;white-space:nowrap;">MARCA</th>
              <th style="padding:5px 8px;font-size:9px;color:#475569;font-weight:700;text-transform:uppercase;text-align:left;">SKU</th>
              <th style="padding:5px 8px;font-size:9px;color:#475569;font-weight:700;text-transform:uppercase;text-align:right;">ESTOQUE</th>
              <th style="padding:5px 8px;font-size:9px;color:#475569;font-weight:700;text-transform:uppercase;text-align:right;">SO/MÊS</th>
              <th style="padding:5px 8px;font-size:9px;color:#475569;font-weight:700;text-transform:uppercase;min-width:100px;">DOH</th>
              <th style="padding:5px 8px;font-size:9px;color:#475569;font-weight:700;text-transform:uppercase;text-align:left;">STATUS</th>
            </tr>
          </thead>
          <tbody id="estoque-detail-tbody"></tbody>
        </table>
      </div>
      <div style="margin-top:8px;font-size:9px;color:#475569;font-style:italic;">* Detalhamento de SKUs disponível apenas para DD-GAM e São João nesta versão.</div>
    </div>

    <!-- DOH Legend -->
    <div style="margin-top:14px;padding-top:10px;border-top:1px solid rgba(255,255,255,0.06);display:flex;flex-wrap:wrap;gap:12px;align-items:center;">
      <span style="font-size:9px;color:#475569;font-weight:700;text-transform:uppercase;letter-spacing:0.05em;">Legenda DOH:</span>
      <span style="font-size:10px;display:flex;align-items:center;gap:4px;"><span style="display:inline-block;width:10px;height:10px;border-radius:2px;background:#ef4444;"></span><span style="color:#94a3b8;">&lt;30d = Crítico</span></span>
      <span style="font-size:10px;display:flex;align-items:center;gap:4px;"><span style="display:inline-block;width:10px;height:10px;border-radius:2px;background:#f97316;"></span><span style="color:#94a3b8;">30–60d = Atenção</span></span>
      <span style="font-size:10px;display:flex;align-items:center;gap:4px;"><span style="display:inline-block;width:10px;height:10px;border-radius:2px;background:#fbbf24;"></span><span style="color:#94a3b8;">60–90d = Monitorar</span></span>
      <span style="font-size:10px;display:flex;align-items:center;gap:4px;"><span style="display:inline-block;width:10px;height:10px;border-radius:2px;background:#34d399;"></span><span style="color:#94a3b8;">&gt;90d = OK</span></span>
    </div>
  `;
}

function estoqueFiltrar(key, btn) {
  // toggle active button
  document.querySelectorAll('#estoque-card .tgl').forEach(b => b.classList.remove('active'));
  btn.classList.add('active');

  const detail = document.getElementById('estoque-detail-panel');
  const detailTitle = document.getElementById('estoque-detail-title');
  const tbody = document.getElementById('estoque-detail-tbody');
  const summaryTbody = document.getElementById('estoque-summary-tbody');

  if (key === 'todos') {
    // show all summary rows
    summaryTbody.querySelectorAll('tr').forEach(r => r.style.display = '');
    detail.style.display = 'none';
    return;
  }

  // filter summary to selected client
  const clients = Object.keys(ESTOQUE_DATA);
  summaryTbody.querySelectorAll('tr').forEach((row, i) => {
    row.style.display = (clients[i] === key) ? '' : 'none';
  });

  const d = ESTOQUE_DATA[key];
  if (!d) return;

  if (!d.skus || d.skus.length === 0) {
    detail.style.display = 'block';
    detailTitle.textContent = key + ' — Detalhamento de SKUs (em breve)';
    tbody.innerHTML = '<tr><td colspan="6" style="padding:20px;text-align:center;color:#475569;font-size:11px;">Detalhamento de SKUs será adicionado em próxima atualização.</td></tr>';
    return;
  }

  const color = ESTOQUE_CLIENT_COLORS[key] || "#94a3b8";
  const maxDoh = Math.max(...d.skus.filter(s => s.doh !== null).map(s => s.doh), 1);
  detailTitle.innerHTML = `<span style="color:${color}">${key}</span> — ${d.skus.length} SKUs · Ref. ${d.data_ref}`;

  tbody.innerHTML = d.skus.map(s => {
    const dohColor = estoqueDohColor(s.doh);
    const dohLabel = s.doh !== null ? s.doh.toFixed(1) + "d" : "—";
    return `<tr style="border-bottom:1px solid rgba(255,255,255,0.04);">
      <td style="padding:7px 8px;font-size:10px;color:#94a3b8;font-weight:700;white-space:nowrap;">${s.marca}</td>
      <td style="padding:7px 8px;font-size:10px;color:#cbd5e1;max-width:320px;">${s.sku}</td>
      <td style="padding:7px 8px;font-size:10px;color:#e2e8f0;text-align:right;">${s.est.toLocaleString("pt-BR")}</td>
      <td style="padding:7px 8px;font-size:10px;color:#94a3b8;text-align:right;">${s.so.toLocaleString("pt-BR")}</td>
      <td style="padding:7px 8px;min-width:100px;">
        <div style="display:flex;align-items:center;gap:6px;">
          <span style="font-size:10px;color:${dohColor};font-weight:700;min-width:36px;">${dohLabel}</span>
          ${estoqueDohBar(s.doh, maxDoh)}
        </div>
      </td>
      <td style="padding:7px 8px;font-size:10px;color:${dohColor};white-space:nowrap;">${s.status}</td>
    </tr>`;
  }).join('');

  detail.style.display = 'block';
}

document.addEventListener('DOMContentLoaded', function() {
  renderEstoqueCard();
});
</script>

<!-- Estoque & DOH Card -->
<div id="estoque-card" class="card full" style="margin-bottom:14px;">
  <!-- content injected by renderEstoqueCard() -->
</div>

"""

# ── Read source ────────────────────────────────────────────────────────────────
print(f"Reading: {SOURCE_FILE}")
with open(SOURCE_FILE, 'r', encoding='utf-8') as f:
    content = f.read()

if ANCHOR not in content:
    raise ValueError(f"Anchor '{ANCHOR}' not found in source file!")

# Check if already injected
if 'estoque-card' in content:
    print("WARNING: estoque-card already exists in file. Aborting to avoid duplicate.")
    raise SystemExit(1)

# ── Inject before anchor ───────────────────────────────────────────────────────
new_content = content.replace(ANCHOR, CARD_HTML + "\n  " + ANCHOR, 1)

# ── Save main file ─────────────────────────────────────────────────────────────
print(f"Writing main file: {SOURCE_FILE}")
with open(SOURCE_FILE, 'w', encoding='utf-8') as f:
    f.write(new_content)

# ── Version copy ───────────────────────────────────────────────────────────────
os.makedirs(VERSOES_DIR, exist_ok=True)
print(f"Creating version: {version_path}")
shutil.copy2(SOURCE_FILE, version_path)

# ── Downloads copy ─────────────────────────────────────────────────────────────
os.makedirs(DOWNLOADS_DIR, exist_ok=True)
print(f"Copying to Downloads: {downloads_path}")
shutil.copy2(SOURCE_FILE, downloads_path)

print("\n✔  Done!")
print(f"   Main:      {SOURCE_FILE}")
print(f"   Version:   {version_path}")
print(f"   Downloads: {downloads_path}")
