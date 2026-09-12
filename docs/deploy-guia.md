# Guia de Publicação & Configuração de Domínio (MVP v0)

Este documento descreve como colocar o site do **Ficha do Político** no ar e conectar ao domínio `.com.br` sem nenhum custo de servidor, mantendo o repositório **privado** e com proteção contra quedas.

---

## 1. Por que Cloudflare Pages ou Vercel?

O site foi construído com **Astro SSG** (Static Site Generation). Isso significa que, no momento do build, ele gera 515 páginas estáticas puras (513 deputados + Home + Critérios).

Como o repositório no GitHub atualmente é **privado**:
- **GitHub Pages:** Requer plano pago do GitHub para repositórios privados.
- **Cloudflare Pages / Vercel:** Suportam repositórios privados **gratuitamente**, com CDN global ultrarrápida, SSL automático e proteção contra ataques de negação de serviço (DDoS).

---

## 2. Opção Recomendada: Cloudflare Pages (100% Gratuito)

### Passo 1: Conectar o Repositório
1. Acesse o painel da [Cloudflare](https://dash.cloudflare.com/) (crie conta gratuita se não tiver).
2. Vá em **Workers & Pages** → **Create application** → aba **Pages** → **Connect to Git**.
3. Selecione a organização `ficha-do-politico` e o repositório `fichadopolitico`.

### Passo 2: Configurações de Build
Preencha exatamente os campos abaixo:
- **Framework preset:** `Astro`
- **Root directory:** `site`
- **Build command:** `npm run build`
- **Build output directory:** `dist`
- **Environment variables:** (nenhuma necessária para o v0)

Clique em **Save and Deploy**. Em menos de 1 minuto o site estará publicado em um subdomínio temporário (ex: `fichadopolitico.pages.dev`).

---

## 3. Conectando o Domínio `.com.br` (Registro.br)

Ao comprar o domínio `fichadopolitico.com.br` no [Registro.br](https://registro.br):

### Método A: DNS via Cloudflare (Recomendado)
1. No painel da Cloudflare, clique em **Add a Site** e digite `fichadopolitico.com.br`.
2. A Cloudflare fornecerá 2 servidores de nome (nameservers), ex:
   - `ns1.cloudflare.com`
   - `ns2.cloudflare.com`
3. Acesse o painel do [Registro.br](https://registro.br), clique no domínio e altere os **Servidores DNS** para os 2 endereços fornecidos pela Cloudflare.
4. No projeto do Pages, vá em **Custom Domains** → digite `fichadopolitico.com.br`.
5. A Cloudflare configura o apontamento e o certificado SSL automaticamente.

### Método B: Apontamento direto CNAME no Registro.br
Se preferir manter o DNS padrão do Registro.br:
1. No projeto Pages, vá em **Custom Domains** → adicione `www.fichadopolitico.com.br`.
2. No painel de DNS do Registro.br, adicione uma entrada do tipo `CNAME`:
   - Nome: `www`
   - Destino: `fichadopolitico.pages.dev`
3. Para a raiz (`fichadopolitico.com.br`), configure o redirecionamento web nativo do Registro.br para `https://www.fichadopolitico.com.br`.

---

## 4. Atualização Periódica dos Dados

Quando novas votações forem incluídas no catálogo:
1. Adicione a votação via `scripts/discovery_votacoes.py`.
2. Rode `python scripts/build_site_data.py`.
3. Faça commit e push para a `main`.
4. A Cloudflare detecta o commit no GitHub automaticamente e dispara um novo build em segundos.
