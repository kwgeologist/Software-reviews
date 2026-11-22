from pathlib import Path
import sys,json,sqlite3
from unittest import mock
B=Path('/workspace/audit-v0.9.70-integrity/compare69');C=Path('/workspace/audit-v0.9.69-tk/checkout');sys.path[:0]=[str(C),str(C/'tests')]
import conftest
out={}
from test_correlation import CorrelationAppTests
x=CorrelationAppTests();x.setUp();a=x.app
try:
 a.layout.spacing=1.25;a.store.save_session(a.layout);a.layout.spacing=7.25
 with mock.patch.object(a.store,'save_session',side_effect=sqlite3.OperationalError('injected disk full')):
  a.close_project()
 closed=a.db is None
 with sqlite3.connect(x.path)as db:stored=json.loads(db.execute("select value from project_meta where key='correlation:session'").fetchone()[0])['spacing']
 out['correlation_close_failed_session']={'closed':closed,'after_close_stored_spacing':stored,'unsaved_spacing':7.25};assert closed and stored==1.25
finally:x.tearDown()
(B/'close-errors-partial.json').write_text(json.dumps(out,indent=2))
from test_xsection import WindowTests
x=WindowTests();x.setUp();w=x.window()
try:
 w.section.name='Audit';w.section.view={'top':111,'x':0};w.store.save_section(w.section);w.top=222
 with mock.patch.object(w.store,'save_section',side_effect=sqlite3.OperationalError('injected disk full')):w.close()
 stored=w.store.sections()['Audit'].view['top'];out['xsection_close_failed_save']={'window_destroyed':not bool(w.winfo_exists()),'stored_top':stored,'unsaved_top':222};assert stored==111 and not w.winfo_exists()
finally:x.tearDown()
(B/'close-errors-partial.json').write_text(json.dumps(out,indent=2))
from test_geosteering_project import WindowProjectTests
x=WindowProjectTests();x.setUp();a=x.app
try:
 a.job.name='Saved';assert a.save();a.job.name='Unsaved';a.mark_dirty()
 with mock.patch('geosteering.project.save_job',side_effect=sqlite3.OperationalError('injected disk full')):
  a.on_close()
 from geosteering import project as link
 job,_=link.load_job(x.db,x.lateral)
 out['geosteering_close_failed_save']={'database_closed':a.db is None,'stored_job_name':job.name,'unsaved_job_name':'Unsaved'};assert a.db is None and job.name=='Saved'
finally:x.tearDown()
(B/'close-errors.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
