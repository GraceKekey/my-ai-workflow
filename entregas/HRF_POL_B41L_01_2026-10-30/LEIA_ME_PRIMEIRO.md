# HRF-POL-B41L-01 — distribuição v0.1.1

**[M/D] Código implementado e pré-registrado. Rodada científica completa NÃO EXECUTADA.**

B41L é uma dependência congelada em `dependencias/HRF_B41L_B1_Lancamento_Limpo/`, com os43 hashes originais verificados. Nenhuma linha dela foi alterada. O código novo fica em `src/`, o notebook em `HRF_POL_B41L_01_Colab.ipynb`. O ZIP original de fontes e o ZIP original de resultados também estão incluídos.

Foram lidos integralmente os capítulos0.1v0.2 e2v1.5 enviados nesta conversa. O trabalho investiga W (propagação e polarização), não geometria holográfica G, dicionário D ou origem de um fóton físico. São cochains U(1) no limite quadrático do Hamiltoniano Wilson original, malha3D periódica Whitney e evolução real. Jones apenas prepara as condições iniciais e fornece a referência externa.

**Resultado técnico atual:** testes originais B41L e testes novos passaram. A fumaça revisada tem6casos concluídos. Em V1, G2/preparação passou; em C+ e H, G3 falhou por resíduo do ajuste temporal acima de0.05. G4/G6 permanecem PENDING. O controle nulo se manteve nulo. Não se afirma sucesso de transporte completo de polarização.

**Lacuna de proveniência:** o POL-01 original nos pacotes HRF_3_Bancadas.zip / HRF_3_Execucoes.zip não foi fornecido. G1/P01–P05 permanece PENDING; o novo controle Jones tem diagnóstico próprio e não recebe o selo do protocolo antigo. G7 não pode PASS com essa dependência pendente. Nenhum resultado negativo foi descartado.

## Uso no Colab

1. Abra o notebook. Monte Drive se desejar; a distribuição pode ser enviada manualmente.
2. Rode as células na ordem: conferência de hashes, dependências, testes, controle convencional e fumaça.
3. Revise os gates e o pré-registro. A célula11 contém `CONFIRMO_COMPLETA=False` por padrão. Ela só roda a família científica se você mudar explicitamente para True no Colab.
4. Os checkpoints ficam no Drive quando montado. Reexecutar a mesma versão retoma os casos interrompidos e verifica os selos dos concluídos. Não editar código/configuração mantendo a mesma pasta de saída.
5. No fim, o notebook cria ZIP, testa CRC e salva cópia no Drive; download no navegador fica opcional para evitar travamento com arquivos grandes.

## Comandos locais técnicos

A partir da raiz extraída:

```bash
python -m pip install -r requirements.txt
python -I scripts/verificar_manifesto.py
python -I scripts/pol.py verify
python -I scripts/pol.py plan --perfil completo --output plano
python -I scripts/pol.py test --output testes_novos
python -I scripts/pol.py controls --output controle_Jones_novo.json
python -I scripts/pol.py run --perfil fumaca --output fumaca_nova --executar
python -I scripts/pol.py evaluate --perfil fumaca --output fumaca_nova
python -I scripts/pol.py figures --input fumaca_nova --output figuras_novas
```

`plan` nunca integra, inclusive se receber `--executar`. `run` sem `--executar` só planeja. A completa também verifica confirmação explícita e ambiente Colab. `--caso ID` seleciona um caso para admissão separada quando não há espaço para a família inteira. Scripts Linux/Windows encaminham os mesmos argumentos, mas a referência de execução verificada é Linux/Colab; Windows não foi executado aqui.

## Arquivos importantes

- `PREREGISTRO_HRF_POL_B41L_01.md` e `configs/`: hipóteses, estados, sementes, critérios e recursos congelados.
- `RELATORIO_MODELO.md`: mapa de campos, integrador original e limites do método de extração.
- `RELATORIO_EXECUCAO.md`: somente testes/fumaça realmente executados e tabela científica futura NOT_EXECUTED.
- `EMENDA_PREEXECUCAO_01.md`: correções técnicas, preservando a primeira fumaça e os critérios.
- `resultados/fumaca_v0_1_1/`: nova fumaça; `resultados/fumaca/`: primeira versão preservada, não substituída.
- `resultados/figuras_fumaca_v0_1_1/`: gráficos e relatório gerados dos dados reais.
- `auditoria/`: fontes lidas, versões, logs, hashes e revisão prévia.

Não iniciar pela completa. O FAIL de qualidade da extração na malha de fumaça deve ser investigado por uma revisão explicitamente identificada, não pela alteração silenciosa das tolerâncias. O notebook completo está implementado para execução futura controlada, sem certificação científica antecipada.
