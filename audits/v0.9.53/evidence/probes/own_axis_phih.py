import sys,json,numpy as np
from pathlib import Path
R=Path('/workspace/audit-v0.9.53/OandG_Workbench_v0.9.53');sys.path[:0]=[str(R),str(R/'tests')]
from test_petro_canonical_curves import CanonicalCurveTests
from database import ProjectDatabase
T=CanonicalCurveTests();T.setUpClass();T.setUp()
try:
 app=T.open_petro();n=app.well.depth.size
 for name,value in [('X',1.),('PHIE',.2),('SW',.5)]:app.well.curves[name]=np.full(n,value);app.well.units[name]='v/v'
 app.commit_curves_to_project(['X','PHIE','SW']);panel=app.open_curve_editor_resample('PHIE',(1.,0.));panel.output_mode.set('overwrite');assert panel.preview(quiet=True) is not None;assert panel.accept()=='PHIE'
 app.zones=[{'name':'REF','top':1010.,'base':1012.}];app.pay_flags=[{'name':'OWN','zone':'REF','output':'PAY_FLAG','criteria':[{'curve':'X','op':'>','value':.5}]}];app.save_project()
 db=ProjectDatabase(T.project)
 try:rows={r[0]:r[1] for r in db.rows('SELECT a.name,v.value_number FROM zone_values v JOIN zone_attributes a ON a.id=v.attribute_id WHERE v.well_id=? AND a.name LIKE ?', (T.blanco,'OWN%'))}
 finally:db.close()
 out={'workflow':'Curve Editor Resample PHIE to 1 ft, overwrite and Accept; X/SW remain on 0.5-ft axis','published':rows,'analytical_constant_curve_reference':{'net':2.,'porosity':.2,'Sw':.5,'phi_h':.4,'HCPT':.2},'refusals':app.last_zone_refusals,'previews':list(app.preview_names),'PHIE_step':float(np.median(np.diff(app.well.depth_of('PHIE'))))};Path('/workspace/audit-v0.9.53/own-axis-phih-evidence.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
finally:T.doCleanups()
