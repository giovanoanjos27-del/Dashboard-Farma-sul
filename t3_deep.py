import re

src = r'C:\Users\valqu\OneDrive\Documentos\Claude\Projects\projeto Dashboard_farma_sul\Dashboard_farma_sul\Dashboard_Farma_Sul_20260512_2220.html'
with open(src, encoding='utf-8') as f:
    content = f.read()

# Check for dynamic ID patterns
print('=== Dynamic canvas ID patterns ===')
patterns = [
    r"[+]\s*['\"][\-]?tend[\-]chart['\"]",
    r"[+]\s*['\"][\-]?ano[\-]chart['\"]",
    r"[+]\s*['\"][\-]line['\"]",
]
for p in patterns:
    hits = re.findall(p, content)
    if hits:
        print(f'  Pattern [{p}]: {hits[:5]}')
    else:
        print(f'  Pattern [{p}]: NONE')

# Check renderXxxTend functions
print()
print('=== Tend render functions declared ===')
for m in re.finditer(r'function\s+(render\w*[Tt]end\w*)\s*\(', content):
    fn = m.group(1)
    calls = len(re.findall(r'(?<!\w)' + re.escape(fn) + r'\s*\(', content)) - 1
    start = m.end()
    depth = 1; pos = start
    while pos < len(content) and depth:
        if content[pos] == '{': depth += 1
        elif content[pos] == '}': depth -= 1
        pos += 1
    body = content[start:pos-1]
    canvas_refs = re.findall(r"getElementById\([\"']([\w-]+)[\"']\)", body)
    print(f'  {fn} (calls:{calls}) -> canvases: {canvas_refs}')

# Check renderWSGaucha actual function name
print()
print('=== renderWS functions ===')
for m in re.finditer(r'function\s+(renderWS\w+)\s*\(', content):
    print(f'  {repr(m.group(1))}')

# Check renderAnoBars family
print()
print('=== renderXxxAnoBars functions ===')
for m in re.finditer(r'function\s+(render\w+AnoBars)\s*\(', content):
    fn = m.group(1)
    calls = len(re.findall(r'(?<!\w)' + re.escape(fn) + r'\s*\(', content)) - 1
    print(f'  {fn} (calls:{calls})')

# Check renderXxxLine functions
print()
print('=== renderXxxLine functions ===')
for m in re.finditer(r'function\s+(render\w+Line)\s*\(', content):
    fn = m.group(1)
    calls = len(re.findall(r'(?<!\w)' + re.escape(fn) + r'\s*\(', content)) - 1
    print(f'  {fn} (calls:{calls})')
