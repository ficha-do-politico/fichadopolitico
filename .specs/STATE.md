# STATE

## Decisions

### AD-001

- **Decisão**: O MVP v0 foca em *votações importantes curadas* por deputado, não em um dump cronológico de votações nominais recentes.
- **Motivo**: A análise competitiva (Meu Congresso, Radar do Congresso, Vamos Cobrar Brasil) já agrega dados parlamentares; a lacuna é o acesso amigável ao cidadão sobre *decisões que importaram*, sem precisar saber o número do PL/PEC antes.
- **Trade-off**: Exige uma camada editorial explícita e curadoria contínua; não pode ser totalmente automatizado no primeiro dia.
- **Escopo**: Definição de produto do MVP v0, UX e catálogo de votações curadas.
- **Data**: 2026-08-18
- **Status**: ativo — substitui o enquadramento da issue #1 no GitHub ("votações nominais mais recentes"), mantendo a mesma fonte de dados e os princípios apartidários.



### AD-002

- **Decisão**: Arquitetura em três camadas — (1) dados oficiais da API da Câmara, (2) catálogo de "temas importantes" curados com critérios transparentes, (3) UX de ficha do deputado voltada ao cidadão.
- **Motivo**: Separa fatos oficiais inegociáveis da seleção editorial; mantém verificabilidade enquanto permite simplificação.
- **Trade-off**: A camada 2 é mantida manualmente em YAML/JSON (ou equivalente) até existir um CMS.
- **Escopo**: Todas as funcionalidades do MVP v0 que exibem votos.
- **Data**: 2026-08-18
- **Status**: ativo



### AD-003

- **Decisão**: A curadoria editorial é explícita, pública e documentada em critérios — nunca disfarçada de neutralidade algorítmica.
- **Motivo**: "Quais votações são importantes?" é o problema difícil do produto; esconder a curadoria corrói a confiança quando o usuário discorda da inclusão.
- **Trade-off**: Expõe o projeto a debate sobre viés de seleção; mitigado publicando critérios e links de fonte por item.
- **Escopo**: Catálogo de votações curadas, README/docs, futuras diretrizes de contribuição.
- **Data**: 2026-08-18
- **Status**: ativo



### AD-004

- **Decisão**: Sem rotulação política, pontuação ou julgamentos de valor sobre deputados (ex.: "progressista", "alinhamento", "bom/mau").
- **Motivo**: Princípio apartidário central do README e AGENTS.md; a diferenciação é *acesso*, não *interpretação*.
- **Trade-off**: Menos "engajamento" que recursos de comparação/alinhamento vistos no Meu Congresso.
- **Escopo**: Todo texto voltado ao usuário, campos do modelo de dados e analytics futuros.
- **Data**: 2026-08-18
- **Status**: ativo



### AD-005

- **Decisão**: A fonte de dados do MVP v0 é exclusivamente a API Dados Abertos da Câmara (`dadosabertos.camara.leg.br`) — endpoints `/deputados`, `/votacoes`, `/votacoes/{id}/votos`, mais links de proposição conforme retornados pela API.
- **Motivo**: Escopo da issue #1, discovery da issue #2 em andamento (Layr); fonte única reduz risco de integração no v0.
- **Trade-off**: Senado, gastos e patrimônio ficam para depois, apesar da visão de longo prazo no README.
- **Escopo**: Ingestão e exibição do MVP v0.
- **Data**: 2026-08-18
- **Status**: ativo



### AD-006

- **Decisão**: Todo fato político exibido (voto, campo de identidade do deputado vindo da API) DEVERÁ linkar para a URL oficial de origem.
- **Motivo**: Pilar inegociável do projeto ("Nosso compromisso é com a verdade"); AGENTS.md §3.1.
- **Trade-off**: A UI deve sempre exibir links de fonte, mesmo quando isso aumenta a densidade visual.
- **Escopo**: Todas as funcionalidades que exibem dados de deputado ou voto.
- **Data**: 2026-08-18
- **Status**: ativo



### AD-007

- **Decisão**: O catálogo curado inicial começa com 4–10 temas propostos pelo time (comentário da Layr na issue #1) e cresce em direção a 20–50 — sem cobertura exaustiva do Congresso.
- **Motivo**: Valida o formato antes da curadoria escalar; alinha com a restrição de "MVP simples".
- **Trade-off**: Cobertura incompleta até o catálogo crescer; deve comunicar "temas selecionados", não "todos os votos".
- **Escopo**: Seed do catálogo de votações curadas e copy de UX.
- **Data**: 2026-08-18
- **Status**: ativo



### AD-008

- **Decisão**: Stack permanece indefinida até a fase de Design; specs são agnósticas de stack.
- **Motivo**: README e AGENTS.md adiam explicitamente a escolha de framework; issue #2 foca primeiro nos contratos de API.
- **Trade-off**: Design/tasks ainda não podem assumir Next.js, Python, etc.
- **Escopo**: Projeto inteiro até o primeiro AD ser substituído após escolha de stack.
- **Data**: 2026-08-18
- **Status**: ativo



### AD-009

- **Decisão**: A ficha pública do MVP v0 NÃO exibe CPF nem outros dados sensíveis retornados pela API (ex.: email, telefone de gabinete), mesmo quando disponíveis no payload ou em artefatos de discovery.
- **Motivo**: PR #4 (`discovery/deputies-data`) gera markdowns com CPF para exploração; o produto cidadão deve expor apenas identificação política mínima (nome, partido, UF, foto) + votos com fonte.
- **Trade-off**: Descarta campos que a API oferece e que concorrentes às vezes exibem; reduz risco de LGPD e superfície de abuso.
- **Escopo**: MVP v0 UI, seeds/fixtures, scripts de exportação pública.
- **Data**: 2026-08-18
- **Status**: ativo



### AD-011

- **Decisão**: O escopo do projeto é estritamente delimitado ao Poder Legislativo Federal (Câmara dos Deputados no v0 e Senado Federal no v1), excluindo permanentemente os âmbitos municipal (Vereadores/Prefeitos) e estadual (Deputados Estaduais/Governadores).
- **Motivo**: Ausência de infraestrutura nacional unificada de dados abertos nos 5.570 municípios e 27 estados. O esforço técnico para construir e manter milhares de scrapers para portais municipais/estaduais heterogêneos inviabilizaria o projeto e comprometeria os pilares de verificabilidade e fonte oficial. O Congresso Nacional é a única esfera com APIs REST públicas padronizadas e mantidas centralmente pelo Estado.
- **Trade-off**: Deixa de atender demandas locais de usuários por vereadores de suas cidades ou deputados estaduais.
- **Escopo**: Modelo de dados, roadmap do produto e arquitetura de ingestão.
- **Data**: 2026-09-12
- **Status**: ativo



### AD-012

- **Decisão**: A stack de frontend do MVP v0 adotará **Astro SSG** (Static Site Generation) com Tailwind CSS, pré-renderizando 513 páginas estáticas individuais de deputados federais e a página de busca principal.
- **Motivo**: Astro gera HTML puro sem runtime JavaScript pesado no cliente, garantindo carregamento instantâneo em conexões mobile (3G/4G), pontuação máxima de performance no Lighthouse e suporte nativo a tags `<meta property="og:...">` pré-renderizadas para cada deputado (essencial para cards formatados com foto no WhatsApp e redes sociais). Além disso, exporta arquivos estáticos (`dist/`) compatíveis com qualquer hospedagem gratuita (Cloudflare Pages, Vercel ou GitHub Pages).
- **Trade-off**: A geração estática exige um rebuild/deploy sempre que novos temas forem adicionados ao catálogo; perfeitamente aceitável dado o ciclo editorial quinzenal/mensal de curadoria.
- **Escopo**: Aplicação web do MVP v0 (`site/`).
- **Data**: 2026-09-12
- **Status**: ativo



## Handoff

- **Feature**: Frontend & Pipeline de Dados do MVP v0
- **Fase / Task**: Plan & Implementation
- **Concluído**: 
  - Discovery de dados concluído e mergeado na `main` (PR #8).
  - 513 deputados federais catalogados em `dados/deputados/`.
  - 5 votações nominais completas extraídas em `dados/votacoes/`.
  - Requisitos formais mapeados em `.specs/features/mvp-v0/spec.md`.
  - Plano técnico de arquitetura e implementação documentado em `.specs/features/mvp-v0/plan.md`.
  - Decisão AD-012 aprovada (Astro SSG + Tailwind CSS).
- **Em progresso**: Implementação do script de consolidação de dados (`scripts/build_site_data.py`) e scaffold do site Astro.
- **Próximo passo**: Executar Tasks 1 a 5 do `plan.md` sob aprovação do time.
- **Bloqueios**: Nenhum.
- **Branch**: `main`
