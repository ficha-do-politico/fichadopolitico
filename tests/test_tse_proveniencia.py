"""
Testes de proveniência do módulo TSE 2026 (P5).

Conforme docs/auditoria-dados-tse-2026.md (Achado A4 / Tarefa P5):
1. Todo registro de candidatura e patrimônio do TSE deve obrigatoriamente
   possuir URL oficial específica e data de coleta (coletado_em).
2. Links genéricos de topo de funil (como a home do DivulgaCand ou raiz do portal de dados abertos)
   são expressamente reprovados.
3. A verificação nos datasets em produção/site roda ativamente quando a suspensão temporária
   estiver desligada (tse_suspenso() == False).
"""

import json
import pathlib
import unittest
from datetime import date, datetime
from urllib.parse import urlparse

ROOT = pathlib.Path(__file__).resolve().parent.parent
CANON_PRESIDENCIA = ROOT / "dados" / "tse" / "presidencia.json"
SITE_PRESIDENCIA = ROOT / "site" / "src" / "data" / "presidencia.json"
CANON_CONGRESSO = ROOT / "dados" / "tse" / "congresso_2026.json"
SITE_CONGRESSO = ROOT / "site" / "src" / "data" / "congresso_2026.json"
SITE_TSE_STATUS = ROOT / "site" / "src" / "data" / "tse_status.json"
SITE_DEPUTADOS = ROOT / "site" / "src" / "data" / "deputados.json"
SITE_SENADORES = ROOT / "site" / "src" / "data" / "senadores.json"

GENERIC_TSE_URLS = {
    "https://divulgacandcontas.tse.jus.br",
    "https://divulgacandcontas.tse.jus.br/",
    "https://divulgacandcontas.tse.jus.br/divulga",
    "https://divulgacandcontas.tse.jus.br/divulga/",
    "https://divulgacandcontas.tse.jus.br/divulga/#",
    "https://divulgacandcontas.tse.jus.br/divulga/#/",
    "https://divulgacandcontas.tse.jus.br/divulga/#/home",
    "https://dadosabertos.tse.jus.br",
    "https://dadosabertos.tse.jus.br/",
    "https://dadosabertos.tse.jus.br/dataset",
    "https://dadosabertos.tse.jus.br/dataset/",
    "https://www.tse.jus.br",
    "https://www.tse.jus.br/",
}


def tse_suspenso() -> bool:
    """Verifica se o módulo TSE 2026 está em regime de suspensão paliativa."""
    if not SITE_TSE_STATUS.exists():
        return False
    with open(SITE_TSE_STATUS, encoding="utf-8") as f:
        return bool(json.load(f).get("suspenso", False))


def validar_url_tse_especifica(url: str) -> tuple[bool, str]:
    """Valida se a URL é HTTPS, pertence ao domínio oficial do TSE e aponta para recurso específico.

    Retorna (valido, motivo_se_invalido).
    """
    if not isinstance(url, str) or not url.strip():
        return False, "URL ausente ou vazia"

    url_limpa = url.strip()

    if not url_limpa.startswith("https://"):
        return False, f"URL deve utilizar HTTPS estrito: {url_limpa}"

    try:
        parsed = urlparse(url_limpa)
    except Exception as exc:
        return False, f"URL com formato inválido ({exc}): {url_limpa}"

    host = (parsed.hostname or "").lower()
    if not host.endswith("tse.jus.br"):
        return False, f"Domínio fora da infraestrutura oficial do TSE: {host}"

    url_normalizada = url_limpa.rstrip("/")
    if url_limpa in GENERIC_TSE_URLS or url_normalizada in GENERIC_TSE_URLS:
        return (
            False,
            f"URL genérica não permitida (deve apontar para candidato ou dataset específico): {url_limpa}",
        )

    # Rejeita URLs sem caminho substantivo além de '/' ou fragmento vazio
    caminho = parsed.path.strip("/")
    fragmento = parsed.fragment.strip("/")
    if not caminho and not fragmento:
        return False, f"URL sem caminho específico: {url_limpa}"

    if caminho == "divulga" and fragmento in ("", "#", "#/", "home"):
        return False, f"URL aponta para home do DivulgaCand: {url_limpa}"

    return True, ""


def validar_data_coleta(data_str: str) -> tuple[bool, str]:
    """Valida se a data de coleta está no formato ISO (YYYY-MM-DD ou YYYY-MM-DDTHH:MM:SS...).

    Retorna (valido, motivo_se_invalido).
    """
    if not isinstance(data_str, str) or not data_str.strip():
        return False, "Data de coleta ausente ou vazia"

    data_limpa = data_str.strip()
    # Suporte a YYYY-MM-DD ou ISO datetime completo
    try:
        if len(data_limpa) == 10:
            dt = date.fromisoformat(data_limpa)
            if dt.year < 2024:
                return False, f"Ano da data de coleta anterior a 2024: {data_limpa}"
            return True, ""
        dt_full = datetime.fromisoformat(data_limpa)
        if dt_full.year < 2024:
            return False, f"Ano da data de coleta anterior a 2024: {data_limpa}"
        return True, ""
    except ValueError as exc:
        return False, f"Data de coleta em formato inválido ({exc}): {data_limpa}"


def validar_registro_candidatura_tse(cand: dict, contexto: str) -> list[str]:
    """Valida proveniência de um registro de candidatura (url de perfil + data de coleta)."""
    erros = []
    # Aceita 'fonte_url', 'tsePerfilUrl' ou 'url_divulgacand'
    url = cand.get("fonte_url") or cand.get("tsePerfilUrl") or cand.get("url_divulgacand")
    if not url:
        erros.append(f"[{contexto}] Registro sem URL de fonte oficial do TSE")
    else:
        valido, motivo = validar_url_tse_especifica(url)
        if not valido:
            erros.append(f"[{contexto}] {motivo}")

    coletado_em = cand.get("coletado_em")
    valido_data, motivo_data = validar_data_coleta(coletado_em)
    if not valido_data:
        erros.append(f"[{contexto}] {motivo_data}")

    return erros


class TestValidadorRegrasProveniencia(unittest.TestCase):
    """Testes unitários do motor de validação de proveniência (executam sempre no CI)."""

    def test_reprova_urls_genericas_do_tse(self):
        urls_genericas = [
            "https://divulgacandcontas.tse.jus.br",
            "https://divulgacandcontas.tse.jus.br/",
            "https://divulgacandcontas.tse.jus.br/divulga/",
            "https://divulgacandcontas.tse.jus.br/divulga/#/",
            "https://divulgacandcontas.tse.jus.br/divulga/#/home",
            "https://dadosabertos.tse.jus.br",
            "https://dadosabertos.tse.jus.br/",
            "https://dadosabertos.tse.jus.br/dataset",
            "https://dadosabertos.tse.jus.br/dataset/",
            "https://www.tse.jus.br",
            "https://www.tse.jus.br/",
        ]
        for url in urls_genericas:
            valido, motivo = validar_url_tse_especifica(url)
            self.assertFalse(valido, f"URL genérica deveria ter sido reprovada: {url}")
            self.assertTrue(motivo, f"Mensagem de motivo esperada para: {url}")

    def test_reprova_urls_nao_https_ou_fora_do_tse(self):
        urls_invalidas = [
            "http://divulgacandcontas.tse.jus.br/divulga/#/candidato/2026/1",
            "https://exemplo.com/candidato/1",
            "https://noticias.uol.com.br/politica/candidatos",
            "",
            "   ",
        ]
        for url in urls_invalidas:
            valido, motivo = validar_url_tse_especifica(url)
            self.assertFalse(valido, f"URL deveria ser inválida: {url}")

    def test_aprova_urls_especificas_e_profundas_do_tse(self):
        urls_validas = [
            "https://divulgacandcontas.tse.jus.br/divulga/#/candidato/2026/2045202026/BR/12345",
            "https://divulgacandcontas.tse.jus.br/divulga/#/candidato/2022/2040602022/SP/280001618036",
            "https://dadosabertos.tse.jus.br/dataset/candidatos-2026",
            "https://cdn.tse.jus.br/estatistica/sead/odsele/consulta_cand/consulta_cand_2026.zip",
        ]
        for url in urls_validas:
            valido, motivo = validar_url_tse_especifica(url)
            self.assertTrue(valido, f"URL válida foi rejeitada indevidamente: {url} ({motivo})")

    def test_validacao_data_coleta(self):
        self.assertTrue(validar_data_coleta("2026-09-24")[0])
        self.assertTrue(validar_data_coleta("2026-09-24T10:30:00")[0])
        self.assertTrue(validar_data_coleta("2026-09-24T10:30:00Z")[0])

        self.assertFalse(validar_data_coleta("")[0])
        self.assertFalse(validar_data_coleta("24/09/2026")[0])
        self.assertFalse(validar_data_coleta("2020-01-01")[0])  # anterior a 2024
        self.assertFalse(validar_data_coleta("data_invalida")[0])

    def test_validar_registro_candidatura_completo(self):
        registro_valido = {
            "fonte_url": "https://divulgacandcontas.tse.jus.br/divulga/#/candidato/2026/2045202026/BR/1",
            "coletado_em": "2026-09-24",
        }
        self.assertEqual(validar_registro_candidatura_tse(registro_valido, "teste"), [])

        registro_invalido = {
            "tsePerfilUrl": "https://divulgacandcontas.tse.jus.br/",
            "coletado_em": "",
        }
        erros = validar_registro_candidatura_tse(registro_invalido, "candidato_x")
        self.assertGreaterEqual(len(erros), 2)


class TestTSEProvenienciaDatasets(unittest.TestCase):
    """Valida proveniência nos datasets reais quando a suspensão estiver desligada.

    Ao desativar a suspensão temporária do TSE 2026, nenhum registro poderá ser
    publicado sem cumprir os requisitos de rastreabilidade oficial.
    """

    def setUp(self):
        if tse_suspenso():
            self.skipTest(
                "Módulo TSE 2026 suspenso (docs/auditoria-dados-tse-2026.md). "
                "Teste de proveniência ativado sob término da suspensão."
            )

    def test_presidencia_dataset_proveniencia(self):
        """Valida que todos os candidatos presidenciais possuem URL específica e data de coleta."""
        self.assertTrue(SITE_PRESIDENCIA.exists())
        with open(SITE_PRESIDENCIA, encoding="utf-8") as f:
            candidatos = json.load(f)

        self.assertGreater(
            len(candidatos), 0, "Dataset de presidência vazio com suspensão desligada."
        )
        erros_totais = []
        for cand in candidatos:
            cid = cand.get("id", "desconhecido")
            erros_totais.extend(validar_registro_candidatura_tse(cand, f"Presidência {cid}"))

            for hist in cand.get("historicoPatrimonial", []):
                ano = hist.get("ano")
                url_bem = hist.get("tseUrl") or hist.get("fonte_url")
                if not url_bem:
                    erros_totais.append(
                        f"[Presidência {cid} - {ano}] Histórico sem URL oficial do TSE"
                    )
                else:
                    valido, motivo = validar_url_tse_especifica(url_bem)
                    if not valido:
                        erros_totais.append(f"[Presidência {cid} - {ano}] {motivo}")

        self.assertEqual(erros_totais, [], "Violações de proveniência encontradas na Presidência.")

    def test_congresso_2026_dataset_proveniencia(self):
        """Valida que todas as candidaturas do Congresso possuem URL específica e data de coleta."""
        self.assertTrue(SITE_CONGRESSO.exists())
        with open(SITE_CONGRESSO, encoding="utf-8") as f:
            congresso = json.load(f)

        self.assertGreater(
            len(congresso), 0, "Dataset do Congresso 2026 vazio com suspensão desligada."
        )
        erros_totais = []
        for pid, cand in congresso.items():
            erros_totais.extend(validar_registro_candidatura_tse(cand, f"Congressista {pid}"))

            pat = cand.get("patrimonio") or {}
            if pat:
                url_pat = pat.get("tse_url") or pat.get("fonte_url")
                if not url_pat:
                    erros_totais.append(f"[Congressista {pid} - Patrimônio] Sem URL oficial do TSE")
                else:
                    valido, motivo = validar_url_tse_especifica(url_pat)
                    if not valido:
                        erros_totais.append(f"[Congressista {pid} - Patrimônio] {motivo}")

        self.assertEqual(
            erros_totais, [], "Violações de proveniência encontradas no Congresso 2026."
        )

    def test_parlamentares_candidatura_2026_proveniencia(self):
        """Valida proveniência nas candidaturas publicadas em deputados.json e senadores.json."""
        erros_totais = []
        for path in (SITE_DEPUTADOS, SITE_SENADORES):
            self.assertTrue(path.exists())
            with open(path, encoding="utf-8") as f:
                parlamentares = json.load(f)

            for p in parlamentares:
                cand = p.get("candidatura_2026")
                if cand:
                    pid = p.get("id")
                    nome = p.get("nome", pid)
                    erros_totais.extend(
                        validar_registro_candidatura_tse(cand, f"Parlamentar {nome} ({pid})")
                    )

        self.assertEqual(
            erros_totais, [], "Violações de proveniência em candidaturas de parlamentares."
        )


if __name__ == "__main__":
    unittest.main()
