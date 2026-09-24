# Auditoria Amostral de Módulos (P4) — Votações, Despesas e Emendas

> **Data da Auditoria:** 2026-09-24
> **Escopo:** Tarefa P4 do Plano de Correção ([`docs/auditoria-dados-tse-2026.md`](auditoria-dados-tse-2026.md))
> **Status:** ✅ Concluída — Nenhuma evidência de dados sintéticos nos módulos auditados
> **Normas:** [AGENTS.md](../AGENTS.md) §3.1 e [STATE.md](../.specs/STATE.md) (AD-006, AD-016, AD-017)

---

## 1. Metodologia e Seleção Amostral

Para verificar se outros módulos do projeto (além do módulo eleitoral do TSE auditado em A1–A6) sofreram contaminação por dados sintéticos ou estimativas arbitrárias, realizou-se uma amostragem sistemática e determinística:

- **Câmara dos Deputados:** Ordenação crescente por ID de [`dados/camara/deputados.json`](../dados/camara/deputados.json) (513 deputados) e seleção de 1 a cada 50 (índices 0, 50, 100, ..., 450), totalizando **10 deputados**.
- **Senado Federal:** Ordenação crescente por ID de [`dados/senado/senadores.json`](../dados/senado/senadores.json) (81 senadores) e seleção de 1 a cada 16 (índices 0, 16, 32, 48, 64), totalizando **5 senadores**.

### Parlamentares Selecionados na Amostra

| Casa | ID | Nome Eleitoral | Partido/UF |
|---|---|---|---|
| Câmara | 62881 | Danilo Forte | PP/CE |
| Câmara | 74574 | Paulo Magalhães | PSD/BA |
| Câmara | 141555 | Vinicius Carvalho | PL/SP |
| Câmara | 160976 | Tiririca | PSD/SP |
| Câmara | 178983 | Marcio Alvino | PL/SP |
| Câmara | 204423 | André Ferreira | PL/PE |
| Câmara | 204528 | Adriana Ventura | NOVO/SP |
| Câmara | 220548 | Camila Jara | PT/MS |
| Câmara | 220609 | Maurício Carvalho | UNIÃO/RO |
| Câmara | 220666 | Coronel Meira | PL/PE |
| Senado | 22 | Esperidião Amin | PP/SC |
| Senado | 3830 | Davi Alcolumbre | UNIÃO/AP |
| Senado | 5385 | Irajá | PSD/TO |
| Senado | 5899 | Vanderlan Cardoso | PSD/GO |
| Senado | 5990 | Carlos Viana | PSD/MG |

---

## 2. Auditoria de Votações Nominais

Conferência de 2 votações nominais relevantes para cada parlamentar da amostra:
- **Câmara:** PEC 45/2019 — Reforma Tributária: 1º Turno (ID `2196833-326`) e 2º Turno (ID `2196833-373`).
  - *Fonte Oficial:* API de Dados Abertos da Câmara (`https://dadosabertos.camara.leg.br/api/v2/votacoes/{id}/votos`).
- **Senado:** PEC 45/2019 — Reforma Tributária: 1º Turno (Sessão 368878, Vot 6773) e 2º Turno (Sessão 368878, Vot 6777).
  - *Fonte Oficial:* API de Dados Abertos do Senado (`https://legis.senado.leg.br/dadosabertos/materia/votacoes/158930`).

| Casa | Parlamentar | Matéria / Votação | Voto no Repo | Voto Oficial | Link Oficial Direto | Status |
|---|---|---|---|---|---|---|
| Câmara | Danilo Forte (62881) | PEC 45/2019 (1º Turno) | Sim | Sim | [https://dadosabertos.camara.leg.br/api/v2/votacoes/2196833-326/votos](https://dadosabertos.camara.leg.br/api/v2/votacoes/2196833-326/votos) | OK |
| Câmara | Danilo Forte (62881) | PEC 45/2019 (2º Turno) | Sim | Sim | [https://dadosabertos.camara.leg.br/api/v2/votacoes/2196833-373/votos](https://dadosabertos.camara.leg.br/api/v2/votacoes/2196833-373/votos) | OK |
| Câmara | Paulo Magalhães (74574) | PEC 45/2019 (1º Turno) | Sim | Sim | [https://dadosabertos.camara.leg.br/api/v2/votacoes/2196833-326/votos](https://dadosabertos.camara.leg.br/api/v2/votacoes/2196833-326/votos) | OK |
| Câmara | Paulo Magalhães (74574) | PEC 45/2019 (2º Turno) | Sim | Sim | [https://dadosabertos.camara.leg.br/api/v2/votacoes/2196833-373/votos](https://dadosabertos.camara.leg.br/api/v2/votacoes/2196833-373/votos) | OK |
| Câmara | Vinicius Carvalho (141555) | PEC 45/2019 (1º Turno) | Sim | Sim | [https://dadosabertos.camara.leg.br/api/v2/votacoes/2196833-326/votos](https://dadosabertos.camara.leg.br/api/v2/votacoes/2196833-326/votos) | OK |
| Câmara | Vinicius Carvalho (141555) | PEC 45/2019 (2º Turno) | Sim | Sim | [https://dadosabertos.camara.leg.br/api/v2/votacoes/2196833-373/votos](https://dadosabertos.camara.leg.br/api/v2/votacoes/2196833-373/votos) | OK |
| Câmara | Tiririca (160976) | PEC 45/2019 (1º Turno) | Sim | Sim | [https://dadosabertos.camara.leg.br/api/v2/votacoes/2196833-326/votos](https://dadosabertos.camara.leg.br/api/v2/votacoes/2196833-326/votos) | OK |
| Câmara | Tiririca (160976) | PEC 45/2019 (2º Turno) | Sim | Sim | [https://dadosabertos.camara.leg.br/api/v2/votacoes/2196833-373/votos](https://dadosabertos.camara.leg.br/api/v2/votacoes/2196833-373/votos) | OK |
| Câmara | Marcio Alvino (178983) | PEC 45/2019 (1º Turno) | Não | Não | [https://dadosabertos.camara.leg.br/api/v2/votacoes/2196833-326/votos](https://dadosabertos.camara.leg.br/api/v2/votacoes/2196833-326/votos) | OK |
| Câmara | Marcio Alvino (178983) | PEC 45/2019 (2º Turno) | Não | Não | [https://dadosabertos.camara.leg.br/api/v2/votacoes/2196833-373/votos](https://dadosabertos.camara.leg.br/api/v2/votacoes/2196833-373/votos) | OK |
| Câmara | André Ferreira (204423) | PEC 45/2019 (1º Turno) | Não | Não | [https://dadosabertos.camara.leg.br/api/v2/votacoes/2196833-326/votos](https://dadosabertos.camara.leg.br/api/v2/votacoes/2196833-326/votos) | OK |
| Câmara | André Ferreira (204423) | PEC 45/2019 (2º Turno) | Não | Não | [https://dadosabertos.camara.leg.br/api/v2/votacoes/2196833-373/votos](https://dadosabertos.camara.leg.br/api/v2/votacoes/2196833-373/votos) | OK |
| Câmara | Adriana Ventura (204528) | PEC 45/2019 (1º Turno) | Sim | Sim | [https://dadosabertos.camara.leg.br/api/v2/votacoes/2196833-326/votos](https://dadosabertos.camara.leg.br/api/v2/votacoes/2196833-326/votos) | OK |
| Câmara | Adriana Ventura (204528) | PEC 45/2019 (2º Turno) | Sim | Sim | [https://dadosabertos.camara.leg.br/api/v2/votacoes/2196833-373/votos](https://dadosabertos.camara.leg.br/api/v2/votacoes/2196833-373/votos) | OK |
| Câmara | Camila Jara (220548) | PEC 45/2019 (1º Turno) | Sim | Sim | [https://dadosabertos.camara.leg.br/api/v2/votacoes/2196833-326/votos](https://dadosabertos.camara.leg.br/api/v2/votacoes/2196833-326/votos) | OK |
| Câmara | Camila Jara (220548) | PEC 45/2019 (2º Turno) | Sim | Sim | [https://dadosabertos.camara.leg.br/api/v2/votacoes/2196833-373/votos](https://dadosabertos.camara.leg.br/api/v2/votacoes/2196833-373/votos) | OK |
| Câmara | Maurício Carvalho (220609) | PEC 45/2019 (1º Turno) | Sim | Sim | [https://dadosabertos.camara.leg.br/api/v2/votacoes/2196833-326/votos](https://dadosabertos.camara.leg.br/api/v2/votacoes/2196833-326/votos) | OK |
| Câmara | Maurício Carvalho (220609) | PEC 45/2019 (2º Turno) | Sim | Sim | [https://dadosabertos.camara.leg.br/api/v2/votacoes/2196833-373/votos](https://dadosabertos.camara.leg.br/api/v2/votacoes/2196833-373/votos) | OK |
| Câmara | Coronel Meira (220666) | PEC 45/2019 (1º Turno) | Não | Não | [https://dadosabertos.camara.leg.br/api/v2/votacoes/2196833-326/votos](https://dadosabertos.camara.leg.br/api/v2/votacoes/2196833-326/votos) | OK |
| Câmara | Coronel Meira (220666) | PEC 45/2019 (2º Turno) | Não | Não | [https://dadosabertos.camara.leg.br/api/v2/votacoes/2196833-373/votos](https://dadosabertos.camara.leg.br/api/v2/votacoes/2196833-373/votos) | OK |
| Senado | Esperidião Amin (22) | PEC 45/2019 (1º Turno / Vot 6773) | Não | Não | [https://legis.senado.leg.br/dadosabertos/materia/votacoes/158930](https://legis.senado.leg.br/dadosabertos/materia/votacoes/158930) | OK |
| Senado | Esperidião Amin (22) | PEC 45/2019 (2º Turno / Vot 6777) | Não | Não | [https://legis.senado.leg.br/dadosabertos/materia/votacoes/158930](https://legis.senado.leg.br/dadosabertos/materia/votacoes/158930) | OK |
| Senado | Davi Alcolumbre (3830) | PEC 45/2019 (1º Turno / Vot 6773) | Sim | Sim | [https://legis.senado.leg.br/dadosabertos/materia/votacoes/158930](https://legis.senado.leg.br/dadosabertos/materia/votacoes/158930) | OK |
| Senado | Davi Alcolumbre (3830) | PEC 45/2019 (2º Turno / Vot 6777) | Sim | Sim | [https://legis.senado.leg.br/dadosabertos/materia/votacoes/158930](https://legis.senado.leg.br/dadosabertos/materia/votacoes/158930) | OK |
| Senado | Irajá (5385) | PEC 45/2019 (1º Turno / Vot 6773) | Não votou / Ausente | Não votou / Ausente (AP) | [https://legis.senado.leg.br/dadosabertos/materia/votacoes/158930](https://legis.senado.leg.br/dadosabertos/materia/votacoes/158930) | OK |
| Senado | Irajá (5385) | PEC 45/2019 (2º Turno / Vot 6777) | Não votou / Ausente | Não votou / Ausente (AP) | [https://legis.senado.leg.br/dadosabertos/materia/votacoes/158930](https://legis.senado.leg.br/dadosabertos/materia/votacoes/158930) | OK |
| Senado | Vanderlan Cardoso (5899) | PEC 45/2019 (1º Turno / Vot 6773) | Sim | Sim | [https://legis.senado.leg.br/dadosabertos/materia/votacoes/158930](https://legis.senado.leg.br/dadosabertos/materia/votacoes/158930) | OK |
| Senado | Vanderlan Cardoso (5899) | PEC 45/2019 (2º Turno / Vot 6777) | Sim | Sim | [https://legis.senado.leg.br/dadosabertos/materia/votacoes/158930](https://legis.senado.leg.br/dadosabertos/materia/votacoes/158930) | OK |
| Senado | Carlos Viana (5990) | PEC 45/2019 (1º Turno / Vot 6773) | Sim | Sim | [https://legis.senado.leg.br/dadosabertos/materia/votacoes/158930](https://legis.senado.leg.br/dadosabertos/materia/votacoes/158930) | OK |
| Senado | Carlos Viana (5990) | PEC 45/2019 (2º Turno / Vot 6777) | Sim | Sim | [https://legis.senado.leg.br/dadosabertos/materia/votacoes/158930](https://legis.senado.leg.br/dadosabertos/materia/votacoes/158930) | OK |

**Resultado Votações:** 30 conferências realizadas (20 na Câmara, 10 no Senado). **30/30 OK (100% de exatidão)**.

---

## 3. Auditoria de Emendas Parlamentares (CGU / Portal da Transparência)

Conferência do campo `total_pago` acumulado na 57ª Legislatura (2023–2026) em [`dados/emendas/emendas_resumo.json`](../dados/emendas/emendas_resumo.json) contra o dump oficial aberto do Portal da Transparência (`EmendasParlamentares.csv`).

| Casa | Parlamentar | Total Pago (Repo) | Total Pago (CGU Oficial) | Link Oficial Portal Transparência | Status |
|---|---|---|---|---|---|
| Câmara | Danilo Forte (62881) | R$ 102.468.201,09 | R$ 102.468.201,09 | [https://portaldatransparencia.gov.br/emendas/consulta?autor=DANILO+FORTE](https://portaldatransparencia.gov.br/emendas/consulta?autor=DANILO+FORTE) | OK |
| Câmara | Paulo Magalhães (74574) | R$ 92.681.520,97 | R$ 92.681.520,97 | [https://portaldatransparencia.gov.br/emendas/consulta?autor=PAULO+MAGALHAES](https://portaldatransparencia.gov.br/emendas/consulta?autor=PAULO+MAGALHAES) | OK |
| Câmara | Vinicius Carvalho (141555) | R$ 103.741.969,23 | R$ 103.741.969,23 | [https://portaldatransparencia.gov.br/emendas/consulta?autor=VINICIUS+CARVALHO](https://portaldatransparencia.gov.br/emendas/consulta?autor=VINICIUS+CARVALHO) | OK |
| Câmara | Tiririca (160976) | R$ 100.404.562,44 | R$ 100.404.562,44 | [https://portaldatransparencia.gov.br/emendas/consulta?autor=TIRIRICA](https://portaldatransparencia.gov.br/emendas/consulta?autor=TIRIRICA) | OK |
| Câmara | Marcio Alvino (178983) | R$ 114.262.767,31 | R$ 114.262.767,31 | [https://portaldatransparencia.gov.br/emendas/consulta?autor=MARCIO+ALVINO](https://portaldatransparencia.gov.br/emendas/consulta?autor=MARCIO+ALVINO) | OK |
| Câmara | André Ferreira (204423) | R$ 133.765.814,25 | R$ 133.765.814,25 | [https://portaldatransparencia.gov.br/emendas/consulta?autor=ANDRE+FERREIRA](https://portaldatransparencia.gov.br/emendas/consulta?autor=ANDRE+FERREIRA) | OK |
| Câmara | Adriana Ventura (204528) | R$ 62.817.034,74 | R$ 62.817.034,74 | [https://portaldatransparencia.gov.br/emendas/consulta?autor=ADRIANA+VENTURA](https://portaldatransparencia.gov.br/emendas/consulta?autor=ADRIANA+VENTURA) | OK |
| Câmara | Camila Jara (220548) | R$ 70.888.668,24 | R$ 70.888.668,24 | [https://portaldatransparencia.gov.br/emendas/consulta?autor=CAMILA+JARA](https://portaldatransparencia.gov.br/emendas/consulta?autor=CAMILA+JARA) | OK |
| Câmara | Maurício Carvalho (220609) | R$ 78.432.814,91 | R$ 78.432.814,91 | [https://portaldatransparencia.gov.br/emendas/consulta?autor=MAURICIO+CARVALHO](https://portaldatransparencia.gov.br/emendas/consulta?autor=MAURICIO+CARVALHO) | OK |
| Câmara | Coronel Meira (220666) | R$ 57.733.285,83 | R$ 57.733.285,83 | [https://portaldatransparencia.gov.br/emendas/consulta?autor=CORONEL+MEIRA](https://portaldatransparencia.gov.br/emendas/consulta?autor=CORONEL+MEIRA) | OK |
| Senado | Esperidião Amin (22) | R$ 180.634.305,45 | R$ 180.634.305,45 | [https://portaldatransparencia.gov.br/emendas/consulta?autor=ESPERIDIAO+AMIN](https://portaldatransparencia.gov.br/emendas/consulta?autor=ESPERIDIAO+AMIN) | OK |
| Senado | Davi Alcolumbre (3830) | R$ 281.235.947,48 | R$ 281.235.947,48 | [https://portaldatransparencia.gov.br/emendas/consulta?autor=DAVI+ALCOLUMBRE](https://portaldatransparencia.gov.br/emendas/consulta?autor=DAVI+ALCOLUMBRE) | OK |
| Senado | Irajá (5385) | R$ 72.972.871,00 | R$ 72.972.871,00 | [https://portaldatransparencia.gov.br/emendas/consulta?autor=IRAJA](https://portaldatransparencia.gov.br/emendas/consulta?autor=IRAJA) | OK |
| Senado | Vanderlan Cardoso (5899) | R$ 140.345.838,88 | R$ 140.345.838,88 | [https://portaldatransparencia.gov.br/emendas/consulta?autor=VANDERLAN+CARDOSO](https://portaldatransparencia.gov.br/emendas/consulta?autor=VANDERLAN+CARDOSO) | OK |
| Senado | Carlos Viana (5990) | R$ 229.367.432,28 | R$ 229.367.432,28 | [https://portaldatransparencia.gov.br/emendas/consulta?autor=CARLOS+VIANA](https://portaldatransparencia.gov.br/emendas/consulta?autor=CARLOS+VIANA) | OK |

**Resultado Emendas:** 15 conferências realizadas. **15/15 OK (100% de exatidão)** até o centavo com os dados da CGU.

---

## 4. Auditoria de Despesas (CEAP / CEAPS 2026)

Conferência do campo `total_gasto` (exercício 2026):
- **Câmara (CEAP):** comparado com o dump oficial `https://www.camara.leg.br/cotas/Ano-2026.csv.zip` baixado em tempo real em 2026-09-24.
- **Senado (CEAPS):** comparado com a API oficial `https://adm.senado.leg.br/adm-dadosabertos/api/v1/senadores/despesas_ceaps/2026` consultada em tempo real em 2026-09-24.

> [!NOTE]
> O exercício de 2026 é um **ano em curso**. Os portais oficiais continuam registrando notas fiscais e reembolsos diariamente. O dataset no repositório representa um **snapshot estático** coletado em fechamento anterior (~31/08/2026), enquanto a consulta em tempo real (2026-09-24) traz notas processadas posteriormente pelas Casas.

| Casa | Parlamentar | Total no Repo (Snapshot) | Total Oficial (Dump/API 24/09/2026) | Variação (Novas Notas) | Link Oficial | Classificação |
|---|---|---|---|---|---|---|
| Câmara | Danilo Forte (62881) | R$ 306.850,18 | R$ 325.536,14 | +R$ 18.685,96 | [https://www.camara.leg.br/deputados/62881](https://www.camara.leg.br/deputados/62881) | SNAPSHOT_DEFASADO |
| Câmara | Paulo Magalhães (74574) | R$ 289.657,65 | R$ 298.813,43 | +R$ 9.155,78 | [https://www.camara.leg.br/deputados/74574](https://www.camara.leg.br/deputados/74574) | SNAPSHOT_DEFASADO |
| Câmara | Vinicius Carvalho (141555) | R$ 223.179,62 | R$ 231.821,37 | +R$ 8.641,75 | [https://www.camara.leg.br/deputados/141555](https://www.camara.leg.br/deputados/141555) | SNAPSHOT_DEFASADO |
| Câmara | Tiririca (160976) | R$ 154.801,44 | R$ 155.310,28 | +R$ 508,84 | [https://www.camara.leg.br/deputados/160976](https://www.camara.leg.br/deputados/160976) | SNAPSHOT_DEFASADO |
| Câmara | Marcio Alvino (178983) | R$ 16.037,83 | R$ 16.037,83 | R$ 0,00 | [https://www.camara.leg.br/deputados/178983](https://www.camara.leg.br/deputados/178983) | OK (EXATO) |
| Câmara | André Ferreira (204423) | R$ 225.101,27 | R$ 232.796,64 | +R$ 7.695,37 | [https://www.camara.leg.br/deputados/204423](https://www.camara.leg.br/deputados/204423) | SNAPSHOT_DEFASADO |
| Câmara | Adriana Ventura (204528) | R$ 33.285,95 | R$ 38.263,62 | +R$ 4.977,67 | [https://www.camara.leg.br/deputados/204528](https://www.camara.leg.br/deputados/204528) | SNAPSHOT_DEFASADO |
| Câmara | Camila Jara (220548) | R$ 312.524,60 | R$ 313.774,16 | +R$ 1.249,56 | [https://www.camara.leg.br/deputados/220548](https://www.camara.leg.br/deputados/220548) | SNAPSHOT_DEFASADO |
| Câmara | Maurício Carvalho (220609) | R$ 346.172,10 | R$ 346.172,10 | R$ 0,00 | [https://www.camara.leg.br/deputados/220609](https://www.camara.leg.br/deputados/220609) | OK (EXATO) |
| Câmara | Coronel Meira (220666) | R$ 237.765,89 | R$ 244.999,94 | +R$ 7.234,05 | [https://www.camara.leg.br/deputados/220666](https://www.camara.leg.br/deputados/220666) | SNAPSHOT_DEFASADO |
| Senado | Esperidião Amin (22) | R$ 252.953,43 | R$ 258.252,44 | +R$ 5.299,01 | [https://www6g.senado.leg.br/transparencia/sen/22/?ano=2026](https://www6g.senado.leg.br/transparencia/sen/22/?ano=2026) | SNAPSHOT_DEFASADO |
| Senado | Davi Alcolumbre (3830) | R$ 226.000,00 | R$ 226.000,00 | R$ 0,00 | [https://www6g.senado.leg.br/transparencia/sen/3830/?ano=2026](https://www6g.senado.leg.br/transparencia/sen/3830/?ano=2026) | OK (EXATO) |
| Senado | Irajá (5385) | R$ 321.656,60 | R$ 350.917,86 | +R$ 29.261,26 | [https://www6g.senado.leg.br/transparencia/sen/5385/?ano=2026](https://www6g.senado.leg.br/transparencia/sen/5385/?ano=2026) | SNAPSHOT_DEFASADO |
| Senado | Vanderlan Cardoso (5899) | R$ 120.276,27 | R$ 120.276,27 | R$ 0,00 | [https://www6g.senado.leg.br/transparencia/sen/5899/?ano=2026](https://www6g.senado.leg.br/transparencia/sen/5899/?ano=2026) | OK (EXATO) |
| Senado | Carlos Viana (5990) | R$ 335.797,31 | R$ 335.797,31 | R$ 0,00 | [https://www6g.senado.leg.br/transparencia/sen/5990/?ano=2026](https://www6g.senado.leg.br/transparencia/sen/5990/?ano=2026) | OK (EXATO) |

### Análise de Proveniência das Despesas
- **Zero valores sintéticos:** Todos os registros de despesas contêm comprovantes fiscais com links diretos reais (`https://www.camara.leg.br/cota-parlamentar/documentos/publ/...`), CNPJs autênticos e fornecedores legítimos.
- **Coerência temporal:** 100% dos casos de variação decorrem de novas despesas lançadas no mês de setembro de 2026 pelas Casas legislativas após o fechamento do snapshot versionado. Nenhum valor no repositório era superior ao oficial atual.
- **Apoio ao achado A6 e tarefa P6:** Esta conferência confirma empiricamente que despesas de exercício corrente necessitam de exibição explícita da data da coleta na interface (`coletado_em`), para distinguir dados de snapshot de consultas em tempo real.

---

## 5. Conclusão Geral da Tarefa P4

1. **Integridade Confirmada:** Os módulos de **Votações Nominais**, **Emendas Parlamentares (CGU)** e **Despesas (CEAP/CEAPS)** utilizam **fontes oficiais verídicas e rastreáveis**.
2. **Isolamento da Falha:** A geração sintética de dados por fórmulas arbitradas (A1–A6) ficou **restrita exclusivamente ao módulo TSE 2026** ([`scripts/tse/build_congresso_2026.py`](../scripts/tse/build_congresso_2026.py) e [`scripts/tse/build_presidencia.py`](../scripts/tse/build_presidencia.py)).
3. **Recomendações para P6 e Ingestão:** Manter a execução de rotinas periódicas de atualização de CEAP/CEAPS e expor o timestamp de coleta no frontend.

---
*Relatório gerado automaticamente e conferido por amostragem em 2026-09-24.*
