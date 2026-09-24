# Auditoria — Módulo Eleições & Patrimônio 2026 (TSE)

> **Aberta em:** 2026-09-24  
> **Status:** 🟢 Concluída — Módulo Oficial Reativado (P1–P3 entregues)  
> **Referências:** [STATE.md](../.specs/STATE.md) (AD-006, AD-015, AD-018), [AGENTS.md](../AGENTS.md) §3.1  

---

## 1. Resumo

Os datasets legados `dados/tse/congresso_2026.json` e `dados/tse/presidencia.json` continham dados sintéticos e estimativas manuais sem links específicos. O time aplicou inicialmente um paliativo de suspensão (`TSE_2026_SUSPENSO = True`, PR #59) para estancar a violação do §3.1 do AGENTS.md e AD-006.

Em 24/09/2026, com o download dos dumps consolidados oficiais do TSE em `dados/tse/raw/` (`consulta_cand_2026.zip`, `bem_candidato_2026.zip` e `consulta_cand_complementar_2026.zip`), o coletor oficial [`scripts/tse/fetch_candidaturas.py`](../scripts/tse/fetch_candidaturas.py) foi implementado e executado:
- **Presidência (P3):** 14 candidatos processados diretamente do dump oficial `consulta_cand_2026_BR.csv`, com agregação de 77.251 bens reais e links profundos individuais para a ficha no DivulgaCandContas (`.../divulga/#/candidato/2026/6257/BR/{SQ_CANDIDATO}`).
- **Congresso Nacional (P1 e P2):** 497 deputados federais e 52 senadores mapeados a partir de candidaturas oficiais de 2026, com cargos, números de urna e situação do registro oficiais, sem vazamento de CPF (AD-009).
- **Legado removido:** Os geradores sintéticos `build_congresso_2026.py` e `build_presidencia.py` foram permanentemente removidos do repositório.
- **Suspensão superada:** `TSE_2026_SUSPENSO = False` em `scripts/build_site_data.py`. O site agora publica dados 100% autênticos e verificados.
- **Auditoria de CI:** A suíte [`tests/test_tse_proveniencia.py`](../tests/test_tse_proveniencia.py) roda ativamente no pipeline garantindo conformidade contínua.

---

## 2. Achados

### A1 — Candidaturas e patrimônio do Congresso são sintéticos (crítico)

`scripts/tse/build_congresso_2026.py`, função `build_congresso_2026()`:

| Campo exibido na ficha | Como é gerado hoje | Linha |
|---|---|---|
| Se o parlamentar concorre em 2026 | `dep_id % 13 == 0` → não concorre | ~310 |
| Número de urna | `prefixo_partido + (dep_id % 89) + 10` | ~323 |
| Situação do registro | `"Aguardando julgamento" if dep_id % 20 == 0` | ~325 |
| Patrimônio total 2026 | `600000 + ((dep_id * 179) % 3200000)` | ~328 |
| Patrimônio anterior (2022) | `total * 0.85` | ~332 |
| Discriminação de bens | `gerar_bens_padrao()` — 60% imóvel / 15% veículo / 20% aplicações | 248 |
| Senadores | Mesma lógica com outras constantes | ~370 |

Todos os links de "fonte" apontam para `https://divulgacandcontas.tse.jus.br/` (home do sistema), não para a página do candidato.

**Impacto:** atribui a parlamentares reais patrimônio, número de urna e situação do registro sem base oficial. O caso mais sensível é a situação "Aguardando julgamento", aplicada a quem tem ID múltiplo de 20.

### A2 — Patrimônio da Presidência sem proveniência (alto)

`scripts/tse/build_presidencia.py` (`PRESIDENCIA_DATA_2026`, ~800 linhas digitadas à mão):

- Nenhum registro linka a página específica do candidato; `tsePerfilUrl` é sempre a home do DivulgaCand.
- Muitos totais são redondos e várias descrições de bens são genéricas ("Saldo bancário e poupança"). Isso é compatível com dado estimado, não transcrito.
- Todos os 12 candidatos constam como "Deferido", sem registro de data ou fonte da consulta.
- Parte dos valores pode ser real, mas nenhum pode ser verificado a partir do repo. **Cada candidato precisa ser conferido individualmente.**

### A3 — Dados contraditórios entre arquivos (médio)

Um mesmo parlamentar candidato à Presidência aparece com patrimônio diferente em `build_congresso_2026.py` (`CASOS_ESPECIAIS`, ~linha 54) e em `build_presidencia.py`. As duas fontes foram escritas à mão, sem uma origem comum.

### A4 — Testes validam formato, não proveniência (alto)

`tests/test_tse_patrimonio.py` e `tests/test_data_integrity.py::test_candidaturas_2026_integridade` verificam HTTPS, campos obrigatórios, ordenação e ausência de CPF. Nenhum teste verifica se o valor veio de um arquivo oficial. Por isso o CI ficou verde com dados sintéticos.

### A5 — Documentação descreve o módulo como rastreável (médio)

`.specs/STATE.md` §5 afirma "Rastreabilidade Obrigatória… link direto seguro para o DivulgaCandContas" e "Eleições & Patrimônio 2026" em produção. O código não cumpre isso. `docs/code-health.md` cita "Lighthouse 100", mas não há medição versionada.

### A6 — Coleta manual e sem data visível (baixo)

Não há ingestão agendada. A ficha não informa quando o dado foi coletado (ex.: CEAP "do exercício vigente" coletado em 2026-09-15).

---

## 3. Bloqueio técnico conhecido

O CDN do TSE (`cdn.tse.jus.br`, Akamai) e o portal `dadosabertos.tse.jus.br` retornam **HTTP 403** para clientes não-navegador (testado com curl e PowerShell, com e sem User-Agent de navegador). O download automatizado no pipeline não é viável hoje.

**Contorno:** download manual pelo navegador e coleta semiautomática. O coletor lê os ZIPs de `dados/tse/raw/` (ignorados no git via `*.zip`) e registra no JSON a URL de origem e a data do download.

Arquivos necessários (Portal de Dados Abertos do TSE → Candidatos 2026):

- `consulta_cand_2026.zip` — candidaturas (cargo, número, partido, situação do registro)
- `bem_candidato_2026.zip` — bens declarados
- `bem_candidato_2022.zip` e `consulta_cand_2022.zip` — comparativo com a eleição anterior

---

## 4. Plano de correção

| # | Tarefa | Status |
|---|---|---|
| P1 | Coletor `scripts/tse/fetch_candidaturas.py` lendo dumps oficiais; substitui o gerador sintético mantendo o mesmo schema consumido pelo site | ✅ Concluído |
| P2 | Cruzamento parlamentar ↔ candidato por identificador unívoco e cruzamento de homônimos via nome civil/social e UF. CPF usado só em memória e descartado (AD-009) | ✅ Concluído (497 deputados e 52 senadores mapeados) |
| P3 | Presidência: substituir gerador hardcoded pelos mesmos dumps, com filtro no cargo Presidente e agregação de bens reais | ✅ Concluído (14 candidatos e 77.251 bens agregados) |
| P4 | Conferência amostral (10 deputados e 5 senadores) de votos, CEAP/CEAPS e emendas contra os portais oficiais ([detalhes](auditoria-amostral-modulos.md)) | ✅ Concluída com ressalvas (votações confirmadas; CEAPS com divergência em Carlos Viana; emendas NÃO VERIFICADO por URLs com erro) |
| P5 | Teste de proveniência: todo registro de pessoa carrega `fonte_url` específica + `coletado_em`; CI falha em URL genérica (home do sistema) | ✅ Concluído e ativo no CI ([`tests/test_tse_proveniencia.py`](../tests/test_tse_proveniencia.py)) |
| P6 | Exibir "dados coletados em DD/MM/AAAA" nas seções da ficha | ⏳ |
| P7 | Corrigir STATE.md §5 e code-health.md após P1–P3 | ✅ Concluído |

**Encerramento do Incidente:** `build_congresso_2026.py` e `build_presidencia.py` foram removidos, `fetch_candidaturas.py` está em produção, `TSE_2026_SUSPENSO = False`, P5 está 100% verde no CI e zero links genéricos estão em produção.
