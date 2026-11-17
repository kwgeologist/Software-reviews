import sys,json,numpy as np
from pathlib import Path
R=Path('/workspace/audit-v0.9.52/OandG_Workbench_v0.9.52');sys.path[:0]=[str(R),str(R/'tests')]
from test_petro_canonical_curves import CanonicalCurveTests
from database import ProjectDatabase
from ogcore import curve_store
T=CanonicalCurveTests();T.setUpClass();T.setUp()
try:
 app=T.open_petro();d=app.well.depth;n=d.size
 x=np.where((d>=1011.5)&(d<=1013.0),60.,130.)
 for name,values in [('GR_AUDIT',x),('PHIE',np.full(n,.2)),('SW',np.full(n,.5))]:app.well.curves[name]=values;app.well.units[name]='API' if name=='GR_AUDIT' else 'v/v'
 app.commit_curves_to_project(['GR_AUDIT','PHIE','SW']);app.zones=[{'name':'REF','top':1010.,'base':1020.}];app.pay_flags=[{'name':'PAY','zone':'REF','output':'PAY_FLAG','criteria':[{'curve':'GR_AUDIT','op':'<','value':80.}]}]
 def read():
  db=ProjectDatabase(T.project)
  try:
   rows={r[0]:r[1] for r in db.rows('SELECT a.name,v.value_number FROM zone_values v JOIN zone_attributes a ON a.id=v.attribute_id WHERE v.well_id=? AND a.name LIKE ?', (T.blanco,'PAY%'))};rec=curve_store.resolve(db,T.blanco,'GR_AUDIT',source='calc',aliases={});dd,v=curve_store.arrays(db,rec)
   return rows,dd.copy(),v.copy()
  finally:db.close()
 app.save_project();before,bd,bv=read()
 panel=app.open_curve_editor_resample('PHIE',(5.,0.));panel.output_mode.set('overwrite');assert panel.preview(quiet=True) is not None;assert panel.accept()=='PHIE';app.save_project();after,ad,av=read()
 found=app._calculation_axis(app.well,['GR_AUDIT','PHIE','SW'],1010.,1020.,['GR_AUDIT']);axis,curves=found if found else (np.array([]),{'GR_AUDIT':np.array([])});inside=(axis>=1010)&(axis<=1020)
 out={'workflow':'Single 2-ft GR pay bed in a 10-ft zone; only constant PHIE resampled to 5 ft and accepted, GR/SW never edited','before':before,'after':after,'cutoff_scientific_axis_and_values_unchanged':bool(np.array_equal(bd,ad) and np.array_equal(bv,av)),'chosen_axis_in_zone':axis[inside].tolist(),'chosen_cutoff_values':curves['GR_AUDIT'][inside].tolist(),'accepted_cutoff_fine_zone_depths':d[(d>=1010)&(d<=1020)].tolist(),'accepted_cutoff_fine_zone_values':x[(d>=1010)&(d<=1020)].tolist(),'refusals':app.last_zone_refusals,'previews':list(app.preview_names),'analytical_pay_support_ft':2.0}
 Path('/workspace/audit-v0.9.52/thin-bed-pay-evidence.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
finally:T.doCleanups()
