"""
Ingestão e padronização vetorial dos logos oficiais dos 30 partidos políticos registrados no TSE.

Atende a:
  - AD-006: Verificabilidade e rastreabilidade estrita da fonte oficial/pública.
  - AD-004: Apartidarismo estrito — tratamento visual idêntico para todas as legendas.
  - SSG offline: Salva os arquivos vetoriais em `site/public/partidos/{slug}.svg` para zero dependência de rede em tempo de build ou execução.
"""

from __future__ import annotations

import base64
import json
import pathlib
import struct
import time
import urllib.parse
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
PARTIDOS_JSON = ROOT / "site" / "src" / "data" / "partidos.json"
OUTPUT_DIR = ROOT / "site" / "public" / "partidos"
MANIFEST_FILE = ROOT / "site" / "src" / "data" / "partidos_logos_manifest.json"

HEADERS = {
    "User-Agent": "FichaDoPoliticoBot/1.0 (https://github.com/ficha-do-politico; contato@fichadopolitico.com.br)"
}

# Mapeamento canônico dos 30 partidos registrados no TSE para seus arquivos oficiais na Wikimedia / Wikipédia
COMMONS_MAPPING: dict[str, str] = {
    "pl": "File:Partido Liberal (Brazil) logo.svg",
    "pt": "File:PT (Brazil) logo 2021.svg",
    "psd": "File:PSD Brazil logo.svg",
    "uniao": "File:União Brasil logo.svg",
    "pp": "File:Progressistas (Brazil) logo.svg",
    "republicanos": "File:Republicanos logo.png",
    "mdb": "File:Brazilian Democratic Movement logo.svg",
    "pode": "File:Podemos (Brasil) logo.svg",
    "psb": "File:Logo of the Brazilian Socialist Party (wordmark color).svg",
    "psdb": "File:Logo of the Brazilian Social Democracy Party (2023).svg",
    "psol": "File:Logo PSOL roxo.svg",
    "pcdob": "File:PCdoB flag.svg",
    "pdt": "File:Bandeira.PDT.png",
    "avante": "File:Avante 70 (Brasil) logo.svg",
    "pv": "File:Bandeira Partido Verde Brasil.svg",
    "novo": "File:Partido Novo logo (2023).svg",
    "solidariedade": "File:Solidariedade 77 (Brasil) logo.svg",
    "prd": "File:Partido Renovação Democrática logo.svg",
    "rede": "File:Rede Sustentabilidade logo.svg",
    "cidadania": "File:Cidadania (Brasil) logo (variant 1).svg",
    "dc": "File:Logomarca Democracia Cristã.png",
    "missao": "File:Bandeira do Partido Missão.svg",
    "agir": "File:Logomarca do Partido Agir.png",
    "democrata": "File:Logomarca O Democrata 35.png",
    "mobiliza": "File:Logomarca Partido Mobiliza.png",
    "pcb": "File:Logo PCB.png",
    "pco": "File:Logo PCO Institucional.svg",
    "prtb": "File:Logomarca do Partido Renovador Trabalhista Brasileiro.png",
    "pstu": "File:Logo PSTU.png",
    "up": "File:Logo - UP site.png",
}


def get_image_info(filename: str) -> dict[str, str | int] | None:
    """Busca a URL direta e metadados no Wikimedia Commons ou na Wikipédia em português."""
    for api_base in (
        "https://commons.wikimedia.org/w/api.php",
        "https://pt.wikipedia.org/w/api.php",
    ):
        params = {
            "action": "query",
            "titles": filename,
            "prop": "imageinfo",
            "iiprop": "url|mime|size",
            "iiurlwidth": "320",
            "format": "json",
        }
        url = f"{api_base}?{urllib.parse.urlencode(params)}"
        req = urllib.request.Request(url, headers=HEADERS)
        try:
            with urllib.request.urlopen(req, timeout=15) as res:
                data = json.loads(res.read().decode("utf-8"))
            pages = data.get("query", {}).get("pages", {})
            for _pid, pdata in pages.items():
                imageinfo = pdata.get("imageinfo")
                if imageinfo and len(imageinfo) > 0:
                    return imageinfo[0]
        except Exception as e:
            print(f"  [Aviso] Falha ao consultar {api_base} para {filename}: {e}")
    return None


def get_png_dimensions(data: bytes) -> tuple[int, int]:
    """Extrai largura e altura do cabeçalho IHDR de um arquivo PNG."""
    if len(data) >= 24 and data[:8] == b"\x89PNG\r\n\x1a\n":
        w, h = struct.unpack(">II", data[16:24])
        return w, h
    return 200, 200


def wrap_png_in_svg(png_data: bytes) -> str:
    """Empacota imagem raster PNG dentro de um container SVG válido e responsivo."""
    w, h = get_png_dimensions(png_data)
    b64 = base64.b64encode(png_data).decode("ascii")
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
        f'width="{w}" height="{h}">\n'
        f'  <image width="{w}" height="{h}" href="data:image/png;base64,{b64}" />\n'
        f"</svg>\n"
    )


def create_default_fallback_svg() -> str:
    """Gera um SVG institucional neutro para fallback de partidos sem logo carregado."""
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100">\n'
        '  <rect width="100" height="100" rx="16" fill="#0f172a" />\n'
        '  <path d="M50 22 L22 36 L22 42 L78 42 L78 36 Z M30 46 L36 46 L36 70 L30 70 Z '
        "M44 46 L50 46 L50 70 L44 70 Z M58 46 L64 46 L64 70 L58 70 Z "
        'M20 74 L80 74 L80 78 L20 78 Z" fill="#ffffff" />\n'
        "</svg>\n"
    )


def fetch_all_logos() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(PARTIDOS_JSON, encoding="utf-8") as f:
        partidos = json.load(f)

    manifest: dict[str, dict[str, str | int]] = {}
    total = len(partidos)
    print(f"Iniciando download e processamento dos logos de {total} partidos...")

    # Gera fallback padrão
    fallback_path = OUTPUT_DIR / "default.svg"
    with open(fallback_path, "w", encoding="utf-8") as f:
        f.write(create_default_fallback_svg())

    for idx, p in enumerate(partidos, 1):
        slug = p["slug"]
        sigla = p["sigla"]
        filename = COMMONS_MAPPING.get(slug)

        if not filename:
            print(f"[{idx}/{total}] ⚠️ {sigla} ({slug}) sem arquivo mapeado.")
            continue

        print(f"[{idx}/{total}] Baixando {sigla} ({slug}) <- {filename}...")
        info = get_image_info(filename)
        if not info:
            raise RuntimeError(f"Não foi possível obter informações para {sigla} ({filename})")

        mime_type = str(info["mime"])
        if "svg" in mime_type:
            img_url = str(info["url"])
        else:
            img_url = str(info.get("thumburl") or info["url"])

        req = urllib.request.Request(img_url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=20) as res:
            content_bytes = res.read()

        target_file = OUTPUT_DIR / f"{slug}.svg"
        if "svg" in mime_type:
            svg_text = content_bytes.decode("utf-8", errors="replace")
            with open(target_file, "w", encoding="utf-8") as f:
                f.write(svg_text)
        else:
            # Imagem PNG empacotada em vetor SVG
            svg_text = wrap_png_in_svg(content_bytes)
            with open(target_file, "w", encoding="utf-8") as f:
                f.write(svg_text)

        manifest[slug] = {
            "sigla": sigla,
            "nome": p["nome"],
            "numero_eleitoral": p["numero_eleitoral"],
            "url_fonte_oficial": img_url,
            "arquivo_fonte": filename,
            "mime_original": mime_type,
            "tamanho_bytes": len(content_bytes),
        }

        # Cortesia de taxa para Wikimedia
        time.sleep(0.4)

    with open(MANIFEST_FILE, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)

    print(f"\nSucesso: {len(manifest)} logos vetoriais salvos em {OUTPUT_DIR.relative_to(ROOT)}")
    print(f"Manifesto de proveniência gravado em {MANIFEST_FILE.relative_to(ROOT)}")


if __name__ == "__main__":
    fetch_all_logos()
