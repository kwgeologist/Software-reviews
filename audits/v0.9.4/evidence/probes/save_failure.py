import sys,types,sqlite3,json
from pathlib import Path
R=Path('/workspace/audit-v0.9.4/OandG_Workbench_v0.9.4');sys.path[:0]=[str(R),str(R/'tests')]
from test_kingdom_native import AppFlowTests,HERE
from seismicworkbench.app import SeismicWorkbench
app=AppFlowTests().stub();statuses=[];app.set_status=lambda x:statuses.append(x);app.survey_id=1;app._save_job=None
class Store:
 def save_interpretation(self,*args):raise sqlite3.OperationalError('synthetic disk full')
app.store=Store();app.save_now=types.MethodType(SeismicWorkbench.save_now,app)
result=app.import_kingdom_horizons([HERE/'H02503.hzn'],confirm=lambda *a,**k:{'choices':{'origin':'6448/3460','unit':'ft'}})
out={'result_returned':result,'status_sequence':statuses,'final_status_claims_import':statuses[-1].startswith('Kingdom horizons imported')};(R.parent/'save-failure-evidence.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
