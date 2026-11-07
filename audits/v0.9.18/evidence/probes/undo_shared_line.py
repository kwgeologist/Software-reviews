import sys,tempfile,json
from pathlib import Path
import numpy as np
R=Path('/workspace/audit-v0.9.18/OandG_Workbench_v0.9.18');B=R.parent;sys.path.insert(0,str(R))
from database import ProjectDatabase
from seismicworkbench.lines2d import Lines2D
from seismicworkbench.interp_registry import Registry
from seismicworkbench.section2d import Section2DView
from seismicworkbench.ties_ui import TiesMixin
from seismicworkbench.mistie import MistieStore
class App(TiesMixin):pass
out={}
with tempfile.TemporaryDirectory()as t:
 db=ProjectDatabase(Path(t)/'p.ogwdb');lines=Lines2D(db);lines.add_control_line('L',[{'value':i+1,'x':i*100.,'y':0.}for i in range(3)],{'kind':'manual'},'EPSG:32613','trace');reg=Registry(db);reg.save_line_picks('L','Horizon','H',np.array([100.,np.nan,200.]));app=App();app._sections2d=[];app.refresh_tree=lambda:None
 for _ in range(2):
  v=object.__new__(Section2DView);v.registry=reg;v.name='L';v.n=3;v.line_id=lines.row('L')['id'];v.mistie=MistieStore(db);v.undo_stack=[];v.anchor={};v._snap=lambda k,z:z;v.refresh_interpretation=lambda:None;v.app=app;v.reload_picks();app.sections2d.append(v)
 a,b=app.sections2d;a.pick_horizon('H',0,110.);b.pick_horizon('H',2,220.);out['after_two_edits']=reg.line_picks('L',3)[('Horizon','H')].tolist();a.undo();out['after_undo_in_first_view']=reg.line_picks('L',3)[('Horizon','H')].tolist();out['expected_revert_first_keep_second']=[100.,None,220.];db.close()
(B/'undo-shared-line-evidence.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
