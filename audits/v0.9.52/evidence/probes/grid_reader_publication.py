import sys,json,tempfile
from pathlib import Path
from unittest.mock import patch
R=Path('/workspace/audit-v0.9.52/OandG_Workbench_v0.9.52');sys.path[:0]=[str(R),str(R/'tests')]
from database import ProjectDatabase
from ogcore import project as P,safeio
from ogmap import grids
from test_project_assets import a_grid
with tempfile.TemporaryDirectory() as td:
 p=P.Project.create(Path(td),'Race');a=ProjectDatabase(p.database_path);b=ProjectDatabase(p.database_path)
 g=a_grid();g.surface.values[:]=1000;g.unit='ft';gid=grids.save(a,g);g=grids.load(a,gid);g.surface.values[:]=9000;g.unit='m';g.notes='new accepted interpretation'
 real=safeio.Publication.promote;seen=[]
 def reader_then_promote(self):
  if not seen:
   r=grids.load(b,gid);seen.append({'value':float(r.surface.values[0,0]),'unit':r.unit})
  return real(self)
 try:
  with patch.object(safeio.Publication,'promote',reader_then_promote):grids.save(a,g)
  error=None
 except Exception as e:error=type(e).__name__+': '+str(e)
 row=dict(b.row('SELECT id,unit,updated_at,file_path FROM map_grids WHERE id=?',(gid,)));r=grids.load(b,gid)
 out={'reader_after_commit':seen,'save_error':error,'reopened_row':row,'reopened_grid':{'value':float(r.surface.values[0,0]),'unit':r.unit,'notes':r.notes}}
 Path('/workspace/audit-v0.9.52/grid-reader-publication-evidence.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2));a.close();b.close()
