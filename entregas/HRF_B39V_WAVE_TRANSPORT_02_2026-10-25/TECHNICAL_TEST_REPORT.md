# Relatório de testes técnicos — WT-02

**25/10/2026 · PRÉ-REGISTRO · NOVAS RODADAS CIENTÍFICAS NÃO EXECUTADAS.**

[M] **89 testes técnicos passaram, zero falhas/erros/skips.** Registro final: reports/technical_tests/release/summary.json e test.log. Código SHA-256: `2ff010bf79949676b8e61fc466a7180e44a396537486c57890233c1755f7e52b`. Estes testes incluem álgebra, dados sintéticos identificados, IO e integrações mínimas de referência matemática, autorizadas pela especificação. Não são execuções de configs/.

| Referência técnica efetivamente calculada | Medida |
|---|---|
| Modo estacionário 729/4913 nós, t=.5 | ordem espacial 1.99689056; RMS 0.00300777754, 0.000753566799 |
| RK4 vs modo semidiscreto exato,343 nós,t=.4 | ordens 3.95925947, 3.98115726 |
| Paridade vertical plana,729 nós,t=.4 | erro relativo 4.58865598e-17 |
| Reflexão s+/s−,729 nós,t=.4 | erro relativo 4.63730423e-17 |
| Ledger com sponge, passivo/recíproco | erro relativo 5.31227728e-12 / 5.31266442e-12 |
| Checkpoint interrompido/retomado,343 nós,t=.32 | 17frames; energia idêntica bit a bit à execução técnica contínua |
| Figuras/exportações da referência de343 nós | PNG, CSV, NPZ, GIF e MP4 H264 (960×720,6frames) verificados |

[D] A execução técnica de343 nós está rotulada TECHNICAL_REFERENCE_ONLY. Sua janela curta e baixa resolução retornam INCONCLUSIVE para a estrutura, como esperado. Não se deduziu uma espiral nem uma ausência física geral de espiral. O pico de amplitude do modo inicial é t=0, logo o mapa de correntes desse snapshot mostra zero, corretamente; não foram desenhados vetores artificiais.

[D] Todos os36 registros de cenários dos12presets continuam NOT_EXECUTED. results/ e figures/ científicos estão vazios; exemplos técnicos ficam somente em reports/technical_tests/. O replay científico de nove variantes não foi realizado. As referências de software não certificam os controles científicos grandes, especialmente a malha de56GiB bloqueada por recursos.

[D] Os logs de desenvolvimento anteriores foram preservados separadamente. build_01/build_02/final_candidate tiveram um campo chamado gates_frozen_during_tests antes do manifesto final; leia-o como constância de parâmetros durante aquele teste, não como alegação de congelamento final já emitido. O recibo release distingue explicitamente gates_unchanged_during_test_run e preregistration_manifest_present (false porque os testes precedem o manifesto). A exportação MP4 falhou no primeiro ensaio por nomes com4dígitos; foi corrigida e verificada com5dígitos. Não foi alegada ausência de codec para ocultar a causa.

[M/?] Scripts Windows fornecidos; não foram executados num Windows nesta máquina Linux. Hashes usam nomes de caminhos POSIX, e admissão Windows possui consulta nativa de memória; isso não equivale a um teste de execução nessa plataforma.

[?] Não foram auditados os dados científicos SPIRAL do celular. Não existe novo veredicto de transporte helicoidal. BLOCKED_NO_VALIDATED_HOLOGRAPHIC_DICTIONARY permanece.
