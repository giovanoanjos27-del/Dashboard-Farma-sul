"""
patch_sellin_metabi.py
Atualiza SELLIN_DATA e SELLIN_TOTAL com valores corretos do META BI X REAL GIOVANO.xlsx.

Fonte primária:  _Recursos/Giovano SCJ/META BI X REAL GIOVANO.xlsx  (plan, meta, hist)
Fonte secundária: Planilha_Mestre_FarmaSul_Giovano.xlsx               (real_m — mais recente)

Principais correções:
  • DD-GAM plan:  27.707 → 38.657  ← problema reportado pelo usuário
  • DD-Gaúcha plan: 29.460 → 25.433
  • Panvel plan:   18.456 → 13.177
  • Nissei plan:    7.825 → 10.540
  • DD-Riomed plan:  7.160 →  7.482
  • Clamed hist:    7.945 →  7.646
  • Todos os meta revisados conforme META BI
"""
import sys
from pathlib import Path
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

BASE = Path(r'C:\Users\valqu\OneDrive\Documentos\Claude\Projects\projeto Dashboard_farma_sul\Dashboard_farma_sul')
SRC  = BASE / 'Dashboard_Farma_Sul_20260512_2220.html'
VER  = BASE / 'versoes' / f'Dashboard_Farma_Sul_{datetime.now().strftime("%Y%m%d_%H%M")}_FixSellIn.html'

print('Lendo dashboard…')
h = SRC.read_text(encoding='utf-8')
orig_len = len(h)

# ─────────────────────────────────────────────────────────────────────────────
# NOVO SELLIN_DATA (valores extraídos do META BI + real_m do mestre)
# ─────────────────────────────────────────────────────────────────────────────
NEW_SELLIN = '''const SELLIN_DATA = [
  { nome:'São João', label:'São João', cor:'#60a5fa', canal:'Rede', hist:29814, plan:32064, meta:22651, real:23010, hist_per:29814, verba:662905,
    hist_m:[1281,5598,1015,9960,5409,3435,497,915,317,75,533,779],
    plan_m:[8500,0,0,10707,5814.68,3692.62,534.27,983.62,340.77,80.62,572.98,837.42],
    meta_m:[1158,3483,1867,4226,3428,3967,1540,1253,1085,644,0,0],
    real_m:[0,8132,3549,1659,1550,4571,1330,0,519,699,1001,null] },
  { nome:'DD-Gaúcha', label:'DD-Gaúcha', cor:'#f97316', canal:'Indireto', hist:24177, plan:25433.05, meta:13440, real:16011, hist_per:24177, verba:285636,
    hist_m:[1441,11854,1041,765,2026,2293,1990,490,944,960,193,180],
    plan_m:[15100,0,0,803.25,2127.3,2407.65,2089.5,514.5,991.2,1008,202.65,189],
    meta_m:[1707,2251,2213,1286,1096,1226,1023,1177,730,731,0,0],
    real_m:[5094,2523,335,436,252,1102,1752,3585,165,484,283,null] },
  { nome:'Panvel', label:'Panvel', cor:'#2dd4bf', canal:'Rede', hist:11158, plan:13177.2, meta:8596, real:11347, hist_per:11158, verba:690168,
    hist_m:[997,0,0,826,482,651,1433,2084,3364,166,970,185],
    plan_m:[500,500,1000,909,530,716,1576.3,2292.4,3700.4,182.6,1067,203.5],
    meta_m:[173,268,838,643,452,579,1769,2062,1081,731,0,0],
    real_m:[0,0,1573,213,465,1744,3869,2265,698,346,174,null] },
  { nome:'DD-GAM', label:'DD-GAM', cor:'#34d399', canal:'Indireto', hist:36721, plan:38657.2, meta:24667, real:49823, hist_per:36721, verba:493402,
    hist_m:[0,10211,170,3536,5744,3440,4359,1701,5586,930,101,943],
    plan_m:[0,11000,0,3713,6031.2,3612,4576.95,1786.05,5865.3,976.5,106.05,990.15],
    meta_m:[1539,1803,2293,3122,2495,2954,3125,3690,2197,1449,0,0],
    real_m:[0,5256,7808,7258,5620,3096,11589,5598,2390,0,1208,null] },
  { nome:'Nissei', label:'Nissei', cor:'#a78bfa', canal:'Rede', hist:9805, plan:10539.78, meta:5629, real:10805, hist_per:9805, verba:414000,
    hist_m:[0,0,3831,593,1133,1131,0,865,736,494,792,230],
    plan_m:[0,4118,0,637,1218,1216,0,929.88,791.2,531.05,851.4,247.25],
    meta_m:[523,699,699,653,572,644,412,472,257,698,0,0],
    real_m:[0,3490,2145,1476,1170,90,2242,54,56,0,82,null] },
  { nome:'DD-Riomed', label:'DD-Riomed', cor:'#fb923c', canal:'Indireto', hist:7100, plan:7482.2, meta:3847, real:6332, hist_per:7100, verba:200479,
    hist_m:[0,1852,2884,1758,0,0,23,12,0,193,378,0],
    plan_m:[0,5000,0,1845.9,0,0,24.15,12.6,0,202.65,396.9,0],
    meta_m:[713,899,724,357,309,347,43,71,55,329,0,0],
    real_m:[0,3743,296,0,1650,238,0,0,405,0,0,null] },
  { nome:'Clamed', label:'Clamed', cor:'#f472b6', canal:'Rede', hist:7646, plan:8411, meta:3639, real:5135, hist_per:7646, verba:125250,
    hist_m:[0,0,7456,190,0,0,0,0,0,0,0,0],
    plan_m:[0,0,8202,209,0,0,0,0,0,0,0,0],
    meta_m:[995,1261,906,54,44,51,7,85,132,104,0,0],
    real_m:[0,0,4731,80,0,24,300,0,0,0,0,null] },
  { nome:'Peniel', label:'Peniel', cor:'#94a3b8', canal:'Indireto', hist:2227, plan:2407.2, meta:1166, real:240, hist_per:2227, verba:7500,
    hist_m:[210,0,1153,460,105,0,0,299,0,0,0,0],
    plan_m:[0,1500,0,483,110.25,0,0,313.95,0,0,0,0],
    meta_m:[205,273,206,87,68,82,86,104,51,4,0,0],
    real_m:[0,0,0,240,0,0,0,0,0,0,0,null] }
];'''

OLD_SELLIN = '''const SELLIN_DATA = [
  { nome:'São João', label:'São João', cor:'#60a5fa', canal:'Rede', hist:29814, plan:32064, meta:23301, real:23010, hist_per:29814, verba:662905,
    hist_m:[1281,5598,1015,9960,5409,3435,497,915,317,75,533,779],
    plan_m:[8500,0,0,10707,5815,3693,534,984,341,81,573,837],
    meta_m:[1158,3483,1867,4226,3428,3967,1540,1253,1085,644,650,0],
    real_m:[0,8132,3549,1659,1550,4571,1330,0,519,699,1001,null] },
  { nome:'DD-Gaúcha', label:'DD-Gaúcha', cor:'#f97316', canal:'Indireto', hist:24177, plan:29460.4, meta:14099, real:16011, hist_per:24177, verba:285636,
    hist_m:[1441,11854,1041,765,2026,2293,1990,490,944,960,193,180],
    plan_m:[15100,0,0,803,2127,2408,1576,2292,3700,183,1067,204],
    meta_m:[1707,2251,2213,1286,1096,1226,1023,1177,730,731,659,0],
    real_m:[5094,2523,335,436,252,1102,1752,3585,165,484,283,null] },
  { nome:'Panvel', label:'Panvel', cor:'#2dd4bf', canal:'Rede', hist:11158, plan:18456, meta:9233, real:11347, hist_per:11158, verba:690168,
    hist_m:[997,0,0,826,482,651,1433,2084,3364,166,970,185],
    plan_m:[500,500,1000,909,530,716,4577,1786,5865,976,106,990],
    meta_m:[173,268,838,643,452,579,1769,2062,1081,731,637,0],
    real_m:[0,0,1573,213,465,1744,3869,2265,698,346,174,null] },
  { nome:'DD-GAM', label:'DD-GAM', cor:'#34d399', canal:'Indireto', hist:36721, plan:27706.98, meta:25964, real:49823, hist_per:36721, verba:493402,
    hist_m:[0,10211,170,3536,5744,3440,4359,1701,5586,930,101,943],
    plan_m:[0,11000,0,3713,6031,3612,0,930,791,531,851,247],
    meta_m:[1539,1803,2293,3122,2495,2954,3125,3690,2197,1449,1297,0],
    real_m:[0,5256,7808,7258,5620,3096,11589,5598,2390,0,1208,null] },
  { nome:'Nissei', label:'Nissei', cor:'#a78bfa', canal:'Rede', hist:9805, plan:7825.3, meta:6252, real:10805, hist_per:9805, verba:414000,
    hist_m:[0,0,3831,593,1133,1131,0,865,736,494,792,230],
    plan_m:[0,4118,0,637,1218,1216,24,13,0,203,397,0],
    meta_m:[523,699,699,653,572,644,412,472,257,698,623,0],
    real_m:[0,3490,2145,1476,1170,90,2242,54,56,0,82,null] },
  { nome:'DD-Riomed', label:'DD-Riomed', cor:'#fb923c', canal:'Indireto', hist:7100, plan:7159.85, meta:4138, real:6332, hist_per:7100, verba:200479,
    hist_m:[0,1852,2884,1758,0,0,23,12,0,193,378,0],
    plan_m:[0,5000,0,1846,0,0,0,314,0,0,0,0],
    meta_m:[713,899,724,357,309,347,43,71,55,333,287,0],
    real_m:[0,3743,296,0,1650,238,0,0,405,0,0,null] },
  { nome:'Clamed', label:'Clamed', cor:'#f472b6', canal:'Rede', hist:7945, plan:8411, meta:3740, real:5135, hist_per:7945, verba:125250,
    hist_m:[0,0,7456,190,0,0,0,299,0,0,0,0],
    plan_m:[0,0,8202,209,0,0,0,0,0,0,0,0],
    meta_m:[995,1261,906,54,44,51,7,85,132,104,101,0],
    real_m:[0,0,4731,80,0,24,300,0,0,0,0,null] },
  { nome:'Peniel', label:'Peniel', cor:'#94a3b8', canal:'Indireto', hist:2227, plan:2407, meta:1166, real:240, hist_per:2227, verba:7500,
    hist_m:[210,0,1153,460,105,0,0,299,0,0,0,0],
    plan_m:[0,1500,0,483,110,0,0,314,0,0,0,0],
    meta_m:[205,273,206,87,68,82,86,104,51,4,0,0],
    real_m:[0,0,0,240,0,0,0,0,0,0,0,null] }
];'''

count = h.count(OLD_SELLIN)
assert count == 1, f'SELLIN_DATA: encontrei {count} ocorrências (esperava 1)'
h = h.replace(OLD_SELLIN, NEW_SELLIN)
print('✅ SELLIN_DATA atualizado com valores do META BI')

# ─────────────────────────────────────────────────────────────────────────────
# SELLIN_TOTAL
# hist=128648, plan=138172, meta=83635, real=122703
# cres_hist=(122703-128648)/128648 = -4.6%
# cres_meta=(122703-83635)/83635  = 46.7%
# cx_falt = meta - real = 83635-122703 = -39068
# ─────────────────────────────────────────────────────────────────────────────
OLD_TOTAL = 'const SELLIN_TOTAL = {hist:128947, plan:133491, meta:87893, real:122703, hist_per:128947, cres_hist:-4.8, cres_meta:39.7, cx_falt:-34810};'
NEW_TOTAL = 'const SELLIN_TOTAL = {hist:128648, plan:138172, meta:83635, real:122703, hist_per:128648, cres_hist:-4.6, cres_meta:46.7, cx_falt:-39068};'

count_t = h.count(OLD_TOTAL)
assert count_t == 1, f'SELLIN_TOTAL: encontrei {count_t} ocorrências (esperava 1)'
h = h.replace(OLD_TOTAL, NEW_TOTAL)
print('✅ SELLIN_TOTAL atualizado (hist=128648, plan=138172, meta=83635, cx_falt=-39068)')

# ─────────────────────────────────────────────────────────────────────────────
# Verificações finais
# ─────────────────────────────────────────────────────────────────────────────
assert 'plan:38657.2' in h,   '❌ DD-GAM plan não atualizado'
assert 'plan:25433.05' in h,  '❌ DD-Gaúcha plan não atualizado'
assert 'plan:13177.2' in h,   '❌ Panvel plan não atualizado'
assert 'plan:10539.78' in h,  '❌ Nissei plan não atualizado'
assert 'plan:7482.2' in h,    '❌ DD-Riomed plan não atualizado'
assert 'hist:7646' in h,      '❌ Clamed hist não atualizado'
assert 'meta:22651' in h,     '❌ São João meta não atualizado'
assert 'plan:138172' in h,    '❌ SELLIN_TOTAL plan não atualizado'
print('✅ Verificações finais OK')

print(f'\nTamanho original: {orig_len:,} | Novo: {len(h):,} | Δ: {len(h)-orig_len:+,}')

# ─── Salvar ───
VER.parent.mkdir(parents=True, exist_ok=True)
VER.write_text(h, encoding='utf-8')
print(f'✅ Versão salva: {VER.name}')

SRC.write_text(h, encoding='utf-8')
print(f'✅ Base ativa atualizada: {SRC.name}')
print('DONE.')
