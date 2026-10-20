# HRF B31-R — relatório completo

Concluído em 2026-10-20T19:01:52.310586+00:00.

**H-par no modelo livre: APOIADA.**

| Bloco | Decisão congelada |
|---|---|
| B31aR | LOCAL_CHM |
| B31e | SEPARA |
| B31f1 | EMERGE |
| B31f2 | OLA_CELULAR |

## Objetivo

Refazer o modular com o controle de tamanho prescrito, comparar emaranhamento das álgebras de células e relações e testar o limite de uma célula e a propagação celular da ola.

## Hipóteses

A-R: forma CHM e localidade suave. E: informação mútua com inclinações aproximadamente −2 para células e −6 para relações. F1: emergência da forma contínua ao aumentar a região. F2: os picos celulares propagam com a velocidade de grupo e retornam a valores pequenos antes e depois da passagem.

## Parâmetros

```json
{
  "fontes": {
    "L_principal": 2048,
    "L_controle": 1024
  },
  "B31aR": {
    "R": [
      8,
      12,
      16,
      20,
      24
    ],
    "qs": [
      11,
      12,
      13
    ]
  },
  "B31e": {
    "discos": [
      2,
      4,
      6,
      8,
      12
    ],
    "MI": {
      "2": [
        8,
        12,
        16,
        24,
        32,
        48
      ],
      "3": [
        12,
        16,
        24,
        32,
        48
      ]
    },
    "ajuste_ultimos": 4
  },
  "B31f1": {
    "R": [
      0.5,
      1,
      2,
      3,
      4,
      6,
      8
    ],
    "qs": [
      12,
      13
    ]
  },
  "B31f2": {
    "Lt": [
      1024,
      2048
    ],
    "xs": [
      -16,
      -12,
      -8,
      -4,
      0,
      4,
      8,
      12,
      16
    ],
    "formas": {
      "celula": 0.5,
      "hexagono": 1.0
    },
    "k0": [
      0.8,
      0.0
    ],
    "dk": 0.13333333333333333,
    "x_ini": -30.0,
    "tempos": [
      0,
      1,
      2,
      3,
      4,
      5,
      6,
      7,
      8,
      9,
      10,
      11,
      12,
      13,
      14,
      15,
      16,
      17,
      18,
      19,
      20,
      21,
      22,
      23,
      24,
      25,
      26,
      27,
      28,
      29,
      30,
      31,
      32,
      33,
      34,
      35,
      36,
      37,
      38,
      39,
      40,
      41,
      42,
      43,
      44,
      45,
      46,
      47,
      48,
      49,
      50,
      51,
      52,
      53,
      54,
      55,
      56,
      57,
      58,
      59,
      60,
      61,
      62,
      63,
      64
    ],
    "taus": [
      1e-10,
      1e-12
    ]
  }
}
```

## Protocolo

A pasta foi extraída do ZIP recebido e os dez hashes foram aprovados por sha256sum -c, com a saída preservada em verificacao_hashes.txt. Executados rodar_B31R.py completo e avaliar_B31R.py resultados com Python isolado (-I). OPENBLAS_NUM_THREADS=1, OMP_NUM_THREADS=1 e MKL_NUM_THREADS=1. Todos os arquivos de src/ e o protocolo permaneceram intactos. O teste sintético do avaliador passou e alcançou todos os ramos; a fumaça não integra a decisão científica.

Ambiente da execução:

```json
{
  "modo": "completo",
  "python": "3.12.14",
  "numpy": "2.2.6",
  "scipy": "1.15.3",
  "maquina": "Linux-6.18.55-x86_64-with-glibc2.41",
  "inicio": "2026-10-20 15:55:54"
}
```

## Medidas e resultados

### A-R — modular

| R | Desvio máximo | dc máximo | ΔL | Δq |
|---|---:|---:|---:|---:|
| 8 | 0.003091996056 | 0.002251268958 | 2.013687231e-05 | 0.0008225816459 |
| 12 | 0.0006043126911 | 0.003071895126 | 6.357578685e-05 | 0.002641611 |
| 16 | 0.001074294503 | 0.003511049438 | 0.0001576692761 | 0.001158489458 |
| 20 | 0.001164874604 | 0.004077435991 | 0.0003034305582 | 0.001354901478 |
| 24 | 0.001507584427 | 0.00330507674 | 0.0005133182975 | 0.002499913691 |

### E — células e relações

| R_d | Inclinação células | Magnético | Elétrico |
|---|---:|---:|---:|
| 2 | -2.03697239 | -6.07625468 | -6.1190765 |
| 3 | -2.07678327 | -6.15874524 | -6.22130781 |

### F1 — regiões pequenas

R* relatado pelo avaliador: 2.

| R | Células | ρ_M | ρ_N | Desvio | S_q mag |
|---|---:|---:|---:|---:|---:|
| 0.5 | 1 | 0.915273456 | 1.06197558 | 0.0847265442 | 0 |
| 1 | 7 | 1.03294318 | 1.05932221 | 0.0593222118 | 0.265952061 |
| 2 | 19 | 1.0294618 | 1.02768807 | 0.0294617957 | 0.640389838 |
| 3 | 37 | 1.00917482 | 1.01067941 | 0.0106794085 | 1.04971778 |
| 4 | 61 | 1.0031473 | 1.00506866 | 0.00506865718 | 1.47579184 |
| 6 | 127 | 0.999672759 | 1.00109068 | 0.00109068251 | 2.35334495 |
| 8 | 241 | 0.996718103 | 0.999657645 | 0.00328189707 | 3.53103278 |

### F2 — ola celular

| Forma | v ajustada | v/v_g | Diferença helicidades |
|---|---:|---:|---:|
| celula | 0.937671753 | 0.996514172 | 0 |
| hexagono | 0.935941176 | 0.994674995 | 0 |

## Controles

Cobertura exata de 30 casos: A-R=5, E=16 (5 discos e 11 pares), F1=7, F2=2. Conferidos os 65 instantes, nove posições, duas formas e dois cortes em cada toro de F2. Os dez hashes congelados continuam iguais após a rodada. Verificação detalhada em VERIFICACAO_COBERTURA.json. Todos os dados completos estão no checkpoint e nas tabelas.

Avaliação congelada integral:

```json
{
  "modo": "completo",
  "B31aR": {
    "decisao": "LOCAL_CHM",
    "validade": true,
    "falhas_validade": [],
    "por_R": {
      "8": {
        "desvio_max": 0.003091996056427626,
        "razoes_min_max": [
          0.9969080039435724,
          1.0006130192718083
        ],
        "desvio_M_canonico": 0.11191955802535491,
        "dc_max": 0.0022512689581237477,
        "localidade_N_por_q": {
          "11": 0.9965465091776605,
          "12": 0.9976753401928269,
          "13": 0.9981795974446706
        },
        "localidade_sobe_com_q": 0.00163308826701003,
        "dif_L": 2.013687230872918e-05,
        "dif_q": 0.0008225816459162261,
        "R_efetivo": 8.150774926246335,
        "S": 4.1448595800931765,
        "S2": 1.9991367989354496,
        "modos_cortados_q13": 94
      },
      "12": {
        "desvio_max": 0.0006043126911023933,
        "razoes_min_max": [
          0.9993956873088976,
          1.0001847746577666
        ],
        "desvio_M_canonico": 0.11086882243774121,
        "dc_max": 0.0030718951255548355,
        "localidade_N_por_q": {
          "11": 0.9822380409228787,
          "12": 0.9869947418833332,
          "13": 0.9905763199866393
        },
        "localidade_sobe_com_q": 0.008338279063760612,
        "dif_L": 6.357578685078913e-05,
        "dif_q": 0.0026416110004309767,
        "R_efetivo": 11.93811205620609,
        "S": 6.012014028970475,
        "S2": 2.892492691115559,
        "modos_cortados_q13": 292
      },
      "16": {
        "desvio_max": 0.0010742945027477635,
        "razoes_min_max": [
          0.9989257054972522,
          1.00027443231335
        ],
        "desvio_M_canonico": 0.11029636698071221,
        "dc_max": 0.003511049438267716,
        "localidade_N_por_q": {
          "11": 0.9590939205339096,
          "12": 0.9667712218261327,
          "13": 0.9731651754036135
        },
        "localidade_sobe_com_q": 0.014071254869703842,
        "dif_L": 0.00015766927614002668,
        "dif_q": 0.0011584894581323224,
        "R_efetivo": 16.0200999004015,
        "S": 8.166465861045879,
        "S2": 3.938230908352444,
        "modos_cortados_q13": 612
      },
      "20": {
        "desvio_max": 0.0011648746038853686,
        "razoes_min_max": [
          0.9988351253961146,
          1.0000813203224497
        ],
        "desvio_M_canonico": 0.10948599465694886,
        "dc_max": 0.004077435991264672,
        "localidade_N_por_q": {
          "11": 0.935067926225685,
          "12": 0.9445111210564174,
          "13": 0.9526426437040006
        },
        "localidade_sobe_com_q": 0.017574717478315627,
        "dif_L": 0.00030343055818449205,
        "dif_q": 0.001354901477769066,
        "R_efetivo": 20.054785693449762,
        "S": 10.331649266073532,
        "S2": 4.987091585143675,
        "modos_cortados_q13": 1051
      },
      "24": {
        "desvio_max": 0.001507584426792885,
        "razoes_min_max": [
          0.9984924155732071,
          1.0000320748709555
        ],
        "desvio_M_canonico": 0.10929846552209566,
        "dc_max": 0.003305076739717777,
        "localidade_N_por_q": {
          "11": 0.9140491031643208,
          "12": 0.9244558954304185,
          "13": 0.9336175601472722
        },
        "localidade_sobe_com_q": 0.0195684569829514,
        "dif_L": 0.0005133182974905726,
        "dif_q": 0.00249991369056074,
        "R_efetivo": 23.962659380415115,
        "S": 12.208614609000652,
        "S2": 5.885335486384825,
        "modos_cortados_q13": 1593
      }
    }
  },
  "B31e": {
    "decisao": "SEPARA",
    "validade": true,
    "falhas_validade": [],
    "inclinacoes": {
      "2": {
        "Z": -2.036972391587003,
        "mag": -6.07625468022038,
        "ele": -6.119076502172109
      },
      "3": {
        "Z": -2.0767832702347335,
        "mag": -6.1587452443686095,
        "ele": -6.221307806091023
      }
    },
    "series_MI": {
      "2": {
        "r": [
          8,
          12,
          16,
          24,
          32,
          48
        ],
        "I_Z": [
          0.03418222045095831,
          0.013280203007671076,
          0.007182736851959248,
          0.003110101294294232,
          0.001734112053063619,
          0.0007659453911772474
        ],
        "I_mag": [
          0.001065282496385045,
          7.1426960632337e-05,
          1.173008278065879e-05,
          9.758528314307569e-07,
          1.7055409884392247e-07,
          1.4782981949679197e-08
        ],
        "I_ele": [
          0.004821672651722508,
          0.00023939342328560542,
          3.7220793309700184e-05,
          3.0010469913577253e-06,
          5.194108467776459e-07,
          4.47223484911774e-08
        ]
      },
      "3": {
        "r": [
          12,
          16,
          24,
          32,
          48
        ],
        "I_Z": [
          0.028490412427529588,
          0.014642777302694476,
          0.006158260885305911,
          0.003402687660498671,
          0.0014937075943342037
        ],
        "I_mag": [
          0.0006378642727087325,
          9.438976621822803e-05,
          7.393354717777356e-06,
          1.2680584235980064e-06,
          1.085103402687082e-07
        ],
        "I_ele": [
          0.0017206656684862764,
          0.00022964125480484654,
          1.7152309730761317e-05,
          2.9023861287669206e-06,
          2.4617005323079866e-07
        ]
      }
    },
    "discos": {
      "2": {
        "n": 19,
        "S_Z": 1.078438143758289,
        "S_q_mag": 0.640389838233155,
        "S_q_ele": 0.21001343770834377,
        "h_mag": 2.394001102611775,
        "h_ele": 15.866126034017048,
        "dim_ele": 17
      },
      "4": {
        "n": 61,
        "S_Z": 1.997076138102397,
        "S_q_mag": 1.475791835944956,
        "S_q_ele": 0.3469503557200406,
        "h_mag": 2.7740024508616736,
        "h_ele": 26.578751966650714,
        "dim_ele": 29
      },
      "6": {
        "n": 127,
        "S_Z": 2.922122466023026,
        "S_q_mag": 2.3533449539760265,
        "S_q_ele": 0.47224439857535827,
        "h_mag": 3.00625114382096,
        "h_ele": 37.22578245698543,
        "dim_ele": 41
      },
      "8": {
        "n": 241,
        "S_Z": 4.144859580091636,
        "S_q_mag": 3.531032784070387,
        "S_q_ele": 0.5821460715771835,
        "h_mag": 3.2115507677375064,
        "h_ele": 53.08007305514631,
        "dim_ele": 59
      },
      "12": {
        "n": 517,
        "S_Z": 6.0120140289699,
        "S_q_mag": 5.361189582531211,
        "S_q_ele": 0.8217432035496631,
        "h_mag": 3.4396974554093793,
        "h_ele": 74.24810725046078,
        "dim_ele": 83
      }
    }
  },
  "B31f1": {
    "decisao": "EMERGE",
    "validade": true,
    "falhas_validade": [],
    "R_estrela": 2,
    "por_R": {
      "0.5": {
        "n": 1,
        "R_efetivo": 0.525037567904332,
        "rho_M_mel": 0.9152734557598583,
        "rho_N": 1.0619755843877277,
        "desvio": 0.0847265442401417,
        "S": 0.1927506816517061,
        "S2": 0.09040397169437003,
        "eps_min": 3.0972950070956187,
        "S_q_mag": 0.0,
        "S_q_ele": 0.0492692260440562,
        "dif_L": 1.2283998263029616e-09,
        "dif_q": 0.0,
        "celula": {
          "M11": 4.7428675021789495,
          "N11": 2.022665899178537,
          "X": 0.35741562177677133,
          "P": 0.8380894432365676,
          "nu": 0.5473081942187107,
          "eps": 3.0972950070956187
        }
      },
      "1": {
        "n": 7,
        "R_efetivo": 1.3891188336410505,
        "rho_M_mel": 1.0329431750429303,
        "rho_N": 1.059322211831643,
        "desvio": 0.05932221183164299,
        "S": 0.6254316541694374,
        "S2": 0.2989594719475879,
        "eps_min": 2.304990552054199,
        "S_q_mag": 0.26595206092001666,
        "S_q_ele": 0.13283554675215256,
        "dif_L": 6.146409670115816e-08,
        "dif_q": 0.0
      },
      "2": {
        "n": 19,
        "R_efetivo": 2.2885857000573573,
        "rho_M_mel": 1.0294617956854282,
        "rho_N": 1.0276880660048144,
        "desvio": 0.02946179568542817,
        "S": 1.078438143758293,
        "S2": 0.5164027203328543,
        "eps_min": 2.0446758798970763,
        "S_q_mag": 0.640389838233155,
        "S_q_ele": 0.21001343770834377,
        "dif_L": 2.3636062640441935e-07,
        "dif_q": 0.0
      },
      "3": {
        "n": 37,
        "R_efetivo": 3.1936788450473776,
        "rho_M_mel": 1.0091748182956815,
        "rho_N": 1.0106794085189617,
        "desvio": 0.010679408518961653,
        "S": 1.5365048151583869,
        "S2": 0.7358813732774279,
        "eps_min": 1.9024338891862387,
        "S_q_mag": 1.0497177783784926,
        "S_q_ele": 0.28058498482170313,
        "dif_L": 6.500602105496966e-07,
        "dif_q": 0.0
      },
      "4": {
        "n": 61,
        "R_efetivo": 4.100674494563627,
        "rho_M_mel": 1.0031473027493354,
        "rho_N": 1.0050686571819827,
        "desvio": 0.005068657181982683,
        "S": 1.9970761381023534,
        "S2": 0.9563520998932933,
        "eps_min": 1.8085500456714565,
        "S_q_mag": 1.475791835944956,
        "S_q_ele": 0.3469503557200406,
        "dif_L": 1.40625032529762e-06,
        "dif_q": 5.961230165052456e-07
      },
      "6": {
        "n": 127,
        "R_efetivo": 5.9168728953125065,
        "rho_M_mel": 0.9996727593738985,
        "rho_N": 1.001090682509571,
        "desvio": 0.001090682509570895,
        "S": 2.9221224660229375,
        "S2": 1.3989229076857181,
        "eps_min": 1.6870805109197082,
        "S_q_mag": 2.3533449539760265,
        "S_q_ele": 0.47224439857535827,
        "dif_L": 4.323315245136072e-06,
        "dif_q": 1.5462394054033268e-07
      },
      "8": {
        "n": 241,
        "R_efetivo": 8.150774926246335,
        "rho_M_mel": 0.9967181029306585,
        "rho_N": 0.9996576445067556,
        "desvio": 0.003281897069341455,
        "S": 4.1448595800931765,
        "S2": 1.9991367989354496,
        "eps_min": 1.57788805967119,
        "S_q_mag": 3.531032784070387,
        "S_q_ele": 0.5821460715771835,
        "dif_L": 1.1362414651272523e-05,
        "dif_q": 1.0514033499386954e-06
      }
    }
  },
  "B31f2": {
    "decisao": "OLA_CELULAR",
    "validade": true,
    "falhas_validade": [],
    "dif_Lt": {
      "celula": {
        "dif_abs": 7.925123014885377e-06,
        "menor_pico": 0.010338590079110355,
        "dif_rel": 0.0007665574274869926
      },
      "hexagono": {
        "dif_abs": 6.753853481741845e-05,
        "menor_pico": 0.054321572106765255,
        "dif_rel": 0.0012433096502560011
      }
    },
    "v_g": 0.9409517485099211,
    "O1_velocidade": true,
    "O2_levanta_e_senta": true,
    "helicidade": true,
    "por_forma": {
      "celula": {
        "t_pico": [
          14.945209260137592,
          19.209819666992033,
          23.47934583259796,
          27.74942304741923,
          32.01245438097695,
          36.27528737790935,
          40.54417485303963,
          44.80962758146624,
          49.069749899277824
        ],
        "altura": [
          0.020702521153020008,
          0.018971841462066465,
          0.017302924458975855,
          0.01577496022829463,
          0.014403905115384693,
          0.013187402638273138,
          0.012114927802894832,
          0.011173109187594496,
          0.010340034441897315
        ],
        "antes_sobre_pico": [
          0.0009914179115191291,
          1.0920935158123617e-05,
          3.5778942698667e-08,
          1.8862930286616984e-10,
          5.211238070067659e-11,
          4.438399240831846e-11,
          3.703209227082019e-11,
          3.110144194183329e-11,
          2.624154771854286e-11
        ],
        "depois_sobre_pico": [
          2.788626411914238e-11,
          3.1776098465561265e-11,
          3.671458060149893e-11,
          4.283254746818109e-11,
          5.2729004048710264e-11,
          3.7837521904473786e-10,
          1.0449058005129841e-07,
          2.23001409890816e-05,
          0.0016008072272116892
        ],
        "altura_sobre_quasiparticula": [
          1.2834393106123068,
          1.2810672312450009,
          1.2798223442797714,
          1.2699543682653975,
          1.270700731860685,
          1.2725210100075934,
          1.2593285050066154,
          1.2625928917742004,
          1.2666401863369003
        ],
        "v_ajuste": 0.9376717526340309,
        "v_sobre_vg": 0.996514172080466,
        "hel_max": 0.0,
        "circ_menos_linear_max": 4.95309607838057e-05
      },
      "hexagono": {
        "t_pico": [
          14.964460241658296,
          19.236549104853648,
          23.514638693147628,
          27.791234718526322,
          32.06199434741755,
          36.333908646799564,
          40.61169836152791,
          44.88344211764238,
          49.151685130998935
        ],
        "altura": [
          0.10735508553521007,
          0.09865644106059045,
          0.0902056549608529,
          0.0824140543387612,
          0.07538067342084445,
          0.06911277682704584,
          0.06357383958946271,
          0.058688354183363475,
          0.05435575913904859
        ],
        "antes_sobre_pico": [
          0.0013267061884928905,
          1.718025022815412e-05,
          7.156868447354742e-08,
          2.0500328590602123e-10,
          3.4022184606515156e-11,
          2.9099814845284363e-11,
          2.4242858583631686e-11,
          2.0319032069374844e-11,
          1.7138720067919354e-11
        ],
        "depois_sobre_pico": [
          1.8447340630908287e-11,
          2.0957256480514608e-11,
          2.4156298531171002e-11,
          2.810648422973129e-11,
          3.3449256909028094e-11,
          5.250882074468955e-10,
          2.0655336345053797e-07,
          3.661302851863157e-05,
          0.002228721851833974
        ],
        "altura_sobre_quasiparticula": [
          0.977185786323371,
          0.9755876643241655,
          0.9699217880577927,
          0.9693829555689641,
          0.9694685372604833,
          0.9701300851439374,
          0.9634176097401952,
          0.9648899072473635,
          0.9667752304440497
        ],
        "v_ajuste": 0.9359411758565847,
        "v_sobre_vg": 0.9946749951192809,
        "hel_max": 0.0,
        "circ_menos_linear_max": 2.4316838002053087e-05
      }
    }
  },
  "global_H_par": "APOIADA",
  "relatum_B31e": "SEPARA",
  "regras": {
    "aR": {
      "tol_L": 0.001,
      "tol_q": 0.01,
      "nu_min": 0.499999999,
      "tol_chm": 0.05,
      "faixa": [
        0.8,
        1.2
      ],
      "tol_c": 0.02,
      "c_nao": 0.1,
      "q_dec": "13",
      "q_ctrl": "12"
    },
    "e": {
      "tol_L_rel": 0.01,
      "nu_min": 0.499999999,
      "Z": [
        -2.4,
        -1.6
      ],
      "rel": [
        -6.8,
        -5.2
      ],
      "iguais": 1.0
    },
    "f1": {
      "tol_L": 0.001,
      "tol_q": 0.01,
      "nu_min": 0.499999999,
      "tol_chm": 0.05,
      "q_dec": "13",
      "q_ctrl": "12"
    },
    "f2": {
      "tol_Z": 1e-08,
      "tol_tau": 1e-06,
      "tol_E": 1e-08,
      "tol_Lt_rel": 0.01,
      "nu_min": 0.499999999,
      "h_min": 1e-08,
      "tol_v": 0.05,
      "sentado": 0.1,
      "tol_hel": 1e-10
    }
  }
}
```

## Interpretação

A classificação global APOIADA segue exclusivamente A-R e F2 conforme o protocolo. As decisões E (SEPARA) e F1 (EMERGE) são relatadas separadamente e não alteram a decisão global.

Os limites foram mantidos sem ajustes após os resultados. R* e inclinações devem ser interpretados junto aos testes de validade. A localidade por sítio de A-R é relatada para os três q e não participa da decisão desta revisão.

## Limites e reprodução

Modelo livre não compacto, sem vórtices ou gap de Polyakov; não constitui uma fronteira holográfica completa. As polarizações circulares usam duas cópias do campo fora do plano. Entropias de centro são diferenciais e dependem da unidade; a informação mútua e a parte quântica são as comparações relevantes. F2 mede Rényi-2, e p_E é fração local de energia, não fração de partícula numa célula. Precisão dupla e os cortes do protocolo foram preservados.

Consulte LEIAME_B31R.md para os comandos originais. requirements_execucao.txt registra as versões utilizadas. Para reproduzir sem reutilizar resultados, execute numa cópia com src/ e protocolo e sem resultados/. O ZIP original está em entrada/. fumaca/ contém somente a execução preliminar recebida. Os dados atuais, logs, tabelas e figuras estão incluídos; não é necessário acessar o repositório para ler ou reproduzir o pacote.
