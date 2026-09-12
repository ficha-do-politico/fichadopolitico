# Code Health & Arquitetura de Escala

**Última atualização:** 2026-09-12  
**Status:** Diagnóstico ativo para o ciclo MVP v0 → v1  
**Documentos de referência:** [MVP.md](../MVP.md), [AGENTS.md](../AGENTS.md), [.specs/STATE.md](../.specs/STATE.md)

---

## 1. Visão Geral

Este documento consolida o diagnóstico técnico de saúde do código, dívidas técnicas acumuladas no desenvolvimento do MVP v0 e as diretrizes arquiteturais necessárias para permitir o crescimento sustentável do portal (suporte ao Senado Federal, despesas da CEAP/CEAPS, declarações de patrimônio do TSE e expansão para 20–50 temas nacionais).

---

## 2. Diagnóstico Técnico do MVP v0

O MVP v0 atingiu com sucesso seus objetivos funcionais:
- Aplicação SSG em Astro com Tailwind CSS com performance e pré-renderização completas ([AD-012](../.specs/STATE.md)).
- Catálogo inicial de 5 votações nominais de relevância pública nacional no Plenário.
- Cobertura dos 513 deputados federais da 57ª legislatura.
- Links oficiais de origem em todas as páginas para garantir verificabilidade ([AD-006](../.specs/STATE.md)).

Contudo, para que a base de código suporte as próximas fases sem necessidade de reescritas traumáticas, foram identificados os seguintes pontos de atenção:

### 2.1. Ingestão e Modelo de Dados (Gargalo Crítico)

1. **Anti-pattern de persistência intermediária em Markdown:**
   - Em `scripts/fetch_deputados.py`, o JSON estruturado da API oficial da Câmara é convertido em tabelas Markdown (`dados/deputados/{id}.md`).
   - Em `scripts/build_site_data.py`, esse mesmo Markdown é parseado via expressões regulares (`re.search`) para reconstruir objetos Python e exportar o JSON do frontend.
   - *Impacto:* Fragilidade a alterações de caracteres (ex.: pipes `|` ou quebras de linha), perda de tipos primitivos e lentidão. Com o volume de dados do Senado e da CEAP, esse modelo se torna insustentável.

2. **Ausência de Single Source of Truth para Curadoria:**
   - A lista de temas e metadados oficiais está hardcoded em `scripts/build_site_data.py` (`TEMAS_CATALOGO`) e replicada em `scripts/discovery_votacoes.py`.
   - *Impacto:* Mistura de código executável com curadoria editorial. Adicionar ou retificar temas exige alterar scripts Python.

3. **Duplicação de rotinas HTTP sem resiliência:**
   - `fetch_deputados.py` e `discovery_votacoes.py` possuem implementações separadas de requisição HTTP via `urllib`.
   - `fetch_deputados.py` usa delay fixo síncrono de 5s sem retentativas em erro 429 ou checkpoint em disco, tornando a execução completa demorada (~42 min) e vulnerável a interrupções.

### 2.2. Frontend e Performance (Astro)

1. **Injeção de 513 nós no DOM inicial:**
   - Em `site/src/pages/index.astro`, todos os 513 parlamentares são instanciados no DOM. A busca client-side percorre todos os nós no evento `input` sem `debounce`.
   - *Impacto:* Risco de travamento em dispositivos móveis e degradação de layout quando novos parlamentares (Senado) forem incorporados.

2. **Tipagem e Contratos de Dados Frágeis:**
   - A pasta `site/` não possui `tsconfig.json` ativo. A inferência de tipos é fragmentada entre props isoladas de componentes Astro.
   - Falta uma pasta canônica de contratos de tipo (`site/src/types/index.ts`).

3. **Duplicação de Assets Inline:**
   - Em `DeputadoCard.astro`, o fallback de avatar com SVG embutido em `onerror` é repetido centenas de vezes no HTML final gerado. Deve ser extraído para um asset estático compartilhado.

### 2.3. Governança, Testes e CI/CD

1. **Ausência Total de Testes Automatizados:**
   - Não há suíte de testes unitários ou de integração no repositório.
   - *Risco LGPD ([AD-009](../.specs/STATE.md)):* Sem testes automatizados, não há garantia contínua de que campos sensíveis (CPF, telefone pessoal, email) não vazem acidentalmente para os datasets públicos compilados.
   - *Risco de Verificabilidade ([AD-006](../.specs/STATE.md)):* Não há validação automatizada de que URLs e códigos de votação estão íntegros e acessíveis.

2. **CI Desconectada do Pipeline de Dados:**
   - O workflow `.github/workflows/deploy.yml` compila o site diretamente a partir de JSONs estáticos versionados manualmente no Git, sem validar ou reexecutar o pipeline de dados. Não há checagem de Pull Requests configurada.

---

## 3. Arquitetura de Pastas para Escala

A estrutura recomendada desacopla **ingestão (ETL)**, **curadoria editorial**, **dados canônicos** e **frontend**:

```text
fichadopolitico/
├── .github/
│   └── workflows/
│       ├── deploy.yml              # Build e deploy no GitHub Pages
│       └── ci.yml                  # Validações de PR: lint, tipos e testes de dados
├── .specs/                         # Decisões arquiteturais (ADRs) e especificações
│   └── STATE.md
├── dados/                          # Base de dados versionada
│   ├── catalogo/                   # Curadoria editorial (Single Source of Truth)
│   │   └── temas.json              # Lista auditável de temas nacionais e IDs oficiais
│   ├── camara/                     # Dados canônicos da Câmara dos Deputados
│   │   ├── deputados.json          # Dataset estruturado completo dos 513 parlamentares
│   │   └── votacoes/               # Votações nominais extraídas ({id}.json)
│   ├── senado/                     # Dados canônicos do Senado Federal (planejado v1)
│   │   ├── senadores.json
│   │   └── votacoes/
│   └── tse/                        # Declarações e patrimônio histórico (planejado v1)
├── docs/                           # Documentação técnica e governança
│   ├── code-health.md              # Este documento
│   └── deploy-guia.md
├── scripts/                        # Pipeline ETL em Python
│   ├── core/                       # Módulo compartilhado
│   │   ├── __init__.py
│   │   ├── http_client.py          # Cliente HTTP resiliente (retries, rate limit)
│   │   └── models.py               # Schemas de dados (Pydantic / TypedDict)
│   ├── camara/                     # Ingestores específicos da Câmara
│   │   ├── fetch_deputados.py
│   │   └── discovery_votacoes.py
│   ├── senado/                     # Ingestores do Senado (planejado v1)
│   └── build_site_data.py          # Compilador final para o site (com validação LGPD)
├── site/                           # Aplicação Astro SSG
│   ├── src/
│   │   ├── components/             # Componentes de UI
│   │   ├── data/                   # Datasets estáticos compilados para o build
│   │   │   ├── parlamentares.json
│   │   │   └── temas.json
│   │   ├── layouts/
│   │   ├── pages/
│   │   │   ├── index.astro
│   │   │   ├── criterios.astro
│   │   │   └── deputado/
│   │   │       └── [id].astro
│   │   └── types/                  # Contratos de tipos em TypeScript
│   │       └── index.ts
│   ├── public/
│   │   └── avatar-placeholder.svg  # Avatar padrão estático compartilhado
│   ├── tsconfig.json               # Configuração TypeScript
│   └── astro.config.mjs
└── tests/                          # Suíte de testes de integridade
    ├── test_lgpd_compliance.py     # Garante ausência de dados sensíveis privados
    ├── test_verificabilidade.py    # Garante links oficiais válidos para todos os votos
    └── test_build_pipeline.py      # Testa integridade da compilação de dados
```

---

## 4. Matriz de Priorização de Refatoração

| Fase | Ação Técnica | Racional & Benefício |
| :--- | :--- | :--- |
| **Fase 1 (Imediata)** | Isolar catálogo de temas em `dados/catalogo/temas.json` | Elimina hardcode e centraliza curadoria editorial aberta. |
| **Fase 1 (Imediata)** | Reestruturar dados da Câmara para JSON canônico (`dados/camara/`) | Elimina o parse de Markdown por regex e prepara a chegada de novas fontes. |
| **Fase 2 (Curto Prazo)** | Criar testes automatizados de LGPD e verificabilidade (`tests/`) | Blinda o projeto contra vazamento de dados privados e votos sem fonte. |
| **Fase 2 (Curto Prazo)** | Configurar `tsconfig.json` e types centrais no frontend Astro | Previne inconsistências em tempo de compilação. |
| **Fase 3 (Médio Prazo)** | Modularizar scripts de ingestão (`scripts/core/http_client.py`) | Reúso de lógica de rede e retries para os coletores do Senado e TSE. |
| **Fase 3 (Médio Prazo)** | Adicionar debounce e otimizações de busca em `index.astro` | Garante fluidez no mobile quando a base atingir > 600 parlamentares. |
