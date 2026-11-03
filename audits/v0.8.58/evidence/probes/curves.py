import sys,json,tempfile
from pathlib import Path
import numpy as np
ROOT=Path('/workspace/audit-v0.8.58/OandG_Workbench_v0.8.58');sys.path[:0]=[str(ROOT),str(ROOT/'tests')]
from database import ProjectDatabase
from ogcore import curve_store as cs
from test_curve_store import write_las
out={}
with tempfile.TemporaryDirectory() as t:
 p=Path(t);db=ProjectDatabase(p/'p.ogwdb');w=db.add_well('A');las=write_las(p/'a.las',np.array([100.,101.,102.]),{'GR':np.array([1.,2.,3.]),'RT':np.array([4.,5.,6.])});lid=db.load_las_file(w,las)
 cached=cs.run(db,lid);record=cs.resolve(db,w,'GR');cs.delete_curve(db,record)
 out['delete_run_cache']={'canonical_resolve_missing':cs.resolve(db,w,'GR') is None,'cached_run_curves':list(cs.run(db,lid).curves),'fresh_database_run_curves':list(db.las_run(lid).curves)}
 rt=cs.resolve(db,w,'RT');first=cs.arrays(db,rt)[0].copy();db.update_well(w,{'elevation_units':'m'});second=cs.read(db,w,'RT')[0].copy();cs.forget(db);third=cs.read(db,w,'RT')[0].copy()
 out['well_unit_cache']={'before_ft':first.tolist(),'cached_after_m':second.tolist(),'fresh_after_m':third.tolist()}
 a=cs.create_curve(db,w,'A',[1.,2.,3.],[10.,20.,30.]);b=cs.derive_curve(db,a,'B')
 out['stable_identity']={'parent_original_id':a.id,'parent_id_after_derive':cs.resolve(db,w,'A').id,'original_id_still_exists':cs.get(db,a.id) is not None,'child_parents':cs.provenance(db,b).get('parents')}
 db.close()
Path('/workspace/audit-v0.8.58/curves-evidence.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
