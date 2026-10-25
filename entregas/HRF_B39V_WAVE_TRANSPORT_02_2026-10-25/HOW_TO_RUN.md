# Instalação, validação, planejamento e execução posterior

**HRF-B39V-3P1-WAVE-TRANSPORT-02 · v0.1 · 25/10/2026 (Brasil)**

**CÓDIGO PREPARADO — PRÉ-REGISTRO — NOVAS SIMULAÇÕES CIENTÍFICAS NÃO EXECUTADAS.**

[D] Descompacte o ZIP e entre em HRF_B39V_WAVE_TRANSPORT_02. Python testado3.12.14, NumPy2.2.6, SciPy1.15.3, Matplotlib3.10.3, Pillow12.3.0. Sem dependência de pytest para o comando test (unittest padrão); pytest pode coletar os mesmos testes se instalado. ffmpeg é opcional para MP4. O arquivo requirements.lock.txt registra as dependências exatas.

```bash
python -m venv .venv
# Linux/macOS
source .venv/bin/activate
# Windows, em alternativa: .venv\Scripts\activate
python -m pip install -r requirements.txt
python -I scripts/verify_manifest.py
python -I scripts/wt02.py validate
python -I scripts/wt02.py plan --config configs/vertical_medium.json --output ../WT02_PLAN
python -I scripts/wt02.py test --output ../WT02_TESTS
```

[D] Cada teste exige diretório de saída novo. `test` limita-se aos testes do projeto, com referências matemáticas pequenas. Nada é executado na instalação/importação. `plan --execute` continua sendo apenas plan, por segurança. Exit codes:0 planejamento/êxito,1 teste/validação falhou,2 recursos/erro numérico/software,3 input requerido ausente,4 congelamento alterado.

[D] Depois de autorização futura para ciência, execute explicitamente:

```bash
python -I scripts/verify_manifest.py hashes_antes_da_execucao.txt
python -I scripts/wt02.py run --config configs/vertical_medium.json --output results/vertical_medium --execute
```

[D] Esta linha não foi executada nesta entrega. Não aciona download nem execução remota. Omissão de --execute só grava um plano. Para uma família, use --case ID para admitir/rodar um caso de cada vez. Relançar o mesmo comando retoma o checkpoint atômico ou reconhece um COMPLETION válido; código/config diferentes exigem nova saída e novo pré-registro. Não sobrescreva um histórico.

```bash
python -I scripts/wt02.py analyze --input results/vertical_medium/flat_z60 --output analysis/flat_z60
python -I scripts/wt02.py visualize --input results/vertical_medium/flat_z60 --analysis analysis --output figures
```

[D] Analyze não resolve PDE; visualize lê campos reais. CSV/NPZ e PNG/GIF/MP4 são exportados. Para comparar dois casos, forneça ambos em --input, análises por nome de caso na mesma pasta e escala comum automática. A maior parte dos controles tem CLI completa; exemplo:

```bash
python -I scripts/wt02.py compare --first results/P/CASO1 --second results/P/CASO2 --allow grid.shape --output analysis/compare_space.json
python -I scripts/wt02.py basic-evidence --input results/P/CASO1 --analysis analysis/CASO1 --output analysis/basic_evidence.json
python -I scripts/wt02.py control-evidence --first results/P/CASO1 --second results/P/CASO2 --analysis-first analysis/CASO1 --analysis-second analysis/CASO2 --allow grid.shape --gate SPATIAL_CONVERGENCE --output analysis/spatial_evidence.json
python -I scripts/wt02.py reference-evidence --spatial results/ref/reference_space_9 results/ref/reference_space_17 results/ref/reference_space_33 --temporal results/ref/reference_time_0.05 results/ref/reference_time_0.025 results/ref/reference_time_0.0125 --output analysis/reference_evidence.json
```

[D] Use as CLIs análogas para TEMPORAL_CONVERGENCE (--allow field.dt), BOUNDARY_ROBUSTNESS (--allow field.boundary) e flow-evidence após rastrear curvas. Evidências de fluxo precisam reanálises sem --evidence inicialmente; depois merge-evidence/certify e nova análise --flowlines --evidence para aplicar todos os gates. Os contrastes devem compartilhar grade, ROI e tempos registrados, e permitir somente a variável efetivamente mudada. Não misture independências.

```bash
python -I scripts/wt02.py merge-evidence --input analysis/reference_evidence.json analysis/basic_evidence.json analysis/spatial_evidence.json analysis/temporal_evidence.json analysis/boundary_evidence.json analysis/flow_evidence.json --output analysis/all_evidence.json
python -I scripts/wt02.py analyze --input results/P/CASO1 --output analysis/CASO1 --flowlines --evidence analysis/all_evidence.json
```

[D] Dados antigos fornecidos depois: baseline_reanalysis aceita uma pasta com splus/sminus ou um caso. O receptor replay exige um único caso completo e o canal incidente original, não figuras ou apenas summary.json:

```bash
python -I scripts/wt02.py reanalyze --input /caminho/spiral_standard --output analysis/baseline
python -I scripts/wt02.py plan --config configs/receiver_frequency_sweep.json --input /caminho/splus --output ../WT02_REPLAY_PLAN
# Apenas após autorização posterior para a varredura científica:
python -I scripts/wt02.py run --config configs/receiver_frequency_sweep.json --input /caminho/splus --output results/replay --execute
```

[D] A interface equivalente, sem isolamento de sys.path, é `python -m hrf_b39v.cli validate|plan|test|run|analyze|visualize ...` a partir da raiz. O launcher -I é recomendado por controlar o caminho e BLAS1. Scripts `bash scripts/run_linux.sh ...` e `scripts\run_windows.bat ...` encaminham os mesmos argumentos; nenhum inicia run por padrão. Instalação é por requirements na raiz extraída, não por um wheel que omita dados históricos.
