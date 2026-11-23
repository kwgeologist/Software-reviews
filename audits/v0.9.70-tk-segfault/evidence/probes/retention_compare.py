from pathlib import Path
import sys,tempfile,weakref,gc,json,os
from unittest import mock
C=Path(sys.argv[1]);sys.path[:0]=[str(C),str(C/'tests')]
import conftest,tkinter as tk
from xsection.widgets import Fields
from seismicworkbench.app import SeismicWorkbench
out={'checkout':str(C),'cases':{}}
with tempfile.TemporaryDirectory(prefix='tk-retention-')as td,mock.patch('pathlib.Path.home',return_value=Path(td)):
 for kind in ['fields','seismic']:
  refs=[];extra=[];rows=[]
  for k in range(20):
   if kind=='fields':
    r=tk.Tk();obj=Fields(r);var=obj.var('value');extra.append(weakref.ref(obj))
   else:r=SeismicWorkbench();r.withdraw()
   refs.append(weakref.ref(r));r.destroy()
   if kind=='fields':del obj,var
   del r;gc.collect();rows.append({'cycle':k+1,'retained_roots':sum(w()is not None for w in refs),'retained_Fields':sum(w()is not None for w in extra)})
  out['cases'][kind]=rows
print(json.dumps(out,indent=2))
