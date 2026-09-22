"""
Coletor e agregador de Emendas Parlamentares Federais da CGU (Portal da Transparência).
Conforme AD-016 (Rastreabilidade de Emendas) e AD-009 (LGPD).

Entrada:
  - Download oficial aberto: https://portaldatransparencia.gov.br/download-de-dados/emendas-parlamentares/download
  - dados/camara/deputados.json
  - dados/senado/senadores.json

Saída:
  - dados/emendas/emendas_resumo.json
"""

import argparse
import csv
import io
import json
import pathlib
import sys
import unicodedata
import urllib.request
import zipfile

ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
DADOS_DIR = ROOT / "dados"
EMENDAS_DIR = DADOS_DIR / "emendas"
CAMARA_FILE = DADOS_DIR / "camara" / "deputados.json"
SENADO_FILE = DADOS_DIR / "senado" / "senadores.json"
OUTPUT_FILE = EMENDAS_DIR / "emendas_resumo.json"
DEFAULT_ZIP_CACHE = EMENDAS_DIR / "EmendasParlamentares.zip"

CGU_DOWNLOAD_URL = (
    "https://portaldatransparencia.gov.br/download-de-dados/emendas-parlamentares/download"
)


def normalize(text: str) -> str:
    """Normaliza texto removendo acentos e convertendo para maiúsculas."""
    if not text:
        return ""
    nfkd = unicodedata.normalize("NFKD", text)
    cleaned = "".join(c for c in nfkd if not unicodedata.combining(c)).upper()
    return " ".join(cleaned.split())


def parse_brazilian_currency(val_str: str) -> float:
    """Converte string no formato '1.234.567,89' ou '1234,56' para float."""
    if not val_str:
        return 0.0
    val_clean = val_str.replace(".", "").replace(",", ".").strip()
    try:
        return float(val_clean)
    except ValueError:
        return 0.0


def format_currency(val: float) -> str:
    """Formata float para moeda brasileira R$ XX.XXX,XX."""
    return f"R$ {val:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def load_parlamentares():
    """Carrega deputados e senadores mapeando nomes normalizados para IDs."""
    if not CAMARA_FILE.exists() or not SENADO_FILE.exists():
        print("ERRO: Arquivos de deputados ou senadores não encontrados.", file=sys.stderr)
        sys.exit(1)

    with open(CAMARA_FILE, encoding="utf-8") as f:
        deputados = json.load(f)

    with open(SENADO_FILE, encoding="utf-8") as f:
        senadores = json.load(f)

    name_to_parlamentar = {}

    for d in deputados:
        info = {
            "id": d["id"],
            "casa": "camara",
            "nome_eleitoral": d["nome_eleitoral"],
            "nome_civil": d["nome_civil"],
            "uf": d["uf"],
            "partido": d["partido"],
        }
        name_to_parlamentar[normalize(d["nome_civil"])] = info
        name_to_parlamentar[normalize(d["nome_eleitoral"])] = info

    for s in senadores:
        info = {
            "id": s["id"],
            "casa": "senado",
            "nome_eleitoral": s["nome_eleitoral"],
            "nome_civil": s["nome_civil"],
            "uf": s["uf"],
            "partido": s["partido"],
        }
        name_to_parlamentar[normalize(s["nome_civil"])] = info
        name_to_parlamentar[normalize(s["nome_eleitoral"])] = info

    return deputados, senadores, name_to_parlamentar


def get_zip_stream(zip_path: pathlib.Path | None = None) -> zipfile.ZipFile:
    """Obtém o objeto ZipFile a partir de arquivo local ou download."""
    if zip_path and zip_path.exists():
        print(f"Lendo pacote de emendas local: {zip_path}")
        return zipfile.ZipFile(zip_path, "r")

    if DEFAULT_ZIP_CACHE.exists():
        print(f"Lendo pacote do cache: {DEFAULT_ZIP_CACHE}")
        return zipfile.ZipFile(DEFAULT_ZIP_CACHE, "r")

    print(f"Baixando pacote de dados consolidado da CGU: {CGU_DOWNLOAD_URL}")
    req = urllib.request.Request(
        CGU_DOWNLOAD_URL,
        headers={"User-Agent": "FichaDoPolitico/1.0 (dados-abertos; contato@fichadopolitico.org)"},
    )

    EMENDAS_DIR.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(req, timeout=120) as resp:
        content = resp.read()

    with open(DEFAULT_ZIP_CACHE, "wb") as f:
        f.write(content)
    print(f"Pacote salvo em cache: {DEFAULT_ZIP_CACHE} ({len(content)} bytes)")

    return zipfile.ZipFile(io.BytesIO(content), "r")


def process_emendas(zf: zipfile.ZipFile, name_to_parlamentar: dict) -> dict:
    """Processa o CSV de emendas parlamentares agrupando por parlamentar."""
    csv_filename = "EmendasParlamentares.csv"
    if csv_filename not in zf.namelist():
        raise FileNotFoundError(f"Arquivo {csv_filename} não encontrado no ZIP.")

    parlamentar_emendas = {}

    with zf.open(csv_filename) as f:
        text_stream = io.TextIOWrapper(f, encoding="latin1")
        reader = csv.reader(text_stream, delimiter=";")
        header = next(reader)

        # Índices das colunas
        idx_ano = header.index("Ano da Emenda")
        idx_tipo = header.index("Tipo de Emenda")
        idx_autor = header.index("Nome do Autor da Emenda")
        idx_num_emenda = header.index("Número da emenda")
        idx_municipio = header.index("Município")
        idx_uf = header.index("UF")
        idx_funcao = header.index("Nome Função")
        idx_subfuncao = header.index("Nome Subfunção")
        idx_v_empenhado = header.index("Valor Empenhado")
        idx_v_liquidado = header.index("Valor Liquidado")
        idx_v_pago = header.index("Valor Pago")
        idx_v_resto_pago = header.index("Valor Restos A Pagar Pagos")

        # Legislatura atual (57ª Legislatura: 2023 a 2026)
        anos_validos = {"2023", "2024", "2025", "2026"}

        for row in reader:
            ano = row[idx_ano].strip()
            if ano not in anos_validos:
                continue

            tipo_emenda = row[idx_tipo].strip()
            # Foco em emendas individuais do parlamentar
            if "Individual" not in tipo_emenda:
                continue

            autor_raw = row[idx_autor].strip()
            autor_norm = normalize(autor_raw)

            parlamentar = name_to_parlamentar.get(autor_norm)
            if not parlamentar:
                continue

            pid = str(parlamentar["id"])
            if pid not in parlamentar_emendas:
                parlamentar_emendas[pid] = {
                    "parlamentar_id": parlamentar["id"],
                    "casa": parlamentar["casa"],
                    "autor_cgu": autor_raw,
                    "nome_eleitoral": parlamentar["nome_eleitoral"],
                    "uf": parlamentar["uf"],
                    "partido": parlamentar["partido"],
                    "total_empenhado": 0.0,
                    "total_liquidado": 0.0,
                    "total_pago": 0.0,
                    "total_resto_pago": 0.0,
                    "especiais_pix_pago": 0.0,
                    "finalidade_definida_pago": 0.0,
                    "funcoes": {},
                    "municipios": {},
                    "total_registros": 0,
                    "ultimas_emendas": [],
                }

            reg = parlamentar_emendas[pid]
            reg["total_registros"] += 1

            v_emp = parse_brazilian_currency(row[idx_v_empenhado])
            v_liq = parse_brazilian_currency(row[idx_v_liquidado])
            v_pago = parse_brazilian_currency(row[idx_v_pago])
            v_resto = parse_brazilian_currency(row[idx_v_resto_pago])

            reg["total_empenhado"] += v_emp
            reg["total_liquidado"] += v_liq
            reg["total_pago"] += v_pago
            reg["total_resto_pago"] += v_resto

            # Categorização da modalidade
            is_pix = "Especiais" in tipo_emenda
            if is_pix:
                reg["especiais_pix_pago"] += v_pago
            else:
                reg["finalidade_definida_pago"] += v_pago

            # Função orçamentária
            funcao = row[idx_funcao].strip().capitalize() or "Outras"
            reg["funcoes"][funcao] = reg["funcoes"].get(funcao, 0.0) + v_pago

            # Município destinatário
            muni = row[idx_municipio].strip().title()
            uf_muni = row[idx_uf].strip().upper()
            if muni and muni.lower() != "sem informação":
                muni_key = f"{muni} - {uf_muni}"
                reg["municipios"][muni_key] = reg["municipios"].get(muni_key, 0.0) + v_pago

            # Amostra das emendas mais recentes (até 5)
            if len(reg["ultimas_emendas"]) < 5 and v_pago > 0:
                reg["ultimas_emendas"].append(
                    {
                        "ano": int(ano),
                        "numero": row[idx_num_emenda].strip(),
                        "tipo": "Emenda Pix" if is_pix else "Finalidade Definida",
                        "funcao": funcao,
                        "subfuncao": row[idx_subfuncao].strip(),
                        "localidade": muni_key
                        if (muni and muni.lower() != "sem informação")
                        else "Nacional",
                        "valor_pago": v_pago,
                        "valor_pago_formatado": format_currency(v_pago),
                    }
                )

    return parlamentar_emendas


def consolidate_summary(parlamentar_emendas: dict) -> dict:
    """Consolida os totais, percentuais e rankings formatados."""
    consolidated = {}

    for pid, data in parlamentar_emendas.items():
        total_pago = round(data["total_pago"], 2)
        pix_pago = round(data["especiais_pix_pago"], 2)
        def_pago = round(data["finalidade_definida_pago"], 2)

        # Percentuais por modalidade
        pct_pix = round((pix_pago / total_pago * 100), 1) if total_pago > 0 else 0.0
        pct_def = round((def_pago / total_pago * 100), 1) if total_pago > 0 else 0.0

        # Ranking de funções com valor pago > 0
        funcoes_sorted = [
            (func, val)
            for func, val in sorted(data["funcoes"].items(), key=lambda x: x[1], reverse=True)
            if val > 0
        ]
        ranking_funcoes = []
        for func, val in funcoes_sorted[:6]:
            pct = round((val / total_pago * 100), 1) if total_pago > 0 else 0.0
            ranking_funcoes.append(
                {
                    "funcao": func,
                    "valor_pago": round(val, 2),
                    "valor_formatado": format_currency(val),
                    "percentual": pct,
                }
            )

        # Ranking de municípios com valor pago > 0
        muni_sorted = [
            (m, val)
            for m, val in sorted(data["municipios"].items(), key=lambda x: x[1], reverse=True)
            if val > 0
        ]
        ranking_municipios = []
        for muni_key, val in muni_sorted[:5]:
            ranking_municipios.append(
                {
                    "municipio": muni_key,
                    "valor_pago": round(val, 2),
                    "valor_formatado": format_currency(val),
                }
            )

        # URL de verificabilidade no Portal da Transparência da CGU
        autor_param = urllib.parse.quote_plus(data["autor_cgu"])
        cgu_url = f"https://portaldatransparencia.gov.br/emendas/consulta?autor={autor_param}"

        consolidated[pid] = {
            "parlamentar_id": data["parlamentar_id"],
            "casa": data["casa"],
            "legislatura": "57ª (2023–2026)",
            "total_registros": data["total_registros"],
            "total_empenhado": round(data["total_empenhado"], 2),
            "total_empenhado_formatado": format_currency(data["total_empenhado"]),
            "total_liquidado": round(data["total_liquidado"], 2),
            "total_liquidado_formatado": format_currency(data["total_liquidado"]),
            "total_pago": total_pago,
            "total_pago_formatado": format_currency(total_pago),
            "total_resto_pago": round(data["total_resto_pago"], 2),
            "total_resto_pago_formatado": format_currency(data["total_resto_pago"]),
            "modalidades": {
                "especiais_pix": {
                    "total_pago": pix_pago,
                    "total_formatado": format_currency(pix_pago),
                    "percentual": pct_pix,
                },
                "finalidade_definida": {
                    "total_pago": def_pago,
                    "total_formatado": format_currency(def_pago),
                    "percentual": pct_def,
                },
            },
            "por_funcao": ranking_funcoes,
            "principais_municipios": ranking_municipios,
            "ultimas_emendas": data["ultimas_emendas"],
            "url_portal_transparencia": cgu_url,
        }

    return consolidated


def main():
    parser = argparse.ArgumentParser(
        description="Gera dados consolidados de Emendas Parlamentares Federais (CGU)."
    )
    parser.add_argument(
        "--zip",
        type=pathlib.Path,
        default=None,
        help="Caminho para arquivo ZIP local das emendas da CGU.",
    )
    args = parser.parse_args()

    print("Carregando base canônica de deputados e senadores...")
    _, _, name_to_parlamentar = load_parlamentares()

    zf = get_zip_stream(args.zip)

    print("Processando emendas da 57ª Legislatura (2023–2026)...")
    parlamentar_emendas = process_emendas(zf, name_to_parlamentar)
    print(f"Total de parlamentares mapeados com emendas: {len(parlamentar_emendas)}")

    consolidated = consolidate_summary(parlamentar_emendas)

    EMENDAS_DIR.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(consolidated, f, ensure_ascii=False, indent=2)

    print(f"Arquivo gerado com sucesso em: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
