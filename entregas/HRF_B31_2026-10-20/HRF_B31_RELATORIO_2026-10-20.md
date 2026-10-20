# HRF B31 — relatório da execução completa

Concluído em 2026-10-20T09:44:31.239776+00:00.

**H-par no modelo livre: INCONCLUSIVA.**

| Bloco | Decisão congelada |
|---|---|
| B31a | INCONCLUSIVO |
| B31b | DUAL_EXATO |
| B31c | GAP_QUEBRA_CHM |
| B31d | CONFIRMADA |

## Objetivo

Testar a hipótese paralela de GMFs emaranhados no modelo livre: Hamiltoniano modular de um disco, dualidade espectral, efeito da massa e uma partícula atravessando a região.

## Hipóteses

A: forma local CHM e aproximação ao limite contínuo. B: igualdade dos espectros não nulos e contagens dos modos nulos. C: a massa aumenta o desvio de CHM e reduz a entropia. D: excesso de Rényi-2 próximo da previsão de quasipartícula, pico perto de ln 2, passagem da ola e independência das helicidades.

## Parâmetros

```json
{
  "B31a": {
    "R": [
      8,
      12,
      16
    ],
    "L_principal": 1024,
    "L_controle": 512
  },
  "B31b": {
    "triangular_n": [
      24
    ],
    "rsa": {
      "N": 600,
      "densidade": 0.9,
      "dmin": 0.8,
      "sementes": [
        20263101,
        20263102,
        20263103
      ]
    }
  },
  "B31c": {
    "R": 12,
    "massas": [
      0.0,
      0.1,
      0.2,
      0.4
    ],
    "L": 1024
  },
  "B31d": {
    "R": 20,
    "Lt": [
      1024,
      2048
    ],
    "k0": [
      0.8,
      0.0
    ],
    "dk": 0.13333333333333333,
    "x_ini": -35.0,
    "tempos": [
      0,
      2,
      4,
      6,
      8,
      10,
      12,
      14,
      16,
      18,
      20,
      22,
      24,
      26,
      28,
      30,
      32,
      34,
      36,
      38,
      40,
      42,
      44,
      46,
      48,
      50,
      52,
      54,
      56,
      58,
      60,
      62,
      64,
      66,
      68,
      70
    ],
    "taus": [
      1e-10,
      1e-12
    ]
  }
}
```

## Protocolo

Executado src/rodar_B31.py completo, seguido de src/avaliar_B31.py resultados, ambos com Python isolado (-I) e uma thread BLAS. Não houve alteração no código científico ou nas regras congeladas. Não se usaram os resultados de fumaça na decisão. O ZIP de entrada e a fumaça recebida foram preservados. O teste sintético do avaliador alcançou todos os ramos; não é evidência física.

Versões e máquina da execução:

```json
{
  "modo": "completo",
  "python": "3.12.14",
  "numpy": "2.2.6",
  "scipy": "1.15.3",
  "maquina": "Linux-6.18.55-x86_64-with-glibc2.41",
  "inicio": "2026-10-20 06:40:52"
}
```

## Medidas e resultados

### B31a — modular

| R | Desvio máximo | Desvio canônico | Localidade N | ΔL | Δq |
|---|---:|---:|---:|---:|---:|
| 8 | 0.00309902992 | 0.111901523 | 0.998179758 | 0.000158545668 | 0.000761890695 |
| 12 | 0.000626867423 | 0.110813599 | 0.990577502 | 0.000501075988 | 0.000873405479 |
| 16 | 0.00112926551 | 0.110161574 | 0.973166741 | 0.00120552365 | 0.00103611465 |

### B31b — dualidade

| Malha | Diferença espectral | Nulos Z / gauge / previstos |
|---|---:|---|
| triangular_24 | 2.66453526e-15 | [1, 1153, 1153] |
| rsa_600_20263101 | 6.10815923e-15 | [1, 1201, 1201] |
| rsa_600_20263102 | 7.31174477e-15 | [1, 1201, 1201] |
| rsa_600_20263103 | 5.38768574e-15 | [1, 1201, 1201] |

### B31c — massa

| m | Desvio máximo | S |
|---|---:|---:|
| 0.0 | 0.000626867423 | 6.01201854 |
| 0.1 | 0.292439401 | 5.4637322 |
| 0.2 | 0.465657339 | 4.91755385 |
| 0.4 | 0.500786262 | 3.9557275 |

### B31d — passagem do quantum

```json
{
  "decisao": "CONFIRMADA",
  "validade": true,
  "falhas_validade": [],
  "dif_Lt": 1.4042876870734577e-05,
  "D1": {
    "avaliavel": true,
    "passa": true,
    "p_E_max": 0.9955202819456997,
    "dS2_no_p_E_max": 0.009500489454107707
  },
  "D2": {
    "passa": true,
    "dS2_max": 0.6699002379392304,
    "em_unidades_de_log2": 0.9664617511652643,
    "p_E_no_max": 0.4443067750662065
  },
  "D3": {
    "passa": true,
    "max_dif_quasiparticula": 0.028078965893089836
  },
  "D4": {
    "passa": true,
    "max_dif_circular_linear": 0.0029017271079641027
  },
  "D6": {
    "passa": true,
    "max_dif_helicidades": 0.0
  }
}
```

## Controles

A cobertura exata dos 13 casos foi conferida: A=3, B=4, C=4, D=2. Cada caso D contém os 36 instantes e ambos os cortes. Os oito hashes do código e protocolo continuam iguais aos do pré-registro. A tabela de D preserva todas as polarizações e os controles.

Avaliação completa:

```json
{
  "modo": "completo",
  "B31a": {
    "decisao": "INCONCLUSIVO",
    "validade": false,
    "falhas_validade": [
      "R=16: |Δρ| entre L1024 e L512 = 1.21e-03"
    ],
    "por_R": {
      "8": {
        "desvio_max": 0.003099029919924501,
        "desvio_M_canonico": 0.11190152270452458,
        "razoes_min_max": [
          0.9969009700800755,
          1.0005928823994996
        ],
        "localidade_N_media": 0.9981797578990058,
        "localidade_M_media": 0.9953557141149232,
        "dif_L": 0.00015854566828021888,
        "dif_q": 0.0007618906946126325,
        "R_efetivo": 8.150774926246335
      },
      "12": {
        "desvio_max": 0.0006268674231121318,
        "desvio_M_canonico": 0.11081359898881882,
        "razoes_min_max": [
          0.9993731325768879,
          1.0001397687236893
        ],
        "localidade_N_media": 0.9905775022089247,
        "localidade_M_media": 0.9961163103899189,
        "dif_L": 0.0005010759876754589,
        "dif_q": 0.0008734054788891443,
        "R_efetivo": 11.93811205620609
      },
      "16": {
        "desvio_max": 0.001129265513780231,
        "desvio_M_canonico": 0.11016157356035072,
        "razoes_min_max": [
          0.9988707344862198,
          1.000164562370744
        ],
        "localidade_N_media": 0.973166741212166,
        "localidade_M_media": 0.9969722227954343,
        "dif_L": 0.0012055236533794478,
        "dif_q": 0.0010361146499031637,
        "R_efetivo": 16.0200999004015
      }
    },
    "melhoria_aproxima_de_1": true
  },
  "B31b": {
    "decisao": "DUAL_EXATO",
    "malhas": [
      {
        "malha": "triangular_24",
        "passa": true,
        "dif": 2.664535259100371e-15,
        "nulos": [
          1,
          1153,
          1153
        ]
      },
      {
        "malha": "rsa_600_20263101",
        "passa": true,
        "dif": 6.1081592279117775e-15,
        "nulos": [
          1,
          1201,
          1201
        ]
      },
      {
        "malha": "rsa_600_20263102",
        "passa": true,
        "dif": 7.311744772471354e-15,
        "nulos": [
          1,
          1201,
          1201
        ]
      },
      {
        "malha": "rsa_600_20263103",
        "passa": true,
        "dif": 5.387685743695656e-15,
        "nulos": [
          1,
          1201,
          1201
        ]
      }
    ]
  },
  "B31c": {
    "decisao": "GAP_QUEBRA_CHM",
    "massas": [
      0.0,
      0.1,
      0.2,
      0.4
    ],
    "desvio_max_por_massa": [
      0.0006268674231121318,
      0.29243940072641594,
      0.46565733890890715,
      0.5007862620493637
    ],
    "S_por_massa": [
      6.012018536307598,
      5.463732204944469,
      4.91755385374984,
      3.9557274958368738
    ],
    "S_decresce": true
  },
  "B31d": {
    "decisao": "CONFIRMADA",
    "validade": true,
    "falhas_validade": [],
    "dif_Lt": 1.4042876870734577e-05,
    "D1": {
      "avaliavel": true,
      "passa": true,
      "p_E_max": 0.9955202819456997,
      "dS2_no_p_E_max": 0.009500489454107707
    },
    "D2": {
      "passa": true,
      "dS2_max": 0.6699002379392304,
      "em_unidades_de_log2": 0.9664617511652643,
      "p_E_no_max": 0.4443067750662065
    },
    "D3": {
      "passa": true,
      "max_dif_quasiparticula": 0.028078965893089836
    },
    "D4": {
      "passa": true,
      "max_dif_circular_linear": 0.0029017271079641027
    },
    "D6": {
      "passa": true,
      "max_dif_helicidades": 0.0
    }
  },
  "global": "INCONCLUSIVA",
  "regras": {
    "a": {
      "tol_L": 0.001,
      "tol_q": 0.01,
      "nu_min": 0.499999999,
      "tol_chm": 0.05,
      "faixa": [
        0.8,
        1.2
      ],
      "loc_chm": 0.95,
      "loc_nao": 0.8,
      "q_dec": "13",
      "q_ctrl": "12"
    },
    "b": {
      "tol_dif": 1e-09,
      "tol_area": 1e-10
    },
    "c": {
      "fator": 2.0,
      "piso": 0.05,
      "q": "13"
    },
    "d": {
      "tol_Z": 1e-08,
      "tol_tau": 1e-06,
      "tol_E": 1e-08,
      "tol_Lt": 0.001,
      "nu_min": 0.499999999,
      "D1_pmin": 0.9,
      "D1_max": 0.34657359027997264,
      "D2": [
        0.85,
        1.15
      ],
      "D2_p": [
        0.3,
        0.7
      ],
      "D3": 0.1,
      "D4": 0.02,
      "D6": 1e-10
    }
  }
}
```

Controles suplementares calculados das três polarizações (não alteram a decisão):

```json
{
  "max_diferenca_tau_todas_polarizacoes": 6.222130033428641e-09,
  "max_diferenca_Lt_todas_polarizacoes": 1.4042876870734577e-05,
  "max_erro_Z": 3.6919356460884956e-12,
  "max_erro_energia": 2.886579864025407e-15
}
```

## Interpretação

B31a: validade numérica não aprovada: R=16: |Δρ| entre L1024 e L512 = 1.21e-03. A classificação inconclusiva não constitui refutação física.
A conclusão segue os critérios congelados, sem ajustar limites ou selecionar casos após conhecer os resultados. A classificação global não pode ser extrapolada para uma teoria holográfica completa.

### Auditoria adicional e limites

Em B31d o código congela os autovalores de Williamson por ν² → max(ν², 1/4). Por isso, o nu_min gravado não é uma verificação independente do limite inferior antes desse ajuste. A auditoria suplementar recalculou os dois mínimos brutos, sem modificar a bancada, e confrontou a fórmula de Rényi-2 com matrizes de Fock de um modo em três ocupações térmicas. Resultados:

```json
{
  "nota": "Suplemento; não altera a classificação do avaliador congelado.",
  "nu_bruto_B31d": {
    "1024": {
      "nu_min_antes_do_clipping": 0.4999999999995148,
      "nu2_min": 0.2499999999995148,
      "passa_limite_protocolo": true
    },
    "2048": {
      "nu_min_antes_do_clipping": 0.49999999999858125,
      "nu2_min": 0.24999999999858127,
      "passa_limite_protocolo": true
    }
  },
  "um_modo": [
    {
      "n": 0.2,
      "fock_dim": 180,
      "renyi2_formula": 0.6658302836507239,
      "renyi2_fock": 0.6658302836507235,
      "diferenca": 4.440892098500626e-16
    },
    {
      "n": 1.0,
      "fock_dim": 180,
      "renyi2_formula": 0.5908158228412321,
      "renyi2_fock": 0.5908158228412326,
      "diferenca": 4.440892098500626e-16
    },
    {
      "n": 3.0,
      "fock_dim": 180,
      "renyi2_formula": 0.5072192238294008,
      "renyi2_fock": 0.5072192238294004,
      "diferenca": 3.3306690738754696e-16
    }
  ]
}
```

A onda coerente tem ΔS₂=0 por construção; não é uma evolução independente calculada do estado coerente. As duas polarizações são cópias iguais do campo fora do plano, como definido no protocolo; não constituem uma simulação completa da polarização de gauge nas ligações. É um campo livre não compacto, sem vórtices; não demonstra reconstrução holográfica do bulk, regime de N grande ou acoplamento forte. B31d mede Rényi-2, e a precisão é dupla.

## Reprodução e arquivos

Código e protocolo completos em src/ e no protocolo original. Instale requirements_execucao.txt em Python compatível; execute com OPENBLAS_NUM_THREADS=1, OMP_NUM_THREADS=1 e MKL_NUM_THREADS=1. Para reprodução integral sem reutilizar checkpoints, copie src/ e o protocolo para outra pasta e rode os dois comandos do LEIAME_B31.md. Os resultados estão em resultados/, as tabelas em tabelas/ e as figuras em figuras/. MANIFEST_SHA256_ENTREGA.json permite conferir todos os arquivos incluídos.
