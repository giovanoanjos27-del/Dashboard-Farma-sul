"""
patch_all_others_todos_mercados.py
====================================
Atualiza ALL OTHERS CAMP em TODOS os mercados (exceto T.BR Farma, já corrigido).

Estruturas corrigidas:
  1. FYTD_MARKET_TOTAL — somar AOC a todos os campos fytd/jan/fev/mar/janmar
  2. VOL_MKT_DATA       — somar AOC a fytd e monthly_val/un
  3. MKTSHARE_OVERVIEW  — adicionar entrada ALL OTHERS CAMP (share %)
  4. NIELSEN_BRAND_VAL  — adicionar entrada ALL OTHERS CAMP (R$M + un)

Fonte dos dados: all_others_data.py (extraído de Base Giovano 26-04.xlsx)
"""
import sys, re, shutil
sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path
from datetime import datetime

# ──────────────────────────────────────────────────────────────────────────────
# 0. Paths e backup
# ──────────────────────────────────────────────────────────────────────────────
BASE = Path(r'C:\Users\valqu\OneDrive\Documentos\Claude\Projects\projeto Dashboard_farma_sul')
DASH = BASE / 'Dashboard_farma_sul' / 'Dashboard_Farma_Sul_20260512_2220.html'
VER  = DASH.parent / 'versoes'
DL   = Path.home() / 'Downloads'
ts   = datetime.now().strftime('%Y%m%d_%H%M')

shutil.copy(DASH, VER / f'Dashboard_Farma_Sul_{ts}_PreAllOthers.html')
h = DASH.read_text(encoding='utf-8')
print(f'Backup: ...PreAllOthers.html  |  {len(h):,} chars')

# ──────────────────────────────────────────────────────────────────────────────
# 1. Carregar dados AOC
# ──────────────────────────────────────────────────────────────────────────────
sys.path.insert(0, str(BASE))
from all_others_data import DATA

SKIP = {'T.BR Farma'}  # já corrigido em patches anteriores

# ──────────────────────────────────────────────────────────────────────────────
# Utilitários
# ──────────────────────────────────────────────────────────────────────────────
def fmt(v, d=4):
    """Formata número com d casas, sem zeros desnecessários."""
    s = f'{v:.{d}f}'
    # remover zeros finais após ponto mas manter ao menos 4 decimais se > 0
    return s.rstrip('0').rstrip('.') if '.' in s else s

def rnd(v, d=4):
    return round(v, d)

errors = []
ok_count = 0

# ──────────────────────────────────────────────────────────────────────────────
# 2. FYTD_MARKET_TOTAL — regex por mercado
# ──────────────────────────────────────────────────────────────────────────────
print('\n══ FYTD_MARKET_TOTAL ══')

# Padrão de uma entrada: 'MARKET': {fytd25_val:X,...janmar26_un:X},
FYTD_PAT = re.compile(
    r"('(?P<mkt>[^']+)':\s*\{"
    r"fytd25_val:(?P<fytd25_val>[\d.]+),"
    r"fytd26_val:(?P<fytd26_val>[\d.]+),"
    r"fytd25_un:(?P<fytd25_un>[\d.]+),"
    r"fytd26_un:(?P<fytd26_un>[\d.]+),"
    r"jan25_val:(?P<jan25_val>[\d.]+),"
    r"fev25_val:(?P<fev25_val>[\d.]+),"
    r"mar25_val:(?P<mar25_val>[\d.]+),"
    r"janmar25_val:(?P<janmar25_val>[\d.]+),"
    r"jan26_val:(?P<jan26_val>[\d.]+),"
    r"fev26_val:(?P<fev26_val>[\d.]+),"
    r"mar26_val:(?P<mar26_val>[\d.]+),"
    r"janmar26_val:(?P<janmar26_val>[\d.]+),"
    r"jan25_un:(?P<jan25_un>[\d.]+),"
    r"fev25_un:(?P<fev25_un>[\d.]+),"
    r"mar25_un:(?P<mar25_un>[\d.]+),"
    r"janmar25_un:(?P<janmar25_un>[\d.]+),"
    r"jan26_un:(?P<jan26_un>[\d.]+),"
    r"fev26_un:(?P<fev26_un>[\d.]+),"
    r"mar26_un:(?P<mar26_un>[\d.]+),"
    r"janmar26_un:(?P<janmar26_un>[\d.]+)\})"
)

fytd_done = 0
for m in FYTD_PAT.finditer(h):
    mkt = m.group('mkt')
    if mkt not in DATA or mkt in SKIP:
        continue
    d = DATA[mkt]
    old = m.group(1)

    # Valores novos = antigo + AOC
    fytd25_v_new = rnd(float(m.group('fytd25_val')) + d['aoc_fytd25_v'])
    fytd26_v_new = rnd(float(m.group('fytd26_val')) + d['aoc_fytd26_v'])
    fytd25_u_new = rnd(float(m.group('fytd25_un'))  + d['aoc_fytd25_u'])
    fytd26_u_new = rnd(float(m.group('fytd26_un'))  + d['aoc_fytd26_u'])
    jan25_v_new  = rnd(float(m.group('jan25_val'))   + d['aoc_jan25_v'])
    fev25_v_new  = rnd(float(m.group('fev25_val'))   + d['aoc_fev25_v'])
    mar25_v_new  = rnd(float(m.group('mar25_val'))   + d['aoc_mar25_v'])
    janmar25_new = rnd(jan25_v_new + fev25_v_new + mar25_v_new)
    jan26_v_new  = rnd(float(m.group('jan26_val'))   + d['aoc_jan26_v'])
    fev26_v_new  = rnd(float(m.group('fev26_val'))   + d['aoc_fev26_v'])
    mar26_v_new  = rnd(float(m.group('mar26_val'))   + d['aoc_mar26_v'])
    janmar26_new = rnd(jan26_v_new + fev26_v_new + mar26_v_new)
    jan25_u_new  = rnd(float(m.group('jan25_un'))    + d['aoc_jan25_u'])
    fev25_u_new  = rnd(float(m.group('fev25_un'))    + d['aoc_fev25_u'])
    mar25_u_new  = rnd(float(m.group('mar25_un'))    + d['aoc_mar25_u'])
    janmar25_u   = rnd(jan25_u_new + fev25_u_new + mar25_u_new)
    jan26_u_new  = rnd(float(m.group('jan26_un'))    + d['aoc_jan26_u'])
    fev26_u_new  = rnd(float(m.group('fev26_un'))    + d['aoc_fev26_u'])
    mar26_u_new  = rnd(float(m.group('mar26_un'))    + d['aoc_mar26_u'])
    janmar26_u   = rnd(jan26_u_new + fev26_u_new + mar26_u_new)

    new = (f"'{mkt}': {{"
           f"fytd25_val:{fytd25_v_new},fytd26_val:{fytd26_v_new},"
           f"fytd25_un:{fytd25_u_new},fytd26_un:{fytd26_u_new},"
           f"jan25_val:{jan25_v_new},fev25_val:{fev25_v_new},mar25_val:{mar25_v_new},janmar25_val:{janmar25_new},"
           f"jan26_val:{jan26_v_new},fev26_val:{fev26_v_new},mar26_val:{mar26_v_new},janmar26_val:{janmar26_new},"
           f"jan25_un:{jan25_u_new},fev25_un:{fev25_u_new},mar25_un:{mar25_u_new},janmar25_un:{janmar25_u},"
           f"jan26_un:{jan26_u_new},fev26_un:{fev26_u_new},mar26_un:{mar26_u_new},janmar26_un:{janmar26_u}}}")

    cnt = h.count(old)
    if cnt != 1:
        errors.append(f'FYTD {mkt}: {cnt}x encontrado')
        continue
    h = h.replace(old, new, 1)
    fytd_done += 1

print(f'  Atualizados: {fytd_done} mercados')

# ──────────────────────────────────────────────────────────────────────────────
# 3. VOL_MKT_DATA — regex por mercado
# ──────────────────────────────────────────────────────────────────────────────
print('\n══ VOL_MKT_DATA ══')

VOL_PAT = re.compile(
    r"('(?P<mkt>[^']+)':\s*\{"
    r"fytd25_val:(?P<fytd25_val>[\d.]+),"
    r"fytd26_val:(?P<fytd26_val>[\d.]+),"
    r"fytd25_un:(?P<fytd25_un>[\d.]+),"
    r"fytd26_un:(?P<fytd26_un>[\d.]+),"
    r"monthly_val:\[(?P<mv>[^\]]+)\],"
    r"monthly_un:\[(?P<mu>[^\]]+)\]\})"
)

vol_done = 0
for m in VOL_PAT.finditer(h):
    mkt = m.group('mkt')
    if mkt not in DATA or mkt in SKIP:
        continue
    d = DATA[mkt]
    old = m.group(1)

    mv_old = [float(x.strip()) for x in m.group('mv').split(',')]
    mu_old = [float(x.strip()) for x in m.group('mu').split(',')]

    fytd25_new = rnd(float(m.group('fytd25_val')) + d['aoc_fytd25_v'])
    fytd26_new = rnd(float(m.group('fytd26_val')) + d['aoc_fytd26_v'])
    fytd25_u   = rnd(float(m.group('fytd25_un'))  + d['aoc_fytd25_u'])
    fytd26_u   = rnd(float(m.group('fytd26_un'))  + d['aoc_fytd26_u'])

    aoc_mv = d['aoc_monthly_v26']
    aoc_mu = d['aoc_monthly_u26']

    n = len(mv_old)
    if n == len(aoc_mv):
        mv_new = [rnd(mv_old[i] + aoc_mv[i]) for i in range(n)]
        mu_new = [rnd(mu_old[i] + aoc_mu[i]) for i in range(n)]
    elif n == 10 and len(aoc_mv) == 9:
        # 10th element = repeat of 9th (T.BR Farma pattern) — já foi tratado
        mv_new = [rnd(mv_old[i] + aoc_mv[min(i,8)]) for i in range(n)]
        mu_new = [rnd(mu_old[i] + aoc_mu[min(i,8)]) for i in range(n)]
    else:
        errors.append(f'VOL {mkt}: monthly len mismatch old={n} aoc={len(aoc_mv)}')
        continue

    mv_str = ','.join(str(x) for x in mv_new)
    mu_str = ','.join(str(x) for x in mu_new)

    new = (f"'{mkt}': {{"
           f"fytd25_val:{fytd25_new},fytd26_val:{fytd26_new},"
           f"fytd25_un:{fytd25_u},fytd26_un:{fytd26_u},"
           f"monthly_val:[{mv_str}],monthly_un:[{mu_str}]}}")

    cnt = h.count(old)
    if cnt != 1:
        errors.append(f'VOL {mkt}: {cnt}x encontrado')
        continue
    h = h.replace(old, new, 1)
    vol_done += 1

print(f'  Atualizados: {vol_done} mercados')

# ──────────────────────────────────────────────────────────────────────────────
# 4. MKTSHARE_OVERVIEW — trabalhar dentro da seção específica
# ──────────────────────────────────────────────────────────────────────────────
print('\n══ MKTSHARE_OVERVIEW ══')

def process_section(h, section_start_marker, data_dict, skip_set, is_mso):
    """
    Processa uma seção (MSO ou NBV) inserindo ALL OTHERS CAMP após SBP em cada mercado.
    is_mso=True: usa fytd25: (sem _val)  |  is_mso=False: usa fytd25_val:
    """
    sec_start = h.find(section_start_marker)
    if sec_start == -1:
        return h, 0, [f'{section_start_marker}: não encontrado']
    sec_end = h.find('\n};', sec_start) + 3
    sec = h[sec_start:sec_end]

    done = 0
    errs = []

    # Padrão do SBP diferente por seção
    if is_mso:
        sbp_pat = r"(    'SBP':\s*\{fytd25:[^_][^\n]+\},?\n)"
    else:
        sbp_pat = r"(    'SBP':\s*\{fytd25_val:[^\n]+\},?\n)"

    for mkt, d in sorted(data_dict.items()):
        if mkt in skip_set:
            continue

        mkt_esc = re.escape(mkt)
        pat = re.compile(
            r"(  '" + mkt_esc + r"':\s*\{(?:.*?\n)*?)"
            + sbp_pat +
            r"(  \},\n)",
            re.DOTALL
        )
        matches = list(pat.finditer(sec))
        if len(matches) == 0:
            continue  # mercado não presente nesta seção
        if len(matches) != 1:
            errs.append(f'{mkt}: {len(matches)} blocos na seção')
            continue

        m = matches[0]
        bloco = m.group(0)
        if 'ALL OTHERS CAMP' in bloco:
            continue  # já tem

        if is_mso:
            # Calcular share %
            tot_fytd25 = d['tot_fytd25_v'] if d['tot_fytd25_v'] > 0 else 1
            tot_fytd26 = d['tot_fytd26_v'] if d['tot_fytd26_v'] > 0 else 1
            fytd25_shr = rnd(d['aoc_fytd25_v'] / tot_fytd25 * 100, 2)
            fytd26_shr = rnd(d['aoc_fytd26_v'] / tot_fytd26 * 100, 2)
            delta_shr  = rnd(fytd26_shr - fytd25_shr, 2)
            mv26  = d['tot_monthly_v26']
            amv26 = d['aoc_monthly_v26']
            monthly_shr = []
            for i in range(9):
                tot_m = mv26[i] if i < len(mv26) else 0
                aoc_m = amv26[i] if i < len(amv26) else 0
                monthly_shr.append(rnd(aoc_m/tot_m*100,2) if tot_m > 0 else 'null')
            monthly_str = ','.join(str(x) for x in monthly_shr)
            jan25_s = rnd(d['aoc_jan25_v']/d['tot_jan25_v']*100,2) if d['tot_jan25_v'] > 0 else 'null'
            feb25_s = rnd(d['aoc_fev25_v']/d['tot_fev25_v']*100,2) if d['tot_fev25_v'] > 0 else 'null'
            mar25_s = rnd(d['aoc_mar25_v']/d['tot_mar25_v']*100,2) if d['tot_mar25_v'] > 0 else 'null'
            aoc_line = (f"    'ALL OTHERS CAMP': {{fytd25:{fytd25_shr}, fytd26:{fytd26_shr}, delta:{delta_shr},"
                        f" monthly:[{monthly_str}], jan25:{jan25_s}, feb25:{feb25_s}, mar25:{mar25_s}}},\n")
        else:
            # NIELSEN_BRAND_VAL
            sbp_line = m.group(2)
            mv_match = re.search(r'monthly_val:\[([^\]]+)\]', sbp_line)
            n_monthly = len(mv_match.group(1).split(',')) if mv_match else 9
            aoc_mv = d['aoc_monthly_v26'][:9]
            aoc_mu = d['aoc_monthly_u26'][:9]
            if n_monthly == 10:
                aoc_mv = list(aoc_mv) + [aoc_mv[8]]
                aoc_mu = list(aoc_mu) + [aoc_mu[8]]
            mv_str = ', '.join(str(rnd(x, 3)) for x in aoc_mv)
            mu_str = ', '.join(str(rnd(x, 1)) for x in aoc_mu)
            aoc_line = (
                f"    'ALL OTHERS CAMP': {{"
                f"fytd25_val:{rnd(d['aoc_fytd25_v'])},fytd26_val:{rnd(d['aoc_fytd26_v'])},"
                f"fytd25_un:{rnd(d['aoc_fytd25_u'])},fytd26_un:{rnd(d['aoc_fytd26_u'])},"
                f"jan_val:{rnd(d['aoc_jan26_v'],4)},fev_val:{rnd(d['aoc_fev26_v'],4)},mar_val:{rnd(d['aoc_mar26_v'],4)},"
                f"jan_un:{rnd(d['aoc_jan26_u'],4)},fev_un:{rnd(d['aoc_fev26_u'],4)},mar_un:{rnd(d['aoc_mar26_u'],4)},"
                f"monthly_val:[{mv_str}],monthly_un:[{mu_str}],"
                f"jan25_val:{rnd(d['aoc_jan25_v'],4)},fev25_val:{rnd(d['aoc_fev25_v'],4)},mar25_val:{rnd(d['aoc_mar25_v'],4)},"
                f"jan25_un:{rnd(d['aoc_jan25_u'],4)},fev25_un:{rnd(d['aoc_fev25_u'],4)},mar25_un:{rnd(d['aoc_mar25_u'],4)}}},\n"
            )

        old_in_sec = m.group(2) + m.group(3)
        new_in_sec = m.group(2) + aoc_line + m.group(3)
        cnt = sec.count(old_in_sec)
        if cnt != 1:
            errs.append(f'{mkt}: {cnt}x na seção')
            continue
        sec = sec.replace(old_in_sec, new_in_sec, 1)
        done += 1

    # Remontar HTML
    h_new = h[:sec_start] + sec + h[sec_end:]
    return h_new, done, errs

h, mso_done, mso_errs = process_section(h, 'MKTSHARE_OVERVIEW = {', DATA, SKIP, is_mso=True)
errors.extend(mso_errs)
print(f'  Atualizados: {mso_done} mercados')

# ──────────────────────────────────────────────────────────────────────────────
# 5. NIELSEN_BRAND_VAL — trabalhar dentro da seção específica
# ──────────────────────────────────────────────────────────────────────────────
print('\n══ NIELSEN_BRAND_VAL ══')

h, nbv_done, nbv_errs = process_section(h, 'NIELSEN_BRAND_VAL = {', DATA, SKIP, is_mso=False)
errors.extend(nbv_errs)

print(f'  Atualizados: {nbv_done} mercados')

# ──────────────────────────────────────────────────────────────────────────────
# Relatório
# ──────────────────────────────────────────────────────────────────────────────
if errors:
    print(f'\n⚠ Erros/avisos ({len(errors)}):')
    for e in errors[:20]:
        print(f'  {e}')

print(f'\nTamanho final: {len(h):,} chars')
print(f'Diferença: +{len(h)-18030951:,} chars')

# Verificações básicas
assert 'ALL OTHERS CAMP' in h
aoc_count = h.count("'ALL OTHERS CAMP'")
print(f"ALL OTHERS CAMP com aspas: {aoc_count}")
# Mínimo esperado: ~4 já existentes + 71 novos MSO + 71 novos NBV + FYTD/VOL não adicionam texto
assert aoc_count > 100, f'Poucos ALL OTHERS CAMP: {aoc_count}'

# ──────────────────────────────────────────────────────────────────────────────
# Salvar
# ──────────────────────────────────────────────────────────────────────────────
DASH.write_text(h, encoding='utf-8')
shutil.copy(DASH, VER / f'Dashboard_Farma_Sul_{ts}_AllOthersTodos.html')
shutil.copy(DASH, DL  / f'Dashboard_FarmaSul_Giovano_{ts}.html')
print(f'\nVersao:    Dashboard_Farma_Sul_{ts}_AllOthersTodos.html')
print(f'Downloads: Dashboard_FarmaSul_Giovano_{ts}.html')
print('DONE.')
