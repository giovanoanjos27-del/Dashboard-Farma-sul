"""
patch_yoy_cob_estado.py
=======================
Adiciona bloco "COBERTURA POR ESTADO (TOP 10)" ao ranking geral do card
EVOLUÇÃO ANUAL — TODOS OS PROVEDORES.

• Aparece na view de ranking (sem provedor selecionado)
• Agrega by_uf de todos os 157 provedores do PROV_DATA
• Barras horizontais top 10 estados por volume de PDVs
• Grid 2 colunas — mesmo visual do detalhe por provedor
• Posição: entre o KPI strip e a tabela de ranking
"""
import sys, shutil
sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path
from datetime import datetime

DASH = Path(r'C:\Users\valqu\OneDrive\Documentos\Claude\Projects\projeto Dashboard_farma_sul\Dashboard_farma_sul\Dashboard_Farma_Sul_20260512_2220.html')
VER  = DASH.parent / 'versoes'
DL   = Path.home() / 'Downloads'
ts   = datetime.now().strftime('%Y%m%d_%H%M')

shutil.copy(DASH, VER / f'Dashboard_Farma_Sul_{ts}_PreYoyCobEstado.html')
h = DASH.read_text(encoding='utf-8')
print(f'Backup: ...PreYoyCobEstado.html  |  {len(h):,} chars')

# ── Anchor: fim de _yoyRenderRanking ─────────────────────────────────────────
OLD = '  bodyEl.innerHTML=kpi+table+btnAll;\n}'

assert h.count(OLD) == 1, f'Anchor não-única: {h.count(OLD)}x'

NEW = r"""  /* ── Cobertura por Estado — Agregado de todos os provedores ── */
  var ufAgg = {};
  (PROV_DATA||[]).forEach(function(p){
    (p.by_uf||[]).forEach(function(u){
      var uf = u[0], tot = u[1]||0, scj = u[2]||0;
      if(!ufAgg[uf]) ufAgg[uf] = {total:0, scj:0};
      ufAgg[uf].total += tot;
      ufAgg[uf].scj   += scj;
    });
  });
  var ufArr = Object.keys(ufAgg).map(function(uf){
    var d = ufAgg[uf];
    var pct = d.total > 0 ? Math.round(d.scj / d.total * 100) : 0;
    return {uf:uf, total:d.total, scj:d.scj, pct:pct};
  }).sort(function(a,b){ return b.total - a.total; }).slice(0,10);

  var ufTop10Html = '';
  if(ufArr.length){
    var maxTot = ufArr[0].total || 1;
    var half   = Math.ceil(ufArr.length / 2);
    var left   = ufArr.slice(0, half);
    var right  = ufArr.slice(half);

    function mkUFRow(u){
      var col = u.pct>=70?'#34d399':u.pct>=40?'#fbbf24':u.pct>=20?'#f97316':'#ef4444';
      var bw  = Math.round(u.total / maxTot * 100);
      return '<div style="display:flex;align-items:center;gap:8px;margin-bottom:6px;">'
        +'<span style="font-size:11px;font-weight:700;color:#94a3b8;min-width:24px;">'+u.uf+'</span>'
        +'<div style="flex:1;background:rgba(255,255,255,0.04);border-radius:3px;height:10px;overflow:hidden;">'
          +'<div style="height:100%;background:'+col+';border-radius:3px;width:'+bw+'%;opacity:0.85;"></div>'
        +'</div>'
        +'<span style="font-size:11px;font-weight:800;color:'+col+';min-width:36px;text-align:right;">'+u.pct+'%</span>'
        +'<span style="font-size:9px;color:#475569;min-width:80px;text-align:right;">'+u.scj.toLocaleString('pt-BR')+'/'+u.total.toLocaleString('pt-BR')+'</span>'
        +'</div>';
    }

    // Legend
    var legend = '<div style="display:flex;gap:12px;margin-top:14px;flex-wrap:wrap;align-items:center;padding:0 2px;">'
      +'<span style="display:flex;align-items:center;gap:4px;font-size:9px;color:#94a3b8;"><span style="width:9px;height:9px;border-radius:2px;background:#34d399;display:inline-block;"></span>≥70%</span>'
      +'<span style="display:flex;align-items:center;gap:4px;font-size:9px;color:#94a3b8;"><span style="width:9px;height:9px;border-radius:2px;background:#fbbf24;display:inline-block;"></span>40–69%</span>'
      +'<span style="display:flex;align-items:center;gap:4px;font-size:9px;color:#94a3b8;"><span style="width:9px;height:9px;border-radius:2px;background:#f97316;display:inline-block;"></span>20–39%</span>'
      +'<span style="display:flex;align-items:center;gap:4px;font-size:9px;color:#94a3b8;"><span style="width:9px;height:9px;border-radius:2px;background:#ef4444;display:inline-block;"></span><20%</span>'
      +'<span style="margin-left:auto;font-size:9px;color:#334155;font-style:italic;">SCJ ativos / total universo IQVIA por estado</span>'
      +'</div>';

    ufTop10Html =
      '<div style="background:#0d1117;border-radius:10px;padding:16px;margin-bottom:16px;">'
      +'<div style="display:flex;justify-content:space-between;align-items:baseline;margin-bottom:14px;">'
        +'<span style="font-size:9px;font-weight:700;color:#475569;letter-spacing:0.08em;text-transform:uppercase;">📍 COBERTURA POR ESTADO (TOP 10) — TODOS OS PROVEDORES</span>'
        +'<span style="font-size:8px;color:#334155;">Barra ∝ volume total de PDVs · % = SCJ ativos / universo</span>'
      +'</div>'
      +'<div style="display:grid;grid-template-columns:1fr 1fr;gap:0 24px;">'
        +'<div>'+left.map(mkUFRow).join('')+'</div>'
        +'<div>'+right.map(mkUFRow).join('')+'</div>'
      +'</div>'
      +legend
      +'</div>';
  }

  bodyEl.innerHTML=kpi+ufTop10Html+table+btnAll;
}"""

h = h.replace(OLD, NEW, 1)
print('Bloco COBERTURA POR ESTADO injetado em _yoyRenderRanking()')

# ── Verificações ──────────────────────────────────────────────────────────────
assert 'ufAgg'      in h, 'ERRO: ufAgg não inserido'
assert 'ufTop10Html' in h, 'ERRO: ufTop10Html não inserido'
assert 'mkUFRow'    in h, 'ERRO: mkUFRow não inserido'
assert 'prov-yoy-body' in h, 'ERRO: prov-yoy-body perdido'
assert h.count('bodyEl.innerHTML=kpi+') == 1, 'ERRO: bodyEl.innerHTML duplicado'
print('Verificações: OK')

# ── Salvar ────────────────────────────────────────────────────────────────────
DASH.write_text(h, encoding='utf-8')
shutil.copy(DASH, VER / f'Dashboard_Farma_Sul_{ts}_YoyCobEstado.html')
shutil.copy(DASH, DL  / f'Dashboard_FarmaSul_Giovano_{ts}.html')
print(f'Versao:    Dashboard_Farma_Sul_{ts}_YoyCobEstado.html')
print(f'Downloads: Dashboard_FarmaSul_Giovano_{ts}.html')
print('DONE.')
