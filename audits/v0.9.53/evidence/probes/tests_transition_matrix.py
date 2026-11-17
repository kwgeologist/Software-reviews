import sys,json,tempfile,copy
from pathlib import Path
from unittest import mock
R=Path('/workspace/audit-v0.9.53/OandG_Workbench_v0.9.53');sys.path[:0]=[str(R),str(R/'tests')]
from database import ProjectDatabase
from ogcore import project as P,well_tests as T
from test_well_tests import ip_record,fm_record,TREATMENTS,RECOVERIES
from geoworkbench.main_window import WellDataManagerApp
from geoworkbench.tests_tab import TestsTab
ORIGINAL={'ip_oil_bbl_d':469.,'acid_gal':500.,'fm_bhp_psi':2403.,'oil_recovery_bbl':12.3}
def science(p):
 db=ProjectDatabase(p.database_path)
 try:
  ip,fm=T.get_test(db,1),T.get_test(db,2)
  return {'ip_oil_bbl_d':ip['oil_rate'],'acid_gal':ip['treatments'][0]['fluid_volume'],'fm_bhp_psi':fm['bhp'],'oil_recovery_bbl':fm['recoveries'][0]['amount']}
 finally:db.close()
out=[]
for mode in ['ip','fm']:
 for route,answer in [('file-save',True),('file-discard',False),('file-cancel',None),('recent-discard',False)]:
  with tempfile.TemporaryDirectory() as td,mock.patch('pathlib.Path.home',return_value=Path(td)):
   projects={}
   for label in ['A','B']:
    p=P.Project.create(Path(td),label);projects[label]=p;db=ProjectDatabase(p.database_path)
    try:
     wid=db.add_well(label+' Well','');assert wid==1
     assert T.save_test(db,ip_record(wid),treatments=TREATMENTS)==1
     assert T.save_test(db,fm_record(wid),recoveries=RECOVERIES)==2
    finally:db.close()
   app=WellDataManagerApp();app.withdraw()
   try:
    app.open_path(projects['A'].manifest_path);app.refresh_wells(select_id=1);app.update()
    tab=next(t for t in app.tabs if isinstance(t,TestsTab));app.notebook.select(tab);app.update();tab.mode.set(mode);tab._mode_changed();testid=1 if mode=='ip' else 2;tab.load(testid)
    field='oil_rate' if mode=='ip' else 'bhp';tab._form()['vars'][field].set('999' if mode=='ip' else '3000')
    holder=tab._form()['children'];holder['tree'].selection_set('0');tab._child_chosen();holder['vars']['fluid_volume' if mode=='ip' else 'amount'].set('900' if mode=='ip' else '55');tab.edit_child();assert tab.dirty()
    keys=['selected_id','loaded','child_rows','editing_new','_loaded_identity','shown'];held=copy.deepcopy({k:getattr(tab,k) for k in keys});held_values=tab.form_values()
    app.notebook.select(next(t for t in app.tabs if t is not tab));app.update()
    with mock.patch('tkinter.messagebox.askyesnocancel',return_value=answer) as asks,mock.patch('tkinter.filedialog.askopenfilename',return_value=str(projects['B'].manifest_path)),mock.patch('tkinter.messagebox.showerror') as errors,mock.patch('tkinter.messagebox.showinfo'):
     if route.startswith('recent'):app.open_recent_project(projects['B'].manifest_path)
     else:app.open_project()
     app.update();prompts=asks.call_count;errs=errors.call_count
    current='B' if app.db.path.resolve()==projects['B'].database_path.resolve() else 'A'
    cleared=tab.loaded is None and tab.child_rows==[] and tab.selected_id is None and not tab.editing_new and tab._loaded_identity is None
    after_none_save=None;whole_refused=None;child_refused=None
    if current=='B':
     app.refresh_wells(select_id=1);app.notebook.select(tab);app.update()
     with mock.patch('tkinter.messagebox.showinfo'),mock.patch('tkinter.messagebox.showerror'):result=tab.save()
     after_none_save=result is None
     for k,v in held.items():setattr(tab,k,copy.deepcopy(v))
     tab._show(held_values,copy.deepcopy(held['child_rows']))
     with mock.patch('tkinter.messagebox.showerror') as error:result=tab.save()
     whole_refused=result is None and error.call_count==1
     tab.forget_loaded();tab.mode.set(mode);tab._mode_changed();tab.load(testid)
     tab.child_rows[0]=copy.deepcopy(held['child_rows'][0]);tab._show_children()
     with mock.patch('tkinter.messagebox.showerror') as error:result=tab.save()
     child_refused=result is None and error.call_count==1
     tab.forget_loaded()
    expected=ORIGINAL.copy()
    if answer is True:expected.update({'ip_oil_bbl_d':999.,'acid_gal':900.} if mode=='ip' else {'fm_bhp_psi':3000.,'oil_recovery_bbl':55.})
    sa,sb=science(projects['A']),science(projects['B']);assert sb==ORIGINAL and sa==expected
    assert current==('A' if answer is None else 'B') and prompts==1 and errs==0
    if current=='B':assert cleared and after_none_save and whole_refused and child_refused
    else:assert tab.dirty()
    out.append({'mode':mode,'route':route,'answer':answer,'current_project':current,'switch_prompts':prompts,'loaded_state_fully_cleared':cleared,'empty_editor_save_refused':after_none_save,'forced_stale_whole_editor_refused':whole_refused,'forced_stale_child_refused':child_refused,'A_reopened_science':sa,'B_reopened_science':sb,'errors_during_normal_open':errs})
   finally:
    for job in app.tk.call('after','info'):
     try:app.after_cancel(job)
     except Exception:pass
    if app.db:app.db.close();app.db=None
    app.destroy()
Path('/workspace/audit-v0.9.53/tests-transition-matrix-evidence.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
