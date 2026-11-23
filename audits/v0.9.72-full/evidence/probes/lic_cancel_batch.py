from pathlib import Path
import sys,json,tempfile,time,sqlite3
B=Path('/workspace/audit-v0.9.72-full');C=B/'checkout';sys.path[:0]=[str(C),str(C/'tests')];import conftest
from database import ProjectDatabase
from ogcore import raster
from ograster import lic_import as li
from test_raster import write_log_image
out={}
class Progress:
 def __init__(self,db,lock=False):self.cancelled=False;self.n=0;self.done=0;self.lock=None;self.db=db;self.use_lock=lock
 def begin(self,name):
  self.n+=1
  if self.n==2001:
   self.cancelled=True
   if self.use_lock:self.lock=sqlite3.connect(self.db.path);self.lock.execute('BEGIN IMMEDIATE')
 def done_item(self,*args):self.done+=1
with tempfile.TemporaryDirectory(prefix='audit-lic2327-')as td:
 root=Path(td);images=root/'Images';images.mkdir();write_log_image(images/'scan.tif',80,1500);lics=root/'LIC';lics.mkdir();db=ProjectDatabase(root/'p.ogwdb')
 try:
  w=db.add_well('Synthetic','30039277000000');paths=[];cal=raster.Calibration([(4000.,100.),(4500.,1400.)])
  for k in range(2327):
   p=lics/f'section-{k}.LIC';raster.write_lic(p,'C:\\Petra\\scan.tif',cal,80,1500,name=f'Section{k}',uwi='30039277000000',group=k);paths.append(p)
  options=li.Options(images);start=time.monotonic();plan=li.plan_import(db,paths,options,single=False);planning=time.monotonic()-start;progress=Progress(db);start=time.monotonic();rep=li.execute(db,plan,progress=progress,write_project_lics=False);out['unlocked_cancel_at_2001']={'files':2327,'planning_seconds':planning,'writing_seconds':time.monotonic()-start,'cancelled_requested':progress.cancelled,'begun':progress.n,'completed':progress.done,'added':len(rep.added),'not_processed_report':rep.cancelled}
  db.execute('DELETE FROM log_files');plan=li.plan_import(db,paths,options,single=False);db.connection.execute('PRAGMA busy_timeout=10');progress=Progress(db,True);start=time.monotonic()
  try:rep=li.execute(db,plan,progress=progress,write_project_lics=False)
  finally:
   if progress.lock:progress.lock.rollback();progress.lock.close()
  out['locked_cancel_at_2001']={'busy_timeout_ms':10,'seconds':time.monotonic()-start,'cancelled_requested':progress.cancelled,'begun':progress.n,'completed':progress.done,'added':len(rep.added),'errors':len(rep.of(li.ERROR)),'not_processed_report':rep.cancelled,'stored_rows':db.row('SELECT COUNT(*) FROM log_files')[0]}
 finally:db.close()
(B/'lic-batch-cancel.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
