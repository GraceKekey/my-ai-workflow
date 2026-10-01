"""Calculadora de duas entradas, sem dependências externas."""

import argparse
import json
import operator
import sys
from decimal import Decimal, DecimalException, InvalidOperation, localcontext
from pathlib import Path


OPERACOES = {
    "soma": operator.add,
    "subtracao": operator.sub,
    "multiplicacao": operator.mul,
    "divisao": operator.truediv,
}


def converter_numero(valor: str) -> Decimal:
    """Aceita ponto ou vírgula decimal e rejeita valores não finitos."""
    try:
        numero = Decimal(valor.strip().replace(",", "."))
    except InvalidOperation as erro:
        raise ValueError("Informe um número válido.") from erro
    if not numero.is_finite():
        raise ValueError("Informe um número finito.")
    return numero


def calcular(operacao: str, a: str, b: str) -> Decimal:
    if operacao not in OPERACOES:
        raise ValueError("Operação inválida: use soma, subtracao, multiplicacao ou divisao.")
    numero_a = converter_numero(a)
    numero_b = converter_numero(b)
    if operacao == "divisao" and numero_b == 0:
        raise ZeroDivisionError("Não é possível dividir por zero.")
    with localcontext() as contexto:
        contexto.prec = 28
        return OPERACOES[operacao](numero_a, numero_b)


def formatar(numero: Decimal) -> str:
    if numero == 0:
        return "0"
    texto = format(numero, "f")
    return texto.rstrip("0").rstrip(".") if "." in texto else texto


def main() -> int:
    parser = argparse.ArgumentParser(description="Realiza um cálculo com dois números.")
    parser.add_argument("operacao", choices=OPERACOES)
    parser.add_argument("a", help="Primeiro número")
    parser.add_argument("b", help="Segundo número")
    parser.add_argument("--output", type=Path, help="Salva o resultado em um arquivo JSON")
    args = parser.parse_args()
    try:
        resultado = calcular(args.operacao, args.a, args.b)
        dados = {
            "operacao": args.operacao,
            "a": args.a,
            "b": args.b,
            "resultado": formatar(resultado),
        }
        texto = json.dumps(dados, ensure_ascii=False, indent=2)
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(texto + "\n", encoding="utf-8")
    except (ValueError, ZeroDivisionError, DecimalException, OSError) as erro:
        print(f"Erro: {erro}", file=sys.stderr)
        return 2
    print(texto)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
