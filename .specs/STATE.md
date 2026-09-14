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
  - 594 fichas geradas (513 deputados + 81 senadores na 57ª Legislatura).
  - 5 votações nominais da Câmara e Senado registradas com links duplos de verificabilidade.
  - Busca rápida unificada na Home com filtros por Casa, Partido e UF.
  - Testes automatizados de LGPD e integridade de fontes com 100% de sucesso.
  - Documentação de backlog de votações criada (`docs/backlog-votacoes.md`).
- **Foco Ativo (v1):**
  1. *Expansão do Catálogo:* Adicionar novos temas nacionais relevantes com votação nominal concluída (meta 10+ matérias).
  2. *Módulo Eleições 2026 (Roadmap Prioritário - AD-015):* Apoio ao eleitor para o pleito de 03/10/2026 (mandatários disputando eleição + bens declarados no TSE).
  3. *Gastos Parlamentares (CEAP/CEAPS):* Modelagem de despesas e notas fiscais oficiais.
- **Próximas Fases (v2 / v3):**
  4. *Destinação de Emendas Parlamentares (AD-016):* Rastreabilidade de valores empenhados/pagos e destino no Transferegov.br (v2).
  5. *Transparência Processual e Judicial (AD-017):* Inquéritos e ações penais no STF e base DataJud/CNJ (v3).
- **Bloqueios:** Nenhum.

---

## 4. Planejamento — Módulo Eleições 2026 (AD-015)

> **Decisão Arquitetural AD-015 (Escopo Eleitoral Focado no Congresso):**  
> Diante da proximidade do pleito nacional (03/10/2026), o portal incluirá apoio à consulta eleitoral com as seguintes diretrizes:
> 1. **Fidelidade ao Escopo Federal (AD-011):** Cobertura restrita a candidatos a Deputado Federal e Senador da República (cargos estaduais e municipais permanecem fora de escopo).
> 2. **Fase 1 (Mandatários & Reeleição):** Sinalização na ficha de quais dos 594 congressistas atuais estão disputando a reeleição ou outro cargo, incorporando os bens declarados no TSE (pleito 2026).
> 3. **Fase 2 (Novos Candidatos Federais):** Ingestão do dump oficial do TSE (DivulgaCandContas 2026) com busca dedicada por UF e cargo, exibindo bens declarados, número de urna e proposta, mantendo integridade e neutralidade (AD-004).

---

## 5. Planejamento — Módulo Destinação de Emendas Parlamentares (AD-016)

> **Decisão Arquitetural AD-016 (Rastreabilidade de Emendas Parlamentares):**  
> Exibir em cada ficha parlamentar a destinação dos recursos do Orçamento Geral da União (emendas individuais, de bancada e transferências especiais):
> 1. **Fontes Oficiais:** Portal da Transparência da CGU (`/api-de-dados/emendas`) e Transferegov.br (convênios e contratos de repasse).
> 2. **Sem Adjetivação:** Exibição quantitativa de valores autorizados, empenhados, liquidados e pagos, acompanhados do município/estado beneficiário e objeto do convênio, sempre linkando o documento fiscal e registro oficial.

---

## 6. Planejamento — Módulo Transparência Processual e Judicial (AD-017)

> **Decisão Arquitetural AD-017 (Integridade Processual e Presunção de Inocência):**  
> Para exibir processos em aberto de parlamentares em tribunais:
> 1. **Fontes Primárias Estritas:** Consulta ao STF (foro por prerrogativa de função para matéria penal) e base DataJud do CNJ.
> 2. **Impedimento de Homônimos:** O match DEVE ser 100% verificado por identificador unívoco para evitar atribuição indevida de processos judiciais de homônimos.
> 3. **Neutralidade e Presunção de Inocência:** Distinção obrigatória e inequívoca entre "Inquérito / Processo em Andamento" e "Condenação Transitada em Julgado". Processos sob segredo de justiça não são exibidos. Link direto para o andamento processual no tribunal de origem é mandatório.

