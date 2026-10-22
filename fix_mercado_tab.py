"""
fix_mercado_tab.py
Corrige as fórmulas SUM da aba MERCADO do Excel:
- Farma Sul  row 40: =SUM(B34:B35,B37:B39,B39) → =SUM(B34:B35,B37:B39)  (remove B39 duplicado)
- T.BR Farma row 52: =SUM(B46:B47,B49:B51,B51) → =SUM(B46:B47,B49:B51)  (remove B51 duplicado)
Idem para colunas C (FYTD26). A coluna de variação (=Cx/Bx-1) se recalcula automaticamente.
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')
import openpyxl
from pathlib import Path

XLS = Path(r'C:\Users\valqu\OneDrive\Documentos\Claude\Projects\projeto Dashboard_farma_sul\Dashboard_farma_sul\_Recursos\Giovano SCJ\Base Giovano 26-04.xlsx')

print('Abrindo Excel...')
wb = openpyxl.load_workbook(str(XLS))
ws = wb['MERCADO']

# Correções de fórmula: remover intervalo duplicado
FIXES = [
    # (row, col, formula_errada, formula_correta, descricao)
    (40, 'B', '=SUM(B34:B35,B37:B39,B39)', '=SUM(B34:B35,B37:B39)', 'Farma Sul FYTD25'),
    (40, 'C', '=SUM(C34:C35,C37:C39,C39)', '=SUM(C34:C35,C37:C39)', 'Farma Sul FYTD26'),
    (52, 'B', '=SUM(B46:B47,B49:B51,B51)', '=SUM(B46:B47,B49:B51)', 'T.BR Farma FYTD25'),
    (52, 'C', '=SUM(C46:C47,C49:C51,C51)', '=SUM(C46:C47,C49:C51)', 'T.BR Farma FYTD26'),
]

changes = 0
for row, col, old_formula, new_formula, desc in FIXES:
    cell = ws[f'{col}{row}']
    actual = cell.value
    if actual == old_formula:
        cell.value = new_formula
        print(f'OK: {desc} ({col}{row})  {old_formula}  →  {new_formula}')
        changes += 1
    elif actual == new_formula:
        print(f'JA CORRETO: {desc} ({col}{row})')
    else:
        print(f'AVISO: {desc} ({col}{row}) formula inesperada: {repr(actual)}')

if changes > 0:
    # Tentar salvar direto; se arquivo estiver aberto no Excel, salvar em cópia
    OUT = XLS
    try:
        wb.save(str(OUT))
        print(f'\n✅ Excel salvo — {changes} fórmulas corrigidas.')
    except PermissionError:
        OUT = XLS.parent / (XLS.stem + '_CORRIGIDO' + XLS.suffix)
        wb.save(str(OUT))
        print(f'\n⚠️  Arquivo original aberto no Excel.')
        print(f'   Salvo em: {OUT.name}')
        print(f'   Feche o Excel e substitua o arquivo original por esta versão corrigida.')
else:
    print('\nNenhuma alteração necessária.')

wb.close()
print('DONE.')
