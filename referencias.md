# Referências — projetos de political tech no Brasil

> **Nota:** Este documento cataloga exclusivamente iniciativas cívicas, projetos de terceiros (open source ou fechados) e referências metodológicas. Para o catálogo de APIs e bases governamentais primárias do Estado brasileiro (Câmara, Senado, TSE, CGU, TCU, etc.), consulte [fontes-oficiais-de-dados.md](fontes-oficiais-de-dados.md).

## Projetos open source (código pra estudar)

### Puxa Ficha
- **O que é:** plataforma cívica de transparência eleitoral para as Eleições 2026 com fichas de candidatos majoritários do Executivo (Presidência da República e Governos Estaduais), vices, pesquisas de intenção de voto agregadas, comparador lado a lado e análise de planos de governo.
- **Site:** [puxaficha.com.br](https://puxaficha.com.br/)
- **Repo:** [github.com/thiago-salvador/puxa-ficha](https://github.com/thiago-salvador/puxa-ficha)
- **Status:** ativo e em produção (Eleições 2026).
- **Mantenedor:** Thiago Salvador.
- **Licença:** Apache 2.0.
- **Stack:** Next.js 15, TypeScript, Tailwind CSS, Supabase.
- **Relevância pra nós:** principal referência viva e ativa de civic tech no ciclo de 2026. Benchmark valioso de UX para o comparador de candidatos, normalização de chapas majoritárias e auditoria de integridade do TSE (documentou e corrigiu duplicidades na leitura do pacote `bem_candidato_2026`). Diferencia-se por ser uma plataforma centrada na corrida eleitoral executiva (com quiz de afinidade), enquanto a Ficha do Político é focada na auditoria permanente de mandatos legislativos (votações nominais e notas fiscais de cota CEAP/CEAPS da Câmara e Senado) sob estrita neutralidade e custo zero de infraestrutura.

### Operação Serenata de Amor
- **O que é:** fiscalização de gastos de deputados federais (CEAP) via IA — o bot "Rosie".
- **Repo:** [github.com/okfn-brasil/serenata-de-amor](https://github.com/okfn-brasil/serenata-de-amor)
- **Status:** inativo/hibernando — o próprio repo avisa "não recebe updates frequentes".
- **Mantenedor:** Open Knowledge Brasil (OKBR).
- **Relevância pra nós:** referência técnica de como puxar dados de gasto parlamentar; ninguém mantém ativamente, então não dá pra contar com resposta de contribuição, só estudar o código.

### Querido Diário
- **O que é:** coleta e indexa diários oficiais municipais (leis, atos).
- **Repo:** [github.com/okfn-brasil/querido-diario](https://github.com/okfn-brasil/querido-diario)
- **Status:** ativo, comunidade viva (Discord, `CONTRIBUTING.md`, sprints de inovação cívica). Reconhecido como Digital Public Good.
- **Mantenedor:** Open Knowledge Brasil.
- **Relevância pra nós:** não é o mesmo escopo (diário oficial ≠ ficha de político), mas é o único dos projetos daqui com processo de contribuição aberto de verdade — bom lugar pra aprender a stack de scraping de dado público brasileiro.

### Perfil Político (OKBR)
- **O que é:** plataforma pra comparar histórico de candidatos — idade, sexo, escolaridade, ocupação, histórico partidário e patrimônio declarado.
- **Repo:** [github.com/okfn-brasil/perfil-politico](https://github.com/okfn-brasil/perfil-politico)
- **Arquitetura:** [post detalhado](https://joaoarthurbm.github.io/arqsoft-blog/posts/perfil-politico/) (2021).
- **Status:** projeto pequeno, ~4 anos atrás, sem sinal de atividade recente.
- **Mantenedor:** Open Knowledge Brasil.
- **Relevância pra nós:** é o mais parecido conceitualmente com a "ficha" que queremos. Vale pegar ideia do schema de campos (não o código) — está morto, então sem problema em se inspirar.

## Metodologia / o que medir (conteúdo, sem código)

### Voto Consciente
- **O que é:** ONG (SP, fundada 1987) de educação política — cursos, rankings, publicações.
- **Site:** votoconsciente.org.br
- **Status:** ativo, mas sem repositório/dataset público conhecido — é conteúdo/educação, não engenharia aberta.
- **Contato:** contato@votoconsciente.org.br
- **Relevância pra nós:** publica o Ranking Legisla (ver abaixo) em parceria; consulta pontual de metodologia, não parceria técnica.

### Legisla Brasil (o "Índice Legisla")
- **O que é:** índice de 17 indicadores em 4 eixos (produção legislativa, mobilização, fiscalização, alinhamento partidário).
- **Site:** legislabrasil.org
- **Status:** ativo, conteúdo corrente.
- **Mantenedor:** organização própria (Olívia Carneiro), parceria com Voto Consciente.
- **Relevância pra nós:** metodologia de indicadores é ótimo ponto de partida pro "o que colocar na ficha" — mas não é open source, sem porta de entrada pra contribuir com código.

## Produtos fechados (referência de UX/produto)

### Radar do Congresso (Congresso em Foco)
- **O que é:** ferramenta do Congresso em Foco (veículo de jornalismo político, grupo UOL) que gera perfil individual de parlamentar, incluindo gastos e acompanhamento de atividade legislativa.
- **Site:** [radar.congressoemfoco.com.br](https://radar.congressoemfoco.com.br/) (ex. de perfil indicado pelo Soutto: [radar.congressoemfoco.com.br/parlamentar/25894/perfil](https://radar.congressoemfoco.com.br/parlamentar/25894/perfil)).
- **Status:** ativo — porém não consegui confirmar detalhes de funcionamento por fetch automatizado (site é uma SPA); vale conferência manual do time antes de tirar conclusões mais profundas.
- **Mantenedor:** Congresso em Foco.
- **Relevância pra nós:** apontado pelo Soutto (17/08) como o produto mais próximo conceitualmente da ficha individual de parlamentar que queremos (múltiplas dimensões — voto, gasto — numa página só). É produto editorial fechado, sem repo/dataset público conhecido até onde verificamos — serve de referência de UX/produto, não de parceria técnica ou código.

---

## Síntese
No cenário de projetos abertos de political tech, o **Puxa Ficha** é hoje o projeto vivo mais avançado na esteira da disputa eleitoral executiva (Presidência, Governadores e pesquisas). No entanto, a **Ficha do Político** mantém um propósito único e complementar: a auditoria permanente e contínua do mandato de parlamentares federais (Câmara e Senado), combinando votações nominais curadas e notas fiscais de cota parlamentar (CEAP/CEAPS), com neutralidade estrita (sem scores ou quizzes) e arquitetura estática (Astro SSG) de custo zero perpétuo. Entre os projetos históricos, Serenata de Amor e Perfil Político servem para consulta de schemas e abordagens legadas, enquanto o Querido Diário é referência em comunidade ativa.

Para os endpoints, formatos e especificações técnicas de extração das fontes governamentais primárias (Câmara, Senado, TSE, CGU, TCU, CNJ), consulte [fontes-oficiais-de-dados.md](fontes-oficiais-de-dados.md).
