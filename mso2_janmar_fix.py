# mso2_janmar_fix.py — Hard-code período estrito Jan-Mar no card MSO2
import shutil, sys, os
sys.stdout.reconfigure(encoding='utf-8')

BASE = r'C:\Users\valqu\OneDrive\Documentos\Claude\Projects\projeto Dashboard_farma_sul'
SRC  = BASE + r'\Dashboard_farma_sul\Dashboard_Farma_Sul_20260512_2220.html'
BKP  = BASE + r'\Dashboard_farma_sul\versoes\Dashboard_Farma_Sul_20260513_1410_PreJanMarFix.html'
OUT  = BASE + r'\Dashboard_farma_sul\versoes\Dashboard_Farma_Sul_20260513_1415_JanMarFix.html'

shutil.copy2(SRC, BKP)
print(f'Backup: {os.path.basename(BKP)}')

with open(SRC, encoding='utf-8') as f:
    c = f.read()

orig_lines = len(c.splitlines())
ok = 0

def rep(label, old, new):
    global c, ok
    n = c.count(old)
    if n == 0:
        print(f'  MISS  {label}')
        return False
    c = c.replace(old, new, 1)
    print(f'  OK ({n})  {label}')
    ok += 1
    return True

NBSP = '\xa0'  # U+00A0 — como está gravado no arquivo

# ── 1. Headline R$/Un ──────────────────────────────────────────────────────
print('\n=== Headline R$/Un ===')
rep('Jul-Mar YoY → Jan-Mar YoY',
    f"' · <span style=\"font-size:11px;color:#94A3B8;\">' + (isVal?'R$ MM':'Unidades') + ' Jul-Mar YoY:{NBSP}</span>'",
    f"' · <span style=\"font-size:11px;color:#94A3B8;\">' + (isVal?'R$ MM':'Unidades') + ' Jan-Mar YoY:{NBSP}</span>'"
)

# ── 2. Tooltip labels ──────────────────────────────────────────────────────
print('\n=== Tooltip R$/Un ===')
rep('tooltip Jul-Mar/25 → Jan-Mar/25 (est.)',
    '<span class="mso2-tip-lbl">Jul-Mar/25</span>',
    '<span class="mso2-tip-lbl">Jan-Mar/25 (est.)</span>'
)
rep('tooltip Jul-Mar/26 → Jan-Mar/26',
    '<span class="mso2-tip-lbl">Jul-Mar/26</span>',
    '<span class="mso2-tip-lbl">Jan-Mar/26</span>'
)
rep('tooltip Δ Jul-Mar → Δ JAN-MAR (YoY)',
    '<span class="mso2-tip-lbl">Δ Jul-Mar</span>',
    '<span class="mso2-tip-lbl">Δ JAN-MAR (YoY)</span>'
)

# ── 3. Cabeçalho tabela ────────────────────────────────────────────────────
print('\n=== Cabeçalho tabela ===')
rep("header 'Δ Jul-Mar' → 'Δ JAN-MAR (YoY)'",
    "'Δ Jul-Mar'",
    "'Δ JAN-MAR (YoY)'"
)

# ── 4. Rodapé GrowthMode ──────────────────────────────────────────────────
print('\n=== Rodapé GrowthMode ===')
rep('rodapé Jul-Mar → Jan-Mar',
    '★ Δ baseado em Jul-Mar (dados mensais 2025 R$/Un não disponíveis individualmente)',
    '★ Acum Jan-Mar/25 estimado proporcionalmente a partir de dados disponíveis.'
)

# ── 5. renderMSO2Insight ───────────────────────────────────────────────────
print('\n=== renderMSO2Insight ===')
rep('insight ·\xa0· Jul-Mar/25 → Jan-Mar/25 (est.)',
    f"'{NBSP}·{NBSP} Jul-Mar/25: '+fmtNI(f25)",
    f"'{NBSP}·{NBSP} Jan-Mar/25 (est.): '+fmtNI(f25)"
)
rep('insight → Jul-Mar/26 → Jan-Mar/26',
    "' → Jul-Mar/26: <strong style=\"color:'+cor+';\">'",
    "' → Jan-Mar/26: <strong style=\"color:'+cor+';\">'",
)

# ── Write ──────────────────────────────────────────────────────────────────
with open(OUT, 'w', encoding='utf-8') as f:
    f.write(c)
shutil.copy2(OUT, SRC)
print(f'\n  Copied to active: {os.path.basename(SRC)}')
print(f'Linhas: {orig_lines} → {len(c.splitlines())} ({len(c.splitlines())-orig_lines:+d})')
print(f'Patches OK: {ok}/8')
print(f'Versão: {os.path.basename(OUT)}')

# ── Verify ─────────────────────────────────────────────────────────────────
print()
lines_list = c.splitlines()
mso2_block = '\n'.join(lines_list[9459:13720])

absent = ['Jul-Mar YoY', 'Jul-Mar/25', 'Jul-Mar/26', 'Δ Jul-Mar', 'baseado em Jul-Mar']
present = ['Jan-Mar YoY', 'Jan-Mar/25 (est.)', 'Jan-Mar/26', 'Δ JAN-MAR (YoY)', 'Jan-Mar/25 estimado']

print('--- AUSENTES no bloco MSO2 (OK = não encontrado) ---')
for n in absent:
    found = n in mso2_block
    print(f"  {'FAIL ainda presente!' if found else 'OK  ausente':20s}  {n}")

print()
print('--- PRESENTES no arquivo (OK = encontrado) ---')
for n in present:
    found = n in c
    print(f"  {'OK  ' if found else 'FAIL':20s}  {n}")
