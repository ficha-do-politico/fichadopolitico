"""
Testes automatizados do pipeline de compilação de dados (scripts/build_site_data.py).

Garante que:
  1. O script de build executa com sucesso sem exceções.
  2. Os datasets canônico e de frontend são gerados com integridade e sincronismo.
  3. A base canônica possui paridade de 513 deputados e todos os temas do catálogo mapeados.
"""

import json
import os
import pathlib
import subprocess
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent
BUILD_SCRIPT = ROOT / 'scripts' / 'build_site_data.py'
CATALOGO_FILE = ROOT / 'dados' / 'catalogo' / 'temas.json'
CAMARA_DEPUTADOS_FILE = ROOT / 'dados' / 'camara' / 'deputados.json'
SENADO_SENADORES_FILE = ROOT / 'dados' / 'senado' / 'senadores.json'
SITE_DEPUTADOS_FILE = ROOT / 'site' / 'src' / 'data' / 'deputados.json'
SITE_SENADORES_FILE = ROOT / 'site' / 'src' / 'data' / 'senadores.json'
SITE_TEMAS_FILE = ROOT / 'site' / 'src' / 'data' / 'temas.json'


class TestBuildPipeline(unittest.TestCase):

    def test_build_script_execution(self):
        """Executa scripts/build_site_data.py e assegura retorno exit code 0."""
        env = os.environ.copy()
        env["PYTHONIOENCODING"] = "utf-8"
        env["PYTHONUTF8"] = "1"

        result = subprocess.run(
            [sys.executable, str(BUILD_SCRIPT)],
            cwd=str(ROOT),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            env=env
        )
        self.assertEqual(
            result.returncode, 0,
            f"build_site_data.py falhou com código {result.returncode}.\nStderr: {result.stderr}\nStdout: {result.stdout}"
        )
        self.assertIn("Sucesso!", result.stdout)

    def test_pipeline_output_files_exist_and_match(self):
        """Verifica se os arquivos gerados existem e se há paridade entre Câmara/Senado e Site."""
        self.assertTrue(CAMARA_DEPUTADOS_FILE.exists())
        self.assertTrue(SENADO_SENADORES_FILE.exists())
        self.assertTrue(SITE_DEPUTADOS_FILE.exists())
        self.assertTrue(SITE_SENADORES_FILE.exists())
        self.assertTrue(SITE_TEMAS_FILE.exists())

        with open(CAMARA_DEPUTADOS_FILE, "r", encoding="utf-8") as f:
            camara_deps = json.load(f)

        with open(SITE_DEPUTADOS_FILE, "r", encoding="utf-8") as f:
            site_deps = json.load(f)

        with open(SENADO_SENADORES_FILE, "r", encoding="utf-8") as f:
            senado_sens = json.load(f)

        with open(SITE_SENADORES_FILE, "r", encoding="utf-8") as f:
            site_sens = json.load(f)

        with open(SITE_TEMAS_FILE, "r", encoding="utf-8") as f:
            site_temas = json.load(f)

        # Paridade exata de dados entre datasets canônicos e datasets consumidos pelo site
        self.assertEqual(len(camara_deps), 513)
        self.assertEqual(len(site_deps), 513)
        self.assertEqual(camara_deps, site_deps, "Dataset de site/src/data difere de dados/camara/deputados.json")

        self.assertEqual(len(senado_sens), 81)
        self.assertEqual(len(site_sens), 81)
        self.assertEqual(senado_sens, site_sens, "Dataset de site/src/data/senadores.json difere de dados/senado/senadores.json")

        # Verifica consistência dos temas compilados
        with open(CATALOGO_FILE, "r", encoding="utf-8") as f:
            catalogo_temas = json.load(f)
        self.assertEqual(site_temas, catalogo_temas, "site/src/data/temas.json difere do catálogo oficial")


if __name__ == "__main__":
    unittest.main()
