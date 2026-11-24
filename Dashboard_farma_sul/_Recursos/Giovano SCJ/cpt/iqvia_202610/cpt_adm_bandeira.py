"""ADM Pharma: Farmácia Canto Grande (Bombinhas/SC, 14202967000160) e Iaso Farma (Ponta Grossa/PR, 46308600000112),
grupo ADM com bandeira INDEPENDENTES na IQVIA, passam para bandeira GRUPO ADM PHARMA / canal FRANQUIAS (lista ADM Nov/26)."""
import json,sys;sys.stdout.reconfigure(encoding="utf-8")
H=sys.argv[1]; h=open(H,encoding="utf-8",newline="").read()
def pega(n):
    t="var "+n+"="; a=h.index(t)+len(t); o,b=json.JSONDecoder().raw_decode(h[a:]); return o,a,a+b
def troca(n,v):
    global h; _,a,b=pega(n); h=h[:a]+json.dumps(v,ensure_ascii=False,separators=(",",":"))+h[b:]
K,_,_=pega("CPT2_KEYS"); F,_,_=pega("CPT2_FAB_ALL"); C,_,_=pega("CPT2_CAT_ALL"); M,_,_=pega("CPT2_MARCA")
G="GRUPO ADM PHARMA"; ix=lambda k: K.index(k)
# Bombinhas: soma na chave ADM/Franquias existente e zera a de Independentes
o=ix(["SC","BOMBINHAS","INDEPENDENTES","INDEPENDENTES",G]); d=ix(["SC","BOMBINHAS",G,"FRANQUIAS",G])
for A in (C,F):
    A[d]=[round(x+y,2) for x,y in zip(A[d],A[o])]; A[o]=[0.0]*len(A[o])
for b in M:
    so=M[b].pop(str(o),None)
    if so: sd=M[b].get(str(d),[0.0]*8); M[b][str(d)]=[round(x+y,2) for x,y in zip(sd,so)]
# Ponta Grossa: não há chave ADM/Franquias na cidade → a própria chave muda de bandeira/canal
p=ix(["PR","PONTA GROSSA","INDEPENDENTES","INDEPENDENTES",G]); K[p]=["PR","PONTA GROSSA",G,"FRANQUIAS",G]
troca("CPT2_KEYS",K); troca("CPT2_CAT_ALL",C); troca("CPT2_FAB_ALL",F); troca("CPT2_MARCA",M)
for n in ("CPT2_LOJAS","CPT2_LOJAS_YTD","CPT2_LOJAS_Q1","CPT2_LOJAS_CAL","CPT2_INTOC","CPT2_INTOC_YTD","CPT2_INTOC_CAL"):
    D,_,_=pega(n)
    for uf in ("SC","PR"):
        s=D.pop(f"{uf}|INDEPENDENTES|INDEPENDENTES|{G}",None)
        if s: k=f"{uf}|FRANQUIAS|{G}|{G}"; D[k]=[x+y for x,y in zip(D.get(k,[0]*len(s)),s)]
    troca(n,D)
for n in ("CPT2_INTOC_YTD","CPT2_LOJAS_YTD"): pass
open(H,"w",encoding="utf-8",newline="").write(h); print("ok")
