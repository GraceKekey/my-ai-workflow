# HRF ELETRON-2D-POST-E67-01 — pacote v0.1

Leia `RELATORIO_AUDITORIA_POST_E67_v0_1.md`.
Este pacote NÃO contém simulação de redes ampliadas nem protocolo de extensão congelado.

- `originals/`: dois ZIPs originais intactos, com código, protocolo, sete dados brutos e resultados.
- `audit.py`: reanálise leve; executada nesta entrega.
- `audit_output/`: hashes, comparação do avaliador, CSV/JSON, ajustes e figura histórica.
- `run_reference_cloud.py`: nova execução integral de referência, somente em GitHub Actions; não executada.
- `workflow_reference_template.yml`: modelo que pressupõe esta pasta na raiz do repositório;
  deve ser colocado em `.github/workflows/` com nome próprio antes do uso. Não foi instalado.
- `PROTOCOLO_EXTENSAO_RASCUNHO_v0_1.md`: plano, critérios propostos, orçamento e gates.
- `STATUS.json`: progresso e bloqueios, sem converter pendências em PASS.
- `MANIFEST_SHA256.json`: hashes desta entrega, não evidência de pré-registro congelado.

Para repetir a reanálise em uma **nova pasta extraída**, instale `requirements.txt` e execute
`python audit.py`. O script recusa sobrescrever `audit_output`; mantenha a cópia entregue e
use uma nova cópia de trabalho sem essa pasta de resultados para a repetição.
O runner de referência recusa sobrescrever `reference_repeat` e exige GitHub Actions.

A tolerância 10⁻¹⁰ da comparação executada serve à reanálise do mesmo dado arquivado;
não é um limiar escolhido para os resultados das futuras simulações.
Para continuar: disponibilizar a credencial de execução por mecanismo seguro (nunca no chat),
preparar o repositório de destino, executar a referência, comparar arrays, medir recursos e
só então congelar e implementar a extensão.
