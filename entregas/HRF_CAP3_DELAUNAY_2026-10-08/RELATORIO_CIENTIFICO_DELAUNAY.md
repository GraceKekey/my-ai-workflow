# HRF CAP3-2D3V-DELAUNAY-01 — relatório científico

## Resposta à pergunta

[M] A redução Whitney produto preserva os dois setores transversais esperados e o kernel de gradientes, com identidade discreta de gauge. As ondas livres medidas têm helicidades opostas reconstruídas espectralmente, propagação do envelope e erros de campo decrescentes nas três resoluções.
[?] Isso não constitui aprovação completa da correspondência com o Capítulo 2: **GATE_HRF_CAP2: PENDING**. A equivalência com a tetraedrização histórica 3D, quantização e contrato físico completo não foi demonstrada.
[M/D] **GATE_DELAUNAY_FREE: FAIL** nesta tentativa pré-registrada: o controle temporal de campo completo falhou; o controle conservador da faixa exterior também falha nos ângulos listados em GATES_FINAL.json. A caixa maior diagnostica o efeito de borda, mas não substitui retrospectivamente a aprovação da suíte original nem resolve o controle temporal.
[?] Não há resultado Delaunay de confinamento dinâmico ou transporte interno de cavidade. Cavidade T=30 e fases T=150/300/500: **NOT_EXECUTED**, por dependência do gate livre. Nada aqui estabelece elétron ou fóton individual.

## Modelo e execução

[D] Malhas Delaunay de pontos de uma grade com deslocamento irregular, semente 20261008, conectividade congelada, caixa livre de lado12, condições naturais exteriores. A irregularidade não é interpretada como emergência da geometria. O dual Voronoi não define as massas. Massas Whitney consistentes exatas e rigidez de curvatura; redução extrudada por unidade de comprimento em z. Derivação em OPERATOR_DERIVATION.md.
[D] Ambos os setores são evoluídos com midpoint implícito, dt=0,009, até T=3,96 λ/c. A referência contínua é um pacote Fourier transversal de frequência positiva, σ_long=0,7 e σ_trans=0,35, com quatro direções. A conexão planar é integrada nas arestas, az é amostrado nos vértices, e a velocidade inicial é projetada para Gauss. Essa inicialização e a borda diferem da Yee e são declaradas, não alegadas como reprodução idêntica.
[D] Sinais analíticos complexos dos setores são evoluídos independentemente. Para h=+1 e h=-1, multiplica-se o setor vertical por +i e -i. Pela linearidade, as duas helicidades compartilham energia, erro de campo e fluxo XY; não se alegam duas integrações independentes quando se usa essa identidade. Os arquivos guardam os setores não rotacionados e o código aplica a quadratura nos diagnósticos. A amplitude FFT é arbitrária; os balanços são relativos à energia inicial medida, não à energia de um quantum. Os mapas de apresentação são normalizados para energia total1.

## Medidas [M]

| PPW | Erro L2 final, faixa | Helicidade absoluta, faixa |
|---|---|---|
| 20 | 0.127116–0.134432 | 0.986189–0.986332 |
| 24 | 0.093932–0.098058 | 0.993259–0.993348 |
| 32 | 0.060785–0.062493 | 0.997655–0.997733 |

Máximo resíduo de Gauss: 3.3166e-14. Máxima deriva da energia quadrática do sinal analítico: 3.37863e-12. O método midpoint conserva a energia quadrática até erro de solução; isso não garante exatidão espacial ou temporal. A ordem temporal independente usa dt=0,018/0,009/0,0045 na mesma malha: razões [1.8699138462426728, 1.8502053392621831, 1.8371735697581315, 1.8278995531537683], passou=False. O critério era2,5–6; permanece FAIL. O diagnóstico de modos individuais e escala espectral está em time_failure_diagnosis.json, sem substituir o teste de campo completo. [H/?] Modos de alta frequência da malha podem contribuir para um regime temporal ainda não assintótico; sua contribuição energética exata não foi medida, logo essa causa não é afirmada como demonstrada.

Os probes temporais de dispersão dos dois setores passaram=True, com seus valores, limites e fases em dispersion_phase_controls.json. São probes de frequência de pacote em bins Fourier, não uma superfície completa de dispersão do espectro da malha irregular. O controle Rayleigh independente está em plane_wave_controls.json.

O diagnóstico FFT longitudinal do E interpolado não é a lei discreta de Gauss nem prova de uma terceira polarização física. A ausência de modo gradiente propagante usa o kernel do operador e a restrição inicial. A reconstrução/interpolação introduz resíduos contínuos de campo mesmo com Gauss discreto conservado.

## Borda e resultado negativo

[D] O limite prévio foi 0,005 da energia na faixa de largura1 junto ao exterior; trata-se de um teste conservador de margem, não uma medição de energia já refletida ou absorvida. [M] Na caixa16/PPW20, as frações finais foram [7.822067739987524e-11, 7.058864029830805e-11, 2.1207298179163775e-10, 4.3390544274683924e-10]. A redução dessa ocupação localiza uma dependência do desenho da caixa. Não concluir que a discretização Delaunay não pode produzir ondas livres. O PASS de outros controles não anula o FAIL pré-registrado da tentativa caixa12.
[?] Para continuar: registrar e validar uma suíte livre com passos temporais menores e controle do espectro modal inicial, além de caixa maior nas três resoluções e convergência separada de borda e da referência espectral, antes da cavidade. Não afrouxar os limites para transformar os resultados desta tentativa em PASS.

## Cavidade, comparação Yee e refinamento

[H] O perfil histórico c_min=0,015 e hipótese ε=μ=1/c_local foram preservados em referências e no planejamento. [D] O arquivo cavity_resource_plan.json estima a resolução local a partir de c_local/0,39, sem alegar medição de fase na cavidade. A estimativa de cobertura exige aproximadamente 456 mil, 894 mil e 1,82 milhão de vértices na região r≤6,4 para os alvos locais10/14/20; nenhuma dessas malhas foi gerada. Refinamento adaptativo e continuidade energética entre regiões não foram testados nesta rodada.
[M, fonte histórica] Yee livre: PASS; Yee curto: FAIL de convergência espacial; Yee longo: NOT_EXECUTED. A comparação atual usa relatórios e dados fornecidos; nenhuma tabela histórica foi renomeada como medição Delaunay. A nova bancada difere em elementos, massas, integrador, preparação e borda. Não há comparação de retenção de cavidade nova com Yee, pois não houve execução Delaunay de cavidade.

## Proveniência, falhas e limites

[D] Os13 documentos do dossiê e843 arquivos históricos tiveram hashes verificados. O pacote compacto omite410 NPZ listados no manifesto histórico; isso limita reanálise dos campos Yee, mas código, CSV/JSON e figuras presentes são preservados. Não são dependências externas necessárias para ler esta entrega.
[D] A primeira tentativa estrutural falhou na gravação de um booleano NumPy; fonte e registro da falha permanecem em results/failed_attempt_01. A correção não alterou critérios ou operadores. A tentativa livre caixa12 com FAIL e seus campos/logs está preservada; a caixa16 é um controle separado. Nenhum resultado negativo foi apagado.
[?] Correspondência histórica completa HRF, cavidade, refinamento adaptativo, absorvedor de cavidade, balanço local de cavidade, identidade local e tempos longos continuam não executados/não aprovados. Este ZIP documenta uma tentativa livre com interrupção condicionada, não o fechamento positivo de todas as fases pedidas.
