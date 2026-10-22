"""
Extrai dados de TODOS os markets da aba 1-Tabela-1.
Gera blocos JS prontos para substituir no dashboard.
"""
import openpyxl, shutil, json, datetime, re
from collections import defaultdict

SRC = r"C:\Users\valqu\OneDrive\Documentos\Claude\Projects\projeto Dashboard_farma_sul\Dashboard_farma_sul\_Recursos\Giovano SCJ\Base Giovano 26-04.xlsx"
TMP = r"C:\Users\valqu\AppData\Local\Temp\base_all_markets.xlsx"
shutil.copy2(SRC, TMP)

print("Abrindo workbook...", flush=True)
wb = openpyxl.load_workbook(TMP, data_only=True, read_only=True)
ws = wb["1-Tabela-1"]

HEADER_ROW = 8
COL = {}
all_rows = []

for i, row in enumerate(ws.iter_rows(values_only=True)):
    if i == HEADER_ROW:
        for j, h in enumerate(row):
            if h is not None:
                COL[str(h).strip()] = j
        continue
    if i < HEADER_ROW:
        continue
    market = row[COL.get("markets", 0)] if COL else None
    if market is not None:
        all_rows.append(list(row))

wb.close()
print(f"Total linhas com market: {len(all_rows)}", flush=True)

def get(row, name):
    idx = COL.get(name)
    return row[idx] if idx is not None and idx < len(row) else None

def sf(v):
    try: return float(v) if v is not None else None
    except: return None

def parse_date(row):
    d = get(row, "Data")
    if isinstance(d, datetime.datetime): return (d.month, d.year)
    return None

def fy_of(m, y):
    if (y == 2023 and m >= 7) or (y == 2024 and m <= 6): return "fy24"
    if (y == 2024 and m >= 7) or (y == 2025 and m <= 6): return "fy25"
    if (y == 2025 and m >= 7) or (y == 2026 and m <= 6): return "fy26"
    return None

def fy_idx(m, y): return (m - 7) % 12

def pkey_of(row):
    p = str(get(row, "Periods") or "").strip()
    if p == "FYTD25": return "fytd25"
    if p == "FYTD26": return "fytd26"
    date = parse_date(row)
    if date:
        m, y = date
        fy = fy_of(m, y)
        if fy: return f"{fy}_{fy_idx(m,y)}"
    return None

def to_M(v): return round(v/1_000_000, 2) if v else None
def to_k(v): return round(v/1_000, 1) if v else None
def r2(v):   return round(v, 2) if v is not None else None

FY26_N = 9  # Jul/25..Mar/26

# ── Aggregate all rows ────────────────────────────────────────────────────────
# mkt_total[mkt][pkey] = {val, unid, shr}
# mkt_brand[mkt][brand][pkey] = {val, unid, shr, avg}
# mkt_sku[mkt][sku][pkey]    = {val, unid, shr, avg}

mkt_total = defaultdict(dict)
mkt_brand = defaultdict(lambda: defaultdict(dict))
mkt_sku   = defaultdict(lambda: defaultdict(dict))

for row in all_rows:
    mkt     = str(get(row, "markets") or "").strip()
    brand   = get(row, "BRAND")
    product = get(row, "Products")
    pkey    = pkey_of(row)
    if not mkt or pkey is None:
        continue
    entry = {
        "val":  sf(get(row, "$")),
        "unid": sf(get(row, "(UNID)")),
        "shr":  sf(get(row, "$ Shr - Product")),
        "avg":  sf(get(row, "Avg (UNID) Price")),
    }
    if brand is None and product is None:
        mkt_total[mkt][pkey] = entry
    elif brand is not None and product is None:
        mkt_brand[mkt][str(brand).strip()][pkey] = entry
    elif product is not None:
        mkt_sku[mkt][str(product).strip()][pkey] = entry

print(f"Markets encontrados: {sorted(mkt_total.keys())}", flush=True)

def monthly_arr(store, fy, n, field, conv=None):
    arr = []
    for i in range(n):
        v = store.get(f"{fy}_{i}", {}).get(field)
        arr.append(conv(v) if conv and v is not None else r2(v))
    return arr

def full_arr12(store, fy, field, conv=None):
    arr = []
    for i in range(12):
        v = store.get(f"{fy}_{i}", {}).get(field)
        arr.append(conv(v) if conv and v is not None else r2(v))
    return arr

# ── JS key mapping (market name → JS key used in dashboard) ─────────────────
# Derived from the dashboard's existing structure names
MKT_JS = {
    "Farma CO":                    "farma_co",
    "Farma Gde RJ":                "farma_gde_rj",
    "Farma Gde SP":                "farma_gde_sp",
    "Farma Indep CO":              "farma_indep_co",
    "Farma Indep Gde RJ":          "farma_indep_gde_rj",
    "Farma Indep Gde SP":          "farma_indep_gde_sp",
    "Farma Indep Int SP":          "farma_indep_int_sp",
    "Farma Indep MG+ES+Int RJ":    "farma_indep_mg",
    "Farma Indep NE":              "farma_indep_ne",
    "Farma Indep Sul":             "farma_indep_sul",
    "Farma Int SP":                "farma_int_sp",
    "Farma MG+ES+Int RJ":          "farma_mg",
    "Farma Moderno CO":            "farma_mod_co",
    "Farma Moderno Gde RJ":        "farma_mod_gde_rj",
    "Farma Moderno Gde SP":        "farma_mod_gde_sp",
    "Farma Moderno Int SP":        "farma_mod_int_sp",
    "Farma Moderno MG+ES+Int RJ":  "farma_mod_mg",
    "Farma Moderno NE":            "farma_mod_ne",
    "Farma Moderno Sul":           "farma_mod_sul",
    "Farma NE":                    "farma_ne",
    "Farma Sul":                   "farmasul",
    "T.BR Farma":                  "T.BR Farma",
    "T.BR Farma Indep":            "T.BR Farma Indep",
    "T.BR Farma Moderno":          "T.BR Farma Moderno",
    "INFC RS":                     "rs",
    "INFC SC":                     "sc",
    "INFC MG":                     "mg",
    "INFC CO":                     "co",
    "INFC BA":                     "ba",
    "INFC Belo Horizonte":         "bh",
    "INFC CE":                     "ce",
    "INFC Cidade Gde Gde RJ":      "infc_cgde_rj",
    "INFC Cidade Gde CO":          "infc_cgde_co",
    "INFC Cidade Gde Gde SP":      "infc_cgde_sp",
    "INFC Cidade Gde Int SP":      "infc_cgde_int_sp",
    "INFC Cidade Gde MG+ES+Int RJ":"infc_cgde_mg",
    "INFC Cidade Gde NE":          "infc_cgde_ne",
    "INFC Cidade Gde Sul":         "infc_cgde_sul",
    "INFC Cidade Peq+Med CO":      "infc_cpm_co",
    "INFC Cidade Peq+Med Int SP":  "infc_cpm_int_sp",
    "INFC Cidade Peq+Med MG+ES+Int RJ": "infc_cpm_mg",
    "INFC Cidade Peq+Med NE":      "infc_cpm_ne",
    "INFC Cidade Peq+Med Sul":     "infc_cpm_sul",
    "INFC Curitiba":               "cwb",
    "INFC DF":                     "df",
    "INFC Fortaleza":              "fortaleza",
    "INFC GO":                     "go",
    "INFC Gde RJ":                 "rj",
    "INFC Gde SP":                 "sp",
    "INFC Int BA":                 "int_ba",
    "INFC Int CE":                 "int_ce",
    "INFC Int MG":                 "int_mg",
    "INFC Int PE":                 "int_pe",
    "INFC Int PR":                 "int_pr",
    "INFC Int RS":                 "int_rs",
    "INFC Int SP":                 "int_sp",
    "INFC MA+PI":                  "ma_pi",
    "INFC MG+ES+Int RJ":           "infc_mg",
    "INFC Man+Bel+Ana":            "man_bel_ana",
    "INFC Manaus":                 "manaus",
    "INFC NE":                     "ne",
    "INFC PE":                     "pe",
    "INFC PR":                     "pr",
    "INFC Porto Alegre":           "poa",
    "INFC Recife":                 "recife",
    "INFC SP":                     "infc_sp",
    "INFC Salvador":               "salvador",
    "INFC Sul":                    "sul",
    "T.BR INFC":                   "T.BR INFC",
    "INA Int MG":                  "ina_int_mg",
    "INA MG":                      "ina_mg",
    "INA MG+ES+Int RJ":            "ina_mg_es",
}

# ── Output file ───────────────────────────────────────────────────────────────
OUT = r"C:\Users\valqu\OneDrive\Documentos\Claude\Projects\projeto Dashboard_farma_sul\all_markets_data.js"

with open(OUT, "w", encoding="utf-8") as f:

    # ── VOL_MKT_HIST ─────────────────────────────────────────────────────────
    f.write("// ═══════════════════════════════════════════════════════════\n")
    f.write("// VOL_MKT_HIST — todos os markets\n")
    f.write("// ═══════════════════════════════════════════════════════════\n")
    f.write("const VOL_MKT_HIST_NEW = {\n")
    for mkt in sorted(mkt_total.keys()):
        td = mkt_total[mkt]
        fy24v = full_arr12(td, "fy24", "val", to_M)
        fy25v = full_arr12(td, "fy25", "val", to_M)
        fy26v = monthly_arr(td, "fy26", FY26_N, "val", to_M) + [None]*3
        fy24u = full_arr12(td, "fy24", "unid", to_k)
        fy25u = full_arr12(td, "fy25", "unid", to_k)
        fy26u = monthly_arr(td, "fy26", FY26_N, "unid", to_k) + [None]*3

        fy24tv = r2(sum(x for x in fy24v if x))
        fy25tv = r2(sum(x for x in fy25v if x))
        fy26fv = r2(sum(x for x in fy26v if x))
        fy25fv = r2(sum(x for x in fy25v[:9] if x))
        fy24tu = r2(sum(x for x in fy24u if x))
        fy25tu = r2(sum(x for x in fy25u if x))
        fy26fu = r2(sum(x for x in fy26u if x))
        fy25fu = r2(sum(x for x in fy25u[:9] if x))

        ratio_v = (fy26fv / fy25fv) if fy25fv else 1
        ratio_u = (fy26fu / fy25fu) if fy25fu else 1
        fy25_aprmaj_v = r2(sum(x for x in fy25v[9:12] if x))
        fy25_aprmaj_u = r2(sum(x for x in fy25u[9:12] if x))
        fy26pv = r2((fy26fv or 0) + (fy25_aprmaj_v or 0) * ratio_v)
        fy26pu = round((fy26fu or 0) + (fy25_aprmaj_u or 0) * ratio_u) if fy26fu else None

        f.write(f"  '{mkt}': {{\n")
        f.write(f"    fy24_un:{fy24u},fy25_un:{fy25u},fy26_un:{fy26u},\n")
        f.write(f"    fy24_val:{fy24v},fy25_val:{fy25v},fy26_val:{fy26v},\n")
        f.write(f"    fy24_total_un:{fy24tu},fy25_total_un:{fy25tu},fy26_proj_un:{fy26pu},fy26_fytd_un:{fy26fu},fy25_fytd_un:{fy25fu},\n")
        f.write(f"    fy24_total_val:{fy24tv},fy25_total_val:{fy25tv},fy26_proj_val:{fy26pv},fy26_fytd_val:{fy26fv},fy25_fytd_val:{fy25fv}\n")
        f.write(f"  }},\n")
    f.write("};\n\n")

    # ── VOL_MKT_DATA ─────────────────────────────────────────────────────────
    f.write("// VOL_MKT_DATA — todos os markets\n")
    f.write("const VOL_MKT_DATA_NEW = {\n")
    for mkt in sorted(mkt_total.keys()):
        td = mkt_total[mkt]
        f25 = td.get("fytd25", {})
        f26 = td.get("fytd26", {})
        mv  = monthly_arr(td, "fy26", FY26_N, "val", to_M)
        mu  = monthly_arr(td, "fy26", FY26_N, "unid", to_k)
        f.write(f"  '{mkt}': {{fytd25_val:{to_M(f25.get('val'))},fytd26_val:{to_M(f26.get('val'))},fytd25_un:{to_k(f25.get('unid'))},fytd26_un:{to_k(f26.get('unid'))},monthly_val:{mv},monthly_un:{mu}}},\n")
    f.write("};\n\n")

    # ── NIELSEN_BRAND_VAL ─────────────────────────────────────────────────────
    f.write("// NIELSEN_BRAND_VAL — todos os markets\n")
    f.write("const NIELSEN_BRAND_VAL_NEW = {\n")
    for mkt in sorted(mkt_brand.keys()):
        f.write(f"  '{mkt}': {{\n")
        for brand in sorted(mkt_brand[mkt].keys()):
            bd = mkt_brand[mkt][brand]
            f25 = bd.get("fytd25", {})
            f26 = bd.get("fytd26", {})
            mv = monthly_arr(bd, "fy26", FY26_N, "val", to_M)
            mu = monthly_arr(bd, "fy26", FY26_N, "unid", to_k)
            jan_v = to_M(bd.get("fy26_6",{}).get("val"))
            fev_v = to_M(bd.get("fy26_7",{}).get("val"))
            mar_v = to_M(bd.get("fy26_8",{}).get("val"))
            jan_u = to_k(bd.get("fy26_6",{}).get("unid"))
            fev_u = to_k(bd.get("fy26_7",{}).get("unid"))
            mar_u = to_k(bd.get("fy26_8",{}).get("unid"))
            f.write(f"    '{brand}': {{fytd25_val:{to_M(f25.get('val'))},fytd26_val:{to_M(f26.get('val'))},fytd25_un:{to_k(f25.get('unid'))},fytd26_un:{to_k(f26.get('unid'))},jan_val:{jan_v},fev_val:{fev_v},mar_val:{mar_v},jan_un:{jan_u},fev_un:{fev_u},mar_un:{mar_u},monthly_val:{mv},monthly_un:{mu}}},\n")
        f.write("  },\n")
    f.write("};\n\n")

    # ── SHR_TREND_DATA ───────────────────────────────────────────────────────
    f.write("// SHR_TREND_DATA — todos os markets\n")
    f.write("const SHR_TREND_DATA_NEW = {\n")
    for mkt in sorted(mkt_brand.keys()):
        f.write(f"  '{mkt}': {{\n")
        for brand in sorted(mkt_brand[mkt].keys()):
            bd = mkt_brand[mkt][brand]
            f25 = bd.get("fytd25", {})
            f26 = bd.get("fytd26", {})
            fy24 = full_arr12(bd, "fy24", "shr")
            fy25 = full_arr12(bd, "fy25", "shr")
            fy26 = monthly_arr(bd, "fy26", FY26_N, "shr") + [None]*3
            delta = r2((f26.get("shr") or 0) - (f25.get("shr") or 0)) if f25.get("shr") and f26.get("shr") else None
            f.write(f"    '{brand}': {{fy24:{fy24},fy25:{fy25},fy26:{fy26},delta:{delta}}},\n")
        f.write("  },\n")
    f.write("};\n\n")

    # ── MKTSHARE_OVERVIEW ────────────────────────────────────────────────────
    f.write("// MKTSHARE_OVERVIEW — todos os markets\n")
    f.write("const MKTSHARE_OVERVIEW_NEW = {\n")
    for mkt in sorted(mkt_brand.keys()):
        f.write(f"  '{mkt}': {{\n")
        for brand in sorted(mkt_brand[mkt].keys()):
            bd = mkt_brand[mkt][brand]
            f25 = bd.get("fytd25", {})
            f26 = bd.get("fytd26", {})
            monthly = monthly_arr(bd, "fy26", FY26_N, "shr")
            jan25   = r2(bd.get("fy25_6",{}).get("shr"))
            feb25   = r2(bd.get("fy25_7",{}).get("shr"))
            mar25   = r2(bd.get("fy25_8",{}).get("shr"))
            fytd25  = r2(f25.get("shr"))
            fytd26  = r2(f26.get("shr"))
            delta   = r2((fytd26 or 0) - (fytd25 or 0)) if fytd25 and fytd26 else None
            f.write(f"    '{brand}': {{fytd25:{fytd25},fytd26:{fytd26},delta:{delta},monthly:{monthly},jan25:{jan25},feb25:{feb25},mar25:{mar25}}},\n")
        f.write("  },\n")
    f.write("};\n\n")

    # ── SKU_MKT_DATA (top 10 por fytd26) ─────────────────────────────────────
    f.write("// SKU_MKT_DATA — todos os markets (top 10 fytd26)\n")
    f.write("const SKU_MKT_DATA_NEW = {\n")
    for mkt in sorted(mkt_sku.keys()):
        skus_all = list(mkt_sku[mkt].keys())
        # Sort by fytd26 shr descending, take top 10
        def shr26(s): return mkt_sku[mkt][s].get("fytd26", {}).get("shr") or 0
        skus_sorted = sorted(skus_all, key=shr26, reverse=True)[:10]
        fytd25 = [r2(mkt_sku[mkt][s].get("fytd25",{}).get("shr")) for s in skus_sorted]
        fytd26 = [r2(mkt_sku[mkt][s].get("fytd26",{}).get("shr")) for s in skus_sorted]
        var    = [r2((fytd26[i] or 0) - (fytd25[i] or 0)) if fytd25[i] is not None and fytd26[i] is not None else None for i in range(len(skus_sorted))]
        # escape product names (may contain special chars)
        skus_json = json.dumps(skus_sorted, ensure_ascii=False)
        f.write(f"  '{mkt}': {{\"skus\":{skus_json},\"fytd25\":{fytd25},\"fytd26\":{fytd26},\"var\":{var}}},\n")
    f.write("};\n\n")

    # ── AVG_DATA ─────────────────────────────────────────────────────────────
    f.write("// AVG_DATA — todos os markets\n")
    f.write("const AVG_DATA_NEW = {\n")
    for mkt in sorted(mkt_sku.keys()):
        js_key = MKT_JS.get(mkt, mkt.lower().replace(" ", "_").replace("+", "_").replace(".", "").replace("-", "_"))
        f.write(f"  {js_key}: {{\n")
        for sku in sorted(mkt_sku[mkt].keys()):
            avg_fy26 = monthly_arr(mkt_sku[mkt][sku], "fy26", FY26_N, "avg")
            f.write(f"    '{sku}':  {avg_fy26},\n")
        f.write("  },\n")
    f.write("};\n\n")

    # ── VMX_MARKET_DATA partial update (monthly dicts) ───────────────────────
    f.write("// VMX monthlies update — todos os markets\n")
    f.write("// Para cada market: fy25, fy26, fy25_rev, fy26_rev\n")
    f.write("const VMX_MONTHLY_NEW = {\n")
    MONTH_ABBR = {7:"Jul",8:"Aug",9:"Sep",10:"Oct",11:"Nov",12:"Dec",
                  1:"Jan",2:"Feb",3:"Mar",4:"Apr",5:"May",6:"Jun"}
    for mkt in sorted(mkt_total.keys()):
        td = mkt_total[mkt]
        fy25u, fy26u, fy25r, fy26r = {}, {}, {}, {}
        for i in range(12):
            k = f"fy25_{i}"
            if k in td:
                m_idx = (i + 7) % 12 + 1  # convert FY idx to calendar month (wrong, needs fix)
                # FY idx 0=Jul, 1=Aug...5=Dec, 6=Jan...11=Jun
                cal_m = ((i + 6) % 12) + 1
                if i < 6: cal_y = 2024 if i < 6 else 2025
                else: cal_y = 2025
                abbr = MONTH_ABBR.get(cal_m, str(cal_m))
                v = td[k].get("val"); u = td[k].get("unid")
                if u: fy25u[abbr] = round(u)
                if v: fy25r[abbr] = round(v)
        for i in range(FY26_N):
            k = f"fy26_{i}"
            if k in td:
                cal_m = ((i + 6) % 12) + 1
                abbr = MONTH_ABBR.get(cal_m, str(cal_m))
                v = td[k].get("val"); u = td[k].get("unid")
                if u: fy26u[abbr] = round(u)
                if v: fy26r[abbr] = round(v)
        f.write(f"  '{mkt}': {{fy25:{json.dumps(fy25u)},fy26:{json.dumps(fy26u)},fy25_rev:{json.dumps(fy25r)},fy26_rev:{json.dumps(fy26r)}}},\n")
    f.write("};\n")

print(f"\nArquivo gerado: {OUT}", flush=True)
print("FIM.", flush=True)
