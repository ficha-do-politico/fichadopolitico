# API Discovery — Contratos de Dados da Câmara e do Senado

## Declaração do Problema

Antes de construir o catálogo de votações curadas do MVP e o pipeline de ingestão, o time precisa de conhecimento verificado sobre o que as APIs oficiais retornam: formatos de campos, paginação, rate limits, ligação proposição↔votação e enums de rótulos de voto. A issue #2 no GitHub rastreia esse trabalho; a Layr começou pelos endpoints `/deputados` da Câmara ([PR #4](https://github.com/ficha-do-politico/fichadopolitico/pull/4), branch `discovery/deputies-data`). Sem o output do discovery de **votações**, entradas do catálogo curado ainda não podem ser mapeadas para `votacao_ids` reais com confiança.

## Progresso Atual (2026-08-18)

| Entregável | Status | Onde |
| ---------- | ------ | ---- |
| DISC-01..03 (`/deputados`) | **Em progresso** — PR #4 aberta | `scripts/fetch_deputados.py`, `dados/deputados/{id}.md`, `discovery/deputados_ordem_ASC_ordenarPor_nome.json` |
| DISC-04..07 (`/votacoes`) | Pendente | — |
| DISC-08..09 (limites/cache) | Pendente | PR #4 usa `--delay` no script; falta documentar formalmente |
| DISC-10 (Senado) | Pendente | — |

**Nota:** Os markdowns do PR #4 incluem CPF e outros campos sensíveis para exploração. O MVP v0 **não** exibirá esses campos (AD-009).

## Objetivos

- [ ] Notas documentadas e reproduzíveis sobre endpoints da Câmara Dados Abertos necessários para o MVP v0
- [ ] Pelo menos um exemplo end-to-end funcionando: tema → proposição → votação → voto por deputado, com URLs
- [ ] Lacunas/limitações conhecidas escritas (Senado adiado mas explorado levemente para o futuro)

## Fora de Escopo

| Funcionalidade | Motivo |
| -------------- | ------ |
| Código de ingestão em produção | Apenas discovery; implementação pertence ao Design/Execute do mvp-v0 |
| TSE / Portal da Transparência | Não é fonte do MVP v0 (AD-005) |
| Integração completa com Senado | Anotado para o futuro; não bloqueia v0 se o caminho da Câmara estiver claro |

---

## Premissas e Questões em Aberto

| Premissa / decisão | Default escolhido | Racional | Confirmado? |
| ------------------ | ----------------- | -------- | ----------- |
| Localização do doc principal | `docs/api/camara.md` (ou `.specs/features/api-discovery/findings.md`); artefatos interim do PR #4 em `scripts/` + `dados/deputados/` | Descobrível por implementadores; PR #4 já gera exemplos reais | n |
| Referência Swagger | https://dadosabertos.camara.leg.br/swagger/api.html (conforme Layr, issue #2) | Já em uso | s |
| Exploração do Senado | Seção breve nos findings; sem entregável bloqueante | Título da issue #2 menciona Senado; MVP é só Câmara | n |

**Questões em aberto:** nenhuma bloqueando a spec — profundidade do Senado é P3.

Dimensões de requisitos implícitos restantes: N/A para esta feature de pesquisa.

---

## User Stories

### P1: Documentação do endpoint deputados da Câmara ⭐ MVP

**User Story**: Como desenvolvedor, quero formatos de resposta documentados para `/deputados` e `/deputados/{id}`, para construir lista de deputados e cabeçalhos de ficha sem chute.

**Por que P1**: PR da Layr em andamento depende disso; listado primeiro nos comentários da issue #2.

**Critérios de Aceite**:

1. QUANDO o doc de discovery é lido ENTÃO um desenvolvedor DEVERÁ encontrar exemplo de request/response para `/deputados` (lista) e `/deputados/{id}` (detalhe) incluindo campos usados pelo MVP: `id`, `nome`, `siglaPartido`, `siglaUf`, `urlFoto`, `urlWebsite` ou padrão de URL oficial do perfil
2. QUANDO existe paginação ENTÃO o doc DEVERÁ descrever parâmetros de página e contagens típicas de resultado
3. QUANDO o doc é commitado ENTÃO cada exemplo DEVERÁ incluir a URL exata consultada e a data de verificação

**Teste Independente**: Outro dev consegue fazer curl nas URLs documentadas e bater os campos.

**IDs de Requisito**: DISC-01, DISC-02, DISC-03

---

### P1: Ligação votações + votos da Câmara ⭐ MVP

**User Story**: Como desenvolvedor, quero saber como ir de uma proposição para IDs de votação e depois para o voto de cada deputado, para popular o catálogo curado.

**Por que P1**: Bloqueia MVP-06..MVP-09 (mapeamento do catálogo).

**Critérios de Aceite**:

1. QUANDO o doc de discovery é lido ENTÃO um desenvolvedor DEVERÁ encontrar o fluxo: identificador da proposição → query `/votacoes?*` → `/votacoes/{id}` → `/votacoes/{id}/votos`
2. QUANDO tipos de voto são retornados ENTÃO o doc DEVERÁ listar todos os valores observados de `tipoVoto` (ou equivalente) com significados oficiais
3. QUANDO um tema seed (ex.: 6×1) é rastreado ENTÃO o doc DEVERÁ incluir exemplo completo funcionando com IDs reais e URLs HTML oficiais de votação e proposição
4. QUANDO existem ambiguidades (múltiplas votações por proposição) ENTÃO o doc DEVERÁ descrever heurísticas de seleção para "votação plenária decisiva"

**Teste Independente**: Seguir o exemplo funcionando; voto de um deputado conhecido bate com o site da Câmara.

**IDs de Requisito**: DISC-04, DISC-05, DISC-06, DISC-07

---

### P2: Notas de rate limits, erros e cache

**User Story**: Como desenvolvedor, quero limites conhecidos da API e modos de falha documentados, para que o Design escolha cache de forma responsável.

**Critérios de Aceite**:

1. QUANDO o doc de discovery cobre operações ENTÃO DEVERÁ anotar comportamento observado de rate limit (429, headers) ou declarar "nenhum observado" com método de teste
2. QUANDO erros comuns ocorrem ENTÃO o doc DEVERÁ listar códigos HTTP e comportamento recomendado do client

**IDs de Requisito**: DISC-08, DISC-09

---

### P3: Reconhecimento Dados Abertos do Senado

**User Story**: Como desenvolvedor planejando v1, quero um esboço curto da API do Senado, para estimar esforço de paridade Câmara/Senado.

**Critérios de Aceite**:

1. QUANDO o doc de discovery é lido ENTÃO uma seção Senado DEVERÁ listar endpoints análogos (ou documentar ausência) comparados à Câmara

**IDs de Requisito**: DISC-10

---

## Casos Limite

- QUANDO o schema da API difere do Swagger ENTÃO o doc DEVERÁ anotar o delta com exemplo
- QUANDO uma proposição tem zero votações nominais ENTÃO o doc DEVERÁ dizer isso com exemplo e impacto no catálogo

---

## Rastreabilidade de Requisitos

| ID de Requisito | Story | Fase | Status |
| --------------- | ----- | ---- | ------ |
| DISC-01 | P1: Deputados | Execute | Em progresso (PR #4) |
| DISC-02 | P1: Deputados | Execute | Em progresso (PR #4) |
| DISC-03 | P1: Deputados | Execute | Em progresso (PR #4) |
| DISC-04 | P1: Votações | Execute | Pendente |
| DISC-05 | P1: Votações | Execute | Pendente |
| DISC-06 | P1: Votações | Execute | Pendente |
| DISC-07 | P1: Votações | Execute | Pendente |
| DISC-08 | P2: Limites | Execute | Pendente |
| DISC-09 | P2: Limites | Execute | Pendente |
| DISC-10 | P3: Senado | - | Pendente |

---

## Critérios de Sucesso

- [ ] Seed do catálogo curado pode ser preenchido com `votacao_ids` reais para ≥4 temas usando apenas o doc de discovery
- [ ] Issue #2 pode ser fechada ou atualizada com link para os findings
- [ ] Sem campos de API fabricados na documentação — todos os exemplos de respostas reais

---

## Relação com Issues do GitHub

| Issue | Relação |
| ----- | ------- |
| [#2 Discovery](https://github.com/ficha-do-politico/fichadopolitico/issues/2) | Alvo direto de implementação desta spec |
| [#1 MVP v0](https://github.com/ficha-do-politico/fichadopolitico/issues/1) | Consumidor do output do discovery |
| [PR #4](https://github.com/ficha-do-politico/fichadopolitico/pull/4) | Implementação parcial de DISC-01..03; falta merge e discovery de votações |

**Nota da issue #2:** Layr reportou uso de `/deputados` e `/deputados/{ID}`; entregou script + 513 fichas markdown (18/08). Senado e endpoints `/votacoes` ainda pendentes.
