# C5B-QO-QW01 — relatório

**STATUS: EXECUÇÃO CONCLUÍDA**

[M] 113 casos executados: 112 gargantas e uma referência PREM. 113 casos numericamente válidos. 13 testes aprovados, 0 falhas e 0 erros.

## O que foi calculado

[M] Métrica isolada exata proposta e extensão composta declarada no README. A geometria composta é um ansatz fixo: b=b_W+2Gm_mat/c², Phi=Phi_W+Phi_E, onde Phi_E vem de TOV com densidade PREM prescrita. Einstein reconstrói o tensor total; o resíduo após retirar o fluido terrestre conservado é o setor exótico necessário. A composição não é uma lei de superposição da GR nem uma EOS terrestre autocoerente.

[F] Para um observador estático, u^t=1/sqrt(A), a^r=c²A'/(2AB) e |a|=c²|A'|/(2A sqrt(B))=c²sqrt(F)|Phi'|. A conservação de um fluido isotrópico exige P'=−(rho c²+P)Phi'. Em distância própria, dP/dl=−(rho+P/c²)g. Portanto −rho*g por unidade de r não é válido arbitrariamente perto da garganta.

[M] b(r0)=r0, A(r0)=alpha/(alpha+2)>0, b'(r0)=2/alpha−1. F=(r−r0)(r+r0−2mu)/r². Flare-out estrito e boca lorentziana requerem alpha>1. A divergência de B=1/F em r0 é de coordenada; usando distância própria, r−r0 é proporcional a l² e os invariantes têm limites finitos.

## Respostas físicas A–J

**A)** [M] Sim, para cada r0>0 e alpha>1 esta garganta remove a singularidade pontual dentro do domínio definido: g→0 na garganta, P é finita e os três invariantes são finitos. Não existe um centro r=0 nessa boca; ele foi substituído por uma superfície mínima e outra região.

**B)** [M] Não apareceu divergência de curvatura ou pressão em nenhum caso admitido. Entretanto P(r0) variou de 1.169150e+19 a 8.603182e+20 Pa, contra 3.639709e+11 Pa no centro PREM de referência. Isso é pressão extrema com densidade ainda prescrita como terrestre, sem EOS que a justifique. O limite paramétrico r0→0 não é regular: curvaturas e tensões podem divergir.

**C)** [M] Sim, em primeira ordem assintótica: A_W=1−2mu/r+O(r⁻²), B_W=1+2mu/r+O(r⁻²), g_W→GM_W/r². O exterior não é exatamente vácuo Schwarzschild: o tensor requerido possui cauda. A garganta remove a singularidade, mas preserva o sinal gravitacional de massa em grande r.

**D)** [M] A gravidade profunda aumenta aproximadamente como no modelo pontual anterior em raios terrestres. As pequenas correções de GR da referência são separadas da comparação Newtoniana na tabela de amostras.

| f | Δg/g PREM a 100 km | P(r0), alpha=2 (Pa) |
|---:|---:|---:|
| 1e-10 | 1.08959791e-05 | 4.871745e+20 |
| 1e-09 | 1.08959791e-04 | 4.871745e+20 |
| 1e-08 | 1.08959791e-03 | 4.871745e+20 |
| 1e-07 | 1.08959791e-02 | 4.871745e+20 |
| 1e-06 | 1.08959791e-01 | 4.871740e+20 |
| 1e-05 | 1.08959791e+00 | 4.871696e+20 |
| 0.0001 | 1.08959791e+01 | 4.871258e+20 |
| 0.001 | 1.08959791e+02 | 4.866873e+20 |

**E)** [M] As menores massas produzem pequenas alterações nos pontos terrestres amostrados; a tabela permite conferir o crescimento sem escolher um limite arbitrário. Isso não estabelece compatibilidade sísmica: faltam EOS, velocidades elásticas, dados e covariâncias. Mesmo quando a alteração macroscópica é pequena, o microambiente da garganta exige pressão e tensor exótico extremos.

**F)** [M] NEC_W mínima variou de -7.253809e+66 a -4.847358e+49 Pa. A magnitude −∫NEC_W dV próprio, em UMA boca até infinito, variou de 8.845306e+31 a 8.348264e+40 J. Ela é um orçamento de violação da NEC, não energia ADM, massa do wormhole, energia de formação ou ANEC. A integral da densidade de energia negativa é calculada separadamente na tabela e é zero para 1<alpha<=2, apesar da NEC violada.

**G)** [M] Escrevendo y=r/r0 e C*=c⁴/(8 pi G), NEC_W=C*/r0² × n_alpha(y). Na garganta, NEC_W=−2C*(alpha−1)/(alpha*r0²). A escala local cresce como r0⁻² a alpha fixo; Kretschmann cresce como r0⁻⁴. A integral própria escala como C*r0 vezes uma função de alpha. A largura negativa é INFINITA: a NEC é negativa em todo r>=r0, com cauda O(r⁻⁴), cuja integral volumétrica converge.

**H)** [M] Aumentar r0 a massa externa fixa significa aumentar alpha. Isso reduz a escala local de tensão/curvatura nos casos grandes, mas não elimina a NEC. Para grandes alpha, o orçamento integrado cresce proporcionalmente a r0; garganta maior não implica menos quantidade exótica integrada. Os valores de cada alpha estão no CSV, incluindo o comportamento próximo do limite alpha=1.

**I)** [M] Há combinações geometricamente regulares, sem horizonte, com convergência numérica e pequenas perturbações nos pontos terrestres amostrados. [?] Não há demonstração de compatibilidade física completa com uma Terra nem de estabilidade dinâmica. Não se deve converter validade numérica em existência física.

**J)** [M] Nenhum critério geométrico mínimo falhou na grade admitida. A exigência de fonte exótica violando NEC já aparece no flare-out; a pressão microscópica extrema e a falta de EOS impedem afirmar um equilíbrio terrestre real. Para alpha=1, o primeiro critério que falha é flare-out estrito; surge um limite de distância própria infinita, sem A=0. Para alpha<1, há F<0 em parte da boca, invalidando a assinatura pretendida. Esses limites não são uma transição dinâmica demonstrada para um buraco negro.

## Curvatura e tensor necessários

[M] Kretschmann na garganta: 3.060555e+14 a 1.029746e+50 m⁻⁴. Finito não significa moderado. O CSV registra Ricci, Ricci² e Kretschmann, tanto da métrica isolada quanto da composição. O tensor está em base ortonormal: E=C*b'/r², p_r=C*(−b/r³+2F Phi'/r), p_t=C*[F(Phi''+Phi'²+Phi'/r)+F'/2*(Phi'+1/r)]. A conservação radial do tensor isolado foi verificada simbolicamente.

[M] O tensor exótico na composição não é simplesmente o isolado: p_r,ex=p_r,total−P_mat, E_ex=E_W. A pressão adicional e os termos de interação geométrica estão nos perfis selecionados. O orçamento integral publicado é o da métrica isolada fornecida, com seu volume próprio; não é apresentado como integral exata do planeta composto.

## Estado não atravessável — análise preliminar

[M] A família fornecida tem A_W(r)>0 para r>0. Phi_E da Terra de referência também é finita: nenhuma escolha admitida cria A_total=0. Variar alpha até 1 não cria um horizonte. [F] Um horizonte estático regular requer analisar A(r_h)=0, a superfície nula e F(r_h), além da regularidade em coordenadas que atravessem o horizonte. [?] Uma evolução A(r,t), b(r,t) deve satisfazer Einstein e conservação covariante. Ela não foi construída; nenhuma interpolação foi inventada.

## Validação e limites

[M] Erro máximo de massa: 3.596e-16. Mudança máxima de pressão na duplicação da resolução: 2.303e-08. Erro máximo frente à ODE independente da pressão: 1.633e-08. Erro máximo do limite assintótico: 2.997e-08. Dados completos em results/validation.json.

[?] Não foram resolvidos EOS, sismologia, suporte quântico de energia exótica, evolução causal, estabilidade dinâmica ou custo de formação. A redução de rho por (1−f) continua um perfil prescrito. Massa gravitacional/Misner–Sharp e integral em volume areal não são massa bariônica em volume próprio. A grade não estima um f máximo observacional permitido.

[H] Um Q orientador corresponder a uma microgeometria de garganta continua hipótese. A possibilidade de estados causais diferentes também continua hipótese. Os resultados aqui são conteúdo matemático de GR com fonte exótica reconstruída; não introduzem uma previsão independente específica de C5B. Não comprovam wormhole terrestre, equivalência entre emaranhamento e wormholes ou resolução da NEC.
