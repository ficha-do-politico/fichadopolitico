# Backlog de Votações Nominais e Radar Legislativo

Este documento organiza as matérias legislativas sugeridas para inclusão no [Catálogo de Temas](../dados/catalogo/temas.json) do **Ficha do Político**, detalhando a situação regimental de cada uma, links oficiais e a viabilidade de inserção imediata.

> **Regra Mandatória ([AGENTS.md](../AGENTS.md) §3.1):**  
> Para constar na ficha de um parlamentar com registro de voto (`Sim`, `Não`, `Abstenção`, `Obstrução` ou `Não Votou/Ausente`), a matéria DEVE ter sido objeto de **votação nominal no Plenário** (da Câmara dos Deputados ou do Senado Federal), com dados consolidados na API oficial. Matérias em fase de coleta de assinaturas, audiências públicas ou votadas apenas simbolicamente em comissões NÃO podem gerar dados de votação nominal na ficha.

---

## 1. Matérias Integradas Recentemente no Catálogo Oficial

### 1.1. PEC da Escala 6×1 / Redução da Jornada para 40h (PEC 221/2019)
- **Autoria / Proposição:** PEC 221/2019 (Dep. Reginaldo Lopes - PT/MG), à qual foi apensada a PEC 8/2025 (Dep. Erika Hilton - PSOL/SP e movimento VAT).
- **Status Regimental:**
  - **Câmara dos Deputados:** Aprovada no Plenário em 2 turnos em 27/05/2026. 1º turno (`2233802-424`: Sim: 472, Não: 22); 2º turno (`2233802-438`: Sim: 461, Não: 19).
  - **Senado Federal:** Matéria `174386` autuada em 28/05/2026. Aprovada na CCJ em 02/09/2026. Aguarda deliberação no Plenário do Senado em 2 turnos.
- **Situação no Portal:** **Integrada ao Catálogo Oficial como Tema 6** (votos nominais dos 513 deputados federais registrados a partir da API oficial).

---

## 2. Matérias em Radar com Impedimento Regimental (Sem Votação Nominal em Plenário)

As propostas abaixo geram forte debate público, mas **não possuem votação nominal no Plenário do Congresso até o momento**. Ficam catalogadas aqui para acompanhamento contínuo.

### 2.1. PEC da Segurança Pública
- **Origem:** Proposta elaborada pelo Ministério da Justiça e Segurança Pública (Poder Executivo) para constitucionalizar o SUSP e ampliar atribuições da Polícia Federal e PRF.
- **Status Regimental:** Fase de negociação com governadores e tramitação no Congresso.
- **Situação de Voto:** **Inviável para a ficha no momento.** Nenhuma votação nominal em plenário registrada.
- **Ação Futura:** Monitorar deliberação plenária.

---

## 2. Matérias em Análise para Expansão do Catálogo (Votação Nominal Existente)

Candidatas prioritárias para expansão da lista de temas (meta v1: 10 a 20 matérias).

### 2.1. Isenção e Tributação do Imposto de Renda
- **Contexto:** Discussões sobre tabela do IRPF (isenção de até 2 salários mínimos vs. proposta de isenção até R$ 5.000).
- **Matérias Relevantes:**
  - **PL 81/2024:** Altera a tabela progressiva mensal do IRPF para garantir isenção a rendimentos de até 2 salários mínimos. Aprovado na Câmara e no Senado em 2024 (Lei nº 14.848/2024).
  - **Reforma da Renda / R$ 5K:** Matéria enviada/em tramitação para o exercício de 2025/2026.
- **Próximo Passo Técnico:** Investigar na API da Câmara (`GET /proposicoes?numero=81&ano=2024`) os IDs de votação nominal de mérito em plenário.

### 2.2. Pauta Ambiental e Emergência Climática ("Devastação / Meio Ambiente")
- **Contexto:** Votações que opõem flexibilização ambiental e preservação de biomas/recursos naturais.
- **Matérias Candidatas com Votação Plenária:**
  - **PL 2159/2021 (Lei Geral do Licenciamento Ambiental):** Estabelece normas gerais para o licenciamento de atividades e empreendimentos. Votação de mérito histórica na Câmara, com envio ao Senado.
  - **MPV 1150/2022 (Mata Atlântica):** Conversão na Lei 14.595/2023, envolvendo vetos e destaques sobre dispositivos de proteção florestal.
  - **PL 1459/2022 (Marco dos Agrotóxicos):** Aprovado no Congresso (Lei 14.785/2023).
  - *(Nota: O PL 490/2007 - Marco Temporal das Terras Indígenas já integra o [catálogo oficial](../dados/catalogo/temas.json) como Tema 3).*
- **Próximo Passo Técnico:** Priorizar entre Licenciamento Ambiental (PL 2159/2021) e o Marco dos Agrotóxicos (PL 1459/2022) e extrair os IDs de votação bicameral.

### 2.3. Segurança Pública e Execução Penal
- **PL 2253/2022 (Fim das "Saidinhas" de Presos):**
  - Matéria deliberada nominalmente na Câmara e no Senado com derrubada de veto presidencial (Lei nº 14.843/2024).
  - Tema de altíssima repercussão popular e divisão clara de votos nominais.

---

## 3. Fluxo de Entrada no Catálogo Oficial

Quando uma matéria atinge deliberação no plenário:
1. Executar o script `scripts/discovery_votacoes.py` passando `siglaTipo`, `numero` e `ano`.
2. Localizar o ID exato da votação nominal no órgão `PLEN` (`idVotacao`).
3. Mapear a votação correspondente no Senado (`scripts/senado/fetch_votacoes.py`).
4. Inserir o registro com justificativa e links de verificabilidade em `dados/catalogo/temas.json`.
5. Rodar `uv run python scripts/build_site_data.py` e testes `uv run python -m unittest discover tests`.
