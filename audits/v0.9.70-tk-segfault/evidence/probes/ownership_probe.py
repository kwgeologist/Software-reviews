from pathlib import Path
import sys,os,json,gc,weakref,tempfile
from unittest import mock
C=Path('/workspace/audit-v0.9.70-integrity/checkout');sys.path[:0]=[str(C),str(C/'tests')]
import conftest
import tkinter as tk
from ogcore import well_selection,pay_sets
from geoworkbench.main_window import WellDataManagerApp
out=[];refs=[]
with tempfile.TemporaryDirectory(prefix='tk-owner-')as td,mock.patch('pathlib.Path.home',return_value=Path(td)):
 for k in range(10):
  a=WellDataManagerApp();a.withdraw();refs.append(weakref.ref(a));a.destroy();del a;gc.collect()
  out.append({'cycle':k+1,'retained_Geo_roots':sum(w()is not None for w in refs),'well_selection_listener_count':len(well_selection._listeners),'listener_owner_classes':[type(getattr(cb,'__self__',None)).__name__ for cb in well_selection._listeners]})
 # Separate diagnostic cleanup of obsolete subscriptions, not a software correction or test pass.
 for cb in list(well_selection._listeners):well_selection.unsubscribe(cb)
 del cb;collected=gc.collect();after=sum(w()is not None for w in refs)
 for wr in refs:
  app=wr()
  if app is not None:
   for modes,command in app.search_var.trace_info():app.search_var.trace_remove(modes,command)
 del app,wr;collected2=gc.collect();after2=sum(w()is not None for w in refs)
 root_ids={id(w())for w in refs if w()is not None}
 variables=[v for v in gc.get_objects()if isinstance(v,tk.Variable)and id(getattr(v,'_root',None))in root_ids]
 removed=0
 for variable in variables:
  for modes,command in variable.trace_info():variable.trace_remove(modes,command);removed+=1
 del variable,variables;collected3=gc.collect();after3=sum(w()is not None for w in refs)
 print(json.dumps({'raw_destroy_cycles':out,'after_external_listener_cleanup':{'retained_roots':after,'collected':collected},'after_external_search_trace_cleanup':{'retained_roots':after2,'collected':collected2},'after_external_all_variable_trace_cleanup':{'retained_roots':after3,'collected':collected3,'removed_trace_commands':removed},'original_shutdown_callback_not_used':True},indent=2))
