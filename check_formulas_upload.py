"""
check_formulas_upload.py
Verifica se as células lidas pelo upload browser contêm fórmulas de array dinâmico.
O SheetJS falha com array-spill formulas (@-prefixed / dynamic array) — retorna 0.
Fórmulas normais (SOMA, referências simples) SheetJS geralmente lê OK.
"""

import openpyxl
import re

EXCEL = r"C:\Users\valqu\OneDrive\Documentos\Claude\Projects\projeto Dashboard_farma_sul\Dashboard_farma_sul\Planilha_Mestre_FarmaSul_Giovano.xlsx"

# Meses que o upload lê nas abas SO_*
MESES_COL_NAMES = ['Jan','Fev','Mar','Abr','Mai','Jun','Jul','Ago','Set','Out','Nov','Dez']

# Abas de Sell Out lidas pelo upload
SO_SHEETS = [
    'SO_São_João', 'SO_SJoao_Caroline', 'SO_SJoao_Isadora',
    'SO_Nissei', 'SO_Nissei_Andre', 'SO_Nissei_Edmar',
    'SO_Clamed', 'SO_Panvel', 'SO_DDGAM', 'SO_DDGaúcha', 'SO_DDRiomed'
]

# Colunas do Estoque_Geral que o upload lê
ESTOQUE_COLS = ['Estoque Atual', 'Venda Ref (Cx/mês)', 'Cobertura (dias)', 'Status']

def is_dynamic_array(formula):
    """Detecta fórmulas de array dinâmico/spill que SheetJS não lê (retorna 0)."""
    if not formula or not isinstance(formula, str):
        return False
    # Prefixo @ indica dynamic array no formato XLSX interno
    if formula.startswith('@'):
        return True
    # Funções que geram spill: UNIQUE, FILTER, SORT, SEQUENCE, etc.
    spill_funcs = ['UNIQUE(', 'FILTER(', 'SORT(', 'SORTBY(', 'SEQUENCE(', 'RANDARRAY(', 'XLOOKUP(', 'XMATCH(']
    fu = formula.upper()
    if any(f in fu for f in spill_funcs):
        return True
    return False

def is_any_formula(cell):
    """Verifica se a célula tem fórmula (data_only=False)."""
    # Quando data_only=False, células com fórmula retornam string começando com =
    v = cell.value
    return isinstance(v, str) and v.startswith('=')

print("=" * 70)
print("DIAGNÓSTICO: Fórmulas nas abas lidas pelo upload browser")
print("=" * 70)

# ── Abas de Sell Out ──────────────────────────────────────────────────────
wb_formula = openpyxl.load_workbook(EXCEL, data_only=False)
wb_value   = openpyxl.load_workbook(EXCEL, data_only=True)

print("\n── SELL OUT: células dos meses (Jan..Dez) ──────────────────────────────")
for sheet_name in SO_SHEETS:
    if sheet_name not in wb_formula.sheetnames:
        print(f"  ❌ {sheet_name}: ABA NÃO ENCONTRADA")
        continue

    ws_f = wb_formula[sheet_name]
    ws_v = wb_value[sheet_name]

    # Ler headers da linha 2 (range:1 no JS pula linha 1 = título)
    # Linha 1 = título, Linha 2 = headers, Linha 3+ = dados
    headers = {}
    for col_idx, cell in enumerate(ws_f[2], start=1):
        val = str(cell.value).strip() if cell.value else ''
        if val in MESES_COL_NAMES:
            headers[val] = col_idx

    if not headers:
        # Tentar linha 1 como header
        for col_idx, cell in enumerate(ws_f[1], start=1):
            val = str(cell.value).strip() if cell.value else ''
            if val in MESES_COL_NAMES:
                headers[val] = col_idx

    total_formula_cells = 0
    dynamic_array_cells = 0
    normal_formula_cells = 0
    value_cells = 0
    sample_issues = []

    # Verificar linhas de dados (a partir da linha 3)
    max_row = ws_f.max_row
    for row_idx in range(3, max_row + 1):
        for mes, col_idx in headers.items():
            cell_f = ws_f.cell(row=row_idx, column=col_idx)
            cell_v = ws_v.cell(row=row_idx, column=col_idx)

            if cell_f.value is None:
                continue

            if is_any_formula(cell_f):
                total_formula_cells += 1
                formula = str(cell_f.value)
                cached = cell_v.value

                if is_dynamic_array(formula):
                    dynamic_array_cells += 1
                    if len(sample_issues) < 3:
                        sample_issues.append(
                            f"    ⚠ {cell_f.coordinate}: {formula[:40]} → cached={cached}"
                        )
                else:
                    normal_formula_cells += 1
            else:
                value_cells += 1

    status = "✅ OK" if dynamic_array_cells == 0 else f"⚠ {dynamic_array_cells} DYNAMIC ARRAY"
    print(f"\n  {sheet_name}: {status}")
    print(f"    Células valor: {value_cells} | Fórmula normal: {normal_formula_cells} | Dynamic array: {dynamic_array_cells}")
    if sample_issues:
        print("    Amostras problemáticas:")
        for s in sample_issues:
            print(s)

# ── Estoque_Geral ─────────────────────────────────────────────────────────
print("\n── ESTOQUE_GERAL: colunas lidas pelo upload ──────────────────────────")
sheet_name = 'Estoque_Geral'
if sheet_name in wb_formula.sheetnames:
    ws_f = wb_formula[sheet_name]
    ws_v = wb_value[sheet_name]

    # Encontrar índices das colunas por header
    headers = {}
    for col_idx, cell in enumerate(ws_f[1], start=1):
        val = str(cell.value).strip() if cell.value else ''
        if val in ESTOQUE_COLS:
            headers[val] = col_idx

    if not headers:
        for col_idx, cell in enumerate(ws_f[2], start=1):
            val = str(cell.value).strip() if cell.value else ''
            if val in ESTOQUE_COLS:
                headers[val] = col_idx

    print(f"  Colunas encontradas: {list(headers.keys())}")

    col_stats = {col: {'formula_norm':0, 'dynamic':0, 'value':0, 'samples':[]}
                 for col in ESTOQUE_COLS}

    max_row = ws_f.max_row
    for row_idx in range(2, max_row + 1):
        for col_name, col_idx in headers.items():
            cell_f = ws_f.cell(row=row_idx, column=col_idx)
            cell_v = ws_v.cell(row=row_idx, column=col_idx)

            if cell_f.value is None:
                continue

            if is_any_formula(cell_f):
                formula = str(cell_f.value)
                if is_dynamic_array(formula):
                    col_stats[col_name]['dynamic'] += 1
                    if len(col_stats[col_name]['samples']) < 2:
                        col_stats[col_name]['samples'].append(
                            f"    ⚠ {cell_f.coordinate}: {formula[:40]} → cached={cell_v.value}"
                        )
                else:
                    col_stats[col_name]['formula_norm'] += 1
            else:
                col_stats[col_name]['value'] += 1

    for col_name in ESTOQUE_COLS:
        if col_name not in headers:
            print(f"  ❓ '{col_name}': coluna não encontrada na aba")
            continue
        s = col_stats[col_name]
        status = "✅ OK" if s['dynamic'] == 0 else f"⚠ DYNAMIC ARRAY: {s['dynamic']}"
        print(f"  '{col_name}': {status} | valor={s['value']} | fórmula normal={s['formula_norm']}")
        for smp in s['samples']:
            print(smp)
else:
    print(f"  ❌ Aba '{sheet_name}' não encontrada")

# ── Cobertura (não usada no upload direto — confirmar) ────────────────────
print("\n── COBERTURA: abas de cobertura são lidas no upload? ───────────────────")
cob_sheets = [s for s in wb_formula.sheetnames if 'Cob' in s or 'Cobertura' in s]
print(f"  Abas de Cobertura na planilha: {cob_sheets}")
print("  (verificar no JS se alguma dessas abas é lida pelo upload browser)")

print("\n" + "=" * 70)
print("RESUMO:")
print("  ✅ OK = SheetJS deve ler corretamente (valores diretos ou fórmulas normais)")
print("  ⚠  = Dynamic Array formula — SheetJS retorna 0 (problema idêntico ao SellIn)")
print("=" * 70)
