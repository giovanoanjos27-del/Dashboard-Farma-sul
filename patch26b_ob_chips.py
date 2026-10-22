"""
PATCH 26b - OB KPI chips background + label color
Corrige os 3 templates JS (renderOBShare, renderOBPreco, renderOBVendas)
"""
import datetime

SRC = r'Dashboard_farma_sul\Dashboard_Farma_Sul_20260512_2220.html'
html = open(SRC, encoding='utf-8').read()
original_len = len(html)

OLD = (
    'ound:rgba(0,0,0,0.2);border-radius:8px;padding:10px 12px;border-top:1.5px solid \'+cor+\';">\'\n'
    '      +\'<div style="font-size:9px;font-weight:700;letter-spacing:0.08em;color:#3d6b63;margin-bottom:3px;">\''
)
NEW = (
    'ound:#FFFFFF;border-radius:8px;padding:10px 12px;border:1px solid #DCE3EC;border-top:2px solid \'+cor+\';">\'\n'
    '      +\'<div style="font-size:9px;font-weight:700;letter-spacing:0.08em;color:#334155;margin-bottom:3px;">\''
)

n = html.count(OLD)
print('Ocorrencias OLD:', n)

if n > 0:
    html = html.replace(OLD, NEW)
    print('[OK x{}] OB KPI chips bg->branco, label->#334155'.format(n))
else:
    print('[MISS] padrao nao encontrado')

# Tambem fix static HTML pre-renderizado (pos ~1374793)
OLD_STATIC = 'background:rgba(0,0,0,0.2);border-radius:8px;padding:10px 12px;border-top:1.5px solid #'
NEW_STATIC = 'background:#FFFFFF;border-radius:8px;padding:10px 12px;border:1px solid #DCE3EC;border-top:2px solid #'
n2 = html.count(OLD_STATIC)
if n2 > 0:
    html = html.replace(OLD_STATIC, NEW_STATIC)
    print('[OK x{}] OB static HTML chips bg->branco'.format(n2))

# Fix label color #3d6b63 -> #334155 nos chips (label dentro do chip)
OLD_LBL = 'font-size:9px;font-weight:700;letter-spacing:0.08em;color:#3d6b63;margin-bottom:3px;'
NEW_LBL = 'font-size:9px;font-weight:700;letter-spacing:0.08em;color:#334155;margin-bottom:3px;'
n3 = html.count(OLD_LBL)
if n3 > 0:
    html = html.replace(OLD_LBL, NEW_LBL)
    print('[OK x{}] OB chip label #3d6b63 -> #334155'.format(n3))

print('\nDiff: {:+,} bytes'.format(len(html) - original_len))

ts = datetime.datetime.now().strftime('%Y%m%d_%H%M')
ver = 'Dashboard_farma_sul/versoes/Dashboard_Farma_Sul_{}_OBChipsFixed.html'.format(ts)
open(SRC, 'w', encoding='utf-8').write(html)
open(ver, 'w', encoding='utf-8').write(html)
print('Salvo: ' + SRC)
print('Versao: ' + ver)
