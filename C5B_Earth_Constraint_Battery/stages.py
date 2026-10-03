"""Sequential Earth confrontation. Undefined material physics remains undefined."""
from __future__ import annotations
import csv, json, math
import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq
from core import *


def prepare_cases():
    fs=list(PARAMS['f_V']);crit=.001/(2+.001)
    fs=sorted(set(fs+[.99*crit,crit,1.01*crit]))
    rows=[{'case':'CONTROL-0','f_V':0.,'M_V_kg':0.,'mu_m':0.,'r0_m':0.,'alpha':2.,'state':'open','pressure_tolerance':.01,'rc_m':0.,'status_numeric':'PASSA','refined':False}]
    for f in fs:
        for tol in PARAMS['relative_pressure_thresholds']:
            threshold=cavity_threshold(f,tol)
            for state in ('open','closed'):
                rc=threshold['rc_m']
                row={'case':f'f{f:.15g}_p{tol}_{state}','f_V':f,'M_V_kg':f*M,'mu_m':G*f*M/C**2,'r0_m':2*G*f*M/C**2,'alpha':2.,'state':state,'pressure_tolerance':tol,'rc_m':rc,'status_numeric':threshold['status'],'refined':f not in PARAMS['f_V'],'pressure_shell_floor':threshold['shell_limit']}
                if rc is not None:
                    h=float(prem.mass(rc));n=norm(f,rc)
                    row.update(kappa=rc/row['r0_m'],normalization=n,removed_PREM_mass_kg=h,removed_PREM_mass_fraction=h/M,material_mass_kg=n*(M-h),virtual_mass_deficit_kg=f*M,total_mass_residual_fraction=(n*(M-h)+f*M-M)/M)
                rows.append(row)
    zero=rows[0];zero.update(kappa=None,normalization=1.,removed_PREM_mass_kg=0.,removed_PREM_mass_fraction=0.,material_mass_kg=M,virtual_mass_deficit_kg=0.,total_mass_residual_fraction=0.)
    save_json('results/grid_definition.json',{'f_V':fs,'alpha':2,'pressure_criteria':PARAMS['relative_pressure_thresholds'],'fixed_before_comparison':True,'cases':len(rows),'thin_shell_critical_f_for_0.1percent':crit})
    return rows


def valid(rows):return [r for r in rows if r['rc_m'] is not None]


def A_mass(rows):
    sens=[]
    for r in rows:
        f=r['f_V'];r['mass_vs_material_status']='PASSA' if f==0 else 'NÃO RESOLVIDO'
        sens.append({'case':r['case'],'f_V':f,'M_V_kg':f*M,'relative_precision_1sigma_for_1sigma_signal':f,'relative_precision_1sigma_for_5sigma_signal':f/5,'status':r['mass_vs_material_status'],'observational_independent_material_likelihood':'not available; PREM is gravitationally normalized'})
    write_csv('tables/01_mass_vs_matter.csv',sens)
    write_csv('tables/01_neutrino_sensitivity.csv',[{'f_V':f,'hypothetical_sigma_relative':s,'signal_to_noise_if_independent':f/s,'is_current_observational_limit':False} for f in PARAMS['f_V'] for s in PARAMS['sensitivity_only']['mass_material_sigma_fraction']])


def roots_on_grid(fun,rr,values=None):
    vv=np.asarray([fun(r) for r in rr]) if values is None else np.asarray(values);out=[]
    for a,b,fa,fb in zip(rr[:-1],rr[1:],vv[:-1],vv[1:]):
        if fa*fb<0:out.append(float(brentq(fun,a,b,xtol=1e-8)))
    return out


def B_gravity(rows):
    crossed=[];sampled=[]
    for r in valid(rows):
        f,rc,state=r['f_V'],r['rc_m'],r['state'];rr=radial_grid(rc,650)
        geo=geometry(rr,f,rc,state);base=geometry(rr,0.,0.);rel=geo['g']/base['g']-1
        def rel_at(x):return float(geometry([x],f,rc,state)['g'][0]/geometry([x],0.,0.)['g'][0]-1)
        for tol in PARAMS['relative_gravity_thresholds']:
            cr=roots_on_grid(lambda x:abs(rel_at(x))-tol,rr,abs(rel)-tol)
            crossed.append({'case':r['case'],'f_V':f,'state':state,'rc_m':rc,'relative_threshold':tol,'crossing_radii_m':json.dumps(cr),'domain_start_relative_anomaly':float(rel[0]),'status':'PASSA' if cr else 'NÃO RESOLVIDO','meaning':'No crossing does not establish exclusion; cavity domain can remove crossing.'})
        if f:
            balance=roots_on_grid(lambda x: float(geometry([x],f,rc,state)['g_virtual'][0])-G*float(geometry([x],f,rc,state)['m'][0])/x**2,rr,geo['g_virtual']-G*geo['m']/rr**2)
        else:balance=[]
        r['virtual_material_balance_radii_m']=json.dumps(balance)
        r['g_surface_m_s2']=float(geo['g'][-1]);r['delta_g_surface_relative']=float(rel[-1]);r['delta_g_at_rc_relative']=float(rel[0])
        for rad in PARAMS['radial_sample_m']+[.1*R,R]:
            inside=rad<max(rc,1e-12)
            sampled.append({'case':r['case'],'f_V':f,'state':state,'r_m':rad,'inside_cavity':inside,'g_C5B_m_s2':None if inside else float(geometry([rad],f,rc,state)['g'][0]),'g_PREM_static_GR_m_s2':float(geometry([rad],0.,0.)['g'][0]),'g_PREM_Newton_m_s2':float(prem.gravity(rad)),'delta_g_relative':None if inside else rel_at(rad)})
        if r['pressure_tolerance']==.01:
            data=[{'r_m':float(x),'g_PREM_Newton':float(prem.gravity(x)),'g_PREM_GR':float(bg),'g_C5B_GR':float(g),'delta_g':float(g-bg),'relative_delta_g':float(d),'rho_material':float(rho)} for x,bg,g,d,rho in zip(rr,base['g'],geo['g'],rel,geo['rho'])]
            write_csv('results/profiles/'+r['case']+'.csv',data)
    write_csv('tables/02_gravity_crossings.csv',crossed);write_csv('tables/02_gravity_samples.csv',sampled)


def C_cavity(rows):
    out=[]
    for r in valid(rows):
        rc=r['rc_m'];volume=4*np.pi*rc**3/3
        # Solid-inner-core existence excludes literal removal of all its material.
        status='EXCLUÍDO' if rc>=IC else ('PASSA' if r['f_V']==0 else 'NÃO RESOLVIDO')
        r.update(cavity_volume_m3=volume,inner_core_volume_fraction_removed=min(1.,(rc/IC)**3),density_external_relative_change=r['normalization']-1,cavity_status=status)
        for freq in PARAMS['sensitivity_only']['seismic_frequency_Hz']:
            wavelength=11262.2/freq
            out.append({'case':r['case'],'f_V':r['f_V'],'rc_m':rc,'cavity_volume_m3':volume,'removed_mass_fraction':r['removed_PREM_mass_fraction'],'inner_core_volume_fraction_removed':r['inner_core_volume_fraction_removed'],'external_density_change_fraction':r['density_external_relative_change'],'frequency_Hz':freq,'central_P_wavelength_m':wavelength,'rc_over_wavelength':rc/wavelength,'classification':'A' if rc>=IC else 'C','status':status,'resolution_is_observed_upper_limit':False})
    write_csv('tables/03_cavity_constraints.csv',out)


def D_inertia(rows):
    out=[];conditional=[]
    for r in valid(rows):
        rc,f,n=r['rc_m'],r['f_V'],r['normalization']
        ir=float(inertia_below(rc));im=n*(I0-ir);delta=im/I0-1
        r.update(I_material_kg_m2=im,I_virtual_assumed_kg_m2=0.,delta_I_over_I=delta,delta_I_microscopic_approx=-f)
        out.append({'case':r['case'],'f_V':f,'rc_m':rc,'I_PREM_kg_m2':I0,'I_PREM_over_MR2':I0/(M*R**2),'I_C5B_kg_m2':im,'delta_M_over_M':r['total_mass_residual_fraction'],'delta_I_over_I':delta,'status':'PASSA' if f==0 else 'NÃO RESOLVIDO','independent_observed_I_covariance_available':False,'virtual_inertia_assumption':'nonrotating central source: zero inertial contribution'})
        for sig in PARAMS['sensitivity_only']['inertia_assumed_sigma_fraction']:
            conditional.append({'case':r['case'],'f_V':f,'assumed_relative_I_sigma':sig,'conditional_sigma_discrepancy':abs(delta)/sig,'conditional_3sigma_status':'EXCLUÍDO' if abs(delta)>3*sig else 'PASSA','is_observed_exclusion':False,'microscopic_f_limit_if_profile_known':3*sig})
    write_csv('tables/04_mass_inertia.csv',out);write_csv('tables/04_inertia_conditional.csv',conditional)
    save_json('results/inertia_reference.json',{'M_PREM_kg':M,'I_PREM_kg_m2':I0,'I_PREM_over_MR2':I0/(M*R**2),'reference':'normalized prescribed QW01 PREM','robust_f_upper_limit':None,'statement':'limite quantitativo ainda não demonstrado'})


def binding_energy(f,rc):
    n=norm(f,rc);hole=float(prem.mass(rc));value=0.
    for lo,hi,co in prem.LAYERS:
        a,b=max(rc,lo*1000),hi*1000
        if a>=b:continue
        def term(x):
            rho=n*1000*prem.NORMALIZATION*np.polynomial.polynomial.polyval(x/R,co)
            mm=n*(float(prem.mass(x))-hole)
            return -4*np.pi*G*rho*(mm+f*M)*x
        value+=quad(term,a,b,epsabs=1e12,epsrel=1e-10)[0]
    return value


def potential(r,f,rc):
    n=norm(f,rc);hole=float(prem.mass(rc));shell=0.
    for lo,hi,co in prem.LAYERS:
        a,b=max(r,rc,lo*1000),hi*1000
        if a<b:shell+=quad(lambda x:4*np.pi*n*1000*prem.NORMALIZATION*np.polynomial.polynomial.polyval(x/R,co)*x,a,b,epsrel=1e-10)[0]
    return -G*((f*M+n*(float(prem.mass(r))-hole))/r+shell)


def E_modes(rows):
    gamma=PARAMS['sensitivity_only']['radial_mode_gamma'];W0=binding_energy(0.,0.)
    omega0=np.sqrt((3*gamma-4)*abs(W0)/(1.5*I0));out=[];pots=[]
    for r in valid(rows):
        f,rc=r['f_V'],r['rc_m'];W=binding_energy(f,rc)
        omega=np.sqrt((3*gamma-4)*abs(W)/(1.5*r['I_material_kg_m2']));d=omega/omega0-1
        r.update(radial_homologous_proxy_delta_omega=d,binding_energy_J=W)
        out.append({'case':r['case'],'f_V':f,'rc_m':rc,'Gamma_fixed':gamma,'omega_benchmark_rad_s':float(omega0),'omega_proxy_rad_s':float(omega),'proxy_delta_omega_over_omega':float(d),'relative_precision_for_5sigma_proxy':abs(float(d))/5,'mode_0S0_prediction_available':False,'status':'MODELO INSUFICIENTE','model':'Homologous fluid energy Rayleigh estimate; not elastic normal-mode eigenfrequency'})
        if r['pressure_tolerance']==.01:
            for rad in np.geomspace(max(rc,1.),R,100):
                u=potential(rad,f,rc);u0=potential(rad,0.,0.)
                pots.append({'case':r['case'],'r_m':rad,'potential_Newton_C5B_m2_s2':u,'potential_Newton_PREM_m2_s2':u0,'delta_potential_m2_s2':u-u0})
    write_csv('tables/05_normal_mode_sensitivity.csv',out);write_csv('tables/05_potential_profiles.csv',pots)


def slichter_benchmark(rhoi,rhoo):
    omega2=4*np.pi*G/3*rhoo*(rhoi-rhoo)/(rhoi+rhoo/2)
    return None if omega2<=0 else 2*np.pi/np.sqrt(omega2)


def F_slichter(rows):
    vic=4*np.pi*IC**3/3;mic=float(prem.mass(IC));rhoi=mic/vic;rhoo=float(prem.density(np.nextafter(IC,np.inf)))
    T0=slichter_benchmark(rhoi,rhoo);out=[]
    for r in valid(rows):
        n,rc,f=r['normalization'],r['rc_m'],r['f_V']
        Ts=T0/np.sqrt(n)
        effective=n*max(mic-float(prem.mass(min(rc,IC))),0)/vic
        Th=slichter_benchmark(effective,n*rhoo)
        # A fixed central source inside a rigid translated hollow shell has zero force
        # for displacements smaller than the cavity (Newton shell theorem).
        d=Ts/T0-1;r['slichter_density_proxy_delta_T']=float(d)
        row={'case':r['case'],'f_V':f,'rc_m':rc,'T_reference_buoyancy_added_mass_s':float(T0),'T_density_scaling_proxy_s':float(Ts),'delta_T_density_proxy_s':float(Ts-T0),'delta_T_density_proxy_relative':float(d),'T_homogenized_shell_proxy_s':None if Th is None else float(Th),'homogenized_shell_proxy_note':'negative buoyancy stiffness' if Th is None else 'toy model only','direct_virtual_rigid_hollow_shell_stiffness_N_m':0.,'fixed_filled_sphere_virtual_stiffness_N_m':4*np.pi*G/3*rhoi*f*M,'future_precision_for_5sigma_density_proxy':abs(float(d))/5,'status':'MODELO INSUFICIENTE','actual_Slichter_detection_assumed':False}
        out.append(row)
    write_csv('tables/06_slichter.csv',out)
    crossings=[]
    sample=sorted((r for r in valid(rows) if r['pressure_tolerance']==.01 and r['state']=='open'),key=lambda r:r['f_V'])
    for target in [.001,.01,.1]:
        brackets=[]
        for a,b in zip(sample[:-1],sample[1:]):
            if (abs(a['slichter_density_proxy_delta_T'])-target)*(abs(b['slichter_density_proxy_delta_T'])-target)<0:
                def fun(f):
                    rc=cavity_threshold(f,.01)['rc_m'];return abs(norm(f,rc)**(-.5)-1)-target
                brackets.append(brentq(fun,a['f_V'],b['f_V']))
        crossings.append({'relative_period_shift':target,'density_proxy_f_crossings':brackets,'physical_f_limit':None})
    save_json('results/slichter_thresholds.json',{'T_benchmark_s':float(T0),'rho_ic_mean_kg_m3':rhoi,'rho_oc_ICB_kg_m3':rhoo,'equation':'omega^2=4*pi*G/3*rho_oc*(rho_ic-rho_oc)/(rho_ic+rho_oc/2)','crossings':crossings,'caveat':'Rigid homogeneous nonrotating buoyancy+added-mass benchmark, not full PREM rotating eigenproblem; source anchoring and cavity motion unspecified.'})


# Explicit PREM P-speed polynomials added separately: never alter the density source.
VP_LAYERS=[(0.,IC,[11.2622,0.,-6.3640]),(IC,3480000.,[11.0487,-4.0362,4.8023,-13.5732]),(3480000.,5701000.,[15.3891,-5.3181,5.5242,-2.5514]),(5701000.,5771000.,[19.0957,-9.8672]),(5771000.,5971000.,[39.7027,-32.6166]),(5971000.,6151000.,[20.3926,-12.2569]),(6151000.,6346600.,[4.1875,3.9382]),(6346600.,6356000.,[6.8]),(6356000.,6368000.,[5.8]),(6368000.,R,[1.45])]


def vp(r):
    for lo,hi,co in VP_LAYERS:
        if lo<=r<=hi:return 1000*np.polynomial.polynomial.polyval(r/R,co)
    raise ValueError('vP fora da Terra')


def travel_removed(rc):
    return sum(2*quad(lambda r:1/(1000*np.polynomial.polynomial.polyval(r/R,co)),lo,min(hi,rc),epsrel=1e-11)[0] for lo,hi,co in VP_LAYERS if lo<rc)


def G_pkikp(rows):
    out=[]
    for r in valid(rows):
        rc=r['rc_m'];removed=travel_removed(rc);r['central_chord_PREM_time_removed_s']=removed
        base={'case':r['case'],'f_V':r['f_V'],'rc_m':rc,'central_chord_PREM_time_s':float(travel_removed(R)),'removed_segment_PREM_time_s':float(removed),'central_ray_assumed':True,'status':'MODELO INSUFICIENTE'}
        out.append({**base,'scenario':'vacuum','delta_t_s':None,'direct_elastic_energy_transmission':1. if rc==0 else 0.,'meaning':'No direct elastic PKIKP through a literal vacuum; no finite arrival-time shift can be assigned'})
        out.append({**base,'scenario':'geometry_without_matter','delta_t_s':None,'direct_elastic_energy_transmission':None,'meaning':'GR metric alone does not define seismic-wave propagation or throat-to-Earth topology'})
        eta=PARAMS['sensitivity_only']['rarefied_density_ratio']
        for ratio in PARAMS['sensitivity_only']['rarefied_vP_ratios']:
            z=eta*ratio;trans=4*z/(1+z)**2
            dt=2*rc/(ratio*vp(0))-removed
            out.append({**base,'scenario':f'rarefied_eta_{eta}_v_ratio_{ratio}','delta_t_s':float(dt),'direct_elastic_energy_transmission':float(trans**2) if rc else 1.,'meaning':'Two normal-incidence plane interfaces; no reverberation, diffraction, attenuation or GR delay; speed is an explicit unknown-material scenario'})
        out.append({**base,'scenario':'ideal_material_interface_matched_speed','delta_t_s':float(2*rc/vp(0)-removed),'direct_elastic_energy_transmission':1.,'meaning':'Idealized speed/impedance matched material, not a vacuum'})
    write_csv('tables/07_pkikp_scenarios.csv',out)
    write_csv('tables/07_time_sensitivity.csv',[{'time_difference_s':t,'radius_of_PREM_segment_with_that_duration_m':float(brentq(lambda rc:travel_removed(rc)-t,0.,IC)),'meaning':'Removed travel-time scale, not a predicted transmitted vacuum arrival'} for t in [.001,.01,.1,1.]])
    save_json('data/PREM_velocity_extension.json',{'source_citation':'Dziewonski & Anderson (1981), Preliminary reference Earth model, Physics of the Earth and Planetary Interiors 25, 297-356; DOI 10.1016/0031-9201(81)90046-7','polynomials_km_s_in_r_over_R':VP_LAYERS,'provenance':'Explicit literature polynomial transcription, additional to unchanged QW01 density-only source; external source retrieval failed in this environment. Simplified 1D diagnostic, not a complete anisotropic elasticity model.'})


def H_hydrostatic(rows):
    out=[]
    for r in valid(rows):
        f,rc,state=r['f_V'],r['rc_m'],r['state'];p,d=pressure(f,rc,state);pref=float(matter(f,rc).evaluate([max(rc,1e-12)])['P0'][0]);ex=d/pref
        r.update(P_rc_Pa=p,pressure_excess_relative_GR=ex,pressure_ref_same_cavity_Pa=pref,surface_stress_support_scale_N_m=rc*p/2,hydrostatic_without_extra_support_status='PASSA' if f==0 else 'EXCLUÍDO',full_hydrostatic_status='PASSA' if f==0 else 'MODELO INSUFICIENTE')
        x=geometry([max(rc,1e-6)],f,rc,state);rad=max(rc,1e-6);mu=G*f*M/C**2
        prw=0. if state=='closed' else -8*ST*mu**2/(rad**3*(rad+2*mu))
        be=2*G*float(x['m'][0])/C**2;bw=2*mu
        cross=-2*ST*(be*float(x['phiWp'][0])+bw*float(x['phiEp'][0]))/rad**2
        extra=prw+cross-d
        r['extra_radial_support_Pa']=extra
        r['NEC_total_at_rc_Pa']=float(x['rho'][0])*C*C+pref+prw+cross
        out.append({'case':r['case'],'f_V':f,'state':state,'rc_m':rc,'P_rc_Pa':p,'P_reference_same_cavity_Pa':pref,'relative_pressure_excess':ex,'pressure_negative':p<0,'A_rc':float(x['A'][0]),'F_rc':float(x['F'][0]),'extra_radial_stress_Pa':extra,'extra_radial_NEC_Pa_if_zero_extra_energy':extra,'support_stress_magnitude_N_m':rc*p/2,'Israel_surface_angular_stress_from_metric_N_m':ST*np.sqrt(float(x['F'][0]))*float(x['phiEp'][0]),'unsupported_cavity_status':r['hydrostatic_without_extra_support_status'],'status':r['full_hydrostatic_status'],'dynamic_stability_demonstrated':False})
        if r['pressure_tolerance']==.01:
            path=ROOT/'results/profiles'/ (r['case']+'.csv')
            with path.open() as handle:data=list(csv.DictReader(handle))
            rr=np.array([float(a['r_m']) for a in data]);pp=pressure_profile(f,rc,state,rr)
            for a,b in zip(data,pp):a['P_C5B_Pa']=float(b)
            write_csv('results/profiles/'+r['case']+'.csv',data)
    write_csv('tables/08_hydrostatic.csv',out)
    for a,r in zip(out,valid(rows)):
        a['NEC_total_at_rc_Pa']=r['NEC_total_at_rc_Pa']
    write_csv('tables/08_hydrostatic.csv',out)


def I_joint(rows):
    out=[]
    for r in rows:
        if r['rc_m'] is None:status='EXCLUÍDO';why='Specified pressure criterion unattainable in prescribed family (Newton diagnostic)'
        elif r.get('cavity_status')=='EXCLUÍDO':status='EXCLUÍDO';why='Literal cavity removes the entire solid inner core'
        elif r['f_V']==0:status='PASSA';why='Conventional baseline control'
        else:status='MODELO INSUFICIENTE';why='Required material/interface support and elastic/dynamic likelihood not specified; no robust joint empirical limit'
        r['joint_status']=status
        out.append({'case':r['case'],'f_V':r['f_V'],'rc_m':r['rc_m'],'status':status,'reason':why,'maximum_allowed_f_demonstrated':False})
    write_csv('tables/09_joint_constraints.csv',out)
    tests=[('A/I','Independent material mass vs GM','Delta M/M=f','NÃO RESOLVIDO'),('B','Deep static gravity','Central fractional signal approximately f*M/m_PREM(r) in weak field','NÃO RESOLVIDO'),('C','Solid inner-core existence','Depends on rc and sampling; rc>=IC excluded for literal empty cavity','TENSÃO'),('D','Total mass and inertia','Delta I/I=n*(1-I_removed/I0)-1; microscopic -f','NÃO RESOLVIDO'),('E','Elastic normal modes','Homologous fluid proxy only; mode kernels not specified','MODELO INSUFICIENTE'),('F','Slichter','Density and anchoring dependent; hollow-shell direct force vanishes locally','MODELO INSUFICIENTE'),('G','PKIKP','Delta t scenario-dependent; vacuum has no direct elastic transmission','MODELO INSUFICIENTE'),('H','Hydrostatic/interface support','P(rc)>0 needs support; composed-metric extra stress required','MODELO INSUFICIENTE'),('K','Open/closed dynamics','Einstein tensor requirements, no evolution law','MODELO INSUFICIENTE')]
    write_csv('tables/summary_by_test.csv',[{'Teste':t,'Observavel':o,'Sensibilidade_a_f':s,'Restricao_obtida':'limite quantitativo ainda não demonstrado' if t!='C' else 'Literal cavity rc >= 1221.5 km incompatible with solid inner core','Status':status,'f_max_robust':None} for t,o,s,status in tests])
    save_json('results/joint_likelihood.json',{'observables':['GM','I','rho_neutrino(r)','v_P(r)','v_S(r)','normal_modes','Slichter'],'theta':['f_V','alpha','r_c'],'fixed_theta_across_tests':True,'conceptual':'log L=-0.5*(O(theta)-D)^T Cov^{-1}*(O(theta)-D), with material and calibration nuisance covariances explicitly required; correlated PREM and gravity inputs must not be double counted','fit_executed':False,'missing':['Independent material mass likelihood','Observed inertia covariance and PREM inversion covariance','Constitutive material and support law','Elastic modes and core-source anchoring'],'global_f_max_robust':None,'statement':'limite quantitativo ainda não demonstrado','unsupported_vacuum_equilibrium':'No f>0 in this battery demonstrates static material equilibrium without extra support.'})
    pred=dict(PARAMS['prediction_preregistered']);pred['M_deficit_kg_interval']=[a*M for a in pred['f_V_interval']];pred['cavity_m_interval']=[cavity_threshold(a,.01)['rc_m'] for a in pred['f_V_interval']];pred['falsification']='If an independent future material-mass reconstruction with total relative sigma <=1e-7 finds a deficit consistent with zero, the predefined interval [9e-7,1.1e-6] is rejected at >=9 Gaussian sigma under this mass convention. No target data used; calibration, interactions and systematics must be controlled.'
    save_json('results/C5B-Earth-01_prediction.json',pred)


FUNCTIONS=[A_mass,B_gravity,C_cavity,D_inertia,E_modes,F_slichter,G_pkikp,H_hydrostatic,I_joint]


def run_stage(index):
    require_regression();progress_path=ROOT/'results/stage_progress.json'
    progress=json.loads(progress_path.read_text()) if progress_path.exists() else []
    if index>1 and index-1 not in progress:raise RuntimeError('Executar etapas sequencialmente')
    rows=prepare_cases() if index==1 else json.loads((ROOT/'results/cases.json').read_text())
    if index<=9:FUNCTIONS[index-1](rows)
    elif index==10:
        from dynamics import run
        run()
    save_json('results/cases.json',rows);write_csv('tables/full_grid.csv',rows)
    if index not in progress:progress.append(index)
    save_json('results/stage_progress.json',progress)
    print(f'STAGE {index} completed; grid={len(rows)}, numeric={len(valid(rows))}',flush=True)
