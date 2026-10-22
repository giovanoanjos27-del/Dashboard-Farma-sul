import sys, re
sys.stdout.reconfigure(encoding='utf-8')
path = r'C:\Users\valqu\OneDrive\Documentos\Claude\Projects\projeto Dashboard_farma_sul\Dashboard_farma_sul\Dashboard_Farma_Sul_20260512_2220.html'
with open(path,'r',encoding='utf-8') as f:
    html = f.read()

# Find the actual function definition (not just references)
pos = html.find('function renderMSOSkuJanMar')
print(f"function renderMSOSkuJanMar @ {pos}")
print(html[pos:pos+4000])
