"""
Testes automatizados de integridade de dados e conformidade (MVP v0).
Valida:
  1. AD-006 (Verificabilidade): Todas as votações e proposições possuem URLs oficiais válidas.
  2. AD-009 (LGPD): Nenhum dado sensível (CPF, email, telefone) está presente no dataset público.
  3. Cobertura da Câmara: 513 deputados federais mapeados com integridade referencial de votos.
"""

import json
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent
CATALOGO_FILE = ROOT / "dados" / "catalogo" / "temas.json"
CAMARA_DEPUTADOS_FILE = ROOT / "dados" / "camara" / "deputados.json"
CAMARA_VOTACOES_DIR = ROOT / "dados" / "camara" / "votacoes"
SENADO_SENADORES_FILE = ROOT / "dados" / "senado" / "senadores.json"
SITE_DEPUTADOS_FILE = ROOT / "site" / "src" / "data" / "deputados.json"
SITE_SENADORES_FILE = ROOT / "site" / "src" / "data" / "senadores.json"
SITE_TEMAS_FILE = ROOT / "site" / "src" / "data" / "temas.json"


class TestDataIntegrity(unittest.TestCase):
    def setUp(self):
        self.assertTrue(CATALOGO_FILE.exists(), f"Catálogo ausente: {CATALOGO_FILE}")
        self.assertTrue(
            CAMARA_DEPUTADOS_FILE.exists(), f"Dataset da Câmara ausente: {CAMARA_DEPUTADOS_FILE}"
        )
        self.assertTrue(
            SENADO_SENADORES_FILE.exists(), f"Dataset do Senado ausente: {SENADO_SENADORES_FILE}"
        )
        self.assertTrue(
            SITE_DEPUTADOS_FILE.exists(), f"Dataset do site ausente: {SITE_DEPUTADOS_FILE}"
        )
        self.assertTrue(
            SITE_SENADORES_FILE.exists(),
            f"Dataset de senadores do site ausente: {SITE_SENADORES_FILE}",
        )
        self.assertTrue(SITE_TEMAS_FILE.exists(), f"Temas do site ausente: {SITE_TEMAS_FILE}")

        with open(CATALOGO_FILE, encoding="utf-8") as f:
            self.temas = json.load(f)

        with open(CAMARA_DEPUTADOS_FILE, encoding="utf-8") as f:
            self.deputados = json.load(f)

        with open(SENADO_SENADORES_FILE, encoding="utf-8") as f:
            self.senadores = json.load(f)

    def test_catalogo_temas_estrutura_e_verificabilidade(self):
        """Verifica se o catálogo de temas atende aos requisitos de verificabilidade (AD-006)."""
        self.assertGreaterEqual(len(self.temas), 4, "MVP deve ter no mínimo 4 temas curados.")

        ids_vistos = set()
        for t in self.temas:
            t_id = t.get("id")
            self.assertTrue(t_id, "Tema sem ID oficial.")
            self.assertNotIn(t_id, ids_vistos, f"ID duplicado no catálogo: {t_id}")
            ids_vistos.add(t_id)

            self.assertTrue(t.get("titulo"), f"Tema {t_id} sem título.")
            self.assertTrue(t.get("proposicao"), f"Tema {t_id} sem identificador de proposição.")

            # Links oficiais obrigatórios com HTTPS
            url_votacao = t.get("url_votacao", "")
            url_proposicao = t.get("url_proposicao", "")
            self.assertTrue(
                url_votacao.startswith("https://dadosabertos.camara.leg.br/"),
                f"Tema {t_id} com url_votacao inválida: {url_votacao}",
            )
            self.assertTrue(
                url_proposicao.startswith("https://"),
                f"Tema {t_id} com url_proposicao inválida: {url_proposicao}",
            )

            # Arquivo da votação deve existir no disco
            votacao_file = CAMARA_VOTACOES_DIR / f"{t_id}.json"
            self.assertTrue(
                votacao_file.exists(), f"Arquivo de votação não encontrado para tema {t_id}"
            )

    def test_deputados_cobertura_57a_legislatura(self):
        """Verifica a cobertura dos 513 parlamentares da Câmara dos Deputados."""
        self.assertEqual(
            len(self.deputados), 513, "O dataset deve conter exatamente 513 deputados federais."
        )

        dep_ids = set()
        for d in self.deputados:
            did = d.get("id")
            self.assertIsInstance(did, int, f"ID de deputado deve ser inteiro: {did}")
            self.assertNotIn(did, dep_ids, f"ID de deputado duplicado: {did}")
            dep_ids.add(did)

            self.assertTrue(d.get("nome_eleitoral"), f"Deputado {did} sem nome eleitoral.")
            self.assertTrue(d.get("partido"), f"Deputado {did} sem sigla do partido.")
            self.assertTrue(d.get("uf"), f"Deputado {did} sem UF.")
            self.assertTrue(
                d.get("url_foto", "").startswith("https://"),
                f"Deputado {did} sem URL de foto válida.",
            )
            self.assertTrue(
                d.get("url_perfil_camara", "").startswith("https://www.camara.leg.br/deputados/"),
                f"Deputado {did} sem link oficial da Câmara.",
            )

    def test_senadores_cobertura_57a_legislatura(self):
        """Verifica a cobertura dos 81 senadores da República em exercício (AD-014)."""
        self.assertEqual(len(self.senadores), 81, "O dataset deve conter exatamente 81 senadores.")

        sen_ids = set()
        for s in self.senadores:
            sid = s.get("id")
            self.assertIsInstance(sid, int, f"ID de senador deve ser inteiro: {sid}")
            self.assertNotIn(sid, sen_ids, f"ID de senador duplicado: {sid}")
            sen_ids.add(sid)

            self.assertTrue(s.get("nome_eleitoral"), f"Senador {sid} sem nome eleitoral.")
            self.assertTrue(s.get("partido"), f"Senador {sid} sem sigla do partido.")
            self.assertTrue(s.get("uf"), f"Senador {sid} sem UF.")
            self.assertTrue(
                s.get("url_foto", "").startswith("https://"),
                f"Senador {sid} sem URL de foto válida.",
            )
            self.assertTrue(
                s.get("url_perfil_senado", "").startswith("https://"),
                f"Senador {sid} sem link oficial do Senado.",
            )

    def test_lgpd_compliance(self):
        """Garante que dados sensíveis (AD-009 / LGPD) nunca existam nos datasets públicos."""
        campos_sensiveis = {"cpf", "email", "telefone", "redes", "redeSocial"}

        # Valida deputados (canônico e site)
        for d in self.deputados:
            for campo in campos_sensiveis:
                self.assertNotIn(
                    campo,
                    d,
                    f"Violação de LGPD detectada: campo '{campo}' no deputado {d.get('id')}",
                )

        with open(SITE_DEPUTADOS_FILE, encoding="utf-8") as f:
            site_deputados = json.load(f)

        for d in site_deputados:
            for campo in campos_sensiveis:
                self.assertNotIn(
                    campo,
                    d,
                    f"Violação de LGPD no site/src/data: campo '{campo}' no deputado {d.get('id')}",
                )

        # Valida senadores (canônico e site)
        for s in self.senadores:
            for campo in campos_sensiveis:
                self.assertNotIn(
                    campo,
                    s,
                    f"Violação de LGPD detectada: campo '{campo}' no senador {s.get('id')}",
                )

        with open(SITE_SENADORES_FILE, encoding="utf-8") as f:
            site_senadores = json.load(f)

        for s in site_senadores:
            for campo in campos_sensiveis:
                self.assertNotIn(
                    campo,
                    s,
                    f"Violação de LGPD no site/src/data: campo '{campo}' no senador {s.get('id')}",
                )

    def test_integridade_votos_nominais(self):
        """Garante que todo deputado possui voto mapeado para cada tema do catálogo."""
        tema_ids = [t["id"] for t in self.temas]
        votos_permitidos = {
            "Sim",
            "Não",
            "Abstenção",
            "Obstrução",
            "Artigo 17",
            "Não votou / Ausente",
        }

        for d in self.deputados:
            votos = d.get("votos", {})
            for tid in tema_ids:
                self.assertIn(tid, votos, f"Deputado {d.get('id')} sem registro para tema {tid}")
                tipo_voto = votos[tid]
                self.assertIn(
                    tipo_voto,
                    votos_permitidos,
                    f"Deputado {d.get('id')} com voto com tipo desconhecido '{tipo_voto}' no tema {tid}",
                )


if __name__ == "__main__":
    unittest.main()
