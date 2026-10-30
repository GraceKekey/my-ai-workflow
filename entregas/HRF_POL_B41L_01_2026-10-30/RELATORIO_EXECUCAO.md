# HRF-POL-B41L-01 — relatório de execução v0.1.2

**30/10/2026 — somente validação técnica e fumaça. Rodada científica completa NOT_EXECUTED.**

[D] Capítulo0.1v0.2 e Capítulo2v1.5 lidos integralmente, sem substituir versões. Código B41L e seus resultados históricos tratados como dependências congeladas. Os43 hashes originais conferiram antes/depois; nenhum fonte B41L foi alterado. Toda implementação nova está fora desse diretório.

[M] **47 testes sintéticos originais passaram e23 testes novos passaram.** Os novos incluem Stokes convencionais, estados elípticos, campo nulo, mistura parcialmente polarizada, perda artificial, mapa incorreto, gauge de campos Whitney, reconstrução de campo constante, fidelidade do integrador e retomada de checkpoint com arrays numéricos idênticos. Há uma referência pequena real de64nós e T=.4; isso é teste técnico, não execução do preset completo.

[D] A primeira rodada de testes novos teve1 erro de tipo no teste de perda (lista Python multiplicada por escalar). As representações dos estados novos foram uniformizadas para arrays. Log e fonte anteriores foram preservados. A primeira fumaça também foi preservada; a revisão técnica da emenda01 corrigiu a comparação do vetor de Gauss, a classificação de janelas ausentes e acrescentou diagnósticos de frequência, sem mudar tolerâncias. Não houve reajuste para obter PASS.

## Fumaça revisada, dados realmente calculados

[M] Foram concluídos6casos: lado5, semente41910001, +z, C+/H/nulo, V0/V1,4períodos nominais. Os dois casos V1 não nulos passaram G2/preparação; G3 não passou, e G4/G6 ficaram pendentes. Os casos nulos se mantiveram nulos, com polarização indefinida. Os estados completos, outras sementes/orientações e os refinamentos científicos ainda não foram executados.

| Estado | Variante | G2 | G3 | G4 | Resíduo MQO | Gauss dinâmico | Deriva de energia |
|---|---|---|---|---|---:|---:|---:|
|C+|V0|FAIL|FAIL|PENDING|0.160886|5.66817e-14|0.000371469|
|C+|V1|PASS|FAIL|PENDING|0.160919|8.93803e-15|0.000377002|
|H|V0|FAIL|FAIL|PENDING|0.142822|4.73697e-14|0.00032699|
|H|V1|PASS|FAIL|PENDING|0.142854|8.44035e-15|0.00033065|
|nulo|V0|PASS|PASS|PASS|0|0|0|
|nulo|V1|PASS|PASS|PASS|0|0|0|

[M/?] C+ e H têm resíduos primários de aproximadamente0.161 e0.143 contra limite0.05. As janelas exigidas existem nesta fumaça; não foi falta de uma janela que causou esse FAIL. A proteção PENDING para janelas insuficientes foi corrigida e registrada, mas não alterou esses vereditos. O ajuste em frequência nominal fixa é insuficiente nesta malha grossa: isso limita o observável e impede certificar transporte a partir desses fasores. Não se infere falha física definitiva da B41L, nem se substitui o resultado por Jones ideal.

## Gates atuais

| Gate | Estado/escopo |
|---|---|
| G0 | PASS de integridade local e fontes congeladas; ambiente diferente do histórico registrado |
| G1 | PENDING para POL-01/P01–P05; diagnóstico novo Jones PASS, sem transferência de veredito |
| G2 | PASS na preparação V1 da fumaça; V0 mostra a carga espúria esperada |
| G3 | FAIL de qualidade de extração nos casos não nulos da fumaça |
| G4 | PENDING por G3 |
| G5 | NOT_EXECUTED para a família científica; os dados de uma malha/uma semente são apenas fumaça |
| G6 | PENDING por G3/G4 |
| G7 | PENDING; sem conclusão positiva de transporte relacional |

[D] O summary.json da fumaça usa PENDING para a robustez ainda não coberta, e não lhe atribui o gate científico completo. O notebook tem CONFIRMO_COMPLETA=False e a distribuição não iniciou nenhum dos2400casos do preset completo. A indicação de notebook preparado refere-se ao fluxo implementado e às verificações estáticas; ele não foi aberto numa sessão real Colab nesta máquina.

## Rodada completa futura — campos ainda sem resultados

| Campo | Estado |
|---|---|
| Completa executada | NÃO |
| Casos completos/2400 |0|
| Stokes das8polarizações em3refinamentos e10sementes | NOT_EXECUTED |
| Robustez por orientação/reversão | NOT_EXECUTED |
| G5/IC95 da família científica | NOT_EXECUTED |
| Correspondência Maxwell×B41L certificada | PENDING |
| Emissão/absorção/fóton individual/holografia | fora de escopo |

[?] POL-01 original não foi localizado nem fornecido. Ele é necessário para afirmar preservação dos P01–P05; não se atribuiu PASS a essa lacuna. A bancada consegue executar os cenários reais B41L e reprovar mapas/extrações, mas não deve declarar sucesso científico com G1 pendente e G3 falhando na fumaça. Qualquer mudança para resolver o método de extração requer revisão identificada e novo congelamento antes de uma rodada completa.

[D] Correção visual 0.1.2: marcadores mostram a janela única no gráfico de Stokes. Ver EMENDA_VISUAL_02.md. Nenhum dado, critério ou módulo numérico foi alterado.
