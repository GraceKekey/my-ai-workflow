# Presets e estimativas antecipadas de recursos

**HRF-B39V-3P1-WAVE-TRANSPORT-02 · v0.1 · 25/10/2026 (Brasil)**

**CÓDIGO PREPARADO — PRÉ-REGISTRO — NOVAS SIMULAÇÕES CIENTÍFICAS NÃO EXECUTADAS.**

[D] Estimativas sem montagem de malha/PDE. RAM é pico conservador por caso: 8500·N +512MiB para FEM/métrica/matrizes/estágios; disco é soma bruta sem presumir compressão. Proxy de CPU =240·N·passos, não FLOPS exatos ou segundos. CPU em horas não foi extrapolada de testes minúsculos. Python/NumPy operam com BLAS1. Os arquivos por caso contêm a estimativa exata, inclusive checkpoint e metadados.

| Preset | casos | RAM pico GiB | disco família GiB | operações proxy |
|---|---:|---:|---:|---:|
| baseline.json | 1 | 1.67 | 1.42 | 1.85e+11 |
| baseline_reanalysis.json | 1 | 4.00 | 1.00 | 0 |
| boundary_controls.json | 7 | 9.66 | 60.49 | 8.32e+12 |
| flat_rotation_pair.json | 2 | 7.39 | 15.90 | 2.17e+12 |
| historical_valleys.json | 4 | 22.05 | 95.17 | 1.36e+13 |
| negative_controls.json | 6 | 7.39 | 47.71 | 6.52e+12 |
| receiver_frequency_sweep.json | 1 | 2.00 | 1.00 | 0 |
| refinement.json | 9 | 56.17 | 131.45 | 1.21e+13 |
| synthetic_valley.json | 2 | 7.39 | 15.90 | 2.17e+12 |
| vertical_long.json | 1 | 11.76 | 13.03 | 1.77e+12 |
| vertical_medium.json | 1 | 7.39 | 7.95 | 1.09e+12 |
| vertical_short.json | 1 | 3.38 | 3.31 | 4.54e+11 |

[D] Os replays representam uma entrada com9 variantes, sem PDE; valores de custos dependem dos dados reais e têm segunda admissão. Baseline reanalysis lê dados existentes e também passa por admissão de headers ZIP. Teto de RAM por execução24GiB, reserva de disco2GiB, limite de operações5e13; outras cotas exatas estão em cada JSON. O cenário de malha209×209×161 excede24GiB e será BLOCKED_RESOURCES. A máquina atual tem32GiB de RAM configurada e4 CPUs, mas recursos efetivamente livres são conferidos novamente, inclusive cgroup. Nenhum parâmetro é reduzido para liberar execução.

[D] Os custos incluem φ e p volumétricos, cortes e canais. O checkpoint é estado atual +ledger e identidade, atômico; o orçamento120·N mais margens cobre campos de grade/checkpoint. Compressão é sem perda. Amostragem float32 dos volumes é explicitada: é precisão reduzida em relação à evolução float64, nunca chamada compressão sem perda da precisão original. As figuras usam no máximo32 pontos por eixo e8000 triângulos por superfície; isso não altera os dados usados nos diagnósticos.

[D] Lista exata de IDs por arquivo:

- `baseline.json`: baseline_documented_configuration.

- `baseline_reanalysis.json`: archived_spiral_only.

- `boundary_controls.json`: sponge_reference, boundary_dirichlet, boundary_neumann, domain_xy150, sponge_width15, sponge_strength025, asymmetric_z_intervention.

- `flat_rotation_pair.json`: splus, sminus.

- `historical_valleys.json`: valley_flat, valley_G_V1a12_sp1, valley_G_V2n_sp1, valley_G_V2o_sp1.

- `negative_controls.json`: zero_source, no_rotation, vertical_parity, passive_historical_control, closed_no_sponge, monopole_control.

- `receiver_frequency_sweep.json`: fixed_incident_signal_replay.

- `refinement.json`: reference_space_9, reference_space_17, reference_space_33, reference_time_0.05, reference_time_0.025, reference_time_0.0125, full_space_53, full_space_105, full_space_209.

- `synthetic_valley.json`: exploratory_flat, analytic_valley.

- `vertical_long.json`: flat_z100.

- `vertical_medium.json`: flat_z60.

- `vertical_short.json`: flat_z25.
