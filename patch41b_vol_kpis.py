"""
PATCH 41b - Fix vol-kpis template + compradora-row border
"""
import datetime

SRC = r'Dashboard_farma_sul\Dashboard_Farma_Sul_20260512_2220.html'
html = open(SRC, encoding='utf-8').read()
orig = len(html)

fixes = 0

# Fix 1: vol-kpis card background + border-radius
old1 = (
    "      return '<div style=\"background:'+k.bg+';border-radius:10px;"
    "padding:12px 14px;border:1px solid '+k.bdr+';border-top-width:2px;\">'"
)
new1 = (
    "      return '<div style=\"background:#EAEEF4;border-radius:12px;"
    "padding:14px 16px;border-top:3px solid '+k.bdr+';"
    "border-left:1px solid rgba(147,187,235,0.5);"
    "border-right:1px solid rgba(147,187,235,0.5);"
    "border-bottom:1px solid rgba(147,187,235,0.5);"
    "box-shadow:0 2px 8px rgba(10,40,80,0.12);\">'"
)
if old1 in html:
    html = html.replace(old1, new1)
    fixes += 1
    print('  [OK] vol-kpis card template → #EAEEF4 + radius 12px')
else:
    print('  [MISS] vol-kpis card template')

# Fix 2: vol-kpis label color
old2 = (
    "        +'<div style=\"font-size:9px;font-weight:700;"
    "color:#94A3B8;letter-spacing:.08em;margin-bottom:4px;\">'+k.yr+'</div>'"
)
new2 = (
    "        +'<div style=\"font-size:9px;font-weight:700;"
    "color:#475569;letter-spacing:.08em;text-transform:uppercase;margin-bottom:4px;\">'+k.yr+'</div>'"
)
if old2 in html:
    html = html.replace(old2, new2)
    fixes += 1
    print('  [OK] vol-kpis label color #94A3B8 → #475569')
else:
    print('  [MISS] vol-kpis label color')

# Fix 3: compradora-row gold border
old3 = 'border-left:1px solid rgba(245,225,164,0.4)'
new3 = 'border-left:2px solid rgba(94,153,208,0.55)'
count3 = html.count(old3)
if count3 > 0:
    html = html.replace(old3, new3)
    fixes += 1
    print(f'  [OK] compradora-row gold border → azul ({count3}x)')
else:
    print('  [MISS] compradora-row border')

# Fix 4: sj-compradora-row border-color additional variant
old4 = 'border-left:1px solid rgba(245,225,164,0.'
if old4 in html:
    import re
    html = re.sub(
        r'border-left:1px solid rgba\(245,225,164,0\.\d+\)',
        'border-left:2px solid rgba(94,153,208,0.55)',
        html
    )
    fixes += 1
    print('  [OK] variant gold border → azul')

print(f'\nTotal: {fixes} fixes')
print('Diff: {:+,} bytes'.format(len(html) - orig))

ts = datetime.datetime.now().strftime('%Y%m%d_%H%M')
ver = f'Dashboard_farma_sul/versoes/Dashboard_Farma_Sul_{ts}_VolKpisFix.html'
open(SRC, 'w', encoding='utf-8').write(html)
open(ver, 'w', encoding='utf-8').write(html)
print('Salvo:', SRC)
print('Versao:', ver)
