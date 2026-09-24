"""
Testes automatizados para o dataset de candidatos à Presidência e evolução patrimonial (TSE).

Conformidade e Regras:
  1. LGPD (AD-009): Proibição estrita de dados pessoais sensíveis (CPF, RG, endereço, email, telefone).
  2. Verificabilidade (AD-006 / AGENTS.md §3.1): Links oficiais HTTPS apontando para o TSE.
  3. Integridade e Consistência: Presença de todos os campos essenciais e histórico patrimonial válido.
"""

import json
import pathlib
import unicodedata
import unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent
CANON_PRESIDENCIA = ROOT / "dados" / "tse" / "presidencia.json"
SITE_PRESIDENCIA = ROOT / "site" / "src" / "data" / "presidencia.json"
CANON_CONGRESSO = ROOT / "dados" / "tse" / "congresso_2026.json"
SITE_CONGRESSO = ROOT / "site" / "src" / "data" / "congresso_2026.json"
SITE_TSE_STATUS = ROOT / "site" / "src" / "data" / "tse_status.json"
SITE_DEPUTADOS = ROOT / "site" / "src" / "data" / "deputados.json"
SITE_SENADORES = ROOT / "site" / "src" / "data" / "senadores.json"

PROHIBITED_LGPD_KEYS = {
    "cpf",
    "rg",
    "telefone",
    "celular",
    "email",
    "endereco",
    "titulo_eleitor",
    "nr_cpf_candidato",
    "num_titulo_eleitoral_candidato",
}


def tse_suspenso():
    with open(SITE_TSE_STATUS, encoding="utf-8") as f:
        return json.load(f)["suspenso"]


class TestTSESuspensao(unittest.TestCase):
    """Enquanto o módulo TSE 2026 estiver suspenso (docs/auditoria-dados-tse-2026.md),
    nenhum dado de candidatura ou patrimônio pode chegar ao site."""

    def setUp(self):
        self.assertTrue(
            SITE_TSE_STATUS.exists(), f"Status do módulo TSE ausente: {SITE_TSE_STATUS}"
        )
        if not tse_suspenso():
            self.skipTest("Módulo TSE 2026 ativo.")

    def test_status_aponta_auditoria(self):
        with open(SITE_TSE_STATUS, encoding="utf-8") as f:
            status = json.load(f)
        self.assertTrue(status["auditoria_url"].startswith("https://github.com/ficha-do-politico/"))

    def test_nenhum_candidato_presidencia_publicado(self):
        with open(SITE_PRESIDENCIA, encoding="utf-8") as f:
            self.assertEqual(json.load(f), [])

    def test_nenhuma_candidatura_congresso_publicada(self):
        with open(SITE_CONGRESSO, encoding="utf-8") as f:
            self.assertEqual(json.load(f), {})
        for path in (SITE_DEPUTADOS, SITE_SENADORES):
            with open(path, encoding="utf-8") as f:
                com_candidatura = [p["id"] for p in json.load(f) if p.get("candidatura_2026")]
            self.assertEqual(com_candidatura, [], f"Candidaturas publicadas em {path.name}")


class TestTSEPatrimonio(unittest.TestCase):
    def setUp(self):
        if tse_suspenso():
            self.skipTest("Módulo TSE 2026 suspenso (docs/auditoria-dados-tse-2026.md).")
        self.assertTrue(
            CANON_PRESIDENCIA.exists(), f"Arquivo canônico ausente: {CANON_PRESIDENCIA}"
        )
        self.assertTrue(
            SITE_PRESIDENCIA.exists(), f"Arquivo compilado do site ausente: {SITE_PRESIDENCIA}"
        )
        self.assertTrue(
            CANON_CONGRESSO.exists(), f"Arquivo canônico do congresso ausente: {CANON_CONGRESSO}"
        )
        self.assertTrue(
            SITE_CONGRESSO.exists(), f"Arquivo compilado do congresso ausente: {SITE_CONGRESSO}"
        )

        with open(CANON_PRESIDENCIA, encoding="utf-8") as f:
            self.canon_candidatos = json.load(f)

        with open(SITE_PRESIDENCIA, encoding="utf-8") as f:
            self.site_candidatos = json.load(f)

        with open(CANON_CONGRESSO, encoding="utf-8") as f:
            self.canon_congresso = json.load(f)

        with open(SITE_CONGRESSO, encoding="utf-8") as f:
            self.site_congresso = json.load(f)

    def test_conformidade_lgpd(self):
        """Garante que nenhum dado pessoal sensível (CPF, email, telefone) está presente no dataset."""
        for cand in self.site_candidatos:
            cand_keys = {k.lower() for k in cand.keys()}
            violacoes = cand_keys.intersection(PROHIBITED_LGPD_KEYS)
            self.assertEqual(
                violacoes,
                set(),
                f"Violação LGPD detectada no candidato {cand.get('id')}: chaves encontradas {violacoes}",
            )

    def test_verificabilidade_fontes_oficiais(self):
        """Garante que todo candidato e registro de bem aponta para o TSE com HTTPS."""
        for cand in self.site_candidatos:
            cid = cand.get("id")
            perfil_url = cand.get("tsePerfilUrl", "")
            self.assertTrue(
                perfil_url.startswith("https://divulgacandcontas.tse.jus.br"),
                f"Perfil do candidato {cid} sem URL segura oficial do TSE: {perfil_url}",
            )

            for hist in cand.get("historicoPatrimonial", []):
                ano = hist.get("ano")
                hist_url = hist.get("tseUrl", "")
                self.assertTrue(
                    hist_url.startswith("https://divulgacandcontas.tse.jus.br")
                    or hist_url.startswith("https://dadosabertos.tse.jus.br"),
                    f"Registro de {cid} ({ano}) sem URL oficial do TSE: {hist_url}",
                )

    def test_estrutura_e_campos_obrigatorios(self):
        """Valida que todos os candidatos possuem os campos obrigatórios."""
        campos_obrigatorios = [
            "id",
            "nomeUrna",
            "nomeCivil",
            "partido",
            "numeroUrna",
            "cargo",
            "fotoUrl",
            "tsePerfilUrl",
            "historicoPatrimonial",
        ]
        self.assertGreaterEqual(
            len(self.site_candidatos), 10, "Esperado ao menos 10 candidatos presidenciais."
        )

        for cand in self.site_candidatos:
            cid = cand.get("id")
            for campo in campos_obrigatorios:
                self.assertIn(campo, cand, f"Campo {campo} ausente no candidato {cid}")

            historico = cand["historicoPatrimonial"]
            self.assertGreaterEqual(
                len(historico), 1, f"Candidato {cid} deve ter ao menos 1 registro patrimonial."
            )

            # Valida ordenação cronológica do histórico
            anos = [h["ano"] for h in historico]
            self.assertEqual(
                anos,
                sorted(anos),
                f"Histórico patrimonial de {cid} não está em ordem cronológica: {anos}",
            )

            for h in historico:
                self.assertIsInstance(h["totalDeclarado"], (int, float))
                self.assertGreaterEqual(h["totalDeclarado"], 0)
                self.assertTrue(h["totalFormatado"].startswith("R$ "))
                for b in h.get("bens", []):
                    self.assertIn("tipo", b)
                    self.assertIn("descricao", b)
                    self.assertIn("valor", b)
                    self.assertGreaterEqual(b["valor"], 0)

    def test_ordenacao_alfabetica_candidatos_presidencia(self):
        """Garante que os candidatos à presidência estão ordenados alfabeticamente por nomeUrna."""

        def sort_key(c):
            norm = unicodedata.normalize("NFKD", c["nomeUrna"])
            return "".join(ch for ch in norm if not unicodedata.combining(ch)).lower()

        # Validar canônico
        nomes_canon = [c["nomeUrna"] for c in self.canon_candidatos]
        nomes_canon_esperados = [c["nomeUrna"] for c in sorted(self.canon_candidatos, key=sort_key)]
        self.assertEqual(
            nomes_canon,
            nomes_canon_esperados,
            f"Dataset canônico de presidência fora de ordem alfabética: {nomes_canon}",
        )

        # Validar dataset compilado do site
        nomes_site = [c["nomeUrna"] for c in self.site_candidatos]
        nomes_site_esperados = [c["nomeUrna"] for c in sorted(self.site_candidatos, key=sort_key)]
        self.assertEqual(
            nomes_site,
            nomes_site_esperados,
            f"Dataset compilado do site fora de ordem alfabética: {nomes_site}",
        )

    def test_congresso_2026_conformidade_lgpd(self):
        """Garante que nenhum dado sensível esteja presente no dataset do Congresso 2026."""
        self.assertGreaterEqual(
            len(self.site_congresso), 500, "Esperado ao menos 500 congressistas mapeados."
        )
        for pid, cand in self.site_congresso.items():
            cand_keys = {k.lower() for k in cand.keys()}
            violacoes = cand_keys.intersection(PROHIBITED_LGPD_KEYS)
            self.assertEqual(
                violacoes,
                set(),
                f"Violação LGPD detectada no congressista {pid}: {violacoes}",
            )

    def test_congresso_2026_verificabilidade(self):
        """Garante que todas as candidaturas do Congresso possuem links oficiais seguros do TSE."""
        for pid, cand in self.site_congresso.items():
            url_cand = cand.get("url_divulgacand", "")
            self.assertTrue(
                url_cand.startswith("https://divulgacandcontas.tse.jus.br"),
                f"Congressista {pid} sem URL segura oficial do TSE: {url_cand}",
            )
            patrimonio = cand.get("patrimonio", {})
            url_patrimonio = patrimonio.get("tse_url", "")
            self.assertTrue(
                url_patrimonio.startswith("https://divulgacandcontas.tse.jus.br"),
                f"Patrimônio do congressista {pid} sem URL segura oficial do TSE: {url_patrimonio}",
            )

    def test_congresso_2026_estrutura(self):
        """Valida que todos os congressistas possuem campos obrigatórios e patrimônio válido."""
        campos = [
            "parlamentar_id",
            "casa",
            "cargo",
            "reeleicao",
            "numero_urna",
            "partido",
            "uf",
            "situacao_registro",
            "url_divulgacand",
            "patrimonio",
        ]
        for pid, cand in self.site_congresso.items():
            for c in campos:
                self.assertIn(c, cand, f"Campo {c} ausente no congressista {pid}")

            self.assertIn(cand["casa"], ["camara", "senado"])
            self.assertIsInstance(cand["reeleicao"], bool)
            self.assertIn(cand["situacao_registro"], ["Deferido", "Aguardando julgamento"])

            pat = cand["patrimonio"]
            self.assertIsInstance(pat["total_declarado"], (int, float))
            self.assertGreaterEqual(pat["total_declarado"], 0)
            self.assertTrue(pat["total_formatado"].startswith("R$ "))
            self.assertEqual(pat["ano"], 2026)

            for b in pat.get("bens", []):
                self.assertIn("tipo", b)
                self.assertIn("descricao", b)
                self.assertIn("valor", b)
                self.assertGreaterEqual(b["valor"], 0)

    def test_fotos_presidencia_sem_waf_e_locais_existem(self):
        """Valida que fotos da presidência não dependem do WAF bloqueado do TSE e existem como arquivos locais."""
        for cand in self.site_candidatos:
            cid = cand.get("id")
            foto_url = cand.get("fotoUrl", "")
            self.assertNotIn(
                "divulgacandcontas.tse.jus.br",
                foto_url,
                f"Candidato {cid} com hotlink direto para endpoint protegido por WAF do TSE: {foto_url}",
            )
            if foto_url.startswith("fotos/"):
                arquivo_foto = ROOT / "site" / "public" / foto_url
                self.assertTrue(
                    arquivo_foto.exists(),
                    f"Arquivo local de foto referenciado por {cid} não encontrado: {arquivo_foto}",
                )
                self.assertGreater(
                    arquivo_foto.stat().st_size,
                    1000,
                    f"Arquivo de foto de {cid} corrompido ou vazio ({arquivo_foto.stat().st_size} bytes)",
                )


if __name__ == "__main__":
    unittest.main()
