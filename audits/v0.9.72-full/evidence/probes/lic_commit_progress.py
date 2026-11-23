from pathlib import Path
import sys,json,tkinter as tk
from unittest import mock
B=Path('/workspace/audit-v0.9.72-full');C=B/'checkout';sys.path[:0]=[str(C),str(C/'tests')];import conftest
from test_v0972_lic_import import _Fixture
from ograster import lic_import as li
from ogcore.task_progress import ProgressWindow
f=_Fixture();f.setUp();root=tk.Tk();root.withdraw()
try:
 paths=[f.lic('30-039-27700'),f.lic('30-039-27701')];plan=li.plan_import(f.db,paths,f.options(),single=False);real=f.db.connection
 class Failing:
  def __getattr__(self,n):return getattr(real,n)
  def commit(self):raise OSError('audit injected commit failure')
 p=ProgressWindow(root,'Import Petra LIC Logs',total=2,unit='logs')
 with mock.patch.object(f.db,'connection',Failing()):r=li.execute(f.db,plan,progress=p)
 p.finish(details=r.summary(),summary=[f'{k}: {v}'for k,v in r.counts().items()]);out={'database_rows':f.db.row('SELECT COUNT(*) FROM log_files')[0],'report_added':len(r.added),'report_errors':len(r.of(li.ERROR)),'progress_counts':p.counts,'visible_tally':p.tally_label.cget('text'),'visible_heading':p.heading_label.cget('text'),'details_contain_error':'Errors: 2'in r.summary()};p.close()
finally:root.destroy();f.doCleanups()
(B/'lic-commit-progress.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
