"""
Ingestão de dados oficiais dos 81 senadores da República em exercício.
Fonte: API de Dados Abertos do Senado Federal (https://legis.senado.leg.br/dadosabertos/)
Endpoint: GET /senador/lista/atual

Conformidade e Regras:
  - LGPD (AD-009): NÃO inclui telefones, emails ou CPF.
  - Verificabilidade (AD-006): Links diretos para fotos e páginas oficiais do Senado em HTTPS.
  - Formato Canônico: dados/senado/senadores.json
"""

import json
import pathlib
import sys

# Permite imports relativos a partir da raiz do projeto
ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT))

from scripts.core.http_client import fetch_json  # noqa: E402

API_SENADO_LISTA_URL = "https://legis.senado.leg.br/dadosabertos/senador/lista/atual"
OUTPUT_DIR = ROOT / "dados" / "senado"
OUTPUT_FILE = OUTPUT_DIR / "senadores.json"


def normalize_url_https(url: str) -> str:
    """Garante que URLs de mídia e perfis utilizem HTTPS para evitar avisos de mixed-content."""
    if not url:
        return ""
    if url.startswith("http://"):
        return "https://" + url[7:]
    return url


def fetch_and_save_senadores():
    print(f"Requisitando lista oficial de senadores em {API_SENADO_LISTA_URL}...")
    payload = fetch_json(API_SENADO_LISTA_URL)

    try:
        lista_exercicio = payload.get("ListaParlamentarEmExercicio", {})
        parlamentares_node = lista_exercicio.get("Parlamentares", {})
        parlamentares = parlamentares_node.get("Parlamentar", [])
    except Exception as e:
        print(f"ERRO: Estrutura inesperada no payload da API do Senado: {e}", file=sys.stderr)
        sys.exit(1)

    if not isinstance(parlamentares, list):
        # Caso a API retorne um único objeto quando houver apenas 1
        parlamentares = [parlamentares]

    print(f"Processando {len(parlamentares)} parlamentares recebidos do Senado...")

    senadores_canonicos = []
    for p in parlamentares:
        ident = p.get("IdentificacaoParlamentar", {})
        mandato = p.get("Mandato", {})

        codigo = ident.get("CodigoParlamentar")
        if not codigo:
            continue

        nome_eleitoral = ident.get("NomeParlamentar", "").strip()
        nome_civil = ident.get("NomeCompletoParlamentar", "").strip()
        partido = ident.get("SiglaPartidoParlamentar", "").strip()
        uf = ident.get("UfParlamentar", "").strip()
        
        participacao = mandato.get("DescricaoParticipacao", "Titular").strip()
        situacao = f"Exercício ({participacao})" if participacao else "Exercício"

        url_foto = normalize_url_https(ident.get("UrlFotoParlamentar", "").strip())
        url_perfil = normalize_url_https(ident.get("UrlPaginaParlamentar", "").strip())

        # Sanitização LGPD (AD-009): telefones e emails NÃO são gravados no dataset público.
        senador = {
            "id": int(codigo),
            "nome_eleitoral": nome_eleitoral,
            "nome_civil": nome_civil,
            "partido": partido,
            "uf": uf,
            "situacao": situacao,
            "url_foto": url_foto,
            "url_perfil_senado": url_perfil,
            "votos": {},
        }
        senadores_canonicos.append(senador)

    # Ordenação alfabética por nome eleitoral
    senadores_canonicos.sort(key=lambda s: s["nome_eleitoral"])

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(senadores_canonicos, f, indent=2, ensure_ascii=False)
        f.write("\n")

    print(f"Sucesso: {len(senadores_canonicos)} senadores salvos em {OUTPUT_FILE}")
    if len(senadores_canonicos) != 81:
        print(
            f"AVISO: Esperavam-se 81 senadores, mas foram processados {len(senadores_canonicos)}.",
            file=sys.stderr,
        )


if __name__ == "__main__":
    fetch_and_save_senadores()
