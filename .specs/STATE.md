# STATE — Ficha do Político

> **Status:** v1 em expansão (Legislativo Federal Bicameral)  
> **Última atualização:** 2026-09-23  
> **Base de Decisões:** AD-001 a AD-021

---

## 1. Visão de Produto & Diferencial Cívico

### 1.1. O Problema
Para saber como um parlamentar votou ou quanto gastou em decisões de grande impacto nacional (ex.: *Escala 6×1*, *Marco Temporal*, *Reforma Tributária*), o cidadão enfrenta uma jornada burocrática e confusa:
1. Descobrir em notícias o número do projeto (PL, PEC, MPV).
2. Entrar nos portais da Câmara ou Senado e decifrar tramitações e requerimentos regimentais.
3. Localizar o parlamentar em listas extensas de votação.

Ferramentas existentes muitas vezes agregam dados sem curadoria, apresentam dumps cronológicos procedimentais irrelevantes ou aplicam scores ideológicos subjetivos.

### 1.2. A Proposta da Ficha
> **A maneira mais rápida e simples de um cidadão buscar um parlamentar e ver imediatamente como ele votou, quanto gastou e qual o patrimônio declarado — em dados crus, sem viés partidário, sem adjetivação e sempre com link direto para a fonte oficial primária.**

---

## 2. Diretrizes Arquiteturais Ativas (ADRs Consolidados)

### 2.1. Produto & Curadoria Editorial
- **AD-001 & AD-007 (Temas Curados vs. Dumps):** O portal foca em votações nominais cruciais de grande repercussão pública nacional (seed inicial de 5 temas, meta de expansão para 10–20 no v1), em vez de dumps cronológicos ou procedimentais.
- **AD-003 (Transparência Editorial):** A curadoria é pública, documentada em critérios auditáveis (`site/src/pages/criterios.astro`) e versionada diretamente em `dados/catalogo/temas.json`.
- **AD-004 (Apartidarismo e Isenção de Scores):** Proibido qualquer score, nota, ranqueamento ou rotulação ideológica ("progressista", "conservador", "governista"). O portal exibe o dado cru oficial; a interpretação cabe exclusivamente ao cidadão.

### 2.2. Fontes Oficiais, Integridade & Privacidade
- **AD-006 (Verificabilidade Estrita):** Todo dado político exibido (identidade parlamentar ou voto nominal) DEVE conter link direto para a URL da fonte oficial de origem (Câmara ou Senado). Fato sem fonte é proibido no projeto.
- **AD-009 (Privacidade e LGPD):** Dados pessoais sensíveis (CPF, email, telefone de gabinete ou endereço residencial) NÃO são expostos na aplicação, mesmo quando disponíveis nas APIs públicas.
- **AD-011 & AD-014 (Escopo Federal Bicameral):** O foco central do v1 cobre o Congresso Nacional (513 Deputados Federais + 81 Senadores da República). A esfera estadual permanece fora do core de produção da v1 pela extrema assimetria de maturidade de dados entre estados, mas não há veto impeditivo para módulos independentes por estado desenvolvidos pela comunidade (ver auditorias empíricas de RJ e SP em [estudo/alerj-viabilidade-tecnica.md](../estudo/alerj-viabilidade-tecnica.md) e [estudo/alesp-viabilidade-tecnica.md](../estudo/alesp-viabilidade-tecnica.md)).

### 2.3. Arquitetura de Software & Stack
- **AD-002 & AD-013 (Desacoplamento em 3 Camadas):**
  1. *Curadoria Editorial:* `dados/catalogo/temas.json` (Single Source of Truth).
  2. *Dados Canônicos:* `dados/camara/` e `dados/senado/` (JSONs estruturados e sanitizados).
  3. *Frontend & Compilador:* Pipeline Python (`scripts/build_site_data.py`) compila datasets estáticos para o consumo do site.
- **AD-012 (Frontend Astro SSG + Tailwind CSS):** Geração estática (HTML puro sem runtime cliente desnecessário), garantindo performance mobile instantânea (Lighthouse 100) e geração de metatags OpenGraph pré-renderizadas por parlamentar.

---

## 3. Decisões Históricas Superadas (Arquivo)

- **AD-005 (Fonte exclusiva Câmara):** Superada pela AD-014 com a expansão bicameral para o Senado Federal.
- **AD-008 (Stack indefinida):** Superada pela AD-012 com a adoção definitiva do Astro SSG + Tailwind CSS.

---

## 4. Handoff & Foco Operacional

- **Fase Atual:** v1 em expansão (Legislativo Federal Bicameral).
- **Módulos Ativos em Produção:**
  - *Votações Nominais Curadas:* 10 temas deliberados na Câmara e Senado com links duplos de verificabilidade (incluindo Arcabouço Fiscal, Regulamentação Tributária, Estrutura dos Ministérios e Recriação do DPVAT/SPVAT).
  - *Gastos Discricionários:* CEAP (Câmara) e CEAPS (Senado) do exercício vigente (AD-019 e AD-020).
  - *Destinação de Emendas Parlamentares:* Execução orçamentária oficial da CGU da 57ª Legislatura (2023–2026), discriminando Emendas Pix e Finalidade Definida (AD-016).
  - *Eleições & Patrimônio 2026:* Candidaturas mapeadas e histórico de bens autodeclarados ao TSE para o Congresso e Presidência (AD-015 e AD-018).
- **Foco Imediato (v1):** Catálogo de votações nominais consolidado em 10 temas (meta inicial atingida; ver `docs/backlog-votacoes.md`).
- **Roadmap Subsequente:**
  - *v2:* Auditoria de Gastos e Cruzamento Societário de Fornecedores da Cota com QSA da Receita Federal e Folha de Servidores (AD-021).
  - *v2:* Rastreabilidade de Convênios na Ponta das Emendas via Transferegov.br.
  - *v3:* Transparência Processual e Judicial via STF e DataJud/CNJ (AD-017).
- **Bloqueios Ativos:** Nenhum.

---

## 5. Decisões Arquiteturais — Módulo Eleições 2026 (AD-015 & AD-018)

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

## 6. Decisões Arquiteturais — Módulo Gastos Parlamentares (AD-019 & AD-020)

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

## 7. Decisões Arquiteturais — Módulo Emendas Parlamentares (AD-016)

> **Decisão Arquitetural AD-016 (Rastreabilidade de Emendas Parlamentares — CGU):**  
> Exibir em cada ficha parlamentar a destinação dos recursos do Orçamento Geral da União (57ª Legislatura: 2023–2026):
> 1. **Fonte Oficial Primária:** Download de dados consolidados abertos da Controladoria-Geral da União (CGU), processando `EmendasParlamentares.csv`.
> 2. **Diferenciação Canônica Neutra:** Distinção explícita entre *Transferências Especiais ("Emendas Pix")* (repasses diretos sem convênio prévio) e *Transferências com Finalidade Definida* (vinculadas a políticas públicas específicas).
> 3. **Agregação e Rastreabilidade Obrigatória:** Cada ficha exibe o total pago, restos a pagar pagos, divisão por funções orçamentárias (Saúde, Educação, Infraestrutura), principais municípios destinatários e link de consulta direta para a página oficial do autor no Portal da Transparência da CGU.
> 4. **Conformidade LGPD (AD-009):** Descarte total de identificadores privados e foco estrito no repasse de recursos públicos a entes federativos.
> 5. **Dataset Canônico:** `dados/emendas/emendas_resumo.json`, compilado via `scripts/cgu/fetch_emendas.py`.

---

## 8. Planejamento — Módulo Transparência Processual e Judicial (AD-017)

> **Decisão Arquitetural AD-017 (Integridade Processual e Presunção de Inocência):**  
> Para exibir processos em aberto de parlamentares em tribunais:
> 1. **Fontes Primárias Estritas:** Consulta ao STF (foro por prerrogativa de função para matéria penal) e base DataJud do CNJ.
> 2. **Impedimento de Homônimos:** O match DEVE ser 100% verificado por identificador unívoco para evitar atribuição indevida de processos judiciais de homônimos.
> 3. **Neutralidade e Presunção de Inocência:** Distinção obrigatória e inequívoca entre "Inquérito / Processo em Andamento" e "Condenação Transitada em Julgado". Processos sob segredo de justiça não são exibidos. Link direto para o andamento processual no tribunal de origem é mandatório.

---

## 9. Planejamento — Módulo Cruzamento Societário e Conformidade de Gastos (AD-021)

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

---

## 10. Governança e Mudanças de Escopo

Para sugerir inclusão de novos campos, alteração de fases ou ajustes de roadmap:
1. Abra uma issue para discussão prévia e exploração de ideias junto ao time.
2. Mudanças aprovadas em escopo, arquitetura ou fases de entrega são formalizadas via Pull Request diretamente neste documento (`.specs/STATE.md`).
3. O time (Antonio, Soutto, Layr, Ludovic) revisa e valida as alterações com base na viabilidade técnica e nos dois pilares inegociáveis do projeto: **apartidarismo** e **verificabilidade de fonte primária**.


