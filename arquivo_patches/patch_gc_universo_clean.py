"""
Auditoria visual — bloco UNIVERSO DE CNPJs na aba Cobertura
Remove os 4 mini-cards duplicados (Total Universo, SCJ Ativos, CIMED, RB)
que repetem os KPIs já visíveis nos cards superiores.
Mantém: título + nota deduplicação + barra segmentada + legenda + bloco Foram Atendidos
Reduz padding do container para compensar o espaço liberado.
"""

import shutil
from datetime import datetime
from pathlib import Path

BASE = Path(r"C:\Users\valqu\OneDrive\Documentos\Claude\Projects\projeto Dashboard_farma_sul\Dashboard_farma_sul")
DASH = BASE / "Dashboard_Farma_Sul_20260512_2220.html"
VER  = BASE / "versoes"
DL   = Path.home() / "Downloads"

html = DASH.read_text(encoding='utf-8')
orig_len = len(html)

# ══════════════════════════════════════════════════════════════
# 1. Remover os 4 mini-cards duplicados
#    (bloco entre "/* ── 4 metric cards ── */" e "/* ── Foram atendidos section ── */")
# ══════════════════════════════════════════════════════════════

OLD_CARDS = """
        /* ── 4 metric cards ── */
        +'<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin:14px 0;">'
          /* 1: Total Universe */
          +'<div style="background:rgba(0,0,0,0.3);border-radius:8px;padding:10px 12px;border:1px solid rgba(103,232,249,0.3);">'
            +'<div style="font-size:8px;color:#94A3B8;font-weight:600;margin-bottom:4px;">🏪 TOTAL UNIVERSO</div>'
            +'<div style="font-size:20px;font-weight:800;color:#67e8f9;line-height:1;">'+p.total.toLocaleString('pt-BR')+'</div>'
            +'<div style="font-size:8px;color:#4a7a7a;margin-top:4px;">Total farmácias do provedor</div>'
          +'</div>'
          /* 2: SCJ Ativos */
          +'<div style="background:rgba(0,0,0,0.3);border-radius:8px;padding:10px 12px;border:1px solid '+barCol+'33;">'
            +'<div style="font-size:8px;color:#94A3B8;font-weight:600;margin-bottom:4px;">✅ SCJ ATIVOS Q3/26</div>'
            +'<div style="font-size:20px;font-weight:800;color:'+barCol+';line-height:1;">'+p.scj.toLocaleString('pt-BR')+'</div>'
            +'<div style="font-size:8px;color:#4a7a7a;margin-top:3px;">Ativos em Jan–Mar/26 (Q3 FY26) · '+_pScj+'% do universo</div>'
            +'<div style="font-size:8px;color:#22c55e;margin-top:2px;font-weight:600;">FY26 acum. Jul–Mar: '+fy26_jul_mar.toLocaleString('pt-BR')+'</div>'
          +'</div>'
          /* 3: CIMED sem SCJ */
          +'<div style="background:rgba(167,139,250,0.06);border-radius:8px;padding:10px 12px;border:1px solid rgba(167,139,250,0.2);">'
            +'<div style="font-size:8px;color:#94A3B8;font-weight:600;margin-bottom:4px;">⚠ CIMED SEM SCJ</div>'
            +'<div style="font-size:20px;font-weight:800;color:#a78bfa;line-height:1;">'+_ci.toLocaleString('pt-BR')+'</div>'
            +'<div style="font-size:8px;color:#4a5568;margin-top:4px;">Têm CIMED, não têm SCJ · '+_pCi+'%</div>'
          +'</div>'
          /* 4: RB sem SCJ */
          +'<div style="background:rgba(96,165,250,0.06);border-radius:8px;padding:10px 12px;border:1px solid rgba(96,165,250,0.2);">'
            +'<div style="font-size:8px;color:#94A3B8;font-weight:600;margin-bottom:4px;">⚠ RB SEM SCJ</div>'
            +'<div style="font-size:20px;font-weight:800;color:#60a5fa;line-height:1;">'+_rb.toLocaleString('pt-BR')+'</div>'
            +'<div style="font-size:8px;color:#4a5568;margin-top:4px;">Têm RB, não têm SCJ · '+_pRb+'%</div>'
          +'</div>'
        +'</div>'

        /* ── Foram atendidos section ── */"""

NEW_CARDS = """

        /* ── Foram atendidos section ── */"""

if OLD_CARDS not in html:
    print("ERRO: bloco dos 4 mini-cards nao encontrado!")
    exit(1)

html = html.replace(OLD_CARDS, NEW_CARDS, 1)
print("4 mini-cards duplicados removidos")

# ══════════════════════════════════════════════════════════════
# 2. Reduzir padding do container externo e ajustar margin-bottom da barra
#    De padding:14px 16px → padding:12px 14px
#    De margin-bottom:14px da barra → margin-bottom:10px
# ══════════════════════════════════════════════════════════════

OLD_CONTAINER = "var _h='<div style=\"background:rgba(0,0,0,0.2);border-radius:8px;padding:14px 16px;margin-bottom:14px;\">'"
NEW_CONTAINER = "var _h='<div style=\"background:rgba(0,0,0,0.2);border-radius:8px;padding:12px 14px;margin-bottom:10px;\">'"

if OLD_CONTAINER in html:
    html = html.replace(OLD_CONTAINER, NEW_CONTAINER, 1)
    print("Padding do container ajustado")
else:
    print("AVISO: container padding nao encontrado (nao critico)")

# ══════════════════════════════════════════════════════════════
# 3. Reduzir margin-bottom da barra segmentada (de 6px → 4px)
#    e aproximar a legenda da barra
# ══════════════════════════════════════════════════════════════

OLD_BAR_WRAP = "'<div style=\"margin-bottom:6px;\">'"
NEW_BAR_WRAP = "'<div style=\"margin-bottom:4px;\">'"

if OLD_BAR_WRAP in html:
    html = html.replace(OLD_BAR_WRAP, NEW_BAR_WRAP, 1)
    print("Margem da barra segmentada ajustada")
else:
    print("AVISO: margem barra nao encontrada (nao critico)")

# ══════════════════════════════════════════════════════════════
# 4. Reduzir margin-bottom da nota de deduplicação (14px → 10px)
# ══════════════════════════════════════════════════════════════

OLD_NOTE = "'<div style=\"background:rgba(52,211,153,0.05);border:1px solid rgba(52,211,153,0.2);border-left:3px solid #34d399;border-radius:6px;padding:8px 12px;margin-bottom:14px;display:flex;gap:10px;align-items:flex-start;\">'"
NEW_NOTE = "'<div style=\"background:rgba(52,211,153,0.05);border:1px solid rgba(52,211,153,0.2);border-left:3px solid #34d399;border-radius:6px;padding:8px 12px;margin-bottom:10px;display:flex;gap:10px;align-items:flex-start;\">'"

if OLD_NOTE in html:
    html = html.replace(OLD_NOTE, NEW_NOTE, 1)
    print("Margem nota deduplicacao ajustada")
else:
    print("AVISO: nota deduplicacao nao encontrada (nao critico)")

# ══════════════════════════════════════════════════════════════
# 5. SALVAR
# ══════════════════════════════════════════════════════════════
ts = datetime.now().strftime('%Y%m%d_%H%M')
versao = VER / f"Dashboard_Farma_Sul_{ts}_GcUniversoClean.html"
shutil.copy(DASH, versao)
print(f"\nVersao salva: {versao.name}")

DASH.write_text(html, encoding='utf-8')
print(f"Dashboard: {len(html):,} chars (era {orig_len:,})")

dl = DL / f"Dashboard_FarmaSul_Giovano_{ts}.html"
shutil.copy(DASH, dl)
print(f"Downloads: {dl.name}")
print("\nDONE.")
