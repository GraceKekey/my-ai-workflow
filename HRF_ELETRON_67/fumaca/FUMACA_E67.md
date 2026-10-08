# Fumaça da E-67 (antes do registro) · 8/10/2026 18h04–18h16 · -clau

Máquina igual à da E-65 (`src/e65_holo.py`, copiado sem mudança): tapete intacto, polarização Z, vácuo quântico,
entropia da álgebra invariante de gauge. Excitação: aperto (squeeze) do modo "chapéu mexicano" de largura w.

1. `fum1.py` (caixa 40 × 46; r = 0,5 e 1,0; w = 1,5 a 4): o aperto muda δS de discos centrados com um perfil que
   **acompanha w** (o pico se desloca de ρ ≈ 3 para ρ ≈ 8 quando w vai de 1,5 a 4, com r = 0,5) e **fecha** longe
   (δS → 0 para ρ ≳ 4w). A energia acrescentada cai com w (0,31 → 0,12 com r = 0,5). r = 1,0 já é forte demais
   (pico deslocado para ρ ≈ w, perfil deformado) → **descartado; amplitudes da rodada: r = 0,1 e 0,25.**
2. `fum2.py` (40 × 46, r = 0,5): mapa de discos pequenos (ρ = 1 e 1,5) andando para fora do centro. O aperto dá
   um sinal suave, com um só máximo em d ≈ 0,85w, que some longe (d ≳ 2w); o padrão de relações (κ = 0,25,
   R = 5,66) dá picos irregulares **dos dois lados da borda** (d ≈ 3,5 e 7,5). Centroide do perfil centrado
   (w = 4): 7,66 (r = 0,25) e 7,24 (r = 0,5).
   Razão dos máximos r = 0,5 / r = 0,25 (w = 4): 2,85 (linear puro em e^r − 1 daria 2,28) → há parte de segunda
   ordem; a faixa de VL foi escrita depois disto (§ abaixo).
3. `fum3.py` (48 × 56): **expoente p de δS ∝ ρ^p em discos pequenos (ρ = 1 a 3)**:
   - aperto w = 4 e 6, r = 0,1 e 0,25, posições d = 0,5w; w; 1,5w: **p = 2,4 a 3,7** (estável entre r = 0,1 e 0,25:
     diferença ≤ 0,15). No centro (d = 0) δS é negativo e p = 4,1 a 6,9 (o disco pequeno está no "platô" do chapéu e só
     vê ordens altas) → **centro excluído das posições da rodada.**
   - padrão de relações R = 5: p = 3,42 no centro (por dentro o tapete é uniforme e a entropia do campo livre não
     depende de κ uniforme), **p = −0,80 na borda (d = R)**, 2,2 a 2,3 em d = R/2 e 1,5R → o mínimo sobre posições
     marca o padrão como **GRUDADO**.
   - V+ (unitário local em pares de vizinhos, raio 5): p = 1,08 (d = 0) e −0,53 (d = 2,5) → GRUDADO.
4. `fum4.py` (caixa 64 × 74, r = 0,25): w = 3 é grosso demais (p = 0,71 no centro, 2,0 em d = 0,5w) → **w = 3
   descartado**; w = 7 cabe (p = 3,03; 3,28; 3,64), mas o centroide sobre todo ρ fica cortado pela caixa e o fecho
   em 4w = 28 não é medível → **centroide numa janela ρ ≤ 3w.**
5. `fum5.py` (64 × 74, r = 0,25; posições 0,5w; w; 1,5w; janela ρ ≤ 3w):

   | w | p por posição | p_min | z (centroide) | z/w | r50 da sombra | z/r50 | E acrescentada |
   |---|---|---|---|---|---|---|---|
   | 4 | 2,84; 2,91; 3,22 | 2,84 | 7,64 | 1,910 | 2,06 | 3,7 | 0,0280 |
   | 5 | 2,81; 3,11; 3,68 | 2,81 | 8,87 | 1,774 | 2,71 | 3,3 | 0,0224 |
   | 6 | 3,13; 3,22; 3,33 | 3,13 | 10,04 | 1,674 | 3,22 | 3,1 | 0,0187 |
   | 7 | 3,03; 3,28; 3,64 | 3,03 | 11,13 | 1,589 | 3,73 | 3,0 | 0,0161 |

   CV(z/w) ≈ 0,07; ajuste z = a + b·w: b ≈ 1,16, a ≈ 3,0 (z/w cai devagar: há um deslocamento fixo de ~3
   unidades de rede). Tempo: ~30 s por largura.

**O que já se viu antes do registro (declarado):** o aperto suave dá p ≈ 3 em todas as larguras (objeto do bulk);
padrão de relações e V+ dão p ≤ 1 (grudados); z cresce com w com inclinação ≈ 1,2 e CV(z/w) ≈ 0,07, perto do limiar
0,10. Os limiares do protocolo (p ≥ 2 / p ≤ 1; CV ≤ 0,10 com inclinação em [0,7; 1,5]; VL em [2,0; 4,5]; VP ≤ 0,3)
foram escritos **depois** disto. A rodada confirma com a grade completa (ρ de 0,25 em 0,25), duas amplitudes,
dois padrões de controle, V+, o mapa fora do centro e as validações. O resultado esperado é **SIM**; o risco real
de não confirmação está em H67-Z (CV perto do limiar) e em VL.

Teste do pipeline: só no modo `teste` (caixa 24 × 28, w = 2 e 3, na pasta temporária da sessão), para checar que os
scripts rodam de ponta a ponta. O resultado desse modo não tem sentido físico (caixa pequena demais) e não entra no
registro. `dados/` e `resultados/` da rodada estão vazios.
