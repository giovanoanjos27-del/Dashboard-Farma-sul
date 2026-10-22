import re
from collections import defaultdict

src = r'C:\Users\valqu\OneDrive\Documentos\Claude\Projects\projeto Dashboard_farma_sul\Dashboard_farma_sul\Dashboard_Farma_Sul_20260512_2220.html'
with open(src, encoding='utf-8') as f:
    content = f.read()
    lines   = content.splitlines()

# ── 1. All canvas IDs in HTML ────────────────────────────────────────────────
canvas_ids = {}
for i, ln in enumerate(lines):
    for cid in re.findall(r'<canvas[^>]+id=["\'](\w[\w-]*)["\']', ln):
        canvas_ids[cid] = i+1

# ── 2. All getElementById calls ──────────────────────────────────────────────
getelems = set(re.findall(r"getElementById\(['\"](\w[\w-]*)['\"]", content))

# ── 3. Canvas IDs never fetched by JS ────────────────────────────────────────
dead_canvas = {cid: ln for cid, ln in canvas_ids.items() if cid not in getelems}
live_canvas = {cid: ln for cid, ln in canvas_ids.items() if cid in getelems}

print(f'Total canvas: {len(canvas_ids)}')
print(f'Live (getElementById): {len(live_canvas)}')
print(f'Dead (never fetched): {len(dead_canvas)}')
print()
print('DEAD CANVAS IDs:')
for cid, ln in sorted(dead_canvas.items(), key=lambda x: x[1]):
    print(f'  L{ln:5d}  #{cid}')

# ── 4. Find render functions that target dead canvas IDs ─────────────────────
print()
print('RENDER FUNCTIONS targeting dead canvas:')
fn_bodies = {}
fn_pat = re.compile(r'function\s+(\w+)\s*\([^)]*\)\s*\{')
for m in fn_pat.finditer(content):
    name = m.group(1)
    start = m.end()
    depth = 1; pos = start
    while pos < len(content) and depth:
        if content[pos] == '{': depth += 1
        elif content[pos] == '}': depth -= 1
        pos += 1
    body = content[start:pos-1]
    fn_bodies[name] = body

dead_fns = {}
for fn_name, body in fn_bodies.items():
    for cid in dead_canvas:
        if f"'{cid}'" in body or f'"{cid}"' in body:
            dead_fns[fn_name] = cid
            break

for fn, cid in sorted(dead_fns.items()):
    # How many times is this fn called?
    calls = len(re.findall(r'(?<!\w)' + re.escape(fn) + r'\s*\(', content)) - 1
    decl_line = next((i+1 for i, ln in enumerate(lines)
                      if re.search(r'function\s+' + re.escape(fn) + r'\s*\(', ln)), '?')
    print(f'  L{str(decl_line):5s}  {fn:40s}  canvas:#{cid}  calls:{calls}')

# ── 5. Dead canvas HTML lines ─────────────────────────────────────────────────
print()
print('DEAD CANVAS HTML (line numbers):')
for cid, ln in sorted(dead_canvas.items(), key=lambda x: x[1]):
    print(f'  L{ln:5d}  <canvas id="{cid}">')
