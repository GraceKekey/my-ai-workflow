# HRF B39V — Wave Transport 02

**PRÉ-REGISTRADO — NOVAS RODADAS CIENTÍFICAS NÃO EXECUTADAS.**

[M] Bancada autossuficiente de campo escalar clássico 3+1: propagação vertical, correntes de energia, fase, vales e receptores. Continuação do código local INTEGRAL → SPIRAL → VVR; não é uma reprodução certificada da rodada do celular.

[D] A especificação completa recebida está em `documentation/ESPECIFICACAO_ORIGINAL.md`. Este texto substitui, para WT-02, a exigência anterior de capítulos externos antes da implementação/execução. Não é necessário Drive, outro chat ou repositório durante o uso. Todas as entradas necessárias aos cenários novos estão incluídas; reanálises exigem os próprios dados que se deseja reanalisar.

```bash
python -m pip install -r requirements.txt
python -I scripts/wt02.py validate
python -I scripts/wt02.py plan --config configs/vertical_medium.json --output ../WT02_PLAN
python -I scripts/wt02.py test --output ../WT02_TESTS
```

[D] O comando `test` executa referências técnicas limitadas, inclusive integrações matemáticas pequenas. Não executa presets científicos. `plan` nunca monta a malha volumétrica nem integra a PDE. Uma execução futura exige o comando separado `run ... --execute`, descrito no manual. Não use `--execute` para apenas conferir o pacote.

Leia `documentation/HOW_TO_RUN.md`, `PROTOCOL_PREREG.md`, `OBSERVABLES_AND_GATES.md` e `RESOURCES.md`. O resumo de verificação está em `documentation/TECHNICAL_TEST_REPORT.md`; os registros separados estão em `reports/technical_tests/`.

[?] Os resultados científicos SPIRAL do celular não foram disponibilizados. Os números históricos transcritos são `USER_REPORTED_NOT_INDEPENDENTLY_REPRODUCED`. Não há novo veredicto sobre hélice.

[D] `provenance/vvr_original/` preserva documentos e recibos da versão anterior; seus bloqueios por capítulos externos e antigos estados não governam WT-02. Os módulos `hrf_integral/` e `historico/` são preservados. A CLI pública suportada é `hrf_b39v.cli` ou o launcher isolado `scripts/wt02.py`.

[M/?] Apenas o mapa W é investigado. **BLOCKED_NO_VALIDATED_HOLOGRAPHIC_DICTIONARY** permanece obrigatório; não há demonstração de G, D, DIO, GMFt, fóton quântico ou gravidade emergente.

Verifique o ZIP: `python -I scripts/verify_manifest.py`. O manifesto completo descreve a entrega; `hashes_antes_da_execucao.txt` congela código, protocolo, configurações e entradas, sem incluir resultados futuros.
