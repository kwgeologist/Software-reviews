from pathlib import Path
import sys,json,tempfile
B=Path('/workspace/audit-v0.9.53');R=B/'OandG_Workbench_v0.9.53';sys.path[:0]=[str(R),str(R/'tests')]
from database import ProjectDatabase
from ogcore import project as P
from ogmap import grids
from test_project_assets import a_grid
with tempfile.TemporaryDirectory() as td:
 p=P.Project.create(Path(td),'Alias cache');db=ProjectDatabase(p.database_path);db.set_project_value('coordinate_system','EPSG:2231');w=db.add_well('W','0512300001');db.execute('INSERT INTO locations(well_id,surface_x,surface_y) VALUES (?,?,?)',(w,3000000,4800000));db.set_formation_top(w,'A',100,source='XON');db.set_formation_top(w,'B',1000,source='XON');a=db.top_definition('A')[0];b=db.top_definition('B')[0];db.add_top_alias(a,'Legacy');g=a_grid();g.source={'kind':'top','formation':'Legacy','measure':'MD'};g.unit='ft';g.excluded=[]
 def fresh():return grids.gather(db,g)
 first=grids.kept_points(db,g,None,fresh).value.tolist();before=db.change_revisions();db.remove_top_alias('Legacy');db.add_top_alias(b,'Legacy');after=db.change_revisions();actual=fresh().value.tolist();cached=grids.kept_points(db,g,None,fresh).value.tolist();db.close();db=ProjectDatabase(p.database_path);reopened=grids.kept_points(db,g,None,lambda:grids.gather(db,g)).value.tolist();db.close()
 out={'before_alias_change':first,'fresh_after_explicit_reassignment':actual,'cached_after_explicit_reassignment':cached,'cached_after_project_reopen':reopened,'revisions_before':before,'revisions_after':after};(B/'alias-cache-evidence.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
