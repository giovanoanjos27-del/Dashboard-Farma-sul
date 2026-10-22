"""
Adiciona ao card Estoque & DOH:
  1. Filtro por MARCA (no canto superior direito do header)
  2. Seção DIAGNÓSTICO no rodapé (resumo por marca + alertas críticos)

Filtros funcionam em combinação: Cliente + Marca simultaneamente.
"""

import re, shutil
from datetime import datetime
from pathlib import Path

BASE  = Path(r"C:\Users\valqu\OneDrive\Documentos\Claude\Projects\projeto Dashboard_farma_sul\Dashboard_farma_sul")
DASH  = BASE / "Dashboard_Farma_Sul_20260512_2220.html"
VER   = BASE / "versoes"
DL    = Path.home() / "Downloads"

html = DASH.read_text(encoding='utf-8')

# ── Novo renderEstoqueCard + estoqueFiltrar + helper ──────────────────────────
OLD_BLOCK_START = "function renderEstoqueCard() {"
OLD_BLOCK_END   = "\ndocument.addEventListener('DOMContentLoaded', function() {\n  renderEstoqueCard();\n});"

start = html.index(OLD_BLOCK_START)
end   = html.index(OLD_BLOCK_END) + len(OLD_BLOCK_END)
old_block = html[start:end]
print(f"Bloco antigo localizado: linhas {html[:start].count(chr(10))+1} – {html[:end].count(chr(10))+1}")

NEW_JS = r"""function renderEstoqueCard() {
  const clients = Object.keys(ESTOQUE_DATA);
  const maxDoh   = Math.max(...clients.map(c => ESTOQUE_DATA[c].doh || 0));

  // ── Coleta todas as marcas existentes nos SKUs ─────────────────────────────
  const marcaSet = new Set();
  clients.forEach(c => {
    (ESTOQUE_DATA[c].skus || []).forEach(s => { if(s.marca) marcaSet.add(s.marca); });
  });
  const marcas = ['Todos', ...Array.from(marcaSet).sort()];

  // ── Summary rows ───────────────────────────────────────────────────────────
  function buildSummaryRows(clientFilter, marcaFilter) {
    let rows = '';
    clients.forEach(name => {
      if (clientFilter && clientFilter !== 'todos' && clientFilter !== name) return;
      const d = ESTOQUE_DATA[name];
      // Se há filtro de marca, recalcula stats apenas para essa marca
      let est_total = d.est_total, so_mes = d.so_mes, doh = d.doh;
      let critico = d.critico, atencao = d.atencao, ok = d.ok;
      if (marcaFilter && marcaFilter !== 'todos') {
        const skusFilt = (d.skus || []).filter(s => s.marca === marcaFilter);
        if (skusFilt.length === 0) return; // cliente sem essa marca: omite
        est_total = skusFilt.reduce((a,s) => a + s.est, 0);
        so_mes    = skusFilt.reduce((a,s) => a + s.so, 0);
        doh       = skusFilt.length > 0 ? Math.round(skusFilt.reduce((a,s) => a + s.doh, 0) / skusFilt.length * 10)/10 : 0;
        critico   = skusFilt.filter(s => s.status.includes('CRÍTICO')).length;
        atencao   = skusFilt.filter(s => s.status.includes('ATENÇÃO')).length;
        ok        = skusFilt.filter(s => s.status.includes('OK')).length;
      }
      const color    = ESTOQUE_CLIENT_COLORS[name] || '#94a3b8';
      const dohColor = estoqueDohColor(doh);
      const dohLabel = doh !== null ? doh.toFixed(1) + 'd' : '—';
      let statusBadge = '';
      if (critico > 0) {
        statusBadge = `<span style="font-size:10px;padding:2px 7px;border-radius:4px;background:rgba(239,68,68,0.15);color:#ef4444;font-weight:700;">🔴 ${critico} crítico${critico > 1 ? 's' : ''}</span>`;
      } else if (atencao > 0) {
        statusBadge = `<span style="font-size:10px;padding:2px 7px;border-radius:4px;background:rgba(249,115,22,0.15);color:#f97316;font-weight:700;">⚠ Monitorar</span>`;
      } else {
        statusBadge = `<span style="font-size:10px;padding:2px 7px;border-radius:4px;background:rgba(52,211,153,0.15);color:#34d399;font-weight:700;">✓ Saudável</span>`;
      }
      rows += `
      <tr style="border-bottom:1px solid rgba(255,255,255,0.04);">
        <td style="padding:10px 8px;font-size:12px;color:${color};font-weight:700;white-space:nowrap;">${name}</td>
        <td style="padding:10px 8px;font-size:12px;color:#e2e8f0;text-align:right;">${est_total.toLocaleString('pt-BR')}</td>
        <td style="padding:10px 8px;font-size:12px;color:#94a3b8;text-align:right;">${so_mes.toLocaleString('pt-BR')}</td>
        <td style="padding:10px 8px;min-width:120px;">
          <div style="display:flex;align-items:center;gap:8px;">
            <span style="font-size:12px;color:${dohColor};font-weight:700;min-width:40px;">${dohLabel}</span>
            ${estoqueDohBar(doh, maxDoh)}
          </div>
        </td>
        <td style="padding:10px 8px;text-align:center;font-size:12px;color:#ef4444;">${critico || '—'}</td>
        <td style="padding:10px 8px;text-align:center;font-size:12px;color:#f97316;">${atencao || '—'}</td>
        <td style="padding:10px 8px;text-align:center;font-size:12px;color:#34d399;">${ok || '—'}</td>
        <td style="padding:10px 8px;">${statusBadge}</td>
      </tr>`;
    });
    return rows || `<tr><td colspan="8" style="padding:20px;text-align:center;color:#475569;font-size:11px;">Nenhum cliente com esta marca.</td></tr>`;
  }

  // ── Botões de filtro cliente ───────────────────────────────────────────────
  const clientBtns = ['Todos', ...clients].map((name, i) => {
    const active = i === 0 ? ' active' : '';
    const key    = name === 'Todos' ? 'todos' : name;
    return `<button class="tgl${active}" data-ef-client="${key}" onclick="estoqueFiltrar('${key}',this)" style="margin:2px 3px;">${name}</button>`;
  }).join('');

  // ── Botões de filtro marca ─────────────────────────────────────────────────
  const marcaBtns = marcas.map((m, i) => {
    const active = i === 0 ? ' active' : '';
    const key    = m === 'Todos' ? 'todos' : m;
    const lbl    = m === 'Todos' ? 'Todas as Marcas' : m;
    return `<button class="tgl${active}" data-ef-marca="${key}" onclick="estoqueFiltrarMarca('${key}',this)" style="margin:2px 3px;font-size:10px;">${lbl}</button>`;
  }).join('');

  // ── Diagnóstico por marca ──────────────────────────────────────────────────
  function buildDiagnostico() {
    // 1. Tabela resumo por marca
    const marcaStats = {};
    clients.forEach(c => {
      (ESTOQUE_DATA[c].skus || []).forEach(s => {
        if (!s.marca) return;
        if (!marcaStats[s.marca]) marcaStats[s.marca] = { est:0, so:0, dohSum:0, n:0, critico:0, atencao:0, ok:0, clientes:new Set() };
        const ms = marcaStats[s.marca];
        ms.est    += s.est;
        ms.so     += s.so;
        ms.dohSum += s.doh;
        ms.n++;
        if (s.status.includes('CRÍTICO')) ms.critico++;
        else if (s.status.includes('ATENÇÃO')) ms.atencao++;
        else ms.ok++;
        ms.clientes.add(c);
      });
    });

    const marcaOrder = Object.keys(marcaStats).sort((a,b) => marcaStats[b].critico - marcaStats[a].critico || a.localeCompare(b));
    let diagRows = marcaOrder.map(m => {
      const ms = marcaStats[m];
      const dohMed = ms.n > 0 ? Math.round(ms.dohSum / ms.n * 10)/10 : 0;
      const dohColor = estoqueDohColor(dohMed);
      const critCol = ms.critico > 0 ? '#ef4444' : '#34d399';
      const clientesList = Array.from(ms.clientes).join(', ');
      return `<tr style="border-bottom:1px solid rgba(255,255,255,0.03);">
        <td style="padding:6px 8px;font-size:11px;color:#e2e8f0;font-weight:700;">${m}</td>
        <td style="padding:6px 8px;font-size:11px;color:#e2e8f0;text-align:right;">${ms.est.toLocaleString('pt-BR')} cx</td>
        <td style="padding:6px 8px;font-size:11px;text-align:right;">
          <span style="color:${dohColor};font-weight:700;">${dohMed}d</span>
        </td>
        <td style="padding:6px 8px;font-size:11px;text-align:center;color:${critCol};font-weight:700;">${ms.critico}</td>
        <td style="padding:6px 8px;font-size:11px;text-align:center;color:#f97316;">${ms.atencao}</td>
        <td style="padding:6px 8px;font-size:10px;color:#64748b;">${clientesList}</td>
      </tr>`;
    }).join('');

    // 2. Alertas top 5 críticos
    const allSkus = [];
    clients.forEach(c => {
      (ESTOQUE_DATA[c].skus || []).forEach(s => {
        if (s.status.includes('CRÍTICO') && s.doh < 45) {
          allSkus.push({...s, cliente: c});
        }
      });
    });
    allSkus.sort((a,b) => a.doh - b.doh);
    const topAlerts = allSkus.slice(0,8);

    let alertRows = topAlerts.length === 0
      ? `<div style="padding:12px;color:#34d399;font-size:11px;">✓ Nenhum SKU em estado crítico abaixo de 45 dias.</div>`
      : topAlerts.map(s => {
          const dohColor = estoqueDohColor(s.doh);
          const clColor  = ESTOQUE_CLIENT_COLORS[s.cliente] || '#94a3b8';
          return `<div style="display:flex;align-items:center;gap:10px;padding:6px 0;border-bottom:1px solid rgba(255,255,255,0.04);">
            <span style="min-width:20px;font-size:16px;">🔴</span>
            <div style="flex:1;min-width:0;">
              <div style="font-size:10px;font-weight:700;color:#e2e8f0;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">${s.sku}</div>
              <div style="font-size:9px;color:#64748b;margin-top:1px;"><span style="color:${clColor};font-weight:700;">${s.cliente}</span> · ${s.marca}</div>
            </div>
            <div style="text-align:right;flex-shrink:0;">
              <div style="font-size:13px;font-weight:800;color:${dohColor};">${s.doh}d</div>
              <div style="font-size:9px;color:#64748b;">${s.est} cx</div>
            </div>
          </div>`;
        }).join('');

    return `
    <div id="estoque-diagnostico" style="margin-top:20px;padding-top:16px;border-top:1px solid rgba(255,255,255,0.08);">
      <div style="font-size:10px;font-weight:700;letter-spacing:0.08em;color:#fbbf24;margin-bottom:12px;">📊 DIAGNÓSTICO DE ESTOQUE</div>
      <div style="display:grid;grid-template-columns:1fr 340px;gap:20px;">

        <!-- Resumo por Marca -->
        <div>
          <div style="font-size:10px;font-weight:700;color:#94a3b8;margin-bottom:8px;text-transform:uppercase;letter-spacing:0.06em;">Resumo por Marca (todos os clientes)</div>
          <div style="overflow-x:auto;">
            <table style="width:100%;border-collapse:collapse;">
              <thead>
                <tr style="border-bottom:1px solid rgba(255,255,255,0.08);">
                  <th style="padding:5px 8px;font-size:9px;color:#475569;font-weight:700;text-transform:uppercase;text-align:left;">MARCA</th>
                  <th style="padding:5px 8px;font-size:9px;color:#475569;font-weight:700;text-transform:uppercase;text-align:right;">ESTOQUE</th>
                  <th style="padding:5px 8px;font-size:9px;color:#475569;font-weight:700;text-transform:uppercase;text-align:right;">DOH MÉD</th>
                  <th style="padding:5px 8px;font-size:9px;color:#ef4444;font-weight:700;text-align:center;">🔴</th>
                  <th style="padding:5px 8px;font-size:9px;color:#f97316;font-weight:700;text-align:center;">⚠</th>
                  <th style="padding:5px 8px;font-size:9px;color:#475569;font-weight:700;text-align:left;">CLIENTES</th>
                </tr>
              </thead>
              <tbody>${diagRows}</tbody>
            </table>
          </div>
        </div>

        <!-- Alertas críticos -->
        <div>
          <div style="font-size:10px;font-weight:700;color:#94a3b8;margin-bottom:8px;text-transform:uppercase;letter-spacing:0.06em;">⚡ SKUs Críticos — DOH &lt; 45d</div>
          <div style="background:rgba(239,68,68,0.04);border:0.5px solid rgba(239,68,68,0.15);border-radius:8px;padding:10px;">
            ${alertRows}
          </div>
          ${topAlerts.length > 0 ? `<div style="margin-top:6px;font-size:9px;color:#475569;font-style:italic;">* SKUs com risco de ruptura. Reposição urgente recomendada.</div>` : ''}
        </div>

      </div>
    </div>`;
  }

  // ── Injetar HTML no card ───────────────────────────────────────────────────
  document.getElementById('estoque-card').innerHTML = `
    <!-- Card Header com filtro de marca -->
    <div class="card-header" style="margin-bottom:16px;display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:12px;">
      <div>
        <div style="font-size:10px;font-weight:700;letter-spacing:0.1em;color:#34d399;margin-bottom:4px;">ESTOQUE &amp; DOH</div>
        <div class="card-title">📦 Estoque &amp; DOH — Por Cliente · Ref. Abr/2026</div>
        <div class="card-sub">Estoque em caixas · Último SO fechado · Days On Hand</div>
      </div>
      <!-- Filtro por Marca -->
      <div style="flex-shrink:0;">
        <div style="font-size:9px;font-weight:700;color:#475569;text-transform:uppercase;letter-spacing:0.06em;margin-bottom:5px;">FILTRAR POR MARCA</div>
        <div id="estoque-marca-btns" style="display:flex;flex-wrap:wrap;gap:0;max-width:460px;">
          ${marcaBtns}
        </div>
      </div>
    </div>

    <!-- Filtro por Cliente -->
    <div style="margin-bottom:14px;display:flex;flex-wrap:wrap;gap:0;">
      ${clientBtns}
    </div>

    <!-- Summary table -->
    <div style="overflow-x:auto;margin-bottom:4px;">
      <table style="width:100%;border-collapse:collapse;">
        <thead>
          <tr style="border-bottom:1px solid rgba(255,255,255,0.08);">
            <th style="padding:6px 8px;font-size:9px;color:#475569;font-weight:700;text-transform:uppercase;text-align:left;">CLIENTE</th>
            <th style="padding:6px 8px;font-size:9px;color:#475569;font-weight:700;text-transform:uppercase;text-align:right;">ESTOQUE (cx)</th>
            <th style="padding:6px 8px;font-size:9px;color:#475569;font-weight:700;text-transform:uppercase;text-align:right;">SO REF/MÊS</th>
            <th style="padding:6px 8px;font-size:9px;color:#475569;font-weight:700;text-transform:uppercase;min-width:140px;">DOH</th>
            <th style="padding:6px 8px;font-size:9px;color:#ef4444;font-weight:700;text-align:center;">🔴 CRÍTICO</th>
            <th style="padding:6px 8px;font-size:9px;color:#f97316;font-weight:700;text-align:center;">⚠ ATENÇÃO</th>
            <th style="padding:6px 8px;font-size:9px;color:#34d399;font-weight:700;text-align:center;">✓ OK</th>
            <th style="padding:6px 8px;font-size:9px;color:#475569;font-weight:700;text-transform:uppercase;text-align:left;">STATUS</th>
          </tr>
        </thead>
        <tbody id="estoque-summary-tbody">
          ${buildSummaryRows('todos', 'todos')}
        </tbody>
      </table>
    </div>

    <!-- Detail panel (SKU-level) -->
    <div id="estoque-detail-panel" style="display:none;margin-top:16px;padding:14px;background:rgba(255,255,255,0.02);border-radius:8px;border:0.5px solid rgba(255,255,255,0.06);">
      <div id="estoque-detail-title" style="font-size:11px;font-weight:700;color:#e2e8f0;margin-bottom:10px;"></div>
      <div style="overflow-x:auto;">
        <table style="width:100%;border-collapse:collapse;">
          <thead>
            <tr style="border-bottom:1px solid rgba(255,255,255,0.08);">
              <th style="padding:5px 8px;font-size:9px;color:#475569;font-weight:700;text-transform:uppercase;text-align:left;white-space:nowrap;">MARCA</th>
              <th style="padding:5px 8px;font-size:9px;color:#475569;font-weight:700;text-transform:uppercase;text-align:left;">SKU</th>
              <th style="padding:5px 8px;font-size:9px;color:#475569;font-weight:700;text-transform:uppercase;text-align:right;">ESTOQUE</th>
              <th style="padding:5px 8px;font-size:9px;color:#475569;font-weight:700;text-transform:uppercase;text-align:right;">SO/MÊS</th>
              <th style="padding:5px 8px;font-size:9px;color:#475569;font-weight:700;text-transform:uppercase;min-width:100px;">DOH</th>
              <th style="padding:5px 8px;font-size:9px;color:#475569;font-weight:700;text-transform:uppercase;text-align:left;">STATUS</th>
            </tr>
          </thead>
          <tbody id="estoque-detail-tbody"></tbody>
        </table>
      </div>
    </div>

    <!-- DOH Legend -->
    <div style="margin-top:14px;padding-top:10px;border-top:1px solid rgba(255,255,255,0.06);display:flex;flex-wrap:wrap;gap:12px;align-items:center;">
      <span style="font-size:9px;color:#475569;font-weight:700;text-transform:uppercase;letter-spacing:0.05em;">Legenda DOH:</span>
      <span style="font-size:10px;display:flex;align-items:center;gap:4px;"><span style="display:inline-block;width:10px;height:10px;border-radius:2px;background:#ef4444;"></span><span style="color:#94a3b8;">&lt;30d = Crítico</span></span>
      <span style="font-size:10px;display:flex;align-items:center;gap:4px;"><span style="display:inline-block;width:10px;height:10px;border-radius:2px;background:#f97316;"></span><span style="color:#94a3b8;">30–60d = Atenção</span></span>
      <span style="font-size:10px;display:flex;align-items:center;gap:4px;"><span style="display:inline-block;width:10px;height:10px;border-radius:2px;background:#fbbf24;"></span><span style="color:#94a3b8;">60–90d = Monitorar</span></span>
      <span style="font-size:10px;display:flex;align-items:center;gap:4px;"><span style="display:inline-block;width:10px;height:10px;border-radius:2px;background:#34d399;"></span><span style="color:#94a3b8;">&gt;90d = OK</span></span>
    </div>

    <!-- Diagnóstico -->
    ${buildDiagnostico()}
  `;

  // ── Guarda funções de build no escopo para re-uso pelos filtros ───────────
  window._estoqueBuildSummary = buildSummaryRows;
  window._estoqueBuildDiag    = buildDiagnostico;
}

// ── Filtro por CLIENTE ────────────────────────────────────────────────────────
function estoqueFiltrar(key, btn) {
  document.querySelectorAll('#estoque-card [data-ef-client]').forEach(b => b.classList.remove('active'));
  btn.classList.add('active');
  window._estoqueClienteAtivo = key;

  const marcaAtiva = window._estoqueMarcaAtiva || 'todos';
  _estoqueAtualizaSummary(key, marcaAtiva);

  const detail = document.getElementById('estoque-detail-panel');
  if (key === 'todos') {
    detail.style.display = 'none';
    return;
  }
  _estoqueAbreDetalhe(key, marcaAtiva);
}

// ── Filtro por MARCA ──────────────────────────────────────────────────────────
function estoqueFiltrarMarca(marca, btn) {
  document.querySelectorAll('#estoque-card [data-ef-marca]').forEach(b => b.classList.remove('active'));
  btn.classList.add('active');
  window._estoqueMarcaAtiva = marca;

  const clienteAtivo = window._estoqueClienteAtivo || 'todos';
  _estoqueAtualizaSummary(clienteAtivo, marca);

  if (clienteAtivo !== 'todos') {
    _estoqueAbreDetalhe(clienteAtivo, marca);
  }
}

// ── Atualiza summary table ────────────────────────────────────────────────────
function _estoqueAtualizaSummary(clienteAtivo, marcaAtiva) {
  if (!window._estoqueBuildSummary) return;
  const tbody = document.getElementById('estoque-summary-tbody');
  if (tbody) tbody.innerHTML = window._estoqueBuildSummary(clienteAtivo, marcaAtiva);
}

// ── Abre painel de detalhe SKU ────────────────────────────────────────────────
function _estoqueAbreDetalhe(clienteKey, marcaKey) {
  const detail     = document.getElementById('estoque-detail-panel');
  const detailTitle= document.getElementById('estoque-detail-title');
  const tbody      = document.getElementById('estoque-detail-tbody');
  const d = ESTOQUE_DATA[clienteKey];
  if (!d) return;

  if (!d.skus || d.skus.length === 0) {
    detail.style.display = 'block';
    detailTitle.textContent = clienteKey + ' — Detalhamento de SKUs (em breve)';
    tbody.innerHTML = '<tr><td colspan="6" style="padding:20px;text-align:center;color:#475569;font-size:11px;">Detalhamento de SKUs será adicionado em próxima atualização.</td></tr>';
    return;
  }

  // Aplica filtro de marca se ativo
  let skus = d.skus;
  if (marcaKey && marcaKey !== 'todos') {
    skus = skus.filter(s => s.marca === marcaKey);
  }

  const color   = ESTOQUE_CLIENT_COLORS[clienteKey] || '#94a3b8';
  const maxDoh  = Math.max(...skus.filter(s => s.doh !== null).map(s => s.doh), 1);
  const marcaLabel = (marcaKey && marcaKey !== 'todos') ? ` · Marca: ${marcaKey}` : '';
  detailTitle.innerHTML = `<span style="color:${color}">${clienteKey}</span>${marcaLabel} — ${skus.length} SKUs · Ref. ${d.data_ref}`;

  if (skus.length === 0) {
    tbody.innerHTML = '<tr><td colspan="6" style="padding:20px;text-align:center;color:#475569;font-size:11px;">Nenhum SKU desta marca para este cliente.</td></tr>';
    detail.style.display = 'block';
    return;
  }

  tbody.innerHTML = skus.map(s => {
    const dohColor = estoqueDohColor(s.doh);
    const dohLabel = s.doh !== null ? s.doh.toFixed(1) + 'd' : '—';
    return `<tr style="border-bottom:1px solid rgba(255,255,255,0.04);">
      <td style="padding:7px 8px;font-size:10px;color:#94a3b8;font-weight:700;white-space:nowrap;">${s.marca}</td>
      <td style="padding:7px 8px;font-size:10px;color:#cbd5e1;max-width:320px;">${s.sku}</td>
      <td style="padding:7px 8px;font-size:10px;color:#e2e8f0;text-align:right;">${s.est.toLocaleString('pt-BR')}</td>
      <td style="padding:7px 8px;font-size:10px;color:#94a3b8;text-align:right;">${s.so.toLocaleString('pt-BR')}</td>
      <td style="padding:7px 8px;min-width:100px;">
        <div style="display:flex;align-items:center;gap:6px;">
          <span style="font-size:10px;color:${dohColor};font-weight:700;min-width:36px;">${dohLabel}</span>
          ${estoqueDohBar(s.doh, maxDoh)}
        </div>
      </td>
      <td style="padding:7px 8px;font-size:10px;color:${dohColor};white-space:nowrap;">${s.status}</td>
    </tr>`;
  }).join('');

  detail.style.display = 'block';
}

document.addEventListener('DOMContentLoaded', function() {
  renderEstoqueCard();
});"""

print("Novo bloco JS pronto.")

# ── Substituição ──────────────────────────────────────────────────────────────
if OLD_BLOCK_START not in html:
    print("ERRO: ponto de início não encontrado!")
    exit(1)

new_html = html[:start] + NEW_JS + html[end:]
print(f"HTML: {len(html):,} -> {len(new_html):,} chars")

# ── Salvar versão + principal ─────────────────────────────────────────────────
ts = datetime.now().strftime('%Y%m%d_%H%M')
versao = VER / f"Dashboard_Farma_Sul_{ts}_EstoqueMarcaFilter.html"
shutil.copy(DASH, versao)
print(f"Versão salva: {versao.name}")

DASH.write_text(new_html, encoding='utf-8')
print(f"Dashboard atualizado: {DASH.name}")

dl = DL / f"Dashboard_FarmaSul_Giovano_{ts}.html"
shutil.copy(DASH, dl)
print(f"Downloads: {dl.name}")
print("\nDONE.")
