# Referências — projetos de political tech no Brasil

> **Nota:** Este documento cataloga exclusivamente iniciativas cívicas, projetos de terceiros (open source ou fechados) e referências metodológicas. Para o catálogo de APIs e bases governamentais primárias do Estado brasileiro (Câmara, Senado, TSE, CGU, TCU, etc.), consulte [fontes-oficiais-de-dados.md](fontes-oficiais-de-dados.md).

## Projetos open source e dados abertos

### Puxa Ficha
- **O que é:** plataforma cívica de transparência eleitoral (Eleições 2026) com fichas de candidatos ao Executivo (Presidência e Governos Estaduais), comparador lado a lado e análise de planos de governo.
- **Site:** [puxaficha.com.br](https://puxaficha.com.br/)
- **Repo:** [github.com/thiago-salvador/puxa-ficha](https://github.com/thiago-salvador/puxa-ficha)
- **Status:** ativo e em produção (Eleições 2026). Licença Apache 2.0.
- **Relevância pra nós:** principal referência viva de civic tech no ciclo de 2026. Benchmark valioso de UX para comparador e normalização de dados eleitorais do TSE.

### Base dos Dados
- **O que é:** organização sem fins lucrativos que limpa, integra e disponibiliza bases públicas brasileiras via BigQuery e pacotes em Python/R.
- **Site:** [basedosdados.org](https://basedosdados.org/)
- **Repo:** [github.com/basedosdados](https://github.com/basedosdados)
- **Status:** ativo e mantido continuamente.
- **Relevância pra nós:** referência analítica para validação cruzada de dados do TSE (bens e candidaturas) e da Câmara dos Deputados (gastos e proposições).

### Querido Diário (OKBR)
- **O que é:** coleta e indexação de diários oficiais municipais para busca de atos do Executivo local.
- **Site:** [queridodiario.ok.org.br](https://queridodiario.ok.org.br/)
- **Repo:** [github.com/okfn-brasil/querido-diario](https://github.com/okfn-brasil/querido-diario)
- **Status:** ativo, comunidade aberta e mantido pela Open Knowledge Brasil. Reconhecido como Digital Public Good.
- **Relevância pra nós:** principal referência em governança comunitária aberta (`CONTRIBUTING.md`, sprints cívicos). Conector natural para atos municipais caso a Ficha venha a cobrir o Executivo local.

### Operação Serenata de Amor (OKBR)
- **O que é:** fiscalização de despesas da cota parlamentar (CEAP) de deputados federais via regras e aprendizado de máquina (bot Rosie).
- **Repo:** [github.com/okfn-brasil/serenata-de-amor](https://github.com/okfn-brasil/serenata-de-amor)
- **Status:** inativo / hibernando.
- **Relevância pra nós:** referência técnica histórica de como tratar e auditar a cota parlamentar da Câmara dos Deputados.

### Perfil Político (OKBR)
- **O que é:** plataforma para comparar histórico de candidatos (idade, escolaridade, ocupação, histórico partidário e patrimônio declarado).
- **Repo:** [github.com/okfn-brasil/perfil-politico](https://github.com/okfn-brasil/perfil-politico)
- **Status:** inativo (sem updates recentes desde ~2021).
- **Relevância pra nós:** referência conceitual de modelagem de dados para agregação de patrimônio e histórico eleitoral.

## Metodologia e Indicadores

### Índice Legisla (Legisla Brasil / Voto Consciente)
- **O que é:** índice de avaliação do mandato de parlamentares com 17 indicadores em 4 eixos (produção legislativa, mobilização, fiscalização e alinhamento partidário).
- **Site:** [legislabrasil.org](https://legislabrasil.org/)
- **Status:** ativo (metodologia fechada, sem repositório aberto).
- **Relevância pra nós:** referência metodológica para métricas quantitativas de atuação legislativa.

## Produtos Fechados (Referência de UX)

### Radar do Congresso (Congresso em Foco)
- **O que é:** ferramenta jornalística com perfil individual de parlamentares, integrando votações e uso de cota.
- **Site:** [radar.congressoemfoco.com.br](https://radar.congressoemfoco.com.br/)
- **Status:** ativo (produto fechado).
- **Relevância pra nós:** referência de interface unificada para visualizar votos e gastos no mesmo perfil de parlamentar.

---

## Posicionamento da Ficha do Político
O ecossistema divide-se entre ferramentas eleitorais sazonais (Puxa Ficha), dados municipais (Querido Diário) ou projetos legados de cota (Serenata). A **Ficha do Político** atua na **auditoria contínua e permanente do mandato federal (Câmara e Senado)**, combinando votações nominais e notas fiscais de cota (CEAP/CEAPS), com neutralidade estrita (dados brutos oficiais, sem scores editoriais) e arquitetura estática (Astro SSG) de custo perpétuo zero.

Para os endpoints, formatos e especificações técnicas de extração das fontes governamentais primárias (Câmara, Senado, TSE, CGU, TCU, CNJ), consulte [fontes-oficiais-de-dados.md](fontes-oficiais-de-dados.md).
