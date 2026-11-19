import re, sys
sys.stdout.reconfigure(encoding='utf-8')

src = r'C:\Users\valqu\OneDrive\Documentos\Claude\Projects\projeto Dashboard_farma_sul\Dashboard_farma_sul\Dashboard_Farma_Sul_20260512_2220.html'
with open(src, encoding='utf-8') as f:
    content = f.read()

# Build position->line number index
newlines = [i for i, c in enumerate(content) if c == '\n']
def pos_to_line(pos):
    import bisect
    return bisect.bisect_left(newlines, pos) + 1

# Find all function declarations
fns = {}
for m in re.finditer(r'function\s+(\w+)\s*\(', content):
    name = m.group(1)
    if name not in fns:
        fns[name] = m.start()

# Count all occurrences of each function name
zero_call = []
one_call = []
for name, decl_pos in fns.items():
    # Quick count via findall
    pattern = r'(?<!\w)' + re.escape(name) + r'(?!\w)'
    hits = len(re.findall(pattern, content))
    # Subtract declaration(s) — typically 1
    # Any occurrence = declaration or call
    decl_count = len(re.findall(r'function\s+' + re.escape(name) + r'\s*\(', content))
    external = hits - decl_count
    if external == 0:
        ln = pos_to_line(decl_pos)
        zero_call.append((ln, name))
    elif external == 1:
        ln = pos_to_line(decl_pos)
        one_call.append((ln, name))

print(f'Total functions declared: {len(fns)}')
print(f'Zero external calls: {len(zero_call)}')
print(f'One external call: {len(one_call)}')
print()

print('=== ZERO external calls (likely dead) ===')
for ln, name in sorted(zero_call):
    print(f'  L{ln:6d}  {name}')

print()
print('=== ONE external call (review) ===')
for ln, name in sorted(one_call):
    print(f'  L{ln:6d}  {name}')
