#!/usr/bin/env python3
import sys
import os

# Add project folder to path
sys.path.insert(0, os.path.dirname(__file__))

def main():
    try:
        from openpyxl import load_workbook
        from openpyxl.utils import get_column_letter
        import pandas as pd

        uploads_dir = r"C:\Users\valqu\AppData\Roaming\Claude\local-agent-mode-sessions\850d6bf0-c2cb-46f6-a7a0-3f7dc3fb8188\786fcc28-4073-487a-b34d-df2c9253ad90\local_b3075bef-1902-48d8-8487-87877f6ea22d\uploads"
        file_path = os.path.join(uploads_dir, "Base Nielsen Giovano 27-03-c84904e9.xlsx")

        if not os.path.exists(file_path):
            print(f"File not found: {file_path}")
            return

        print("=" * 100)
        print("STEP 1: OPENING WORKBOOK")
        print("=" * 100)

        wb = load_workbook(file_path, data_only=False)
        sheets = wb.sheetnames

        print(f"Total sheets: {len(sheets)}")
        for i, sheet in enumerate(sheets, 1):
            print(f"  {i}. {sheet}")

        print("\n" + "=" * 100)
        print("STEP 2: IDENTIFYING PRICE SHEETS")
        print("=" * 100)

        price_sheets = []
        keywords = ['preço', 'price', 'avg', 'médio', 'medio']

        for sheet_name in sheets:
            lower_name = sheet_name.lower()
            if any(kw in lower_name for kw in keywords):
                price_sheets.append(sheet_name)
                print(f"FOUND: {sheet_name}")

        if not price_sheets:
            print("No price sheets found. Showing first 3 rows of all sheets:")
            for sheet_name in sheets[:3]:
                print(f"\n{sheet_name}:")
                ws = wb[sheet_name]
                for i, row in enumerate(ws.iter_rows(values_only=True)):
                    if i < 3:
                        print(f"  Row {i+1}: {row}")
        else:
            print(f"\nTotal price sheets found: {len(price_sheets)}")

            print("\n" + "=" * 100)
            print("STEP 3: ANALYZING PRICE SHEETS WITH PANDAS")
            print("=" * 100)

            for sheet_name in price_sheets:
                print(f"\n{'='*100}")
                print(f"SHEET: {sheet_name}")
                print(f"{'='*100}")

                df = pd.read_excel(file_path, sheet_name=sheet_name)
                print(f"\nShape: {df.shape[0]} rows x {df.shape[1]} columns")
                print(f"Columns: {list(df.columns)}")
                print(f"\nFirst 10 rows:")
                print(df.head(10).to_string())

                print(f"\nData types:")
                print(df.dtypes)

                if df.shape[0] > 0:
                    print(f"\nFirst column unique values:")
                    unique_vals = df.iloc[:, 0].unique()
                    for val in unique_vals[:20]:
                        print(f"  - {val}")
                    if len(unique_vals) > 20:
                        print(f"  ... and {len(unique_vals) - 20} more")

        print("\n" + "=" * 100)
        print("ANALYSIS COMPLETE")
        print("=" * 100)

    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
