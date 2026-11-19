"""
Novo card: EVOLUÇÃO YoY POR PROVEDOR
- Ranking: FY25 Jul-Mar vs FY26 Jul-Mar por provedor (delta %)
- CIMED + RB consolidados em coluna única
- Inserido ANTES do FILTRO GRUPO PROVEDOR no painel consolidado
"""

import shutil
from datetime import datetime
from pathlib import Path

BASE = Path(r"C:\Users\valqu\OneDrive\Documentos\Claude\Projects\projeto Dashboard_farma_sul\Dashboard_farma_sul")
DASH = BASE / "Dashboard_Farma_Sul_20260512_2220.html"
VER  = BASE / "versoes"
DL   = Path.home() / "Downloads"

html = DASH.read_text(encoding='utf-8')
orig_len = len(html)

# ══════════════════════════════════════════════════════════════
# 1. JS — renderProvYoYCard()
# ══════════════════════════════════════════════════════════════

NEW_JS = r"""
/* ═══ EVOLUCAO YoY POR PROVEDOR ═══ */
var _yoySortKey = 'delta';   // 'delta' | 'opp' | 'reconq'
var _yoyMinPDVs = 100;        // filtro mínimo FY25 PDV-meses (evita ruído)
var _yoyShowAll  = false;

function setYoYSort(k, btn){
  _yoySortKey = k;
  document.querySelectorAll('#prov-yoy-card .yoy-sort-btn').forEach(function(b){
    b.style.background = 'transparent';
    b.style.color = '#64748b';
    b.style.borderColor = 'rgba(255,255,255,0.07)';
  });
  btn.style.background  = 'rgba(251,191,36,0.15)';
  btn.style.color       = '#fbbf24';
  btn.style.borderColor = 'rgba(251,191,36,0.3)';
  renderProvYoYCard();
}

function toggleYoYAll(btn){
  _yoyShowAll = !_yoyShowAll;
  btn.textContent = _yoyShowAll ? 'Ver Top 20' : 'Ver todos (' + _yoyTotal + ')';
  renderProvYoYCard();
}

var _yoyTotal = 0;

function renderProvYoYCard(){
  var bodyEl = document.getElementById('prov-yoy-body');
  if(!bodyEl || typeof PROV_DATA === 'undefined') return;

  // ── Computar métricas YoY para cada provedor ──
  var rows = [];
  PROV_DATA.forEach(function(p){
    var M = p.monthly || [];
    // FY25 Jul→Mar: índices 3-11 (9 meses)
    var fy25 = 0;
    for(var i=3;i<=11;i++) fy25 += (M[i]||0);
    // FY26 Jul→Mar: índices 15-23 (9 meses)
    var fy26 = 0;
    for(var i=15;i<=23;i++) fy26 += (M[i]||0);
    // Q1 (Jan-Mar) FY25: M[9],M[10],M[11] | FY26: M[21],M[22],M[23]
    var q1_25 = (M[9]||0)+(M[10]||0)+(M[11]||0);
    var q1_26 = (M[21]||0)+(M[22]||0)+(M[23]||0);
    var delta   = fy25 > 0 ? (fy26 - fy25) / fy25 * 100 : null;
    var q1_delta= q1_25 > 0 ? (q1_26 - q1_25) / q1_25 * 100 : null;
    var opp     = p.opp_total || 0;
    var reconq  = p.reconquista || 0;
    var atend   = (opp + reconq) > 0 ? Math.round(reconq / (opp + reconq) * 100) : 0;
    if(fy25 >= _yoyMinPDVs || fy26 >= _yoyMinPDVs){
      rows.push({
        name:    p.name,
        total:   p.total,
        scj:     p.scj,
        pct:     p.pct,
        fy25:    fy25,
        fy26:    fy26,
        delta:   delta,
        q1_25:   q1_25,
        q1_26:   q1_26,
        q1_delta: q1_delta,
        opp_ci:  p.opp_ci||0,
        opp_rb:  p.opp_rb||0,
        opp:     opp,
        reconq:  reconq,
        atend:   atend
      });
    }
  });

  _yoyTotal = rows.length;

  // ── Ordenar ──
  rows.sort(function(a,b){
    if(_yoySortKey === 'opp')    return b.opp   - a.opp;
    if(_yoySortKey === 'reconq') return b.atend  - a.atend;
    // default: delta (nulls ao final)
    if(a.delta === null && b.delta === null) return 0;
    if(a.delta === null) return 1;
    if(b.delta === null) return -1;
    return b.delta - a.delta;
  });

  var visible = _yoyShowAll ? rows : rows.slice(0, 20);

  // ── Totais globais ──
  var totFy25 = 0, totFy26 = 0, totOpp = 0, totReconq = 0, totQ1_25 = 0, totQ1_26 = 0;
  rows.forEach(function(r){ totFy25+=r.fy25; totFy26+=r.fy26; totOpp+=r.opp; totReconq+=r.reconq; totQ1_25+=r.q1_25; totQ1_26+=r.q1_26; });
  var totDelta = totFy25 > 0 ? (totFy26 - totFy25) / totFy25 * 100 : 0;
  var totQ1D   = totQ1_25 > 0 ? (totQ1_26 - totQ1_25) / totQ1_25 * 100 : 0;
  var totAtend = (totOpp + totReconq) > 0 ? Math.round(totReconq / (totOpp + totReconq) * 100) : 0;
  var dCol     = function(v){ return v === null ? '#64748b' : v >= 0 ? '#34d399' : '#ef4444'; };
  var dSign    = function(v){ return v === null ? '—' : (v >= 0 ? '+' : '') + v.toFixed(1) + '%'; };
  var maxFy26  = Math.max.apply(null, rows.map(function(r){ return r.fy26; })) || 1;

  // ── KPI strip topo ──
  var kpiHtml =
    '<div style="display:grid;grid-template-columns:repeat(5,1fr);gap:1px;background:rgba(255,255,255,0.04);border-radius:10px;overflow:hidden;margin-bottom:16px;">'
    +kpiCell('TOTAL PROVEDORES', rows.length + ' ativos', '≥ '+ _yoyMinPDVs +' PDV·meses FY25 ou FY26', '#94a3b8')
    +kpiCell('FY25 Jul→Mar', totFy25.toLocaleString('pt-BR'), 'PDV·meses consolidado (9 meses)', '#3b82f6')
    +kpiCell('FY26 Jul→Mar', totFy26.toLocaleString('pt-BR'), 'PDV·meses Jul/25→Mar/26', '#22c55e')
    +kpiCell('VARIAÇÃO YoY', dSign(totDelta), 'FY26 vs FY25 mesmo período', dCol(totDelta))
    +kpiCell('OPORT. CIMED+RB', totOpp.toLocaleString('pt-BR') + ' · ' + totAtend + '% conv.', 'Deduplicado nacional · Reconquistados: ' + totReconq.toLocaleString('pt-BR'), '#f97316')
    +'</div>';

  function kpiCell(lbl, val, sub, col){
    return '<div style="background:#0d1117;padding:12px 16px;">'
      +'<div style="font-size:8px;font-weight:700;letter-spacing:0.08em;color:#475569;margin-bottom:4px;">'+lbl+'</div>'
      +'<div style="font-size:18px;font-weight:800;color:'+col+';line-height:1;">'+val+'</div>'
      +'<div style="font-size:8px;color:#334155;margin-top:3px;">'+sub+'</div>'
      +'</div>';
  }

  // ── Header tabela ──
  var tableHtml = '<div style="overflow-x:auto;">'
    +'<table style="width:100%;border-collapse:collapse;font-size:10px;">'
    +'<thead>'
    +'<tr style="border-bottom:1px solid rgba(255,255,255,0.06);">'
      +'<th style="padding:8px 6px;text-align:left;color:#475569;font-weight:700;font-size:8px;letter-spacing:0.06em;white-space:nowrap;">#</th>'
      +'<th style="padding:8px 6px;text-align:left;color:#475569;font-weight:700;font-size:8px;letter-spacing:0.06em;">PROVEDOR</th>'
      +'<th style="padding:8px 6px;text-align:right;color:#3b82f6;font-weight:700;font-size:8px;white-space:nowrap;">FY25<br>Jul→Mar</th>'
      +'<th style="padding:8px 6px;text-align:right;color:#22c55e;font-weight:700;font-size:8px;white-space:nowrap;">FY26<br>Jul→Mar</th>'
      +'<th style="padding:8px 6px;text-align:right;color:#fbbf24;font-weight:700;font-size:8px;white-space:nowrap;">Δ YoY</th>'
      +'<th style="padding:8px 6px;text-align:right;color:#94a3b8;font-weight:700;font-size:8px;white-space:nowrap;">Q1 25</th>'
      +'<th style="padding:8px 6px;text-align:right;color:#94a3b8;font-weight:700;font-size:8px;white-space:nowrap;">Q1 26</th>'
      +'<th style="padding:8px 6px;text-align:right;color:#94a3b8;font-weight:700;font-size:8px;white-space:nowrap;">Δ Q1</th>'
      +'<th style="padding:8px 6px;text-align:right;color:#a78bfa;font-weight:700;font-size:8px;white-space:nowrap;">CIMED<br>+RB</th>'
      +'<th style="padding:8px 6px;text-align:right;color:#34d399;font-weight:700;font-size:8px;white-space:nowrap;">Reconq.</th>'
      +'<th style="padding:8px 6px;text-align:right;color:#f97316;font-weight:700;font-size:8px;white-space:nowrap;">% Conv.</th>'
      +'<th style="padding:8px 6px;font-weight:700;font-size:8px;color:#94a3b8;white-space:nowrap;">Trend FY26</th>'
    +'</tr>'
    +'</thead>'
    +'<tbody>';

  visible.forEach(function(r, idx){
    var rank = idx + 1;
    var dc  = dCol(r.delta);
    var qdc = dCol(r.q1_delta);
    var isTop3 = rank <= 3 && _yoySortKey === 'delta' && r.delta > 0;
    var isBad  = r.delta !== null && r.delta < -15;
    var rowBg  = isTop3 ? 'background:rgba(52,211,153,0.04);' : isBad ? 'background:rgba(239,68,68,0.03);' : '';
    var rankIcon = rank === 1 ? '🥇' : rank === 2 ? '🥈' : rank === 3 ? '🥉' : rank;

    // Spark bar para Trend FY26 (9 meses)
    var M = [];
    for(var i=0;i<PROV_DATA.length;i++){
      if(PROV_DATA[i].name === r.name){ M = PROV_DATA[i].monthly || []; break; }
    }
    var sparkVals = [];
    for(var i=15;i<=23;i++) sparkVals.push(M[i]||0);
    var smx = Math.max.apply(null, sparkVals) || 1;
    var spark = '<div style="display:flex;align-items:flex-end;gap:1px;height:20px;width:80px;">';
    sparkVals.forEach(function(v){
      var h = Math.max(1, Math.round(v/smx*18));
      var c = v > smx*0.7 ? '#34d399' : v > smx*0.4 ? '#fbbf24' : '#94a3b8';
      spark += '<div style="flex:1;height:'+h+'px;background:'+c+';border-radius:1px;opacity:0.8;"></div>';
    });
    spark += '</div>';

    var atendCol = r.atend >= 50 ? '#34d399' : r.atend >= 25 ? '#fbbf24' : '#ef4444';

    tableHtml +=
      '<tr style="border-bottom:0.5px solid rgba(255,255,255,0.04);'+rowBg+'">'
      +'<td style="padding:7px 6px;color:#475569;font-size:9px;font-weight:700;text-align:center;">'+rankIcon+'</td>'
      +'<td style="padding:7px 6px;font-size:10px;font-weight:600;color:#D1D5DB;max-width:160px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">'+r.name+'</td>'
      +'<td style="padding:7px 6px;text-align:right;color:#3b82f6;font-size:10px;">'+r.fy25.toLocaleString('pt-BR')+'</td>'
      +'<td style="padding:7px 6px;text-align:right;color:#22c55e;font-size:10px;font-weight:600;">'+r.fy26.toLocaleString('pt-BR')+'</td>'
      +'<td style="padding:7px 6px;text-align:right;font-size:11px;font-weight:800;color:'+dc+';">'+dSign(r.delta)+'</td>'
      +'<td style="padding:7px 6px;text-align:right;color:#64748b;font-size:9px;">'+r.q1_25.toLocaleString('pt-BR')+'</td>'
      +'<td style="padding:7px 6px;text-align:right;color:#94a3b8;font-size:9px;font-weight:600;">'+r.q1_26.toLocaleString('pt-BR')+'</td>'
      +'<td style="padding:7px 6px;text-align:right;font-size:10px;font-weight:700;color:'+qdc+';">'+dSign(r.q1_delta)+'</td>'
      +'<td style="padding:7px 6px;text-align:right;color:#a78bfa;font-size:10px;font-weight:600;">'+(r.opp > 0 ? r.opp.toLocaleString('pt-BR') : '<span style="color:#1e293b">—</span>')+'</td>'
      +'<td style="padding:7px 6px;text-align:right;color:#34d399;font-size:10px;">'+(r.reconq > 0 ? r.reconq.toLocaleString('pt-BR') : '<span style="color:#1e293b">—</span>')+'</td>'
      +'<td style="padding:7px 6px;text-align:right;font-size:10px;font-weight:700;color:'+atendCol+';">'+(r.opp > 0 ? r.atend+'%' : '<span style="color:#1e293b">—</span>')+'</td>'
      +'<td style="padding:7px 6px;">'+spark+'</td>'
      +'</tr>';
  });

  // Linha de total
  tableHtml +=
    '<tr style="border-top:1px solid rgba(251,191,36,0.2);background:rgba(251,191,36,0.03);">'
    +'<td style="padding:8px 6px;"></td>'
    +'<td style="padding:8px 6px;font-size:10px;font-weight:800;color:#fbbf24;">TOTAL</td>'
    +'<td style="padding:8px 6px;text-align:right;color:#3b82f6;font-weight:700;font-size:10px;">'+totFy25.toLocaleString('pt-BR')+'</td>'
    +'<td style="padding:8px 6px;text-align:right;color:#22c55e;font-weight:700;font-size:10px;">'+totFy26.toLocaleString('pt-BR')+'</td>'
    +'<td style="padding:8px 6px;text-align:right;font-size:11px;font-weight:800;color:'+dCol(totDelta)+';">'+dSign(totDelta)+'</td>'
    +'<td style="padding:8px 6px;text-align:right;color:#64748b;font-size:9px;">'+totQ1_25.toLocaleString('pt-BR')+'</td>'
    +'<td style="padding:8px 6px;text-align:right;color:#94a3b8;font-size:9px;font-weight:700;">'+totQ1_26.toLocaleString('pt-BR')+'</td>'
    +'<td style="padding:8px 6px;text-align:right;font-size:10px;font-weight:800;color:'+dCol(totQ1D)+';">'+dSign(totQ1D)+'</td>'
    +'<td style="padding:8px 6px;text-align:right;color:#a78bfa;font-weight:700;font-size:10px;">'+totOpp.toLocaleString('pt-BR')+'</td>'
    +'<td style="padding:8px 6px;text-align:right;color:#34d399;font-weight:700;font-size:10px;">'+totReconq.toLocaleString('pt-BR')+'</td>'
    +'<td style="padding:8px 6px;text-align:right;font-size:10px;font-weight:800;color:#f97316;">'+totAtend+'%</td>'
    +'<td></td>'
    +'</tr>';

  tableHtml += '</tbody></table></div>';

  // Botão ver todos
  var btnAll = '<div style="text-align:center;margin-top:10px;">'
    +'<button onclick="toggleYoYAll(this)" style="font-size:10px;padding:6px 18px;border-radius:8px;border:0.5px solid rgba(255,255,255,0.1);background:transparent;color:#64748b;cursor:pointer;">'
    +(_yoyShowAll ? 'Ver Top 20' : 'Ver todos (' + rows.length + ')')
    +'</button></div>';

  bodyEl.innerHTML = kpiHtml + tableHtml + btnAll;
}
"""

ANCHOR_JS = '\nfunction initSellin(){'
if ANCHOR_JS not in html:
    print("ERRO: anchor JS nao encontrado!")
    exit(1)
html = html.replace(ANCHOR_JS, NEW_JS + ANCHOR_JS, 1)
print("JS renderProvYoYCard() inserido")

# ══════════════════════════════════════════════════════════════
# 2. HTML — Card antes do FILTRO GRUPO PROVEDOR
# ══════════════════════════════════════════════════════════════

CARD_HTML = """
    <!-- EVOLUÇÃO YoY POR PROVEDOR -->
    <div id="prov-yoy-card" class="card full" style="margin-bottom:18px;">
      <div class="card-header" style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:12px;margin-bottom:16px;">
        <div>
          <div style="font-size:10px;font-weight:700;letter-spacing:0.1em;color:#22c55e;margin-bottom:4px;">📈 EVOLUÇÃO ANUAL — TODOS OS PROVEDORES</div>
          <div class="card-title">Positivação FY25 vs FY26 por Provedor · Jul→Mar (9 meses)</div>
          <div class="card-sub">PDV·meses acumulados Jul/24→Mar/25 vs Jul/25→Mar/26 · CIMED + RB consolidado · ordenável</div>
        </div>
        <div style="display:flex;gap:6px;flex-wrap:wrap;align-items:center;">
          <span style="font-size:9px;color:#475569;font-weight:700;text-transform:uppercase;letter-spacing:0.06em;">Ordenar por:</span>
          <button class="yoy-sort-btn" onclick="setYoYSort('delta',this)"
            style="font-size:10px;font-weight:700;padding:4px 12px;border-radius:6px;border:0.5px solid rgba(251,191,36,0.3);cursor:pointer;background:rgba(251,191,36,0.15);color:#fbbf24;">
            Δ% Positivação
          </button>
          <button class="yoy-sort-btn" onclick="setYoYSort('opp',this)"
            style="font-size:10px;font-weight:700;padding:4px 12px;border-radius:6px;border:0.5px solid rgba(255,255,255,0.07);cursor:pointer;background:transparent;color:#64748b;">
            Oportunidades
          </button>
          <button class="yoy-sort-btn" onclick="setYoYSort('reconq',this)"
            style="font-size:10px;font-weight:700;padding:4px 12px;border-radius:6px;border:0.5px solid rgba(255,255,255,0.07);cursor:pointer;background:transparent;color:#64748b;">
            % Reconquista
          </button>
        </div>
      </div>
      <div id="prov-yoy-body">
        <div style="text-align:center;padding:40px;color:#334155;font-size:12px;">Carregando...</div>
      </div>
    </div>

"""

ANCHOR_HTML = '    <!-- FILTRO GRUPO PROVEDOR -->'
if ANCHOR_HTML not in html:
    print("ERRO: anchor HTML nao encontrado!")
    exit(1)
html = html.replace(ANCHOR_HTML, CARD_HTML + ANCHOR_HTML, 1)
print("Card HTML inserido antes do filtro provedor")

# ══════════════════════════════════════════════════════════════
# 3. Inicializar renderProvYoYCard() no initCobertura()
# ══════════════════════════════════════════════════════════════

ANCHOR_INIT = 'if(typeof renderGCCard'
if ANCHOR_INIT not in html:
    # fallback: append to initCobertura
    print("AVISO: initCobertura anchor nao encontrado — buscando alternativa")
    ANCHOR_INIT2 = 'if(typeof renderGCHPositiv'
    if ANCHOR_INIT2 in html:
        html = html.replace(ANCHOR_INIT2,
            'if(typeof renderProvYoYCard==="function") setTimeout(renderProvYoYCard, 300);\n  ' + ANCHOR_INIT2, 1)
        print("renderProvYoYCard() wired ao initCobertura via fallback")
else:
    html = html.replace(ANCHOR_INIT,
        'if(typeof renderProvYoYCard==="function") setTimeout(renderProvYoYCard, 300);\n  ' + ANCHOR_INIT, 1)
    print("renderProvYoYCard() wired ao initCobertura")

# ══════════════════════════════════════════════════════════════
# 4. SALVAR
# ══════════════════════════════════════════════════════════════
ts = datetime.now().strftime('%Y%m%d_%H%M')
versao = VER / f"Dashboard_Farma_Sul_{ts}_ProvYoY.html"
shutil.copy(DASH, versao)
print(f"\nVersao salva: {versao.name}")

DASH.write_text(html, encoding='utf-8')
print(f"Dashboard: {len(html):,} chars (era {orig_len:,})")

dl = DL / f"Dashboard_FarmaSul_Giovano_{ts}.html"
shutil.copy(DASH, dl)
print(f"Downloads: {dl.name}")
print("\nDONE.")
