import sys,json,tempfile
from pathlib import Path
from unittest import mock
R=Path('/workspace/audit-v0.9.52/OandG_Workbench_v0.9.52');sys.path[:0]=[str(R),str(R/'tests')]
from database import ProjectDatabase
from ogcore import project as P,production
from geoworkbench.main_window import WellDataManagerApp
from geoworkbench.formation_tab import FormationTopsTab
from geoworkbench.production_tab import ProductionTab,ProductionRowDialog
from geoworkbench.location import DirectionalSurveyManager
with tempfile.TemporaryDirectory() as td,mock.patch('pathlib.Path.home',return_value=Path(td)):
 projects={}
 for label,md,oil in [('A',6000.,100.),('B',6100.,200.)]:
  p=P.Project.create(Path(td),label);projects[label]=p;db=ProjectDatabase(p.database_path)
  try:
   wid=db.add_well(label+' Well','');assert wid==1;db.update_well(wid,{'kb_elevation':1000.});db.set_formation_top(wid,'Marker',md,'Client');production.save_row(db,wid,{'month':'2026-01','source':'Client','oil':oil})
  finally:db.close()
 app=WellDataManagerApp();app.withdraw()
 try:
  app.open_path(projects['A'].manifest_path);app.refresh_wells(select_id=1);app.update()
  top=next(t for t in app.tabs if isinstance(t,FormationTopsTab));app.notebook.select(top);app.update();top.tree.selection_set('1');top.on_select();top.form.vars['measured_depth'].set('6123')
  prod=next(t for t in app.tabs if isinstance(t,ProductionTab));app.notebook.select(prod);app.update();dlg=ProductionRowDialog(prod,production.rows(app.db,1)[0]);dlg.vars['oil'].set('999');assert dlg.dirty()
  survey=DirectionalSurveyManager(app);survey.manual_vars['measured_depth'].set('9999')
  with mock.patch('tkinter.messagebox.askyesnocancel',return_value=False) as ask,mock.patch('tkinter.messagebox.showerror') as err:
   app.open_path(projects['B'].manifest_path);app.update();app.refresh_wells(select_id=1);app.update()
   app.notebook.select(top);app.update();md_after=top.form.vars['measured_depth'].get()
   app.notebook.select(prod);app.update();visible_oil=production.rows(app.db,1)[0]['oil']
   prompts=ask.call_count;errors=[str(c) for c in err.call_args_list]
  out={'workflow':'A selected top with unsaved form text, dirty modeless Production month, Directional manager with pending manual point; File Open B with Discard','production_dialog_destroyed':not bool(dlg.winfo_exists()),'directional_manager_destroyed':not bool(survey.winfo_exists()),'formation_top_MD_after_B_refresh':md_after,'B_production_oil':visible_oil,'dirty_editor_prompts':prompts,'errors':errors,'B_deviation_rows':app.db.row('SELECT count(*) FROM deviation_points')[0]}
  assert out['production_dialog_destroyed'] and out['directional_manager_destroyed'] and float(md_after)==6100. and visible_oil==200. and out['B_deviation_rows']==0
  Path('/workspace/audit-v0.9.52/other-editor-transition-evidence.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
 finally:
  for job in app.tk.call('after','info'):
   try:app.after_cancel(job)
   except Exception:pass
  if app.db:app.db.close();app.db=None
  app.destroy()
