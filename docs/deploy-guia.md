# Guia de Publicação & Configuração de Domínio (MVP v0)

Este documento descreve como colocar o site do **Ficha do Político** no ar e conectar ao domínio `.com.br` sem nenhum custo de servidor.

---

## 1. Opções de Hospedagem Gratuita

O site foi construído com **Astro SSG** (Static Site Generation). Ele gera 515 páginas estáticas puras (513 deputados + Home + Critérios).

### Opção A: GitHub Pages (Padrão para repositório público)
Com o repositório público, o GitHub Pages é a opção mais nativa e direta:
1. No repositório GitHub, vá em **Settings** → **Pages**.
2. Sob **Build and deployment** → **Source**, selecione **GitHub Actions**.
3. O fluxo automatizado em `.github/workflows/deploy.yml` fará o build e deploy a cada push ou merge na `main`.
4. O endereço temporário será: `https://ficha-do-politico.github.io/fichadopolitico/`.

### Opção B: Cloudflare Pages (Alternativa / Repositórios privados)
Se o time optar por manter o repositório privado no futuro ou desejar proteção contra ataques de negação de serviço (DDoS) via Cloudflare:
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

## 2. Conectando o Domínio `.com.br` (Registro.br)

Ao registrar `fichadopolitico.com.br` no [Registro.br](https://registro.br):

### Método 1: Apontamento direto no GitHub Pages
1. No painel de DNS do [Registro.br](https://registro.br), crie 4 registros do tipo **A** (para a raiz `@`) apontando para os IPs do GitHub Pages:
   - `185.199.108.153`
   - `185.199.109.153`
   - `185.199.110.153`
   - `185.199.111.153`
2. Crie 1 registro do tipo **CNAME**:
   - Nome: `www`
   - Destino: `ficha-do-politico.github.io.`
3. No GitHub: **Settings** → **Pages** → em **Custom domain**, digite `fichadopolitico.com.br` e clique em Save.
4. Após verificação do DNS pelo GitHub, marque a caixa **Enforce HTTPS**.

### Método 2: DNS via Cloudflare (Se usar Cloudflare Pages)
1. No painel da Cloudflare, clique em **Add a Site** e digite `fichadopolitico.com.br`.
2. A Cloudflare fornecerá 2 servidores de nome (nameservers), ex:
   - `ns1.cloudflare.com`
   - `ns2.cloudflare.com`
3. Acesse o painel do [Registro.br](https://registro.br), clique no domínio e altere os **Servidores DNS** para os 2 endereços fornecidos pela Cloudflare.
4. No projeto do Pages, vá em **Custom Domains** → digite `fichadopolitico.com.br`.
5. A Cloudflare configura o apontamento e o certificado SSL automaticamente.

### Método 3: Apontamento direto CNAME no Registro.br (Cloudflare Pages)
Se preferir manter o DNS padrão do Registro.br:
1. No projeto Pages, vá em **Custom Domains** → adicione `www.fichadopolitico.com.br`.
2. No painel de DNS do Registro.br, adicione uma entrada do tipo `CNAME`:
   - Nome: `www`
   - Destino: `fichadopolitico.pages.dev`
3. Para a raiz (`fichadopolitico.com.br`), configure o redirecionamento web nativo do Registro.br para `https://www.fichadopolitico.com.br`.

---

## 3. Atualização Periódica dos Dados

Quando novas votações forem incluídas no catálogo:
1. Adicione a votação via `scripts/discovery_votacoes.py`.
2. Rode `python scripts/build_site_data.py`.
3. Faça commit e push para a `main`.
4. O GitHub Actions (ou Cloudflare Pages) detecta o commit no GitHub automaticamente e publica um novo build em minutos.
