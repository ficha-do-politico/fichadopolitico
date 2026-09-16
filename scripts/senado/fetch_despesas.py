"""
Ingestão e agregação oficial das despesas da Cota para Exercício da Atividade Parlamentar dos Senadores (CEAPS)
do Senado Federal para o exercício de 2026.

Fonte Oficial:
  - API de Dados Abertos Administrativos do Senado: https://adm.senado.leg.br/adm-dadosabertos/api/v1/senadores/despesas_ceaps/{ano}
  - Portal de Transparência do Senado: https://www6g.senado.leg.br/transparencia/sen/{codSenador}/?ano={ano}

Conformidade e Regras:
  - LGPD (AD-009): Descarte de CPFs pessoais e mascaramento de CPFs de prestadores.
  - Verificabilidade (AD-006): Link direto oficial para a página de transparência de cada senador.
  - Performance & SSG: Dados sumarizados por categoria e top despesas, gerando JSON leve (~60 KB).
"""

import argparse
import http.client
import json
import pathlib
import re
import sys
import urllib.request
from collections import defaultdict

ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT))

SENADO_DIR = ROOT / "dados" / "senado"
SENADORES_FILE = SENADO_DIR / "senadores.json"
OUTPUT_FILE = SENADO_DIR / "despesas_2026.json"

API_CEAPS_TEMPLATE = (
    "https://adm.senado.leg.br/adm-dadosabertos/api/v1/senadores/despesas_ceaps/{ano}"
)
PORTAL_TRANSPARENCIA_TEMPLATE = (
    "https://www6g.senado.leg.br/transparencia/sen/{codSenador}/?ano={ano}"
)


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


def formatar_data(data_str: str) -> str:
    """Converte '2026-01-21' para '21/01/2026'."""
    if not data_str:
        return ""
    partes = data_str.strip().split("-")
    if len(partes) == 3:
        ano, mes, dia = partes
        return f"{dia}/{mes}/{ano}"
    return data_str


def mascarar_cnpj_cpf(identificador: str) -> str:
    """
    Sanitiza e mascara CPF de pessoa física para conformidade com LGPD (AD-009).
    Mantém CNPJs comerciais com pontuação legível.
    """
    if not identificador:
        return ""
    apenas_numeros = re.sub(r"\D", "", identificador)
    if len(apenas_numeros) == 11:
        return f"***.{apenas_numeros[3:6]}.{apenas_numeros[6:9]}-**"
    if len(apenas_numeros) == 14:
        return (
            f"{apenas_numeros[:2]}.{apenas_numeros[2:5]}.{apenas_numeros[5:8]}/"
            f"{apenas_numeros[8:12]}-{apenas_numeros[12:]}"
        )
    return identificador.strip()


def normalizar_categoria(descricao: str) -> str:
    """Normaliza descrições longas de despesas do Senado para títulos concisos."""
    if not descricao:
        return "Outros"
    limpa = descricao.strip().rstrip(".")
    mapa = {
        "ALUGUEL DE IMÓVEIS PARA ESCRITÓRIO POLÍTICO, COMPREENDENDO DESPESAS CONCERNENTES A ELES": "Aluguel de Escritório Político",
        "ALUGUEL DE IMOVEIS PARA ESCRITORIO POLITICO, COMPREENDENDO DESPESAS CONCERNENTES A ELES": "Aluguel de Escritório Político",
        "AQUISIÇÃO DE MATERIAL DE CONSUMO PARA USO NO ESCRITÓRIO POLÍTICO, INCLUSIVE AQUISIÇÃO OU LOCAÇÃO DE SOFTWARE, DESPESAS POSTAIS, AQUISIÇÃO DE PUBLICAÇÕES, LOCAÇÃO DE MÓVEIS E DE EQUIPAMENTOS": "Material de Consumo e Equipamentos",
        "AQUISICAO DE MATERIAL DE CONSUMO PARA USO NO ESCRITORIO POLITICO, INCLUSIVE AQUISICAO OU LOCACAO DE SOFTWARE, DESPESAS POSTAIS, AQUISICAO DE PUBLICACOES, LOCACAO DE MOVEIS E DE EQUIPAMENTOS": "Material de Consumo e Equipamentos",
        "CONTRATAÇÃO DE CONSULTORIAS, ASSESSORIAS, PESQUISAS, TRABALHOS TÉCNICOS E OUTROS SERVIÇOS DE APOIO AO EXERCÍCIO DO MANDATO PARLAMENTAR": "Consultorias e Assessorias Técnicas",
        "CONTRATACAO DE CONSULTORIAS, ASSESSORIAS, PESQUISAS, TRABALHOS TECNICOS E OUTROS SERVICOS DE APOIO AO EXERCICIO DO MANDATO PARLAMENTAR": "Consultorias e Assessorias Técnicas",
        "DIVULGAÇÃO DA ATIVIDADE PARLAMENTAR": "Divulgação da Atividade Parlamentar",
        "DIVULGACAO DA ATIVIDADE PARLAMENTAR": "Divulgação da Atividade Parlamentar",
        "LOCOMOÇÃO, HOSPEDAGEM, ALIMENTAÇÃO, COMBUSTÍVEIS E LUBRIFICANTES": "Locomoção, Hospedagem e Combustíveis",
        "LOCOMOCAO, HOSPEDAGEM, ALIMENTACAO, COMBUSTIVEIS E LUBRIFICANTES": "Locomoção, Hospedagem e Combustíveis",
        "PASSAGENS AÉREAS, AQUÁTICAS E TERRESTRES NACIONAIS": "Passagens Aéreas e Terrestres",
        "PASSAGENS AEREAS, AQUATICAS E TERRESTRES NACIONAIS": "Passagens Aéreas e Terrestres",
        "SERVIÇOS DE SEGURANÇA PRIVADA": "Serviços de Segurança Privada",
        "SERVICOS DE SEGURANCA PRIVADA": "Serviços de Segurança Privada",
    }
    return mapa.get(limpa.upper(), limpa.title())


def baixar_e_processar_ceaps_senado(ano: int = 2026) -> dict:
    url_api = API_CEAPS_TEMPLATE.format(ano=ano)
    print(f"Requisitando dados oficiais da CEAPS do Senado em {url_api}...")

    req = urllib.request.Request(
        url_api,
        headers={
            "User-Agent": "FichaDoPolitico/1.0 (+https://github.com/ficha-do-politico)",
            "Accept": "application/json",
        },
    )

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            try:
                raw_bytes = resp.read()
            except http.client.IncompleteRead as e:
                raw_bytes = e.partial
        payload = json.loads(raw_bytes.decode("utf-8"))
    except Exception as e:
        print(f"Erro ao baixar CEAPS do Senado: {e}", file=sys.stderr)
        raise

    print(f"Total de {len(payload)} lançamentos de CEAPS recebidos para o ano de {ano}.")

    # Carrega senadores válidos da base canônica
    senadores_validos = set()
    if SENADORES_FILE.exists():
        with open(SENADORES_FILE, encoding="utf-8") as f:
            for s in json.load(f):
                senadores_validos.add(int(s["id"]))

    despesas_por_senador = defaultdict(
        lambda: {"total": 0.0, "categorias": defaultdict(float), "despesas": []}
    )

    for item in payload:
        cod_senador = item.get("codSenador")
        if not cod_senador:
            continue

        sen_id = int(cod_senador)
        if senadores_validos and sen_id not in senadores_validos:
            continue

        valor_raw = item.get("valorReembolsado")
        if valor_raw is None:
            continue

        try:
            valor = float(valor_raw)
        except (ValueError, TypeError):
            continue

        if valor <= 0:
            continue

        cat_nome = normalizar_categoria(item.get("tipoDespesa", ""))
        data_fmt = formatar_data(item.get("data", ""))
        fornecedor = (item.get("fornecedor") or "").strip()
        cnpj_cpf = mascarar_cnpj_cpf(item.get("cpfCnpj") or "")

        sen_data = despesas_por_senador[sen_id]
        sen_data["total"] += valor
        sen_data["categorias"][cat_nome] += valor

        sen_data["despesas"].append(
            {
                "data": data_fmt,
                "fornecedor": fornecedor,
                "cnpj_cpf": cnpj_cpf,
                "categoria": cat_nome,
                "valor": round(valor, 2),
                "valor_formatado": formatar_moeda(valor),
                "url_documento": None,
            }
        )

    print(f"Despesas processadas para {len(despesas_por_senador)} senadores da República.")

    resultado_final = {}
    for sen_id, s_info in despesas_por_senador.items():
        total = round(s_info["total"], 2)

        categorias_lista = []
        for cat_nome, cat_val in sorted(
            s_info["categorias"].items(), key=lambda x: x[1], reverse=True
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

        s_info["despesas"].sort(key=lambda x: x["valor"], reverse=True)
        maiores_despesas = s_info["despesas"][:5]

        resultado_final[str(sen_id)] = {
            "ano": ano,
            "total_gasto": total,
            "total_formatado": formatar_moeda(total),
            "total_documentos": len(s_info["despesas"]),
            "categorias": categorias_lista,
            "maiores_despesas": maiores_despesas,
            "fonte_oficial": PORTAL_TRANSPARENCIA_TEMPLATE.format(codSenador=sen_id, ano=ano),
        }

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(resultado_final, f, ensure_ascii=False, indent=2)

    print(
        f"Sucesso: {len(resultado_final)} registros de CEAPS do Senado salvos em {OUTPUT_FILE} "
        f"({OUTPUT_FILE.stat().st_size / 1024:.1f} KB)"
    )
    return resultado_final


def main():
    parser = argparse.ArgumentParser(description="Ingestão das despesas da CEAPS do Senado Federal")
    parser.add_argument(
        "--ano", type=int, default=2026, help="Ano da cota parlamentar (padrão: 2026)"
    )
    args = parser.parse_args()
    baixar_e_processar_ceaps_senado(ano=args.ano)


if __name__ == "__main__":
    main()
