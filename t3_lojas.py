import re, sys
sys.stdout.reconfigure(encoding='utf-8')

src = r'C:\Users\valqu\OneDrive\Documentos\Claude\Projects\projeto Dashboard_farma_sul\Dashboard_farma_sul\Dashboard_Farma_Sul_20260512_2220.html'
with open(src, encoding='utf-8') as f:
    content = f.read()

# 1. Find ALL functions with truly 0 external calls
print('=== Functions with 0 external calls ===')
fn_pat = re.compile(r'function\s+(\w+)\s*\([^)]*\)\s*\{')
for m in fn_pat.finditer(content):
    name = m.group(1)
    decl_ln = content.count('\n', 0, m.start()) + 1
    # Count all calls (not just declaration)
    all_calls = list(re.finditer(r'(?<!\w)' + re.escape(name) + r'\s*\(', content))
    # Remove the declaration itself
    external_calls = [c for c in all_calls if abs(content.count('\n', 0, c.start()) + 1 - decl_ln) > 2]
    if len(external_calls) == 0:
        print(f'  L{decl_ln}  {name}')

print()

# 2. Check renderXxxLojas, renderXxxEstoqueLinha, renderXxxEstoqueTend variants
targets = ['Lojas','EstoqueLinha','EstoqueTend','Estoque']
print('=== Lojas/Estoque render functions ===')
for m in fn_pat.finditer(content):
    name = m.group(1)
    for t in targets:
        if t in name and 'render' in name.lower():
            decl_ln = content.count('\n', 0, m.start()) + 1
            all_calls = list(re.finditer(r'(?<!\w)' + re.escape(name) + r'\s*\(', content))
            external_calls = [c for c in all_calls if abs(content.count('\n', 0, c.start()) + 1 - decl_ln) > 2]
            print(f'  L{decl_ln}  {name}  (ext calls: {len(external_calls)})')
            break
