# Especificação do MVP — Ficha do Político

> **Status:** MVP v0 online / v1 em expansão (Senado Federal)  
> **Última atualização:** 2026-09-13 (reflete decisões AD-001 a AD-014)

Este documento define o escopo do **Produto Mínimo Viável (MVP)** do Ficha do Político. Ele é a fonte da verdade sobre o que estamos construindo agora e o que fica para depois, versionado diretamente no repositório através de Pull Requests.

---

## 1. O Problema & A Proposta de Valor

Hoje, para saber como um parlamentar votou em decisões de grande repercussão nacional (ex.: *Escala 6×1*, *Marco Temporal*, *Reforma Tributária*, *Isenções Fiscais*), o cidadão enfrenta uma jornada burocrática e confusa:
1. Descobrir em notícias o número do projeto (PL, PEC, MPV).
2. Entrar no portal da Câmara e decifrar tramitações e requerimentos regimentais.
3. Localizar o parlamentar em listas extensas de votação.

Ferramentas existentes no mercado (como Meu Congresso e Radar do Congresso) agregam muitos dados, mas são orientadas a sessões legislativas ou apresentam dumps cronológicos crus onde a maioria dos votos são votações procedimentais sem interesse público geral.

### A Proposta da Ficha (Diferencial)
> **A maneira mais rápida e simples de um cidadão buscar um deputado federal e ver imediatamente como ele votou em um conjunto selecionado e transparente de decisões cruciais para o país — sempre com link direto para a fonte oficial e sem nenhuma adjetivação ou viés partidário.**

---

## 2. Escopo do MVP v0 (Foco Atual)

O MVP v0 valida o formato da ficha com o menor esforço viável:

### O que ENTRA no v0:
1. **Cargo Único:** **Deputado Federal** (513 parlamentares da Câmara dos Deputados em exercício).
2. **Fonte de Dados Única:** API de Dados Abertos da Câmara dos Deputados (`dadosabertos.camara.leg.br`).
3. **Busca Search-First:** Campo de busca simples por nome do parlamentar.
4. **Ficha do Deputado:**
   - Dados básicos de identificação: nome eleitoral, foto oficial, partido e estado (UF).
   - Link direto para o perfil oficial na Câmara.
5. **Votos em Temas Curados:**
   - Lista de **4 a 10 votações de grande relevância pública** (seed inicial: *Escala 6×1*, *MP do Gás do Povo*, *PEC da Segurança Pública*, *Veto da Dosimetria*).
   - Voto nominal do deputado em cada tema: `Sim`, `Não`, `Abstenção`, `Obstrução`, `Ausente` (conforme registrado oficialmente pela API).
   - Links duplos de verificabilidade para cada voto: link para a votação oficial e link para a íntegra da proposição.
6. **Catálogo de Temas Público e Versionado:** O arquivo com os temas escolhidos e os IDs das votações oficiais fica aberto no repositório, com critérios de curadoria documentados e auditáveis.

---

## 3. Escopo do MVP v1 (Próxima Fase)

Após validar a experiência do v0 com usuários reais, o escopo se expandirá para:
1. **Senado Federal:** Paridade completa para os 81 Senadores (dados da API do Senado).
2. **Gastos Parlamentares (CEAP / CEAPS):** Detalhamento de notas fiscais e gastos das cotas parlamentares da Câmara e do Senado.
3. **Patrimônio Declarado (TSE):** Evolução de bens declarados à Justiça Eleitoral a cada eleição.
4. **Catálogo Ampliado:** Expansão da curadoria para 20 a 50 temas nacionais relevantes.
5. **Navegação Avançada:** Filtros por partido, estado e temas.

---

## 4. O que está FORA DE ESCOPO

### Fora de escopo no v0 (de propósito):
- Senado, gastos e patrimônio (planejados para o v1).
- Contas de usuário, login, deputados salvos ou favoritos.
- Notificações ou alertas.
- Aplicativo mobile nativo (o site será 100% web responsivo).

### Fora de escopo DEFINITIVO (Decisões Arquiteturais):
1. **Esferas Municipal e Estadual (AD-011):** Não cobriremos Vereadores, Prefeitos, Deputados Estaduais ou Governadores. O Brasil possui 5.570 municípios e 27 estados sem APIs abertas unificadas; tentar raspar portais heterogêneos inviabilizaria a manutenção e a verificabilidade técnica do projeto.
2. **Julgamentos de Valor ou Scores Políticos (AD-004):** Sem notas, sem rankings, sem classificação ideológica ("conservador", "progressista", "governista", "oposição"). A ficha exibe apenas o dado cru oficial. A interpretação é soberana do eleitor.
3. **Exibição de Dados Pessoais Sensíveis (AD-009):** Não exibimos CPF, telefone pessoal ou email, respeitando a privacidade e a LGPD.

---

## 5. Como Propor Mudanças de Escopo

Para sugerir inclusão de novos campos, alteração de fases ou ajustes de roadmap:
1. Não utilize apenas comentários soltos em issues do GitHub.
2. Abra um Pull Request alterando este arquivo (`MVP.md`) ou propondo uma nova decisão arquitetural em `.specs/STATE.md`.
3. O time (Antonio, Soutto, Layr, Ludovic) revisa e debate as alterações com base na viabilidade técnica e nos pilares do projeto.
