"""
patch_acumulado_fy.py
Insere card "EVOLUÇÃO ACUMULADA FY25 vs FY26" no panel-sellout.
Posicionamento: entre o filtro de cliente e os content divs dos clientes
(sempre visível, independente do cliente selecionado).

Dados usados (todos os 7 clientes SO):
  SJ_REC / SJ_UNID · NS.total.rec / NS.total.vol
  CL_REC_* / CL_VOL_* · PV_REC / PV_VOL
  GAM_REC / GAM_VOL · GAUCHA_REC / GAUCHA_VOL
  RIOMED_REC_* / RIOMED_VOL_*

FY25 = Jul/2024→Jun/2025 | FY26 = Jul/2025→Jun/2026
Meses futuros (null) exibidos como linha tracejada + transparência.
"""
import sys
from pathlib import Path
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

BASE = Path(r'C:\Users\valqu\OneDrive\Documentos\Claude\Projects\projeto Dashboard_farma_sul\Dashboard_farma_sul')
SRC  = BASE / 'Dashboard_Farma_Sul_20260512_2220.html'
VER  = BASE / 'versoes' / f'Dashboard_Farma_Sul_{datetime.now().strftime("%Y%m%d_%H%M")}_AcumuladoFY.html'

print('Lendo dashboard…')
h = SRC.read_text(encoding='utf-8')
orig_len = len(h)

# ─────────────────────────────────────────────────────────────────────────────
# Âncora: justo antes do primeiro content div de cliente
# ─────────────────────────────────────────────────────────────────────────────
ANCHOR = '  <!-- Conteúdos dinâmicos por cliente -->\n  <div id="sellout-content-saojoao" class="sellout-client-content" style="display: none;">'
assert h.count(ANCHOR) == 1, f'Âncora não encontrada ({h.count(ANCHOR)}×)'

CARD = r"""  <!-- ════════════ CARD EVOLUÇÃO ACUMULADA FY25 vs FY26 ════════════ -->
  <div id="card-acumulado-fy" class="card full" style="margin-bottom:16px;">
    <div class="card-header">
      <div>
        <div class="card-title">📈 EVOLUÇÃO ACUMULADA FY25 vs FY26</div>
        <div class="card-sub" id="acum-sub">Faturamento Acumulado · Jul/24–Jun/25 vs Jul/25–Jun/26 · Todos os Clientes Sell Out</div>
      </div>
      <div style="display:flex;align-items:center;gap:14px;">
        <div class="toggle-group">
          <button class="tgl active blue" id="acum-btn-rec" onclick="setAcumMode('rec',this)">R$</button>
          <button class="tgl" id="acum-btn-vol" onclick="setAcumMode('vol',this)">Un.</button>
        </div>
        <div style="display:flex;gap:14px;align-items:center;">
          <span style="display:flex;align-items:center;gap:5px;font-size:11px;font-weight:700;color:#60a5fa;">
            <span style="width:18px;height:2.5px;background:#3b82f6;display:inline-block;border-radius:2px;"></span>FY25
          </span>
          <span style="display:flex;align-items:center;gap:5px;font-size:11px;font-weight:700;color:#34d399;">
            <span style="width:18px;height:2.5px;background:#34d399;display:inline-block;border-radius:2px;"></span>FY26
          </span>
          <span style="display:flex;align-items:center;gap:5px;font-size:10px;color:#64748B;">
            <span style="width:20px;height:2.5px;display:inline-block;border-radius:2px;background:repeating-linear-gradient(90deg,#64748B 0,#64748B 4px,transparent 4px,transparent 8px);"></span>Projetado
          </span>
        </div>
      </div>
    </div>

    <!-- KPI chips -->
    <div id="acum-kpi-strip" style="display:grid;grid-template-columns:repeat(3,1fr);gap:10px;padding:14px 0 16px;"></div>

    <!-- Gráfico principal: acumulado -->
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;">
      <div>
        <div style="font-size:9px;font-weight:700;letter-spacing:.12em;color:#3d6b63;text-transform:uppercase;margin-bottom:8px;">💰 Faturamento Acumulado (R$)</div>
        <div style="position:relative;height:240px;"><canvas id="acum-rec-canvas"></canvas></div>
      </div>
      <div>
        <div style="font-size:9px;font-weight:700;letter-spacing:.12em;color:#3d6b63;text-transform:uppercase;margin-bottom:8px;">📦 Unidades Acumuladas</div>
        <div style="position:relative;height:240px;"><canvas id="acum-vol-canvas"></canvas></div>
      </div>
    </div>

    <!-- Diagnóstico automático -->
    <div id="acum-diag" style="margin-top:14px;padding:12px 16px;background:rgba(255,255,255,0.03);border-radius:8px;border-left:3px solid rgba(59,130,246,0.4);font-size:11px;color:#D1D5DB;line-height:1.7;"></div>
  </div>

  <script>
  (function(){
    /* ── Modo ativo ─────────────────────────────────────────────────── */
    var _acumMode   = 'rec';
    var _acumChartR = null;
    var _acumChartV = null;
    var _acumReady  = false;

    window.setAcumMode = function(mode, btn){
      _acumMode = mode;
      ['acum-btn-rec','acum-btn-vol'].forEach(function(id){
        var b = document.getElementById(id);
        if(!b) return;
        var on = (id === 'acum-btn-'+mode);
        if(on) b.classList.add('active'); else b.classList.remove('active');
        b.style.color      = on ? '#fbbf24' : '#D1D5DB';
        b.style.background = on ? 'rgba(251,191,36,0.12)' : '#161B22';
        b.style.fontWeight = on ? '700' : '600';
      });
      var sub = document.getElementById('acum-sub');
      if(sub) sub.textContent = mode === 'rec'
        ? 'Faturamento Acumulado · Jul/24–Jun/25 vs Jul/25–Jun/26 · Todos os Clientes Sell Out'
        : 'Unidades Acumuladas · Jul/24–Jun/25 vs Jul/25–Jun/26 · Todos os Clientes Sell Out';
    };

    /* ── Formatar valores ────────────────────────────────────────────── */
    function _fmtR(v){
      if(!v) return 'R$ 0';
      if(v >= 1e6) return 'R$ '+( v/1e6).toFixed(1)+'M';
      if(v >= 1e3) return 'R$ '+(v/1e3).toFixed(0)+'K';
      return 'R$ '+v.toFixed(0);
    }
    function _fmtU(v){
      if(!v) return '0';
      if(v >= 1e6) return (v/1e6).toFixed(1)+'M';
      if(v >= 1e3) return (v/1e3).toFixed(0)+'K';
      return v.toFixed(0);
    }
    function _fmtAxis(v, isRec){
      if(isRec){
        if(v >= 1e6) return 'R$'+(v/1e6).toFixed(0)+'M';
        if(v >= 1e3) return 'R$'+(v/1e3).toFixed(0)+'K';
        return 'R$'+v;
      } else {
        if(v >= 1e6) return (v/1e6).toFixed(1)+'M';
        if(v >= 1e3) return (v/1e3).toFixed(0)+'K';
        return v+'';
      }
    }
    function _pct(a,b){ return a>0 ? ((b-a)/a*100).toFixed(1) : '—'; }

    /* ── Extrair serie FY de um array mensal ─────────────────────────── */
    /* arr24[0..11]=Jan-Dez/24, arr25[0..11]=Jan-Dez/25, arr26[0..11]=Jan-Dez/26 */
    /* FY25 = Jul/24[idx6..11] + Jan/25[idx0..5] */
    /* FY26 = Jul/25[idx6..11] + Jan/26[idx0..5] */
    function _fy(arr24, arr25, arr26){
      var fy25 = [], fy26 = [];
      for(var i=6;i<12;i++) fy25.push((arr24 && arr24[i] != null) ? +arr24[i] : 0);
      for(var i=0;i<6;i++) fy25.push((arr25 && arr25[i] != null) ? +arr25[i] : 0);
      for(var i=6;i<12;i++) fy26.push((arr25 && arr25[i] != null) ? +arr25[i] : 0);
      for(var i=0;i<6;i++) fy26.push((arr26 && arr26[i] != null) ? +arr26[i] : null);
      return { fy25:fy25, fy26:fy26 };
    }

    /* ── Somar todos os clientes ─────────────────────────────────────── */
    function _buildTotals(){
      var totRec25 = new Array(12).fill(0);
      var totRec26 = new Array(12).fill(null);
      var totVol25 = new Array(12).fill(0);
      var totVol26 = new Array(12).fill(null);

      function _addSeries(fySer, tgt25, tgt26){
        for(var i=0;i<12;i++){
          if(fySer.fy25[i] != null) tgt25[i] = (tgt25[i]||0) + fySer.fy25[i];
          if(fySer.fy26[i] != null) tgt26[i] = (tgt26[i]||0) + fySer.fy26[i];
        }
      }

      /* São João */
      if(typeof SJ_REC !== 'undefined')
        _addSeries(_fy(SJ_REC['2024'],SJ_REC['2025'],SJ_REC['2026']), totRec25, totRec26);
      if(typeof SJ_UNID !== 'undefined')
        _addSeries(_fy(SJ_UNID['2024'],SJ_UNID['2025'],SJ_UNID['2026']), totVol25, totVol26);

      /* Nissei */
      if(typeof NS !== 'undefined' && NS.total){
        _addSeries(_fy(NS.total.rec['2024'],NS.total.rec['2025'],NS.total.rec['2026']), totRec25, totRec26);
        _addSeries(_fy(NS.total.vol['2024'],NS.total.vol['2025'],NS.total.vol['2026']), totVol25, totVol26);
      }

      /* Clamed */
      if(typeof CL_REC_2024 !== 'undefined'){
        _addSeries(_fy(CL_REC_2024,CL_REC_2025,CL_REC_2026), totRec25, totRec26);
        _addSeries(_fy(CL_VOL_2024,CL_VOL_2025,CL_VOL_2026), totVol25, totVol26);
      }

      /* Panvel */
      if(typeof PV_REC !== 'undefined'){
        _addSeries(_fy(PV_REC['2024'],PV_REC['2025'],PV_REC['2026']), totRec25, totRec26);
        _addSeries(_fy(PV_VOL['2024'],PV_VOL['2025'],PV_VOL['2026']), totVol25, totVol26);
      }

      /* DD-GAM */
      if(typeof GAM_REC !== 'undefined'){
        _addSeries(_fy(GAM_REC['2024'],GAM_REC['2025'],GAM_REC['2026']), totRec25, totRec26);
        _addSeries(_fy(GAM_VOL['2024'],GAM_VOL['2025'],GAM_VOL['2026']), totVol25, totVol26);
      }

      /* DD-Gaúcha */
      if(typeof GAUCHA_REC !== 'undefined'){
        _addSeries(_fy(GAUCHA_REC['2024'],GAUCHA_REC['2025'],GAUCHA_REC['2026']), totRec25, totRec26);
        _addSeries(_fy(GAUCHA_VOL['2024'],GAUCHA_VOL['2025'],GAUCHA_VOL['2026']), totVol25, totVol26);
      }

      /* DD-Riomed */
      if(typeof RIOMED_REC_2024 !== 'undefined'){
        _addSeries(_fy(RIOMED_REC_2024,RIOMED_REC_2025,RIOMED_REC_2026), totRec25, totRec26);
        _addSeries(_fy(RIOMED_VOL_2024,RIOMED_VOL_2025,RIOMED_VOL_2026), totVol25, totVol26);
      }

      return { rec25:totRec25, rec26:totRec26, vol25:totVol25, vol26:totVol26 };
    }

    /* ── Calcular cumulativo ─────────────────────────────────────────── */
    function _cum(arr){
      var result = [], sum = 0, lastVal = null;
      for(var i=0;i<arr.length;i++){
        if(arr[i] != null && arr[i] > 0){
          sum += arr[i];
          lastVal = sum;
          result.push(sum);
        } else if(arr[i] === null){
          result.push(null); /* quebra a linha — meses futuros */
        } else {
          result.push(sum || null);
        }
      }
      return result;
    }

    /* Projeção: preenche null após último valor com valor flat (linha tracejada) */
    function _cumProjected(arr){
      var result = [], sum = 0;
      for(var i=0;i<arr.length;i++){
        if(arr[i] != null && arr[i] > 0) sum += arr[i];
        result.push(sum > 0 ? sum : null);
      }
      return result;
    }

    /* ── Criar gradiente de área ─────────────────────────────────────── */
    function _grad(ctx, ca, col){
      if(!ca) return col+'44';
      try {
        var g = ctx.createLinearGradient(0, ca.top, 0, ca.bottom);
        g.addColorStop(0, col+'66');
        g.addColorStop(1, col+'08');
        return g;
      } catch(e){ return col+'44'; }
    }

    /* ── Render principal ────────────────────────────────────────────── */
    window.renderAcumuladoFY = function(){
      if(typeof Chart === 'undefined') return;

      var totals  = _buildTotals();
      var FY_LBL  = ['Jul','Ago','Set','Out','Nov','Dez','Jan','Fev','Mar','Abr','Mai','Jun'];
      var GC = 'rgba(255,255,255,0.07)';
      var TC = '#4a6b65';

      /* Cumulativos */
      var cumRec25 = _cum(totals.rec25);
      var cumRec26 = _cum(totals.rec26);
      var cumRec26P= _cumProjected(totals.rec26);
      var cumVol25 = _cum(totals.vol25);
      var cumVol26 = _cum(totals.vol26);
      var cumVol26P= _cumProjected(totals.vol26);

      /* Totais para KPIs */
      var sumRec25 = totals.rec25.reduce(function(s,v){return s+(v||0);},0);
      var sumRec26 = totals.rec26.reduce(function(s,v){return s+(v||0);},0);
      var sumVol25 = totals.vol25.reduce(function(s,v){return s+(v||0);},0);
      var sumVol26 = totals.vol26.reduce(function(s,v){return s+(v||0);},0);
      var dRec = _pct(sumRec25, sumRec26);
      var dVol = _pct(sumVol25, sumVol26);

      /* ── KPI strip ─────────────────────────────────────────────────── */
      var kpiEl = document.getElementById('acum-kpi-strip');
      if(kpiEl){
        function _kpiHtml(label, val25, val26, delta, isRec, accentColor){
          var dNum = parseFloat(delta);
          var dCol = isNaN(dNum) ? '#94A3B8' : (dNum>=0?'#34d399':'#ef4444');
          var dStr = isNaN(dNum) ? '—' : (dNum>=0?'▲ +':' ▼ ')+Math.abs(dNum).toFixed(1)+'%';
          return '<div style="background:#161B22;border-radius:10px;padding:12px 14px;border-top:2px solid '+accentColor+';">'
            +'<div style="font-size:9px;font-weight:700;letter-spacing:.1em;color:#3d6b63;margin-bottom:5px;text-transform:uppercase;">'+label+'</div>'
            +'<div style="font-size:9px;color:#475569;margin-bottom:2px;">FY25: <span style="color:#64748B;font-weight:600;">'+val25+'</span></div>'
            +'<div style="display:flex;align-items:baseline;gap:8px;">'
              +'<span style="font-size:18px;font-weight:800;color:'+accentColor+';line-height:1;">'+val26+'</span>'
              +'<span style="font-size:11px;font-weight:700;color:'+dCol+';">'+dStr+'</span>'
            +'</div>'
            +'<div style="font-size:9px;color:#475569;margin-top:3px;">FY26 YTD vs FY25</div>'
          +'</div>';
        }
        kpiEl.innerHTML =
          _kpiHtml('💰 Faturamento FY25', _fmtR(sumRec25), '—', '—', true, '#3b82f6') +
          _kpiHtml('💰 Faturamento FY26 YTD', _fmtR(sumRec25), _fmtR(sumRec26), dRec, true, '#34d399') +
          _kpiHtml('📦 Unidades FY26 YTD', _fmtU(sumVol25), _fmtU(sumVol26), dVol, false, '#2dd4bf');

        /* re-render com valores corretos */
        kpiEl.innerHTML =
          _kpiHtml('💰 Fat. FY25 Completo',    _fmtR(sumRec25), _fmtR(sumRec25), '0', true,  '#3b82f6') +
          _kpiHtml('💰 Fat. FY26 YTD',         _fmtR(sumRec25), _fmtR(sumRec26), dRec, true, '#34d399') +
          _kpiHtml('📦 Un. FY26 YTD',          _fmtU(sumVol25), _fmtU(sumVol26), dVol, false,'#2dd4bf');

        /* Simplificado e correto */
        function _dStr(num){
          var n = parseFloat(num);
          if(isNaN(n)) return '<span style="color:#64748B;">—</span>';
          var col = n>=0?'#34d399':'#ef4444';
          return '<span style="color:'+col+';font-weight:700;">'+(n>=0?'▲ +':'▼ ')+Math.abs(n).toFixed(1)+'%</span>';
        }
        kpiEl.innerHTML = [
          {lbl:'💰 Faturamento FY25',  v25:_fmtR(sumRec25), v26:'—', d:'—',  ac:'#3b82f6'},
          {lbl:'💰 Faturamento FY26 YTD', v25:_fmtR(sumRec25), v26:_fmtR(sumRec26), d:dRec, ac:'#34d399'},
          {lbl:'📦 Unidades FY26 YTD',  v25:_fmtU(sumVol25), v26:_fmtU(sumVol26), d:dVol, ac:'#2dd4bf'},
        ].map(function(k){
          return '<div style="background:#161B22;border-radius:10px;padding:12px 14px;border-top:2px solid '+k.ac+';">'
            +'<div style="font-size:8px;font-weight:700;letter-spacing:.1em;color:#3d6b63;margin-bottom:6px;text-transform:uppercase;">'+k.lbl+'</div>'
            +(k.v25 !== '—' ? '<div style="font-size:9px;color:#475569;margin-bottom:2px;">FY25: <span style="color:#64748B;font-weight:600;">'+k.v25+'</span></div>' : '')
            +'<div style="display:flex;align-items:baseline;gap:8px;">'
              +'<span style="font-size:18px;font-weight:800;color:'+k.ac+';line-height:1;">'+(k.v26!=='—'?k.v26:k.v25)+'</span>'
              +_dStr(k.d)
            +'</div>'
          +'</div>';
        }).join('');
      }

      /* ── Helper para criar/atualizar chart ───────────────────────────── */
      function _makeChart(canvasId, cum25, cum26, cum26Proj, chartRef, isRec){
        var canvas = document.getElementById(canvasId);
        if(!canvas) return chartRef;
        if(chartRef){ try{ chartRef.destroy(); }catch(e){} }

        var co = {
          backgroundColor:'#0a1a18', titleColor:'#e2e8f0', bodyColor:'#D1D5DB',
          borderColor:'rgba(255,255,255,0.13)', borderWidth:1, padding:10,
          callbacks:{
            title: function(items){ return FY_LBL[items[0].dataIndex] + (isRec?' (Acumulado)':('' )); },
            label: function(item){
              var val = item.raw;
              if(val == null) return item.dataset.label+': —';
              return item.dataset.label+': '+(isRec ? _fmtR(val) : _fmtU(val));
            },
            afterBody: function(items){
              var idx = items[0] ? items[0].dataIndex : -1;
              if(idx < 0) return [];
              var v25 = cum25[idx], v26 = cum26Proj[idx];
              if(v25 && v26 && v25>0){
                var diff = v26-v25, pct = (diff/v25*100).toFixed(1);
                var sym = diff>=0?'+':'';
                return ['─────────────────','Δ vs FY25: '+sym+pct+'%  ('+sym+(isRec?_fmtR(Math.abs(diff)):_fmtU(Math.abs(diff)))+')'];
              }
              return [];
            }
          }
        };

        return new Chart(canvas.getContext('2d'), {
          type: 'line',
          data: {
            labels: FY_LBL,
            datasets: [
              {
                label: 'FY25',
                data: cum25,
                borderColor: '#3b82f6',
                backgroundColor: function(ctx){
                  var ca = ctx.chart.chartArea;
                  return _grad(ctx.chart.ctx, ca, '#3b82f6');
                },
                pointBackgroundColor: '#3b82f6',
                pointBorderColor: '#0D1117',
                pointBorderWidth: 1.5,
                pointRadius: 3,
                pointHoverRadius: 6,
                borderWidth: 2.5,
                tension: 0.4,
                fill: true,
                spanGaps: false
              },
              {
                label: 'FY26',
                data: cum26,
                borderColor: '#34d399',
                backgroundColor: function(ctx){
                  var ca = ctx.chart.chartArea;
                  return _grad(ctx.chart.ctx, ca, '#34d399');
                },
                pointBackgroundColor: '#34d399',
                pointBorderColor: '#0D1117',
                pointBorderWidth: 1.5,
                pointRadius: 3,
                pointHoverRadius: 6,
                borderWidth: 2.5,
                tension: 0.4,
                fill: true,
                spanGaps: false
              },
              {
                label: 'FY26 (proj.)',
                data: cum26Proj,
                borderColor: '#34d39966',
                borderDash: [5,4],
                backgroundColor: 'transparent',
                pointBackgroundColor: '#34d39966',
                pointBorderColor: 'transparent',
                pointRadius: 2,
                pointHoverRadius: 4,
                borderWidth: 1.5,
                tension: 0.4,
                fill: false,
                spanGaps: true
              }
            ]
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            interaction: { mode: 'index', intersect: false },
            plugins: {
              legend: {
                display: false
              },
              tooltip: { backgroundColor:'#0a1a18', titleColor:'#e2e8f0', bodyColor:'#D1D5DB',
                borderColor:'rgba(255,255,255,0.13)', borderWidth:1, padding:10, callbacks: co.callbacks }
            },
            scales: {
              x: { grid:{ color:GC }, ticks:{ color:TC, font:{size:9} } },
              y: {
                grid:{ color:GC },
                ticks:{
                  color:TC,
                  font:{size:9},
                  callback: function(v){ return _fmtAxis(v, isRec); }
                },
                min: 0
              }
            }
          }
        });
      }

      /* ── Renderizar os dois gráficos ──────────────────────────────── */
      _acumChartR = _makeChart('acum-rec-canvas', cumRec25, cumRec26, cumRec26P, _acumChartR, true);
      _acumChartV = _makeChart('acum-vol-canvas', cumVol25, cumVol26, cumVol26P, _acumChartV, false);

      /* ── Diagnóstico automático ────────────────────────────────────── */
      var diagEl = document.getElementById('acum-diag');
      if(diagEl){
        var dRecN = parseFloat(dRec), dVolN = parseFloat(dVol);
        var dRecCol = isNaN(dRecN)?'#94A3B8':(dRecN>=0?'#34d399':'#ef4444');
        var dVolCol = isNaN(dVolN)?'#94A3B8':(dVolN>=0?'#34d399':'#ef4444');
        var dRecSign = (!isNaN(dRecN)&&dRecN>=0)?'▲ +':'▼ ';
        var dVolSign = (!isNaN(dVolN)&&dVolN>=0)?'▲ +':'▼ ';

        /* Mês com maior crescimento vs FY25 */
        var bestMonth = '—', bestGrowth = -Infinity;
        for(var i=0;i<12;i++){
          if(totals.rec25[i]>0 && totals.rec26[i]!=null){
            var g = (totals.rec26[i]-totals.rec25[i])/totals.rec25[i]*100;
            if(g>bestGrowth){ bestGrowth=g; bestMonth=FY_LBL[i]; }
          }
        }
        var bestCol = bestGrowth>=0?'#34d399':'#ef4444';
        var bestStr = bestGrowth!=-Infinity ? (bestGrowth>=0?'+':'')+bestGrowth.toFixed(1)+'%' : '—';

        /* Número de meses com dados em FY26 */
        var mesesFY26 = totals.rec26.filter(function(v){return v!=null&&v>0;}).length;

        diagEl.innerHTML = '<strong style="color:#fbbf24;font-size:10px;letter-spacing:.08em;">📊 DIAGNÓSTICO ACUMULADO FY25 vs FY26 — SELL OUT TOTAL</strong><br>'
          +'💰 <strong>Faturamento FY26 YTD</strong> ('+mesesFY26+' meses acumulados): <strong style="color:'+dRecCol+';">'+_fmtR(sumRec26)+'</strong>'
          +' vs FY25 <strong style="color:#94A3B8;">'+_fmtR(sumRec25)+'</strong>'
          +' — <span style="color:'+dRecCol+';font-weight:700;">'+dRecSign+Math.abs(dRecN).toFixed(1)+'%</span><br>'
          +'📦 <strong>Unidades FY26 YTD</strong>: <strong style="color:'+dVolCol+';">'+_fmtU(sumVol26)+'</strong>'
          +' vs FY25 <strong style="color:#94A3B8;">'+_fmtU(sumVol25)+'</strong>'
          +' — <span style="color:'+dVolCol+';font-weight:700;">'+dVolSign+Math.abs(dVolN).toFixed(1)+'%</span><br>'
          +(bestMonth!=='—' ? '📈 <strong>Melhor mês FY26</strong>: <strong style="color:'+bestCol+';">'+bestMonth+'</strong> com <span style="color:'+bestCol+';">'+bestStr+'</span> vs FY25<br>' : '')
          +'<span style="font-size:9px;color:#475569;">Período FY25: Jul/24–Jun/25 · FY26 YTD: Jul/25–Abr/26 (meses projetados em tracejado) · Fonte: Todos os clientes Sell Out</span>';
      }

      _acumReady = true;
    };

    /* ── Aguardar Chart.js e dados estarem disponíveis ─────────────── */
    var _acumAttempts = 0;
    function _acumInit(){
      _acumAttempts++;
      if(_acumAttempts > 60) return; /* timeout 6s */
      if(typeof Chart === 'undefined' || typeof SJ_REC === 'undefined'){
        setTimeout(_acumInit, 100);
        return;
      }
      window.renderAcumuladoFY();
    }
    setTimeout(_acumInit, 200);

  })();
  </script>

"""

h = h.replace(ANCHOR, CARD + ANCHOR, 1)
print('✅ Card Evolução Acumulada inserido antes de sellout-content-saojoao')

# ─────────────────────────────────────────────────────────────────────────────
# Verificações
# ─────────────────────────────────────────────────────────────────────────────
assert 'card-acumulado-fy' in h,        '❌ card id não encontrado'
assert 'renderAcumuladoFY' in h,        '❌ função não encontrada'
assert 'acum-rec-canvas' in h,          '❌ canvas R$ não encontrado'
assert 'acum-vol-canvas' in h,          '❌ canvas Un não encontrado'
assert 'acum-kpi-strip' in h,           '❌ KPI strip não encontrado'
assert 'acum-diag' in h,                '❌ diagnóstico não encontrado'
assert '_fy(' in h,                     '❌ helper _fy não encontrado'
assert h.count('card-acumulado-fy') == 1, '❌ card duplicado'
print('✅ Verificações OK')

print(f'\nTamanho original: {orig_len:,} | Novo: {len(h):,} | Δ: {len(h)-orig_len:+,}')

VER.parent.mkdir(parents=True, exist_ok=True)
VER.write_text(h, encoding='utf-8')
print(f'✅ Versão salva: {VER.name}')
SRC.write_text(h, encoding='utf-8')
print(f'✅ Base ativa atualizada: {SRC.name}')
print('DONE.')
