# HRF-POL-GEOMETRY-01 — relatório científico

## Objetivo e hipóteses

[H] H1 mistura espectral prejudica o extrator monofrequência; H2 a falha pode ocorrer no controle regular; H3 correlação tetraédrica altera a mistura frente a Poisson; H4 cristal tetraédrico difere da rede desordenada. Resultados são modelos finitos, não água/gelo realistas ou demonstração ontológica.

## Parâmetros e protocolo

[D] Domínio periódico L=4, N=64 e 216, mesmas densidades em cada nível, k=(0,0,1)·2π/L; G5 acrescenta k=(1,0,0). Casos 4/8/8/8/6, total 34. Construção helicoidal histórica q=Re Q_s, v=|k|Im Q_s; limpeza V1; s histórico corresponde a S3 inicial=-s na base destrógira. Ajuste escalar somente no lançamento para igualar energia. Amplitude de referência e amplitude efetiva estão registradas; não são ambas impostas simultaneamente.

[D] Operadores e integrador B41L e extrator POL congelados. V0 pareado reconstruído pela identidade gauge q0=q1+t vL, v0=v1+vL, sem uma segunda integração. Predição multimodal utiliza autovalores da rede e projeções iniciais, com a fase discreta exata do Verlet, sem ajustar frequências aos dados temporais.

## Medidas e resultados

[M] Integrações físicas concluídas: 34/34. Tempo total da rodada: 0.75 min.

| Gate | Estado |
|---|---|
| G0 | PASS |
| G1 | PASS |
| G2 | PASS |
| G3 | PASS |
| G4 | FAIL |
| G6 | PENDING |
| G5 | FAIL |
| G7 | FAIL |

| Família | N | Casos | Resíduo mono mediano | Resíduo multimodal mediano | Pureza mínima mediana |
|---|---:|---:|---:|---:|---:|
| G1 | 64 | 2 | 0.213782 | 0.00555784 | 0.41255 |
| G1 | 216 | 2 | 0.0992985 | 0.000937617 | 0.831494 |
| G2 | 64 | 4 | 0.212103 | 0.0286014 | 0.91123 |
| G2 | 216 | 4 | 0.0710702 | 0.00964266 | 0.996946 |
| G3 | 64 | 4 | 0.26662 | 0.0652571 | 0.559188 |
| G3 | 216 | 4 | 0.0914085 | 0.0127633 | 0.994691 |
| G4 | 64 | 4 | 0.386744 | 0.0446627 | 0.825644 |
| G4 | 216 | 4 | 0.151496 | 0.0123745 | 0.995873 |
| G5 | 64 | 3 | 0.462248 | 0.07549 | 0.991775 |
| G5 | 216 | 3 | 0.190988 | 0.014574 | 0.998898 |

## Controles, convergência e interpretação

[M/H] H1: 21/23 casos irregulares elegíveis, com cobertura modal >=95% e mistura significativa, satisfizeram a regra pré-registrada. H1 é compatível nesta coorte. A regra não inclui G1/G5 e não reclassifica o extrator original.
[M/H] H2: 4/4 casos regulares excederam o limite monofrequência. A presença da falha na malha regular impede atribuí-la exclusivamente à irregularidade.

[M/H] H3: a razão das larguras espectrais G4/G3 foi 0,918909 (N64) e 1,046683 (N216). Não se observou efeito de 20% consistente nos dois níveis da coorte. Isso não exclui efeitos menores ou outras configurações.

[M/H] H4: a razão G5/G4 foi 0,474803 (N64) e 0,799193 (N216), compatível com redução da largura espectral neste modelo finito. O segundo nível fica muito próximo do corte exploratório de 0,8. Não é uma certificação populacional nem uma conclusão sobre água/gelo reais.

[?] H3/H4: comparações descritivas por família na tabela e no CSV. Duas realizações e dois tamanhos não certificam um efeito universal, uma fase líquida/cristalina física ou convergência populacional. Não se converte uma diferença de medianas em descoberta estabelecida.

[M/D] Qualidade das malhas, q tetraédrico, g(r), ângulos, coordenação nativa e conectividade Delaunay/Whitney são registrados separadamente. G1 usa triangulação Freudenthal, G5 usa lifting ponderado periódico para desempatar coesfericidades, sem deslocar os pontos. Essas escolhas de regulador podem afetar os observáveis e pertencem aos limites da comparação.

[?] Esta bancada testa o mapa W: propagação e polarização. Não deriva U(1), ħ, fóton individual, holografia, matéria ou uma trajetória helicoidal de energia. Critérios e resultados históricos B1/B41/B41H/B41L/POL-B41L-01 permanecem intactos. Os casos e as falhas estão preservados.

## Controles quantitativos complementares

[M] Maior deriva de energia: 0.00331331269 (limite 0,005). Maior variação vetorial relativa de Gauss: 1.45255296e-13 (limite 1e-8). Mediana da carga inicial relativa V0 pareada: 0.789929567; maior valor V1: 1.93527616e-15. Todos os 34 casos passaram preparação e conservação.

[?] As frações de helicidade da tabela são medidas do extrator monofrequência, cuja qualidade não passou; seus valores altos isolados não certificam polarização. Em particular, G5 pode apresentar fração próxima de 1 e ainda falhar no ajuste.

[M] Na cúbica, dois grupos espectrais significativos dividem aproximadamente a energia, embora as médias espectrais nos dois eixos transversais coincidam. Uma diferença quase nula entre médias não demonstra degenerescência de todos os modos. A triangulação Freudenthal é um regulador com direções privilegiadas; pontos cúbicos uniformes não garantem isotropia perfeita da discretização.

[D] Errata editorial: o texto automático anterior rotulava uma contagem agrupada de várias famílias como H1. A classificação computacional congelada sempre usou somente G2/G3/G4 e foi preservada (21/23). O relatório automático original foi arquivado; esta revisão corrige apenas a apresentação, sem tocar código, critérios, dados ou vereditos.

[?] A comparação não isola somente as posições: G1 e G5 exigiram escolhas de triangulação diferentes para resolver degenerescências. Os pesos de desempate de G5 são periódicos na supercélula, mas não impõem a simetria de translação da célula primitiva ao operador. Portanto, H4 é condicional ao regulador declarado; um efeito não deve ser atribuído exclusivamente à ordem cristalina sem controles adicionais de triangulação.
