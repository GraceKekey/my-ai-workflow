import json
import subprocess
import sys
import tempfile
import unittest
from decimal import Decimal
from pathlib import Path

from calculadora import calcular, converter_numero, formatar


RAIZ = Path(__file__).resolve().parents[1]


class TestCalculadora(unittest.TestCase):
    def test_soma(self):
        self.assertEqual(calcular("soma", "10", "5"), Decimal("15"))

    def test_subtracao_com_resultado_negativo(self):
        self.assertEqual(calcular("subtracao", "5", "10"), Decimal("-5"))

    def test_multiplicacao(self):
        self.assertEqual(calcular("multiplicacao", "-2.5", "4"), Decimal("-10"))

    def test_divisao(self):
        self.assertEqual(calcular("divisao", "10", "4"), Decimal("2.5"))

    def test_soma_decimal(self):
        self.assertEqual(calcular("soma", "0.1", "0.2"), Decimal("0.3"))

    def test_virgula_decimal(self):
        self.assertEqual(calcular("soma", "1,5", "2,25"), Decimal("3.75"))

    def test_divisao_periodica(self):
        self.assertEqual(
            calcular("divisao", "1", "3"), Decimal("0.3333333333333333333333333333")
        )

    def test_divisao_por_zero(self):
        for zero in ("0", "0.0", "-0"):
            with self.subTest(zero=zero), self.assertRaises(ZeroDivisionError):
                calcular("divisao", "10", zero)

    def test_operacao_invalida(self):
        with self.assertRaises(ValueError):
            calcular("potencia", "2", "3")

    def test_numero_invalido(self):
        with self.assertRaises(ValueError):
            calcular("soma", "abc", "2")

    def test_valores_nao_finitos(self):
        for valor in ("NaN", "Infinity", "-Infinity"):
            with self.subTest(valor=valor), self.assertRaises(ValueError):
                converter_numero(valor)

    def test_formatacao(self):
        exemplos = {"100": "100", "2.500": "2.5", "-0.00": "0", "0.0001": "0.0001"}
        for entrada, esperado in exemplos.items():
            with self.subTest(entrada=entrada):
                self.assertEqual(formatar(Decimal(entrada)), esperado)

    def test_cli_salva_resultado(self):
        with tempfile.TemporaryDirectory() as pasta:
            arquivo = Path(pasta) / "resultados" / "resultado.json"
            processo = subprocess.run(
                [sys.executable, str(RAIZ / "calculadora.py"), "soma", "10", "5",
                 "--output", str(arquivo)],
                capture_output=True, text=True, check=False,
            )
            self.assertEqual(processo.returncode, 0, processo.stderr)
            dados = json.loads(processo.stdout)
            self.assertEqual(dados["resultado"], "15")
            self.assertEqual(dados, json.loads(arquivo.read_text(encoding="utf-8")))

    def test_cli_rejeita_divisao_por_zero(self):
        processo = subprocess.run(
            [sys.executable, str(RAIZ / "calculadora.py"), "divisao", "10", "0"],
            capture_output=True, text=True, check=False,
        )
        self.assertEqual(processo.returncode, 2)
        self.assertIn("dividir por zero", processo.stderr)
        self.assertEqual(processo.stdout, "")

    def test_cli_aceita_virgula_com_numero_negativo(self):
        processo = subprocess.run(
            [sys.executable, str(RAIZ / "calculadora.py"), "--", "soma", "-1,5", "2"],
            capture_output=True, text=True, check=False,
        )
        self.assertEqual(processo.returncode, 0, processo.stderr)
        self.assertEqual(json.loads(processo.stdout)["resultado"], "0.5")


if __name__ == "__main__":
    unittest.main()
