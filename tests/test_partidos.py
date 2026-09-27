"""
Testes automatizados de integridade, verificabilidade e apartidarismo do Guia de Partidos.
Alinhado a:
  - AGENTS.md §3.1: Proibição estrita de dados sintéticos ou adjetivação subjetiva.
  - AD-004: Apartidarismo e ausência de scores/rótulos ideológicos.
  - AD-006: Verificabilidade com link direto para o portal oficial do TSE.
  - AD-011 / AD-014: Paridade bicameral e integridade matemática de bancadas.
"""

import json
import pathlib
import re
import unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent
TSE_PARTIDOS_FILE = ROOT / "dados" / "tse" / "partidos.json"
SITE_PARTIDOS_FILE = ROOT / "site" / "src" / "data" / "partidos.json"
CANON_DEPUTADOS_FILE = ROOT / "dados" / "camara" / "deputados.json"
CANON_SENADORES_FILE = ROOT / "dados" / "senado" / "senadores.json"


class TestGuiaPartidos(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with open(TSE_PARTIDOS_FILE, encoding="utf-8") as f:
            cls.tse_partidos = json.load(f)

        with open(SITE_PARTIDOS_FILE, encoding="utf-8") as f:
            cls.site_partidos = json.load(f)

        with open(CANON_DEPUTADOS_FILE, encoding="utf-8") as f:
            cls.deputados = json.load(f)

        with open(CANON_SENADORES_FILE, encoding="utf-8") as f:
            cls.senadores = json.load(f)

    def test_arquivos_existem_e_contem_30_partidos(self):
        """Verifica se os datasets canônico e do site existem e cobrem os 30 partidos registrados no TSE."""
        self.assertTrue(TSE_PARTIDOS_FILE.exists())
        self.assertTrue(SITE_PARTIDOS_FILE.exists())
        self.assertEqual(len(self.tse_partidos), 30)
        self.assertEqual(len(self.site_partidos), 30)

    def test_verificabilidade_oficial_tse(self):
        """Assegura que todo partido tem fonte oficial no TSE e metadados cadastrais válidos (AD-006)."""
        data_regex = re.compile(r"^\d{2}/\d{2}/\d{4}$")
        for p in self.site_partidos:
            sigla = p.get("sigla")
            self.assertTrue(sigla, "Partido sem sigla definida.")
            self.assertTrue(p.get("nome"), f"Partido {sigla} sem nome oficial.")

            nr = p.get("numero_eleitoral")
            self.assertIsInstance(nr, int, f"Partido {sigla} com número eleitoral inválido.")
            self.assertTrue(
                10 <= nr <= 90, f"Partido {sigla} com número fora do intervalo 10-90: {nr}"
            )

            deferimento = p.get("deferimento", "")
            self.assertTrue(
                data_regex.match(deferimento),
                f"Partido {sigla} com data de deferimento inválida: {deferimento}",
            )

            fonte = p.get("fonte_oficial_tse", "")
            self.assertTrue(
                fonte.startswith("https://www.tse.jus.br"),
                f"Partido {sigla} com URL oficial do TSE inválida: {fonte}",
            )
            self.assertTrue(
                p.get("presidente_nacional"), f"Partido {sigla} sem presidente registrado."
            )

    def test_apartidarismo_e_neutralidade_estrita(self):
        """Garante a ausência de scores, notas ou rótulos subjetivos atribuídos pela plataforma (AD-004)."""
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
        for p in self.site_partidos:
            sigla = p.get("sigla")
            intersecao = set(p.keys()).intersection(campos_proibidos)
            self.assertEqual(
                len(intersecao),
                0,
                f"Violação AD-004: chaves de score/rótulo encontradas no partido {sigla}: {intersecao}",
            )

            # Autodeclaração estatutária deve citar artigo de abertura de documento oficial
            auto = p.get("autodeclaracao", {})
            self.assertTrue(
                auto.get("artigo"), f"Partido {sigla} sem citação de artigo estatutário."
            )
            self.assertTrue(auto.get("texto"), f"Partido {sigla} sem texto estatutário literal.")
            self.assertIn("Estatuto", auto.get("artigo"))

    def test_integridade_matematica_bancadas(self):
        """Valida que a soma das bancadas partidárias fecha exatamente com 513 deputados e 81 senadores."""
        total_deps = sum(p["bancada"]["deputados"] for p in self.site_partidos)
        total_sens = sum(p["bancada"]["senadores"] for p in self.site_partidos)

        # 513 deputados federais na Câmara
        self.assertEqual(total_deps, 513)

        # 80 senadores filiados + 1 senador sem partido (Romário) = 81
        sens_sem_partido = sum(1 for s in self.senadores if s.get("partido") == "S/Partido")
        self.assertEqual(sens_sem_partido, 1)
        self.assertEqual(total_sens + sens_sem_partido, 81)

        # Percentual de ocupação do Congresso Nacional
        for p in self.site_partidos:
            b = p["bancada"]
            self.assertEqual(b["total_congresso"], b["deputados"] + b["senadores"])
            pct_esperado = round((b["total_congresso"] / 594.0) * 100, 2)
            self.assertAlmostEqual(b["percentual_congresso"], pct_esperado, places=2)

    def test_integridade_recursos_publicos(self):
        """Garante consistência matemática entre despesas de cota, emendas e dados individuais."""
        total_ceap_deps = sum(
            d.get("despesas_2026", {}).get("total_gasto", 0.0) if d.get("despesas_2026") else 0.0
            for d in self.deputados
        )
        total_ceap_partidos = sum(p["recursos"]["ceap_camara_2026"] for p in self.site_partidos)
        self.assertAlmostEqual(total_ceap_deps, total_ceap_partidos, places=2)

        total_ceaps_sens = sum(
            s.get("despesas_2026", {}).get("total_gasto", 0.0) if s.get("despesas_2026") else 0.0
            for s in self.senadores
        )
        sens_sem_partido_ceaps = sum(
            s.get("despesas_2026", {}).get("total_gasto", 0.0)
            if s.get("despesas_2026") and s.get("partido") == "S/Partido"
            else 0.0
            for s in self.senadores
        )
        total_ceaps_partidos = sum(p["recursos"]["ceaps_senado_2026"] for p in self.site_partidos)
        self.assertAlmostEqual(
            total_ceaps_sens, total_ceaps_partidos + sens_sem_partido_ceaps, places=2
        )

        for p in self.site_partidos:
            r = p["recursos"]
            self.assertGreaterEqual(r["ceap_camara_2026"], 0)
            self.assertGreaterEqual(r["ceaps_senado_2026"], 0)
            self.assertGreaterEqual(r["emendas_cgu_pagas"], 0)
            self.assertAlmostEqual(
                r["total_cota_2026"],
                r["ceap_camara_2026"] + r["ceaps_senado_2026"],
                places=2,
            )

    def test_fidelidade_e_votacoes_curadas(self):
        """Verifica a integridade das distribuições de votos nominais e das taxas de adesão."""
        for p in self.site_partidos:
            sigla = p["sigla"]
            dep_count = p["bancada"]["deputados"]

            camara_votacoes = p["votacoes"]["camara"]["temas"]
            self.assertEqual(len(camara_votacoes), 10)

            for v in camara_votacoes:
                dist = v["distribuicao_votos"]
                soma_votos = (
                    dist["sim"] + dist["nao"] + dist["abstencao"] + dist["ausente"] + dist["outro"]
                )
                self.assertEqual(
                    soma_votos,
                    dep_count,
                    f"Soma de votos no tema {v['tema_id']} diverge da bancada do partido {sigla}",
                )

                adesao = v["taxa_adesao_orientacao"]
                if adesao is not None:
                    self.assertTrue(
                        0.0 <= adesao <= 100.0,
                        f"Taxa de adesão inválida no partido {sigla}: {adesao}",
                    )

            media_adesao = p["coesao"]["media_adesao_orientacao"]
            if media_adesao is not None:
                self.assertTrue(0.0 <= media_adesao <= 100.0)


if __name__ == "__main__":
    unittest.main()
