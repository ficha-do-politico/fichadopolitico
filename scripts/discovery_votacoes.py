"""
Script de Discovery: Votações Nominais da Câmara dos Deputados
Ficha do Político - MVP v0

Investiga e documenta o fluxo de dados:
Proposição -> Votações -> Votação de Mérito no Plenário -> Votos Nominais por Deputado.

Uso:
  python scripts/discovery_votacoes.py --demo
  python scripts/discovery_votacoes.py --tipo PEC --numero 45 --ano 2019
  python scripts/discovery_votacoes.py --votacao 2196833-326
"""

import argparse
import json
import os
import pathlib
import sys
import time
import urllib.parse
import urllib.request
import urllib.error

ROOT = pathlib.Path(__file__).resolve().parent.parent
DEPUTADOS_DIR = ROOT / 'dados' / 'deputados'
OUT_DIR = ROOT / 'dados' / 'votacoes'

API_BASE = 'https://dadosabertos.camara.leg.br/api/v2'
USER_AGENT = 'FichaDoPoliticoBot/0.1 (github.com/ficha-do-politico)'


def fetch_json(url: str, retries: int = 3, delay: float = 1.0) -> dict:
    """Faz requisição GET na API de Dados Abertos com retentativas e headers adequados."""
    req = urllib.request.Request(
        url,
        headers={
            'Accept': 'application/json',
            'User-Agent': USER_AGENT,
        }
    )
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                return json.loads(resp.read().decode('utf-8'))
        except urllib.error.HTTPError as e:
            if e.code == 429:
                wait = (attempt + 1) * 3
                print(f"  [Aviso] Rate limit (429). Aguardando {wait}s...", file=sys.stderr)
                time.sleep(wait)
            elif e.code >= 500 and attempt < retries - 1:
                time.sleep(2)
            else:
                raise
        except Exception:
            if attempt < retries - 1:
                time.sleep(2)
            else:
                raise
    raise RuntimeError(f"Falha ao consultar {url}")


def buscar_proposicao(tipo: str, numero: int, ano: int) -> dict:
    """Localiza o ID oficial e metadados de uma proposição."""
    url = f"{API_BASE}/proposicoes?siglaTipo={urllib.parse.quote(tipo)}&numero={numero}&ano={ano}"
    res = fetch_json(url)
    dados = res.get('dados', [])
    if not dados:
        raise ValueError(f"Proposição {tipo} {numero}/{ano} não encontrada na API.")
    return dados[0]


def listar_votacoes_proposicao(proposicao_id: int) -> list:
    """Lista todas as votações registradas para uma proposição."""
    url = f"{API_BASE}/proposicoes/{proposicao_id}/votacoes"
    res = fetch_json(url)
    return res.get('dados', [])


def detalhar_votacao(votacao_id: str) -> dict:
    """Obtém os detalhes e metadados de uma votação."""
    url = f"{API_BASE}/votacoes/{votacao_id}"
    res = fetch_json(url)
    return res.get('dados', {})


def obter_orientacoes(votacao_id: str) -> list:
    """Obtém orientações partidárias de uma votação."""
    url = f"{API_BASE}/votacoes/{votacao_id}/orientacoes"
    try:
        res = fetch_json(url)
        return res.get('dados', [])
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return []
        raise


def obter_votos_nominais(votacao_id: str) -> list:
    """Obtém os votos nominais registrados dos deputados."""
    url = f"{API_BASE}/votacoes/{votacao_id}/votos"
    res = fetch_json(url)
    return res.get('dados', [])


def filtrar_votacoes_plenario_merito(votacoes: list) -> list:
    """
    Heurística para identificar votações de mérito no Plenário:
    1. Órgão deve ser 'PLEN'.
    2. Exclui requerimentos de adiamento, retirada de pauta, encerramento de discussão ou urgência.
    3. Exclui redação final se houver votação de substitutivo/turno anterior.
    4. Prioriza votações de 1º e 2º turnos (em PECs) ou aprovação de Substitutivo / Parecer de Mérito (em PLs/MPVs).
    """
    candidatas = []
    for v in votacoes:
        sigla = v.get('siglaOrgao', '')
        desc = v.get('descricao', '')
        desc_lower = desc.lower()

        if sigla != 'PLEN':
            continue

        # Ignora requerimentos puramente procedimentais
        if any(termo in desc_lower for termo in [
            'requerimento de adiamento',
            'requerimento de retirada de pauta',
            'requerimento de encerramento',
            'requerimento de quebra de interstício',
            'urgência (art. 155',
        ]):
            continue

        # Verifica se é votação de mérito ou turno
        is_turno = any(t in desc_lower for t in ['primeiro turno', '1º turno', '1o turno', 'segundo turno', '2º turno', '2o turno'])
        is_merito = any(m in desc_lower for m in ['substitutivo', 'subemenda substitutiva', 'projeto de lei de conversão', 'parecer da comissão', 'aprovada a proposta de emenda'])
        is_destaque_chave = 'mantido o texto' in desc_lower or 'suprimido o texto' in desc_lower

        if is_turno or is_merito or is_destaque_chave:
            candidatas.append(v)

    return candidatas


def carregar_ids_deputados_locais() -> set:
    """Carrega os IDs dos deputados já mapeados no diretório dados/deputados."""
    if not DEPUTADOS_DIR.exists():
        return set()
    ids = set()
    for f in DEPUTADOS_DIR.glob('*.md'):
        try:
            ids.add(int(f.stem))
        except ValueError:
            pass
    return ids


def analisar_votos(votacao_id: str, salvar_artefato: bool = True) -> dict:
    """Analisa e sumariza os votos nominais de uma votação."""
    detalhes = detalhar_votacao(votacao_id)
    votos = obter_votos_nominais(votacao_id)
    orientacoes = obter_orientacoes(votacao_id)
    deputados_conhecidos = carregar_ids_deputados_locais()

    # Contagem de tipos de voto
    contagem_tipos = {}
    deputados_votaram = set()
    votos_map = {}

    for v in votos:
        tv = v.get('tipoVoto')
        contagem_tipos[tv] = contagem_tipos.get(tv, 0) + 1
        dep = v.get('deputado_', {})
        dep_id = dep.get('id')
        if dep_id:
            deputados_votaram.add(dep_id)
            votos_map[dep_id] = {
                'nome': dep.get('nome'),
                'partido': dep.get('siglaPartido'),
                'uf': dep.get('siglaUf'),
                'tipoVoto': tv,
                'dataRegistro': v.get('dataRegistroVoto'),
            }

    # Deputados ausentes / não votantes
    ausentes = []
    if deputados_conhecidos:
        for dep_id in sorted(deputados_conhecidos - deputados_votaram):
            ausentes.append(dep_id)

    resumo = {
        'votacao_id': votacao_id,
        'dataHora': detalhes.get('dataHoraRegistro') or detalhes.get('data'),
        'descricao': detalhes.get('descricao'),
        'siglaOrgao': detalhes.get('siglaOrgao'),
        'uri_api': f"{API_BASE}/votacoes/{votacao_id}",
        'url_portal_votacao': f"https://dadosabertos.camara.leg.br/api/v2/votacoes/{votacao_id}",
        'total_votos_registrados': len(votos),
        'total_deputados_locais': len(deputados_conhecidos),
        'total_ausentes_nao_votantes': len(ausentes),
        'distribuicao_votos': contagem_tipos,
        'total_orientacoes': len(orientacoes),
        'orientacoes': [
            {
                'bancada': o.get('siglaPartidoBloco'),
                'orientacao': o.get('orientacaoVoto'),
            }
            for o in orientacoes
        ],
        'amostra_votos': list(votos_map.values())[:5],
    }

    if salvar_artefato:
        OUT_DIR.mkdir(parents=True, exist_ok=True)
        out_file = OUT_DIR / f"{votacao_id}.json"
        with open(out_file, 'w', encoding='utf-8') as f:
            json.dump({
                'metadados': resumo,
                'votos': votos_map,
                'ausentes_ids': ausentes,
            }, f, indent=2, ensure_ascii=False)
        print(f"  [Salvo] Artefato de votação salvo em: {out_file.relative_to(ROOT)}")

    return resumo


def executar_demo():
    """Executa demonstração com votações históricas de relevância do MVP v0."""
    print("=" * 70)
    print("DEMO: Discovery de Votações Nominais da Câmara dos Deputados (MVP v0)")
    print("=" * 70)

    temas = [
        {
            'nome': 'Reforma Tributária (1º Turno)',
            'tipo': 'PEC',
            'numero': 45,
            'ano': 2019,
            'votacao_id': '2196833-326',
        },
        {
            'nome': 'Reforma Tributária (2º Turno)',
            'tipo': 'PEC',
            'numero': 45,
            'ano': 2019,
            'votacao_id': '2196833-373',
        },
        {
            'nome': 'Marco Temporal das Terras Indígenas',
            'tipo': 'PL',
            'numero': 490,
            'ano': 2007,
            'votacao_id': '345311-270',
        },
        {
            'nome': 'PEC da Anistia aos Partidos (2º Turno)',
            'tipo': 'PEC',
            'numero': 9,
            'ano': 2023,
            'votacao_id': '2352476-168',
        },
        {
            'nome': 'Taxação de Compras Internacionais / Mover',
            'tipo': 'PL',
            'numero': 914,
            'ano': 2024,
            'votacao_id': '2422697-75',
        },
    ]

    for t in temas:
        print(f"\n--- {t['nome']} ({t['tipo']} {t['numero']}/{t['ano']}) ---")
        analise = analisar_votos(t['votacao_id'], salvar_artefato=True)
        print(f"  Votação ID: {analise['votacao_id']}")
        print(f"  Data/Hora: {analise['dataHora']}")
        print(f"  Descrição: {analise['descricao'][:100]}...")
        print(f"  Distribuição de votos: {analise['distribuicao_votos']}")
        print(f"  Votos nominais registrados: {analise['total_votos_registrados']}")
        print(f"  Deputados sem registro (ausentes/não votou): {analise['total_ausentes_nao_votantes']}")
        print("  Orientações de bancada:")
        for o in analise['orientacoes'][:4]:
            print(f"    - {o['bancada']}: {o['orientacao']}")


def main():
    parser = argparse.ArgumentParser(description="Discovery de Votações Nominais da Câmara")
    parser.add_argument('--demo', action='store_true', help="Executa análise das votações de temas-chave do MVP")
    parser.add_argument('--tipo', type=str, help="Tipo da proposição (ex: PEC, PL, PLP, MPV)")
    parser.add_argument('--numero', type=int, help="Número da proposição")
    parser.add_argument('--ano', type=int, help="Ano da proposição")
    parser.add_argument('--votacao', type=str, help="ID da votação para inspecionar votos")

    args = parser.parse_args()

    if args.demo:
        executar_demo()
        return

    if args.votacao:
        analisar_votos(args.votacao, salvar_artefato=True)
        return

    if args.tipo and args.numero and args.ano:
        prop = buscar_proposicao(args.tipo, args.numero, args.ano)
        p_id = prop['id']
        print(f"Proposição encontrada: {args.tipo} {args.numero}/{args.ano} (ID: {p_id})")
        print(f"Ementa: {prop.get('ementa')}")
        vots = listar_votacoes_proposicao(p_id)
        print(f"Total de votações: {len(vots)}")
        merito = filtrar_votacoes_plenario_merito(vots)
        print(f"Votações de mérito/turno no Plenário ({len(merito)}):")
        for v in merito:
            print(f"  [{v['id']}] {v.get('dataHoraRegistro') or v.get('data')}: {v.get('descricao')}")
        return

    parser.print_help()


if __name__ == '__main__':
    main()
