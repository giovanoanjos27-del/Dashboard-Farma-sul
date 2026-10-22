"""Inspeciona as primeiras 20 linhas e 16 colunas da aba 1-Tabela-1"""
import openpyxl

EXCEL_PATH = r"C:\Users\valqu\OneDrive\Documentos\Claude\Projects\projeto Dashboard_farma_sul\Dashboard_farma_sul\_Recursos\Giovano SCJ\Base Giovano (25-05).xlsx"

wb = openpyxl.load_workbook(EXCEL_PATH, read_only=True, data_only=True)
ws = wb['1-Tabela-1']

print("=== Primeiras 20 linhas (1-Tabela-1) ===")
for i, row in enumerate(ws.iter_rows(min_row=1, max_row=20, max_col=16, values_only=True)):
    print(f"L{i+1}: {row}")

wb.close()
