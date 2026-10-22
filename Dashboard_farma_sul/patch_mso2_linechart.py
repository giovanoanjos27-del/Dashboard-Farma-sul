"""
patch_mso2_linechart.py
Replaces the /* HEATMAP TABLE */ block in renderMSO2() with a conditional
LINE CHART (when isShare===true) / HEATMAP (when isShare===false) block.
"""

import os
import shutil
from datetime import datetime

SRC = r"C:\Users\valqu\OneDrive\Documentos\Claude\Projects\projeto Dashboard_farma_sul\Dashboard_farma_sul\Dashboard_Farma_Sul_20260512_2220.html"
VERSIONS_DIR = r"C:\Users\valqu\OneDrive\Documentos\Claude\Projects\projeto Dashboard_farma_sul\Dashboard_farma_sul\versoes"

# ── anchors ───────────────────────────────────────────────────────────────────
START_ANCHOR = "  /* HEATMAP TABLE */"
END_ANCHOR   = "  renderMSO2Insight();"

# ── new code (replaces everything between START_ANCHOR and END_ANCHOR) ────────
NEW_BLOCK = """  /* TABLE / LINE CHART */
  var tableEl = document.getElementById('mso2-table');
  var tblTitleEl = document.getElementById('mso2-table-title');
  if(tblTitleEl) tblTitleEl.style.display='none';
  if(tableEl){
    if(isShare){
      /* LINE CHART — share % evolution Jan/25·Fev/25·Mar/25 → Jan/26·Fev/26·Mar/26 */
      var dLine = MKTSHARE_OVERVIEW[mkt];
      if(!dLine){ tableEl.innerHTML=''; }
      else {
        tableEl.innerHTML = '<div style="margin-bottom:6px;">'
          +'<div style="font-size:9px;font-weight:700;letter-spacing:.13em;color:#64748b;text-transform:uppercase;margin-bottom:10px;">EVOLUÇÃO MENSAL DO SHARE — Jan/25 · Fev/25 · Mar/25 &nbsp;→&nbsp; Jan/26 · Fev/26 · Mar/26</div>'
          +'<div style="position:relative;height:210px;">'
            +'<canvas id="mso2-line-canvas"></canvas>'
          +'</div>'
          +'</div>';
        var prevLChart = Chart.getChart('mso2-line-canvas');
        if(prevLChart) prevLChart.destroy();
        var cvLine = document.getElementById('mso2-line-canvas');
        cvLine.removeAttribute('width'); cvLine.removeAttribute('height');
        cvLine.style.width=''; cvLine.style.height='';
        var lineLabels = ['Jan/25','Fev/25','Mar/25','Jan/26','Fev/26','Mar/26'];
        var lineDatasets = brands.map(function(b){
          var bd=dLine[b]; if(!bd) return null;
          var j25=bd.jan25!=null?bd.jan25:bd.fytd25;
          var f25=bd.feb25!=null?bd.feb25:bd.fytd25;
          var m25=bd.mar25!=null?bd.mar25:bd.fytd25;
          var j26=bd.monthly[6], f26=bd.monthly[7], m26=bd.monthly[8];
          var cor=colors[b]||'#e2e8f0';
          return {
            label:b,
            data:[j25,f25,m25,j26,f26,m26],
            borderColor:cor,
            backgroundColor:cor+'18',
            pointBackgroundColor:[cor+'99',cor+'99',cor+'99',cor,cor,cor],
            pointBorderColor:[cor+'99',cor+'99',cor+'99',cor,cor,cor],
            pointRadius:[3,3,3,5,5,5],
            pointHoverRadius:8,
            tension:0.35,
            borderWidth:2.5,
            fill:false,
            borderDash:[]
          };
        }).filter(Boolean);
        new Chart(cvLine, {
          type:'line',
          data:{labels:lineLabels, datasets:lineDatasets},
          options:{
            responsive:true,
            maintainAspectRatio:false,
            interaction:{mode:'index',intersect:false},
            plugins:{
              legend:{display:false},
              tooltip:{
                backgroundColor:'#1e293b',
                borderColor:'rgba(255,255,255,0.1)',
                borderWidth:1,
                titleColor:'#94A3B8',
                titleFont:{size:11,weight:'700'},
                bodyColor:'#e2e8f0',
                bodyFont:{size:11},
                padding:10,
                callbacks:{
                  label:function(ctx){
                    return ' '+ctx.dataset.label+': '+ctx.parsed.y.toFixed(2)+'%';
                  }
                }
              }
            },
            scales:{
              x:{
                ticks:{color:'#64748b',font:{size:10}},
                grid:{color:'rgba(255,255,255,0.05)'},
                border:{color:'rgba(255,255,255,0.08)'}
              },
              y:{
                ticks:{color:'#64748b',font:{size:10},callback:function(v){return v.toFixed(1)+'%';}},
                grid:{color:'rgba(255,255,255,0.05)'},
                border:{color:'rgba(255,255,255,0.08)'}
              }
            }
          },
          plugins:[{
            id:'mso2sep',
            afterDraw:function(chart){
              var cx=chart.ctx, xs=chart.scales.x;
              var x=(xs.getPixelForValue(2)+xs.getPixelForValue(3))/2;
              cx.save();
              cx.strokeStyle='rgba(251,191,36,0.35)';
              cx.setLineDash([4,4]);
              cx.lineWidth=1.5;
              cx.beginPath();
              cx.moveTo(x,chart.chartArea.top);
              cx.lineTo(x,chart.chartArea.bottom);
              cx.stroke();
              cx.setLineDash([]);
              cx.fillStyle='rgba(251,191,36,0.55)';
              cx.font='700 9px system-ui,sans-serif';
              cx.textAlign='center';
              cx.letterSpacing='0.1em';
              cx.fillText('2025  →  2026',x,chart.chartArea.top+10);
              cx.restore();
            }
          }]
        });
      }
    } else {
      /* HEATMAP — R$ MM / Unidades: % change per month */
      function heatCell(dpp){
        var abs=Math.abs(dpp);
        var alpha=isShare?Math.min(0.65,abs/4):Math.min(0.65,Math.abs(dpp)/30);
        var bg=dpp>=0?'rgba(52,211,153,'+alpha+')':'rgba(239,68,68,'+alpha+')';
        var txt=dpp>=0?'#6ee7b7':'#fca5a5';
        if(abs<(isShare?0.05:0.2)){bg='transparent';txt='#64748b';}
        var label=isShare?((dpp>=0?'+':'')+dpp.toFixed(2)+'pp'):((dpp>=0?'+':'')+dpp.toFixed(1)+'%');
        return '<td style="padding:8px 12px;text-align:center;font-size:11px;font-weight:700;color:'+txt+';background:'+bg+';border:0.5px solid rgba(255,255,255,0.04);">'+label+'</td>';
      }
      var months=[{k:'jan'},{k:'fev'},{k:'mar'}];
      var rows2=brands.map(function(b){
        var p25=d25[b],p26=d26[b]; if(!p25||!p26) return '';
        var cor=colors[b]||'#e2e8f0';
        var mCells=months.map(function(m){
          var v25=p25[m.k],v26=p26[m.k];
          if(v25===null||v25===undefined||v26===null||v26===undefined)
            return '<td style="padding:8px 12px;text-align:center;font-size:11px;color:#3d4451;border:0.5px solid rgba(255,255,255,0.04);">—</td>';
          var dv=isShare?Math.round((v26-v25)*100)/100:(v25>0?Math.round((v26-v25)/v25*1000)/10:0);
          return heatCell(dv);
        }).join('');
        var acumD=calcDelta(p25.acum,p26.acum);
        return '<tr>'
          +'<td style="padding:8px 12px;border:0.5px solid rgba(255,255,255,0.04);">'
            +'<span style="display:inline-block;width:7px;height:7px;border-radius:50%;background:'+cor+';margin-right:6px;vertical-align:middle;"></span>'
            +'<span style="font-size:10px;font-weight:700;color:'+cor+';">'+b+'</span>'
          +'</td>'
          +mCells
          +heatCell(acumD.raw)
          +'</tr>';
      }).join('');
      var thStyle='padding:8px 12px;font-size:9px;font-weight:700;letter-spacing:.1em;color:#64748b;text-transform:uppercase;background:#0D1117;border:0.5px solid rgba(255,255,255,0.04);';
      tableEl.innerHTML='<div style="background:#161B22;border-radius:10px;overflow:hidden;border:0.5px solid rgba(255,255,255,0.06);">'
        +'<table style="width:100%;border-collapse:collapse;">'
        +'<thead><tr>'
        +'<th style="'+thStyle+'text-align:left;">MARCA</th>'
        +'<th style="'+thStyle+'text-align:center;">JAN</th>'
        +'<th style="'+thStyle+'text-align:center;">FEV</th>'
        +'<th style="'+thStyle+'text-align:center;">MAR</th>'
        +'<th style="'+thStyle+'text-align:center;">ACUM</th>'
        +'</tr></thead><tbody>'+rows2+'</tbody></table>'
        +(GrowthMode?'<div style="padding:5px 12px;font-size:9px;color:#3d4451;">★ Acum Jan-Mar/25 estimado proporcionalmente.</div>':'')
        +'</div>';
    }
  }
"""

# ── main ──────────────────────────────────────────────────────────────────────
def main():
    with open(SRC, "r", encoding="utf-8") as f:
        content = f.read()

    # locate start and end anchors
    idx_start = content.find(START_ANCHOR)
    if idx_start == -1:
        raise ValueError(f"START_ANCHOR not found: {START_ANCHOR!r}")

    idx_end = content.find(END_ANCHOR, idx_start)
    if idx_end == -1:
        raise ValueError(f"END_ANCHOR not found after position {idx_start}: {END_ANCHOR!r}")

    print(f"START_ANCHOR found at char {idx_start}")
    print(f"END_ANCHOR   found at char {idx_end}")

    # build new content: everything before START, then NEW_BLOCK, then END_ANCHOR onward
    new_content = content[:idx_start] + NEW_BLOCK + content[idx_end:]

    # verify replacement
    if "/* TABLE / LINE CHART */" not in new_content:
        raise RuntimeError("Replacement marker not found in result — aborting.")
    if "mso2-line-canvas" not in new_content:
        raise RuntimeError("mso2-line-canvas not found in result — aborting.")
    if "mso2sep" not in new_content:
        raise RuntimeError("mso2sep not found in result — aborting.")
    if "/* HEATMAP TABLE */" in new_content:
        raise RuntimeError("Old START_ANCHOR still present — replacement failed.")

    # backup
    os.makedirs(VERSIONS_DIR, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M")
    backup_name = f"Dashboard_Farma_Sul_{ts}_MSO2LineChart.html"
    backup_path = os.path.join(VERSIONS_DIR, backup_name)
    shutil.copy2(SRC, backup_path)
    print(f"Backup saved: {backup_path}")

    # write main file
    with open(SRC, "w", encoding="utf-8") as f:
        f.write(new_content)
    print(f"Main file updated: {SRC}")

    # final verification
    with open(SRC, "r", encoding="utf-8") as f:
        verify = f.read()
    assert "/* TABLE / LINE CHART */" in verify, "VERIFY FAILED: new comment missing"
    assert "mso2-line-canvas" in verify,          "VERIFY FAILED: mso2-line-canvas missing"
    assert "mso2sep" in verify,                    "VERIFY FAILED: mso2sep missing"
    assert "/* HEATMAP TABLE */" not in verify,    "VERIFY FAILED: old block still present"
    print("All verifications PASSED.")

if __name__ == "__main__":
    main()
