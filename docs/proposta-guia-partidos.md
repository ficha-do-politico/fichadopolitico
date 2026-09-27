# Especificação & Backlog: Guia de Partidos Auditável e Neutro

> **Status:** Proposta / Backlog (v2)  
> **Pilares:** Apartidarismo estrito ([AD-004](file:///C:/gitrepos/fichadopolitico/.specs/STATE.md#L29)) e Verificabilidade em Fonte Oficial Primária ([AD-006](file:///C:/gitrepos/fichadopolitico/.specs/STATE.md#L32)).

---

## 1. Motivação & Contexto Cívico

Em plataformas de transparência e canais populares, partidos políticos frequentemente recebem rótulos informais (ex.: *"camaleão"*, *"pragmático"*, *"radical"*) ou espectros subjetivos (*"centro-direita"*, *"esquerda"*).

Para a **Ficha do Político**, adjetivações de terceiros ou enquadramentos ideológicos opinativos são terminantemente vedados pelas diretrizes de apartidarismo e neutralidade. O propósito de um Guia de Partidos no projeto é fornecer **dados crus, fatos verificáveis e autodeclarações oficiais**, permitindo que o cidadão audite as legendas com base no que elas registraram em cartório/TSE e em como suas bancadas efetivamente votaram e gastaram recursos públicos.

---

## 2. Estrutura Canônica da Ficha de Cada Partido

Toda página ou ficha partidária deve ser estruturada sobre cinco blocos rigorosamente verificáveis:

### 2.1. Identidade Oficial & Registro (TSE)
- **Número Eleitoral:** Número de urna oficial registrado no TSE (ex.: 13, 15, 22, 30, 50).
- **Data de Registro/Homologação:** Data oficial da concessão do registro definitivo pelo Tribunal Superior Eleitoral.
- **Estatuto Partidário Oficial:** Link permanente e rastreável para a íntegra do estatuto arquivado no repositório oficial do TSE (`tse.jus.br`).
- **Presidente Nacional Oficial:** Dirigente registrado perante a Justiça Eleitoral (SGIP/TSE).

### 2.2. Autodeclaração Estatutária (Princípios Oficiais)
- Em vez de a plataforma definir a ideologia da agremiação, deve-se citar textualmente o artigo de abertura do próprio estatuto aprovado pela Justiça Eleitoral:
  > *"Conforme o art. 1º do estatuto registrado no TSE, o partido declara ter como princípios fundamentais..."*
- Citação literal, sem glosas, sem adjetivação externa e com referência à página/artigo do documento registrado.

### 2.3. Força Parlamentar Atual (Congresso Nacional)
- Número de **Deputados Federais** em exercício (Câmara dos Deputados).
- Número de **Senadores da República** em exercício (Senado Federal).
- Porcentagem de ocupação das cadeiras do Congresso Nacional.

### 2.4. Comportamento e Coesão em Votações-Chave
- Exibição da distribuição agregada de votos da bancada (Sim / Não / Abstenção / Ausente) nas votações nominais catalogadas pela Ficha do Político (10 na Câmara e 9 no Senado).
- Comparação entre a **orientação oficial da liderança da bancada** registrada em ata e o **voto real dos parlamentares**, evidenciando fidelidade e dissidências sem juízo de valor.

### 2.5. Volume de Recursos Públicos sob Gestão da Bancada
- **Cota Parlamentar (CEAP/CEAPS):** Total consolidado de gastos operacionais reembolsados aos deputados e senadores da bancada no exercício.
- **Emendas Parlamentares:** Montante total de emendas pagas da 57ª Legislatura destinadas por parlamentares da legenda (discriminando emendas individuais e de bancada, via dados abertos da CGU).

---

## 3. Checklist Técnico de Implementação

- [x] Ingestão do cadastro partidário oficial do TSE (`dados/tse/partidos.json` via `scripts/tse/build_partidos_base.py`).
- [x] Compilação de agregados por partido no script de build (`scripts/build_site_data.py` gerando `site/src/data/partidos.json`).
- [x] Testes de conformidade, ausência de adjetivação/scores ideológicos e integridade matemática em `tests/test_partidos.py`.
- [x] Fase 2: Rota estática `/partidos` (visão geral e comparativa de agremiações no Astro SSG).
- [x] Fase 3: Geração de rotas estáticas `/partido/[sigla]` via Astro SSG com layout detalhado e matriz de votações nominais.
