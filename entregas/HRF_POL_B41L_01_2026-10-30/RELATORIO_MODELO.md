# HRF-POL-B41L-01 — contrato do modelo e da interface v0.1.1

## Fontes efetivamente consultadas

[D] Capítulo0.1v0.2 (09/10/2026), integral: RUP B→A, componentes/interfaces, custo mínimo, G/W/D separados e preservação de falhas. Capítulo2v1.5 (29/10/2026), integral: especialmente §§2.3,2.4,2.5.3,2.7.2,2.11,2.13–2.14. Fonte B41L: pré-registro, LEIAME, b41l_comum.py, b41l_limpeza.py, b41l_bloco_b.py, malha.py e operadores/campos de c5a_photon_closure.py/c5a_curl_curl_emergente.py. Os resultados B41L recebidos foram auditados sem nova classificação. POL-01/P01–P05 não está presente; sua regra não foi inventada.

## Estado, geometria e dinâmica

[M] A conexão é a cochain real q por aresta orientada, U=exp(iq), com velocidade v e momento pi=M1v no gauge temporal, sem arrasto G. Caixa periódica L=4, sementes e sequência RNG idênticas à rotina `malha_do_caso`; PC.montar_W gera a malha tridimensional Delaunay e suas massas Whitney. N é número de nós, E de arestas, T de tetraedros; não são células de boundaryCFT. M1 e M2 positivos, K=d1T M2d1, H=1/2vT M1v+1/2qT Kq. Reutiliza o limite quadrático do cosseno Wilson; não executa a dinâmica compacta não linear.

[D] B41L não oferece uma função de passo independente: o velocity-Verlet está dentro de `b41l_bloco_b.conservacao`. O adaptador localiza e compila, sem mudar suas operações ou ordem, quatro nós AST originais: v+=dt*a/2; q+=dt*v; a=-lu.solve(K@q); v+=dt*a/2. Confere literalmente sua estrutura antes de compilar e registra o hash AST. Não altera nem importa uma versão reescrita do arquivo congelado. Um teste de64 nós compara bit a bit as amostras de energia à rotina original completa, no mesmo ambiente. Isso não demonstra equivalência binária com outra versão de Python/SciPy.

[D] Primário V1: q=ReQ como no original, v limpo pelo `Limpador` original. V0 usa v sem limpeza. Não há V1E como calibração, nem ajuste de xi. Q é o mapa de deRham original de -i*amplitude*Jones/omega em base transversal original. Definição de base: `b41l_limpeza.base_transversal`, ea×eb=kh; para +z ela retorna ea=y, eb=-x. H/V referem-se a esses eixos, não a x/y globais. Reversão de propagação também transforma a base e a interpretação do sinal de S3.

## Observável físico e gauge

[F/M] O código original PC.campos_tet reconstrói formas Whitney no centro dos tetraedros. O adaptador chama E=PC.campos_tet(C,i*v,1).E=-Wv e B=PC.campos_tet(C,q,1).B. Ele não chama q de campo elétrico. A energia global usa a massa completa M1, não uma quadratura de centro aproximada. O momento P operacional vem de integral de E×B por volume; sem afirmação de momento quântico individual.

[F/M] Gauge temporal residual: q→q+d0chi, v e pi inalterados, chi independente do tempo. E fica igual e B depende só de d1q, pois d1d0=0. Componente dinâmica de potencial escalar não é modelada e nenhuma invariância sob mudança temporal arbitrária de chi é reivindicada. O teste mede erros relativos ao campo não nulo e usa piso absoluto apenas no estado zero. O teste adversarial inclui um mapa errado E+0.1Wq, que quebra esse controle.

[M] Preparação inicial: fasor aproximado -Wv+iomegaWqT, com qT obtido por projeção somente no observador. Não muda o estado evoluído. O fasor inicial usa hipótese harmônica explícita e é um diagnóstico de preparação; a evidência de transporte vem da série temporal física E(t), não da Jones lançada.

## Fasores, Stokes e pureza

[M] Oito subvolumes fixos da caixa, pesos de volume calculados da malha. Em cada instante, registra-se a projeção espacial de E em exp(-ik·x), separando ea,eb e kh. O mapa é apenas medição, sem recalibrar amplitude por estado ou renormalizar a evolução. O erro da quadratura espacial de centro exige refinamento; direções reversas/diagonais e diferentes sementes estão no plano.

[M] Em janelas fixas de2,3,4períodos nominais, ajusta-se MQO complexa nas bases exp(-iomega t),exp(+iomega t),DC. Exige24amostras e condição<=100. Os fasores saem desses ajustes às séries do campo. Omega=|k| é fixo para todo o ensaio, inclusive quando a rede dispersa. Não se escolhe uma frequência para reduzir o resíduo; fases/frequências dinâmicas são apenas diagnósticos separados. Essa escolha pode reprovar o gate de extração mesmo se a dinâmica estiver correta mas fora da banda estreita nominal. O FAIL da fumaça é precisamente de qualidade de ajuste e não prova por si só falha do modelo fotônico.

[F/M] Coerência Cij=Σreg Vreg E_i*E_j/ΣVreg, com S0=TrC,S1=C11-C22,S2=2ReC12,S3=2ImC12. Assim (1,+i)/sqrt2 tem S3>0. A soma incoerente entre regiões permite DoP<1 e pureza<1; a identidade de um único vetor Jones puro não é usada como prova de preservação. S0 zero dá orientação/helicidade indefinidas. Os quocientes de Stokes são observáveis adimensionais; não são renormalização aplicada ao campo.

[?] O observável é estreito em banda e espacialmente projetado. Pode perder informação de modos fora da banda escolhida; resíduo, potência longitudinal e sensibilidade de janela medem essa limitação. Fase desenrolada e diferença omega1-omega2 só são reportadas com amplitude válida e passos de fase aceitáveis. Não inferem spin quântico, emissão, geometria emergente ou dicionário holográfico.

## Gates, custos e execução

[D] Valores exatos estão no pré-registro e em criterios.json. G0 protege hashes; G1 original PENDING; G2 preparação; G3 observáveis; G4 evolução; G5 três refinamentos, orientação, sementes e diferenças temporais; G6 comparação; G7 não pode PASS com dependência essencial pendente. V0 é par diagnóstico, V1 decide o setor principal. Famílias nunca descartam sementes ruins. Taxas são calculadas por semente com Clopper–Pearson95%, não tratando janelas correlacionadas como ensaios independentes.

[D] Preset completo2400casos,30montagens de malha por sequência seed/lado (as montagens inferiores podem repetir pela fidelidade da sequência RNG);1worker, sem promessa de aceleração GPU. Estimativa de pico5MB por nó +256MiB:~5.27GB no lado10; limite12GiB. Disco sem presumir compressão:até~46.9GB para família, teto128GiB e reserva2GiB. Números exatos são impressos por plan. O número de passos real depende das lascas e do limite wmax; se ultrapassar40961frames, o caso é BLOCKED_RESOURCES, sem subamostrar silenciosamente. Todas as amostras temporais são a cada passo; isso limita aliasing até o wmax original. Custo de CPU em segundos não é extrapolado de fumaça.

[D] Checkpoints atômicos por seed/n/k/estado/variante/dt, incluindo q,v,a, séries e snapshots. Retomada recompõe o estado do próximo passo sem duplicar amostras. Conclusão exige run.json COMPLETED e selo SHA de run/fields/evaluation. Mudança de fonte/configuração exige nova pasta e nova versão, em vez de reutilizar checkpoints indevidos. Resultados antigos permanecem congelados.
