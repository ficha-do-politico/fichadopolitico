# Code Health & Arquitetura do Repositório

> **Documentos de referência:** [STATE.md](../.specs/STATE.md), [MVP.md](../MVP.md), [AGENTS.md](../AGENTS.md)

---

## 1. Visão Geral da Arquitetura

O **Ficha do Político** opera em arquitetura desacoplada em 3 camadas, com compilação estática (SSG) pré-renderizada:

```
[APIs Oficiais / Dumps em Lote]
             │
             ▼ (1) Scripts ETL (Python + scripts/core/http_client.py)
[Base Canônica Versionada]
 ├── dados/catalogo/temas.json     (Single Source of Truth editorial)
 ├── dados/camara/                 (deputados.json, votacoes/*.json, ceap/)
 ├── dados/senado/                 (senadores.json, votacoes/*.json, ceaps/)
 └── dados/tse/                    (candidatos_2026.json, bens/)
             │
             ▼ (2) Compilador (scripts/build_site_data.py)
[site/src/data/ (Datasets de Build)]
             │
             ▼ (3) Astro SSG + Tailwind CSS
[site/dist/ (594+ páginas estáticas prontas para deploy em CDN)]
```

---

## 2. Padrões Mandatórios de Qualidade

1. **Tipagem e Contratos:**
   - Frontend tipado estritamente via TypeScript (`site/src/types/index.ts` e `site/tsconfig.json`). O comando `npm --prefix site run check` não deve produzir erros ou warnings.
   - Schemas de dados canônicos consumidos diretamente em JSON, sem persistência intermediária em Markdown ou parsing por regex.

2. **Integridade de Dados e LGPD:**
   - Todo dataset passa pela suíte automatizada `tests/test_data_integrity.py`.
   - É terminantemente proibido expor CPF, telefone pessoal, email funcional/pessoal ou endereço nos datasets compilados (`AD-009`).
   - Todo voto e gasto associado a parlamentar exige link direto para fonte oficial primária (`AD-006`).

3. **Tooling & Formatação:**
   - Gerenciamento de ambiente Python via `uv` com `pyproject.toml` e `uv.lock`.
   - Lint e formatação estrita via `ruff` (`uv run ruff check` e `uv run ruff format --check`).

4. **Resiliência de Ingestão:**
   - Requisições a APIs públicas devem utilizar `scripts/core/http_client.py` com tratamento de rate limit (HTTP 429 backoff) e retries automáticos para falhas transitórias de rede.
   - Para volumes massivos (CEAP, despesas e bens), priorizar dumps em lote (.zip / .csv) em vez de varreduras por centenas de requisições individuais.

---

## 3. Gargalos e Desafios Técnicos Ativos

1. **Volume de Dados vs. Build Time:**
   - À medida que o catálogo expande para 20+ temas e novas fontes (emendas CGU e processos DataJud), os datasets em `site/src/data/` aumentam. Manter payloads otimizados para não inflar o tamanho do bundle JavaScript transferido ao cliente.
2. **Normalização de Nomes e Desambiguação:**
   - Cruzamentos bicamerais e eleitorais (Câmara x Senado x TSE) exigem identificadores unívocos (código parlamentar, SQ_CANDIDATO) para blindar contra homônimos em futuras integrações judiciais (STF/CNJ).
