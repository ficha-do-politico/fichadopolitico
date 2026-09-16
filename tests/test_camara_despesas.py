"""
Testes automatizados do módulo de Gastos Parlamentares — CEAP 2026 (Câmara dos Deputados).
Valida:
  1. AD-006 (Verificabilidade): URLs oficiais HTTPS de notas fiscais e comprovantes na Câmara.
  2. AD-009 (LGPD): Descarte total de CPF de parlamentares e mascaramento de CPFs de prestadores.
  3. Integridade Matemática: Coerência dos totais e somatório das fatias por categoria.
  4. Cobertura: Mais de 500 deputados federais mapeados na cota parlamentar de 2026.
"""

import json
import pathlib
import re
import unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent
CANON_DESPESAS_FILE = ROOT / "dados" / "camara" / "despesas_2026.json"
SITE_DESPESAS_FILE = ROOT / "site" / "src" / "data" / "despesas_camara_2026.json"
SITE_DEPUTADOS_FILE = ROOT / "site" / "src" / "data" / "deputados.json"


class TestCamaraDespesas(unittest.TestCase):
    def setUp(self):
        self.assertTrue(
            CANON_DESPESAS_FILE.exists(),
            f"Dataset canônico de despesas ausente: {CANON_DESPESAS_FILE}",
        )
        self.assertTrue(
            SITE_DESPESAS_FILE.exists(),
            f"Dataset de despesas do site ausente: {SITE_DESPESAS_FILE}",
        )
        self.assertTrue(
            SITE_DEPUTADOS_FILE.exists(),
            f"Dataset de deputados do site ausente: {SITE_DEPUTADOS_FILE}",
        )

        with open(CANON_DESPESAS_FILE, encoding="utf-8") as f:
            self.despesas = json.load(f)

        with open(SITE_DEPUTADOS_FILE, encoding="utf-8") as f:
            self.deputados = json.load(f)

    def test_cobertura_deputados_ceap(self):
        """Assegura cobertura de despesas para mais de 500 deputados federais em 2026."""
        self.assertGreaterEqual(
            len(self.despesas),
            500,
            f"Esperado ao menos 500 deputados com despesas na CEAP 2026, obtido {len(self.despesas)}",
        )

    def test_estrutura_e_verificabilidade_despesas(self):
        """Valida que todas as despesas possuem URLs oficiais da Câmara e campos íntegros."""
        for dep_id, desp in self.despesas.items():
            self.assertEqual(desp.get("ano"), 2026, f"Ano inválido para deputado {dep_id}")
            self.assertGreater(
                desp.get("total_gasto", 0),
                0,
                f"Total gasto deve ser positivo para deputado {dep_id}",
            )
            self.assertTrue(
                desp.get("total_formatado", "").startswith("R$"),
                f"Formatação monetária incorreta no deputado {dep_id}",
            )
            self.assertTrue(
                desp.get("fonte_oficial", "").startswith("https://www.camara.leg.br/deputados/"),
                f"Fonte oficial inválida no deputado {dep_id}",
            )

            # Valida categorias
            categorias = desp.get("categorias", [])
            self.assertGreater(len(categorias), 0, f"Sem categorias no deputado {dep_id}")
            soma_pct = sum(c.get("percentual", 0) for c in categorias)
            self.assertTrue(
                98.0 <= soma_pct <= 102.0,
                f"Soma dos percentuais de categorias inconsistente ({soma_pct}%) no dep {dep_id}",
            )

            # Valida maiores despesas e links de comprovantes
            maiores = desp.get("maiores_despesas", [])
            self.assertLessEqual(len(maiores), 5, f"Mais de 5 maiores despesas no dep {dep_id}")
            for m in maiores:
                self.assertTrue(m.get("fornecedor"), f"Despesa sem fornecedor no dep {dep_id}")
                self.assertGreater(m.get("valor", 0), 0, f"Despesa zerada no dep {dep_id}")
                url_doc = m.get("url_documento")
                if url_doc:
                    self.assertTrue(
                        url_doc.startswith("https://www.camara.leg.br/cota-parlamentar/"),
                        f"URL de nota fiscal não oficial ou insegura no dep {dep_id}: {url_doc}",
                    )

    def test_conformidade_lgpd_estrita(self):
        """Assegura conformidade com AD-009 (LGPD): ausência de CPFs expostos."""
        campos_proibidos = {"cpf", "email", "telefone", "endereco", "rg"}

        for dep_id, desp in self.despesas.items():
            chaves = set(desp.keys()).intersection(campos_proibidos)
            self.assertEqual(
                chaves,
                set(),
                f"Chaves proibidas por LGPD encontradas em despesas do dep {dep_id}: {chaves}",
            )

            for m in desp.get("maiores_despesas", []):
                cnpj_cpf = m.get("cnpj_cpf", "")
                # Se for CPF (11 dígitos numéricos), deve estar mascarado
                apenas_nums = re.sub(r"\D", "", cnpj_cpf)
                if len(apenas_nums) == 11:
                    self.assertTrue(
                        cnpj_cpf.startswith("***."),
                        f"CPF de prestador não mascarado no dep {dep_id}: {cnpj_cpf}",
                    )

    def test_integracao_site_deputados(self):
        """Verifica se os deputados compilados para o site contêm o campo despesas_2026."""
        deps_com_despesa = [d for d in self.deputados if d.get("despesas_2026")]
        self.assertGreaterEqual(
            len(deps_com_despesa),
            500,
            f"Esperado ao menos 500 deputados com despesas_2026 no site, obtido {len(deps_com_despesa)}",
        )

        # Validação específica de paridade oficial para Adilson Barroso (ID: 221328)
        adilson = next((d for d in self.deputados if d["id"] == 221328), None)
        self.assertIsNotNone(adilson, "Deputado Adilson Barroso não encontrado.")
        self.assertIsNotNone(adilson.get("despesas_2026"), "Adilson Barroso sem despesas_2026.")
        self.assertAlmostEqual(
            adilson["despesas_2026"]["total_gasto"],
            296927.14,
            places=2,
            msg="Total de CEAP de Adilson Barroso difere do oficial da Câmara.",
        )


if __name__ == "__main__":
    unittest.main()
