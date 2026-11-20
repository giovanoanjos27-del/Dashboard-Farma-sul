"""CPT Clientes: Base/Espelho não repete bandeira que já está num OL nas mesmas UFs.
Para cada Base/Espelho-X, sai a bandeira que algum OL (não base, não SEM/OL) cobre em alguma UF da base
(respeitando CPT2_OL_UFS e CPT2_OL_SEM_UF). Uso: python cpt_base_espelho.py <base.html>"""
import sys, json
H = sys.argv[1]; h = open(H, encoding="utf-8", newline="").read()


def pega(nome):
    tag = "var " + nome + "="; a = h.index(tag) + len(tag)
    o, n = json.JSONDecoder().raw_decode(h[a:]); return o, a, a + n


B, a, b = pega("CPT2_OL_BANS"); U, _, _ = pega("CPT2_OL_UFS"); SU, _, _ = pega("CPT2_OL_SEM_UF"); K, _, _ = pega("CPT2_KEYS")
ALL = sorted({k[0] for k in K})
for base in [o for o in B if o.startswith("Base/")]:
    bu = set(U.get(base, ALL)); sai = []
    for ban in list(B[base]):
        for o, l in B.items():
            if o == base or o.startswith("Base/") or o == "SEM/OL" or ban not in l: continue
            if bu & (set(U.get(o, ALL)) - set(SU.get(o, {}).get(ban, []))):
                sai.append((ban, o)); B[base].remove(ban); break
    print(base, "→", len(B[base]), "bandeiras · saíram:", sai)
h = h[:a] + json.dumps(B, ensure_ascii=False, separators=(",", ":")) + h[b:]
open(H, "w", encoding="utf-8", newline="").write(h)
