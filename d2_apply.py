import shutil, sys, os
sys.stdout.reconfigure(encoding='utf-8')

BASE = r'C:\Users\valqu\OneDrive\Documentos\Claude\Projects\projeto Dashboard_farma_sul'
SRC  = BASE + r'\Dashboard_farma_sul\Dashboard_Farma_Sul_20260512_2220.html'
BKP  = BASE + r'\Dashboard_farma_sul\versoes\Dashboard_Farma_Sul_20260513_1210_PreD2.html'
OUT  = BASE + r'\Dashboard_farma_sul\versoes\Dashboard_Farma_Sul_20260513_1215_D2.html'

shutil.copy2(SRC, BKP)
print(f'Backup: {os.path.basename(BKP)}')

with open(SRC, encoding='utf-8') as f:
    content = f.read()

orig_lines = len(content.splitlines())
c = content
ok_count = 0

def patch(label, old, new, src):
    n = src.count(old)
    if n == 0:
        print(f'  MISS ({n})  {label}')
        return src, False
    if n > 1:
        print(f'  WARN ({n})  {label}  — using first occurrence')
    r = src.replace(old, new, 1)
    print(f'  OK    {label}')
    return r, True

def header(name):
    bar = '═' * (len(name) + 2)
    return f'\n/* ═{bar}═ */\n/* ═ {name} ═ */\n/* ═{bar}═ */'

# ════════════════════════════════════════════════════════════════════════════
# D2 — Structural comment headers (no code moved, pure annotation)
# ════════════════════════════════════════════════════════════════════════════
print('\n=== D2 — headers ===')

inserts = [
    # (anchor_old, header_text)
    ('const SJ_UNID = {',
     header('SÃO JOÃO — SELL-OUT (VOL + RECEITA)') + '\nconst SJ_UNID = {'),

    ('const NS = {',
     header('NISSEI — SELL-OUT (VOL + RECEITA + LOJAS)') + '\nconst NS = {'),

    ('const PV_VOL = {',
     header('PANVEL — SELL-OUT (VOL + RECEITA + RANK)') + '\nconst PV_VOL = {'),

    ('const CL_REC_2024 = [null,null,538754',
     header('CLAMED — SELL-OUT (VOL + RECEITA + RANK)') + '\nconst CL_REC_2024 = [null,null,538754'),

    ('const GAM_VOL = {',
     header('DD-GAM — SELL-OUT (VOL + RECEITA + RANK)') + '\nconst GAM_VOL = {'),

    ('const GAUCHA_VOL = {',
     header('DD-GAÚCHA — SELL-OUT (VOL + RECEITA + RANK)') + '\nconst GAUCHA_VOL = {'),

    ('const RIOMED_REC_2024 = [null',
     header('DD-RIOMED — SELL-OUT (VOL + RECEITA + RANK)') + '\nconst RIOMED_REC_2024 = [null'),

    ('const SJ_COBERTURA = [',
     header('SÃO JOÃO — COBERTURA & ESTOQUE') + '\nconst SJ_COBERTURA = ['),

    ('const NS_FILIAL_DATA = [',
     header('NISSEI — FILIAIS & COBERTURA') + '\nconst NS_FILIAL_DATA = ['),
]

for old, new in inserts:
    label = old[:50].strip()
    c, ok = patch(label, old, new, c)
    if not ok:
        sys.exit(1)
    ok_count += 1

# ── Write ─────────────────────────────────────────────────────────────────
with open(OUT, 'w', encoding='utf-8') as f:
    f.write(c)
shutil.copy2(OUT, SRC)
print(f'\n  Copied to active: {os.path.basename(SRC)}')

new_lines = len(c.splitlines())
delta = new_lines - orig_lines
print(f'\nLinhas: {orig_lines} → {new_lines} ({delta:+d})')
print(f'Headers adicionados: {ok_count}')
print(f'Versão: {os.path.basename(OUT)}')

# ── Verify ──────────────────────────────────────────────────────────────
print()
checks = [
    'SÃO JOÃO — SELL-OUT',
    'NISSEI — SELL-OUT',
    'PANVEL — SELL-OUT',
    'CLAMED — SELL-OUT',
    'DD-GAM — SELL-OUT',
    'DD-GAÚCHA — SELL-OUT',
    'DD-RIOMED — SELL-OUT',
    'SÃO JOÃO — COBERTURA',
    'NISSEI — FILIAIS',
]
for needle in checks:
    print(f"  {'OK  ' if needle in c else 'FAIL'}  {needle}")
