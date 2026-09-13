"""
Ingestão de dados oficiais dos 513 deputados federais da Câmara dos Deputados em exercício.
Fonte: API de Dados Abertos da Câmara dos Deputados (https://dadosabertos.camara.leg.br/api/v2/)
Endpoints:
  - GET /deputados?ordem=ASC&ordenarPor=nome
  - GET /deputados/{id}

Conformidade e Regras:
  - LGPD (AD-009): NÃO inclui telefones, emails ou CPF.
  - Verificabilidade (AD-006): Links diretos para fotos e páginas oficiais da Câmara em HTTPS.
  - Formato Canônico: dados/camara/deputados.json
"""

import argparse
import json
import pathlib
import sys

# Permite imports relativos a partir da raiz do projeto
ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from scripts.core.http_client import fetch_json  # noqa: E402

API_CAMARA_LISTA_URL = (
    "https://dadosabertos.camara.leg.br/api/v2/deputados?ordem=ASC&ordenarPor=nome"
)
API_CAMARA_DETAIL_URL = "https://dadosabertos.camara.leg.br/api/v2/deputados/{}"
OUTPUT_DIR = ROOT / "dados" / "camara"
OUTPUT_FILE = OUTPUT_DIR / "deputados.json"


def normalize_url_https(url: str) -> str:
    """Garante que URLs de fotos e perfis utilizem HTTPS para evitar mixed-content."""
    if not url:
        return ""
    if url.startswith("http://"):
        return "https://" + url[7:]
    return url


def load_existing_votos() -> dict:
    """Preserva votos já computados caso o dataset canônico exista."""
    if not OUTPUT_FILE.exists():
        return {}
    try:
        with open(OUTPUT_FILE, encoding="utf-8") as f:
            deps = json.load(f)
            return {d["id"]: d.get("votos", {}) for d in deps if "id" in d}
    except Exception:
        return {}


def fetch_and_save_deputados(limit: int | None = None, fetch_details: bool = False):
    print(f"Requisitando lista oficial de deputados em {API_CAMARA_LISTA_URL}...")
    payload = fetch_json(API_CAMARA_LISTA_URL)
    dados = payload.get("dados", [])

    if limit:
        dados = dados[:limit]

    print(f"Processando {len(dados)} deputados da Câmara...")
    existing_votos = load_existing_votos()

    deputados_canonicos = []
    for idx, d in enumerate(dados, 1):
        dep_id = d["id"]
        nome_eleitoral = d.get("nome", "").strip()
        partido = d.get("siglaPartido", "").strip()
        uf = d.get("siglaUf", "").strip()
        url_foto = normalize_url_https(d.get("urlFoto", "").strip())
        url_perfil = f"https://www.camara.leg.br/deputados/{dep_id}"

        nome_civil = nome_eleitoral
        situacao = "Exercício (Titular)"

        if fetch_details:
            try:
                detail = fetch_json(API_CAMARA_DETAIL_URL.format(dep_id))
                dd = detail.get("dados", {})
                nome_civil = dd.get("nomeCivil", nome_civil)
                us = dd.get("ultimoStatus", {})
                condicao = us.get("condicaoEleitoral", "")
                sit = us.get("situacao", "Exercício")
                situacao = f"{sit} ({condicao})" if condicao else sit
            except Exception as e:
                print(f"  [Aviso] Falha ao detalhar deputado {dep_id}: {e}", file=sys.stderr)

        # Sanitização LGPD (AD-009): CPF, telefone e email NÃO entram no dataset público.
        deputado = {
            "id": int(dep_id),
            "nome_eleitoral": nome_eleitoral,
            "nome_civil": nome_civil,
            "partido": partido,
            "uf": uf,
            "situacao": situacao,
            "url_foto": url_foto,
            "url_perfil_camara": url_perfil,
            "votos": existing_votos.get(int(dep_id), {}),
        }
        deputados_canonicos.append(deputado)

        if idx % 50 == 0 or idx == len(dados):
            print(f"  Processados {idx}/{len(dados)}...")

    deputados_canonicos.sort(key=lambda s: s["nome_eleitoral"])

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(deputados_canonicos, f, indent=2, ensure_ascii=False)
        f.write("\n")

    print(f"Sucesso: {len(deputados_canonicos)} deputados salvos em {OUTPUT_FILE}")


def main():
    parser = argparse.ArgumentParser(
        description="Ingestão oficial dos deputados federais da Câmara"
    )
    parser.add_argument("--limit", type=int, help="Limita o número de deputados para teste rápido")
    parser.add_argument(
        "--details",
        action="store_true",
        help="Busca endpoint de detalhes biográficos de cada deputado",
    )
    args = parser.parse_args()

    fetch_and_save_deputados(limit=args.limit, fetch_details=args.details)


if __name__ == "__main__":
    main()
