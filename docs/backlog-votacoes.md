# Backlog de Votações Nominais e Radar Legislativo

Este documento organiza as matérias legislativas sugeridas para inclusão no [Catálogo de Temas](../dados/catalogo/temas.json) do **Ficha do Político**, detalhando a situação regimental de cada uma, links oficiais e a viabilidade de inserção imediata.

> **Regra Mandatória ([AGENTS.md](../AGENTS.md) §3.1):**  
> Para constar na ficha de um parlamentar com registro de voto (`Sim`, `Não`, `Abstenção`, `Obstrução` ou `Não Votou/Ausente`), a matéria DEVE ter sido objeto de **votação nominal no Plenário** (da Câmara dos Deputados ou do Senado Federal), com dados consolidados na API oficial. Matérias em fase de coleta de assinaturas, audiências públicas ou votadas apenas simbolicamente em comissões NÃO podem gerar dados de votação nominal na ficha.

---

## 1. Matérias Integradas no Catálogo Oficial

### 1.1. PEC da Escala 6×1 / Redução da Jornada para 40h (PEC 221/2019)
- **Autoria / Proposição:** PEC 221/2019 (Dep. Reginaldo Lopes - PT/MG), com PEC 8/2025 apensada (Dep. Erika Hilton - PSOL/SP).
- **Status Regimental:** Aprovada na Câmara em 2 turnos (votação `2233802-438`: Sim: 461, Não: 19). Aguarda Plenário no Senado.
- **Situação no Portal:** **Tema 6**.

### 1.2. Novo Arcabouço Fiscal (PLP 93/2023)
- **Autoria / Proposição:** Poder Executivo / Ministério da Fazenda. Substituição do Teto de Gastos da EC 95/2016.
- **Status Regimental:**
  - **Câmara dos Deputados:** Aprovado Substitutivo em 23/05/2023 (`2357053-47`: Sim: 372, Não: 108, Abst: 1).
  - **Senado Federal:** Aprovado em 21/06/2023 (Matéria `157826`, Votação `6714`: Sim: 57, Não: 17).
- **Situação no Portal:** **Integrado ao Catálogo Oficial como Tema 7** (cobertura bicameral nominal 100%).

### 1.3. Regulamentação da Reforma Tributária (PLP 68/2024)
- **Autoria / Proposição:** Poder Executivo. Instituição do IBS, CBS e Imposto Seletivo.
- **Status Regimental:**
  - **Câmara dos Deputados:** Aprovada Subemenda Substitutiva Global em 10/07/2024 (`2430143-72`: Sim: 336, Não: 142, Abst: 2).
  - **Senado Federal:** Aprovado Substitutivo em 12/12/2024 (Matéria `164914`, Votação `6899`: Sim: 49, Não: 19).
- **Situação no Portal:** **Integrado ao Catálogo Oficial como Tema 8** (cobertura bicameral nominal 100%).

---

## 2. Matérias em Radar com Impedimento Regimental (Sem Votação Nominal em Plenário)

As propostas abaixo geram forte debate público, mas **não possuem votação nominal de mérito no Plenário do Congresso para a 57ª Legislatura**. Ficam catalogadas aqui para acompanhamento contínuo.

### 2.1. PEC da Segurança Pública
- **Origem:** Proposta elaborada pelo Ministério da Justiça e Segurança Pública (Poder Executivo).
- **Status Regimental:** Fase de negociação com governadores e tramitação inicial. Sem votação nominal em plenário.

### 2.2. Isenção do IRPF até 2 Salários Mínimos (PL 81/2024)
- **Auditoria Técnica:** O Substitutivo (`2417025-56`, 12/03/2024) foi aprovado **simbolicamente** no Plenário da Câmara e do Senado (0 votos nominais). As votações nominais da sessão foram apenas recursos regimentais de preferência. Inviável para registro de votos por parlamentar.

### 2.3. Decreto de Armas / CACs (PDL 206/2024)
- **Auditoria Técnica:** O texto substitutivo (`2430026-39`, 28/05/2024) foi aprovado de forma **simbólica** na Câmara dos Deputados (0 votos nominais).

### 2.4. Fim das "Saidinhas" de Presos (PL 2253/2022)
- **Auditoria Técnica:** No Senado Federal houve votação nominal plena em 20/02/2024 (`6818`: Sim: 62, Não: 2). Na Câmara dos Deputados, a aprovação final de 2024 foi simbólica (`493361-84`), e a votação de mérito anterior data de agosto de 2022 (56ª Legislatura, anterior aos atuais deputados). A derrubada de veto ocorreu em sessão conjunta do Congresso Nacional (fora da API direta da Câmara).

---

## 3. Matérias em Análise para Próxima Expansão (Meta 10+ Temas)

Candidatas prioritárias para expansão da lista de temas no v1:

### 3.1. Regulamentação de Apostas Esportivas e Cassinos Online (PL 3626/2023)
- **Contexto:** Regulação das "Bets" e inclusão de jogos online/iGaming.
- **Status Regimental:** Votação nominal na Câmara em 21/12/2023 (`2374400-110`: Sim: 292, Não: 114) e votações nominais em destaques no Senado.

### 3.2. Estrutura dos Ministérios do Governo Federal (MPV 1154/2023)
- **Contexto:** Organização básica da Esplanada e esvaziamento das atribuições dos ministérios do Meio Ambiente e dos Povos Indígenas.
- **Status Regimental:** Votação nominal na Câmara (`2345493-41`: Sim: 337, Não: 125) e no Senado (`6704`: Sim: 51, Não: 19).

### 3.3. PEC das Drogas / Criminalização da Posse (PEC 45/2023)
- **Contexto:** Mandado de criminalização para posse/porte de qualquer quantidade de substância entorpecente.
- **Status Regimental:** Aprovada em 2 turnos no Plenário do Senado (`6825`: Sim: 52, Não: 9). Aguarda deliberação em Plenário na Câmara dos Deputados.

---

## 3. Fluxo de Entrada no Catálogo Oficial

Quando uma matéria atinge deliberação no plenário:
1. Executar o script `scripts/discovery_votacoes.py` passando `siglaTipo`, `numero` e `ano`.
2. Localizar o ID exato da votação nominal no órgão `PLEN` (`idVotacao`).
3. Mapear a votação correspondente no Senado (`scripts/senado/fetch_votacoes.py`).
4. Inserir o registro com justificativa e links de verificabilidade em `dados/catalogo/temas.json`.
5. Rodar `uv run python scripts/build_site_data.py` e testes `uv run python -m unittest discover tests`.
