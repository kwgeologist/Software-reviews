import sys,json,tempfile,os
from pathlib import Path
import numpy as np
R=Path('/workspace/audit-v0.9.18/OandG_Workbench_v0.9.18');B=R.parent;sys.path[:0]=[str(R),str(R/'tests')]
from test_petro_integration import PetroIntegrationTests
from ogcore import curve_store as C
from petroworkbench.well_data import exact_view
out={'exact_view_relative_tolerance':{'source_depth':[5000.003],'target_depth':[5000.],'mapped_values':exact_view([5000.003],[123.],[5000.]).tolist()}}
case=PetroIntegrationTests('runTest');case.setUpClass();case.setUp()
try:
 app=case.open_petro();key=app.active_well_key;d=app.well.depth[20:25].copy();v=np.arange(5,dtype=float)+10.;app.well.set_series('OWN',d,v);app.well.units['OWN']='v/v';app._store_active_workspace();app._save_geo_workspace(key)
 rec=C.resolve(app.geo_db,case.blanco,'OWN');before=C.arrays(app.geo_db,rec)[0].copy();out['own_depth_before']=before.tolist();app._execute_formula_text('OWN = OWN * 2');app._store_active_workspace();app._save_geo_workspace(key);C.forget(app.geo_db);during=C.read(app.geo_db,case.blanco,'OWN')[0].copy();app.discard_preview();app._store_active_workspace();app._save_geo_workspace(key);C.forget(app.geo_db);after=C.read(app.geo_db,case.blanco,'OWN')[0].copy();out['preview_save']={'reference_samples':len(app.well.depth),'own_samples_before':len(before),'stored_samples_during_preview':len(during),'stored_samples_after_discard':len(after),'has_own_series_after_discard':app.well.has_own_depth('OWN'),'axis_preserved_after_discard':bool(np.array_equal(before,after))}
finally:case.tearDown()
(B/'petro-preview-evidence.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
