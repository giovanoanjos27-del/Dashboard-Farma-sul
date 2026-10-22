import re, shutil, sys, os
sys.stdout.reconfigure(encoding='utf-8')

BASE = r'C:\Users\valqu\OneDrive\Documentos\Claude\Projects\projeto Dashboard_farma_sul'
SRC  = BASE + r'\Dashboard_farma_sul\Dashboard_Farma_Sul_20260512_2220.html'
BKP  = BASE + r'\Dashboard_farma_sul\versoes\Dashboard_Farma_Sul_20260513_1100_PreT8.html'
OUT  = BASE + r'\Dashboard_farma_sul\versoes\Dashboard_Farma_Sul_20260513_1105_T8.html'

shutil.copy2(SRC, BKP)
print(f'Backup: {os.path.basename(BKP)}')

with open(SRC, encoding='utf-8') as f:
    content = f.read()

orig_lines = len(content.splitlines())
c = content
changes = 0

# ── helper ──────────────────────────────────────────────────────────────────
def patch(label, old, new, src):
    if old not in src:
        print(f'  MISS  {label}')
        return src, False
    n = src.replace(old, new, 1)
    print(f'  OK    {label}')
    return n, True

# ════════════════════════════════════════════════════════════════════════════
# renderAnoChart — 4 surgical edits
# ════════════════════════════════════════════════════════════════════════════
print('\n=== renderAnoChart ===')

# 1. Remove the old destroy + replace function opening
c, ok = patch('remove destroy + maxVal',
    'function renderAnoChart(canvasId, anos, vals, isVol, colors){\n'
    '  var existing = _anoCharts[canvasId];\n'
    '  if(existing) existing.destroy();\n'
    '  var canvas = document.getElementById(canvasId);\n'
    '  if(!canvas) return;',
    'function renderAnoChart(canvasId, anos, vals, isVol, colors){\n'
    '  var canvas = document.getElementById(canvasId);\n'
    '  if(!canvas) return;',
    c)
if not ok: sys.exit(1)
changes += 1

# 2. Extract fmt + add helpers BEFORE the new Chart call
# Target: the blank line + fmt closing brace + blank line + _anoCharts line
# Use regex to handle trailing whitespace on blank lines
m = re.search(
    r"(    return v\.toLocaleString\('pt-BR'\) \+ ' un';\n  }\n)"
    r"\s*"
    r"  _anoCharts\[canvasId\] = new Chart\(canvas, \{",
    c
)
if not m:
    print('  MISS  fmt-to-newChart bridge')
    sys.exit(1)

replacement = (
    "    return v.toLocaleString('pt-BR') + ' un';\n"
    "  }\n\n"
    "  var bgColors = colors || ['rgba(59,130,246,0.75)','rgba(45,212,191,0.75)','rgba(52,211,153,0.75)'];\n"
    "  var bdColors = colors ? colors.map(function(c){return c.replace('0.75','1');})\n"
    "                       : ['#3b82f6','#2dd4bf','#34d399'];\n\n"
    "  function yTickCb(v){\n"
    "    if(!isVol){\n"
    "      if(v >= 1e6) return 'R$ '+(v/1e6).toFixed(1)+'M';\n"
    "      if(v >= 1e3) return 'R$ '+(v/1e3).toFixed(0)+'K';\n"
    "      return 'R$ '+v;\n"
    "    }\n"
    "    if(v >= 1e6) return (v/1e6).toFixed(1)+'M un';\n"
    "    if(v >= 1e3) return (v/1e3).toFixed(0)+'K un';\n"
    "    return v+' un';\n"
    "  }\n\n"
    "  function onCompleteCb(anim){\n"
    "    var chart = anim.chart;\n"
    "    var ctx2 = chart.ctx;\n"
    "    ctx2.save();\n"
    "    ctx2.font = 'bold 12px Inter, sans-serif';\n"
    "    ctx2.textAlign = 'center';\n"
    "    ctx2.textBaseline = 'bottom';\n"
    "    chart.data.datasets.forEach(function(dataset, i){\n"
    "      var meta = chart.getDatasetMeta(i);\n"
    "      meta.data.forEach(function(bar, j){\n"
    "        var val = dataset.data[j];\n"
    "        if(val == null) return;\n"
    "        var colors2 = ['#3b82f6','#2dd4bf','#34d399'];\n"
    "        ctx2.fillStyle = (dataset.borderColor && dataset.borderColor[j]) || colors2[j] || '#ffffff';\n"
    "        ctx2.fillText(fmt(val), bar.x, bar.y - 4);\n"
    "      });\n"
    "    });\n"
    "    ctx2.restore();\n"
    "  }\n\n"
    "  // ── T8: update-or-create (skip destroy on re-renders) ────────────────\n"
    "  var existing = _anoCharts[canvasId];\n"
    "  if(existing){\n"
    "    existing.data.labels                              = anos;\n"
    "    existing.data.datasets[0].data                   = vals;\n"
    "    existing.data.datasets[0].backgroundColor        = bgColors;\n"
    "    existing.data.datasets[0].borderColor            = bdColors;\n"
    "    existing.options.scales.y.ticks.callback         = yTickCb;\n"
    "    existing.options.plugins.tooltip.callbacks.label = function(ctx){ return '  '+fmt(ctx.raw); };\n"
    "    existing.options.animation.onComplete            = onCompleteCb;\n"
    "    existing.update();\n"
    "    return;\n"
    "  }\n\n"
    "  _anoCharts[canvasId] = new Chart(canvas, {"
)
c = c[:m.start()] + replacement + c[m.end():]
print('  OK    fmt-to-newChart bridge + update block')
changes += 1

# 3. Replace the hardcoded colors in the new Chart data section
# Use regex to handle potential trailing spaces
m3 = re.search(
    r"        backgroundColor: colors \|\| \['rgba\(59,130,246,0\.75\)','rgba\(45,212,191,0\.75\)','rgba\(52,211,153,0\.75\)'\],\n"
    r"        borderColor:     colors \? colors\.map\(function\(c\)\{return c\.replace\('0\.75','1'\);\}\) *\n"
    r"                               : \['#3b82f6','#2dd4bf','#34d399'\],",
    c
)
if m3:
    c = c[:m3.start()] + "        backgroundColor: bgColors,\n        borderColor:     bdColors," + c[m3.end():]
    print('  OK    replace hardcoded bgColors in dataset')
    changes += 1
else:
    print('  MISS  replace hardcoded bgColors in dataset')
    sys.exit(1)

# 4. Replace the inline y-axis callback with yTickCb reference (regex for robustness)
m4 = re.search(
    r"            callback: function\(v\) \{[^}]+if\(!isVol\)\{[^}]+\}[^}]+\}",
    c, re.DOTALL
)
if m4:
    c = c[:m4.start()] + "            callback: yTickCb" + c[m4.end():]
    print('  OK    replace inline yAxis callback with yTickCb')
    changes += 1
else:
    print('  MISS  replace inline yAxis callback with yTickCb')
    sys.exit(1)

# 5. Replace the inline onComplete with onCompleteCb reference (regex for robustness)
m5 = re.search(
    r"        onComplete: function\(anim\) \{.*?ctx2\.restore\(\);\s*\}",
    c, re.DOTALL
)
if m5:
    c = c[:m5.start()] + "        onComplete: onCompleteCb" + c[m5.end():]
    print('  OK    replace inline onComplete with onCompleteCb')
    changes += 1
else:
    print('  MISS  replace inline onComplete with onCompleteCb')
    sys.exit(1)

# Also remove the now-orphaned var maxVal line (no longer needed)
c, ok = patch('remove orphan maxVal line',
    "  var GC = 'rgba(255,255,255,0.09)', TC = '#4a6b65';\n"
    "  var maxVal = Math.max.apply(null, vals.filter(function(v){return v!=null;}));",
    "  var GC = 'rgba(255,255,255,0.09)', TC = '#4a6b65';",
    c)
# Not critical if it misses — just keep it
changes += 1

# ════════════════════════════════════════════════════════════════════════════
# renderLineChart — 2 surgical edits
# ════════════════════════════════════════════════════════════════════════════
print('\n=== renderLineChart ===')

# 1. Remove destroy call
c, ok = patch('remove destroy',
    "  var existing = Chart.getChart(ctx);\n"
    "  if(existing) existing.destroy();\n",
    "  var existing = Chart.getChart(ctx);\n",
    c)
if not ok: sys.exit(1)
changes += 1

# 2. Insert update block before `  var chart = new Chart(ctx, {`
# This string is unique in the file (renderAnoChart uses `_anoCharts[canvasId] = new Chart`)
c, ok = patch('insert update block before new Chart',
    "  var chart = new Chart(ctx, {",
    "  // ── T8: update-or-create ────────────────────────────────────────────\n"
    "  if(existing){\n"
    "    existing.data.datasets = builtDatasets;\n"
    "    existing.options.scales.y.ticks.callback = function(v){ return yFmt(v); };\n"
    "    existing.options.plugins.tooltip.callbacks.label = function(c){\n"
    "      if(c.raw == null) return null;\n"
    "      return ' '+c.dataset.label+': '+ttFmt(c.raw);\n"
    "    };\n"
    "    existing.update('none');\n"
    "    if(legendId){\n"
    "      var lgU = document.getElementById(legendId);\n"
    "      if(lgU) lgU.innerHTML = datasets.map(function(d){\n"
    "        var col = COLORS[d.label] || '#D1D5DB';\n"
    "        var is26 = d.label==='2026'||d.label==='2026*';\n"
    "        return '<span style=\"display:flex;align-items:center;gap:5px;font-size:10px;font-weight:'+(is26?'700':'500')+';color:'+(is26?col:'#D1D5DB')+';\">'"\
    "\n        + '<span style=\"width:'+(is26?'20':'14')+'px;height:'+(is26?'3':'2')+'px;background:'+col+';display:inline-block;border-radius:2px;'+(d.dashed?'background:repeating-linear-gradient(90deg,'+col+' 0px,'+col+' 4px,transparent 4px,transparent 8px);':'')+'\"></span>'"\
    "\n        + d.label + '</span>';\n"
    "      }).join('');\n"
    "    }\n"
    "    return;\n"
    "  }\n\n"
    "  var chart = new Chart(ctx, {",
    c)
if not ok: sys.exit(1)
changes += 1

# ── Write ────────────────────────────────────────────────────────────────────
with open(OUT, 'w', encoding='utf-8') as f:
    f.write(c)

# Copy OUT to main active file
shutil.copy2(OUT, SRC)
print(f'\n  Copied to active file: {os.path.basename(SRC)}')

new_lines = len(c.splitlines())
delta = new_lines - orig_lines
print(f'\nLinhas: {orig_lines} → {new_lines} ({delta:+d})')
print(f'Total patches: {changes}')
print(f'Versão: {os.path.basename(OUT)}')

# ── Verify ───────────────────────────────────────────────────────────────────
print()
checks = [
    ('renderAnoChart update() path',    'existing.update();\n    return;\n  }\n\n  _anoCharts[canvasId]'),
    ('renderLineChart update(none)',     "existing.update('none');"),
    ('onCompleteCb ref in new Chart',    'onComplete: onCompleteCb'),
    ('yTickCb ref in new Chart',         'callback: yTickCb'),
    ('renderAnoChart destroy GONE',      'if(existing) existing.destroy();\n  var canvas'),
    ('renderLineChart destroy GONE',     'if(existing) existing.destroy();\n\n  var yFmt'),
]
for label, needle in checks:
    if label.endswith('GONE'):
        found = needle in c
        print(f"  {'FAIL' if found else 'OK  '}  {label}")
    else:
        found = needle in c
        print(f"  {'OK  ' if found else 'FAIL'}  {label}")
