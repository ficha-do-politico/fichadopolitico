# Ficha do politico

>**Nosso compromisso é com a verdade.**

Ficha pública e apartidária de parlamentares: como votaram, quanto gastaram, o que declaram de patrimônio — sempre com a fonte oficial linkada.

## O Problema & A Proposta de Valor

Hoje, para saber como um parlamentar votou ou quanto gastou, o cidadão enfrenta uma jornada burocrática entre portais de transparência confusos, diários oficiais e tramitações regimentais complexas. Ferramentas existentes muitas vezes agregam dados demais sem curadoria ou aplicam scores subjetivos.

A **Ficha do Político** é a maneira mais rápida e simples de qualquer cidadão buscar um parlamentar e auditar votos, gastos de cota e patrimônio — em dados crus, sem juízo de valor, sem filtros ideológicos e sempre com link direto para a fonte oficial primária.

## Status & Roadmap

🚧 **Em produção (v1 bicameral em expansão):** veja o escopo ativo, decisões arquiteturais consolidadas (ADRs) e roadmap em [.specs/STATE.md](.specs/STATE.md).

- Para a especificação técnica detalhada das APIs e dumps de dados oficiais (incluindo Câmara, Senado, TSE, CGU, TCU e CNJ), veja [fontes-oficiais-de-dados.md](fontes-oficiais-de-dados.md).
- Para análise de projetos cívicos correlatos, benchmarks de UX e referências metodológicas, veja [referencias.md](referencias.md).

## Princípios

- Apartidário — nenhum dado é filtrado ou destacado por viés político.
- Toda informação exibida cita a fonte oficial original.
- Código aberto (MIT); os dados em si são públicos por natureza.

## Como rodar o site localmente

Recomendamos o uso de [uv](https://github.com/astral-sh/uv) para gerenciamento rápido do ambiente Python.

```bash
# 1. Compilar os dados de votações e parlamentares
uv run python scripts/build_site_data.py

# 2. Executar testes de integridade de dados e LGPD
uv run python -m unittest discover tests

# 3. Validar linter e formatação (opcional)
uv run ruff check

# 4. Instalar dependências do site
cd site
npm install

# 5. Rodar em modo de desenvolvimento (http://localhost:4321)
npm run dev

# 6. Gerar build estático pré-renderizado (pasta site/dist/)
npm run build
```

Para instruções de hospedagem gratuita com domínio próprio, veja o [Guia de Publicação e Deploy](docs/deploy-guia.md).

## Como contribuir

Abra uma issue ou peça pra entrar na organização. Não precisa nome real — handle já basta.
