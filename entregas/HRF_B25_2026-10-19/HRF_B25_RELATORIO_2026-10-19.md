# HRF B25 — relatório da rodada completa

## Resultado do avaliador congelado [M]

- B25-R, R1 (cone único): **BIRREFRINGÊNCIA FRACA**.
- B25-R, R2 (luz × saltos): **INDEFINIDO**.
- B25-Q: **EMERGE**.
- B25-T: **exploratório**, sem decisão confirmatória pré-registrada.

Essas são as saídas literais do avaliador fornecido, sem ajuste de critérios após os resultados. São resultados de toy model [M], não demonstração de geometria física universal, de um elétron ou de um fóton individual.

## Execução, integridade e cobertura [D/M]

Comando: `python -I src/rodar_B25.py completo`, seguido de `python -I src/avaliar_B25.py resultados`.
Foram concluídas 40 amostras principais de R, 10 controles N-Poisson, 15 amostras exploratórias de dose, 9 casos Q mais 2 controles sem sinal, e 5 pacotes T.
Cobertura e os 10 hashes originais: ver `resultados/CONFERENCIA_COBERTURA.json` (passou: True). Nenhum arquivo científico pré-registrado foi editado. Dados em `fumaca/` e o teste sintético são separados dos resultados completos.
Início/fim do orquestrador, no fuso America/Sao_Paulo: 2026-10-19 17:37:28 / 2026-10-19 18:18:56. Tempo medido: 2488.5 s.
Python 3.12.14, NumPy 2.2.6, SciPy 1.15.3; quota de 4 CPUs, 32 GiB e 4 threads BLAS. Os tempos podem diferir da estimativa original. Resultados gravados apenas neste ambiente; sem publicação no GitHub.

## B25-R — controles e medidas

- V1_stokes_e_d1: `True`.
- V2_whitney_exato: `True`.
- V3_residuo_cg: `True`.
- V4_invariancia_afim: `True`.
- V5_N_Poisson: `True`.
- V6_iso_nulo: `True`.

Em n=24, IC 95% t de Student (média [inferior; superior]):

- P em F-ani: 0.0034909821 [0.00237942; 0.0046025442].
- P em F-iso: 0.00021807942 [-0.00047305122; 0.00090921007].
- G em F-ani: 1.0273382 [1.0205677; 1.0341086].
- G em F-iso: 0.99061098 [0.98255678; 0.99866518].
- η_L em F-ani: 1.1364178 [1.1337297; 1.139106].
- η_H em F-ani: 1.106253 [1.0992345; 1.1132714].

Leitura dos limiares: R1 usa o IC de P e a magnitude da média para distinguir cone único, birrefringência fraca e os demais ramos. R2 exige que o IC de G fique todo dentro de [0,97;1,03] para UMA GEOMETRIA, ou todo fora de [0,95;1,05] para DUAS GEOMETRIAS. Um IC que indique desvio de G=1 pode continuar INDEFINIDO por esses limiares pré-registrados; significância estatística não substitui a regra de decisão.

Os IC 99% dos controles, as inclinações entre tamanhos, o índice geral de Plebanski, as 19 direções e a dose exploratória permanecem nos JSON/CSV. As figuras não redefinem os gates. Se algum controle invalidar a decisão, o rótulo INCONCLUSIVO deve ser respeitado; tendências brutas não o substituem.

## B25-Q — anéis de baixa energia

| Spin | Triângulo λ=0,05 | Quadrilátero | δJ | Ordem triângulo | Ordem δJ |
|---|---:|---:|---:|---:|---:|
| S=1 | 0.9995375 | 0.99685371 | 1.00001 | 2.13768 | 2.93935 |
| S=2 | 0.99946898 | 0.99680364 | 1.0002315 | 2.11588 | 1.8278 |
| S=3 | 0.99946482 | 0.99681483 | 1.0002851 | 2.11346 | 1.86386 |

Controles congelados: {"Q0": true, "Q1": true, "Q2": true, "Q3": true, "Q4": true, "N1_sem_sinal": true}.
Todos os casos e controles, inclusive desvios da previsão e resíduos, estão preservados em B25Q.json e B25Q_casos.csv.

[?] O caminho denso do código original (D≤7000) registra resíduo 0 sem calcular um diagnóstico independente de norma. Essa convenção original foi preservada; não se apresenta o zero como resíduo numericamente medido. No caminho esparso, o código calcula o resíduo normalizado descrito no protocolo. O avaliador foi aplicado como fornecido.

## B25-T — radar direto, sem decisão confirmatória

| Família | Eixo | v_radar/v_homog | Pureza final | Pureza prevista | Deriva E |
|---|---|---:|---:|---:|---:|
| ani | x | 0.98715699 | 0.9999787 | 0.99999021 | 3.2063e-05 |
| ani | y | 0.98328157 | 0.99999146 | 0.99998325 | 3.2299e-05 |
| ani | z | 0.97553822 | 0.99996467 | 0.99999917 | 3.9355e-05 |
| iso | x | 1.001596 | 0.99998237 | 0.99999996 | 2.3668e-05 |
| iso | y | 1.0007033 | 0.999997 | 0.99999992 | 2.3946e-05 |

O código mede um pacote em lâmina filtrado, com helicidade configurada h=+1; não constitui uma varredura de ambas as helicidades. Os resultados não substituem o teste principal no limite k→0. A projeção/filtro, os passos e as estimativas de velocidade permanecem no código original e nos JSON. O estimador de λ_max em T chama eigsh sem fixar explicitamente v0; portanto, mesmo com a semente geométrica registrada, não se promete reprodução bit a bit dos passos e diagnósticos entre execuções. A deriva E fornecida é a diferença entre energia final e inicial, não o máximo da deriva em todos os instantes.

[F/D] Convenção adicional a preservar na leitura: o código escolhe t1 e t2 pela ordem cartesiana dos eixos restantes. Para propagação em +y, t1=x e t2=z, portanto t1×t2=-y. Assim, o rótulo h=+1 da configuração não é uma convenção de helicidade física com a mesma mão relativa a +k em todos os eixos. A pureza acima é o diagnóstico na base escolhida pelo código; a fonte congelada não foi corrigida ou reorientada nesta execução. Isso limita a leitura da helicidade de T, sem alterar as decisões R ou Q do avaliador.

Concordância de velocidades e alta pureza durante esta janela finita não aprovam automaticamente a condição de cone único. R1 mantém sua decisão estatística independente, com as amostras e os controles do bloco R.

## Interpretação e limites

[M] As classificações acima respondem às hipóteses operacionais da bancada com a regra U (massas unitárias) e seus controles W. [H/?] Uma leitura ontológica do substrato ou uma equivalência com geometria física requer trabalho adicional. A homogeneização é de onda longa, a malha é congelada, as correções microscópicas de ordem superior não foram incluídas e ħ continua uma entrada.
[D] Não houve mudança de limiares, substituição de amostras ou promoção de testes de fumaça a resultados completos. Não se apagaram resultados negativos. As decisões completas e todos os controles constam no JSON original do avaliador.

## Arquivos

`src/` e protocolo: originais; `resultados/`: saídas completas e avaliação; `logs/`: execução e teste sintético; `tabelas/`: CSV derivados; `figuras/`: gráficos derivados; `tools/`: preparação da entrega. O manifesto desta entrega permite conferir os arquivos. Os relatórios não exigem acesso a GitHub, Drive ou repositório externo.
