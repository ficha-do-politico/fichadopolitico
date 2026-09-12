# Discovery Técnico: Votações Nominais da Câmara dos Deputados

**Data de Realização:** 2026-09-12  
**Contexto:** MVP v0 — Ficha do Político  
**Requisitos Atendidos:** DISC-04, DISC-05, DISC-06, DISC-07 ([spec.md](../.specs/features/api-discovery/spec.md))  
**Fonte Oficial Primária:** API de Dados Abertos da Câmara dos Deputados (`dadosabertos.camara.leg.br/api/v2`)

---

## 1. Resumo Executivo & Conclusões Técnicas

1. **Viabilidade do MVP v0:** É 100% viável ligar qualquer tema nacional importante ao voto nominal de cada um dos deputados federais sem intermediários ou raspagem de tela. A API REST da Câmara fornece endpoints oficiais estruturados.
2. **O "Pulo do Gato" sobre Ausências:** A API da Câmara **NÃO retorna** os deputados ausentes no endpoint `/votacoes/{id}/votos`. O endpoint retorna apenas os parlamentares que registraram voto formal. Portanto, a regra de negócio para a ficha é: se um deputado em exercício na data da votação não consta no payload de votos, seu status factual é **`Não votou / Ausente`**.
3. **Descoberta sobre Temas do Seed Inicial (Alerta ao Time):**
   - A **PEC da Escala 6×1** e a **PEC da Segurança Pública** (mencionadas no rascunho inicial do [MVP.md](../MVP.md)) **não possuem votação nominal no Plenário da Câmara até o momento** (estiveram em fase de coleta de assinaturas/comissões). Pela regra do [AGENTS.md](../AGENTS.md) §3.1 ("zero afirmação factual sem fonte rastreável"), temas sem votação plenária concluída não podem entrar como voto sim/não.
   - Foram identificadas e mapeadas com sucesso votações de impacto nacional massivo da 57ª Legislatura: **Reforma Tributária (PEC 45/2019)**, **Marco Temporal (PL 490/2007)**, **PEC da Anistia aos Partidos (PEC 9/2023)** e **Taxação das Compras Internacionais / Programa Mover (PL 914/2024)**.

---

## 2. Fluxo Completo de Consulta (Da Ideia ao Voto Nominal)

```
[Tema / Matéria Legislativa]
         │
         ▼ (1) GET /proposicoes?siglaTipo={TIPO}&numero={NUM}&ano={ANO}
[Proposição Oficial (ID: ex. 2196833)]
         │
         ▼ (2) GET /proposicoes/{id}/votacoes
[Histórico de Votações (dezenas de itens)]
         │
         ▼ (3) Heurística de Mérito (Filtro: siglaOrgao == 'PLEN', 1º/2º turno ou Substitutivo)
[ID da Votação Decisiva (ex. 2196833-326)]
         │
         ├──────────────────────────────────────────────┐
         ▼ (4) GET /votacoes/{id}/votos                  ▼ (5) GET /votacoes/{id}/orientacoes
[Lista Nominal de Votos por Deputado]          [Orientações de Governo/Oposição e Bancadas]
(Sim, Não, Abstenção, Obstrução, Artigo 17)    (Sim, Não, Liberado, Obstrução)
```

---

## 3. Especificação dos Endpoints

### 3.1. Localização da Proposição
- **Endpoint:** `GET /proposicoes`
- **Query Params:** `siglaTipo` (string), `numero` (int), `ano` (int)
- **Exemplo:** `https://dadosabertos.camara.leg.br/api/v2/proposicoes?siglaTipo=PEC&numero=45&ano=2019`
- **Campos Relevantes:**
  - `dados[0].id`: ID numérico oficial da proposição (ex: `2196833`).
  - `dados[0].ementa`: Descrição legal oficial da matéria.

### 3.2. Histórico de Votações da Proposição
- **Endpoint:** `GET /proposicoes/{id}/votacoes`
- **Exemplo:** `https://dadosabertos.camara.leg.br/api/v2/proposicoes/2196833/votacoes`
- **Campos Relevantes no Array:**
  - `id`: Identificador único da votação (formato: `{idProposicao}-{seq}`, ex: `2196833-326`).
  - `dataHoraRegistro`: Timestamp ISO (ex: `2023-07-06T21:49:55`).
  - `siglaOrgao`: Sigla do colegiado (`PLEN` para Plenário, `CCJC` para Comissão, etc.).
  - `descricao`: Texto oficial do resultado e do objeto votado.
  - `aprovacao`: Indicador de aprovação (geralmente `1` para aprovado, `0` para rejeitado, ou `null`).

### 3.3. Detalhe da Votação
- **Endpoint:** `GET /votacoes/{id}`
- **Exemplo:** `https://dadosabertos.camara.leg.br/api/v2/votacoes/2196833-326`
- **Campos Relevantes:**
  - `siglaOrgao`: Garantir que é `PLEN`.
  - `uriEvento`: Link para a reunião/sessão legislativa (ex: evento `68337`).
  - `proposicoesAfetadas`: Lista com metadados das matérias vinculadas.

### 3.4. Votos Nominais dos Deputados
- **Endpoint:** `GET /votacoes/{id}/votos`
- **Exemplo:** `https://dadosabertos.camara.leg.br/api/v2/votacoes/2196833-326/votos`
- **Estrutura de Cada Item:**
  ```json
  {
    "tipoVoto": "Sim",
    "dataRegistroVoto": "2023-07-06T21:48:10",
    "deputado_": {
      "id": 141398,
      "uri": "https://dadosabertos.camara.leg.br/api/v2/deputados/141398",
      "nome": "Carlos Zarattini",
      "siglaPartido": "PT",
      "uriPartido": "https://dadosabertos.camara.leg.br/api/v2/partidos/36844",
      "siglaUf": "SP",
      "idLegislatura": 57,
      "urlFoto": "https://www.camara.leg.br/internet/deputado/bandep/141398.jpg",
      "email": "dep.carloszarattini@camara.leg.br"
    }
  }
  ```

### 3.5. Orientações de Bancada / Lideranças
- **Endpoint:** `GET /votacoes/{id}/orientacoes`
- **Exemplo:** `https://dadosabertos.camara.leg.br/api/v2/votacoes/345311-270/orientacoes`
- **Estrutura:**
  ```json
  {
    "orientacaoVoto": "Sim",
    "codTipoLideranca": "B",
    "siglaPartidoBloco": "Governo"
  }
  ```
  Permite mostrar na ficha se o deputado seguiu ou divergiu da orientação da liderança de seu partido/bloco ou do Governo/Oposição.

---

## 4. Dicionário de Tipos de Voto (`tipoVoto`)

Observado empiricamente nas votações nominais da 57ª Legislatura:

| Valor na API (`tipoVoto`) | Significado Regimental | Como Exibir na Ficha |
|---|---|---|
| `Sim` | Voto a favor da matéria/substitutivo | **Sim** (verde/neutro) |
| `Não` | Voto contrário à matéria/substitutivo | **Não** (vermelho/neutro) |
| `Abstenção` | O parlamentar registrou presença e declarou abstenção formal | **Abstenção** |
| `Artigo 17` | Aplicação do Art. 17 do Regimento Interno: o Presidente da Câmara só vota em caso de empate ou quórum qualificado | **Artigo 17 (Presidência)** |
| `Obstrução` | A bancada ou parlamentar registrou obstrução para impedir quórum | **Obstrução** |
| *(Não listado no payload)* | O parlamentar não registrou voto no painel eletrônico durante a chamada nominal | **Não votou / Ausente** |

---

## 5. Heurística de Seleção: Votação Decisiva de Mérito (DISC-07)

Uma proposição de grande repercussão pode ter de **20 a mais de 100 votações** registradas na API. A grande maioria é ruído procedimental.

### Regra Algorítmica de Filtro:
1. **Órgão Deliberativo:** Deve ter `siglaOrgao == 'PLEN'`. Votações em comissões temáticas (`CCJC`, `CFT`, etc.) representam apenas uma fração dos parlamentares e não o plenário completo.
2. **Descarte de Requerimentos Procedimentais:** Descartar votações cuja descrição contenha:
   - `Requerimento de adiamento`
   - `Requerimento de retirada de pauta`
   - `Requerimento de encerramento da discussão`
   - `Requerimento de quebra de interstício`
   - `Requerimento de Urgência (Art. 155)` (a menos que o objetivo do tema curado seja especificamente a tramitação urgente)
3. **Descarte de Redação Final:** Descartar `Aprovada a Redação Final`, pois é apenas ajuste formal de texto após a matéria substantiva já ter sido aprovada.
4. **Identificação da Votação de Mérito:**
   - **Para PECs (Propostas de Emenda à Constituição):** Procurar a votação que aprove o texto em **1º Turno** (`primeiro turno` / `1º turno`) e em **2º Turno** (`segundo turno` / `2º turno`). Exemplo: *"Aprovado, em primeiro turno, o Substitutivo..."*.
   - **Para Projetos de Lei (PL / PLP):** Procurar a aprovação da `Subemenda Substitutiva Global`, `Substitutivo` ou do próprio `Projeto de Lei`. Exemplo: *"Aprovada a Subemenda Substitutiva Global ao Projeto de Lei nº 490, de 2007, adotada pelo relator... ressalvados os destaques"*.
   - **Para Medidas Provisórias (MPV):** Procurar a aprovação *"na forma do Projeto de Lei de Conversão, ressalvados os destaques"*.

---

## 6. Mapeamento dos Casos Reais para o MVP v0 (Seed Curado)

Foram gerados artefatos consolidados em `dados/votacoes/` pelo script `scripts/discovery_votacoes.py`:

| Tema Curado | Proposição | Votação ID | Data/Hora | Descrição Resumida | Arquivo Local |
|---|---|---|---|---|---|
| **Reforma Tributária (1º Turno)** | PEC 45/2019 (ID: 2196833) | `2196833-326` | 2023-07-06 21:49 | Aprovado o Substitutivo em 1º turno (Sim: 382, Não: 118, Abst: 3) | [`dados/votacoes/2196833-326.json`](../dados/votacoes/2196833-326.json) |
| **Reforma Tributária (2º Turno)** | PEC 45/2019 (ID: 2196833) | `2196833-373` | 2023-07-07 01:39 | Aprovada a PEC 45/2019 em 2º turno (Sim: 375, Não: 113, Abst: 3) | [`dados/votacoes/2196833-373.json`](../dados/votacoes/2196833-373.json) |
| **Marco Temporal das Terras Indígenas** | PL 490/2007 (ID: 345311) | `345311-270` | 2023-05-30 20:12 | Aprovada a Subemenda Substitutiva Global (Sim: 283, Não: 155, Abst: 1) | [`dados/votacoes/345311-270.json`](../dados/votacoes/345311-270.json) |
| **Anistia aos Partidos Políticos (2º Turno)** | PEC 9/2023 (ID: 2352476) | `2352476-168` | 2024-07-11 18:52 | Aprovada a PEC em 2º turno (Sim: 338, Não: 83, Abst: 4) | [`dados/votacoes/2352476-168.json`](../dados/votacoes/2352476-168.json) |
| **Taxação de Compras Internacionais (Mover)** | PL 914/2024 (ID: 2422697) | `2422697-75` | 2024-05-28 22:08 | Mantido o texto da alíquota de 20% (Sim: 280, Não: 121) | [`dados/votacoes/2422697-75.json`](../dados/votacoes/2422697-75.json) |

---

## 7. Links Oficiais para Cumprimento do AGENTS.md §3.1

Para cada voto exibido na interface pública, o sistema deve fornecer dois links clicáveis de verificabilidade oficial:

1. **Link da Proposição:**  
   `https://www.camara.leg.br/propostas-legislativas/{proposicao_id}`  
   Exemplo: [PEC 45/2019](https://www.camara.leg.br/propostas-legislativas/2196833)
2. **Link da Votação / Registro Oficial:**  
   `https://dadosabertos.camara.leg.br/api/v2/votacoes/{votacao_id}`  
   Exemplo: [Votação 2196833-326 (API)](https://dadosabertos.camara.leg.br/api/v2/votacoes/2196833-326)  
   E para sessões deliberativas na web: `https://www.camara.leg.br/evento-legislativo/{idEvento}` (ex: [Sessão Deliberativa 68337](https://www.camara.leg.br/evento-legislativo/68337)).
