# HRF-HOLO-B39V-02 — Falha de execução do código original

Data: 2026-10-22_215409, America/Sao_Paulo. Autoria HRF: Mario José do Canto Filho, MD. Execução: Codex.

## Objetivo e protocolo
[M] Executar os comandos fornecidos: instalar requirements.txt e rodar `python -m hrf_boundary.run --config config/benchmark.json --output results`. Código, configuração e nove hashes originais preservados, conferidos antes e depois. BLAS/OMP/MKL com uma thread por processo.

## Parâmetros
[M] Nx=18, Ny=6, κ=1, m=0,35, 108 osciladores; faixas 2 a 7, treino 2/4/6 e teste 3/5/7. Arquivo config/benchmark.json intacto.

## Resultado da execução
[D] Dependências instaladas/atendidas: exit 0. Benchmark original: exit 1, `ValueError: K non positive` em harmonic_covariances, antes de calcular covariâncias, entropias ou gates. Não foram produzidos resultados científicos, resultados.json ou RESUMO.md pelo executor. A pasta results foi apenas criada pelo programa.
[M] NumPy 2.2.6, SciPy 1.15.3, Python 3.12.14. Logs em auditoria/pip_install.txt e auditoria/execucao_log.txt.

## Diagnóstico separado da rodada
[M] O índice de sítio é definido como i=x*Ny+y. Entretanto, na montagem dos vizinhos, `hrf_boundary/run.py` usa `K[i,xx]-=kappa`, ignorando yy. Assim as interações são inseridas nas colunas 0…17 em vez de nos 108 índices de sítios. A matriz resultante não é a matriz simétrica do Hamiltoniano declarado.
[M] Erro máximo de simetria |K−Kᵀ|: 2,0. O menor valor devolvido por scipy.linalg.eigh, que interpreta o triângulo inferior como uma matriz simétrica, foi −9,9614289515. A menor raiz da parte simetrizada é −3,5704527473. Esses valores são diagnóstico do defeito, não evidência de instabilidade do modelo harmônico proposto.

A correção de indexação a revisar em nova versão seria:

```diff
-                K[i,xx]-=kappa
+                K[i,xx*ny+yy]-=kappa
```

[D] A fonte original não foi alterada e não foi executada uma bancada corrigida. Não foi ajustado qualquer parâmetro ou tolerância. tools/diagnosticar_matriz.py registra somente a inspeção algébrica da matriz defeituosa.

## Interpretação e limites
[?] Os testes quânticos, pureza, informação mútua e forma de faixa não foram alcançados; não há PASS_NUMERIC para esta rodada. O programa abortou antes de escrever seus gates, portanto EXECUTION_FAILED_ORIGINAL_CODE é um rótulo deste relatório, não uma saída de avaliação científica do programa.
[H] Nenhuma inferência holográfica, reconstrução bulk, vínculo com B39V ou DIO/GMFt foi testada. Uma nova execução exige uma versão corrigida identificada separadamente; os hashes atuais continuam documentando o pacote que falhou.

## Arquivos
Pacote autocontido com entrada original, código, protocolo, configurações, logs de instalação/execução, diagnóstico, ambiente, hashes antes/depois e este relatório. STATUS.json original com NOT_EXECUTED é um registro histórico preservado; o estado desta tentativa está em auditoria/status_execucao.json.
