# Contexto do MVP v0

**Coletado em:** 2026-08-18  
**Spec:** `.specs/features/mvp-v0/spec.md`  
**Status:** Pronto para design (pendente confirmação do AD-001 pelo time)

---

## Material de Origem

Decisões capturadas a partir de:

- Issue [#1](https://github.com/ficha-do-politico/fichadopolitico/issues/1) no GitHub (escopo MVP original + comentário da Layr sobre temas seed)
- Debate de análise competitiva (ago/2026) — Meu Congresso, Radar do Congresso, Vamos Cobrar Brasil
- `referencias.md`, `AGENTS.md`, README
- Restrição do time: **MVP simples que simplifica a visualização de votos em leis importantes para o país**

---

## Visão de Produto Travada

### Experiência hero

```
[ Busca: nome do deputado ]

→ João Silva — PL / SP
  [foto]  [link perfil oficial Câmara]

  Como votou em temas relevantes
  ─────────────────────────────────
  Trabalho
    Fim da escala 6×1          SIM     27/05/2026
                               PEC XXX/XXXX
                               [Ver votação] [Ver projeto]
                               Fonte: Câmara dos Deputados

  Meio ambiente
    PL do desmatamento         NÃO     ...
  ...
```

Modelo mental do cidadão: **deputado primeiro, tema depois** — inverso de ferramentas orientadas a projeto.

### O que explicitamente NÃO construímos no v0

- "Fulano é progressista/conservador"
- Score de alinhamento vs. opiniões do usuário
- Ficha completa de CEAP/gastos/patrimônio (território Radar/Vamos Cobrar)
- Alegar completude de todas as votações do Congresso

---

## Resoluções de Áreas Cinzentas

### 1. Curado vs. votos recentes (pivô de escopo)

**Pergunta:** Entregar votos recentes cronológicos (issue #1 original) ou temas importantes curados (conclusão do debate)?

**Decisão:** Temas importantes curados (AD-001). Lista de votos recentes é commodity; simplificação curada é a hipótese a validar.

**Racional:** Quando a 6×1 passou, grandes veículos publicaram listas por deputado — a demanda existe, mas a entrega é jornalismo episódico, não ferramenta permanente.

---

### 2. Múltiplas votações por tema

**Pergunta:** Alguns temas têm votações em comissão + plenário, ou revotações. Mostrar uma ou todas?

**Decisão:** Exibição default = **última votação plenária decisiva** do tema. Linha expansível ou link secundário revela todos os `votacao_ids` mapeados com datas.

**Racional:** A pergunta do cidadão costuma ser "onde ele ficou?" — a plenária mais recente responde; power users expandem.

**Confirmado?** n — o time pode preferir mostrar todas upfront por transparência.

---

### 3. Agrupamento e rótulos de temas

**Pergunta:** Agrupar temas por tag (Trabalho, Meio ambiente) ou lista flat?

**Decisão:** `tags[]` opcional no catálogo; UI agrupa sob cabeçalhos de tag quando ≥2 temas compartilham a tag, senão lista flat ordenada por `priority`.

**Racional:** Mantém v0 simples com 4 temas; escala visualmente quando o catálogo cresce para 20–50.

---

### 4. Tom de copy da camada editorial

**Pergunta:** Como dizer "escolhemos estes votos" sem soar tendencioso?

**Decisão:** Usar enquadramento factual:

> "Selecionamos votações de grande relevância pública para facilitar o acesso. A lista não é exaustiva. Critérios de seleção."

Nunca: "as votações mais importantes do país" (implica julgamento universal).

**Racional:** AD-003 — curadoria transparente, não falsa neutralidade.

---

### 5. Catálogo seed inicial (Layr + debate)

Temas seed propostos para v0 (IDs oficiais a definir via api-discovery):

| Prioridade | Título do tema (provisório) | Notas |
| ---------- | --------------------------- | ----- |
| 1 | Fim da escala 6×1 | Sinal forte de demanda pública (listas na mídia) |
| 2 | MP do Gás do Povo | Sugestão da Layr; agenda 2026 |
| 3 | PEC da Segurança Pública | Sugestão da Layr |
| 4 | Veto ao PL da Dosimetria | Sugestão da Layr |
| 5+ | PL desmatamento, blindagem/anistia, reforma tributária, marco temporal | Exemplos do debate; adicionar conforme mapeamento na API avança |

Fonte de contexto da lista da Layr: [IREE — principais pautas 2026](https://iree.org.br/as-principais-pautas-do-congresso-em-2026/) (secundária, não oficial — usada só para brainstorming de seleção de temas, não para dados de voto).

---

### 6. Estados vazios e parciais

| Estado | UX |
| ------ | -- |
| Deputado encontrado, catálogo ainda sem votos | Cabeçalho da ficha + "Catálogo em construção" |
| Tema mapeado, API sem voto do deputado | Exibir rótulo oficial de ausência da API |
| API fora | Banner de erro; se houver cache, exibir com "Dados de {data}" |
| Busca sem resultados | "Nenhum deputado encontrado" |

---

## Ideias Adiadas (fora de escopo — não implementar a partir deste contexto)

- Paridade com Senado (Layr: "segundo momento")
- Modo comparação ("compare 2 deputados nestes temas")
- Pedidos de tema enviados por usuários sem revisão de mantenedor
- Detecção automatizada de temas a partir de RSS de notícias

---

## Inputs para Design

Quando a fase de Design começar, priorizar:

1. **Layout search-first** — barra de busca acima da dobra no mobile
2. **Componente de card de voto** — título do tema, badge de voto (Sim/Não/…), data, ref. da proposição, links duplos de fonte
3. **Schema do catálogo** — localização do arquivo, script de validação, check de CI que IDs de votação resolvem
4. **Estratégia de cache** — rate limits da API da Câmara (output da issue #2 deve informar TTL)

Stack permanece aberta (AD-008). PR em andamento da Layr em `/deputados` pode informar a primeira escolha de implementação — ler antes do Design.
