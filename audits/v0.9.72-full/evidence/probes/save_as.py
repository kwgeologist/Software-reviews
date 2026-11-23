from pathlib import Path
import sys,json,sqlite3
from unittest import mock
B=Path('/workspace/audit-v0.9.72-full');C=B/'checkout';sys.path[:0]=[str(C),str(C/'tests')];import conftest
from test_v0971_persistence import GeoPendingEdits
from ogcore import project_ui
x=GeoPendingEdits();x.setUp();out={}
try:
 parent=Path(x.x.temp.name);original=x.path;edited=x.tab.form.vars['well_name'].get()
 with mock.patch.object(project_ui,'ask_project_location',return_value=(parent,'SavedAs',{})),mock.patch('geoworkbench.main_window.messagebox.askyesnocancel',return_value=True):
  x.app.save_project_as()
 copied=x.app.db.path
 def name(p):
  con=sqlite3.connect(p)
  try:return con.execute('SELECT well_name FROM wells WHERE id=?',(x.well,)).fetchone()[0]
  finally:con.close()
 out={'expected_saved_as_name':edited,'original_stored_name_after':name(original),'new_copy_stored_name':name(copied),'new_project_opened':copied!=original,'new_open_header_name':next(t for t in x.app.tabs if type(t).__name__=='WellTab').form.vars['well_name'].get()}
finally:x.tearDown()
(B/'save-as-results.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
