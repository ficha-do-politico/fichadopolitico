# Especificação & Backlog: Hemiciclo Parlamentar Interativo (Cadeiras do Congresso)

> **Status:** Proposta / Backlog (v2)  
> **Pilares:** Apartidarismo estrito ([AD-004](file:///C:/gitrepos/fichadopolitico/.specs/STATE.md#L29)), Verificabilidade Oficial ([AD-006](file:///C:/gitrepos/fichadopolitico/.specs/STATE.md#L32)) e Paridade Bicameral ([AD-011](file:///C:/gitrepos/fichadopolitico/.specs/STATE.md#L34)/[AD-014](file:///C:/gitrepos/fichadopolitico/.specs/STATE.md#L34)).

---

## 1. Visão do Produto & Proposta de Valor

O **Hemiciclo Parlamentar** (*Parliamentary Seating / Hemicycle Chart*) é a representação visual em formato de semicírculo da distribuição física e quantitativa das cadeiras legislativas:
- **Senado Federal:** 81 assentos parlamentares (distribuídos em 3 fileiras concêntricas).
- **Câmara dos Deputados:** 513 assentos parlamentares (distribuídos em 5 a 6 fileiras concêntricas).

Em vez de forçar o cidadão a ler tabelas numéricas extensas, o Hemiciclo permite apreender imediatamente a **composição das bancadas** e a **geometria de votação** de qualquer deliberação oficial do Congresso Nacional.

---

## 2. Modos de Uso na Plataforma

### 2.1. Modo Composição do Congresso (Foto do Poder Atual)
- **Localização:** Home (`/`), aba de Parlamentares ou seção dedicada `/congresso`.
- **Objetivo:** Exibir o tamanho relativo de cada bancada partidária ou bloco parlamentar oficial registrado.
- **Interatividade:**
  - **Hover/Tap no assento:** Exibe tooltip com foto, nome parlamentar, partido e UF do titular.
  - **Hover/Tap na legenda do partido:** Destaca todos os assentos daquela bancada e atenua os demais.
  - **Filtro de busca integrado:** Clicar numa bancada filtra automaticamente a listagem de parlamentares da página.

### 2.2. Modo Votação Nominal (Placar do Plenário)
- **Localização:** Página individual de votação (`/votacao/[id]`).
- **Objetivo:** Visualizar o resultado de votações nominais cruciais no plenário (Câmara ou Senado).
- **Codificação de Cores Oficial:**
  - 🟢 **Verde:** Voto "Sim"
  - 🔴 **Vermelho:** Voto "Não"
  - 🟡 **Amarelo:** Abstenção / Obstrução / Artigo 17
  - ⚪ **Cinza:** Não votou / Ausência registrada
- **Valor Cívico:** O eleitor compreende visualmente de onde veio o apoio ou a rejeição da matéria sem intermediários ou narrativas enviesadas.

---

## 3. Diretriz de Neutralidade & Ordenação de Cadeiras ([AD-004](file:///C:/gitrepos/fichadopolitico/.specs/STATE.md#L29))

> **Regra Mandatória de Apartidarismo:**  
> É estritamente **PROIBIDO** ordenar os assentos da esquerda para a direita simulando um espectro ideológico ("esquerda", "centro", "direita"), pois isso exigiria arbitragem subjetiva e juízo de valor.

### Critérios Oficiais de Agrupamento e Ordenação:
1. **Agrupamento por Bancada:** Assentos do mesmo partido ficam contíguos no arco.
2. **Agrupamento por Bloco Parlamentar Oficial:** Opção de agrupar conforme os blocos partidários formalmente registrados na Mesa Diretora da Câmara e do Senado (dados oficiais de API).
3. **Ordenação Neutra das Bancadas no Arco:**
   - **Critério A (Padrão):** Por tamanho decrescente de bancada (maiores bancadas agrupadas ao centro ou nas extremidades com simetria neutra).
   - **Critério B:** Por ordem alfabética da sigla partidária (critério 100% formal e objetivo).

---

## 4. Arquitetura Técnica & Performance (Astro SSG)

- **Geração Estática em SVG:**
  - As coordenadas polares `(x, y)` dos arcos concêntricos são computadas via função matemática leve durante o build (`scripts/build_site_data.py` ou componente Astro server-side).
  - Sem necessidade de runtime cliente de bibliotecas externas pesadas (como D3.js completo).
  - SVG inline com classes Tailwind para transições de cor e opacidade (`transition-colors duration-150`).
- **Acessibilidade (a11y):**
  - Cada ponto `<circle>` possui atributos `role="button"`, `aria-label="Senador [Nome] - [Partido]/[UF]"` e foco por teclado.
- **Responsividade Mobile:**
  - `viewBox` responsivo com escala vetorial automática, garantindo legibilidade perfeita tanto em telas de 360px quanto em monitores desktop 4K.

---

## 5. Checklist de Implementação Futura

- [ ] Utilitário geométrico para cálculo de posições concêntricas de hemiciclos (81 e 513 nós).
- [ ] Ingestão dos blocos partidários vigentes via APIs de dados abertos da Câmara e Senado.
- [ ] Componente `HemicycleChart.astro` reutilizável em modo `composicao` e modo `votacao`.
- [ ] Integração com as páginas de votação nominal (`/votacao/[id]`).
- [ ] Testes de conformidade de schema e acessibilidade a11y em `tests/test_hemiciclo.py`.
