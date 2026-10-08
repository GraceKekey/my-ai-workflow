# LEIAME — HRF ELETRON-67 — pacote para execução externa

**Data:** 8 de outubro de 2026 · **Autoria:** Mario José do Canto Filho, MD · código: Claude (`-clau`)
**Estado:** pré-registrado, **não executado**. A execução será feita pelo pesquisador num repositório na nuvem.
**Protocolo:** `HRF_ELETRON_67_PROTOCOLO_2026-10-08_1820-clau.md` (mesmo arquivo e mesmo SHA-256 do registro das 18h20).
Nada aqui é elétron.

## O que mudou em relação ao pacote das 18h20

Só a portabilidade, sem mudar física, parâmetros ou regras:

- `src/e67_rodar.py` e `src/avaliar_e67.py`: os caminhos fixos da máquina original (`/home/claude/E67` e uma pasta
  temporária da sessão) viraram caminhos relativos à pasta do pacote; o modo `teste` agora grava em `teste_saida/`.
- `src/e67_rodar.py`: o número de processos pode ser escolhido pela variável `E67_PROCESSOS` (padrão 2). Cada tarefa
  é independente e determinística; o número de processos não muda o resultado.
- Os SHA-256 desses dois arquivos no registro das 18h20 ficam **superados** pelos de `hashes_antes_da_execucao.txt`
  deste pacote. Os demais arquivos (protocolo, `e65_holo.py`, `e67_particula.py`, fumaça) não mudaram.

## Requisitos

- Python ≥ 3.10 com `numpy` e `scipy` (`pip install -r requirements.txt`). Testado com Python 3.13.16, numpy 2.5.3 e
  scipy 1.18.1.
- Memória: até ~2 GB por processo (matrizes de 4 736 × 4 736). Com 2 processos, reserve ~4–5 GB de RAM.
- Tempo: 25 a 40 min com 2 processos numa máquina de 2 núcleos; varia com a máquina.

## Passos

```bash
# 0. conferir que nada mudou desde o registro (a linha de comentário gera só um aviso)
sha256sum -c hashes_antes_da_execucao.txt

# 1. (opcional) teste do encadeamento numa caixa minúscula — ~10 s; o resultado NÃO tem sentido físico
python3 src/e67_rodar.py teste && python3 src/avaliar_e67.py teste
rm -rf teste_saida

# 2. rodada da E-67
python3 src/e67_rodar.py
python3 src/avaliar_e67.py | tee resultados/saida_avaliacao.txt
```

Para usar mais processos (se houver memória): `E67_PROCESSOS=4 python3 src/e67_rodar.py`.

## O que trazer de volta para o relatório

- `dados/` — 7 arquivos: `aperto_4.json`, `aperto_5.json`, `aperto_6.json`, `aperto_7.json`, `padrao_4.json`,
  `padrao_5.json`, `vmais_5.json`;
- `resultados/E67_resumo.json`, `resultados/log_execucao.txt` e `resultados/saida_avaliacao.txt`;
- versões de Python, numpy e scipy e o tipo de máquina (`python3 -c "import sys,numpy,scipy;print(sys.version,numpy.__version__,scipy.__version__)"`).

Com isso, o relatório (Objetivo → Hipóteses → Parâmetros → Protocolo → Medidas → Resultados → Controles/convergência →
Interpretação) e as figuras são feitos sem rodar de novo.

## Regras de registro

- Não editar nenhum arquivo listado em `hashes_antes_da_execucao.txt` antes de rodar. Se algo precisar mudar, a mudança
  entra no relatório como **desvio do protocolo**, com o motivo.
- O protocolo (§9) pede uma decisão [D] do pesquisador: **exceção à D-E1** para esta bancada (não há onda injetada; um
  saca-rolha clássico teria imagem nula no campo livre; o saca-rolha exige a polarização no plano, ainda não
  implementada). A decisão do pesquisador sobre essa exceção entra no relatório.
