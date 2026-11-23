from pathlib import Path
import sys,tempfile,weakref,gc,json,tkinter as tk
from unittest import mock
C=Path('/workspace/audit-v0.9.72-full/checkout');sys.path[:0]=[str(C),str(C/'tests')];import conftest
from petroworkbench.app import PetroWorkbench
refs=[];out=[]
with tempfile.TemporaryDirectory(prefix='petro-root-retention-')as td,mock.patch('pathlib.Path.home',return_value=Path(td)):
 for k in range(10):
  a=PetroWorkbench();a.withdraw();refs.append(weakref.ref(a));a.destroy();del a;gc.collect();out.append({'cycle':k+1,'retained_roots':sum(w()is not None for w in refs)})
 roots={id(w())for w in refs if w()is not None};variables=[v for v in gc.get_objects()if isinstance(v,tk.Variable)and id(getattr(v,'_root',None))in roots];removed=0
 for v in variables:
  for modes,command in v.trace_info():v.trace_remove(modes,command);removed+=1
 del variables,v;collected=gc.collect();print(json.dumps({'destroy_cycles':out,'after_diagnostic_trace_cleanup':{'retained_roots':sum(w()is not None for w in refs),'removed_traces':removed,'collected':collected}},indent=2))
