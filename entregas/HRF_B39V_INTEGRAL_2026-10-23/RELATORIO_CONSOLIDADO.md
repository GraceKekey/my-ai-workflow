# Relatório consolidado — HRF B39V integral

## Objetivo

[D] Executar a extensão volumétrica e controles conhecidos de AdS/CFT, com autorização posterior ao pedido original de pré-registro. O novo dicionário de 23/10 foi recebido e incorporado antes do freeze principal.

## Hipóteses

[M] Convergência do campo KG em ADM prescrito e reconstrução de referências sintéticas conhecidas. [H/?] A identidade física HRF→CFT e DIO→manifestação não é fornecida pelas fórmulas bibliográficas.

## Parâmetros

[D] Toda a configuração principal foi congelada em config/. Duas séries suplementares foram registradas antes de obter seus próprios resultados: cavidade AdS/trabalho externo e domínio compacto com fonte resolvida. Os protocolos e hashes respectivos são preservados. Não substituem nem ajustam a bancada histórica.

## Protocolo

[D] FEM P1 tetraédrico, massa concentrada, shift adjunto Hamiltoniano, RK4, osciladores recíprocos, 468 posições históricas, regras e limiares herdados. Fontes e geometria 3D são candidatas explícitas. A única correção anterior à rodada científica foi o incremento de diferença finita do teste unitário de energia; fonte do teste e log inicial estão em preregistro/v1 e EMENDAS.md.

## Medidas

[M] Campo nos receptores, resposta demodulada e filtrada, relé e luminosidade são canais distintos. Energia medida é o Hamiltoniano das perturbações (campo+osciladores+acoplamento); não inclui a energia total e as interferências da rede estacionária adicionada analiticamente ao readout. Arquivos signals.npz principais guardam sinais em float32 para distribuição, enquanto métricas/energia e decisões foram calculadas em float64. Controles compactos são guardados em float64.

## Resultados

```json
{
  "software": "PASS_SOFTWARE",
  "numerical": "PASS_NUMERICAL",
  "controlled_reference": "PASS_HOLOGRAPHIC_REFERENCE",
  "dictionary_formulas": "PASS_HOLOGRAPHIC_REFERENCE",
  "transfer": "INCONCLUSIVE",
  "HRF_holographic_reconstruction": "BLOCKED_NO_VALIDATED_HOLOGRAPHIC_DICTIONARY",
  "scenarios": {
    "smoke": {
      "gate": "INCONCLUSIVE",
      "adversarial_controls": [
        {
          "case": "parity_reflected_rotation",
          "relative_peak_vector_difference": 1.4904113155155435e-13,
          "status": "PASS_NUMERICAL",
          "scope": "finite-mesh artifact diagnostic, not physical chirality inference"
        }
      ],
      "reason": "No continuum-certified full historical transfer; coarse candidate comparisons descriptive",
      "comparisons": [
        {
          "id": "G_P_s+1",
          "fired": 0,
          "shadow_vs_flat": 0,
          "focus_peak_ratio": 1.0,
          "median_peak_ratio": 1.0,
          "median_arrival_delay_vs_flat": 0.0,
          "reference_zero_undefined": 0
        },
        {
          "id": "G_P_s-1",
          "fired": 0,
          "shadow_vs_flat": 0,
          "focus_peak_ratio": 1.7759440794311254,
          "median_peak_ratio": 0.9999999999999991,
          "median_arrival_delay_vs_flat": 0.0,
          "reference_zero_undefined": 0
        }
      ],
      "executed": 2,
      "blocked": 0,
      "planned": 2,
      "analysis_note": "Descriptive ratios corrected post-execution; see reanalise/ERRATA.md and original preserved reports"
    },
    "standard": {
      "gate": "INCONCLUSIVE",
      "adversarial_controls": [
        {
          "case": "C_mass0",
          "relative_peak_vector_difference": 0.9987858671599338,
          "status": "DESCRIPTIVE_NOT_CERTIFIED"
        },
        {
          "case": "C_mass1p2",
          "relative_peak_vector_difference": 0.9875909727693325,
          "status": "DESCRIPTIVE_NOT_CERTIFIED"
        },
        {
          "case": "C_frequency2p2",
          "relative_peak_vector_difference": 0.9998864945416418,
          "status": "DESCRIPTIVE_NOT_CERTIFIED"
        },
        {
          "case": "C_neumann",
          "relative_peak_vector_difference": 0.03182680106681711,
          "status": "DESCRIPTIVE_NOT_CERTIFIED"
        },
        {
          "case": "C_half_dt",
          "relative_peak_vector_difference": 0.0003928109277201041,
          "status": "PASS_NUMERICAL"
        },
        {
          "case": "C_harmonic",
          "relative_peak_vector_difference": 3.384867319917592,
          "status": "DESCRIPTIVE_NOT_CERTIFIED"
        },
        {
          "case": "M_P_s+1",
          "relative_peak_vector_difference": 0.8605628519108601,
          "status": "DESCRIPTIVE_NOT_CERTIFIED"
        },
        {
          "case": "parity_reflected_rotation",
          "relative_peak_vector_difference": 2.5326909141443744e-14,
          "status": "PASS_NUMERICAL",
          "scope": "finite-mesh artifact diagnostic, not physical chirality inference"
        }
      ],
      "reason": "No continuum-certified full historical transfer; coarse candidate comparisons descriptive",
      "comparisons": [
        {
          "id": "G_P_s+1",
          "fired": 0,
          "shadow_vs_flat": 0,
          "focus_peak_ratio": 1.0,
          "median_peak_ratio": 1.0,
          "median_arrival_delay_vs_flat": 0.0,
          "reference_zero_undefined": 0
        },
        {
          "id": "G_P_s-1",
          "fired": 0,
          "shadow_vs_flat": 0,
          "focus_peak_ratio": 1.7193151799620172,
          "median_peak_ratio": 1.000000000000002,
          "median_arrival_delay_vs_flat": 0.0,
          "reference_zero_undefined": 0
        },
        {
          "id": "G_V1a6_s+1",
          "fired": 0,
          "shadow_vs_flat": 0,
          "focus_peak_ratio": 1.5927944537644545,
          "median_peak_ratio": 0.8896678573807018,
          "median_arrival_delay_vs_flat": 3.5,
          "reference_zero_undefined": 0
        },
        {
          "id": "G_V1a12_s+1",
          "fired": 0,
          "shadow_vs_flat": 104,
          "focus_peak_ratio": 1.7662972421582663,
          "median_peak_ratio": 0.5944559731356993,
          "median_arrival_delay_vs_flat": 6.0,
          "reference_zero_undefined": 0
        },
        {
          "id": "G_V1a12_s-1",
          "fired": 0,
          "shadow_vs_flat": 100,
          "focus_peak_ratio": 1.7514711919186867,
          "median_peak_ratio": 0.5935499149284316,
          "median_arrival_delay_vs_flat": 6.0,
          "reference_zero_undefined": 0
        },
        {
          "id": "G_V1a18_s+1",
          "fired": 0,
          "shadow_vs_flat": 196,
          "focus_peak_ratio": 1.5314587676159406,
          "median_peak_ratio": 0.2912630743296306,
          "median_arrival_delay_vs_flat": 4.5,
          "reference_zero_undefined": 0
        },
        {
          "id": "G_V2n_s+1",
          "fired": 0,
          "shadow_vs_flat": 143,
          "focus_peak_ratio": 3.1128906565257353,
          "median_peak_ratio": 0.5481680445894986,
          "median_arrival_delay_vs_flat": 6.0,
          "reference_zero_undefined": 0
        },
        {
          "id": "G_V2n_s-1",
          "fired": 0,
          "shadow_vs_flat": 145,
          "focus_peak_ratio": 2.851908870635296,
          "median_peak_ratio": 0.4829589199409754,
          "median_arrival_delay_vs_flat": 6.0,
          "reference_zero_undefined": 0
        },
        {
          "id": "G_V2o_s+1",
          "fired": 0,
          "shadow_vs_flat": 161,
          "focus_peak_ratio": 3.0878122537246018,
          "median_peak_ratio": 0.4206229398623011,
          "median_arrival_delay_vs_flat": 5.0,
          "reference_zero_undefined": 0
        },
        {
          "id": "G_V2o_s-1",
          "fired": 0,
          "shadow_vs_flat": 164,
          "focus_peak_ratio": 3.477820102692047,
          "median_peak_ratio": 0.44215715222720353,
          "median_arrival_delay_vs_flat": 5.0,
          "reference_zero_undefined": 0
        },
        {
          "id": "G_V3s44_s+1",
          "fired": 0,
          "shadow_vs_flat": 114,
          "focus_peak_ratio": 2.1267950598868093,
          "median_peak_ratio": 0.6309123096360367,
          "median_arrival_delay_vs_flat": 7.0,
          "reference_zero_undefined": 0
        },
        {
          "id": "G_V3s45_s+1",
          "fired": 0,
          "shadow_vs_flat": 115,
          "focus_peak_ratio": 2.1381786692733495,
          "median_peak_ratio": 0.6281595033128039,
          "median_arrival_delay_vs_flat": 7.0,
          "reference_zero_undefined": 0
        },
        {
          "id": "T_T1f03_s+1",
          "fired": 0,
          "shadow_vs_flat": 450,
          "focus_peak_ratio": 0.5555435540207113,
          "median_peak_ratio": 0.0175631764252462,
          "median_arrival_delay_vs_flat": 1.0,
          "reference_zero_undefined": 0
        },
        {
          "id": "T_T1Rf03_s+1",
          "fired": 0,
          "shadow_vs_flat": 248,
          "focus_peak_ratio": 4.27629172173687,
          "median_peak_ratio": 0.21391349375314853,
          "median_arrival_delay_vs_flat": 3.0,
          "reference_zero_undefined": 0
        },
        {
          "id": "T_T1f05_s+1",
          "fired": 0,
          "shadow_vs_flat": 468,
          "focus_peak_ratio": 0.2053611552755553,
          "median_peak_ratio": 0.0006867741521989045,
          "median_arrival_delay_vs_flat": -2.0,
          "reference_zero_undefined": 0
        },
        {
          "id": "T_T1Rf05_s+1",
          "fired": 0,
          "shadow_vs_flat": 374,
          "focus_peak_ratio": 9.097612045135262,
          "median_peak_ratio": 0.031003873951864144,
          "median_arrival_delay_vs_flat": 1.0,
          "reference_zero_undefined": 0
        },
        {
          "id": "T_T1f08_s+1",
          "fired": 0,
          "shadow_vs_flat": 468,
          "focus_peak_ratio": 0.06345674861861827,
          "median_peak_ratio": 1.481302111786677e-06,
          "median_arrival_delay_vs_flat": -81.0,
          "reference_zero_undefined": 0
        },
        {
          "id": "T_T1Rf08_s+1",
          "fired": 0,
          "shadow_vs_flat": 434,
          "focus_peak_ratio": 9.41230090652189,
          "median_peak_ratio": 0.001031903807239221,
          "median_arrival_delay_vs_flat": -9.0,
          "reference_zero_undefined": 0
        },
        {
          "id": "M_P_s+1",
          "fired": 0,
          "shadow_vs_flat": 4,
          "focus_peak_ratio": 166.84921870056286,
          "median_peak_ratio": 9.837710018434626,
          "median_arrival_delay_vs_flat": 2.0,
          "reference_zero_undefined": 0
        },
        {
          "id": "M_V1a18_s+1",
          "fired": 0,
          "shadow_vs_flat": 34,
          "focus_peak_ratio": 75.172963297599,
          "median_peak_ratio": 1.2459593274326228,
          "median_arrival_delay_vs_flat": 5.0,
          "reference_zero_undefined": 0
        },
        {
          "id": "C_mass0",
          "fired": 0,
          "shadow_vs_flat": 298,
          "focus_peak_ratio": 27204.531008846345,
          "median_peak_ratio": 0.0035297300321265237,
          "median_arrival_delay_vs_flat": -293.0,
          "reference_zero_undefined": 0
        },
        {
          "id": "C_mass1p2",
          "fired": 0,
          "shadow_vs_flat": 428,
          "focus_peak_ratio": 1.5061235842304768,
          "median_peak_ratio": 0.003476000690477746,
          "median_arrival_delay_vs_flat": -1.0,
          "reference_zero_undefined": 0
        },
        {
          "id": "C_frequency2p2",
          "fired": 0,
          "shadow_vs_flat": 468,
          "focus_peak_ratio": 0.003598412050126495,
          "median_peak_ratio": 0.002077633094917909,
          "median_arrival_delay_vs_flat": 2.0,
          "reference_zero_undefined": 0
        },
        {
          "id": "C_neumann",
          "fired": 0,
          "shadow_vs_flat": 110,
          "focus_peak_ratio": 1.0000020463997557,
          "median_peak_ratio": 0.3613497346663279,
          "median_arrival_delay_vs_flat": -9.5,
          "reference_zero_undefined": 0
        },
        {
          "id": "C_half_dt",
          "fired": 0,
          "shadow_vs_flat": 0,
          "focus_peak_ratio": 1.0026199791318047,
          "median_peak_ratio": 1.0020375361856189,
          "median_arrival_delay_vs_flat": 0.0,
          "reference_zero_undefined": 0
        },
        {
          "id": "C_harmonic",
          "fired": 0,
          "shadow_vs_flat": 0,
          "focus_peak_ratio": 50.0519452292502,
          "median_peak_ratio": 37.248693014595084,
          "median_arrival_delay_vs_flat": 1.0,
          "reference_zero_undefined": 0
        }
      ],
      "executed": 26,
      "blocked": 0,
      "planned": 26,
      "analysis_note": "Descriptive ratios corrected post-execution; see reanalise/ERRATA.md and original preserved reports"
    },
    "high_resolution": {
      "gate": "INCONCLUSIVE",
      "adversarial_controls": [],
      "reason": "No continuum-certified full historical transfer; coarse candidate comparisons descriptive",
      "comparisons": [],
      "executed": 0,
      "blocked": 26,
      "planned": 26
    }
  },
  "HRT": "BLOCKED_NOT_IMPLEMENTED",
  "QES": "BLOCKED_NO_VARIATIONAL_STATE_FUNCTIONAL",
  "controlled_AdS_and_external_work": "PASS_NUMERICAL",
  "resolved_3D_control": "PASS_NUMERICAL",
  "resolved_3D_checks": {
    "parity_relative_error": true,
    "spatial_refinement_relative_error": true,
    "boundary_relative_error": true,
    "all_receivers_detected": true
  },
  "status_counts": {
    "BLOCKED": 30,
    "DESCRIPTIVE_NOT_CERTIFIED": 6,
    "EXECUTED": 35,
    "PASS_HOLOGRAPHIC_REFERENCE": 2,
    "PASS_NUMERICAL": 25,
    "PASS_SOFTWARE": 32
  },
  "scope": "executed all implemented planned cases; explicit blocked gates and resource admission are not executed simulations",
  "software_tests": 32,
  "executed_volumetric_scenarios": 35,
  "frozen_hash_verification": {
    "checked": 196,
    "status": "PASS",
    "manifest_sha256": "e2a2342581dbf31124f737c631ced50e1bbb0d80b5da95d220f642354691403d"
  }
}
```

### Falhas avaliadas

[]

### Bloqueios

[D] 30 itens com bloqueio explícito, incluindo os casos de alta resolução. O planejamento de memória excede os 32 GiB disponíveis; não houve alocação de malha alta nem simulação desses casos. HRT, QES, dicionário físico HRF e extensão multissetorial são lacunas concretas, não verificações aprovadas.

## Controles e convergência

[M] Ordens: Minkowski espacial 1.994342; temporal 4.019933; cavidade AdS espacial 1.993622. Deriva energética estática 3.457e-11. Balanço trabalho da métrica dinâmica: erro relativo 1.145e-05.

[M] RT: erro relativo no holdout 3.937e-10; HKLL: erro 1.002e-15. Kernel euclidiano, GKPW fonte/resposta, FG e código lógico com controle negativo constam de dictionary.json. Estes são testes em domínios conhecidos e não descoberta de uma dualidade HRF.

## Interpretação

[?] O domínio histórico coarse não resolve σ=1.5 e não conserva amplitudes/disparos da superfície. Não se conclui equivalência ou refutação física antes de convergência, normalização dimensional e fronteiras adequadas. O controle compacto testa propagação 3D com fonte resolvida, mas não substitui os 468 receptores históricos. FAIL de refinamento/borda/simetria deve permanecer FAIL mesmo se o código executou corretamente.

[D] A correção pós-execução da normalização descritiva de sombra está documentada em reanalise/ERRATA.md, com relatórios originais preservados. Os valores efetivos de subamostragem estão em CORRESPONDENCIA_FINAL.csv; AMOSTRA=1 no volume difere do valor histórico .5. Nenhum critério ou veredito físico foi promovido por essas correções.

[D] Não se infere frente universal de meia-chegada, emergência de partícula de um relé, geometria gravitacional dinâmica de uma métrica prescrita ou holografia física de uma regressão sintética. PASS_HOLOGRAPHIC_REFERENCE e bloqueio de E2 são resultados compatíveis. Os resultados históricos e negativos permanecem intactos.
