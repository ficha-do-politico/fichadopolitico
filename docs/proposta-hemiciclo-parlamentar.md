# Especificação & Backlog: Composição do Congresso & Hemiciclo Parlamentar (Semi-Donut de Bancadas)

> **Status:** Proposta / Backlog (v2)  
> **Pilares:** Apartidarismo estrito ([AD-004](file:///C:/gitrepos/fichadopolitico/.specs/STATE.md#L29)), Verificabilidade Oficial ([AD-006](file:///C:/gitrepos/fichadopolitico/.specs/STATE.md#L32)) e Paridade Bicameral ([AD-011](file:///C:/gitrepos/fichadopolitico/.specs/STATE.md#L34)/[AD-014](file:///C:/gitrepos/fichadopolitico/.specs/STATE.md#L34)).

---

## 1. Visão do Produto & Proposta de Valor

A **Composição das Bancadas do Congresso** permite ao cidadão apreender visualmente a distribuição de forças políticas nas duas casas legislativas:
- **Câmara dos Deputados:** 513 cadeiras (distribuídas entre partidos e federações).
- **Senado Federal:** 81 cadeiras (distribuídas entre bancadas e blocos oficiais).

Em vez de exigir a leitura de extensas tabelas de legendas, o portal oferecerá uma visualização geométrica clara das bancadas, permitindo auditar imediatamente a correlação de poder e a formação de maiorias legislativas.

---

## 2. Paradigma Visual: Semi-Donut Particionado vs. Pontinhos de Assento

Com base no benchmark prático de infografia cívica, avaliamos dois formatos visuais:

### 2.1. Abordagem Recomendada: Semi-Donut Particionado (Arco de Bancadas)
*Inspirado na infografia oficial de composição partidária da Câmara dos Deputados.*
- **Como funciona:** Um semicírculo oco (formato meia-rosca/arco) dividido em fatias contínuas proporcionais ao número de assentos de cada partido ou federação partidária.
- **Por que é superior no produto:**
  1. **Usabilidade Mobile Impecável:** Em telas de smartphones (360px a 400px), desenhar 513 bolinhas individuais gera um borrão ilegível onde o toque tátil é impossível. O semi-donut mantém fatias nítidas, legíveis e confortáveis para o toque em qualquer resolução.
  2. **Compreensão Imediata de Maioria:** O arco contínuo permite identificar de relance o domínio de bancadas sobre o hemiciclo e a proximidade da maioria simples (257 na Câmara, 41 no Senado) ou de três quintos (308 na Câmara, 49 no Senado).
  3. **Miolo Informativo Interativo:** O espaço interno oco do arco é aproveitado para exibir a bancada em foco no hover/touch (ex: `PL • 99 deputados (19,3%)`) ou elencar legendas com representação menor (1 a 3 cadeiras).

### 2.2. Abordagem Secundária: Matriz de Cadeiras Pontilhadas (Pontinhos)
- Representação de cada assento por um círculo discreto (81 círculos no Senado em 3 fileiras; 513 círculos na Câmara em 6 fileiras).
- **Adequação:** Viável para o **Senado Federal** (81 nós têm boa legibilidade em telas médias), mas subótimo para a Câmara dos Deputados em dispositivos móveis. Pode ser considerado como modo de visualização alternativo específico para o Senado ou para telas desktop em votações nominais.

---

## 3. Modos de Uso na Plataforma

### 3.1. Modo Composição do Congresso (Foto do Poder Atual)
- **Localização:** Home (`/`), aba de Parlamentares ou seção `/congresso`.
- **Alternador de Casas:** Botão de controle direto `[ Câmara (513) | Senado (81) ]`.
- **Interatividade:**
  - **Hover/Tap na fatia do partido:** Destaca a fatia, esmaece as demais e exibe no centro a sigla, total de cadeiras e percentual da casa.
  - **Clique de filtro:** Clicar na fatia do partido aciona instantaneamente o filtro multiselect da página, exibindo na listagem apenas os parlamentares daquela bancada.
  - **Legendas Menores:** Partidos com bancadas unitárias ou reduzidas podem ser listados no miolo central ou agrupados de forma transparente com expansão sob demanda.

### 3.2. Modo Votação Nominal (Placar do Plenário)
- **Localização:** Página individual de deliberação (`/votacao/[id]`).
- **Objetivo:** O arco do semi-donut é colorido conforme a deliberação nominal registrada na matéria:
  - 🟢 **Verde:** Voto "Sim"
  - 🔴 **Vermelho:** Voto "Não"
  - 🟡 **Amarelo:** Abstenção / Obstrução / Art. 17
  - ⚪ **Cinza:** Não votou / Ausência registrada
- **Valor Cívico:** O cidadão visualiza instantaneamente como a matéria passou ou travou no plenário sem mediação retórica.

---

## 4. Diretriz de Neutralidade & Ordenação ([AD-004](file:///C:/gitrepos/fichadopolitico/.specs/STATE.md#L29))

> **Regra Mandatória de Apartidarismo:**  
> É terminantemente **PROIBIDO** ordenar as fatias do arco simulando um espectro ideológico esquerda-direita ("esquerda", "centro", "direita"), o que constituiria arbitragem subjetiva e infração das diretrizes editoriais do projeto.

### Critérios Neutros de Ordenação das Fatias:
1. **Critério Canônico (Tamanho de Bancada):** Fatias dispostas da maior bancada para a menor, garantindo leitura hierárquica clara do peso de cada agremiação.
2. **Critério de Bloco Oficial:** Agrupamento por blocos parlamentares formalmente registrados perante a Mesa Diretora da Câmara ou do Senado (dados oficiais de API).
3. **Critério Alfabético:** Ordenação neutra por ordem alfabética da sigla partidária.

---

## 5. Arquitetura Técnica & Performance (Astro SSG)

- **Renderização em SVG Puro:**
  - As fatias do semi-donut são geradas como arcos vetoriais `<path d="M... A... L... A... Z">` computados estaticamente durante o build.
  - Sem uso de bibliotecas clientes pesadas (ex.: dependência inteira de D3 ou Chart.js desnecessária).
  - Peso do componente inferior a 3 KB.
- **Acessibilidade e Semântica:**
  - Cada fatia possui atributos ARIA (`role="graphics-symbol"`, `aria-label="Bancada do [Partido]: [N] cadeiras, [X]%"`) e suporte a navegação por foco de teclado.
- **Responsividade Total:**
  - `viewBox` vetorial escalável preservando proporções perfeitas de 320px a 4K.

---

## 6. Checklist de Implementação

- [ ] Utilitário geométrico para cálculo de arcos SVG de semi-donut (`scripts/core/svg_arc.py` ou helper TypeScript).
- [ ] Agregação de totais de bancadas no compilador de dados (`scripts/build_site_data.py`).
- [ ] Componente `SemiDonutBancadas.astro` com suporte a alternância Câmara/Senado.
- [ ] Integração do clique na fatia com o filtro multiselect de parlamentares em `index.astro`.
- [ ] Variante do componente para placares de votação nominal (`/votacao/[id]`).
- [ ] Testes automatizados de consistência da soma das cadeiras (513 e 81) em `tests/test_bancadas.py`.
