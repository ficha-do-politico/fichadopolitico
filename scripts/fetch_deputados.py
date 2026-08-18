"""
Fetches deputy details from Câmara dos Deputados API and saves
individual markdown files in dados/deputados/.

Usage:
  python scripts/fetch_deputados.py           # first 10 (validation)
  python scripts/fetch_deputados.py --all     # all 513
  python scripts/fetch_deputados.py --limit 50 --delay 3
"""

import json
import pathlib
import sys
import time
import urllib.request
import urllib.error

ROOT = pathlib.Path(__file__).resolve().parent.parent
LIST_JSON = ROOT / 'discovery' / 'deputados_ordem_ASC_ordenarPor_nome.json'
OUT_DIR = ROOT / 'dados' / 'deputados'
DETAIL_URL = 'https://dadosabertos.camara.leg.br/api/v2/deputados/{}'


def fetch_json(url):
    req = urllib.request.Request(url, headers={'Accept': 'application/json'})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode('utf-8'))


def render_md(detail, basic):
    d = detail['dados']
    us = d.get('ultimoStatus') or {}
    g = us.get('gabinete') or {}

    nome_eleitoral = us.get('nomeEleitoral', d['nomeCivil'])

    redes = d.get('redeSocial') or []
    redes_md = ', '.join(redes) if redes else '—'

    foto_url = us.get('urlFoto', basic.get('urlFoto', ''))

    def row(label, value, source):
        v = str(value) if value else '—'
        return f'| {label} | {v} | {source} |'

    lines = [
        f'# Dep. {nome_eleitoral.title()}',
        '',
        f'![Foto]({foto_url})',
        '',
        '| Campo | Valor | Fonte |',
        '|---|---|---|',
        row('Nome civil', d.get('nomeCivil'), f'`GET /deputados/{d["id"]}`'),
        row('Nome eleitoral', nome_eleitoral, f'`GET /deputados/{d["id"]}`'),
        row('CPF', d.get('cpf'), f'`GET /deputados/{d["id"]}`'),
        row('Partido', basic.get('siglaPartido'), '`GET /deputados`'),
        row('UF', basic.get('siglaUf'), '`GET /deputados`'),
        row('Data de nascimento', d.get('dataNascimento'), f'`GET /deputados/{d["id"]}`'),
        row('Naturalidade',
            f'{d.get("municipioNascimento", "")} - {d.get("ufNascimento", "")}'.strip(' -'),
            f'`GET /deputados/{d["id"]}`'),
        row('Sexo', d.get('sexo'), f'`GET /deputados/{d["id"]}`'),
        row('Escolaridade', d.get('escolaridade'), f'`GET /deputados/{d["id"]}`'),
    ]
    situacao = us.get('situacao', '')
    condicao = us.get('condicaoEleitoral', '')
    situacao_str = f'{situacao} ({condicao})' if condicao else situacao

    gab_parts = []
    if g.get('predio'):
        gab_parts.append(f'Prédio {g["predio"]}')
    if g.get('sala'):
        gab_parts.append(f'Sala {g["sala"]}')
    if g.get('andar') is not None:
        gab_parts.append(f'Andar {g["andar"]}')
    gabinete_str = ', '.join(gab_parts) if gab_parts else '—'

    lines += [
        row('Situação', situacao_str or '—', f'`GET /deputados/{d["id"]}`'),
        row('Gabinete', gabinete_str, f'`GET /deputados/{d["id"]}`'),
        row('Telefone', g.get('telefone'), f'`GET /deputados/{d["id"]}`'),
        row('Email', g.get('email') or basic.get('email'), '`GET /deputados`'),
        row('Redes sociais', redes_md, f'`GET /deputados/{d["id"]}`'),
        '',
        '---',
        '',
        f'*Dados coletados em {time.strftime("%Y-%m-%d")} via [Dados Abertos - Câmara dos Deputados](https://dadosabertos.camara.leg.br/api/v2/)*',
        '',
    ]
    return '\n'.join(lines)


def main():
    limit = None
    delay = 5

    args = sys.argv[1:]
    i = 0
    while i < len(args):
        if args[i] == '--all':
            limit = None
        elif args[i] == '--limit' and i + 1 < len(args):
            limit = int(args[i + 1])
            i += 1
        elif args[i] == '--delay' and i + 1 < len(args):
            delay = float(args[i + 1])
            i += 1
        i += 1

    if limit is None and '--all' not in sys.argv:
        limit = 10

    deputies = json.loads(LIST_JSON.read_text(encoding='utf-8'))['dados']
    if limit:
        deputies = deputies[:limit]

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    total = len(deputies)
    print(f'Fetching {total} deputy details (delay={delay}s)...')

    for idx, d in enumerate(deputies, 1):
        did = d['id']
        nome = d['nome']
        out_path = OUT_DIR / f'{did}.md'

        try:
            detail = fetch_json(DETAIL_URL.format(did))
            md = render_md(detail, d)
            out_path.write_text(md, encoding='utf-8')
            print(f'  [{idx:3d}/{total}] {did} — {nome}')
        except urllib.error.HTTPError as e:
            print(f'  [{idx:3d}/{total}] {did} — ERRO HTTP {e.code}: {nome}', file=sys.stderr)
        except Exception as e:
            print(f'  [{idx:3d}/{total}] {did} — ERRO: {e} ({nome})', file=sys.stderr)

        if idx < total:
            time.sleep(delay)

    print(f'Done. Files saved to {OUT_DIR}')


if __name__ == '__main__':
    main()
