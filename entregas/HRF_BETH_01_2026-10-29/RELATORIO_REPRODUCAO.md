# HRF-BETH-01 — reprodução do controle Maxwell

**29/10/2026 · EXECUÇÃO CONCLUÍDA · 11/11 testes passaram.**

## Objetivo e escopo

[M] Reproduzir integralmente o programa recebido para torque material em placa birrefringente ideal. Código, parâmetros e critérios foram preservados; nenhum ajuste pós-resultados foi aplicado. Este é um controle clássico de Maxwell em passagem única, não uma reprodução instrumental completa do experimento Beth (1936).

## Integridade e execução

[D] ZIP de entrada SHA-256: `76d786b491aac4c765915f2754129adddef9cece4ddecfad9facb88b0635ff40`. CRC válido. Manifesto geral: 20 arquivos conferidos; congelamento de protocolo/código/testes: 4 arquivos conferidos antes e depois da execução. O ZIP original e todos os arquivos recebidos estão preservados.

[M] Ambiente: Python 3.12.14, NumPy 2.2.6, SciPy 1.15.3, Matplotlib 3.10.3. BLAS/OMP limitados a 1 thread. Instalação adicional não foi necessária nesta máquina. Testes executados em 0.6309s; bancada e quatro figuras em 2.9174s. Ambos os processos terminaram com código 0; os comandos e o ambiente completos estão em auditoria/execucao.json.

```text
python -I -m unittest discover -s tests -v
python -I run_bench.py --out resultados
```

[D] A execução usou uma cópia nova em reproducao/. Os resultados anteriores em original/ não foram sobrescritos. A avaliação JSON foi regenerada com data e ambiente desta execução. O arquivo de relatório de execução do pacote recebido continua em original/; este documento é o relatório da reprodução.

## Resultados

| Medida | Resultado reproduzido |
|---|---:|
| Potência |10mW|
| Comprimento de onda |532nm|
| Índices próprios |1.50 e1.55|
| Área transversal |1mm²|
| Espessura de meia onda calculada |5.32µm|
| Pontos na integração principal |1025|
| Torque material integrado |5.648598625673e-18 N m|
| Referência2P/omega |5.648603056244e-18 N m|
| Torque por diferença de fluxos |5.648603056244e-18 N m|
| Erro relativo contra2P/omega |7.843658064483e-07|
| Erro relativo de balanço |7.843658067210e-07|
| Razão volume/referência |0.999999215634|
| Inversão de sinal do torque |erro relativo0.0|
| StokesS3, circular+ |+1 →−1|
| Convergência monotônica |PASS|
| Testes unitários |11/11 PASS|
| Gate global do controle |PASS|
| Ponte HRF/Capítulo2 →Beth |NOT_EXECUTED|

[M] O limiar relativo congelado 5e-5 foi satisfeito sem alteração. Os testes também verificam potência/retardo nulos, polarizações lineares, linear45° com quarto de onda não nulo, escalas com potência/comprimento de onda e resposta ilustrativa do pêndulo.

## Comparação com os arquivos recebidos

[M] Os seis CSVs foram reproduzidos **byte a byte**. Parâmetros, valores principais e reversos, referência analítica, checks, limiares, veredito e gates do JSON também coincidem exatamente. Data/ambiente do JSON e logs são registros novos; não se afirma identidade binária de PNGs/logs entre ambientes diferentes.

[D] As quatro figuras foram regeneradas a partir dos cálculos e verificadas como PNGs válidos. A avaliação consolidada é condicionada também aos testes unitários concluídos; o PASS isolado emitido pelo runner não foi usado como substituto do teste.

## Conferência analítica adicional

[F/M] Conferência por fórmulas fechadas, sem importar ou alterar o módulo congelado: para as convenções da fonte nx<ny, torque contínuo circular± é ±(P/omega)(1−cosδ), e linear45° é −(P/omega)sinδ. Os resultados de integração trapezoidal têm fator(h/2)cot(h/2), com h=δ/(N−1). As 165 linhas de varredura foram conferidas. A diferença máxima normalizada por P/omega foi7.0919e-15 no volume e2.6731e-14 no fluxo.

[M] Ordens sucessivas de convergência: 2.00069577, 2.00017385, 2.00004346, 2.00001086, 2.00000272, 2.00000068; consistentes com ordem 2 da regra trapezoidal. A trajetória mecânica foi comparada à solução analítica do oscilador subamortecido sob torque constante; erro absoluto máximo5.8775e-14rad. Esses diagnósticos adicionais não substituem nem alteram gates pré-registrados, e compartilham as mesmas hipóteses ópticas/mecânicas, sem evidência experimental independente.

## Limites e proveniência

[?] Os documentos internos HRF/B41 e a fonte Beth citados no pacote não foram objeto de nova auditoria documental nesta reprodução. O estado B41-M02 informado no pacote foi preservado, não novamente testado ou revalidado.

[M/?] **PASS restrito ao controle eletromagnético idealizado.** Não foram modeladas reflexões Fresnel, perdas, dispersão, bordas ou o arranjo multipasse completo de Beth. O pêndulo usa constantes sintéticas; não valida sensibilidade instrumental. Não foi executada a conexão com o setor relacional, nem derivado spin quântico/hbar. `gate_hrf_beth` permanece NOT_EXECUTED.

[D] Nota de compatibilidade: requirements.txt original declara NumPy>=1.26, mas o código utiliza np.trapezoid, disponível a partir de NumPy 2.0. Isso não impediu esta execução, feita com NumPy 2.2.6. O requisito original foi preservado para manter os hashes; para repetir o ambiente, use requirements_reproducao.lock. Não se deve atribuir uma eventual falha com NumPy 1.26 à física da bancada.
