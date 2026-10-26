# HRF-BH-COSMO-01 — reprodução e verificação independente

**26/10/2026 — EXECUÇÃO CONCLUÍDA. Código original preservado.**

[M] Foi executada a totalidade dos cálculos implementados no pacote recebido, em processo Python isolado (`python3 -I bench_bh_cosmologia.py`), sem otimização que desative assert. Biblioteca padrão apenas. Saída 0, nenhum erro em stderr, tempo de execução 0.054305s nesta máquina. Não foi necessária correção de código.

[D] O ZIP de entrada passou no CRC; os 9 arquivos do manifesto de entrada conferiram SHA-256. O código reproduzido tem SHA-256 `2c5fb4b13d142257134662fe7d31de14ebe3858e1a79d61dc2f2071833ab3fc8`. O original, incluindo seus resultados anteriores, permanece em original/ e o próprio ZIP de entrada está preservado em entrada/.

[M] Os cinco arquivos de resultados produzidos e o stdout JSON ficaram **idênticos byte a byte** aos recebidos. Valores arredondados nos CSVs mantêm a precisão definida pelo código, sem alteração de parâmetros ou tolerâncias. Logs, Python/OS/comando e datas UTC estão em reproducao/execucao.json.

| Operação implementada | Verificação desta execução | Resultado |
|---|---|---|
| Escala de curvatura FLRW | 4 valores de abs(Omega_k); conferência independente Decimal com 50 dígitos | PASS matemático condicional |
| Visibilidade paramétrica toy | 4 combinações A/p; solução algébrica independente | PASS matemático, sem limite observacional |
| Rotação rígida | 4 pares; identidade zero também em aritmética racional exata | PASS do controle negativo |
| Rotação diferencial | 8 posições; fórmula fechada independente | 4 aproximações e 4 afastamentos |
| Equivalência Schwarzschild | M=c²r/(2G), conferência Decimal com 50 dígitos | PASS dimensional condicional |

[M] Com H0=67.4km/s/Mpc e Robs=46 Gly assumidos: raio de Hubble14.507302992296575 Gly; raios de curvatura205.164,324.393,458.761 e1450.730 Gly para |Omega_k|=.005,.002,.001,.0001. O valor piRcurv só representa a distância geodésica máxima se for assumida a3-esfera fechada simplesmente conexa (Omega_k negativo na convenção usual), não um diâmetro de buraco negro.

[M] Na equivalência dimensional com rs=46 Gly assumido, M=1.473564482231e+23Msun. Esse número não estima a massa de um universo interior. As velocidades e posições do toy de rotação estão em unidades arbitrárias, não são observações de galáxias.

[D] A conferência independente não importa o programa original, pois ele contém cálculos e gravação de arquivos no nível do módulo. Assim, a reprodução principal foi executada uma única vez e registrada. A verificação separada usa AST para ler constantes, Decimal de 50 dígitos, identidade de rotação rígida com Fractions e a expressão diferencial (omega_obj−omega_obs)(x_obs*y_obj−y_obs*x_obj)/distancia. Arredondamentos finais de 3 e 9 casas decimais foram verificados nas respectivas escalas.

[?] BHC-01 documental do relatório recebido **não foi revalidado**: os capítulos internos citados não vieram no ZIP e não se afirma que foram lidos nesta reprodução. As referências externas e seus dados observacionais não foram baixados nem ajustados. O relatório original foi preservado, sem trocar seus gates por aprovações novas.

[?] BHC-06–09 continuam NOT_TESTED: o pacote não contém uma métrica de interior cosmológico, solução Einstein/Kerr, integração relativística 4D, ajuste CMB/BAO/SNe/H(z) ou explicação dinâmica da expansão acelerada. A proposta BHC-REL-02 não foi implementada nem executada por esta reprodução. Não há condições físicas completas no pacote para essa etapa.

[M/?] **Conclusão mantida: o tamanho real de um universo no interior de um buraco negro não é identificável por esta bancada.** Os controles confirmam as operações matemáticas condicionais fornecidas, sem validar a hipótese cosmológica. Não há demonstração de DIO/GMFt ou de dicionário holográfico.

[D] Entrega: código original, ZIP original, resultados anteriores, resultados reproduzidos, stdout/stderr, comparação byte a byte, verificador independente, recibos e manifesto SHA-256. Nenhum histórico anterior foi sobrescrito.
