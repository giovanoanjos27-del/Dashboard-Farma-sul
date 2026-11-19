"""
patch_label_maior.py
====================
Aumenta as letras dos labels do mapa:
  UF: 11px → 14px
  %:  10px → 13px
  Badge: opacidade 0.55 → 0.72, padding maior, borda lateral pctCol
  iconSize: [52,34] → [64,42]
"""
import sys, shutil
sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path
from datetime import datetime

DASH = Path(r'C:\Users\valqu\OneDrive\Documentos\Claude\Projects\projeto Dashboard_farma_sul\Dashboard_farma_sul\Dashboard_Farma_Sul_20260512_2220.html')
VER  = DASH.parent / 'versoes'
DL   = Path.home() / 'Downloads'
ts   = datetime.now().strftime('%Y%m%d_%H%M')

shutil.copy(DASH, VER / f'Dashboard_Farma_Sul_{ts}_PreLabelMaior.html')
h = DASH.read_text(encoding='utf-8')
print(f'Backup  |  {len(h):,} chars')

def replace_once(html, old, new, label):
    cnt = html.count(old)
    assert cnt == 1, f'ERRO [{label}]: {cnt}x encontrado'
    print(f'✓ {label}')
    return html.replace(old, new, 1)

OLD = (
    "        html: '<div style=\"pointer-events:none;text-align:center;transform:translate(-50%,-50%);white-space:nowrap;\">'\n"
    "          +'<div style=\"display:inline-block;background:rgba(0,0,0,0.55);'\n"
    "            +'border-radius:5px;padding:2px 6px 3px 6px;'\n"
    "            +'border-bottom:2px solid '+pctCol+';'\n"
    "            +'box-shadow:0 2px 6px rgba(0,0,0,0.7);\">'\n"
    "            +'<div style=\"font-size:11px;font-weight:900;color:#fff;line-height:1.2;letter-spacing:.04em;\">'+uf+'</div>'\n"
    "            +(pct!==null\n"
    "              ? '<div style=\"font-size:10px;font-weight:800;color:#fff;line-height:1.1;\">'+pct+'%</div>'\n"
    "              : '')\n"
    "          +'</div>'\n"
    "          +'</div>',\n"
    '        iconSize:[52,34], iconAnchor:[26,17]\n'
)

NEW = (
    "        html: '<div style=\"pointer-events:none;text-align:center;transform:translate(-50%,-50%);white-space:nowrap;\">'\n"
    "          +'<div style=\"display:inline-block;background:rgba(0,0,0,0.72);'\n"
    "            +'border-radius:6px;padding:3px 8px 4px 8px;'\n"
    "            +'border-left:3px solid '+pctCol+';'\n"
    "            +'box-shadow:0 2px 8px rgba(0,0,0,0.85);\">'\n"
    "            +'<div style=\"font-size:14px;font-weight:900;color:#fff;line-height:1.2;letter-spacing:.05em;text-shadow:0 1px 2px #000;\">'+uf+'</div>'\n"
    "            +(pct!==null\n"
    "              ? '<div style=\"font-size:13px;font-weight:800;color:#fff;line-height:1.1;text-shadow:0 1px 2px #000;\">'+pct+'%</div>'\n"
    "              : '')\n"
    "          +'</div>'\n"
    "          +'</div>',\n"
    '        iconSize:[64,42], iconAnchor:[32,21]\n'
)

h = replace_once(h, OLD, NEW, 'Labels UF 14px + % 13px + badge mais escuro')

assert 'font-size:14px' in h, 'ERRO: 14px não inserido'
assert 'font-size:13px' in h, 'ERRO: 13px não inserido'
assert 'iconSize:[64,42]' in h, 'ERRO: iconSize não atualizado'
print('Verificações: OK')
print(f'Tamanho final: {len(h):,} chars')

DASH.write_text(h, encoding='utf-8')
shutil.copy(DASH, VER / f'Dashboard_Farma_Sul_{ts}_LabelMaior.html')
shutil.copy(DASH, DL  / f'Dashboard_FarmaSul_Giovano_{ts}.html')
print(f'Downloads: Dashboard_FarmaSul_Giovano_{ts}.html')
print('DONE.')
