# HRF-POL-B41L-01 — relatório da rodada Codex

## Objetivo

[M] Avaliar transporte de polarização na dinâmica B41L real, usando o pré-registro e V1 como lançamento principal.

## Hipóteses e parâmetros

[D] Mesmos 2.400 casos: dez sementes, malhas 6³/8³/10³, três direções, oito polarizações mais fase alterada e nulo, V0/V1, oito períodos e refinamento temporal na maior malha. Nenhuma tolerância ou semente foi alterada.

## Protocolo e integridade

[D] Execução explicitamente autorizada pelo usuário no Codex em quatro processos, BLAS uma thread por processo. A emenda 03 altera somente o gerenciamento; os dez módulos numéricos, as configurações e a dependência B41L permanecem idênticos à distribuição 0.1.2. Os 43 hashes B41L conferiram antes e depois. Os 28 testes técnicos prévios passaram.

## Medidas e resultados

[M] Casos concluídos: 2400/2400. Tempo de parede: 4.863 horas. Estado de execução: COMPLETED.

| Gate | Estado |
|---|---|
| G0 | PASS |
| G1 | PENDING |
| G2 | PASS |
| G3 | FAIL |
| G4 | FAIL |
| G5 | FAIL |
| G6 | PENDING |
| G7 | PENDING |

[M] Gates por malha e variante abaixo excluem o nulo e usam dt_scale=1. As falhas não são descartadas. As linhas completas, incluindo controles nulos e dt/2, estão no CSV.

| Malha | Variante | Casos | G2 PASS | G3 PASS | G4 PASS | G6 PASS |
|---|---|---:|---:|---:|---:|---:|
| 6³ | V0 | 270 | 0 | 0 | 0 | 0 |
| 6³ | V1 | 270 | 270 | 0 | 0 | 0 |
| 8³ | V0 | 270 | 0 | 16 | 13 | 0 |
| 8³ | V1 | 270 | 270 | 16 | 13 | 13 |
| 10³ | V0 | 270 | 0 | 259 | 241 | 0 |
| 10³ | V1 | 270 | 270 | 259 | 241 | 241 |

## Controles e convergência

[M] Ordem espacial medida: 4.294325476468947. Diferenças temporais e intervalos Clopper–Pearson completos no summary.json. O controle V0 preserva o lançamento original; não recebe limpeza adicional.

## Interpretação e limites

[?] G1/P01–P05 original continua PENDING porque HRF_3_Bancadas.zip / HRF_3_Execucoes.zip não foram fornecidos. G7 não pode PASS enquanto faltar essa dependência. Nenhum PASS isolado certifica todo o transporte relacional. Falhas de qualidade, conservação ou convergência permanecem no resultado congelado.

[F/M] O campo e os Stokes são reconstruídos da evolução real de cochains B41L, não copiados de Jones. Jones prepara/referencia os estados. O modelo usa o limite quadrático Wilson e geometria prescrita periódica; não demonstra fóton individual, origem de U(1), ħ ou holografia. Nenhum veredito histórico B1/B41/B41H/B41L foi reclassificado.

[D] Este relatório posterior substitui apenas a indicação de NOT_EXECUTED da nova rodada completa, não reescreve os pré-registros ou relatórios anteriores. Logs, casos, selos e campos originais estão preservados.
