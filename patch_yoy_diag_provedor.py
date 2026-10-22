"""
patch_yoy_diag_provedor.py
==========================
1. Remove bloco estático yoy-diagnostico do cabeçalho do card YoY
2. Insere diagnóstico DINÂMICO ao final de _yoyRenderDetail()
   — só aparece quando um provedor específico está selecionado
   — 3 colunas: ① Evolução Anual ② Q1 Trend ③ Oportunidade
   — interpretação automática baseada nos dados reais do provedor
"""
import sys, shutil
sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path
from datetime import datetime

DASH = Path(r'C:\Users\valqu\OneDrive\Documentos\Claude\Projects\projeto Dashboard_farma_sul\Dashboard_farma_sul\Dashboard_Farma_Sul_20260512_2220.html')
VER  = DASH.parent / 'versoes'
DL   = Path.home() / 'Downloads'
ts   = datetime.now().strftime('%Y%m%d_%H%M')

shutil.copy(DASH, VER / f'Dashboard_Farma_Sul_{ts}_PreDiagProv.html')
h = DASH.read_text(encoding='utf-8')
print(f'Backup: ...PreDiagProv.html')
print(f'Tamanho original: {len(h):,} chars')

# ═══════════════════════════════════════════════════════════════════════════════
# 1) REMOVER bloco estático yoy-diagnostico
# ═══════════════════════════════════════════════════════════════════════════════
START_MARKER = '\n      <!-- ▼ DIAGNÓSTICO EVOLUÇÃO ANUAL -->'
END_MARKER   = '      <!-- ▲ DIAGNÓSTICO EVOLUÇÃO ANUAL -->\n'

s = h.find(START_MARKER)
e = h.find(END_MARKER)
assert s != -1, 'ERRO: marcador início yoy-diagnostico não encontrado'
assert e != -1, 'ERRO: marcador fim yoy-diagnostico não encontrado'
e += len(END_MARKER)

removed_block = h[s:e]
assert 'yoy-diagnostico' in removed_block, 'ERRO: yoy-diagnostico não está no bloco'
h = h[:s] + h[e:]
print(f'Bloco estático removido: {e - s:,} chars')

# ═══════════════════════════════════════════════════════════════════════════════
# 2) INSERIR diagnóstico dinâmico antes de bodyEl.innerHTML = kpi + cimedRb + canvas + ufHtml;
# ═══════════════════════════════════════════════════════════════════════════════
OLD_INNER = '  bodyEl.innerHTML = kpi + cimedRb + canvas + ufHtml;'

assert h.count(OLD_INNER) == 1, f'ERRO: anchor não-única ({h.count(OLD_INNER)}x)'

NEW_INNER = r"""  /* ── Diagnóstico dinâmico do provedor ── */
  var dDeltaInterp = delta===null ? 'Dados insuficientes para análise.'
    : delta > 20  ? 'Crescimento acelerado — canal ativo e em forte expansão.'
    : delta > 5   ? 'Crescimento sólido — positivação em alta.'
    : delta >= 0  ? 'Leve crescimento — estabilidade com pequeno ganho.'
    : delta > -10 ? 'Queda leve — monitorar sell-in e rupturas.'
    : delta > -25 ? 'Queda moderada — ação comercial recomendada.'
    :               'Queda expressiva — ação comercial prioritária urgente.';

  var dQ1Interp = q1d===null ? '—'
    : (delta!==null && q1d > delta+5) ? 'Q1 acelerando vs FY — tendência positiva no trimestre.'
    : (delta!==null && q1d < delta-5) ? 'Q1 desacelerando vs FY — atenção ao trimestre atual.'
    : 'Q1 em linha com tendência anual.';

  var oppLevel  = opp>500?'Alta':opp>200?'Média':opp>50?'Baixa':'Mínima';
  var oppColor  = opp>500?'#06b6d4':opp>200?'#22c55e':opp>50?'#fbbf24':'#64748b';
  var reconqLvl = atend>=50?'Alta':atend>=25?'Média':'Baixa';
  var reconqClr = atend>=50?'#34d399':atend>=25?'#fbbf24':'#ef4444';

  var diagHtml =
    '<div style="margin-top:16px;border-radius:10px;background:rgba(34,197,94,0.04);border:0.5px solid rgba(34,197,94,0.18);overflow:hidden;">'
    // header
    +'<div style="padding:10px 16px;background:rgba(34,197,94,0.06);border-bottom:0.5px solid rgba(34,197,94,0.12);">'
    +'<span style="font-size:9px;font-weight:800;letter-spacing:0.12em;color:#22c55e;text-transform:uppercase;">📋 DIAGNÓSTICO — '+p.name+'</span>'
    +'</div>'
    // grid 3 colunas
    +'<div style="padding:14px 16px;display:grid;grid-template-columns:1fr 1fr 1fr;gap:12px;">'

    // ── Col 1 — Evolução Anual ──────────────────────────────────────────
    +'<div style="background:#0D1117;border-radius:8px;padding:12px;border-left:3px solid #22c55e;">'
    +'<div style="font-size:9px;font-weight:800;color:#22c55e;letter-spacing:0.1em;text-transform:uppercase;margin-bottom:10px;">① Evolução Anual</div>'
    +'<div style="display:flex;flex-direction:column;gap:6px;">'
    // FY25
    +'<div style="background:rgba(59,130,246,0.07);border-radius:6px;padding:8px 10px;">'
    +'<div style="font-size:8px;font-weight:700;color:#3b82f6;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:3px;">FY25 · Jul/24–Mar/25</div>'
    +'<div style="font-size:16px;color:#e2e8f0;font-weight:800;">'+fy25.toLocaleString('pt-BR')+'<span style="font-size:9px;color:#64748b;margin-left:4px;">PDV-meses</span></div>'
    +'</div>'
    // FY26
    +'<div style="background:rgba(34,197,94,0.07);border-radius:6px;padding:8px 10px;">'
    +'<div style="font-size:8px;font-weight:700;color:#22c55e;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:3px;">FY26 · Jul/25–Mar/26</div>'
    +'<div style="font-size:16px;color:#e2e8f0;font-weight:800;">'+fy26.toLocaleString('pt-BR')+'<span style="font-size:9px;color:#64748b;margin-left:4px;">PDV-meses</span></div>'
    +'</div>'
    // Delta
    +'<div style="background:rgba(34,197,94,0.05);border-radius:6px;padding:10px;border:0.5px solid rgba(34,197,94,0.15);">'
    +'<div style="font-size:8px;font-weight:700;color:#94a3b8;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:4px;">Δ% FY25 → FY26</div>'
    +'<div style="font-size:22px;font-weight:900;color:'+dCol(delta)+';line-height:1;">'+(delta===null?'—':(delta>=0?'+':'')+delta.toFixed(1)+'%')+'</div>'
    +'<div style="font-size:8px;color:#64748b;margin-top:5px;line-height:1.5;">'+dDeltaInterp+'</div>'
    +'</div>'
    +'</div></div>'

    // ── Col 2 — Q1 & Tendência ─────────────────────────────────────────
    +'<div style="background:#0D1117;border-radius:8px;padding:12px;border-left:3px solid #a78bfa;">'
    +'<div style="font-size:9px;font-weight:800;color:#a78bfa;letter-spacing:0.1em;text-transform:uppercase;margin-bottom:10px;">② Tendência Q1</div>'
    +'<div style="display:flex;flex-direction:column;gap:6px;">'
    // Q1 FY25
    +'<div style="background:rgba(148,163,184,0.07);border-radius:6px;padding:8px 10px;">'
    +'<div style="font-size:8px;font-weight:700;color:#94a3b8;margin-bottom:3px;">Q1 FY25 · Jan–Mar/25</div>'
    +'<div style="font-size:14px;color:#e2e8f0;font-weight:700;">'+q1_25.toLocaleString('pt-BR')+'<span style="font-size:9px;color:#64748b;margin-left:4px;">PDV-meses</span></div>'
    +'</div>'
    // Q1 FY26
    +'<div style="background:rgba(139,92,246,0.07);border-radius:6px;padding:8px 10px;">'
    +'<div style="font-size:8px;font-weight:700;color:#a78bfa;margin-bottom:3px;">Q1 FY26 · Jan–Mar/26</div>'
    +'<div style="font-size:14px;color:#e2e8f0;font-weight:700;">'+q1_26.toLocaleString('pt-BR')+'<span style="font-size:9px;color:#64748b;margin-left:4px;">PDV-meses</span></div>'
    +'</div>'
    // Delta Q1
    +'<div style="background:rgba(139,92,246,0.06);border-radius:6px;padding:10px;border:0.5px solid rgba(139,92,246,0.18);">'
    +'<div style="font-size:8px;font-weight:700;color:#94a3b8;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:4px;">Δ% Q1 YoY</div>'
    +'<div style="font-size:20px;font-weight:900;color:'+dCol(q1d)+';line-height:1;">'+(q1d===null?'—':(q1d>=0?'+':'')+q1d.toFixed(1)+'%')+'</div>'
    +'<div style="font-size:8px;color:#64748b;margin-top:5px;line-height:1.5;">'+dQ1Interp+'</div>'
    +'</div>'
    +'</div></div>'

    // ── Col 3 — Oportunidade & Reconquista ────────────────────────────
    +'<div style="background:#0D1117;border-radius:8px;padding:12px;border-left:3px solid #f97316;">'
    +'<div style="font-size:9px;font-weight:800;color:#f97316;letter-spacing:0.1em;text-transform:uppercase;margin-bottom:10px;">③ Oportunidade</div>'
    +'<div style="display:flex;flex-direction:column;gap:6px;">'
    // CIMED
    +'<div style="background:rgba(167,139,250,0.07);border-radius:6px;padding:8px 10px;">'
    +'<div style="font-size:8px;font-weight:700;color:#a78bfa;margin-bottom:3px;">CIMED sem SCJ</div>'
    +'<div style="font-size:14px;color:#e2e8f0;font-weight:700;">'+(p.opp_ci||0).toLocaleString('pt-BR')+'<span style="font-size:9px;color:#64748b;margin-left:4px;">PDVs</span></div>'
    +'</div>'
    // RB
    +'<div style="background:rgba(96,165,250,0.07);border-radius:6px;padding:8px 10px;">'
    +'<div style="font-size:8px;font-weight:700;color:#60a5fa;margin-bottom:3px;">RB sem SCJ</div>'
    +'<div style="font-size:14px;color:#e2e8f0;font-weight:700;">'+(p.opp_rb||0).toLocaleString('pt-BR')+'<span style="font-size:9px;color:#64748b;margin-left:4px;">PDVs</span></div>'
    +'</div>'
    // Consolidado + nível
    +'<div style="background:rgba(249,115,22,0.07);border-radius:6px;padding:8px 10px;">'
    +'<div style="font-size:8px;font-weight:700;color:#f97316;margin-bottom:3px;">Consolidado (Dedup.)</div>'
    +'<div style="font-size:14px;color:#e2e8f0;font-weight:700;">'+opp.toLocaleString('pt-BR')+'<span style="font-size:9px;color:#64748b;margin-left:4px;">PDVs</span></div>'
    +'<div style="font-size:8px;margin-top:3px;color:'+oppColor+';font-weight:700;">Nível: '+oppLevel+'</div>'
    +'</div>'
    // Reconquista
    +'<div style="background:rgba(52,211,153,0.07);border-radius:6px;padding:8px 10px;border:0.5px solid rgba(52,211,153,0.12);">'
    +'<div style="font-size:8px;font-weight:700;color:#34d399;margin-bottom:3px;">🔄 Reconquista</div>'
    +'<div style="font-size:14px;color:#e2e8f0;font-weight:700;">'+reconq.toLocaleString('pt-BR')+'<span style="font-size:9px;color:#64748b;margin-left:4px;">PDVs</span></div>'
    +'<div style="font-size:8px;margin-top:3px;color:'+reconqClr+';font-weight:700;">Conv. '+atend+'% — '+reconqLvl+' prioridade</div>'
    +'</div>'
    +'</div></div>'

    +'</div></div>'; // /grid-3-cols, /diagnostico

  bodyEl.innerHTML = kpi + cimedRb + canvas + ufHtml + diagHtml;"""

h = h.replace(OLD_INNER, NEW_INNER, 1)
print('Diagnóstico dinâmico injetado em _yoyRenderDetail()')

# ═══════════════════════════════════════════════════════════════════════════════
# Verificações
# ═══════════════════════════════════════════════════════════════════════════════
assert 'yoy-diagnostico'     not in h,  'ERRO: bloco estático ainda presente!'
assert 'DIAGNÓSTICO — \'+p.name' in h,  'ERRO: diagnóstico dinâmico não encontrado'
assert 'dDeltaInterp'        in h,      'ERRO: variável interpretação não encontrada'
assert 'reconqLvl'           in h,      'ERRO: variável reconquista não encontrada'
assert 'prov-yoy-body'       in h,      'ERRO: prov-yoy-body perdido'
assert 'prov-yoy-card'       in h,      'ERRO: prov-yoy-card perdido'
print('Verificações: OK')
print(f'Tamanho final: {len(h):,} chars')

# ═══════════════════════════════════════════════════════════════════════════════
# Salvar
# ═══════════════════════════════════════════════════════════════════════════════
DASH.write_text(h, encoding='utf-8')
shutil.copy(DASH, VER / f'Dashboard_Farma_Sul_{ts}_DiagProv.html')
shutil.copy(DASH, DL  / f'Dashboard_FarmaSul_Giovano_{ts}.html')
print(f'Versao:    Dashboard_Farma_Sul_{ts}_DiagProv.html')
print(f'Downloads: Dashboard_FarmaSul_Giovano_{ts}.html')
print('DONE.')
