# Referências — projetos de political tech no Brasil

Levantamento inicial (a partir de indicações do Zé Gustavo e da Esther) do que já existe antes de desenhar o escopo do `fichadopolitico`. Ver também a issue #1 (MVP) e a nota de investigação original na conversa com o Antonio.

## Operação Serenata de Amor
- **O que é:** fiscalização de gastos de deputados federais (CEAP) via IA — o bot "Rosie".
- **Repo:** [github.com/okfn-brasil/serenata-de-amor](https://github.com/okfn-brasil/serenata-de-amor)
- **Status:** inativo/hibernando — o próprio repo avisa "não recebe updates frequentes".
- **Mantenedor:** Open Knowledge Brasil (OKBR).
- **Relevância pra nós:** referência técnica de como puxar dados de gasto parlamentar; ninguém mantém ativamente, então não dá pra contar com resposta de contribuição, só estudar o código.

## Querido Diário
- **O que é:** coleta e indexa diários oficiais municipais (leis, atos).
- **Repo:** [github.com/okfn-brasil/querido-diario](https://github.com/okfn-brasil/querido-diario)
- **Status:** ativo, comunidade viva (Discord, `CONTRIBUTING.md`, sprints de inovação cívica). Reconhecido como Digital Public Good.
- **Mantenedor:** Open Knowledge Brasil.
- **Relevância pra nós:** não é o mesmo escopo (diário oficial ≠ ficha de político), mas é o único dos projetos daqui com processo de contribuição aberto de verdade — bom lugar pra aprender a stack de scraping de dado público brasileiro.

## Perfil Político (OKBR)
- **O que é:** plataforma pra comparar histórico de candidatos — idade, sexo, escolaridade, ocupação, histórico partidário e patrimônio declarado.
- **Repo:** [github.com/okfn-brasil/perfil-politico](https://github.com/okfn-brasil/perfil-politico)
- **Arquitetura:** [post detalhado](https://joaoarthurbm.github.io/arqsoft-blog/posts/perfil-politico/) (2021).
- **Status:** projeto pequeno, ~4 anos atrás, sem sinal de atividade recente.
- **Mantenedor:** Open Knowledge Brasil.
- **Relevância pra nós:** é o mais parecido conceitualmente com a "ficha" que queremos. Vale pegar ideia do schema de campos (não o código) — está morto, então sem problema em se inspirar.

## Voto Consciente
- **O que é:** ONG (SP, fundada 1987) de educação política — cursos, rankings, publicações.
- **Site:** votoconsciente.org.br
- **Status:** ativo, mas sem repositório/dataset público conhecido — é conteúdo/educação, não engenharia aberta.
- **Contato:** contato@votoconsciente.org.br
- **Relevância pra nós:** publica o Ranking Legisla (ver abaixo) em parceria; consulta pontual de metodologia, não parceria técnica.

## Legisla Brasil (o "Índice Legisla")
- **O que é:** índice de 17 indicadores em 4 eixos (produção legislativa, mobilização, fiscalização, alinhamento partidário).
- **Site:** legislabrasil.org
- **Status:** ativo, conteúdo corrente.
- **Mantenedor:** organização própria (Olívia Carneiro), parceria com Voto Consciente.
- **Relevância pra nós:** metodologia de indicadores é ótimo ponto de partida pro "o que colocar na ficha" — mas não é open source, sem porta de entrada pra contribuir com código.

## TSE — Divulgação de Candidaturas e Contas (DivulgaCandContas)
- **O que é:** sistema oficial do TSE de consulta individual de candidato — dados pessoais, patrimônio declarado, prestação de contas de campanha, situação da candidatura.
- **Site:** [divulgacandcontas.tse.jus.br](https://divulgacandcontas.tse.jus.br/) (ex. de perfil individual indicado pelo Soutto: [Flávio Bolsonaro](https://divulgacandcontas.tse.jus.br/divulga/#/candidato/BR/BR/20322002026/280002551544/2026/BR)).
- **Dados abertos:** a UI de consulta é uma SPA feita pra navegação humana; pra consumo programático o caminho é o portal separado [dadosabertos.tse.jus.br](https://dadosabertos.tse.jus.br/), que disponibiliza ~172 datasets em CSV — candidatos, bens declarados, prestação de contas partidária, resultados eleitorais, eleitorado.
- **Status:** ativo, mantido pelo próprio TSE.
- **Relevância pra nós:** é a fonte primária oficial já citada de forma genérica no README como "TSE (patrimônio declarado, histórico eleitoral)" — agora com URL concreta. Indicado pelo Soutto (17/08) ao levantar o que já existe antes de codar o MVP. Provável caminho de integração futura: `dadosabertos.tse.jus.br` (CSV), não scraping da UI.

## Radar do Congresso (Congresso em Foco)
- **O que é:** ferramenta do Congresso em Foco (veículo de jornalismo político, grupo UOL) que gera perfil individual de parlamentar, incluindo gastos e acompanhamento de atividade legislativa.
- **Site:** [radar.congressoemfoco.com.br](https://radar.congressoemfoco.com.br/) (ex. de perfil indicado pelo Soutto: [radar.congressoemfoco.com.br/parlamentar/25894/perfil](https://radar.congressoemfoco.com.br/parlamentar/25894/perfil)).
- **Status:** ativo — porém não consegui confirmar detalhes de funcionamento por fetch automatizado (site é uma SPA); vale conferência manual do time antes de tirar conclusões mais profundas.
- **Mantenedor:** Congresso em Foco.
- **Relevância pra nós:** apontado pelo Soutto (17/08) como o produto mais próximo conceitualmente da ficha individual de parlamentar que queremos (múltiplas dimensões — voto, gasto — numa página só). É produto editorial fechado, sem repo/dataset público conhecido até onde verificamos — mesma categoria de "consulta de referência de UX/campos", não parceria técnica, como Legisla Brasil e Plataforma Autoridades Brasil abaixo.

## Plataforma Autoridades Brasil
- **O que é:** produto B2B pago de "inteligência política" (monitoramento de agenda institucional/lobby para empresas).
- **Status:** ativo, mas é produto comercial fechado, não projeto cívico aberto.
- **Relevância pra nós:** é o mais "produto acabado" parecido com a ideia de ficha 360°, mas modelo de negócio oposto ao espírito apartidário/aberto do `fichadopolitico`.

---

## Síntese
Nenhum projeto vivo cobre exatamente o que queremos: ficha individual e apartidária de político (voto + gasto + patrimônio) open source. Os dois projetos mais próximos conceitualmente (Serenata de Amor, Perfil Político) estão mortos — dá pra saquear ideia de schema e abordagem técnica sem conflito. Querido Diário é o único com comunidade viva pra aprender processo de contribuição. Voto Consciente/Legisla Brasil valem consulta de metodologia de indicadores, não parceria de código. Radar do Congresso é o produto fechado mais parecido em conceito de "ficha única" — vale de referência de UX/campos. TSE DivulgaCandContas confirma que a fonte oficial de patrimônio/histórico eleitoral já prevista no README tem caminho de dados abertos em CSV (`dadosabertos.tse.jus.br`), não só a UI de consulta.
