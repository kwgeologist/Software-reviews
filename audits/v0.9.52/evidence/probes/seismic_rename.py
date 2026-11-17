import sys,json,tempfile
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch
R=Path('/workspace/audit-v0.9.52/OandG_Workbench_v0.9.52');sys.path[:0]=[str(R),str(R/'tests')]
from database import ProjectDatabase
from ogcore import project as P
from ogmap import grids
from test_project_assets import a_grid
from seismicworkbench.grids_ui import GridsMixin
with tempfile.TemporaryDirectory() as td:
 p=P.Project.create(Path(td),'Audit');a=ProjectDatabase(p.database_path);b=ProjectDatabase(p.database_path)
 gid=grids.save(a,a_grid());old=grids.load(a,gid).surface.values.copy()
 def while_dialog(*args,**kw):
  latest=grids.load(b,gid);latest.surface.values+=500;latest.notes='new interpretation';latest.unit='m';grids.save(b,latest);return 'Renamed in Seismic'
 app=SimpleNamespace(db=a,_grids_changed=lambda *a:None)
 with patch('seismicworkbench.grids_ui.simpledialog.askstring',side_effect=while_dialog):GridsMixin.rename_project_grid(app,gid)
 latest=grids.load(b,gid);result={'initial_first':float(old[0,0]),'other_session_expected_first':float(old[0,0]+500),'stored_first':float(latest.surface.values[0,0]),'stored_unit':latest.unit,'stored_notes':latest.notes,'stored_name':latest.name};print(json.dumps(result,indent=2));Path('/workspace/audit-v0.9.52/seismic-rename-evidence.json').write_text(json.dumps(result,indent=2));a.close();b.close()
