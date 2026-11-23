from pathlib import Path
import sys,json,numpy as np
B=Path('/workspace/audit-v0.9.72-full');C=B/'checkout';sys.path.insert(0,str(C));from ogcore import pay,production
from ogcore.depth import DepthConverter
out={}
d=np.arange(0.,2001.,100.);p=np.ones(d.shape,bool);curves={'PHIE':np.full(d.shape,.2),'SW':np.full(d.shape,.3)}
for name,stations,expected in [('vertical',[(0.,0.),(2000.,2000.)],2000.),('inclined',[(0.,0.),(2000.,1000.)],1000.),('shallow_upturn',[(0.,0.),(10000.,10000.),(12000.,9990.)],None),('reversal_between_grid_points',[(0.,0.),(10000.,10000.),(11000.,10100.),(11000.2,10099.9),(12000.,10200.)],None)]:
 top=10000. if name in ('shallow_upturn','reversal_between_grid_points')else 0.;base=top+2000.;axis=d+top;c=DepthConverter(stations,0);s=pay.summarize(axis,p,top,base,curves,{},tvd_of_md=c.tvd_of_md);out[name]={'stations':stations,'zone_MD':[top,base],'expected_TVD_gross':expected,'gross':s.gross,'net':s.net,'ng':s.ratio,'phih':s.phih,'gross_md':s.gross_md,'note':s.tvd_note,'detected_reversal':not pay.tvd_rises_through(top,base,c.tvd_of_md,axis)}
 if expected is not None:assert abs(s.gross-expected)<1e-8 and abs(s.net-expected)<1e-8 and abs(s.phih-.2*expected)<1e-8
c=DepthConverter([(0,0),(1000,1000),(2000,900),(3000,1100)],100);out['inverse']={'md':c.to_md(1050,'TVD'),'expected':2750};assert c.to_md(1050,'TVD')==2750
s=production.summarize([],eur=100000,gross_span=1000);out['eur_no_months']={'eur_per_ft':s.get('eur_per_ft'),'expected':100};assert s.get('eur_per_ft')==100
sensitivity=[]
c=DepthConverter([(0,0),(10000,10000),(12000,9950)],0)
for step in [100.,.25]:
 axis=np.arange(10000.,12000.+step/2,step);ss=pay.summarize(axis,np.ones(axis.shape,bool),10000.,12000.,{'PHIE':np.full(axis.shape,.2)}, {},tvd_of_md=c.tvd_of_md);sensitivity.append({'sample_step_ft':step,'gross':ss.gross,'net':ss.net,'note':ss.tvd_note})
out['same_survey_sampling_sensitivity']=sensitivity
(B/'numerical-reference.json').write_text(json.dumps(out,indent=2,default=str));print(json.dumps(out,indent=2,default=str))
