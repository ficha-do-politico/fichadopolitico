"""
Ingestão e agregação oficial das despesas da Cota para Exercício da Atividade Parlamentar (CEAP)
da Câmara dos Deputados para o exercício de 2026.

Fonte Oficial:
  - Portal de Dados Abertos da Câmara dos Deputados: https://www.camara.leg.br/cotas/Ano-2026.csv.zip

Conformidade e Regras:
  - LGPD (AD-009): O CPF de parlamentares é 100% descartado. CPFs de fornecedores pessoa física são mascarados.
  - Verificabilidade (AD-006): Cada despesa preserva a urlDocumento oficial original do comprovante fiscal na Câmara.
  - Performance & SSG: Compila dados sumarizados por categoria e maiores despesas, mantendo o JSON canônico leve (< 400 KB).
"""

import argparse
import csv
import io
import json
import pathlib
import re
import sys
import urllib.request
import zipfile
from collections import defaultdict

ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT))

CAMARA_DIR = ROOT / "dados" / "camara"
DEPUTADOS_FILE = CAMARA_DIR / "deputados.json"
OUTPUT_FILE = CAMARA_DIR / "despesas_2026.json"

URL_DUMP_TEMPLATE = "https://www.camara.leg.br/cotas/Ano-{ano}.csv.zip"


def formatar_moeda(valor: float) -> str:
    """Formata valor float para o padrão monetário brasileiro R$ 1.234,56."""
    inteiro, decimal = f"{valor:.2f}".split(".")
    partes = []
    for i, c in enumerate(reversed(inteiro)):
        if i > 0 and i % 3 == 0:
            partes.append(".")
        partes.append(c)
    inteiro_formatado = "".join(reversed(partes))
    return f"R$ {inteiro_formatado},{decimal}"


def formatar_data(data_iso: str) -> str:
    """Converte '2026-04-17T00:00:00' para '17/04/2026'."""
    if not data_iso:
        return ""
    data_limpa = data_iso.split("T")[0]
    partes = data_limpa.split("-")
    if len(partes) == 3:
        ano, mes, dia = partes
        return f"{dia}/{mes}/{ano}"
    return data_iso


def mascarar_cnpj_cpf(identificador: str) -> str:
    """
    Sanitiza e mascara CPF de pessoa física para conformidade com LGPD (AD-009).
    Mantém CNPJs comerciais com pontuação legível.
    """
    if not identificador:
        return ""
    apenas_numeros = re.sub(r"\D", "", identificador)
    # Se for CPF (11 dígitos), mascara para proteção de dados do cidadão prestador
    if len(apenas_numeros) == 11:
        return f"***.{apenas_numeros[3:6]}.{apenas_numeros[6:9]}-**"
    # Se for CNPJ (14 dígitos), formata como XX.XXX.XXX/XXXX-XX
    if len(apenas_numeros) == 14:
        return (
            f"{apenas_numeros[:2]}.{apenas_numeros[2:5]}.{apenas_numeros[5:8]}/"
            f"{apenas_numeros[8:12]}-{apenas_numeros[12:]}"
        )
    return identificador.strip()


def normalizar_categoria(descricao: str) -> str:
    """Normaliza nomes de categorias da cota para visualização legível e limpa."""
    if not descricao:
        return "Outros"
    limpa = descricao.strip().rstrip(".")
    mapa = {
        "MANUTENÇÃO DE ESCRITÓRIO DE APOIO À ATIVIDADE PARLAMENTAR": "Manutenção de Escritório",
        "MANUTENCAO DE ESCRITORIO DE APOIO A ATIVIDADE PARLAMENTAR": "Manutenção de Escritório",
        "LOCAÇÃO OU FRETAMENTO DE VEÍCULOS AUTOMOTORES": "Locação de Veículos",
        "LOCACAO OU FRETAMENTO DE VEICULOS AUTOMOTORES": "Locação de Veículos",
        "DIVULGAÇÃO DA ATIVIDADE PARLAMENTAR": "Divulgação da Atividade Parlamentar",
        "DIVULGACAO DA ATIVIDADE PARLAMENTAR": "Divulgação da Atividade Parlamentar",
        "PASSAGEM AÉREA - SIGEPA": "Passagens Aéreas",
        "PASSAGEM AEREA - SIGEPA": "Passagens Aéreas",
        "PASSAGENS AÉREAS": "Passagens Aéreas",
        "PASSAGENS AEREAS": "Passagens Aéreas",
        "PASSAGEM AÉREA - REEMBOLSO": "Passagens Aéreas (Reembolso)",
        "PASSAGEM AEREA - REEMBOLSO": "Passagens Aéreas (Reembolso)",
        "COMBUSTÍVEIS E LUBRIFICANTES": "Combustíveis e Lubrificantes",
        "COMBUSTIVEIS E LUBRIFICANTES": "Combustíveis e Lubrificantes",
        "CONSULTORIAS, PESQUISAS E TRABALHOS TÉCNICOS": "Consultorias e Pesquisas",
        "CONSULTORIAS, PESQUISAS E TRABALHOS TECNICOS": "Consultorias e Pesquisas",
        "SERVIÇO DE SEGURANÇA PRESTADO POR EMPRESA ESPECIALIZADA": "Serviços de Segurança",
        "SERVICO DE SEGURANCA PRESTADO POR EMPRESA ESPECIALIZADA": "Serviços de Segurança",
        "SERVIÇO DE TÁXI, PEDÁGIO E ESTACIONAMENTO": "Táxi, Pedágio e Estacionamento",
        "SERVICO DE TAXI, PEDAGIO E ESTACIONAMENTO": "Táxi, Pedágio e Estacionamento",
        "FORNECIMENTO DE ALIMENTAÇÃO DO PARLAMENTAR": "Alimentação do Parlamentar",
        "FORNECIMENTO DE ALIMENTACAO DO PARLAMENTAR": "Alimentação do Parlamentar",
        "HOSPEDAGEM ,EXCETO DO PARLAMENTAR NO DISTRITO FEDERAL": "Hospedagem (fora do DF)",
        "HOSPEDAGEM ,EXCETO DO PARLAMENTAR NO DISTRITO FEDERAL.": "Hospedagem (fora do DF)",
        "TELEFONIA": "Telefonia",
        "SERVIÇOS POSTAIS": "Serviços Postais",
        "SERVICOS POSTAIS": "Serviços Postais",
        "PARTICIPAÇÃO EM CURSO, PALESTRA OU EVENTO SIMILAR": "Cursos e Eventos",
        "PARTICIPACAO EM CURSO, PALESTRA OU EVENTO SIMILAR": "Cursos e Eventos",
    }
    return mapa.get(limpa.upper(), limpa.title())


def baixar_e_processar_despesas(ano: int = 2026) -> dict:
    url_dump = URL_DUMP_TEMPLATE.format(ano=ano)
    print(f"Baixando dump consolidado da CEAP da Câmara: {url_dump}...")

    req = urllib.request.Request(
        url_dump,
        headers={"User-Agent": "FichaDoPolitico/1.0 (+https://github.com/ficha-do-politico)"},
    )

    with urllib.request.urlopen(req, timeout=60) as resp:
        conteudo_zip = resp.read()

    print(f"Download concluído: {len(conteudo_zip) / (1024 * 1024):.2f} MB. Descompactando...")
    zf = zipfile.ZipFile(io.BytesIO(conteudo_zip))
    csv_nome = zf.namelist()[0]

    # Carrega os deputados cadastrados para saber quem processar
    deputados_validos = {}
    if DEPUTADOS_FILE.exists():
        with open(DEPUTADOS_FILE, encoding="utf-8") as f:
            for d in json.load(f):
                deputados_validos[int(d["id"])] = d["nome_eleitoral"]

    print(f"Agrupando despesas por parlamentar a partir de {csv_nome}...")

    despesas_por_deputado = defaultdict(
        lambda: {"total": 0.0, "categorias": defaultdict(float), "despesas": []}
    )

    with zf.open(csv_nome) as f:
        text_stream = io.TextIOWrapper(f, encoding="utf-8", errors="replace")
        reader = csv.DictReader(text_stream, delimiter=";")

        for linha in reader:
            ide_cadastro = linha.get("ideCadastro", "").strip()
            if not ide_cadastro or not ide_cadastro.isdigit():
                continue

            dep_id = int(ide_cadastro)
            # Filtra apenas deputados constantes da nossa base legislativa
            if deputados_validos and dep_id not in deputados_validos:
                continue

            try:
                vlr_liquido = float(linha.get("vlrLiquido", "0").replace(",", "."))
            except ValueError:
                continue

            # Desconsidera glosas/restituições nulas ou valores zerados
            if vlr_liquido <= 0:
                continue

            desc_categoria = normalizar_categoria(linha.get("txtDescricao", ""))
            url_doc = linha.get("urlDocumento", "").strip()
            if url_doc.startswith("http://"):
                url_doc = "https://" + url_doc[7:]

            dep_data = despesas_por_deputado[dep_id]
            dep_data["total"] += vlr_liquido
            dep_data["categorias"][desc_categoria] += vlr_liquido

            fornecedor = linha.get("txtFornecedor", "").strip()
            cnpj_cpf = mascarar_cnpj_cpf(linha.get("txtCNPJCPF", ""))
            data_emissao = formatar_data(linha.get("datEmissao", ""))

            dep_data["despesas"].append(
                {
                    "data": data_emissao,
                    "fornecedor": fornecedor,
                    "cnpj_cpf": cnpj_cpf,
                    "categoria": desc_categoria,
                    "valor": round(vlr_liquido, 2),
                    "valor_formatado": formatar_moeda(vlr_liquido),
                    "url_documento": url_doc if url_doc.startswith("https://") else None,
                }
            )

    print(f"Despesas processadas para {len(despesas_por_deputado)} deputados federais.")

    # Formata payload final sumarizado por parlamentar
    resultado_final = {}
    for dep_id, d_info in despesas_por_deputado.items():
        total = round(d_info["total"], 2)

        # Ordena categorias por valor gasto decrescente
        categorias_lista = []
        for cat_nome, cat_val in sorted(
            d_info["categorias"].items(), key=lambda x: x[1], reverse=True
        ):
            c_val = round(cat_val, 2)
            pct = round((c_val / total * 100) if total > 0 else 0.0, 1)
            categorias_lista.append(
                {
                    "categoria": cat_nome,
                    "valor": c_val,
                    "valor_formatado": formatar_moeda(c_val),
                    "percentual": pct,
                }
            )

        # Seleciona as 5 maiores despesas individuais
        d_info["despesas"].sort(key=lambda x: x["valor"], reverse=True)
        maiores_despesas = d_info["despesas"][:5]

        resultado_final[str(dep_id)] = {
            "ano": ano,
            "total_gasto": total,
            "total_formatado": formatar_moeda(total),
            "total_documentos": len(d_info["despesas"]),
            "categorias": categorias_lista,
            "maiores_despesas": maiores_despesas,
            "fonte_oficial": f"https://www.camara.leg.br/deputados/{dep_id}",
        }

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(resultado_final, f, ensure_ascii=False, indent=2)

    print(
        f"Sucesso: {len(resultado_final)} registros de despesas salvos em {OUTPUT_FILE} "
        f"({OUTPUT_FILE.stat().st_size / 1024:.1f} KB)"
    )
    return resultado_final


def main():
    parser = argparse.ArgumentParser(
        description="Ingestão das despesas da CEAP da Câmara dos Deputados"
    )
    parser.add_argument(
        "--ano", type=int, default=2026, help="Ano da cota parlamentar (padrão: 2026)"
    )
    args = parser.parse_args()
    baixar_e_processar_despesas(ano=args.ano)


if __name__ == "__main__":
    main()
