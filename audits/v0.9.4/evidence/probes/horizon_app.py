import sys,json
from pathlib import Path
R=Path('/workspace/audit-v0.9.4/OandG_Workbench_v0.9.4');sys.path[:0]=[str(R),str(R/'tests')]
from test_kingdom_native import AppFlowTests,HERE
app=AppFlowTests().stub();app.import_kingdom_horizons([HERE/'H02503.hzn'],confirm=lambda *a,**k:{'choices':{'origin':'6448/3460','unit':'ft'}});before=len(app.interp.horizons['10300']);report=app.import_kingdom_horizons([HERE/'H02503.hzn'],confirm=lambda *a,**k:{'choices':{'origin':'0/0','unit':'ft','policy':'Replace'}});out={'prior_picks':before,'after_picks':len(app.interp.horizons['10300']),'report':report,'save_calls':app.saved,'status':app.status};(R.parent/'horizon-app-evidence.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
