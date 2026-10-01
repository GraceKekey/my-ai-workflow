# Cálculos simples

Calculadora em Python para soma, subtração, multiplicação e divisão. Não precisa
instalar bibliotecas. Aceita ponto ou vírgula decimal e calcula com precisão de
28 dígitos significativos. Entradas inválidas e divisão por zero geram uma
mensagem de erro.

## Executar no GitHub

1. Abra a aba **Actions** deste repositório.
2. Selecione **Cálculos simples** e clique em **Run workflow**.
3. Escolha a operação, informe os dois números e confirme em **Run workflow**.
4. Ao terminar, abra a execução para ver o resultado no passo **Calcular**.
   O arquivo `resultado.json` também fica disponível no artefato
   **resultado-calculo**.

Cada execução testa todas as operações antes de calcular. Publicações na branch
`main` executam os testes e o exemplo `10 + 5 = 15` automaticamente.

## Executar com Python

Use Python 3.10 ou superior:

```sh
python calculadora.py soma 10 5
python calculadora.py subtracao 10 5
python calculadora.py multiplicacao 10 5
python calculadora.py divisao 10 5
python calculadora.py soma 0,1 0,2 --output resultado.json
python calculadora.py -- soma -1,5 2
```

Use `--` antes da operação ao informar números negativos com vírgula pela linha
de comando. No GitHub Actions, basta preencher os números normalmente.

Exemplo de resultado:

```json
{
  "operacao": "soma",
  "a": "10",
  "b": "5",
  "resultado": "15"
}
```

## Testes

```sh
python -m unittest discover -s tests -v
```

Os testes verificam as quatro operações, números negativos, casas decimais,
entradas inválidas, divisão por zero e a geração do arquivo de resultado.
