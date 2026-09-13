# Fontes Oficiais de Dados Públicos

Este documento cataloga as fontes de dados primárias e oficiais do Estado brasileiro que alimentam ou alimentarão a base do **Ficha do Político**.

> **Regra Fundamental do Projeto ([AGENTS.md](AGENTS.md)):**  
> Todo dado factual exibido em uma ficha (identificação, votação, gasto, emenda, patrimônio ou sanção) deve ser estritamente rastreável à sua fonte primária oficial, com link explícito para o endpoint da API ou página de registro original. Fontes secundárias (imprensa, redes sociais) não são utilizadas para dados estruturados.

---

## 1. Poder Legislativo Federal

### 1.1. Câmara dos Deputados
- **O que é:** Órgão representativo dos cidadãos na esfera federal (513 deputados federais).
- **Status no projeto:** **Em produção (Base do MVP v0)**.
- **Documentação Swagger:** [dadosabertos.camara.leg.br/swagger/api.html](https://dadosabertos.camara.leg.br/swagger/api.html)
- **Base URL da API:** `https://dadosabertos.camara.leg.br/api/v2`
- **Dumps em lote:** [dadosabertos.camara.leg.br/arquivos/](https://dadosabertos.camara.leg.br/arquivos/) (arquivos anuais em CSV/JSON/XML)
- **Autenticação:** Nenhuma (livre).
- **Protocolo:** REST JSON / XML e Dumps CSV.
- **Endpoints-chave:**
  - `GET /deputados`: lista deputados em exercício ou históricos com partido, UF e ID.
  - `GET /deputados/{id}`: dados biográficos completos, gabinete, redes sociais e último status.
  - `GET /votacoes`: lista sessões de votações com data, tipo de proposição e código.
  - `GET /votacoes/{id}/votos`: lista nominal de votos de cada deputado em uma votação específica (Sim, Não, Abstenção, Obstrução, Artigo 17, etc.).
  - `GET /deputados/{id}/despesas`: Cota para o Exercício da Atividade Parlamentar (CEAP) detalhada por documento fiscal, tipo de gasto e fornecedor (planejado para pós-v0).
  - `GET /proposicoes/{id}`: dados oficiais da proposição legislativa (PL, PEC, MPV, etc.).
- **Notas técnicas de engenharia:**
  - A API possui paginação com cabeçalhos `Link` no padrão RFC 5988 (`rel="next"`, etc.).
  - Para validação de dados em lote, os arquivos CSV anuais em `/arquivos/` são mais eficientes e reduzem a pressão no servidor da Câmara que fazer centenas de chamadas pontuais.

---

### 1.2. Senado Federal
- **O que é:** Câmara alta do Congresso Nacional, representante dos Estados e do Distrito Federal (81 senadores).
- **Status no projeto:** Planejado (fase pós-v0).
- **Atenção Técnica — Separação de APIs:** O Senado Federal mantém dois serviços de dados abertos distintos:
  
#### A. API Legislativa (Secretaria-Geral da Mesa)
- **Documentação Swagger:** [legis.senado.leg.br/dadosabertos/docs/ui/index.html](https://legis.senado.leg.br/dadosabertos/docs/ui/index.html)
- **Base URL:** `https://legis.senado.leg.br/dadosabertos/`
- **Autenticação:** Nenhuma.
- **Protocolo:** REST (retorna JSON via cabeçalho `Accept: application/json` ou XML por padrão).
- **Endpoints-chave:**
  - `GET /senador/lista/atual`: lista de todos os 81 senadores em exercício com código parlamentar, dados partidários, UF e foto.
  - `GET /senador/{codigo}`: biografia, composição de comissões, mandatos e filiações partidárias.
  - `GET /senador/{codigo}/autorias`: matérias e proposições de autoria do senador.
  - `GET /senador/{codigo}/votacoes`: histórico de votações nominais do senador.
  - `GET /plenario/lista/votacao/{dataInicio}/{dataFim}`: votações nominais ocorridas no plenário do Senado.
  - `GET /materia/{codigo}`: metadados da proposição tramitando no Senado (PLS, PEC, PRS).

#### B. API Administrativa & Transparência (Gastos / CEAPS)
- **Documentação Swagger:** [adm.senado.gov.br/adm-dadosabertos/swagger-ui/index.html](https://adm.senado.gov.br/adm-dadosabertos/swagger-ui/index.html)
- **Portal de Dados Abertos:** [www12.senado.leg.br/dados-abertos](https://www12.senado.leg.br/dados-abertos)
- **Autenticação:** Nenhuma.
- **Protocolo:** REST JSON e downloads em CSV.
- **Endpoints-chave:**
  - `GET /adm-dadosabertos/senador/buscarDespesasCeapsPorAno`: despesas da Cota para Exercício da Atividade Parlamentar dos Senadores (CEAPS).
  - Dumps anuais de ressarcimento de despesas médicas e passagens aéreas não inclusas na cota.

---

### 1.3. Congresso Nacional (Sessões Conjuntas)
- **O que é:** Sessões que reúnem Deputados e Senadores para deliberação conjunta.
- **Portal:** [congressonacional.leg.br](https://www.congressonacional.leg.br/)
- **Relevância para a ficha:** Votações de vetos presidenciais e aprovação do Orçamento Geral da União (LOA, LDO, PPA). Votos nominais em vetos presidenciais são cruciais para medir a postura dos parlamentares diante de decisões do Executivo.

---

## 2. Poder Judiciário & Justiça Eleitoral

### 2.1. Tribunal Superior Eleitoral (TSE)
- **O que é:** Órgão de cúpula da Justiça Eleitoral responsável pela organização de eleições, registro de candidaturas e prestação de contas eleitorais.
- **Status no projeto:** Planejado (patrimônio declarado e histórico eleitoral).
- **Fontes do TSE:**
  1. **DivulgaCandContas (Frontend de consulta humana):** [divulgacandcontas.tse.jus.br](https://divulgacandcontas.tse.jus.br/) — interface SPA detalhada por pleito.
  2. **Portal de Dados Abertos do TSE:** [dadosabertos.tse.jus.br](https://dadosabertos.tse.jus.br/) — catálogo de datasets em formato CSV.
  3. **Catálogo Nacional de Dados Abertos:** [dados.gov.br](https://dados.gov.br/) (conjuntos de dados eleitorais do TSE).
- **Entidades de interesse:**
  - **Bens declarados de candidatos:** lista item a item de patrimônio informado à Justiça Eleitoral a cada pleito (imóveis, veículos, aplicações financeiras, dinheiro em espécie, participações em empresas).
  - **Prestação de contas eleitorais:** receitas e despesas de campanha, doadores (pessoas físicas e fundos partidários/eleitorais).
  - **Histórico de candidaturas:** cargos disputados anteriormente, coligações, suplências e resultados eleitorais desde 1994.
- **Alerta Técnico Crítico (WAF / Anti-Bot):**
  - Os domínios do TSE (`dadosabertos.tse.jus.br` e `divulgacandcontas.tse.jus.br`) utilizam camada de proteção WAF (Akamai/Cloudflare) que retorna **HTTP 403 Forbidden** para clientes HTTP automatizados comuns (como Python `urllib`, `requests` ou `curl`) sem TLS fingerprinting ou cabeçalhos de navegador adequados.
  - **Estratégia de engenharia recomendada:** Não fazer scraping direto da interface do DivulgaCandContas em runtime. O pipeline deve baixar os dumps consolidados em lote (.zip / .csv) por ano eleitoral direto dos repositórios de dados abertos ou via espelhos confiáveis.

---

### 2.2. Conselho Nacional de Justiça (CNJ) — Base DataJud
- **O que é:** Base Nacional de Dados do Poder Judiciário que centraliza metadados processuais de todo o Brasil.
- **Status no projeto:** Investigação técnica avançada.
- **Documentação da API Pública:** [datajud-wiki.cnj.jus.br/api-publica/](https://datajud-wiki.cnj.jus.br/api-publica/)
- **Base URL:** `https://api-publica.datajud.cnj.jus.br/`
- **Autenticação:** Requer API Key pública fornecida diretamente na documentação da Wiki do CNJ (via header `Authorization: APIKey <chave>`).
- **Protocolo:** REST com interface compatível com Elasticsearch (`_search`).
- **Tribunais cobertos:**
  - Tribunais Superiores: STF, STJ, TST, TSE, STM (`api_publica_stf`, `api_publica_stj`, `api_publica_tse`, etc.).
  - Justiça Federal: TRF1 a TRF6 (`api_publica_trf1`, etc.).
  - Justiça Estadual: 27 Tribunais de Justiça Estaduais (`api_publica_tjsp`, `api_publica_tjrj`, `api_publica_tjmg`, etc.).
- **Relevância para a ficha:** Permite consultar a existência de processos judiciais públicos em andamento ou julgados envolvendo a pessoa do parlamentar (inquéritos, ações civis públicas por improbidade administrativa, ações populares).
- **Ressalva jurídica e ética:** Processos em segredo de justiça não são retornados pela API. Toda exibição deve distinguir processo em andamento de condenação transitada em julgado para respeitar a presunção de inocência e as diretrizes do [AGENTS.md](AGENTS.md).

---

### 2.3. Supremo Tribunal Federal (STF)
- **O que é:** Corte constitucional responsável pelo julgamento penal de deputados federais e senadores (foro por prerrogativa de função, CF art. 53, §1º).
- **Portal de Dados Abertos:** [transparencia.stf.jus.br](https://transparencia.stf.jus.br/extensions/dados_abertos/dados_abertos.html)
- **Entidades de interesse:** Inquéritos (INQ), Ações Penais (AP), Ações Diretas de Inconstitucionalidade (ADI) e Reclamações envolvendo parlamentares federais.

---

## 3. Poder Executivo Federal, Orçamento & Fiscalização

### 3.1. Portal da Transparência do Governo Federal (CGU)
- **O que é:** Principal portal de transparência dos gastos públicos do Executivo Federal, gerido pela Controladoria-Geral da União (CGU).
- **Status no projeto:** Planejado (gastos, emendas e fiscalização).
- **Documentação Swagger:** [api.portaldatransparencia.gov.br/swagger-ui/index.html](https://api.portaldatransparencia.gov.br/swagger-ui/index.html)
- **Portal de Downloads em Lote:** [portaldatransparencia.gov.br/download-de-dados](https://portaldatransparencia.gov.br/download-de-dados)
- **Autenticação:** Requer chave de API gratuita via cadastro no Gov.br (header `chave-api-dados`). O download de arquivos CSV completos não requer chave.
- **Endpoints-chave:**
  - `GET /api-de-dados/emendas`: emendas parlamentares federais (individuais, bancada, comissão, relator). Retorna autor, número da emenda, valor empenhado, liquidado e pago.
  - `GET /api-de-dados/emendas/documentos/{codigo}`: documentos de liquidação/pagamento vinculados à emenda.
  - `GET /api-de-dados/peps`: **Cadastro de Pessoas Expostas Politicamente (PEP)**. Permite certificar oficialmente se um indivíduo ou familiar é classificado como PEP pela legislação antibranqueamento de capitais.
  - `GET /api-de-dados/servidores/remuneracao`: remuneração bruta e líquida de servidores públicos e ocupantes de cargos em comissão no Executivo.
  - `GET /api-de-dados/viagens-por-cpf`: histórico de viagens a trabalho pagas com recursos da União (passagens e diárias).
  - `GET /api-de-dados/ceis`, `GET /api-de-dados/cnep`, `GET /api-de-dados/cepim`: cadastros de empresas e entidades sancionadas, declaradas inidôneas ou impedidas de licitar com o poder público.

---

### 3.2. Transferegov.br (antiga Plataforma +Brasil / SICONV — Ministério da Gestão)
- **O que é:** Sistema oficial de operacionalização de transferências voluntárias e emendas parlamentares da União para Estados, Municípios e organizações da sociedade civil.
- **Status no projeto:** Investigação técnica avançada.
- **Nova API Pública (2026):** [api-publica.transferegov.gestao.gov.br](https://api-publica.transferegov.gestao.gov.br)
- **Repositório de Dados Abertos (CSV):** [repositorio.dados.gov.br](https://repositorio.dados.gov.br)
- **Relevância para a ficha:** Permite rastrear **onde foi parar o dinheiro das emendas parlamentares**. Mostra o convênio, o município destinatário, a empresa contratada na ponta da obra/serviço e a situação de execução física da parceria.

---

### 3.3. Siga Brasil (Senado Federal)
- **O que é:** Sistema de informações orçamentárias desenvolvido pelo Senado Federal que agrega dados do SIAFI e SIOP.
- **Portal:** [www12.senado.leg.br/orcamento/sigabrasil](https://www12.senado.leg.br/orcamento/sigabrasil)
- **Relevância para a ficha:** Permite cruzamento de dados contábeis consolidados sobre a execução orçamentária de emendas parlamentares e transferências especiais ("emendas PIX").

---

### 3.4. Tribunal de Contas da União (TCU)
- **O que é:** Órgão de controle externo que auxilia o Congresso Nacional na fiscalização contábil, financeira e patrimonial da administração pública.
- **Status no projeto:** Investigação técnica avançada.
- **Portal de Transparência e Dados Abertos:** [portal.tcu.gov.br/transparencia/dados-abertos/](https://portal.tcu.gov.br/transparencia/dados-abertos/)
- **Sistemas essenciais:**
  - **CADIRREG (Cadastro de Contas Julgadas Irregulares):** [contasirregulares.tcu.gov.br/](https://contasirregulares.tcu.gov.br/) — relação de gestores e políticos que tiveram suas contas julgadas irregulares pelo TCU com decisão irrecorrível. É a lista oficial enviada à Justiça Eleitoral para fins de inelegibilidade sob a **Lei da Ficha Limpa (Lei Complementar nº 135/2010)**.
  - **Cadastro de Inabilitados e Inidôneos:** [contas.tcu.gov.br/ords/f?p=INABILITADOS:INICIO](https://contas.tcu.gov.br/ords/f?p=INABILITADOS:INICIO) — pessoas físicas e jurídicas declaradas inabilitadas para exercício de cargo em comissão ou função de confiança (art. 60 da Lei 8.443/1992).

---

## 4. Dados Societários, Registro Mercantil & Contratos Públicos

### 4.1. Receita Federal do Brasil — Dados Abertos do CNPJ
- **O que é:** Base completa do Cadastro Nacional da Pessoa Jurídica disponibilizada publicamente pela Receita Federal.
- **Portal:** [dados.gov.br/dados/conjuntos-dados/cadastro-nacional-da-pessoa-juridica---cnpj](https://dados.gov.br/dados/conjuntos-dados/cadastro-nacional-da-pessoa-juridica---cnpj)
- **Formato:** Dumps mensais compactados em CSV (.zip).
- **Tabela essencial:** `Socios` (Quadro de Sócios e Administradores — QSA).
- **Relevância para a ficha:** Cruzamento do CPF/nome civil do político para identificar participações societárias ativas ou históricas em empresas privadas, cooperativas ou holdings patrimoniais. Crucial para checagem cruzada com declaração de bens do TSE e contratos governamentais.

---

### 4.2. Compras.gov.br (antigo ComprasNet / SIASG)
- **O que é:** Sistema Integrado de Administração de Serviços Gerais do Governo Federal que gerencia compras públicas e licitações.
- **Documentação Swagger:** [dadosabertos.compras.gov.br/swagger-ui/index.html](https://dadosabertos.compras.gov.br/swagger-ui/index.html)
- **Relevância para a ficha:** Permite identificar se empresas fornecedoras que receberam pagamentos da cota parlamentar (CEAP) ou de emendas também possuem contratos licitados com a administração federal.

---

## 5. Matriz de Prioridade & Estratégia de Ingestão

| Fonte Oficial | Domínio | Formato Primário | Autenticação | Dificuldade de Coleta | Prioridade Roadmap |
|---|---|---|---|---|---|
| **Câmara dos Deputados** | Votos e Perfil | REST JSON / Dumps CSV | Nenhuma | Baixa | **MVP v0 (Ativo)** |
| **Câmara dos Deputados (CEAP)** | Gastos de Deputados | REST JSON / CSV | Nenhuma | Baixa | **v1 (Próximo)** |
| **TSE (Bens Declarados)** | Patrimônio Político | Dumps CSV por eleição | Nenhuma (requer bulk download devido a WAF) | Média | **v1 (Próximo)** |
| **Senado Federal (Legis)** | Votos e Perfil | REST JSON / XML | Nenhuma | Baixa | **v1 (Próximo)** |
| **Senado Federal (CEAPS)** | Gastos de Senadores | REST JSON / CSV | Nenhuma | Baixa | **v1 (Próximo)** |
| **Portal da Transparência (CGU)** | Emendas Parlamentares | REST JSON / Dumps CSV | API Key gratuita (via Gov.br) | Média | **v2** |
| **TCU (CADIRREG)** | Ficha Limpa / Contas | Consulta web / Export CSV | Nenhuma | Baixa | **v2** |
| **Transferegov.br** | Destino de Emendas | REST JSON / Dumps CSV | Nenhuma | Média | **v2** |
| **CNJ (DataJud)** | Processos Judiciais | REST Elasticsearch | API Key pública | Alta | **v3 (Avançado)** |
| **Receita Federal (CNPJ QSA)** | Empresas e Vínculos | Dumps CSV (~GBs) | Nenhuma | Alta (volume) | **v3 (Avançado)** |