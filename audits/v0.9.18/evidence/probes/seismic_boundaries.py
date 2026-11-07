import sys,tempfile,json,types
from pathlib import Path
import numpy as np
from pyproj import Transformer
R=Path('/workspace/audit-v0.9.18/OandG_Workbench_v0.9.18');B=R.parent;sys.path[:0]=[str(R),str(R/'tests')]
from database import ProjectDatabase
from seismicworkbench.lines2d import Lines2D
from seismicworkbench.interp_registry import Registry
from seismicworkbench.section2d import Section2DView
from seismicworkbench.ties_ui import TiesMixin
from seismicworkbench.project import SeismicStore
from seismicworkbench.interpretation import Interpretation
from ogcore import seis_ties
out={}
with tempfile.TemporaryDirectory()as t:
 p=Path(t);db=ProjectDatabase(p/'p.ogwdb');lines=Lines2D(db);pts=[{'value':i+1,'x':500000.+i*100,'y':4400000.}for i in range(3)];lines.add_control_line('L',pts,{'kind':'manual'},'EPSG:32613','trace');reg=Registry(db);reg.save_line_picks('L','Horizon','H',np.array([100.,np.nan,200.]));other=ProjectDatabase(p/'p.ogwdb')
 def view(d):
  v=object.__new__(Section2DView);v.registry=Registry(d);v.name='L';v.n=3;v.line_id=Lines2D(d).row('L')['id'];v.mistie=__import__('seismicworkbench.mistie',fromlist=['MistieStore']).MistieStore(d);v.undo_stack=[];v.anchor={};v._snap=lambda k,z:z;v.changed=lambda:None;v.reload_picks();return v
 a,b=view(db),view(other);a.pick_horizon('H',0,110.);b.pick_horizon('H',2,220.);out['two_session_2d']={'first_writer_expected_trace0':110.,'second_writer_expected_trace2':220.,'stored':reg.line_picks('L',3)[('Horizon','H')].tolist()};other.close()
 # Same physical crossing, two explicitly declared coordinate systems.
 lines.add_control_line('UTM',[{'value':1,'x':500000.,'y':4399900.},{'value':2,'x':500000.,'y':4400100.}],{'kind':'manual'},'EPSG:32613','trace');tr=Transformer.from_crs(32613,4326,always_xy=True);ll=[tr.transform(x,4400000.)for x in [499900.,500100.]];lines.add_control_line('Geographic',[{'value':i+1,'x':x,'y':y}for i,(x,y)in enumerate(ll)],{'kind':'manual'},'EPSG:4326','trace')
 class App(TiesMixin):pass
 app=App();app.lines2d=lines;app.sections=[];app.footprints=lambda:[];app.survey=None
 result=app.ties_of_line('UTM');out['mixed_crs_tie']={'actual_UTM_to_Geographic_ties':len([x for x in result if x.get('other')=='Geographic']),'expected_after_transform':len(seis_ties.polyline_intersections([500000,500000],[4399900,4400100],[499900,500100],[4400000,4400000])),'stored_crs':[lines.row(n)['crs']for n in ['UTM','Geographic']]}
 # Deleted-object saves are not included in the 3-D stale-write check.
 sid=db.execute("INSERT INTO seismic_surveys(name,file_path,domain,units)VALUES('S','s.sgy','time','ms')");store=SeismicStore(db);it=Interpretation((2,2));it.set_horizon_pick('H3',0,0,100.);store.save_interpretation(sid,it,{},{});old,st,vis=store.load_interpretation(sid,(2,2));new,st2,vis2=store.load_interpretation(sid,(2,2));new.set_horizon_pick('H3',1,1,250.);store.save_interpretation(sid,new,st2,vis2);old.horizons.pop('H3');old.deleted.add(('Horizon','H3'))
 try:store.save_interpretation(sid,old,st,vis);out['stale_delete_3d']={'conflict':False,'remaining_rows':db.row('SELECT COUNT(*) FROM seismic_horizons WHERE survey_id=? AND name=?',(sid,'H3'))[0]}
 except Exception as e:out['stale_delete_3d']={'conflict':True,'exception':type(e).__name__}
 db.close()
(B/'seismic-boundaries-evidence.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
