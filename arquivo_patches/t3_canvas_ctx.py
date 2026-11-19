import re, sys
sys.stdout.reconfigure(encoding='utf-8')

src = r'C:\Users\valqu\OneDrive\Documentos\Claude\Projects\projeto Dashboard_farma_sul\Dashboard_farma_sul\Dashboard_Farma_Sul_20260512_2220.html'
with open(src, encoding='utf-8') as f:
    lines = f.readlines()

targets = ['sjc-line','sjc-ano-chart','sj-line','sj-ano-chart','ns-line','ns-ano-chart',
           'cl-ano-chart','pv-line','pv-ano-chart','gam-line','gam-ano-chart',
           'gch-line','gch-ano-chart','rio-ano-chart',
           'ws-gam-bar','ws-gaucha-bar','iqvia-nac-bar-opp','cons-topcid',
           'cons-comp-bar','cons-ws-bar']

for i, ln in enumerate(lines):
    for t in targets:
        if t in ln and 'canvas' in ln:
            # Show context: 2 lines before and after
            start = max(0, i-2)
            end = min(len(lines), i+3)
            print(f'--- L{i+1} ({t}) ---')
            for j in range(start, end):
                prefix = '>>>' if j == i else '   '
                print(f'{prefix} L{j+1}: {lines[j].rstrip()}')
            print()
