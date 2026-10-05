"""
Testes de data de coleta (P6 de docs/auditoria-dados-tse-2026.md).

Despesas de exercício corrente (CEAP/CEAPS) e emendas (CGU) são snapshots de bases
que mudam continuamente. Todo registro por parlamentar deve carregar `coletado_em`
real (ISO, não futura) para a ficha distinguir o snapshot da consulta em tempo real.
"""

import json
import pathlib
import unittest
from datetime import date

from test_tse_proveniencia import validar_data_coleta

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATASETS = {
    "CEAP Câmara": ROOT / "dados" / "camara" / "despesas_2026.json",
    "CEAPS Senado": ROOT / "dados" / "senado" / "despesas_2026.json",
    "Emendas CGU": ROOT / "dados" / "emendas" / "emendas_resumo.json",
}


class TestDataColetaDatasets(unittest.TestCase):
    def test_todo_registro_possui_data_coleta_valida(self):
        hoje = date.today()
        for nome, caminho in DATASETS.items():
            with self.subTest(dataset=nome):
                with open(caminho, encoding="utf-8") as f:
                    registros = json.load(f)
                self.assertGreater(len(registros), 0, f"{nome} vazio.")

                erros = []
                for pid, reg in registros.items():
                    coletado_em = reg.get("coletado_em")
                    valido, motivo = validar_data_coleta(coletado_em)
                    if not valido:
                        erros.append(f"{pid}: {motivo}")
                    elif date.fromisoformat(coletado_em[:10]) > hoje:
                        erros.append(f"{pid}: data de coleta futura {coletado_em}")
                self.assertEqual(erros, [], f"{nome}: {erros[:5]}")


if __name__ == "__main__":
    unittest.main()
