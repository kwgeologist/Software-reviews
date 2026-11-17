import sys,json,tempfile,threading,time
from pathlib import Path
from unittest.mock import patch
R=Path('/workspace/audit-v0.9.53/OandG_Workbench_v0.9.53');sys.path[:0]=[str(R),str(R/'tests')]
from database import ProjectDatabase
from ogcore import project as P
from ogmap import grids
from test_project_assets import a_grid
with tempfile.TemporaryDirectory() as td:
 p=P.Project.create(Path(td),'Create');db=ProjectDatabase(p.database_path);db.close();one=threading.Event();two=threading.Event();writing=threading.Event();ids={};errors=[];real=grids.write_file
 def write(g,path):
  r=real(g,path)
  if threading.current_thread().name=='A':writing.set();time.sleep(.3)
  return r
 def worker(label,value):
  db=None
  try:
   if label=='B':one.wait(10)
   db=ProjectDatabase(p.database_path)
   if label=='A':one.set();two.wait(10)
   else:two.set();writing.wait(10)
   g=a_grid();g.name='Same';g.surface.values[:]=value;ids[label]=grids.save(db,g)
  except Exception as e:errors.append(type(e).__name__+': '+str(e));one.set();two.set();writing.set()
  finally:
   if db:db.close()
 with patch.object(grids,'write_file',write):
  threads=[threading.Thread(target=worker,args=(l,v),name=l) for l,v in [('A',1000),('B',9000)]]
  for t in threads:t.start()
  for t in threads:t.join(20)
 db=ProjectDatabase(p.database_path);loaded={l:grids.load(db,i) for l,i in ids.items()};out={'errors':errors,'grids':{l:{'id':g.id,'name':g.name,'file':g.file.name,'value':float(g.surface.values[0,0])} for l,g in loaded.items()}};db.close();assert not errors and len(loaded)==2 and loaded['A'].file!=loaded['B'].file
 Path('/workspace/audit-v0.9.53/grid-creation-evidence.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
