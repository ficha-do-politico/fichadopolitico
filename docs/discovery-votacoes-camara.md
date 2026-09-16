# Heurísticas de Extração: Votações Nominais da Câmara

> **Documento de referência para APIs completas:** [fontes-oficiais-de-dados.md](../fontes-oficiais-de-dados.md)  
> **Diretrizes de verificabilidade:** [STATE.md](../.specs/STATE.md) (AD-006) e [AGENTS.md](../AGENTS.md) (§3.1)

---

## 1. Regras Fundamentais de Negócio

1. **Votação Plenária Obrigatória:**  
   Apenas deliberações com votação nominal no Plenário (`siglaOrgao == 'PLEN'`) podem alimentar o catálogo de votos da ficha. Matérias em comissões, audiências ou com votação simbólica não geram registro individual de voto.
2. **Inferência de Ausência (Ausente ≠ Abstenção):**  
   O endpoint oficial `/votacoes/{id}/votos` retorna **apenas** os parlamentares que registraram voto no painel eletrônico. Se um parlamentar estava em exercício na data e não consta na lista de votantes, seu status factual e neutro na ficha deve ser **`Não votou / Ausente`**.

---

## 2. Fluxo de Consulta de Dados

```
[Matéria / Tema Curado]
          │
          ▼ 1. GET /proposicoes?siglaTipo={TIPO}&numero={NUM}&ano={ANO}
[ID Oficial da Proposição]
          │
          ▼ 2. GET /proposicoes/{id}/votacoes
[Histórico de Votações da Proposição]
          │
          ▼ 3. Aplicação da Heurística de Mérito (seção 4)
[ID da Votação Decisiva de Plenário]
          │
          ├──────────────────────────────────────────────┐
          ▼ 4. GET /votacoes/{id}/votos                  ▼ 5. GET /votacoes/{id}/orientacoes
[Lista de Votos Nominais]                        [Orientações de Bancadas/Governo]
```

Para especificações detalhadas de cabeçalhos, rate limits e paginação da API da Câmara, consulte [fontes-oficiais-de-dados.md](../fontes-oficiais-de-dados.md#11-câmara-dos-deputados).

---

## 3. Dicionário de Votos (`tipoVoto`)

| Retorno na API | Significado Regimental | Exibição na Ficha |
|---|---|---|
| `Sim` | Voto favorável à proposição ou substitutivo | **Sim** |
| `Não` | Voto contrário à matéria ou substitutivo | **Não** |
| `Abstenção` | Parlamentar registrou presença e abstenção formal | **Abstenção** |
| `Artigo 17` | Aplicação do Art. 17 do Regimento: Presidente da Câmara só vota em empate ou quórum qualificado | **Artigo 17 (Presidência)** |
| `Obstrução` | Registro formal de obstrução para impedir quórum | **Obstrução** |
| *(Omitido na API)* | Parlamentar em exercício que não votou | **Não votou / Ausente** |

---

## 4. Heurística de Seleção de Votação Decisiva (Mérito)

Proposições de grande impacto costumam acumular dezenas de votações procedimentais. O pipeline de discovery (`scripts/discovery_votacoes.py`) aplica os seguintes filtros:

1. **Filtro de Órgão:** Exigir estritamente `siglaOrgao == 'PLEN'`.
2. **Descarte de Requerimentos Procedimentais:** Descartar votações cuja descrição contenha:
   - `Requerimento de adiamento`
   - `Requerimento de retirada de pauta`
   - `Requerimento de encerramento da discussão`
   - `Requerimento de quebra de interstício`
   - `Requerimento de Urgência` (exceto se a matéria curada for especificamente a urgência)
3. **Descarte de Redação Final:** Descartar registros com `Aprovada a Redação Final` (ajuste formal de texto pós-mérito).
4. **Identificação do Mérito por Tipo de Matéria:**
   - **PECs:** Buscar aprovação de texto em **1º Turno** (`primeiro turno` / `1º turno`) ou **2º Turno** (`segundo turno` / `2º turno`).
   - **PL / PLP:** Buscar aprovação de `Subemenda Substitutiva Global`, `Substitutivo` ou do próprio `Projeto de Lei`.
   - **MPV:** Buscar aprovação `na forma do Projeto de Lei de Conversão`.

---

## 5. Padrão de Links Oficiais de Verificabilidade

Toda votação cadastrada em `dados/catalogo/temas.json` deve fornecer URLs públicas oficiais diretas:

1. **Proposição na Câmara:**  
   `https://www.camara.leg.br/propostas-legislativas/{proposicao_id}`
2. **Votação na API Oficial:**  
   `https://dadosabertos.camara.leg.br/api/v2/votacoes/{votacao_id}`
3. **Sessão Deliberativa (Áudio/Vídeo/Ata):**  
   `https://www.camara.leg.br/evento-legislativo/{idEvento}`
