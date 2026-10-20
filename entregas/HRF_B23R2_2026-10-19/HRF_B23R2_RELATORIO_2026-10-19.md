# Relatório HRF B23-R2 — retomada completa

Entrega preparada em 2026-10-20T01:15:25.564555+00:00.

**Resultado geral do avaliador congelado: PARCIAL.**

B23a-R2: **PARCIAL**. B23b-R2: **CONVERGE_6F**.

## Objetivo

Concluir a emergência quântica nos aglomerados finitos e a convergência spin → rotor com as seis faces do cubo fechado, retomando a rodada recebida.

## Hipóteses

Razões elétricas e de anel próximas de 1 quando λ diminui, correções com ordem ≥ 1,5; D(S) estritamente decrescente em S=2–12 e ordem ≥ 1,5 na janela S=6–12. Regras completas no protocolo original incluído.

## Parâmetros

B23a: cubo S=1, faixa S=3, plaqueta S=4; λ=0,4,0,2,0,1,0,05. Controles: dois métodos em λ=0,1 para os três aglomerados, N1 e N3 no cubo. B23b: β=0,5,1,2,3; S=1,2,3,4,6,8,10,12; quatro rotores de referência, dois truncamentos e duas verificações de âncora.

## Protocolo e proveniência

Foram mantidos os casos calculados na máquina anterior e retomados somente os ausentes, com os arquivos científicos e regras de decisão intactos. O estado recebido, o ZIP original e os logs de ambas as fases estão preservados. Dois processos paralelos, com uma thread BLAS cada; limite de 4 CPUs e 32 GiB. A configuração original foi preservada; a proveniência da retomada está em PROVENIENCIA_RETOMADA.json.

Versões da retomada: {"python": "3.12.14", "numpy": "2.2.6", "scipy": "1.15.3", "matplotlib": "3.10.3"}. A troca de máquina e de bibliotecas é um desvio operacional documentado; não há alegação de reprodução bit a bit. Casos já recebidos não foram recalculados nesta execução.

## Medidas e resultados

### B23a-R2

| Caso | δJ (λ=0,05) | Anel (λ=0,05) | Ordem δJ | Ordem anel |
|---|---:|---:|---:|---:|
| cubo S=1 | 1.000012483 | 0.9997715805 | 1.04326 | 1.9844 |
| faixa S=3 | 1.000023428 | 0.9989899584 | 1.97376 | 2.00099 |
| plaqueta S=4 | 0.9998926203 | 0.998469838 | 2.00784 | 1.99231 |

### B23b-R2

| β | D(6) | D(12) | Ordem 6–12 | Monótono |
|---|---:|---:|---:|---|
| 0.5 | 0.001198788129 | 0.0003268320816 | 1.87448 | True |
| 1.0 | 0.01473287679 | 0.004073671407 | 1.85406 | True |
| 2.0 | 0.104604951 | 0.0300058335 | 1.80079 | True |
| 3.0 | 0.2864406184 | 0.08574221297 | 1.73897 | True |

## Controles e validade

Todos os 12 casos principais e 5 controles da B23a, e os 36 casos (32 spins + 4 rotores) e 4 controles da B23b estão presentes. A cobertura exata, preservação dos valores recebidos e sete hashes congelados foram verificados.

B23a:

```json
{
  "decisao": "PARCIAL",
  "A0": true,
  "A1": true,
  "A2": true,
  "A3": false,
  "A4": true,
  "todos_os_lacos": true,
  "dois_metodos": true,
  "N1": true,
  "N3": true,
  "N3_razoes_livres": [
    0.9992328939445165,
    0.9992328939445351
  ]
}
```

B23b:

```json
{
  "decisao": "CONVERGE_6F",
  "validade": {
    "discordancia_E_H_max": 1.0800249583553523e-12,
    "residuo_max": 1.1727258643029046e-12,
    "seis_faces_iguais": true,
    "truncamento_max": 2.681472053443005e-13,
    "ancora_max": 0.0,
    "valido": true
  },
  "recertificacao_B23R_max_dif": {
    "0.5": 1.7203252711261996e-14,
    "1.0": 1.8028981085826956e-14,
    "2.0": 9.547918011776346e-15
  },
  "recertificado": true
}
```

Resultados detalhados de cada regra por caso estão em resultados/avaliacao_B23R2.json. O teste sintético exercitou todos os ramos do avaliador, sem contar como evidência física. Figuras foram geradas somente após a avaliação.

## Interpretação e limites

Na B23a-R2, critérios que não passaram: A3. Em cubo S=1, A3 não passou: ordem elétrica 1.0432588 e ordem do anel 1.9844016; a regra exige ambas ≥ 1,5 na janela λ=0,2,0,1,0,05. Na B23b-R2, a validade numérica passou, D(S) decresceu estritamente para os quatro β e todas as ordens da janela de decisão superaram 1,5.

A interpretação deve seguir as regras congeladas, inclusive possíveis resultados parciais ou inconclusivos. Esta é uma bancada em aglomerados finitos: não demonstra a fase de Coulomb no limite termodinâmico. O cubo é uma superfície fechada de seis faces, não uma rede cúbica periódica. ħ já entra nas relações de comutação; o experimento não deriva ħ. Os 18 pares conhecidos da B23R são recertificação, e não teste cego. B23c não foi reexecutada.

O ZIP inclui código, protocolo, entrada original, estado recebido, resultados, logs, figuras, tabelas e hashes. Não é necessário acessar o repositório para ler ou reproduzir o pacote.
