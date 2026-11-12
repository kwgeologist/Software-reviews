import sys,tempfile,json
from pathlib import Path
from types import SimpleNamespace,MethodType
from unittest.mock import patch
R=Path('/workspace/audit-v0.9.39/OandG_Workbench_v0.9.39');sys.path[:0]=[str(R),str(R/'tests')]
from database import ProjectDatabase
from ogcore import project as P
from ogmap import georef
from ogmap.window import MapWindow
from test_map_images import make_image
with tempfile.TemporaryDirectory() as td:
 p=P.Project.create(Path(td),'Audit');a=ProjectDatabase(p.database_path);b=ProjectDatabase(p.database_path)
 image=georef.import_image(a,make_image(Path(td)/'plat.png'),'Plat');held={image.id:georef.load_image(a,image.id)}
 app=SimpleNamespace(db=a,image_layers=lambda:held,_data_signature=lambda:None,_show_images=lambda:None,_fill_stack=lambda:None)
 for name in ('save_image_layer','set_image_opacity'):setattr(app,name,MethodType(getattr(MapWindow,name),app))
 def meanwhile(*args,**kwargs):
  newer=georef.load_image(b,image.id);newer.points=[georef.ControlPoint(0,0,500000,4200000),georef.ControlPoint(200,0,502000,4200000),georef.ControlPoint(0,100,500000,4199000)];newer.solve();georef.save(b,newer);return 50
 with patch('ogmap.window.simpledialog.askinteger',side_effect=meanwhile):MapWindow.ask_image_opacity(app,image.id)
 latest=georef.load_image(b,image.id);result={'other_session_registered':True,'stored_registered_after_opacity':latest.registered,'stored_opacity':latest.opacity,'stored_points':len(latest.points)};print(json.dumps(result,indent=2));Path('/workspace/audit-v0.9.39/image-opacity-evidence.json').write_text(json.dumps(result,indent=2));a.close();b.close()
