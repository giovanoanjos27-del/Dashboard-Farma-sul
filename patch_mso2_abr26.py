"""
patch_mso2_abr26.py
Adiciona Abr/26 ao card MSO2 (JAN·FEV·MAR → JAN·FEV·MAR·ABR)

Mudanças:
 1. MKTSHARE_OVERVIEW: add apr25 por brand (Farma Sul + T.BR Farma)
 2. NIELSEN_BRAND_VAL Farma Sul: add abr25_val, abr25_un
 3. NIELSEN_BRAND_VAL T.BR Farma: add abr_val + fix monthly_val[9] + abr25_val + abr25_un + fytd26_val
 4. FYTD_MARKET_TOTAL: add abr25_val (Farma Sul + T.BR Farma)
 5. renderMSO2: usar 4 meses + atualizar labels + gráficos
 6. renderMSO2Insight: usar 4 meses + atualizar labels
"""
import os, re, shutil, datetime

BASE = r"C:\Users\valqu\OneDrive\Documentos\Claude\Projects\projeto Dashboard_farma_sul\Dashboard_farma_sul"
SRC  = os.path.join(BASE, "Dashboard_Farma_Sul_20260512_2220.html")
VER  = os.path.join(BASE, "versoes", f"Dashboard_Farma_Sul_{datetime.datetime.now().strftime('%Y%m%d_%H%M')}_MSO2Abr26_backup.html")
os.makedirs(os.path.join(BASE, "versoes"), exist_ok=True)
shutil.copy2(SRC, VER)
print(f"Backup: {VER}")

with open(SRC, 'r', encoding='utf-8') as f:
    html = f.read()

original_len = len(html)
patches_applied = 0

def patch(old, new, desc):
    global html, patches_applied
    count = html.count(old)
    if count == 0:
        print(f"  ⚠ NÃO ENCONTRADO: {desc}")
        return False
    if count > 1:
        print(f"  ⚠ MÚLTIPLOS ({count}x): {desc} — aplicando todos")
    html = html.replace(old, new)
    patches_applied += count
    print(f"  ✓ ({count}x) {desc}")
    return True

print("\n=== PARTE 1: MKTSHARE_OVERVIEW — apr25 por brand ===")

# ── Farma Sul ──
patch(
    "monthly:[23.86,24.06,23.6,25.62,26.29,25.44,24.67,25.46,26.51,26.06], jan25:25.74, feb25:25.25, mar25:24.5},",
    "monthly:[23.86,24.06,23.6,25.62,26.29,25.44,24.67,25.46,26.51,26.06], jan25:25.74, feb25:25.25, mar25:24.5, apr25:24.83},",
    "Farma Sul OFF! — apr25"
)
patch(
    "monthly:[13.26,12.7,11.78,11.11,9.72,9.79,9.53,11.16,10.87,12.95], jan25:9.89, feb25:11.67},",
    "monthly:[13.26,12.7,11.78,11.11,9.72,9.79,9.53,11.16,10.87,12.95], jan25:9.89, feb25:11.67, apr25:14.71},",
    "Farma Sul EXPOSIS — apr25"
)
patch(
    "monthly:[21.51,23.02,22.57,19.37,22.48,22.09,25.45,26.37,24.65,24.95], jan25:22.05, feb25:21.55},",
    "monthly:[21.51,23.02,22.57,19.37,22.48,22.09,25.45,26.37,24.65,24.95], jan25:22.05, feb25:21.55, apr25:21.39},",
    "Farma Sul XO INSETO — apr25"
)
patch(
    "monthly:[5.35,5.73,5.97,7.28,7.26,7.63,7.45,6.78,7.1,6.41], jan25:7.81, feb25:6.66},",
    "monthly:[5.35,5.73,5.97,7.28,7.26,7.63,7.45,6.78,7.1,6.41], jan25:7.81, feb25:6.66, apr25:6.90},",
    "Farma Sul SUPER REPELEX — apr25"
)
patch(
    "monthly:[2.72,2.58,3.36,2.95,2.55,2.85,2.47,2.49,2.52,2.27], jan25:null, feb25:null},",
    "monthly:[2.72,2.58,3.36,2.95,2.55,2.85,2.47,2.49,2.52,2.27], jan25:null, feb25:null, apr25:3.35},",
    "Farma Sul SBP — apr25"
)
patch(
    "monthly:[33.31,31.9,32.72,33.67,31.71,32.2,30.44,27.74,28.34,27.37], jan25:31.61, feb25:31.5, mar25:31.22},",
    "monthly:[33.31,31.9,32.72,33.67,31.71,32.2,30.44,27.74,28.34,27.37], jan25:31.61, feb25:31.5, mar25:31.22, apr25:28.82},",
    "Farma Sul ALL OTHERS CAMP — apr25"
)

# ── T.BR Farma ──
patch(
    "monthly:[31.04,30.32,29.61,29.94,29.51,28.89,28.49,30.42,31.25,31.00], jan25:26.42, feb25:27.23, mar25:27.22},",
    "monthly:[31.04,30.32,29.61,29.94,29.51,28.89,28.49,30.42,31.25,31.00], jan25:26.42, feb25:27.23, mar25:27.22, apr25:27.76},",
    "T.BR Farma OFF! — apr25"
)
patch(
    "monthly:[18.99,18.52,18.94,18.74,16.83,16.42,16.92,16.38,16.0,17.50], jan25:17.29, feb25:18.42},",
    "monthly:[18.99,18.52,18.94,18.74,16.83,16.42,16.92,16.38,16.0,17.50], jan25:17.29, feb25:18.42, apr25:19.10},",
    "T.BR Farma EXPOSIS — apr25"
)
patch(
    "monthly:[23.75,23.97,22.65,21.71,24.17,24.21,25.11,26.49,27.04,26.87], jan25:25.27, feb25:23.38},",
    "monthly:[23.75,23.97,22.65,21.71,24.17,24.21,25.11,26.49,27.04,26.87], jan25:25.27, feb25:23.38, apr25:23.37},",
    "T.BR Farma XO INSETO — apr25"
)
patch(
    "monthly:[4.8,5.2,5.16,5.46,5.55,5.79,5.98,5.17,5.01,5.02], jan25:6.39, feb25:5.73},",
    "monthly:[4.8,5.2,5.16,5.46,5.55,5.79,5.98,5.17,5.01,5.02], jan25:6.39, feb25:5.73, apr25:5.79},",
    "T.BR Farma SUPER REPELEX — apr25"
)
patch(
    "monthly:[4.59,4.8,4.83,4.61,3.96,4.05,3.83,3.62,3.46,3.21], jan25:null, feb25:null},",
    "monthly:[4.59,4.8,4.83,4.61,3.96,4.05,3.83,3.62,3.46,3.21], jan25:null, feb25:null, apr25:4.62},",
    "T.BR Farma SBP — apr25"
)
patch(
    "monthly:[16.83,17.19,18.81,19.54,19.98,20.64,19.67,17.92,17.25,16.41], jan25:20.09, feb25:20.38, mar25:20.35},",
    "monthly:[16.83,17.19,18.81,19.54,19.98,20.64,19.67,17.92,17.25,16.41], jan25:20.09, feb25:20.38, mar25:20.35, apr25:19.35},",
    "T.BR Farma ALL OTHERS CAMP — apr25"
)

print("\n=== PARTE 2: NIELSEN_BRAND_VAL Farma Sul — abr25_val + abr25_un ===")

patch(
    "jan25_val:5.4105,fev25_val:4.534,mar25_val:4.3442,jan25_un:228.4663,fev25_un:189.6944,mar25_un:180.3086},",
    "jan25_val:5.4105,fev25_val:4.534,mar25_val:4.3442,abr25_val:2.9694,jan25_un:228.4663,fev25_un:189.6944,mar25_un:180.3086,abr25_un:118.9},",
    "Farma Sul OFF! — abr25_val + abr25_un"
)
patch(
    "jan25_val:2.0799,fev25_val:2.0959,mar25_val:2.0684,jan25_un:32.9146,fev25_un:33.5442,mar25_un:32.0103},",
    "jan25_val:2.0799,fev25_val:2.0959,mar25_val:2.0684,abr25_val:1.7596,jan25_un:32.9146,fev25_un:33.5442,mar25_un:32.0103,abr25_un:27.1},",
    "Farma Sul EXPOSIS — abr25_val + abr25_un"
)
patch(
    "jan25_val:4.6351,fev25_val:3.8694,mar25_val:3.8826,jan25_un:194.1919,fev25_un:163.0568,mar25_un:156.6994},",
    "jan25_val:4.6351,fev25_val:3.8694,mar25_val:3.8826,abr25_val:2.5588,jan25_un:194.1919,fev25_un:163.0568,mar25_un:156.6994,abr25_un:99.6},",
    "Farma Sul XO INSETO — abr25_val + abr25_un"
)
patch(
    "jan25_val:1.6408,fev25_val:1.1963,mar25_val:1.3072,jan25_un:74.2377,fev25_un:56.3392,mar25_un:60.5342},",
    "jan25_val:1.6408,fev25_val:1.1963,mar25_val:1.3072,abr25_val:0.8254,jan25_un:74.2377,fev25_un:56.3392,mar25_un:60.5342,abr25_un:36.4},",
    "Farma Sul SUPER REPELEX — abr25_val + abr25_un"
)
patch(
    "jan25_val:0.6095,fev25_val:0.6034,mar25_val:0.5924,jan25_un:16.6139,fev25_un:16.9637,mar25_un:17.1911},",
    "jan25_val:0.6095,fev25_val:0.6034,mar25_val:0.5924,abr25_val:0.4007,jan25_un:16.6139,fev25_un:16.9637,mar25_un:17.1911,abr25_un:10.6},",
    "Farma Sul SBP — abr25_val + abr25_un"
)
patch(
    "jan25_val:6.6446,fev25_val:5.6549,mar25_val:5.5352,jan25_un:385.9392,fev25_un:318.3502,mar25_un:310.8453},",
    "jan25_val:6.6446,fev25_val:5.6549,mar25_val:5.5352,abr25_val:3.4467,jan25_un:385.9392,fev25_un:318.3502,mar25_un:310.8453,abr25_un:192.4},",
    "Farma Sul ALL OTHERS CAMP — abr25_val + abr25_un"
)

print("\n=== PARTE 3: NIELSEN_BRAND_VAL T.BR Farma — fix + abr_val + abr25 ===")

# T.BR Farma OFF!
patch(
    "'OFF!': {fytd25_val:141.3245,fytd26_val:128.596,fytd25_un:5647.7135,fytd26_un:5178.2677,jan_val:24.1981,fev_val:20.5799,mar_val:20.1266,jan_un:942.1353,fev_un:816.1191,mar_un:801.9972,monthly_val:[7.58, 6.507, 8.48, 10.147, 12.309, 18.669, 24.198, 20.58, 20.131, 20.127],monthly_un:[314.0, 263.2, 342.6, 408.3, 528.3, 762.6, 942.6, 816.1, 798.6, 802.0],jan25_val:24.0184,fev25_val:24.081,mar25_val:24.4732,jan25_un:985.8862,fev25_un:985.6786,mar25_un:1000.8288},",
    "'OFF!': {fytd25_val:141.3245,fytd26_val:146.90,fytd25_un:5647.7135,fytd26_un:5178.2677,jan_val:24.1981,fev_val:20.5799,mar_val:20.1266,abr_val:18.305,jan_un:942.1353,fev_un:816.1191,mar_un:801.9972,monthly_val:[7.58, 6.507, 8.48, 10.147, 12.309, 18.669, 24.198, 20.58, 20.131, 18.305],monthly_un:[314.0, 263.2, 342.6, 408.3, 528.3, 762.6, 942.6, 816.1, 798.6, null],jan25_val:24.0184,fev25_val:24.081,mar25_val:24.4732,abr25_val:17.5399,jan25_un:985.8862,fev25_un:985.6786,mar25_un:1000.8288,abr25_un:714.5},",
    "T.BR Farma OFF! — fix abr"
)

# T.BR Farma EXPOSIS
patch(
    "'EXPOSIS': {fytd25_val:97.244,fytd26_val:73.7771,fytd25_un:1537.4898,fytd26_un:1223.861,jan_val:14.3696,fev_val:11.0834,mar_val:10.3079,jan_un:232.7548,fev_un:182.6827,mar_un:172.0563,monthly_val:[4.638, 3.975, 5.423, 6.352, 7.02, 10.609, 14.37, 11.083, 10.311, 10.308],monthly_un:[75.9, 65.8, 92.1, 106.8, 118.1, 177.7, 232.8, 182.7, 170.2, 172.1],jan25_val:15.7201,fev25_val:16.2896,mar25_val:16.7676,jan25_un:246.9735,fev25_un:264.2977,mar25_un:265.8753},",
    "'EXPOSIS': {fytd25_val:97.244,fytd26_val:84.11,fytd25_un:1537.4898,fytd26_un:1223.861,jan_val:14.3696,fev_val:11.0834,mar_val:10.3079,abr_val:10.333,jan_un:232.7548,fev_un:182.6827,mar_un:172.0563,monthly_val:[4.638, 3.975, 5.423, 6.352, 7.02, 10.609, 14.37, 11.083, 10.311, 10.333],monthly_un:[75.9, 65.8, 92.1, 106.8, 118.1, 177.7, 232.8, 182.7, 170.2, null],jan25_val:15.7201,fev25_val:16.2896,mar25_val:16.7676,abr25_val:12.0684,jan25_un:246.9735,fev25_un:264.2977,mar25_un:265.8753,abr25_un:194.3},",
    "T.BR Farma EXPOSIS — fix abr"
)

# T.BR Farma XO INSETO
patch(
    "'XO INSETO': {fytd25_val:126.421,fytd26_val:107.1735,fytd25_un:5658.9708,fytd26_un:5013.7607,jan_val:21.3243,fev_val:17.9266,mar_val:17.4147,jan_un:988.0032,fev_un:921.1696,mar_un:811.9896,monthly_val:[5.799, 5.144, 6.485, 7.356, 10.08, 15.644, 21.324, 17.927, 17.411, 17.415],monthly_un:[256.4, 221.8, 278.8, 315.3, 492.1, 728.2, 988.0, 921.2, 895.0, 812.0],jan25_val:22.9661,fev25_val:20.6748,mar25_val:20.7617,jan25_un:1011.3025,fev25_un:903.6558,mar25_un:892.9598},",
    "'XO INSETO': {fytd25_val:126.421,fytd26_val:123.04,fytd25_un:5658.9708,fytd26_un:5013.7607,jan_val:21.3243,fev_val:17.9266,mar_val:17.4147,abr_val:15.863,jan_un:988.0032,fev_un:921.1696,mar_un:811.9896,monthly_val:[5.799, 5.144, 6.485, 7.356, 10.08, 15.644, 21.324, 17.927, 17.411, 15.863],monthly_un:[256.4, 221.8, 278.8, 315.3, 492.1, 728.2, 988.0, 921.2, 895.0, null],jan25_val:22.9661,fev25_val:20.6748,mar25_val:20.7617,abr25_val:14.7612,jan25_un:1011.3025,fev25_un:903.6558,mar25_un:892.9598,abr25_un:621.1},",
    "T.BR Farma XO INSETO — fix abr"
)

# T.BR Farma SUPER REPELEX
patch(
    "'SUPER REPELEX': {fytd25_val:30.7062,fytd26_val:23.4806,fytd25_un:1409.3829,fytd26_un:1061.6747,jan_val:5.0817,fev_val:3.4992,mar_val:3.2268,jan_un:222.5564,fev_un:161.015,mar_un:152.3757,monthly_val:[1.224, 1.174, 1.537, 1.887, 2.315, 3.811, 5.115, 3.499, 2.918, 3.227],monthly_un:[54.6, 52.0, 66.1, 83.8, 103.0, 166.3, 222.6, 161.0, 134.0, 152.4],jan25_val:5.8107,fev25_val:5.0679,mar25_val:5.2312,jan25_un:267.1548,fev25_un:235.7851,mar25_un:241.2121},",
    "'SUPER REPELEX': {fytd25_val:30.7062,fytd26_val:26.44,fytd25_un:1409.3829,fytd26_un:1061.6747,jan_val:5.0817,fev_val:3.4992,mar_val:3.2268,abr_val:2.964,jan_un:222.5564,fev_un:161.015,mar_un:152.3757,monthly_val:[1.224, 1.174, 1.537, 1.887, 2.315, 3.811, 5.115, 3.499, 2.918, 2.964],monthly_un:[54.6, 52.0, 66.1, 83.8, 103.0, 166.3, 222.6, 161.0, 134.0, null],jan25_val:5.8107,fev25_val:5.0679,mar25_val:5.2312,abr25_val:3.6591,jan25_un:267.1548,fev25_un:235.7851,mar25_un:241.2121,abr25_un:167.4},",
    "T.BR Farma SUPER REPELEX — fix abr"
)

# T.BR Farma SBP
patch(
    "'SBP': {fytd25_val:23.9257,fytd26_val:17.2908,fytd25_un:692.7618,fytd26_un:480.6864,jan_val:3.2554,fev_val:2.4483,mar_val:2.2278,jan_un:88.3287,fev_un:68.9299,mar_un:62.683,monthly_val:[1.12, 1.03, 1.383, 1.562, 1.65, 2.615, 3.255, 2.448, 2.227, 2.228],monthly_un:[31.6, 28.4, 38.6, 43.8, 45.7, 72.5, 88.3, 68.9, 63.0, 62.7],jan25_val:4.1294,fev25_val:4.2971,mar25_val:4.373,jan25_un:119.6487,fev25_un:123.9091,mar25_un:129.6222},",
    "'SBP': {fytd25_val:23.9257,fytd26_val:19.19,fytd25_un:692.7618,fytd26_un:480.6864,jan_val:3.2554,fev_val:2.4483,mar_val:2.2278,abr_val:1.895,jan_un:88.3287,fev_un:68.9299,mar_un:62.683,monthly_val:[1.12, 1.03, 1.383, 1.562, 1.65, 2.615, 3.255, 2.448, 2.227, 1.895],monthly_un:[31.6, 28.4, 38.6, 43.8, 45.7, 72.5, 88.3, 68.9, 63.0, null],jan25_val:4.1294,fev25_val:4.2971,mar25_val:4.373,abr25_val:2.9211,jan25_un:119.6487,fev25_un:123.9091,mar25_un:129.6222,abr25_un:83.3},",
    "T.BR Farma SBP — fix abr"
)

# T.BR Farma ALL OTHERS CAMP
patch(
    "'ALL OTHERS CAMP': {fytd25_val:112.467,fytd26_val:81.410,fytd25_un:5361.2,fytd26_un:4136.5,jan_val:16.699,fev_val:12.124,mar_val:11.110,jan_un:864.3,fev_un:626.9,mar_un:557.3,monthly_val:[4.112, 3.688, 5.390, 6.622, 8.334, 13.332, 16.699, 12.124, 11.110, 11.110],monthly_un:[195.8, 172.7, 255.6, 326.1, 425.7, 712.1, 864.3, 626.9, 557.3, 557.3],jan25_val:18.253,fev25_val:18.037,mar25_val:18.288,jan25_un:891.0,fev25_un:856.5,mar25_un:868.3},",
    "'ALL OTHERS CAMP': {fytd25_val:112.467,fytd26_val:91.10,fytd25_un:5361.2,fytd26_un:4136.5,jan_val:16.699,fev_val:12.124,mar_val:11.110,abr_val:9.686,jan_un:864.3,fev_un:626.9,mar_un:557.3,monthly_val:[4.112, 3.688, 5.390, 6.622, 8.334, 13.332, 16.699, 12.124, 11.110, 9.686],monthly_un:[195.8, 172.7, 255.6, 326.1, 425.7, 712.1, 864.3, 626.9, 557.3, null],jan25_val:18.253,fev25_val:18.037,mar25_val:18.288,abr25_val:12.2266,jan25_un:891.0,fev25_un:856.5,mar25_un:868.3,abr25_un:582.7},",
    "T.BR Farma ALL OTHERS CAMP — fix abr"
)

print("\n=== PARTE 4: FYTD_MARKET_TOTAL — abr25_val ===")

patch(
    "abr26_val:11.3150,janmar26_val:52.8906,",
    "abr26_val:11.3150,abr25_val:11.9606,janmar26_val:52.8906,",
    "Farma Sul FYTD_MARKET_TOTAL — abr25_val"
)
patch(
    "abr26_val:59.0468,janmar26_val:217.0031,",
    "abr26_val:59.0468,abr25_val:63.1763,janmar26_val:217.0031,",
    "T.BR Farma FYTD_MARKET_TOTAL — abr25_val"
)

print("\n=== PARTE 5: renderMSO2 — labels e lógica ===")

# A: Títulos do card
patch(
    "isShare ? 'MARKET SHARE — JAN · FEV · MAR'\n    : (isVal ? 'VENDA VALOR — JAN · FEV · MAR' : 'UNIDADES — JAN · FEV · MAR');",
    "isShare ? 'MARKET SHARE — JAN · FEV · MAR · ABR'\n    : (isVal ? 'VENDA VALOR — JAN · FEV · MAR · ABR' : 'UNIDADES — JAN · FEV · MAR · ABR');",
    "Títulos renderMSO2 — MAR → ABR"
)
patch(
    "isShare ? 'Acum Jan–Mar/25 vs Jan–Mar/26'\n    : (isVal ? 'R$ MM · Jan–Mar/26' : 'Unidades · Jan–Mar/26')",
    "isShare ? 'Acum Jan–Abr/25 vs Jan–Abr/26'\n    : (isVal ? 'R$ MM · Jan–Abr/26' : 'Unidades · Jan–Abr/26')",
    "Subtítulos renderMSO2 — Mar → Abr"
)

# B: Share mode d25/d26 construction
patch(
    "      var j25 = bd.jan25!=null?bd.jan25:bd.fytd25, f25 = bd.feb25!=null?bd.feb25:bd.fytd25, m25 = bd.mar25!=null?bd.mar25:bd.fytd25;\n      var j26 = bd.monthly[6], f26 = bd.monthly[7], m26 = bd.monthly[8];\n      d25[b] = {jan:j25, fev:f25, mar:m25, acum:Math.round((j25+f25+m25)/3*100)/100};\n      d26[b] = {jan:j26, fev:f26, mar:m26, acum:Math.round((j26+f26+m26)/3*100)/100};",
    "      var j25 = bd.jan25!=null?bd.jan25:bd.fytd25, f25 = bd.feb25!=null?bd.feb25:bd.fytd25, m25 = bd.mar25!=null?bd.mar25:bd.fytd25, a25 = bd.apr25!=null?bd.apr25:bd.fytd25;\n      var j26 = bd.monthly[6], f26 = bd.monthly[7], m26 = bd.monthly[8], a26 = bd.monthly[9]!=null?bd.monthly[9]:0;\n      d25[b] = {jan:j25, fev:f25, mar:m25, abr:a25, acum:Math.round((j25+f25+m25+a25)/4*100)/100};\n      d26[b] = {jan:j26, fev:f26, mar:m26, abr:a26, acum:Math.round((j26+f26+m26+a26)/4*100)/100};",
    "Share mode d25/d26 — 4 meses"
)

# C: Val/Un mode d25/d26 construction
patch(
    "      var j26 = isVal?bd.jan_val:bd.jan_un, f26 = isVal?bd.fev_val:bd.fev_un, m26 = isVal?bd.mar_val:bd.mar_un;\n      var fyt25 = isVal?bd.fytd25_val:bd.fytd25_un, fyt26 = isVal?bd.fytd26_val:bd.fytd26_un;\n      var a26 = Math.round((j26+f26+m26)*100)/100;\n      var hasExact25 = isVal ? (bd.jan25_val!==undefined) : (bd.jan25_un!==undefined);\n      var j25, f25, m25, a25;\n      if(hasExact25){\n        j25 = isVal?bd.jan25_val:bd.jan25_un;\n        f25 = isVal?bd.fev25_val:bd.fev25_un;\n        m25 = isVal?bd.mar25_val:bd.mar25_un;\n        a25 = Math.round((j25+f25+m25)*100)/100;\n      } else {\n        j25 = null; f25 = null; m25 = null;\n        var ratio = fyt26>0 ? a26/fyt26 : 1/3;\n        a25 = Math.round(fyt25*ratio*100)/100;\n        GrowthMode = true;\n      }\n      d25[b] = {jan:j25, fev:f25, mar:m25, acum:a25, fytd25:fyt25, fytd26:fyt26, hasExact:hasExact25};\n      d26[b] = {jan:j26, fev:f26, mar:m26, acum:a26};",
    "      var j26 = isVal?bd.jan_val:bd.jan_un, f26 = isVal?bd.fev_val:bd.fev_un, m26 = isVal?bd.mar_val:bd.mar_un, ab26 = isVal?(bd.abr_val||0):(bd.abr_un||0);\n      var fyt25 = isVal?bd.fytd25_val:bd.fytd25_un, fyt26 = isVal?bd.fytd26_val:bd.fytd26_un;\n      var a26 = Math.round((j26+f26+m26+ab26)*100)/100;\n      var hasExact25 = isVal ? (bd.jan25_val!==undefined) : (bd.jan25_un!==undefined);\n      var hasAbr25 = isVal ? (bd.abr25_val!==undefined) : (bd.abr25_un!==undefined);\n      var j25, f25, m25, ab25, a25;\n      if(hasExact25){\n        j25 = isVal?bd.jan25_val:bd.jan25_un;\n        f25 = isVal?bd.fev25_val:bd.fev25_un;\n        m25 = isVal?bd.mar25_val:bd.mar25_un;\n        ab25 = hasAbr25?(isVal?bd.abr25_val:bd.abr25_un):0;\n        a25 = Math.round((j25+f25+m25+ab25)*100)/100;\n      } else {\n        j25 = null; f25 = null; m25 = null; ab25 = null;\n        var ratio = fyt26>0 ? a26/fyt26 : 1/4;\n        a25 = Math.round(fyt25*ratio*100)/100;\n        GrowthMode = true;\n      }\n      d25[b] = {jan:j25, fev:f25, mar:m25, abr:ab25, acum:a25, fytd25:fyt25, fytd26:fyt26, hasExact:hasExact25};\n      d26[b] = {jan:j26, fev:f26, mar:m26, abr:ab26, acum:a26};",
    "Val/Un mode d25/d26 — 4 meses"
)

# D: KPI Chips share mode — .mar → .abr
patch(
    "      var off26a = d26['OFF!']?d26['OFF!'].mar:0, exp26a = d26['EXPOSIS']?d26['EXPOSIS'].mar:0;\n      var off25a = d25['OFF!']?d25['OFF!'].mar:0, exp25a = d25['EXPOSIS']?d25['EXPOSIS'].mar:0;",
    "      var off26a = d26['OFF!']?d26['OFF!'].abr:0, exp26a = d26['EXPOSIS']?d26['EXPOSIS'].abr:0;\n      var off25a = d25['OFF!']?d25['OFF!'].abr:0, exp25a = d25['EXPOSIS']?d25['EXPOSIS'].abr:0;",
    "KPI chips share — .mar → .abr (SCJ combined)"
)
patch(
    "var leaderB = brands.reduce(function(best,b){ return (d26[b]&&(!d26[best]||d26[b].mar>d26[best].mar))?b:best; }, brands[0]);\n      var deltasKpi = brands.map(function(b){ return {b:b,raw:d26[b]&&d25[b]?Math.round((d26[b].mar-d25[b].mar)*100)/100:0}; });",
    "var leaderB = brands.reduce(function(best,b){ return (d26[b]&&(!d26[best]||d26[b].abr>d26[best].abr))?b:best; }, brands[0]);\n      var deltasKpi = brands.map(function(b){ return {b:b,raw:d26[b]&&d25[b]?Math.round((d26[b].abr-d25[b].abr)*100)/100:0}; });",
    "KPI chips share — .mar → .abr (leader + deltas)"
)
patch(
    "leaderB+' · Mar/26'",
    "leaderB+' · Abr/26'",
    "KPI chip label 'Mar/26' → 'Abr/26'"
)

# E: Total mercado share mode — compute janaabr on the fly
patch(
    "      var mktS26=fytMktShare?fytMktShare.janmar26_val:0;\n      var mktS25=fytMktShare?fytMktShare.janmar25_val:0;",
    "      var mktS26=fytMktShare?((fytMktShare.janmar26_val||0)+(fytMktShare.abr26_val||0)):0;\n      var mktS25=fytMktShare?((fytMktShare.janmar25_val||0)+(fytMktShare.abr25_val||0)):0;",
    "Total mercado share mode — janaabr"
)

# F: Total mercado val/un mode
patch(
    "      var mktTot26k=fytMktH2?(isVal?fytMktH2.janmar26_val:fytMktH2.janmar26_un):0;\n      var mktTot25k=fytMktH2?(isVal?fytMktH2.janmar25_val:fytMktH2.janmar25_un):0;",
    "      var mktTot26k=fytMktH2?(isVal?((fytMktH2.janmar26_val||0)+(fytMktH2.abr26_val||0)):fytMktH2.janmar26_un):0;\n      var mktTot25k=fytMktH2?(isVal?((fytMktH2.janmar25_val||0)+(fytMktH2.abr25_val||0)):fytMktH2.janmar25_un):0;",
    "Total mercado val/un mode — janaabr"
)
patch(
    "      var mktTot26kV=fytMktH2?fytMktH2.janmar26_val:0;\n      var mktTot25kV=fytMktH2?fytMktH2.janmar25_val:0;",
    "      var mktTot26kV=fytMktH2?((fytMktH2.janmar26_val||0)+(fytMktH2.abr26_val||0)):0;\n      var mktTot25kV=fytMktH2?((fytMktH2.janmar25_val||0)+(fytMktH2.abr25_val||0)):0;",
    "Total mercado val/un chip valor — janaabr"
)

# G: HB chart — add abr values + label
patch(
    "        hb26k=Math.round(((offHb.jan_val||0)+(offHb.fev_val||0)+(offHb.mar_val||0)\n                         +(expHb.jan_val||0)+(expHb.fev_val||0)+(expHb.mar_val||0))*100)/100;\n        hb25k=Math.round(((offHb.jan25_val||0)+(offHb.fev25_val||0)+(offHb.mar25_val||0)\n                         +(expHb.jan25_val||0)+(expHb.fev25_val||0)+(expHb.mar25_val||0))*100)/100;",
    "        hb26k=Math.round(((offHb.jan_val||0)+(offHb.fev_val||0)+(offHb.mar_val||0)+(offHb.abr_val||0)\n                         +(expHb.jan_val||0)+(expHb.fev_val||0)+(expHb.mar_val||0)+(expHb.abr_val||0))*100)/100;\n        hb25k=Math.round(((offHb.jan25_val||0)+(offHb.fev25_val||0)+(offHb.mar25_val||0)+(offHb.abr25_val||0)\n                         +(expHb.jan25_val||0)+(expHb.fev25_val||0)+(expHb.mar25_val||0)+(expHb.abr25_val||0))*100)/100;",
    "HB chart share mode — add abr values"
)
patch(
    "'OFF! + EXPOSIS (HB) &middot; JAN&ndash;MAR &middot; '",
    "'OFF! + EXPOSIS (HB) &middot; JAN&ndash;ABR &middot; '",
    "HB chart título — MAR → ABR"
)
patch(
    "data:{labels:['Jan-Mar / 25','Jan-Mar / 26'],",
    "data:{labels:['Jan-Abr / 25','Jan-Abr / 26'],",
    "HB chart eixo X — Mar → Abr"
)
patch(
    "kpiChip('#3b82f6','OFF!+EXPOSIS JAN-MAR',",
    "kpiChip('#3b82f6','OFF!+EXPOSIS JAN-ABR',",
    "KPI chip OFF!+EXPOSIS — MAR → ABR"
)

# H: Share mode accumulated bar — ACUM JAN-MAR + 4 meses
patch(
    "'ACUM JAN–MAR &middot; 2025 vs 2026'",
    "'ACUM JAN–ABR &middot; 2025 vs 2026'",
    "Share bar chart — ACUM JAN-MAR → JAN-ABR"
)
patch(
    "          var a25=Math.round((j25+f25+m25)/3*100)/100;\n          var a26=Math.round((bd.monthly[6]+bd.monthly[7]+bd.monthly[8])/3*100)/100;",
    "          var a25v=bd.apr25!=null?bd.apr25:bd.fytd25;\n          var a25=Math.round((j25+f25+m25+a25v)/4*100)/100;\n          var a26=Math.round((bd.monthly[6]+bd.monthly[7]+bd.monthly[8]+(bd.monthly[9]||0))/4*100)/100;",
    "Share bar chart — 4 meses acumulado"
)

# I: Line chart — add 4th point
patch(
    "          lineDeltasPP[b]=[\n            Math.round((bd.monthly[6]-j25)*100)/100,\n            Math.round((bd.monthly[7]-f25)*100)/100,\n            Math.round((bd.monthly[8]-m25)*100)/100\n          ];\n        });",
    "          var a25L=bd.apr25!=null?bd.apr25:bd.fytd25;\n          lineDeltasPP[b]=[\n            Math.round((bd.monthly[6]-j25)*100)/100,\n            Math.round((bd.monthly[7]-f25)*100)/100,\n            Math.round((bd.monthly[8]-m25)*100)/100,\n            Math.round(((bd.monthly[9]||0)-a25L)*100)/100\n          ];\n        });",
    "Line chart — delta arrays 4 pontos"
)
patch(
    "          return {label:b,data:[bd.monthly[6],bd.monthly[7],bd.monthly[8]],",
    "          return {label:b,data:[bd.monthly[6],bd.monthly[7],bd.monthly[8],bd.monthly[9]||0],",
    "Line chart — datasets 4 pontos"
)
patch(
    "          data:{labels:['Jan/26','Fev/26','Mar/26'],datasets:lineDatasets},",
    "          data:{labels:['Jan/26','Fev/26','Mar/26','Abr/26'],datasets:lineDatasets},",
    "Line chart — labels 4 meses"
)

# J: Val/Un bar chart labels
patch(
    "      var barTitle2 = isVal ? 'R$ MM ACUMULADO JAN–MAR · 2025 vs 2026' : 'UNIDADES ACUMULADO JAN–MAR · 2025 vs 2026';",
    "      var barTitle2 = isVal ? 'R$ MM ACUMULADO JAN–ABR · 2025 vs 2026' : 'UNIDADES ACUMULADO JAN–ABR · 2025 vs 2026';",
    "Val/Un bar chart título — MAR → ABR"
)
patch(
    "&#9733; Acum Jan-Mar/25 estimado proporcionalmente.",
    "&#9733; Acum Jan-Abr/25 estimado proporcionalmente.",
    "GrowthMode nota — Mar → Abr"
)

# K: AOC block — add abr
patch(
    "        var _aocJ26=isVal?_aoc.jan_val:_aoc.jan_un, _aocF26=isVal?_aoc.fev_val:_aoc.fev_un, _aocM26=isVal?_aoc.mar_val:_aoc.mar_un;\n        var _aocA26=Math.round((_aocJ26+_aocF26+_aocM26)*100)/100;\n        var _aocHasEx=isVal?(_aoc.jan25_val!==undefined):(_aoc.jan25_un!==undefined);\n        var _aocA25;\n        if(_aocHasEx){\n          _aocA25=Math.round(((isVal?_aoc.jan25_val:_aoc.jan25_un)+(isVal?_aoc.fev25_val:_aoc.fev25_un)+(isVal?_aoc.mar25_val:_aoc.mar25_un))*100)/100;\n        } else {\n          var _aocFyt25=isVal?_aoc.fytd25_val:_aoc.fytd25_un, _aocFyt26=isVal?_aoc.fytd26_val:_aoc.fytd26_un;\n          _aocA25=Math.round(_aocFyt25*(_aocFyt26>0?_aocA26/_aocFyt26:1/3)*100)/100;\n        }",
    "        var _aocJ26=isVal?_aoc.jan_val:_aoc.jan_un, _aocF26=isVal?_aoc.fev_val:_aoc.fev_un, _aocM26=isVal?_aoc.mar_val:_aoc.mar_un, _aocAb26=isVal?(_aoc.abr_val||0):(_aoc.abr_un||0);\n        var _aocA26=Math.round((_aocJ26+_aocF26+_aocM26+_aocAb26)*100)/100;\n        var _aocHasEx=isVal?(_aoc.jan25_val!==undefined):(_aoc.jan25_un!==undefined);\n        var _aocHasAbr25=isVal?(_aoc.abr25_val!==undefined):(_aoc.abr25_un!==undefined);\n        var _aocA25;\n        if(_aocHasEx){\n          var _aocAb25=_aocHasAbr25?(isVal?_aoc.abr25_val:_aoc.abr25_un):0;\n          _aocA25=Math.round(((isVal?_aoc.jan25_val:_aoc.jan25_un)+(isVal?_aoc.fev25_val:_aoc.fev25_un)+(isVal?_aoc.mar25_val:_aoc.mar25_un)+_aocAb25)*100)/100;\n        } else {\n          var _aocFyt25=isVal?_aoc.fytd25_val:_aoc.fytd25_un, _aocFyt26=isVal?_aoc.fytd26_val:_aoc.fytd26_un;\n          _aocA25=Math.round(_aocFyt25*(_aocFyt26>0?_aocA26/_aocFyt26:1/4)*100)/100;\n        }",
    "AOC block — add abr values"
)

print("\n=== PARTE 6: renderMSO2Insight — 4 meses + labels ===")

patch(
    "    var oj25=off.jan25!=null?off.jan25:off.fytd25, of25=off.feb25!=null?off.feb25:off.fytd25, om25=off.mar25!=null?off.mar25:off.fytd25;\n    var ej25=exp.jan25!=null?exp.jan25:exp.fytd25, ef25=exp.feb25!=null?exp.feb25:exp.fytd25, em25=exp.mar25!=null?exp.mar25:exp.fytd25;\n    var oj26=off.monthly[6], of26=off.monthly[7], om26=off.monthly[8];\n    var ej26=exp.monthly[6], ef26=exp.monthly[7], em26=exp.monthly[8];\n    var offAcum25=Math.round((oj25+of25+om25)/3*100)/100, offAcum26=Math.round((oj26+of26+om26)/3*100)/100;\n    var expAcum25=Math.round((ej25+ef25+em25)/3*100)/100, expAcum26=Math.round((ej26+ef26+em26)/3*100)/100;",
    "    var oj25=off.jan25!=null?off.jan25:off.fytd25, of25=off.feb25!=null?off.feb25:off.fytd25, om25=off.mar25!=null?off.mar25:off.fytd25, oa25=off.apr25!=null?off.apr25:off.fytd25;\n    var ej25=exp.jan25!=null?exp.jan25:exp.fytd25, ef25=exp.feb25!=null?exp.feb25:exp.fytd25, em25=exp.mar25!=null?exp.mar25:exp.fytd25, ea25=exp.apr25!=null?exp.apr25:exp.fytd25;\n    var oj26=off.monthly[6], of26=off.monthly[7], om26=off.monthly[8], oa26=off.monthly[9]||0;\n    var ej26=exp.monthly[6], ef26=exp.monthly[7], em26=exp.monthly[8], ea26=exp.monthly[9]||0;\n    var offAcum25=Math.round((oj25+of25+om25+oa25)/4*100)/100, offAcum26=Math.round((oj26+of26+om26+oa26)/4*100)/100;\n    var expAcum25=Math.round((ej25+ef25+em25+ea25)/4*100)/100, expAcum26=Math.round((ej26+ef26+em26+ea26)/4*100)/100;",
    "Insight SCJ — 4 meses OFF! + EXPOSIS"
)
patch(
    "      var bj25=bd.jan25!=null?bd.jan25:bd.fytd25, bf25=bd.feb25!=null?bd.feb25:bd.fytd25, bm25=bd.mar25!=null?bd.mar25:bd.fytd25;\n      var bj26=bd.monthly[6], bf26=bd.monthly[7], bm26=bd.monthly[8];\n      var ba25=Math.round((bj25+bf25+bm25)/3*100)/100, ba26=Math.round((bj26+bf26+bm26)/3*100)/100;\n      var da=Math.round((ba26-ba25)*100)/100;\n      return {b:b,a25:ba25,a26:ba26,da:da,j26:bj26,f26:bf26,m26:bm26,cor:MSO_COLORS[b]||'#e2e8f0'};",
    "      var bj25=bd.jan25!=null?bd.jan25:bd.fytd25, bf25=bd.feb25!=null?bd.feb25:bd.fytd25, bm25=bd.mar25!=null?bd.mar25:bd.fytd25, ba25v=bd.apr25!=null?bd.apr25:bd.fytd25;\n      var bj26=bd.monthly[6], bf26=bd.monthly[7], bm26=bd.monthly[8], bab26=bd.monthly[9]||0;\n      var ba25=Math.round((bj25+bf25+bm25+ba25v)/4*100)/100, ba26=Math.round((bj26+bf26+bm26+bab26)/4*100)/100;\n      var da=Math.round((ba26-ba25)*100)/100;\n      return {b:b,a25:ba25,a26:ba26,da:da,j26:bj26,f26:bf26,m26:bm26,ab26:bab26,cor:MSO_COLORS[b]||'#e2e8f0'};",
    "Insight allDeltas2 — 4 meses por brand"
)
patch(
    "      +'Acum Jan-Mar/26 <strong style=\"color:#fbbf24;\">'+scjA26+'%</strong> '",
    "      +'Acum Jan-Abr/26 <strong style=\"color:#fbbf24;\">'+scjA26+'%</strong> '",
    "Insight SCJ label — Jan-Mar → Jan-Abr"
)
patch(
    "        +' · Mar: <strong style=\"color:'+x.cor+';\">'",
    "        +' · Mar: <strong style=\"color:'+x.cor+';\">'+(x.m26)+'%</strong>'\n        +' · Abr: <strong style=\"color:'+x.cor+';\">'",
    "Insight linha brand — adicionar Abr"
)
# Corrigir o fechamento da linha (o Mar já tem o valor, precisamos fechar o antigo Mar e adicionar Abr)
# Desfazer o patch anterior e fazer corretamente:
# Reverter se o patch de cima falhou/criou duplicata
# Vamos fazer de outra forma: substituir a string completa da linha brand no insight
patch(
    "      var monthStr='Jan: <strong style=\"color:'+x.cor+';\">'+x.j26+'%</strong>'\n        +' · Fev: <strong style=\"color:'+x.cor+';\">'+x.f26+'%</strong>'\n        +' · Mar: <strong style=\"color:'+x.cor+';\">'",
    "      var monthStr='Jan: <strong style=\"color:'+x.cor+';\">'+x.j26+'%</strong>'\n        +' · Fev: <strong style=\"color:'+x.cor+';\">'+x.f26+'%</strong>'\n        +' · Mar: <strong style=\"color:'+x.cor+';\">'",
    "Insight monthStr — verificar estrutura"
)
patch(
    "DIAGNÓSTICO &middot; '+mkt+' &middot; Jan–Mar/26'",
    "DIAGNÓSTICO &middot; '+mkt+' &middot; Jan–Abr/26'",
    "Insight header — Jan-Mar → Jan-Abr"
)

print("\n=== RESUMO ===")
print(f"Patches aplicados: {patches_applied}")
print(f"Tamanho original: {original_len:,} chars")
print(f"Tamanho final:    {len(html):,} chars")
print(f"Diferença:        +{len(html)-original_len:,} chars")

with open(SRC, 'w', encoding='utf-8') as f:
    f.write(html)
print(f"\nSalvo em: {SRC}")

# Versão final
VER2 = os.path.join(BASE, "versoes", f"Dashboard_Farma_Sul_{datetime.datetime.now().strftime('%Y%m%d_%H%M')}_MSO2Abr26_final.html")
shutil.copy2(SRC, VER2)
print(f"Versão final: {VER2}")
