"""Login MG (24/11/2026): usuário 'MG' (senhas definidas pelo Giovano), perfil 'mg' = só a aba Sell Out e só o cliente Araujo.
Uso: python mg_login.py <base.html>"""
import sys
H = sys.argv[1]; h = open(H, encoding="utf-8", newline="").read()


def rep(a, b, n=1):
    global h
    if h.count(a) != n and h.count(a.replace("\n", "\r\n")) == n: a, b = a.replace("\n", "\r\n"), b.replace("\n", "\r\n")
    assert h.count(a) == n, (h.count(a), a[:90]); h = h.replace(a, b)


assert "role:'mg'" not in h, "já aplicado"
rep("""                  <option value="SCJ">SCJ</option>
                </select>""", """                  <option value="SCJ">SCJ</option>
                  <option value="MG">MG</option>
                </select>""")
rep("""  'SCJ':     { s1:'123', s2:'123', role:'scj' }
};""", """  'SCJ':     { s1:'123', s2:'123', role:'scj' },
  'MG':      { s1:'12345', s2:'12345', role:'mg' }   /* MG: só Sell Out › Araujo */
};""")
rep("var _loginRole     = null; /* 'full' | 'scj' */", "var _loginRole     = null; /* 'full' | 'scj' | 'mg' */")
rep("""  /* Restrições específicas por usuário (role full com visão parcial) */""",
    """  if(_loginRole==='mg'){
    /* MG: só a aba Sell Out e só o cliente Araujo */
    document.querySelectorAll('.ctab').forEach(function(b){ if(!/'sellout'/.test(b.getAttribute('onclick')||'')) b.style.display='none'; });
    var _sel=document.getElementById('sellout-client-selector');
    if(_sel){ for(var _i=_sel.options.length-1;_i>=0;_i--){ if(_sel.options[_i].value!=='araujo') _sel.remove(_i); } _sel.value='araujo'; }
    ['btn-update-data','btn-save-dashboard','sj-compradora-row','ns-compradora-row'].forEach(function(id){ var e=document.getElementById(id); if(e) e.style.display='none'; });
    var _tMG=document.getElementById('dash-main-title'); if(_tMG) _tMG.textContent='Dashboard Sell Out — Araujo';
    setTimeout(function(){ var _bS=document.querySelector('.ctab[onclick*=sellout]'); switchClient('sellout', _bS);
      var _s2=document.getElementById('sellout-client-selector'); if(_s2) _s2.value='araujo'; switchSellOutClient('araujo'); }, 900);
  }
  /* Restrições específicas por usuário (role full com visão parcial) */""")
rep("""  /* Bloqueio de acesso para perfil SCJ */
  if(_loginRole==='scj'){""", """  /* MG: só Sell Out */
  if(_loginRole==='mg' && id!=='sellout'){ if(typeof showAccessDenied==='function') showAccessDenied(); return; }
  /* Bloqueio de acesso para perfil SCJ */
  if(_loginRole==='scj'){""")
rep("""function switchSellOutClient(clientId) {
  activeSelloutClient = clientId;""", """function switchSellOutClient(clientId) {
  if(typeof _loginRole!=='undefined' && _loginRole==='mg') clientId = 'araujo';   /* MG: só Araujo */
  activeSelloutClient = clientId;""")
open(H, "w", encoding="utf-8", newline="").write(h); print("ok")
