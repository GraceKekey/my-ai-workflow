# C5B Earth Constraint Battery / QW03

Bateria exploratória com parâmetros comuns para A–K. Sucesso numérico não confirma a C5B nem prova estabilidade física.

## Reprodução

A partir da raiz do repositório:

```bash
python -m pip install -r C5B_Earth_Constraint_Battery/requirements.txt
python C5B_Earth_Constraint_Battery/run_all.py
```

O runner reproduz os 18 valores publicados no relatório QW02, executa controles automatizados, percorre as dez etapas sequencialmente, valida e cria gráficos PNG/PDF, relatório e ZIP. Qualquer falha de regressão bloqueia os testes novos. `01_*.py` até `10_*.py` permitem executar etapas separadas respeitando a ordem salva em `results/stage_progress.json`.

## Fontes preservadas

- `../c5b_qo/study.py`: densidade PREM exata do QW01, conferida por SHA256. O ZIP inclui esse arquivo para reprodução isolada.
- `data/C5B_QO_QW02_Open_Closed_Cavity_Local.md`: relatório recebido, preservado integralmente e conferido por SHA256.
- Os CSVs originais QW02 e documentos teóricos adicionais não foram enviados. A regressão utiliza os números explícitos do relatório, sem fabricar CSVs antigos.

`parameters.json` centraliza constantes, grades, normalização, cenários e a previsão C5B-Earth-01 fixada antes da comparação com dados-alvo. Nenhum dado-alvo foi ajustado; nenhum limite observacional é atribuído a uma sensibilidade hipotética.

## Artefatos

- `tables/full_grid.csv`: todos os parâmetros e resultados por caso.
- `tables/01_*` a `tables/summary_by_test.csv`: confronto e sensibilidades de cada teste.
- `results/validation.json`, `test_results.json`, `regression_QW02.json`: verificações.
- `results/10_dynamic_symbolic.json`: Einstein e Bianchi; não é uma evolução dinâmica.
- `results/C5B-Earth-01_prediction.json`: previsão condicional, não confirmação.
- `plots/`: 12 figuras, PNG e PDF.
- `C5B_QO_QW03_Earth_Constraint_Battery.md`: relatório em 21 seções.
- `../C5B_QO_QW03_Earth_Constraint_Battery.zip`: entrega completa, com CRC e manifesto SHA256 verificados.

## Limites físicos

A composição de métrica/densidade é prescrita e exige stresses adicionais e suporte de cavidade. Proxies de modos/Slichter não são frequências elásticas PREM. Vácuo não transmite PKIKP diretamente. Fontes externas não puderam ser consultadas; não há likelihood ou covariância observacional independente no pacote. O limite conjunto quantitativo ainda não foi demonstrado.
