import sys,tempfile,json
from pathlib import Path
sys.path.insert(0,'/workspace/audit-v0.8.58/OandG_Workbench_v0.8.58')
from database import ProjectDatabase
from ogcore import repositories as R
with tempfile.TemporaryDirectory() as t:
 p=Path(t);outside=p/'outside.txt';outside.write_text('synthetic fixture only');db=ProjectDatabase(p/'p.ogwdb');ref='@repository/TEST/'+str(outside)
 res=R.resolve_stored(ref,config={});actual=db.resolve_path(ref)
 out={'reference':ref,'resolver_status':res.status,'resolver_path':str(res.path),'database_resolved_path':str(actual),'outside_file_accessible':actual.exists() and actual.read_text()=='synthetic fixture only'}
 db.close()
Path('/workspace/audit-v0.8.58/repository-evidence.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
