import sys,json
from pathlib import Path
R=Path('/workspace/audit-v0.9.53/OandG_Workbench_v0.9.53');sys.path[:0]=[str(R),str(R/'tests')]
from test_v0941_fixes import GridFileAfterCommit
from database import ProjectDatabase
from ogmap import grids
out={}
for mode in ['before','after']:
 T=GridFileAfterCommit();T.setUp()
 try:
  T.killed(mode);db=ProjectDatabase(T.project.database_path)
  try:
   before=[x.name for x in T.live.parent.iterdir()];g=grids.load(db,T.gid);out[mode]={'files_before_load':before,'row_updated_at':db.row('SELECT updated_at FROM map_grids WHERE id=?',(T.gid,))[0],'file_updated_at':g.updated_at,'value_first':float(g.surface.values[0,0]),'notes':g.notes,'old_bytes_preserved':T.live.read_bytes()==T.before_bytes};assert out[mode]['row_updated_at']==out[mode]['file_updated_at']
  finally:db.close()
 finally:T.doCleanups()
Path('/workspace/audit-v0.9.53/grid-commit-recovery-evidence.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
