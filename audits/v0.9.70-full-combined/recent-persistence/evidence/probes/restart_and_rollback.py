from pathlib import Path
import sys,os,json,tempfile,subprocess,sqlite3,shutil
import numpy as np
B=Path('/workspace/audit-v0.9.70-integrity');C=B/'checkout';sys.path[:0]=[str(C),str(C/'tests')]
import conftest
from database import ProjectDatabase
from seismicworkbench.project import SeismicStore
from correlationworkbench.store import Store as CorStore
from correlationworkbench.model import Layout
from xsection.store import Store as XStore
from xsection.model import Section,SectionWell,Correlation
from ogmap import drawings
from test_geosteering_project import make_project
from geosteering import project as link
out={}
with tempfile.TemporaryDirectory(prefix='v0970-restart-')as td:
 root=Path(td);db,well,typeid,off,demo=make_project(root)
 db.update_well(well,{'well_name':'Saved restart well'})
 depth=np.array([12000.,12001.,12002.]);db.save_petro_state(well,{'audit':'saved'},depth,{'AUDIT_CURVE':np.array([1.,2.,3.])})
 sid=db.execute("insert into seismic_surveys(name,file_path)values('restart fixture','fixture.sgy')")
 s=SeismicStore(db);i,st,vi=s.load_interpretation(sid,(3,3));i.horizon('RestartH')[(1,1)]=678.5;i.faults['RestartF']=[{'i':1,'j':1,'twt':680.,'section':'IL 1'}];s.save_interpretation(sid,i,st,vi)
 did=drawings.save(db,drawings.Drawing('Restart polygon','fault',np.array([[0,0],[1,0],[1,1],[0,0]]),{'dip':45}))
 layout=Layout();layout.spacing=3.25;CorStore(db).save_session(layout)
 sec=Section('Restart section',[SectionWell(well)]);sec.correlations.append(Correlation(name='Restart correlation',points={str(well):12001.}));XStore(db).save_section(sec)
 job,_=link.load_job(db,well);job.name='Restart job';link.save_job(db,job)
 path=db.path;db.close()
 # New interpreter: load through actual storage APIs and verify raw persisted data too.
 code="""from pathlib import Path
import sys,json
sys.path[:0]=[sys.argv[1],sys.argv[1]+'/tests']
import conftest
from database import ProjectDatabase
from seismicworkbench.project import SeismicStore
from correlationworkbench.store import Store as CS
from xsection.store import Store as XS
from ogmap import drawings
from geosteering import project as link
p=sys.argv[2];w=int(sys.argv[3]);sid=int(sys.argv[4]);did=int(sys.argv[5]);db=ProjectDatabase(p)
i,_,_=SeismicStore(db).load_interpretation(sid,(3,3));state=db.load_petro_state(w)
r={'well_name':db.row('select well_name from wells where id=?',(w,))[0], 'tops':db.row('select count(*) from formation_tops')[0],'petro_values':state[2]['AUDIT_CURVE'].tolist(),'horizon':float(i.horizons['RestartH'][(1,1)]),'fault':i.faults['RestartF'],'polygon_vertices':drawings.load(db,did).xy.tolist(),'correlation_spacing':CS(db).session().spacing,'section_correlation':XS(db).sections()['Restart section'].correlations[0].points,'geosteer_job':link.load_job(db,w)[0].name,'integrity':db.row('pragma integrity_check')[0]}
print(json.dumps(r));db.close()
"""
 def child(p):
  r=subprocess.run([sys.executable,'-c',code,str(C),str(p),str(well),str(sid),str(did)],text=True,capture_output=True,check=True);v=json.loads(r.stdout);assert v['horizon']==678.5 and v['petro_values']==[1,2,3] and v['well_name']=='Saved restart well' and v['geosteer_job']=='Restart job' and v['correlation_spacing']==3.25 and v['section_correlation']=={str(well):12001.} and v['integrity']=='ok';return v
 out['fresh_interpreter_original']=child(path)
 copy=root/'synced-copy';shutil.copytree(root,copy,ignore=shutil.ignore_patterns('synced-copy'));out['fresh_interpreter_simulated_synced_copy']=child(copy/path.name)
 # A rollback-mode process dies during an uncommitted write after spilling pages.
 raw=root/'rollback-crash.ogwdb';con=sqlite3.connect(raw);con.execute('create table fixture(id integer primary key,payload blob)');con.executemany('insert into fixture values(?,?)',[(k,b'OLD'*1000)for k in range(300)]);con.commit();con.close()
 crash="""import sqlite3,os,sys
c=sqlite3.connect(sys.argv[1]);c.execute('pragma cache_size=5');c.execute('begin immediate');c.execute('update fixture set payload=?',(b'NEW'*1000,));os._exit(0)
""";subprocess.run([sys.executable,'-c',crash,str(raw)],check=True)
 assert Path(str(raw)+'-journal').exists();work=root/'rollback-working';work.mkdir();target=work/raw.name;shutil.copy2(raw,target);shutil.copy2(Path(str(raw)+'-journal'),Path(str(target)+'-journal'))
 con=sqlite3.connect(target);count=con.execute("select count(*) from fixture where payload=?",(b'OLD'*1000,)).fetchone()[0];integrity=con.execute('pragma integrity_check').fetchone()[0];con.close();assert count==300 and integrity=='ok';out['C_DELETE_uncommitted_crash_working_copy']={'journal_preserved_before_recovery':True,'previous_committed_rows_restored':count,'integrity':integrity,'uncommitted_NEW_rows_not_expected_to_survive':True}
(B/'restart-and-rollback.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
