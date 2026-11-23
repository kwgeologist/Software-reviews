from pathlib import Path
import sys,tempfile,gc,json,tkinter as tk,weakref,types
from unittest import mock
C=Path('/workspace/audit-v0.9.70-integrity/checkout');sys.path[:0]=[str(C),str(C/'tests')];import conftest
from geoworkbench.main_window import WellDataManagerApp
from ogcore import well_selection
with tempfile.TemporaryDirectory(prefix='tk-referrer-')as td,mock.patch('pathlib.Path.home',return_value=Path(td)):
 a=WellDataManagerApp();a.withdraw();wr=weakref.ref(a);a.destroy();records=[]
 for ref in gc.get_referrers(a):
  r={'type':type(ref).__name__}
  if isinstance(ref,types.MethodType):r['method']=ref.__func__.__qualname__
  if isinstance(ref,dict):r['keys_referring_to_root']=[str(k)for k,v in list(ref.items())if v is a][:10]
  if isinstance(ref,types.CellType):
   r['cell_contents_type']=type(ref.cell_contents).__name__
  records.append(r)
 variables=[v for v in gc.get_objects()if isinstance(v,tk.Variable)and v._tk is a.tk];traces=[]
 for var in variables:
  t=var.trace_info()
  if t:traces.append({'name':str(var),'traces':t})
 print(json.dumps({'root_referrers':records,'live_variable_traces_after_destroy':traces,'selection_listeners':len(well_selection._listeners),'after_after_destroy':[{'id':j,'info':a.tk.call('after','info',j),'script_command_exists':bool(a.tk.call('info','commands',str(a.tk.call('after','info',j)[0])))}for j in a.tk.call('after','info')]},indent=2))
 # No cleanup/control conclusions are inferred merely from deleting this local name.
