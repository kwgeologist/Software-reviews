import sys,json,tempfile
from pathlib import Path
from unittest import mock
R=Path('/workspace/audit-v0.9.52/OandG_Workbench_v0.9.52');sys.path[:0]=[str(R),str(R/'tests')]
from database import ProjectDatabase
from ogcore import project as P
from geoworkbench.main_window import WellDataManagerApp
from geoworkbench.well_tab import WellTab
out=[]
for route,answer in [('file-save',True),('file-discard',False),('file-cancel',None),('recent-discard',False)]:
 with tempfile.TemporaryDirectory() as td,mock.patch('pathlib.Path.home',return_value=Path(td)):
  projects={}
  for label in ['A','B']:
   p=P.Project.create(Path(td),label);projects[label]=p;db=ProjectDatabase(p.database_path)
   try:
    wid=db.add_well(label+' Well','');assert wid==1;db.update_well(wid,{'kb_elevation':1000.});db.set_formation_top(wid,'Marker',6000.,'Client')
   finally:db.close()
  app=WellDataManagerApp();app.withdraw()
  try:
   app.open_path(projects['A'].manifest_path);app.refresh_wells(select_id=1);app.update()
   tab=next(t for t in app.tabs if isinstance(t,WellTab));app.notebook.select(tab);app.update();tab.form.vars['kb_elevation'].set('1234');assert tab.dirty()
   stale={k:getattr(tab,k) for k in ['_baseline','_loaded_well','_loaded_identity']}
   app.notebook.select(next(t for t in app.tabs if t is not tab));app.update()
   with mock.patch('tkinter.messagebox.askyesnocancel',return_value=answer) as ask,mock.patch('tkinter.filedialog.askopenfilename',return_value=str(projects['B'].manifest_path)),mock.patch('tkinter.messagebox.showerror') as errors:
    if route.startswith('recent'):app.open_recent_project(projects['B'].manifest_path)
    else:app.open_project()
    app.update();prompts=ask.call_count;errs=[str(c) for c in errors.call_args_list]
   current='B' if app.db.path.resolve()==projects['B'].database_path.resolve() else 'A'
   old_dirty=tab.dirty();forced=None
   if current=='B':
    app.refresh_wells(select_id=1);app.notebook.select(tab);app.update()
    for k,v in stale.items():setattr(tab,k,v)
    tab.form.vars['kb_elevation'].set('1234')
    with mock.patch('tkinter.messagebox.showerror') as e:tab.save()
    forced={'refusal_count':e.call_count}
    tab.refresh();forced['refresh_kb']=tab.form.vars['kb_elevation'].get()
   rows={}
   for label,p in projects.items():
    db=ProjectDatabase(p.database_path)
    try:rows[label]=dict(db.row('SELECT w.kb_elevation,t.measured_depth,t.tvd,t.tvdss FROM wells w JOIN formation_tops t ON t.well_id=w.id WHERE w.id=1'))
    finally:db.close()
   expected_a=1234. if answer is True else 1000.;assert rows['A']['kb_elevation']==expected_a
   assert rows['B']=={'kb_elevation':1000.,'measured_depth':6000.,'tvd':6000.,'tvdss':-5000.}
   assert current==('A' if answer is None else 'B') and prompts==1
   if forced:assert forced['refusal_count']==1 and float(forced['refresh_kb'])==1000.
   out.append({'route':route,'user_answer':answer,'current_project':current,'prompts':prompts,'pending_dirty_after_transition':old_dirty,'persisted_reopened':rows,'forced_stale_identity':forced,'errors_during_open':errs})
  finally:
   for job in app.tk.call('after','info'):
    try:app.after_cancel(job)
    except Exception:pass
   if app.db:app.db.close();app.db=None
   app.destroy()
Path('/workspace/audit-v0.9.52/header-transition-matrix-evidence.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
