# HRF-FM — ELETRON-2D-POST-E67-01
## Auditoria documental e reanálise independente dos dados arquivados

**Data:** 8 de outubro de 2026. **Versão:** 0.1.
**Estado:** A1 concluída; reprodução integral A2 e extensão B–F pendentes.
**Natureza:** [M] reanálise numérica do toy model; [D] planejamento; [?] robustez física ainda aberta.

## Resultado principal desta entrega

O avaliador original foi executado novamente sobre os sete JSON históricos, numa cópia separada.
Todas as métricas e decisões coincidiram com o resumo arquivado, com tolerância de comparação absoluta
e relativa de 10⁻¹⁰. Os 65 hashes do manifesto do pacote de resultados foram verificados sem divergência.
Isso confirma a integridade do material e a reprodutibilidade do pós-processamento.
**Não constitui uma nova execução das covariâncias nem demonstra convergência de tamanho ou resolução.**

A classificação histórica permanece **H67=SIM — regime não linear**, **H67-N=NORMALIZÁVEL**,
**H67-Z=PROPORCIONAL**, estritamente nos critérios operacionais originais.
O fecho w=7 permanece **NOT_MEASURED**.

## 1. Fontes e preservação

Primeiro foram consultados o esqueleto do Research Book e procuradas referências E67/E-67 nos
Markdown e textos dos DOCX diretamente disponíveis no projeto. O corpus fornecido não continha o pacote E-67.
A busca dirigida no Drive localizou o relatório final, protocolo, pacote de execução e resultados completos.
O Capítulo 2 v1.1 foi consultado para delimitar a interface fotônica; não foi usado como substituição do modo Z.

- [Relatório E67 final v0.2](https://drive.google.com/file/d/1V1Ae8mZSk9blkxXvtOY30CdzNKINeS9Q/view)
- [Protocolo E67 original](https://drive.google.com/file/d/1Zl1CvWEwRtuDxu4dQwPriOEz3R2RI-12/view)
- [Pacote original](https://drive.google.com/file/d/14C1Ial-fKVKtFbPMKxhUUePoEE34Sl_m/view)
- [Resultados completos](https://drive.google.com/file/d/1VSEvA3k8z4_Txt9F0MLUfMYhczOAoFLX/view)
- [Pasta da execução histórica](https://drive.google.com/drive/folders/1JX1IFFLBBAS4XVuE2Tw3SypjkFPVWJMT)

O ZIP de código baixado tem SHA-256 `422c982a0dbbbd95ea9e3be82b77b99653b7ad4976c479fddb3044c751002ee3`,
igual ao registro pré-execução. O ZIP de entrega dos resultados tem SHA-256
`78bd7580f67c36c3e79f359e0e0641e2df7749924d3128b019fbb74374b6af09`.
Ele contém o artefato original do GitHub com SHA-256
`e42b5be5ff95d6785b5a3ad3e5b382ed4a312ca309f25b0fde047bd0f719c131`, também verificado.
São arquivos diferentes; não se exige igualdade entre esses dois hashes.
Os 18 arquivos do pacote original estão cobertos pela proveniência histórica e pelos arquivos preservados.

## 2. Modelo e auditoria do código

O código constrói uma rede triangular periódica retangular com 4.736 nós.
O Hamiltoniano é H=ΣQ²/(2M)+½Σκw_e(Z_i−Z_j)², M=√3/2, w_e=1/√3, κ=1.
Nas coordenadas de massa, o vácuo é X=½Ktil^(-1/2) e P=½Ktil^(1/2), restritos ao
subespaço ortogonal ao modo constante. O código remove o menor autovalor presumindo ser esse modo.
A extensão deve verificar explicitamente multiplicidade do núcleo e resíduos, sem simplesmente recortar autovalores negativos.

O aperto usa Sx=I+(exp(r)−1)ffᵀ e Sp=I+(exp(−r)−1)ffᵀ, com f normalizado e média zero.
Logo Sp=Sx^(-T): é transformação canônica no subespaço físico. Isso justifica a preservação
analítica da condição quântica do estado, mas não substitui a medição dos erros numéricos.

A função `entropia_gauge` forma diferenças de posição XY e o complemento de Schur de momento
PC=PA[1:,1:]−ccᵀ/v, v=ΣPA. Calcula ν pela matriz simétrica LᵀPC L, com XY=LLᵀ.
O mínimo de ν é capturado **antes** de recortar ν para 0,5 no cálculo entrópico.
O autovalor quadrado é recortado para zero antes da raiz: um valor negativo levaria ν_min=0
e falharia no teste, mas seu valor negativo exato não está preservado. A extensão deve registrá-lo.

Essa é a entropia condicionada da álgebra escolhida, excluindo o termo clássico do centro;
não é automaticamente a entropia de uma fatoração de Hilbert comum.
Mudar essa definição seria mudar a bancada.

**Limitação de auditoria:** os dados armazenam entropias e mínimos simpléticos, não as matrizes
integrais ou todos os espectros. Positividade e condição de incerteza não foram recalculadas
independentemente nesta entrega. A instrumentação histórica registra 2.207 regiões e
ν_min=0,4999999999991239, acima de 0,5−10⁻⁹.

## 3. Métricas reproduzidas a partir dos JSON históricos

| w | p mínimo | Classe | z | VL | Fecho |
|---|---:|---|---:|---:|---|
| 4 | 2,8368439 | NORMALIZÁVEL | 7,6476093 | 3,0950532 | 0,00259023 — PASS |
| 5 | 2,8065980 | NORMALIZÁVEL | 8,8624580 | 2,9848231 | 0,00268129 — PASS |
| 6 | 3,1346522 | NORMALIZÁVEL | 10,0357950 | 2,9640339 | 0,00250260 — PASS |
| 7 | 3,0254958 | NORMALIZÁVEL | 11,1192752 | 1,6902675 — FAIL | NOT_MEASURED |

V0: R²=0,9998877113, PASS. VK: dispersão 8,926×10⁻¹⁴, PASS.
V+: máximo em discos contendo o suporte 5,006×10⁻¹², PASS.
VP: diferenças 0,137656; 0,137160; 0,119326; 0,120510, todas PASS.
VC: os dois padrões κ=0,25 e o unitário gauge local permanecem GRUDADA.
H67-L: valores históricos pequenos não demonstram δS≈δK para o K local usado.
H67-R: z/r50≈3,72;3,27;3,12;2,98 não coincide com a referência pontual 1,55.

O avaliador trata NaN de fecho como aceitável no booleano agregado VF; isso segue a exclusão
operacional de w=7, mas pode induzir leitura errada. A saída histórica foi preservada e o CSV/JSON
novo dá a w=7 o estado explícito NOT_MEASURED. Também foi preservada a omissão histórica da
nota VL na frase do avaliador; o relatório mantém a correção separada prevista no v0.2.
Outro risco latente: `nanmin` pode ignorar uma sonda ausente e comparações com NaN podem
gerar INTERMEDIÁRIA; isso não foi detectado como ocorrência nos sete casos válidos,
mas merece status INVALID explícito na extensão.

## 4. Achado exploratório sobre VL

A máscara de VL seleciona raios por |δS(0,25)|. Ela mistura uma parte com δS negativo e
outra com δS positivo, ambas com razões positivas, porém de magnitudes diferentes.

| w | Raios com δS<0 | Raios com δS>0 | Mediana da razão na parte negativa | Mediana na parte positiva |
|---|---:|---:|---:|---:|
| 4 | 0 | 15 | — | 3,09505 |
| 5 | 11 | 19 | 1,26219 | 3,10093 |
| 6 | 18 | 22 | 1,42769 | 3,10387 |
| 7 | 22 | 20 | 1,53284 | 3,16154 |

Em w=7, a maioria dos 42 pontos selecionados pertence à faixa de razões baixas.
A mediana global de 1,6902675 é a média dos dois maiores valores dessa faixa baixa.
Portanto, o salto da mediana entre w=6 e w=7 está associado à inversão do peso dessas duas partes.
O menor |δS(0,1)| selecionado em w=7 é 0,00313727: não há evidência, nesses dados, de
denominador próximo de zero como explicação trivial.

**[M] Isto é um diagnóstico retrospectivo da métrica, não uma correção do FAIL.**
As respostas entrópicas nas duas amplitudes já são diferentes de uma simples relação linear
em diversos raios, inclusive nas larguras com VL agregado PASS. Ainda não foi determinado
quanto disso decorre de tamanho finito, discretização ou aperto finito.

O Hamiltoniano é quadrático: sua evolução canônica é linear. Entropia e parametrização exponencial
do aperto podem responder não linearmente sem interação não linear no Hamiltoniano.
A expressão histórica “regime não linear” deve continuar acompanhada dessa distinção.

## 5. Ajustes históricos z(w)

| Modelo | Ajuste nos quatro pontos | RMSE descritivo |
|---|---|---:|
| Proporcional estrito | z=1,69009859w | 0,607034 |
| Afim | z=1,15883346w+3,04270027 | 0,033284 |
| Quadrático | z=−0,03284206w²+1,52009614w+2,09028048 | 0,005405 |

O ajuste afim descreve os quatro pontos muito melhor que a proporcionalidade estrita.
O quadrático tem três parâmetros para quatro pontos; sua melhora não estabelece uma lei física.
CV(z/w)=0,0693813 satisfaz o critério histórico, mas z/w cai de 1,91190 para 1,58847.
O resultado sustenta **proporcionalidade operacional no intervalo histórico e uma relação afim
aproximada**, não proporcionalidade universal nem lei de escala fisicamente validada.
Os RMSE são resíduos descritivos, não incertezas físicas nem erros do solver.

## 6. Geometria e custo da próxima etapa

Na rede 64×74, L=(64;64,08588) e o raio de injetividade do toro é 32.
Logo discos de raio 28 e 30 cabem geometricamente sem auto-sobreposição na própria referência.
A falta de fecho em w=7 é uma limitação da janela executada, não uma impossibilidade geométrica
de medir 4w nessa rede. Isso não exclui efeito de tamanho finito nas correlações.

| Rede | Nós | GiB por matriz densa float64 | Fator N³ relativo |
|---|---:|---:|---:|
| 64×74 | 4.736 | 0,167 | 1,00 |
| 80×92 | 7.360 | 0,404 | 3,75 |
| 96×112 | 10.752 | 0,861 | 11,70 |
| 128×148 | 18.944 | 2,674 | 64,00 |

O código mantém diversas matrizes, cópias e áreas de trabalho; os valores por matriz não são
estimativas de pico. Em 128×148, oito matrizes já ocupariam 21,4 GiB, antes do solver.
Não é prudente iniciar a maior rede em um runner pequeno sem instrumentação e orçamento.
A proposta inicial é 64×74, 80×92 e 96×112, sujeita à medição do pico de memória e tempo.
Esses fatores N³ descrevem diagonalização densa, não preveem o tempo total com precisão.
Nenhum benchmark das novas redes foi executado.

Um aumento de N com a=1 testa tamanho finito; refinamento exige reduzir a e conservar
domínio físico, larguras e dinâmica. O rascunho separa essas duas baterias.
Uma implementação espectral por simetria translacional pode reduzir custo no vácuo intacto,
mas precisaria ser validada contra a implementação densa antes de substituir qualquer cálculo.

## 7. Dinâmica e relação com o Capítulo 2

As equações de Hamilton do modelo auditado fornecem xdot=p e pdot=−Ktil x.
Há, portanto, uma evolução linear matematicamente justificável para propor futuramente.
Entretanto, ela produz correlações cruzadas x–p, ausentes da rotina estática de entropia.
É necessário generalizar a redução gauge e a análise simplética antes de usá-la no tempo.
Fase F permanece PENDING e condicionada aos controles estáticos.

O Capítulo 2 descreve conexão relacional U(1), estrutura curl–curl e duas polarizações transversais.
O E-67 usa o modo Z escalar fora do plano e um estado gaussiano apertado. Nenhuma equivalência
entre esses sistemas foi derivada aqui. Não se importou dinâmica CAP3, helicidade ou identificação fotônica.
Termos históricos dos arquivos foram preservados; a redação corrente usa sistema/subsistema físico.

## 8. Bloqueio de execução e entregáveis

A habilidade `cloud-calculos-github:rodar-calculos` exige disparo por `triggerWorkflow.py`
e `GITHUB_TOKEN` no ambiente de execução, sem processamento pesado local.
A verificação segura retornou `GITHUB_TOKEN_configurado=False`.
Nenhum disparo foi enviado; nenhum resultado de nova rede foi produzido.
A execução histórica ocorreu em GraceKekey/my-ai-workflow; a integração disponível aponta para
mariocantofilho/my-ai-workspace. O novo código ainda não foi publicado nem o workflow de destino verificado.
Não se presume que disparar um workflow genérico enviaria os arquivos deste chat.

| Entrega solicitada | Estado real |
|---|---|
| Plano e critérios | Rascunho detalhado; congelamento depende da reprodução integral |
| Código reprodutível | Reanálise executada; runner de referência preparado, apenas validado sintaticamente |
| Auditoria E-67 | Integridade, protocolo, fonte e pós-processamento concluídos; matrizes pendentes |
| Convergência por tamanho | NOT_EXECUTED |
| Fecho w=7 | NOT_MEASURED |
| Comparação z(w) | Concluída somente para dados históricos |
| Mapas e figuras | Replotagem dos dados históricos, sem nova reconstrução |
| CSV/JSON | Métricas históricas, diagnóstico VL, ajustes e auditoria |
| Falhas e limitações | Registradas nesta versão e no status JSON |
| Relatório Markdown | Este documento |

## 9. Resposta científica provisória

**Ainda não é possível decidir se a normalizabilidade é robusta a tamanho, resolução e escolhas
da reconstrução.** O pós-processamento histórico é reprodutível e a classificação NORMALIZÁVEL
se mantém nos dados disponíveis. Não há medições adicionais que decidam a robustez pedida.
NORMALIZÁVEL é aqui o nome de uma classe baseada no expoente de discos pequenos, não uma
prova independente de normalização de um estado material no bulk.

Há fundamento para continuar testando a excitação como objeto matemático localizado na regra
de reconstrução escolhida. Sua interpretação como precursora de matéria permanece [H]/[?].
Não foram demonstrados elétron, massa eletrônica, carga, spin 1/2, estatística fermiônica,
partícula de Fock, quantização fotônica, geometria gravitacional real ou estabilidade temporal.

![Reanálise dos dados históricos](audit_output/archival_reanalysis.png)
