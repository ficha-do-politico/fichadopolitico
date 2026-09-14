"""
Cliente HTTP resiliente para os pipelines de ingestão de dados públicos.
Implementa retries automáticos com backoff exponencial e tratamento de rate-limit (HTTP 429).
Alinhado à Fase 3 do Code Health (docs/code-health.md) e AD-014.
"""

import json
import logging
import time
import urllib.error
import urllib.request
from typing import Any

logger = logging.getLogger("http_client")

DEFAULT_HEADERS = {
    "User-Agent": "FichaDoPoliticoBot/1.0 (+https://github.com/ficha-do-politico)",
    "Accept": "application/json",
}


def fetch_json(
    url: str,
    headers: dict[str, str] | None = None,
    timeout: int = 25,
    max_retries: int = 3,
    backoff_factor: float = 2.0,
) -> Any:
    """
    Executa requisição GET HTTP(S) retornando payload JSON decodificado.
    Suporta retries automáticos em caso de HTTP 429, 500, 502, 503, 504 e ConnectionResetError.
    """
    req_headers = dict(DEFAULT_HEADERS)
    if headers:
        req_headers.update(headers)

    req = urllib.request.Request(url, headers=req_headers)
    last_error: Exception | None = None

    for attempt in range(1, max_retries + 1):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as response:
                data = response.read()
                charset = response.headers.get_content_charset() or "utf-8"
                text = data.decode(charset, errors="replace")
                return json.loads(text)
        except urllib.error.HTTPError as e:
            last_error = e
            # Trata Rate Limit (429) ou instabilidades temporárias do servidor (5xx)
            if e.code in (429, 500, 502, 503, 504) and attempt < max_retries:
                wait_time = backoff_factor**attempt
                retry_after = e.headers.get("Retry-After")
                if retry_after and retry_after.isdigit():
                    wait_time = max(wait_time, float(retry_after))
                logger.warning(
                    f"HTTP {e.code} ao acessar {url}. Tentativa {attempt}/{max_retries}. "
                    f"Aguardando {wait_time:.1f}s antes de tentar novamente..."
                )
                time.sleep(wait_time)
            else:
                raise
        except (urllib.error.URLError, TimeoutError, ConnectionResetError) as e:
            last_error = e
            if attempt < max_retries:
                wait_time = backoff_factor**attempt
                logger.warning(
                    f"Falha de conexão ({e}) ao acessar {url}. Tentativa {attempt}/{max_retries}. "
                    f"Aguardando {wait_time:.1f}s..."
                )
                time.sleep(wait_time)
            else:
                raise

    if last_error:
        raise last_error
    raise RuntimeError(f"Falha desconhecida ao requisitar {url}")
