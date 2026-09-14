"""
Ingestão de votações nominais oficiais do Senado Federal correspondentes aos temas do catálogo.
Fonte: API de Dados Abertos do Senado Federal (https://legis.senado.leg.br/dadosabertos/)
Endpoint: GET /materia/votacoes/{codigoMateria}

Conformidade e Regras:
  - LGPD (AD-009): NÃO inclui CPF, email institucional/pessoal ou telefone.
  - Verificabilidade (AD-006): Links diretos para sessões plenárias e matérias no portal oficial em HTTPS.
  - Formato Canônico: dados/senado/votacoes/{tema_id}.json
"""

import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT))

from scripts.core.http_client import fetch_json  # noqa: E402

SENADO_VOTACOES_MAP = [
    {
        "tema_id": "2196833-326",
        "codigo_materia": 158930,
        "votacao_id": 6773,
        "sessao_id": 368878,
        "proposicao": "PEC 45/2019",
        "data": "2023-11-08",
        "resultado_oficial": "Aprovado em 1º turno (Sim: 53, Não: 24)",
        "url_votacao": "https://www25.senado.leg.br/web/atividade/sessao-plenaria/-/p/sessao/368878",
        "url_proposicao": "https://www25.senado.leg.br/web/atividade/materias/-/materia/158930",
    },
    {
        "tema_id": "2196833-373",
        "codigo_materia": 158930,
        "votacao_id": 6777,
        "sessao_id": 368878,
        "proposicao": "PEC 45/2019",
        "data": "2023-11-08",
        "resultado_oficial": "Aprovado em 2º turno (Sim: 53, Não: 24)",
        "url_votacao": "https://www25.senado.leg.br/web/atividade/sessao-plenaria/-/p/sessao/368878",
        "url_proposicao": "https://www25.senado.leg.br/web/atividade/materias/-/materia/158930",
    },
    {
        "tema_id": "345311-270",
        "codigo_materia": 157888,
        "votacao_id": 6756,
        "sessao_id": 359754,
        "proposicao": "PL 2903/2023",
        "data": "2023-09-27",
        "resultado_oficial": "Aprovado (Sim: 43, Não: 21)",
        "url_votacao": "https://www25.senado.leg.br/web/atividade/sessao-plenaria/-/p/sessao/359754",
        "url_proposicao": "https://www25.senado.leg.br/web/atividade/materias/-/materia/157888",
    },
    {
        "tema_id": "2352476-168",
        "codigo_materia": 164727,
        "votacao_id": 6874,
        "sessao_id": 422342,
        "proposicao": "PEC 9/2023",
        "data": "2024-08-14",
        "resultado_oficial": "Aprovado em 2º turno (Sim: 54, Não: 16)",
        "url_votacao": "https://www25.senado.leg.br/web/atividade/sessao-plenaria/-/p/sessao/422342",
        "url_proposicao": "https://www25.senado.leg.br/web/atividade/materias/-/materia/164727",
    },
    {
        "tema_id": "2422697-75",
        "codigo_materia": 163889,
        "votacao_id": 6836,
        "sessao_id": 408825,
        "proposicao": "PL 914/2024",
        "data": "2024-06-05",
        "resultado_oficial": "Aprovado (Sim: 67, Não: 0)",
        "url_votacao": "https://www25.senado.leg.br/web/atividade/sessao-plenaria/-/p/sessao/408825",
        "url_proposicao": "https://www25.senado.leg.br/web/atividade/materias/-/materia/163889",
    },
]

OUTPUT_DIR = ROOT / "dados" / "senado" / "votacoes"


def normalize_voto_senado(sigla_voto: str) -> str:
    sigla = (sigla_voto or "").strip()
    if sigla == "Sim":
        return "Sim"
    if sigla in ("Não", "Nao"):
        return "Não"
    if sigla in ("Abstenção", "Abstencao"):
        return "Abstenção"
    if "art. 51" in sigla.lower() or "presidente" in sigla.lower():
        return "Presidente (Art. 51)"
    # P-NRV (Presente - Não registrou voto), AP (Atividade parlamentar),
    # LS (Licença saúde), MIS (Missão), etc.
    return "Não votou / Ausente"


def fetch_and_save_senado_votacoes():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Iniciando ingestão de {len(SENADO_VOTACOES_MAP)} votações nominais do Senado...")

    # Cache de matérias consultadas para não repetir requisições HTTP para a mesma matéria
    materia_cache = {}

    for config in SENADO_VOTACOES_MAP:
        tema_id = config["tema_id"]
        cod_mat = config["codigo_materia"]
        vot_id = config["votacao_id"]

        print(f"\nProcessando tema {tema_id} (Matéria {cod_mat}, Votação {vot_id})...")

        if cod_mat not in materia_cache:
            url = f"https://legis.senado.leg.br/dadosabertos/materia/votacoes/{cod_mat}"
            print(f"Requisitando dados em {url}...")
            payload = fetch_json(url)
            materia_cache[cod_mat] = payload
        else:
            payload = materia_cache[cod_mat]

        try:
            materia_node = payload.get("VotacaoMateria", {}).get("Materia", {})
            votacoes_node = materia_node.get("Votacoes", {}).get("Votacao", [])
            if not isinstance(votacoes_node, list):
                votacoes_node = [votacoes_node]
        except Exception as e:
            print(
                f"ERRO: Estrutura inválida na resposta da matéria {cod_mat}: {e}", file=sys.stderr
            )
            sys.exit(1)

        votacao_alvo = None
        for v in votacoes_node:
            if str(v.get("CodigoSessaoVotacao")) == str(vot_id):
                votacao_alvo = v
                break

        if not votacao_alvo:
            print(
                f"ERRO: Votação {vot_id} não encontrada para a matéria {cod_mat}", file=sys.stderr
            )
            sys.exit(1)

        descricao = votacao_alvo.get("DescricaoVotacao", "")
        votos_parl = votacao_alvo.get("Votos", {}).get("VotoParlamentar", [])
        if not isinstance(votos_parl, list):
            votos_parl = [votos_parl]

        votos_map = {}
        for vp in votos_parl:
            ident = vp.get("IdentificacaoParlamentar", {})
            cod_parl = ident.get("CodigoParlamentar") or vp.get("CodigoParlamentar")
            if not cod_parl:
                continue

            nome = ident.get("NomeParlamentar", "").strip()
            partido = ident.get("SiglaPartidoParlamentar", "").strip()
            uf = ident.get("UfParlamentar", "").strip()
            sigla_voto = vp.get("SiglaVoto", "")

            votos_map[str(cod_parl)] = {
                "nome": nome,
                "partido": partido,
                "uf": uf,
                "tipoVoto": normalize_voto_senado(sigla_voto),
            }

        metadados = {
            "tema_id": tema_id,
            "senado_votacao_id": vot_id,
            "senado_sessao_id": config["sessao_id"],
            "codigo_materia": cod_mat,
            "proposicao": config["proposicao"],
            "data": config["data"],
            "descricao": descricao,
            "resultado_oficial": config["resultado_oficial"],
            "url_votacao": config["url_votacao"],
            "url_proposicao": config["url_proposicao"],
        }

        output_file = OUTPUT_DIR / f"{tema_id}.json"
        data_to_save = {
            "metadados": metadados,
            "votos": votos_map,
        }

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(data_to_save, f, indent=2, ensure_ascii=False)
            f.write("\n")

        print(f"Sucesso: {len(votos_map)} votos salvos em {output_file.relative_to(ROOT)}")

    print("\nIngestão de votações do Senado concluída com sucesso!")


if __name__ == "__main__":
    fetch_and_save_senado_votacoes()
