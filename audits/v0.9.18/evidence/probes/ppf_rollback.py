import sys,tempfile,json,hashlib
from pathlib import Path
R=Path('/workspace/audit-v0.9.18/OandG_Workbench_v0.9.18');B=R.parent;sys.path[:0]=[str(R),str(R/'tests')]
from database import ProjectDatabase
from ogcore import petra_ppf as P,curve_store as C
from test_petra_ppf import write_ppf,HEADER
out={}
with tempfile.TemporaryDirectory()as t:
 p=Path(t);first='WELL,"42401123450000"\nLOGHDR,"GR",3,1000.000,1001.000,0.50000,0,""\nLOGDATA,10.0,20.0,30.0\nLOGEND\n';second='WELL,"42401123450001"\nWELLNAM,"Synthetic","2","Synthetic 2"\n';src=write_ppf(p,first,second);db=ProjectDatabase(p/'p.ogwdb');P.apply(db,P.Plan(P.scan(src),datum='EPSG:4326'));las=next((p/'Imported Logs').glob('*.las'));before=las.read_bytes();wid=db.row('SELECT id FROM wells WHERE api14=?',('42401123450000',))[0];beforevalues=C.read(db,wid,'GR')[1].tolist();src=write_ppf(p,first.replace('10.0,20.0,30.0','99.0,88.0,77.0'),second)
 class Task:
  cancelled=False
  def __call__(self,k,total):
   if k==1:self.cancelled=True
 plan=P.Plan(P.scan(src),datum='EPSG:4326',blank_only=False)
 try:P.apply(db,plan,task=Task())
 except Exception as e:out['exception']=type(e).__name__
 C.forget(db);out.update(existing_file_preserved=before==las.read_bytes(),file_now_contains_new_samples='99.0000' in las.read_text(),db_before=beforevalues,db_after=C.read(db,wid,'GR')[1].tolist(),newly_written_tracked=list(map(str,plan.written)));db.close()
(B/'ppf-rollback-evidence.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
