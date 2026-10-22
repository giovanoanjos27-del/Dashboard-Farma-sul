import re, sys
sys.stdout.reconfigure(encoding='utf-8')

src = r'C:\Users\valqu\OneDrive\Documentos\Claude\Projects\projeto Dashboard_farma_sul\Dashboard_farma_sul\Dashboard_Farma_Sul_20260512_2220.html'
with open(src, encoding='utf-8') as f:
    content = f.read()

def get_fn_body(fname):
    m = re.search(r'function\s+' + re.escape(fname) + r'\s*\([^)]*\)\s*\{', content)
    if not m:
        return None, None
    start = m.end()
    depth = 1; pos = start
    while pos < len(content) and depth:
        if content[pos] == '{': depth += 1
        elif content[pos] == '}': depth -= 1
        pos += 1
    return content[start:pos-1], content.count('\n', 0, m.start()) + 1

# Check renderWSGAM body - how does it access canvas?
print('=== renderWSGAM canvas access ===')
body, ln = get_fn_body('renderWSGAM')
if body:
    # Find canvas/getElementById patterns
    for pat in [r'getElementById\([^)]+\)', r'new Chart\([^,]+', r'getContext']:
        for m in re.finditer(pat, body):
            print(f'  {m.group(0)[:80]}')

print()

# Check renderAnoChart - does it call getElementById(canvasId) with a variable?
print('=== renderAnoChart internals ===')
body2, ln2 = get_fn_body('renderAnoChart')
if body2:
    print(f'  Declared at L{ln2}')
    print(f'  First 400 chars: {body2[:400]}')

print()

# Check renderLineChart
print('=== renderLineChart internals ===')
body3, ln3 = get_fn_body('renderLineChart')
if body3:
    print(f'  Declared at L{ln3}')
    print(f'  First 400 chars: {body3[:400]}')

print()

# Now the key question: for each "dead" function, how many calls does it have
# and where are those calls?
dead_fns = [
    'renderCLAnoBars','renderCompSCJ','renderGAMAnoBars','renderGAMLine',
    'renderGCHAnoBars','renderGCHLine','renderNSAnoBars','renderNSLine',
    'renderPVAnoBars','renderPVLine','renderRioAnoBars','renderSJAnoBars',
    'renderSJCAnoBars','renderSJCLine','renderSJLine','renderTopCidades',
    'renderWSConsolidado','renderWSGAM','renderWSGaucha'
]

# Also try unicode variant
lines_content = content.splitlines()

print('=== Call sites for "dead" functions ===')
for fn in dead_fns:
    # Find all call sites (not declaration)
    fn_decl = re.search(r'function\s+' + re.escape(fn) + r'\s*\(', content)
    decl_ln = content.count('\n', 0, fn_decl.start()) + 1 if fn_decl else '?'

    # Find calls
    call_sites = []
    for m in re.finditer(r'(?<!\w)' + re.escape(fn) + r'\s*\(', content):
        call_ln = content.count('\n', 0, m.start()) + 1
        if fn_decl and abs(call_ln - decl_ln) > 2:
            # Not the declaration itself
            snippet = content[max(0,m.start()-40):m.end()+20].replace('\n',' ')
            call_sites.append(f'L{call_ln}: ...{snippet}...')

    print(f'\n  {fn} (decl:L{decl_ln}, {len(call_sites)} external calls):')
    for cs in call_sites:
        print(f'    {cs}')
