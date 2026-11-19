"""
patch_shr_trend_fy26.py
Injeta os arrays fy26 no SHR_TREND_DATA do dashboard HTML.
Lê shr_trend_fy26.json e adiciona fy26:[...] em cada linha de marca.
"""
import os, json, re, shutil
from datetime import datetime

BASE     = r"C:\Users\valqu\OneDrive\Documentos\Claude\Projects\projeto Dashboard_farma_sul"
HTML_DIR = os.path.join(BASE, "Dashboard_farma_sul")
SRC_HTML = os.path.join(HTML_DIR, "Dashboard_Farma_Sul_20260512_2220.html")
JSON_PATH = os.path.join(BASE, "shr_trend_fy26.json")

# Criar versão antes de editar
ts = datetime.now().strftime("%Y%m%d_%H%M")
VER_DIR  = os.path.join(HTML_DIR, "versoes")
os.makedirs(VER_DIR, exist_ok=True)
VER_HTML = os.path.join(VER_DIR, f"Dashboard_Farma_Sul_{ts}.html")
shutil.copy2(SRC_HTML, VER_HTML)
print(f"Versão criada: {VER_HTML}")

# Carregar dados fy26
with open(JSON_PATH, "r", encoding="utf-8") as f:
    fy26_data = json.load(f)

print(f"Mercados no JSON: {len(fy26_data)}")

# Formatar array JS: [v0, v1, ..., null, null, null]
def fmt_arr(arr):
    parts = []
    for v in arr:
        if v is None:
            parts.append("null")
        else:
            parts.append(str(v))
    return "[" + ",".join(parts) + "]"

# Ler HTML
print(f"Lendo {SRC_HTML}...")
with open(SRC_HTML, "r", encoding="utf-8") as f:
    lines = f.readlines()

print(f"Total de linhas: {len(lines)}")

# Processar linha a linha
# Estado: dentro do SHR_TREND_DATA, mercado atual
in_shr = False
current_mkt = None
new_lines = []

# Padrões
pat_start = re.compile(r"const SHR_TREND_DATA\s*=\s*\{")
pat_mkt   = re.compile(r"^\s+'([^']+)':\s*\{$")  # início de mercado
pat_brand = re.compile(r"^(\s+'(OFF!|EXPOSIS|XO INSETO|SUPER REPELEX|SBP)':\s+\{)(fy24:\[.*?\],fy25:\[.*?\])(},?)$")
pat_end   = re.compile(r"^\};\s*$")  # fim do objeto

changes = 0
skipped_brands = []

for i, line in enumerate(lines):
    stripped = line.rstrip("\n")

    if not in_shr:
        if pat_start.search(stripped):
            in_shr = True
        new_lines.append(line)
        continue

    # Dentro do SHR_TREND_DATA
    # Detectar abertura de mercado: '  Farma Sul': {'
    mkt_match = re.match(r"^  '([^']+)':\s*\{$", stripped)
    if mkt_match:
        current_mkt = mkt_match.group(1)
        new_lines.append(line)
        continue

    # Detectar linha de marca
    # Padrão: "    'OFF!':          {fy24:[...],fy25:[...]},"
    brand_match = re.match(
        r"^(\s+'(OFF!|EXPOSIS|XO INSETO|SUPER REPELEX|SBP)':\s+\{)(fy24:\[.*?\],fy25:\[.*?\])(},?)$",
        stripped
    )
    if brand_match:
        prefix   = brand_match.group(1)   # "    'OFF!':          {"
        brand    = brand_match.group(2)   # "OFF!"
        fy_data  = brand_match.group(3)   # "fy24:[...],fy25:[...]"
        suffix   = brand_match.group(4)   # "}," ou "}"

        # Verificar se já tem fy26 (segurança)
        if "fy26:" in stripped:
            new_lines.append(line)
            changes += 1  # já está correto, contar
            continue

        # Buscar fy26 no JSON
        if current_mkt and current_mkt in fy26_data and brand in fy26_data[current_mkt]:
            fy26_arr = fy26_data[current_mkt][brand]
            fy26_str = fmt_arr(fy26_arr)
            new_data = fy_data + ",fy26:" + fy26_str
            # Reconstruir linha com mesma indentação
            indent = len(stripped) - len(stripped.lstrip())
            new_line = " " * indent + prefix.lstrip() + new_data + suffix + "\n"
            # Preservar indentação original
            original_indent = line[:len(line) - len(line.lstrip())]
            new_line = original_indent + prefix.lstrip() + new_data + suffix + "\n"
            new_lines.append(new_line)
            changes += 1
        else:
            # Mercado ou marca não encontrado no JSON
            skipped_brands.append(f"{current_mkt}::{brand}")
            new_lines.append(line)
        continue

    # Detectar fim do SHR_TREND_DATA (linha com apenas "};")
    if stripped == "};":
        in_shr = False
        current_mkt = None

    new_lines.append(line)

print(f"Linhas modificadas: {changes}")
if skipped_brands:
    print(f"Marcas sem dados fy26: {skipped_brands}")

# Gravar HTML atualizado
print(f"Gravando {SRC_HTML}...")
with open(SRC_HTML, "w", encoding="utf-8") as f:
    f.writelines(new_lines)

print("✅ Patch aplicado com sucesso!")

# Verificação rápida
print("\n=== VERIFICAÇÃO PÓS-PATCH ===")
import subprocess
result = subprocess.run(
    ["python", "-c", f"""
import re
with open(r'{SRC_HTML}', 'r', encoding='utf-8') as f:
    content = f.read()
# Contar ocorrências de fy26: no SHR_TREND_DATA
idx_start = content.find('const SHR_TREND_DATA')
idx_end   = content.find('var _shrActiveBrand')
chunk = content[idx_start:idx_end]
cnt = chunk.count('fy26:')
print(f'fy26: entries no SHR_TREND_DATA: {{cnt}}')
# Verificar Farma Sul OFF!
m = re.search(r"'Farma Sul': \\{{.*?'OFF!':\\s+\\{{(.*?)\\}},", chunk, re.DOTALL)
if m:
    print('Farma Sul / OFF! encontrado')
    line = m.group(1)[:200]
    print('  ' + line)
"""],
    capture_output=True, text=True
)
print(result.stdout)
if result.stderr:
    print("STDERR:", result.stderr[:300])
