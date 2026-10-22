# Segundo Cérebro — Dashboard Farma Sul

> **REGRA ZERO:** Antes de qualquer trabalho:
> 1. Ler este arquivo
> 2. Ler `memory/status.md` — estado atual, meses confirmados, pendências
> 3. Ler `memory/MEMORY.md` — índice de tudo disponível
> 4. Verificar se existe nota diária hoje em `Dashboard_farma_sul/01 - Diário/YYYY-MM-DD.md`; se não existir, criar automaticamente
> Economiza toques e garante contexto completo sem o usuário repetir nada.

---

## Quem sou eu
**Giovano Anjos** — giovanoanjos27@gmail.com — Representante comercial HB (Repelentes & Inseticidas), gerencia dados de sell-out NielsenIQ para rede Farma Sul (SC/RS/PR).

---

## Arquivo principal
| O quê | Onde |
|-------|------|
| **dashboard (BASE ATIVO)** | `Dashboard_farma_sul/Dashboard_Farma_Sul_20260512_2220.html` |
| **versões** | `Dashboard_farma_sul/versoes/Dashboard_Farma_Sul_YYYYMMDD_HHMM.html` |
| **planilha mestre** | `Dashboard_farma_sul/Planilha_Mestre_FarmaSul_Giovano.xlsx` |
| **pipeline atualização** | `atualizar_dados.py` (rodar para sincronizar Excel → HTML) |

**REGRA OBRIGATÓRIA:** Toda alteração → salvar principal + criar versão com data/hora. Nunca sobrescrever sem versão.

## Pipeline de Dados (ROTAS FIXAS)
| Módulo | Aba(s) na planilha mestre |
|--------|--------------------------|
| **Sell Out SJ Total** | SO_SJoao_Isadora + SO_SJoao_Caroline (soma) |
| **Sell Out SJ Isadora** | SO_SJoao_Isadora |
| **Sell Out SJ Caroline** | SO_SJoao_Caroline |
| **Sell Out Nissei** | SO_Nissei (total HB) · SO_Nissei_Andre · SO_Nissei_Edmar |
| **Sell Out Clamed** | SO_Clamed |
| **Sell Out Panvel** | SO_Panvel |
| **Sell Out GAM** | SO_DDGAM |
| **Sell Out Gaúcha** | SO_DDGaúcha |
| **Sell Out Riomed** | SO_DDRiomed |
| **Sell In** | SO_SellIn |
| **Estoque Geral** | Estoque_Geral |
| **Cobertura** | Cob_SJoao (isadora) · Cob_SJoao ( Caroline) · Cob_Nissei · Cob_Clamed · Cob_Panvel |

**Comando de atualização:** `python atualizar_dados.py`
Exporta automaticamente cópia para `~\Downloads\Dashboard_FarmaSul_Giovano_YYYYMMDD_HHMM.html`

---

## Clientes (atalhos)
| Atalho | Quem é |
|--------|--------|
| **SJ** ou **São João** | São João Farmácias — maior conta, SC/RS/PR |
| **Isadora** | Compradora HB (repelentes) na São João |
| **Caroline** | Compradora conveniência (Lysoform/Glade/Pato) na São João |
| **Nissei** | Nissei Farmácias — PR/SP |
| **André** | Comprador OFF+EXPOSIS na Nissei |
| **Edmar** | Comprador RAID+Elétricos na Nissei |
| **CL** ou **Clamed** | Clamed Farmácias — SC |
| **PV** ou **Panvel** | Panvel Farmácias — SC/PR/RS |
| **GAM** ou **DD-GAM** | Distribuidor GAM — PR/SC/SP |
| **Gaúcha** ou **DD-Gaúcha** | Distribuidor Gaúcha — RS/SC/PR |
| **Riomed** | Distribuidor Riomed — SC/RS/SP |

→ Detalhes completos: `memory/clientes/`

---

## Termos técnicos
| Termo | Significado |
|-------|-------------|
| **SO** | Sell Out (saída de caixa) |
| **SI** | Sell In (compra do distribuidor) |
| **SJ_REC** | Array receita TOTAL São João (não só Isadora!) |
| **SJ_UNID** | Array volume TOTAL São João |
| **SJC_*** | Arrays exclusivos da Caroline |
| **Isadora** (nos arrays) | SJ_REC − SJC (calculado, não armazenado separado) |
| **override block** | Bloco JS ~linha 21600+ que sobrescreve consts no load |
| **saveDashboard()** | Serializa dados atuais de volta ao HTML |
| **sjModo** | `'total'` / `'isadora'` / `'caroline'` — controla a aba ativa |
| **parcial** | Meses incompletos do ano em curso |
| **HB** | Household & Body (linha OFF!/EXPOSIS) |
| **ED** | Estudo de Distribuição |

→ Glossário completo: `memory/glossary.md`

---

## Projetos ativos
| Projeto | Status |
|---------|--------|
| **dashboard** | ABR/2026 — manutenção contínua |

---

## Preferências do Giovano
- Sempre criar versão antes de editar
- Confirmar valores com usuário antes de aplicar dados novos
- Responder em português (pt-BR)
- Após cada ajuste: informar o que mudou de forma concisa + atualizar `memory/status.md`
- **Consultar memória primeiro** — nunca pedir contexto que já está salvo aqui

---

## Protocolo de sessão

### Ao iniciar
1. Ler este CLAUDE.md
2. Ler `memory/status.md` (estado do dashboard, pendências)
3. Verificar nota diária `Dashboard_farma_sul/01 - Diário/YYYY-MM-DD.md`; criar se não existir
4. Informar ao Giovano: último estado do dashboard + o que está pendente

### Após cada alteração no dashboard
1. Criar versão em `versoes/` com timestamp
2. Atualizar tabela "Últimas alterações" em `memory/status.md`
3. Atualizar tabela de meses confirmados se novos dados foram inseridos
4. Registrar na nota diária do dia (seção Dashboard)
