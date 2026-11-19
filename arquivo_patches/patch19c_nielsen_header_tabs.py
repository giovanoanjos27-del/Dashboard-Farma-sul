"""
PATCH 19c — Nielsen Tema Claro: header + tabs + body quando Nielsen ativo
JS toggle da classe `nielsen-theme` no body + CSS para header/ctabs/body
"""
import datetime

SRC = r'Dashboard_farma_sul\Dashboard_Farma_Sul_20260512_2220.html'
html = open(SRC, encoding='utf-8').read()
original_len = len(html)
patches = 0

# ──────────────────────────────────────────────────────────────────────────────
# 1. CSS: .nielsen-theme para header, ctabs, body, filtros
# ──────────────────────────────────────────────────────────────────────────────
NEW_CSS = '''
/* ════════════════════════════════════════════════════════
   NIELSEN THEME — header/tabs/body quando aba Nielsen ativa
   ════════════════════════════════════════════════════════ */
body.nielsen-theme {
  background: #EBF0F5 !important;
}
body.nielsen-theme .header {
  background: #E2EAF8 !important;
  border-bottom-color: rgba(59,130,246,0.20) !important;
}
/* Título e subtítulo do header */
body.nielsen-theme .header h1,
body.nielsen-theme .header .header-title {
  color: #1e293b !important;
}
body.nielsen-theme .header .header-sub {
  color: #64748b !important;
}
/* Badge "Atualizado" */
body.nielsen-theme .update-badge,
body.nielsen-theme [class*="badge"],
body.nielsen-theme [style*="Atualizado"] {
  background: rgba(59,130,246,0.12) !important;
  color: #1d4ed8 !important;
  border-color: rgba(59,130,246,0.25) !important;
}
/* Tab bar */
body.nielsen-theme .ctabs {
  background: #D8E4F5 !important;
  border-bottom-color: rgba(59,130,246,0.25) !important;
}
body.nielsen-theme .ctab {
  color: #64748b !important;
}
body.nielsen-theme .ctab:hover {
  color: #1e293b !important;
}
body.nielsen-theme .ctab.active {
  color: #1d4ed8 !important;
  border-bottom-color: #1d4ed8 !important;
}
body.nielsen-theme .cdot-live {
  background: #3b82f6 !important;
}
/* Filtros globais */
body.nielsen-theme .filters {
  background: #EBF0F5 !important;
  border-bottom-color: rgba(59,130,246,0.12) !important;
}
/* Scrollbar global */
body.nielsen-theme ::-webkit-scrollbar-thumb {
  background: rgba(59,130,246,0.25) !important;
}
'''

# Inserir antes do final do bloco <style>
OLD_STYLE_END = '.u-badge-cyan{font-size:9px;font-weight:700;background:#06b6d422;color:#06b6d4;border-radius:3px;padding:1px 5px;}'
if OLD_STYLE_END in html:
    html = html.replace(OLD_STYLE_END, OLD_STYLE_END + NEW_CSS, 1)
    patches += 1
    print('[OK] CSS: .nielsen-theme para header/tabs/body adicionado')
else:
    print('[MISS] CSS: anchor u-badge-cyan nao encontrado')

# ──────────────────────────────────────────────────────────────────────────────
# 2. JS: toggle body.classList 'nielsen-theme' em switchClient
# ──────────────────────────────────────────────────────────────────────────────
OLD_ACTIVE = 'activePanel=id;\n  // Re-render Nielsen charts when switching to nielsen panel'
NEW_ACTIVE = '''activePanel=id;
  // Nielsen theme toggle
  document.body.classList.toggle('nielsen-theme', id==='nielsen');
  // Re-render Nielsen charts when switching to nielsen panel'''

if OLD_ACTIVE in html:
    html = html.replace(OLD_ACTIVE, NEW_ACTIVE, 1)
    patches += 1
    print('[OK] JS: switchClient → toggle nielsen-theme no body')
else:
    print('[MISS] JS: anchor activePanel=id nao encontrado')

# ──────────────────────────────────────────────────────────────────────────────
# 3. JS: ativar nielsen-theme na carga inicial (Nielsen é o painel padrão)
#    Inserir após o DOMContentLoaded ou no final do script principal
# ──────────────────────────────────────────────────────────────────────────────
# Nielsen começa como painel ativo (class="main active" id="panel-nielsen")
# Precisamos adicionar a classe ao body na carga da página
OLD_INIT_ANCHOR = 'if(typeof initNielsenCharts===\'function\') initNielsenCharts();'
# Não vamos mexer aí — vamos buscar o DOMContentLoaded ou window.onload
OLD_LOAD = 'window.addEventListener(\'load\','
pos_load = html.find(OLD_LOAD)
if pos_load == -1:
    OLD_LOAD = 'document.addEventListener(\'DOMContentLoaded\','
    pos_load = html.find(OLD_LOAD)

if pos_load != -1:
    print(f'[INFO] window.load/DOMContentLoaded encontrado em {pos_load}')
    # Inserir classe inicial logo no início do handler
    load_open = html.find('{', pos_load)
    if load_open != -1:
        html = html[:load_open+1] + "\n  if(document.getElementById('panel-nielsen')&&document.getElementById('panel-nielsen').classList.contains('active')){document.body.classList.add('nielsen-theme');}" + html[load_open+1:]
        patches += 1
        print('[OK] JS: nielsen-theme ativado na carga inicial via load event')
else:
    # Fallback: inserir um script inline no panel-nielsen
    OLD_FALLBACK = '<!-- ═══════════ NIELSEN ═══════════ -->'
    if OLD_FALLBACK in html:
        html = html.replace(OLD_FALLBACK,
            '<!-- ═══════════ NIELSEN ═══════════ -->\n<script>document.body.classList.add(\'nielsen-theme\');</script>',
            1)
        patches += 1
        print('[OK] JS: nielsen-theme ativado via script inline no painel')
    else:
        print('[MISS] Não foi possível injetar init do tema no load')

# ──────────────────────────────────────────────────────────────────────────────
# 4. Salvar
# ──────────────────────────────────────────────────────────────────────────────
print(f'\nPatches: {patches}')
print(f'Diff   : {len(html) - original_len:+,} bytes')

ts = datetime.datetime.now().strftime('%Y%m%d_%H%M')
ver = f'Dashboard_farma_sul/versoes/Dashboard_Farma_Sul_{ts}_NielsenHeaderTabs.html'
open(SRC, 'w', encoding='utf-8').write(html)
open(ver, 'w', encoding='utf-8').write(html)
print(f'\nSalvo : {SRC}')
print(f'Versao: {ver}')
