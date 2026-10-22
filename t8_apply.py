import re, shutil, sys, os
sys.stdout.reconfigure(encoding='utf-8')

BASE = r'C:\Users\valqu\OneDrive\Documentos\Claude\Projects\projeto Dashboard_farma_sul'
SRC  = BASE + r'\Dashboard_farma_sul\Dashboard_Farma_Sul_20260512_2220.html'
BKP  = BASE + r'\Dashboard_farma_sul\versoes\Dashboard_Farma_Sul_20260513_1100_PreT8.html'
OUT  = BASE + r'\Dashboard_farma_sul\versoes\Dashboard_Farma_Sul_20260513_1105_T8.html'

# ── backup ──────────────────────────────────────────────────────────────────
shutil.copy2(SRC, BKP)
print(f'Backup: {os.path.basename(BKP)}')

with open(SRC, encoding='utf-8') as f:
    content = f.read()

original_len = len(content.splitlines())

# ════════════════════════════════════════════════════════════════════════════
# PATCH 1 — renderAnoChart
# ════════════════════════════════════════════════════════════════════════════
OLD_ANO = r"""function renderAnoChart(canvasId, anos, vals, isVol, colors){
  var existing = _anoCharts[canvasId];
  if(existing) existing.destroy();
  var canvas = document.getElementById(canvasId);
  if(!canvas) return;

  var GC = 'rgba(255,255,255,0.09)', TC = '#4a6b65';
  var maxVal = Math.max.apply(null, vals.filter(function(v){return v!=null;}));

  // Format value for display
  function fmt(v){
    if(v == null) return '-';
    if(!isVol){
      if(v >= 1e6) return 'R$ ' + (v/1e6).toFixed(2) + 'M';
      if(v >= 1e3) return 'R$ ' + Math.round(v/1e3) + 'K';
      return 'R$ ' + v;
    }
    // Unidades: mostrar número completo com ponto separador
    return v.toLocaleString('pt-BR') + ' un';
  }

  _anoCharts[canvasId] = new Chart(canvas, {
    type: 'bar',
    data: {
      labels: anos,
      datasets: [{
        data: vals,
        backgroundColor: colors || ['rgba(59,130,246,0.75)','rgba(45,212,191,0.75)','rgba(52,211,153,0.75)'],
        borderColor:     colors ? colors.map(function(c){return c.replace('0.75','1');})
                               : ['#3b82f6','#2dd4bf','#34d399'],
        borderWidth: 2,
        borderRadius: 8,
        borderSkipped: false,
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        tooltip: {
          backgroundColor: '#0a1a18',
          titleColor: '#e2e8f0',
          bodyColor: '#D1D5DB',
          borderColor: 'rgba(255,255,255,0.13)',
          borderWidth: 1,
          padding: 12,
          callbacks: {
            label: function(ctx) { return '  ' + fmt(ctx.raw); }
          }
        },
        // Inline data labels on bars
        datalabels: undefined,
      },
      scales: {
        x: {
          grid: { display: false },
          ticks: { color: '#D1D5DB', font: { size: 12, weight: '600' } }
        },
        y: {
          grid: { color: GC },
          ticks: {
            color: TC,
            font: { size: 10 },
            callback: function(v) {
              if(!isVol){
                if(v >= 1e6) return 'R$ '+(v/1e6).toFixed(1)+'M';
                if(v >= 1e3) return 'R$ '+(v/1e3).toFixed(0)+'K';
                return 'R$ '+v;
              }
              if(v >= 1e6) return (v/1e6).toFixed(1)+'M un';
              if(v >= 1e3) return (v/1e3).toFixed(0)+'K un';
              return v+' un';
            }
          },
          beginAtZero: true
        }
      },
      animation: {
        duration: 900, easing: 'easeOutQuart',
        onComplete: function(anim) {
          // Draw value labels on top of bars
          var chart = anim.chart;
          var ctx2 = chart.ctx;
          ctx2.save();
          ctx2.font = 'bold 12px Inter, sans-serif';
          ctx2.textAlign = 'center';
          ctx2.textBaseline = 'bottom';
          chart.data.datasets.forEach(function(dataset, i) {
            var meta = chart.getDatasetMeta(i);
            meta.data.forEach(function(bar, j) {
              var val = dataset.data[j];
              if(val == null) return;
              var colors2 = ['#3b82f6','#2dd4bf','#34d399'];
              ctx2.fillStyle = (dataset.borderColor && dataset.borderColor[j]) || colors2[j] || '#ffffff';
              ctx2.fillText(fmt(val), bar.x, bar.y - 4);
            });
          });
          ctx2.restore();
        }
      }
    }
  });
}"""

NEW_ANO = r"""function renderAnoChart(canvasId, anos, vals, isVol, colors){
  var canvas = document.getElementById(canvasId);
  if(!canvas) return;

  var GC = 'rgba(255,255,255,0.09)', TC = '#4a6b65';

  function fmt(v){
    if(v == null) return '-';
    if(!isVol){
      if(v >= 1e6) return 'R$ ' + (v/1e6).toFixed(2) + 'M';
      if(v >= 1e3) return 'R$ ' + Math.round(v/1e3) + 'K';
      return 'R$ ' + v;
    }
    // Unidades: mostrar número completo com ponto separador
    return v.toLocaleString('pt-BR') + ' un';
  }

  var bgColors = colors || ['rgba(59,130,246,0.75)','rgba(45,212,191,0.75)','rgba(52,211,153,0.75)'];
  var bdColors = colors ? colors.map(function(c){return c.replace('0.75','1');})
                       : ['#3b82f6','#2dd4bf','#34d399'];

  function yTickCb(v){
    if(!isVol){
      if(v >= 1e6) return 'R$ '+(v/1e6).toFixed(1)+'M';
      if(v >= 1e3) return 'R$ '+(v/1e3).toFixed(0)+'K';
      return 'R$ '+v;
    }
    if(v >= 1e6) return (v/1e6).toFixed(1)+'M un';
    if(v >= 1e3) return (v/1e3).toFixed(0)+'K un';
    return v+' un';
  }

  function onCompleteCb(anim){
    // Draw value labels on top of bars
    var chart = anim.chart;
    var ctx2 = chart.ctx;
    ctx2.save();
    ctx2.font = 'bold 12px Inter, sans-serif';
    ctx2.textAlign = 'center';
    ctx2.textBaseline = 'bottom';
    chart.data.datasets.forEach(function(dataset, i){
      var meta = chart.getDatasetMeta(i);
      meta.data.forEach(function(bar, j){
        var val = dataset.data[j];
        if(val == null) return;
        var colors2 = ['#3b82f6','#2dd4bf','#34d399'];
        ctx2.fillStyle = (dataset.borderColor && dataset.borderColor[j]) || colors2[j] || '#ffffff';
        ctx2.fillText(fmt(val), bar.x, bar.y - 4);
      });
    });
    ctx2.restore();
  }

  // ── T8: update-or-create (skip destroy + new Chart on re-renders) ────────
  var existing = _anoCharts[canvasId];
  if(existing){
    existing.data.labels                              = anos;
    existing.data.datasets[0].data                   = vals;
    existing.data.datasets[0].backgroundColor        = bgColors;
    existing.data.datasets[0].borderColor            = bdColors;
    existing.options.scales.y.ticks.callback         = yTickCb;
    existing.options.plugins.tooltip.callbacks.label = function(ctx){ return '  '+fmt(ctx.raw); };
    existing.options.animation.onComplete            = onCompleteCb;
    existing.update();
    return;
  }

  _anoCharts[canvasId] = new Chart(canvas, {
    type: 'bar',
    data: {
      labels: anos,
      datasets: [{
        data: vals,
        backgroundColor: bgColors,
        borderColor:     bdColors,
        borderWidth: 2,
        borderRadius: 8,
        borderSkipped: false,
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        tooltip: {
          backgroundColor: '#0a1a18',
          titleColor: '#e2e8f0',
          bodyColor: '#D1D5DB',
          borderColor: 'rgba(255,255,255,0.13)',
          borderWidth: 1,
          padding: 12,
          callbacks: {
            label: function(ctx) { return '  ' + fmt(ctx.raw); }
          }
        },
        // Inline data labels on bars
        datalabels: undefined,
      },
      scales: {
        x: {
          grid: { display: false },
          ticks: { color: '#D1D5DB', font: { size: 12, weight: '600' } }
        },
        y: {
          grid: { color: GC },
          ticks: {
            color: TC,
            font: { size: 10 },
            callback: yTickCb
          },
          beginAtZero: true
        }
      },
      animation: {
        duration: 900, easing: 'easeOutQuart',
        onComplete: onCompleteCb
      }
    }
  });
}"""

# ════════════════════════════════════════════════════════════════════════════
# PATCH 2 — renderLineChart: remove destroy; add update-or-create before new Chart
# ════════════════════════════════════════════════════════════════════════════
OLD_LINE_DESTROY = "  var existing = Chart.getChart(ctx);\n  if(existing) existing.destroy();"
NEW_LINE_DESTROY = "  var existing = Chart.getChart(ctx);"

# The update block goes right before "  var chart = new Chart(ctx, {"
OLD_LINE_NEW = "  var chart = new Chart(ctx, {"
NEW_LINE_NEW = """\
  // ── T8: update-or-create (skip destroy + new Chart on re-renders) ────────
  if(existing){
    existing.data.datasets = builtDatasets;
    existing.options.scales.y.ticks.callback = function(v){ return yFmt(v); };
    existing.options.plugins.tooltip.callbacks.label = function(c){
      if(c.raw == null) return null;
      return ' '+c.dataset.label+': '+ttFmt(c.raw);
    };
    existing.update('none');
    if(legendId){
      var lgU = document.getElementById(legendId);
      if(lgU) lgU.innerHTML = datasets.map(function(d){
        var col = COLORS[d.label] || '#D1D5DB';
        var is26 = d.label==='2026'||d.label==='2026*';
        return '<span style="display:flex;align-items:center;gap:5px;font-size:10px;font-weight:'+(is26?'700':'500')+';color:'+(is26?col:'#D1D5DB')+';">'
          + '<span style="width:'+(is26?'20':'14')+'px;height:'+(is26?'3':'2')+'px;background:'+col+';display:inline-block;border-radius:2px;'+(d.dashed?'background:repeating-linear-gradient(90deg,'+col+' 0px,'+col+' 4px,transparent 4px,transparent 8px);':'')+'"></span>'
          + d.label + '</span>';
      }).join('');
    }
    return;
  }

  var chart = new Chart(ctx, {\
"""

# ── Apply patches ────────────────────────────────────────────────────────────
c = content

# Patch 1
if OLD_ANO in c:
    c = c.replace(OLD_ANO, NEW_ANO, 1)
    print('PATCH 1 renderAnoChart: OK')
else:
    print('PATCH 1 renderAnoChart: NOT FOUND — check old_string')
    sys.exit(1)

# Patch 2a — remove destroy line
if OLD_LINE_DESTROY in c:
    c = c.replace(OLD_LINE_DESTROY, NEW_LINE_DESTROY, 1)
    print('PATCH 2a renderLineChart destroy: OK')
else:
    print('PATCH 2a renderLineChart destroy: NOT FOUND')
    sys.exit(1)

# Patch 2b — insert update block before new Chart in renderLineChart
# Must target only the one inside renderLineChart, not renderAnoChart
# renderLineChart's new Chart is: `  var chart = new Chart(ctx, {`
# renderAnoChart's is: `  _anoCharts[canvasId] = new Chart(canvas, {`
if OLD_LINE_NEW in c:
    c = c.replace(OLD_LINE_NEW, NEW_LINE_NEW, 1)
    print('PATCH 2b renderLineChart new Chart: OK')
else:
    print('PATCH 2b renderLineChart new Chart: NOT FOUND')
    sys.exit(1)

# ── Write output ─────────────────────────────────────────────────────────────
with open(OUT, 'w', encoding='utf-8') as f:
    f.write(c)

new_len = len(c.splitlines())
diff = new_len - original_len
print(f'\nLinhas: {original_len} → {new_len} ({diff:+d})')
print(f'Versão salva: {os.path.basename(OUT)}')

# ── Verify: confirm destroy is gone from renderAnoChart ──────────────────────
print()
if 'if(existing) existing.destroy();\n  var canvas = document.getElementById(canvasId);\n  if(!canvas) return;\n  \n  var GC' in c:
    print('WARN: old renderAnoChart destroy still present!')
else:
    print('OK: renderAnoChart destroy removed')

if "if(existing) existing.destroy();\n\n  var yFmt" in c:
    print('WARN: old renderLineChart destroy still present!')
else:
    print('OK: renderLineChart destroy removed')

# Confirm update paths exist
if 'existing.update();\n    return;\n  }\n\n  _anoCharts[canvasId] = new Chart' in c:
    print('OK: renderAnoChart update() path present')
else:
    print('WARN: renderAnoChart update() path not found')

if "existing.update('none');" in c:
    print('OK: renderLineChart update(none) path present')
else:
    print("WARN: renderLineChart update('none') not found")
