from pathlib import Path
import sys,os,tempfile,json
import numpy as np
B=Path('/workspace/audit-v0.9.70-full');C=Path('/workspace/audit-v0.9.70-integrity/checkout');sys.path[:0]=[str(C),str(C/'tests')]
import conftest
from database import ProjectDatabase
from ogcore import curve_store
out={}
def bytes_of(obj):
 seen=set()
 def walk(o):
  if id(o)in seen:return 0
  seen.add(id(o))
  if isinstance(o,np.ndarray):return o.nbytes
  if isinstance(o,dict):return sum(walk(x)for x in o.values())
  if isinstance(o,(list,tuple)):return sum(walk(x)for x in o)
  if hasattr(o,'__dict__'):return walk(vars(o))
  return 0
 return walk(obj)
with tempfile.TemporaryDirectory(prefix='v0970-cache-audit-')as td:
 r=Path(td);db=ProjectDatabase(r/'fixture.ogwdb');p=r/'samples.las';n=10001
 with p.open('w')as f:
  f.write('~Version\nVERS. 2.0\nWRAP. NO\n~Well\nSTRT.FT 0\nSTOP.FT 10000\nSTEP.FT 1\nNULL. -999.25\nWELL. Fixture\n~Curve\nDEPT.FT : depth\nGR.API : gamma ray\nRT.OHMM : resistivity\n~A\n');np.savetxt(f,np.column_stack([np.arange(n),np.full(n,50.),np.full(n,10.)]),fmt='%.3f')
 ids=[]
 for k in range(8):
  wid=db.add_well(f'Cache fixture {k}','');db.load_las_file(wid,p);ids.append(db.row('select id from log_files where well_id=?',(wid,))[0])
 curve_store.forget();before=curve_store._cache.evicted
 for lid in ids:curve_store.run(db,lid)
 cache=curve_store._cache;actual=bytes_of(list(cache.values()));out['las_run_cache']={'runs':len(cache),'reported_cache_bytes':cache.bytes,'actual_unique_numpy_bytes':actual,'configured_max_bytes':cache.max_bytes,'max_items':cache.max_items,'evictions':cache.evicted-before,'one_entry_accounting_bytes':[cache.size_of(x)for x in cache.values()]};assert len(cache)==8 and cache.bytes==512 and actual>1_000_000
 curve_store.forget();db.close()
(B/'cache-and-sources.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
