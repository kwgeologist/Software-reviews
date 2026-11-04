import sys,time,json,tempfile
from pathlib import Path
from collections import Counter
R=Path('/workspace/audit-v0.9.4/OandG_Workbench_v0.9.4');sys.path.insert(0,str(R))
from database import ProjectDatabase
from ogcore import ihs298 as I
out={}
with tempfile.TemporaryDirectory()as t:
 for size in [0,112000]:
  db=ProjectDatabase(Path(t)/f'p{size}.ogwdb');rows=((f'SEED-{n}','Seed',f'42{n:08d}0000',f'42{n:08d}0000',f'42{n:08d}0000','2026-01-01','2026-01-01')for n in range(size))
  with db.atomic():db.connection.executemany('INSERT INTO wells(well_uid,well_name,api_uwi,api14,api14_src,created_at,updated_at)VALUES(?,?,?,?,?,?,?)',rows)
  entities=[I.Entity(str(n),1,uwis=[f'43999{n:05d}0000'],months={'2025-01':{'oil':1.,'gas':2.,'water':0.}})for n in range(100)];parsed=I.Parsed(Path('synthetic.98c'),entities=entities,issues=I.Issues());start=time.perf_counter();plan=I.plan(db,parsed);planning=time.perf_counter()-start
  sqlcounts=Counter()
  def trace(s):
   if s.startswith('UPDATE wells SET api14='):sqlcounts['whole_table_api_refresh']+=1
   if s.strip().upper()=='COMMIT':sqlcounts['commits']+=1
  db.connection.set_trace_callback(trace);start=time.perf_counter();I.apply(db,plan);elapsed=time.perf_counter()-start;db.connection.set_trace_callback(None)
  query=[r[3]for r in db.rows('EXPLAIN QUERY PLAN UPDATE wells SET api14=ogw_api14(api_uwi), api14_src=api_uwi WHERE api14_src IS NOT api_uwi')];out[str(size)]={'new_wells':100,'planning_seconds':planning,'apply_seconds':elapsed,'sql_counts':dict(sqlcounts),'api_refresh_query_plan':query};db.close()
(R.parent/'performance-evidence.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
