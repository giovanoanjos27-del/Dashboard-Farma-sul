"""
patch_nielsen_btn_all_cards.py
Adiciona botão "Exportar Nielsen Excel" nos 3 cards da aba Nielsen.

Antes: botão só no Card 1 (msoMarketSel), função injectBtn injetava 1 botão.
Agora:  3 botões (btn-nielsen-xls-1/2/3), cada um lendo o seletor do seu card.
"""
import sys
from pathlib import Path
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

BASE = Path(r'C:\Users\valqu\OneDrive\Documentos\Claude\Projects\projeto Dashboard_farma_sul\Dashboard_farma_sul')
SRC  = BASE / 'Dashboard_Farma_Sul_20260512_2220.html'
VER  = BASE / 'versoes' / f'Dashboard_Farma_Sul_{datetime.now().strftime("%Y%m%d_%H%M")}_NielsenBtn3Cards.html'

print('Lendo dashboard…')
h = SRC.read_text(encoding='utf-8')
orig_len = len(h)

# ─────────────────────────────────────────────────────────────────────────────
# 1. injectBtn — de 1 botão para 3 botões (um por card)
# ─────────────────────────────────────────────────────────────────────────────
OLD_INJECT = """/* ── 1. Injetar botão no header do card MSO ── */
function injectBtn(){
  var sel = document.getElementById('msoMarketSel');
  if(!sel) return;
  var wrap = sel.parentNode;
  if(document.getElementById('btn-nielsen-xls')) return;
  var btn = document.createElement('button');
  btn.id = 'btn-nielsen-xls';
  btn.innerHTML = '&#128229; Exportar Nielsen Excel';
  btn.title = 'Exporta relatório executivo .xlsx com 5 abas analíticas';
  btn.style.cssText = 'display:inline-flex;align-items:center;gap:5px;font-size:11px;font-weight:700;'
    +'background:rgba(251,191,36,0.1);border:1px solid rgba(251,191,36,0.35);color:#fbbf24;'
    +'border-radius:6px;padding:6px 14px;cursor:pointer;font-family:inherit;transition:background 0.2s;';
  btn.onmouseover = function(){ this.style.background='rgba(251,191,36,0.22)'; };
  btn.onmouseout  = function(){ this.style.background='rgba(251,191,36,0.1)'; };
  btn.onclick = triggerExport;
  wrap.appendChild(btn);
}"""

NEW_INJECT = """/* ── 1. Injetar botão em TODOS os 3 cards Nielsen ── */
function injectBtn(){
  var cards = [
    {selId:'msoMarketSel',  btnId:'btn-nielsen-xls-1'},
    {selId:'mso2MarketSel', btnId:'btn-nielsen-xls-2'},
    {selId:'mso3MarketSel', btnId:'btn-nielsen-xls-3'}
  ];
  var CSS = 'display:inline-flex;align-items:center;gap:5px;font-size:11px;font-weight:700;'
    +'background:rgba(251,191,36,0.1);border:1px solid rgba(251,191,36,0.35);color:#fbbf24;'
    +'border-radius:6px;padding:6px 14px;cursor:pointer;font-family:inherit;transition:background 0.2s;';
  cards.forEach(function(c){
    var sel = document.getElementById(c.selId);
    if(!sel || document.getElementById(c.btnId)) return;
    var btn = document.createElement('button');
    btn.id = c.btnId;
    btn.innerHTML = '&#128229; Exportar Nielsen Excel';
    btn.title = 'Exporta relatório executivo .xlsx com 5 abas analíticas';
    btn.style.cssText = CSS;
    btn.onmouseover = function(){ this.style.background='rgba(251,191,36,0.22)'; };
    btn.onmouseout  = function(){ this.style.background='rgba(251,191,36,0.1)'; };
    (function(sId, bId){ btn.onclick = function(){ triggerExport(sId, bId); }; })(c.selId, c.btnId);
    sel.parentNode.appendChild(btn);
  });
}"""

count = h.count(OLD_INJECT)
assert count == 1, f'injectBtn: encontrei {count} ocorrências (esperava 1)'
h = h.replace(OLD_INJECT, NEW_INJECT)
print('✅ injectBtn atualizado → injeta botão nos 3 cards')

# ─────────────────────────────────────────────────────────────────────────────
# 2. getState — aceitar selId como parâmetro
# ─────────────────────────────────────────────────────────────────────────────
OLD_GETSTATE = """/* ── 4. Capturar estado atual ── */
function getState(){
  var sel = document.getElementById('msoMarketSel');
  var market = sel ? sel.value : 'T.BR Farma';"""

NEW_GETSTATE = """/* ── 4. Capturar estado atual ── */
function getState(selId){
  var sel = document.getElementById(selId || 'msoMarketSel');
  var market = sel ? sel.value : 'T.BR Farma';"""

count2 = h.count(OLD_GETSTATE)
assert count2 == 1, f'getState: encontrei {count2} ocorrências (esperava 1)'
h = h.replace(OLD_GETSTATE, NEW_GETSTATE)
print('✅ getState atualizado → aceita selId')

# ─────────────────────────────────────────────────────────────────────────────
# 3. triggerExport — aceitar selId e btnId como parâmetros
# ─────────────────────────────────────────────────────────────────────────────
OLD_TRIGGER = """/* ── 5. Trigger principal ── */
function triggerExport(){
  var state = getState();
  if(!state) return;
  var btn = document.getElementById('btn-nielsen-xls');
  if(btn){ btn.disabled=true; btn.textContent='⏳ Gerando…'; }
  loadExcelJS(function(){
    showToast('⏳ Gerando relatório Nielsen…', 'info');
    setTimeout(function(){ buildExcel(state, btn); }, 80);
  });
}"""

NEW_TRIGGER = """/* ── 5. Trigger principal ── */
function triggerExport(selId, btnId){
  selId = selId || 'msoMarketSel';
  btnId = btnId || 'btn-nielsen-xls-1';
  var state = getState(selId);
  if(!state) return;
  var btn = document.getElementById(btnId);
  if(btn){ btn.disabled=true; btn.textContent='⏳ Gerando…'; }
  loadExcelJS(function(){
    showToast('⏳ Gerando relatório Nielsen…', 'info');
    setTimeout(function(){ buildExcel(state, btn); }, 80);
  });
}"""

count3 = h.count(OLD_TRIGGER)
assert count3 == 1, f'triggerExport: encontrei {count3} ocorrências (esperava 1)'
h = h.replace(OLD_TRIGGER, NEW_TRIGGER)
print('✅ triggerExport atualizado → recebe selId e btnId')

# ─────────────────────────────────────────────────────────────────────────────
# Verificações finais
# ─────────────────────────────────────────────────────────────────────────────
assert 'btn-nielsen-xls-1' in h, '❌ btn-nielsen-xls-1 não encontrado'
assert 'btn-nielsen-xls-2' in h, '❌ btn-nielsen-xls-2 não encontrado'
assert 'btn-nielsen-xls-3' in h, '❌ btn-nielsen-xls-3 não encontrado'
assert 'mso2MarketSel' in h,     '❌ mso2MarketSel não encontrado'
assert 'mso3MarketSel' in h,     '❌ mso3MarketSel não encontrado'
assert 'function getState(selId)' in h, '❌ getState(selId) não encontrado'
assert 'function triggerExport(selId, btnId)' in h, '❌ triggerExport(selId,btnId) não encontrado'
print('✅ Verificações finais OK')

print(f'\nTamanho original: {orig_len:,} | Novo: {len(h):,} | Δ: {len(h)-orig_len:+,}')

VER.parent.mkdir(parents=True, exist_ok=True)
VER.write_text(h, encoding='utf-8')
print(f'✅ Versão salva: {VER.name}')

SRC.write_text(h, encoding='utf-8')
print(f'✅ Base ativa atualizada: {SRC.name}')
print('DONE.')
