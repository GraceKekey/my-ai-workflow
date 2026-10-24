# Baseline anterior: fatos acessíveis e números informados

**Estado: CÓDIGO NOVO — PRÉ-REGISTRADO — SIMULAÇÕES CIENTÍFICAS NÃO EXECUTADAS.**

[D] VVR-01, v0.1, 24/10/2026. [F] física estabelecida; [M] modelo; [H] hipótese; [?] aberto; [D] decisão.


[D] O pacote SPIRAL local é a entrega de 23/10 com 45 testes e smoke técnico 13³, t=0,6, cinco frames por giro. A rodada científica posterior foi executada por Mario no Colab, conforme seu relato. Seu relatório e os volumes não estavam acessíveis nesta auditoria; os dois conjuntos não são confundidos. `reports/baseline_informado.json` transcreve os valores fornecidos, com o marcador RAW_NOT_VERIFIED.

[M, configuração verificável no código] Preset antigo plano: x,y=±130, z=±25, 67×67×33; fonte ω=0,13, m=0,05, F=0,02, σxy=12, σz=10, pulso sin² de160, t_final=520, dt solicitado0,1 e registros0,5. Casas Ω=1,85, γ=0,10, g=0,05; extras passivos; rede estacionária desligada. A geometria desse preset era flat. A fonte antiga normalizava a carga na massa discreta de cada caso.

[M, informado, sem nova conferência bruta] Dois casos s±, 1.041 frames cada; PASS dos pipelines de visualização, zscan e helicity; estrutura INCONCLUSIVE_SPIRAL_STRUCTURE; zero torções aceitas, 1.041 cristas ambíguas/indefinidas e zero relés por caso. Quiralidade média aproximada ±0,107966586 e erro de reflexão da potência angular ~3,8e−16. Fluxo líquido relativo máximo: 5,184e−12 /9,756e−12; assimetrias hemisféricas:1,828e−12 /1,524e−12. São alegações do registro fornecido, não números reproduzidos aqui.

[F/M] Para a relação dispersiva plana ω²=k²+m², a portadora dá k=0,12, comprimento2π/0,12≈52,36 e velocidade de grupo0,12/0,13≈0,9231. Um pulso tem banda finita: a portadora sozinha não certifica resolução ou dessintonia. O kz exploratório informado~0,01177 e passo formal~533 não passaram pelo gate antigo e não demonstram uma hélice.

[?] Leitura máxima~2,46e−11 precisa ser conferida em `observations.npz`, incluindo o canal histórico completo e eventuais componentes estacionárias. O limiar de trava plano s+ presente na tabela congelada é1,1031300280569998e−8; o valor da leitura não foi confirmado. Ωfonte≠Ωreceptor é uma hipótese parcial, não explicação causal já estabelecida. Outras causas incluem diluição3D, massa/dispersão, normalização, transientes, filtragem e acoplamento.

[D] A rotina de reanálise verifica hashes dos frames e cortes, reproduz o readout com o módulo histórico, mede espectros e fluxos orientados, e escreve em outra pasta. O campo `previous_archived_verdict` é preservado. Novos diagnósticos e critérios não reescrevem o veredito antigo.

[?] Há confirmação local da inconsistência RUNNING/COMPLETED nos dois smokes antigos; a origem no código foi inspecionada. A situação nos arquivos científicos do celular continua pendente. Impactos quantitativos das demais erratas não foram medidos na rodada grande.
