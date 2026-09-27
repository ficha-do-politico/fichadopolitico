"""
Compila os dados de 513 deputados federais e as votações curadas para o frontend do MVP v0.

Entrada:
  - dados/catalogo/temas.json (catálogo curado com proposições e links oficiais)
  - dados/camara/deputados.json (dataset canônico consolidado da Câmara)
  - dados/camara/votacoes/*.json (votações nominais extraídas da API da Câmara)
  - dados/senado/senadores.json (dataset canônico consolidado do Senado)

Saída:
  - site/src/data/deputados.json (dataset compacto consumido pelo site)
  - site/src/data/senadores.json (dataset de senadores consumido pelo site)
  - site/src/data/temas.json (catálogo dos temas consumido pelo site)

Regras de negócio:
  - LGPD / AD-009: NÃO inclui CPF, telefone pessoal ou email.
  - Verificabilidade / AGENTS.md §3.1: Cada voto e tema inclui links oficiais diretos.
  - Regra de Ausência: Se o parlamentar não registrou voto no painel eletrônico, é categorizado como 'Não votou / Ausente'.
"""

import json
import pathlib
import sys
import unicodedata

ROOT = pathlib.Path(__file__).resolve().parent.parent
CATALOGO_FILE = ROOT / "dados" / "catalogo" / "temas.json"
CAMARA_DIR = ROOT / "dados" / "camara"
CANON_DEPUTADOS_FILE = CAMARA_DIR / "deputados.json"
VOTACOES_DIR = CAMARA_DIR / "votacoes"
SENADO_DIR = ROOT / "dados" / "senado"
CANON_SENADORES_FILE = SENADO_DIR / "senadores.json"
SENADO_VOTACOES_DIR = SENADO_DIR / "votacoes"
TSE_DIR = ROOT / "dados" / "tse"
CANON_PRESIDENCIA_FILE = TSE_DIR / "presidencia.json"
CANON_CONGRESSO_2026_FILE = TSE_DIR / "congresso_2026.json"
CANON_PARTIDOS_TSE_FILE = TSE_DIR / "partidos.json"
CANON_DESPESAS_2026_FILE = CAMARA_DIR / "despesas_2026.json"
CANON_SENADO_DESPESAS_2026_FILE = SENADO_DIR / "despesas_2026.json"
EMENDAS_DIR = ROOT / "dados" / "emendas"
CANON_EMENDAS_FILE = EMENDAS_DIR / "emendas_resumo.json"
SITE_DATA_DIR = ROOT / "site" / "src" / "data"

# Módulo TSE 2026: alimentado pelos dumps oficiais do TSE (scripts/tse/fetch_candidaturas.py)
# em cumprimento às tarefas P1–P3 de docs/auditoria-dados-tse-2026.md.
TSE_2026_SUSPENSO = False
TSE_AUDITORIA_URL = "https://github.com/ficha-do-politico/fichadopolitico/blob/main/docs/auditoria-dados-tse-2026.md"


def load_catalogo_temas():
    if not CATALOGO_FILE.exists():
        print(f"ERRO: Catálogo de temas não encontrado em {CATALOGO_FILE}", file=sys.stderr)
        sys.exit(1)
    with open(CATALOGO_FILE, encoding="utf-8") as f:
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
        with open(filepath, encoding="utf-8") as f:
            votacoes_data[vid] = json.load(f)
    return votacoes_data


def load_senado_votacoes(temas):
    senado_votacoes_data = {}
    if not SENADO_VOTACOES_DIR.exists():
        return senado_votacoes_data
    for tema in temas:
        vid = tema["id"]
        filepath = SENADO_VOTACOES_DIR / f"{vid}.json"
        if filepath.exists():
            with open(filepath, encoding="utf-8") as f:
                senado_votacoes_data[vid] = json.load(f)
    return senado_votacoes_data


def load_deputados_base():
    """Carrega dados biográficos canônicos dos deputados a partir de dados/camara/deputados.json."""
    if not CANON_DEPUTADOS_FILE.exists():
        print(
            f"ERRO: Dataset canônico da Câmara não encontrado em {CANON_DEPUTADOS_FILE}",
            file=sys.stderr,
        )
        sys.exit(1)

    with open(CANON_DEPUTADOS_FILE, encoding="utf-8") as f:
        raw_deputados = json.load(f)

    deputados = []
    for d in raw_deputados:
        deputados.append(
            {
                "id": int(d["id"]),
                "nome_eleitoral": str(d["nome_eleitoral"]),
                "nome_civil": str(d["nome_civil"]),
                "partido": str(d["partido"]),
                "uf": str(d["uf"]),
                "situacao": str(d["situacao"]),
                "url_foto": str(d["url_foto"]),
                "url_perfil_camara": str(
                    d.get("url_perfil_camara") or f"https://www.camara.leg.br/deputados/{d['id']}"
                ),
            }
        )
    return deputados


def load_congresso_2026():
    """Carrega dados canônicos de candidaturas e patrimônio do Congresso Nacional (TSE 2026)."""
    if TSE_2026_SUSPENSO or not CANON_CONGRESSO_2026_FILE.exists():
        return {}
    with open(CANON_CONGRESSO_2026_FILE, encoding="utf-8") as f:
        return json.load(f)


def load_camara_despesas_2026():
    """Carrega dados canônicos agregados da CEAP 2026 da Câmara dos Deputados."""
    if not CANON_DESPESAS_2026_FILE.exists():
        return {}
    with open(CANON_DESPESAS_2026_FILE, encoding="utf-8") as f:
        return json.load(f)


def load_senado_despesas_2026():
    """Carrega dados canônicos agregados da CEAPS 2026 do Senado Federal."""
    if not CANON_SENADO_DESPESAS_2026_FILE.exists():
        return {}
    with open(CANON_SENADO_DESPESAS_2026_FILE, encoding="utf-8") as f:
        return json.load(f)


def load_emendas():
    """Carrega dados canônicos consolidados de emendas parlamentares (CGU 2023-2026)."""
    if not CANON_EMENDAS_FILE.exists():
        return {}
    with open(CANON_EMENDAS_FILE, encoding="utf-8") as f:
        return json.load(f)


def validar_integridade(deputados, temas):
    """Validações estritas de conformidade com AD-006 (verificabilidade) e AD-009 (LGPD)."""
    # 1. Validação de verificabilidade dos temas
    for t in temas:
        if not t.get("url_votacao", "").startswith("https://"):
            raise ValueError(f"Tema {t.get('id')} sem url_votacao oficial válida.")
        if not t.get("url_proposicao", "").startswith("https://"):
            raise ValueError(f"Tema {t.get('id')} sem url_proposicao oficial válida.")

    # 2. Validação LGPD: assegurar que dados privados nunca entrem nos datasets públicos
    campos_proibidos = {
        "cpf",
        "email",
        "telefone",
        "redes",
        "redeSocial",
        "rg",
        "endereco",
        "titulo_eleitor",
    }
    for d in deputados:
        chaves_encontradas = set(d.keys()).intersection(campos_proibidos)
        if chaves_encontradas:
            raise ValueError(
                f"Violação LGPD detectada: chaves proibidas {chaves_encontradas} no deputado {d.get('id')}"
            )
        cand = d.get("candidatura_2026")
        if cand:
            chaves_cand = set(cand.keys()).intersection(campos_proibidos)
            if chaves_cand:
                raise ValueError(
                    f"Violação LGPD na candidatura 2026: chaves {chaves_cand} no deputado {d.get('id')}"
                )
            url_tse = cand.get("url_divulgacand", "")
            if not url_tse.startswith("https://divulgacandcontas.tse.jus.br"):
                raise ValueError(f"Deputado {d.get('id')} com URL DivulgaCand inválida: {url_tse}")

        desp = d.get("despesas_2026")
        if desp:
            chaves_desp = set(desp.keys()).intersection(campos_proibidos)
            if chaves_desp:
                raise ValueError(
                    f"Violação LGPD nas despesas 2026: chaves {chaves_desp} no deputado {d.get('id')}"
                )
            for m in desp.get("maiores_despesas", []):
                u_doc = m.get("url_documento")
                if u_doc and not u_doc.startswith("https://"):
                    raise ValueError(
                        f"URL de comprovante fiscal insegura no deputado {d.get('id')}: {u_doc}"
                    )

        emendas = d.get("emendas")
        if emendas:
            chaves_emendas = set(emendas.keys()).intersection(campos_proibidos)
            if chaves_emendas:
                raise ValueError(
                    f"Violação LGPD nas emendas: chaves {chaves_emendas} no deputado {d.get('id')}"
                )
            u_cgu = emendas.get("url_portal_transparencia", "")
            if u_cgu and not u_cgu.startswith("https://portaldatransparencia.gov.br"):
                raise ValueError(f"URL CGU inválida no deputado {d.get('id')}: {u_cgu}")

        part = d.get("participacao_votacoes")
        if not part or not isinstance(part, dict):
            raise ValueError(f"Deputado {d.get('id')} sem participacao_votacoes válida.")
        if part.get("total") != len(temas):
            raise ValueError(f"Deputado {d.get('id')} com total de temas divergente do catálogo.")
        if not (0 <= part.get("registrados", -1) <= part.get("total", 0)):
            raise ValueError(
                f"Deputado {d.get('id')} com votos registrados fora do intervalo válido."
            )


def validar_senadores(senadores, temas):
    """Validações estritas de conformidade com AD-006 (verificabilidade) e AD-009 (LGPD) para o Senado."""
    campos_proibidos = {
        "cpf",
        "email",
        "telefone",
        "redes",
        "redeSocial",
        "rg",
        "endereco",
        "titulo_eleitor",
    }
    temas_senado_count = sum(1 for t in temas if "senado" in t)
    for s in senadores:
        chaves_encontradas = set(s.keys()).intersection(campos_proibidos)
        if chaves_encontradas:
            raise ValueError(
                f"Violação LGPD detectada: chaves proibidas {chaves_encontradas} no senador {s.get('id')}"
            )
        cand = s.get("candidatura_2026")
        if cand:
            chaves_cand = set(cand.keys()).intersection(campos_proibidos)
            if chaves_cand:
                raise ValueError(
                    f"Violação LGPD na candidatura 2026: chaves {chaves_cand} no senador {s.get('id')}"
                )
            url_tse = cand.get("url_divulgacand", "")
            if not url_tse.startswith("https://divulgacandcontas.tse.jus.br"):
                raise ValueError(f"Senador {s.get('id')} com URL DivulgaCand inválida: {url_tse}")
        desp = s.get("despesas_2026")
        if desp:
            chaves_desp = set(desp.keys()).intersection(campos_proibidos)
            if chaves_desp:
                raise ValueError(
                    f"Violação LGPD nas despesas 2026: chaves {chaves_desp} no senador {s.get('id')}"
                )
        emendas = s.get("emendas")
        if emendas:
            chaves_emendas = set(emendas.keys()).intersection(campos_proibidos)
            if chaves_emendas:
                raise ValueError(
                    f"Violação LGPD nas emendas: chaves {chaves_emendas} no senador {s.get('id')}"
                )
            u_cgu = emendas.get("url_portal_transparencia", "")
            if u_cgu and not u_cgu.startswith("https://portaldatransparencia.gov.br"):
                raise ValueError(f"URL CGU inválida no senador {s.get('id')}: {u_cgu}")
        url_perfil = s.get("url_perfil_senado", "")
        if not url_perfil.startswith("https://"):
            raise ValueError(f"Senador {s.get('id')} com url_perfil_senado inválida: {url_perfil}")

        part = s.get("participacao_votacoes")
        if not part or not isinstance(part, dict):
            raise ValueError(f"Senador {s.get('id')} sem participacao_votacoes válida.")
        if part.get("total") != temas_senado_count:
            raise ValueError(
                f"Senador {s.get('id')} com total divergente de temas do Senado ({part.get('total')} != {temas_senado_count})."
            )
        if not (0 <= part.get("registrados", -1) <= part.get("total", 0)):
            raise ValueError(
                f"Senador {s.get('id')} com votos registrados fora do intervalo válido."
            )

    for t in temas:
        if "senado" in t:
            sen_info = t["senado"]
            if not sen_info.get("url_votacao", "").startswith("https://"):
                raise ValueError(f"Tema {t.get('id')} sem url_votacao oficial do Senado válida.")
            if not sen_info.get("url_proposicao", "").startswith("https://"):
                raise ValueError(f"Tema {t.get('id')} sem url_proposicao oficial do Senado válida.")


def clean_sigla(s: str) -> str:
    """Normaliza sigla para comparação robusta insensível a acentos e caixa."""
    if not s:
        return ""
    nfkd = unicodedata.normalize("NFKD", str(s))
    return "".join(c for c in nfkd if not unicodedata.combining(c)).upper().strip()


def slugify_sigla(s: str) -> str:
    """Gera slug canônico em minúsculas e sem acentos para rotas estáticas (ex: 'uniao', 'pl')."""
    return clean_sigla(s).lower()


def get_orientacao_camara(orientacoes: list[dict], sigla_partido: str) -> str | None:
    """Extrai a orientação oficial de bancada para uma sigla partidária na Câmara dos Deputados."""
    sig = clean_sigla(sigla_partido)
    # 1. Match exato da sigla
    for o in orientacoes:
        b_clean = clean_sigla(o.get("bancada", ""))
        if b_clean == sig:
            return o.get("orientacao")
    # 2. Match de federação partidária oficial
    for o in orientacoes:
        b_clean = clean_sigla(o.get("bancada", ""))
        if "FDR" in b_clean:
            if sig in b_clean:
                return o.get("orientacao")
            if sig == "PCDOB" and "PC" in b_clean:
                return o.get("orientacao")
    # 3. Match de bloco parlamentar
    for o in orientacoes:
        b_clean = clean_sigla(o.get("bancada", ""))
        if "BL" in b_clean:
            if sig in b_clean:
                return o.get("orientacao")
            if sig == "REPUBLICANOS" and "REP" in b_clean:
                return o.get("orientacao")
            if sig == "CIDADANIA" and "CID" in b_clean:
                return o.get("orientacao")
    return None


def validar_partidos(partidos: list[dict]):
    """Validações estritas de conformidade com AD-004 (apartidarismo), AD-006 (verificabilidade) e AD-009 (LGPD)."""
    campos_proibidos = {
        "espectro",
        "ideologia",
        "rotulo",
        "score",
        "nota",
        "classificacao",
        "alinhamento",
        "ranking",
    }
    for p in partidos:
        fonte = p.get("fonte_oficial_tse", "")
        if not fonte.startswith("https://www.tse.jus.br"):
            raise ValueError(f"Partido {p.get('sigla')} com link oficial do TSE inválido: {fonte}")

        nr = p.get("numero_eleitoral")
        if not isinstance(nr, int) or not (10 <= nr <= 90):
            raise ValueError(f"Partido {p.get('sigla')} com número eleitoral inválido: {nr}")

        chaves_proibidas = set(p.keys()).intersection(campos_proibidos)
        if chaves_proibidas:
            raise ValueError(
                f"Violação AD-004 (Apartidarismo): chaves subjetivas/scores detectadas no partido {p.get('sigla')}: {chaves_proibidas}"
            )

        bancada = p.get("bancada", {})
        if bancada.get("total_congresso") != bancada.get("deputados", 0) + bancada.get(
            "senadores", 0
        ):
            raise ValueError(f"Inconsistência na soma da bancada do partido {p.get('sigla')}")

        recursos = p.get("recursos", {})
        if recursos.get("total_cota_2026", 0) < 0 or recursos.get("emendas_cgu_pagas", 0) < 0:
            raise ValueError(f"Recursos negativos detectados no partido {p.get('sigla')}")

    slugs_vistos = set()
    for p in partidos:
        slug = p.get("slug", "")
        if not slug or not slug.isalnum():
            raise ValueError(f"Partido {p.get('sigla')} com slug inválido: {slug}")
        if slug in slugs_vistos:
            raise ValueError(f"Slug duplicado detectado: {slug}")
        slugs_vistos.add(slug)


def compile_partidos_data(deputados, senadores, temas, votacoes_site_data):
    """Compila agregação estatística neutra dos partidos com representação e dados oficiais do TSE."""
    if not CANON_PARTIDOS_TSE_FILE.exists():
        print(
            f"AVISO: Arquivo canônico do TSE não encontrado em {CANON_PARTIDOS_TSE_FILE}",
            file=sys.stderr,
        )
        return []

    with open(CANON_PARTIDOS_TSE_FILE, encoding="utf-8") as f:
        tse_partidos = json.load(f)

    partidos_compilados = []

    for p in tse_partidos:
        sigla = p["sigla"]
        sigla_norm = clean_sigla(sigla)

        deps = [d for d in deputados if clean_sigla(d.get("partido", "")) == sigla_norm]
        sens = [s for s in senadores if clean_sigla(s.get("partido", "")) == sigla_norm]

        total_deps = len(deps)
        total_sens = len(sens)
        total_cong = total_deps + total_sens
        pct_cong = round((total_cong / 594.0) * 100, 2)

        ceap_camara = round(
            sum(
                d.get("despesas_2026", {}).get("total_gasto", 0.0)
                if d.get("despesas_2026")
                else 0.0
                for d in deps
            ),
            2,
        )
        ceaps_senado = round(
            sum(
                s.get("despesas_2026", {}).get("total_gasto", 0.0)
                if s.get("despesas_2026")
                else 0.0
                for s in sens
            ),
            2,
        )
        total_cota = round(ceap_camara + ceaps_senado, 2)

        emendas_pago = 0.0
        emendas_pix = 0.0
        emendas_definida = 0.0

        for par in deps + sens:
            em = par.get("emendas")
            if em:
                emendas_pago += em.get("total_pago", 0.0)
                mods = em.get("modalidades", {})
                emendas_pix += mods.get("especiais_pix", {}).get("total_pago", 0.0)
                emendas_definida += mods.get("finalidade_definida", {}).get("total_pago", 0.0)

        emendas_pago = round(emendas_pago, 2)
        emendas_pix = round(emendas_pix, 2)
        emendas_definida = round(emendas_definida, 2)

        # Votações na Câmara dos Deputados
        camara_temas_resultado = []
        taxas_adesao_validas = []

        for tema in temas:
            vid = tema["id"]
            v_meta = votacoes_site_data.get(vid, {}).get("camara", {})
            orients = v_meta.get("orientacoes", [])
            orientacao = get_orientacao_camara(orients, sigla)

            dist = {"sim": 0, "nao": 0, "abstencao": 0, "ausente": 0, "outro": 0}
            for d in deps:
                voto = d.get("votos", {}).get(vid, "Não votou / Ausente")
                if voto == "Sim":
                    dist["sim"] += 1
                elif voto == "Não":
                    dist["nao"] += 1
                elif voto in ("Abstenção", "Artigo 17"):
                    dist["abstencao"] += 1
                elif voto == "Não votou / Ausente":
                    dist["ausente"] += 1
                else:
                    dist["outro"] += 1

            total_votantes = dist["sim"] + dist["nao"] + dist["abstencao"] + dist["outro"]
            taxa_adesao = None

            if orientacao and orientacao in ("Sim", "Não") and total_votantes > 0:
                if orientacao == "Sim":
                    taxa_adesao = round((dist["sim"] / total_votantes) * 100, 1)
                elif orientacao == "Não":
                    taxa_adesao = round((dist["nao"] / total_votantes) * 100, 1)
                taxas_adesao_validas.append(taxa_adesao)

            camara_temas_resultado.append(
                {
                    "tema_id": vid,
                    "tema_titulo": tema.get("titulo", ""),
                    "orientacao_bancada": orientacao or "Sem orientação registrada",
                    "distribuicao_votos": dist,
                    "total_votantes": total_votantes,
                    "taxa_adesao_orientacao": taxa_adesao,
                }
            )

        # Votações no Senado Federal
        senado_temas_resultado = []
        for tema in temas:
            vid = tema["id"]
            if vid in votacoes_site_data and "senado" in votacoes_site_data[vid]:
                dist = {"sim": 0, "nao": 0, "abstencao": 0, "ausente": 0, "outro": 0}
                for s in sens:
                    voto = s.get("votos", {}).get(vid, "Não votou / Ausente")
                    if voto == "Sim":
                        dist["sim"] += 1
                    elif voto == "Não":
                        dist["nao"] += 1
                    elif voto in ("Abstenção", "Artigo 17"):
                        dist["abstencao"] += 1
                    elif voto == "Não votou / Ausente":
                        dist["ausente"] += 1
                    else:
                        dist["outro"] += 1

                senado_temas_resultado.append(
                    {
                        "tema_id": vid,
                        "tema_titulo": tema.get("titulo", ""),
                        "distribuicao_votos": dist,
                        "total_votantes": dist["sim"]
                        + dist["nao"]
                        + dist["abstencao"]
                        + dist["outro"],
                    }
                )

        media_adesao = (
            round(sum(taxas_adesao_validas) / len(taxas_adesao_validas), 1)
            if taxas_adesao_validas
            else None
        )

        partido_dict = {
            "sigla": sigla,
            "slug": slugify_sigla(sigla),
            "nome": p["nome"],
            "numero_eleitoral": p["numero_eleitoral"],
            "deferimento": p["deferimento"],
            "criacao": p.get("criacao", ""),
            "presidente_nacional": p["presidente_nacional"],
            "fonte_oficial_tse": p["fonte_oficial_tse"],
            "federacao": p.get("federacao"),
            "autodeclaracao": p.get("autodeclaracao", {}),
            "bancada": {
                "deputados": total_deps,
                "senadores": total_sens,
                "total_congresso": total_cong,
                "percentual_congresso": pct_cong,
                "deputados_ids": [d["id"] for d in deps],
                "senadores_ids": [s["id"] for s in sens],
            },
            "recursos": {
                "ceap_camara_2026": ceap_camara,
                "ceaps_senado_2026": ceaps_senado,
                "total_cota_2026": total_cota,
                "emendas_cgu_pagas": emendas_pago,
                "emendas_pix_pagas": emendas_pix,
                "emendas_definida_pagas": emendas_definida,
            },
            "coesao": {
                "media_adesao_orientacao": media_adesao,
                "total_votacoes_avaliadas": len(taxas_adesao_validas),
            },
            "votacoes": {
                "camara": {
                    "total_temas": len(camara_temas_resultado),
                    "temas": camara_temas_resultado,
                },
                "senado": {
                    "total_temas": len(senado_temas_resultado),
                    "temas": senado_temas_resultado,
                },
            },
        }
        partidos_compilados.append(partido_dict)

    # Ordenação neutra: maiores bancadas primeiro; desempate alfabético por sigla
    partidos_compilados.sort(key=lambda x: (-x["bancada"]["total_congresso"], x["sigla"]))

    validar_partidos(partidos_compilados)
    return partidos_compilados


def main():
    print("Compilando dados para o site do Ficha do Político...")
    SITE_DATA_DIR.mkdir(parents=True, exist_ok=True)
    CAMARA_DIR.mkdir(parents=True, exist_ok=True)
    SENADO_DIR.mkdir(parents=True, exist_ok=True)

    temas = load_catalogo_temas()
    print(f"Carregados {len(temas)} temas a partir de {CATALOGO_FILE.relative_to(ROOT)}")

    votacoes = load_votacoes(temas)
    print(
        f"Carregadas {len(votacoes)} votações oficiais da Câmara em {VOTACOES_DIR.relative_to(ROOT)}"
    )

    senado_votacoes = load_senado_votacoes(temas)
    print(
        f"Carregadas {len(senado_votacoes)} votações oficiais do Senado em {SENADO_VOTACOES_DIR.relative_to(ROOT)}"
    )

    congresso_2026 = load_congresso_2026()
    print(f"Carregadas {len(congresso_2026)} candidaturas de 2026 do Congresso Nacional (TSE)")

    despesas_camara_2026 = load_camara_despesas_2026()
    print(f"Carregadas despesas da CEAP 2026 para {len(despesas_camara_2026)} deputados da Câmara")

    despesas_senado_2026 = load_senado_despesas_2026()
    print(
        f"Carregadas despesas da CEAPS 2026 para {len(despesas_senado_2026)} senadores da República"
    )

    emendas = load_emendas()
    print(f"Carregadas emendas parlamentares (CGU 2023-2026) para {len(emendas)} parlamentares")

    deputados_base = load_deputados_base()
    print(f"Carregados {len(deputados_base)} deputados (base canônica)")

    deputados = []
    for dep in deputados_base:
        dep_id_str = str(dep["id"])
        dep["candidatura_2026"] = congresso_2026.get(dep_id_str)
        dep["despesas_2026"] = despesas_camara_2026.get(dep_id_str)
        dep["emendas"] = emendas.get(dep_id_str)

        votos_map = {}
        votos_registrados_count = 0
        for tema in temas:
            vid = tema["id"]
            votacao_json = votacoes[vid]
            votos_dict = votacao_json.get("votos", {})

            if dep_id_str in votos_dict:
                tipo_voto = votos_dict[dep_id_str].get("tipoVoto", "Sim")
                votos_map[vid] = tipo_voto
                if tipo_voto != "Não votou / Ausente":
                    votos_registrados_count += 1
            else:
                # Se não consta na lista de quem registrou voto no painel, é formalmente Ausente
                votos_map[vid] = "Não votou / Ausente"

        dep["votos"] = votos_map
        total_temas_camara = len(temas)
        dep["participacao_votacoes"] = {
            "total": total_temas_camara,
            "registrados": votos_registrados_count,
            "percentual": round((votos_registrados_count / total_temas_camara) * 100, 1)
            if total_temas_camara > 0
            else 0.0,
            "formatado": f"{votos_registrados_count}/{total_temas_camara}",
        }
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
        with open(CANON_SENADORES_FILE, encoding="utf-8") as f:
            senadores_raw = json.load(f)

        for sen in senadores_raw:
            sen_id_str = str(sen["id"])
            sen["candidatura_2026"] = congresso_2026.get(sen_id_str)
            sen["despesas_2026"] = despesas_senado_2026.get(sen_id_str)
            sen["emendas"] = emendas.get(sen_id_str)
            votos_map = {}
            votos_registrados_count = 0
            total_senado_temas = 0
            for tema in temas:
                vid = tema["id"]
                if vid in senado_votacoes:
                    total_senado_temas += 1
                    votacao_json = senado_votacoes[vid]
                    votos_dict = votacao_json.get("votos", {})
                    if sen_id_str in votos_dict:
                        tipo_voto = votos_dict[sen_id_str].get("tipoVoto", "Sim")
                        votos_map[vid] = tipo_voto
                        if tipo_voto != "Não votou / Ausente":
                            votos_registrados_count += 1
                    else:
                        votos_map[vid] = "Não votou / Ausente"
            sen["votos"] = votos_map
            sen["participacao_votacoes"] = {
                "total": total_senado_temas,
                "registrados": votos_registrados_count,
                "percentual": round((votos_registrados_count / total_senado_temas) * 100, 1)
                if total_senado_temas > 0
                else 0.0,
                "formatado": f"{votos_registrados_count}/{total_senado_temas}",
            }
            senadores.append(sen)

        senadores.sort(key=lambda s: s["nome_eleitoral"].lower())
        validar_senadores(senadores, temas)

        # Atualiza o arquivo canônico do Senado
        with open(CANON_SENADORES_FILE, "w", encoding="utf-8") as f:
            json.dump(senadores, f, ensure_ascii=False, indent=2)

        out_senadores = SITE_DATA_DIR / "senadores.json"
        with open(out_senadores, "w", encoding="utf-8") as f:
            json.dump(senadores, f, ensure_ascii=False, indent=2)
        print(
            f"  - {len(senadores)} senadores exportados em: {out_senadores} ({out_senadores.stat().st_size / 1024:.1f} KB)"
        )

    # 3. Compila metadados detalhados de cada votação (distribuição, orientações de bancada)
    votacoes_site_data = {}
    for tema in temas:
        vid = tema["id"]
        camara_raw = votacoes.get(vid, {})
        camara_meta = camara_raw.get("metadados", {})

        # Calcula distribuição precisa de votos da Câmara
        votos_camara_dict = camara_raw.get("votos", {})
        camara_dist = {}
        for v_item in votos_camara_dict.values():
            tv = v_item.get("tipoVoto", "Sim")
            camara_dist[tv] = camara_dist.get(tv, 0) + 1

        # Deputados que não registraram voto no painel eletrônico
        ausentes_camara = 513 - len(votos_camara_dict)
        if ausentes_camara > 0:
            camara_dist["Não votou / Ausente"] = ausentes_camara

        item = {
            "id": vid,
            "camara": {
                "votacao_id": camara_meta.get("votacao_id", vid),
                "dataHora": camara_meta.get("dataHora"),
                "descricao": camara_meta.get("descricao"),
                "siglaOrgao": camara_meta.get("siglaOrgao", "PLEN"),
                "total_votos_registrados": len(votos_camara_dict),
                "total_deputados_locais": 513,
                "total_ausentes": ausentes_camara,
                "distribuicao_votos": camara_dist,
                "orientacoes": camara_meta.get("orientacoes", []),
            },
        }

        if vid in senado_votacoes:
            sen_raw = senado_votacoes[vid]
            sen_meta = sen_raw.get("metadados", {})
            sen_votos_dict = sen_raw.get("votos", {})
            sen_dist = {}
            for v_item in sen_votos_dict.values():
                tv = v_item.get("tipoVoto", "Sim")
                sen_dist[tv] = sen_dist.get(tv, 0) + 1
            ausentes_senado = 81 - len(sen_votos_dict)
            if ausentes_senado > 0:
                sen_dist["Não votou / Ausente"] = ausentes_senado

            item["senado"] = {
                "senado_votacao_id": sen_meta.get("senado_votacao_id"),
                "senado_sessao_id": sen_meta.get("senado_sessao_id"),
                "codigo_materia": sen_meta.get("codigo_materia"),
                "data": sen_meta.get("data"),
                "descricao": sen_meta.get("descricao"),
                "resultado_oficial": sen_meta.get("resultado_oficial"),
                "url_votacao": sen_meta.get("url_votacao"),
                "url_proposicao": sen_meta.get("url_proposicao"),
                "total_votos_registrados": len(sen_votos_dict),
                "total_senadores": 81,
                "total_ausentes": ausentes_senado,
                "distribuicao_votos": sen_dist,
            }

        votacoes_site_data[vid] = item

    out_votacoes = SITE_DATA_DIR / "votacoes.json"
    with open(out_votacoes, "w", encoding="utf-8") as f:
        json.dump(votacoes_site_data, f, ensure_ascii=False, indent=2)

    # 4. Grava datasets do frontend Astro
    out_deputados = SITE_DATA_DIR / "deputados.json"
    with open(out_deputados, "w", encoding="utf-8") as f:
        json.dump(deputados, f, ensure_ascii=False, indent=2)

    out_temas = SITE_DATA_DIR / "temas.json"
    with open(out_temas, "w", encoding="utf-8") as f:
        json.dump(temas, f, ensure_ascii=False, indent=2)

    out_tse_status = SITE_DATA_DIR / "tse_status.json"
    with open(out_tse_status, "w", encoding="utf-8") as f:
        json.dump(
            {"suspenso": TSE_2026_SUSPENSO, "auditoria_url": TSE_AUDITORIA_URL},
            f,
            ensure_ascii=False,
            indent=2,
        )

    if TSE_2026_SUSPENSO or CANON_PRESIDENCIA_FILE.exists():
        presidencia = []
        if not TSE_2026_SUSPENSO:
            with open(CANON_PRESIDENCIA_FILE, encoding="utf-8") as f:
                presidencia = json.load(f)
        out_presidencia = SITE_DATA_DIR / "presidencia.json"
        with open(out_presidencia, "w", encoding="utf-8") as f:
            json.dump(presidencia, f, ensure_ascii=False, indent=2)
        print(
            f"  - {len(presidencia)} candidatos à presidência exportados em: {out_presidencia} ({out_presidencia.stat().st_size / 1024:.1f} KB)"
        )

    if TSE_2026_SUSPENSO or CANON_CONGRESSO_2026_FILE.exists():
        out_congresso_2026 = SITE_DATA_DIR / "congresso_2026.json"
        with open(out_congresso_2026, "w", encoding="utf-8") as f:
            json.dump(congresso_2026, f, ensure_ascii=False, indent=2)
        print(
            f"  - {len(congresso_2026)} candidaturas do congresso exportadas em: {out_congresso_2026} ({out_congresso_2026.stat().st_size / 1024:.1f} KB)"
        )

    if CANON_DESPESAS_2026_FILE.exists():
        out_despesas = SITE_DATA_DIR / "despesas_camara_2026.json"
        with open(out_despesas, "w", encoding="utf-8") as f:
            json.dump(despesas_camara_2026, f, ensure_ascii=False, indent=2)
        print(
            f"  - {len(despesas_camara_2026)} despesas CEAP exportadas em: {out_despesas} ({out_despesas.stat().st_size / 1024:.1f} KB)"
        )

    if CANON_SENADO_DESPESAS_2026_FILE.exists():
        out_despesas_senado = SITE_DATA_DIR / "despesas_senado_2026.json"
        with open(out_despesas_senado, "w", encoding="utf-8") as f:
            json.dump(despesas_senado_2026, f, ensure_ascii=False, indent=2)
        print(
            f"  - {len(despesas_senado_2026)} despesas CEAPS exportadas em: {out_despesas_senado} ({out_despesas_senado.stat().st_size / 1024:.1f} KB)"
        )

    # 5. Compila e exporta partidos (TSE + Bancadas do Congresso Nacional)
    partidos_data = compile_partidos_data(deputados, senadores, temas, votacoes_site_data)
    out_partidos = SITE_DATA_DIR / "partidos.json"
    with open(out_partidos, "w", encoding="utf-8") as f:
        json.dump(partidos_data, f, ensure_ascii=False, indent=2)
    print(
        f"  - {len(partidos_data)} partidos exportados em: {out_partidos} ({out_partidos.stat().st_size / 1024:.1f} KB)"
    )

    print("Sucesso!")
    print(
        f"  - Dataset canônico da Câmara: {canon_deputados} ({canon_deputados.stat().st_size / 1024:.1f} KB)"
    )
    print(
        f"  - {len(deputados)} deputados exportados em: {out_deputados} ({out_deputados.stat().st_size / 1024:.1f} KB)"
    )
    print(
        f"  - {len(temas)} temas exportados em: {out_temas} ({out_temas.stat().st_size / 1024:.1f} KB)"
    )
    print(
        f"  - {len(votacoes_site_data)} detalhes de votações exportados em: {out_votacoes} ({out_votacoes.stat().st_size / 1024:.1f} KB)"
    )


if __name__ == "__main__":
    main()
