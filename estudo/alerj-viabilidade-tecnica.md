# Estudo de Viabilidade Técnica — Deputados Estaduais (ALERJ / Rio de Janeiro)

> **Data:** 2026-09-23  
> **Status:** Concluído (Spike Exploratório)  
> **Referência Arquitetural:** [AD-011 e AD-014 (.specs/STATE.md)](../.specs/STATE.md)  
> **Autores:** Antigravity & Antonio Leblanc

---

## 1. Veredito Executivo

A inclusão de **Deputados Estaduais da ALERJ** com paridade de recursos em relação ao Congresso Nacional (Câmara e Senado) é **tecnicamente inviável no momento atual** sem recorrer a scrapers frágeis, quebra de contratos e OCR/parsing de PDFs de diários oficiais.

A ALERJ não possui infraestrutura moderna de dados abertos para o processo legislativo e despesas operacionais:
* O domínio `dadosabertos.alerj.rj.gov.br` **não existe** (falha de DNS).
* O Portal da Transparência não expõe API REST pública (rota `/api` retorna `404 Not Found`).
* O sistema de projetos e tramitação ainda reside em uma camada legada sobre **IBM Lotus Notes** (`www3.alerj.rj.gov.br/lotus_notes/default.asp`).
* As despesas do legislativo são publicadas em **relatórios anuais fechados em formato PDF**, sem detalhamento transacional por nota fiscal/fornecedor via API ou CSV.

---

## 2. Diagnóstico dos Endpoints Oficiais Testados

| Endpoint / URL | Status | Formato / Resposta | Observações Técnicas |
| :--- | :---: | :---: | :--- |
| `https://dadosabertos.alerj.rj.gov.br` | **ERR** | Falha DNS (`NXDOMAIN`) | Inexistente. Não há portal central de dados abertos como o federal. |
| `https://transparencia.alerj.rj.gov.br/api` | **404** | Not Found | Não existe camada de API REST pública exposta no portal. |
| `https://www.alerj.rj.gov.br/Deputados/QuemSao` | **200** | HTML (ASP.NET) | Lista com foto e links para as páginas dos 70 deputados da 13ª Legislatura. |
| `https://www.alerj.rj.gov.br/Deputados/PerfilDeputado/{id}` | **200** | HTML puro | Apenas release biográfico (institucional/assessoria) e contato. **Zero dados de votos nominais ou despesas.** |
| `http://www3.alerj.rj.gov.br/lotus_notes/default.asp?id=161` | **200** | Classic ASP / Lotus Notes | Busca textual de Projetos de Lei (2023–2027). Não expõe votações nominais estruturadas. |
| `https://transparencia.alerj.rj.gov.br/section/report/104` | **200** | HTML com links PDF | Relatório de Gastos do Poder Legislativo. Disponibiliza apenas links para PDFs anuais (`RELATÓRIO 2024 pdf`, `RELATÓRIO 2023 pdf`). |
| `https://transparencia.alerj.rj.gov.br/section/report/121` | **200** | HTML | Emendas Parlamentares Impositivas em formato tabular estático/PDF. |
| `https://divulgacandcontas.tse.jus.br` (TSE) | **200 / 403** | JSON / CSV Dumps | Base federal unificada. Contém candidaturas e declaração de patrimônio de todos os 70 eleitos da ALERJ. |

---

## 3. Análise Detalhada por Eixo do Produto

### 3.1. Eixo 1: Votações Nominais (Gargalo Crítico)
* **Como é na Câmara/Senado:** A API da Câmara (`dadosabertos.camara.leg.br/api/v2/votacoes/{id}/votos`) e a do Senado entregam um JSON com ID do parlamentar, nome, partido, UF e o voto explícito ("Sim", "Não", "Abstenção", "Obstrução").
* **Como é na ALERJ:** Não existe registro estruturado de votos por proposição. Para auditar como votou cada deputado em um projeto específico (ex.: aumento de alíquota de ICMS ou privatizações), o fluxo exige:
  1. Localizar o número do projeto no sistema Lotus Notes;
  2. Identificar a data da sessão plenária em que houve deliberação nominal;
  3. Baixar o arquivo PDF do **Diário Oficial do Estado do Rio de Janeiro (DOERJ - Caderno Poder Legislativo / Parte II)** da data correspondente;
  4. Realizar parsing/OCR do texto da ata da sessão para encontrar as transcrições taquigráficas de votação nominal.
* **Impacto:** Custo de desenvolvimento elevadíssimo, altíssima taxa de quebra e manutenção manual insustentável.

### 3.2. Eixo 2: Gastos de Cota e Verbas Indenizatórias
* **Como é na Câmara/Senado:** A Câmara publica dumps anuais consolidados em `Ano-2026.csv.zip` com cada comprovante de despesa, CNPJ do prestador de serviço, link direto para a nota fiscal autenticada e número do documento.
* **Como é na ALERJ:** O Portal da Transparência (`report/104`) disponibiliza apenas demonstrativos anuais em PDF da folha consolidada do Poder Legislativo. Não há endpoint público estruturado para inspecionar, por deputado:
  * Fornecedores individuais contratados;
  * Comprovantes e notas fiscais digitalizadas;
  * Classificação categorizada de despesas por mês.
* **Impacto:** Impossibilidade de aplicar cruzamento com QSA da Receita Federal (AD-021) ou rastreabilidade de comprovantes no padrão do produto.

### 3.3. Eixo 3: Identidade, Eleições e Patrimônio (100% Viável)
* **Fonte:** Tribunal Superior Eleitoral (TSE Dados Abertos e DivulgaCandContas).
* **Viabilidade:** Total. O TSE unifica as eleições federais e estaduais (eleições gerais de 2022 e 2026).
* **Dados Disponíveis:**
  * Lista oficial dos 70 deputados eleitos para a 13ª Legislatura (2023–2027) do RJ;
  * Votação nominal nas urnas e partido de registro;
  * Histórico de bens autodeclarados (imóveis, veículos, contas bancárias, ações);
  * Link oficial e permanente no DivulgaCandContas.

---

## 4. Matriz Comparativa de Viabilidade

| Requisito do Projeto | Congresso Nacional (Federal) | ALERJ (Estadual RJ) | Veredito RJ |
| :--- | :---: | :---: | :---: |
| **API REST Oficial Estável** | Sim (Swagger / OpenData) | Não | ❌ Bloqueante |
| **Dumps Abertos em CSV/JSON** | Sim (diários / mensais) | Não (PDFs anuais) | ❌ Bloqueante |
| **Votações Nominais Estruturadas** | Sim (link permanente do voto) | Apenas no Diário Oficial em PDF | ❌ Inviável |
| **Gastos por Comprovante/CNPJ** | Sim (CEAP / CEAPS) | Não exposto por transação | ❌ Inviável |
| **Patrimônio Declarado e Bens** | Sim (TSE DivulgaCand) | Sim (TSE DivulgaCand) | ✅ Viável |
| **Candidaturas 2026** | Sim (TSE) | Sim (TSE) | ✅ Viável |

---

## 5. Conclusão e Recomendações

1. **Manutenção do Escopo Federal ([AD-011 / AD-014](../.specs/STATE.md)):** Recomenda-se manter o produto focado no Congresso Nacional (513 deputados + 81 senadores) e Presidência da República. O esforço para sustentar dados estaduais da ALERJ multiplicaria a complexidade do pipeline com retorno analítico assimétrico.
2. **Cenário de Piloto Parcial (Se houver interesse futuro do grupo):**
   Caso o time decida um dia exibir deputados estaduais do RJ, a **única rota sustentável** é criar um módulo simplificado com selo explícito:
   * **"Ficha Eleitoral & Patrimonial (TSE)"**, sem promessa de votações em plenário nem de cota interna da ALERJ.
   * Exibição restrita a: dados da eleição 2022/2026, votação recebida no estado, evolução de patrimônio no TSE e links oficiais externos.
