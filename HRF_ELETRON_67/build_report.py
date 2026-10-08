"""Export the complete E67 evidence without changing its evaluator or thresholds."""
import csv
import hashlib
import json
import os
from pathlib import Path
import math

ROOT = Path(__file__).resolve().parent
OUT = ROOT


def read(path):
    return json.loads(path.read_text())


def finite(value):
    if isinstance(value, float) and not math.isfinite(value):
        return None
    if isinstance(value, dict):
        return {k: finite(v) for k, v in value.items()}
    if isinstance(value, list):
        return [finite(v) for v in value]
    return value


def show(value):
    return f'{value:.8g}' if isinstance(value, (int,float)) and math.isfinite(value) else 'não medido'


def main():
    result = read(OUT/'resultados'/'E67_resumo.json')
    expected = ['aperto_4','aperto_5','aperto_6','aperto_7','padrao_4','padrao_5','vmais_5']
    audit = [read(OUT/'auditoria'/f'{case}.json') for case in expected]
    assert all(a['execution_status']=='COMPLETED' for a in audit)
    datasets = {case: read(OUT/'dados'/f'{case}.json') for case in expected}
    for case, data in datasets.items():
        assert len(data['rhos']) == 95 and data['rhos'][0] == .5 and data['rhos'][-1] == 24
        if case.startswith('aperto'):
            assert len(data['S0']) == 95
            for r in ('r0.1','r0.25'):
                assert len(data[r]['S'])==95 and set(data[r]['sondas'])=={'0.5','1.0','1.5'}
    assert len(datasets['aperto_5']['r0.25']['mapa'])==17
    assert all(len(row)==16 for row in datasets['aperto_5']['r0.25']['mapa'])
    all_nu = min(a['nu_min_all_calls'] for a in audit)
    physical = all(a['Vnu_same_original_tolerance_ok'] for a in audit)
    authoritative = dict(original_decisions=result['decisoes'],
                         original_evaluator_preserved=True, complete_seven_cases=True,
                         full_grid=[64,74], entropy_calls=sum(a['entropy_region_calls'] for a in audit),
                         nu_min_every_region=all_nu, Vnu_all_regions_ok=physical,
                         verdict_after_full_Vnu_audit=(result['decisoes']['H67 (partícula no bulk)']
                                                        if physical else 'INCONCLUSIVO — Vν falhou em uma região'),
                         unchanged_tolerance=1e-9, interpretation_tag='[M]')
    (OUT/'AUDITORIA_FINAL.json').write_text(json.dumps(authoritative,indent=2,ensure_ascii=False,allow_nan=False)+'\n')
    (OUT/'resultados'/'E67_resumo_JSON_PADRAO.json').write_text(json.dumps(finite(result),indent=2,ensure_ascii=False,allow_nan=False)+'\n')
    with (OUT/'resultados'/'E67_perfis.csv').open('w',newline='') as f:
        writer=csv.writer(f);writer.writerow(['w','squeeze_r','rho','S_vacuo','S_estado','delta_S','delta_K'])
        for w in (4,5,6,7):
            a=datasets[f'aperto_{w}']
            for r in (.1,.25):
                b=a[f'r{r}']
                for rho, s0, s, dk in zip(a['rhos'],a['S0'],b['S'],b['dK_centrado']):
                    writer.writerow([w,r,rho,s0,s,s-s0,dk])
    with (OUT/'resultados'/'E67_sondas.csv').open('w',newline='') as f:
        writer=csv.writer(f);writer.writerow(['case','squeeze_r','offset_fraction','rho','delta_S'])
        for case,a in datasets.items():
            records=[(r,a[f'r{r}']['sondas']) for r in (.1,.25)] if case.startswith('aperto') else [('',a['sondas'])]
            for r, probes in records:
                for fraction,values in probes.items():
                    for rho,v in zip(a['rp'],values):writer.writerow([case,r,fraction,rho,v])
    text=['# HRF ELETRON-67 — relatório de execução completa', '',
          '[M] Resultado: **'+authoritative['verdict_after_full_Vnu_audit']+'**.', '',
          'Executados os sete casos da rede 64×74 (4.736 nós), com quatro larguras, dois apertos, dois padrões de relações e o controle unitário V+. O modo `teste` não foi usado. Cada perfil centrado contém 95 raios; o mapa deslocado contém 17×16 discos.', '',
          'Os critérios do protocolo e o avaliador original foram mantidos. Nenhum dos arquivos fornecidos no pacote corrigido foi alterado. Uma instrumentação adicional registrou ν em todas as chamadas de entropia, inclusive nos perfis V+ e nas mudanças de nó de referência, que o runner original não incorporava integralmente a seu `nu_min`.', '',
          '## Excitação suave — r=0,25', '',
          '| w | p mínimo | Classe | z | z/w | z/r50 | Linearidade |',
          '|---|---:|---|---:|---:|---:|---:|']
    for w in (4,5,6,7):
        o=result['aperto'][f'w{w}']; a=o['0.25']
        text.append(f"| {w} | {show(a['p_min'])} | {a['classe_N']} | {show(a['z_centroide'])} | {show(a['z_sobre_w'])} | {show(a['z_sobre_r50'])} | {show(o['linearidade'])} |")
    text+=['','## Decisões e controles','']
    text += ['- '+k+': **'+v+'**.' for k,v in result['decisoes'].items()]
    text += ['', 'Ajuste z(w): '+json.dumps(result['ajuste_z'],ensure_ascii=False)+'.', '',
             '| Validação | Status | Medição |','|---|---|---|']
    for name,a in result['validacoes'].items():
        evidence={k:finite(v) for k,v in a.items() if k!='ok'}
        text.append(f"| {name} | {'PASS' if a['ok'] else 'FAIL'} | {json.dumps(evidence,ensure_ascii=False)} |")
    text += ['',f"Auditoria adicional Vν: {'PASS' if physical else 'FAIL'}, mínimo {all_nu:.12f} em {authoritative['entropy_calls']} regiões avaliadas.",'',
             '## Limites da conclusão','',
             'O resultado caracteriza a regra de reconstrução escolhida para um campo gaussiano livre fora do plano no instante zero. Não certifica uma geometria gravitacional real, uma partícula de Fock, um fóton HRF-CAP2, um elétron, carga, spin ou massa eletrônica. A evolução temporal não pertence a este ensaio.', '',
             'O próprio protocolo declara que os limiares foram definidos após testes de fumaça e que o resultado esperado já era conhecido. Esta rodada verifica o protocolo congelado; não constitui um teste cego com critérios definidos antes de qualquer observação.', '',
             'O fecho para w=7 não é mensurável: 4w=28 excede o raio máximo 24. O NaN original foi preservado em E67_resumo.json; a cópia JSON padrão usa null. Isso não é um PASS para essa medição.', '',
             'Os resultados negativos e validações que falharem permanecem nos dados, na avaliação e neste relatório. Todas as medidas desta execução são [M].', '',
             '## Arquivos','',
             '`dados/`: sete JSON brutos. `resultados/`: avaliação original, CSV, mapas e figuras. `auditoria/`: mínimos de ν e tempo por caso. `ambiente.json`: versões e commit executado. `PROVENIENCIA_PRE_EXECUCAO.json`: hashes do pacote corrigido e instrumentação de auditoria.']
    (OUT/'RELATORIO_E67.md').write_text('\n'.join(text)+'\n')
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import numpy as np
    fig,axes=plt.subplots(1,2,figsize=(11,4))
    for w in (4,5,6,7):
        a=datasets[f'aperto_{w}'];rho=np.array(a['rhos']);delta=np.array(a['r0.25']['S'])-np.array(a['S0'])
        axes[0].plot(rho,delta,label=f'w={w}')
    axes[0].set(xlabel='Raio do disco',ylabel='Delta S',title='[M] Aperto r=0,25');axes[0].legend()
    a=datasets['aperto_5']['r0.25'];im=axes[1].imshow(np.array(a['mapa']).T,origin='lower',aspect='auto',extent=[-.5,16.5,.5,16.5]);axes[1].set(xlabel='Deslocamento do centro',ylabel='Raio do disco',title='[M] Mapa w=5, r=0,25');fig.colorbar(im,ax=axes[1],label='Delta S');fig.tight_layout();fig.savefig(OUT/'resultados'/'E67_figuras.png',dpi=160);plt.close(fig)
    print(json.dumps(authoritative,ensure_ascii=False,indent=2))


if __name__=='__main__':
    main()
