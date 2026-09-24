# Estudo de Viabilidade Técnica — Deputados Estaduais (ALESP / São Paulo)

> **Data:** 2026-09-23  
> **Status:** Concluído (Spike Exploratório)  
> **Referência:** [AD-011 e AD-014 (.specs/STATE.md)](../.specs/STATE.md) | [Estudo ALERJ/RJ](alerj-viabilidade-tecnica.md)  
> **Autores:** Antigravity & Antonio Leblanc

---

## 1. Veredito Executivo

A **ALESP (Assembleia Legislativa do Estado de São Paulo)** apresenta um ecossistema de dados abertos **significativamente mais maduro e moderno** que o da ALERJ (Rio de Janeiro).

A ALESP mantém uma instância oficial da plataforma **CKAN** com API REST padronizada e dumps estruturados em **JSON** e **XML** atualizados em tempo quase real (exercício de 2026).
* **Gastos de Gabinete:** **100% Estruturados em JSON**. O arquivo `despesas_gabinetes.json` entrega transações com CNPJ, fornecedor, tipo de despesa, matrícula e nome do deputado.
* **Deputados:** Lista canônica e metadados disponíveis via `deputados.json` e `deputados.xml`.
* **Votações em Comissões:** Disponíveis em `comissoes_permanentes_votacoes.xml` com o voto nominal de cada parlamentar.
* **Votações em Plenário (O Limite):** Não estão empacotadas no catálogo do CKAN. Votações nominais do plenário exigem raspagem da consulta web de sessões plenárias ou consulta a resumos legislativos.

---

## 2. Catálogo de Endpoints e Dumps Descobertos

| Recurso / Serviço | Endpoint Oficial | Formato | Status |
| :--- | :--- | :---: | :---: |
| **API do Catálogo CKAN** | `https://ckan.al.sp.gov.br/api/3/action/package_list` | JSON | ✅ **200 OK** (26 datasets) |
| **Metadados de Despesas** | `https://ckan.al.sp.gov.br/api/3/action/package_show?id=despesas-de-gabinete` | JSON | ✅ **200 OK** |
| **Dump Despesas de Gabinete** | `https://www3.al.sp.gov.br/repositorio/dados-abertos/output/json/despesas_gabinetes.json` | JSON | ✅ **200 OK** (Ativo 2026) |
| **Dump Deputados Estaduais** | `https://www3.al.sp.gov.br/repositorio/dados-abertos/output/json/deputados.json` | JSON | ✅ **200 OK** |
| **Votações nas Comissões** | `https://www.al.sp.gov.br/repositorioDados/processo_legislativo/comissoes_permanentes_votacoes.xml` | XML | ✅ **200 OK** |
| **Presença nas Comissões** | `https://ckan.al.sp.gov.br/api/3/action/package_show?id=presenca-nas-comissoes` | JSON/XML | ✅ **200 OK** |
| **Lotação de Servidores** | `https://ckan.al.sp.gov.br/api/3/action/package_show?id=lotacoes-dos-servidores` | JSON/XML | ✅ **200 OK** |

---

## 3. Análise Detalhada por Eixo

### 3.1. Eixo Gastos (Despesas de Gabinete): Nível de Maturidade Alto
Diferente da ALERJ (que só fornece PDFs fechados), a ALESP expõe um JSON aberto com o histórico completo de reembolsos da verba indenizatória:

```json
{
  "id": 6,
  "ano": 2026,
  "mes": 8,
  "matricula": 300188,
  "deputado": "Barros Munhoz",
  "valor": 282.5,
  "tipo": "PJ",
  "cnpj": "43283811001393",
  "fornecedor": "KALUNGA COM. E IND. GRÁFICA LTDA."
}
```

* **Potencial de Auditoria:** Permite calcular o total gasto por deputado, categorias de despesa e realizar cruzamento societário com o QSA da Receita Federal ([AD-021](../.specs/STATE.md)) para identificar eventuais incompatibilidades de fornecedores.
* **Limitação:** Ao contrário da CEAP da Câmara dos Deputados, o dump não traz a URL direta do espelho da nota fiscal ou recibo escaneado.

### 3.2. Eixo Votações Nominais: Parcial (Comissões Sim, Plenário Web)
* **Comissões Permanentes:** A ALESP disponibiliza o dataset `votacoes-nas-comissoes` com voto individual registrado ("Favorável ao parecer", "Contrário", "Abstenção") com ID do deputado e ID da proposição.
* **Plenário Geral:** As deliberações em plenário (PEC estadual, projetos de lei do governador) não possuem dump consolidado no CKAN até o momento. A consulta pública existe na interface web, exigindo raspagem pontual para temas curados.

### 3.3. Eixo Patrimônio & Eleições: Totalmente Coberto (TSE)
* A Justiça Eleitoral (TSE) cobre os **94 deputados estaduais eleitos em São Paulo** (2022 e pleito 2026) com dados de bens, partido e votação no estado.

---

## 4. Matriz Comparativa: RJ (ALERJ) vs. SP (ALESP) vs. Federal (Câmara)

| Dimensão | Federal (Câmara) | SP (ALESP) | RJ (ALERJ) |
| :--- | :---: | :---: | :---: |
| **Portal de Dados Abertos** | Swagger REST API / Dumps CSV | Portal CKAN / JSON / XML | Inexistente (DNS nulo) |
| **Despesas Estruturadas** | Sim (com link da NF) | Sim (JSON com CNPJ/fornecedor) | Não (apenas relatórios em PDF) |
| **Votações em Plenário** | Sim (REST JSON com link) | Scraping de interface web | Não (atas em PDF no DOERJ) |
| **Votações em Comissões** | Sim (REST JSON) | Sim (`comissoes_votacoes.xml`) | Não estruturado |
| **Lotação / Servidores** | Sim (Dumps CSV) | Sim (`lotacoes-dos-servidores`) | Não estruturado |
| **Viabilidade de Ingestão** | **Nativa / Produção** | **Alta (para gastos e perfil)** | **Muito Baixa (OCR/PDFs)** |

---

## 5. Diretriz para Futuros Agentes e Contribuidores

* **Não há veto impeditivo:** Caso outro agente ou contribuidor queira implementar um pipeline para **São Paulo (ALESP)**, o caminho dos dados para gastos e identidade está aberto via API CKAN (`ckan.al.sp.gov.br`).
* **Abordagem Recomendada para um MVP de SP:**
  1. Consumir `despesas_gabinetes.json` para auditar a verba de gabinete dos 94 deputados de SP.
  2. Cruzar com a base do TSE para bens e eleições.
  3. Focar a curadoria de votações em temas emblemáticos selecionados via scraper da ordem do dia / painel eletrônico.
