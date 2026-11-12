import sys,json,tempfile
from pathlib import Path
R=Path('/workspace/audit-v0.9.39/OandG_Workbench_v0.9.39');sys.path[:0]=[str(R),str(R/'tests')]
from database import ProjectDatabase
from ogcore import project as P
from ogmap import grids
from test_project_assets import a_grid
with tempfile.TemporaryDirectory() as td:
 p=P.Project.create(Path(td),'Audit');db=ProjectDatabase(p.database_path)
 folder=p.paths.ensure('grids');target=folder/'Imported.ogwgrid';grids.write_file(a_grid('Imported',value=9000),target);before=target.read_bytes()
 new=a_grid('Imported',value=1000);gid=grids.save(db,new)
 result={'preexisting_unlisted_first':9000,'new_grid_file':new.file.name,'old_bytes_preserved':target.read_bytes()==before,'file_first_after_save':float(grids.read_file(target).surface.values[0,0]),'registered_rows':len(grids.list_grids(db))};print(json.dumps(result,indent=2));Path('/workspace/audit-v0.9.39/grid-unlisted-evidence.json').write_text(json.dumps(result,indent=2));db.close()
