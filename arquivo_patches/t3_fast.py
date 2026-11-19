import re, sys
sys.stdout.reconfigure(encoding='utf-8')

src = r'C:\Users\valqu\OneDrive\Documentos\Claude\Projects\projeto Dashboard_farma_sul\Dashboard_farma_sul\Dashboard_Farma_Sul_20260512_2220.html'
with open(src, encoding='utf-8') as f:
    content = f.read()

# Fast approach: just grep for specific function names
target_fns = [
    'renderSJLojas','renderNSLojas','renderCLLojas','renderPVLojas',
    'renderGAMLojas','renderGCHLojas','renderRioLojas','renderSJCLojas',
    'renderNSEstoqueLinha','renderCLEstoqueLinha','renderPVEstoqueLinha',
    'renderGAMEstoqueLinha','renderGCHEstoqueLinha','renderRioEstoqueLinha',
    'renderSJEstoqueLinha','renderSJCEstoqueLinha',
    'renderNSEstoqueTend','renderCLEstoqueTend','renderPVEstoqueTend',
    'renderGAMEstoqueTend','renderGCHEstoqueTend','renderRioEstoqueTend',
    'renderSJEstoqueTend','renderSJCEstoqueTend',
]

print('=== Target function call counts ===')
for fn in target_fns:
    calls = len(re.findall(r'(?<!\w)' + re.escape(fn) + r'\s*\(', content))
    declared = 1 if re.search(r'function\s+' + re.escape(fn) + r'\s*\(', content) else 0
    ext = calls - declared
    if declared:
        print(f'  {fn}: declared=YES, ext_calls={ext}')
    else:
        print(f'  {fn}: NOT FOUND')

# Check for renderXxxLojas in any form
print()
print('=== All renderXxx functions with "Loja" or "loja" ===')
for m in re.finditer(r'function\s+(render\w*[Ll]oja\w*)\s*\(', content):
    fn = m.group(1)
    calls = len(re.findall(r'(?<!\w)' + re.escape(fn) + r'\s*\(', content))
    print(f'  {fn}: total={calls}, ext={calls-1}')

# Check what's at the estoque sections in HTML
print()
print('=== estoque-lojas HTML elements ===')
for m in re.finditer(r'id=["\']([^"\']*loja[^"\']*)["\']', content, re.IGNORECASE):
    lines_before = content.count('\n', 0, m.start()) + 1
    print(f'  L{lines_before}: {m.group(0)}')
