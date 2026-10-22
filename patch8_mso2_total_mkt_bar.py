"""
patch8_mso2_total_mkt_bar.py
Corrige o gráfico TOTAL MERCADO no card MSO2 (mso2-mkt-total):
  - acum25v e acum26v incluíam apenas janmar_val (Jan+Fev+Mar)
  - Agora somam também abr25_val / abr26_val → Jan+Fev+Mar+Abr correto
  - Unidades: sem dado de Abr disponível, mantém janmar (só R$)
"""
import os, shutil, datetime

BASE = r"C:\Users\valqu\OneDrive\Documentos\Claude\Projects\projeto Dashboard_farma_sul\Dashboard_farma_sul"
SRC  = os.path.join(BASE, "Dashboard_Farma_Sul_20260512_2220.html")

with open(SRC, 'r', encoding='utf-8') as f:
    html = f.read()

original_len = len(html)

OLD = (
    '      var acum25v = fytMkt ? (fytMkt.janmar25_val||0) : 0;\n'
    '      var acum26v = fytMkt ? (fytMkt.janmar26_val||0) : 0;'
)

NEW = (
    '      var acum25v = fytMkt ? ((fytMkt.janmar25_val||0)+(fytMkt.abr25_val||0)) : 0;\n'
    '      var acum26v = fytMkt ? ((fytMkt.janmar26_val||0)+(fytMkt.abr26_val||0)) : 0;'
)

count = html.count(OLD)
print(f"Ocorrências encontradas: {count}")

if count == 0:
    print("ERRO: trecho não encontrado — verifique o arquivo")
    exit(1)
if count > 1:
    print(f"AVISO: {count} ocorrências — esperado 1")

html = html.replace(OLD, NEW)
print(f"Patch aplicado: acum25v/acum26v agora somam abr_val")
print(f"Original: {original_len:,} | Final: {len(html):,} | Diff: {len(html)-original_len:+,}")

with open(SRC, 'w', encoding='utf-8') as f:
    f.write(html)
print(f"\nSalvo: {SRC}")

VER = os.path.join(BASE, "versoes", f"Dashboard_Farma_Sul_{datetime.datetime.now().strftime('%Y%m%d_%H%M')}_MSO2TotalBarFix.html")
shutil.copy2(SRC, VER)
print(f"Versão: {VER}")
