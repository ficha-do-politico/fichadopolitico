"""
Compila os dados de 513 deputados federais e as votações curadas para o frontend do MVP v0.

Entrada:
  - dados/catalogo/temas.json (catálogo curado com proposições e links oficiais)
  - dados/camara/deputados.json (dataset canônico consolidado da Câmara)
  - dados/camara/votacoes/*.json (votações nominais extraídas da API da Câmara)
  - dados/camara/deputados/*.md (fallback para bootstrap se deputados.json não existir)

Saída:
  - dados/camara/deputados.json (dataset canônico consolidado da Câmara)
  - site/src/data/deputados.json (dataset compacto consumido pelo site)
  - site/src/data/temas.json (catálogo dos temas consumido pelo site)

Regras de negócio:
  - LGPD / AD-009: NÃO inclui CPF, telefone pessoal ou email.
  - Verificabilidade / AGENTS.md §3.1: Cada voto e tema inclui links oficiais diretos.
  - Regra de Ausência: Se o parlamentar não registrou voto no painel eletrônico, é categorizado como 'Não votou / Ausente'.
"""

import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
CATALOGO_FILE = ROOT / 'dados' / 'catalogo' / 'temas.json'
CAMARA_DIR = ROOT / 'dados' / 'camara'
CANON_DEPUTADOS_FILE = CAMARA_DIR / 'deputados.json'
DEPUTADOS_DIR = CAMARA_DIR / 'deputados'
VOTACOES_DIR = CAMARA_DIR / 'votacoes'
SENADO_DIR = ROOT / 'dados' / 'senado'
CANON_SENADORES_FILE = SENADO_DIR / 'senadores.json'
SITE_DATA_DIR = ROOT / 'site' / 'src' / 'data'


def load_catalogo_temas():
    if not CATALOGO_FILE.exists():
        print(f"ERRO: Catálogo de temas não encontrado em {CATALOGO_FILE}", file=sys.stderr)
        sys.exit(1)
    with open(CATALOGO_FILE, "r", encoding="utf-8") as f:
        temas = json.load(f)
    if not temas:
        print("ERRO: Catálogo de temas vazio.", file=sys.stderr)
        sys.exit(1)
    return temas


def load_votacoes(temas):
    votacoes_data = {}
    for tema in temas:
        vid = tema["id"]
        filepath = VOTACOES_DIR / f"{vid}.json"
        if not filepath.exists():
            print(f"ERRO: Arquivo de votação não encontrado: {filepath}", file=sys.stderr)
            sys.exit(1)
        with open(filepath, "r", encoding="utf-8") as f:
            votacoes_data[vid] = json.load(f)
    return votacoes_data


def parse_deputado_md(filepath: pathlib.Path):
    """Fallback legatário: parseia dados a partir do markdown gerado no discovery."""
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


def load_deputados_base():
    """Carrega dados biográficos canônicos dos deputados a partir de JSON ou fallback em MD."""
    if CANON_DEPUTADOS_FILE.exists():
        with open(CANON_DEPUTADOS_FILE, "r", encoding="utf-8") as f:
            raw_deputados = json.load(f)
        deputados = []
        for d in raw_deputados:
            deputados.append({
                "id": int(d["id"]),
                "nome_eleitoral": str(d["nome_eleitoral"]),
                "nome_civil": str(d["nome_civil"]),
                "partido": str(d["partido"]),
                "uf": str(d["uf"]),
                "situacao": str(d["situacao"]),
                "url_foto": str(d["url_foto"]),
                "url_perfil_camara": str(d.get("url_perfil_camara") or f"https://www.camara.leg.br/deputados/{d['id']}"),
            })
        return deputados

    # Fallback se deputados.json ainda não tiver sido compilado
    md_files = sorted(DEPUTADOS_DIR.glob("*.md")) if DEPUTADOS_DIR.exists() else []
    if not md_files:
        print(f"ERRO: Nem {CANON_DEPUTADOS_FILE} nem arquivos em {DEPUTADOS_DIR} encontrados.", file=sys.stderr)
        sys.exit(1)

    print(f"Aviso: {CANON_DEPUTADOS_FILE} ausente. Carregando dados a partir de {len(md_files)} arquivos .md (fallback)")
    return [parse_deputado_md(p) for p in md_files]


def validar_integridade(deputados, temas):
    """Validações estritas de conformidade com AD-006 (verificabilidade) e AD-009 (LGPD)."""
    # 1. Validação de verificabilidade dos temas
    for t in temas:
        if not t.get("url_votacao", "").startswith("https://"):
            raise ValueError(f"Tema {t.get('id')} sem url_votacao oficial válida.")
        if not t.get("url_proposicao", "").startswith("https://"):
            raise ValueError(f"Tema {t.get('id')} sem url_proposicao oficial válida.")

    # 2. Validação LGPD: assegurar que dados privados nunca entrem nos datasets públicos
    campos_proibidos = {"cpf", "email", "telefone", "redes", "redeSocial"}
    for d in deputados:
        chaves_encontradas = set(d.keys()).intersection(campos_proibidos)
        if chaves_encontradas:
            raise ValueError(f"Violação LGPD detectada: chaves proibidas {chaves_encontradas} no deputado {d.get('id')}")


def validar_senadores(senadores):
    """Validações estritas de conformidade com AD-006 (verificabilidade) e AD-009 (LGPD) para o Senado."""
    campos_proibidos = {"cpf", "email", "telefone", "redes", "redeSocial"}
    for s in senadores:
        chaves_encontradas = set(s.keys()).intersection(campos_proibidos)
        if chaves_encontradas:
            raise ValueError(f"Violação LGPD detectada: chaves proibidas {chaves_encontradas} no senador {s.get('id')}")
        url_perfil = s.get("url_perfil_senado", "")
        if not url_perfil.startswith("https://"):
            raise ValueError(f"Senador {s.get('id')} com url_perfil_senado inválida: {url_perfil}")


def main():
    print("Compilando dados para o site do Ficha do Político...")
    SITE_DATA_DIR.mkdir(parents=True, exist_ok=True)
    CAMARA_DIR.mkdir(parents=True, exist_ok=True)
    SENADO_DIR.mkdir(parents=True, exist_ok=True)

    temas = load_catalogo_temas()
    print(f"Carregados {len(temas)} temas a partir de {CATALOGO_FILE.relative_to(ROOT)}")

    votacoes = load_votacoes(temas)
    print(f"Carregadas {len(votacoes)} votações oficiais em {VOTACOES_DIR.relative_to(ROOT)}")

    deputados_base = load_deputados_base()
    print(f"Carregados {len(deputados_base)} deputados (base canônica)")

    deputados = []
    for dep in deputados_base:
        dep_id_str = str(dep["id"])

        votos_map = {}
        for tema in temas:
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

    # Ordena deputados por nome eleitoral para busca e navegação previsíveis
    deputados.sort(key=lambda d: d["nome_eleitoral"].lower())

    # Validação estrita antes de gravar em disco
    validar_integridade(deputados, temas)

    # 1. Grava dataset canônico da Câmara
    canon_deputados = CAMARA_DIR / "deputados.json"
    with open(canon_deputados, "w", encoding="utf-8") as f:
        json.dump(deputados, f, ensure_ascii=False, indent=2)

    # 2. Processa e compila senadores se existirem
    senadores = []
    if CANON_SENADORES_FILE.exists():
        with open(CANON_SENADORES_FILE, "r", encoding="utf-8") as f:
            senadores = json.load(f)
        validar_senadores(senadores)
        out_senadores = SITE_DATA_DIR / "senadores.json"
        with open(out_senadores, "w", encoding="utf-8") as f:
            json.dump(senadores, f, ensure_ascii=False, indent=2)
        print(f"  - {len(senadores)} senadores exportados em: {out_senadores} ({out_senadores.stat().st_size / 1024:.1f} KB)")

    # 3. Grava datasets do frontend Astro
    out_deputados = SITE_DATA_DIR / "deputados.json"
    with open(out_deputados, "w", encoding="utf-8") as f:
        json.dump(deputados, f, ensure_ascii=False, indent=2)

    out_temas = SITE_DATA_DIR / "temas.json"
    with open(out_temas, "w", encoding="utf-8") as f:
        json.dump(temas, f, ensure_ascii=False, indent=2)

    print("Sucesso!")
    print(f"  - Dataset canônico da Câmara: {canon_deputados} ({canon_deputados.stat().st_size / 1024:.1f} KB)")
    print(f"  - {len(deputados)} deputados exportados em: {out_deputados} ({out_deputados.stat().st_size / 1024:.1f} KB)")
    print(f"  - {len(temas)} temas exportados em: {out_temas} ({out_temas.stat().st_size / 1024:.1f} KB)")


if __name__ == "__main__":
    main()
