"""Standalone plots, complete report, verification and reproducible ZIP."""
from __future__ import annotations
import csv,hashlib,json,time,zipfile,platform
from pathlib import Path
import numpy as np
from core import *
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.integrate import quad


def plots(rows):
    (ROOT/'plots').mkdir(parents=True,exist_ok=True)
    plt.rcParams.update({'font.size':9,'figure.figsize':(7,4.6)})
    def save(name):
        plt.tight_layout()
        for ext in ['png','pdf']:plt.savefig(ROOT/'plots'/f'{name}.{ext}',dpi=170)
        plt.close()
    select=[r for r in rows if r['rc_m'] is not None and r['pressure_tolerance']==.01 and r['state']=='open' and r['f_V'] in [0.,1e-12,1e-9,1e-6,1e-4,1e-3]]
    for key,title,name,logy in [('g_C5B_GR','Static proper acceleration (m/s²)','01_gravity',True),('delta_g','|Δg| (m/s²)','02_delta_gravity',True),('relative_delta_g','|Δg/g PREM|','03_relative_gravity',True),('P_C5B_Pa','Material pressure (Pa)','04_pressure',True),('rho_material','Prescribed density (kg/m³)','05_density',False)]:
        plt.figure()
        for r in select:
            with (ROOT/'results/profiles'/(r['case']+'.csv')).open() as f:records=list(csv.DictReader(f))
            x=np.array([float(a['r_m']) for a in records]);y=np.array([float(a[key]) for a in records])
            if key in ('delta_g','relative_delta_g'):y=abs(y)
            mask=y>0 if logy else np.ones_like(y,dtype=bool)
            plt.plot(x[mask],y[mask],label=f"f={r['f_V']:.0e}")
        plt.xscale('log')
        if logy:plt.yscale('log')
        plt.xlabel('Areal radius r (m)');plt.ylabel(title);plt.legend(fontsize=8);save(name)
    plt.figure()
    for tol in PARAMS['relative_pressure_thresholds']:
        rr=sorted([r for r in rows if r['rc_m'] is not None and r['f_V']>0 and r['pressure_tolerance']==tol and r['state']=='open'],key=lambda r:r['f_V'])
        plt.loglog([r['f_V'] for r in rr],[r['rc_m'] for r in rr],'-o',ms=3,label=f'pressure excess {100*tol:g}%')
    for height in [.01,1,10,100,1e3,1e4,1e5,IC]:
        plt.axhline(height,color='gray',lw=.5,alpha=.4)
    plt.text(1.1e-12,IC,'inner-core radius',fontsize=8);plt.xlabel('f_V');plt.ylabel('Minimum cavity radius (m)');plt.legend();save('06_cavity_thresholds')
    ss=[r for r in rows if r['rc_m'] is not None and r['f_V']>0 and r['state']=='open' and r['pressure_tolerance']==.01]
    plt.figure();plt.semilogx([r['f_V'] for r in ss],[r['delta_I_over_I'] for r in ss],'-o');plt.axhline(0,color='gray',lw=.7);plt.xlabel('f_V');plt.ylabel('ΔI/I, fixed cavity rule');save('07_inertia')
    plt.figure();plt.semilogx([r['f_V'] for r in ss],[r['slichter_density_proxy_delta_T'] for r in ss],'-o');plt.xlabel('f_V');plt.ylabel('Density-scaling proxy ΔT/T');plt.title('Slichter sensitivity proxy; full eigenmode not solved');save('08_slichter_proxy')
    plt.figure();plt.semilogx([r['f_V'] for r in ss],[r['radial_homologous_proxy_delta_omega'] for r in ss],'-o');plt.xlabel('f_V');plt.ylabel('Homologous-fluid proxy Δω/ω');plt.title('Not an elastic Earth normal-mode prediction');save('09_mode_proxy')
    plt.figure()
    for ratio in [.1,.5,1.,2.]:
        yy=[2*r['rc_m']/(ratio*11262.2)-r['central_chord_PREM_time_removed_s'] for r in ss]
        plt.semilogx([r['f_V'] for r in ss],yy,label=f'rarefied v/v_center={ratio:g}')
    plt.xlabel('f_V');plt.ylabel('1D central-chord Δt (s)');plt.legend();save('10_PKIKP_scenarios')
    plt.figure()
    for state in ['open','closed']:
        y=np.geomspace(1.00001,100,800)
        a=y/(y+1) if state=='open' else 1-1/y
        plt.semilogx(y,a,label=state)
    plt.xlabel('r/r0');plt.ylabel('Isolated lapse A');plt.legend();save('11_open_closed_geometry')
    plt.figure()
    plt.loglog([r['f_V'] for r in ss],[abs(r['extra_radial_support_Pa']) for r in ss],'-o',label='open composed extra radial stress')
    plt.xlabel('f_V');plt.ylabel('|extra radial stress at cavity| (Pa)');plt.legend();save('12_support_stress')


def validate(rows):
    out={};out['mass_residual_max']=max(abs(r['total_mass_residual_fraction']) for r in rows if r['rc_m'] is not None)
    import sys,scipy,sympy
    out['software_versions']={'Python':sys.version.split()[0],'NumPy':np.__version__,'SciPy':scipy.__version__,'Matplotlib':matplotlib.__version__,'SymPy':sympy.__version__}
    out['all_case_scalars_finite']=all(np.isfinite(v) for r in rows for v in r.values() if isinstance(v,(int,float)))
    from scipy.integrate import simpson
    convergence=[]
    for f,rc in [(0.,0.),(1e-6,cavity_threshold(1e-6,.01)['rc_m']),(1e-3,cavity_threshold(1e-3,.01)['rc_m'])]:
        vals=[]
        for res in [120,240]:
            value=0.;n=norm(f,rc);hole=float(prem.mass(rc))
            for lo,hi,co in prem.LAYERS:
                a,b=max(rc,lo*1000,1e-8),hi*1000
                if a>=b:continue
                rr=np.geomspace(a,b,res)
                rho=n*1000*prem.NORMALIZATION*np.polynomial.polynomial.polyval(rr/R,co)
                gg=G*(f*M+n*(prem.mass(rr)-hole))/rr**2
                value+=simpson(rho*gg*rr,x=np.log(rr))
            vals.append(float(value))
        pn,dn=pressure_newton(f,rc)
        convergence.append({'f_V':f,'resolution':[120,240],'pressure_Pa':vals,'relative_change':abs(vals[1]/vals[0]-1),'high_resolution_error_vs_analytic':abs(vals[1]/(pn+dn)-1)})
    out['radial_resolution_convergence']=convergence
    out['QW02_regression']=json.loads((ROOT/'results/regression_QW02.json').read_text())['passed']
    out['tests']=json.loads((ROOT/'results/test_results.json').read_text())
    out['dynamic_symbolic_checks']=json.loads((ROOT/'results/10_dynamic_symbolic.json').read_text())['passed']
    out['cases_requested']=len(rows);out['cases_numerically_evaluated']=sum(r['rc_m'] is not None for r in rows);out['analytically_rejected_pressure_cases']=sum(r['rc_m'] is None for r in rows)
    out['statuses']={s:sum(r['joint_status']==s for r in rows) for s in ['PASSA','TENSÃO','EXCLUÍDO','NÃO RESOLVIDO','MODELO INSUFICIENTE']}
    out['negative_total_radial_NEC_at_cavity_cases']=sum(r.get('NEC_total_at_rc_Pa',0)<0 for r in rows)
    out['numerical_success']=bool(out['all_case_scalars_finite'] and out['mass_residual_max']<1e-13 and out['tests']['passed'] and out['dynamic_symbolic_checks'] and max(a['high_resolution_error_vs_analytic'] for a in convergence)<3e-5)
    out['physical_model_confirmed']=False;out['robust_global_f_upper_limit']=None
    save_json('results/validation.json',out)
    if not out['numerical_success']:raise RuntimeError('Final numerical validation failed')
    return out


def report(rows,verification):
    cloud_source=ROOT/'data/source_access_cloud.json'
    available_sources=[a for a in json.loads(cloud_source.read_text()) if a.get('available')] if cloud_source.exists() else []
    source_note=(f"Metadados/textos de {len(available_sources)} referências públicas foram obtidos no GitHub Actions; ver `data/source_access_cloud.json`. Isso não fornece os dados brutos ou covariâncias necessários para uma likelihood observacional." if available_sources else 'Consulta a páginas científicas externas ficou indisponível neste ambiente; `data/source_access.json` documenta tentativas.')
    neutrino_source=next((a for a in available_sources if a['name']=='neutrino_primary'),None)
    if neutrino_source and neutrino_source.get('extract'):
        source_note+='\n\nCanais identificados na referência primária de neutrinos (sem transformar informações bibliográficas em um limite independente de modelo):\n\n'+json.dumps(neutrino_source['extract'],ensure_ascii=False)
    def reference(f):return next(r for r in rows if r['f_V']==f and r['pressure_tolerance']==.01 and r['state']=='open')
    small=reference(1e-6);large=reference(.001);reg=json.loads((ROOT/'results/regression_QW02.json').read_text());sl=json.loads((ROOT/'results/slichter_thresholds.json').read_text());pred=json.loads((ROOT/'results/C5B-Earth-01_prediction.json').read_text())
    sample='\n'.join(f"| {f:g} | {reference(f)['rc_m']:.6g} | {reference(f)['delta_I_over_I']:.6g} | {reference(f)['inner_core_volume_fraction_removed']:.6g} | {reference(f)['extra_radial_support_Pa']:.6g} |" for f in PARAMS['f_V'])
    summary_rows=list(csv.DictReader((ROOT/'tables/summary_by_test.csv').open()))
    table='\n'.join('| '+ ' | '.join(str(r[k]) for k in ['Teste','Observavel','Sensibilidade_a_f','Restricao_obtida','Status'])+' |' for r in summary_rows)
    doc=f'''# C5B-QO-QW03 — Earth Constraint Battery

STATUS: EXECUÇÃO CONCLUÍDA (bateria numérica exploratória). Não é validação física da hipótese.

## 1. Objetivo
Confrontar [H] C5B com observáveis terrestres e tornar limitações, exclusões e previsões explícitas. [M] {verification['cases_requested']} combinações, {verification['cases_numerically_evaluated']} perfis executados; {verification['analytically_rejected_pressure_cases']} critérios de pressão rejeitados analiticamente. Não há ajuste a dados observacionais.

## 2. Modelo usado
[F] Métrica ds²=-A c²dt²+dr²/F+r²dΩ². [M] alpha=2, r0=2GM_V/c², F_virtual=1-r0/r; A_open=r/(r+r0), A_closed=F_virtual. Renormalização QW02: n=(1-f)/(1-m0(rc)/M); rho=n rho_PREM e m=n(m0(r)-m0(rc)) fora da cavidade. Dentro dela, não há matéria terrestre prescrita.

[M] Reconstrução declarada do QW02 a partir do QW01: F_total=F_virtual-2Gm/(c²r), phi=phi_matter+0.5 log A_virtual. phi_matter vem da TOV para a matéria prescrita com a mesma cavidade. Esta composição exige um tensor adicional anisotrópico. Não é a solução TOV de um único fluido terrestre autocoerente.

[F] A aceleração própria estática é g=c² sqrt(F) dphi/dr. A conservação de um fluido isotrópico estático dá P'=-(rho c²+P) phi'. Inserir g próprio diretamente em dP/dr omitiria o fator entre distância própria e raio areal. Não integrar até o horizonte fechado.

## 3. Parâmetros
Ver `parameters.json`, incluindo constantes, dez f de 1e-12 a 1e-3, controle zero, critérios 10%, 1%, 0.1%, e três pontos refinados no limiar de casca fina. Todo caso conserva o mesmo theta=(f,alpha,rc) em A–I. Os critérios de pressão são diagnósticos escolhidos pelo pedido, não limites experimentais.

## 4. Dados observacionais
[F] PREM reutilizado exatamente, SHA256 {verify_prem()}. Os coeficientes são um perfil de densidade simplificado previamente usado e normalizado pela massa gravitacional; não são medição independente de massa material. Não substituímos os coeficientes por outro PREM.

[?] Os documentos C5B04, bifurcação e notebooks não foram fornecidos/encontrados. O relatório QW02 foi fornecido; seus CSVs/código não. Consulta a páginas científicas externas ficou indisponível neste ambiente; `data/source_access.json` documenta tentativas. Nenhuma incerteza observacional numérica foi inventada nem extraída desses acessos falhos. Referências bibliográficas conhecidas ao final são identificadas; não há likelihood de neutrinos, dados de frequências, covariância de I ou tempos PKIKP observados no pacote.

[F] Na GR, massa de energia integrada em raio areal, massa ADM, massa de repouso/bariônica em volume próprio e massa inferida por nucleons são diferentes. A convenção QW02 usa integral areal. Qualquer confronto real por neutrinos deve converter volumes/caminhos e tratar composição, interação, energia de ligação e calibração. Para f muito pequeno essas correções convencionais não podem ser ignoradas.

## 5. Testes de regressão QW02
[M] 18/18 valores do relatório reproduzidos; maior erro relativo {max(a['relative_error'] for a in reg['cases']):.6g}, compatível com os valores arredondados. As sete pressões microscópicas concordam a melhor que 3.4e-8. Esta é regressão dos números publicados no relatório, não comparação com CSVs ausentes. Referências, tolerâncias e erros completos em `tables/regression_QW02.csv`.

## 6. Massa material × gravidade
[M] M_areal_material=(1-f)M; déficit definido fM. As sensibilidades para 1 e 5 sigma estão em `tables/01_mass_vs_matter.csv`; são precisões futuras requeridas. [?] Não há limite robusto de neutrinos estabelecido nesta bateria. Não usar PREM normalizado por M como confirmação independente. Todos os f não nulos ficam NÃO RESOLVIDOS neste canal.

## 7. Perfil gravitacional central
[M] Perfis estáticos GR e diagnóstico Newton separados. O controle zero recupera a referência TOV/PREM, cuja diferença Newtoniana é de ordem da compactação terrestre. Gravidade superficial quase não distingue f porque a massa total foi fixada. No campo fraco, um núcleo aproximadamente homogêneo dá Δg/g~fM/m0(r) e raios de influência proporcional a f^(1/3), mas remoção e renormalização da cavidade modificam essa regra. Todos os cruzamentos numéricos 0.01%, 0.1%, 1%, 10%, 100% e a igualdade aproximada das contribuições aparecem em `tables/02_gravity_crossings.csv`; raios dentro da cavidade são marcados como fora do domínio material, não extrapolados.

## 8. Cavidade
[M] Para excesso de pressão 1%, f=1e-6 requer rc={small['rc_m']:.6g} m; f=1e-3 requer rc={large['rc_m']:.6g} m. A cavidade pode ser macroscópica.

[M] No diagnóstico Newtoniano, ΔP/P_matter >=2f/(1-f): o peso dm/r^4 favorece massa material pequena no interior e a média ponderada do m encerrado é <= metade da massa material da casca. A igualdade só aparece no limite de casca infinitamente fina. Portanto o critério de excesso <0.1% é inacessível para f >=0.001/2.001 ≈0.000499750125 nesta família prescrita. Este é limite de um critério do modelo, não uma exclusão observacional geral C5B. A regressão valida a aproximação fraca dos raios terrestres; correções GR foram checadas.

[F/M] Uma cavidade literalmente vazia que remove todo o núcleo interno (rc>=1221.5 km) contradiz o modelo de núcleo interno sólido. Casos assim são excluídos nessa interpretação. Abaixo disso, ausência de dados e kernels impede limites sísmicos rígidos: classificação C, atualmente não resolvido, com escalas de comprimento de onda registradas. Não transformamos λ=v/frequência em uma resolução experimental universal.

## 9. Massa + momento de inércia
[M] I0={I0:.9g} kg m²; I0/(MR²)={I0/(M*R**2):.9g}. Para a componente central não rotante, I_virtual=0. O mesmo perfil dá ΔI/I=n(1-I_removed/I0)-1. Para cavidade pequena, ΔI/I≈-f; para cavidades grandes, a renormalização externa pode aumentar I e inverter o sinal. Não corrigimos a densidade para zerar I.

| f | rc mínimo 1% (m) | ΔI/I | fração de volume do núcleo interno removida | stress radial extra aberto (Pa) |
|---:|---:|---:|---:|---:|
{sample}

[?] Não há covariância observacional independente para comparar esses desvios com I observado. Limites 3 sigma para precisões hipotéticas estão explicitamente em `tables/04_inertia_conditional.csv`; não são exclusões empíricas. **Limite quantitativo ainda não demonstrado.**

## 10. Modos normais
[M] Calculamos Δpotencial Newtoniano, energia de ligação e uma aproximação radial homóloga de fluido: omega²=(3Gamma-4)|W|/(1.5 I), Gamma=5/3 fixo. A energia inclui autoatração e atração central. [?] Sem tensor elástico e kernels de modos, isso não é omega_0S0 nem qualquer modo terrestre identificado. As precisões espectrais na tabela são sensibilidade desse proxy. Status MODELO INSUFICIENTE para frequências observacionais.

## 11. Slichter
[M] Benchmark não rotante homogêneo, empuxo e massa adicionada: omega²=(4πG/3)rho_oc(rho_ic-rho_oc)/(rho_ic+rho_oc/2). Densidades média PREM interna e externa na ICB dão T_benchmark={sl['T_benchmark_s']/3600:.6g} h. Não é solução elástica/rotante PREM exata nem período observado.

[M] Calculamos dois cenários distintos: apenas escala de densidades n, com ΔT/T=n^-1/2-1; e núcleo homogeneizado com massa retirada, que pode perder o sinal restaurador nesse toy model. Para uma fonte fixa dentro de uma cavidade de uma casca rígida transladada, o teorema da casca dá força linear direta zero enquanto o deslocamento é menor que rc. Substituir o campo central divergente na fórmula de Slichter inventaria acoplamento. Fonte presa ao núcleo, fonte fixa e cavidade com borda presa não são equivalentes. Cruzamentos de 0.1%, 1%, 10% são registrados apenas para o proxy e podem estar ausentes na grade. Nenhuma detecção atual ou estabilidade dinâmica foi assumida.

## 12. PKIKP
[M] Aproximação 1D para diâmetro central, com extensão explícita de polinômios de vP PREM e sem alteração de densidade original. 2∫0^rc dr/vP dá a escala do trecho removido. 1 ms, 10 ms, 0.1 s e 1 s correspondem aproximadamente a 5.63 m, 56.3 m, 563 m e 5.63 km. Não são previsões de um sinal que atravessa vácuo.

[F] Vácuo não transmite diretamente onda elástica PKIKP: não existe um Δt finito de chegada direta nesse cenário. Geometria sem matéria também não define um meio elástico. [M] Cenários rarefeitos com rho/rho_ext=0.01 e velocidades 0.1, 0.5, 1 e 2 vezes a velocidade central, além de interface ideal com velocidade casada, mostram atraso/avanço e coeficientes de transmissão de duas interfaces planas. Não incluem difração, trajetórias reais, atenuação, anisotropia ou reverberações. Status MODELO INSUFICIENTE para excluir por dados reais.

## 13. Equilíbrio hidrostático
[M] P obtida por conservação do fluido na métrica composta; o comparador possui exatamente a mesma cavidade e massa material. Aberto: pressão finita na garganta. Fechado: observador estático/pressão divergem ao se aproximar do horizonte; domínio de matéria começa em rc>r0.

[F/M] A geometria composta não tem o tensor de um único fluido PREM. Calculamos stress radial adicional p_extra=p_W+cross-ΔP, onde cross=-2(c⁴/8πG)(b_matter phi'_W+b_W phi'_matter)/r². Em alpha=2, o stress isolado fechado fora do horizonte é zero; isso NÃO elimina os stresses adicionais da composição com matéria. Aberto, p_W=-8(c⁴/8πG)mu²/[r³(r+2mu)] e a NEC radial isolada é negativa. O setor extra de energia local zero com p_extra<0 também viola NEC radial na decomposição adotada. Pequena sobrepressão material não implica pequena tensão geométrica.

[M] Sem suporte para P(rc)>0, a cavidade vazia não satisfaz equilíbrio de interface. Registramos a escala |stress_superficial|~P rc/2 e o stress angular de Israel para o salto de derivada da métrica, como grandezas distintas. O suporte físico e seu acoplamento não foram fornecidos. Todos os f>0 falham no cenário de cavidade sem suporte; com setor extra, são MODELO INSUFICIENTE. Não há prova de estabilidade.

## 14. Ajuste/confronto conjunto
[M] Nenhum ajuste foi executado. Um único theta por caso atravessa os testes. Likelihood conceitual com GM,I,rho_neutrino,vP,vS,modos,Slichter requer covariâncias e leis materiais. PREM e gravidade não são canais estatisticamente independentes automaticamente. Ver `results/joint_likelihood.json`.

| Teste | Observável | Sensibilidade a f_V | Restrição obtida | Status |
|---|---|---|---|---|
{table}

Cada teste e a combinação têm f_max robusto nulo no sentido de **não calculável**, não f_max=0; o JSON usa `null`. **Limite quantitativo ainda não demonstrado.** No submodelo sem qualquer suporte de cavidade, nenhum f>0 demonstra equilíbrio; isso rejeita esse submodelo incompleto, não toda modificação C5B possível.

## 15. Região excluída
[M] Casos com o critério de pressão inacessível são excluídos desse critério; cavidades que eliminam todo o núcleo interno são excluídas da interpretação material terrestre literal. [F/M] Matéria estática até o horizonte fechado e interfaces materiais sem suporte com P(rc)>0 são inválidas. As demais falhas de observáveis ainda exigem dados/constitutivas; não foram ocultadas nem substituídas por ajuste.

## 16. Região ainda permitida
[?] Não foi demonstrada nenhuma faixa simultaneamente compatível com TODOS os observáveis gravitacionais, materiais e sísmicos. Valores pequenos podem gerar alterações pequenas em canais macroscópicos, mas permanecem não resolvidos e exigem suporte e dinâmica. 'Não excluído por esta bateria' não significa 'fisicamente permitido' ou confirmação.

## 17. Melhor observável futuro
[?] Para separar diretamente matéria e gravidade, a massa/número de nucleons inferida independentemente é o discriminador conceitual mais limpo. Na prática, observações sísmicas com travessias centrais e kernels de momento de inércia podem restringir cavidades macroscópicas antes; não existe ranking quantitativo de poder sem ruído/covariância. Slichter necessita primeiro de um modelo de acoplamento e uma medição confiável. Não alegamos que neutrinos já atingem as precisões necessárias.

## 18. Previsão falsificável C5B-Earth-01
[H/M] Previsão condicional fixada em `parameters.json` antes de usar dados-alvo: alpha=2, f∈[9e-7,1.1e-6], rc mínimo do critério de pressão 1% ({pred['cavity_m_interval'][0]:.6g}–{pred['cavity_m_interval'][1]:.6g} m). Prevê déficit de massa material na convenção QW02 de [9e-7,1.1e-6] M, ou [{pred['M_deficit_kg_interval'][0]:.6g},{pred['M_deficit_kg_interval'][1]:.6g}] kg. A precisão futura total requerida é <=1e-7 relativa.

Se dados FUTUROS independentes medirem massa material, devidamente convertida para a convenção areal/energia, com sigma/M<=1e-7, e não encontrarem esse déficit (resultado compatível com zero), esse intervalo será excluído a pelo menos 9 sigma sob ruído gaussiano e sistemáticas controladas. Não usamos o canal-alvo para ajustar f. A região é atualmente não resolvida, não demonstrada sobrevivente conjunta; o setor de suporte continua uma condição pendente. Uma previsão baseada só na definição de déficit é falsificável para essa parametrização, mas não constitui novo mecanismo causal derivado da C5B.

## 19. Teste exploratório aberto↔fechado
[M] Derivamos G_mu_nu para A(x0,r),F(x0,r), x0=ct, e conferimos por cálculo independente de Christoffel/Ricci. ∇mu G^mu_nu=0 foi verificada simbolicamente nas componentes temporal e radial. G_tr=-F_x0/(rF); fluxo ortonormal=-c⁴F_x0/(8πGr sqrt(AF)). Portanto variar F geralmente exige fluxo; mantendo F fixo não há fluxo radial obrigatório nessa ansatz diagonal, embora stresses anisotrópicos possam variar com o lapse.

[?] Não escolhemos interpolação temporal. Condições de extremidade A_inicial=A_open e A_final=F não são equação de evolução. Horizonte, junções, NEC e causalidade exigem chart regular e setor constitutivo. F=0 numa garganta aberta mínima não prova horizonte de eventos. Identidade de Bianchi não prova realizabilidade física, transição dinâmica nem propagação subluminal.

## 20. Limitações
Perfil de densidade prescrito, composição GR com stresses extras, cavidade/interface sem suporte especificado, velocidades sísmicas suplementares simplificadas, proxies de modos e Slichter, ausência de dados-alvo/covariâncias e fontes externas não consultadas com sucesso. Não há solução dinâmica, EOS terrestre completa, exclusão empírica global de f ou confirmação C5B. Mesmo o déficit material precisa de conversão relativística e composição nuclear para ser inferido por neutrinos.

[M] {verification['tests']['tests_run']} testes automatizados aprovados; controles de massa, fonte, horizonte, limite f pequeno, GR fraca, pressão e unidades. Convergência radial, conservação e tensor simbólico em `results/validation.json`. Sucesso numérico não implica estabilidade física.

## 21. Próximos testes
Obter dados/covariâncias independentes e o código/CSVs QW02 originais; definir suporte conservado e constitutiva elástica sem ajustar observáveis; resolver modos com gravidade e elasticidade acopladas; definir ancoragem da fonte/cavidade para Slichter; propagar raios e ondas com interface real; testar o déficit previsto sem ajuste pós-dados; derivar uma evolução causal aberto↔fechado.

## Referências e procedência
- Relatório QW02 enviado nesta conversa: preservado em `data/`, fonte dos 18 valores de regressão.
- QW01 e PREM pré-existentes: SHA256 registrado; nunca alterados.
- Dziewonski, A. M.; Anderson, D. L. (1981). Preliminary reference Earth model. Physics of the Earth and Planetary Interiors 25, 297–356. DOI: 10.1016/0031-9201(81)90046-7. Referência bibliográfica dos polinômios; sem dados brutos externos novos no ajuste.
- Slichter, L. B. (1961). The fundamental free mode of the Earth's inner core. PNAS 47, 186–190. DOI: 10.1073/pnas.47.2.186. Referência do problema físico; benchmark aqui derivado sob aproximações declaradas.
- Neutrino tomography of Earth, arXiv:1803.05901: referência para futura obtenção de likelihood, não usada para um limite numérico. Consulta externa falhou; não atribuímos nenhuma precisão publicada sem acesso.
'''
    doc=doc.replace('Consulta a páginas científicas externas ficou indisponível neste ambiente; `data/source_access.json` documenta tentativas.',source_note)
    doc=doc.replace('As precisões espectrais na tabela são sensibilidade desse proxy.', 'As precisões espectrais na tabela são sensibilidade desse proxy. O trabalho da borda interna sob pressão não nula e a rigidez do suporte geométrico também não são modelados; a fórmula não é um autovalor da cavidade em equilíbrio.')
    doc=doc.replace('Pequena sobrepressão material não implica pequena tensão geométrica.',f"Pequena sobrepressão material não implica pequena tensão geométrica. Em {verification['negative_total_radial_NEC_at_cavity_cases']} casos, a NEC radial TOTAL também é negativa na borda da cavidade; os valores estão no CSV hidrostático e na grade completa. Para f=1e-6, critério 1%, estado aberto, o stress extra na borda é {small['extra_radial_support_Pa']:.6g} Pa.")
    if available_sources:
        doc=doc.replace('fontes externas não consultadas com sucesso','ausência de dados observacionais brutos e covariâncias, mesmo com metadados bibliográficos acessíveis')
        doc=doc.replace('Consulta externa falhou; não atribuímos nenhuma precisão publicada sem acesso.','Metadados e excertos obtidos quando acessíveis; nenhuma precisão é usada como likelihood sem seus pressupostos e sistemáticas.')
    (ROOT/'C5B_QO_QW03_Earth_Constraint_Battery.md').write_text(doc)


def package():
    included=[]
    for p in ROOT.rglob('*'):
        if p.is_file() and not any(s in p.parts for s in ['__pycache__','.mplconfig','.cache']) and p.name not in ['manifest_sha256.json','package_verification.json']:
            included.append(p)
    included.append(ROOT.parent/'c5b_qo/study.py')
    manifest={str(p.relative_to(ROOT.parent)):hashlib.sha256(p.read_bytes()).hexdigest() for p in included}
    save_json('results/manifest_sha256.json',manifest);included.append(ROOT/'results/manifest_sha256.json')
    path=ROOT.parent/'C5B_QO_QW03_Earth_Constraint_Battery.zip'
    with zipfile.ZipFile(path,'w',zipfile.ZIP_DEFLATED) as z:
        for p in sorted(included):z.write(p,str(p.relative_to(ROOT.parent)))
    with zipfile.ZipFile(path) as z:
        assert z.testzip() is None
        for name,digest in manifest.items():assert hashlib.sha256(z.read(name)).hexdigest()==digest
        count=len(z.namelist())
    verification={'zip_name':path.name,'bytes':path.stat().st_size,'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'files':count,'CRC_verified':True,'manifest_files_verified':len(manifest)}
    save_json('results/package_verification.json',verification);return verification


def finish(start):
    rows=json.loads((ROOT/'results/cases.json').read_text());verification=validate(rows)
    plots(rows);report(rows,verification)
    verification['elapsed_seconds']=time.time()-start
    save_json('results/validation.json',verification)
    p=package();print(json.dumps({'STATUS':'EXECUÇÃO CONCLUÍDA','validation':verification,'ZIP':p},indent=2),flush=True)
