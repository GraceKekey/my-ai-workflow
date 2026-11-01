# HRF-POL-GEOMETRY-01 — relatório de auditoria

[D] Fontes locais somente. O prompt original está em documentos/PROMPT_ORIGINAL.md; inventário com hashes em auditoria/INVENTARIO_FONTES.json. Capítulo 0.1 v0.2 relido integralmente. Capítulo 2 v1.5 lido integralmente no ciclo anterior e seções pertinentes relidas neste ciclo. Não se alegou acesso ao Google Drive.

[D] B41L original e dez módulos POL anteriores preservados, hashes em HASHES_FONTES_CONGELADAS.txt; os 43 hashes originais B41L também conferem. O kernel de quatro instruções e a montagem Whitney são reutilizados. Os adaptadores alteram apenas coordenadas/topologia de entrada, com escolhas de desempate documentadas. Nenhum solver Maxwell/Jones substituiu a dinâmica.

[M] 47 testes originais B41L e 12 testes de interfaces passaram. Os novos controles incluem fonte nula, Gauss, dois sinais helicoidais medidos, energia inicial, coordenação, fechamento periódico, espectro discreto Verlet, identidade V0 e retomada de checkpoint bit a bit. A fumaça tem cinco casos separados; a principal tem exatamente 34 (4/8/8/8/6). Não houve expansão para milhares de casos.

[D] Falhas de desenvolvimento preservadas: solve batched no NumPy 2 corrigido antes da fumaça; validação do padding do casco convexo antecipada incorretamente em G5 N216, corrigida para aplicar primeiro a mesma seleção de caixa do construtor original. Logs e fontes das duas revisões em auditoria/correcao_preexecucao_01 e 02. Nenhum ponto ou tetraedro do domínio central foi removido.

[D] As 16 malhas principais passaram geometria/topologia e esferas vazias. Pontos e metadados foram selados antes da principal (48 entradas). Nenhum código em src/, configuração ou critério foi editado depois da fumaça/principal. Todos os 34 selos de conclusão e os SHA-256 dos campos e avaliações foram conferidos nesta auditoria.

[M] Ambiente e admissão estão em resultados/principal/preparacao.json. Python 3.12.14, NumPy 2.2.6, SciPy 1.15.3, quatro CPUs/processos, uma thread por biblioteca. Orçamento conservador de RAM 7.516.192.768 bytes e disco 1.761.750.320 bytes. A execução principal levou 44,982 s; os tempos de geração/preparação e desenvolvimento não estão incluídos nessa duração.

[?] A mediana 0,0779 citada no pedido refere-se a amostra não identificada. A reanálise local de todos os casos V1, dt_scale=1, não nulos do precursor encontra medianas dos máximos de resíduo de 0,112473 (N216), 0,0577872 (N512), 0,0365572 (N1000). Não foi atribuída equivalência entre amostras. O precursor usava pontos estratificados com jitter, não o novo Poisson condicionado a N.

[D] O identificador G1 desta bancada significa qualidade geométrica, não o G1 histórico relativo a POL-01/P01–P05. Essa fonte histórica continua ausente e seu estado não foi alterado. Todos os nomes de gates devem ser lidos no respectivo protocolo.

[?] G6 é diagnóstico independente: 28 PASS e seis PENDING por cobertura/erro de predição. Seus resultados não substituem G4. Robustez populacional e convergência com mais tamanhos/controle temporal principal permanecem não certificadas. A versão atual usa epsilon=mu=1 em uma geometria prescrita; não é óptica molecular de água/gelo.

[D] O relatório científico recebeu uma errata exclusivamente editorial: contagem H1 corrigida para a amostra irregular do avaliador congelado. Versão gerada original preservada. Dados e JSON de avaliação não foram reclassificados.

[D] Instruções de reprodução: as saídas completas estão preservadas. Reexecutar o mesmo pacote apenas verifica/retoma casos já selados. Para nova rodada física use cópia independente, mantenha pontos/configurações/critério congelados e não sobrescreva os arquivos originais.

[?] Limite de atribuição causal: os pontos G5 e sua rede nativa são regulares, mas a regra de desempate do solver usa pesos por sítio na supercélula. Sua conectividade não é obrigada a ter a simetria da célula primitiva. O efeito observado combina padrão posicional e escolha de triangulação, ambas registradas; não foi declarado um efeito material de gelo versus água.
