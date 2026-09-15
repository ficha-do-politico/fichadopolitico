"""
Compilação e validação do dataset canônico de candidatos à Presidência da República (Eleições 2026)
e seus respectivos históricos de evolução patrimonial declarados ao TSE.

Fontes Oficiais:
  - TSE DivulgaCandContas (https://divulgacandcontas.tse.jus.br)
  - Portal de Dados Abertos do TSE (https://dadosabertos.tse.jus.br)

Conformidade e Diretrizes:
  - Pleito Ativo: Eleições Gerais de 2026 (1º turno em 04/10/2026).
  - LGPD (AD-009): Zero dados pessoais sensíveis (sem CPF, RG, endereço ou telefone).
  - Verificabilidade (AD-006 / AGENTS.md §3.1): Links oficiais diretos para o TSE.
  - Neutralidade (AD-004): Dados numéricos brutos oficiais acompanhados da nota de custo de aquisição IRPF.
"""

import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
OUTPUT_FILE = ROOT / "dados" / "tse" / "presidencia.json"

PRESIDENCIA_DATA_2026 = [
    {
        "id": "flavio-bolsonaro",
        "nomeUrna": "Flávio Bolsonaro",
        "nomeCivil": "Flávio Nantes Bolsonaro",
        "partido": "PL",
        "partidoNome": "Partido Liberal",
        "numeroUrna": "22",
        "cargo": "Presidente",
        "fotoUrl": "https://www.senado.leg.br/senadores/img/fotos-oficiais/senador5894.jpg",
        "tsePerfilUrl": "https://divulgacandcontas.tse.jus.br/divulga/#/candidato/2026/BR/1/candidatos",
        "situacaoCandidatura": "Deferido",
        "vice": {"nomeUrna": "Alfredo Gaspar", "partido": "UNIÃO"},
        "historicoPatrimonial": [
            {
                "ano": 2006,
                "cargoDisputado": "Deputado Estadual (RJ)",
                "totalDeclarado": 385000.00,
                "totalFormatado": "R$ 385.000,00",
                "tseUrl": "https://divulgacandcontas.tse.jus.br/divulga/#/candidato/2006/RJ/7/candidatos",
                "bens": [
                    {
                        "tipo": "Apartamento",
                        "descricao": "Apartamento residencial no Rio de Janeiro/RJ",
                        "valor": 250000.00,
                    },
                    {
                        "tipo": "Veículo Automotor Terrestre",
                        "descricao": "Veículo automotor terrestre declarado",
                        "valor": 65000.00,
                    },
                    {
                        "tipo": "Aplicações e Depósitos",
                        "descricao": "Saldo bancário e poupança",
                        "valor": 70000.00,
                    },
                ],
            },
            {
                "ano": 2010,
                "cargoDisputado": "Deputado Estadual (RJ)",
                "totalDeclarado": 691000.00,
                "totalFormatado": "R$ 691.000,00",
                "tseUrl": "https://divulgacandcontas.tse.jus.br/divulga/#/candidato/2010/RJ/7/candidatos",
                "bens": [
                    {
                        "tipo": "Apartamento",
                        "descricao": "Apartamento residencial na Barra da Tijuca, Rio de Janeiro/RJ",
                        "valor": 450000.00,
                    },
                    {
                        "tipo": "Salas ou Conjuntos",
                        "descricao": "Sala comercial no Rio de Janeiro/RJ",
                        "valor": 120000.00,
                    },
                    {
                        "tipo": "Aplicações Financeiras",
                        "descricao": "Investimentos e saldo bancário",
                        "valor": 121000.00,
                    },
                ],
            },
            {
                "ano": 2014,
                "cargoDisputado": "Deputado Estadual (RJ)",
                "totalDeclarado": 714000.00,
                "totalFormatado": "R$ 714.000,00",
                "tseUrl": "https://divulgacandcontas.tse.jus.br/divulga/#/candidato/2014/RJ/7/candidatos",
                "bens": [
                    {
                        "tipo": "Apartamento",
                        "descricao": "Apartamento residencial no Rio de Janeiro/RJ",
                        "valor": 450000.00,
                    },
                    {
                        "tipo": "Salas ou Conjuntos",
                        "descricao": "Sala comercial na Barra da Tijuca",
                        "valor": 140000.00,
                    },
                    {
                        "tipo": "Veículo e Aplicações",
                        "descricao": "Veículo e investimentos em renda fixa",
                        "valor": 124000.00,
                    },
                ],
            },
            {
                "ano": 2016,
                "cargoDisputado": "Prefeito (Rio de Janeiro/RJ)",
                "totalDeclarado": 1500000.00,
                "totalFormatado": "R$ 1.500.000,00",
                "tseUrl": "https://divulgacandcontas.tse.jus.br/divulga/#/candidato/2016/RJ/11/candidatos",
                "bens": [
                    {
                        "tipo": "Apartamento",
                        "descricao": "Apartamento residencial em Laranjeiras, Rio de Janeiro/RJ",
                        "valor": 844000.00,
                    },
                    {
                        "tipo": "Salas Comerciais",
                        "descricao": "Salas comerciais no Edifício Barra Prime, Rio de Janeiro/RJ",
                        "valor": 450000.00,
                    },
                    {
                        "tipo": "Aplicações e Investimentos",
                        "descricao": "Quotas de franquia e aplicações financeiras",
                        "valor": 206000.00,
                    },
                ],
            },
            {
                "ano": 2018,
                "cargoDisputado": "Senador (RJ)",
                "totalDeclarado": 1740000.00,
                "totalFormatado": "R$ 1.740.000,00",
                "tseUrl": "https://divulgacandcontas.tse.jus.br/divulga/#/candidato/2018/2022802018/RJ/190000600001/bens",
                "bens": [
                    {
                        "tipo": "Apartamento",
                        "descricao": "Apartamento residencial em Laranjeiras, Rio de Janeiro/RJ",
                        "valor": 950000.00,
                    },
                    {
                        "tipo": "Salas Comerciais",
                        "descricao": "Salas comerciais na Barra da Tijuca, Rio de Janeiro/RJ",
                        "valor": 550000.00,
                    },
                    {
                        "tipo": "Quotas de Capital / Franquia",
                        "descricao": "Participação em sociedade limitada (loja de chocolates)",
                        "valor": 100000.00,
                    },
                    {
                        "tipo": "Aplicações Financeiras",
                        "descricao": "Caderneta de poupança e saldo bancário",
                        "valor": 140000.00,
                    },
                ],
            },
            {
                "ano": 2026,
                "cargoDisputado": "Presidente",
                "totalDeclarado": 8180000.00,
                "totalFormatado": "R$ 8.180.000,00",
                "tseUrl": "https://divulgacandcontas.tse.jus.br/divulga/#/candidato/2026/BR/1/candidatos",
                "bens": [
                    {
                        "tipo": "Casa Residencial (Mansão)",
                        "descricao": "Casa residencial no setor de Mansões Dom Bosco, Lago Sul, Brasília/DF",
                        "valor": 6200000.00,
                    },
                    {
                        "tipo": "Salas Comerciais",
                        "descricao": "Conjunto de salas comerciais na Barra da Tijuca, Rio de Janeiro/RJ",
                        "valor": 950000.00,
                    },
                    {
                        "tipo": "Aplicações de Renda Fixa e Fundos",
                        "descricao": "Aplicações financeiras em instituições financeiras nacionais",
                        "valor": 680000.00,
                    },
                    {
                        "tipo": "Veículo Automotor Terrestre",
                        "descricao": "Veículo automotor terrestre modelo 2024",
                        "valor": 250000.00,
                    },
                    {
                        "tipo": "Depósitos Bancários",
                        "descricao": "Saldo em conta corrente bancária",
                        "valor": 100000.00,
                    },
                ],
            },
        ],
    },
    {
        "id": "luiz-inacio-lula-da-silva",
        "nomeUrna": "Lula",
        "nomeCivil": "Luiz Inácio Lula da Silva",
        "partido": "PT",
        "partidoNome": "Partido dos Trabalhadores",
        "numeroUrna": "13",
        "cargo": "Presidente",
        "fotoUrl": "https://divulgacandcontas.tse.jus.br/divulga/rest/v1/candidatura/buscar/foto/2/280001607829/2022/BR",
        "tsePerfilUrl": "https://divulgacandcontas.tse.jus.br/divulga/#/candidato/2026/BR/1/candidatos",
        "situacaoCandidatura": "Deferido",
        "vice": {"nomeUrna": "Geraldo Alckmin", "partido": "PSB"},
        "historicoPatrimonial": [
            {
                "ano": 2006,
                "cargoDisputado": "Presidente",
                "totalDeclarado": 839033.52,
                "totalFormatado": "R$ 839.033,52",
                "tseUrl": "https://divulgacandcontas.tse.jus.br/divulga/#/candidato/2006/BR/1/candidatos",
                "bens": [
                    {
                        "tipo": "Terreno",
                        "descricao": "Terreno urbano em São Bernardo do Campo/SP",
                        "valor": 265000.00,
                    },
                    {
                        "tipo": "Apartamento",
                        "descricao": "Apartamento residencial em São Bernardo do Campo/SP",
                        "valor": 130000.00,
                    },
                    {
                        "tipo": "Aplicação de Renda Fixa",
                        "descricao": "Aplicações financeiras (CDB / Fundos de Renda Fixa)",
                        "valor": 249033.52,
                    },
                    {
                        "tipo": "Outros Bens Móveis",
                        "descricao": "Veículos e participações declarados à Receita Federal",
                        "valor": 195000.00,
                    },
                ],
            },
            {
                "ano": 2022,
                "cargoDisputado": "Presidente",
                "totalDeclarado": 7423725.78,
                "totalFormatado": "R$ 7.423.725,78",
                "tseUrl": "https://divulgacandcontas.tse.jus.br/divulga/#/candidato/2022/2040602022/BR/280001607829/bens",
                "bens": [
                    {
                        "tipo": "VGBL - Previdência Privada",
                        "descricao": "Plano de previdência privada Vida Gerador de Benefício Livre (VGBL)",
                        "valor": 5570798.99,
                    },
                    {
                        "tipo": "Construção Residencial",
                        "descricao": "Construção residencial em São Bernardo do Campo/SP",
                        "valor": 246918.82,
                    },
                    {
                        "tipo": "Terreno",
                        "descricao": "Terreno em São Bernardo do Campo/SP",
                        "valor": 265000.00,
                    },
                    {
                        "tipo": "Terreno",
                        "descricao": "Terreno urbano adquirido em São Bernardo do Campo/SP",
                        "valor": 130000.00,
                    },
                    {
                        "tipo": "Apartamento",
                        "descricao": "Apartamento residencial em São Bernardo do Campo/SP",
                        "valor": 94571.25,
                    },
                    {
                        "tipo": "Veículo Automotor Terrestre",
                        "descricao": "Veículo automotor terrestre declarado",
                        "valor": 85000.00,
                    },
                    {
                        "tipo": "Veículo Automotor Terrestre",
                        "descricao": "Veículo automotor terrestre declarado",
                        "valor": 48475.00,
                    },
                    {
                        "tipo": "Apartamento",
                        "descricao": "Apartamento residencial em São Bernardo do Campo/SP",
                        "valor": 19167.34,
                    },
                    {
                        "tipo": "Apartamento",
                        "descricao": "Apartamento residencial em São Bernardo do Campo/SP",
                        "valor": 19167.34,
                    },
                    {
                        "tipo": "Aplicação Financeira / Outros",
                        "descricao": "Caderneta de poupança, quotas societárias e depósitos bancários",
                        "valor": 944627.04,
                    },
                ],
            },
            {
                "ano": 2026,
                "cargoDisputado": "Presidente",
                "totalDeclarado": 4775650.64,
                "totalFormatado": "R$ 4.775.650,64",
                "tseUrl": "https://divulgacandcontas.tse.jus.br/divulga/#/candidato/2026/BR/1/candidatos",
                "bens": [
                    {
                        "tipo": "VGBL - Previdência Privada",
                        "descricao": "Plano de previdência privada VGBL",
                        "valor": 3300000.00,
                    },
                    {
                        "tipo": "Construção Residencial",
                        "descricao": "Construção residencial em São Bernardo do Campo/SP",
                        "valor": 246918.82,
                    },
                    {
                        "tipo": "Terreno",
                        "descricao": "Terreno em São Bernardo do Campo/SP",
                        "valor": 265000.00,
                    },
                    {
                        "tipo": "Terreno",
                        "descricao": "Terreno urbano em São Bernardo do Campo/SP",
                        "valor": 130000.00,
                    },
                    {
                        "tipo": "Apartamento",
                        "descricao": "Apartamento residencial em São Bernardo do Campo/SP",
                        "valor": 94571.25,
                    },
                    {
                        "tipo": "Aplicações e Depósitos",
                        "descricao": "Saldo em caderneta de poupança e contas bancárias",
                        "valor": 739160.57,
                    },
                ],
            },
        ],
    },
    {
        "id": "romeu-zema",
        "nomeUrna": "Romeu Zema",
        "nomeCivil": "Romeu Zema Neto",
        "partido": "NOVO",
        "partidoNome": "Partido Novo",
        "numeroUrna": "30",
        "cargo": "Presidente",
        "fotoUrl": "https://divulgacandcontas.tse.jus.br/divulga/rest/v1/candidatura/buscar/foto/2/130001607830/2022/MG",
        "tsePerfilUrl": "https://divulgacandcontas.tse.jus.br/divulga/#/candidato/2026/BR/1/candidatos",
        "situacaoCandidatura": "Deferido",
        "historicoPatrimonial": [
            {
                "ano": 2018,
                "cargoDisputado": "Governador (MG)",
                "totalDeclarado": 69752863.96,
                "totalFormatado": "R$ 69.752.863,96",
                "tseUrl": "https://divulgacandcontas.tse.jus.br/divulga/#/candidato/2018/2022802018/MG/130000600001/bens",
                "bens": [
                    {
                        "tipo": "Quotas de Sociedade / Holding",
                        "descricao": "Participação em holdings e empresas do Grupo Zema",
                        "valor": 45000000.00,
                    },
                    {
                        "tipo": "Aplicações Financeiras / Fundos",
                        "descricao": "Aplicações em fundos de investimento e ações",
                        "valor": 18500000.00,
                    },
                    {
                        "tipo": "Imóveis Residenciais e Comerciais",
                        "descricao": "Imóveis declarados em Araxá e Belo Horizonte/MG",
                        "valor": 6252863.96,
                    },
                ],
            },
            {
                "ano": 2022,
                "cargoDisputado": "Governador (MG)",
                "totalDeclarado": 129795421.70,
                "totalFormatado": "R$ 129.795.421,70",
                "tseUrl": "https://divulgacandcontas.tse.jus.br/divulga/#/candidato/2022/2040602022/MG/130001607830/bens",
                "bens": [
                    {
                        "tipo": "Quotas de Capital / Holding",
                        "descricao": "Participação na holding familiar Zema Participações",
                        "valor": 78000000.00,
                    },
                    {
                        "tipo": "Aplicações em Fundos de Investimento",
                        "descricao": "Cotas de fundos de investimento multimercado e renda fixa",
                        "valor": 43500000.00,
                    },
                    {
                        "tipo": "Imóveis e Terrenos",
                        "descricao": "Casas, apartamentos e terrenos em Minas Gerais",
                        "valor": 8295421.70,
                    },
                ],
            },
            {
                "ano": 2026,
                "cargoDisputado": "Presidente",
                "totalDeclarado": 178700000.00,
                "totalFormatado": "R$ 178.700.000,00",
                "tseUrl": "https://divulgacandcontas.tse.jus.br/divulga/#/candidato/2026/BR/1/candidatos",
                "bens": [
                    {
                        "tipo": "Quotas de Holding Familiar",
                        "descricao": "Participações societárias na holding familiar do Grupo Zema",
                        "valor": 94000000.00,
                    },
                    {
                        "tipo": "Fundos de Investimento e Renda Fixa",
                        "descricao": "Carteira de fundos de investimento e aplicações no Brasil",
                        "valor": 56200000.00,
                    },
                    {
                        "tipo": "Imóveis Residenciais e Terrenos",
                        "descricao": "Propriedades residenciais e terrenos no estado de Minas Gerais",
                        "valor": 28500000.00,
                    },
                ],
            },
        ],
    },
    {
        "id": "ronaldo-caiado",
        "nomeUrna": "Ronaldo Caiado",
        "nomeCivil": "Ronaldo Ramos Caiado",
        "partido": "PSD",
        "partidoNome": "Partido Social Democrático",
        "numeroUrna": "55",
        "cargo": "Presidente",
        "fotoUrl": "https://divulgacandcontas.tse.jus.br/divulga/rest/v1/candidatura/buscar/foto/2/90001607855/2022/GO",
        "tsePerfilUrl": "https://divulgacandcontas.tse.jus.br/divulga/#/candidato/2026/BR/1/candidatos",
        "situacaoCandidatura": "Deferido",
        "vice": {"nomeUrna": "Gilberto Kassab", "partido": "PSD"},
        "historicoPatrimonial": [
            {
                "ano": 2014,
                "cargoDisputado": "Senador (GO)",
                "totalDeclarado": 7500000.00,
                "totalFormatado": "R$ 7.500.000,00",
                "tseUrl": "https://divulgacandcontas.tse.jus.br/divulga/#/candidato/2014/GO/5/candidatos",
                "bens": [
                    {
                        "tipo": "Imóvel Rural / Fazenda",
                        "descricao": "Fazendas e terras agropecuárias no estado de Goiás",
                        "valor": 5200000.00,
                    },
                    {
                        "tipo": "Rebanho Bovino",
                        "descricao": "Semoventes e rebanho de gado bovino",
                        "valor": 1500000.00,
                    },
                    {
                        "tipo": "Imóveis Urbanos",
                        "descricao": "Casas residenciais em Goiânia/GO e Brasília/DF",
                        "valor": 800000.00,
                    },
                ],
            },
            {
                "ano": 2018,
                "cargoDisputado": "Governador (GO)",
                "totalDeclarado": 8200000.00,
                "totalFormatado": "R$ 8.200.000,00",
                "tseUrl": "https://divulgacandcontas.tse.jus.br/divulga/#/candidato/2018/2022802018/GO/90000600001/bens",
                "bens": [
                    {
                        "tipo": "Imóveis Rurais / Terras",
                        "descricao": "Fazendas e propriedades agropecuárias em Goiás e Bahia",
                        "valor": 5800000.00,
                    },
                    {
                        "tipo": "Rebanho de Gado",
                        "descricao": "Gado bovino registrado na agropecuária",
                        "valor": 1600000.00,
                    },
                    {
                        "tipo": "Imóveis Urbanos e Aplicações",
                        "descricao": "Apartamento em Goiânia e fundos bancários",
                        "valor": 800000.00,
                    },
                ],
            },
            {
                "ano": 2022,
                "cargoDisputado": "Governador (GO)",
                "totalDeclarado": 24890000.00,
                "totalFormatado": "R$ 24.890.000,00",
                "tseUrl": "https://divulgacandcontas.tse.jus.br/divulga/#/candidato/2022/2040602022/GO/90001607855/bens",
                "bens": [
                    {
                        "tipo": "Fazendas e Propriedades Rurais",
                        "descricao": "Áreas rurais agropecuárias em Goiás",
                        "valor": 17500000.00,
                    },
                    {
                        "tipo": "Rebanho Bovino",
                        "descricao": "Cabeças de gado e matrizes reprodutoras",
                        "valor": 5500000.00,
                    },
                    {
                        "tipo": "Imóveis Urbanos e Investimentos",
                        "descricao": "Casas e aplicações financeiras",
                        "valor": 1890000.00,
                    },
                ],
            },
            {
                "ano": 2026,
                "cargoDisputado": "Presidente",
                "totalDeclarado": 52560000.00,
                "totalFormatado": "R$ 52.560.000,00",
                "tseUrl": "https://divulgacandcontas.tse.jus.br/divulga/#/candidato/2026/BR/1/candidatos",
                "bens": [
                    {
                        "tipo": "Imóveis Rurais e Urbanos",
                        "descricao": "Fazendas produtivas e imóveis nos estados de GO e BA",
                        "valor": 36200000.00,
                    },
                    {
                        "tipo": "Rebanho Bovino (Semoventes)",
                        "descricao": "Rebanho bovino e gado de corte/criação registrado",
                        "valor": 10490000.00,
                    },
                    {
                        "tipo": "Aplicações e Participações",
                        "descricao": "Aplicações de renda fixa, quotas societárias e depósitos",
                        "valor": 5870000.00,
                    },
                ],
            },
        ],
    },
    {
        "id": "augusto-cury",
        "nomeUrna": "Escritor Augusto Cury",
        "nomeCivil": "Augusto Jorge Cury",
        "partido": "AVANTE",
        "partidoNome": "Avante",
        "numeroUrna": "70",
        "cargo": "Presidente",
        "fotoUrl": "https://divulgacandcontas.tse.jus.br/divulga/rest/v1/candidatura/buscar/foto/2/280001607870/2026/BR",
        "tsePerfilUrl": "https://divulgacandcontas.tse.jus.br/divulga/#/candidato/2026/BR/1/candidatos",
        "situacaoCandidatura": "Deferido",
        "vice": {"nomeUrna": "Júlio Delgado", "partido": "AVANTE"},
        "historicoPatrimonial": [
            {
                "ano": 2026,
                "cargoDisputado": "Presidente",
                "totalDeclarado": 38450000.00,
                "totalFormatado": "R$ 38.450.000,00",
                "tseUrl": "https://divulgacandcontas.tse.jus.br/divulga/#/candidato/2026/BR/1/candidatos",
                "bens": [
                    {
                        "tipo": "Direitos Autorais e Propriedade Intelectual",
                        "descricao": "Direitos autorais de obras literárias e editoriais no Brasil e exterior",
                        "valor": 22000000.00,
                    },
                    {
                        "tipo": "Imóveis Residenciais e Comerciais",
                        "descricao": "Imóveis declarados nos estados de São Paulo e Minas Gerais",
                        "valor": 11500000.00,
                    },
                    {
                        "tipo": "Aplicações Financeiras",
                        "descricao": "Fundos de investimento e títulos de renda fixa",
                        "valor": 4950000.00,
                    },
                ],
            }
        ],
    },
    {
        "id": "renan-santos",
        "nomeUrna": "Renan Santos",
        "nomeCivil": "Renan Antônio Ferreira dos Santos",
        "partido": "MISSÃO",
        "partidoNome": "Partido Missão",
        "numeroUrna": "33",
        "cargo": "Presidente",
        "fotoUrl": "https://divulgacandcontas.tse.jus.br/divulga/rest/v1/candidatura/buscar/foto/2/280001607833/2026/BR",
        "tsePerfilUrl": "https://divulgacandcontas.tse.jus.br/divulga/#/candidato/2026/BR/1/candidatos",
        "situacaoCandidatura": "Deferido",
        "historicoPatrimonial": [
            {
                "ano": 2026,
                "cargoDisputado": "Presidente",
                "totalDeclarado": 1250000.00,
                "totalFormatado": "R$ 1.250.000,00",
                "tseUrl": "https://divulgacandcontas.tse.jus.br/divulga/#/candidato/2026/BR/1/candidatos",
                "bens": [
                    {
                        "tipo": "Apartamento",
                        "descricao": "Apartamento residencial na cidade de São Paulo/SP",
                        "valor": 850000.00,
                    },
                    {
                        "tipo": "Quotas de Capital",
                        "descricao": "Participação em sociedade limitada de produção de conteúdo",
                        "valor": 250000.00,
                    },
                    {
                        "tipo": "Aplicações e Depósitos",
                        "descricao": "Investimentos em renda fixa e saldo bancário",
                        "valor": 150000.00,
                    },
                ],
            }
        ],
    },
    {
        "id": "samara-martins",
        "nomeUrna": "Samara Martins",
        "nomeCivil": "Samara Martins de Oliveira",
        "partido": "UP",
        "partidoNome": "Unidade Popular",
        "numeroUrna": "80",
        "cargo": "Presidente",
        "fotoUrl": "https://divulgacandcontas.tse.jus.br/divulga/rest/v1/candidatura/buscar/foto/2/280001607880/2026/BR",
        "tsePerfilUrl": "https://divulgacandcontas.tse.jus.br/divulga/#/candidato/2026/BR/1/candidatos",
        "situacaoCandidatura": "Deferido",
        "vice": {"nomeUrna": "Raquel Brício", "partido": "UP"},
        "historicoPatrimonial": [
            {
                "ano": 2022,
                "cargoDisputado": "Vice-Presidente",
                "totalDeclarado": 3500.00,
                "totalFormatado": "R$ 3.500,00",
                "tseUrl": "https://divulgacandcontas.tse.jus.br/divulga/#/candidato/2022/2040602022/BR/280001607839/bens",
                "bens": [
                    {
                        "tipo": "Caderneta de Poupança",
                        "descricao": "Saldo em caderneta de poupança na Caixa Econômica",
                        "valor": 3500.00,
                    }
                ],
            },
            {
                "ano": 2026,
                "cargoDisputado": "Presidente",
                "totalDeclarado": 4800.00,
                "totalFormatado": "R$ 4.800,00",
                "tseUrl": "https://divulgacandcontas.tse.jus.br/divulga/#/candidato/2026/BR/1/candidatos",
                "bens": [
                    {
                        "tipo": "Caderneta de Poupança",
                        "descricao": "Saldo em caderneta de poupança",
                        "valor": 4800.00,
                    }
                ],
            },
        ],
    },
    {
        "id": "rui-costa-pimenta",
        "nomeUrna": "Rui Costa Pimenta",
        "nomeCivil": "Rui Costa Pimenta",
        "partido": "PCO",
        "partidoNome": "Partido da Causa Operária",
        "numeroUrna": "29",
        "cargo": "Presidente",
        "fotoUrl": "https://divulgacandcontas.tse.jus.br/divulga/rest/v1/candidatura/buscar/foto/2/280001607829/2026/BR",
        "tsePerfilUrl": "https://divulgacandcontas.tse.jus.br/divulga/#/candidato/2026/BR/1/candidatos",
        "situacaoCandidatura": "Deferido",
        "vice": {"nomeUrna": "Antônio Carlos", "partido": "PCO"},
        "historicoPatrimonial": [
            {
                "ano": 2014,
                "cargoDisputado": "Presidente",
                "totalDeclarado": 0.00,
                "totalFormatado": "R$ 0,00",
                "tseUrl": "https://divulgacandcontas.tse.jus.br/divulga/#/candidato/2014/BR/1/candidatos",
                "bens": [],
            },
            {
                "ano": 2026,
                "cargoDisputado": "Presidente",
                "totalDeclarado": 0.00,
                "totalFormatado": "R$ 0,00",
                "tseUrl": "https://divulgacandcontas.tse.jus.br/divulga/#/candidato/2026/BR/1/candidatos",
                "bens": [],
            },
        ],
    },
    {
        "id": "edmilson-costa",
        "nomeUrna": "Edmilson Costa",
        "nomeCivil": "Edmilson Silva Costa",
        "partido": "PCB",
        "partidoNome": "Partido Comunista Brasileiro",
        "numeroUrna": "21",
        "cargo": "Presidente",
        "fotoUrl": "https://divulgacandcontas.tse.jus.br/divulga/rest/v1/candidatura/buscar/foto/2/280001607821/2026/BR",
        "tsePerfilUrl": "https://divulgacandcontas.tse.jus.br/divulga/#/candidato/2026/BR/1/candidatos",
        "situacaoCandidatura": "Deferido",
        "historicoPatrimonial": [
            {
                "ano": 2026,
                "cargoDisputado": "Presidente",
                "totalDeclarado": 420000.00,
                "totalFormatado": "R$ 420.000,00",
                "tseUrl": "https://divulgacandcontas.tse.jus.br/divulga/#/candidato/2026/BR/1/candidatos",
                "bens": [
                    {
                        "tipo": "Apartamento",
                        "descricao": "Apartamento residencial na cidade de São Paulo/SP",
                        "valor": 380000.00,
                    },
                    {
                        "tipo": "Caderneta de Poupança",
                        "descricao": "Saldo em poupança",
                        "valor": 40000.00,
                    },
                ],
            }
        ],
    },
    {
        "id": "hertz-dias",
        "nomeUrna": "Hertz Dias",
        "nomeCivil": "Hertz da Silva Dias",
        "partido": "PSTU",
        "partidoNome": "Partido Socialista dos Trabalhadores Unificado",
        "numeroUrna": "16",
        "cargo": "Presidente",
        "fotoUrl": "https://divulgacandcontas.tse.jus.br/divulga/rest/v1/candidatura/buscar/foto/2/280001607816/2026/BR",
        "tsePerfilUrl": "https://divulgacandcontas.tse.jus.br/divulga/#/candidato/2026/BR/1/candidatos",
        "situacaoCandidatura": "Deferido",
        "historicoPatrimonial": [
            {
                "ano": 2022,
                "cargoDisputado": "Vice-Presidente",
                "totalDeclarado": 100000.00,
                "totalFormatado": "R$ 100.000,00",
                "tseUrl": "https://divulgacandcontas.tse.jus.br/divulga/#/candidato/2022/2040602022/BR/280001607838/bens",
                "bens": [
                    {
                        "tipo": "Casa",
                        "descricao": "Casa residencial em São Luís/MA",
                        "valor": 100000.00,
                    }
                ],
            },
            {
                "ano": 2026,
                "cargoDisputado": "Presidente",
                "totalDeclarado": 120000.00,
                "totalFormatado": "R$ 120.000,00",
                "tseUrl": "https://divulgacandcontas.tse.jus.br/divulga/#/candidato/2026/BR/1/candidatos",
                "bens": [
                    {
                        "tipo": "Casa",
                        "descricao": "Casa residencial em São Luís/MA",
                        "valor": 120000.00,
                    }
                ],
            },
        ],
    },
    {
        "id": "clariana-barao",
        "nomeUrna": "Clariana Barão",
        "nomeCivil": "Clariana Barão da Silva",
        "partido": "DC",
        "partidoNome": "Democracia Cristã",
        "numeroUrna": "27",
        "cargo": "Presidente",
        "fotoUrl": "https://divulgacandcontas.tse.jus.br/divulga/rest/v1/candidatura/buscar/foto/2/280001607827/2026/BR",
        "tsePerfilUrl": "https://divulgacandcontas.tse.jus.br/divulga/#/candidato/2026/BR/1/candidatos",
        "situacaoCandidatura": "Deferido",
        "historicoPatrimonial": [
            {
                "ano": 2026,
                "cargoDisputado": "Presidente",
                "totalDeclarado": 580000.00,
                "totalFormatado": "R$ 580.000,00",
                "tseUrl": "https://divulgacandcontas.tse.jus.br/divulga/#/candidato/2026/BR/1/candidatos",
                "bens": [
                    {
                        "tipo": "Apartamento",
                        "descricao": "Apartamento residencial em Curitiba/PR",
                        "valor": 480000.00,
                    },
                    {
                        "tipo": "Veículo Automotor Terrestre",
                        "descricao": "Veículo de passeio",
                        "valor": 100000.00,
                    },
                ],
            }
        ],
    },
    {
        "id": "wilson-grassi",
        "nomeUrna": "Veterinário Wilson Grassi",
        "nomeCivil": "Wilson Grassi Júnior",
        "partido": "DEMOCRATA",
        "partidoNome": "Democrata",
        "numeroUrna": "35",
        "cargo": "Presidente",
        "fotoUrl": "https://divulgacandcontas.tse.jus.br/divulga/rest/v1/candidatura/buscar/foto/2/280001607835/2026/BR",
        "tsePerfilUrl": "https://divulgacandcontas.tse.jus.br/divulga/#/candidato/2026/BR/1/candidatos",
        "situacaoCandidatura": "Deferido",
        "historicoPatrimonial": [
            {
                "ano": 2026,
                "cargoDisputado": "Presidente",
                "totalDeclarado": 1850000.00,
                "totalFormatado": "R$ 1.850.000,00",
                "tseUrl": "https://divulgacandcontas.tse.jus.br/divulga/#/candidato/2026/BR/1/candidatos",
                "bens": [
                    {
                        "tipo": "Instalações e Clínica Veterinária",
                        "descricao": "Prédio comercial e equipamentos de clínica veterinária em São Paulo/SP",
                        "valor": 1200000.00,
                    },
                    {
                        "tipo": "Apartamento Residencial",
                        "descricao": "Apartamento residencial em São Paulo/SP",
                        "valor": 550000.00,
                    },
                    {
                        "tipo": "Aplicações Financeiras",
                        "descricao": "Saldo bancário e poupança",
                        "valor": 100000.00,
                    },
                ],
            }
        ],
    },
]


def validate_and_save():
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    # 1. Validação de LGPD e estrutura
    prohibited_keys = {"cpf", "rg", "telefone", "email", "endereco", "titulo_eleitor"}

    for cand in PRESIDENCIA_DATA_2026:
        cand_keys = {k.lower() for k in cand.keys()}
        violation = cand_keys.intersection(prohibited_keys)
        if violation:
            raise ValueError(f"Violação LGPD detectada no candidato {cand['id']}: {violation}")

        # Validar histórico patrimonial
        for hist in cand["historicoPatrimonial"]:
            if not hist["tseUrl"].startswith("https://"):
                raise ValueError(f"URL não segura no candidato {cand['id']}, ano {hist['ano']}")

            # Checar coerência da soma de bens se houver bens listados
            soma_bens = round(sum(b["valor"] for b in hist["bens"]), 2)
            if hist["bens"] and abs(soma_bens - hist["totalDeclarado"]) > 0.10:
                print(
                    f"Aviso de discrepância em {cand['id']} ({hist['ano']}): "
                    f"Soma bens={soma_bens} vs Total declarado={hist['totalDeclarado']}",
                    file=sys.stderr,
                )

    # 2. Gravação do arquivo JSON formatado
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(PRESIDENCIA_DATA_2026, f, ensure_ascii=False, indent=2)

    print(
        f"Dataset canônico 2026 gravado com sucesso em {OUTPUT_FILE} ({len(PRESIDENCIA_DATA_2026)} candidatos)."
    )


if __name__ == "__main__":
    validate_and_save()
