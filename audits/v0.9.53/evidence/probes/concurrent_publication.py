import sys,json,tempfile
from pathlib import Path
from unittest.mock import patch
B=Path('/workspace/audit-v0.9.53');R=B/'OandG_Workbench_v0.9.53';sys.path[:0]=[str(R),str(R/'tests')]
from database import ProjectDatabase
from ogcore import project as P
from ogmap import grids
from test_project_assets import a_grid
with tempfile.TemporaryDirectory() as td:
 p=P.Project.create(Path(td),'Concurrent');a=ProjectDatabase(p.database_path);b=ProjectDatabase(p.database_path)
 g=a_grid();g.unit='ft';g.surface.values[:]=1000;gid=grids.save(a,g)
 ga=grids.load(a,gid);gb=grids.load(b,gid);ga.unit='m';ga.surface.values[:]=2000;ga.notes='Writer A';gb.unit='ft';gb.surface.values[:]=3000;gb.notes='Writer B'
 real=grids._promote_committed;calls=[]
 def overlap(db,*args):
  if db is a and not calls:
   calls.append('A committed; B saves before A promotes');grids.save(b,gb)
  return real(db,*args)
 with patch.object(grids,'_promote_committed',side_effect=overlap):grids.save(a,ga)
 row=dict(a.row('SELECT id,unit,updated_at,source FROM map_grids WHERE id=?',(gid,)));got=grids.load(b,gid)
 out={'interleaving':calls,'both_saves_returned_success':True,'db_row':row,'loaded_file':{'unit':got.unit,'updated_at':got.updated_at,'value':float(got.surface.values[0,0]),'notes':got.notes},'writer_A_updated_at':ga.updated_at,'writer_B_updated_at':gb.updated_at}
 (B/'concurrent-publication-evidence.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2));a.close();b.close()
