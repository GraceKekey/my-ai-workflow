# HRF-FM — ELETRON-2D-POST-E67-01

**[D] RASCUNHO, NÃO CONGELADO, NÃO EXECUTADO.** Data: 2026-10-08.
Não confundir hashes de integridade deste pacote com pré-registro concluído.
A reprodução integral das covariâncias do E-67 deve preceder o congelamento.
Os dados históricos e o diagnóstico exploratório de VL já são conhecidos.

## 1. Dependências e etapas

A1: verificar os hashes e reaplicar o avaliador aos dados arquivados — concluído.
A2: executar novamente os sete casos originais, com ν registrado em todas as chamadas — pendente.
A3: comparar S, S0, sondas, energias, mapas e métricas, preservando discrepâncias — pendente.
B0: fixar ambiente, medir RAM/tempo do controle, validar implementação escalável — pendente.
B1: congelar protocolo, configuração, fonte e avaliador de extensão com SHA-256, antes de qualquer nova medição.
B2: executar w=7 primeiro, nas três redes; depois w=4,5,6 e controles; não selecionar resultados favoráveis.
C/D: novas larguras e amplitudes, cada bateria identificada; F dinâmica permanece PENDING.

## 2. Contrato histórico imutável

Rede triangular retangular periódica com número par de linhas, a=1, κ=1,
peso de ligação 1/√3 e massa por nó √3/2. Centro L/2+(0,25;0,1).
Polarização Z; perfil chapéu mexicano com média removida e norma euclidiana 1.
Mesma álgebra de diferenças de Z e momentos condicionada ao momento total da região;
termo clássico do centro excluído. Não substituir pela entropia de fatores locais sem registrar outra bancada.

H67-N: p_min≥2 NORMALIZÁVEL; p_min≤1 GRUDADA; restante INTERMEDIÁRIA.
Decisão agregada original somente para w={4,5,6,7}: pelo menos três classes iguais, senão MISTA.
H67-Z: ajuste z=intercepto+inclinação*w, CV populacional de z/w; PROPORCIONAL se CV≤0,10 e inclinação∈[0,7;1,5]; NÃO PROPORCIONAL se CV≥0,30 ou inclinação<0,4; senão PARCIAL.
VL: mediana de δS(0,25)/δS(0,1), selecionando |δS(0,25)|≥metade do máximo da janela. Aceitação [2;4,5], sem alterações.
VP≤0,3; VF≤0,01; V0 R²≥0,99 em 3≤ρ≤20; ν≥0,5−10⁻⁹;
VK≤10⁻⁸; V+≤10⁻⁸ em ρ≥5,5; três controles GRUDADA.
H67 geral preserva a regra original, incluindo a nota obrigatória “regime não linear” se VL falhar.
O fecho histórico w=7 é NOT_MEASURED.

## 3. Tamanho finito versus refinamento

**Tamanho finito:** a=1, mesmas larguras físicas, mesmas amplitudes, massa e κ.
Três redes candidatas iniciais: 64×74, 80×92, 96×112. A opção 128×148 fica subordinada ao orçamento.
Não chamar aumento de N a a fixo de refinamento espacial.

**Refinamento verdadeiro (bateria separada):** domínio físico fixo ~64×64,086,
(NX,NY,a)=(64,74,1),(96,112,2/3),(128,148,1/2).
A rede 96×112 não conserva exatamente Ly: substituir por uma sequência com dimensões físicas
exatamente coincidentes ou declarar e controlar a pequena diferença antes de congelar.
Uma sequência exata é (64,74,1),(128,148,1/2),(192,222,1/3), muito mais cara.
M(a)=√3 a²/2, peso 1/√3, κ=1: Ktil escala como 1/a², conservando c de longo comprimento.
Preservar w, centros, raios e domínio em unidades físicas, e normalizar o modo nas variáveis canônicas.
Definir previamente equivalência entre estados apertados sob discretização.
Não há implementação validada desse refinamento neste pacote; status PENDING.

## 4. Janela e geometria

Para o toro retangular original, o raio de injetividade é min(Lx,Ly)/2.
Na referência, vale 32. Discos individuais com ρ≤30 são admissíveis sem auto-sobreposição;
isso permite medir 4w=28 para w=7. Sobreposição entre diferentes discos de uma varredura é esperada
e implica correlação das medidas, não invalidação geométrica automática.
Registrar cardinalidade e máscara de cada disco, periodicidade, graus 6 e 3N ligações.
Usar primeiro ρ=0,5…30, passo 0,25, nas três redes para comparação em janela comum.
Relatar em separado cortes Rmax=24,28,30, sem extrapolar. Fecho em Rmax=28 possui apenas um raio de cauda;
por isso não demonstra convergência da cauda. Nas redes maiores, acrescentar Rmax=36 e 40 quando admissível.
Separar efeito de rede em janela fixa de efeito de janela na mesma rede.
z histórico mantém ρ≤3w; ampliar a janela global não altera z diretamente se esse trecho estiver completo.
H67-N depende das sondas pequenas, não do Rmax do perfil centrado.

## 5. Diagnóstico prioritário VL

Conservar VL oficial; exportar todos os raios selecionados, numeradores, denominadores e sinais.
Registrar contagens e medianas por sinal de δS, sem substituir a regra decisória.
As duas faixas de raios já observadas são diagnóstico retrospectivo, não teste independente pré-registrado.
Calcular VL no intervalo comum e em cada janela estendida. Identificar se surgem novos máximos
que alteram a seleção; não atribuir uma alteração exclusivamente à cauda sem conferir essa seleção.
Se a falha persistir com convergência, concluir no máximo não linearidade da resposta entrópica
ao aperto finito. O Hamiltoniano quadrático continua gerando evolução linear das variáveis canônicas.

## 6. Critérios novos propostos — ainda não congelados

Reprodução: tolerância absoluta 10⁻⁹ + relativa 10⁻⁸ nos arrays brutos; decisões idênticas;
divergências examinadas e registradas, sem afrouxar limites históricos.
Convergência de tamanho: comparar cada par adjacente em janela física comum;
|Δp_min|≤0,05, |Δz|/|z_maior|≤1%, |ΔVL|/|VL_maior|≤2%,
mesma classe por largura e mesmos controles nos três tamanhos.
Exigir os dois pares, não só o último; caso contrário NÃO_CONVERGIDO no intervalo testado.
Esses limites são escolhas operacionais [D], não constantes físicas nem prova do limite infinito.
Erro do perfil: max|δS_N−δS_maior|/max|δS_maior|≤1%, além dos critérios acima.
Repetição com solver alternativo e ν bruto antes de clipping: desvios entrópicos ≤10⁻⁹+10⁻⁸|S|.
Valores não finitos: INVALID, jamais INTERMEDIÁRIA/PASS. Não usar nanmin para ocultar sondas ausentes.
Nenhum teste de classe é válido se os controles físicos correspondentes falharem.

## 7. Larguras, amplitudes e regra de reconstrução

Candidatas fora da referência: w={3,8,9,10}, nas redes que acomodem pelo menos 4w+2 sem auto-sobreposição.
Não redefinir H67-N agregado para oito larguras: relatar referência e cada largura adicional separadamente.
Amplitudes separadas: r={−0,1;−0,05;0;0,025;0,05;0,1;0,25}; decisões históricas continuam r=0,25.
Comparar derivadas centradas em r=0 e termos quadráticos; r=0 controla cancelamento de S−S0.
Conservar modo e κ; perfis alternativos (p.ex. derivada gaussiana de média zero) exigem pré-registro próprio,
com normalização, energia e largura efetiva explicitadas para evitar comparar estados incompatíveis.
Uma só família de chapéu mexicano não demonstra universalidade da reconstrução.

## 8. Ajustes e incertezas

Comparar z=aw, z=aw+b, z=aw+b+cw², sempre indicando número de parâmetros e resíduos.
As quatro larguras históricas são treinamento/descritivas; novas larguras são validação fora da faixa.
Relatar erro de previsão, CV(z/w), estabilidade do intercepto e sensibilidade a ρmax/janela 3w.
Não inferir lei física da melhora do ajuste quadrático em quatro pontos.
Incertezas numéricas: diferenças de solver, tamanho, passo radial e resolução espacial;
não confundir resíduos do ajuste com erro numérico nem tratar discos correlacionados como amostras independentes.
Sem convergência espacial, a lei de escala física continua [?].

## 9. Dinâmica futura — derivação condicional, não bancada executada

No espaço físico sem modo constante, H=(pᵀp+xᵀKtil x)/2,
xdot=p e pdot=−Ktil x. Logo Σdot=AΣ+ΣAᵀ, A=[[0,I],[−Ktil,0]].
No subespaço positivo, Ω=√Ktil e
T(t)=[[cos(Ωt),Ω⁻¹sen(Ωt)],[−Ωsen(Ωt),cos(Ωt)]], Σ(t)=TΣ(0)Tᵀ.
A covariância cruzada x–p geralmente deixa de ser zero: não reutilizar a rotina estática XP
como se continuasse válida. É necessário derivar a redução gauge condicionada incluindo os blocos cruzados.
E=Tr(P+Ktil X)/2 é conservada analiticamente; a energia excedente evita subtrair grande energia de vácuo.
Gate futuro: energia, simplecticidade, positividade e redução gauge validadas antes de evolução.
Fase F=PENDING; nenhuma identificação automática com CAP3 ou com o fóton vetorial do Capítulo 2.
