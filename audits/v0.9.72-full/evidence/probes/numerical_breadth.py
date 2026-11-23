from pathlib import Path
import sys,json,math,numpy as np
B=Path('/workspace/audit-v0.9.72-full');sys.path.insert(0,str(B/'checkout'))
from ogcore import depth,pay,water,formulas,production,velocity_model,gridders
from ogcore.surface import Surface
from ogvol import engine as v
checks=[]
def check(name,actual,expected):
 np.testing.assert_allclose(actual,expected,rtol=1e-9,atol=1e-8);checks.append({'name':name,'actual':np.asarray(actual).tolist(),'expected':np.asarray(expected).tolist(),'passed':True})
check('MD to TVD linear segment',depth.linear_interpolate([(0,0),(1000,800)],500),400)
check('TVDSS sign convention',depth.subsea_from_tvd(5000,1000),-4000)
check('TVD unique crossing',depth.md_at_tvd([(0,0),(1000,1000),(2000,900),(3000,1100)],1050),2750)
check('Arps Rw temperature',water.arps(.1,75,150),.1*(75+6.77)/(150+6.77))
check('Archie saturation reference',formulas.evaluate('((RW)/(RT*PHI**2))**0.5',{'RW':.1,'RT':10.,'PHI':.2}),.5)
check('Temperature gradient per 100ft',water.formation_temperature([0,1000],70,1.4),[70,84])
check('TWT milliseconds to feet',velocity_model.depth_below_datum(10000,2000,'ms','ft/s','ft'),10000)
check('TWT seconds to metres',velocity_model.depth_below_datum(10000,2,'s','ft/s','m'),3048)
case=v.Case(mode='manual',area=100.,area_unit='acres',rf=.2,inputs={'net_pay':v.Input('constant',value=10.,unit='ft'),'porosity':v.Input('constant',value=20.,unit='%'),'sw':v.Input('constant',value=30.,unit='%'),'bo':v.Input('constant',value=1.25)})
r=v.compute(case);expected=7758*100*10*.2*.7/1.25;check('Manual OOIP',r.totals.in_place,expected);check('Recoverable oil',r.totals.recoverable,.2*expected)
case.inputs['net_pay']=v.Input('grid',surface=Surface.regular(0,0,100,100,np.full((3,3),10.)),unit='ft');case.mode='grid';r=v.compute(case);check('Grid cell-count area',r.totals.area_acres,4*10000/43560);check('Grid net acre feet',r.totals.net_af,4*10000/43560*10)
surface=Surface.regular(100,200,10,20,np.array([[1.,3.],[5.,7.]]));check('Bilinear grid sample',surface.sample(np.array([105.]),np.array([210.])),[4.])
d=np.array([0.,5.,10.]);s=pay.summarize(d,np.ones(3,bool),0,10,{'PHIE':np.full(3,.2),'SW':np.full(3,.3)},{});check('Pay gross/net/NG', [s.gross,s.net,s.ratio],[10,10,1]);check('PhiH/HCPV',[s.phih,s.hcpt],[2,1.4])
p=production.summarize([{'month':'2020-01','source':'S','oil':100.,'gas':600.,'water':50.}]);check('Production BOE, GOR and water cut',[p.get('cum_boe'),p.get('gor'),p.get('water_cut')],[200,6000,1/3])
stations=[{'md':0.,'inc':0.,'azi':0.},{'md':1000.,'inc':0.,'azi':0.},{'md':2000.,'inc':90.,'azi':0.}]
depth.minimum_curvature(stations);curved_leg=2000/math.pi;check('Minimum curvature circular quarter-turn',[stations[-1]['tvd'],stations[-1]['ns'],stations[-1]['ew']],[1000+curved_leg,curved_leg,0])
u=np.array([0.,0.,10.,10.]);vv=np.array([0.,10.,0.,10.]);zz=1+2*u+3*vv;g=gridders.grid_values(u,vv,zz,(11,11),gridders.Options(method='trend',scope='global'));yy,xx=np.indices((11,11));check('Planar trend gridding',g,1+2*xx+3*yy)
(B/'numerical-breadth.json').write_text(json.dumps({'synthetic_reference_checks':checks,'count':len(checks),'real_production_used':False},indent=2));print(json.dumps({'checks_passed':len(checks)},indent=2))
