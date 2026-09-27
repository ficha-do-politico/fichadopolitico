"""
Testes automatizados de integridade, paridade bicameral e apartidarismo do Hemiciclo de Bancadas.

Alinhado a:
  - AD-004: Apartidarismo estrito — proibição de espectro ideológico ou rótulos subjetivos.
  - AD-006: Verificabilidade e integridade matemática com fontes oficiais.
  - AD-011 / AD-014: Paridade bicameral — 513 cadeiras na Câmara e 81 no Senado Federal.
  - docs/proposta-hemiciclo-parlamentar.md: Especificação do Hemiciclo e semi-donut.
"""

import json
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent
BANCADAS_FILE = ROOT / "site" / "src" / "data" / "bancadas.json"
CANON_DEPUTADOS_FILE = ROOT / "dados" / "camara" / "deputados.json"
CANON_SENADORES_FILE = ROOT / "dados" / "senado" / "senadores.json"


class TestHemicicloBancadas(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with open(BANCADAS_FILE, encoding="utf-8") as f:
            cls.bancadas_data = json.load(f)

        with open(CANON_DEPUTADOS_FILE, encoding="utf-8") as f:
            cls.deputados = json.load(f)

        with open(CANON_SENADORES_FILE, encoding="utf-8") as f:
            cls.senadores = json.load(f)

    def test_arquivo_existe_e_estrutura_valida(self):
        """Valida que bancadas.json existe e possui chaves para Câmara e Senado."""
        self.assertTrue(BANCADAS_FILE.exists())
        self.assertIn("camara", self.bancadas_data)
        self.assertIn("senado", self.bancadas_data)

    def test_integridade_camara_513_cadeiras(self):
        """Assegura paridade bicameral e fechamento exato em 513 deputados na Câmara."""
        camara = self.bancadas_data["camara"]
        self.assertEqual(camara["total_cadeiras"], 513)
        self.assertEqual(camara["maioria_absoluta"], 257)
        self.assertEqual(camara["maioria_simples"], 257)
        self.assertEqual(camara["maioria_qualificada_3_5"], 308)

        bancadas = camara["bancadas"]
        self.assertGreater(len(bancadas), 0)

        soma_cadeiras = sum(b["cadeiras"] for b in bancadas)
        self.assertEqual(
            soma_cadeiras, 513, "A soma das bancadas da Câmara deve ser exatamente 513"
        )

        soma_percentual = sum(b["percentual"] for b in bancadas)
        self.assertAlmostEqual(soma_percentual, 100.0, delta=0.5)

    def test_integridade_senado_81_cadeiras(self):
        """Assegura paridade bicameral e fechamento exato em 81 senadores no Senado."""
        senado = self.bancadas_data["senado"]
        self.assertEqual(senado["total_cadeiras"], 81)
        self.assertEqual(senado["maioria_absoluta"], 41)
        self.assertEqual(senado["maioria_simples"], 41)
        self.assertEqual(senado["maioria_qualificada_3_5"], 49)

        bancadas = senado["bancadas"]
        self.assertGreater(len(bancadas), 0)

        soma_cadeiras = sum(b["cadeiras"] for b in bancadas)
        self.assertEqual(soma_cadeiras, 81, "A soma das bancadas do Senado deve ser exatamente 81")

        soma_percentual = sum(b["percentual"] for b in bancadas)
        self.assertAlmostEqual(soma_percentual, 100.0, delta=0.5)

    def test_ordenacao_neutra_apartidaria(self):
        """Garante ordenação unicamente pelo tamanho de bancada (AD-004), sem espectro ideológico."""
        campos_proibidos = {
            "espectro",
            "ideologia",
            "rotulo",
            "posicao",
            "alinhamento",
            "ranking",
            "nota",
        }

        for casa_key in ("camara", "senado"):
            bancadas = self.bancadas_data[casa_key]["bancadas"]
            for i in range(len(bancadas) - 1):
                b_atual = bancadas[i]
                b_prox = bancadas[i + 1]

                # Nenhuma bancada pode conter atributos subjetivos
                chaves = set(b_atual.keys())
                self.assertFalse(
                    chaves & campos_proibidos,
                    f"Campo proibido por AD-004 encontrado na bancada {b_atual.get('sigla')}",
                )

                # Ordenação: maior bancada primeiro; desempate alfabético por sigla
                self.assertTrue(
                    b_atual["cadeiras"] > b_prox["cadeiras"]
                    or (
                        b_atual["cadeiras"] == b_prox["cadeiras"]
                        and b_atual["sigla"] <= b_prox["sigla"]
                    ),
                    f"Ordenação neutra violada entre {b_atual['sigla']} e {b_prox['sigla']}",
                )

    def test_correspondencia_com_dados_canonicos(self):
        """Valida que as contagens de bancadas batem precisamente com os parlamentares canônicos."""
        # Câmara
        contagem_canon_camara = {}
        for d in self.deputados:
            p = d.get("partido") or "S/Partido"
            contagem_canon_camara[p] = contagem_canon_camara.get(p, 0) + 1

        bancadas_camara_dict = {
            b["sigla"]: b["cadeiras"] for b in self.bancadas_data["camara"]["bancadas"]
        }
        self.assertEqual(contagem_canon_camara, bancadas_camara_dict)

        # Senado
        contagem_canon_senado = {}
        for s in self.senadores:
            p = s.get("partido") or "S/Partido"
            contagem_canon_senado[p] = contagem_canon_senado.get(p, 0) + 1

        bancadas_senado_dict = {
            b["sigla"]: b["cadeiras"] for b in self.bancadas_data["senado"]["bancadas"]
        }
        self.assertEqual(contagem_canon_senado, bancadas_senado_dict)


if __name__ == "__main__":
    unittest.main()
