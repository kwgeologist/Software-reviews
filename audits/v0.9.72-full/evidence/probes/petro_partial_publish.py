from pathlib import Path
import sys,json,sqlite3
from unittest import mock
B=Path('/workspace/audit-v0.9.72-full');C=B/'checkout';sys.path[:0]=[str(C),str(C/'tests')];import conftest
from test_petro_integration import PetroIntegrationTests
from ogcore import pay
PetroIntegrationTests.setUpClass();x=PetroIntegrationTests();x.setUp();out={}
try:
 app=x.open_petro();app.zones.append({'name':'Gallup SS','top':5440.,'base':5500.,'color':'#ff0000'});app.pay_flags.append({'name':'Net Pay','zone':'Gallup SS','output':'PAY_FLAG','criteria':pay.parse_criteria('GR < 80\nNPHI > 0.05',app.display_curves)});app.save_project()
 def stored():
  con=sqlite3.connect(x.project)
  try:return con.execute("SELECT value_number FROM zone_values v JOIN zone_attributes a ON a.id=v.attribute_id WHERE well_id=? AND a.name='Net Pay gross'",(x.blanco,)).fetchone()[0]
  finally:con.close()
 before=stored();app.zones[-1]['base']=5520.
 with mock.patch.object(app.geo_db,'publish_zone_values',side_effect=sqlite3.OperationalError('audit injected publish failure'))as publish,mock.patch('tkinter.messagebox.showerror')as err,mock.patch('tkinter.messagebox.showwarning')as warn:
  result=app.save_project();calls=publish.call_count;alerts=err.call_count+warn.call_count
 out={'before_published_gross':before,'expected_gross_after_accepted_zone_edit':80.,'after_failed_publish_gross':stored(),'publish_failure_calls':calls,'save_return':result,'UI_error_warning_count':alerts,'last_zone_refusals':getattr(app,'last_zone_refusals',None)}
 # Inspect stored Petro state through existing DB API without rerunning a save.
 loaded=app.geo_db.load_petro_state(x.blanco);out['stored_zone_base']=next(z['base'] for z in loaded[0]['zones'] if z['name']=='Gallup SS')
 out['live_accepted_base']=app.zones[-1]['base']
finally:x.tearDown()
(B/'petro-partial-publish.json').write_text(json.dumps(out,indent=2,default=str));print(json.dumps(out,indent=2,default=str))
