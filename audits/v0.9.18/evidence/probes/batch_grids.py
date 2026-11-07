import sys,tempfile,json
from pathlib import Path
import numpy as np
R=Path('/workspace/audit-v0.9.18/OandG_Workbench_v0.9.18');B=R.parent;sys.path[:0]=[str(R),str(R/'tests')]
from database import ProjectDatabase
from ogcore import curve_store as C,batch_curves as BC
from test_curve_store import write_las
out={}
with tempfile.TemporaryDirectory()as t:
 p=Path(t);db=ProjectDatabase(p/'p.ogwdb');w=db.add_well('Synthetic');db.load_las_file(w,write_las(p/'a.las',np.array([1000.,1001.,1002.]),{'A':np.array([10.,20.,30.])}));db.load_las_file(w,write_las(p/'b.las',np.array([1000.5,1001.5]),{'B':np.array([100.,200.])}));job=BC.job_for('Custom','OUT = A + B');result=BC.calculate_well(db,job,job.recipe,w,{});d,v,u=C.read(db,w,'OUT');out['offgrid_inputs']={'A_depth':[1000.,1001.,1002.],'B_depth':[1000.5,1001.5],'stored_output_depth':d.tolist(),'stored_output_values':v.tolist(),'engine_report':result}
 C.create_curve(db,w,'OWN',np.array([1000.5,1001.5]),np.array([5.,6.]));rec=C.resolve(db,w,'OWN');out['own_axis_calculated']={'canonical_read_depth':C.arrays(db,rec)[0].tolist()};job=BC.job_for('Custom','COPY = OWN * 2')
 try:out['own_axis_calculated']['batch_result']=BC.calculate_well(db,job,job.recipe,w,{})
 except Exception as e:out['own_axis_calculated']['batch_error']={'type':type(e).__name__,'message':str(e)}
 db.close()
(B/'batch-grids-evidence.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
