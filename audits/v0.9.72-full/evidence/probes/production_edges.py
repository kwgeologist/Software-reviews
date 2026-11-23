from pathlib import Path
import sys,json,tempfile,math
B=Path('/workspace/audit-v0.9.72-full');C=B/'checkout';sys.path[:0]=[str(C),str(C/'tests')];import conftest
from ogcore import production as p
from database import ProjectDatabase
history=[{'month':m,'oil':v,'source':'S'}for m,v in [('2019-12',-100.),('2020-01',200.),('2020-02',100.),('2020-03',100.)]];s=p.summarize(history);out={'first_window':{'first_production_month':s.first_month,'expected_first3_oil':400.,'observed_first3_oil':s.get('first3_oil'),'cumulative_all_history':s.get('cum_oil')}}
with tempfile.TemporaryDirectory(prefix='audit-production-')as td:
 db=ProjectDatabase(Path(td)/'p.ogwdb')
 try:
  w=db.add_well('Synthetic','');r=p.import_rows(db,[{'month':'2020-01','oil':'1e999'}],{'month':'month','oil':'oil'},well_id=w,source='S');raw=p.rows(db,w);summary=p.summarize(raw);out['nonfinite_import']={'report':str(r),'problems':r.problems,'stored_oil':raw[0]['oil'],'cumulative_oil':summary.get('cum_oil'),'isfinite':math.isfinite(summary.get('cum_oil'))}
 finally:db.close()
(B/'production-edge-results.json').write_text(json.dumps(out,indent=2,default=str));print(json.dumps(out,indent=2,default=str))
