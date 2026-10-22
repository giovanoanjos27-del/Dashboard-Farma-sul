import re

src = r'C:\Users\valqu\OneDrive\Documentos\Claude\Projects\projeto Dashboard_farma_sul\Dashboard_farma_sul\Dashboard_Farma_Sul_20260512_2220.html'
with open(src, encoding='utf-8') as f:
    content = f.read()
    lines = content.splitlines()

# Find all occurrences of dynamic canvas ID patterns
print('=== Functions using dynamic canvas IDs ===')

patterns = [
    ("+ '-tend-chart'", r"\+\s*['\"][\-]tend[\-]chart['\"]"),
    ('+ "-tend-chart"', r'\+\s*"[\-]tend[\-]chart"'),
    ("+ '-line'", r"\+\s*['\"][\-]line['\"]"),
    ('+ "-line"', r'\+\s*"[\-]line"'),
    ("+ '-ano-chart'", r"\+\s*['\"][\-]ano[\-]chart['\"]"),
]

for label, pat in patterns:
    for m in re.finditer(pat, content):
        # Find line number
        ln = content[:m.start()].count('\n') + 1
        snippet = content[max(0, m.start()-80):m.end()+40].replace('\n',' ')
        print(f'  [{label}] L{ln}: ...{snippet}...')
        print()

# Find the enclosing function for each hit
print()
print('=== Enclosing functions for dynamic patterns ===')
combined_pat = r"\+\s*['\"][\-](tend[\-]chart|line|ano[\-]chart)['\"]"
for m in re.finditer(combined_pat, content):
    pos = m.start()
    # Walk backward to find function declaration
    chunk = content[:pos]
    fn_matches = list(re.finditer(r'function\s+(\w+)\s*\(', chunk))
    if fn_matches:
        fn_name = fn_matches[-1].group(1)
        fn_decl_line = chunk.count('\n') - chunk[:fn_matches[-1].start()].count('\n') + 1
        fn_line = fn_matches[-1].start()
        fn_decl_line = content[:fn_matches[-1].start()].count('\n') + 1
        ln = content[:pos].count('\n') + 1
        pattern_text = m.group(0)
        print(f'  L{ln} [{pattern_text.strip()}] inside function: {fn_name} (declared L{fn_decl_line})')

# Also check renderWSCrossover - what does it target?
print()
print('=== renderWSCrossover body (first 600 chars) ===')
m = re.search(r'function\s+renderWSCrossover\s*\(', content)
if m:
    start = m.end()
    depth = 1; pos = start
    while pos < len(content) and depth:
        if content[pos] == '{': depth += 1
        elif content[pos] == '}': depth -= 1
        pos += 1
    body = content[start:pos-1]
    canvas_refs = re.findall(r"getElementById\([\"']([\w-]+)[\"']\)", body)
    calls = len(re.findall(r'(?<!\w)renderWSCrossover\s*\(', content)) - 1
    print(f'  calls: {calls}')
    print(f'  canvas refs: {canvas_refs}')
    print(f'  body[:600]: {body[:600]}')
