"""General spherical Einstein tensor, not an invented transition solution."""
import sympy as s
from core import save_json


def run():
    t,r,theta,phi=s.symbols('x0 r theta phi',real=True);coords=[t,r,theta,phi]
    A=s.Function('A')(t,r);F=s.Function('F')(t,r)
    g=s.diag(-A,1/F,r*r,r*r*s.sin(theta)**2);gi=g.inv()
    gamma={}
    for a in range(4):
        for b in range(4):
            for c in range(4):
                val=sum(gi[a,d]*(s.diff(g[d,c],coords[b])+s.diff(g[d,b],coords[c])-s.diff(g[b,c],coords[d])) for d in range(4))/2
                gamma[a,b,c]=s.simplify(val)
    Ric=s.zeros(4)
    for a in range(4):
        for b in range(a,4):
            val=sum(s.diff(gamma[c,a,b],coords[c])-s.diff(gamma[c,a,c],coords[b])+sum(gamma[c,c,d]*gamma[d,a,b]-gamma[c,b,d]*gamma[d,a,c] for d in range(4)) for c in range(4))
            Ric[a,b]=Ric[b,a]=s.simplify(val)
    scalar=s.simplify(sum(gi[a,b]*Ric[a,b] for a in range(4) for b in range(4)))
    Ein=s.simplify(Ric-g*scalar/2)
    pr=s.diff(A,r)/(2*A);prr=s.diff(A,r,2)/(2*A)-s.diff(A,r)**2/(2*A*A);pt=s.diff(A,t)/(2*A)
    angular=F*(prr+pr**2)+s.diff(F,r)*pr/2+F*pr/r+s.diff(F,r)/(2*r)+s.diff(F,t,2)/(2*A*F)-3*s.diff(F,t)**2/(4*A*F*F)-s.diff(F,t)*pt/(2*A*F)
    expect={(0,0):A*(1-F-r*s.diff(F,r))/r**2,(1,1):(F-1+2*r*F*pr)/(r*r*F),(0,1):-s.diff(F,t)/(r*F),(2,2):r*r*angular}
    checks={f'G_{a}{b}_formula':s.simplify(Ein[a,b]-v)==0 for (a,b),v in expect.items()}
    mixed=gi*Ein
    for nu in (0,1):
        div=sum(s.diff(mixed[mu,nu],coords[mu])+sum(gamma[mu,mu,lam]*mixed[lam,nu]-gamma[lam,mu,nu]*mixed[mu,lam] for lam in range(4)) for mu in range(4))
        checks[f'Bianchi_mixed_{nu}']=s.simplify(div)==0
    result={'coordinate_time':'x0=c*t (metres)','metric':'diag(-A(x0,r),1/F(x0,r),r^2,r^2 sin(theta)^2)','Einstein_covariant':{f'G_{a}{b}':str(s.simplify(Ein[a,b])) for a,b in [(0,0),(0,1),(1,1),(2,2)]},'Ricci_scalar':str(scalar),'symbolic_checks':checks,'passed':all(checks.values()),'stress_conversion':'T_ab=c^4/(8 pi G)*G_ab','radial_orthonormal_flux':'T_hat01=-c^4/(8 pi G)*F_x0/(r sqrt(A F))','radial_null_conditions':'epsilon+p_r +/-2*T_hat01 >=0','fixed_F_consequence':'F_x0=0 implies zero radial energy flux in this diagonal ansatz; a spatially dependent changing lapse may change anisotropic pressure without requiring radial flux. Einstein equations alone do not supply an evolution law for that matter.','apparent_horizon_caution':'g^ab dr_a dr_b=F; F=0 at an open minimal throat is not sufficient to assert an event horizon. Closed A=F horizon needs regular coordinates and global extension.','transition_requirements':['Metric smooth in a regular chart, Lorentzian outside the trapped region','A>0,F>0 static observer domain; A=0 cannot be crossed with this static chart','Changing F generically requires radial energy flux and time-dependent anisotropic stresses','A fixed F changes no Misner-Sharp mass and does not by itself transfer energy radially','Distributional jumps require Israel junction stresses and their conservation','Bianchi identity ensures divergence of inferred Einstein stress vanishes, not a microphysical realizability or causal stability theorem','A constitutive sector and initial/boundary conditions must specify hyperbolic, causal evolution; neither superluminality nor a transition is demonstrated'],'ansatz':'General A(x0,r),F(x0,r), with endpoint constraints only: A(t_initial,r)=A_open(r), A(t_final,r)=F(r). No arbitrary interpolation selected.','dynamic_evolution_solved':False}
    save_json('results/10_dynamic_symbolic.json',result)
    if not result['passed']:raise RuntimeError('Symbolic tensor check failed')
    print('Dynamic tensor and two Bianchi components verified',flush=True)

if __name__=='__main__':run()
