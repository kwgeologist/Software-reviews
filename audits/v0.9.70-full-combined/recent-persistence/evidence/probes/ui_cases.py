from pathlib import Path
import sys,tempfile,json,sqlite3,os
from unittest import mock
B=Path('/workspace/audit-v0.9.70-integrity'); C=B/'checkout';sys.path[:0]=[str(C),str(C/'tests')]
import conftest
out={}
from test_seismic_app import SeismicAppTests
x=SeismicAppTests();x.setUp(); a=x.app
try:
 a.select_survey(a.db.rows('select * from seismic_surveys')[0]['id'])
 a.interp.set_horizon_pick('Horizon 1',6,8,1000.0);assert a.save_now()
 a.interp.set_horizon_pick('Horizon 1',6,8,1200.0)
 with mock.patch.object(a.store,'save_interpretation',side_effect=sqlite3.OperationalError('injected disk I/O error')):
  a.close_project()
 closed=a.db is None
 a.open_project(x.path);a.select_survey(a.db.rows('select * from seismic_surveys')[0]['id'])
 actual=float(a.interp.horizons['Horizon 1'][(6,8)])
 out['seismic_close_failed_save']={'closed_despite_save_error':closed,'saved_before':1000,'unsaved_edit':1200,'after_reopen':actual};assert closed and actual==1000
finally:x.tearDown()
(B/'ui-cases-partial.json').write_text(json.dumps(out,indent=2))
from test_geo_tabs import GeoTabTests
x=GeoTabTests();x.setUp();a=x.app;path=a.db.path;w=x.well_id
try:
 tab=x.tab('WellTab');tab.form.vars['well_name'].set('Edited Draft');assert tab.dirty()
 a.save_project(); old=a.db.row('select well_name from wells where id=?',(w,))[0]
 with mock.patch('tkinter.messagebox.askyesnocancel',return_value=None)as ask:
  a.on_close();asked=ask.call_count
 with sqlite3.connect(path)as db:after=db.execute('select well_name from wells where id=?',(w,)).fetchone()[0]
 out['geo_save_and_exit_dirty_header']={'dirty_before_save':True,'after_save_project':old,'after_exit_reopen':after,'dirty_prompt_calls':asked};assert old=='Tab Well' and after=='Tab Well' and asked==0
finally:
 x.home_patch.stop();x.temp.cleanup()
(B/'ui-cases-partial.json').write_text(json.dumps(out,indent=2))
# A manifest exists but its database has never arrived (no existing database removed).
from ogcore.project import Project
from seismicworkbench.app import SeismicWorkbench
with tempfile.TemporaryDirectory(prefix='missing-manifest-target-')as td:
 p=Project.create(td,'Incomplete');assert not p.database_path.exists();a=SeismicWorkbench();a.withdraw()
 try:
  a.open_project(p.manifest_path)
  out['existing_manifest_missing_database']={'database_created':p.database_path.exists(),'app_opened_database':a.db is not None,'well_count':a.db.row('select count(*) from wells')[0] if a.db else None};assert a.db is not None and p.database_path.exists()
 finally:a.close_project();a.destroy()
(B/'ui-cases.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
