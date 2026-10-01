# Calculadora e física quântica na nuvem

Calculadora em Python para soma, subtração, multiplicação e divisão. Não precisa
instalar bibliotecas. Aceita ponto ou vírgula decimal e calcula com precisão de
28 dígitos significativos. Entradas inválidas e divisão por zero geram uma
mensagem de erro.

## Executar no GitHub

1. Abra a aba **Actions** deste repositório.
2. Selecione **Cálculos simples** e clique em **Run workflow**.
3. Escolha a operação, informe os dois números e confirme em **Run workflow**.
4. Ao terminar, abra a execução para ver o resultado no passo **Calcular**.
   O arquivo `resultado.json` também fica disponível no artefato
   **resultado-calculo**.

Cada execução testa todas as operações antes de calcular. Publicações na branch
`main` executam os testes e o exemplo `10 + 5 = 15` automaticamente.

## Executar com Python

Use Python 3.10 ou superior:

```sh
python calculadora.py soma 10 5
python calculadora.py subtracao 10 5
python calculadora.py multiplicacao 10 5
python calculadora.py divisao 10 5
python calculadora.py soma 0,1 0,2 --output resultado.json
python calculadora.py -- soma -1,5 2
```

Use `--` antes da operação ao informar números negativos com vírgula pela linha
de comando. No GitHub Actions, basta preencher os números normalmente.

Exemplo de resultado:

```json
{
  "operacao": "soma",
  "a": "10",
  "b": "5",
  "resultado": "15"
}
```

## Testes

```sh
python -m unittest discover -s tests -p 'test_calculadora.py' -v
```

Os testes verificam as quatro operações, números negativos, casas decimais,
entradas inválidas, divisão por zero e a geração do arquivo de resultado.

## Oscilador harmônico quântico 1D

O módulo `quantum` constrói um Hamiltoniano tridiagonal esparso com NumPy/SciPy e
obtém os primeiros autovalores e autovetores. Todo cálculo acima de 255 pontos é
recusado fora do GitHub Actions. A execução completa pela CLI também exige
GitHub Actions; o ambiente local serve para desenvolvimento, planejamento e
testes pequenos. Não é necessário informar chaves ou criar segredos.

### Executar na nuvem

1. Abra **Actions → Física quântica na nuvem → Run workflow**.
2. Escolha `main` e preencha os parâmetros abaixo.
3. Confirme **Run workflow**. Uma execução na fila ou em andamento ainda não
   representa um resultado concluído.
4. Aguarde o estado **Success**. O resumo mostra as energias e a validação.
5. Baixe o artefato **quantum-results**, disponível por 30 dias.

Publicações em `main` que alterem o módulo, seus testes, dependências ou workflow
executam automaticamente a demonstração padrão. Execuções ficam serializadas
por branch, sem cancelar um cálculo anterior.

| Parâmetro | Padrão | Significado / limite |
|---|---:|---|
| `grid_points` | 4095 | Pontos interiores da malha fina; 127..200000. `N+1` deve ser divisível por `2^(levels-1)`. |
| `states` | 6 | Estados n=0..5; 1..32, com malha grossa suficiente. |
| `half_width` | 8 | Paredes em xi=±8; 3..20 comprimentos do oscilador. |
| `levels` | 3 | Malhas com passo sucessivamente dividido por 2; 3..5. |
| `mass` | 1 | Massa positiva, em unidades consistentes. |
| `omega` | 1 | Frequência **angular** positiva; em SI, rad/s. Para frequência f em Hz use omega=2*pi*f. |
| `hbar` | 1 | Constante de Planck reduzida positiva; em SI, J*s. |
| `max_seconds` | 600 | Limite real do processo, incluindo saídas; 60..2400 s. |
| `memory_mb` | 4096 | Teto de memória estimada em **MiB**; 256..4096. Um teto menor que a estimativa é recusado. |
| `resume_run_id` | vazio | ID numérico de uma execução anterior deste repositório, com checkpoints no artefato. |

### Unidades e aproximações

O problema físico é

`H = -(hbar^2 / (2*m))*d^2/dx^2 + (m*omega^2/2)*x^2`.

Usamos `a=sqrt(hbar/(m*omega))`, `xi=x/a` e `epsilon=E/(hbar*omega)`.
O Hamiltoniano reduzido é `H/(hbar*omega)=-d^2/dxi^2/2+xi^2/2`.
Assim, os parâmetros de massa, frequência e hbar definem a conversão de unidades;
a malha e o problema numérico ficam bem condicionados mesmo ao usar valores SI.
Os padrões `m=omega=hbar=1` são **unidades reduzidas**, sem atribuição de kg, s ou J.
Com entradas em kg, rad/s e J*s, os resultados físicos são em m e J.
As funções de onda seguem `psi(x)=phi(xi)/sqrt(a)`, com unidade de comprimento^-1/2.

A solução exata no eixo infinito tem `epsilon_n=n+1/2` e
`phi_n(xi)=H_n(xi)*exp(-xi^2/2)/(pi^(1/4)*sqrt(2^n*n!))`.
As funções de Hermite normalizadas são calculadas por recorrência.
Usamos diferenças finitas centrais de segunda ordem e condições de Dirichlet
`phi(-L)=phi(L)=0`, em um domínio finito. Para `dx=2*L/(N+1)`, a diagonal do
Hamiltoniano é `1/dx^2+xi^2/2`; as diagonais vizinhas são `-1/(2*dx^2)`.
Os vetores de norma euclidiana 1 são divididos por `sqrt(dx)` para que
`sum(|phi|^2)*dx=1`. O sinal global é alinhado ao analítico antes da comparação.

`scipy.sparse.linalg.eigsh` usa shift-invert em sigma=0, tolerância `1e-11`,
até 4000 iterações e início pseudoaleatório reproduzível (semente 1729).
A matriz permanece esparsa CSC; não construímos uma matriz densa N*N.
O solver reduz o erro algébrico; os principais erros físicos da demonstração
são a discretização O(dx^2) e a truncagem do domínio. Uma tolerância do solver
menor não remove esses dois erros.

### Validação numérica

A configuração padrão resolve N=1023, 2047 e 4095, com `dx=16/4096` na malha fina.
Outra malha de 5119 pontos amplia L de 8 para 10 mantendo o mesmo dx e verifica
o efeito das paredes. Esta comparação adicional mantém separados o erro da malha
e o erro do domínio. O resumo inclui:

- Erro relativo das energias <1e-4 e erro L2 das funções de onda <1e-3.
- Sobreposição com as funções analíticas >0.9999.
- Erros de normalização/ortogonalidade <1e-9.
- Resíduo `||H*phi-epsilon*phi||*sqrt(dx)/max(1,|epsilon|)` <1e-7.
- Erros decrescentes e ordem de convergência entre 1.7 e 2.3.
- Mudança das energias ao ampliar o domínio <1e-7 em unidades reduzidas.

Ordens não são calculadas para erros abaixo de 1e-9, onde o arredondamento pode
dominar; ausência de ordens só é aceita quando todos os erros já estão <1e-8.
Os limites são critérios da demonstração, não uma garantia para todo problema
físico. Malha grossa, domínio curto ou muitos estados podem falhar corretamente.
Se qualquer critério falhar, o workflow termina com erro e preserva as saídas
para diagnóstico; resultados de um workflow falho não devem ser tratados como
um cálculo validado.

### Recursos, lotes e retomada

O runner escolhido é `ubuntu-24.04`. A documentação do GitHub lista 4 CPUs e
16 GB de RAM para esse runner em repositórios públicos, como este:
[especificações oficiais](https://docs.github.com/en/actions/reference/runners/github-hosted-runners).
O código consulta a memória disponível do runner e eventual limite de cgroup,
adota no máximo 60% da memória disponível e nunca excede o teto de 4096 MiB.
BLAS usa uma thread para evitar excesso de paralelismo e variar menos os tempos.

Antes de resolver qualquer malha maior, estima a memória por
`512 MiB + 8*N*(4*ncv+16*k+80) + 8*ncv^2 bytes`, com
`ncv=max(20,2*k+1)`. A margem cobre CSC, fatoração esparsa, espaço de trabalho
ARPACK, funções de onda, validação e gráficos. N=4095 e k=6 exige aproximadamente
520 MiB segundo esse modelo, e o teste de domínio cerca de 522 MiB.
Esses valores são estimativas conservadoras, não medições de consumo máximo.

Um piloto de 255 pontos **na nuvem** mede o solver com os mesmos estados e domínio.
O tempo é estimado como `2 + 10*max(tempo_piloto,0.02)*N/255` segundos por malha,
mais 30 s para saídas. O fator 10 dá margem para variação; convergência do ARPACK
e hardware podem tornar a previsão imprecisa. O plano é recusado acima de 80%
do orçamento, e memória/tempo restante são verificados antes de cada malha.
O processo tem ainda um timeout externo real; o job inteiro tem limite de 45 min.
Não aumente N apenas porque há RAM: examine `resource_plan.json`, os tempos
medidos em `convergence.csv` e os critérios numéricos do teste menor.

As malhas são processadas sequencialmente, com checkpoint atômico por malha.
Para continuar uma execução interrompida, informe seu `resume_run_id` no botão
Run workflow e mantenha os parâmetros físicos, malha e versão do código.
É permitido ajustar os orçamentos de memória/tempo. Os checkpoints são rejeitados
se os parâmetros, código ou versões de NumPy/SciPy diferirem; resíduos e normas
são novamente verificados. Nenhum pickle é carregado.

Checkpoints retomam **malhas completas**, não uma iteração ARPACK interrompida.
O lote em execução será recalculado após timeout; para problemas que não caibam
em um único lote, é necessário outro algoritmo ou runner. Cancelamento forçado
pelo usuário ou encerramento do runner pode impedir o upload; em falhas normais,
o passo de artefatos usa `always()` e preserva logs/checkpoints já produzidos.

### Conteúdo do artefato

| Arquivo | Conteúdo |
|---|---|
| `summary.json`, `report.md`, `status.json` | Resultados, validação, procedência e estado final. |
| `parameters.json`, `resource_plan.json` | Entradas, escalas, estimativas e calibração de tempo. |
| `energies.csv`, `convergence.csv` | Energias e erros/tempos por malha. |
| `wavefunctions.npz` | xi, x físico, funções de onda reduzidas/físicas e analíticas, energias. |
| `spectrum.png`, `convergence.png` | Espectro, funções de onda e convergência. |
| `checkpoints/*.npz`, `progress.json` | Lotes concluídos e progresso para retomada. |
| `manifest.json` | SHA-256 dos arquivos de dados; logs e status são excluídos. |
| `run.log`, `calculation.log`, `tests.log`, `dependencies.log`, `environment.txt` | Logs e versões usadas. |

### Verificações locais leves

Sem instalar bibliotecas científicas:

```sh
python -m unittest discover -s tests -p 'test_quantum_resources.py' -v
python -m quantum.run --dry-run --output planning
```

O planejamento valida as entradas e estima memória, sem diagonalizar matrizes.
A estimativa de tempo depende do piloto no runner e fica nula no planejamento local.
Na nuvem, são executados todos os testes, incluindo estrutura esparsa, fórmulas
analíticas, convergência, checkpoints corrompidos e a CLI com geração de artefatos
e retomada. As dependências científicas estão fixadas em `requirements-quantum.txt`.
