import sys,json,numpy as np
from pathlib import Path
R=Path('/workspace/audit-v0.9.53/OandG_Workbench_v0.9.53');sys.path[:0]=[str(R),str(R/'tests')]
from test_petro_canonical_curves import CanonicalCurveTests
from database import ProjectDatabase
from ogcore import curve_store
T=CanonicalCurveTests();T.setUpClass();T.setUp()
try:
 app=T.open_petro();w=app.well;n=w.depth.size
 w.curves['X']=np.ones(n);w.units['X']='v/v';app.commit_curves_to_project(['X'])
 app.zones=[{'name':'LATE_ZONE','top':1010.,'base':1012.}]
 app.pay_flags=[{'name':'LATE_PAY','zone':'LATE_ZONE','output':'PAY_FLAG','criteria':[{'curve':'X','op':'>','value':.5}]}]
 app.save_project();actual=app.geo_db.save_petro_state;injected=[]
 def interleave(*args,**kwargs):
  if not injected:
   injected.append(True);db=ProjectDatabase(T.project)
   try:curve_store.create_curve(db,T.blanco,'X',w.depth,np.zeros(n),unit='v/v',description='new accepted zero curve')
   finally:db.close()
  return actual(*args,**kwargs)
 app.geo_db.save_petro_state=interleave;app._report_curve_conflicts=lambda *a:None
 app.save_project()
 def read():
  db=ProjectDatabase(T.project)
  try:
   r=curve_store.resolve(db,T.blanco,'X',source='calc',aliases={});d,v=curve_store.arrays(db,r)
   return {'accepted_X_all_zero':bool(np.all(v==0)),'accepted_description':r.description,'net':db.row('SELECT v.value_number FROM zone_values v JOIN zone_attributes a ON a.id=v.attribute_id WHERE v.well_id=? AND a.name=?',(T.blanco,'LATE_PAY net'))[0]}
  finally:db.close()
 stale=read();app.geo_db.save_petro_state=actual;app.save_project();refreshed=read()
 out={'late_edit_after_reconcile':stale,'next_save':refreshed,'unaccepted_previews':list(app.preview_names),'expected_net_for_zero_curve':0};Path('/workspace/audit-v0.9.53/late-curve-publication-evidence.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
finally:T.doCleanups()
