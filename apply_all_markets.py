"""
Aplica all_markets_data.js ao dashboard HTML.
Patcha 7 estruturas JS + VMX_MARKET_DATA (monthlies) para todos os 71 mercados.
"""
import re, shutil, datetime, os, json

BASE      = r"C:\Users\valqu\OneDrive\Documentos\Claude\Projects\projeto Dashboard_farma_sul"
DATA_FILE = rf"{BASE}\all_markets_data.js"
HTML_SRC  = rf"{BASE}\Dashboard_farma_sul\Dashboard_Farma_Sul_ABR2026_GIOVANO_FIXED.html"
VERS_DIR  = rf"{BASE}\Dashboard_farma_sul\versoes"

# Mapeamento de chaves erradas (extraction) → chaves corretas (dashboard) para AVG_DATA
AVG_KEY_FIX = {
    "cwb":            "infc_cwb",
    "poa":            "infc_poa",
    "rj":             "infc_gde_rj",
    "sp":             "infc_gde_sp",
    "ne":             "infc_ne",
    "sul":            "infc_sul",
    "mg":             "infc_mg",
    "co":             "infc_co",
    "ba":             "infc_ba",
    "ce":             "infc_ce",
    "pe":             "infc_pe",
    "df":             "infc_df",
    "go":             "infc_go",
    "bh":             "infc_bh",
    "fortaleza":      "infc_for",
    "recife":         "infc_recife",
    "salvador":       "infc_salvador",
    "manaus":         "infc_manaus",
    "man_bel_ana":    "infc_man_bel",
    "ma_pi":          "infc_mapi",
    "infc_mg":        "infc_mg_es",   # INFC MG+ES+Int RJ
    "infc_cgde_co":   "infc_cg_co",
    "infc_cgde_rj":   "infc_cg_gde_rj",
    "infc_cgde_sp":   "infc_cg_gde_sp",
    "infc_cgde_int_sp": "infc_cg_int_sp",
    "infc_cgde_mg":   "infc_cg_mg",
    "infc_cgde_ne":   "infc_cg_ne",
    "infc_cgde_sul":  "infc_cg_sul",
    "infc_cpm_co":    "infc_cp_co",
    "infc_cpm_int_sp":"infc_cp_int_sp",
    "infc_cpm_mg":    "infc_cp_mg",
    "infc_cpm_ne":    "infc_cp_ne",
    "infc_cpm_sul":   "infc_cp_sul",
    "int_ba":         "infc_int_ba",
    "int_ce":         "infc_int_ce",
    "int_mg":         "infc_int_mg",
    "int_pe":         "infc_int_pe",
    "int_pr":         "infc_int_pr",
    "int_rs":         "infc_int_rs",
    "int_sp":         "infc_int_sp",
    # T.BR keys (unquoted in AVG_DATA)
    "T.BR Farma":         "tbr_farma",
    "T.BR Farma Indep":   "tbr_farma_indep",
    "T.BR Farma Moderno": "tbr_farma_mod",
    "T.BR INFC":          "tbr_infc",
}

# ── Ler e preparar dados ──────────────────────────────────────────────────────
with open(DATA_FILE, "r", encoding="utf-8") as f:
    data_raw = f.read().replace("None", "null")

def parse_section(text, section_name, quoted_keys=True):
    marker = f"const {section_name} = {{"
    start = text.find(marker)
    if start == -1:
        print(f"  [WARN] seção '{section_name}' não encontrada")
        return {}
    inner_start = start + len(marker) - 1
    depth = 0
    i = inner_start
    while i < len(text):
        if text[i] == '{':   depth += 1
        elif text[i] == '}':
            depth -= 1
            if depth == 0:
                inner = text[inner_start+1:i]
                break
        i += 1

    if quoted_keys:
        pat = re.compile(r"^  '([^']+)':\s*\{", re.MULTILINE)
    else:
        pat = re.compile(r"^  (\S+):\s*\{", re.MULTILINE)

    entries = {}
    starts = list(pat.finditer(inner))
    for idx, m in enumerate(starts):
        key = m.group(1)
        s   = m.start()
        e   = starts[idx+1].start() if idx+1 < len(starts) else len(inner)
        entry = inner[s:e].rstrip().rstrip(',').rstrip()
        entries[key] = entry
    return entries

new_vol_hist   = parse_section(data_raw, "VOL_MKT_HIST_NEW")
new_vol_data   = parse_section(data_raw, "VOL_MKT_DATA_NEW")
new_brand_val  = parse_section(data_raw, "NIELSEN_BRAND_VAL_NEW")
new_shr_trend  = parse_section(data_raw, "SHR_TREND_DATA_NEW")
new_mkt_share  = parse_section(data_raw, "MKTSHARE_OVERVIEW_NEW")
new_sku_data   = parse_section(data_raw, "SKU_MKT_DATA_NEW")
new_avg_data   = parse_section(data_raw, "AVG_DATA_NEW", quoted_keys=False)
new_vmx        = parse_section(data_raw, "VMX_MONTHLY_NEW")

# Corrigir chaves AVG_DATA
new_avg_fixed = {}
for k, v in new_avg_data.items():
    dk = AVG_KEY_FIX.get(k, k)   # usa mapeamento se disponível, senão mantém
    # Substituir chave no texto da entrada também
    new_entry = v.replace(f"  {k}: {{", f"  {dk}: {{", 1)
    new_avg_fixed[dk] = new_entry
new_avg_data = new_avg_fixed

print(f"Entradas lidas:")
for name, d in [("VOL_MKT_HIST", new_vol_hist), ("VOL_MKT_DATA", new_vol_data),
                ("NIELSEN_BRAND_VAL", new_brand_val), ("SHR_TREND_DATA", new_shr_trend),
                ("MKTSHARE_OVERVIEW", new_mkt_share), ("SKU_MKT_DATA", new_sku_data),
                ("AVG_DATA", new_avg_data), ("VMX_MONTHLY", new_vmx)]:
    print(f"  {name}: {len(d)} mercados")

# ── Ler dashboard ─────────────────────────────────────────────────────────────
with open(HTML_SRC, "r", encoding="utf-8") as f:
    html = f.read()
print(f"\nDashboard carregado: {len(html):,} chars")

# ── Backup ────────────────────────────────────────────────────────────────────
os.makedirs(VERS_DIR, exist_ok=True)
ts     = datetime.datetime.now().strftime("%Y%m%d_%H%M")
backup = os.path.join(VERS_DIR, f"Dashboard_Farma_Sul_{ts}_preAllMarkets2.html")
shutil.copy2(HTML_SRC, backup)
print(f"Backup salvo: {backup}")

# ── Função de substituição (multi-line) ───────────────────────────────────────
def replace_entry(html, struct_name, market_key, new_entry, quoted=True):
    """Localiza e substitui entrada de mercado — aceita var ou const."""
    for kw in ("const", "var", "let"):
        marker = f"{kw} {struct_name} = {{"
        blk = html.find(marker)
        if blk != -1:
            break
    else:
        return html, False

    search = f"  '{market_key}': {{" if quoted else f"  {market_key}: {{"
    pos = html.find(search, blk)
    if pos == -1:
        return html, False

    open_pos = pos + search.index('{')
    depth = 0
    i = open_pos
    while i < len(html):
        if html[i] == '{':   depth += 1
        elif html[i] == '}':
            depth -= 1
            if depth == 0:
                end = i + 1
                break
        i += 1

    if html[end:end+1] == ',':  end += 1
    if html[end:end+1] == '\n': end += 1

    html = html[:pos] + new_entry + ",\n" + html[end:]
    return html, True

# ── Função de substituição (inline JSON) ─────────────────────────────────────
def replace_json_struct(html, struct_name, new_entries_dict):
    """
    Para estruturas armazenadas como JSON inline (var NAME = {...}).
    new_entries_dict: {excel_key: {field: value, ...}}
    """
    for kw in ("var", "const", "let"):
        marker = f"{kw} {struct_name} = {{"
        pos = html.find(marker)
        if pos != -1:
            break
    else:
        print(f"  [SKIP] {struct_name} não encontrado")
        return html, 0

    depth = 0
    i = pos + len(marker) - 1
    while i < len(html):
        if html[i] == '{':   depth += 1
        elif html[i] == '}':
            depth -= 1
            if depth == 0:
                end = i + 1
                break
        i += 1

    json_str = html[pos + len(marker) - 1 : end]
    try:
        data = json.loads(json_str)
    except Exception as e:
        print(f"  [ERRO] parse JSON {struct_name}: {e}")
        return html, 0

    count = 0
    for excel_key, new_val in new_entries_dict.items():
        if excel_key in data:
            data[excel_key] = new_val
            count += 1

    new_json = json.dumps(data, ensure_ascii=False, separators=(',', ':'))
    html = html[:pos + len(marker) - 1] + new_json + html[end:]
    return html, count

# ── Preparar SKU_MKT_DATA como dicts ─────────────────────────────────────────
# SKU_MKT_DATA_NEW está em format multi-line; converter para dicts Python para
# substituição JSON
sku_dict_new = {}
sku_pat = re.compile(r"'([^']+)':\s*\{\"skus\":(\[.*?\]),\"fytd25\":(\[.*?\]),\"fytd26\":(\[.*?\]),\"var\":(\[.*?\])\}")
for mkt, entry in new_sku_data.items():
    m = sku_pat.search(entry)
    if m:
        try:
            sku_dict_new[mkt] = {
                "skus":   json.loads(m.group(2)),
                "fytd25": json.loads(m.group(3)),
                "fytd26": json.loads(m.group(4)),
                "var":    json.loads(m.group(5)),
            }
        except: pass

print(f"  SKU_MKT_DATA parsed: {len(sku_dict_new)} mercados")

# ── Aplicar estruturas multi-line ─────────────────────────────────────────────
PATCHES = [
    (new_vol_hist,  "VOL_MKT_HIST",     True),
    (new_vol_data,  "VOL_MKT_DATA",     True),
    (new_brand_val, "NIELSEN_BRAND_VAL",True),
    (new_shr_trend, "SHR_TREND_DATA",   True),
    (new_mkt_share, "MKTSHARE_OVERVIEW",True),
    (new_avg_data,  "AVG_DATA",         False),
]

total_ok = 0
total_miss = 0

for new_dict, cname, quoted in PATCHES:
    ok = miss = 0
    for mkt, entry in new_dict.items():
        html, replaced = replace_entry(html, cname, mkt, entry, quoted)
        if replaced: ok += 1
        else:
            miss += 1
            print(f"  MISS: {cname} / '{mkt}'")
    print(f"{cname}: {ok} substituídos, {miss} faltando")
    total_ok   += ok
    total_miss += miss

# ── Aplicar SKU_MKT_DATA (JSON inline) ───────────────────────────────────────
html, sku_count = replace_json_struct(html, "SKU_MKT_DATA", sku_dict_new)
print(f"SKU_MKT_DATA: {sku_count} mercados atualizados")

# ── VMX_MARKET_DATA — substituir monthlies ────────────────────────────────────
vmx_marker = "var VMX_MARKET_DATA = {"
vmx_pos = html.find(vmx_marker)
vmx_count = 0
if vmx_pos != -1:
    depth = 0
    i = vmx_pos + len(vmx_marker) - 1
    while i < len(html):
        if html[i] == '{':   depth += 1
        elif html[i] == '}':
            depth -= 1
            if depth == 0:
                vmx_end = i + 1
                break
        i += 1

    vmx_json_str = html[vmx_pos + len(vmx_marker) - 1 : vmx_end]
    try:
        vmx_data = json.loads(vmx_json_str)
    except Exception as e:
        print(f"  [ERRO] parse VMX JSON: {e}")
        vmx_data = None

    if vmx_data:
        for mkt_excel, entry_str in new_vmx.items():
            m = re.search(
                r'\{fy25:(\{"[^"]+":.*?\}),fy26:(\{"[^"]+":.*?\}),fy25_rev:(\{"[^"]+":.*?\}),fy26_rev:(\{"[^"]+":.*?\})\}',
                entry_str
            )
            if m and mkt_excel in vmx_data:
                try:
                    vmx_data[mkt_excel]["fy25"]     = json.loads(m.group(1))
                    vmx_data[mkt_excel]["fy26"]     = json.loads(m.group(2))
                    vmx_data[mkt_excel]["fy25_rev"] = json.loads(m.group(3))
                    vmx_data[mkt_excel]["fy26_rev"] = json.loads(m.group(4))
                    vmx_count += 1
                except Exception as e:
                    print(f"  [ERRO] VMX parse '{mkt_excel}': {e}")

        new_vmx_json = json.dumps(vmx_data, ensure_ascii=False, separators=(',', ':'))
        html = html[:vmx_pos + len(vmx_marker) - 1] + new_vmx_json + html[vmx_end:]
        print(f"VMX_MARKET_DATA: {vmx_count} mercados atualizados")
else:
    print("  [SKIP] VMX_MARKET_DATA não encontrado")

# ── Salvar ────────────────────────────────────────────────────────────────────
with open(HTML_SRC, "w", encoding="utf-8") as f:
    f.write(html)

# Salvar versão final
final_ver = os.path.join(VERS_DIR, f"Dashboard_Farma_Sul_{ts}_AllMarkets.html")
shutil.copy2(HTML_SRC, final_ver)

print(f"\nSalvo: {HTML_SRC}")
print(f"Versão final: {final_ver}")
print(f"Total multi-line: {total_ok} substituições, {total_miss} faltando")
print(f"SKU_MKT_DATA: {sku_count} | VMX: {vmx_count}")
print("FIM.")
