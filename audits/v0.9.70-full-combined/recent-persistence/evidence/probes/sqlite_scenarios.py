from pathlib import Path
import sys,os,json,tempfile,shutil,sqlite3,subprocess,zlib,hashlib
import numpy as np
B=Path('/workspace/audit-v0.9.70-integrity');C=B/'checkout';sys.path[:0]=[str(C),str(C/'tests')]
import conftest
from database import ProjectDatabase
from seismicworkbench.project import SeismicStore
from seismicworkbench.interpretation import HorizonPicks
out={}
def grid(v):
 h=HorizonPicks((3,3));h[(0,0)]=float(v);return h

def value(path):
 with sqlite3.connect(str(path))as con:
  b=con.execute("select picks from seismic_horizons where name='H'").fetchone()[0];return float(np.frombuffer(zlib.decompress(b),'<f4')[0])
def seed(p):
 d=ProjectDatabase(p);sid=d.execute("INSERT INTO seismic_surveys(name,file_path)VALUES('Fixture','synthetic.sgy')");s=SeismicStore(d);i,st,vi=s.load_interpretation(sid,(3,3));i.horizon('H')[(0,0)]=1;s.save_interpretation(sid,i,st,vi);return d,sid,s
with tempfile.TemporaryDirectory(prefix='v0970-sync-synthetic-')as td:
 r=Path(td);d,sid,s=seed(r/'desktop.ogwdb');con=d.connection
 out['actual_config']={'journal_mode':con.execute('pragma journal_mode').fetchone()[0],'synchronous':con.execute('pragma synchronous').fetchone()[0],'wal_autocheckpoint':con.execute('pragma wal_autocheckpoint').fetchone()[0]}
 i,st,vi=s.load_interpretation(sid,(3,3));i.horizon('H')[(0,0)]=2;s.save_interpretation(sid,i,st,vi)
 shutil.copy2(d.path,r/'A-main.ogwdb');out['A_default_open_connection_main_only']={'stored_value':value(r/'A-main.ogwdb'),'expected':2};assert value(r/'A-main.ogwdb')==2
 d.close();shutil.copy2(r/'desktop.ogwdb',r/'B-main.ogwdb');assert value(r/'B-main.ogwdb')==2;out['B_clean_close_main_only']={'value':2}
 # Two genuinely independent local copies; use the business storage API for both.
 shutil.copy2(r/'desktop.ogwdb',r/'laptop.ogwdb');a=ProjectDatabase(r/'desktop.ogwdb');b=ProjectDatabase(r/'laptop.ogwdb')
 for db,v in [(a,30),(b,40)]:
  ss=SeismicStore(db);ii,st,vi=ss.load_interpretation(sid,(3,3));ii.horizon('H')[(0,0)]=v;ss.save_interpretation(sid,ii,st,vi)
 a.close();b.close();out['D_independent_replicas']={'desktop':value(r/'desktop.ogwdb'),'laptop':value(r/'laptop.ogwdb')};assert out['D_independent_replicas']=={'desktop':30.,'laptop':40.}
 # E: preserve both, then simulate provider choosing the older copy into a NEW destination.
 shutil.copy2(r/'desktop.ogwdb',r/'newer-preserved.ogwdb');shutil.copy2(r/'B-main.ogwdb',r/'canonical-after-stale-sync.ogwdb');reopen=ProjectDatabase(r/'canonical-after-stale-sync.ogwdb');loaded=SeismicStore(reopen).load_interpretation(sid,(3,3))[0].horizons['H'][(0,0)];reopen.close();out['E_stale_generation_selected']={'selected':float(loaded),'newer_preserved':value(r/'newer-preserved.ogwdb'),'application_accepts_without_generation_error':True};assert loaded==2
 # Conditional WAL: explicitly set it ONLY on a synthetic database, then use Workbench writes.
 d=ProjectDatabase(r/'desktop.ogwdb');assert d.connection.execute('pragma journal_mode=WAL').fetchone()[0]=='wal';d.connection.execute('pragma wal_autocheckpoint=0')
 ss=SeismicStore(d);ii,st,vi=ss.load_interpretation(sid,(3,3));ii.horizon('H')[(0,0)]=99;ss.save_interpretation(sid,ii,st,vi)
 shutil.copy2(d.path,r/'WAL-main-only.ogwdb');main_value=value(r/'WAL-main-only.ogwdb');out['A_inherited_WAL_open_connection']={'main_only':main_value,'committed_in_connection':99.,'wal_bytes':Path(str(d.path)+'-wal').stat().st_size};assert main_value==30
 d.close();shutil.copy2(r/'desktop.ogwdb',r/'WAL-clean-close.ogwdb');assert value(r/'WAL-clean-close.ogwdb')==99;out['B_WAL_clean_close']={'value':99}
 # Abrupt exit leaves a committed WAL, not a checkpointed main file.
 code="""import sqlite3,os,zlib,numpy as np,sys
c=sqlite3.connect(sys.argv[1]);c.execute('pragma journal_mode=WAL');c.execute('pragma wal_autocheckpoint=0');a=np.full((3,3),np.nan,dtype='<f4');a[0,0]=123;c.execute('update seismic_horizons set picks=? where name=\"H\"',(zlib.compress(a.tobytes()),));c.commit();os._exit(0)
"""
 subprocess.run([sys.executable,'-c',code,str(r/'desktop.ogwdb')],check=True)
 shutil.copy2(r/'desktop.ogwdb',r/'C-main-only.ogwdb');out['C_committed_WAL_abrupt_exit']={'main_only':value(r/'C-main-only.ogwdb'),'expected_latest':123,'wal_present':Path(str(r/'desktop.ogwdb')+'-wal').exists()};assert out['C_committed_WAL_abrupt_exit']['main_only']==99
 w=r/'working';w.mkdir();dbcopy=w/'complete.ogwdb';shutil.copy2(r/'desktop.ogwdb',dbcopy);shutil.copy2(Path(str(r/'desktop.ogwdb')+'-wal'),Path(str(dbcopy)+'-wal'));assert value(dbcopy)==123;out['C_recovery_on_disposable_complete_pair']={'value':123}
 # Recovery Access no-sidecar claim: a different untouched synthetic pair, no shm copied.
 w=r/'readonly_probe';w.mkdir();p=w/'probe.ogwdb';shutil.copy2(r/'desktop.ogwdb',p);shutil.copy2(Path(str(r/'desktop.ogwdb')+'-wal'),Path(str(p)+'-wal'));before={x.name for x in w.iterdir()}
 from ogcore.recovery import ReadOnlyProject
 rr=ReadOnlyProject(p);during={x.name for x in w.iterdir()};val=rr.connection.execute("select picks from seismic_horizons where name='H'").fetchone()[0];rr.close();out['recovery_readonly_sidecar']={'created_files':sorted(during-before),'value':float(np.frombuffer(zlib.decompress(val),'<f4')[0])};assert 'probe.ogwdb-shm'in during-before
 # No client files accessed. Show foreign lock marker behavior on a synthetic marker.
 from ogcore.safeio import SessionLock,write_json
 lock=SessionLock(r/'fake.ogwdb','.seismic.lock');write_json(lock.path,{'host':'other-computer','pid':1234,'user':'fixture','since':'synthetic'});holder=lock.holder();lock.acquire();out['advisory_lock']={'foreign_holder_detected':holder is not None,'acquire_still_overwrites_marker':json.loads(lock.path.read_text())['host']!='other-computer'};lock.release()
(B/'sqlite-scenarios.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
