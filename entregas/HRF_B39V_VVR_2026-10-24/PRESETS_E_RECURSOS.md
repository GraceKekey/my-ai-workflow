# Presets exatos e recursos previstos

**CÓDIGO NOVO — PRÉ-REGISTRADO — SIMULAÇÕES CIENTÍFICAS NÃO EXECUTADAS.**

[D] v0.1 · 24/10/2026 · W apenas; G/D separados.

[D] Estimativas SEM execução. RAM por caso é pico estimado; disco é soma da família inteira sem supor ganho de compressão. A CPU usa proxy240×nós×passos, ajustado à cadência comum; sem throughput calibrado não há previsão defensável em horas. A cota individual é24GiB de RAM e5e13 operações proxy, e a análise tem24GiB/4GiB de RAM/disco.

| Preset | Casos | RAM pico GiB | Disco total GiB | CPU proxy total | Admissão neste ambiente |
|---|---:|---:|---:|---:|---|
| `baseline_reanalysis.json` | 1 | 4.00 | 1.00 | 0.000e+00 | PLANNED_NOT_EXECUTED |
| `chirality_pair.json` | 2 | 7.39 | 15.90 | 2.174e+12 | PLANNED_NOT_EXECUTED |
| `negative_controls.json` | 5 | 7.39 | 39.76 | 5.435e+12 | BLOCKED_RESOURCES |
| `receivers_frequency_sweep.json` | 1 | 2.00 | 1.00 | 0.000e+00 | PLANNED_NOT_EXECUTED |
| `refinement_study.json` | 9 | 56.17 | 131.43 | 1.206e+13 | BLOCKED_RESOURCES |
| `valleys_exploratory.json` | 4 | 7.39 | 31.81 | 4.348e+12 | BLOCKED_RESOURCES |
| `valleys_historical.json` | 4 | 22.05 | 95.17 | 1.359e+13 | BLOCKED_RESOURCES |
| `vertical_boundary_control.json` | 7 | 9.66 | 60.49 | 8.323e+12 | BLOCKED_RESOURCES |
| `vertical_symmetric.json` | 3 | 11.76 | 24.29 | 3.316e+12 | BLOCKED_RESOURCES |

[D] O ambiente de auditoria tinha cerca de25GiB livres; a reserva adicional de2GiB explica bloqueios mesmo quando a cota configurada de disco é maior. O caso completo209²×161 sozinho exige~56,17GiB estimados e ultrapassa24GiB. A seleção`--case` reaplica admissão ao caso, sem alterar o modelo ou apagar resultados. O Colab/Drive terá seus próprios recursos, a checar novamente. Todos os casos científicos têm ainda as dependências documentais bloqueadas.

## baseline_reanalysis

- `archived_spiral_only`: baseline_reanalysis; classe`READ_ONLY_ARCHIVED_DATA`; RAM4.00GiB, disco1.00GiB; NOT_EXECUTED.

## chirality_pair

- `splus`: PDE; classe`EXPLORATORY_3D_PRESCRIBED_GEOMETRY`; RAM7.39GiB, disco7.95GiB; grade[105, 105, 79]; 1041volumes; dt planejado antes do CFL0.1; resolução-proxyadequada; NOT_EXECUTED.
- `sminus`: PDE; classe`EXPLORATORY_3D_PRESCRIBED_GEOMETRY`; RAM7.39GiB, disco7.95GiB; grade[105, 105, 79]; 1041volumes; dt planejado antes do CFL0.1; resolução-proxyadequada; NOT_EXECUTED.

## negative_controls

- `zero_source`: PDE; classe`EXPLORATORY_3D_PRESCRIBED_GEOMETRY`; RAM7.39GiB, disco7.95GiB; grade[105, 105, 79]; 1041volumes; dt planejado antes do CFL0.1; resolução-proxyadequada; NOT_EXECUTED.
- `no_rotation`: PDE; classe`EXPLORATORY_3D_PRESCRIBED_GEOMETRY`; RAM7.39GiB, disco7.95GiB; grade[105, 105, 79]; 1041volumes; dt planejado antes do CFL0.1; resolução-proxyadequada; NOT_EXECUTED.
- `vertical_parity`: PDE; classe`EXPLORATORY_3D_PRESCRIBED_GEOMETRY`; RAM7.39GiB, disco7.95GiB; grade[105, 105, 79]; 1041volumes; dt planejado antes do CFL0.1; resolução-proxyadequada; NOT_EXECUTED.
- `passive_historical_control`: PDE; classe`EXPLORATORY_3D_PRESCRIBED_GEOMETRY`; RAM7.39GiB, disco7.95GiB; grade[105, 105, 79]; 1041volumes; dt planejado antes do CFL0.1; resolução-proxyadequada; NOT_EXECUTED.
- `closed_no_sponge`: PDE; classe`EXPLORATORY_3D_PRESCRIBED_GEOMETRY`; RAM7.39GiB, disco7.95GiB; grade[105, 105, 79]; 1041volumes; dt planejado antes do CFL0.1; resolução-proxyadequada; NOT_EXECUTED.

## receivers_frequency_sweep

- `fixed_incident_signal_replay`: receiver_replay; classe`EXPLORATORY_PASSIVE_COUNTERFACTUAL`; RAM2.00GiB, disco1.00GiB; NOT_EXECUTED.

  Nove replays, um fator por vez: omega_0.1, omega_0.13, omega_0.2, omega_0.5, omega_1.85, gamma_0.05, gamma_0.2, coupling_0.025, coupling_0.1. Nenhum executado.

## refinement_study

- `reference_space_9`: numerical_reference; classe`EXPLORATORY_3D_PRESCRIBED_GEOMETRY`; RAM0.51GiB, disco0.06GiB; grade[9, 9, 9]; 21volumes; dt planejado antes do CFL0.025; resolução-proxyadequada; NOT_EXECUTED.
- `reference_space_17`: numerical_reference; classe`EXPLORATORY_3D_PRESCRIBED_GEOMETRY`; RAM0.54GiB, disco0.06GiB; grade[17, 17, 17]; 21volumes; dt planejado antes do CFL0.025; resolução-proxyadequada; NOT_EXECUTED.
- `reference_space_33`: numerical_reference; classe`EXPLORATORY_3D_PRESCRIBED_GEOMETRY`; RAM0.78GiB, disco0.07GiB; grade[33, 33, 33]; 21volumes; dt planejado antes do CFL0.025; resolução-proxyadequada; NOT_EXECUTED.
- `reference_time_0.05`: numerical_reference; classe`EXPLORATORY_3D_PRESCRIBED_GEOMETRY`; RAM0.78GiB, disco0.07GiB; grade[33, 33, 33]; 21volumes; dt planejado antes do CFL0.05; resolução-proxyadequada; NOT_EXECUTED.
- `reference_time_0.025`: numerical_reference; classe`EXPLORATORY_3D_PRESCRIBED_GEOMETRY`; RAM0.78GiB, disco0.07GiB; grade[33, 33, 33]; 21volumes; dt planejado antes do CFL0.025; resolução-proxyadequada; NOT_EXECUTED.
- `reference_time_0.0125`: numerical_reference; classe`EXPLORATORY_3D_PRESCRIBED_GEOMETRY`; RAM0.78GiB, disco0.07GiB; grade[33, 33, 33]; 21volumes; dt planejado antes do CFL0.0125; resolução-proxyadequada; NOT_EXECUTED.
- `full_space_53`: PDE; classe`EXPLORATORY_3D_PRESCRIBED_GEOMETRY`; RAM1.41GiB, disco2.18GiB; grade[53, 53, 41]; 2081volumes; dt planejado antes do CFL0.083333333; resolução-proxyNÃO certificada; NOT_EXECUTED.
- `full_space_105`: PDE; classe`EXPLORATORY_3D_PRESCRIBED_GEOMETRY`; RAM7.57GiB, disco15.05GiB; grade[105, 105, 81]; 2081volumes; dt planejado antes do CFL0.083333333; resolução-proxyadequada; NOT_EXECUTED.
- `full_space_209`: PDE; classe`EXPLORATORY_3D_PRESCRIBED_GEOMETRY`; RAM56.17GiB, disco113.78GiB; grade[209, 209, 161]; 2081volumes; dt planejado antes do CFL0.083333333; resolução-proxyadequada; NOT_EXECUTED.

## valleys_exploratory

- `exploratory_flat`: PDE; classe`EXPLORATORY_3D_PRESCRIBED_GEOMETRY`; RAM7.39GiB, disco7.95GiB; grade[105, 105, 79]; 1041volumes; dt planejado antes do CFL0.1; resolução-proxyadequada; NOT_EXECUTED.
- `analytic_valley`: PDE; classe`EXPLORATORY_3D_PRESCRIBED_GEOMETRY`; RAM7.39GiB, disco7.95GiB; grade[105, 105, 79]; 1041volumes; dt planejado antes do CFL0.1; resolução-proxyNÃO certificada; NOT_EXECUTED.
- `historic_extrusion15`: PDE; classe`EXPLORATORY_3D_PRESCRIBED_GEOMETRY`; RAM7.39GiB, disco7.95GiB; grade[105, 105, 79]; 1041volumes; dt planejado antes do CFL0.1; resolução-proxyNÃO certificada; NOT_EXECUTED.
- `historic_extrusion30`: PDE; classe`EXPLORATORY_3D_PRESCRIBED_GEOMETRY`; RAM7.39GiB, disco7.95GiB; grade[105, 105, 79]; 1041volumes; dt planejado antes do CFL0.1; resolução-proxyNÃO certificada; NOT_EXECUTED.

## valleys_historical

- `valley_flat`: PDE; classe`HISTORICAL_HEIGHT_EXPLORATORY_3D_EXTENSION`; RAM22.05GiB, disco23.79GiB; grade[161, 161, 105]; 1041volumes; dt planejado antes do CFL0.1; resolução-proxyadequada; NOT_EXECUTED.
- `valley_G_V1a12_sp1`: PDE; classe`HISTORICAL_HEIGHT_EXPLORATORY_3D_EXTENSION`; RAM22.05GiB, disco23.79GiB; grade[161, 161, 105]; 1041volumes; dt planejado antes do CFL0.1; resolução-proxyadequada; NOT_EXECUTED.
- `valley_G_V2n_sp1`: PDE; classe`HISTORICAL_HEIGHT_EXPLORATORY_3D_EXTENSION`; RAM22.05GiB, disco23.79GiB; grade[161, 161, 105]; 1041volumes; dt planejado antes do CFL0.1; resolução-proxyadequada; NOT_EXECUTED.
- `valley_G_V2o_sp1`: PDE; classe`HISTORICAL_HEIGHT_EXPLORATORY_3D_EXTENSION`; RAM22.05GiB, disco23.79GiB; grade[161, 161, 105]; 1041volumes; dt planejado antes do CFL0.1; resolução-proxyadequada; NOT_EXECUTED.

## vertical_boundary_control

- `sponge_reference`: PDE; classe`EXPLORATORY_3D_PRESCRIBED_GEOMETRY`; RAM7.39GiB, disco7.95GiB; grade[105, 105, 79]; 1041volumes; dt planejado antes do CFL0.1; resolução-proxyadequada; NOT_EXECUTED.
- `boundary_dirichlet`: PDE; classe`EXPLORATORY_3D_PRESCRIBED_GEOMETRY`; RAM7.39GiB, disco7.95GiB; grade[105, 105, 79]; 1041volumes; dt planejado antes do CFL0.1; resolução-proxyadequada; NOT_EXECUTED.
- `boundary_neumann`: PDE; classe`EXPLORATORY_3D_PRESCRIBED_GEOMETRY`; RAM7.39GiB, disco7.95GiB; grade[105, 105, 79]; 1041volumes; dt planejado antes do CFL0.1; resolução-proxyadequada; NOT_EXECUTED.
- `domain_xy150`: PDE; classe`EXPLORATORY_3D_PRESCRIBED_GEOMETRY`; RAM9.66GiB, disco10.50GiB; grade[121, 121, 79]; 1041volumes; dt planejado antes do CFL0.1; resolução-proxyadequada; NOT_EXECUTED.
- `sponge_width15`: PDE; classe`EXPLORATORY_3D_PRESCRIBED_GEOMETRY`; RAM7.39GiB, disco7.95GiB; grade[105, 105, 79]; 1041volumes; dt planejado antes do CFL0.1; resolução-proxyadequada; NOT_EXECUTED.
- `sponge_strength025`: PDE; classe`EXPLORATORY_3D_PRESCRIBED_GEOMETRY`; RAM7.39GiB, disco7.95GiB; grade[105, 105, 79]; 1041volumes; dt planejado antes do CFL0.1; resolução-proxyadequada; NOT_EXECUTED.
- `asymmetric_z_intervention`: PDE; classe`EXPLICIT_ASYMMETRIC_BOUNDARY_INTERVENTION`; RAM9.66GiB, disco10.23GiB; grade[105, 105, 105]; 1041volumes; dt planejado antes do CFL0.1; resolução-proxyadequada; NOT_EXECUTED.

## vertical_symmetric

- `flat_z25`: PDE; classe`EXPLORATORY_3D_PRESCRIBED_GEOMETRY`; RAM3.38GiB, disco3.31GiB; grade[105, 105, 33]; 1041volumes; dt planejado antes do CFL0.1; resolução-proxyadequada; NOT_EXECUTED.
- `flat_z60`: PDE; classe`EXPLORATORY_3D_PRESCRIBED_GEOMETRY`; RAM7.39GiB, disco7.95GiB; grade[105, 105, 79]; 1041volumes; dt planejado antes do CFL0.1; resolução-proxyadequada; NOT_EXECUTED.
- `flat_z100`: PDE; classe`EXPLORATORY_3D_PRESCRIBED_GEOMETRY`; RAM11.76GiB, disco13.03GiB; grade[105, 105, 129]; 1041volumes; dt planejado antes do CFL0.1; resolução-proxyadequada; NOT_EXECUTED.

[D] Volumes guardamφ/p e são reconstruídos paraJ/e em streaming; isso reduz disco em comparação a guardar todos os derivados. A reconstrução nativa deJ/e pode exigir novamente a memória do operador. Cortes/anéis e séries dos receptores mantêm a cadência diagnóstica. O refinamento completo usa volumes0,25 em todas as suas malhas; demais famílias usam0,5. Não se muda a cadência automaticamente para caber no disco. NPZ é sem perda sobre os arrays float32 declarados; checkpoints e ledger são float64.
