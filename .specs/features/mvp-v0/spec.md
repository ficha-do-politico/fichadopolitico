# MVP v0 — Votações Importantes por Deputado Federal (Câmara)

## Declaração do Problema

Cidadãos brasileiros que querem saber como seu deputado federal votou em decisões de relevância nacional (ex.: escala 6×1, PL do desmatamento, anistia/blindagem) hoje precisam seguir um caminho em várias etapas: matéria jornalística → descobrir número do PL/PEC → portal da Câmara → encontrar a votação → localizar o deputado → interpretar Sim/Não/Abstenção. Ferramentas existentes (Meu Congresso, Radar do Congresso, Vamos Cobrar Brasil) agregam bem dados parlamentares, mas permanecem orientadas a projetos ou sessões; nenhuma otimiza *"buscar deputado → ver como votou no que importou"* em segundos.

O MVP valida uma proposição mais estreita e diferenciada: **a maneira mais simples de descobrir como um deputado federal votou em um conjunto pequeno e transparentemente curado de decisões importantes** — sempre com links para fontes oficiais, nunca com interpretação política.

## Objetivos

- [ ] Um cidadão consegue encontrar um deputado pelo nome e ver seu voto (Sim/Não/Abstenção/Ausente/Orientação) em cada tema importante curado em menos de 30 segundos
- [ ] Cada linha de voto linka para as URLs oficiais da votação e da proposição na Câmara
- [ ] O catálogo curado, os critérios de seleção e o mapeamento para votos oficiais são públicos no repositório
- [ ] O produto comunica claramente que exibe *votações importantes selecionadas*, não o histórico completo de votos

## Fora de Escopo

Explicitamente excluído no v0. Documentado para evitar creep de escopo.

| Funcionalidade | Motivo |
| -------------- | ------ |
| Histórico cronológico completo de votações | O MVP diferenciado é simplificação curada, não mais um navegador de votos (ver AD-001) |
| Gastos / CEAP (Portal da Transparência) | Adiado conforme issue #1; concorrentes já cobrem bem |
| Patrimônio / histórico eleitoral (TSE) | Adiado conforme issue #1 |
| Senado Federal | Adiado conforme issue #1; Layr sugere paridade depois (comentário na issue #1) |
| Busca/filtros avançados (partido, UF, explorador por tema) | v0 é busca por deputado primeiro; exploração vem depois |
| Contas de usuário, deputados salvos, alertas | Sem autenticação no v0 |
| Rótulos políticos, scores, alinhamento, rankings | Viola AD-004 |
| Detecção automatizada de "importância" via ML/notícias | Curadoria do v0 é manual e transparente (AD-003) |
| App mobile nativo | Web responsivo basta para validar o MVP |

---

## Premissas e Questões em Aberto

| Premissa / decisão | Default escolhido | Racional | Confirmado? |
| ------------------ | ----------------- | -------- | ----------- |
| Formato do catálogo curado | Arquivo versionado (YAML/JSON) no repo | Transparente, revisável em PRs, sem CMS no v0 | n |
| Temas seed iniciais | 4 da Layr + espaço para crescer até ~20 | Comentário na issue #1 + AD-007 | n |
| Deputado ausente de uma votação | Exibir `Ausente` ou `Não votou` conforme valor da API; nunca inferir | API oficial é fonte da verdade (AD-006) | s |
| Múltiplas votações por tema | Catálogo mapeia tema → lista ordenada de IDs de votação; UI mostra último voto decisivo ou todos (ver context.md) | Alguns temas abrangem várias votações | n |
| Stack / hospedagem | Indefinido (AD-008) | Fase de Design | n |
| Atualização de dados | Job periódico ou fetch sob demanda; limiar de stale a definir no Design | Dependência de API externa | n |
| Deputados fictícios/teste | Usar apenas IDs sintéticos; sem votos fabricados para pessoas reais | AGENTS.md §3.1 | s |

**Questões em aberto:**
1. **UI para múltiplas votações por tema** — mostrar só a mais recente vs. sublista completa? (Default no context.md: mostrar última decisiva + expandir para todas)
2. **Mínimo de temas curados para "lançamento"** — 4 (lista da Layr) ou 10? (Default: 4 funcionais + caminho documentado até 20)

Todas as outras dimensões resolvidas ou marcadas como N/A abaixo.

### Dimensões de requisitos implícitos (varredura Medium)

| Dimensão | Resolução |
| -------- | --------- |
| Validação de entrada e limites | Busca de deputado: trim de espaços, mín. 2 caracteres; sem injeção especial além dos limites da query da API |
| Falha / falha parcial | Se API da Câmara indisponível, exibir erro com retry; se uma votação faltar, mostrar tema como "dado indisponível" com horário da última sync — nunca omitir silenciosamente |
| Idempotência / retry / duplicatas | Refresh de ingestão/cache idempotente por `(deputado_id, votacao_id)` |
| Limites de auth e rate limit | Site público read-only; respeitar rate limits da API da Câmara via cache |
| Concorrência / ordenação | Ordem do catálogo curado = ordem de exibição; sort estável pelo campo `priority` |
| Ciclo de vida / expiração de dados | TTL de respostas cacheadas definido no Design; catálogo curado permanente até PR remover entrada |
| Observabilidade | Logar falhas de API e timestamps de sync; sem PII |
| Falha de dependência externa | API da Câmara fora → modo degradado com dados cacheados + banner visível de stale |
| Integridade de transição de estado | N/A — consumidor read-only de registros oficiais |

---

## User Stories

### P1: Votações importantes curadas na ficha do deputado ⭐ MVP

**User Story**: Como cidadão, quero buscar um deputado federal e ver imediatamente como ele votou em temas nacionais importantes (em linguagem simples), para entender seu histórico sem caçar números de PL.

**Por que P1**: Proposta de valor diferenciada central (AD-001); substitui a "lista de votos recentes" da issue #1.

**Critérios de Aceite**:

1. QUANDO um usuário busca um deputado pelo nome ENTÃO o sistema DEVERÁ retornar deputados federais ativos correspondentes (nome, partido, UF, foto) da API da Câmara
2. QUANDO um usuário abre a ficha de um deputado ENTÃO o sistema DEVERÁ exibir uma seção intitulada equivalente a "Como votou em temas relevantes" listando cada tema curado com o voto do deputado (Sim/Não/Abstenção/Ausente/Orientação conforme retornado pela API)
3. QUANDO um voto é exibido ENTÃO o sistema DEVERÁ mostrar o título legível do tema, identificador oficial da proposição (ex.: PEC 221/2019), data da votação e links clicáveis para a página oficial da votação e da proposição na Câmara
4. QUANDO um tema curado não tem registro de voto correspondente para o deputado ENTÃO o sistema DEVERÁ exibir a verdade da API (ex.: Ausente) ou "sem registro nesta votação" — nunca inventar um voto
5. QUANDO o catálogo curado é renderizado ENTÃO o sistema DEVERÁ incluir nota visível de que os temas são *selecionados por relevância pública* com link para os critérios de seleção públicos (AD-003)

**Teste Independente**: Popular catálogo com um tema (ex.: "Fim da escala 6×1" mapeado para um ID de votação real); abrir ficha de um deputado conhecido; verificar que o voto bate com a API `/votacoes/{id}/votos` da Câmara e que os links de fonte resolvem.

**IDs de Requisito**: MVP-01, MVP-02, MVP-03, MVP-04, MVP-05

---

### P1: Catálogo público de votações curadas ⭐ MVP

**User Story**: Como contribuidor, quero que a lista de "temas importantes" e seu mapeamento para votos oficiais fique no repositório com critérios documentados, para que a curadoria seja transparente e revisável.

**Por que P1**: A camada editorial *é* o moat do produto; deve ir no MVP, não como afterthought (AD-002, AD-003).

**Critérios de Aceite**:

1. QUANDO o repositório é clonado ENTÃO um arquivo de catálogo curado DEVERÁ existir documentando por tema: `id`, `title`, `short_description`, `tags`, `proposicao_ref`, `votacao_ids[]`, `source_urls[]`, `added_date`, `criteria_note`
2. QUANDO um novo tema é adicionado ENTÃO o PR DEVERÁ incluir as URLs oficiais da Câmara usadas para verificar o mapeamento
3. QUANDO o catálogo é lido pela aplicação ENTÃO os temas DEVERÃO renderizar em ordem estável de `priority`
4. QUANDO existirem menos de 4 temas ENTÃO o sistema DEVERÁ continuar funcionando — tamanho do catálogo não é bloqueador em runtime

**Teste Independente**: Adicionar tema dummy com ID de votação inválido; ingestão/validação falha ruidosamente em dev; tema válido carrega na ficha do deputado.

**IDs de Requisito**: MVP-06, MVP-07, MVP-08, MVP-09

---

### P1: Rastreabilidade de fonte oficial ⭐ MVP

**User Story**: Como leitor cético, quero que todo voto exibido link de volta ao registro oficial da Câmara, para que eu possa verificar a afirmação sozinho.

**Por que P1**: Pilar inegociável do projeto (AD-006, AGENTS.md §3.1).

**Critérios de Aceite**:

1. QUANDO qualquer voto é exibido ENTÃO o sistema DEVERÁ renderizar ao menos um link para a URL oficial da votação na Câmara construída a partir dos dados da API ou URL documentada no catálogo
2. QUANDO campos de identidade do deputado (nome, partido, UF, foto) são exibidos ENTÃO o sistema DEVERÁ linkar para a URL oficial do perfil do deputado na Câmara (`/deputados/{id}`)
3. QUANDO links de fonte são renderizados ENTÃO o sistema NÃO DEVERÁ usar agregadores não oficiais como fonte primária — notícias/redes sociais só podem aparecer em `criteria_note` do catálogo como contexto secundário, rotulado como não oficial

**Teste Independente**: Clicar em todo link de fonte na ficha; cada um resolve para `camara.leg.br` ou `dadosabertos.camara.leg.br`.

**IDs de Requisito**: MVP-10, MVP-11, MVP-12

---

### P2: Navegação pela lista de deputados

**User Story**: Como cidadão sem um deputado específico em mente, quero navegar pela lista de deputados federais atuais, para descobrir fichas a partir da lista.

**Por que P2**: Listado nos critérios de aceite da issue #1; suporta descoberta, mas busca-first é o fluxo hero.

**Critérios de Aceite**:

1. QUANDO um usuário abre o índice de deputados ENTÃO o sistema DEVERÁ listar deputados federais atuais com nome, partido, UF e thumbnail de foto da API da Câmara
2. QUANDO um usuário clica em um deputado na lista ENTÃO o sistema DEVERÁ navegar para a ficha do deputado (P1)

**Teste Independente**: Lista carrega 513± deputados; clicar em qualquer um leva à ficha com seção de votos curados.

**IDs de Requisito**: MVP-13, MVP-14

---

### P2: Página de documentação dos critérios de seleção

**User Story**: Como cidadão, quero ler como e por que votações foram selecionadas como "importantes", para julgar a camada editorial de forma justa.

**Por que P2**: Necessário para o modelo de confiança do AD-003; pode ir como página markdown no v0.

**Critérios de Aceite**:

1. QUANDO um usuário segue o link "critérios de seleção" ENTÃO o sistema DEVERÁ exibir critérios documentados (ex.: cobertura na mídia nacional, debate público amplo, impacto direto em política — texto exato aprovado pelo time)
2. QUANDO os critérios são exibidos ENTÃO o sistema DEVERÁ declarar que o catálogo é incompleto e convidar issues/PRs para adições

**Teste Independente**: Link da ficha do deputado abre doc de critérios; conteúdo bate com `docs/criterios-selecao.md` do repo ou equivalente.

**IDs de Requisito**: MVP-15, MVP-16

---

### P3: Exportar resumo de votos do deputado

**User Story**: Como jornalista ou militante, quero exportar o resumo de votos curados de um deputado, para reutilizar dados verificados com atribuição.

**Por que P3**: Meu Congresso oferece export; paridade desejável mas não necessária para validar a UX central.

**Critérios de Aceite**:

1. QUANDO um usuário clica em exportar na ficha do deputado ENTÃO o sistema DEVERÁ baixar CSV ou JSON contendo tema, voto, data e URLs oficiais de fonte

**IDs de Requisito**: MVP-17

---

## Casos Limite

- QUANDO a API da Câmara retorna HTTP 5xx ou timeout ENTÃO o sistema DEVERÁ exibir erro visível ao usuário e NÃO DEVERÁ exibir votos stale sem indicador de desatualização
- QUANDO um deputado não é encontrado ENTÃO o sistema DEVERÁ mostrar "nenhum deputado encontrado" com sugestão de verificar a grafia
- QUANDO a busca retorna homônimos ENTÃO o sistema DEVERÁ desambiguar com partido + UF
- QUANDO um ID de votação no catálogo não existe mais na API ENTÃO o sistema DEVERÁ marcar a entrada do catálogo como quebrada em admin/logs e mostrar "dado indisponível" na UI para aquele tema
- QUANDO a API retorna tipo de voto fora de Sim/Não/Abstenção/Ausente (ex.: Obstrução, Art. 17) ENTÃO o sistema DEVERÁ exibir o rótulo oficial verbatim, sem traduzir para Sim/Não
- QUANDO o catálogo curado está vazio ENTÃO o sistema DEVERÁ mostrar ficha do deputado com empty state explicando que o catálogo está sendo construído — não crashar

---

## Rastreabilidade de Requisitos

| ID de Requisito | Story | Fase | Status |
| --------------- | ----- | ---- | ------ |
| MVP-01 | P1: Votos curados na ficha | Design | Pendente |
| MVP-02 | P1: Votos curados na ficha | Design | Pendente |
| MVP-03 | P1: Votos curados na ficha | Design | Pendente |
| MVP-04 | P1: Votos curados na ficha | Design | Pendente |
| MVP-05 | P1: Votos curados na ficha | Design | Pendente |
| MVP-06 | P1: Catálogo público | Design | Pendente |
| MVP-07 | P1: Catálogo público | Design | Pendente |
| MVP-08 | P1: Catálogo público | Design | Pendente |
| MVP-09 | P1: Catálogo público | Design | Pendente |
| MVP-10 | P1: Rastreabilidade de fonte | Design | Pendente |
| MVP-11 | P1: Rastreabilidade de fonte | Design | Pendente |
| MVP-12 | P1: Rastreabilidade de fonte | Design | Pendente |
| MVP-13 | P2: Lista de deputados | Design | Pendente |
| MVP-14 | P2: Lista de deputados | Design | Pendente |
| MVP-15 | P2: Doc de critérios | Design | Pendente |
| MVP-16 | P2: Doc de critérios | Design | Pendente |
| MVP-17 | P3: Export | - | Pendente |

**Cobertura**: 17 total, 0 mapeados para tasks, 17 não mapeados ⚠️ (esperado pré-Design)

---

## Critérios de Sucesso

- [ ] Um usuário de primeira viagem consegue responder "como o deputado X votou na 6×1?" com uma busca + um clique, sem abas externas
- [ ] 100% dos votos exibidos numa ficha têm links oficiais funcionando (spot-check manual de 5 deputados × todos os temas seed)
- [ ] Time concorda que o seed do catálogo curado (≥4 temas) mapeia corretamente para a API da Câmara antes do demo público
- [ ] README/issue #1 atualizados para refletir o enquadramento refinado do MVP após aprovação da spec

---

## Relação com Issues do GitHub

| Issue | Relação |
| ----- | ------- |
| [#1 MVP v0](https://github.com/ficha-do-politico/fichadopolitico/issues/1) | Esta spec **refina** a issue #1: substitui "votações recentes" por "temas relevantes curados"; mantém lista de deputados, ficha, links oficiais, fonte só Câmara |
| [#2 API discovery](https://github.com/ficha-do-politico/fichadopolitico/issues/2) | Pré-requisito para mapear entradas do catálogo para `votacao_ids` reais; ver `features/api-discovery/spec.md` |

## Posicionamento Competitivo (referência)

| Projeto | Votos fáceis | Ficha completa | Temas importantes | UX cidadão |
| ------- | ------------ | -------------- | ----------------- | ---------- |
| Meu Congresso | Forte | Médio | Médio | Bom |
| Radar do Congresso | Forte | Excelente | Bom | Bom |
| Vamos Cobrar Brasil | Forte | Excelente | Bom | Muito bom |
| **Ficha do Político (v0)** | **Meta: Forte** | **Adiado** | **Foco principal** | **Foco principal** |

Ver também `referencias.md` para referências open source e de dados oficiais.
