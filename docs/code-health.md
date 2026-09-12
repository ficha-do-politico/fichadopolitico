# Code Health & Arquitetura de Escala

**Última atualização:** 2026-09-12  
**Status:** Diagnóstico ativo para o ciclo MVP v0 → v1  
**Documentos de referência:** [MVP.md](../MVP.md), [AGENTS.md](../AGENTS.md), [.specs/STATE.md](../.specs/STATE.md)

---

## 1. Visão Geral

Este documento consolida o diagnóstico técnico de saúde do código, dívidas técnicas saneadas no MVP v0 (PR #12), gargalos ativos e as diretrizes arquiteturais necessárias para permitir o crescimento sustentável do portal (suporte ao Senado Federal, despesas da CEAP/CEAPS, declarações de patrimônio do TSE e expansão para 20–50 temas nacionais).

---

## 2. Diagnóstico Técnico

### 2.1. Dívidas Saneadas no MVP v0 (PR #12 / AD-013)

1. **Single Source of Truth para Curadoria Editorial:**
   - Criado `dados/catalogo/temas.json`. Elimina hardcode de temas em scripts executáveis (`build_site_data.py` e `discovery_votacoes.py`).
2. **Desacoplamento de Dados da Câmara:**
   - Dados migrados para `dados/camara/` (`deputados/`, `votacoes/` e dataset canônico estruturado `dados/camara/deputados.json`).
3. **Suíte Automatizada de Integridade e LGPD:**
   - Implementado `tests/test_data_integrity.py` validando AD-006 (verificabilidade e integridade referencial de URLs/votos) e AD-009 (ausência de CPF, email e telefone pessoal em datasets públicos).
4. **CI Ativo em Pull Requests:**
   - Criado `.github/workflows/ci.yml` executando a suíte de testes de dados e o build estático do Astro em cada PR para a branch `main`.

---

### 2.2. Gargalos Críticos Ativos (Foco v0 → v1)

1. **Anti-pattern de Persistência Intermediária em Markdown:**
   - `scripts/build_site_data.py` ainda lê e parseia 513 arquivos `.md` via expressões regulares (`re.search`) para gerar os JSONs do site.
   - *Impacto:* Fragilidade a caracteres especiais (ex.: pipes `|`), lentidão e perda de tipagem nativa. A geração deve consumir diretamente JSONs canônicos brutos da API.
2. **Ausência de Step de Compilação de Dados no CI:**
   - O workflow `.github/workflows/ci.yml` executa os testes sobre os JSONs já gerados, mas **não reexecuta** `python scripts/build_site_data.py`. Alterações no catálogo ou entradas podem quebrar a compilação sem falhar o CI.
3. **Injeção de 513 nós no DOM inicial e busca sem debounce:**
   - Em `site/src/pages/index.astro`, todos os parlamentares são instanciados diretamente no DOM e a busca client-side filtra todos os nós a cada evento `input`.
   - *Impacto:* Risco de engasgo em conexões móveis lentas, que aumentará com a adição do Senado (81 senadores).
4. **Tipagem e Contratos de Dados Frágeis no Frontend:**
   - A pasta `site/` não possui `tsconfig.json` ativo nem validação via `astro check`. Falta pasta canônica de contratos de tipo (`site/src/types/index.ts`).
5. **Duplicação de Assets Inline:**
   - Em `DeputadoCard.astro` e `[id].astro`, o SVG de avatar fallback embutido em `onerror` é repetido centenas de vezes no HTML gerado. Deve ser extraído para `site/public/avatar-placeholder.svg`.
6. **Duplicação e Fragilidade de Rotinas HTTP:**
   - `fetch_deputados.py` e `discovery_votacoes.py` duplicam chamadas `urllib`. `fetch_deputados.py` opera com delay fixo de 5s sem backoff exponencial em HTTP 429 nem checkpoint em disco.
7. **Ausência de Linters, Formatadores e Lock de Dependências Python:**
   - Não há ferramentas de lint/formatação configuradas (`ruff`, `eslint`, `prettier`). Não há `pyproject.toml` ou `requirements.txt` formalizando o ambiente Python.

---

## 3. Arquitetura Alvo para Escala (v1)

A estrutura modulariza **ingestão (ETL)**, **curadoria editorial**, **dados canônicos** e **frontend**:

```text
fichadopolitico/
├── .github/
│   └── workflows/
│       ├── deploy.yml              # Build e deploy no GitHub Pages
│       └── ci.yml                  # CI: testes, lint, types e reexecução do pipeline
├── .specs/                         # Decisões arquiteturais (ADRs) e especificações
│   └── STATE.md
├── dados/                          # Base de dados versionada
│   ├── catalogo/                   # Curadoria editorial (Single Source of Truth)
│   │   └── temas.json              # Lista auditável de temas nacionais e IDs oficiais
│   ├── camara/                     # Dados canônicos da Câmara dos Deputados
│   │   ├── deputados.json          # Dataset canônico completo dos 513 parlamentares
│   │   └── votacoes/               # Votações nominais extraídas ({id}.json)
│   ├── senado/                     # Dados canônicos do Senado Federal (planejado v1)
│   │   ├── senadores.json
│   │   └── votacoes/
│   └── tse/                        # Declarações e patrimônio histórico (planejado v1)
├── docs/                           # Documentação técnica e governança
│   ├── code-health.md              # Este documento
│   └── deploy-guia.md
├── scripts/                        # Pipeline ETL em Python
│   ├── core/                       # Módulo compartilhado (planejado v1)
│   │   ├── http_client.py          # Cliente HTTP resiliente (retries, rate limit 429)
│   │   └── models.py               # Schemas de validação de dados
│   ├── camara/                     # Ingestores da Câmara (migração das rotinas soltas)
│   │   ├── fetch_deputados.py
│   │   └── discovery_votacoes.py
│   ├── senado/                     # Ingestores do Senado (planejado v1)
│   └── build_site_data.py          # Compilador final para o site (consome JSON canônico)
├── site/                           # Aplicação Astro SSG
│   ├── src/
│   │   ├── components/             # Componentes de UI
│   │   ├── data/                   # Datasets estáticos compilados para o build
│   │   │   ├── deputados.json
│   │   │   └── temas.json
│   │   ├── layouts/
│   │   ├── pages/
│   │   │   ├── index.astro
│   │   │   ├── criterios.astro
│   │   │   └── deputado/
│   │   │       └── [id].astro
│   │   └── types/                  # Contratos de tipos em TypeScript (planejado v1)
│   │       └── index.ts
│   ├── public/
│   │   ├── favicon.svg
│   │   └── avatar-placeholder.svg  # Avatar padrão compartilhado
│   ├── tsconfig.json               # Configuração TypeScript estrita (planejado v1)
│   └── astro.config.mjs
└── tests/                          # Suíte de testes automatizados
    ├── test_data_integrity.py      # Testes de integridade, links oficiais e LGPD
    └── test_build_pipeline.py      # Teste de ponta a ponta da compilação de dados
```

---

## 4. Matriz de Priorização de Refatoração

| Fase | Ação Técnica | Status | Racional & Benefício |
| :--- | :--- | :---: | :--- |
| **Fase 1** | Isolar catálogo de temas em `dados/catalogo/temas.json` | ✅ Concluído (PR #12) | Centraliza curadoria editorial aberta sem misturar com código. |
| **Fase 1** | Reestruturar dados da Câmara em `dados/camara/` | ✅ Concluído (PR #12) | Prepara repositório para acomodar Senado e TSE. |
| **Fase 2** | Criar testes automatizados de LGPD e verificabilidade | ✅ Concluído (PR #12) | Blindagem contínua contra vazamento de dados e votos sem fonte. |
| **Fase 2** | Ativar CI com validação em Pull Requests | ✅ Concluído (PR #12) | Garante que PRs não quebrem integridade de dados nem build do site. |
| **Fase 2** | Eliminar parse de Markdown em `build_site_data.py` | ⏳ Pendente | Consumir JSONs canônicos diretamente; remover regex frágil. |
| **Fase 2** | Configurar `tsconfig.json` e types centrais no frontend | ⏳ Pendente | Previne inconsistências em tempo de compilação no Astro. |
| **Fase 3** | Modularizar cliente HTTP resiliente (`http_client.py`) | ⏳ Pendente | Reúso de rotinas com retries e backoff 429 para Câmara, Senado e TSE. |
| **Fase 3** | Otimizar busca e DOM em `index.astro` (debounce/render) | ⏳ Pendente | Garante fluidez no mobile quando a base atingir > 600 parlamentares. |
| **Fase 3** | Extrair SVG de avatar para `avatar-placeholder.svg` | ⏳ Pendente | Reduz tamanho do HTML gerado e elimina duplicação de inline SVG. |
| **Fase 3** | Incluir step de compilação de dados no CI | ⏳ Pendente | Garante que o pipeline ETL executa sem erros antes do build Astro. |
