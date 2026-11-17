import sys,json,numpy as np
from pathlib import Path
R=Path('/workspace/audit-v0.9.53/OandG_Workbench_v0.9.53');sys.path[:0]=[str(R),str(R/'tests')]
from test_petro_canonical_curves import CanonicalCurveTests
from database import ProjectDatabase
from ogcore import pay,curve_store
T=CanonicalCurveTests();T.setUpClass();T.setUp()
try:
 app=T.open_petro();d=np.array([1010.,1011.,1012.]);v=np.ones(3)
 app.well.set_series('X',d,v);app.well.units['X']='v/v';app.commit_curves_to_project(['X'])
 app.zones=[{'name':'REF','top':1010.,'base':1012.}];criteria=[{'curve':'X','op':'>','value':.5}];app.pay_flags=[{'name':'OWN','zone':'REF','output':'PAY_FLAG','criteria':criteria}];app.save_project()
 db=ProjectDatabase(T.project)
 try:
  stored=curve_store.resolve(db,T.blanco,'X',source='calc',aliases={});sd,sv=curve_store.arrays(db,stored);rows={r[0]:r[1] for r in db.rows('SELECT a.name,v.value_number FROM zone_values v JOIN zone_attributes a ON a.id=v.attribute_id WHERE v.well_id=? AND a.name LIKE ?', (T.blanco,'OWN%'))}
 finally:db.close()
 inside=pay.zone_samples(d,1010,1012);mask=pay.pay_mask({'X':v},{'X':'v/v'},criteria,inside);reference=pay.summarize(d,mask,1010,1012,{'X':v},{'X':'v/v'},criteria)
 out={'actual_accepted_axis':sd.tolist(),'accepted_values':sv.tolist(),'published':rows,'own_axis_reference_net':reference.net,'analytical_constant_pay_interval':2.0,'zone_refusals':app.last_zone_refusals,'previews':list(app.preview_names)}
 Path('/workspace/audit-v0.9.53/own-axis-pay-evidence.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
finally:T.doCleanups()
