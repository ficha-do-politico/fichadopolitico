# Discussão & Análise de Naming — Ficha do Político

> **Data:** 2026-09-12  
> **Status:** Proposta para alinhamento da equipe (Antonio, Soutto, Ludovic, Layr)  
> **Objetivo:** Avaliar a marca atual (`fichadopolitico`), analisar propostas alternativas para aumentar o apelo popular/viralidade orgânica e definir critérios de escolha sem comprometer o apartidarismo e a credibilidade.

---

## 1. Contexto & Motivação

O nome provisório do projeto foi definido como **Ficha do Político** (`fichadopolitico`).  
Embora seja descritivo e funcional para a fase inicial, surgiu o questionamento sobre se este é o melhor nome para:
1. "Pegar" no imaginário popular e facilitar o boca a boca (WhatsApp, redes sociais);
2. Refletir com precisão a proposta do produto (MVP focado em votos nominais de deputados federais e roadmap futuro de gastos/patrimônio);
3. Manter autoridade técnica e institucional, evitando a percepção de viés partidário ou sensacionalismo.

---

## 2. Diagnóstico do Nome Atual (`fichadopolitico`)

### Prós
- **SEO e clareza imediata:** Quem pesquisa por um parlamentar no Google tem intenção de busca alinhada a "ficha do deputado X".
- **Memória cultural:** Alude ao conceito de "ficha limpa" e "puxar a ficha", já consolidado no Brasil.

### Contras & Limitações
- **Tom policialesco/punitivo:** O termo "ficha" remete frequentemente a antecedentes criminais ou ficha policial. Para uma plataforma cujo objetivo é expor dados oficiais e neutros (onde a maioria dos dados da v0 são votos regulares em plenário), pode passar a impressão de um tribunal de exceção pré-julgador.
- **Pouco dinâmico:** É um substantivo estático; não estimula ação imediata nem vira verbo fácil no cotidiano.
- **Foco restrito ao indivíduo:** Centraliza a figura no "político" como pessoa, quando o núcleo da ferramenta é a fiscalização do mandato, dos votos e dos recursos públicos.

---

## 3. A Armadilha da "Viralidade por Meme" vs. Credibilidade Cívica

Ao buscar um nome com potencial de "viralizar", é comum cogitar expressões coloquiais, perguntas informais ou trocadilhos (ex: *"tuvotounoque"*). Contudo, em tecnologia cívica e dados públicos no Brasil, essa abordagem carrega riscos estruturais:

1. **Desqualificação imediata por viés:**  
   Em discussões políticas acaloradas, se o link compartilhado tem cara de piada, meme ou página de sátira, o interlocutor do outro lado desqualifica o dado instantaneamente (*"isso é meme/página partidária"*). Para ser usado como argumento de fato verificado, o nome precisa carregar **peso e sobriedade técnica**.
2. **Regionalismo e estranhamento linguístico:**  
   Termos regionais (como o pronome "tu") soam muito naturais no Rio Grande do Sul e partes do Norte/Nordeste, mas soam estranhos ou artificiais em São Paulo, Minas Gerais e Centro-Oeste. A ferramenta é de abrangência federal.
3. **Viralidade sustentável:**  
   O que faz ferramentas cívicas de sucesso viralizarem (como *Agência Lupa*, *Aos Fatos*, *Serenata de Amor*, *Meu Congresso Nacional*) não é a piada, mas sim a **utilidade imediata** e a **facilidade de citar a fonte como autoridade**.

---

## 4. Mapeamento de Rotas de Naming

| Território Semântico | Exemplos | Prós | Contras / Riscos |
| :--- | :--- | :--- | :--- |
| **Rota 1: Ação / Verbo**<br>*(O que o cidadão faz na prática)* | • **ComoVotou**<br>• **QuemVotou**<br>• **PuxaFicha** | • Vira expressão instantânea no WhatsApp (*"Como votou seu deputado? Olha no ComoVotou"*).<br>• Curto, amigável, direto ao ponto e fácil de digitar no celular. | `ComoVotou` pode exigir esforço de comunicação quando o projeto expandir para gastos (CEAP) e patrimônio (TSE). |
| **Rota 2: Transparência & Dados Crus**<br>*(Institucional moderno e neutro)* | • **Ficha Aberta**<br>• **Voto Aberto**<br>• **Raio-X Parlamentar** | • Soa perene, jornalístico e confiável para imprensa, academia e eleitores.<br>• Apartidarismo explícito no tom. | Menos informal; `Voto Aberto` pode colidir com a bandeira legislativa sobre votações não-secretas. |
| **Rota 3: Expressão Popular Brasileira**<br>*(Identidade cultural forte)* | • **PuxaCapivara** / **Capivara**<br>• **Preto no Branco**<br>• **Sem Rodeio** | • "Puxar a capivara" é a gíria nacional definitiva para investigar histórico.<br>• Memorabilidade altíssima. | "Capivara" no linguajar de segurança pública é quase exclusivamente sinônimo de histórico criminal. Risco de parecer perseguição. |
| **Rota 4: Evolução Direta**<br>*(Lapidação do nome atual)* | • **Ficha Parlamentar**<br>• **A Ficha** (ex: `aficha.org`) | • Resolve o tom excessivamente informal mantendo a raiz do projeto original. | Pode soar excessivamente burocrático se não tiver um design forte. |

---

## 5. Comparativo dos Dois Principais Finalistas

### Opção A: `ComoVotou` (Foco em engajamento e utilidade imediata)
- **Posicionamento:** A ferramenta definitiva para consultar como cada deputado votou nas matérias do Congresso.
- **Por que funciona:** 
  - Conecta 1:1 com a dor principal do eleitor em época de eleição ou votação polêmica.
  - Impossível de associar a qualquer partido ou ideologia.
  - Nome curto (9 letras), sonoro, sem necessidade de hífen ou caracteres complexos.
- **Trade-off:** Se a plataforma no v1/v2 tiver forte presença de gastos (CEAP) e patrimônio declarado (TSE), o nome precisará ser complementado por uma assinatura/tagline institucional (ex: *ComoVotou — Votações, gastos e histórico parlamentar*).

### Opção B: `Ficha Aberta` (Foco em perenidade e escopo amplo)
- **Posicionamento:** A plataforma de dados abertos e históricos de mandatos públicos.
- **Por que funciona:**
  - Preserva a ideia original da "ficha", mas remove a carga negativa substituindo por "aberta" (alusão direta a dados abertos e transparência ativa).
  - Acomoda perfeitamente votações nominais, gastos da cota parlamentar, doações de campanha e patrimônio sem nenhum estranhamento temático.
- **Trade-off:** Tem um apelo ligeiramente mais institucional e menos coloquial do que `ComoVotou`.

---

## 6. Checklist de Decisão para a Equipe

Antes de bater o martelo sobre a marca, os seguintes passos técnicos e estratégicos devem ser validados:

1. **Consulta de domínios no [Registro.br](https://registro.br):**
   - Disponibilidade de `.com.br` e `.org.br` para os finalistas.
2. **Disponibilidade internacional (`.org` / `.net`):**
   - Importante caso o time prefira um TLD de organização sem fins lucrativos.
3. **Handles de redes sociais:**
   - Checar disponibilidade no Bluesky, X/Twitter, Instagram e GitHub.
4. **Votação interna:**
   - Alinhamento entre os membros do time com base nas três perguntas-chave:
     - *Um eleitor desconfiado aceita o dado vindo desse domínio como neutro?*
     - *É fácil de ditar por áudio de WhatsApp sem precisar soletrar?*
     - *Resiste ao crescimento do escopo pelos próximos 3 a 5 anos?*
