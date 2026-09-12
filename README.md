# fichadopolitico

Ficha pública e apartidária de parlamentares: como votaram, quanto gastaram, o que declaram de patrimônio — sempre com a fonte oficial linkada.

**Nosso compromisso é com a verdade.**

## Status

🚧 MVP em construção — veja a especificação detalhada em [MVP.md](MVP.md) (discussões e histórico na [issue #1](../../issues/1)).

## Fontes de dados (planejadas)

- Câmara dos Deputados — [Dados Abertos](https://dadosabertos.camara.leg.br/) (votações nominais, deputados)
- Senado Federal — Dados Abertos
- Portal da Transparência (gastos)
- TSE (patrimônio declarado, histórico eleitoral)

Para a especificação técnica detalhada das APIs e dumps de dados oficiais (incluindo Câmara, Senado, TSE, CGU, TCU e CNJ), veja [fontes-oficiais-de-dados.md](fontes-oficiais-de-dados.md).  
Para análise de projetos cívicos correlatos, benchmarks de UX e referências metodológicas, veja [referencias.md](referencias.md).

## Princípios

- Apartidário — nenhum dado é filtrado ou destacado por viés político.
- Toda informação exibida cita a fonte oficial original.
- Código aberto (MIT); os dados em si são públicos por natureza.

## Como rodar o site localmente

```bash
# 1. Compilar os dados de votações e deputados
python scripts/build_site_data.py

# 2. Executar testes de integridade de dados e LGPD
python -m unittest discover tests

# 3. Instalar dependências do site
cd site
npm install

# 4. Rodar em modo de desenvolvimento (http://localhost:4321)
npm run dev

# 5. Gerar build estático pré-renderizado (pasta site/dist/)
npm run build
```

Para instruções de hospedagem gratuita com domínio próprio, veja o [Guia de Publicação e Deploy](docs/deploy-guia.md).

## Como contribuir

Abra uma issue ou peça pra entrar na organização. Não precisa nome real — handle já basta.
