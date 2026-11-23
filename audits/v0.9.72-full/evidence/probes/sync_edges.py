from pathlib import Path
import sys,json,tempfile,sqlite3,shutil,logging
B=Path('/workspace/audit-v0.9.72-full');C=B/'checkout';sys.path[:0]=[str(C),str(C/'tests')];import conftest
from database import ProjectDatabase
from ogcore import sync_safety as s,recovery
out={}
with tempfile.TemporaryDirectory(prefix='audit-sync-')as td:
 root=Path(td);p=root/'p.ogwdb';d=ProjectDatabase(p);w=d.add_well('Saved before', '');d.close();before=s.stamp_of_file(p);old=root/'old.ogwdb';shutil.copy2(p,old);d=ProjectDatabase(p,create=False);d.update_well(w,{'well_name':'Committed newer'});d.connection.execute('PRAGMA busy_timeout=50');lock=sqlite3.connect(p);lock.execute('BEGIN IMMEDIATE')
 try:
  result=d.close();out['close_under_write_lock']={'close_return':result,'before_seq':before.seq}
 finally:lock.rollback();lock.close()
 now=s.stamp_of_file(p);c=sqlite3.connect(p);name=c.execute('SELECT well_name FROM wells WHERE id=?',(w,)).fetchone()[0];c.close();out['close_under_write_lock'].update(after_seq=now.seq,generation_changed=now.generation_id!=before.generation_id,committed_name=name,problems_after_lock_released=[x.kind for x in s.problems(p)])
 shutil.copy2(old,p);out['stale_replaced_same_generation']={'problems':[x.kind for x in s.problems(p)],'accepted_generation_seq':s.accepted(before.project_uid)['generation_seq']}
 hand=s.handoff_path(p);record=json.loads(hand.read_text());record['generation_seq']='corrupt-but-valid-json';hand.write_text(json.dumps(record))
 try:s.problems(p);error=None
 except Exception as e:error=type(e).__name__+': '+str(e)
 out['malformed_handoff']={'observed_exception':error,'expected':'classified unverified-copy result'}
 hand.unlink();r=recovery.ReadOnlyProject(p,forensic=True)
 try:out['recovery_schema_note']={'schema':r.schema,'supported_database_schema':31,'known_schema':recovery.KNOWN_SCHEMA,'notes':r.notes(),'originals_unchanged':r.originals_unchanged()}
 finally:r.close()
(B/'sync-edge-results.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
