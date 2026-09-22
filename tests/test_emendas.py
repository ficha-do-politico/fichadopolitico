"""
Testes automatizados do módulo de Emendas Parlamentares Federais — CGU 2023–2026 (AD-016).
Valida:
  1. AD-006 (Verificabilidade): URLs oficiais HTTPS da CGU (Portal da Transparência).
  2. AD-009 (LGPD): Ausência estrita de dados privados/sensíveis (CPF, telefone, email, etc.).
  3. Integridade Matemática: Coerência de valores pagos, percentuais e soma das modalidades.
  4. Cobertura: Ampla representatividade de deputados e senadores da 57ª Legislatura.
"""

import json
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent
CANON_EMENDAS_FILE = ROOT / "dados" / "emendas" / "emendas_resumo.json"
SITE_DEPUTADOS_FILE = ROOT / "site" / "src" / "data" / "deputados.json"
SITE_SENADORES_FILE = ROOT / "site" / "src" / "data" / "senadores.json"


class TestEmendasParlamentares(unittest.TestCase):
    def setUp(self):
        self.assertTrue(
            CANON_EMENDAS_FILE.exists(),
            f"Dataset canônico de emendas ausente: {CANON_EMENDAS_FILE}",
        )
        self.assertTrue(
            SITE_DEPUTADOS_FILE.exists(),
            f"Dataset de deputados do site ausente: {SITE_DEPUTADOS_FILE}",
        )
        self.assertTrue(
            SITE_SENADORES_FILE.exists(),
            f"Dataset de senadores do site ausente: {SITE_SENADORES_FILE}",
        )

        with open(CANON_EMENDAS_FILE, encoding="utf-8") as f:
            self.emendas = json.load(f)

        with open(SITE_DEPUTADOS_FILE, encoding="utf-8") as f:
            self.deputados = json.load(f)

        with open(SITE_SENADORES_FILE, encoding="utf-8") as f:
            self.senadores = json.load(f)

    def test_cobertura_emendas(self):
        """Assegura cobertura de mais de 500 parlamentares federais na legislatura."""
        self.assertGreaterEqual(
            len(self.emendas),
            500,
            f"Esperado ao menos 500 parlamentares com emendas, obtido {len(self.emendas)}",
        )

    def test_conformidade_lgpd(self):
        """Valida que nenhum campo proibido por LGPD (AD-009) está exposto no dataset de emendas."""
        campos_proibidos = {
            "cpf",
            "email",
            "telefone",
            "redes",
            "rg",
            "endereco",
            "titulo_eleitor",
        }
        for pid, data in self.emendas.items():
            chaves = set(data.keys()).intersection(campos_proibidos)
            self.assertFalse(
                chaves,
                f"Violação LGPD detectada: chaves proibidas {chaves} no parlamentar {pid}",
            )

    def test_verificabilidade_cgu(self):
        """Garante que todo parlamentar possui link oficial HTTPS para o Portal da Transparência."""
        for pid, data in self.emendas.items():
            url = data.get("url_portal_transparencia", "")
            self.assertTrue(
                url.startswith("https://portaldatransparencia.gov.br/emendas/"),
                f"URL da CGU inválida para parlamentar {pid}: {url}",
            )

    def test_integridade_matematica_modalidades(self):
        """Verifica se a soma das modalidades bate com o total pago."""
        for pid, data in self.emendas.items():
            total_pago = data.get("total_pago", 0.0)
            modalidades = data.get("modalidades", {})
            pix = modalidades.get("especiais_pix", {}).get("total_pago", 0.0)
            finalidade = modalidades.get("finalidade_definida", {}).get("total_pago", 0.0)

            # Tolerância para arredondamentos de float
            soma_modalidades = round(pix + finalidade, 2)
            self.assertAlmostEqual(
                total_pago,
                soma_modalidades,
                delta=1.0,
                msg=f"Discrepância na soma de modalidades para parlamentar {pid}: total {total_pago} vs soma {soma_modalidades}",
            )

    def test_integracao_datasets_site(self):
        """Garante que a compilação do site inclui o nó de emendas nos parlamentares."""
        deps_com_emendas = [d for d in self.deputados if d.get("emendas")]
        sens_com_emendas = [s for s in self.senadores if s.get("emendas")]

        self.assertGreater(
            len(deps_com_emendas),
            450,
            f"Esperado mais de 450 deputados com nó de emendas no site, obtido {len(deps_com_emendas)}",
        )
        self.assertGreater(
            len(sens_com_emendas),
            60,
            f"Esperado mais de 60 senadores com nó de emendas no site, obtido {len(sens_com_emendas)}",
        )


if __name__ == "__main__":
    unittest.main()
