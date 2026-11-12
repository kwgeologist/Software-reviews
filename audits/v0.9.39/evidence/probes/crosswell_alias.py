import sys,json,numpy as np
from pathlib import Path
R=Path('/workspace/audit-v0.9.39/OandG_Workbench_v0.9.39');sys.path[:0]=[str(R),str(R/'tests')]
from test_petro_canonical_curves import CanonicalCurveTests
from database import ProjectDatabase
from ogcore import curve_aliases
T=CanonicalCurveTests();T.setUpClass();T.setUp()
try:
 app=T.open_petro();first=T.blanco
 curve_aliases.set_curves(app.geo_db,'AUDIT_ALIAS',['A_ONLY','B_ONLY']);app._reload_project_aliases();app._refresh_aliases()
 def configure(name):
  w=app.well;w.curves[name]=np.ones(w.depth.size);w.units[name]='';app.commit_curves_to_project([name]);app._refresh_aliases()
  app.zones=[{'name':'AUDIT_ZONE','top':float(w.depth[10]),'base':float(w.depth[20])}]
  app.pay_flags=[{'name':'ALIAS_PAY','zone':'AUDIT_ZONE','output':'PAY_FLAG','criteria':[{'curve':'AUDIT_ALIAS','op':'>','value':0.5}]}]
 def read():
  db=ProjectDatabase(T.project)
  try:return [dict(r) for r in db.rows('SELECT w.well_name,v.value_number FROM zone_values v JOIN zone_attributes a ON a.id=v.attribute_id JOIN wells w ON w.id=v.well_id WHERE a.name=? ORDER BY w.id',('ALIAS_PAY net',))]
  finally:db.close()
 configure('A_ONLY');app.save_project();before=read();active_A=app.curve_source('AUDIT_ALIAS')
 other=next(wid for wid in (r[0] for r in app.geo_db.rows('SELECT id FROM wells ORDER BY id')) if wid!=first)
 app.switch_well(app._geo_workspace_key(other));configure('B_ONLY');active_B=app.curve_source('AUDIT_ALIAS');app.save_project();after=read()
 result={'active_alias_in_A':active_A,'first_well_results_before_switch':before,'active_alias_in_B':active_B,'results_after_save_with_B_active':after};print(json.dumps(result,indent=2));Path('/workspace/audit-v0.9.39/crosswell-alias-evidence.json').write_text(json.dumps(result,indent=2))
finally:T.doCleanups()
