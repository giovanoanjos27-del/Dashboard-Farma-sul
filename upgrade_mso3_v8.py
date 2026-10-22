#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
upgrade_mso3_v8.py
Dois patches no dashboard:
  1. Substitui FYTD_MARKET_TOTAL com valores corretos (shr=100, brand=None) do fytd_market_total_v2.json
  2. Corrige todas as cores escuras/invisíveis dentro do renderMSO3 (v7)
     #374151 -> #94A3B8
     #1e293b -> #64748b
"""

import json, shutil, re
from pathlib import Path
from datetime import datetime

BASE = Path(r"C:\Users\valqu\OneDrive\Documentos\Claude\Projects\projeto Dashboard_farma_sul")
DASH_DIR = BASE / "Dashboard_farma_sul"
DASH_FILE = DASH_DIR / "Dashboard_Farma_Sul_20260512_2220.html"
VERS_DIR = DASH_DIR / "versoes"
JSON_FILE = BASE / "fytd_market_total_v2.json"

ts = datetime.now().strftime("%Y%m%d_%H%M")

# ── Backup / versão ──────────────────────────────────────────────────────────
pre_version = VERS_DIR / f"Dashboard_Farma_Sul_{ts}_PreMSO3v8.html"
shutil.copy2(str(DASH_FILE), str(pre_version))
print(f"Backup criado: {pre_version.name}")

# ── Lê HTML ──────────────────────────────────────────────────────────────────
html = DASH_FILE.read_text(encoding="utf-8")
original_len = len(html)

# ════════════════════════════════════════════════════════════════════════════
# PATCH 1 — FYTD_MARKET_TOTAL: substitui com valores corretos
# ════════════════════════════════════════════════════════════════════════════
with open(str(JSON_FILE), "r", encoding="utf-8") as f:
    data = json.load(f)

# Monta bloco JS
lines = ["const FYTD_MARKET_TOTAL = {"]
for mkt, d in data.items():
    lines.append(
        f"  '{mkt}': {{fytd25_val:{d['fytd25_val']},fytd26_val:{d['fytd26_val']},"
        f"fytd25_un:{d['fytd25_un']},fytd26_un:{d['fytd26_un']}}},"
    )
lines.append("};")
new_block = "\n".join(lines)

# Encontra bloco antigo usando regex
pattern = r"const FYTD_MARKET_TOTAL = \{[^}]*(?:\{[^}]*\}[^}]*)*\};"
m = re.search(pattern, html, re.DOTALL)
if not m:
    # fallback: busca entre marcadores de linhas conhecidos
    start_marker = "const FYTD_MARKET_TOTAL = {"
    end_marker = "};\n\nconst NIELSEN_FYTD_VAL"
    idx_s = html.find(start_marker)
    idx_e = html.find(end_marker)
    if idx_s == -1 or idx_e == -1:
        raise RuntimeError("FYTD_MARKET_TOTAL nao encontrado no HTML!")
    old_block = html[idx_s : idx_e + 2]  # inclui '};'
    html = html[:idx_s] + new_block + html[idx_e + 2:]
    print(f"PATCH 1 OK (fallback) — {len(data)} mercados substituidos")
else:
    old_block = m.group(0)
    html = html[:m.start()] + new_block + html[m.end():]
    print(f"PATCH 1 OK (regex) — {len(data)} mercados substituidos")

# Verifica
if "const FYTD_MARKET_TOTAL" not in html:
    raise RuntimeError("Patch 1 FALHOU — const FYTD_MARKET_TOTAL sumiu!")

# ════════════════════════════════════════════════════════════════════════════
# PATCH 2 — Corrige cores escuras DENTRO do bloco renderMSO3 + END MSO3
# ════════════════════════════════════════════════════════════════════════════
START_ANCHOR = "function renderMSO3(){"
END_ANCHOR   = "/* ═══════════ END MSO3 ═══════════ */"

idx_start = html.find(START_ANCHOR)
idx_end   = html.find(END_ANCHOR)
if idx_start == -1 or idx_end == -1:
    raise RuntimeError("Nao encontrou bloco renderMSO3 para patch de cores!")

mso3_block = html[idx_start : idx_end + len(END_ANCHOR)]

# Substituições de cor
# #374151 (slate-700 escuro) -> #94A3B8 (slate-400 claro, legível em dark bg)
# #1e293b (slate-800 muito escuro) -> #64748b (slate-500 médio, legível)
mso3_fixed = mso3_block
mso3_fixed = mso3_fixed.replace("color:#374151", "color:#94A3B8")
mso3_fixed = mso3_fixed.replace("color:#1e293b", "color:#64748b")

changes_374151 = mso3_block.count("color:#374151")
changes_1e293b = mso3_block.count("color:#1e293b")

html = html[:idx_start] + mso3_fixed + html[idx_end + len(END_ANCHOR):]

print(f"PATCH 2 OK — cores corrigidas: #374151->{changes_374151}x, #1e293b->{changes_1e293b}x")

# ── Salva arquivo principal ───────────────────────────────────────────────
DASH_FILE.write_text(html, encoding="utf-8")
print(f"\nArquivo principal salvo: {DASH_FILE.name} ({len(html):,} chars)")

# ── Versão final ─────────────────────────────────────────────────────────
final_version = VERS_DIR / f"Dashboard_Farma_Sul_{ts}_MSO3v8.html"
shutil.copy2(str(DASH_FILE), str(final_version))
print(f"Versão final salva: {final_version.name}")

# ── Verificação rápida ────────────────────────────────────────────────────
print("\n--- Verificacao ---")
# Confirma valores
for mkt in ["Farma Sul", "T.BR Farma", "Farma Indep Sul"]:
    d = data.get(mkt, {})
    cres = (d.get("fytd26_val",0)/d.get("fytd25_val",1)-1)*100 if d.get("fytd25_val",0)>0 else 0
    print(f"  {mkt:<25} F25={d.get('fytd25_val',0):.3f}MM  F26={d.get('fytd26_val',0):.3f}MM  Cres={cres:+.2f}%")

# Confirma que cores escuras NAO existem mais no bloco renderMSO3
idx_start2 = html.find(START_ANCHOR)
idx_end2   = html.find(END_ANCHOR)
final_block = html[idx_start2 : idx_end2 + len(END_ANCHOR)]
remaining_374151 = final_block.count("color:#374151")
remaining_1e293b = final_block.count("color:#1e293b")
print(f"\n  Cores escuras restantes no MSO3: #374151={remaining_374151} | #1e293b={remaining_1e293b}")
if remaining_374151 == 0 and remaining_1e293b == 0:
    print("  Todas as cores corrigidas com sucesso!")
else:
    print("  ATENCAO: ainda existem cores escuras!")

print("\nDone. v8 aplicado.")
