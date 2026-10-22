"""
patch_yoy_diagnostico.py
========================
Injeta bloco DIAGNÓSTICO no card EVOLUÇÃO ANUAL — TODOS OS PROVEDORES.
Explica: fonte dos dados, metodologia de cálculo e como interpretar.
Posição: entre o card-header e o prov-yoy-body (antes do ranking).
"""
import sys, shutil
sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path
from datetime import datetime

DASH = Path(r'C:\Users\valqu\OneDrive\Documentos\Claude\Projects\projeto Dashboard_farma_sul\Dashboard_farma_sul\Dashboard_Farma_Sul_20260512_2220.html')
VER  = DASH.parent / 'versoes'
DL   = Path.home() / 'Downloads'
ts   = datetime.now().strftime('%Y%m%d_%H%M')

shutil.copy(DASH, VER / f'Dashboard_Farma_Sul_{ts}_PreDiagYoY.html')
h = DASH.read_text(encoding='utf-8')
print(f'Backup: ...PreDiagYoY.html')

# ── HTML do diagnóstico ───────────────────────────────────────────────────────
DIAG_HTML = """
      <!-- ▼ DIAGNÓSTICO EVOLUÇÃO ANUAL -->
      <div id="yoy-diagnostico" style="margin-bottom:16px;border-radius:10px;background:rgba(34,197,94,0.04);border:0.5px solid rgba(34,197,94,0.22);overflow:hidden;">

        <!-- Header clicável -->
        <div onclick="(function(){
          var b=document.getElementById('yoy-diag-body');
          var a=document.getElementById('yoy-diag-arrow');
          var open=b.style.display!=='none';
          b.style.display=open?'none':'block';
          a.textContent=open?'▶ Ver diagnóstico':'▼ Ocultar';
        })()" style="display:flex;justify-content:space-between;align-items:center;padding:10px 16px;cursor:pointer;user-select:none;background:rgba(34,197,94,0.06);">
          <span style="font-size:9px;font-weight:800;letter-spacing:0.12em;color:#22c55e;text-transform:uppercase;">
            📋 DIAGNÓSTICO — Fonte dos Dados &amp; Metodologia de Análise
          </span>
          <span id="yoy-diag-arrow" style="font-size:9px;color:#22c55e;font-weight:700;white-space:nowrap;">▼ Ocultar</span>
        </div>

        <!-- Corpo expandido por padrão -->
        <div id="yoy-diag-body" style="display:block;padding:14px 16px 16px 16px;">

          <!-- Grid 3 colunas -->
          <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:12px;">

            <!-- ① FONTE DOS DADOS -->
            <div style="background:#0D1117;border-radius:8px;padding:12px;border-left:3px solid #22c55e;">
              <div style="font-size:9px;font-weight:800;color:#22c55e;letter-spacing:0.1em;text-transform:uppercase;margin-bottom:10px;">① Fonte dos Dados</div>

              <div style="display:flex;flex-direction:column;gap:6px;">
                <div style="background:rgba(34,197,94,0.07);border-radius:6px;padding:8px 10px;">
                  <div style="font-size:8px;font-weight:700;color:#94a3b8;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:3px;">Base principal</div>
                  <div style="font-size:10px;color:#e2e8f0;font-weight:600;">PROV_DATA — 157 distribuidores</div>
                  <div style="font-size:9px;color:#64748b;margin-top:2px;">Planilha Mestre · consolidação sell-out por provedor</div>
                </div>
                <div style="background:rgba(34,197,94,0.07);border-radius:6px;padding:8px 10px;">
                  <div style="font-size:8px;font-weight:700;color:#94a3b8;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:3px;">Canais alimentadores</div>
                  <div style="font-size:9px;color:#e2e8f0;line-height:1.6;">
                    SO_DDGAM · SO_DDGaúcha · SO_Riomed<br>
                    SO_SJoao · SO_Nissei · SO_Clamed · SO_Panvel
                  </div>
                </div>
                <div style="background:rgba(34,197,94,0.07);border-radius:6px;padding:8px 10px;">
                  <div style="font-size:8px;font-weight:700;color:#94a3b8;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:3px;">Granularidade</div>
                  <div style="font-size:9px;color:#e2e8f0;line-height:1.6;">
                    PDV-meses por distribuidor<br>
                    Série: Abr/24 → Mar/26 (24 meses)<br>
                    Oportunidade: IQVIA (CIMED + RB ativos)
                  </div>
                </div>
                <div style="background:rgba(34,197,94,0.07);border-radius:6px;padding:8px 10px;">
                  <div style="font-size:8px;font-weight:700;color:#94a3b8;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:3px;">Atualização</div>
                  <div style="font-size:9px;color:#e2e8f0;">
                    Sincronizado via <code style="background:rgba(34,197,94,0.1);padding:1px 5px;border-radius:3px;color:#22c55e;font-size:8px;">atualizar_dados.py</code><br>
                    <span style="color:#64748b;">Importa Excel → HTML em uma execução</span>
                  </div>
                </div>
              </div>
            </div>

            <!-- ② METODOLOGIA -->
            <div style="background:#0D1117;border-radius:8px;padding:12px;border-left:3px solid #06b6d4;">
              <div style="font-size:9px;font-weight:800;color:#06b6d4;letter-spacing:0.1em;text-transform:uppercase;margin-bottom:10px;">② Metodologia de Cálculo</div>

              <!-- Períodos -->
              <div style="margin-bottom:8px;">
                <div style="font-size:8px;font-weight:700;color:#475569;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:5px;">Janelas de Tempo</div>
                <div style="display:grid;grid-template-columns:1fr 1fr;gap:4px;">
                  <div style="background:rgba(148,163,184,0.07);border-radius:5px;padding:6px 8px;border-top:2px solid #94a3b8;">
                    <div style="font-size:8px;color:#94a3b8;font-weight:700;">FY25</div>
                    <div style="font-size:10px;color:#e2e8f0;font-weight:700;">Jul/24 → Mar/25</div>
                    <div style="font-size:8px;color:#475569;">9 meses · M[3..11]</div>
                  </div>
                  <div style="background:rgba(6,182,212,0.07);border-radius:5px;padding:6px 8px;border-top:2px solid #06b6d4;">
                    <div style="font-size:8px;color:#06b6d4;font-weight:700;">FY26</div>
                    <div style="font-size:10px;color:#e2e8f0;font-weight:700;">Jul/25 → Mar/26</div>
                    <div style="font-size:8px;color:#475569;">9 meses · M[15..23]</div>
                  </div>
                  <div style="background:rgba(148,163,184,0.05);border-radius:5px;padding:6px 8px;">
                    <div style="font-size:8px;color:#64748b;font-weight:700;">Q1 FY25</div>
                    <div style="font-size:9px;color:#94a3b8;">Jan–Mar/25 · M[9..11]</div>
                  </div>
                  <div style="background:rgba(6,182,212,0.05);border-radius:5px;padding:6px 8px;">
                    <div style="font-size:8px;color:#0891b2;font-weight:700;">Q1 FY26</div>
                    <div style="font-size:9px;color:#94a3b8;">Jan–Mar/26 · M[21..23]</div>
                  </div>
                </div>
              </div>

              <!-- Fórmulas -->
              <div style="font-size:8px;font-weight:700;color:#475569;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:5px;">Fórmulas</div>
              <div style="display:flex;flex-direction:column;gap:4px;">
                <div style="background:rgba(251,191,36,0.07);border-radius:5px;padding:6px 10px;font-size:9px;">
                  <span style="color:#fbbf24;font-weight:700;">Δ% Positivação</span>
                  <span style="color:#94a3b8;margin:0 4px;">=</span>
                  <span style="color:#e2e8f0;">(FY26 − FY25) / FY25 × 100</span>
                </div>
                <div style="background:rgba(251,191,36,0.07);border-radius:5px;padding:6px 10px;font-size:9px;">
                  <span style="color:#fbbf24;font-weight:700;">Oportunidade</span>
                  <span style="color:#94a3b8;margin:0 4px;">=</span>
                  <span style="color:#e2e8f0;">PDVs sem SCJ onde CIMED ou RB atuam</span>
                </div>
                <div style="background:rgba(251,191,36,0.07);border-radius:5px;padding:6px 10px;font-size:9px;">
                  <span style="color:#fbbf24;font-weight:700;">Reconquista</span>
                  <span style="color:#94a3b8;margin:0 4px;">=</span>
                  <span style="color:#e2e8f0;">Comprou FY25, parou no FY26</span>
                </div>
                <div style="background:rgba(251,191,36,0.07);border-radius:5px;padding:6px 10px;font-size:9px;">
                  <span style="color:#fbbf24;font-weight:700;">Filtro mínimo</span>
                  <span style="color:#94a3b8;margin:0 4px;">=</span>
                  <span style="color:#e2e8f0;">≥ 100 PDV-meses em FY25 ou FY26</span>
                </div>
              </div>
            </div>

            <!-- ③ COMO INTERPRETAR -->
            <div style="background:#0D1117;border-radius:8px;padding:12px;border-left:3px solid #fbbf24;">
              <div style="font-size:9px;font-weight:800;color:#fbbf24;letter-spacing:0.1em;text-transform:uppercase;margin-bottom:10px;">③ Como Interpretar</div>

              <div style="display:flex;flex-direction:column;gap:6px;">

                <!-- Leitura do Delta -->
                <div style="font-size:8px;font-weight:700;color:#475569;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:2px;">Leitura do Δ%</div>
                <div style="display:flex;align-items:flex-start;gap:8px;background:rgba(52,211,153,0.06);border-radius:6px;padding:7px 9px;">
                  <div style="width:10px;height:10px;border-radius:50%;background:#34d399;margin-top:1px;flex-shrink:0;box-shadow:0 0 5px rgba(52,211,153,0.5);"></div>
                  <div>
                    <div style="font-size:9px;color:#34d399;font-weight:700;">Δ% positivo — Crescimento</div>
                    <div style="font-size:8px;color:#64748b;line-height:1.5;">Mais PDVs compraram o produto neste período. Canal ativo e em expansão.</div>
                  </div>
                </div>
                <div style="display:flex;align-items:flex-start;gap:8px;background:rgba(239,68,68,0.06);border-radius:6px;padding:7px 9px;">
                  <div style="width:10px;height:10px;border-radius:50%;background:#ef4444;margin-top:1px;flex-shrink:0;box-shadow:0 0 5px rgba(239,68,68,0.4);"></div>
                  <div>
                    <div style="font-size:9px;color:#ef4444;font-weight:700;">Δ% negativo — Queda / Risco</div>
                    <div style="font-size:8px;color:#64748b;line-height:1.5;">Menos PDVs positivados. Possível problema de ruptura, sell-in fraco ou entrada de concorrente.</div>
                  </div>
                </div>

                <!-- Oportunidade vs Reconquista -->
                <div style="font-size:8px;font-weight:700;color:#475569;text-transform:uppercase;letter-spacing:0.08em;margin-top:4px;margin-bottom:2px;">Prioridade de Ação</div>
                <div style="display:flex;align-items:flex-start;gap:8px;background:rgba(6,182,212,0.06);border-radius:6px;padding:7px 9px;">
                  <span style="font-size:12px;margin-top:-1px;">🎯</span>
                  <div>
                    <div style="font-size:9px;color:#06b6d4;font-weight:700;">Oportunidade alta</div>
                    <div style="font-size:8px;color:#64748b;line-height:1.5;">Muitos PDVs do provedor já compram CIMED ou RB — base pronta para ativação SCJ.</div>
                  </div>
                </div>
                <div style="display:flex;align-items:flex-start;gap:8px;background:rgba(251,191,36,0.06);border-radius:6px;padding:7px 9px;">
                  <span style="font-size:12px;margin-top:-1px;">🔄</span>
                  <div>
                    <div style="font-size:9px;color:#fbbf24;font-weight:700;">Reconquista alta</div>
                    <div style="font-size:8px;color:#64748b;line-height:1.5;">PDVs que já conhecem o produto e pararam. Maior taxa de conversão — prioridade imediata.</div>
                  </div>
                </div>

                <!-- Q1 Trend -->
                <div style="margin-top:4px;background:rgba(139,92,246,0.06);border-radius:6px;padding:7px 9px;border:0.5px solid rgba(139,92,246,0.15);">
                  <div style="font-size:8px;font-weight:700;color:#a78bfa;margin-bottom:3px;">Q1 FY25 vs Q1 FY26 (Jan–Mar)</div>
                  <div style="font-size:8px;color:#64748b;line-height:1.5;">Tendência mais recente. Isola sazonalidade do início de ano — identifica aceleração ou desaceleração no trimestre mais quente do setor.</div>
                </div>

              </div>
            </div>

          </div><!-- /grid 3 cols -->
        </div><!-- /yoy-diag-body -->
      </div><!-- /yoy-diagnostico -->
      <!-- ▲ DIAGNÓSTICO EVOLUÇÃO ANUAL -->
"""

# ── Injeção: antes de <div id="prov-yoy-body"> ───────────────────────────────
ANCHOR = '<div id="prov-yoy-body">'
assert h.count(ANCHOR) == 1, f'ERRO: anchor nao unica ({h.count(ANCHOR)}x)'

h = h.replace(ANCHOR, DIAG_HTML + ANCHOR, 1)

# ── Verificações ──────────────────────────────────────────────────────────────
assert 'yoy-diagnostico'   in h
assert 'yoy-diag-body'     in h
assert 'yoy-diag-arrow'    in h
assert 'PROV_DATA'         in h
assert 'prov-yoy-body'     in h
assert 'prov-yoy-card'     in h
print('Verificações: OK')

# ── Salvar ────────────────────────────────────────────────────────────────────
DASH.write_text(h, encoding='utf-8')
shutil.copy(DASH, VER / f'Dashboard_Farma_Sul_{ts}_DiagYoY.html')
shutil.copy(DASH, DL  / f'Dashboard_FarmaSul_Giovano_{ts}.html')
print(f'Versao:    Dashboard_Farma_Sul_{ts}_DiagYoY.html')
print(f'Downloads: Dashboard_FarmaSul_Giovano_{ts}.html')
print('DONE.')
