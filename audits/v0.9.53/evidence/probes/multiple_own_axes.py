import sys,json,numpy as np
from pathlib import Path
R=Path('/workspace/audit-v0.9.53/OandG_Workbench_v0.9.53');sys.path[:0]=[str(R),str(R/'tests')]
from test_petro_canonical_curves import CanonicalCurveTests
from database import ProjectDatabase
from ogcore import curve_store
T=CanonicalCurveTests();T.setUpClass();T.setUp()
try:
 app=T.open_petro();d=app.well.depth[:-1]+.25;n=d.size
 x=np.where(np.isclose(np.mod(d-.25,1.),.5),1.,0.)
 for name,values in [('X',x),('PHIE',np.full(n,.2)),('SW',np.full(n,.5))]:app.well.set_series(name,d,values);app.well.units[name]='v/v'
 app.commit_curves_to_project(['X','PHIE','SW']);app.zones=[{'name':'REF','top':1010.25,'base':1012.25}];app.pay_flags=[{'name':'PAY','zone':'REF','output':'PAY_FLAG','criteria':[{'curve':'X','op':'>','value':.5}]}]
 def read():
  db=ProjectDatabase(T.project)
  try:
   rows={r[0]:r[1] for r in db.rows('SELECT a.name,v.value_number FROM zone_values v JOIN zone_attributes a ON a.id=v.attribute_id WHERE v.well_id=? AND a.name LIKE ?', (T.blanco,'PAY%'))};rec=curve_store.resolve(db,T.blanco,'X',source='calc',aliases={});dd,v=curve_store.arrays(db,rec)
   return rows,dd.copy(),v.copy()
  finally:db.close()
 app.save_project();before,bd,bv=read()
 panel=app.open_curve_editor_resample('PHIE',(1.,.25));panel.output_mode.set('overwrite');assert panel.preview(quiet=True) is not None;assert panel.accept()=='PHIE';app.save_project();after,ad,av=read()
 found=app._calculation_axis(app.well,['X','PHIE','SW'],1010.25,1012.25,['X']);axis,curves=found if found else (np.array([]),{'X':np.array([])});inside=(axis>=1010.25)&(axis<=1012.25)
 out={'workflow':'X, PHIE and SW initially on independent 0.5-ft axes shifted 0.25 ft from the well; only constant PHIE resampled to 1 ft at origin 0.25','before':before,'after':after,'X_scientific_axis_and_values_unchanged':bool(np.array_equal(bd,ad) and np.array_equal(bv,av)),'chosen_axis_in_zone':axis[inside].tolist(),'chosen_X_values':curves['X'][inside].tolist(),'accepted_X_fine_zone_depths':d[(d>=1010.25)&(d<=1012.25)].tolist(),'accepted_X_fine_zone_values':x[(d>=1010.25)&(d<=1012.25)].tolist(),'refusals':app.last_zone_refusals,'previews':list(app.preview_names),'analytical_pay_support_ft':1.0}
 Path('/workspace/audit-v0.9.53/multiple-own-axes-evidence.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
finally:T.doCleanups()
