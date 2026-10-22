"""
patch_iqvia_toggle.py
=====================
Adiciona toggle ao card ESTUDO ED NACIONAL:
- Mapa interativo: sempre visível
- KPIs + barra composição + tabela UF: oculto por padrão,
  expansível via botão "KPIs & Tabela ▼"
Não altera nenhum dado, JS ou outra visualização.
"""
import sys, shutil
sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path
from datetime import datetime

DASH = Path(r'C:\Users\valqu\OneDrive\Documentos\Claude\Projects\projeto Dashboard_farma_sul\Dashboard_farma_sul\Dashboard_Farma_Sul_20260512_2220.html')
VER  = DASH.parent / 'versoes'
DL   = Path.home() / 'Downloads'
ts   = datetime.now().strftime('%Y%m%d_%H%M')

shutil.copy(DASH, VER / f'Dashboard_Farma_Sul_{ts}_PreIqviaToggle.html')
print(f'Backup: Dashboard_Farma_Sul_{ts}_PreIqviaToggle.html')

h = DASH.read_text(encoding='utf-8')

# ── Localizar iqvia-nac-body e calcular posições ──────────────────────────────
p_body = h.find('<div id="iqvia-nac-body"')
assert p_body != -1, 'iqvia-nac-body nao encontrado'

# Fechar iqvia-nac-body (contar divs)
depth = 0; i = p_body
while i < len(h):
    if h[i:i+4] == '<div':   depth += 1; i += 4
    elif h[i:i+6] == '</div>': depth -= 1; i += 6
    else: i += 1
    if depth == 0: body_end = i; break
else:
    raise AssertionError('iqvia-nac-body: fechamento nao encontrado')

# Posição onde os KPIs começam (primeiro grid repeat(4,1fr) após o mapa)
kpi_grid_marker = 'grid-template-columns:repeat(4,1fr)'
kpi_grid_pos = h.find(kpi_grid_marker, p_body)
assert kpi_grid_pos != -1 and kpi_grid_pos < body_end, 'grid KPI nao encontrado dentro de iqvia-nac-body'

# Voltar até o <div que abre esse grid
kpi_start = h.rfind('<div', p_body, kpi_grid_pos)
assert kpi_start != -1, 'div de abertura do grid KPI nao encontrado'

# O </div> de fechamento do iqvia-nac-body fica em [body_end-6 : body_end]
close_body_div = body_end - 6
assert h[close_body_div:body_end] == '</div>', f'Esperado </div> em {close_body_div}, encontrado: {repr(h[close_body_div:body_end])}'

print(f'iqvia-nac-body: [{p_body} .. {body_end}]')
print(f'KPI section começa em: {kpi_start}')
print(f'Fechamento iqvia-nac-body em: {close_body_div}')
print(f'Secao a envolver: {close_body_div - kpi_start:,} chars')

# ── HTML do botão toggle ──────────────────────────────────────────────────────
TOGGLE_BTN = (
    '<div style="text-align:right;margin-bottom:10px;">'
    '<button id="iqvia-toggle-btn" '
    'onclick="(function(){'
      'var d=document.getElementById(\'iqvia-details\');'
      'var b=document.getElementById(\'iqvia-toggle-btn\');'
      'if(d.style.display===\'none\'){'
        'd.style.display=\'\';'
        'b.textContent=\'Ocultar detalhes ▲\';'
      '}else{'
        'd.style.display=\'none\';'
        'b.textContent=\'KPIs & Tabela ▼\';'
      '}'
    '})()" '
    'style="font-size:10px;font-weight:700;padding:5px 16px;border-radius:7px;'
    'background:rgba(6,182,212,0.12);border:0.5px solid rgba(6,182,212,0.35);'
    'color:#67e8f9;cursor:pointer;font-family:inherit;letter-spacing:0.06em;'
    'transition:background 0.2s;">'
    'KPIs &amp; Tabela &#9660;'
    '</button></div>'
    '<div id="iqvia-details" style="display:none;">'
)
TOGGLE_CLOSE = '</div>'  # fecha iqvia-details

# ── Aplicar (de trás para frente para manter offsets) ─────────────────────────
# 1) Inserir </div> fechando iqvia-details, antes do </div> do iqvia-nac-body
h = h[:close_body_div] + TOGGLE_CLOSE + h[close_body_div:]

# 2) Inserir botão + abertura de iqvia-details no início da seção KPI
h = h[:kpi_start] + TOGGLE_BTN + h[kpi_start:]

# ── Verificações ──────────────────────────────────────────────────────────────
assert 'iqvia-toggle-btn'  in h, 'ERRO: botao toggle nao inserido'
assert 'iqvia-details'     in h, 'ERRO: div iqvia-details nao inserido'
assert h.count('iqvia-details') == 2, f'ERRO: esperado 2 refs a iqvia-details, encontrei {h.count("iqvia-details")}'
assert 'iqvia-nac-body'    in h, 'ERRO: iqvia-nac-body perdido'
assert 'brazil-choro-svg'  in h, 'ERRO: mapa SVG perdido'
assert 'Universe Brasil'   in h, 'ERRO: KPI Universe Brasil perdido'
print('Verificacoes: OK')

# ── Salvar ────────────────────────────────────────────────────────────────────
DASH.write_text(h, encoding='utf-8')
shutil.copy(DASH, VER / f'Dashboard_Farma_Sul_{ts}_IqviaToggle.html')
shutil.copy(DASH, DL  / f'Dashboard_FarmaSul_Giovano_{ts}.html')
print(f'\nSalvo:     {DASH.name}')
print(f'Versao:    Dashboard_Farma_Sul_{ts}_IqviaToggle.html')
print(f'Downloads: Dashboard_FarmaSul_Giovano_{ts}.html')
print('DONE.')
