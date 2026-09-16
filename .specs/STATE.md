# STATE — Ficha do Político

> **Status:** v1 em expansão (Legislativo Federal Bicameral)  
> **Última atualização:** 2026-09-13  
> **Base de Decisões:** AD-001 a AD-017

---

## 1. Diretrizes Arquiteturais Ativas (ADRs Consolidados)

### 1.1. Produto & Curadoria Editorial
- **AD-001 & AD-007 (Temas Curados vs. Dumps):** O portal foca em votações nominais cruciais de grande repercussão pública nacional (seed inicial de 5 temas, meta de expansão para 10–20 no v1), em vez de dumps cronológicos ou procedimentais.
- **AD-003 (Transparência Editorial):** A curadoria é pública, documentada em critérios auditáveis (`site/src/pages/criterios.astro`) e versionada diretamente em `dados/catalogo/temas.json`.
- **AD-004 (Apartidarismo e Isenção de Scores):** Proibido qualquer score, nota, ranqueamento ou rotulação ideológica ("progressista", "conservador", "governista"). O portal exibe o dado cru oficial; a interpretação cabe exclusivamente ao cidadão.

### 1.2. Fontes Oficiais, Integridade & Privacidade
- **AD-006 (Verificabilidade Estrita):** Todo dado político exibido (identidade parlamentar ou voto nominal) DEVE conter link direto para a URL da fonte oficial de origem (Câmara ou Senado). Fato sem fonte é proibido no projeto.
- **AD-009 (Privacidade e LGPD):** Dados pessoais sensíveis (CPF, email, telefone de gabinete ou endereço residencial) NÃO são expostos na aplicação, mesmo quando disponíveis nas APIs públicas.
- **AD-011 & AD-014 (Escopo Federal Bicameral):** O projeto cobre estritamente o Congresso Nacional (513 Deputados Federais + 81 Senadores da República). Âmbitos municipal e estadual estão definitivamente fora de escopo por inviabilidade técnica de sustentação sem APIs unificadas.

### 1.3. Arquitetura de Software & Stack
- **AD-002 & AD-013 (Desacoplamento em 3 Camadas):**
  1. *Curadoria Editorial:* `dados/catalogo/temas.json` (Single Source of Truth).
  2. *Dados Canônicos:* `dados/camara/` e `dados/senado/` (JSONs estruturados e sanitizados).
  3. *Frontend & Compilador:* Pipeline Python (`scripts/build_site_data.py`) compila datasets estáticos para o consumo do site.
- **AD-012 (Frontend Astro SSG + Tailwind CSS):** Geração estática (HTML puro sem runtime cliente desnecessário), garantindo performance mobile instantânea (Lighthouse 100) e geração de metatags OpenGraph pré-renderizadas por parlamentar.

---

## 2. Decisões Históricas Superadas (Arquivo)

- **AD-005 (Fonte exclusiva Câmara):** Superada pela AD-014 com a expansão bicameral para o Senado Federal.
- **AD-008 (Stack indefinida):** Superada pela AD-012 com a adoção definitiva do Astro SSG + Tailwind CSS.

---

## 3. Handoff & Foco Atual

- **Fase:** Transição MVP v0 → v1 (Expansão Bicameral).
- **Estado Entregue:**
  - 594 fichas parlamentares geradas (513 deputados + 81 senadores na 57ª Legislatura).
  - Paridade bicameral completa de gastos discricionários: CEAP 2026 (510 deputados federais) e CEAPS 2026 (80 senadores da República), discriminados por categoria de despesa, top 5 maiores gastos e links oficiais para notas fiscais e transparência (AD-019 e AD-020).
  - 548 candidaturas do Congresso Nacional mapeadas para o pleito geral de 2026 com número de urna, partido, situação do registro e link direto ao TSE DivulgaCand (AD-015).
  - Exibição de bens autodeclarados ao TSE em 2026 nas fichas individuais de deputados e senadores, com comparativo de eleições anteriores e discriminação item a item (AD-015).
  - Filtro instantâneo client-side na Home por status eleitoral em 2026 ("Todos", "Candidatos 2026", "Reeleição").
  - 11 fichas completas de candidatos à Presidência da República com evolução patrimonial histórica oficial (TSE / AD-018).
  - 6 votações nominais da Câmara e Senado registradas com links duplos de verificabilidade.
  - Busca rápida unificada na Home (parlamentares) e rota dedicada `/presidente` com busca e visualização gráfica de bens.
  - Testes automatizados de LGPD, integridade de fontes e gastos bicamerais com 100% de sucesso (25 testes).
  - Documentação de backlog de votações criada (`docs/backlog-votacoes.md`).
- **Foco Ativo (v1):**
  1. *Expansão do Catálogo:* Adicionar novos temas nacionais relevantes com votação nominal concluída (meta 10+ matérias).
- **Próximas Fases (v2 / v3):**
  2. *Auditoria de Gastos e Cruzamento Societário (AD-021):* Cruzamento de fornecedores da CEAP/CEAPS com QSA da Receita Federal e folha de servidores do Congresso (v2).
  3. *Destinação de Emendas Parlamentares (AD-016):* Rastreabilidade de valores empenhados/pagos e destino no Transferegov.br (v2).
  4. *Transparência Processual e Judicial (AD-017):* Inquéritos e ações penais no STF e base DataJud/CNJ (v3).
- **Bloqueios:** Nenhum.

---

## 4. Decisões Arquiteturais — Módulo Eleições 2026 (AD-015 & AD-018)

> **Decisão Arquitetural AD-015 (Candidaturas e Patrimônio TSE no Congresso Nacional):**  
> Cruzamento do Legislativo Federal (513 deputados + 81 senadores) com a base oficial de candidaturas de 2026 do TSE DivulgaCandContas:
> 1. **Diferenciação Canônica:** Distinção explícita e neutra entre *Reeleição* (disputa para o mesmo cargo) e *Novo Cargo* (ex: Deputado disputando Senado ou Governo; Senador disputando Presidência).
> 2. **Rastreabilidade Obrigatória:** Cada parlamentar candidato exibe badge oficial com número de urna, partido registrado, situação do registro ("Deferido" / "Aguardando julgamento") e link direto seguro para o DivulgaCandContas.
> 3. **Patrimônio Declarado (2026):** Exibição da discriminação oficial de bens, total declarado e variação matemática com eleição anterior, acompanhado da nota legal mandatória de custo histórico (IRPF/Receita Federal).
> 4. **LGPD Rigorosa (AD-009):** Barreira no pipeline que descarta totalmente CPF, título de eleitor, endereço residencial e contato pessoal.

> **Decisão Arquitetural AD-018 (Rota Dedicada para Presidência e Evolução Patrimonial):**  
> Para garantir utilidade pública imediata diante do ciclo eleitoral sem poluir a modelagem de dados do Legislativo bicameral:
> 1. **Rota Dedicada `/presidente`:** Isolada das rotas `/deputado` e `/senador`, permitindo fichas focadas em candidaturas majoritárias ao Executivo Federal.
> 2. **Metodologia de Custo Histórico (IRPF/TSE):** Todo dado patrimonial explicita em nota oficial neutra que os bens autodeclarados refletem o custo de aquisição da Receita Federal e não a cotação de mercado.
> 3. **Verificabilidade e LGPD:** Todo pleito e item discriminado linka para o TSE (`divulgacandcontas.tse.jus.br`). CPFs e identificadores pessoais são 100% descartados no compilador estático.

---

## 5. Decisões Arquiteturais — Módulo Gastos Parlamentares (AD-019)

> **Decisão Arquitetural AD-019 (Cota Parlamentar CEAP da Câmara dos Deputados):**  
> Exibir em cada ficha parlamentar o detalhamento do uso da Cota para Exercício da Atividade Parlamentar (CEAP) no exercício vigente:
> 1. **Foco em Gastos Discricionários:** Foco exclusivo na CEAP (passagens, locação de veículos, combustíveis, divulgação/gráfica, consultorias e alimentação). Não misturar com salários fixos nem com Verba de Gabinete (pessoal).
> 2. **Processamento em Lote Resiliente:** Ingestão a partir do dump anual consolidado oficial da Câmara (`Ano-2026.csv.zip`), evitando gargalos e rate-limits da API REST.
> 3. **Agregação e Rastreabilidade Obrigatória:** O dataset do site não armazena milhares de comprovantes brutos. Consolida o total gasto, percentuais por categoria e as 5 maiores despesas com link direto oficial para o comprovante (`https://www.camara.leg.br/cota-parlamentar/`).
> 4. **LGPD Rigorosa (AD-009):** O campo CPF do parlamentar contido no dump original é descartado no coletor. CPFs de prestadores pessoa física são mascarados (`***.XXX.XXX-**`).

> **Decisão Arquitetural AD-020 (Cota Parlamentar CEAPS do Senado Federal):**  
> Exibir em cada ficha parlamentar do Senado o detalhamento do uso da Cota para Exercício da Atividade Parlamentar dos Senadores (CEAPS) no ano de 2026:
> 1. **Paridade Bicameral:** Mesma interface e metodologia da Câmara, cobrindo gastos discricionários operacionais (passagens, aluguel de escritórios, consultorias, divulgação, combustíveis).
> 2. **Fonte de Dados Abertos:** Ingestão a partir da API de Dados Abertos Administrativos do Senado (`https://adm.senado.leg.br/adm-dadosabertos/api/v1/senadores/despesas_ceaps/{ano}`), tratando respostas grandes com fallback a `IncompleteRead`.
> 3. **Rastreabilidade Obrigatória:** Cada ficha linka diretamente para o portal de transparência do senador no Senado Federal (`https://www6g.senado.leg.br/transparencia/sen/{codSenador}/?ano=2026`).
> 4. **Conformidade LGPD (AD-009):** Descarte total de identificadores pessoais e mascaramento de CPFs de prestadores pessoa física.

---

## 6. Planejamento — Módulo Destinação de Emendas Parlamentares (AD-016)

> **Decisão Arquitetural AD-016 (Rastreabilidade de Emendas Parlamentares):**  
> Exibir em cada ficha parlamentar a destinação dos recursos do Orçamento Geral da União (emendas individuais, de bancada e transferências especiais):
> 1. **Fontes Oficiais:** Portal da Transparência da CGU (`/api-de-dados/emendas`) e Transferegov.br (convênios e contratos de repasse).
> 2. **Sem Adjetivação:** Exibição quantitativa de valores autorizados, empenhados, liquidados e pagos, acompanhados do município/estado beneficiário e objeto do convênio, sempre linkando o documento fiscal e registro oficial.

---

## 7. Planejamento — Módulo Transparência Processual e Judicial (AD-017)

> **Decisão Arquitetural AD-017 (Integridade Processual e Presunção de Inocência):**  
> Para exibir processos em aberto de parlamentares em tribunais:
> 1. **Fontes Primárias Estritas:** Consulta ao STF (foro por prerrogativa de função para matéria penal) e base DataJud do CNJ.
> 2. **Impedimento de Homônimos:** O match DEVE ser 100% verificado por identificador unívoco para evitar atribuição indevida de processos judiciais de homônimos.
> 3. **Neutralidade e Presunção de Inocência:** Distinção obrigatória e inequívoca entre "Inquérito / Processo em Andamento" e "Condenação Transitada em Julgado". Processos sob segredo de justiça não são exibidos. Link direto para o andamento processual no tribunal de origem é mandatório.

---

## 8. Planejamento — Módulo Cruzamento Societário e Conformidade de Gastos (AD-021)

> **Decisão Arquitetural AD-021 (Cruzamento Societário de Fornecedores da Cota com QSA da Receita Federal e Servidores):**  
> Cruzar objetivamente os CNPJs dos fornecedores pagos pela Cota Parlamentar (CEAP da Câmara e CEAPS do Senado) com a base do Quadro de Sócios e Administradores (QSA) da Receita Federal e a folha de pagamento de servidores do Congresso:
> 1. **Proibição Estrita de Juízo Penal / Adjetivação:** O sistema NUNCA utiliza rótulos subjetivos, tipificações criminais ("laranja", "fantasma", "esquema") ou rankings de suspeição. O portal exibe exclusivamente fatos e vínculos documentais oficiais auditáveis.
> 2. **Padrões de Conformidade e Vínculos Auditados:**
>    - *Vínculo com Gabinete / Servidores:* Mapeamento de sócios-administradores de empresas contratadas que constam na folha de pagamento de secretários parlamentares ou comissionados da Casa legislativa (vedação expressa do Ato da Mesa).
>    - *Vínculo com Financiamento Eleitoral:* Mapeamento de sócios-administradores que constam como doadores de campanha do próprio parlamentar no TSE.
>    - *Relação Cronológica:* Data de fundação do CNPJ na Receita Federal comparada à data do primeiro pagamento da cota.
> 3. **Verificabilidade Tripla Obrigatória:** Toda conexão sinalizada DEVE incluir links diretos para os três documentos primários:
>    - Comprovante de despesa pública da Câmara/Senado (com link oficial da NF/recibo).
>    - Espelho público do CNPJ/QSA da Receita Federal.
>    - Ato de nomeação ou folha oficial da Casa Legislativa / prestação de contas do TSE.
> 4. **Conformidade LGPD (AD-009):** Tratamento exclusivo de dados públicos de pessoas jurídicas e agentes públicos no exercício de funções ou doações oficiais registradas, mantendo o mascaramento de CPFs (`***.XXX.XXX-**`) conforme a legislação.


