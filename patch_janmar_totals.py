"""
patch_janmar_totals.py
1. Injeta campos mensais reais (jan25_val..janmar26_un) no FYTD_MARKET_TOTAL
   para todos os 72 mercados.
2. Corrige renderMSO2: Total Mercado usa FYTD_MARKET_TOTAL em vez de somar
   apenas as 5 marcas SCJ.
3. Corrige renderMSO3: Total Mercado FYTD usa os valores corretos ja existentes.
"""

import json, re, shutil
from datetime import datetime
from pathlib import Path

SRC      = r"C:\Users\valqu\OneDrive\Documentos\Claude\Projects\projeto Dashboard_farma_sul\Dashboard_farma_sul\Dashboard_Farma_Sul_20260512_2220.html"
VERS_DIR = r"C:\Users\valqu\OneDrive\Documentos\Claude\Projects\projeto Dashboard_farma_sul\Dashboard_farma_sul\versoes"
DL_DIR   = r"C:\Users\valqu\Downloads"
TOTALS   = r"C:\Users\valqu\OneDrive\Documentos\Claude\Projects\projeto Dashboard_farma_sul\janmar_market_totals.json"

ts   = datetime.now().strftime('%Y%m%d_%H%M')
VERS = fr"{VERS_DIR}\Dashboard_Farma_Sul_{ts}_JanMarTotais.html"
DL   = fr"{DL_DIR}\Dashboard_FarmaSul_Giovano_{ts}.html"

print("Lendo HTML...")
with open(SRC, 'r', encoding='utf-8') as f:
    html = f.read()

print("Lendo totais extraidos...")
with open(TOTALS, 'r', encoding='utf-8') as f:
    totals = json.load(f)

ok = []
err = []

# ─── PASSO 1: Atualizar FYTD_MARKET_TOTAL com campos mensais ─────────────────
# Cada entrada tem o padrao: 'MKT_NAME': {fytd25_val:X,...,fytd26_un:Y},
# Vamos adicionar os campos mensais no final do objeto

def make_monthly_fields(mkt_data):
    """Retorna string com os campos mensais a adicionar."""
    d = mkt_data
    fields = (
        f",jan25_val:{d['jan25_val']}"
        f",fev25_val:{d['fev25_val']}"
        f",mar25_val:{d['mar25_val']}"
        f",janmar25_val:{d['janmar25_val']}"
        f",jan26_val:{d['jan26_val']}"
        f",fev26_val:{d['fev26_val']}"
        f",mar26_val:{d['mar26_val']}"
        f",janmar26_val:{d['janmar26_val']}"
        f",jan25_un:{d['jan25_un']}"
        f",fev25_un:{d['fev25_un']}"
        f",mar25_un:{d['mar25_un']}"
        f",janmar25_un:{d['janmar25_un']}"
        f",jan26_un:{d['jan26_un']}"
        f",fev26_un:{d['fev26_un']}"
        f",mar26_un:{d['mar26_un']}"
        f",janmar26_un:{d['janmar26_un']}"
    )
    return fields

updated_mkts = 0
missing_mkts = []

for mkt_name, mkt_data in totals.items():
    monthly = make_monthly_fields(mkt_data)

    # Buscar a entrada no HTML:
    # Padrao: 'MKT_NAME': {...,fytd26_un:NUM},
    # Queremos substituir a parte final "},\n" por ",<monthly>},\n"

    # Escapar caracteres especiais no nome do mercado para regex
    escaped = re.escape(mkt_name)

    # Padrao: encontrar o objeto do mercado que termina com fytd26_un:NUMERO}
    pat = rf"('{escaped}': \{{[^}}]*fytd26_un:[0-9.]+)\}}"

    def repl(m, monthly=monthly):
        existing = m.group(1)
        # Verificar se ja tem os campos mensais
        if 'janmar25_val' in existing:
            return m.group(0)  # ja tem, nao alterar
        return existing + monthly + '}'

    new_html, count = re.subn(pat, repl, html)
    if count > 0:
        html = new_html
        updated_mkts += 1
        ok.append(f'FYTD_MARKET_TOTAL {mkt_name}')
    else:
        missing_mkts.append(mkt_name)

if missing_mkts:
    print(f"  AVISO: {len(missing_mkts)} mercados nao encontrados no FYTD_MARKET_TOTAL:")
    for m in missing_mkts[:5]: print(f"    - {m}")
print(f"  Mercados atualizados: {updated_mkts}")

# ─── PASSO 2: Corrigir renderMSO2 — Total Mercado ────────────────────────────
# Substituir o bloco que soma as 5 marcas SCJ pelo uso do FYTD_MARKET_TOTAL

OLD_MSO2_BLOCK = """    var nbv = NIELSEN_BRAND_VAL[mkt];
    if(!nbv){
      mktTotalEl.innerHTML = '';
    } else {
      var bList2 = ['OFF!','EXPOSIS','XO INSETO','SUPER REPELEX','SBP'];
      var acum25v = 0, acum26v = 0; // R$MM acumulado Jan+Fev+Mar
      var acum25u = 0, acum26u = 0; // Unidades acumulado Jan+Fev+Mar
      var brandAcum = []; // por marca para tooltip
      bList2.forEach(function(b){
        var bd = nbv[b]; if(!bd) return;
        var v25 = (bd.jan25_val||0)+(bd.fev25_val||0)+(bd.mar25_val||0);
        var v26 = (bd.jan_val||0)+(bd.fev_val||0)+(bd.mar_val||0);
        var u25 = (bd.jan25_un||0)+(bd.fev25_un||0)+(bd.mar25_un||0);
        var u26 = (bd.jan_un||0)+(bd.fev_un||0)+(bd.mar_un||0);
        acum25v += v25; acum26v += v26;
        acum25u += u25; acum26u += u26;
        brandAcum.push({b:b, v25:Math.round(v25*100)/100, v26:Math.round(v26*100)/100,
          u25:Math.round(u25), u26:Math.round(u26)});
      });
      acum25v = Math.round(acum25v*100)/100;
      acum26v = Math.round(acum26v*100)/100;
      acum25u = Math.round(acum25u);
      acum26u = Math.round(acum26u);"""

NEW_MSO2_BLOCK = """    var nbv = NIELSEN_BRAND_VAL[mkt];
    var fytMkt = (typeof FYTD_MARKET_TOTAL !== 'undefined') ? FYTD_MARKET_TOTAL[mkt] : null;
    if(!nbv && !fytMkt){
      mktTotalEl.innerHTML = '';
    } else {
      // Total real do mercado (todas as marcas, fonte: NielsenIQ 1-Tabela-1)
      var acum25v = fytMkt ? (fytMkt.janmar25_val||0) : 0;
      var acum26v = fytMkt ? (fytMkt.janmar26_val||0) : 0;
      var acum25u = fytMkt ? (fytMkt.janmar25_un||0) : 0;
      var acum26u = fytMkt ? (fytMkt.janmar26_un||0) : 0;
      acum25v = Math.round(acum25v*100)/100;
      acum26v = Math.round(acum26v*100)/100;
      acum25u = Math.round(acum25u);
      acum26u = Math.round(acum26u);"""

if OLD_MSO2_BLOCK in html:
    html = html.replace(OLD_MSO2_BLOCK, NEW_MSO2_BLOCK, 1)
    ok.append('renderMSO2 Total Mercado — usa FYTD_MARKET_TOTAL.janmar')
else:
    err.append('renderMSO2 Total Mercado block NAO encontrado')

# ─── PASSO 3: Corrigir renderMSO3 — Total Mercado FYTD ───────────────────────
# renderMSO3 deve usar fytd25_val/fytd26_val do FYTD_MARKET_TOTAL
# Verificar se ja esta correto ou precisa de ajuste

idx_mso3 = html.find('function renderMSO3(')
if idx_mso3 >= 0:
    mso3_chunk = html[idx_mso3:idx_mso3+500]
    if 'FYTD_MARKET_TOTAL' in mso3_chunk:
        ok.append('renderMSO3 ja usa FYTD_MARKET_TOTAL OK')
    else:
        err.append('renderMSO3 NAO usa FYTD_MARKET_TOTAL — verificar manualmente')
else:
    err.append('renderMSO3 funcao nao encontrada')

# ─── SALVAR ──────────────────────────────────────────────────────────────────
print("Salvando...")
with open(SRC, 'w', encoding='utf-8') as f:
    f.write(html)

shutil.copy2(SRC, VERS)
shutil.copy2(SRC, DL)

print()
print("=" * 60)
print("PATCH JANMAR TOTAIS — RESULTADO")
print("=" * 60)
for c in ok:
    print(f"  OK   {c}")
for c in err:
    print(f"  MISS {c}")
print()
print(f"  Versao: {VERS.split(chr(92))[-1]}")
print(f"  DL:     {DL.split(chr(92))[-1]}")
print("=" * 60)
