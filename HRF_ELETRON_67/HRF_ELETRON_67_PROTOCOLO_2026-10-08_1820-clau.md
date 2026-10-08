# HRF — ELETRON-67 — Uma excitação localizada da fronteira aparece como objeto solto no bulk?
## Protocolo pré-registrado (fronteira 2D, leitura por Ryu–Takayanagi) — NÃO EXECUTADO

**Data:** 8 de outubro de 2026, 18h20 (America/Sao_Paulo)
**Autoria:** Mario José do Canto Filho, MD · desenho, código e execução numérica: Claude (`-clau`)
**Origem:** conversa de 8/10 depois da E-65 (17h–18h): onde fica o "ponto de atração" de uma partícula reconstruída
no bulk — no fundo da cúpula ou no meio da área da fronteira? Resposta dada [F]: na holografia, uma partícula é um
objeto **solto dentro do bulk**, a uma profundidade ligada ao seu tamanho; a fronteira só vê a sua "sombra" (o campo
que chega até ela), com largura da ordem da profundidade; o centro de atração é o centro do objeto, no bulk. Pedido do
pesquisador (18h03): **"ok, faça esse prompt mas não rode ainda".** A rodada só acontece depois de "pode rodar".
**Base:** `HRF_ELETRON_65_RELATORIO_2026-10-08_1455-clau.md` (padrões de relações = cúpulas apoiadas na fronteira, com
halo); `HRF_Nota_Modelos_de_Campo_Leitura_b_PT_2026-10-08_1520-clau.md`. **Decisão [D] (14h27):** leituras (a) e (b)
em paralelo, com tendência do pesquisador pela (b); esta bancada é da leitura (b).
**Marcas:** [F] estabelecido · [M] toy model · [H] hipótese HRF · [?] aberto · [D] decisão. **Nada aqui é elétron.**

---

## 1. Pergunta

Na E-65, um padrão nas **relações** do tapete (força κ menor num disco) foi lido no bulk como uma **cúpula apoiada na
fronteira**, com halo. Uma partícula deveria ser outra coisa: um objeto **solto** no bulk, que toca a fronteira só
pelo seu campo. Pergunta: uma **excitação quântica localizada do estado** do tapete — sem mudar nenhuma relação — é
lida pela regra de Ryu–Takayanagi

- **(i) como objeto do bulk**: só o campo dele chega à fronteira; ou
- **(ii) grudada na fronteira**, como o padrão de relações da E-65?

E a profundidade da imagem no bulk **acompanha o tamanho** da excitação?

## 2. Modelo e escolhas

- **Fronteira e campo [M]:** iguais aos da E-65, sem mudança no código (`src/e65_holo.py` copiado): tapete intacto,
  rede triangular a = 1, periódica, **64 × 74 = 4 736 GMFs**; polarização fora do plano (Z nos GMFs, Q conjugado);
  H = Σ Q²/(2M) + ½ Σ_e κ_e w_e (Z_i − Z_j)², w_e = 1/√3, M = √3/2, κ = 1 (c = 1). Vácuo quântico gaussiano.
  Entropia da álgebra invariante de gauge (diferenças de Z e momentos, condicionada ao fluxo total da região).
- **Excitação [D]: aperto (squeeze) de um único modo suave.** Modo f = "chapéu mexicano" de largura w,
  f ∝ (1 − r²/2w²) e^(−r²/2w²), com média exatamente zero (não mexe no modo constante de Z, que é gauge) e norma 1.
  O aperto faz X_f → e^r X_f e P_f → e^(−r) P_f; o estado continua gaussiano e o cálculo é exato. **As relações
  (κ) não mudam: muda o estado, não as regras** — na linguagem da holografia, é "estado" e não "fonte" [F].
- **Por que não uma onda clássica [F]:** num campo livre, qualquer estado coerente (onda clássica, inclusive um
  saca-rolha) é o vácuo deslocado por operadores que agem modo a modo; a entropia de toda região fica igual à do
  vácuo. Pela regra de Ryu–Takayanagi, a imagem no bulk de uma onda clássica é **nula**. Uma imagem exige uma
  excitação genuinamente quântica; o aperto é a mais simples entre as gaussianas. (Consequência para D-E1: §9.)
- **Regra holográfica [D]:** a mesma da E-65 — fronteira plana e bulk de três dimensões de espaço; um disco de raio
  ρ ↔ semiesfera de raio ρ, topo na profundidade ρ; forma linearizada.
- **Como separar "objeto do bulk" de "grudado" [F → M]:** num disco **pequeno** de raio ρ, longe de bordas:
  - se a excitação é uma mudança **suave do estado**, a mudança de entropia é governada pela primeira lei do
    emaranhamento (δS = δ⟨K⟩), proporcional à densidade de energia local vezes ρ³ (fronteira com duas dimensões de
    espaço). Na holografia, é o caso em que só o campo do objeto do bulk chega à fronteira (decaimento
    "normalizável", z^Δ) → **expoente p ≈ 3** em δS ∝ ρ^p;
  - se a excitação está **presa à rede ou às regras** (relações mudadas, ou edição na escala de um GMF), o disco
    pequeno muda pelas ligações que cruzam a sua borda, proporcional ao perímetro → **p ≲ 1**.
- **Profundidade [D]:** centroide de |δS(ρ)| dos discos centrados, na janela ρ ≤ 3w, lido como profundidade z
  (disco ρ ↔ topo na profundidade ρ). É uma profundidade **efetiva**: o valor absoluto depende da definição; o teste é
  como ela escala com w.
- **Sombra [F, descritivo]:** r50 = raio que contém metade de Σ|δε_i| (energia acrescentada em cada GMF). Referência:
  para uma partícula pontual na profundidade z₀ (AdS₄ de Poincaré), ⟨T₀₀⟩ ∝ z₀³/(z₀² + r²)³, r50 ≈ 0,64 z₀,
  logo **z/r50 ≈ 1,55**.

## 3. Parâmetros

| Item | Valores |
|---|---|
| Larguras do modo | w ∈ {4; 5; 6; 7} |
| Amplitudes do aperto | r ∈ {0,1; 0,25} (decisões com r = 0,25) |
| Centro | c = centro da caixa + (0,25; 0,1) |
| Discos centrados | ρ = 0,5 a 24, passo 0,25 |
| Discos pequenos | ρ ∈ {1; 1,5; 2; 2,5; 3}, centrados em d = 0,5w; w; 1,5w (ao longo de x); centro excluído (fumaça) |
| Mapa fora do centro | w = 5, r = 0,25: centro do disco d = 0…16, raio 1…16 (passo 1) |
| Controle "padrão" | κ = 0,25 num disco de raio R ∈ {4; 5} (como na E-65); discos pequenos em d = 0,5R; R; 1,5R |
| Controle V+ | unitário local invariante de gauge (aperto do modo-diferença de pares disjuntos de vizinhos dentro de P(c, 5), r = 0,25); discos pequenos em d = 2,5; 5; 7,5 |

## 4. Medidas

Para cada w e r: perfil δS(ρ) dos discos centrados; expoente p em cada posição (ajuste log-log de |δS| contra ρ nos
cinco discos pequenos) e p_min (menor das três posições); z (centroide, ρ ≤ 3w); z/w; r50; z/r50; energia
acrescentada total; ρ do pico; fecho = max |δS(ρ ≥ 4w)| / max |δS| (w = 4, 5, 6; em w = 7, 4w = 28 > 24, não
medível); razão δS/δ⟨K⟩ da primeira lei com K local (Bisognano–Wichmann) em 2 ≤ ρ ≤ 3w (exploratória); linearidade
= mediana de δS(r = 0,25)/δS(r = 0,1) onde |δS(0,25)| ≥ metade do máximo. Controles: p por posição e p_min.

## 5. Regras de decisão

| Código | Regra |
|---|---|
| **H67-N** (principal: objeto do bulk × grudado) | Por largura, com r = 0,25: p_min ≥ 2,0 → **NORMALIZÁVEL** (objeto do bulk: só o campo chega à fronteira); p_min ≤ 1,0 → **GRUDADA**; senão INTERMEDIÁRIA. Classe de H67-N = a classe de pelo menos 3 das 4 larguras; senão MISTA |
| **H67-Z** (profundidade acompanha o tamanho) | Ajuste z = a + b·w e CV de z/w: **PROPORCIONAL** se CV ≤ 0,10 e b ∈ [0,7; 1,5]; **NÃO PROPORCIONAL** se CV ≥ 0,30 ou b < 0,4; senão PARCIAL. O deslocamento a é registrado. *Uma profundidade que cresce com w é em parte esperada pela geometria e pelo campo sem escala (como a parede da E-65); o teste de fato é H67-N com os controles.* |
| **H67-R** (sombra × profundidade) | Descritivo: z/r50 comparado com 1,55 (partícula pontual) |
| **H67-L** (primeira lei) | Exploratório: mediana de δS/δ⟨K⟩ registrada |
| **H67** (geral) | **SIM** se H67-N NORMALIZÁVEL, H67-Z PROPORCIONAL e a base aprovada; **NÃO** se H67-N GRUDADA; senão PARCIAL; **INCONCLUSIVO** se V0, Vν, VK, V+ ou VC falharem |

## 6. Controles e validações

| Código | Exigência | Se falhar |
|---|---|---|
| V0 lei de área [F] | S(ρ) do vácuo linear em 3 ≤ ρ ≤ 20, R² ≥ 0,99 | INCONCLUSIVO |
| Vν | ν ≥ 1/2 em todas as regiões (tolerância 10⁻⁹) | INCONCLUSIVO |
| VK | independência do GMF de referência ≤ 10⁻⁸ (vácuo, ρ = 6) | INCONCLUSIVO |
| V+ fecho [F] | discos que contêm P(c, 5) (ρ ≥ 5,5): \|δS\| ≤ 10⁻⁸ (unitário local não muda a entropia de quem o contém) | INCONCLUSIVO |
| **VC controles grudados** | padrão R = 4, padrão R = 5 e V+ precisam sair **GRUDADA** pela mesma regra de H67-N | INCONCLUSIVO (a regra não separaria os casos) |
| VL linearidade | razão em [2,0; 4,5] para todas as larguras (linear puro ≈ 2,5; quadrático puro 6,25) | registrado; se falhar, H67 sai com a nota "regime não linear" |
| VP expoente estável | \|p_min(r = 0,1) − p_min(r = 0,25)\| ≤ 0,3 em todas as larguras | registrado |
| VF fecho do aperto | fecho ≤ 0,01 (w = 4, 5, 6) | registrado |
| Mapa fora do centro | δS de discos deslocados (w = 5) | descritivo (figura) |

## 7. Fumaça

Ver `fumaca/FUMACA_E67.md`. **Declarado:** a fumaça já mostrou p ≈ 2,8 a 3,1 nas quatro larguras (r = 0,25), os
controles com p ≤ 1 nas bordas, z/w = 1,91 → 1,59 (CV ≈ 0,07; inclinação ≈ 1,16; deslocamento ≈ 3) e z/r50 ≈ 3,7 → 3,0.
Os limiares foram escritos depois. O resultado esperado é **SIM**; o risco real está em H67-Z (CV perto do limiar) e
em VL. A rodada confirma com a grade completa, duas amplitudes, dois padrões de controle, V+, o mapa e as validações.

## 8. Ressalvas registradas antes

- **Campo livre:** como na E-65, Ryu–Takayanagi entra como **regra de reconstrução escolhida** [D]; o vácuo de um
  campo livre não é um estado holográfico no sentido de AdS/CFT. O resultado é [M] sobre essa regra [?].
- **Não é "uma partícula" no sentido de um quantum:** com r pequeno, o estado apertado é o vácuo mais um pouco de
  "pares de quanta" no modo f. Um estado de um quantum só (Fock) não é gaussiano e pede outra máquina [?].
- **Instante t = 0:** o modo f não é estacionário; ele se espalha com velocidade c = 1. Na holografia, uma excitação
  da fronteira que se espalha corresponde a uma partícula que **cai** para dentro do bulk [F]. A evolução no tempo
  não é testada aqui (candidata à próxima bancada).
- **Sem gravidade:** a bancada lê só o emaranhamento (área de Ryu–Takayanagi em primeira ordem). A atração (a
  curvatura do bulk em volta do objeto) viria das equações de Einstein linearizadas, que saem da primeira lei [F];
  não é calculada. "Objeto do bulk" aqui quer dizer: no mapa de emaranhamento, não como massa que curva o espaço.
- **Profundidade efetiva:** z é um centroide definido por [D]; a fumaça mostra um deslocamento fixo de ~3 unidades de
  rede. A sombra r50 usa |δε|, que mistura partes de primeira ordem (com sinal) e de segunda ordem; é descritiva.
- Só a polarização fora do plano (Z). Nada aqui é elétron: sem carga, sem spin, sem a massa do elétron.

## 9. Pedido de decisão [D] — exceção à D-E1

A D-E1 manda que todas as ondas injetadas sejam saca-rolhas. Nesta bancada:

1. **não há onda injetada**: a excitação é uma mudança quântica do estado no instante zero (como na E-65, que não
   injetou nada);
2. um saca-rolha é uma onda **clássica** (estado coerente); no campo livre, a imagem dele no bulk é exatamente zero
   [F] — seria um controle nulo que não acrescenta nada;
3. um saca-rolha precisa das **duas polarizações no plano** (os próprios U_nm como variáveis), que exigem o
   emaranhamento de gauge com modos de borda, ainda não implementado.

**Proposta:** registrar a E-67 como exceção à D-E1, com a versão saca-rolha pendente (polarização no plano + excitação
quântica circular). **Se o pesquisador não aprovar a exceção, a bancada não roda** e passa a depender da polarização
no plano.

## 10. Tempo e arquivos

Estimativa: 25 a 40 min em 2 processos (até ~2 GB de memória por processo; a máquina tem 7 GB).
Arquivos: `src/e65_holo.py` (cópia da E-65, sem mudança: mesmo SHA-256), `src/e67_particula.py`, `src/e67_rodar.py`,
`src/avaliar_e67.py`, `fumaca/`, `hashes_antes_da_execucao.txt`. Comandos da rodada (só depois de "pode rodar"):
`python3 src/e67_rodar.py` e depois `python3 src/avaliar_e67.py`.
