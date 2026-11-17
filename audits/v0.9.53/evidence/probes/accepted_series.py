import sys,json,numpy as np
from pathlib import Path
R=Path('/workspace/audit-v0.9.53/OandG_Workbench_v0.9.53');sys.path[:0]=[str(R),str(R/'tests')]
from test_petro_canonical_curves import CanonicalCurveTests
from database import ProjectDatabase
from ogcore import curve_store
T=CanonicalCurveTests();T.setUpClass();T.setUp()
try:
 app=T.own_axis_curve();w=app.well;app._execute_formula_text('OWN = OWN * 0')
 depth=T.OWN_DEPTH+0.25;values=T.OWN_VALUES+10
 db=ProjectDatabase(T.project);curve_store.create_curve(db,T.blanco,'OWN',depth,values,unit='%',description='new accepted description');db.close()
 app.save_project()
 def read():
  db=ProjectDatabase(T.project)
  try:
   r=curve_store.resolve(db,T.blanco,'OWN',source='calc',aliases={})
   if r is None:return None
   d,v=curve_store.arrays(db,r);return {'axis':d.tolist(),'axis_unit':r.depth_unit,'values':v.tolist(),'curve_unit':r.unit,'description':r.description}
  finally:db.close()
 during=read();assert during['axis']==depth.tolist() and during['values']==values.tolist() and during['curve_unit']=='%' and during['description']=='new accepted description'
 app.discard_preview();app.save_project();after=read();assert after==during
 app._keep_before_preview('OWN');app.well.curves['OWN']=np.zeros(app.well.depth.size);app.preview_names=['OWN']
 db=ProjectDatabase(T.project);curve_store.delete_curve(db,curve_store.resolve(db,T.blanco,'OWN',source='calc',aliases={}));db.close()
 app.save_project();app.discard_preview();app.save_project();deleted=read();assert deleted is None
 out={'external_full_series_preserved_during_preview':during,'after_discard':after,'after_external_delete_save_discard_save':deleted,'status':'passed'};print(json.dumps(out,indent=2));Path('/workspace/audit-v0.9.53/accepted-series-evidence.json').write_text(json.dumps(out,indent=2))
finally:T.doCleanups()
