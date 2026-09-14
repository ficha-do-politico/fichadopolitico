# STATE — Ficha do Político

> **Status:** v1 em expansão (Legislativo Federal Bicameral)  
> **Última atualização:** 2026-09-13  
> **Base de Decisões:** AD-001 a AD-014

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
  - 5 votações nominais da Câmara registradas com links duplos de verificabilidade.
  - Busca rápida unificada na Home com filtros por Casa, Partido e UF.
  - Testes automatizados de LGPD e integridade de fontes com 100% de sucesso.
- **Foco Ativo:**
  1. *Votações Nominais no Senado:* Mapear IDs de votações oficiais no Senado para os temas do catálogo e ingestão de votos.
  2. *Expansão do Catálogo:* Adicionar novos temas nacionais relevantes (meta 10+ matérias).
  3. *Gastos Parlamentares (CEAP/CEAPS):* Modelagem de despesas e notas fiscais oficiais.
- **Bloqueios:** Nenhum.
