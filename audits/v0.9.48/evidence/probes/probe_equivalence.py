from pathlib import Path
import sys,json,dataclasses,inspect,importlib,tempfile
from unittest.mock import patch
import numpy as np
R=Path(sys.argv[1]);O=Path(sys.argv[2]);sys.path[:0]=[str(R),str(R/'tests'),str(R/'tools/release')]
from cython_modules import PROTECTED
mods={n:importlib.import_module(n) for n in PROTECTED};out={};rng=np.random.default_rng(948)
def norm(v):
 if isinstance(v,np.ma.MaskedArray):return {'data':norm(v.data),'mask':norm(v.mask)}
 if isinstance(v,np.ndarray):return {'shape':v.shape,'dtype':str(v.dtype),'bytes':v.tobytes().hex()}
 if dataclasses.is_dataclass(v):return norm({f.name:getattr(v,f.name) for f in dataclasses.fields(v)})
 if isinstance(v,dict):return {str(k):norm(x) for k,x in v.items()}
 if isinstance(v,(tuple,list)):return [norm(x) for x in v]
 if isinstance(v,(np.number,float)):return {'float64':np.float64(v).tobytes().hex()}
 if isinstance(v,Path):return str(v)
 if v is None or isinstance(v,(str,bool,int)):return v
 return {'class':type(v).__name__}
def case(name,fn):
 try:out[name]={'value':norm(fn())}
 except Exception as e:out[name]={'exception':type(e).__name__,'message':str(e)}
f=mods['ogcore.formulas'];a=np.array([0.,1.,2.,np.nan,-1.]);b=np.array([1.,0.,2.,3.,-1.])
for expr in ['A/B','A*B**2','LOG10(A)+SQRT(B)','A > 1','1/0','A + MISSING']:
 case('formulas:'+expr,lambda e=expr:f.evaluate(e,{**f.HELPERS,'NP':np,'A':a,'B':b}))
w=mods['ogcore.water'];case('water',lambda:[w.arps([.05,.1,np.nan],75,[60,212,300]),w.rw_from_salinity([1000,100000,5000],[75,212,150]),w.formation_temperature([0,10000,np.nan],70,1.4)])
c=mods['ogcore.core_equations'];case('core_equations',lambda:[c.sample_at([0,1,2,4],[0,10,np.nan,40],[-1,0,.5,1,1.5,2,4,5]),c.values_at([{'depth':2,'value':3},{'depth':1,'value':4}],[.98,1.5,2]),c.identifiers('Organic Carbon (TOC)')])
mm=mods['ogcore.multimineral'];m=mm.Model(shale_mode="fixed");vols=[{'calcite':.8,'fluid':.2},{'dolomite':.88,'fluid':.12},{'calcite':.4,'dolomite':.45,'fluid':.15}];logs=[mm.forward(m,v) for v in vols];case('multimineral',lambda:mm.invert(m,{k:np.array([x[k] for x in logs]) for k in mm.MEASUREMENTS}))
mv=mods['ogcore.multivariate'];x=rng.normal(size=40);y=2+3*x+rng.normal(0,.01,40);y[3]=np.nan
case('multivariate_regression',lambda:mv.linear_regression(y,[x],['X']));case('multivariate_kmeans',lambda:mv.kmeans([x,y],['X','Y'],3,seed=948))
p=mods['ogcore.pay'];d=np.cumsum(rng.uniform(.25,1.5,200))+4000;curves={'PHIE':rng.uniform(0,.3,200),'SW':rng.uniform(.1,1,200)};units={'PHIE':'v/v','SW':'v/v'};crit=p.parse_criteria('PHIE > .1\nSW < .6',curves);mask=p.pay_mask(curves,units,crit,p.zone_samples(d,4010,4150));case('pay',lambda:[p.sample_support(d,4010,4150),mask,p.summarize(d,mask,4010,4150,curves,units,crit)])
co=mods['petroworkbench.curve_ops'];case('curve_ops',lambda:[co.smooth_values([0,2,np.nan,8,10],{'method':'Moving Average','strength':'Custom','window':3}),co.smooth_values([1,2,3],{'method':'Moving Average','strength':'Custom','window':3})])
g=mods['ogcore.gridders'];u=np.array([0,0,5,5,2.5]);v=np.array([0,5,0,5,2.5]);z=10+u+2*v
for method in ['Inverse distance','Minimum curvature','Linear triangulation','Polynomial trend']:
 case('gridders:'+method,lambda method=method:g.grid_values(u,v,z,(7,7),g.Options(method=method)))
mc=mods['ogcore.mincurv'];grid=rng.normal(size=(17,23));case('mincurv',lambda:[mc.smooth(grid,2),mc.dct(grid),mc.min_curvature(u,v,z,(7,7))])
gg=mods['ogcore.gridding'];picks=np.full((9,11),np.nan);picks[0,0]=10;picks[0,10]=20;picks[8,0]=30;picks[8,10]=40;picks[4,5]=25;case('gridding',lambda:gg.grid_picks(picks))
vm=mods['ogcore.velocity_model'];case('velocity_model',lambda:[vm.depth_below_datum([10000,3000,np.nan],[1000,2000,1000],'ms','ft/s','m'),vm.average_velocity([5000,0,np.nan],[1000,0,1000],'ms','ft','ft/s')]);case('velocity_bad_unit',lambda:vm.depth_below_datum(10000,1000,'us','ft/s','ft'))
from ogcore.surface import Surface
E=mods['ogvol.engine'];net=Surface.regular(0,0,100,100,np.array([[10,20,30],[20,30,40],[30,40,50]],float));inputs={'net_pay':E.Input('grid',net,unit='ft'),'porosity':E.Input('constant',value=.2,unit='v/v'),'sw':E.Input('constant',value=.3,unit='v/v'),'bo':E.Input('constant',value=1.25)};case('volumetrics',lambda:E.compute(E.Case(inputs=inputs,rf=.2,metres_per_unit=.3048)).totals)
from test_batch_zones import Project
bz=mods['ogcore.batch_zones']
with tempfile.TemporaryDirectory() as td:
 pr=Project(Path(td));definition=pr.definition();wid=pr.wells['A-1'];case('batch_zones',lambda:bz.calculate_well(pr.db,definition,wid,pr.db.formation_tops_for([wid])[wid],'XON',bz.aliases(pr.db)));pr.db.close()
lic=mods['ogcore.licensing']
with patch.object(lic,'state_path',return_value=Path('/tmp/audit-clock-hook')):
 case('licensing_internal_global',lambda:lic.ClockState().path)
# Names and call signatures, ignoring intentionally stripped docstrings.
signatures={}
for name,module in mods.items():
 signatures[name]={}
 for key,value in vars(module).items():
  if not key.startswith('_') and callable(value) and getattr(value,'__module__',None)==name:
   try:signatures[name][key]=str(inspect.signature(value))
   except (ValueError,TypeError):signatures[name][key]='unavailable'
O.write_text(json.dumps({'origins':{k:v.__file__ for k,v in mods.items()},'cases':out,'signatures':signatures},indent=2));print('cases',len(out),'exceptions',[(k,v) for k,v in out.items() if 'exception' in v])
