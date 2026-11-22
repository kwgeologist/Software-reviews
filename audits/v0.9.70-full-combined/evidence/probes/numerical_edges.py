from pathlib import Path
import sys,json
import numpy as np
B=Path('/workspace/audit-v0.9.70-full');C=Path('/workspace/audit-v0.9.70-integrity/checkout');sys.path[:0]=[str(C),str(C/'tests')]
from ogcore.depth import DepthConverter
from ogcore import pay,production
from geosteering.model import Trajectory
out={}
c=DepthConverter([(0,0),(1000,1000),(2000,900),(3000,1100)],100)
md=c.to_md(1050,'TVD');back=c.from_md(md,'TVD');out['nonmonotonic_inverse']={'survey':c.survey,'requested_TVD':1050,'returned_MD':md,'forward_TVD_at_returned_MD':back,'correct_unique_crossing_MD':2750.};assert md==2000 and back==900
# Only the last segment reaches1050, so ambiguity of multiple roots does not explain this wrong inverse.
t=Trajectory.from_positions([0,1000,2000,3000],[0,1000,900,1100],[0,0,995,1975],[0,0,0,0]);out['geosteering_inverse_for_comparison']={'first_crossing_MD':t.md_at_tvd(1050)};assert abs(t.md_at_tvd(1050)-2750)<1e-6
axis=np.arange(1000.,3001.,250.);allpay=np.ones(axis.shape,bool);s=pay.summarize(axis,allpay,1000,3000,{'PHIE':np.full(axis.shape,.2),'SW':np.full(axis.shape,.3)},{},tvd_of_md=c.tvd_of_md)
out['pay_nonmonotonic']={'gross_TVD':s.gross,'net_TVD_all_samples_pay':s.net,'net_gross_ratio':s.ratio,'gross_MD':s.gross_md,'net_MD':s.net_md};assert s.gross==100 and s.net>s.gross and s.ratio>1
s=production.summarize([],eur=100000,gross_span=1000);out['eur_without_months']={'eur':s.get('eur'),'gross_span':s.get('gross_span'),'eur_per_ft':s.get('eur_per_ft'),'expected':100.};assert s.get('eur_per_ft')is None
# Pure numeric reference checks, not client production/geological observations.
s=production.summarize([{'month':'2020-01','source':'S','oil':100.,'gas':600.,'water':50.}],eur=100000,gross_span=1000)
out['production_reference']={'cum_boe':s.get('cum_boe'),'gor':s.get('gor'),'water_cut':s.get('water_cut'),'eur_per_ft':s.get('eur_per_ft')};assert s.get('cum_boe')==200 and s.get('gor')==6000 and s.get('eur_per_ft')==100
(B/'numerical-edges.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
