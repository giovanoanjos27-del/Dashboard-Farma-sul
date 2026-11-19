"""
1. Adiciona filtro por UF ao card Intocáveis (Cobertura + novo Sell In)
2. Insere card Intocáveis no Sell In (abaixo da Positivação Mensal)
3. Wires renderIntocSellinCard() ao initSellin()
"""

import re, shutil
from datetime import datetime
from pathlib import Path

BASE = Path(r"C:\Users\valqu\OneDrive\Documentos\Claude\Projects\projeto Dashboard_farma_sul\Dashboard_farma_sul")
DASH = BASE / "Dashboard_Farma_Sul_20260512_2220.html"
VER  = BASE / "versoes"
DL   = Path.home() / "Downloads"

html = DASH.read_text(encoding='utf-8')
orig_len = len(html)

# ══════════════════════════════════════════════════════════════
# 1. ADICIONAR JS: estado + funções para card Sell In
# ══════════════════════════════════════════════════════════════
NEW_JS = r"""
/* ═══════ INTOCÁVEIS — SELL IN (com filtro UF) ═══════ */
var _intocSellinDist = 'gam';
var _intocSellinSku  = 'kids200';
var _intocSellinUF   = 'todos';

function setIntocSellinDist(v, btn){
  _intocSellinDist = v;
  btn.closest('.toggle-group').querySelectorAll('.tgl').forEach(function(b){b.classList.remove('active','blue');});
  btn.classList.add('active','blue');
  _intocSellinUF = 'todos'; // reset UF ao trocar distribuidor
  renderIntocSellinCard();
}

function setIntocSellinUF(uf, btn){
  _intocSellinUF = uf;
  document.querySelectorAll('#intoc-sellin-uf-row button').forEach(function(b){
    b.style.background = b.getAttribute('data-uf') === uf ? 'rgba(251,191,36,0.18)' : 'transparent';
    b.style.color      = b.getAttribute('data-uf') === uf ? '#fbbf24' : '#64748b';
    b.style.borderColor= b.getAttribute('data-uf') === uf ? 'rgba(251,191,36,0.4)' : 'rgba(255,255,255,0.07)';
  });
  renderIntocSellinCard();
}

function setIntocSellinSku(sku){
  _intocSellinSku = sku;
  renderIntocSellinCard();
}

function renderIntocSellinCard(){
  var bodyEl  = document.getElementById('intoc-sellin-body');
  var ufRow   = document.getElementById('intoc-sellin-uf-row');
  var kpiEl   = document.getElementById('intoc-sellin-kpi');
  if(!bodyEl) return;

  var dnData  = _intocSellinDist === 'gam' ? DN_INTOC_GAM : DN_INTOC_GCH;
  var skuKey  = _intocSellinSku;
  var ufFilt  = _intocSellinUF;

  /* ── Coleta UFs disponíveis ── */
  var allUFs = [];
  var keys = Object.keys(dnData).filter(function(k){ return k !== 'soma'; });
  keys.forEach(function(k){
    (dnData[k].ufs || []).forEach(function(u){ if(allUFs.indexOf(u.uf) < 0) allUFs.push(u.uf); });
  });
  // ordena por DN% do skuKey selecionado
  var skuUfOrder = ((dnData[skuKey] || dnData['kids200']).ufs || []).map(function(u){ return u.uf; });
  allUFs.sort(function(a,b){ return skuUfOrder.indexOf(a) - skuUfOrder.indexOf(b); });

  /* ── Botões de filtro UF ── */
  if(ufRow){
    var UFColors = {SC:'#fb923c',SP:'#34d399',PR:'#3b82f6',RS:'#2dd4bf',MS:'#888',GO:'#a78bfa',MT:'#f97316'};
    var ufBtns = '<span style="font-size:9px;font-weight:700;color:#475569;text-transform:uppercase;letter-spacing:0.06em;white-space:nowrap;margin-right:4px;">ESTADO:</span>';
    ['todos'].concat(allUFs).forEach(function(uf){
      var isActive = uf === ufFilt;
      var col  = uf === 'todos' ? '#94a3b8' : (UFColors[uf] || '#888');
      var bg   = isActive ? 'rgba(251,191,36,0.18)' : 'transparent';
      var bdc  = isActive ? 'rgba(251,191,36,0.4)'  : 'rgba(255,255,255,0.07)';
      var tc   = isActive ? '#fbbf24' : col;
      var lbl  = uf === 'todos' ? 'Todos' : uf;
      ufBtns += '<button data-uf="'+uf+'" onclick="setIntocSellinUF(\''+uf+'\',this)"'
        +' style="font-size:10px;font-weight:700;padding:3px 11px;border-radius:6px;border:0.5px solid '+bdc+';cursor:pointer;background:'+bg+';color:'+tc+';transition:all 0.15s;">'+lbl+'</button>';
    });
    ufRow.innerHTML = ufBtns;
  }

  /* ── SKU sub-tabs ── */
  var nomes = {soma:'Somatório', kids200:'Kids 200ML', spray170:'Spray 170ML', locao200:'Loção 200ML'};
  var tabs = ['soma','kids200','spray170','locao200'].map(function(k){
    var isAct = k === skuKey;
    var bg  = isAct ? 'rgba(251,191,36,0.15)' : 'transparent';
    var col = isAct ? '#fbbf24' : '#64748b';
    var bdc = isAct ? 'rgba(251,191,36,0.3)' : 'rgba(255,255,255,0.07)';
    var icon = k === 'soma' ? '∑' : '🏆';
    return '<button onclick="setIntocSellinSku(\''+k+'\')" style="font-size:10px;font-weight:700;padding:4px 12px;border-radius:6px;border:0.5px solid '+bdc+';cursor:pointer;background:'+bg+';color:'+col+';">'+icon+' '+nomes[k]+'</button>';
  }).join('');
  var tabsHtml = '<div style="display:flex;gap:6px;margin-bottom:14px;flex-wrap:wrap;">'+tabs+'</div>';

  /* ── KPI strip de UF selecionada ── */
  var kpiHtml = '';
  if(ufFilt !== 'todos' && kpiEl){
    var UFColors2 = {SC:'#fb923c',SP:'#34d399',PR:'#3b82f6',RS:'#2dd4bf',MS:'#888',GO:'#a78bfa'};
    var col2 = UFColors2[ufFilt] || '#fbbf24';
    var allSkuData = ['kids200','spray170','locao200'].map(function(k){
      var s = (dnData[k] || {}).ufs || [];
      var u = s.filter(function(x){ return x.uf === ufFilt; })[0];
      return { nome: nomes[k], pdvs: u ? u.pdvs : 0, total: u ? u.total : 0, dn: u ? u.dn : 0 };
    });
    kpiHtml = '<div style="margin-top:12px;padding:12px 16px;background:rgba(251,191,36,0.04);border-radius:10px;border:0.5px solid rgba(251,191,36,0.2);">'
      +'<div style="font-size:10px;font-weight:700;color:'+col2+';margin-bottom:10px;letter-spacing:0.06em;">📍 DETALHE — '+ufFilt+'</div>'
      +'<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:10px;">'
      +allSkuData.map(function(s){
        var gap = s.total - s.pdvs;
        var dohColor = s.dn >= 50 ? '#34d399' : s.dn >= 35 ? '#fbbf24' : '#ef4444';
        return '<div style="background:#161B22;border-radius:8px;padding:12px;">'
          +'<div style="font-size:9px;font-weight:700;color:#475569;margin-bottom:6px;text-transform:uppercase;">'+s.nome+'</div>'
          +'<div style="font-size:20px;font-weight:800;color:'+dohColor+';line-height:1;">'+s.dn.toFixed(1)+'%</div>'
          +'<div style="font-size:10px;color:#94a3b8;margin-top:4px;">'+s.pdvs+' positivados / '+s.total+' PDVs</div>'
          +'<div style="font-size:10px;color:#ef4444;margin-top:2px;font-weight:600;">'+gap+' PDVs sem SKU</div>'
          +'</div>';
      }).join('')
      +'</div>'
      +'</div>';
    kpiEl.style.display = 'block';
    kpiEl.innerHTML = kpiHtml;
  } else if(kpiEl){
    kpiEl.style.display = 'none';
  }

  /* ── Barras por UF ── */
  var bodyHtml = '';
  var UFColors3 = {SC:'#fb923c',SP:'#34d399',PR:'#3b82f6',RS:'#2dd4bf',MS:'#888',GO:'#a78bfa',MT:'#f97316'};

  if(skuKey === 'soma'){
    var soma = dnData['soma'];
    bodyHtml += '<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-bottom:16px;">'
      +'<div style="background:#161B22;border-radius:8px;padding:12px;border-top:2px solid #fbbf24;">'
        +'<div style="font-size:9px;font-weight:700;color:#475569;margin-bottom:5px;text-transform:uppercase;">PDVs ≥ 1 Intocável</div>'
        +'<div style="font-size:22px;font-weight:800;color:#fbbf24;line-height:1;">'+soma.algum.toLocaleString('pt-BR')+'</div>'
        +'<div style="font-size:10px;color:#94a3b8;margin-top:3px;">'+soma.dnAlgum.toFixed(1)+'% DN</div></div>'
      +'<div style="background:#161B22;border-radius:8px;padding:12px;border-top:2px solid #2dd4bf;">'
        +'<div style="font-size:9px;font-weight:700;color:#475569;margin-bottom:5px;text-transform:uppercase;">PDVs ≥ 2 Intocáveis</div>'
        +'<div style="font-size:22px;font-weight:800;color:#2dd4bf;line-height:1;">'+soma.dois.toLocaleString('pt-BR')+'</div>'
        +'<div style="font-size:10px;color:#94a3b8;margin-top:3px;">'+soma.dnDois.toFixed(1)+'% DN</div></div>'
      +'<div style="background:#161B22;border-radius:8px;padding:12px;border-top:2px solid #34d399;">'
        +'<div style="font-size:9px;font-weight:700;color:#475569;margin-bottom:5px;text-transform:uppercase;">PDVs com os 3</div>'
        +'<div style="font-size:22px;font-weight:800;color:#34d399;line-height:1;">'+soma.todos.toLocaleString('pt-BR')+'</div>'
        +'<div style="font-size:10px;color:#94a3b8;margin-top:3px;">'+soma.dnTodos.toFixed(1)+'% DN Full Portfolio</div></div>'
      +'</div>';
    var ufsSoma = ufFilt === 'todos' ? soma.ufs : soma.ufs.filter(function(u){ return u.uf === ufFilt; });
    ufsSoma.forEach(function(u){
      var col = UFColors3[u.uf] || '#888';
      var pct = Math.round(u.dn);
      bodyHtml += '<div class="bar-item" data-togglesel="1">'
        +'<div class="bar-item-header">'
        +'<span class="uf-badge" style="background:'+col+'22;color:'+col+';font-size:10px;padding:2px 7px;">'+u.uf+'</span>'
        +'<span class="bar-name">'+u.total.toLocaleString('pt-BR')+' PDVs total</span>'
        +'<span class="u-lbl-muted">'+u.pdvs.toLocaleString('pt-BR')+' PDVs</span>'
        +'<span class="bar-val" style="color:#fbbf24">'+u.dn.toFixed(1)+'% DN</span>'
        +'</div>'
        +'<div class="bar-track"><div class="bar-fill" style="width:0%;background:#fbbf24;" data-pct="'+pct+'"></div></div>'
        +'</div>';
    });
  } else {
    var sku = dnData[skuKey];
    if(!sku){ bodyEl.innerHTML = tabsHtml+'<div style="padding:20px;text-align:center;color:#475569;">Sem dados.</div>'; return; }
    var ufsFiltered = ufFilt === 'todos' ? sku.ufs : sku.ufs.filter(function(u){ return u.uf === ufFilt; });
    ufsFiltered.forEach(function(u){
      var col = UFColors3[u.uf] || '#888';
      var pct = Math.round(u.dn);
      var gap = u.total - u.pdvs;
      bodyHtml += '<div class="bar-item" data-togglesel="1">'
        +'<div class="bar-item-header">'
        +'<span class="uf-badge" style="background:'+col+'22;color:'+col+';font-size:10px;padding:2px 7px;">'+u.uf+'</span>'
        +'<span class="bar-name">'+u.total.toLocaleString('pt-BR')+' PDVs total</span>'
        +'<span class="u-lbl-muted">'+u.pdvs.toLocaleString('pt-BR')+' positivados</span>'
        +'<span class="bar-val" style="color:#fbbf24">'+u.dn.toFixed(1)+'% DN</span>'
        +'<span style="font-size:10px;color:#ef4444;margin-left:8px;">'+gap+' sem SKU</span>'
        +'</div>'
        +'<div class="bar-track"><div class="bar-fill" style="width:0%;background:#fbbf24;" data-pct="'+pct+'"></div></div>'
        +'</div>';
    });
    if(ufsFiltered.length === 0){
      bodyHtml = '<div style="padding:20px;text-align:center;color:#475569;font-size:11px;">Nenhum dado para este filtro.</div>';
    }
  }

  bodyEl.innerHTML = tabsHtml + bodyHtml;

  // Anima barras
  setTimeout(function(){
    bodyEl.querySelectorAll('.bar-fill[data-pct]').forEach(function(b){
      b.style.transition = 'width 0.6s ease';
      b.style.width = b.getAttribute('data-pct') + '%';
    });
  }, 50);
}
"""

# Inserir novo JS antes do DOMContentLoaded ou antes de initSellin
ANCHOR_JS = '\nfunction initSellin(){'
if ANCHOR_JS not in html:
    print("ERRO: anchor JS nao encontrado")
    exit(1)
html = html.replace(ANCHOR_JS, NEW_JS + ANCHOR_JS, 1)
print("JS adicionado: renderIntocSellinCard + estado + helpers")

# ══════════════════════════════════════════════════════════════
# 2. ADICIONAR renderIntocSellinCard() ao initSellin()
# ══════════════════════════════════════════════════════════════
OLD_INIT = '''  // Evolução Mensal de Positivação GAM + Gaúcha
  setTimeout(function(){ if(typeof renderMensalPos==='function') renderMensalPos(); }, 150);
}'''
NEW_INIT = '''  // Evolução Mensal de Positivação GAM + Gaúcha
  setTimeout(function(){ if(typeof renderMensalPos==='function') renderMensalPos(); }, 150);
  // Intocáveis × Distribuição Numérica
  setTimeout(function(){ if(typeof renderIntocSellinCard==='function') renderIntocSellinCard(); }, 200);
}'''
if OLD_INIT not in html:
    print("ERRO: initSellin fim nao encontrado")
    exit(1)
html = html.replace(OLD_INIT, NEW_INIT, 1)
print("initSellin(): renderIntocSellinCard() adicionado")

# ══════════════════════════════════════════════════════════════
# 3. HTML DO CARD SELL IN — inserir após card positivação mensal
# ══════════════════════════════════════════════════════════════
CARD_HTML = """
<!-- INTOCÁVEIS × DISTRIBUIÇÃO NUMÉRICA — SELL IN -->
<div id="intoc-sellin-card" class="card full" style="margin-bottom:14px;">
  <div class="card-header" style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:12px;margin-bottom:16px;">
    <div>
      <div style="font-size:10px;font-weight:700;letter-spacing:0.1em;color:#fbbf24;margin-bottom:4px;">🏆 INTOCÁVEIS × CARTEIRA DE CLIENTES</div>
      <div class="card-title">Distribuição Numérica dos 3 SKUs Intocáveis</div>
      <div class="card-sub">OFF Loção 200ml · OFF Spray 170ml · OFF Kids 200ml · DN% por estado</div>
    </div>
    <div class="toggle-group">
      <button class="tgl active blue" onclick="setIntocSellinDist('gam',this)">DD-GAM</button>
      <button class="tgl" onclick="setIntocSellinDist('gaucha',this)">DD-Gaúcha</button>
    </div>
  </div>
  <!-- Filtro UF -->
  <div id="intoc-sellin-uf-row" style="display:flex;flex-wrap:wrap;gap:4px;align-items:center;margin-bottom:14px;"></div>
  <!-- Corpo: SKU tabs + barras -->
  <div id="intoc-sellin-body"></div>
  <!-- KPI detalhe quando UF selecionada -->
  <div id="intoc-sellin-kpi" style="display:none;"></div>
</div>
"""

ANCHOR_HTML = '</div>\n\n\n\n  <!-- VERBAS -->'
if ANCHOR_HTML not in html:
    ANCHOR_HTML = '</div>\n\n\n  <!-- VERBAS -->'
if ANCHOR_HTML not in html:
    ANCHOR_HTML = '</div>\n\n  <!-- VERBAS -->'
if ANCHOR_HTML not in html:
    print("ERRO: ancora HTML para inserção nao encontrada!")
    exit(1)

# IMPORTANTE: preservar o </div> de fechamento do card anterior
html = html.replace(ANCHOR_HTML, '</div>' + CARD_HTML + '\n\n\n\n  <!-- VERBAS -->', 1)
print("Card Intocáveis inserido no Sell In (abaixo do card de Positivação)")

# ══════════════════════════════════════════════════════════════
# 4. SALVAR
# ══════════════════════════════════════════════════════════════
ts = datetime.now().strftime('%Y%m%d_%H%M')
versao = VER / f"Dashboard_Farma_Sul_{ts}_IntocSellin.html"
shutil.copy(DASH, versao)
print(f"\nVersao salva: {versao.name}")

DASH.write_text(html, encoding='utf-8')
print(f"Dashboard: {len(html):,} chars (era {orig_len:,})")

dl = DL / f"Dashboard_FarmaSul_Giovano_{ts}.html"
shutil.copy(DASH, dl)
print(f"Downloads: {dl.name}")
print("\nDONE.")
