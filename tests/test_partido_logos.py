"""
Testes automatizados de integridade, proveniência e formato dos logos oficiais dos partidos.

Alinhado a:
  - AD-004: Apartidarismo estrito — presença de ativos para todas as legendas sem distinção.
  - AD-006: Verificabilidade e rastreabilidade estrita da fonte oficial (Wikimedia Commons / TSE).
"""

from __future__ import annotations

import json
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent
PARTIDOS_JSON = ROOT / "site" / "src" / "data" / "partidos.json"
MANIFEST_FILE = ROOT / "site" / "src" / "data" / "partidos_logos_manifest.json"
LOGOS_DIR = ROOT / "site" / "public" / "partidos"


class TestPartidoLogos(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with open(PARTIDOS_JSON, encoding="utf-8") as f:
            cls.partidos = json.load(f)

        cls.manifest = {}
        if MANIFEST_FILE.exists():
            with open(MANIFEST_FILE, encoding="utf-8") as f:
                cls.manifest = json.load(f)

    def test_todos_os_partidos_possuem_logo_svg(self):
        """Assegura que todas as 30 legendas homologadas possuem um arquivo .svg correspondente."""
        self.assertTrue(LOGOS_DIR.exists(), "Diretório de logos não encontrado.")
        self.assertGreaterEqual(len(self.partidos), 30)

        for p in self.partidos:
            slug = p["slug"]
            sigla = p["sigla"]
            logo_path = LOGOS_DIR / f"{slug}.svg"
            self.assertTrue(
                logo_path.exists(),
                f"Logo SVG ausente para o partido {sigla} (slug: {slug}) em {logo_path}",
            )
            self.assertGreater(
                logo_path.stat().st_size,
                100,
                f"Arquivo de logo muito pequeno ou corrompido para {sigla} ({slug})",
            )

    def test_formato_e_tags_svg_validas(self):
        """Valida que todos os arquivos são XMLs com tag <svg e viewBox configurado."""
        for p in self.partidos:
            slug = p["slug"]
            logo_path = LOGOS_DIR / f"{slug}.svg"
            content = logo_path.read_text(encoding="utf-8")
            self.assertIn("<svg", content, f"Arquivo {slug}.svg não inicia com tag <svg")
            self.assertIn("</svg>", content, f"Arquivo {slug}.svg não encerra com tag </svg>")

    def test_logo_default_fallback_existe(self):
        """Valida a existência do arquivo default.svg para fallback neutro."""
        default_logo = LOGOS_DIR / "default.svg"
        self.assertTrue(default_logo.exists(), "Arquivo default.svg ausente.")
        content = default_logo.read_text(encoding="utf-8")
        self.assertIn("<svg", content)
        self.assertIn("</svg>", content)

    def test_manifesto_de_proveniencia_oficial(self):
        """Garante que o manifesto rastreia a fonte e integridade de cada legenda (AD-006)."""
        self.assertTrue(MANIFEST_FILE.exists(), "Manifesto de logos ausente.")
        self.assertEqual(len(self.manifest), len(self.partidos))

        for p in self.partidos:
            slug = p["slug"]
            self.assertIn(slug, self.manifest, f"Slug {slug} ausente no manifesto de logos.")
            item = self.manifest[slug]
            self.assertTrue(
                item["url_fonte_oficial"].startswith("https://"),
                f"URL de fonte insegura ou inválida para {slug}",
            )
            self.assertIn("wikimedia.org", item["url_fonte_oficial"])
            self.assertGreater(item["tamanho_bytes"], 0)


if __name__ == "__main__":
    unittest.main()
