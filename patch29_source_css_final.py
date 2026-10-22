"""
PATCH 29 — Migração Visual Total: edita CSS fonte (linhas 7-520)
Substitui TODOS os valores escuros diretamente na fonte original.
Sem depender de !important cascades.
"""
import datetime, re

SRC = r'Dashboard_farma_sul\Dashboard_Farma_Sul_20260512_2220.html'
html = open(SRC, encoding='utf-8').read()
original_len = len(html)
patches = 0

def rpl(old, new, desc, count=0):
    global html, patches
    n = html.count(old)
    if n == 0:
        print('[MISS] ' + desc)
        return
    html = html.replace(old, new) if count == 0 else html.replace(old, new, count)
    patches += 1
    print('[OK x{}] {}'.format(n, desc))

# ==============================================================================
# 1. BODY / base
# ==============================================================================
rpl('background:#0D1117;color:#e2e8f0;min-height:100vh;font-size:14px;',
    'background:#F4F7FB;color:#334155;min-height:100vh;font-size:14px;',
    'body bg + color')

# ==============================================================================
# 2. HEADER
# ==============================================================================
rpl('border-bottom:0.5px solid rgba(245,225,164,0.2);position:sticky;top:0;z-index:100;background:#0D1117;}',
    'border-bottom:1px solid #DCE3EC;position:sticky;top:0;z-index:100;background:#FFFFFF;}',
    'header bg + border')
rpl('.header h1{font-size:20px;font-weight:700;color:#F5E1A4;letter-spacing:-0.5px;}',
    '.header h1{font-size:20px;font-weight:700;color:#1E293B;letter-spacing:-0.5px;}',
    'header h1 color')
rpl('.header-sub{font-size:11px;color:#94A3B8;margin-top:2px;}',
    '.header-sub{font-size:11px;color:#64748B;margin-top:2px;}',
    'header-sub color')
# header gradient override at ~line 388
rpl('background: linear-gradient(135deg, #101828 0%, #1F2937 50%, #101828 100%) !important;\n  border-bottom: 1px solid rgba(103,232,249,0.08) !important;',
    'background: #FFFFFF !important;\n  border-bottom: 1px solid #DCE3EC !important;',
    'header gradient override')

# ==============================================================================
# 3. CTABS
# ==============================================================================
rpl('.ctabs{background:#0D1117;border-bottom:0.5px solid rgba(245,225,164,0.40);',
    '.ctabs{background:#FFFFFF;border-bottom:1px solid #DCE3EC;',
    'ctabs bg + border')
rpl('.ctab:hover{color:#D1D5DB;}',
    '.ctab:hover{color:#475569;}',
    'ctab hover color')
rpl('.ctab.active{color:#F5E1A4;border-bottom-color:#F5E1A4;}',
    '.ctab.active{color:#1D4ED8;border-bottom-color:#1D4ED8;}',
    'ctab.active color')
rpl('color:#94A3B8;cursor:pointer;white-space:nowrap;transition:all 0.15s;display:flex;align-items:center;gap:5px;letter-spacing:0.01em;}',
    'color:#64748B;cursor:pointer;white-space:nowrap;transition:all 0.15s;display:flex;align-items:center;gap:5px;letter-spacing:0.01em;}',
    'ctab default color')
# ctab.active box-shadow override
rpl('box-shadow: 0 2px 16px rgba(103,232,249,0.2) !important;',
    'box-shadow: none !important;',
    'ctab.active shadow')
rpl('background: rgba(255,255,255,0.09) !important;',
    'background: rgba(71,85,105,0.06) !important;',
    'ctab:hover bg')

# ==============================================================================
# 4. FILTERS / fsel
# ==============================================================================
rpl('.filters{padding:8px 24px;border-bottom:0.5px solid rgba(245,225,164,0.12);',
    '.filters{padding:8px 24px;border-bottom:1px solid #DCE3EC;',
    'filters border')
rpl('.filter-label{font-size:10px;color:#94A3B8;font-weight:700;letter-spacing:0.08em;}',
    '.filter-label{font-size:10px;color:#64748B;font-weight:700;letter-spacing:0.08em;}',
    'filter-label color')
rpl('border:0.5px solid rgba(255,255,255,0.13);background:rgba(255,255,255,0.04);color:#D1D5DB;cursor:pointer;appearance:none;-webkit-appearance:none;background-image:url("data:image/svg+xml,%3Csvg xmlns=\'http://www.w3.org/2000/svg\' width=\'10\' height=\'6\'%3E%3Cpath d=\'M0 0l5 6 5-6z\' fill=\'%235a6478\'/%3E%3C/svg%3E");background-repeat:no-repeat;background-position:right 8px center;}',
    'border:1px solid #CBD5E1;background:#FFFFFF;color:#334155;cursor:pointer;appearance:none;-webkit-appearance:none;background-image:url("data:image/svg+xml,%3Csvg xmlns=\'http://www.w3.org/2000/svg\' width=\'10\' height=\'6\'%3E%3Cpath d=\'M0 0l5 6 5-6z\' fill=\'%2364748B\'/%3E%3C/svg%3E");background-repeat:no-repeat;background-position:right 8px center;}',
    'fsel base style')
rpl('.fsel:focus{outline:none;border-color:rgba(245,225,164,0.4);}',
    '.fsel:focus{outline:none;border-color:#3B82F6;}',
    'fsel:focus border')

# ==============================================================================
# 5. SELLOUT CLIENT SELECTOR
# ==============================================================================
rpl('border:1px solid rgba(245,225,164,0.45);\n  background:#0D1117;\n  color:#FFFFFF;',
    'border:1px solid #CBD5E1;\n  background:#FFFFFF;\n  color:#1E293B;',
    'sellout-client-selector base')
rpl('background-image:url("data:image/svg+xml,%3Csvg xmlns=\'http://www.w3.org/2000/svg\' width=\'10\' height=\'6\'%3E%3Cpath d=\'M0 0l5 6 5-6z\' fill=\'%23F5E1A4\'/%3E%3C/svg%3E");',
    'background-image:url("data:image/svg+xml,%3Csvg xmlns=\'http://www.w3.org/2000/svg\' width=\'10\' height=\'6\'%3E%3Cpath d=\'M0 0l5 6 5-6z\' fill=\'%2364748B\'/%3E%3C/svg%3E");',
    'sellout-client-selector arrow')
rpl('#sellout-client-selector:hover{\n  border-color:rgba(245,225,164,0.75);\n  box-shadow:0 0 0 2px rgba(245,225,164,0.12);\n}',
    '#sellout-client-selector:hover{\n  border-color:#3B82F6;\n  box-shadow:0 0 0 2px rgba(59,130,246,0.08);\n}',
    'sellout-client-selector hover')
rpl('#sellout-client-selector:focus{\n  outline:none;\n  border-color:#F5E1A4;\n  box-shadow:0 0 0 3px rgba(245,225,164,0.18);\n}',
    '#sellout-client-selector:focus{\n  outline:none;\n  border-color:#3B82F6;\n  box-shadow:0 0 0 3px rgba(59,130,246,0.12);\n}',
    'sellout-client-selector focus')
rpl('#sellout-client-selector option{\n  background:#0D1117;\n  color:#FFFFFF;\n}',
    '#sellout-client-selector option{\n  background:#FFFFFF;\n  color:#1E293B;\n}',
    'sellout-client-selector option')
rpl('#panel-sellout .filter-label{\n  color:#F5E1A4;',
    '#panel-sellout .filter-label{\n  color:#64748B;',
    'panel-sellout filter-label')

# ==============================================================================
# 6. KPI-GRID (gap background + border)
# ==============================================================================
rpl('background:rgba(245,225,164,0.12);border-radius:12px;overflow:hidden;margin-bottom:18px;border:1.5px solid rgba(234,179,8,0.5);}',
    'background:transparent;border-radius:12px;overflow:hidden;margin-bottom:18px;border:1px solid #DCE3EC;}',
    'kpi-grid bg + border')

# ==============================================================================
# 7. KPI-CELL
# ==============================================================================
rpl('.kpi-cell{background:#161B22;padding:16px 18px;position:relative;overflow:hidden;}',
    '.kpi-cell{background:#FFFFFF;padding:16px 18px;position:relative;overflow:hidden;}',
    'kpi-cell base bg')
rpl('.kpi-cell::before{content:\'\';position:absolute;top:0;left:0;right:0;height:2px;background:var(--accent,#3b82f6);opacity:0.6;}',
    '.kpi-cell::before{content:\'\';position:absolute;top:0;left:0;right:0;height:2px;background:var(--accent,#3b82f6);opacity:0.8;}',
    'kpi-cell::before opacity')
# kpi-cell gradient override with !important
rpl('background: linear-gradient(135deg, #1F2937 0%, #101828 100%) !important;\n  border-top:2px solid rgba(245,225,164,0.5) !important;',
    'background: #FFFFFF !important;\n  border-top:2px solid var(--accent,#3b82f6) !important;',
    'kpi-cell gradient !important override')
rpl('.kpi-cell:hover {\n  transform: translateY(-2px) scale(1.01);\n  box-shadow: 0 4px 24px rgba(0,0,0,0.5), 0 0 20px rgba(245,225,164,0.15);\n}',
    '.kpi-cell:hover {\n  transform: translateY(-2px) scale(1.01);\n  box-shadow: 0 4px 16px rgba(15,23,42,0.08);\n}',
    'kpi-cell hover shadow')
rpl('background: radial-gradient(ellipse at top left, rgba(245,225,164,0.06), transparent 60%);',
    'background: radial-gradient(ellipse at top left, rgba(59,130,246,0.04), transparent 60%);',
    'kpi-cell::after gradient')
rpl('.kpi-cell::before {\n  opacity: 1 !important;\n  background: linear-gradient(90deg, var(--accent,#F5E1A4), rgba(245,225,164,0.4)) !important;\n  height: 3px !important;\n}',
    '.kpi-cell::before {\n  opacity: 1 !important;\n  background: linear-gradient(90deg, var(--accent,#3b82f6), rgba(59,130,246,0.5)) !important;\n  height: 3px !important;\n}',
    'kpi-cell::before gradient')
rpl('.kpi-cell.updated-2026{border-top:3px solid #34d399 !important;}\n.kpi-cell.updated-2026::before{background:#34d399 !important;opacity:0.8 !important;}',
    '.kpi-cell.updated-2026{border-top:3px solid #16a34a !important;}\n.kpi-cell.updated-2026::before{background:#16a34a !important;opacity:0.8 !important;}',
    'kpi-cell.updated-2026')

# ==============================================================================
# 8. KPI text
# ==============================================================================
rpl('.kpi-tag{font-size:12px;font-weight:700;letter-spacing:0.5px;color:#B0BAC9;text-transform:uppercase;margin-bottom:8px;}',
    '.kpi-tag{font-size:12px;font-weight:700;letter-spacing:0.5px;color:#64748B;text-transform:uppercase;margin-bottom:8px;}',
    'kpi-tag color')
rpl('.kpi-val{font-size:1.2rem;font-weight:700;letter-spacing:-0.5px;color:var(--accent,#F5E1A4);line-height:1;}',
    '.kpi-val{font-size:1.2rem;font-weight:700;letter-spacing:-0.5px;color:var(--accent,#1D4ED8);line-height:1;}',
    'kpi-val accent default')
rpl('.kpi-sub{font-size:11px;color:#9CA3AF;margin-top:5px;}',
    '.kpi-sub{font-size:11px;color:#64748B;margin-top:5px;}',
    'kpi-sub color')
rpl('.kpi-sub{font-size:10px !important;color:#4a5568 !important;letter-spacing:0.02em;}',
    '.kpi-sub{font-size:10px !important;color:#64748B !important;letter-spacing:0.02em;}',
    'kpi-sub !important override')
rpl('text-shadow: 0 0 20px rgba(245,225,164,0.45);',
    'text-shadow: none;',
    'kpi-val text-shadow')
rpl('color: #6b7a9a !important;',
    'color: #64748B !important;',
    'kpi-tag !important color')

# ==============================================================================
# 9. DELTA badges
# ==============================================================================
rpl('background: rgba(34,211,238,0.12) !important;\n  color: #22D3EE !important;\n  border: 1px solid rgba(34,211,238,0.25) !important;',
    'background: rgba(22,163,74,0.08) !important;\n  color: #16a34a !important;\n  border: 1px solid rgba(22,163,74,0.2) !important;',
    'delta-up to green')
rpl('.delta-up{background:rgba(34,211,238,0.1);color:#22D3EE;}',
    '.delta-up{background:rgba(22,163,74,0.08);color:#16a34a;}',
    'delta-up base')
rpl('.delta-down{background:rgba(248,113,113,0.1);color:#F87171;}',
    '.delta-down{background:rgba(220,38,38,0.08);color:#dc2626;}',
    'delta-down base')

# ==============================================================================
# 10. CARDS
# ==============================================================================
rpl('.card{background:#161B22;border-radius:12px;padding:20px;border:1px solid rgba(245,225,164,0.28);backdrop-filter:none;}',
    '.card{background:#FFFFFF;border-radius:12px;padding:20px;border:1px solid #DCE3EC;backdrop-filter:none;}',
    'card base')
rpl('box-shadow: 0 8px 32px rgba(0,0,0,0.5), 0 0 0 1px rgba(245,225,164,0.18);\n  border-color: rgba(245,225,164,0.45) !important;',
    'box-shadow: 0 4px 16px rgba(15,23,42,0.08);\n  border-color: rgba(59,130,246,0.2) !important;',
    'card hover shadow+border')
rpl('.card{box-shadow:0 4px 24px rgba(0,0,0,0.4) !important;transition:box-shadow 0.2s ease;}',
    '.card{box-shadow:0 1px 3px rgba(15,23,42,0.05) !important;transition:box-shadow 0.2s ease;}',
    'card shadow !important')
rpl('.card:hover{box-shadow:0 6px 32px rgba(0,0,0,0.6) !important;}',
    '.card:hover{box-shadow:0 4px 16px rgba(15,23,42,0.08) !important;}',
    'card hover shadow !important')
# card standardization override with !important
rpl('.card {\n  background:#161B22 !important;\n  border: 0.5px solid rgba(245,225,164,0.08) !important;\n  border-radius: 14px !important;\n}',
    '.card {\n  background:#FFFFFF !important;\n  border: 1px solid #DCE3EC !important;\n  border-radius: 14px !important;\n}',
    'card standardization !important')
rpl('.card:hover {\n  border-color: rgba(255,255,255,0.14) !important;\n  box-shadow: 0 6px 28px rgba(0,0,0,0.35) !important;\n  transform: translateY(-1px) !important;\n}',
    '.card:hover {\n  border-color: rgba(59,130,246,0.2) !important;\n  box-shadow: 0 4px 16px rgba(15,23,42,0.08) !important;\n  transform: translateY(-1px) !important;\n}',
    'card hover standardization !important')
rpl('.card-title { color: #d1d5e0 !important;\n  font-size: 13px !important;\n}',
    '.card-title { color: #1E293B !important;\n  font-size: 13px !important;\n}',
    'card-title enhancement override')
rpl('/* Uniform card-title color across all panels */\n.card-title { color: #D1D5DB !important; }\n.card-sub   { color:#94A3B8 !important; }',
    '/* Uniform card-title color across all panels */\n.card-title { color: #1E293B !important; }\n.card-sub   { color:#64748B !important; }',
    'card-title uniform !important')
rpl('.card-title{font-size:13px;font-weight:700;color:#F5E1A4;line-height:1.3;}',
    '.card-title{font-size:13px;font-weight:700;color:#1E293B;line-height:1.3;}',
    'card-title base')
rpl('.card-sub{font-size:10px;color:#94A3B8;margin-top:3px;}',
    '.card-sub{font-size:10px;color:#64748B;margin-top:3px;}',
    'card-sub base')

# ==============================================================================
# 11. SECTION LABEL
# ==============================================================================
rpl('.section-label{font-size:10px;font-weight:700;letter-spacing:0.12em;color:#D1D5DB;text-transform:uppercase;margin-bottom:12px;}',
    '.section-label{font-size:10px;font-weight:700;letter-spacing:0.12em;color:#475569;text-transform:uppercase;margin-bottom:12px;}',
    'section-label color')

# ==============================================================================
# 12. HBAR
# ==============================================================================
rpl('.hbar-outer{flex:1;height:26px;background:rgba(255,255,255,0.09);border-radius:5px;overflow:hidden;}',
    '.hbar-outer{flex:1;height:26px;background:#EEF2F7;border-radius:5px;overflow:hidden;}',
    'hbar-outer bg')
rpl('.hbar-right{font-size:11px;color:#94A3B8;min-width:56px;text-align:right;flex-shrink:0;}',
    '.hbar-right{font-size:11px;color:#64748B;min-width:56px;text-align:right;flex-shrink:0;}',
    'hbar-right color')
rpl('.hbar-label{font-size:12px;font-weight:600;color:#D1D5DB;text-align:right;min-width:100px;max-width:100px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;flex-shrink:0;}',
    '.hbar-label{font-size:12px;font-weight:600;color:#475569;text-align:right;min-width:100px;max-width:100px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;flex-shrink:0;}',
    'hbar-label color')

# ==============================================================================
# 13. TOGGLE-GROUP / TGL
# ==============================================================================
rpl('.toggle-group{display:flex;background:rgba(255,255,255,0.04);border-radius:7px;padding:2px;gap:2px;flex-shrink:0;}',
    '.toggle-group{display:flex;background:#EEF2F7;border-radius:7px;padding:2px;gap:2px;flex-shrink:0;}',
    'toggle-group bg')
rpl('.tgl{font-size:10px;font-weight:700;letter-spacing:0.05em;padding:4px 10px;border-radius:5px;border:none;cursor:pointer;color:#94A3B8;background:transparent;transition:all 0.15s;}',
    '.tgl{font-size:10px;font-weight:700;letter-spacing:0.05em;padding:4px 10px;border-radius:5px;border:none;cursor:pointer;color:#64748B;background:transparent;transition:all 0.15s;}',
    'tgl base color')
rpl('.tgl.active{background:rgba(255,255,255,0.13);color:#e2e8f0;}',
    '.tgl.active{background:#FFFFFF;color:#1E293B;box-shadow:0 1px 3px rgba(15,23,42,0.08);}',
    'tgl.active bg+color')
rpl('.tgl.active.blue{background:rgba(245,225,164,0.15);color:#F5E1A4;}',
    '.tgl.active.blue{background:rgba(29,78,216,0.1);color:#1D4ED8;}',
    'tgl.active.blue')
rpl('.tgl.active.purple{background:rgba(45,212,191,0.2);color:#2dd4bf;}',
    '.tgl.active.purple{background:rgba(124,58,237,0.1);color:#7C3AED;}',
    'tgl.active.purple')
rpl('.tgl.active.green{background:rgba(52,211,153,0.2);color:#34d399;}',
    '.tgl.active.green{background:rgba(22,163,74,0.1);color:#16a34a;}',
    'tgl.active.green')
rpl('box-shadow: 0 0 12px rgba(103,232,249,0.3) !important;',
    'box-shadow: 0 1px 3px rgba(15,23,42,0.08) !important;',
    'tgl.active shadow')

# ==============================================================================
# 14. BAR LIST
# ==============================================================================
rpl('.bar-item:hover{background:rgba(255,255,255,0.03);}',
    '.bar-item:hover{background:rgba(71,85,105,0.04);}',
    'bar-item hover')
rpl('.bar-item.selected{background:rgba(245,225,164,0.05);border-color:rgba(245,225,164,0.2);}',
    '.bar-item.selected{background:rgba(59,130,246,0.04);border-color:rgba(59,130,246,0.15);}',
    'bar-item.selected')
rpl('.bar-name{font-size:12px;color:#D1D5DB;font-weight:500;flex:1;min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;}',
    '.bar-name{font-size:12px;color:#475569;font-weight:500;flex:1;min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;}',
    'bar-name color')
rpl('.bar-track{background:rgba(255,255,255,0.04);border-radius:4px;height:6px;overflow:hidden;}',
    '.bar-track{background:#EEF2F7;border-radius:4px;height:6px;overflow:hidden;}',
    'bar-track bg')
rpl('.bar-expand{margin-top:8px;padding:8px;background:rgba(255,255,255,0.02);border-radius:6px;display:none;gap:16px;flex-wrap:wrap;}',
    '.bar-expand{margin-top:8px;padding:8px;background:#F8FAFC;border-radius:6px;display:none;gap:16px;flex-wrap:wrap;}',
    'bar-expand bg')
rpl('.expand-item{font-size:10px;color:#94A3B8;}',
    '.expand-item{font-size:10px;color:#64748B;}',
    'expand-item color')

# ==============================================================================
# 15. DONUT / DL
# ==============================================================================
rpl('.donut-center-val{font-size:18px;font-weight:700;color:#e2e8f0;line-height:1;}',
    '.donut-center-val{font-size:18px;font-weight:700;color:#0F172A;line-height:1;}',
    'donut-center-val color')
rpl('.donut-center-sub{font-size:10px;color:#94A3B8;margin-top:3px;}',
    '.donut-center-sub{font-size:10px;color:#64748B;margin-top:3px;}',
    'donut-center-sub color')
rpl('.dl-item2:hover,.dl-item2.dli-active{background:rgba(255,255,255,0.04);border-color:rgba(255,255,255,0.13);}',
    '.dl-item2:hover,.dl-item2.dli-active{background:rgba(59,130,246,0.04);border-color:rgba(59,130,246,0.12);}',
    'dl-item2 hover')
rpl('.dl-name{font-size:12px;color:#D1D5DB;font-weight:600;}',
    '.dl-name{font-size:12px;color:#334155;font-weight:600;}',
    'dl-name color')
rpl('.dl-vol{font-size:11px;color:#94A3B8;}',
    '.dl-vol{font-size:11px;color:#64748B;}',
    'dl-vol color')
rpl('.dl-bar-wrap{height:2px;background:rgba(255,255,255,0.10);border-radius:2px;margin-top:5px;overflow:hidden;}',
    '.dl-bar-wrap{height:2px;background:#EEF2F7;border-radius:2px;margin-top:5px;overflow:hidden;}',
    'dl-bar-wrap bg')
rpl('.donut-tip{position:absolute;background:#161B22;border:0.5px solid rgba(255,255,255,0.12);',
    '.donut-tip{position:absolute;background:#0F172A;border:0.5px solid rgba(148,163,184,0.25);',
    'donut-tip bg + border')
rpl('.donut-tip-name{font-weight:700;color:#e2e8f0;margin-bottom:3px;}',
    '.donut-tip-name{font-weight:700;color:#FFFFFF;margin-bottom:3px;}',
    'donut-tip-name color')
rpl('.donut-tip-row{color:#94A3B8;}',
    '.donut-tip-row{color:#E2E8F0;}',
    'donut-tip-row color')
rpl('.donut-tip-val{color:#D1D5DB;font-weight:600;}',
    '.donut-tip-val{color:#FFFFFF;font-weight:600;}',
    'donut-tip-val color')
rpl('.dl-item{display:flex;align-items:center;gap:7px;font-size:11px;color:#D1D5DB;cursor:pointer;}',
    '.dl-item{display:flex;align-items:center;gap:7px;font-size:11px;color:#475569;cursor:pointer;}',
    'dl-item color')

# ==============================================================================
# 16. UF legend
# ==============================================================================
rpl('.uf-legend-item{display:flex;align-items:center;gap:5px;font-size:10px;color:#D1D5DB;}',
    '.uf-legend-item{display:flex;align-items:center;gap:5px;font-size:10px;color:#475569;}',
    'uf-legend-item color')
rpl('.kpi-grid-4 {\n  display:grid;grid-template-columns:repeat(4,1fr);\n  gap:1px;background:rgba(255,255,255,0.04);',
    '.kpi-grid-4 {\n  display:grid;grid-template-columns:repeat(4,1fr);\n  gap:1px;background:#DCE3EC;',
    'kpi-grid-4 gap bg')

# ==============================================================================
# 17. SUB-TABS (.stab)
# ==============================================================================
rpl('.sub-tabs{display:flex;gap:4px;margin-bottom:16px;padding-bottom:12px;border-bottom:0.5px solid rgba(245,225,164,0.25);}',
    '.sub-tabs{display:flex;gap:4px;margin-bottom:16px;padding-bottom:12px;border-bottom:1px solid #DCE3EC;}',
    'sub-tabs border')
rpl('.stab{font-size:11px;font-weight:600;padding:5px 14px;border-radius:7px;border:0.5px solid rgba(245,225,164,0.30);background:#2D3748;color:#CBD5E0;cursor:pointer;transition:all 0.15s;display:flex;align-items:center;gap:5px;}',
    '.stab{font-size:11px;font-weight:600;padding:5px 14px;border-radius:7px;border:1px solid #CBD5E1;background:#F8FAFC;color:#475569;cursor:pointer;transition:all 0.15s;display:flex;align-items:center;gap:5px;}',
    'stab base')
rpl('.stab.active{background:rgba(245,225,164,0.15);color:#F5E1A4;border-color:rgba(245,225,164,0.60);}',
    '.stab.active{background:rgba(29,78,216,0.08);color:#1D4ED8;border-color:rgba(29,78,216,0.3);}',
    'stab.active')
rpl('box-shadow: 0 2px 12px rgba(245,225,164,0.2) !important;',
    'box-shadow: 0 1px 4px rgba(29,78,216,0.1) !important;',
    'stab.active shadow')

# ==============================================================================
# 18. META-TABLE
# ==============================================================================
rpl('.meta-table th{font-size:11px;font-weight:700;color:#D1D5DB;text-transform:uppercase;letter-spacing:0.08em;padding:8px 10px;border-bottom:0.5px solid rgba(245,225,164,0.15);text-align:right;}',
    '.meta-table th{font-size:11px;font-weight:700;color:#475569;text-transform:uppercase;letter-spacing:0.08em;padding:8px 10px;border-bottom:1px solid #DCE3EC;text-align:right;}',
    'meta-table th')
rpl('.meta-table td{font-size:13px;padding:7px 10px;border-bottom:0.5px solid rgba(245,225,164,0.05);text-align:right;font-variant-numeric:tabular-nums;}',
    '.meta-table td{font-size:13px;padding:7px 10px;border-bottom:1px solid #F1F5F9;text-align:right;font-variant-numeric:tabular-nums;}',
    'meta-table td')
rpl('.meta-table td:first-child{text-align:left;color:#D1D5DB;font-weight:600;}',
    '.meta-table td:first-child{text-align:left;color:#334155;font-weight:600;}',
    'meta-table td:first-child')
rpl('.meta-table tr:hover td{background:rgba(255,255,255,0.02);}',
    '.meta-table tr:hover td{background:rgba(59,130,246,0.03);}',
    'meta-table tr:hover')

# ==============================================================================
# 19. TABLE general
# ==============================================================================
rpl('table th{font-size:12px !important;letter-spacing:0.08em !important;color:#B0BAC9 !important;padding:10px 14px !important;}',
    'table th{font-size:12px !important;letter-spacing:0.08em !important;color:#475569 !important;padding:10px 14px !important;}',
    'table th !important')
rpl('table td{font-size:14px !important;padding:10px 14px !important;border-bottom:0.5px solid rgba(255,255,255,0.04) !important;}',
    'table td{font-size:14px !important;padding:10px 14px !important;border-bottom:1px solid #F1F5F9 !important;}',
    'table td !important')
rpl('table tbody tr:hover {\n  background: rgba(103,232,249,0.06) !important;\n}',
    'table tbody tr:hover {\n  background: rgba(59,130,246,0.04) !important;\n}',
    'table tr:hover')

# ==============================================================================
# 20. SCROLLBAR
# ==============================================================================
rpl('::-webkit-scrollbar-track { background:#0D1117; }',
    '::-webkit-scrollbar-track { background:#F1F5F9; }',
    'scrollbar-track bg')

# ==============================================================================
# 21. FOOTER + ALERTS
# ==============================================================================
rpl('.dash-footer{font-size:10px;color:#3d4451;padding:12px 0 4px;display:none;justify-content:space-between;border-top:0.5px solid rgba(255,255,255,0.04);margin-top:8px;}',
    '.dash-footer{font-size:10px;color:#94A3B8;padding:12px 0 4px;display:none;justify-content:space-between;border-top:1px solid #EEF2F7;margin-top:8px;}',
    'dash-footer')
rpl('.partial-alert{background:rgba(251,191,36,0.06);border:0.5px solid rgba(251,191,36,0.2);border-radius:8px;padding:8px 14px;font-size:11px;color:#fbbf24;margin-bottom:14px;}',
    '.partial-alert{background:rgba(217,119,6,0.06);border:1px solid rgba(217,119,6,0.2);border-radius:8px;padding:8px 14px;font-size:11px;color:#d97706;margin-bottom:14px;}',
    'partial-alert')

# ==============================================================================
# 22. ED Leaflet
# ==============================================================================
rpl('#ed-leaflet-map{height:600px;border-radius:0 0 12px 12px;background:#080f1c;}',
    '#ed-leaflet-map{height:600px;border-radius:0 0 12px 12px;background:#EEF2F7;}',
    'ed-leaflet-map bg')
rpl('.ed-mtgl{background:rgba(0,0,0,0.2);border:1px solid rgba(234,179,8,0.15);\n  color:#94A3B8;',
    '.ed-mtgl{background:#F8FAFC;border:1px solid #CBD5E1;\n  color:#475569;',
    'ed-mtgl base')

# ==============================================================================
# 23. Diagnóstico [id$="-diag"] inline bg that may remain
# ==============================================================================
rpl('background:#161B22;border:0.5px solid rgba(255,255,255,0.12);',
    'background:#0F172A;border:1px solid rgba(148,163,184,0.25);',
    'donut-tip bg/border duplicate check')

print('\nTotal patches: {}'.format(patches))
print('Diff: {:+,} bytes'.format(len(html) - original_len))

ts = datetime.datetime.now().strftime('%Y%m%d_%H%M')
ver = 'Dashboard_farma_sul/versoes/Dashboard_Farma_Sul_{}_GlobalSourceFix.html'.format(ts)
open(SRC, 'w', encoding='utf-8').write(html)
open(ver, 'w', encoding='utf-8').write(html)
print('Salvo: ' + SRC)
print('Versao: ' + ver)
