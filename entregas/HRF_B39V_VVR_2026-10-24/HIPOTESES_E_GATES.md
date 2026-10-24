# Hipóteses, estados e critérios quantitativos

**CÓDIGO NOVO — PRÉ-REGISTRADO — SIMULAÇÕES CIENTÍFICAS NÃO EXECUTADAS.**

[D] v0.1 · 24/10/2026 · W apenas; G/D separados.


[D] Valores exatos: `config/gates.json`, cobertos pelo manifesto. Tolerâncias são escolhas anteriores às execuções, motivadas por alvos de discretização e controles negativos; NÃO são barras de erro já medidas. Nenhum limiar de disparo histórico é ajustável nesta bancada.

| Estado | Definição e grandezas | Incerteza/tolerância | Controles que podem fazê-lo falhar |
|---|---|---|---|
| PASS_SOFTWARE | Todos os testes algébricos/de integridade passam; sintaxe/importações válidas | zero falhas; log completo | corrupção de chunks, NaN, controles de falso candidato, configuração alterada |
| PASS_NUMERICAL_REFERENCE | Modo KG analítico na caixa, três malhas e três dt efetivos | RMS≤0,02; ordem espacial≥1,5; temporal≥3,5 | erro de sinal, dt instável, ordens incorretas; NÃO EXECUTADO |
| PASS_VERTICAL_SYMMETRY_CONTROL | Reflexão do escalar, energia e vetor J | erro L2 relativoφ≤2e−6; e≤1e−3; J≤5e−3; denominador≥1e−30 | fonte/indexação/sponge assimétricas; domínio assimétrico não é teste aplicável |
| PASS_ENERGY_BALANCE | H−H0−Wfonte+Dsponge+Drec | erro relativo≤1e−6; escala=max(|H|,|H0|,|W|+|D|,1e−20) | dissipação omitida, adjunto errado, passo inadequado |
| PASS_PHASE_DIAGNOSTIC | Lock-in definido em anel de amplitude válida | ≥16 registros; janelas1,5/2/2,5ciclos; pisos1e−14 e1e−6 | janela curta, campo zero ou alias; não significa torção |
| PASS_AZIMUTHAL_FLOW_DIAGNOSTIC | Correntes físicas, circulação e momentos finitos calculados | tríade métrica e quadratura explícitas; alinhamento indefinido quando denominador nulo | métricas inválidas, fluxo não finito, componente coordenada tratada como própria |
| PASS_RECEIVER_SPECTRAL_DIAGNOSTIC | Espectro recebido e reprodução do readout bruto | ≥16 amostras uniformes; erro do canal≤1e−10; potência no décimo superior da banda≤1e−3 | canal de rede omitido, amostragem insuficiente, troca de Ω/unidades |
| HELICAL_PHASE_CANDIDATE | kz linear não nulo, pureza do modo e persistência entre janelas | pureza≥0,6; ≥4z conectados; span≥0,5rad; RMS/span≤0,25; sensibilidade de kz≤20%; passo de fase≤0,8π | m≠0 comkz0; lacuna preenchida; ajuste fora do domínio; resolução inadequada |
| HELICAL_ENERGY_TRANSPORT_CANDIDATE | Curvas J/e com deslocamento axial e rotação, medidas em cada hemisfério | critérios detalhados abaixo e TODOS os controles necessários verdadeiros | fase que gira radialmente; circulação sem z; z reto; empates de lobo; reflexão |
| NO_RESOLVED_HELICAL_TRANSPORT | Ambos os hemisférios têm dados/controles adequados e não atingem o critério | não substitui ausência de informação por nulo físico | se faltar qualquer controle, retornaINCONCLUSIVE |
| INCONCLUSIVE | Informação, fase, domínio, sementes ou certificação insuficientes | nenhum PASS inferido da ausência de dados | dados ausentes, piso não alcançado, retorno grande, resolução duvidosa |
| FAIL_NUMERICAL | Referência, paridade aplicável ou balanço falha; dados não finitos | tolerâncias acima; nenhuma correção pós-hoc silenciosa | mutações de sinais, fontes de energia omitidas, matriz inválida |
| BLOCKED_RESOURCES | Estimativa/cota ou recursos reais impedem execução | RAM/disco/CPU proxy congelados; reserva2GiB | memória1byte, disco insuficiente, CPU acima da cota |
| BLOCKED_MISSING_HISTORICAL_DATA | Referência obrigatória ou dado histórico necessário ausente | nomes e tentativas registrados; não preencher com dados sintéticos | bibliografia inacessível, geometria ausente, baseline sem arquivos reais |

[D] Para ANGULAR_PHASE_STRUCTURE: potência dos modos m≠0≥0,5 em algum anel utilizável. AZIMUTHAL_ENERGY_CIRCULATION: |integralJtheta|>0,05 integral|Jtheta|. VERTICAL_ENERGY_TRANSPORT: energia bruta para fora acumulada por pelo menos um par de planos>0,01 do máximo deEcampo; planos distintos não são somados para contar a mesma energia várias vezes. São flags operacionais, não conclusão de partículas ou de fluxo líquido ascendente.

[D] Aceitação de curvas por hemisfério: plano≥3σz e sementes somente após desligamento completo da fonte; tempo inicial=max(primeiro10% da fluência final, fim da fonte). Pelo menos16 sementes com erro de quadratura≤5%. Cada curva: ≥16frames, ≥um período, raio≥2Δ, spanθ≥π, |Δz|≥max(20,4Δ), CVr≤0,25, RMS relativoθ(z)≤0,20, ≥90% incrementos axiais para fora. Segmentos inválidos não são reconectados. Fluxo ponderado amostrado candidato≥20%, refluxo≤10%. Norma física deJ/e deve ser≤1+1e−5 e Δtvolume≤0,5 menor célula. Saída na sponge encerra o trecho, sem completar uma volta artificial.

[D] Controles obrigatórios para aceitar transporte: referência numérica, energia, paridade, convergência ESPACIAL e TEMPORAL, robustez de FRONTEIRA e refinamento das CURVAS. Campo em ROI/tempos comuns deve variar≤5%, chegada≤5%, fluxos≤10%, resposta dos receptores≤10% e classificações devem ser preservadas. Fração das curvas pode mudar no máximo0,05 absoluto, mantendo classificação. Evidências incluem hashes dos arquivos reais; um plano de execução não certifica um teste.

[D] Resolução mínima:3células porσ e12 por comprimento de onda próprio. Além da portadora, planejamento usaω+4π/duração como proxy conservadora da banda do pulso, sem alegar corte espectral rígido. A reanálise usa banda95% medida, ignorando canais abaixo do piso relativo de potência1e−12 ou absoluto1e−28, e verifica max(r)k95≤0,8Ntheta/2. Aliasing já introduzido antes da gravação exige refinamento; não é excluído só pelo espectro amostrado.

[?] Os erros de ajuste de kz são descritivos; variação com janela/malha/fronteira é parte obrigatória da avaliação. PASS de funcionamento não é PASS físico. G/D permanecemBLOCKED_NO_VALIDATED_HOLOGRAPHIC_DICTIONARY em todos os ramos.
