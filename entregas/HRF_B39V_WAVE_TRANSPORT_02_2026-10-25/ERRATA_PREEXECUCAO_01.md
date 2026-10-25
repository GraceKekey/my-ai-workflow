# Errata de documentação01 — 25/10/2026

[D] Correção anterior a qualquer rodada científica WT-02: o último exemplo de HOW_TO_RUN.md passou a usar analysis_certified/CASO1. A versão anterior mostrava a própria pasta analysis/CASO1 que continha summary.json usado como evidência hashada; isso poderia invalidar a trilha de auditoria ao sobrescrevê-la.

[D] As evidências calculadas e seus arquivos-fonte devem permanecer imutáveis. Uma nova análise certificada ou apresentação deve usar outra saída. A CLI já permite esse comportamento; não foi necessário mudar código, parâmetros, tolerâncias ou critérios de decisão. O hash de código permanece 2ff010bf79949676b8e61fc466a7180e44a396537486c57890233c1755f7e52b.

[D] O manifesto e manual anteriores estão preservados em provenance/documentation_revision_01/. O ZIP anterior também foi preservado, sem sobrescrita. O manifesto ativo foi reemitido com a revisão documental01; a versão externa solicitada do pacote continua v0_1. Nenhuma nova simulação científica foi executada.
