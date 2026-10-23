# HRF-B39V-BULK-3P1 — Revisão e execução

Data: 2026-10-22_224541, America/Sao_Paulo. Autor HRF: Mario José do Canto Filho, MD. Revisão e execução: Codex.

## Objetivo e escopo
[M] Executar o baseline KG volumétrico em uma métrica 3+1 prescrita, após revisão do código e correção de defeitos autorizada pelo usuário. Este pacote não implementa holografia, RT/HRT, HKLL ou uma reprodução integral da B39V.

## Revisão anterior à execução
[D] O usuário autorizou revisar, corrigir e reexecutar em caso de erro. O índice 3D do operador de fluxo foi conferido e a PDE concorda com a métrica declarada: u_tt = N/c² div(Nc² grad u) − (Ncm)²u, com c=1/z e L=1. A força implementada é um drive de aceleração de coordenada; não há normalização independente de uma fonte covariante J.
[M] Foram corrigidas lacunas de software, sem alterar parâmetros ou PDE: validação de entradas e receptores fora do domínio; limite de estabilidade que inclui o termo de massa; detecção de estados não finitos; armazenamento obrigatório do instante final; coordenadas reais dos receptores, configuração e hash da fonte executada na saída. A gaussiana espacial da fonte passou a ser pré-calculada, sem mudança de valores. energy_proxy foi identificado explicitamente como integral de u²+v², não energia KG conservada.
[D] Preservados: original/src/bulk3d.py, ZIP de entrada, manifesto inicial e todas as referências históricas. A única alteração entre os 15 arquivos do manifesto é src/bulk3d.py. Patch em auditoria/alteracoes.patch; hashes antigo/novo em auditoria/hashes_revisao.json.

## Testes
[M] Seis testes aprovados: entradas inválidas, receptor fora do domínio, instabilidade de massa que o CFL antigo não rejeitava, instante final fora da cadência, referência numérica independente/convergência e regressão do benchmark original.
[M] O controle independente usa malha plana Dirichlet 5³ interior, Laplaciano por produtos de Kronecker e DOP853, contra o Verlet revisado. Erros máximos: 1,30770e−7 (dt=0,02) e 3,26869e−8 (dt=0,01), razão 4,00067. Simetria dos receptores ±x e valor zero na fronteira passaram. Esse teste confirma convergência temporal no problema semidiscreto plano; não certifica convergência espacial da geometria AdS com vale.
[M] O teste de regressão obteve igualdade exata das 13 observações entre código original e revisado para a configuração fornecida. As correções não mudaram as curvas desse benchmark. Logs em auditoria/testes_log.txt e testes reproduzíveis em testes/testar_bulk3d.py.

## Execução e parâmetros
[D] requirements.txt atendido e execução revisada concluída, ambos exit 0. Comando: python -I src/bulk3d.py --config config/benchmark.json --output results. Nenhuma falha de execução exigiu nova correção. Python 3.12.14, NumPy 2.2.6, SciPy 1.15.3; BLAS/OMP/MKL limitados a uma thread.
[M] Configuração original: 25×25×17, AdS4 probe, dt=0,015, 240 passos, 13 observações, quatro receptores, massa 1,6 e frequência 1,85. Parâmetros físicos e configuração preservados.

## Resultados
[D] Classe do programa: **NUMERICAL_PROBE_ONLY_NOT_HOLOGRAPHIC**. bulk_pde=COMPUTED, holographic_dictionary=BLOCKED, RT_HRT/HKLL=NOT_IMPLEMENTED e B39V_exact_reproduction=NOT_TESTED.
[M] Todos os estados permaneceram finitos. Lapso mínimo 0,99521223. dt·ω_limite=0,0648767, abaixo de 2 para o critério de Verlet. Valores finais dos receptores: [1.6648853446658042e-06, 1.4189656137338747e-08, 1.6178102999507452e-07, 1.6948973240190146e-07].
[M] Coordenadas reais na grade: [[6.0, 0.0, 3.25], [8.0, 0.0, 3.25], [6.0, 3.0, 3.25], [6.0, 0.0, 6.25]]. Os pedidos em z=3 e z=6 foram amostrados em z=3,25 e z=6,25; isso agora consta explicitamente na saída.

## Limitações e interpretação
[?] A janela termina em t=3,6, enquanto a fonte é cortada em t=8. Não foi estendida a duração nem mudado seu envelope: o código original usa uma rampa sin² e corte abrupto. Não há análise de chegada após o pulso, de foco/sombra, de disparos, energia conservada, reflexões ou convergência espacial neste benchmark. A gaussiana tem caudas não compactas; amplitudes pequenas precoces não são uma medida de velocidade de frente causal.
[D] Não foi atribuído PASS_BASELINE_NUMERICAL do protocolo: a convergência temporal foi controlada em um problema de referência, mas a convergência espacial e os demais controles da configuração física permanecem por demonstrar. Status COMPUTED não certifica esses testes ausentes.
[H] A geometria foi introduzida, não reconstruída. Os resultados não estabelecem bulk emergente, dualidade AdS/CFT, reprodução quantitativa da B39V ou DIO/GMFt.

## Entrega
Pacote autocontido com entrada e fonte originais, código revisado, testes, patch, documentação, configuração, observáveis JSON/CSV/PNG, relatórios, logs, ambiente e manifestos. STATUS.json e documentos históricos com NÃO EXECUTADO foram preservados; os resultados desta tentativa estão em results/ e neste relatório.
