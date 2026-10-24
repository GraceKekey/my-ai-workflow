# HRF B39V — SPIRAL Diagnostics v0.1

[D] **PRÉ-REGISTRADO — GRANDES SIMULAÇÕES CIENTÍFICAS NÃO EXECUTADAS.** Esta derivação acrescenta observação volumétrica e diagnósticos à bancada integral, sem alterar o diretório anterior. Testes unitários e exemplos de smoke técnico mínimo são identificados separadamente. Não se pressupõe uma espiral ascendente.

Comece por PROTOCOLO_SPIRAL.md, PRESETS_E_RECURSOS.md e LIMITES_DA_INTERPRETACAO.md. Código novo e núcleo reutilizado estão em hrf_integral/. Fontes originais e seus hashes estão em historico/ e reference/. As 468 posições e limiares recuperados estão em inputs/. Os dados grandes históricos não são necessários aos novos comandos; não foram copiados, alterados ou reexecutados. As CLIs antigas completas, preservadas por proveniência, exigem o pacote integral anterior.

## Instalar e testar

Python 3.11+; a verificação nesta entrega usou Python 3.12 e as versões registradas no relatório técnico.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python -I scripts/test.py
```

No Windows: `.venv\Scripts\Activate.ps1` após criar o venv; use `python` em vez de `python3`. FFmpeg é opcional para MP4. GIF e PNG usam Pillow/Matplotlib e não dependem dele.

## Planejar sem integrar

```bash
python -m hrf_integral.run --config config/spiral_standard.json --output results/spiral_standard
```

O comando imprime custos estimados e grava plan.json; **sem `--execute` não inicia a PDE**. `--case` permite selecionar um caso do plano. A malha localmente refinada é retangular graduada, sem AMR/hanging nodes. Saídas volumétricas podem exigir dezenas de GiB; os limites e o total do sweep são conferidos antes de alocar.

## Executar posteriormente em ambiente autorizado

```bash
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python -m hrf_integral.run --config config/spiral_standard.json --output results/spiral_standard --execute
python -m hrf_integral.plot3d --input results/spiral_standard --output figures/spiral_standard
python -m hrf_integral.spiral_report --input results/spiral_standard --output reports/spiral_standard
```

Alternativa com Python isolado: `python -I scripts/spiral.py run ...`, `plot3d ...`, `spiral_report ...`. scripts/run_spiral_linux.sh e run_spiral_windows.ps1 recebem preset e saída; por padrão usam apenas spiral_smoke. O código/fonte e a configuração fazem parte da identidade do checkpoint. Retomar o mesmo comando verifica integridade e aproveita casos prontos ou o último frame atômico. Para parâmetros alterados use saída nova e nova identificação exploratória.

## Exportar

```bash
python -m hrf_integral.export_data --input results/spiral_standard/splus --frame 10 --format csv --output exports/frame10.csv
python -m hrf_integral.export_data --input results/spiral_standard/splus --frame 10 --kind phase --slice-index 4 --format json --output exports/phase_z0.json
python -m hrf_integral.export_data --input results/spiral_standard/splus --kind diagnostics --format npz --output exports/diagnostics.npz
```

JSON/CSV extensos têm guarda `--max-bytes`. Volumes e cortes já são gravados em NPZ; PNG/GIF/MP4 são produzidos pelo plotter. Diagramas, tabelas e relatórios distinguem chegada do campo, resposta seletiva, relé e hipótese DIO. Uma fase indefinida é mascarada, não inventada.

Os relatórios técnicos e exemplos desta entrega, se presentes, estão em reports/technical_smoke e examples/technical_smoke. Nenhuma imagem desse smoke certifica uma espiral ou a transferência histórica. O gate de holografia HRF continua `BLOCKED_NO_VALIDATED_HOLOGRAPHIC_DICTIONARY`.
