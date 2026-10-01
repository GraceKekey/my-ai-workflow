# Ensaio C5B-QO — resultados e limites

[M] O ensaio **não determina um maior f permitido para a Terra real**. Ele mede sensibilidade de dois modelos e identifica singularidades. As tolerâncias ilustrativas não são limites observacionais.

[F/M] g superficial = 9.82030229 m/s² em todos os casos PREM prescritos; isso decorre da massa total e do raio fixos, e não valida a estrutura interna.

[M] PREM original: M=5.973176948e+24 kg; multiplicador=0.999836444; P central sem fonte=363.971 GPa; I/(MR²)=0.3307995.

| f | Mc (kg) | rs (m) | Δg/g0 a 100 km | influência (km) |
|---:|---:|---:|---:|---:|
| 0 | 0.0000e+00 | 0.0000e+00 | 0.0000e+00 | 0.000 |
| 1e-08 | 5.9722e+16 | 8.8701e-11 | 1.0896e-03 | 10.290 |
| 1e-07 | 5.9722e+17 | 8.8701e-10 | 1.0896e-02 | 22.169 |
| 1e-06 | 5.9722e+18 | 8.8701e-09 | 1.0896e-01 | 47.762 |
| 1e-05 | 5.9722e+19 | 8.8701e-08 | 1.0896e+00 | 102.902 |
| 0.0001 | 5.9722e+20 | 8.8701e-07 | 1.0896e+01 | 221.732 |
| 0.001 | 5.9722e+21 | 8.8701e-06 | 1.0896e+02 | 478.136 |
| 0.01 | 5.9722e+22 | 8.8701e-05 | 1.0896e+03 | 1036.152 |
| 0.05 | 2.9861e+23 | 4.4351e-04 | 5.4480e+03 | 1830.336 |
| 0.1 | 5.9722e+23 | 8.8701e-04 | 1.0896e+04 | 2372.566 |
| 0.25 | 1.4931e+24 | 2.2175e-03 | 2.7240e+04 | 3539.933 |
| 0.5 | 2.9861e+24 | 4.4351e-03 | 5.4480e+04 | 6371.000 |

[M] Identidade exata do perfil escalado: Δg/g0=f[M/m0(r)−1]. No centro, g0~r, o excesso~f/r² e a diferença relativa~f/r³. Para rho central finita, P~G*Mc*(1−f)*rho0(0)/r para qualquer f>0.

[M] Os máximos das tabelas referem-se apenas ao domínio r>=max(1 m,100 rs). São dependentes do corte; a pressão não tem máximo global finito na extensão pontual. A tabela de cortes verifica essa dependência. O limite formal r→0 não é uma trajetória física através do horizonte. m0 é a integral matemática do perfil prescrito desde zero; a pequena massa formal dentro de rs e a massa excluída pelo corte estão nas tabelas, não são uma atmosfera física dentro do horizonte.

[F] r<=rs fica fora do domínio. Schwarzschild descreve vácuo, não o interior completo com matéria. A aceleração própria de um observador estático é a_N/sqrt(1−rs/r), diferente da aceleração de coordenada e do movimento em queda livre. Seu excesso sobre a_N é <=1% para r/rs>=50.7513 e <=0.1% para r/rs>=500.7502. epsilon=rs/r>=0.1 (r<=10rs) marca campo forte nesta convenção explícita. O observador estático não existe no horizonte. Essa comparação central não resolve a estrutura relativística com matéria.

[M] O politropo mantém K fixo e massa total fixa. Sua solução livre obedece f=sin(z)/z, R_solucao/R_terra=z/pi; a integração por shooting reproduz isso. A família f>0 possui rho~1/r, P~1/r²: existe solução formal truncada, mas não um centro regular. As variações são relativas ao politropo f=0, cujo perfil de densidade não é PREM.

| f | R_solucao/R_terra | variação de raio |
|---:|---:|---:|
| 0 | 1.000000000 | 0.000000% |
| 1e-08 | 0.999999990 | -0.000001% |
| 1e-07 | 0.999999900 | -0.000010% |
| 1e-06 | 0.999999000 | -0.000100% |
| 1e-05 | 0.999990000 | -0.001000% |
| 0.0001 | 0.999900010 | -0.009999% |
| 0.001 | 0.999000997 | -0.099900% |
| 0.01 | 0.990097428 | -0.990257% |
| 0.05 | 0.952210157 | -4.778984% |
| 0.1 | 0.907928624 | -9.207138% |
| 0.25 | 0.787682256 | -21.231774% |
| 0.5 | 0.603354564 | -39.664544% |

[?] Estabilidade dinâmica não foi calculada. Hidrostática estática e convergência não provam estabilidade nem longevidade. Para um BH são necessários acreção, condições de contorno absorventes, energia/temperatura, transporte, composição e relatividade com matéria; uma atmosfera mantida estática sobre o horizonte não é demonstrada por este ensaio.

[F/?] Sismologia poderia testar as faixas de f por tempos de viagem, modos normais, estrutura/raio do núcleo e velocidades elásticas recalculadas com EOS, além de momento de inércia. A família PREM escalada dá I_f=(1−f)I0: mesmo com g superficial idêntica, muda uma restrição global. PREM é um modelo de referência; seus coeficientes não trazem aqui uma covariância que permita excluir quantitativamente cada faixa. Não se infere f_max de percentuais arbitrários. As singularidades impedem uma extensão regular do toy model, mas não constituem, sozinhas, um limite observacional universal para um BH com fluxo de acreção.

[H] C5B-QO não foi incorporada às equações. Uma proposta de regularização precisaria demonstrar em equações como remove a singularidade, preserva conservação, recupera GR em domínios testados e prevê observáveis novos. Ajustar uma solução não é evidência experimental. Não há conclusão de que exista um BH na Terra.

Validação: rs(f=1)=8.870103 mm; conservação de massa, quadratura independente da pressão, duplicação da resolução, mudança de passo/tolerância ODE e solução analítica politrópica verificadas. Os erros efetivos estão em validacao.json. Os testes executáveis incluem esfera uniforme, identidade de perturbação e horizonte excluído.
