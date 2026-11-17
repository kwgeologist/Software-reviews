import sys,json,hashlib
from pathlib import Path
from unittest.mock import patch
B=Path('/workspace/audit-v0.9.53');R=B/'OandG_Workbench_v0.9.53';sys.path[:0]=[str(R),str(R/'tests')]
from test_v0952_fixes import GridTopNames
from database import ProjectDatabase
from ogmap import grids
from ogcore import safeio
x=GridTopNames();x.setUp()
try:
 before={gid:x.snapshot(gid) for gid in (x.top,x.iso)}
 with patch.object(safeio.Publication,'promote',side_effect=PermissionError('audit injected locked target')):
  x.db.rename_top_definition(x.db.top_definition('Gallup')[0],'Gallup Sandstone')
 out={'source_after_locked_rename':{str(g):x.source_of(g) for g in before},'content_unchanged':{str(g):x.snapshot(g)[0:3]==before[g][0:3] for g in before}}
 x.db.close();x.db=ProjectDatabase(x.project.database_path)
 out['source_after_reopen']={str(g):x.source_of(g) for g in before}
 (B/'locked-grid-source-evidence.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
finally:x.doCleanups()
