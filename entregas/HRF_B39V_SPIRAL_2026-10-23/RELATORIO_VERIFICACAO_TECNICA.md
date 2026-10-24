# Verificação técnica da entrega

[D] Grandes simulações científicas não executadas. Apenas 45 testes unitários algébricos e smoke indispensável da versão final (primeiro smoke preservado): dois sentidos,13³ nós,t=.6,24 passos de.025,cinco frames por caso. Checkpoint interrompido no passo6 e retomado.

[M] 31 PNGs verificados, dois GIFs de cinco frames e dois MP4s conferidos com ffprobe. JSON/CSV/NPZ exportados e lidos. Campos phi/energia/fluxo finitos e energia não negativa no smoke. Paridade entre rotações refletidas: erro relativo 0.0. Isso é verificação técnica, não evidência de uma espiral.

[D] Pipeline de visualização: PASS_SPIRAL_VISUALIZATION_PIPELINE. Z-scan computado no smoke: PASS_ZSCAN_DIAGNOSTICS no escopo técnico de chegada por limiar. Informação física e helicidade não resolvidas: FAIL_NO_RESOLVED_INFORMATION por fonte/tempo insuficientes. Estrutura: INCONCLUSIVE_SPIRAL_STRUCTURE. Nenhuma fase foi inventada: mapas e exportação usam cinza/NaN/null.

[D] Freeze de 196 arquivos conferido. Os 495 arquivos do manifesto da entrega integral anterior foram conferidos sem alterações. Os limiares históricos permaneceram intactos. A falha de dtype na primeira versão do teste e sua correção anterior ao smoke estão em ALTERACOES.md e reports/unit_tests_initial.log.

[?] Grandes presets, convergência e contornos físicos da nova bancada continuam não executados. O sweep controls ultrapassa o orçamento de disco padrão; filtrar um caso ou revisar limite explicitamente antes de executar externamente. Holografia HRF: BLOCKED_NO_VALIDATED_HOLOGRAPHIC_DICTIONARY.

```json
{
  "paired_helicity_comparison": {
    "status": "INCONCLUSIVE_INSUFFICIENT_PHASE",
    "matched_phase_rings": 0,
    "mean_chirality_plus": null,
    "mean_chirality_minus": null,
    "angular_power_reflection_relative_error": null,
    "orbital_sign_flip_relative_error": 0.46855104078969684,
    "notice": "comparison of operational angular data; no holography, particle helicity or upward-transport conclusion",
    "plus_case": "splus",
    "minus_case": "sminus",
    "plus_twist": {
      "upper": {
        "kz": null,
        "phase_crest_dtheta_dz": null,
        "pitch_z_per_2pi": null
      },
      "lower": {
        "kz": null,
        "phase_crest_dtheta_dz": null,
        "pitch_z_per_2pi": null
      },
      "all": {
        "kz": null,
        "phase_crest_dtheta_dz": null,
        "pitch_z_per_2pi": null
      }
    },
    "minus_twist": {
      "upper": {
        "kz": null,
        "phase_crest_dtheta_dz": null,
        "pitch_z_per_2pi": null
      },
      "lower": {
        "kz": null,
        "phase_crest_dtheta_dz": null,
        "pitch_z_per_2pi": null
      },
      "all": {
        "kz": null,
        "phase_crest_dtheta_dz": null,
        "pitch_z_per_2pi": null
      }
    }
  },
  "state": "PREREGISTERED_NO_FINAL_SCIENTIFIC_EXECUTION",
  "unit_tests_passed": 45,
  "technical_smoke_completed_cases": 2,
  "smoke_grid": [
    13,
    13,
    13
  ],
  "smoke_t_end": 0.6,
  "smoke_dt": 0.025,
  "frames_per_case": 5,
  "checkpoint_nonzero_step_before_resume": 6,
  "PNG_verified": 31,
  "GIF_verified": 2,
  "MP4_verified": 2,
  "volume_JSON_CSV_NPZ_export_verified": true,
  "phase_undefined_exported_as_JSON_null": true,
  "rotation_reflection_relative_error_smoke": 0.0,
  "source_freeze_files_verified": 196,
  "source_freeze_sha256": "99185be880281f546092b541e1d90b837778f4277e93df2e775cc70b5758fc1a",
  "code_sha256": "d25a2e858ba8b6a4ded8cc704ebc22422ab2ca71d71b9216055d929fd398595a",
  "previous_integral_files_verified_unchanged": 495,
  "large_presets_executed": [],
  "scientific_structure": "INCONCLUSIVE_SPIRAL_STRUCTURE",
  "HRF_holography": "BLOCKED_NO_VALIDATED_HOLOGRAPHIC_DICTIONARY",
  "versions": {
    "numpy": "2.2.6",
    "scipy": "1.15.3",
    "matplotlib": "3.10.3",
    "Pillow": "12.3.0"
  }
}
```

[M] O diagnóstico orbital comparativo do smoke coarse apresentou erro relativo de reflexão 0.46855104078969684. Não se certifica simetria/conservação orbital nessa resolução; o momento orbital depende de gradientes e quadratura. O teste de campo nodal refletido é separado. Sem fase resolvida, a comparação de helicidade continua inconclusiva. Não houve ajuste de parâmetro para reduzir esse erro.

[D] No Windows, o script fornecido usa python -X utf8 -I; para comandos manuais, acrescentar -X utf8 ao Python ao gerar relatórios Unicode. Execução verificada em Linux; launcher Windows revisado estaticamente.
