"""GR prescribed-density reconstruction; QW02 source and changes are documented."""
from __future__ import annotations
import hashlib, importlib.util, json, math, os
from functools import lru_cache
from pathlib import Path
import numpy as np
from scipy.integrate import quad, solve_ivp
from scipy.optimize import brentq
ROOT=Path(__file__).resolve().parent
os.environ.setdefault('MPLCONFIGDIR', str(ROOT/'results/.mplconfig'))
os.environ.setdefault('XDG_CACHE_HOME', str(ROOT/'results/.cache'))
spec=importlib.util.spec_from_file_location('qw03_prem',ROOT.parent/'c5b_qo/study.py')
prem=importlib.util.module_from_spec(spec); spec.loader.exec_module(prem)
G,C,M,R=prem.G,prem.C,prem.M,prem.R
IC=1221500.; RHOC=float(prem.density(0)); EPS=G*M/(R*C*C); PS=G*M*M/R**4
PARAMS=json.loads((ROOT/'parameters.json').read_text())
ST=C**4/(8*np.pi*G)


def verify_prem():
    h=hashlib.sha256((ROOT.parent/'c5b_qo/study.py').read_bytes()).hexdigest()
    if h!=PARAMS['expected_PREM_sha256']: raise RuntimeError('PREM original foi alterado')
    return h


def save_json(name,value):
    p=ROOT/name;p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(value,indent=2,ensure_ascii=False,allow_nan=False)+'\n')


def write_csv(name,rows):
    import csv
    p=ROOT/name;p.parent.mkdir(parents=True,exist_ok=True)
    if not rows:return
    keys=list(dict.fromkeys(k for row in rows for k in row))
    with p.open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=keys);w.writeheader();w.writerows(rows)


def inertia_below(r):
    return sum(8*np.pi/3*1000*prem.NORMALIZATION*(prem.primitive(a,np.clip(r,lo*1000,hi*1000),4)-prem.primitive(a,lo*1000,4)) for lo,hi,a in prem.LAYERS)
I0=float(inertia_below(R))


def norm(f,rc):
    if not (0<=rc<R):raise ValueError('A cavidade deve ser menor que a Terra')
    return (1-f)/(1-float(prem.mass(rc))/M)


# Exact polynomial integrals: rho m/r^2 and rho/r^2; long double suppresses cancellation.
def _int_power(p,a,b):
    a,b=np.longdouble(a),np.longdouble(b)
    if p==-1:return np.log(b/a)
    if a==0 and p<0:raise ValueError('Integral singular')
    return (b**(p+1)-a**(p+1))/(p+1)


def integrals(rc):
    pbase=np.longdouble(0); L=np.longdouble(0)
    for lo,hi,co in prem.LAYERS:
        a,b=max(rc,lo*1000),hi*1000
        if a>=b:continue
        rho={j:np.longdouble(1000*prem.NORMALIZATION*cc)/np.longdouble(R)**j for j,cc in enumerate(co) if cc}
        mp={j+3:4*np.longdouble(np.pi)*cc/(j+3) for j,cc in rho.items()}
        offset=np.longdouble(float(prem.mass(lo*1000)))-sum(cc*np.longdouble(lo*1000)**j for j,cc in mp.items())
        mp[0]=offset
        for i,cc in rho.items():
            if rc>0:L+=cc*_int_power(i-2,a,b)
            for j,dd in mp.items():
                if dd!=0:pbase+=np.longdouble(G)*cc*dd*_int_power(i+j-2,a,b)
    return pbase,L


def pressure_newton(f,rc):
    p,L=integrals(rc); h=np.longdouble(float(prem.mass(rc))); n=np.longdouble(norm(f,rc))
    return float(n*n*(p-G*h*L)),float(n*G*f*M*L)


def cavity_threshold(f,tol):
    if f==0:return {'rc_m':0.,'status':'PASSA','weak_pressure_excess':0.}
    r0=2*G*f*M/C**2
    # Infinitesimal massive outer shell: mean material mass is half its total mass.
    floor=2*f/(1-f)
    if floor>=tol:return {'rc_m':None,'status':'EXCLUÍDO','reason':'Critério de pressão inacessível nesta família prescrita','shell_limit':floor}
    def fun(logr):
        p,d=pressure_newton(f,np.exp(logr));return d/p-tol
    hi=R*(1-1e-5)
    if fun(np.log(hi))>0:return {'rc_m':None,'status':'NÃO RESOLVIDO','reason':'Raiz no limite de casca muito fina','shell_limit':floor}
    rc=float(np.exp(brentq(fun,np.log(max(r0*100,1e-13)),np.log(hi),xtol=1e-12)))
    p,d=pressure_newton(f,rc)
    return {'rc_m':rc,'status':'PASSA','weak_pressure_excess':d/p,'shell_limit':floor}


class MatterReference:
    """TOV matter-only comparator with exactly the same prescribed cavity and rho."""
    def __init__(self,f,rc,rtol=2e-10):
        self.f,self.rc,self.n=f,rc,norm(f,rc);self.h=float(prem.mass(rc));self.parts=[]
        state=[0.,.5*np.log1p(-2*EPS*(1-f))/EPS]
        for lo,hi,co in reversed(prem.LAYERS):
            a,b=max(rc,lo*1000,1e-12),hi*1000
            if a>=b:continue
            def rhs(t,v):
                rr=R*np.exp(t);x=rr/R
                rho=self.n*1000*prem.NORMALIZATION*np.polynomial.polynomial.polyval(x,co)
                mm=self.n*(float(prem.mass(rr))-self.h)/M
                FF=1-2*EPS*mm/x
                q,psi=v;dpsi=(mm+4*np.pi*EPS*x**3*q)/(x*FF)
                return [-(rho/(M/R**3)+EPS*q)*dpsi,dpsi]
            sol=solve_ivp(rhs,(np.log(b/R),np.log(a/R)),state,method='DOP853',rtol=rtol,atol=2e-13,max_step=.6,dense_output=True)
            if not sol.success:raise RuntimeError(sol.message)
            self.parts.append((np.log(a/R),np.log(b/R),sol.sol));state=sol.y[:,-1]
    def evaluate(self,r):
        rr=np.atleast_1d(np.asarray(r,dtype=float));t=np.log(np.maximum(rr,1e-12)/R)
        pp=np.zeros_like(rr);phi=np.zeros_like(rr)
        for a,b,s in self.parts:
            mask=(t>=a-1e-14)&(t<=b+1e-14)
            if mask.any():q,psi=s(t[mask]);pp[mask]=q*PS;phi[mask]=psi*EPS
        rho=self.n*prem.density(rr);mm=self.n*(prem.mass(rr)-self.h)
        FF=1-2*G*mm/(C*C*rr)
        phip=G*(mm+4*np.pi*rr**3*pp/C**2)/(C*C*rr**2*FF)
        return {'P0':pp,'phiE':phi,'rho':rho,'m':mm,'FE':FF,'phiEp':phip}


@lru_cache(maxsize=180)
def matter(f,rc):return MatterReference(f,rc)


def geometry(r,f,rc,state='open'):
    rr=np.atleast_1d(np.asarray(r,dtype=float));mu=G*f*M/C**2;r0=2*mu
    if np.any(rr<rc):raise ValueError('r dentro da cavidade: matéria externa não definida')
    if f and np.any(rr<r0):raise ValueError('r abaixo do domínio areal de uma boca')
    e=matter(float(f),float(rc)).evaluate(rr)
    if f==0:phiW=np.zeros_like(rr);phipW=np.zeros_like(rr)
    elif state=='open':phiW=-.5*np.log1p(2*mu/rr);phipW=mu/(rr*(rr+2*mu))
    else:
        if np.any(rr<=r0):raise ValueError('observador estático fechado no horizonte não existe')
        phiW=.5*np.log1p(-r0/rr);phipW=mu/(rr*(rr-r0))
    # Factored isolated F prevents loss of the exact throat zero to roundoff.
    F=(rr-r0)/rr-2*G*e['m']/(C*C*rr)
    if np.any(F< -1e-14):raise ValueError('F negativo no domínio estático composto')
    F=np.maximum(F,0.)
    phi=e['phiE']+phiW;phip=e['phiEp']+phipW
    return {**e,'F':F,'A':np.exp(2*phi),'phi':phi,'phiWp':phipW,'phip':phip,
            'g':C*C*np.sqrt(F)*phip,'g_virtual':C*C*np.sqrt(np.maximum((rr-r0)/rr,0))*phipW,
            'g_newton':G*(f*M+e['m'])/rr**2}


def pressure(f,rc,state='open',rtol=2e-10):
    e=matter(float(f),float(rc))
    if not f:return float(e.evaluate([max(rc,1e-12)])['P0'][0]),0.
    r0=2*G*f*M/C**2
    if state=='closed' and rc<=r0:raise ValueError('Pressão estática diverge no horizonte')
    start=max(rc,r0);q=[0.]
    for lo,hi,co in reversed(prem.LAYERS):
        a,b=max(start,lo*1000),hi*1000
        if a>=b:continue
        def rhs(t,v):
            rr=max(start,np.exp(t));x=geometry([rr],f,rc,state)
            rho=e.n*1000*prem.NORMALIZATION*np.polynomial.polynomial.polyval(rr/R,co)
            return [-rr*(float(x['phip'][0])*v[0]+(rho/RHOC+float(x['P0'][0])/(RHOC*C*C))*float(x['phiWp'][0]))]
        sol=solve_ivp(rhs,(np.log(b),np.log(a)),q,method='DOP853',rtol=rtol,atol=1e-25,max_step=.5)
        if not sol.success:raise RuntimeError(sol.message)
        q=sol.y[:,-1]
    d=float(q[0]*RHOC*C*C);return float(e.evaluate([start])['P0'][0])+d,d


def radial_grid(rc,resolution=1100):
    a=max(rc,1e-6)
    extra=[lo*1000 for lo,_,_ in prem.LAYERS if a<lo*1000<R]
    return np.unique(np.r_[np.geomspace(a,R,resolution),np.linspace(a,R,resolution),extra,[v for v in PARAMS['radial_sample_m'] if a<=v<=R]])


def pressure_profile(f,rc,state,rr):
    out=np.zeros_like(rr);minimum=max(rc,1e-6);q=[0.]
    for lo,hi,co in reversed(prem.LAYERS):
        a,b=max(minimum,lo*1000),hi*1000
        if a>=b:continue
        def rhs(t,v):
            r=max(minimum,np.exp(t));x=geometry([r],f,rc,state)
            rho=matter(f,rc).n*1000*prem.NORMALIZATION*np.polynomial.polynomial.polyval(r/R,co)
            return [-r*(rho/RHOC+v[0])*float(x['phip'][0])]
        sol=solve_ivp(rhs,(np.log(b),np.log(a)),q,method='DOP853',rtol=2e-10,atol=1e-25,max_step=.5,dense_output=True)
        mask=(rr>=a)&(rr<=b)
        out[mask]=sol.sol(np.log(rr[mask]))[0]*RHOC*C*C;q=sol.y[:,-1]
    return out


def require_regression():
    p=ROOT/'results/regression_QW02.json'
    if not p.exists() or not json.loads(p.read_text()).get('passed'):raise RuntimeError('Regressão QW02 não aprovada: testes novos bloqueados')
