"""
Compila os dados de 513 deputados federais e as votações curadas para o frontend do MVP v0.

Entrada:
  - dados/deputados/*.md (513 parlamentares da 57ª legislatura)
  - dados/votacoes/*.json (votações nominais extraídas da API da Câmara)

Saída:
  - site/src/data/deputados.json (dataset compacto com identificação e mapa de votos)
  - site/src/data/temas.json (catálogo dos temas com metadados e links oficiais)

Regras de negócio:
  - LGPD / AD-009: NÃO inclui CPF, telefone pessoal ou email.
  - Verificabilidade / AGENTS.md §3.1: Cada voto e tema inclui links oficiais diretos.
  - Regra de Ausência: Se o parlamentar não registrou voto no painel eletrônico, é categorizado como 'Não votou / Ausente'.
"""

import glob
import json
import os
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
DEPUTADOS_DIR = ROOT / 'dados' / 'deputados'
VOTACOES_DIR = ROOT / 'dados' / 'votacoes'
SITE_DATA_DIR = ROOT / 'site' / 'src' / 'data'

TEMAS_CATALOGO = [
    {
        "id": "2196833-326",
        "ordem": 1,
        "titulo": "Reforma Tributária (1º Turno)",
        "subtitulo": "Aprovação do texto-base da Reforma Tributária sobre o consumo.",
        "proposicao": "PEC 45/2019",
        "proposicao_id": 2196833,
        "data": "2023-07-06",
        "resultado_oficial": "Aprovado em 1º turno (Sim: 382, Não: 118, Abst: 3)",
        "url_votacao": "https://dadosabertos.camara.leg.br/api/v2/votacoes/2196833-326",
        "url_proposicao": "https://www.camara.leg.br/propostas-legislativas/2196833",
        "criterio_resumo": "Reforma constitucional que reestrutura o sistema de tributação sobre o consumo no Brasil."
    },
    {
        "id": "2196833-373",
        "ordem": 2,
        "titulo": "Reforma Tributária (2º Turno)",
        "subtitulo": "Confirmação em 2º turno da Reforma Tributária sobre o consumo.",
        "proposicao": "PEC 45/2019",
        "proposicao_id": 2196833,
        "data": "2023-07-07",
        "resultado_oficial": "Aprovado em 2º turno (Sim: 375, Não: 113, Abst: 3)",
        "url_votacao": "https://dadosabertos.camara.leg.br/api/v2/votacoes/2196833-373",
        "url_proposicao": "https://www.camara.leg.br/propostas-legislativas/2196833",
        "criterio_resumo": "Votação definitiva do texto principal da PEC 45/2019 na Câmara antes do envio ao Senado."
    },
    {
        "id": "345311-270",
        "ordem": 3,
        "titulo": "Marco Temporal das Terras Indígenas",
        "subtitulo": "Restrição das demarcações às terras tradicionalmente ocupadas em 5 de outubro de 1988.",
        "proposicao": "PL 490/2007",
        "proposicao_id": 345311,
        "data": "2023-05-30",
        "resultado_oficial": "Aprovado Substitutivo (Sim: 283, Não: 155, Abst: 1)",
        "url_votacao": "https://dadosabertos.camara.leg.br/api/v2/votacoes/345311-270",
        "url_proposicao": "https://www.camara.leg.br/propostas-legislativas/345311",
        "criterio_resumo": "Projeto que estabelece a data da promulgação da Constituição de 1988 como marco para demarcação de terras indígenas."
    },
    {
        "id": "2352476-168",
        "ordem": 4,
        "titulo": "PEC da Anistia aos Partidos Políticos (2º Turno)",
        "subtitulo": "Anistia de multas eleitorais aplicadas a partidos por descumprimento de cotas de gênero e raça.",
        "proposicao": "PEC 9/2023",
        "proposicao_id": 2352476,
        "data": "2024-07-11",
        "resultado_oficial": "Aprovado em 2º turno (Sim: 338, Não: 83, Abst: 4)",
        "url_votacao": "https://dadosabertos.camara.leg.br/api/v2/votacoes/2352476-168",
        "url_proposicao": "https://www.camara.leg.br/propostas-legislativas/2352476",
        "criterio_resumo": "Emenda à Constituição que concedeu anistia a partidos políticos sobre prestações de contas anteriores e redistribuição de cotas."
    },
    {
        "id": "2422697-75",
        "ordem": 5,
        "titulo": "Taxação de Compras Internacionais (Mover / Blusinhas)",
        "subtitulo": "Cobrança de alíquota de 20% do Imposto de Importação sobre compras internacionais até US$ 50.",
        "proposicao": "PL 914/2024",
        "proposicao_id": 2422697,
        "data": "2024-05-28",
        "resultado_oficial": "Mantido o texto da alíquota (Sim: 280, Não: 121)",
        "url_votacao": "https://dadosabertos.camara.leg.br/api/v2/votacoes/2422697-75",
        "url_proposicao": "https://www.camara.leg.br/propostas-legislativas/2422697",
        "criterio_resumo": "Votação do destaque no PL do Programa Mover que instituiu o fim da isenção tributária para remessas postais internacionais de pequeno valor."
    }
]


def load_votacoes():
    votacoes_data = {}
    for tema in TEMAS_CATALOGO:
        vid = tema["id"]
        filepath = VOTACOES_DIR / f"{vid}.json"
        if not filepath.exists():
            print(f"ERRO: Arquivo de votação não encontrado: {filepath}", file=sys.stderr)
            sys.exit(1)
        with open(filepath, "r", encoding="utf-8") as f:
            votacoes_data[vid] = json.load(f)
    return votacoes_data


def parse_deputado_md(filepath: pathlib.Path):
    dep_id = int(filepath.stem)
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    foto_match = re.search(r'\!\[Foto\]\((https?://[^\)]+)\)', content)
    foto_url = foto_match.group(1) if foto_match else ""

    def get_field(label: str) -> str:
        m = re.search(r'\|\s*' + re.escape(label) + r'\s*\|\s*([^\|]+?)\s*\|', content)
        return m.group(1).strip() if m else ""

    nome_eleitoral = get_field("Nome eleitoral")
    nome_civil = get_field("Nome civil")
    partido = get_field("Partido")
    uf = get_field("UF")
    situacao = get_field("Situação")

    return {
        "id": dep_id,
        "nome_eleitoral": nome_eleitoral,
        "nome_civil": nome_civil,
        "partido": partido,
        "uf": uf,
        "situacao": situacao,
        "url_foto": foto_url,
        "url_perfil_camara": f"https://www.camara.leg.br/deputados/{dep_id}",
    }


def main():
    print("Compilando dados para o site do MVP v0...")
    SITE_DATA_DIR.mkdir(parents=True, exist_ok=True)

    votacoes = load_votacoes()
    print(f"Carregadas {len(votacoes)} votações oficiais.")

    md_files = sorted(DEPUTADOS_DIR.glob("*.md"))
    if not md_files:
        print(f"ERRO: Nenhum arquivo em {DEPUTADOS_DIR}", file=sys.stderr)
        sys.exit(1)

    deputados = []
    for p in md_files:
        dep = parse_deputado_md(p)
        dep_id_str = str(dep["id"])

        votos_map = {}
        for tema in TEMAS_CATALOGO:
            vid = tema["id"]
            votacao_json = votacoes[vid]
            votos_dict = votacao_json.get("votos", {})

            if dep_id_str in votos_dict:
                votos_map[vid] = votos_dict[dep_id_str].get("tipoVoto", "Sim")
            else:
                # Se não consta na lista de quem registrou voto no painel, é formalmente Ausente
                votos_map[vid] = "Não votou / Ausente"

        dep["votos"] = votos_map
        deputados.append(dep)

    # Ordena deputados por nome eleitoral para facilitar busca e navegação
    deputados.sort(key=lambda d: d["nome_eleitoral"].lower())

    out_deputados = SITE_DATA_DIR / "deputados.json"
    with open(out_deputados, "w", encoding="utf-8") as f:
        json.dump(deputados, f, ensure_ascii=False, indent=2)

    out_temas = SITE_DATA_DIR / "temas.json"
    with open(out_temas, "w", encoding="utf-8") as f:
        json.dump(TEMAS_CATALOGO, f, ensure_ascii=False, indent=2)

    print(f"Sucesso!")
    print(f"  - {len(deputados)} deputados exportados em: {out_deputados} ({out_deputados.stat().st_size / 1024:.1f} KB)")
    print(f"  - {len(TEMAS_CATALOGO)} temas exportados em: {out_temas} ({out_temas.stat().st_size / 1024:.1f} KB)")


if __name__ == "__main__":
    main()
