# C5B-QO-QW02 — teste local: garganta aberta, fechada e cavidade

## Status
Teste exploratório local, construído a partir do código e PREM do pacote C5B_QO_QW01 fornecido pelo usuário. Não é uma evolução dinâmica completa.

## Definições

- Massa virtual: `M_V = f_V M_earth`.
- `mu_V = G M_V/c^2`.
- Função radial mantida: `F(r)=1-b(r)/r=(r-r0)(r+r0-2mu_V)/r^2`.
- Estado aberto: `A_open(r)=r/(r+2mu_V)` (família QW01).
- Estado fechado de comparação: `A_closed(r)=F(r)`. A garganta coincide com um horizonte em `r=r0`.
- Cavidade: matéria PREM prescrita começa apenas em `r_c=kappa r0`; a massa material externa é renormalizada para `(1-f_V)M_earth`.

## Resultado estrutural do estado fechado

Com `A_closed=F`, o tensor efetivo isolado satisfaz

`E = C* r0(2mu_V-r0)/r^4`, `p_r=-E`, `p_t=E`,

logo `NEC_radial=E+p_r=0` e `NEC_tangencial=2E`. Assim:

- `1<alpha=r0/mu_V<2`: NEC radial saturada e NEC tangencial positiva;
- `alpha=2`: exterior exatamente Schwarzschild, tensor efetivo local nulo;
- `alpha>2`: NEC tangencial negativa.

O caso `alpha=2` é o comparador mais limpo entre estado aberto e fechado: ambos têm a mesma escala de massa virtual e a mesma função radial `F=1-2mu_V/r`, mas o aberto tem `A=r/(r+2mu_V)` e o fechado `A=F`.

## Caso representativo f_V=1e-8, alpha=2

- `r0 = 8.8701029e-11 m`.
- Aberto, matéria até a garganta: `P(r0)=4.8717451e20 Pa`, finita.
- Fechado, matéria estática até o horizonte: `P -> infinito` e aceleração própria estática `-> infinito`.
- Fechado com `r_c=1.001 r0`: `P=3.6035366e22 Pa`.
- Fechado com `r_c=1.01 r0`: `P=1.0643951e22 Pa`.
- Em `r_c=2r0`: fechado `P=4.8717451e20 Pa`; aberto `P=2.6433218e20 Pa`.
- Em `r_c=100r0`: aberto `5.8660882e18 Pa`; fechado `5.9251931e18 Pa`.
- Para cavidades grandes, os dois estados convergem porque têm o mesmo limite assintótico de primeira ordem.

## Cavidade necessária para reduzir a sobrepressão geométrica

Critério: comparar `P_total(r_c)` com a pressão do mesmo modelo PREM com a mesma cavidade, mas sem a contribuição geométrica central. Para `alpha=2`, estado aberto; no regime de cavidade grande o estado fechado dá praticamente os mesmos raios.

| f_V | r_c para +10% | r_c para +1% |
|---:|---:|---:|
| 1e-10 | 1.433 cm | 14.332 cm |
| 1e-8 | 1.433 m | 14.331 m |
| 1e-6 | 143.309 m | 1.432 km |
| 1e-4 | 14.268 km | 137.567 km |
| 1e-3 | 137.686 km | 1,153.685 km |

Os últimos casos já removem uma fração espacial relevante do interior e não podem ser tratados como uma perturbação microscópica simples.

## Interpretação

[M] O estado aberto regulariza a garganta e admite pressão material finita até `r0`, mas requer violação da NEC no tensor efetivo QW01.

[M] O estado fechado `A=F` cria um horizonte. Matéria estática não pode ser prolongada até `r0` com pressão finita; uma cavidade `r_c>r0` regulariza o problema no domínio estático externo.

[M] Para `alpha=2`, o estado fechado é Schwarzschild exterior e não requer tensor efetivo local exótico fora do horizonte, enquanto o estado aberto exige tensões anisotrópicas NEC-negativas.

[M] Em raios macroscópicos os estados aberto e fechado são praticamente indistinguíveis para a mesma `M_V`; a diferença relevante está no microambiente da garganta/horizonte.

[?] Não foi demonstrada uma transição dinâmica aberta↔fechada. Uma evolução real exige métrica dependente do tempo, fluxo de energia-momento e conservação covariante.

[?] A cavidade é um ansatz. Uma interface matéria-vácuo com pressão interna não nula exige condições de junção/suporte (por exemplo, tensões de superfície ou um setor Q que forneça o suporte).
