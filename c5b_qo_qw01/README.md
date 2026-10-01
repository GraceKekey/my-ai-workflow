# C5B-QO-QW01 — garganta central e planeta tipo Terra

Ensaio matemático exploratório, com GR como modelo-base. Não demonstra um
wormhole na Terra nem comprova a hipótese C5B-QO.

## Executar

Python 3.12; instale as dependências e rode os testes **antes** da grade:

```sh
python -m pip install -r c5b_qo_qw01/requirements.txt
python c5b_qo_qw01/tests/test_c5b_qo_qw01.py
python c5b_qo_qw01/src/run_c5b_qo_qw01.py
```

O programa exige um registro de testes aprovados correspondente aos hashes dos
arquivos atuais. A pasta `c5b_qo/` deve estar ao lado de `c5b_qo_qw01/`.
No ZIP entregue, o arquivo PREM original está incluído nessa estrutura.

## PREM reutilizado, sem alterações

Importa `c5b_qo/study.py`, commit
`313e3e7db01c64be08091172c5c6f4e6d5bdda86` do ensaio anterior.
SHA-256: `637d641a905960f4c789e0f6327e5a6b0a407c5dde1a4943e8675ef16678c1f1`.
As constantes, densidade, camadas, normalização e integral de massa são as mesmas.
Fonte: Dziewonski & Anderson (1981), https://doi.org/10.1016/0031-9201(81)90046-7.
O código anterior é verificado e não editado.

## Modelo declarado

Wormhole isolado: A_W=r/(r+2mu), b_W=2mu+(r0−2mu)r0/r,
mu=G*f*M/c² e r0=alpha*mu. Apenas uma boca r>=r0 é integrada.
O caso f=0 é uma referência sem garganta, e não um wormhole de raio zero.

Aceleração própria: g=c²*sqrt(F)*Phi', F=1−b/r, Phi=ln(A)/2.
Hidrostática isotrópica: dP/dr=−(rho*c²+P)*Phi'. Usar −rho*g por unidade
de r confunde distância própria com raio areal; próximo da garganta isso falha.

Para incluir matéria há uma **extensão composta prescrita**, sem alegar que
superposição de métricas seja uma regra da GR:

- Soluciona-se TOV para a Terra de referência com densidade `(1−f)*rho_PREM`;
  isso fornece Phi_E(r), P_E(r). A densidade ainda não provém de uma EOS.
- Na boca, m_mat(r)=(1−f)*[m0(r)−m0(r0)]/[1−m0(r0)/M];
  rho_mat é normalizada pelo mesmo fator, conservando a massa exterior.
- Define-se b_total=b_W+2G*m_mat/c² e Phi_total=Phi_W+Phi_E.
  Esta é uma escolha fixa de ansatz, não ajustada para melhorar os resultados.
- Reconstrói-se T_total pela equação de Einstein e integra-se a pressão da
  matéria com Phi_total. O setor exótico requerido é T_total−T_mat; a mudança
  de pressão desse setor, inclusive o termo de interação geométrica, é registrada.
  T_mat é conservado pela hidrostática; Bianchi conserva T_total e o resíduo.
- A referência Phi_E usa o perfil regular até zero como campo auxiliar, mas
  a matéria física na boca começa em r0. A massa removida/normalização está
  registrada. Não há integração física através de r<r0.

Isso não resolve EOS, composição, temperatura, elasticidade, sismologia,
possibilidade de produzir o tensor exótico ou estabilidade dinâmica.
O f=0 relativístico reproduz o PREM Newtoniano anterior dentro da precisão
esperada de campo fraco, e a pequena diferença é documentada.

## NEC e curvatura

Usa E_W em J/m³, rho_W=E_W/c² em kg/m³ e pressões em Pa.
NEC radial=E_W+p_r. A NEC do wormhole isolado é negativa para todos os
raios de uma boca válida. Sua largura radial é **infinita**. A integral
negativa em volume próprio de uma boca até infinito converge e é publicada.
Ela não é ANEC ao longo de uma geodésica nula, energia ADM, energia de formação
nem massa total exótica. A energia negativa de E_W é calculada separadamente:
é zero para alpha<=2, apesar da NEC violada, e positiva em magnitude para alpha>2.

Curvatura: Ricci em m^-2, Ricci² e Kretschmann em m^-4. As fórmulas analíticas
permitem avaliar r=r0 diretamente; B divergente nesse ponto é uma singularidade
de coordenada, não por si só de curvatura. Para cada r0>0 e alpha>1, as
curvaturas são finitas, mas crescem fortemente quando r0 diminui.

## Arquivos

- `data/`: parâmetros e identificação do PREM.
- `results/summary.csv`: 57 casos da grade inicial.
- `results/full_grid.csv`: todos os casos e refinamentos.
- `results/earth_samples.csv`: todos os pontos terrestres pedidos e comparação
  com a fonte pontual anterior, calculada pela mesma implementação.
- `results/validation.json`: erros efetivos, validade geométrica e limitações.
- `results/test_results.json`, `test_log.txt`: testes e hashes.
- `plots/`: gráficos PNG e PDF, separando escalas terrestre e microscópica.
- `report/C5B_QO_QW01_REPORT.md`: respostas A–J, resultados negativos e limites.
- `report/symbolic_derivations.json`: identidades e conservação simbólicas.

Compatibilidade sísmica e estabilidade dinâmica permanecem abertas. Uma grade
com boa convergência numérica não prova viabilidade física.
