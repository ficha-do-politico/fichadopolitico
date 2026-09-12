# Plano de Implementação — MVP v0 (Frontend & Pipeline de Dados)

> **Status:** Em planejamento / aguardando execução  
> **Referência de Requisitos:** [`.specs/features/mvp-v0/spec.md`](spec.md) (MVP-01 a MVP-17)  
> **Decisões Relacionadas:** AD-001 a AD-011 em [`.specs/STATE.md`](../../STATE.md)  
> **Data:** 2026-09-12  

---

## 1. Objetivo

Transformar os dados de discovery consolidados (513 deputados federais e as 5 primeiras votações nominais curadas) em uma aplicação web estática, responsiva, rápida e apartidária, pronta para ser publicada com domínio próprio (`.com.br`) em infraestrutura gratuita de alta disponibilidade.

---

## 2. Decisão Arquitetural de Stack: Por que Astro SSG e não Vanilla JS puro?

| Critério | Vanilla JS puro (SPA ou HTML solto) | Astro SSG (Static Site Generation) | Impacto para o Projeto |
|---|---|---|---|
| **Compartilhamento Social (WhatsApp/X)** | ❌ Péssimo. WhatsApp e robôs não executam JS para ver o card de um deputado específico; todos teriam a mesma thumbnail genérica da home. | ✅ Perfeito. Cada uma das 513 páginas `/deputado/[id]` tem suas tags `<meta property="og:title">` e `<meta property="og:image">` pré-renderizadas com a foto e nome do parlamentar. | **Crítico:** se um cidadão mandar a ficha de um deputado no grupo da família ou no X, o card com foto e nome aparece formatado na hora. |
| **Templates e Manutenção** | ❌ Complexo. Duplicação de código HTML em 513 arquivos ou dezenas de linhas de manipulação manual de DOM (`document.createElement`). | ✅ Componentes reutilizáveis limpos (`Header.astro`, `VotoBadge.astro`, `DeputadoCard.astro`). | Qualquer ajuste visual ou novo campo é editado em um único componente. |
| **Performance e Custo** | Depende de runtime no cliente. | ✅ Zero JavaScript desnecessário no cliente. A página do deputado é puro HTML/CSS pré-compilado, abrindo instantaneamente em conexões 3G. | Nota 100/100 no Google Lighthouse e carregamento sub-segundo. |
| **Deploy e Hospedagem** | Simples. | ✅ Idêntico: o build gera uma pasta de arquivos estáticos (`site/dist/`), que roda de graça no Cloudflare Pages, Vercel ou GitHub Pages. | Zero custo de servidor ou banco de dados ativo. |

**Conclusão:** Astro oferece a simplicidade e leveza do HTML estático puro, mas com o poder de templates e geração de 513 páginas individuais otimizadas para redes sociais e buscadores.

---

## 3. Arquitetura em Três Camadas

```
[Camada 1: Ingestão de Dados Oficiais]
  dados/deputados/*.md (513 parlamentares da 57ª legislatura)
  dados/votacoes/*.json (5 votações com votos nominais e ausentes)
           │
           ▼
[Camada 2: Script de Compilação (scripts/build_site_data.py)]
  Valida integridade, vincula votos por ID de deputado e gera:
  ├── site/src/data/deputados.json (~45 KB gzip)
  └── site/src/data/temas.json (<5 KB)
           │
           ▼
[Camada 3: Aplicação Web Astro (site/)]
  ├── src/pages/index.astro (Home com busca client-side instantânea)
  ├── src/pages/deputado/[id].astro (513 páginas geradas estaticamente via getStaticPaths)
  └── src/pages/criterios.astro (Transparência editorial e critérios públicos)
```

---

## 4. Estrutura de Diretórios e Arquivos

```
fichadopolitico/
├── scripts/
│   ├── fetch_deputados.py        (já existente)
│   ├── discovery_votacoes.py     (já existente)
│   └── build_site_data.py        (novo: compila markdown/json em datasets otimizados para o site)
├── site/
│   ├── package.json
│   ├── astro.config.mjs
│   ├── tailwind.config.cjs
│   ├── public/
│   │   ├── favicon.svg
│   │   └── robots.txt
│   └── src/
│       ├── data/                 (JSONs compilados pelo build_site_data.py)
│       │   ├── deputados.json
│       │   └── temas.json
│       ├── layouts/
│       │   └── Layout.astro      (Navbar, footer, SEO/OpenGraph global)
│       ├── components/
│       │   ├── Navbar.astro
│       │   ├── Footer.astro
│       │   ├── SearchDeputados.astro (Input de busca instantânea reativo)
│       │   ├── DeputadoCard.astro
│       │   └── VotoBadge.astro   (Renderiza Sim/Não/Abstenção/Obstrução/Ausente com cores neutras)
│       └── pages/
│           ├── index.astro       (Página inicial: Hero + Busca + Grid)
│           ├── deputado/
│           │   └── [id].astro    (Ficha individual: dados oficiais + tabela de votos + links de fonte)
│           └── criterios.astro   (Declaração de princípios apartidários e critérios de curadoria)
```

---

## 5. Especificação das Telas e Fluxos

### 5.1. Tela Inicial (`/`) — Requisitos MVP-01, MVP-13, MVP-14
- **Hero:**
  - Título: *Ficha do Político*
  - Subtítulo: *A maneira mais simples e direta de saber como seu deputado federal votou nas decisões cruciais do país.*
  - Badge: *100% apartidário • Fonte oficial: Câmara dos Deputados*
- **Campo de Busca Hero:**
  - Input centralizado com placeholder: *"Digite o nome do deputado, partido ou estado (ex: Nikolas, Tabata, SP, PL)..."*
  - Filtro em tempo real no cliente com debounce (pesquisa por nome eleitoral, nome civil, partido e sigla de UF).
  - Contador dinâmico: *"Exibindo 513 de 513 deputados federais"*.
- **Grid de Cards de Deputados:**
  - Foto oficial com fallback.
  - Nome eleitoral em destaque.
  - Tag com `Partido` • `UF`.
  - Link clicável direto para a ficha `/deputado/[id]`.

### 5.2. Ficha do Deputado (`/deputado/[id]`) — Requisitos MVP-02, MVP-03, MVP-04, MVP-10, MVP-11, MVP-12
- **Cabeçalho de Identificação Oficial:**
  - Foto oficial do parlamentar.
  - Nome eleitoral e nome civil completo.
  - Partido e Estado (UF).
  - Link externo com ícone: *"Ver perfil oficial na Câmara dos Deputados ↗"* (`https://www.camara.leg.br/deputados/{id}`).
- **Alerta de Contexto:**
  - Aviso explicativo: *"Esta ficha exibe o voto oficial registrado no Plenário da Câmara dos Deputados em um conjunto curado de matérias de grande relevância nacional. Não representa o histórico total de tramitações do parlamentar."* ([Critérios de seleção](criterios)).
- **Tabela / Lista de Votações Curadas (5 temas seed):**
  Para cada tema:
  - **Título do tema:** (ex.: *Reforma Tributária - 1º Turno*, *Marco Temporal das Terras Indígenas*, etc.).
  - **Proposição:** Identificador formal (ex.: `PEC 45/2019`, `PL 490/2007`) e data da votação.
  - **Voto do Deputado:** Badge com rótulo fiel aos dados da Câmara:
    - `Sim` (verde neutro)
    - `Não` (vermelho neutro)
    - `Abstenção` (amarelo neutro)
    - `Obstrução` (laranja neutro)
    - `Artigo 17` (cinza com tooltip explicativo sobre o voto do Presidente)
    - `Não votou / Ausente` (cinza neutro)
  - **Rastreabilidade Obrigatória (AGENTS.md §3.1):**
    - Link oficial 1: *Registro oficial da votação (Câmara) ↗*
    - Link oficial 2: *Íntegra da proposição legislativa ↗*

### 5.3. Página de Critérios e Transparência (`/criterios`) — Requisitos MVP-15, MVP-16
- Declaração explícita de apartidarismo: sem adjetivos, sem notas, sem classificação ideológica.
- Metodologia de seleção de matérias: relevância pública nacional, cobertura ampla da imprensa, votações de mérito em Plenário.
- Convite aberto à comunidade: instruções para sugerir novos temas via Pull Request no repositório.

---

## 6. Plano de Tarefas & Sequência de Execução

1. **Task 1 (Data Pipeline):** Criar `scripts/build_site_data.py` para processar `dados/deputados/*.md` e `dados/votacoes/*.json` e exportar `deputados.json` e `temas.json`.
2. **Task 2 (Scaffold Web):** Inicializar projeto Astro com Tailwind CSS na pasta `site/`, configurar layouts básicos e rotas estáticas.
3. **Task 3 (Componentes Core):** Construir componentes `Navbar`, `Footer`, `VotoBadge` e `DeputadoCard`.
4. **Task 4 (Páginas):**
   - Construir `site/src/pages/index.astro` com busca rápida client-side.
   - Construir `site/src/pages/deputado/[id].astro` com renderização estática dos 513 parlamentares.
   - Construir `site/src/pages/criterios.astro`.
5. **Task 5 (Validação e Build):** Rodar `npm run build` no `site/`, testar geração de 100% das 513 páginas estáticas e verificar integridade de links e acessibilidade.
6. **Task 6 (Deploy Docs):** Documentar instruções para conectar ao Cloudflare Pages / Vercel e configurar o domínio `.com.br`.
