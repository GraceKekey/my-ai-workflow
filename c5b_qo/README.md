# Ensaio C5B-QO: massa central em planeta de massa terrestre

Ensaio diagnóstico; não pressupõe a existência de um buraco negro na Terra.
Execute com Python 3.12 e as dependências fixadas:

```sh
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
python study.py --output results
```

O relatório `results/relatorio.md` explica as hipóteses, resultados negativos,
regiões excluídas e a impossibilidade de deduzir um limite observacional sem
dados e suas incertezas. Os CSV têm unidades nos nomes das colunas. Os gráficos
são exportados em PNG e PDF. `validacao.json`, `parametros.json` e
`manifesto_sha256.json` registram a reprodução e verificações.

## Interpretações de símbolos perdidos no prompt

- Os valores de f são os do texto, de 0 a 0.50. A referência de 8.9 mm é para
  **f=1**, usada exclusivamente como teste, fora da grade principal.
- As equações de pressão recebem o sinal negativo: dP/dr = -rho*g.
- Os raios de comparação escolhidos são 100 km, 1221.5 km, 3480 km e R/2.
- A tabela inclui Mc, massa material, rs, rs/R, g nesses raios e na superfície,
  gravidade e pressão máximas **no domínio truncado**, suas posições, diferenças
  relativas, raio de influência, momento de inércia e validade.

## Física e fontes

PREM: Dziewonski & Anderson (1981), *Preliminary reference Earth model*,
Physics of the Earth and Planetary Interiors 25, 297–356,
https://doi.org/10.1016/0031-9201(81)90046-7.
Os polinômios de densidade e limites de camada usados estão integralmente em
`study.py` e em `parametros.json`; densidade publicada em g/cm³, convertida
para kg/m³. Incluem a camada oceânica de 3 km do PREM esférico.

O perfil PREM escalado não é um equilíbrio autocoerente nem um novo ajuste
sísmico. Para a etapa autocoerente usa-se um politropo n=1 (gamma=2),
P=K*rho² e K=2*G*R_terra²/pi, fixado uma única vez pelo modelo f=0.
Massa total e K ficam fixos; o raio livre é resolvido, e não forçado a R_terra.
Integram-se numericamente massa e entalpia com shooting e compara-se a uma
solução analítica independente. Nenhum parâmetro é reajustado por f.

Para f>0, as duas famílias são singulares quando formalmente extrapoladas
até zero: PREM prescrito tem P~1/r; o politropo tem rho~1/r e P~1/r².
Isso impede interpretar as soluções como equilíbrios centrais regulares.
Para um buraco negro, extrapolação até r=0 é apenas diagnóstico matemático;
o horizonte já exclui essa região. Não se resolve acreção, TOV, transporte
de calor, temperatura, composição, ondas sísmicas ou estabilidade dinâmica.

Domínio computacional: r>=max(1 m,100*rs), preservando campo fraco. A dependência
em cortes maiores é publicada; não existe pressão máxima global finita para
f>0 no modelo pontual. Schwarzschild é exato em vácuo; a comparação de aceleração
própria de observadores estáticos é somente uma referência para a componente
central, não uma métrica exata dentro de toda a matéria. A pressão interna e a
gravidade total relativísticas exigiriam uma solução com matéria e condições
de contorno adequadas.

Tolerâncias de 1%, 5% e 10% nas tabelas de sensibilidade são cenários ilustrativos,
não erros de medição nem limites físicos inferidos. Não se retorna um f máximo
para a Terra real sem uma análise observacional.
