"""
patch_mso_insight_colors.py
Torna o mso-insight (Diagnóstico do Card 1 — $ Share FYTD) dinâmico:
  • Regra de cor: delta > 0 → verde (#34d399) | delta < 0 → vermelho (#ef4444)
  • Antes: XO INSETO +2.03pp aparecia em vermelho (errado)
  • Depois: qualquer número positivo = verde, negativo = vermelho
O conteúdo é regenerado a cada chamada de renderMSO() conforme o mercado selecionado.
"""
import sys
from pathlib import Path
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

BASE = Path(r'C:\Users\valqu\OneDrive\Documentos\Claude\Projects\projeto Dashboard_farma_sul\Dashboard_farma_sul')
SRC  = BASE / 'Dashboard_Farma_Sul_20260512_2220.html'
VER  = BASE / 'versoes' / f'Dashboard_Farma_Sul_{datetime.now().strftime("%Y%m%d_%H%M")}_InsightColors.html'

print('Lendo dashboard…')
h = SRC.read_text(encoding='utf-8')
orig_len = len(h)

# ─────────────────────────────────────────────────────────────────────────────
# 1. Substituir o bloco estático mso-insight por um placeholder vazio
#    (o conteúdo será gerado pelo JS dinâmico)
# ─────────────────────────────────────────────────────────────────────────────
# Localizar o div#mso-insight estático (pode ter conteúdo variável)
import re

OLD_INSIGHT_PAT = r'<div id="mso-insight"[^>]*>.*?</div>'
m = re.search(OLD_INSIGHT_PAT, h, re.DOTALL)
assert m, '❌ div#mso-insight não encontrado'

OLD_INSIGHT = m.group(0)
NEW_INSIGHT = '<div id="mso-insight" style="margin-top:14px;padding:12px 16px;background:rgba(255,255,255,0.03);border-radius:8px;border-left:3px solid rgba(255,255,255,0.1);font-size:11px;color:#D1D5DB;line-height:1.7;"></div>'

h = h.replace(OLD_INSIGHT, NEW_INSIGHT, 1)
print('✅ div#mso-insight esvaziado (será preenchido pelo JS)')

# ─────────────────────────────────────────────────────────────────────────────
# 2. Injetar geração dinâmica no renderMSO(), antes de renderMSO2()
# ─────────────────────────────────────────────────────────────────────────────
OLD_RENDERMSO_END = """  renderMSO2();
  renderMSO3();
}

/* ═══════════ MSO JAN·FEV — 2025 vs 2026 ═══════════ */"""

NEW_RENDERMSO_END = """  // ── Diagnóstico dinâmico mso-insight ──
  var insEl = document.getElementById('mso-insight');
  if(insEl){
    function _dc(v){ return v>0?'#34d399':v<0?'#ef4444':'#94A3B8'; }
    function _pp(v){ return (v>0?'+':'')+v.toFixed(2)+'pp'; }
    var lines = ['<strong style="color:#fbbf24;font-size:10px;letter-spacing:0.08em;">📊 DIAGNÓSTICO · '+mkt+'</strong>'];
    /* OFF! */
    var offDc = _dc(off.delta);
    lines.push('📦 <strong style="color:#fbbf24;">OFF!</strong> '
      +(off.delta>=0?'ganhou':'perdeu')
      +' <strong style="color:'+offDc+';">'+_pp(off.delta)+'</strong>'
      +' de share FYTD26 vs FYTD25 em <strong style="color:#e2e8f0;">'+mkt+'</strong>'
      +' — atual: <strong style="color:'+_dc(off.fytd26-off.fytd25)+';">'+off.fytd26+'%</strong>.');
    /* SCJ Combined */
    var scjDc = _dc(scj_d);
    var scjArr = scj_d>=0?'▲':'▼';
    lines.push('🏆 <strong style="color:#fbbf24;">SCJ Combined</strong> (OFF!+EXPOSIS): <strong style="color:#e2e8f0;">'+scj_f26+'%</strong> FYTD26'
      +' <span style="color:'+scjDc+';">'+scjArr+' '+Math.abs(scj_d).toFixed(1)+'pp</span> vs FYTD25.');
    /* Maior concorrente por delta absoluto */
    var competitors = MSO_BRANDS.filter(function(b){ return b!=='OFF!'&&b!=='EXPOSIS'&&b!=='ALL OTHERS CAMP'; });
    if(competitors.length>0){
      var topC = competitors.slice().sort(function(a,b){ return Math.abs(d[b].delta)-Math.abs(d[a].delta); })[0];
      var tc = d[topC];
      if(tc){
        var tcc = _dc(tc.delta);
        lines.push((tc.delta>=0?'⚠️':'✅')+' <strong style="color:'+tcc+';">'+topC+'</strong>: '
          +tc.fytd26+'% share FYTD26 — '
          +(tc.delta>=0?'crescendo':'recuando')
          +' <strong style="color:'+tcc+';">'+_pp(tc.delta)+'</strong>'
          +(tc.delta>0?', concorrente em expansão.':'.'));
      }
    }
    insEl.innerHTML = lines.join('<br>');
  }

  renderMSO2();
  renderMSO3();
}

/* ═══════════ MSO JAN·FEV — 2025 vs 2026 ═══════════ */"""

assert h.count(OLD_RENDERMSO_END) == 1, f'Âncora renderMSO end: {h.count(OLD_RENDERMSO_END)} ocorrências'
h = h.replace(OLD_RENDERMSO_END, NEW_RENDERMSO_END)
print('✅ renderMSO → diagnóstico dinâmico com cores verde/vermelho por sinal do delta')

# ─────────────────────────────────────────────────────────────────────────────
# Verificações
# ─────────────────────────────────────────────────────────────────────────────
assert 'function _dc(v)' in h,             '❌ _dc helper não encontrado'
assert '_pp(off.delta)' in h,              '❌ _pp helper não encontrado'
assert 'concorrente em expansão' in h,     '❌ texto diagnóstico não encontrado'
assert 'id="mso-insight"' in h,            '❌ div mso-insight não encontrado'
print('✅ Verificações OK')

print(f'\nTamanho original: {orig_len:,} | Novo: {len(h):,} | Δ: {len(h)-orig_len:+,}')

VER.parent.mkdir(parents=True, exist_ok=True)
VER.write_text(h, encoding='utf-8')
print(f'✅ Versão salva: {VER.name}')
SRC.write_text(h, encoding='utf-8')
print(f'✅ Base ativa atualizada: {SRC.name}')
print('DONE.')
