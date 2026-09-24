# Auditoria — Módulo Eleições & Patrimônio 2026 (TSE)

> **Aberta em:** 2026-09-24
> **Status:** 🔴 Em correção
> **Referências:** [STATE.md](../.specs/STATE.md) (AD-006, AD-015, AD-018), [AGENTS.md](../AGENTS.md) §3.1

---

## 1. Resumo

Os datasets `dados/tse/congresso_2026.json` e `dados/tse/presidencia.json`, publicados nas fichas de deputados, senadores e na rota `/presidente`, **não vêm de fonte oficial rastreável**. Parte dos valores é gerada por fórmula a partir do ID do parlamentar. Isso viola AD-006 (verificabilidade estrita) e a regra §3.1 do AGENTS.md.

Decisão do time: **manter as páginas no ar e substituir os dados pelos oficiais do TSE**, aplicando imediatamente um paliativo de suspensão da exibição dos dados sintéticos enquanto P1–P3 são desenvolvidos.

Os demais módulos (votações nominais, CEAP/CEAPS, emendas CGU) usam fontes oficiais reais nos coletores. A conferência amostral P4 foi concluída com ressalvas ([detalhes](auditoria-amostral-modulos.md)).

### Paliativo em Produção (PR #59 / commit `bf0fd86`)

Para estancar imediatamente a violação do §3.1 do AGENTS.md e AD-006 sem quebrar o site, foi implementado o regime de suspensão temporária:
- **`scripts/build_site_data.py` (`TSE_2026_SUSPENSO = True`):** zera a exportação de `candidatura_2026` e `patrimonio` nos arquivos JSON consumidos pelo Astro (`dados/camara/deputados.json`, `dados/senado/senadores.json`, `site/src/data/congresso_2026.json`, `site/src/data/presidencia.json`), e emite `site/src/data/tse_status.json` com status de suspensão.
- **Componentes do Site:** `/presidente` renderiza o aviso oficial [`TseSuspensoAviso.astro`](../site/src/components/TseSuspensoAviso.astro) redirecionando para o DivulgaCandContas; listagens de parlamentares na home ocultam colunas e filtros de 2026.
- **Garantia em Testes:** `tests/test_tse_patrimonio.py::TestTSESuspensao` garante no CI que nenhum dado de candidatura ou patrimônio 2026 seja publicado enquanto a suspensão estiver ativa.

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
| P1 | Coletor `scripts/tse/fetch_candidaturas.py` lendo dumps oficiais; substitui o gerador sintético mantendo o mesmo schema consumido pelo site | ⏳ Aguardando dumps |
| P2 | Cruzamento parlamentar ↔ candidato por identificador unívoco (verificar se o dump 2026 traz CPF; se não, nome de urna + UF + cargo com lista de revisão manual). CPF usado só em memória e descartado (AD-009) | ⏳ |
| P3 | Presidência: substituir `PRESIDENCIA_DATA_2026` hardcoded pelos mesmos dumps, com filtro no cargo Presidente | ⏳ |
| P4 | Conferência amostral (10 deputados e 5 senadores) de votos, CEAP/CEAPS e emendas contra os portais oficiais ([detalhes](auditoria-amostral-modulos.md)) | ✅ Concluída com ressalvas (votações confirmadas; CEAPS com divergência em Carlos Viana; emendas NÃO VERIFICADO por URLs com erro) |
| P5 | Teste de proveniência: todo registro de pessoa carrega `fonte_url` específica + `coletado_em`; CI falha em URL genérica (home do sistema) | ⏳ |
| P6 | Exibir "dados coletados em DD/MM/AAAA" nas seções da ficha | ⏳ |
| P7 | Corrigir STATE.md §5 e code-health.md após P1–P3 | ⏳ |

Critério de encerramento: `build_congresso_2026.py` e `PRESIDENCIA_DATA_2026` removidos, P5 ativo no CI e nenhum link de fonte genérico nos datasets do TSE.
