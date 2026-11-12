import sys,json,numpy as np
from pathlib import Path
R=Path('/workspace/audit-v0.9.39/OandG_Workbench_v0.9.39');sys.path[:0]=[str(R),str(R/'tests')]
from test_petro_canonical_curves import CanonicalCurveTests
from database import ProjectDatabase
from ogcore import curve_store
T=CanonicalCurveTests();T.setUpClass();T.setUp()
try:
 app=T.open_petro();w=app.well;n=w.depth.size
 w.curves['X']=np.full(n,1.0);w.units['X']='v/v';w.descriptions['X']='accepted';app.commit_curves_to_project(['X'])
 app.zones=[{'name':'AUDIT','top':float(w.depth[10]),'base':float(w.depth[20])}]
 app.pay_flags=[{'name':'AUDITPAY','zone':'AUDIT','output':'PAY_FLAG','criteria':[{'curve':'X','op':'>','value':0.5,'percent':False}]}]
 def read():
  db=ProjectDatabase(T.project)
  try:
   rows=[dict(r) for r in db.rows('SELECT a.name,v.value_number FROM zone_values v JOIN zone_attributes a ON a.id=v.attribute_id WHERE v.well_id=? AND a.name LIKE ?', (T.blanco,'AUDITPAY%'))]
   d=curve_store.read(db,T.blanco,'X','calc')
   return {'zones':rows,'canonical_X_first':float(d[1][0]) if d else None}
  finally:db.close()
 app.save_project();before=read()
 app._execute_formula_text('X = X * 0');preview=list(app.preview_names);app.save_project();during=read()
 app.discard_preview();app.save_project();after=read()
 result={'before':before,'previews':preview,'during_preview':during,'after_discard':after};print(json.dumps(result,indent=2));Path('/workspace/audit-v0.9.39/preview-zone-evidence.json').write_text(json.dumps(result,indent=2))
finally:T.doCleanups()
