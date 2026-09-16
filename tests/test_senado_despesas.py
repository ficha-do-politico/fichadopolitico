"""
Testes automatizados do módulo de Gastos Parlamentares — CEAPS 2026 (Senado Federal).
Valida:
  1. AD-006 (Verificabilidade): URLs oficiais da transparência no Senado.
  2. AD-009 (LGPD): Descarte total de dados sensíveis e mascaramento de CPFs de prestadores.
  3. Integridade Matemática: Coerência dos totais e somatório das fatias por categoria.
  4. Cobertura: Ao menos 75 dos 81 senadores da República com despesas na CEAPS 2026.
"""

import json
import pathlib
import re
import unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent
CANON_DESPESAS_SENADO = ROOT / "dados" / "senado" / "despesas_2026.json"
SITE_DESPESAS_SENADO = ROOT / "site" / "src" / "data" / "despesas_senado_2026.json"
SITE_SENADORES_FILE = ROOT / "site" / "src" / "data" / "senadores.json"


class TestSenadoDespesas(unittest.TestCase):
    def setUp(self):
        self.assertTrue(
            CANON_DESPESAS_SENADO.exists(),
            f"Dataset canônico de despesas do Senado ausente: {CANON_DESPESAS_SENADO}",
        )
        self.assertTrue(
            SITE_DESPESAS_SENADO.exists(),
            f"Dataset de despesas do Senado no site ausente: {SITE_DESPESAS_SENADO}",
        )
        self.assertTrue(
            SITE_SENADORES_FILE.exists(),
            f"Dataset de senadores do site ausente: {SITE_SENADORES_FILE}",
        )

        with open(CANON_DESPESAS_SENADO, encoding="utf-8") as f:
            self.despesas = json.load(f)

        with open(SITE_SENADORES_FILE, encoding="utf-8") as f:
            self.senadores = json.load(f)

    def test_cobertura_senadores_ceaps(self):
        """Assegura cobertura de despesas para a ampla maioria dos senadores em 2026."""
        self.assertGreaterEqual(
            len(self.despesas),
            75,
            f"Esperado ao menos 75 senadores com despesas na CEAPS 2026, obtido {len(self.despesas)}",
        )

    def test_estrutura_e_verificabilidade_despesas_senado(self):
        """Valida que todas as despesas possuem URLs oficiais do Senado e campos íntegros."""
        for sen_id, desp in self.despesas.items():
            self.assertEqual(desp.get("ano"), 2026, f"Ano inválido para senador {sen_id}")
            self.assertGreater(
                desp.get("total_gasto", 0),
                0,
                f"Total gasto deve ser positivo para senador {sen_id}",
            )
            self.assertTrue(
                desp.get("total_formatado", "").startswith("R$"),
                f"Formatação monetária incorreta no senador {sen_id}",
            )
            self.assertTrue(
                desp.get("fonte_oficial", "").startswith(
                    "https://www6g.senado.leg.br/transparencia/sen/"
                ),
                f"Fonte oficial inválida no senador {sen_id}: {desp.get('fonte_oficial')}",
            )

            # Valida categorias
            categorias = desp.get("categorias", [])
            self.assertGreater(len(categorias), 0, f"Sem categorias no senador {sen_id}")
            soma_pct = sum(c.get("percentual", 0) for c in categorias)
            self.assertTrue(
                98.0 <= soma_pct <= 102.0,
                f"Soma dos percentuais de categorias inconsistente ({soma_pct}%) no senador {sen_id}",
            )

            # Valida maiores despesas
            maiores = desp.get("maiores_despesas", [])
            self.assertLessEqual(len(maiores), 5, f"Mais de 5 maiores despesas no senador {sen_id}")
            for m in maiores:
                self.assertTrue(m.get("fornecedor"), f"Despesa sem fornecedor no senador {sen_id}")
                self.assertGreater(m.get("valor", 0), 0, f"Despesa zerada no senador {sen_id}")

    def test_conformidade_lgpd_estrita_senado(self):
        """Assegura conformidade com AD-009 (LGPD): ausência de dados pessoais sensíveis."""
        campos_proibidos = {"cpf", "email", "telefone", "endereco", "rg"}

        for sen_id, desp in self.despesas.items():
            chaves = set(desp.keys()).intersection(campos_proibidos)
            self.assertEqual(
                chaves,
                set(),
                f"Chaves proibidas por LGPD encontradas em despesas do senador {sen_id}: {chaves}",
            )

            for m in desp.get("maiores_despesas", []):
                cnpj_cpf = m.get("cnpj_cpf", "")
                apenas_nums = re.sub(r"\D", "", cnpj_cpf)
                # Se for CPF de 11 dígitos, não pode estar em texto puro
                if len(apenas_nums) == 11 and not (
                    cnpj_cpf.startswith("***.") or "***" in cnpj_cpf
                ):
                    self.fail(f"CPF de prestador não mascarado no senador {sen_id}: {cnpj_cpf}")

    def test_integracao_site_senadores(self):
        """Verifica se os senadores compilados para o site contêm o campo despesas_2026."""
        sens_com_despesa = [s for s in self.senadores if s.get("despesas_2026")]
        self.assertGreaterEqual(
            len(sens_com_despesa),
            75,
            f"Esperado ao menos 75 senadores com despesas_2026 no site, obtido {len(sens_com_despesa)}",
        )


if __name__ == "__main__":
    unittest.main()
